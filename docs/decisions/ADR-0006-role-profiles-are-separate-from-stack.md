---
type: decision
id: ADR-0006
title: Role profiles are separate from stack packs, with overlays and custom roles
status: proposed
date: '2026-11-17'
description: Roles are directories (`role.yaml`, prompt, rules, checklist, outputs, prompt-guide). A bundle's
  `roles/<role>/` overrides any single part; `ackit role new` defines a new role; `extends` inherits missing
  parts.
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

Prompts and checklists differ by role (developer, tester, security, reviewer, business analyst, architect, designer, devops) and by team, independent of technology.

## Options

1. Hard-code roles.
2. Fold roles into stack packs.
3. Role directories with a `role.yaml` profile, per-part overlay, and a scaffold for new roles.

## Decision

Roles are directories (`role.yaml`, prompt, rules, checklist, outputs, prompt-guide). A bundle's `roles/<role>/` overrides any single part; `ackit role new` defines a new role; `extends` inherits missing parts.

## Why

What a role does does not depend on the language, and what a language needs does not depend on the role; coupling them multiplies files. Per-part overlay lets a team change one rule without forking a role.

## Consequences

`ackit validate` checks role completeness (ACF030). Role profiles and stack packs are documented separately.
