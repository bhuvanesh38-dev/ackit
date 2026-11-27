---
type: decision
id: ADR-0001
title: Adopt the Agent Context Format
description: Why this repository keeps agent context as ACF
status: proposed
date: '2026-11-17'
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:12:45Z'
---

## Context

The kit itself needs agent context, and it is the first test of the format.

## Options

1. Ad-hoc notes: no structure, cannot be validated.
2. An ACF bundle: typed documents validated by the kit's own tool.

## Decision

This repository keeps its context as an ACF bundle in `docs/`.

## Why

A format we ask others to adopt must survive our own use; every gap we feel is a gap in the spec.

## Consequences

`ackit validate docs --strict` is part of this repository's definition of done.
