---
type: test-evidence
title: 'Evidence for F-005: the session heading shape rule'
item: F-005
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T21:35:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

The feature is the single task T-023; its evidence is EV-T-023 and its review REV-T-023. The full suite and the strict validation of the kit's own documents pass (see EV-T-023 for the counts). The three acceptance criteria are met: ACF045 is a warning by default and an error with `severity: {ACF045: error}`, ACF021 is unchanged and the guard test passes with its baseline untouched, and the on-hold block is documented with a test.

## Coverage

ACF045 checks the shape only (not that the day or week matches the date, nor that the sha exists). The core `work` set is unchanged.
