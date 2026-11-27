---
type: reference
title: Integrating agent-orchestly with ACF
description: What a workflow orchestrator (agent-orchestly) must change to read and write ACF
status: draft
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:14:03Z'
---

# Integrating agent-orchestly with ACF

agent-orchestly is the author's job orchestrator; it is used here as the example consumer. The same contract fits any orchestrator. Nothing in the kit imports or depends on it, and this document changes nothing in it: it lists what the orchestrator must change.

## 1. Context store mode

Orchestly's `context.mode` is `own` (it scaffolds a local repo) or `external` (an existing store path). Map both onto ACF:

- `own`: scaffold with `ackit init <repo> --bundle <state>/context-repo --yes` instead of the built-in scaffold templates; then commit locally as today.
- `external`: `context.path` is the bundle root. Run `ackit validate <path>` at job start and refuse to run (or warn, per config) on errors.

## 2. Templates become ACF types

| Orchestly template | ACF type | Notes |
|---|---|---|
| `session-entry.md` | `session` (entry inside `sessions/<author>/<branch>.md`) | keep the heading `## date (Day, Www) - branch @ sha - title` and the labels Done / Faced / Decisions / Build / Next / Blockers; add `item:` to the file frontmatter |
| `index-line.md` | `session-index` | one line `- YYYY-MM-DD - branch - title - [entry](path)` |
| `test-evidence.md` | `test-evidence` | frontmatter `item`, `result: pass|fail|partial`; sections Commands, Results, Coverage |
| `review-record.md` | `review` | frontmatter `item`, `role`, `verdict`; sections Scope, Findings, Resolution, Verdict |
| `handoff-record.md` | `handoff` | frontmatter `item`; sections Summary, Evidence, Open items, Needs a person |
| `module-record.md` | `module` | `M-<slug>` id, sections Responsibility, Public surface, Dependencies, Owners |
| `job-overview.md` | `task` (work item) | map `work-item` to `id`, job status to the work status set (draft, ready, in-progress, in-review, done, blocked, cancelled) |
| `setup-record.md` | a section of the session entry (Build) | environment and setup facts are session facts, not a document type |
| `scaffold-readme.md`, `scaffold-index.md` | `ackit init` and `ackit index --write` | delete the templates |

Replace the template header comment `<!-- orchestly-template name=... version=N -->` with frontmatter `generated: {by: orchestly/<version>, at: ...}`; keep the job id in `sources` or a custom key (unknown keys are preserved). Template files can stay if the orchestrator renders them itself; they must produce frontmatter and sections that `ackit validate` accepts. Easiest path: render through `ackit new <type>`.

Replace `last-verified:` with `verified: [{by, at}]` and never write a `human:` actor.

## 3. Gate calls

| Orchestly step | Call | On failure |
|---|---|---|
| Intake (work item known) | `ackit check --gate start --item <id> --role developer --json` | park the job; surface the failed checks |
| Prepare / Code | `ackit prompt developer --item <id> --budget <chars>` | use the output as the system prompt; add the code-task text |
| Test | `ackit prompt tester --item <id>`; write `test-evidence` | `result: fail` blocks handoff |
| Review | `ackit prompt reviewer --item <id>` and, when the change touches auth, input or data, `ackit prompt security --item <id>`; write `review` records | `verdict: blocked` stops the job |
| Handoff | `ackit check --gate handoff --item <id> --json` then `ackit validate <bundle> --strict` | do not open the pull request; list failed checks under "Needs a person" |

Exit codes: 0 pass, 1 fail, 2 usage error. `--json` gives `{gate, item, passed, checks:[{name, level, detail}]}`.

## 4. Roles and profiles

Orchestly executors currently carry their own prompts. Replace them with `ackit prompt <role>`; add `--explain` to log which documents shaped a prompt. Teams that need a different reviewer simply drop `roles/reviewer/rules.md` into the bundle. Custom roles work the same way (`ackit role new`).

## 5. What orchestly must write

At job end: session entry, test evidence, review records, a journal entry for each decision, a handoff, plus status moves with `history`. It must not write `verified` or `signoff` for a human, and must leave committing the context to a person unless configured otherwise.

## 6. Migration

For an existing orchestly-written store, use `ackit import` with a mapping file; imported records arrive as `draft`.

## 7. Compatibility contract (ACF 1.2)

The orchestrator's field names live in one module (`kitfields.py`) and are checked against `ackit types --markdown` at start-up. The kit keeps these stable: the CLI calls `init`, `new`, `index --write`, `validate [--strict]`, `check --gate start|handoff --json`, `prompt`, `types --markdown`, their exit codes and output shapes (for the types listing: a `## \`type\`` heading per type, `- Required frontmatter:` with backticked keys, `- Statuses:`). Field renames between versions are listed with old and new names in CHANGELOG.md (1.0.0: `stale_after` to `review_by`, `sources[].resource` to `ref`; neither is used by the orchestrator today). Update `kitfields.py` in one step from that table when a later version renames something it uses.

## 8. Suggested agent (1.1)

`role.yaml` may carry `suggested_agent: {capability, reasoning, independent_of}`. Read it with `ackit role list --bundle <path> --json` and use it as the role-default level of the agent-selection order (below an explicit user choice), mapping `capability` to a model through the adopter's own map. Honour `independent_of` by not reusing the agent that played that role for the same item.

## 9. Work tracking: points, runs, external_id (1.2)

A ticket in any tracker is `external_id` on a feature, task or issue. One run of a task by an agent is an appended `runs` record `{id, at, outcome, tokens?, turns?, commit?, by?}` on that task, not a new document. `points` (scale and limits in `ackit.yaml`) tells the orchestrator how to start: at or below `points.auto_start_max` start by itself, up to `points.signoff_max` wait for `signoff`, above it split the item (ACF032). Move status with `ackit status <id> <new-status> --bundle <path>`, which checks the transition and records `history`.
