---
type: test-evidence
title: 'Evidence for T-002: id_allocation with reserved ranges'
item: T-002
result: pass
status: final
generated:
  by: plane-session/agent
  at: '2026-11-20T13:40:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q tests/test_acf13_ids.py
.venv/bin/ackit validate docs --strict
.venv/bin/python -m pytest -q tests/test_examples.py     # leakage test
```

## Results

```
168 passed, 2 skipped in 63.84s
76 documents: 0 error(s), 0 warning(s)
tests/test_examples.py: 4 passed
```

The T-001 guard (`tests/test_guard_baseline.py`) passed unchanged on the ten old-style bundles after the code change, so bundles without the new key validate as under 1.2. Four existing assertions changed because the version moved on purpose: `acf_version` of new and imported bundles is `"1.3"` (`tests/test_okf_compat.py` two places, `tests/test_acf12.py` one place) and `ackit.__version__ == "1.3.0"`; `test_every_rule_has_a_case` gained ACF037.

Proof P2 (`test_p2_two_writers_in_parallel`): two clones of one bundle, each author creating ten tasks one after another in a real `python -m ackit new` subprocess, the two authors at the same time, then the union of the files (a merge of two branches that each added files) in both orders. With `reserved-range` (alice 1000 to 1999, bob 2000 to 2999) ACF009 reports no duplicate in either merge. With `sequential` allocation the same procedure reports duplicate ids in both merges. Both parametrisations pass.

## Coverage

Added at the developer's request (ADR-0020): `ackit ids assign` (block and one-line `ranges` styles, first range, `--size`, comments and other keys kept, refusals write nothing, CLI note when the strategy is still sequential; tests in `tests/test_acf13_ids.py`, 17 tests in that file). Covered: sequential unchanged without the key; range allocation inside the range, continuing after the highest id and ignoring ids outside it, including the width-4 `ADR-` prefix; refusal for no author, unknown author and full range (exit 2 with a message); `--author` and `$ACKIT_AUTHOR`; six bad configurations reported by ACF037 and a good one quiet; ACF009 unchanged. Not covered: concurrent writers inside one clone (the same author running two `ackit new` at once can still race, as before; out of scope of ADR-0018); a real `git merge` (the test merges by union of files, which is what git does for added files with different names; same-named files cannot occur because file names start with the id); an author without a range is refused, whereas ADR-0018 "Consequences" describes a sequential fallback (see ADR-0020, which restates the decision). `ackit import` still allocates its own ids from the source and is unchanged.

## After the independent review

Fixes for the review (`docs/reviews/REV-T-002-id-allocation.md`): invalid configuration refuses allocation, `ids assign` is scoped to the `id_allocation` block and keeps CRLF, refuses a missing `ackit.yaml` and ambiguous author names. Re-run: `191 passed, 2 skipped in 65.10s`; `77 documents: 0 error(s), 0 warning(s)`.
