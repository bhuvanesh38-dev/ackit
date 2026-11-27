---
type: decision
id: ADR-0018
title: Concurrent writers use reserved id ranges per author
status: superseded
superseded_by: ADR-0020
description: id_allocation offers sequential (default) and reserved-range strategies; author-prefixed
  ids are not shipped because they change the id patterns
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
- superseded
---

## Context

`ackit new` takes the next id from the current bundle, so two authors on different branches can both create `T-005`; ACF009 only fires after the merge. orchestly's roadmap already lists `T-001` clashes across jobs.

## Options

1. Keep sequential allocation and rely on ACF009 at merge.
2. `reserved-range`: each author owns a numeric range (for example 1000 to 1999) set in configuration; `ackit new` allocates inside the author's range.
3. `author-prefixed`: ids such as `T-bh-001`.
4. Random ids.

## Decision

Options 1 and 2 ship in ACF 1.3 as `id_allocation: {strategy: sequential | reserved-range, ranges: {<author>: [low, high]}}`; the default stays `sequential`. `ackit new` takes the author from `--author` or configuration, and refuses to allocate outside the range or past its end. ACF009 is unchanged.

## Why

A reserved range keeps ids numeric and readable and leaves every id pattern (ACF016) and every consumer regex alone, so it is additive. Author-prefixed ids change the patterns and break consumers; random ids lose readability.

## Consequences

Easier: no clash by construction for authors who have a range. Harder: ranges need an owner who hands them out and a rule for authors without one (they fall back to sequential and may clash; the test plan covers it). Not proven yet: the plan includes a two-writer concurrency test before this ADR is accepted. Supersedes: none.
