---
type: decision
id: ADR-0012
title: Agnostic core; adopter specifics only in adopters
status: proposed
date: '2026-11-17'
description: The core (spec, templates, roles, packs, validator) names no company, repository, tool or
  host; hosts and ticket tools appear only as neutral examples. Adopter-specific rules, mappings, answers
  and overlays live under `adopters/<adopter>/`, marked as examples; `adopters/example/` is a starting
  point.
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

The kit is a personal product with one beta user whose store taught the design. Company, host and tool specifics must not leak into the standard.

## Options

1. Ship the beta user's conventions as the defaults.
2. Keep the core neutral and put each adopter under `adopters/<name>/`.

## Decision

The core (spec, templates, roles, packs, validator) names no company, repository, tool or host; hosts and ticket tools appear only as neutral examples. Adopter-specific rules, mappings, answers and overlays live under `adopters/<adopter>/`, marked as examples; `adopters/example/` is a starting point.

## Why

A standard that carries one company's habits is not a standard. Lessons from the beta user shaped the generic design instead of its defaults.

## Consequences

A leakage grep is part of the definition of done (rule R-no-adopter-specifics-in-core). Adopter overlay, role profile and stack pack are three different things and are documented as such.

Amendment (same day): the layer is named `adopters/` (not `profiles/`), so that "profile" means only a role profile (`role.yaml`). The folders are `adopters/example/` and one folder per beta user.
