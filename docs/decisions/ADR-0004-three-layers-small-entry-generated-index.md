---
type: decision
id: ADR-0004
title: 'Three layers: small entry, generated index, records'
status: proposed
date: '2026-11-17'
description: AGENTS.md (budgeted, one row per document), a generated index.md, and records loaded on demand.
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

An always-loaded file that grows becomes noise; context must load progressively.

## Options

1. One big file.
2. Entry plus index plus records, with a size budget on the entry.

## Decision

AGENTS.md (budgeted, one row per document), a generated index.md, and records loaded on demand.

## Why

Agents pay for what they load. A budget on the entry and a generated index keep the cheap path cheap and make drift detectable (ACF013, ACF024).

## Consequences

Detail must move out of the entry; the validator fails an entry over budget.
