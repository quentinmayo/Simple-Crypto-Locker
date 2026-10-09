# Legacy implementation review

This review describes the original Simple-Crypto-Locker teaching project at
commit `2741935`. It is a static review: the original programs were not executed.
The original author is Quentin Mayo. Wild Bat is the name for the modernization.

## What the original project does

The Windows/Python 2 client requests a public key from a CherryPy server, selects
documents from a directory under the user's desktop, writes encrypted copies,
and deletes their originals. It then writes a separate record containing the
file keys, protected with the server's public key. A Tkinter dialog starts a
recovery flow that requests the server's private key and attempts to restore
documents.

The server generates its RSA key pair at startup and holds it in memory. There
is no durable recovery store. Its private-key endpoint does not check payment
or authenticate the requester.

## Findings

| Finding | Evidence in the original source | Consequence |
| --- | --- | --- |
| Original documents are deleted | `HW1.py`, `pwn_documents()` | Running the client can cause real data loss. |
| Recovery metadata is saved after document processing | `HW1.py`, `main()` | A failure before the metadata write can leave files without their recovery record. |
| Server keys live only in memory | `server.py`, `MrPWN.__init__()` | Restarting the server replaces the key required by earlier sessions. |
| Unauthenticated private-key endpoint | `server.py`, `unpwn_me_please()` | Any caller that can reach the service can request the private key. |
| Listener binds to all IPv4 interfaces | `server.py`, module-level startup | Exposure depends on the host's network and firewall configuration. |
| Decrypted data is evaluated as Python | `HW1.py`, `unpwn_pwn()` | Recovery metadata is treated as executable code. |
| Trailing zero bytes are stripped on recovery | `HW1.py`, `decrypt()` | Some binary documents cannot round-trip without corruption. |
| Encryption has no authentication tag | `HW1.py`, `encrypt()` and `decrypt()` | The format provides no authenticated check that content is unchanged. |
| Requests have no timeout and retry indefinitely | `HW1.py`, `main()` and `unpwn_pwn()` | Network failures can leave the program waiting indefinitely. |
| Broad exception handlers obscure failures | `HW1.py`, recovery loop | Failed restores can be hidden while cleanup continues. |
| Startup side effects | `server.py` and `test.py` | Importing these modules starts the server or generates and prints keys. |
| Obsolete runtime assumptions | Python 2 syntax, `_winreg`, `Tkinter`, and historical Crypto APIs | This is not an installable modern Python application. |

## Historical materials

`CryptoLocker.pptx` and `README.md.pdf` are historical materials. This review did
not inspect their contents. They are not current installation or operation
instructions. Git history preserves the original source and README for static
study.

## Modernization boundaries

An educational replacement can model document availability, incident events,
containment, and recovery without touching users' documents. It should use
synthetic examples, explain its assumptions, and keep observed behavior distinct
from simulated behavior. Tests should verify those boundaries as well as the
lesson outcomes.

Upgrading the destructive document-processing flow, persistence, or remote
key-release service is outside the modernization scope. The replacement must
not claim to decrypt files created by the original project.
