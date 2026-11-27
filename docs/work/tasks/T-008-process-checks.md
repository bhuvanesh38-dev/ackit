---
type: task
id: T-008
title: process_checks contract and ackit checks run
status: done
feature: F-002
points: 3
depends_on:
- T-002
signoff:
  by: human:kit-owner
  at: '2026-11-20T12:51:13Z'
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.2.1
  at: '2026-11-20T11:59:05Z'
---

<!-- ACF task: A unit of work under a feature, small enough for one agent session.
  writes: planner or developer | reviews: reviewer | signs off: reviewer
  update when: status changes
  rules:
  - Names the module(s) it touches.
  - Acceptance criteria are checkable.
  - `points` (optional) is in the configured scale; above `signoff_max` it is split before it is ready, above `auto_start_max` it needs `signoff`.
  - `runs` (optional) records each run: id, at, outcome, and optionally tokens, turns, commit, by.
-->

## Goal

Implement the checks half of ADR-0019 and ADR-0016. Touches: new `checks.py`, `cli.py`, `SPEC.md`.

## Acceptance criteria

- Config entries `{name, level, when, run, description}` are validated; `run` is an argument list run without a shell, with a timeout
- A failing block check exits 1; a failing warn check prints and exits 0; a timeout is a failure
- Proof P4: a socket guard test shows `validate`, `branch resolve` and `checks run` without commands open no connection
- The core ships no check of its own
