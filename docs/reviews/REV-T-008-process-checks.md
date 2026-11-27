---
type: review
title: 'Review of T-008: process checks'
item: T-008
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T18:40:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-20, of `src/ackit/checks.py`, `ackit checks run`, ACF041, the tests, SPEC, the changelog and the evidence. The reviewer ran the check tests and confirmed `shell=False` and that the core ships no check.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | `cli.py` | major | `--name` with another `--when` ran nothing and exited 0 | Exit 2 with the right `--when`; tested |
| 2 | tests, evidence | major | The P4 proof was a weak socket patch described as a proof | Wider tripwire (connect, lookup, Popen), exact exit code, a static no-network-import test; evidence and SPEC reworded |
| 3 | `checks.py` | minor | A timeout left grandchildren running | Own process group, group kill; tested |
| 4 | `checks.py` | minor | Non-UTF-8 output was reported as "could not run" | Decoded with replacement; tested |
| 5 | `checks.py` | minor | Output unbounded | Last 64 KiB kept; documented |
| 6 | `checks.py` | minor | The full environment goes to the child | Accepted and documented in SPEC |
| 7 | `checks.py` | minor | Standard input inherited | `/dev/null`; tested |
| 8 | `checks.py` | minor | Message stripping removed characters of the child's text | Built conditionally; tested |
| 9 | `checks.py` | minor | Timeout message said "number" | Says whole number; tested |
| 10 | tests | minor | Several paths untested | Most added; the output cap, relative executable lookup and Windows are listed as not covered |
| 11 | evidence | minor | Counts not re-verified | Updated |
| 12 | ADR-0016 | minor | Names orchestly and AX | Accepted: product names, not company, customer or person names |

## Resolution

Findings 1 to 9 and 11 fixed and verified (20 check tests pass); 10 partly and 6 and 12 accepted for the reasons above.

## Verdict

approve.
