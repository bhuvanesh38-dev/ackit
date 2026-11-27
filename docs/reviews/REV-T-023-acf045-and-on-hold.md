---
type: review
title: 'Review of T-023: ACF045 and the on-hold status block'
item: T-023
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T21:30:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-23, of the rule, its regular expression, the tests, the SPEC, ADOPTION and CHANGELOG text, and the on-hold block. The reviewer ran the new tests, the guard test and `ackit validate docs --strict`, tried adversarial headings against the expression, and compared the three copies of the on-hold block.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | minor | The changelog said a bundle validates as before except for the new warning, without saying that `--strict` fails on a warning | CHANGELOG and SPEC say so and name `severity: {ACF045: off}` |
| 2 | minor | The guard baseline holds no session entry, so it cannot show how ACF045 interacts with ACF021; no test for a session in an author workspace folder | Tests for ACF021 unchanged on a valid old-style heading, for a workspace session, and for `off`; the evidence says what the baseline contains |
| 3 | nit | A branch with a space, `NONE` and week 00 were untested; day names are English only | Added to the test lists; the SPEC states the English names and W01 to W53 |
| 4 | nit | The evidence counted 142 documents | Corrected |

## Resolution

All findings fixed. The reviewer found no catastrophic backtracking, confirmed ACF021 is untouched, that a non-date heading still gives ACF021 only, that the three copies of the on-hold block agree, and that the transition test really writes the history it names. The kit's own first session entry needed `@ none` instead of `@ initial`, which shows the new warning does reach real bundles.

## Verdict

approve. The rule is additive, off by one setting, and a warning by default.
