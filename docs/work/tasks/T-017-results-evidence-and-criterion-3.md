---
type: task
id: T-017
title: Results, evidence and criterion 3
status: done
feature: F-003
depends_on:
- T-013
- T-015
- T-016
points: 3
history:
- draft
- ready
- in-progress
- blocked
- in-progress
- in-review
- done
generated:
  by: ackit/1.3.0
  at: '2026-11-23T09:26:17Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T10:49:17Z'
signoff:
  by: human:kit-owner
  at: '2026-11-23T10:49:17Z'
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

Run everything, write the result table of all 17 checks, the evidence and the review, and update the epic. Modules touched: docs (evidence, review, epic), the adopter's CHECKS.md.

## Acceptance criteria

- A result table lists all 17 checks as proven (fired and clean, same in both routes) or not proven with the reason
- A test-evidence record and an independent review record exist; the journal records any difference found
- E-002 criterion 3 is updated to what the table proves, not to what was intended
- The full suite and `ackit validate docs --strict` pass
