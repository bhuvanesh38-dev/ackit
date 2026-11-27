---
type: feature-stage
title: 'Test-Plan: One owner for each gate check'
status: signed-off
feature: F-003
stage: test-plan
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:16Z'
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
| TP-1 safety self-test | the scratch origin is local, the tracker override points to a local port, no real credential file is read; the run refuses to start otherwise |
| TP-2 per check, clean | each `[n/17]` verdict is the same in both routes on a clean state |
| TP-3 per check, firing | a state that makes the check fail or warn gives the same verdict and message in both routes; a check that cannot fire is listed as not proven |
| TP-4 amend and empty commit | amend passes, empty commit blocks, in both routes |
| TP-5 push input | refs given on a push reach the gate (checks 15 and 17 fire in a push) |
| TP-6 limits | the default timeout and the 64 KiB output cap against the gate's real run and output on the full copy |
| TP-7 ownership table | every check appears once with an owner today and after adoption; the overlay config validates |

## Environments

A scratch store and scratch code repository under a temporary folder, built from committed files only; the kit's own test suite for the parts that need no store (the table and config tests); the real-layout test runs only when the store path variable is set, as today.
