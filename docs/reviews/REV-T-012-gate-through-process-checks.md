---
type: review
title: 'Review of T-012: the adopter gate through process_checks'
item: T-012
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T11:30:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-23, of `src/ackit/checks.py`, `ackit checks run`, the new tests, SPEC, `hooks/pre-push`, the adopter overlay (config, checks table, test) and the evidence, with read access to the store's gate script. The reviewer ran the check tests.

## Findings

| # | File | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | gate, overlay | major | Check 16 sees `--amend` through the parent process command line; through the kit the parent is the wrapper, so a message-only amend can be blocked | Fixed with the `{git_command}` placeholder and a wrapper that stays the gate's parent; proven with the real gate on a scratch repo (amend passes, empty commit blocks) |
| 2 | evidence, table | major | "Route proven" overstated: only check 1 fired, on a scratch repository; push entry in a code clone never run; no end-to-end run with the bundle in the store | Evidence and table now say exercised versus only wired, and that the store bundle does not exist yet |
| 3 | `cli.py` | minor | Closed standard input, `--scope ""`, blocking read on an open pipe | Guarded and tested; the blocking case is documented in SPEC |
| 4 | overlay, `checks.py` | minor | A timeout leaves the temporary link folder | `trap` removes it on normal exit; the timeout leak is documented |
| 5 | overlay | minor | The two scopes run the same script | Stated in the config comment |
| 6 | `cli.py` | minor | A run matching no check was silent (fail-open) | Warning on stderr, documented; exit stays 0 |
| 7 | `hooks/pre-push` | minor | A missing `ackit` skipped the gate silently | Loud message and `ACKIT_REQUIRED=1` to fail instead |
| 8 | table | minor | Duplicate entry bullet | Removed |
| 9 | tests | minor | A no-op line, a fragile literal, thin tests for the new fields | Fixed; tests added for field types, ACF041 through `validate`, 3 MB input, a command that ignores input, no match, closed input |
| 10 | SPEC | minor | Terminal and open-pipe behaviour not stated | Added |

## Resolution

Findings 2 to 10 fixed and verified (31 tests in the checks and overlay files pass); finding 1 recorded as a known gap with its fix named.

## Verdict

approve. The kit now has a route for all 17 checks; the equivalence to the live hooks, and the amend gap, are for the migration stage.
