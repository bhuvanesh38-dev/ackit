---
type: feature
id: F-002
title: 'Shared store: design and build'
description: Code lines and registry, store-to-code pairing, developer workspaces, concurrent writers,
  process gates, compatibility layer
status: in-review
epic: E-002
tier: large
history:
- draft
- ready
- in-progress
- in-review
generated:
  by: ackit/1.2.1
  at: '2026-11-20T10:43:49Z'
---

## Goal

Extend ACF and `ackit` so that one shared store can serve several repositories, code lines and developers, with the store's existing needs covered by the format and the tool rather than by loose conventions and scripts. This feature is delivered in stages, each signed off by the developer before the next starts; no code is written before the design stage is signed off.

## Acceptance criteria

- The success criteria of epic E-002 hold, each with evidence.
- The design records every decision with its options and reason (ADR) and keeps the core agnostic: no organisation names, paths or branches outside the adopter's overlay.
- Existing bundles (the kit's own `docs/`, `examples/`, orchestly's bundle) still validate unchanged: the new capability is additive, and the format version moves to 1.3 with a changelog entry.

## Stages

Signed off in order: [01-analysis](/work/features/F-002-shared-store/01-analysis.md), 02-design, 03-plan, 04-tasks, 05-test-plan; 06-journal is the running record. All five stages are signed off; the build (T-001 to T-012) is done with evidence and review. The feature stays `in-review` on purpose: the migration rehearsal and the pilot are not finished (see the epic's criteria table), and the remaining work is tracked in F-003 (one owner per gate check) and by the open decisions in the journal.
