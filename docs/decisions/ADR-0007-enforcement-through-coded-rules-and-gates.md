---
type: decision
id: ADR-0007
title: Enforcement through coded rules and gates
status: proposed
date: '2026-11-17'
description: '`ackit validate` with codes ACF001 upward; `ackit check --gate start|handoff`.'
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

A format nobody checks decays.

## Options

1. Convention only.
2. A validator with stable rule codes, configurable severity and exit codes, plus start and handoff gates.

## Decision

`ackit validate` with codes ACF001 upward; `ackit check --gate start|handoff`.

## Why

Stable codes let teams tune severity per project and let CI and orchestrators act on results; gates put the checks where work changes hands.

## Consequences

Every rule needs SPEC text, a `RULE_TEXT` entry and a test that makes it fire.
