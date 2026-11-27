---
type: test-evidence
title: 'Evidence for F-003: one owner for each gate check'
item: F-003
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T20:00:00Z'
---

## Commands

```bash
ACKIT_BETA_STORE=<store root> .venv/bin/python -m pytest -q
.venv/bin/python <the adopter overlay's equivalence/harness.py> --source-store <store root> --cases <all four case files>
.venv/bin/ackit validate docs --strict
```

## Results

```
full suite with the store path set: 358 passed, 1 skipped
all 62 equivalence cases on the real store source: pass in both routes
ackit validate docs --strict: 0 errors
```

Per task: T-013 EV-T-013, T-014 EV-T-014, T-015 EV-T-015, T-016 EV-T-016, T-017 EV-T-017 (the per-check table). Each task has an independent review record (REV-T-013 to REV-T-017).

## Coverage

What the feature proves and does not prove is in the table of T-017: 11 checks proven, 4 by their hint line only, 2 with a stand-in; each row proves one firing condition; the push-time scope of checks 3, 5 to 14 and 16, the real build and a real tracker are not shown.
