---
type: decision
id: ADR-0015
title: The environment registry and the branch policy are two separate configurations
status: accepted
description: The core ships a generic environment_registry shape (with key-path mapping onto an adopter's
  own file) and a separate branch_policy; adopters accept the defaults or replace them
date: '2026-11-20'
generated:
  by: plane-session/agent
  at: '2026-11-20T11:50:00Z'
verified:
- by: human:kit-owner
  at: '2026-11-20T12:05:51Z'
- by: human:kit-owner
  at: '2026-11-23T07:08:30Z'
history:
- proposed
- accepted
---

## Context

F-002 must let one shared store serve several repositories and code lines. Two facts are needed: where code lives (which environment uses which branch of which repository at which stage) and how work and context branches are created. The first adopter already has the first in its `environments/registry.yaml` (each environment carries a `code_line`, `stages.<stage>.branches.<repo>`, `defaults.development_stage`, `code_repos`) and agent-orchestly reads a generic form of it through an `EnvironmentRegistry` whose key paths are options. The developer decided on 2026-11-20 that the two are different configurations, that the kit ships a basic default for both, and that every name reflects its purpose.

## Options

1. One combined block (environments plus branch rules).
2. Two blocks: `environment_registry` (facts) and `branch_policy` (rules).
3. Ship nothing; each adopter brings its own registry and rules.

## Decision

Option 2, in ACF 1.3, optional in `ackit.yaml`; each block may carry `file:` to live in its own file.

`environment_registry` resolves, from inline data or from `source_file`, to one internal model: `default_stage`, `repositories`, `environments` (`id`, `repository`, `code_line`, per-stage `branches` per repository) and an `extensions` map the core never reads (tenants, infrastructure). `key_paths` map an adopter's own file onto the model; the defaults are the shape orchestly's generic adapter already uses. The first adopter's file maps with `default_stage: defaults.development_stage`, `repositories: code_repos`, `code_line: code_line` and the default `stages.${stage}.branches.${repo}`; its overlay under `adopters/` carries that mapping.

`branch_policy` holds `work_branch` (`base_stage`, default the registry's `default_stage`; `name_pattern`) and `context_branch` (`base`: `matching-code-base-branch` or `default-branch`; `fallback`, default `main`; `name_pattern`, default `{author}-{code_branch}`; `required_before_code_push`).

## Why

Facts change when environments are added; rules change when a team changes how it works. Separate blocks let an adopter change one without touching the other, and an adopter with its own registry only maps it. Option 3 would leave every adopter re-implementing the same lookup, which is how orchestly and the store came to have two.

## Consequences

Easier: one lookup for both the work branch and the store branch. Harder: the kit now owns a small reader that overlaps orchestly's; see ADR-0016 for who owns it. The first adopter's mapping must be tested against the real file. Existing bundles have neither block and behave exactly as before. Supersedes: none.
