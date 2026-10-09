"""Command-line interface; reports go to stdout, diagnostics to stderr."""

import argparse
import json

from . import __version__
from .simulation import MAX_DOCUMENTS, SCENARIO_DESCRIPTIONS, Report, Scenario, simulate


def document_count(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("documents must be an integer") from exc
    if not 1 <= number <= MAX_DOCUMENTS:
        raise argparse.ArgumentTypeError(f"documents must be between 1 and {MAX_DOCUMENTS}")
    return number


def render_text(report: Report) -> str:
    lines = [
        f"Wild Bat {__version__} | {report.scenario.value}",
        "SIMULATION ONLY: synthetic labels, no file encryption or document access.",
        "",
    ]
    for event in report.events:
        subject = f" [{event.document}]" if event.document else ""
        lines.append(f"{event.step:02d}. {event.kind}{subject}: {event.message}")
    lines.extend(["", "Result: " + ", ".join(f"{key}={value}" for key, value in report.summary.items())])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="wild-bat",
        description="Explore incident containment and recovery with synthetic data in memory.",
    )
    parser.add_argument("--version", action="version", version=f"Wild Bat {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("scenarios", help="list built-in exercises")
    demo = commands.add_parser("demo", help="run an in-memory exercise")
    demo.add_argument("--scenario", choices=[s.value for s in Scenario], default="recovery")
    demo.add_argument("--documents", type=document_count, default=3, metavar="N",
                      help=f"synthetic document count, 1–{MAX_DOCUMENTS} (default: 3)")
    demo.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    if args.command == "scenarios":
        for scenario, description in SCENARIO_DESCRIPTIONS.items():
            print(f"{scenario.value:12} {description}")
        return 0

    report = simulate(args.scenario, args.documents)
    print(json.dumps(report.to_dict(), indent=2) if args.format == "json" else render_text(report))
    return 0
