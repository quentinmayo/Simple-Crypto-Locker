"""A deterministic state model, not an encryption or filesystem engine."""

from dataclasses import asdict, dataclass, replace
from enum import Enum

from . import __version__

MAX_DOCUMENTS = 1000


class Scenario(str, Enum):
    RECOVERY = "recovery"
    CONTAINMENT = "containment"
    NO_BACKUP = "no-backup"


SCENARIO_DESCRIPTIONS = {
    Scenario.RECOVERY: "Late detection; all documents restored from simulated backups.",
    Scenario.CONTAINMENT: "Detection after one document; contain, then restore it.",
    Scenario.NO_BACKUP: "Late detection with no backups; documents remain unavailable.",
}


class State(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    RESTORED = "restored"


@dataclass(frozen=True)
class Document:
    """A label and availability state; never a path or real document content."""

    name: str
    state: State = State.AVAILABLE


@dataclass(frozen=True)
class Event:
    step: int
    kind: str
    document: str | None
    message: str


@dataclass(frozen=True)
class Report:
    scenario: Scenario
    documents: tuple[Document, ...]
    events: tuple[Event, ...]

    @property
    def summary(self) -> dict[str, int]:
        return {
            "total": len(self.documents),
            "affected": sum(e.kind == "unavailable" for e in self.events),
            "restored": sum(d.state == State.RESTORED for d in self.documents),
            "unavailable": sum(d.state == State.UNAVAILABLE for d in self.documents),
            "untouched": sum(d.state == State.AVAILABLE for d in self.documents),
        }

    def to_dict(self) -> dict:
        """Return a new JSON-compatible snapshot with a versioned schema."""
        return {
            "schema_version": 1,
            "version": __version__,
            "simulation": True,
            "scenario": self.scenario.value,
            "summary": self.summary,
            "documents": [asdict(d) for d in self.documents],
            "events": [asdict(e) for e in self.events],
        }


def simulate(scenario: Scenario | str = Scenario.RECOVERY, documents: int = 3) -> Report:
    """Model one built-in exercise using generated labels entirely in memory.

    No file paths, document contents, keys, URLs, or executable inputs are accepted.
    Availability changes are symbolic. Restoring a document changes only its state.
    """
    scenario = Scenario(scenario)
    if type(documents) is not int or not 1 <= documents <= MAX_DOCUMENTS:
        raise ValueError(f"documents must be an integer between 1 and {MAX_DOCUMENTS}")

    items = [Document(f"sample-{n:04d}.txt") for n in range(1, documents + 1)]
    events: list[Event] = []

    def record(kind: str, message: str, name: str | None = None) -> None:
        events.append(Event(len(events) + 1, kind, name, message))

    record("prepared", f"Created {documents} synthetic document labels in memory.")
    has_backups = scenario != Scenario.NO_BACKUP
    record("backup", "Simulated backups available." if has_backups else "No simulated backups.")

    affected = 1 if scenario == Scenario.CONTAINMENT else documents
    for index in range(affected):
        items[index] = replace(items[index], state=State.UNAVAILABLE)
        record("unavailable", "Marked unavailable; no encryption performed.", items[index].name)

    record("detected", f"Simulated alert after {affected} document(s) became unavailable.")
    record("contained", f"Simulated containment; {documents - affected} document(s) untouched.")

    if has_backups:
        for index in range(affected):
            items[index] = replace(items[index], state=State.RESTORED)
            record("restored", "Restored availability from a simulated backup.", items[index].name)
    else:
        record("recovery-unavailable", "No backup exists in this model; affected documents stay unavailable.")

    record("completed", "Exercise complete. All document states existed only in memory.")
    return Report(scenario, tuple(items), tuple(events))
