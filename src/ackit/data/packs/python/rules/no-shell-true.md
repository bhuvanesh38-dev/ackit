---
title: "No shell=True with dynamic input"
severity: blocking
applies_to: [developer, security, reviewer]
---
## Rule

Call subprocess with an argument list; never shell=True with a string built from input.

## Why

Shell metacharacters in input become command execution.

## How to check

Grep the diff for shell=True, os.system and eval/exec.
