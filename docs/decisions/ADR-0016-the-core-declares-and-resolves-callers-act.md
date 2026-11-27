---
type: decision
id: ADR-0016
title: The core declares, validates and resolves; callers read git and act
status: accepted
description: Branch policy and process checks stay offline in the core as pure resolution and validation;
  creating branches, reading git and any network call belong to the caller or to adopter commands; the
  registry file is the one opt-in local read outside the bundle
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

The architecture rule is that the core never reads outside the bundle and never uses the network. The registry is a file at the store root, outside any project folder; "enforce the branch policy" could mean three different things. Who owns the registry reader is also open, because orchestly has one.

## Options

1. The kit reads git to see which branches exist and creates the branches itself.
2. The kit resolves names and validates the policy as pure functions; the caller passes in the facts (existing branches, the code base branch) and performs the git actions.
3. The kit only documents the policy.

## Decision

Option 2. The core gains pure functions such as `resolve_work_branch(environment, repository, author, task)` and `resolve_context_branch(code_base_branch, author, code_branch, existing_context_branches)`, a validator for both config blocks, and a command `ackit branch resolve` that prints the result. The core never runs git for this and never uses the network.

Two stated changes to the architecture text: (a) `environment_registry.source_file` may point outside the bundle root; it is read only when configured, read-only, a local file; (b) adopter process checks (ADR-0019) run commands the adopter listed, and those commands may do anything; the core itself still opens no connection.

The reader is owned by the kit (`ackit.registry`, a small module with the model in ADR-0015). agent-orchestly keeps its own adapter for now; the proposal to the orchestly owner (the `rough_work` session) is to read the same key-path options so one config describes both, and to move onto the kit reader later if it wants to. Nothing in orchestly is edited from this feature.

## Why

Pure resolution keeps the offline rule, is trivially testable, and lets any orchestrator, hook or person use it. "Store pull request before code push" is a fact about a remote, so it can only be an adopter check; the kit declares `required_before_code_push` and ADR-0019 gives the adopter a place to enforce it.

## Consequences

Easier: the same resolution in a post-checkout hook, orchestly and AX. Harder: every caller must supply the existing-branch list. The architecture document and SPEC need the two amendments above. Supersedes: none.
