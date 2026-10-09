# Architecture

Wild Bat separates a pure simulation model from a small command-line interface.
Its runtime uses only Python's standard library.

```text
CLI arguments -> validated scenario and count -> in-memory state transitions
                                             -> immutable report -> stdout
```

## Code map

| Module | Responsibility |
| --- | --- |
| `wild_bat/simulation.py` | Scenario definitions, immutable data objects, transitions, and reports. |
| `wild_bat/cli.py` | Argument validation, text formatting, JSON serialization, and stdout. |
| `wild_bat/__main__.py` | Module execution entry point. |
| `wild_bat/__init__.py` | Package identity and version. |
| `tests/` | Scenario invariants, boundary validation, CLI integration, and safety regressions. |

## State model

A document contains only a generated label and one of three states:

```text
available -> unavailable -> restored
```

An untouched document stays `available`. Without a simulated backup, an affected
document stays `unavailable`. No bytes are encrypted, transformed, deleted, or
restored. The `Document`, `Event`, and `Report` dataclasses are frozen; a simulation
builds its own working list and returns tuples. Calls share no mutable run state.

`simulate()` accepts a built-in scenario and an integer document count from 1
through 1000. It returns a report without printing. `Report.to_dict()` produces a
fresh JSON-compatible snapshot. Invalid values raise `ValueError`.

## Assumptions

- Detection is scripted after one affected document in `containment`, and after
  all documents in the other scenarios.
- Containment immediately stops additional modeled impact.
- When backups exist, they are complete, usable, and independent of the incident.
- Recovery restores every affected document when those backups are available.
- There is no elapsed-time model, real alert collection, network isolation,
  storage failure, cryptography, or endpoint-agent integration.

These assumptions make the lessons reproducible. They also mean results cannot
predict real incident duration, cost, detection coverage, or recoverability.

## Boundaries

The public interface has no path, URL, key, shell-command, or file-content input.
The simulation does not scan the filesystem, open documents, start processes,
contact services, or register startup behavior. Text and JSON renderers output
reports to stdout. Python may read package files and create normal bytecode cache
files; installation and shell redirection have their usual filesystem effects.

Tests run every scenario with common file, socket, and process operations mocked
to fail. CLI integration tests execute in a temporary directory containing a
sentinel document and check that it remains unchanged and no extra files appear.
These are regression checks, not an operating-system sandbox or a formal proof
of isolation.

The retired `HW1.py` and `server.py` contain only an explanatory exit on direct
execution and have no import-time behavior. Historical Git revisions retain the
original implementation and are outside these boundaries.
