---
type: decision
id: ADR-0019
title: Process checks, author workspaces and consumer layout are adopter configuration
status: accepted
description: The core defines a contract for adopter process checks, an owned per-author workspace and
  a configurable consumer layout; every organisation-specific value lives in the adopter's own overlay under adopters/
date: '2026-11-20'
generated:
  by: plane-session/agent
  at: '2026-11-20T11:50:00Z'
verified:
- by: human:kit-owner
  at: '2026-11-20T12:05:51Z'
history:
- proposed
- accepted
---

## Context

The store runs 17 commit and push checks: about 7 about context documents, about 10 about code and process (protected branches, migration naming, store pull request before code push, no replaced remote commits). It keeps `developers/<user>/` (312 of 646 Markdown files) and exposes `AGENTS.md` and `rules/` to Claude Code and AX at fixed paths. The kit has validation rules for documents only, a per-author session layout, and `ackit check --gate start|handoff` for work items (a different thing, so the name `gates` is not reused).

## Options

1. Put the store's checks and paths into the core.
2. Define contracts in the core; the adopter fills them in configuration.
3. Leave all three to adopter scripts outside the kit.

## Decision

Option 2, ACF 1.3, all optional.

- `process_checks`: a list of `{name, level: block | warn, when: pre-commit | pre-push | on-demand, run: [argv...], description}`. `ackit checks run --when <point>` runs the commands without a shell; exit 0 is pass; a failing `block` exits 1, a failing `warn` prints. The core ships no check. The seven document checks map to existing ACF rules; the ten code and process checks become entries in the adopter's overlay under `adopters/`, including the store-pull-request-before-code-push check (ADR-0016).
- `author_workspace`: `{root: "developers/{author}", in_index: false}`. Documents under it must carry `author` equal to the folder name (ACF036, warn); they are left out of shared index budgets; the append-only rules still apply.
- `consumer_layout`: `{entry, entry_links, rules_dir, rules_links}`. `ackit link --check` verifies the links; creation stays with `ackit init --link-entry` and the adopter's installer. The first adopter sets `AGENTS.md`, `.claude/CLAUDE.md`, `rules/`, `.claude/rulebook`.

The store's stage names (analysis, frs, tdd, test-plan, implementation, journal) are mapped to the kit's in the adopter overlay's `mapping.yaml`; the core stage names do not change.

## Why

The checks that matter most are process facts the kit cannot know offline, so the core offers a place and a contract and no content. Fixed paths belong to the consumers (Claude Code, AX), not to the standard.

## Consequences

Easier: the store's hooks call one command instead of one script per check, and any adopter can do the same. Harder: running adopter commands is the one place the kit executes code it did not write, so the commands are listed in a reviewed file and run without a shell. The concurrency test, the mapping and the registry mapping are all proven in the plan stage, not here. Supersedes: none.
