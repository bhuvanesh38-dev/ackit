---
title: "No unsanitised HTML injection"
severity: blocking
applies_to: [developer, security, reviewer]
---
## Rule

Never pass user-controlled strings to dangerouslySetInnerHTML or innerHTML without sanitising.

## Why

It is the commonest route to stored and reflected XSS in a React app.

## How to check

Grep the diff for dangerouslySetInnerHTML and innerHTML; each has a sanitiser.
