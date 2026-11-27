---
type: decision
id: ADR-0008
title: Agent output is draft until a human verifies it
status: proposed
date: '2026-11-17'
description: '`stable` and `accepted` require a `verified` entry by a `human:` actor (ACF011); editing
  drops it.'
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

Generated context can be confidently wrong.

## Options

1. Trust everything generated.
2. Trust nothing.
3. Drafts by default; trusted states require a `human:` verifier.

## Decision

`stable` and `accepted` require a `verified` entry by a `human:` actor (ACF011); editing drops it.

## Why

It uses the format's own trust fields and makes the human review step visible and checkable.

## Consequences

Fresh bundles validate with draft documents; teams verify the important ones.
