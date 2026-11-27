---
type: issue
id: I-002
title: 'ACF 1.2: points, runs and four kit friction fixes'
description: ACF 1.2 adds optional points and runs; ackit gains --slug, status and history on create
status: in-review
severity: medium
history:
- draft
- ready
- in-progress
- in-review
generated:
  by: ackit/1.2.0
  at: '2026-11-19T08:43:02Z'
---

## Symptom

An orchestrator that drives development as feature -> task -> job (design decision D3) has nowhere in ACF 1.1 to record how big a task is, how each run of it went, or which external ticket it mirrors. `points`, `runs` and `external_id` are unknown pass-through keys: nothing checks them. Using the kit for this work also showed four frictions: `ackit new` makes 90+ character file names, a status change means hand-editing `status` and `history`, `new` does not write `history`, and the validator's transition errors do not say what is legal.

## Expected

ACF 1.2 (minor, backward compatible): optional `points` and `runs` on task and issue, `external_id` defined on epic, feature, task and issue, all validated. `ackit new --slug`, a capped default slug, `ackit status`, history written on create, and validator messages that list the legal values.

## Reproduction

`ackit new --bundle docs issue "<a 90 character title>"` produces a file name of the whole title; `ackit status` does not exist; `ackit validate` on `history: [draft, done]` says only "illegal status transition draft -> done".

## Cause

ACF 1.1 was designed for documents and gates, not for an orchestrator that estimates, runs and writes results back per task.

## Fix

Version 1.2.0 (ACF 1.2). See [ADR-0014](/decisions/ADR-0014-points-and-runs-are-optional-fields.md): `points` and `runs` in `types.yaml` as `optional:` fields with checks ACF031 to ACF034 in `validate.py`, `points` settings in `ackit.yaml`, SPEC sections 4, 5, 6, 9, 13, CHANGELOG 1.2.0, ORCHESTLY-INTEGRATION section 9, INTEROP field-map row. Friction fixes: `scaffold.default_slug` and `--slug` (F1), `ackit status` / `scaffold.set_status` (F2), `history` on create for work types (F3), legal values in ACF006, ACF007 and ACF026 messages (F4). Not done, by design: orchestly reading the fields (orchestly change); computing points (orchestly, design D7).

## Evidence

See [test evidence EV-I-002](/evidence/EV-I-002-acf-1-2-points-runs.md) and the [review](/reviews/REV-I-002-acf-1-2-points-runs.md). The item stays `in-review`: a person reviews the diff before it is done.
