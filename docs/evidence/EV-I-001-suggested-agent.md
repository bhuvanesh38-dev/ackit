---
type: test-evidence
title: 'Evidence for I-001: suggested agent'
item: I-001
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-17T17:05:28Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
.venv/bin/ackit role list --bundle docs
.venv/bin/ackit prompt reviewer --bundle docs --explain
```

## Results

```
97 passed, 1 skipped in 29.56s
41 documents: 0 error(s), 0 warning(s)
```

`role list` prints the existing columns unchanged followed by `agent: capability high, reasoning normal, independent of developer` for the reviewer. `prompt --explain` prints `suggested agent: capability high, reasoning normal, independent of developer (role profile; ...)`.

## Coverage

Tests: built-in defaults per role (8 parametrised), no vendor or model names in `role.yaml` files, `role list` column order and `--json`, `--explain` line, ACF030 cases (bad capability, bad reasoning, unknown key, unknown role, self-independence, non-mapping, CLI exit code 1), field optional for custom roles. Not covered: an orchestrator actually consuming the field (orchestly change, pending a real-run test).
