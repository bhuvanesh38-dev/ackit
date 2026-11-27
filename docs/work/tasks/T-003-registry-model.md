---
type: task
id: T-003
title: environment_registry model, reader and validation
status: done
feature: F-002
points: 2
depends_on:
- T-002
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

Implement the registry half of ADR-0015: the internal model, the reader for inline data or `source_file` (opt-in, read-only, may be outside the bundle), `key_paths` mapping, validation of the block. Touches: new `registry.py`, `validate.py`, `SPEC.md`.

## Acceptance criteria

- Inline and `source_file` registries resolve to the same model; a missing file or unknown key path gives a clear error
- Absent block changes nothing (guard passes)
- Defaults match the generic shape orchestly's yaml adapter reads (recorded comparison)
- No other file outside the bundle is read

## Recorded comparison with agent-orchestly's yaml adapter

Same defaults: `environments`, `id`, `repo`, `default_stage`, `stages.${stage}.branches.${repo}`. Differences, all on purpose:

| Topic | orchestly | kit |
|---|---|---|
| Default stage when absent | the string `default` | none; a lookup without a stage is an error |
| Repositories | only `repos.${repo}.path` for local paths | `repositories` key path (default `repos`), a list or a mapping of names; no local-path lookup |
| Branch lookup | renders `${stage}` and `${repo}` into a path | enumerates stages and repositories, so dotted names work; `${stage}` must come before `${repo}` |
| Path syntax | `$.` prefix, indexes, wildcards | dotted keys only |
| Bad data | missing branch, duplicate ids, non-mapping entries pass or crash | each is a reported problem (ACF038) |
| Extras | provisioner, plug-in adapters, null registry | `code_line`, `extensions`, inline data, `source_file` relative to the bundle |
