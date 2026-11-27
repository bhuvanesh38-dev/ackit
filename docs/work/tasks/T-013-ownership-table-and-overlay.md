---
type: task
id: T-013
title: Ownership table and overlay configuration
status: done
feature: F-003
points: 2
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.3.0
  at: '2026-11-23T09:26:16Z'
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

Give each gate check one owner today and one after adoption, and make the overlay say so. Modules touched: the first adopter's overlay (CHECKS.md, store-config.yaml), tests/test_store_config.py.

## Acceptance criteria

- The adopter's CHECKS.md has a row per check with owner today and owner after adoption, matching the design table; no row has two owners for one fact
- The overlay sets `agents_md_max_lines: 300` and the severity of ACF013 to warn through `severity`; `ackit validate` of a bundle with a 352-line entry then warns and does not fail
- A draft of the adoption PR contents lists the files to add (ackit.yaml, hooks) and the script lines to drop once a kit rule owns the fact; it is a document, nothing is applied
- The overlay config test counts the dispositions of the new table and passes
