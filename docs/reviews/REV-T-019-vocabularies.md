---
type: review
title: 'Review of T-019: vocabularies and rules ACF043 and ACF044'
item: T-019
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-24T09:00:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-24, of the vocabulary loader, the two rules, the binding on `ticket-resolution`, the tests and the evidence. The reviewer probed the loader directly with odd inputs, compared the file reading with the environment registry's, and checked how the rules interact with `severity`, scoped validation and the gate.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | major | A source with mixed or non-string keys crashed with an exception instead of giving ACF044 | The keys are converted to text for the message; tests for those shapes |
| 2 | minor | A vocabulary that had a problem was still registered, so every bound value also fired ACF043 | A vocabulary with a problem is not used; tested |
| 3 | minor | `of_type` gave a misleading "no values" when the type has no `id` | The message says no document of that type with an `id` was found |
| 4 | minor | The binding surviving a `types:` override was untested | Tests: kept by an override, switched off by `vocab: {}` |
| 5 | minor | A malformed or unmatched binding is silent | Documented as intended in the module text and the evidence |
| 6 | nit | `key_path` is a plain dotted path; `values` accepted mappings | Documented; `values` now accepts plain strings only |
| 7 | nit | Several ACF044 paths were untested | 12 more cases (28 faults in all) |

## Resolution

All findings fixed except the silent binding, which the design chose. The reviewer found nothing unsafe: reading a source file follows the same precedent as the environment registry, nothing is written or run, special files are refused, and existing bundles are unchanged (the guard test passes).

## Verdict

approve.
