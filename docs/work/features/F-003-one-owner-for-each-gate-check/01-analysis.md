---
type: feature-stage
title: 'Analysis: One owner for each gate check'
status: signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-23T09:18:35Z'
feature: F-003
stage: analysis
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:16Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T09:18:35Z'
history:
- draft
- signed-off
---

## Problem

The store's 17 gate checks are all reachable through the kit (T-012), but ownership is muddled. A check can be done twice (a kit rule and the same section of the store script), by the wrong owner (a generic fact kept in an org script, or an org policy turned into a kit rule), or with two severities (ACF013 is an error where the gate warns). Success criterion 3 of E-002 also asks that each check has a test that makes it fire; today only checks 1 and 16 were seen to fire. The kit must be finished and proven before the store is migrated.

## Findings

Facts (read 2026-11-23, the first adopter overlay's `CHECKS.md` and the adopter store's gate script):

- Dispositions today: 2 rule (5, 8), 4 rule + gate (2, 7, 9, 10), 11 entry. The `store-gate` entry runs the whole script, so any check also built as a kit rule would run twice until the store script drops its copy.
- Differences found: check 10 is an error in the kit and a warning in the gate; check 9 tests `review_by` in the kit and `last-verified` in the store; check 8 reads `index.md` in the kit and `knowledge-base.md` in the store.
- Generic by nature (assessment, not yet decided): 16 empty or whitespace-only commit, 17 overriding remote changes, 1 protected branch (the kit already has `branch_policy`), 11 local-only leakage, 2 "context updated today". Specific to the adopter: 3 and 6 (Flyway), 4 (Gradle build), 13 (Java), 14 (data-changing SQL), 15 (store PR before the code push).
- Proven so far: the gate runs under a hook through `ackit checks run` (T-012); check 16 passes an amend and blocks an empty commit with the real gate on a scratch repo. Not proven: an end-to-end run with the bundle installed in a store, checks 15 and 17 in a real push, and a same-result comparison for all 17.
- The kit core must not name the organisation (the leakage test); org settings stay under `adopters/`.

## Open questions

1. Is each of 16, 17, 1, 11 and 2 owned by the kit, or does the store script keep it? (the owner decides; ADR to record it)
2. For the 4 split checks, where is the line? In particular the severity of check 10 and the field mapping for check 9.
3. Does the store drop its copy of a check only in the adoption PR (my recommendation), or sooner?
4. The equivalence test needs a scratch copy of the store; confirm it may be a copy under /tmp and never the live store.

## Scope decision after review (2026-11-23)

Only one adopter exists, so moving generic checks (16, 17, 1, 11, 2) into the kit core has no second user and creates overlap with the store script until the adoption PR. Reduced scope: (A3) one owner and one severity for each of the 4 split checks, (A4) an equivalence test of all 17 on a scratch copy, (A5) the written contents of the adoption PR. Moving a generic check into the core waits for a second adopter or for the store's own decision.
