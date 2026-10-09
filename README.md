# Wild Bat

**A small, offline incident-response lab for learning how containment and backups
change an incident's outcome.**

Wild Bat is the educational successor to Quentin Mayo's Simple-Crypto-Locker
project. Version 0.1.0 replaces the original Python 2 client and key server with
an installable Python CLI, deterministic scenarios, structured reports, and tests.

Every “document” is a generated label and an availability state in memory. The
simulator does not open documents, encrypt data, contact a server, or delete files.
It is a teaching model, not a cryptography tool, malware sample, or recovery utility.

## Quick start

Requires **Python 3.12 or later**. There are no third-party runtime dependencies.
From this repository's root, run:

```sh
python3.12 -m wild_bat demo
python3.12 -m wild_bat demo --scenario containment
python3.12 -m wild_bat demo --scenario no-backup
```

On Windows, use `py -3.12` in place of `python3.12`. You can also use an installed
Python 3.13 or 3.14 interpreter. Running from source needs no package installation
or network access.

The default exercise ends with:

```text
Result: total=3, affected=3, restored=3, unavailable=0, untouched=0
```

## Install the command

macOS / Linux:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
wild-bat scenarios
wild-bat demo --scenario containment --documents 5
```

Windows PowerShell, without requiring an activation script:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\wild-bat.exe demo --scenario containment --documents 5
```

Installation may download the setuptools build dependency. The application itself
runs offline. The distribution is installed from this checkout; these instructions
do not imply that a package has been published on PyPI.

## Compare the exercises

| Scenario | Detection | Backup assumption | Result with 3 documents |
| --- | --- | --- | --- |
| `recovery` | After all documents are affected | Usable backups exist | 3 restored |
| `containment` | After the first document is affected | Usable backups exist | 1 restored, 2 untouched |
| `no-backup` | After all documents are affected | No backup exists | 3 remain unavailable |

These outcomes follow explicit model assumptions; they are not measurements of
real detection products or proof that a production recovery plan will succeed.

## Reports and tests

```sh
python3.12 -m wild_bat demo --scenario containment --format json
python3.12 -m unittest discover -s tests -v
```

Reports go to standard output. JSON includes a simulation marker, schema version,
ordered events, document states, and summary counts. See the [CLI reference](docs/cli.md).

## Documentation

- [Guided exercise](docs/tutorial.md): a short lab with questions and expected outcomes.
- [CLI reference](docs/cli.md): commands, arguments, JSON schema, and exit codes.
- [Architecture](docs/architecture.md): state transitions, model assumptions, and boundaries.
- [Migration guide](docs/migration.md): what changed from the original project.
- [Legacy review](docs/legacy-review.md): a static analysis of the original implementation.
- [Contributing](CONTRIBUTING.md): local setup and change requirements.
- [Security policy](SECURITY.md): scope and reporting guidance.
- [Changelog](CHANGELOG.md): release changes.

## Project status

This is an initial educational release. `HW1.py` and `server.py` are retired stubs
that exit without starting the original programs. `test.py` now runs the test
suite. The original code remains in Git history; `CryptoLocker.pptx` and
`README.md.pdf` remain historical artifacts, not current instructions.

Wild Bat cannot decrypt `.enc` files from historical versions. No license file is
currently declared in this repository; license selection remains a maintainer
release decision.
