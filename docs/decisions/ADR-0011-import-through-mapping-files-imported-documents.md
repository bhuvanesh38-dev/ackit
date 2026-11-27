---
type: decision
id: ADR-0011
title: Import through mapping files; imported documents stay draft
status: proposed
date: '2026-11-17'
description: '`ackit import` maps files by glob, preserves unknown keys (clashes become `source_*`), stubs
  missing sections, records `sources`, and writes drafts.'
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

Teams already have context in their own layouts; asking them to rewrite it blocks adoption.

## Options

1. Manual migration.
2. A fixed importer per known layout.
3. A mapping file (glob to type, destination, id, defaults).

## Decision

`ackit import` maps files by glob, preserves unknown keys (clashes become `source_*`), stubs missing sections, records `sources`, and writes drafts.

## Why

A mapping is data, reusable and reviewable; drafts keep the trust model intact.

## Consequences

Source files are only read; the importer reports placeholders for required keys it could not infer.
