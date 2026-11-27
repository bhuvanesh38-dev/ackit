---
type: task
id: T-004
title: branch_policy model and pure resolvers
status: done
feature: F-002
points: 1
depends_on:
- T-003
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

Implement the policy half of ADR-0015 and the resolvers of ADR-0016: `resolve_work_branch` and `resolve_context_branch` as pure functions, validation of the block. Touches: new `branchpolicy.py`, `validate.py`.

## Acceptance criteria

- Work branch base is the registry's default stage unless the policy sets one
- Context branch base is the store branch matching the code base branch when the caller lists it, else the fallback
- The functions run no git and no network (asserted by test)
