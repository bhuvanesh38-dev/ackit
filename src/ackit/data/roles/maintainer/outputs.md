| Write or update | Type | Format |
|---|---|---|
| Any stale or drifted document | its own type | update body, `generated.at`; remove `verified`; set new `review_by` |
| Log entry | `log.md` | `## date` heading, newest first, what changed and why |
| Index | `index.md` | `ackit index --write` |
| Decision record | `decision` | when retiring or restructuring documents |
