---
type: decision
id: ADR-0002
title: ACF is a profile of OKF v0.2
status: superseded
date: '2026-11-17'
description: Define ACF as an OKF profile.
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
superseded_by: ADR-0013
---

## Context

OKF defines bundles of markdown with frontmatter, trust fields and reserved files, but no software-project vocabulary, no lifecycle, and no enforcement.

## Options

1. Invent a new format.
2. Use OKF as is.
3. Define ACF as an OKF profile: valid OKF, plus rules.

## Decision

Define ACF as an OKF profile.

## Why

Existing OKF consumers keep working, unknown keys are preserved, and ACF adds only what projects need: types, sections, lifecycle, roles and checks. A new format would split the ecosystem; plain OKF cannot be enforced.

## Consequences

Every ACF bundle is an OKF bundle. The one extension is the non-concept `roles/` overlay directory.
