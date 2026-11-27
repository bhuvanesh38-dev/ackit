---
type: feature-stage
title: 'Analysis: Support and per-environment knowledge'
status: signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-23T09:18:42Z'
feature: F-004
stage: analysis
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:19Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T09:18:42Z'
history:
- draft
- signed-off
---

## Problem

The kit is meant to be the knowledge base that ticket resolution relies on, but it has no document type or layout for support tickets or for per-environment, per-tenant knowledge. The store holds this today as loose files: `support/` (a ticket-resolution template, examples) and `saas/<tenant>/context.md` (3 tenants). There is no per-feature documentation across environments, and the other adopter session found 0 store hits for loan penalties, bulk repayment import and loan statements.

## Findings

Facts (read 2026-11-23):

- Kit types nearest to this: `incident` (Symptom, Cause, Fix, Checks, Follow-ups), `reference`, `runbook`, `issue`. There is no `support` type and no per-environment layout rule. The kit does have `environment_registry` (ACF038) and `code_lines` (ACF035) in config.
- Store: the first adopter's store holds a `saas/<tenant>/` folder for each of 3 tenants, 4 files in all (`context.md` per tenant, one SQL file). `support/` holds `ticket-resolution-template.md` and examples. A separate support clone holds a casebook skeleton (read 2026-11-23): `saas/index.md` and `saas/log.md` only, 0 pages, written by the support-assistant session on 2026-11-20 in OKF 0.2. Its design: `saas/<environment>/<tenant>/support/` (scope tenant), `saas/<environment>/support/` (scope code-line), `saas/_platform/support/` (scope platform); inside a `support/` folder the page types are `resolutions/`, `patterns/`, `vendors/`, `platform/`. The tenant layout is therefore real but empty, and the support assistant already owns its design.
- The ticket-resolution template has sections: 1 Ticket Metadata, 2 Symptom, 3 Diagnosis, 4 Root Cause, 4a System Behavior Note (optional), 5 Resolution (six types: data fix, diagnostic query only, customer guidance, UI/config change, code fix, external vendor), 6 Verification, 7 Follow-up, 8 Tags. Its own audit says only about 20 of 262 tickets had a reusable write-up.
- The trust model already fits: agent-written documents start `draft`, a person runs `ackit verify`, ACF011 blocks `stable` without it, `review_by` marks staleness.
- The kit has no masking; customer data handling must stay with the producer (the support assistant).

## Open questions

1. Answered 2026-11-23: `ticket-resolution`, `issue-pattern` and `platform-behaviour` enter the core first; `tenant` and `vendor` are plain registered references (values the adopter registers), not document types.
2. Are `environment` and `tenant` required fields on these documents, or optional?
3. The casebook layout is settled by the support-assistant session (see findings). Does the kit adopt it as is (validate scope, environment and tenant against the folder), or define its own? Recommendation: adopt, and build nothing until a few real resolutions exist.
4. Per-environment feature documentation: one document per feature with an environments table, or one document per feature per environment?
5. Who verifies a ticket resolution as `human:`: the support assistant's design names support engineers as reviewers; the person runs `ackit verify`, and the support assistant's approve only checks the entry (agreed 2026-11-23, see the journal).

## Cross-check with the support assistant design (read 2026-11-23)

Facts: the support assistant's casebook specification (`design/knowledge/casebook.md`, D-001) already defines the page types (`ticket-resolution`, `issue-pattern`, `tenant`, `platform-behaviour`, `vendor`), their frontmatter (scope, tenants, code_line, verified_at_commit, resolution_type, tickets, sources), the body (the ticket-resolution template), and a lifecycle (agent drafts from a closed ticket, a person approves, patterns after three similar tickets, staleness by code check, deprecate rather than delete). Its log (Q-7, 2026-11-20) says the casebook lives in the store under `saas/<environment>/<tenant>/support`, grouped by environment, with support engineers as reviewers; `casebook.md` still describes a separate repository, so the two the support assistant documents disagree (asked of that session).

The kit already supports what is needed without core code: `types:` in `ackit.yaml` adds document types (SPEC section 5), OKF import and export exist (INTEROP), and the trust gate ACF011 already enforces "stable needs a `human:` verifier".

**Consequence for scope (revised 2026-11-23 on the kit owner's direction).** The support types are generic, so they belong in the kit core as proper templates, not in an adopter overlay: each is created with `ackit new`, carries the usual Writes / Reviews / Signs off roles, required sections, statuses and a role prompt, and passes the leakage test because none of it names an organisation. The overlay keeps only org settings (folder names, limits). The earlier reduction (an overlay registering the support assistant's types) is withdrawn.

Design rule: align each core type with the fields the support assistant's drafts already write (scope, tenants, code_line, resolution_type, module, tickets, sources); do not redefine them. Sections come from the existing ticket-resolution template. Roles follow the agreed flow: the support agent writes (draft, `generated.by` names the agent), a support engineer reviews and signs off through `ackit verify` (human verifier, ACF011), a developer is consulted for code claims.

Scope of the feature: (1) the core types, candidates `ticket-resolution`, `issue-pattern`, `platform-behaviour`, with `tenant` and `vendor` pages after the pilot; (2) the approval handshake (settled, see the journal); (3) a pilot of 5 to 10 real resolutions through draft, approval, validation and retrieval; (4) rules the pilot shows are missing (for example environment and tenant matching the folder). Per-environment feature documentation for developers and testers is a separate later step with its own analysis.

## Requirement added by the kit owner (2026-11-23): registered module, vendor and tenant

A `ticket-resolution` names a module, vendors and tenants, and each must be a value the adopter has registered, so the knowledge base is not split by spelling. Registered by the adopter in configuration, not fixed in the core (the same idea as `environment_registry` and ACF035 for code lines). Facts: the kit already has a `module` document type and the start gate checks that a task's named modules exist; there is no vendor or tenant registry. Open design questions for the design stage: one generic `vocabularies` config (module, vendor, tenant, each from a list, a source file, or documents of a type) versus separate configs; whether tenants come from the existing environment registry; the validation rule's severity.

## Answers recorded before sign-off (2026-11-23)

- Types in the core first: `ticket-resolution`, `issue-pattern`, `platform-behaviour`. `tenant` and `vendor` are registered references, not types.
- A resolution needs engineering effort, and so creates an issue or task, when its resolution type is data fix or code fix (to be confirmed at the design stage against the six types). The other types (diagnostic query, customer guidance, UI or configuration change, vendor issue) create no work item.
- Ticket links: ADR-0021 (proposed): sub, duplicate and related stay in the tracker; the kit links through `external_id` and the `tickets` list.
- Entry-file size, stage conversion and closing F-002: the kit owner will decide after the kit is finished.
