---
type: review
title: 'Review of I-002: ACF 1.2'
status: final
item: I-002
role: reviewer
verdict: approve
generated:
  by: ackit/1.2.0
  at: '2026-11-19T08:44:25Z'
---

## Scope

Self-check by the implementing agent against the reviewer checklist. It is not an independent review: a person (or a different agent) should review the diff before I-002 moves to `done`; the item stays `in-review` for that.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | `src/ackit/cli.py` types listing | low | A new `- Optional frontmatter:` line appears in `ackit types --markdown`; a strict parser of that output could notice | Existing lines unchanged and in the same order; recorded in CHANGELOG 1.2.0 |
| 2 | `src/ackit/validate.py` ACF032 | low | Large estimate on `in-review` or `done` is not flagged | Intended: those items were started under an earlier rule; stated in ADR-0014 |
| 3 | `src/ackit/scaffold.py` `set_status` | low | Does not check completion rules (ACF012) when moving to `done` | The validator reports it; moving status is a separate concern from proving it |

## Resolution

Findings 1 to 3 accepted and documented; no code change needed.

## Verdict

approve for the kit change as a self-check; independent human review still required before `done`.
