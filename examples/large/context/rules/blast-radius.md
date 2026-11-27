---
type: rule
id: R-blast-radius
title: Check callers before editing a shared symbol
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

Before editing a method, list its callers and every usage including strings, queries, configs and tests.

## Why

A change that suits one caller silently changes the others.

## How to check

The session entry or review names the usages found for each edited symbol.
