---
type: test-evidence
title: 'Evidence for T-013: ownership table and overlay configuration'
item: T-013
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T11:20:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q <the adopter overlay's tests/test_store_config.py>
.venv/bin/python -m pytest -q tests/test_validate.py -k "signoff or signed_off"
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
overlay config tests: 6 passed, 1 skipped (the real-layout test needs the store path variable)
validate tests for sign-off: 2 passed
whole suite: 320 passed, 3 skipped
ackit validate docs --strict: 128 documents, 0 errors, 0 warnings
```

What the new tests show: the overlay's check table has, for each of the 17 checks, the gate as owner today and a single owner after adoption (a gate or a named kit rule); a 352-line entry file gives a warning under the overlay's settings (budget 300, ACF013 set to warn) and an error without them, so the kit and the store's gate now agree on severity. The adoption-PR draft lists the files to add, the checks the gate keeps, and the script sections dropped only when a kit rule owns the fact, with the condition for each.

Two kit gaps found while doing the task and fixed with tests: `ackit verify --status signed-off` did not write `signoff` (before this task); a task above the auto-start limit had no command to record its human sign-off, so `ackit verify --signoff` was added (person only).

## Coverage

Not covered by this task, on purpose: whether the kit route and the direct route give the same verdict per check (T-015 to T-017). The table states ownership; it does not prove behaviour.
