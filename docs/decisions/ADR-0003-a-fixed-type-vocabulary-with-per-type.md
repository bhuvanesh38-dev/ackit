---
type: decision
id: ADR-0003
title: A fixed type vocabulary with per-type sections and ownership
status: proposed
date: '2026-11-17'
description: A fixed vocabulary of 23 types, each with required frontmatter, required sections, a status
  set and an owner; extensible under `types:` in `ackit.yaml`.
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

Free-form types give agents nothing to rely on and a validator nothing to check.

## Options

1. Free-form types only.
2. A small fixed vocabulary, extensible by config.
3. A large vocabulary covering every case.

## Decision

A fixed vocabulary of 23 types, each with required frontmatter, required sections, a status set and an owner; extensible under `types:` in `ackit.yaml`.

## Why

A template, a checkable shape and a named owner per type is what makes documents trustworthy; extension by data keeps the core small.

## Consequences

Types changes are data edits to `types.yaml`; docs/DOC-TYPES.md is generated from it.
