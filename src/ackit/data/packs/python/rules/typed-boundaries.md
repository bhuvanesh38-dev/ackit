---
title: "Validate data at the boundary"
severity: advisory
applies_to: [developer, reviewer]
---
## Rule

Parse external input into typed models (dataclass, pydantic) at the edge; inner code trusts the type.

## Why

Unvalidated dicts spread shape assumptions across the code.

## How to check

Entry points convert input before passing it on.
