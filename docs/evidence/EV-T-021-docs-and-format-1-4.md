---
type: test-evidence
title: 'Evidence for T-021: documentation and format 1.4'
item: T-021
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-24T11:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q tests/test_acf12.py tests/test_okf_compat.py tests/test_guard_baseline.py
.venv/bin/ackit validate docs --strict
```

## Results

```
full suite: 470 passed, 7 skipped (before the review fixes)
after the review fixes: the three files above, 52 passed, 1 skipped
ackit validate docs --strict: 153 documents, 0 errors, 0 warnings
```

`ACF_VERSION` is 1.4 and the package is 1.4.0 (`__init__.py`, `pyproject.toml`); the version test and the import test expect them. The guard test is unchanged and passes. SPEC describes the three types, `vocabularies` and `vocab`, the `support` role, the version sentence and the ACF014 row; the CHANGELOG has a 1.4.0 entry.

## Coverage

No code behaviour changed in this task. Whether the SPEC text matches the code was checked by the independent review (see REV-T-021). The 1.1 backward-compatibility test now asserts that its version replacement happened; before, it matched nothing once new bundles were written as 1.4.
