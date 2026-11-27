---
type: feature-stage
title: 'Plan: Support and per-environment knowledge'
status: signed-off
feature: F-004
stage: plan
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:19Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T09:34:16Z'
history:
- draft
- signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-23T09:34:16Z'
---

## Steps

1. Types and templates (T-018): the three types in the registry, DOC-TYPES regenerated, templates through `ackit new`.
2. Vocabularies (T-019): config loader, binding fields on types, rules ACF043 and ACF044, tests that make each fire.
3. Role (T-020): the `support` role with its five parts and prompt tests.
4. Docs and release (T-021): SPEC section, rule table, CHANGELOG, format version 1.4, guard test run.
5. Pilot (T-022): the adopter's vocabulary values in its overlay and 5 to 10 real resolutions through the whole flow; depends on pages from the producer.

## Risks

- The producer's pages differ from the types (field names, numbers as text): align the type, do not rewrite the producer; found by the pilot.
- A vocabulary source that is large or missing: a missing file is a configuration error, not silence.
- The pilot depends on real resolutions that do not exist yet: T-022 stays blocked until they do; the build is not held up by it.
