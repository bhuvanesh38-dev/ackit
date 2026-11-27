---
type: task
id: T-023
title: ACF045 session heading rule and the on-hold status documentation
status: done
feature: F-005
points: 2
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.3.0
  at: '2026-11-23T10:58:12Z'
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

Build feature F-005: rule ACF045 (the session entry heading shape) and the documented, tested on-hold status set. Modules touched: `validate.py`, SPEC, ADOPTION, CHANGELOG, the validate tests.

## Acceptance criteria

- ACF045 fires, as a warning by default, on a session entry heading that lacks `(Day, Www)`, the branch, `@ <7 to 40 hex characters or none>` or the title; a valid heading, and the `@ none` form, do not fire it
- `severity: {ACF045: error}` makes it an error; ACF021 is unchanged
- The guard test passes without a change to its baseline (a 1.0 to 1.3 bundle validates as before)
- The on-hold `status_sets` block is in SPEC and ADOPTION, with a test: `in-progress` to `on-hold` to `in-progress` is legal, `on-hold` to `done` is refused
- SPEC rule table, RULE_TEXT, CHANGELOG and the full suite agree; `ackit validate docs --strict` passes
