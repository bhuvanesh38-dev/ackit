---
type: issue
id: I-001
title: Role profiles have no suggested agent or model
status: done
severity: medium
generated:
  by: ackit/1.0.0
  at: '2026-11-17T16:59:47Z'
history:
- draft
- ready
- in-progress
- in-review
- done
---

<!-- ACF issue: A bug or defect report and its fix.
  writes: tester or developer | reviews: reviewer | signs off: reviewer
  update when: as the cause becomes known
  rules:
  - Reproduction is concrete enough to run.
  - Done needs test evidence of the fix and a review record.
-->

## Symptom

`role.yaml` has no field for a suggested agent or model, so tools like agent-orchestly skip the "kit role default" level of their model-routing order.

## Expected

Role profiles can declare a tool-neutral suggestion, e.g. `suggested_agent: {capability: high|standard|fast, reasoning: deep|normal, independent_of: developer}`. It names no vendor or model (the agnostic core), and the adopter maps capability tiers to real models. `ackit role` and `ackit prompt --explain` show it, and orchestly uses it as the third precedence level.

## Reproduction

`grep suggested src/ackit/data/roles/*/role.yaml` returns nothing.

## Cause

Not designed in 1.0: role profiles described the work, not the kind of agent suited to it.

## Fix

Added the optional `suggested_agent` field (1.1.0): built-in defaults in each `role.yaml`, ACF030 validation (`roles.validate_suggested_agent`), an `agent:` column appended to `ackit role list` plus `role list --json`, a `suggested agent` line in `ackit prompt --explain`, SPEC section 7, ADOPTION, CHANGELOG 1.1.0, and example tier maps under `adopters/`. Still open: orchestly reading the field, to be tested against a real orchestly run (user rule: test with the real thing, not only fakes); that is orchestly's change, not the kit's.

## Evidence

See [test evidence EV-I-001](/evidence/EV-I-001-suggested-agent.md) and the [review](/reviews/REV-I-001-suggested-agent.md). pytest: `97 passed, 1 skipped`. `ackit validate docs --strict`: `41 documents: 0 error(s), 0 warning(s)`.
