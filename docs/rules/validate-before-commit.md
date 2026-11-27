---
type: rule
id: R-validate-before-commit
title: Validate the bundle before committing
status: draft
severity: blocking
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Rule

`ackit validate docs --strict` must pass before every commit.

## Why

A broken bundle misleads the next agent and the next adopter.

## How to check

Run the command; exit code 0.
