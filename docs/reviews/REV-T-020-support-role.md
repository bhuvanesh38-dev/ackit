---
type: review
title: 'Review of T-020: the support role'
item: T-020
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-24T10:30:00Z'
---

## Scope

An independent read-only review by a separate agent of the role's five parts and prompt guide against the design, the base prompt, an existing role and the type rules, with the prompt rendered in a scratch bundle.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | minor | The role said to leave `resolution_type` empty and ask, but it is required and the checklist wanted no validation error | The prompt and checklist say an empty value is a known error while its question is open |
| 2 | minor | The base prompt says "ask for a work item" while the mission works from ticket evidence | The mission says a work item is optional and to ignore that line; a test checks the order |
| 3 | minor | Nothing said the role may run only read-only queries; `verified_at_commit` could be filled | Both added to the prompt and the rules |
| 4 | minor | Questions "at the end of the page" and "under the section" disagreed | One form: under the section, starting with `Question:` |
| 5 | minor | The guard-rail test searched the whole output, and the no-item test checked only a title | Tests assert the prompt and the rules separately, the override order, and `gates: -` |
| 6 | nit | A rule against editing a verified page clashed with "updated when the ticket is reopened"; the owner text of `platform-behaviour` said only developer | The rule gives the route (a new page naming the old one); the owner text says developer or support agent |

## Resolution

All findings fixed. The reviewer found nothing unsafe: nothing in the prompt lets the agent verify, commit or push; `run-readonly-queries` is a valid tool name used by other roles; an empty `gates` list works in validation, the role list and the responsibilities table.

## Verdict

approve.
