---
type: task
id: T-006
title: code_lines field, --code-line and ACF035
status: done
feature: F-002
points: 3
depends_on:
- T-003
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

Implement ADR-0017. Touches: `validate.py`, `prompt.py`, `cli.py`, `SPEC.md`, `DOC-TYPES.md`.

## Acceptance criteria

- `code_lines` is optional on every type; absent means every line
- `validate --code-line` and `prompt --code-line` keep only matching documents
- ACF035 is an error for an id the configured registry does not know; without a registry the ids are free text (a wrong shape is always reported)
- Proof P3: for each store branch, count the documents that differ from `main` and classify them tag-able or branch-only; saved as evidence for the migration stage
