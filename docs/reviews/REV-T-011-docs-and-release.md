---
type: review
title: 'Review of T-011: documents for 1.3.0'
item: T-011
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T21:30:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-20, of T-011 and of F-002 as a whole: SPEC against the code (every key, command and rule ACF035 to ACF042 with severities), the architecture and README amendments, the changelog, `ackit --help`, ADR statuses, task, evidence and review records for T-001 to T-011, contradictions between the ADRs and the build, and name leakage. The reviewer ran the guard and leakage tests and the strict validation.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | SPEC, README, pyproject, INTEROP | minor | Stale "ACF 1.2" strings and "1.1 or 1.2" wording | Updated to 1.3 and "1.0 to 1.2" |
| 2 | CHANGELOG | minor | `--json` on `checks run` and `link` omitted | Added |
| 3 | task T-011 | minor | No review record yet | This record |
| 4 | journal | minor | Six differences between ADR text and build not recorded | One correction entry in the journal |
| 5 | leakage | none | No organisation, customer or person names outside `adopters/`; sibling-project and tool names only | Accepted |
| 6 | ADRs | none | No ADR accepted by an agent; ADR-0020 is `proposed` with no `verified` entry | Left for the kit owner |

## Resolution

Findings 1 to 4 fixed; strict validation clean and the suite passes.

## Verdict

approve.
