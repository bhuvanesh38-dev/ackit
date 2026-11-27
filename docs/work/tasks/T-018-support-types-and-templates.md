---
type: task
id: T-018
title: Support types and templates
status: done
feature: F-004
points: 3
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.3.0
  at: '2026-11-23T09:27:26Z'
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

Add the three support types to the core registry with templates. Modules touched: src/ackit/data/types.yaml, docs/DOC-TYPES.md (generated), tests.

## Acceptance criteria

- `ticket-resolution`, `issue-pattern` and `platform-behaviour` exist with the required keys, sections, `doc` status set, human verification at stable, `dir: ""` and the Writes / Reviews / Signs off text of the design
- `resolution_type` accepts only 1 to 6 (ACF026 otherwise); a complete page validates and each missing key or section is reported
- `ackit new` creates each type with its sections; DOC-TYPES.md is regenerated
- A page under a nested `<environment>/<tenant>/support/` path raises no ACF022
