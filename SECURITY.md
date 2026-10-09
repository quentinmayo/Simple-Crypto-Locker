# Security policy

Wild Bat's supported direction is security education with synthetic data.
Real document encryption, destructive file processing, startup persistence, and
remote key-release services are outside its scope.

## Historical code

The original Simple-Crypto-Locker scripts can delete documents and lose recovery
keys. Do not run historical revisions on a machine containing data you need.
See the [static legacy review](docs/legacy-review.md) for the observed behavior.
Historical slides and PDFs are not current setup instructions.

## Reporting a problem

For documentation mistakes or incorrect simulated results, open a repository
issue with the version, command, expected result, and actual result. Use only
synthetic examples; omit documents, credentials, keys, and personal information.

For a vulnerability involving unintended file access, data loss, code execution,
or unexpected network activity, use GitHub's private vulnerability reporting
option if the repository provides one. If that option is unavailable, ask the
maintainer to establish a private reporting channel before sharing sensitive
details. No dedicated private contact or response-time commitment is currently
published by this project.
