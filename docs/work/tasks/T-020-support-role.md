---
type: task
id: T-020
title: Support role
status: done
feature: F-004
depends_on:
- T-018
points: 3
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.3.0
  at: '2026-11-23T09:27:27Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T09:47:34Z'
signoff:
  by: human:kit-owner
  at: '2026-11-23T09:47:34Z'
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

Add the kit role `support` with all five parts. Modules touched: src/ackit/data/roles/support, roles tests.

## Acceptance criteria

- `ackit role list` shows `support` owning the three types, with its gates and suggested agent
- role.yaml, prompt, rules, checklist and outputs exist and pass ACF030
- The prompt tells the agent to draft only what the evidence supports, list missing facts as questions, never write `verified`, and never write a data change as a recipe
- `ackit prompt --role support` prints the prompt in a bundle that has the types
