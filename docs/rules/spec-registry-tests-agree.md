---
type: rule
id: R-spec-registry-tests-agree
title: SPEC, registry and tests change together
status: draft
severity: blocking
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Rule

A changed validation rule, type or status set updates SPEC.md, types.yaml or RULE_TEXT, and a test that makes it fire, in the same commit.

## Why

The spec is the product; a registry or test that drifts from it makes the validator lie.

## How to check

`tests/test_validate.py::test_every_rule_has_a_case` passes and the diff touches all three.
