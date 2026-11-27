---
title: "No auth tokens in web storage"
severity: advisory
applies_to: [developer, security]
---
## Rule

Keep session tokens in HttpOnly cookies, not localStorage or sessionStorage.

## Why

Any XSS reads web storage; HttpOnly cookies are out of script reach.

## How to check

Grep for localStorage.setItem with token or jwt.
