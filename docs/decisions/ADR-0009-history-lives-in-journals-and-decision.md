---
type: decision
id: ADR-0009
title: History lives in journals and decision records, not in living documents
status: proposed
date: '2026-11-17'
description: Living documents state current truth; journals (newest first, never edited) and ADRs (superseded,
  not edited) hold the why and the corrections.
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

Documents that accumulate their own history stop stating what is true now.

## Options

1. Edit documents in place and rely on version control.
2. Append-only journals and superseding ADRs.

## Decision

Living documents state current truth; journals (newest first, never edited) and ADRs (superseded, not edited) hold the why and the corrections.

## Why

Version control shows what changed, not why; the reasons are what the next agent lacks.

## Consequences

A decision or correction costs one journal entry in the same turn.
