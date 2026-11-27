---
type: workflow
title: shop-platform workflow
description: Build, test, lint and review flow
status: draft
commands:
  build: ./gradlew build -x test
  test: ./gradlew test
  lint: ./gradlew check
  run: ./gradlew bootRun
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:40Z'
---

# Workflow

## Commands

| Task | Command |
|---|---|
| build | `./gradlew build -x test` |
| test | `./gradlew test` |
| lint | `./gradlew check` |
| run | `./gradlew bootRun` |

## Branching and review

Branch naming, PR flow, who reviews, who merges. Merging is a person's decision.

## Definition of done

- Build and tests pass (commands above), evidence recorded as a test-evidence record
- Reviewed (review record, verdict approve), security checklist run when the change touches auth, input or data
- Journal updated with any decision or correction
- Session entry written
