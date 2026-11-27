---
type: rule
id: R-no-jdbc-in-loops
title: No repository or JDBC call inside a loop
status: draft
severity: blocking
applies_to:
- developer
- reviewer
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:40Z'
review_by: '2027-11-17T15:14:40Z'
---

## Rule

Bulk-fetch into a Map, hoist loop-invariant lookups, write with saveAll; never query per element.

## Why

Round-trips then grow with N and a list endpoint melts under real data.

## How to check

Review each loop and stream body for repository, JdbcTemplate and entity-lazy-load calls.
