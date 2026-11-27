---
type: review
title: 'Review of T-017: the equivalence result table'
item: T-017
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T19:00:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-23, of the result table, its test, the evidence, the epic's criterion 3 row, the journal entry and the checks' real source. The reviewer was asked whether each named case really makes its check act or stay clean, whether the "not shown" columns are complete and true, whether the counts are right, whether the test would catch a wrong table, and whether the journal is accurate.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | major | The push-time scope was admitted for 3, 5, 6, 7, 13, 14 and 16 only; checks 8 to 12 also change scope at push | Added to rows 8 to 12; the table, the evidence, the epic row and the journal now say checks 3, 5 to 14 and 16 |
| 2 | major | Row 13 overstated: only the raw string parser rule is exercised | The row lists the blocking rules, the escape hatch and the warning rules that no case exercises |
| 3 | major | Row 6 overstated: three of about ten conditions | The row lists the conditions not shown |
| 4 | minor | Rows 1, 2, 14, 15 and 8 to 11 left their other conditions unsaid | Each row's last column lists them; "proven" is defined as one firing condition and a clean case |
| 5 | minor | The test passed a case in a column it did not belong in, and treated commit-flow cases as matching any row | The test checks verdicts against the column, commit-flow cases to row 16 and their outcome, and hint-only rows to hint verdicts; a negative-control test |
| 6 | nit | "No difference in verdicts" ignored the output cap | Wording now mentions the 64 KiB cap |

## Resolution

All findings fixed; the reviewer confirmed the counts (62 cases; 11 proven, 4 by hint, 2 with a stand-in), that every named case's expected text exists in the gate's source, and that the by-hint claim is sound.

## Verdict

approve. The table claims one firing condition per check, says so, and lists what is not exercised.
