# Contributing to Wild Bat

The project teaches incident containment and recovery using synthetic state in
memory. Contributions should strengthen that educational purpose.

## Development setup

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

On Windows, create the environment with `py -3.12 -m venv .venv` and invoke
`.\.venv\Scripts\python.exe` directly for pip and unittest commands.

The test suite uses `unittest`; no test framework installation is required.
Source-only development also works without installation via `python3.12 -m wild_bat`.

## Change requirements

- Keep the simulator independent of real document contents, file paths, network
  services, cryptography, process execution, and startup registration.
- Document each scenario's assumptions and expected outcome.
- Test meaningful state invariants and failure behavior when code changes.
- Keep JSON schema changes explicit; changing an existing field's meaning or
  type requires a schema-version decision and updated reference documentation.
- Update the changelog and relevant guides when behavior changes.
- Keep version metadata in `pyproject.toml` and `wild_bat/__init__.py` consistent.

Do not reintroduce the legacy destructive client or remote key service. Static
historical analysis belongs in the documentation. Report security issues using
[SECURITY.md](SECURITY.md).

## Validation and release

CI is configured to run tests on Linux, macOS, and Windows with Python 3.12, 3.13,
and 3.14, install the package, and smoke-test the command. Local runs do not prove
that every matrix job passes; inspect the actual GitHub Actions results after
publishing a branch.

Before a public package release, the maintainer must select a license, review the
documentation, verify CI, and decide the distribution channel. The repository
does not currently automate package publication.
