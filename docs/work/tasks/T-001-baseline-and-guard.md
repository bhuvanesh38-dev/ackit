---
type: task
id: T-001
title: Baseline and guard for old bundles
status: done
feature: F-002
points: 2
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.2.1
  at: '2026-11-20T11:58:44Z'
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

Record how bundles without any new key validate today and guard that they keep doing so. Touches: `docs/evidence/`, `tests/`.

## Acceptance criteria

- `ackit validate` output of the kit's `docs/`, `examples/` and a read-only copy of orchestly's bundle is saved as baseline evidence before any code change
- A test compares a fresh run with the baseline and fails when an old bundle's errors or warnings change
- The guard is shown to fail by temporarily making a rule fire on an old bundle (result recorded)
