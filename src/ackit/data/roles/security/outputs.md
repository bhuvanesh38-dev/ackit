| Write or update | Type | Format |
|---|---|---|
| Security review | `review` | `role: security`; findings table with file:line, severity, fix; verdict |
| Issue per confirmed vulnerability | `issue` | `severity:` set; Reproduction describes the check, never a live exploit |
| Rule proposal | `rule` (draft) | when a finding shows a missing never-break rule: Rule / Why / How to check |
| Journal entry | `journal` | `finding:` entry for accepted risks and the human who accepted them |

## Findings (machine-readable)

When an orchestrator runs you headless, ALSO answer with ONE JSON object (no prose around it, no code fence) that a program can parse:

```json
{"verdict": "approve" | "changes-requested" | "blocked",
 "findings": [{"severity": "blocking" | "major" | "minor" | "info", "file": "<path>", "line": <number>,
               "title": "<what is wrong, one line>", "detail": "<why it matters and what to change>"}]}
```

`approve` only when no finding is `blocking`. Every finding has a severity, a file, a line, a title and a detail. The review record
above is the human-readable copy of the same findings.
