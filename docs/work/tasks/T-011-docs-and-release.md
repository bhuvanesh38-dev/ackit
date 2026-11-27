---
type: task
id: T-011
title: Documentation and ACF 1.3 release
status: done
feature: F-002
points: 2
depends_on:
- T-010
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

Finish the documents for 1.3.0. Touches: `SPEC.md`, `docs/architecture.md`, `DOC-TYPES.md`, `CHANGELOG`, ADR files.

## Acceptance criteria

- SPEC has the 1.3 section; the architecture text carries the two amendments (registry file outside the bundle, adopter commands)
- `ackit validate docs --strict` shows 0 errors and the baseline guard passes
- The ADRs are ready for the developer to run `ackit verify`; none is accepted by an agent
