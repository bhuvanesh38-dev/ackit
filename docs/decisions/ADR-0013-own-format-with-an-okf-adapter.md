---
type: decision
id: ADR-0013
title: Own format with an OKF adapter, superseding ADR-0002
status: proposed
date: '2026-11-17'
supersedes: ADR-0002
description: ACF 1.0 stands alone; OKF v0.2 interop through an adapter
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:44:50Z'
---

## Context

ADR-0002 made ACF a profile of OKF v0.2 so existing OKF consumers would keep working. OKF is an early (v0.2) external specification: its vocabulary is general-purpose, it can change under us, and being valid OKF constrained field names and structure we want to design for software projects (work items, roles, gates, ownership).

## Options

1. Stay an OKF profile and track its versions.
2. Fork OKF into a private variant that is still called a profile.
3. Own format, ACF 1.0, with an adapter for OKF in both directions.

## Decision

ACF 1.0 is a standalone format. OKF is supported through `ackit export --okf` and `ackit import --okf`; the field map is `review_by` <-> `stale_after` and `sources[].ref` <-> `sources[].resource`, statuses via `acf_status`, the role overlay under `.acf/roles/`. The root index carries `acf_version: "1.0"` only.

## Why

Independence from a v0.2 spec we do not control, freedom to name and shape fields for software projects (`review_by` says what a human must do; a source `ref` can be a path or URL), and no requirement that every future ACF feature fit OKF. Interop is kept because the adapter is lossless for everything ACF writes, with a documented list of what cannot round-trip.

## Consequences

Field renames are recorded in docs/CHANGELOG.md. The CLI calls and output shapes used by orchestrators (`init`, `new`, `index --write`, `validate`, `check --json`, `prompt`, `types --markdown`) stay stable. The version is 1.0.0. ADR-0002 is superseded.
