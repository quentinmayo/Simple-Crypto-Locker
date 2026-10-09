# CLI reference

Use `wild-bat` after installation, or `python3.12 -m wild_bat` from the repository
root. Both interfaces accept the same arguments.

```sh
wild-bat --help
wild-bat --version
wild-bat scenarios
wild-bat demo --help
wild-bat demo --scenario recovery --documents 3 --format text
```

## Commands

`scenarios` lists the three built-in scenarios and their assumptions.

`demo` generates synthetic document labels, simulates availability changes,
and prints a report. It accepts no input paths or document contents.

| Argument | Values | Default |
| --- | --- | --- |
| `--scenario` | `recovery`, `containment`, `no-backup` | `recovery` |
| `--documents` | Integer from 1 through 1000 | `3` |
| `--format` | `text`, `json` | `text` |

Running without a command prints usage and exits with status 2. `--version` is a
top-level option: use `wild-bat --version`.

## JSON report

```sh
wild-bat demo --scenario containment --documents 3 --format json
```

The output is a single JSON object with these fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Report contract version; currently integer `1`. |
| `version` | Application version, currently `0.1.0`. |
| `simulation` | Always `true` for this application. |
| `scenario` | The chosen scenario name. |
| `summary` | Counts described below. |
| `documents` | Objects containing `name` and final `state`. Names are labels, not paths. |
| `events` | Objects containing `step`, `kind`, `document`, and `message`. |

`step` is a one-based ordering number, not a timestamp. `document` is a generated
label or `null` for exercise-wide events. Event kinds are `prepared`, `backup`,
`unavailable`, `detected`, `contained`, `restored`, `recovery-unavailable`, and
`completed`. Not every scenario emits every kind. Messages are explanatory prose;
consumers should use the structured fields instead of parsing messages.

For the command above, `summary` is:

```json
{
  "total": 3,
  "affected": 1,
  "restored": 1,
  "unavailable": 0,
  "untouched": 2
}
```

`affected` counts documents that became unavailable at any point. `restored` and
`unavailable` divide that group by their final state. `untouched` counts documents
that remained `available` throughout the exercise. Therefore:

```text
affected = restored + unavailable
total = restored + unavailable + untouched
```

Reports are deterministic for the same scenario and document count. There are no
real cryptographic keys, ciphertext, file contents, or machine identifiers.

## Output and exit codes

Successful reports use stdout; argument errors use stderr. A completed exercise
returns `0`, including `no-backup`: the command succeeded even though its modeled
recovery failed. Usage errors return `2`. Retired legacy scripts return `1`.

To save a report, use your shell's output redirection to a new filename:

```sh
wild-bat demo --format json > exercise-report.json
```

The shell creates or overwrites that report file. The application has no output
path option and does not write reports directly.
