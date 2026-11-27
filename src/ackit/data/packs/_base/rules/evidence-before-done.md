---
title: "No work item is done without evidence"
severity: blocking
applies_to: []
---
## Rule

An item reaches done only with a passing test-evidence record, an approving review record and a journal.

## Why

Claims of 'works' without output cannot be checked by the next reader or agent.

## How to check

`ackit validate` fails ACF012 when a done item lacks any of the three.
