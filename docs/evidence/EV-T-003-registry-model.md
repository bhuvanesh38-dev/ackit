---
type: test-evidence
title: 'Evidence for T-003: environment_registry model and reader'
item: T-003
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T14:40:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf13_registry.py
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
tests/test_acf13_registry.py: 28 passed
```

## Coverage

Covered: inline and `source_file` (relative and absolute) give an equal model; `extensions` carried and not interpreted; own-file key paths; other branch shapes; ten configuration errors with a clear message; malformed, binary and non-mapping files; bad branch templates reported without a crash; wrong value types; the guard (`tests/test_guard_baseline.py`) still passes, so a bundle without the block validates as before; only the configured file is opened (patched `open` and `read_text`). The recorded comparison with orchestly's adapter is in the task body. The first end-to-end run against a real registry is proof P1 in the evidence of T-005.
