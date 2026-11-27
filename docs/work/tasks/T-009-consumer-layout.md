---
type: task
id: T-009
title: consumer_layout and ackit link --check
status: done
feature: F-002
points: 2
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
  at: '2026-11-20T11:59:06Z'
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

Implement the layout half of ADR-0019. Touches: new `layout.py`, `validate.py`, `cli.py`, `SPEC.md`. `init.py` is unchanged: creation stays with `--link-entry`.

## Acceptance criteria

- `ackit link --check` reports each configured link as ok, missing or wrong
- Creation stays with `ackit init --link-entry`; nothing is created by `--check`
