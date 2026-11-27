---
type: workflow
title: agent-context-kit workflow
description: Build, test and review flow
status: draft
commands:
  build: ''
  test: .venv/bin/python -m pytest
  lint: .venv/bin/ackit validate docs --strict
  run: ''
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:12:45Z'
---

# Workflow

## Commands

| Task | Command |
|---|---|
| test | `.venv/bin/python -m pytest` |
| validate this bundle | `.venv/bin/ackit validate docs --strict` |
| regenerate the type reference | `ackit types --markdown` (see DOC-TYPES.md) |
| regenerate the index | `ackit index --bundle docs --write` |

## Branching and review

Work on a branch, small logical commits, review before merge. Merging is a person's decision. Commit messages carry no tool trailers.

## Definition of done

- Tests pass and the bundle validates with `--strict`
- A new or changed validation rule updates SPEC.md section 9, `RULE_TEXT`, and has a test that makes it fire
- Journal entry for any decision or correction; session entry written
