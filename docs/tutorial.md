# A 15-minute incident-response exercise

## Goal

Explain the difference between limiting an incident's impact and restoring data
after impact. You need Python 3.12+ and this checkout. No documents, server, keys,
network connection, or third-party runtime packages are needed.

All document labels and events in this lab are simulated. The commands below
run from the repository root; use `py -3.12` on Windows.

## 1. Establish the baseline

```sh
python3.12 -m wild_bat demo --scenario recovery --documents 5
```

Expected counts: 5 affected, 5 restored, 0 unavailable, 0 untouched. Read the
event order: availability loss occurs before detection and containment; recovery
then uses a simulated backup.

Discuss: Why does successful recovery not erase the fact that five documents
were affected? What operational disruption does this simplified model omit?

## 2. Contain earlier

```sh
python3.12 -m wild_bat demo --scenario containment --documents 5
```

Expected counts: 1 affected, 1 restored, 0 unavailable, 4 untouched. The model
places detection after the first availability change. Containment prevents the
other four changes, and a backup restores the affected document.

Discuss: Which benefit came from containment, and which came from the backup?
The model assumes immediate detection and isolation at the chosen point; what
would need to be measured before making that claim about a real environment?

## 3. Remove the backup assumption

```sh
python3.12 -m wild_bat demo --scenario no-backup --documents 5
```

Expected counts: 5 affected, 0 restored, 5 unavailable, 0 untouched. Containment
has occurred, but this model provides no recovery route without a backup.

Discuss: Why does stopping further impact not restore availability? Which backup
properties would you need to validate outside this exercise?

## 4. Inspect the evidence

```sh
python3.12 -m wild_bat demo --scenario containment --documents 5 --format json
```

Identify the `simulation` marker, the detection event, the containment event, and
the final document states. Confirm that `affected = restored + unavailable` and
`total = restored + unavailable + untouched`.

## Instructor notes

There is no cleanup step: the application keeps its modeled documents in memory.
If you explicitly saved reports with shell redirection, those reports remain.
Changing the document count changes event volume, not detection quality or timing.
With one document, both recovery and containment affect and restore that one
document; use at least two to show the benefit of early containment.

The simulator cannot validate a production backup, demonstrate actual ransomware
behavior, or measure the effectiveness of a security product. Use it to clarify
assumptions and prepare questions for authorized defensive exercises.
