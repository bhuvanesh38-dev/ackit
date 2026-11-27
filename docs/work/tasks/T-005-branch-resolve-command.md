---
type: task
id: T-005
title: ackit branch resolve and the first adopter's mapping proof
status: done
feature: F-002
points: 2
depends_on:
- T-004
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

Add `ackit branch resolve` and prove the registry mapping on the real file. Touches: `cli.py`, a throwaway comparison script outside the kit.

## Acceptance criteria

- The command prints work and context branch for given environment, repository, stage, author and code base branch, as text and `--json`
- Proof P1: a read-only copy of the real registry of the first adopter resolves every environment, repository and stage to the same branch as orchestly's `YamlRegistry` (zero differences, or each difference listed and explained); orchestly is read, not edited
- Context-branch resolution is checked against the store's real branch names supplied by the caller
