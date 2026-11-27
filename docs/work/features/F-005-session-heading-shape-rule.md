---
type: feature
id: F-005
title: Session heading shape rule
description: Enforce the session entry heading shape (date, day and week, branch, sha, title) as an opt-in-severity
  rule; document on-hold as a bundle-level status
status: done
epic: E-002
tier: small
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.3.0
  at: '2026-11-23T09:54:13Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T10:50:13Z'
signoff:
  by: human:kit-owner
  at: '2026-11-23T10:50:13Z'
---

<!-- ACF feature: A deliverable change. tier small = one document; tier large = a folder of staged documents signed off in order.
  writes: business-analyst (requirements) | reviews: reviewer | signs off: human owner per stage
  update when: every stage change; journal on every decision
  rules:
  - Large features: stages analysis, design, plan, tasks, test-plan, journal; a stage is signed off before the next is started.
  - Small features carry `signoff` before status ready.
  - Done needs test evidence, a review record and a journal entry.
-->

## Goal

Two requests from a consumer of the kit (a bundle that keeps session logs and uses an on-hold status), both checked against the code on 2026-11-23. (1) The session entry heading `## YYYY-MM-DD (Day, Www) - branch @ sha - title` is only text in the type's rules; rule ACF021 checks just that the heading starts with a date and that the six labels exist. Make the shape checkable. (2) The store's universal statuses include on-hold; the kit's `work` set has none. A bundle can already declare its own status set.

## Acceptance criteria

- A new rule ACF045 checks the heading shape of every session entry: date, `(Day, Www)`, branch, `@ sha` (7 to 40 hex characters, or the explicit word `none` for an entry not tied to a commit), title. It is a warning by default and a bundle makes it an error with `severity: {ACF045: error}`; a 1.0 to 1.3 bundle validates exactly as before (the guard test passes), because tightening ACF021 itself would break existing bundles.
- ACF021 is unchanged; SPEC, RULE_TEXT, the rule table and a firing case in the validate tests agree.
- The bundle-level `on-hold` status set is documented in SPEC and ADOPTION with the exact `status_sets` block, and a test shows `in-progress` to `on-hold` to `in-progress` and the refusal of `on-hold` to `done`. The kit's own `work` set does not change while there is one adopter that wants it.

## Design

ACF045 reads the session type's headings with one regular expression in `validate.py`, beside `session()`; the severity comes from the existing `severity` config, so no new config key. The word `none` is explicit rather than an omitted sha, so a heading stays parseable. The `on-hold` block is documentation plus a test, no code: a bundle's `status_sets` replace a set by name (read in `bundle.py`).

## Plan

1. Add the rule, its text and a firing case; 2. add the test for the on-hold block; 3. SPEC, ADOPTION, CHANGELOG; 4. full suite, guard test, review.

## Test plan

A heading with each part missing or malformed fires ACF045; a valid one and the `none` form do not; with no `severity` setting it is a warning, with `severity: {ACF045: error}` an error; the ten old-style bundles validate unchanged; the on-hold transitions as above.
