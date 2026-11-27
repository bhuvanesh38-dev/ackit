---
type: journal
title: 'Journal: Support and per-environment knowledge'
status: draft
about: F-004
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:19Z'
---

# Journal: Support and per-environment knowledge

Append-only. Newest entry first. Never edit a past entry; correct it with a new one. Kinds: decision, correction, finding, note.

## 2026-11-23 - finding: what the T-018 review changed

The review found that the enum check used Python equality, so `1.0` and `true` passed as `resolution_type: 1`; the check now compares type and value (no existing bundle uses a non-string enum). It also found that `ackit new` wrote the first enum value, so an unclassified ticket resolution looked like type 1, a data fix; a numeric choice is now left empty so ACF004 reports it. Two behaviour changes for T-021 to put in the changelog: a bundle that already had pages of type `ticket-resolution`, `issue-pattern` or `platform-behaviour` (an unknown type until now, ACF003) now gets the type's required-key and section checks, and an adopter overlay that defines the same type name still wins. The template for a ticket resolution restores the real template's per-type prompts (what to fill for each of the six types) and says to pick the primary type.

## 2026-11-23 - decision: types, engineering threshold, written decision record

The kit owner agreed with the reduced scope. `tenant` and `vendor` are plain registered references, not document types. A resolution of type data fix or code fix needs engineering and creates an issue or task. The ticket-link recommendation is now the decision record ADR-0021 (proposed until the kit owner verifies it). The analysis records these answers before its sign-off.

## 2026-11-23 - decision: ticket flow and links

Facts (SPEC section 4 and rules ACF018, ACF034): the kit links a task to a feature, a feature to an epic, and any item to others with `depends_on`; `external_id` is one non-empty string and is tracker-agnostic (the tracker and its key are the adopter's business, for example `tracker:3198`). The kit has no sub-task, duplicate or related-ticket link.

Decision (kit owner): a ticket in any tracker is data on a `ticket-resolution` through its `tickets` list and on an issue or task through `external_id`. The resolution carries one of the six resolution types of the ticket-resolution template. Only a resolution that needs engineering effort creates an issue or task. Ticket-level sub, duplicate and related relations stay in the tracker; several tickets with one cause share one resolution through the `tickets` list. A new link field (`parent`, `duplicate_of`) is added only if a real run shows the need. To confirm in design: which of the six types count as "needs engineering" (proposal: data fix and code fix).

## 2026-11-23 - decision: design drafted

Design, plan, tasks T-018 to T-022 and test plan are drafted from the signed analysis: three core types with templates and roles, a `vocabularies` config with rules ACF043 and ACF044 for registered module, vendor and tenant values, a core `support` role, format 1.4 (additive). Facts read: ACF022 checks only a path prefix, so `dir: ""` keeps the casebook's nested layout free of warnings; enums compare exact values, so `resolution_type: 5` works as a number; the kit has ten roles and none for support. The pilot task is blocked until real resolutions exist. Nothing is built before the design stage is signed off.

## 2026-11-23 - correction: the support types go in the kit core, not an overlay

Earlier today the scope said the kit adds no core type and registers the support assistant's types through an overlay. The kit owner corrected this: the types are generic, so they are core templates with clear writer, reviewer and sign-off roles; the overlay holds only org settings. The analysis scope is rewritten; the earlier overlay-only decision is withdrawn. The layout and approval handshake from the support-assistant session stand.

## 2026-11-23 - decision: approval handshake with the support assistant; layout confirmed

Facts from the support-assistant session (it checked its code and files): the layout in use is `<environment>/<tenant>/support/resolutions/<number>-<slug>.md` inside the store's `saas/` folder (casebook_layout "saas"); `knowledge/casebook.md` still describes a separate repository and is out of date (the support assistant will fix it only when its user says so). Its drafts carry `status: draft` and `generated.by` naming the agent; it never writes `stable` or `verified`, and no approve command exists yet.

Decision proposed by the support assistant, to be confirmed by its user: the approve step never writes `verified`. A person runs `ackit verify <page> --by human:<id> --status stable`; the support assistant's approve only checks that the entry exists, then lets its index pick the page up. `approved by <reviewer>` leaves `generated.by`, which names the agent only. This matches the kit's trust gate (ACF011) and the rule that an agent never writes a human verification. The kit side needs no change for it. `ackit validate` over the casebook runs as a gate before the support assistant index; no kit rules are built until real resolutions exist.

## 2026-11-23 - note: journal started

Created for F-004.
