---
type: task
id: T-019
title: Vocabularies and rules ACF043 ACF044
status: done
feature: F-004
depends_on:
- T-018
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

Add the `vocabularies` config, the binding of type fields to vocabularies, and rules ACF043 and ACF044. Modules touched: a new src/ackit/vocab.py, validate.py, types.yaml (bindings), tests, SPEC rule table.

## Acceptance criteria

- A vocabulary takes its values from a list, from a local source file with a key path, or from the ids of documents of a type
- A bound field with an unregistered value is ACF043 (error); without a `vocabularies` block nothing is checked and old bundles validate unchanged
- A missing source file, an unknown key or a bad shape is ACF044 (error)
- Each rule has a case in the validate tests that makes it fire, and the guard test still passes
