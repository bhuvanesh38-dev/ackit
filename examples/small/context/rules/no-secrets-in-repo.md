---
type: rule
id: R-no-secrets-in-repo
title: No secrets in the repository
status: draft
severity: blocking
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:36Z'
review_by: '2027-11-17T15:14:36Z'
---

## Rule

Never commit credentials, tokens, keys or personal data; read them from the environment or a secret store.

## Why

A secret in git history is public for good and costs a rotation across every environment.

## How to check

Run a secret scanner on the diff; grep the diff for key, token, password.
