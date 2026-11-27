---
type: rule
id: R-no-shell-true
title: No shell=True with dynamic input
status: draft
severity: blocking
applies_to:
- developer
- security
- reviewer
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:36Z'
review_by: '2027-11-17T15:14:36Z'
---

## Rule

Call subprocess with an argument list; never shell=True with a string built from input.

## Why

Shell metacharacters in input become command execution.

## How to check

Grep the diff for shell=True, os.system and eval/exec.
