---
type: review
title: 'Review of T-009: consumer layout'
item: T-009
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T19:30:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-20, of `src/ackit/layout.py`, `ackit link --check`, ACF042, the tests, SPEC, the changelog and the evidence. The reviewer ran the layout tests and confirmed that `--check` creates and changes nothing.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | `layout.py` | major | The entry source was checked even with no links configured, so a bundle without an entry file failed with no block at all | Nothing is checked when no link is configured; tested both ways |
| 2 | evidence | minor | Dangling-link sentence garbled; relative and chained links untested | Tests added; evidence rewritten |
| 3 | `layout.py` | minor | A missing source produced one row with a bundle path | One `missing` row per link |
| 4 | `cli.py` | minor | Default target inside the bundle gave a confusing result | Exit 2 with a message when the target is the bundle |
| 5 | `cli.py`, SPEC | minor | `--check` is mandatory and not explained | SPEC says `ackit link` alone is refused |
| 6 | `layout.py` | minor | OSError and symlink loops could traceback | Reported as `wrong`; loop tested |
| 7 | `layout.py` | minor | Duplicate or nested link paths accepted | Refused by ACF042; tested |
| 8 | `cli.py` | minor | A missing bundle gave a traceback; errors with `--json` go to stderr | Exit 2; behaviour stated in SPEC |
| 9 | tests | minor | Several paths untested | Most added; the rest listed as not covered |

## Resolution

All nine fixed or stated; 18 layout tests pass.

## Verdict

approve.
