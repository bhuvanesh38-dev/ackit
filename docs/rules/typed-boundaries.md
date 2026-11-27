---
type: rule
id: R-typed-boundaries
title: Validate data at the boundary
status: draft
severity: advisory
applies_to:
- developer
- reviewer
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:12:45Z'
review_by: '2027-11-17T15:12:45Z'
---

## Rule

Parse external input into typed models (dataclass, pydantic) at the edge; inner code trusts the type.

## Why

Unvalidated dicts spread shape assumptions across the code.

## How to check

Entry points convert input before passing it on.
