---
type: task
id: T-015
title: Commit-mode cases
status: done
feature: F-003
depends_on:
- T-014
points: 3
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.3.0
  at: '2026-11-23T09:26:16Z'
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

Add commit-mode cases: a firing and a clean case for each check that runs on commit, and the amend and empty-commit cases. Modules touched: the harness case files.

## Acceptance criteria

- For each commit-mode check (store: 2, 5, 7, 8, 9, 10, 11, 12, 14, 16; code clone: 1, 3, 6, 13) a clean and a firing case exist, or a recorded reason it cannot fire
- For every case the verdict and message are the same in both routes; a difference fails the run and is reported, not hidden
- An amend passes and an empty commit blocks in both routes
- A check skipped in both routes is reported as not proven
