---
type: workflow
title: notes-cli workflow
description: Build, test, lint and review flow
status: draft
commands:
  build: python -m build
  test: python -m pytest
  lint: ruff check .
  run: ''
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:36Z'
---

# Workflow

## Commands

| Task | Command |
|---|---|
| build | `python -m build` |
| test | `python -m pytest` |
| lint | `ruff check .` |
| run | `` |

## Branching and review

Branch naming, PR flow, who reviews, who merges. Merging is a person's decision.

## Definition of done

- Build and tests pass (commands above), evidence recorded as a test-evidence record
- Reviewed (review record, verdict approve), security checklist run when the change touches auth, input or data
- Journal updated with any decision or correction
- Session entry written
