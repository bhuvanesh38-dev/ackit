---
type: task
id: T-014
title: Equivalence harness and safety
status: done
feature: F-003
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

Build the equivalence harness and its safety checks. Modules touched: a new folder under the first adopter's overlay (harness script, case files), no change to the core.

## Acceptance criteria

- The harness builds a scratch store from `git archive HEAD` of the store and a scratch code repository, with a bare `origin` under a temporary folder; the live store working tree is not read
- A safety self-test fails the run unless origin is local, the tracker override points to a local port, the token and config paths are scratch paths, and no emergency-skip variable is set
- It runs a case through the direct route (hook calls the gate) and the kit route (hook calls `ackit checks run`) and parses each `[n/17]` verdict from the output
- A case file format lets a later task add a check without changing the harness
