# Changelog

## 0.1.0 — Unreleased

- Introduce Wild Bat, a Python 3.12+ educational incident and recovery simulator.
- Add deterministic recovery, containment, and no-backup scenarios.
- Add CLI validation, text reports, and a versioned JSON report format.
- Add package metadata and the `wild-bat` console command.
- Add regression tests and a cross-platform CI matrix.
- Replace the README and add a tutorial, CLI reference, architecture description,
  migration guide, static legacy review, contribution guide, and security policy.
- Retire the destructive Python 2 client and key server; replace their entry
  points with explanatory stubs and remove their configuration.
- Preserve the historical PDF and slide deck as reference artifacts.

This is a breaking change in purpose and interface. Legacy encrypted files and
server keys are not supported by the new application.
