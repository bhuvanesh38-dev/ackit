---
type: test-evidence
title: 'Evidence for I-003 items 19 and 20: wrap-up part, role path, findings format'
status: final
item: I-003
result: pass
generated:
  by: ackit/1.2.1
  at: '2026-11-19T10:01:09Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
.venv/bin/ackit role check --bundle <bundle>
.venv/bin/ackit prompt developer --bundle <bundle> --part wrap-up
.venv/bin/ackit role path developer --bundle <bundle>
```

## Results

```
before (1.2.0): 143 passed, 1 skipped
after  (1.2.1): 148 passed, 1 skipped in 47.44s
```

The last three commands were also run against a real orchestly bundle with a `roles/developer/prompt.md` and `wrap-up.md` overlay: `roles complete`, the wrap-up text, and the overlay folder path. `ruff` is not installed here and is not configured.

## Coverage

`tests/test_roles_prompt.py` (5 new tests): `wrap-up` is in KINDS and optional, a role without it is complete, an overlay `wrap-up.md` is read with origin `overlay`, an empty one is reported by `role check`, `ackit prompt --part wrap-up` prints it (exit 1 when none) and the generated prompt is unchanged by it; `ackit role path` prints the overlay folder (with and without it), exits 2 for an unknown role or no name; reviewer and security prompts contain the findings format and every key and severity. `test_okf_compat.py` version assertion moved to 1.2.1. Not covered: an orchestrator parsing the findings (orchestly `tests/test_readiness.py` does).
