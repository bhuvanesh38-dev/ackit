---
type: decision
id: ADR-0001
title: Adopt the Agent Context Format
description: Why this repository keeps agent context as ACF
status: proposed
date: '2026-11-17'
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:40Z'
---

## Context

Agents and people need the same, small, checkable source of project context.

## Options

1. Ad-hoc notes: no structure, cannot be validated.
2. ACF bundle: typed documents, validated in CI.

## Decision

Keep agent context as an ACF bundle in this repository.

## Why

Typed, validated context stays accurate and is cheap to load progressively.

## Consequences

Documents need owners and upkeep; `ackit validate` runs in CI.
