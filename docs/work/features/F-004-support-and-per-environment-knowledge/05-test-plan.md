---
type: feature-stage
title: 'Test-Plan: Support and per-environment knowledge'
status: signed-off
feature: F-004
stage: test-plan
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

## Cases

| Case | What it shows |
|---|---|
| TP-1 types | `ackit new` makes each type with its sections; a complete page validates; each missing required key or section is reported (ACF004, ACF005); a resolution type outside 1 to 6 is ACF026 |
| TP-2 trust | a `stable` page without a `human:` verifier is ACF011; after `ackit verify` it passes |
| TP-3 vocabulary values | a registered value passes; an unregistered module, vendor or tenant is ACF043; no `vocabularies` block means no check |
| TP-4 vocabulary sources | a list, a source file with a key path, and documents of a type each work; a missing file or a bad shape is ACF044 |
| TP-5 layout | a page under `<environment>/<tenant>/support/resolutions/` raises no ACF022 |
| TP-6 role | `ackit role list` shows `support`; its parts pass ACF030; the prompt names the draft-only and never-verify rules |
| TP-7 guard | the ten old-style bundles still validate unchanged; the leakage test passes |
| TP-8 pilot | 5 to 10 real pages: validate clean after verification; the producer's index picks only verified pages |

## Environments

The kit's own test suite for TP-1 to TP-7. TP-8 runs on a copy of the casebook with real pages, read only for the producer's files.
