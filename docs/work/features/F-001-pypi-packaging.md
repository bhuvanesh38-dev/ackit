---
type: feature
id: F-001
title: Package and publish the kit
status: draft
tier: small
epic: E-001
description: Installable wheel and a pre-commit hook entry
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Goal

`pip install` gives `ackit` and the data files.

## Acceptance criteria

- Wheel contains `ackit/data/**`.
- `.pre-commit-hooks.yaml` hook runs `ackit validate`.

## Design

setuptools package data; no code changes expected.

## Plan

1. Build the wheel in a clean venv.
2. Run the test suite against the installed wheel.

## Test plan

Install the wheel in a fresh venv and run `ackit init` on a sample repository.
