---
title: "Record structural decisions with the reason"
severity: advisory
applies_to: [planner, developer]
---
## Rule

A structural or contract choice gets a decision record (options, decision, why) before the code.

## Why

Code shows what was chosen, never what was rejected or why.

## How to check

Search the diff for new modules, tables, public APIs; each has a linked ADR.
