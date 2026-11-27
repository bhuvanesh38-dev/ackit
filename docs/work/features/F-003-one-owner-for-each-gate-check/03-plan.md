---
type: feature-stage
title: 'Plan: One owner for each gate check'
status: signed-off
feature: F-003
stage: plan
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:16Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T09:34:15Z'
history:
- draft
- signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-23T09:34:15Z'
---

## Steps

1. Ownership and configuration (T-013): the two-column table in the adopter's CHECKS.md, the overlay `severities` and budget for check 10, a draft of the adoption PR contents as a document.
2. Harness and safety (T-014): scratch store builder, bare origin, isolation environment, per-check verdict parser, the two routes, a safety self-test.
3. Commit-mode cases (T-015): firing and clean cases for the store checks and the code-clone checks that can fire without a build.
4. Push-mode cases (T-016): checks 15 and 17 with a local stand-in for the tracker, check 4 with a stub build, wrapper limits on the full copy.
5. Results (T-017): a result table of all 17 (proven, not proven with reason), evidence and review, journal, and an update of E-002 criterion 3.

## Risks

- A check cannot be made to fire in a scratch repository (build, tracker): recorded as not proven, not hidden.
- The gate's behaviour depends on the developer's machine (home folder files, tokens): isolation overrides and a clean environment; the safety self-test fails the run if a real path or the network is touched.
- The full-copy run is slow: timeouts are measured, not guessed.
