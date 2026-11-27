---
type: review
title: 'Review of T-007: author workspace'
item: T-007
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T17:30:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-20, of `src/ackit/workspace.py`, ACF036 and ACF040, the index and ACF024 changes, the tests, SPEC, the changelog and the evidence. The reviewer ran the workspace tests.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | SPEC, tests | major | "Append-only rules still apply" was untested, and the kit has only journal and session format rules | Wording says ACF020 and ACF021; a workspace journal test fires ACF020 |
| 2 | task, evidence | major | The expectation was not in the task; the Touches line was wrong | Recorded in the task body; Touches corrected |
| 3 | evidence | major | W3 was a no-frontmatter smoke test presented as more | Evidence says so and states what it proves |
| 4 | `validate.py` | minor | ACF036 fired on unparsable and untyped files | Skipped; tested |
| 5 | `validate.py` | minor | A non-string author was coerced | Must be a string; tested |
| 6 | `workspace.py` | minor | Roots like `./{author}` or `{author}` did nothing or hid everything | Refused; tested |
| 7 | `workspace.py` | minor | A non-mapping `ackit.yaml` crashed `config` | Guarded; tested |
| 8 | `validate.py` | minor | Config evaluated per document | Evaluated once |
| 9 | task, plan | minor | Size-budget wording | Task wording corrected |
| 10 | `workspace.py` | minor | Backslash in a root | Refused |

## Resolution

All ten fixed and verified (22 workspace tests pass). Remaining untested: Windows separators in `rel` and a real `ackit index --write` round trip, accepted: both go through the same helper.

## Verdict

approve.
