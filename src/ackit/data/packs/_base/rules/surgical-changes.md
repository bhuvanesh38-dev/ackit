---
title: "Change only what the work item needs"
severity: advisory
applies_to: [developer, reviewer]
---
## Rule

Every changed line traces to the work item; unrelated problems are reported, not fixed.

## Why

Unrelated edits hide the real change from review and raise merge conflicts.

## How to check

Compare the diff with the acceptance criteria; flag any hunk that traces to nothing.
