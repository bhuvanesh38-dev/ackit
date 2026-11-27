---
type: rule
id: R-surgical-changes
title: Change only what the work item needs
status: draft
severity: advisory
applies_to:
- developer
- reviewer
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:36Z'
review_by: '2027-11-17T15:14:36Z'
---

## Rule

Every changed line traces to the work item; unrelated problems are reported, not fixed.

## Why

Unrelated edits hide the real change from review and raise merge conflicts.

## How to check

Compare the diff with the acceptance criteria; flag any hunk that traces to nothing.
