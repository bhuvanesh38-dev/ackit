---
type: task
id: T-010
title: First adopter content
status: done
feature: F-002
points: 3
depends_on:
- T-005
- T-006
- T-007
- T-008
- T-009
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

Fill the first adopter's overlay under `adopters/`: registry mapping, branch policy, id range example, the code and process checks as `process_checks` entries, stage-name mapping, consumer layout. Touches: that overlay only.

## Acceptance criteria

- The mapping files validate with the kit
- All 17 store checks are accounted for with an explicit disposition (rule, rule plus gate, entry that calls the store's own script, or hook only with the reason); none copied. Corrected after the review: the planned split of seven rules and ten entries did not hold, see the evidence
- The stage-name mapping covers analysis, frs, tdd, test-plan, implementation and journal
- The leakage grep finds organisation names only under `adopters/`
