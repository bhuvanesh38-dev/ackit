---
type: review
title: 'Review of T-021: documentation and format 1.4'
item: T-021
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-24T11:15:00Z'
---

## Scope

An independent read-only review by a separate agent of the diff against the code: every SPEC claim about the three types, vocabularies, the enum changes and the support role; the CHANGELOG entry; every remaining "1.3" as a current version.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | major | SPEC and CHANGELOG called `vocabularies` a list; the code requires a mapping of name to source | Both say a mapping of name to a source |
| 2 | major | "A 1.0 to 1.3 bundle validates as before" overclaimed: ACF045 adds a warning and the three type names gain checks | The CHANGELOG header and the SPEC versioning sentence name both exceptions |
| 3 | minor | The 1.1 backward-compatibility test replaced `"1.3"` in an index now written as `"1.4"`, so it checked nothing | It replaces `"1.4"` and asserts the change happened |
| 4 | minor | Stale current-version text in the package description, INTEROP field map and the repo's own `docs/index.md` | All three say 1.4 |
| 5 | nit | A stray blank line in the CHANGELOG | Removed |

## Resolution

All findings fixed. The reviewer confirmed against the code: `dir: ""` on the three types, the enum 1 to 6, the type-strict enum check, no default for a numeric enum, the `vocab` and `vocabularies` behaviour, ACF043/044/045 severities, the support role, and that remaining "1.3" mentions are historical.

## Verdict

approve.
