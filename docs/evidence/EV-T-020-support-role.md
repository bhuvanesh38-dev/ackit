---
type: test-evidence
title: 'Evidence for T-020: the support role'
item: T-020
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-24T10:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_roles_prompt.py
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
tests/test_roles_prompt.py: the role is in the parametrized role tests and has 4 tests of its own (the guard rails asserted separately in the prompt and in the rules, the work-item override, the listing, `gates: -`)
full suite: 469 passed, 7 skipped (the guard test passes with its baseline unchanged)
```

The role `support` has role.yaml, a prompt, rules, a checklist (SUP-01 to SUP-08), outputs and a prompt guide; `validate_role` reports no problem (ACF030). `ackit role list` shows it owning `ticket-resolution`, `issue-pattern` and `platform-behaviour` with a suggested agent. `ackit prompt support` prints the prompt both with a work item and without one, and the prompt and the rules each carry the guard rails: fill only what the evidence supports, list a missing fact as a question, never write `verified`, run only read-only queries, never write a data change as a recipe, never write `verified_at_commit`, use registered values only, name `work_item` for a type 1 or 5 resolution. A prompt-guide test requires the guide's parts.

## Coverage

The role has no gate: its pages are not work items, so the start and handoff gates do not apply (`gates: []`). The prompt is text; whether an agent follows it is shown by the pilot (T-022), not by a unit test. The base prompt's "Work item" section still says to ask for a work item when none is given; the mission text, which comes first, tells the agent to ignore that and work from ticket evidence (tested). An empty `resolution_type` is a validation error while its question is open; the role says so. `ackit prompt support` is the command (the task text said `--role support`).
