---
type: review
title: 'Review of T-013: ownership table and overlay configuration'
item: T-013
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T11:50:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-23, of the T-013 changes: the adopter overlay's checks table, `store-config.yaml`, the adoption-PR draft and its test, `verify_doc` and `ackit verify --signoff`, SPEC, CHANGELOG, and the evidence record. The agent ran the focused tests, the whole-bundle validation and the leakage test.

## Findings

| # | File | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | task text, design | minor | The key is `severity`, not `severities`; a key spelled `severities` is silently ignored | Task text corrected; the signed design is not edited, the correction is in the F-003 journal |
| 2 | `scaffold.py` | major or minor | `--status signed-off` let a non-person write `signoff`, so "agents cannot sign off" was not true | Both routes now refuse any actor that is not `human:<id>`; tested |
| 3 | `scaffold.py` | minor | An empty `human:` id passed; `--signoff` overwrote an existing sign-off; help and SPEC said "task only" | Empty id refused, existing sign-off kept, wording corrected; tested |
| 4 | adoption-PR draft | minor | "352 lines against a 150 target" was not supported by a readable file (the entry file reads 324 lines) | Reworded to what the gate and the kit default say (300 and 150) |
| 5 | overlay test | nit | The test appended duplicate YAML keys and removed the overlay with a string replace | Rewritten to update and dump the config |
| 6 | validator | minor | A severity value other than error, warn or off is stored as written and neither counts nor fails | Recorded in the journal as a small gap; not fixed in this task |
| 7 | checks table | nit | Rows 16 and 17 omit "until a second adopter wants them" | Left: the note lives in the design; the table states owners |

## Resolution

All acceptance criteria of T-013 were confirmed by the reviewer (table with two owner columns, overlay severity and budget, adoption-PR draft as a document, test counts). Findings 1 to 5 fixed and verified; 6 recorded; 7 left on purpose.

## Verdict

approve. Ownership is stated once per check, the overlay makes the kit agree with the gate on the entry-file size, and the sign-off command is now person-only on both routes.
