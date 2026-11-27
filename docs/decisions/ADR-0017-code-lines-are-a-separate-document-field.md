---
type: decision
id: ADR-0017
title: Code lines are a separate document field, not an extension of applies_to
status: accepted
description: Documents carry an optional code_lines list; validate and prompt accept a code line; ids
  are checked against the registry when one is configured
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

A rule can be true only for one code line (a Java 11 line versus a language-level 21 line). Today `applies_to` narrows a rule by module or role (it is read as roles in the prompt builder), and `modules` names modules. The store registry already names a code line `code_line`.

## Options

1. Reuse `applies_to` with line ids mixed in.
2. A new optional field `code_lines`.
3. No field; scope only by branch (one store branch per line).

## Decision

Option 2 (ACF 1.3). `code_lines` is an optional list of ids on any type. Absent or empty means every line. `ackit validate --code-line <id>` and `ackit prompt --code-line <id>` keep only documents that apply. New rule ACF035 (error): when `environment_registry` is configured, every id in `code_lines` must be a `code_line` of a known environment; without a registry the ids are free text. The name is `code_lines`, not `lines`, because `agents_md_max_lines` already uses "lines" for text lines. Branch-per-line stays the default branch policy; tags are an option, not a replacement.

## Why

`applies_to` already means two other things; a third would make every consumer guess. A separate field keeps old bundles valid. Checking against the registry catches typos, which a free-text tag would silently ignore.

## Consequences

Easier: one rule file for a line-specific fact instead of a branch copy. Harder: nothing yet measures how many store documents really differ per line (5 to 31 of 507 per store branch on 2026-11-20); the migration stage must decide which differences become tags and which stay as branch content. Supersedes: none.
