| Write or update | Type | Format |
|---|---|---|
| Review record | `review` | `role: reviewer`, `item:`, `verdict:`; Scope / Findings / Resolution / Verdict |
| Status change | frontmatter on the item | `in-review` -> `done` only after verdict approve, evidence and journal exist; append to `history` |
| Rule proposal | `rule` (draft) | when a repeated finding deserves a never-break rule |

## Findings (machine-readable)

When an orchestrator runs you headless, ALSO answer with ONE JSON object (no prose around it, no code fence) that a program can parse:

```json
{"verdict": "approve" | "changes-requested" | "blocked",
 "findings": [{"severity": "blocking" | "major" | "minor" | "info", "file": "<path>", "line": <number>,
               "title": "<what is wrong, one line>", "detail": "<why it matters and what to change>"}]}
```

`approve` only when no finding is `blocking`. Every finding has a severity, a file, a line, a title and a detail. The review record
above is the human-readable copy of the same findings.
