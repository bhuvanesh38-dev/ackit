---
type: task
id: T-022
title: Pilot with real resolutions
status: draft
feature: F-004
depends_on:
- T-021
points: 3
history:
- draft
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

Run 5 to 10 real resolutions through the flow with the producer and the adopter's vocabulary values. Modules touched: the adopter's overlay (vocabulary values), evidence records; no change to the producer or the store by the kit.

## Acceptance criteria

- The adopter's overlay lists its modules, vendors and tenants as vocabulary values
- 5 to 10 real pages written by the producer are validated on a copy, verified by a person with `ackit verify`, and pass `ackit validate --strict`
- The producer's index picks up only verified pages (checked on the producer side)
- Differences between the producer's pages and the types are listed and resolved by changing the type or the producer's plan, not hidden; rules the pilot shows missing become new tasks
