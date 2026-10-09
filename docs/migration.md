# Moving from Simple-Crypto-Locker to Wild Bat

Version 0.1.0 intentionally changes the project's purpose to a synthetic,
in-memory educational lab. It is not a compatible upgrade of the original
encryption client or server.

| Original component | Current behavior |
| --- | --- |
| `HW1.py` | Retired stub; prints an explanation and exits with status 1. |
| `server.py` | Retired stub; no server or network listener is started. |
| `config.js` | Removed; the simulator needs no server URLs or target extensions. |
| `test.py` | Runs the actual regression test suite. |
| Python 2 / Windows APIs | Python 3.12+ and standard-library runtime. |
| Crypto, requests, CherryPy, Tkinter | No longer used by the application. |
| Desktop document selection and encryption | Generated document labels and symbolic availability states. |
| Remote key release and recovery | Scripted recovery from a simulated backup. |
| Original README | Replaced with current installation, usage, and documentation links. |
| PDF and slide deck | Retained as historical artifacts; not current operating instructions. |

## Start fresh

Use a new virtual environment and the instructions in the [README](../README.md).
There is no server to start and no old configuration to migrate. Do not copy
personal documents, legacy `.enc` files, or keys into this project for a demo.

## Existing encrypted files

Wild Bat does not read or decrypt legacy `.enc` files, import recovery metadata,
or preserve a running historical server's keys. A code update is not a recovery
procedure. Preserve existing evidence and key material; do not treat the new CLI
as a way to recover historical data.

## Historical study

The [legacy review](legacy-review.md) describes the original source at commit
`2741935`. Git history retains it for static review. Current safety properties
apply only to the replacement implementation, not to historical revisions or
instructions embedded in the retained artifacts.
