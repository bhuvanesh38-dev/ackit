---
type: task
id: T-021
title: Docs and format 1.4
status: done
feature: F-004
depends_on:
- T-018
- T-019
- T-020
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

Document the additions and move the format to 1.4. Modules touched: SPEC.md, docs/CHANGELOG.md, docs/architecture.md if affected, version constants, README.

## Acceptance criteria

- SPEC describes the three types, `vocabularies`, ACF043 and ACF044 and the `support` role; the rule table and RULE_TEXT agree
- CHANGELOG has a 1.4.0 entry; ACF_VERSION and the package version are 1.4; a 1.0 to 1.3 bundle validates exactly as before (guard test)
- The leakage test and the whole suite pass; `ackit validate docs --strict` reports 0 errors
