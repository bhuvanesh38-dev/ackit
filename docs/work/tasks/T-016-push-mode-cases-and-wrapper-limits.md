---
type: task
id: T-016
title: Push-mode cases and wrapper limits
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
  at: '2026-11-23T09:26:17Z'
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

Add push-mode cases and the wrapper limits. Modules touched: the harness case files.

## Acceptance criteria

- Checks 15 and 17 fire in a push in both routes, with the tracker replaced by a local stand-in and the refs passed on standard input
- Check 4 runs with a stub build command; the real build is recorded as not run
- The default timeout and the 64 KiB output cap are measured against the gate's real runtime and output on the full scratch copy, and the numbers are written down
- The gate finds its sibling scripts through the temporary link (a firing case of a check that needs one: 12, 13 or 15)
