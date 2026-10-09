import json
import unittest
from contextlib import ExitStack
from dataclasses import FrozenInstanceError
from unittest.mock import patch

from wild_bat.simulation import MAX_DOCUMENTS, Scenario, State, simulate


class SimulationTests(unittest.TestCase):
    def test_recovery_restores_every_affected_document(self):
        report = simulate("recovery", 5)
        self.assertEqual(report.summary, dict(total=5, affected=5, restored=5, unavailable=0, untouched=0))
        self.assertTrue(all(d.state == State.RESTORED for d in report.documents))

    def test_containment_limits_impact_and_restores_one_document(self):
        report = simulate("containment", 5)
        self.assertEqual(report.summary, dict(total=5, affected=1, restored=1, unavailable=0, untouched=4))

    def test_no_backup_cannot_claim_recovery(self):
        report = simulate("no-backup", 5)
        self.assertEqual(report.summary, dict(total=5, affected=5, restored=0, unavailable=5, untouched=0))
        self.assertFalse(any(e.kind == "restored" for e in report.events))

    def test_detection_precedes_containment_and_recovery(self):
        for scenario in Scenario:
            with self.subTest(scenario=scenario):
                kinds = [e.kind for e in simulate(scenario).events]
                self.assertLess(kinds.index("detected"), kinds.index("contained"))
                recovery = "recovery-unavailable" if scenario == Scenario.NO_BACKUP else "restored"
                self.assertLess(kinds.index("contained"), kinds.index(recovery))
                self.assertEqual(kinds[-1], "completed")

    def test_counts_and_event_sequences_at_boundaries(self):
        for scenario in Scenario:
            for count in (1, MAX_DOCUMENTS):
                with self.subTest(scenario=scenario, count=count):
                    report = simulate(scenario, count)
                    totals = report.summary
                    self.assertEqual(totals["restored"] + totals["unavailable"] + totals["untouched"], count)
                    self.assertEqual(totals["affected"], totals["restored"] + totals["unavailable"])
                    self.assertEqual([e.step for e in report.events], list(range(1, len(report.events) + 1)))
                    self.assertEqual(len({d.name for d in report.documents}), count)

    def test_invalid_document_counts_are_rejected(self):
        for count in (0, -1, MAX_DOCUMENTS + 1, True, 1.5, "3", None):
            with self.subTest(count=count), self.assertRaises(ValueError):
                simulate(documents=count)

    def test_unknown_scenario_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate("unknown")

    def test_reports_are_deterministic_and_independent(self):
        first = simulate()
        snapshot = first.to_dict()
        snapshot["documents"][0]["name"] = "changed"
        simulate("no-backup")
        self.assertEqual(first, simulate())
        self.assertNotEqual(first.documents[0].name, "changed")
        with self.assertRaises(FrozenInstanceError):
            first.documents[0].state = State.UNAVAILABLE

    def test_json_schema_marks_results_as_simulated(self):
        snapshot = json.loads(json.dumps(simulate().to_dict()))
        self.assertEqual(snapshot["schema_version"], 1)
        self.assertIs(snapshot["simulation"], True)
        self.assertEqual(snapshot["documents"][0]["state"], "restored")

    def test_all_scenarios_work_with_file_network_and_process_access_blocked(self):
        targets = ("builtins.open", "io.open", "os.scandir", "os.remove", "os.replace",
                   "socket.socket", "subprocess.Popen")
        with ExitStack() as stack:
            for target in targets:
                stack.enter_context(patch(target, side_effect=AssertionError(f"Unexpected access: {target}")))
            for scenario in Scenario:
                self.assertEqual(simulate(scenario).summary["total"], 3)


if __name__ == "__main__":
    unittest.main()
