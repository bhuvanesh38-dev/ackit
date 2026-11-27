---
type: decision
id: ADR-0020
title: Authors without an id range are refused; ranges are assigned through the shared file
status: accepted
description: Restates ADR-0018 without its stale consequence. An author with no range is refused, never
  given sequential ids; ackit ids assign adds the next free range to ackit.yaml
date: '2026-11-20'
supersedes:
- ADR-0018
generated:
  by: plane-session/agent
  at: '2026-11-20T14:20:00Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T06:58:18Z'
history:
- proposed
- accepted
---

## Context

ADR-0018 introduced `id_allocation` with `sequential` and `reserved-range`. Its Decision says `ackit new` refuses to allocate outside the author's range; its Consequences says an author without a range "falls back to sequential and may clash". The two disagree, and a reader of the ADR alone cannot tell which one the tool does. A second question came up while building it: how does a new author get a range at all, and why can the tool not simply pick one.

## Options

1. Keep the fallback: an author without a range gets sequential ids.
2. Refuse, and tell the developer to add a range by hand.
3. Refuse, and provide a command that adds the next free range to the shared `ackit.yaml`.
4. Let `ackit new` create a range on the author's own branch the first time it is needed.

## Decision

Option 3 (ACF 1.3). The strategies, ranges, `--author` and `$ACKIT_AUTHOR`, ACF037 and ACF009 are as in ADR-0018. An author with no range, a missing author and a full range are refused (exit 2) with a message that names the fix. `ackit ids assign <author> [--size N]` (default size 1000) adds one line, `<author>: [low, high]`, to `id_allocation.ranges` in `ackit.yaml`: the block starts after the highest existing range (or at 1000), so it cannot overlap one; the rest of the file, comments included, is untouched; nothing is written if the result would not validate. The line must reach the shared branch before the author creates items.

## Why

A silent fallback recreates the clash that reserved ranges exist to prevent, and it shows up only at merge. Option 4 fails the same way: two branches each create "the next" range and both pick the same block. The safe rule is that a range is agreed in the shared file first and used second; the command makes that one step easy without hiding it.

## Consequences

Easier: a new person or agent gets a range with one command and a merge. Harder: they cannot create items until that merge happens. Two branches that both assign a range before merging may pick the same block; the merge then conflicts or ACF037 reports the overlap, so it is visible. A `fallback: sequential` option is not provided; an adopter that wants it needs a new decision. Supersedes: ADR-0018 (its Consequences sentence about a sequential fallback is replaced by this decision; everything else in it stands).
