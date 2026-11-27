---
type: rule
id: R-record-decisions
title: Record structural decisions with the reason
status: draft
severity: advisory
applies_to:
- planner
- developer
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:12:45Z'
review_by: '2027-11-17T15:12:45Z'
---

## Rule

A structural or contract choice gets a decision record (options, decision, why) before the code.

## Why

Code shows what was chosen, never what was rejected or why.

## How to check

Search the diff for new modules, tables, public APIs; each has a linked ADR.
