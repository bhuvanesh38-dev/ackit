---
title: "Check callers before editing a shared symbol"
severity: blocking
applies_to: [developer, reviewer]
---
## Rule

Before editing a method, list its callers and every usage including strings, queries, configs and tests.

## Why

A change that suits one caller silently changes the others.

## How to check

The session entry or review names the usages found for each edited symbol.
