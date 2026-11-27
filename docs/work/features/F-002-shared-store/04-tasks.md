---
type: feature-stage
title: 'Tasks: Shared store: design and build'
status: signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-20T12:04:13Z'
feature: F-002
stage: tasks
generated:
  by: ackit/1.2.1
  at: '2026-11-20T10:43:49Z'
---

## Tasks

Eleven tasks, 26 points, all `draft` (a task above 2 points needs a `signoff` before it leaves `draft`, so you start each one by signing it). The plan's step 2 (5 points) is split into T-003, T-004 and T-005; no task is above 3 points, so none needs splitting further.

| Task | Plan step | Points | Depends on | What it delivers |
|---|---|---|---|---|
| [T-001](/work/tasks/T-001-baseline-and-guard.md) | 0 | 2 | none | baseline of old bundles and a guard test |
| [T-002](/work/tasks/T-002-id-allocation.md) | 1 | 3 | T-001 | `id_allocation`, reserved ranges, proof P2, version 1.3.0 |
| [T-003](/work/tasks/T-003-registry-model.md) | 2 | 2 | T-002 | `environment_registry` model, reader, key paths, validation |
| [T-004](/work/tasks/T-004-branch-policy.md) | 2 | 1 | T-003 | `branch_policy` and the pure resolvers |
| [T-005](/work/tasks/T-005-branch-resolve-command.md) | 2 | 2 | T-004 | `ackit branch resolve`, proof P1 on the real registry |
| [T-006](/work/tasks/T-006-code-lines.md) | 3 | 3 | T-003 | `code_lines`, `--code-line`, ACF035, proof P3 |
| [T-007](/work/tasks/T-007-author-workspace.md) | 4 | 3 | T-002 | `author_workspace`, ACF036 |
| [T-008](/work/tasks/T-008-process-checks.md) | 5 | 3 | T-002 | `process_checks`, `ackit checks run`, proof P4 |
| [T-009](/work/tasks/T-009-consumer-layout.md) | 6 | 2 | T-002 | `consumer_layout`, `ackit link --check` |
| [T-010](/work/tasks/T-010-first-adopter-content.md) | 7 | 3 | T-005, T-006, T-007, T-008, T-009 | First adopter content, 17 of 17 checks accounted for |
| [T-011](/work/tasks/T-011-docs-and-release.md) | 8 | 2 | T-010 | SPEC 1.3, architecture amendments, CHANGELOG, release |

Order: T-001 first; T-002 next (it starts version 1.3.0); then T-003 to T-005, T-006, T-007, T-008 and T-009 in any order that respects the dependencies; T-010 and T-011 last. Every task keeps the plan's rules: kit repository only, SPEC and CHANGELOG changed in the same task as the code, the guard from T-001 and `ackit validate docs --strict` pass before a task is done, and each task records its proof as test-evidence.

Peer and ownership notes: nothing here edits agent-orchestly, the store or Ansible; the kit has a single owner; commits and any publishing are the developer's call.
