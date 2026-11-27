---
type: epic
id: E-002
title: Shared store support (ACF 1.3)
description: Make the kit able to run and maintain a shared context store that serves several repositories,
  code lines and developers
status: in-progress
history:
- draft
- ready
- in-progress
generated:
  by: ackit/1.2.1
  at: '2026-11-20T10:43:49Z'
---

<!-- ACF epic: A body of work delivered by several features.
  writes: business-analyst | reviews: human owner | signs off: human owner
  update when: when scope changes; closed when all features are done
  rules:
  - Done only when every child feature is done.
  - Success criteria are measurable.
-->

## Goal

The kit becomes the framework that maintains a **shared context store**: one repository, outside the code repositories, that serves several code repositories, several code lines (branch families, tenants) and several developers and agents writing at once. The first adopter is a company whose `agent-context` store today has conventions and scripts but no framework. The kit is improved with the full capability first, proven by agent-orchestly maintaining context for agentic development, and only then applied to that store.

## Scope

In scope: a model for code lines and a registry; pairing of a store branch with a code branch; developer workspaces; safe concurrent writing and id allocation; an extension point for process gates (the checks a store runs on commit and push); a compatibility layer so existing consumers (Claude Code, AX, hooks) keep reading the same paths; a migration path from the current store layout.

Out of scope: hosting or a network service; changing code repositories; moving store data that is not context (SQL dumps, HTML reports, personal work product); any change to the first adopter's live store before the pilot is signed off.

## Success criteria

- `ackit validate --strict` reports 0 errors on a migrated **copy** of the main project folder of the store.
- The always-loaded entry is 150 lines or fewer, and a typical Java task loads fewer characters than today's baseline (129k characters, measured 2026-11-20); the target number is set in the design stage.
- Every one of the store's 17 gate checks is accounted for: mapped to an ACF validator rule or to an adopter gate, each with a test that makes it fire.
- Two writers creating work items at the same time on different branches never produce the same id, proven by a test.
- The paths AX and Claude Code read (`AGENTS.md`, `rules/`, `.claude/CLAUDE.md`, `.claude/rulebook`) are unchanged after migration, proven by a path diff.
- One real orchestly job maintains its context through the new kit capability and its records validate.

## Features

- [F-002 Shared store: design and build](/work/features/F-002-shared-store/feature.md)
- [F-003 One owner for each gate check](/work/features/F-003-one-owner-for-each-gate-check/feature.md) (closes criterion 3)

## Progress against the success criteria (2026-11-23)

| # | Criterion | State | Evidence or what is missing |
|---|---|---|---|
| 1 | `validate --strict` 0 errors on a migrated copy | open | rehearsal gave 1 error (entry 352 lines vs 150) and 142 link warnings; decision on the entry size pending |
| 2 | Entry 150 lines or fewer, fewer characters loaded | open | same decision; `agents_md_max_lines: 300` is a stopgap in the overlay |
| 3 | All 17 checks accounted for, each with a test that fires | done, with stated limits | all 17 have an owner (CHECKS.md) and each was made to fire and to stay clean in both routes on a scratch copy of the store (RESULTS.md, EV-T-017): 11 proven, 4 proven by their hint line only (the gate never prints those warnings), 2 proven with a stand-in (the build for check 4, the tracker for check 15). Each row proves one firing condition; not shown: the real build, a real tracker, the push-time scope of checks 3, 5 to 14 and 16, and the other conditions of checks 1, 2, 6, 13, 14 and 15 (listed in RESULTS.md) |
| 4 | Two writers never get the same id | done | T-002, EV-T-002 |
| 5 | Consumer paths unchanged after migration | partly | T-009 checks the links; the path diff on a real migration is not run |
| 6 | One real orchestly job uses the capability | open | waiting on the orchestly session; the kit does not edit orchestly |
