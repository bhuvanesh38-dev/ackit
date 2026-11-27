---
title: "No secrets in the repository"
severity: blocking
applies_to: []
---
## Rule

Never commit credentials, tokens, keys or personal data; read them from the environment or a secret store.

## Why

A secret in git history is public for good and costs a rotation across every environment.

## How to check

Run a secret scanner on the diff; grep the diff for key, token, password.
