---
type: test-evidence
title: 'Evidence for I-002: ACF 1.2'
status: final
item: I-002
result: pass
generated:
  by: ackit/1.2.0
  at: '2026-11-19T08:44:25Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
.venv/bin/ackit new --bundle docs issue "<long title>" --slug acf-1-2-points-runs --set severity=medium
.venv/bin/ackit status --bundle docs I-002 ready      # then in-progress, in-review
.venv/bin/ackit status --bundle docs I-002 draft      # refused
```

## Results

```
before (baseline, ACF 1.1.0): 97 passed, 1 skipped in 25.35s
after  (ACF 1.2.0):          143 passed, 1 skipped in 39.13s
45 documents: 0 error(s), 0 warning(s)   (ackit validate docs --strict)
```

`ackit new` wrote `history: [draft]` and a 41-character file name for a 52-character title; the three `ackit status` calls produced `history: draft -> ready -> in-progress -> in-review`; the refused call printed `error: illegal transition in-review -> draft for I-002; legal from 'in-review': ['done', 'in-progress']` and exit code 1. `ruff` is not installed in this environment and is not configured in `pyproject.toml`, so no lint run was possible.

## Coverage

`tests/test_acf12.py` (42 tests): points valid, invalid and out of scale, configured scale, bad config, split rule (ready and in-progress refused above `signoff_max`, draft allowed), sign-off above `auto_start_max`; runs shape (each required key, optional keys, unknown keys kept, YAML timestamps, non-unique ids, non-list); `external_id`; a 1.1 bundle validates unchanged; OKF export and import keep `points`, `runs`, `external_id`; default slug cap and `--slug` (also on a large feature); history on create; `ackit status` legal, by path, illegal, unknown status, unknown id, final state, file untouched on refusal; improved messages. `test_validate.py` has one new case per new rule code. Not covered: an orchestrator consuming the fields.
