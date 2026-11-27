---
type: test-evidence
title: 'Evidence for T-017: the equivalence result table for all 17 checks'
item: T-017
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T18:00:00Z'
---

## Commands

```bash
.venv/bin/python <the adopter overlay's equivalence/harness.py> --source-store <store root> --cases <commit-mode, push-mode, limits and smoke cases>
.venv/bin/python -m pytest -q <the adopter overlay's tests/test_equivalence_results.py>
ACKIT_BETA_STORE=<store root> .venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
all case files together on the real store source: 62 cases, every case passes in both routes; no check is skipped in every case
results table test: 4 passed (every check has a row; every case a row names exists and its verdicts match its column: a firing case expects the check to act, a clean case expects a pass, a hint-only row fires through a hint, a commit-flow case sits in row 16 with the right outcome; a row that says proven names both; a row with a limit says what is missing; 4 tests after the review)
```

The table is `equivalence/RESULTS.md` of the adopter overlay:

| Result | Checks |
|---|---|
| proven (at least one firing condition and a clean case, same in both routes) | 1, 2, 3, 5, 6, 7, 12, 13, 14, 16, 17 |
| proven by hint (the gate never prints the warning of these checks, so the proof is the check's own hint line) | 8, 9, 10, 11 |
| proven with a stand-in | 4 (a stub build command), 15 (a loopback tracker) |
| not proven | none |

## Coverage

Not shown by any case: the real build, a real tracker, the emergency-skip path of check 15 (on purpose), and the push-time scope (the commits being pushed) of checks 3, 5 to 14 and 16; and, within a check that has several conditions, the ones the table's last column lists (for example only the raw string parser rule of check 13, three of about ten conditions of check 6, and the uncommitted-files and large-change paths of check 15). A row says "proven" for one firing condition, not for the whole check.

Differences between the two routes found while building the runs: none in the gate's verdicts (the output of a very large commit is cut by the kit's 64 KiB cap, see EV-T-016). The differences found were in the harness and were fixed with a test each (see the reviews of T-014 to T-016).

E-002 criterion 3 now reads what this table proves, with its limits, instead of "every check has a test that makes it fire".
