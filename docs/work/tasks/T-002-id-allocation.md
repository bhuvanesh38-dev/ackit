---
type: task
id: T-002
title: id_allocation with reserved ranges
status: done
feature: F-002
points: 3
depends_on:
- T-001
signoff:
  by: human:kit-owner
  at: '2026-11-20T12:51:13Z'
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.2.1
  at: '2026-11-20T11:59:04Z'
---

<!-- ACF task: A unit of work under a feature, small enough for one agent session.
  writes: planner or developer | reviews: reviewer | signs off: reviewer
  update when: status changes
  rules:
  - Names the module(s) it touches.
  - Acceptance criteria are checkable.
  - `points` (optional) is in the configured scale; above `signoff_max` it is split before it is ready, above `auto_start_max` it needs `signoff`.
  - `runs` (optional) records each run: id, at, outcome, and optionally tokens, turns, commit, by.
-->

## Goal

Implement ADR-0018 as restated by ADR-0020: `id_allocation` (`sequential` default, `reserved-range`), `ackit new --author`, refusal for a missing author, an author without a range and a full range, `ackit ids assign`, rule ACF037. Version becomes 1.3.0 here. Touches: new `idalloc.py`, `scaffold.py`, `cli.py`, `validate.py`, `SPEC.md`, `CHANGELOG`.

## Acceptance criteria

- Without the key, `ackit new` allocates exactly as before (guard from T-001 passes)
- With ranges, a new id is inside the author's range and a full or unknown range is refused with a clear message
- Proof P2: two author clones create ten items each in parallel; after merging both ways ACF009 reports no clash with ranges and does report the clash without them; result saved as test-evidence
- ACF009 and ACF016 are unchanged
- A missing author, an author without a range and an invalid `id_allocation` are refused with a message, never guessed (no sequential fallback)
- `ackit ids assign <author>` adds the next free range touching only that block, and writes nothing when the result would not validate
- ACF037 reports an unusable `id_allocation`
