---
type: rule
id: R-no-adopter-specifics-in-core
title: No adopter specifics in the core
status: draft
severity: blocking
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Rule

No company, repository, host or tool name outside `adopters/<adopter>/`; hosts and ticket tools appear only as neutral examples.

## Why

The standard must stay agnostic (ADR-0012).

## How to check

Run the leakage grep over the repository excluding `adopters/` and the history; it returns nothing.
