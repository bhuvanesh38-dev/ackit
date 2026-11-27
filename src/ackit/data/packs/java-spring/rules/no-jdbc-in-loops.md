---
title: "No repository or JDBC call inside a loop"
severity: blocking
applies_to: [developer, reviewer]
---
## Rule

Bulk-fetch into a Map, hoist loop-invariant lookups, write with saveAll; never query per element.

## Why

Round-trips then grow with N and a list endpoint melts under real data.

## How to check

Review each loop and stream body for repository, JdbcTemplate and entity-lazy-load calls.
