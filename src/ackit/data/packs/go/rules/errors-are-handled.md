---
title: "Every error is handled or returned"
severity: blocking
applies_to: [developer, reviewer]
---
## Rule

Never discard an error with _; return it wrapped with context or handle it with a stated reason.

## Why

Swallowed errors turn into silent data corruption and untraceable failures.

## How to check

Run go vet and errcheck; grep the diff for '_ =' on error returns.
