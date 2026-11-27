---
type: decision
id: ADR-0021
title: Ticket links stay in the tracker
status: accepted
description: A ticket in any tracker keeps its sub, duplicate and related relations in that tracker; the
  kit links tickets only through external_id and the tickets list
date: '2026-11-23'
generated:
  by: ackit/1.3.0
  at: '2026-11-23T09:15:44Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T09:18:27Z'
history:
- proposed
- accepted
---

<!-- ACF decision: Architecture or process decision record (ADR) - what was decided and why.
  writes: planner or developer | reviews: reviewer | signs off: human owner
  update when: never edited once accepted - superseded by a new record
  rules:
  - Options lists at least two options.
  - Why states the deciding reason, not a restatement.
  - `supersedes` and `superseded_by` are reciprocal.
-->


## Context

Support tickets live in a tracker (a ticket tracker today, any other later). The kit stores the knowledge that comes out of them: a `ticket-resolution` document, and, only when engineering effort is needed, an issue or task. The kit already links a task to a feature, a feature to an epic, and any item to others with `depends_on`; `external_id` is one tracker-agnostic string (ACF034). It has no sub-task, duplicate or related-ticket link. The question: should the kit add them for tickets?

## Options

1. Add link fields to the kit (`parent`, `duplicate_of`, `related`): the kit could answer "which tickets duplicate this one" without the tracker. Cost: a second copy of relations the tracker already owns, kept in step by hand, with new validation rules and a format change for a need no run has shown.
2. Keep ticket-level relations in the tracker; link only through `external_id` (a work item) and a `tickets` list (a resolution): nothing to keep in step, no format change. Cost: the kit cannot show the tracker's relation graph on its own.

## Decision

Option 2: sub, duplicate and related relations between tickets stay in the tracker; the kit links a ticket through `external_id` on an issue or task and through the `tickets` list on a `ticket-resolution`, and adds `parent` or `duplicate_of` only if a real run shows the need.

## Why

The tracker already owns these relations and the people who change them work there, so a copy in the kit would drift. Several tickets with one cause need no duplicate link: they share one resolution through the `tickets` list. Building a link no run has asked for is the cost the kit owner wants to avoid (build only on run evidence).

## Consequences

Easier: no new fields or rules; the format version does not change; any tracker fits. Harder: a reader who wants the relation graph opens the tracker. Next: F-004 designs `ticket-resolution` with a `tickets` list; a resolution of type data fix or code fix (needs engineering) creates an issue or task whose `external_id` carries the ticket key. Revisit if a pilot run shows a link is missed. Supersedes: none.
