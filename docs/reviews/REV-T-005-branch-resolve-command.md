---
type: review
title: 'Review of T-005: ackit branch resolve'
item: T-005
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T15:30:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-20, covering T-004 and T-005 together: `src/ackit/branchpolicy.py`, `ackit branch resolve`, ACF039, `tests/test_acf13_branches.py`, SPEC and the changelog. The reviewer ran the branch tests.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | `branchpolicy.py` pattern check | major | Patterns with format specs or conversions (`{author:d}`, `{author:{bogus}}`) passed validation and crashed at resolve time | Such patterns are refused by ACF039; five cases tested |
| 2 | `cli.py` branch list file | minor | A missing or undecodable file gave a traceback | Exit 2 with a message; tested |
| 3 | `branchpolicy.py` | minor | An empty author, task or branch silently gave no name | Refused with a message (exit 1); tested |
| 4 | `branchpolicy.py` | minor | Names are not checked as git refs | Stated in SPEC and the module: the caller checks; accepted |
| 5 | `cli.py`, SPEC | minor | The `--code-base-branch` default was undocumented and not shown | SPEC states it; output has `code_base_branch`; tested |
| 6 | `cli.py` | minor | An unknown `base_stage` exits 1 at resolve time, not 2 | Accepted: it is a resolution failure; tested |
| 7 | tests | minor | Purity test did not guard file opens; no end-to-end ACF039; CLI paths untested | Added: open and `read_text` guarded, ACF039 through `validate`, file list, repository, explicit base, bad policy |
| 8 | evidence | minor | Proof P1 not recorded | Recorded in `EV-T-005-branch-resolve-command.md` |

## Resolution

Finding 1 fixed; 2, 3, 5, 7 and 8 fixed or recorded; 4 and 6 accepted with the reasons above. Verified: 25 branch tests pass.

## Verdict

approve.
