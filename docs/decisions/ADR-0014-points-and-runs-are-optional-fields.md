---
type: decision
id: ADR-0014
title: Points and runs are optional fields, not new types
status: proposed
description: points and runs are optional validated fields on task and issue; a ticket is external_id; a job is a runs record
date: 2026-11-19
generated:
  by: ackit/1.2.0
  at: '2026-11-19T08:43:17Z'
---

## Context

An orchestrator drives development as feature -> task -> job, where a job is one run of a task (design decision D3). It needs to record an estimate per task, the result of each run, and the external ticket a work item mirrors. ACF 1.1 has no field for any of these.

## Options

1. New document types `ticket` and `job`. Pros: one file per run. Cons: a file per run floods the bundle, the run has no life apart from its task, and the ticket would duplicate a tracker's own record.
2. Leave it to unknown pass-through keys, as before. Pros: no change. Cons: nothing checks the shape, so every consumer re-invents it.
3. Optional, validated fields on existing types: `points` and `runs` on task and issue, `external_id` on epic, feature, task and issue.

## Decision

Option 3 (ACF 1.2, minor, backward compatible). `points` is an integer in a scale configured under `points:` in `ackit.yaml` (default `[1, 2, 3, 5, 8]`, `auto_start_max: 2`, `signoff_max: 5`). `runs` is an ordered list of `{id, at, outcome, tokens?, turns?, commit?, by?}` with unique ids. `external_id` is a non-empty string. New codes ACF031 (points scale), ACF032 (split rule), ACF033 (runs shape), ACF034 (external_id).

## Why

The task is the unit that is estimated and run, so the record belongs on it; a run list is small and append-only, and it diffs in review. The fields are optional so every 1.1 bundle validates unchanged. `by` is free text so the core names no agent or tool.

Open choices and why they were made this way:

- Above `signoff_max` the rule is an error (ACF032), not a warning, on `ready` and `in-progress` only. It is a binary fact an orchestrator can act on, and a warning would let an item that must be split be started; the severity is configurable per code like every rule, and `draft`, `blocked` and `cancelled` items may keep a large estimate (it is how a split gets proposed).
- Above `auto_start_max` the sign-off requirement reuses ACF027 and the small-feature pattern (a `signoff: {by, at}` before the item leaves `draft`), so there is one sign-off mechanism, not two. It applies to issues as well as tasks because both carry `points`.
- `at` must carry a time (a bare date is rejected) because two runs on one day must be orderable.
- Unknown keys inside a run record are preserved, per the SPEC rule on unknown keys.
- The scale and limits are bundle configuration, not part of the type registry, because teams size differently; an unusable `points` config is reported (ACF031 on `ackit.yaml`) and the defaults are used.

## Consequences

Easier: an orchestrator reads `points` to choose auto-start, sign-off or split, appends a `runs` record per job, and maps a ticket through `external_id`. Harder: nothing validates that `runs[].commit` exists or that `tokens` are accurate; the field records what the tool reports. Next: orchestly reads and writes the fields (its change, to be tested against a real run); computing points from facts is orchestly's job (D7), not the kit's. Supersedes: none.
