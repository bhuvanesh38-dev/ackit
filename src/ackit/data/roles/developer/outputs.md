| Write or update | Type | Format |
|---|---|---|
| Session entry | `session` | `## date (Day, Www) - branch @ sha - title` with Done / Faced / Decisions / Build / Next / Blockers; plus one line in the session index |
| Test evidence | `test-evidence` | `item:` set, `result:` pass or fail, real command output |
| Journal entry | `journal` | `## date - decision: title` for each decision or correction |
| Module / reference docs you changed | `module`, `reference` | keep sections; update `generated.at`; drop `verified` so a human re-verifies |
| Handoff | `handoff` | when the item is finished: summary, evidence links, open items, needs a person |
| Work item status | frontmatter | move `in-progress` -> `in-review` and append the status to `history` |
