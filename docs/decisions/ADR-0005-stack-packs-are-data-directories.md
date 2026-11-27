---
type: decision
id: ADR-0005
title: Stack packs are data directories
status: proposed
date: '2026-11-17'
description: A pack is a directory with `pack.yaml`, optional rules and template overrides; `--pack-dir`
  adds packs.
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

Different stacks need different commands, default rules and module discovery, and new stacks appear constantly.

## Options

1. A Python class per stack.
2. A directory of declarative data per stack.

## Decision

A pack is a directory with `pack.yaml`, optional rules and template overrides; `--pack-dir` adds packs.

## Why

Adding a stack must not need a release of the kit; declarative detection and variants cover build-tool differences.

## Consequences

Detection is limited to what `pack.yaml` can express; exotic stacks use the generic pack plus answers.
