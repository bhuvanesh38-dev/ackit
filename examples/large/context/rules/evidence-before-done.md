---
type: rule
id: R-evidence-before-done
title: No work item is done without evidence
status: draft
severity: blocking
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:40Z'
review_by: '2027-11-17T15:14:40Z'
---

## Rule

An item reaches done only with a passing test-evidence record, an approving review record and a journal.

## Why

Claims of 'works' without output cannot be checked by the next reader or agent.

## How to check

`ackit validate` fails ACF012 when a done item lacks any of the three.
