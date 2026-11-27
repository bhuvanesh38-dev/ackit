---
type: review
title: 'Review of T-015: commit-mode cases'
item: T-015
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T15:00:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-23, of the commit-mode case file, the commit-flow additions to the harness, their tests and the evidence. The reviewer read the real gate and was asked whether each expectation is tied to its check, whether the commit-flow hooks can leave the scratch folder, whether the amend and empty-commit cases really run a commit through each route, and whether the acceptance criteria are met.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | major | A "created" commit did not prove the hook ran | Each route must show the gate ran (its sections, or the kit's PASS line for the gate entry); a test with a no-op kit hook fails the case |
| 2 | major | Criterion 4 (a check skipped in both routes is reported as not proven) was not implemented, and the evidence said it was | `not_proven` and a line printed by the run; a test; check 4 is reported |
| 3 | major | Commit-flow cases never compared the two routes | A blocked commit's gate text is compared between the routes (the kit's own frame and summary lines removed); a passing commit shows the gate text in the direct route only, so only the exit state is compared there |
| 4 | minor | The guard accepted any regular-file hook inside the scratch folder | A regular-file pre-commit hook must equal the generated text exactly; tested |
| 5 | minor | The direct hook was restored outside a `finally` | try/finally |
| 6 | minor | `commit_args` were not validated (`--no-verify` would pass vacuously) | Allowlist: `--amend`, `--allow-empty`, `-q`, `-m <message>`; tested |
| 7 | minor | The entry-size case depended on the live file's size | It writes a 320-line file |
| 8 | minor | The staleness clean case had a date that would expire | A far-future date |
| 9 | minor | Several clean cases had no `match` | Matches added (and one for check 13's hint) |
| 10 | minor | The coverage test pooled verdicts across cases | It requires a clean-only case and an acting case per check, check 4 named as the one exception; tested |
| 11, 12 | nit | A header pointed at notes that did not exist; no clean `list_db` case | A note at the case; a clean `list_db` case added |
| 13 | nit | Routes always run in the same order | Left: both repositories are reset between routes |

## Resolution

All findings fixed except 13 (left on purpose) and verified: harness tests pass, the 39 commit-mode cases and the smoke cases pass on the real store source, the full suite passes.

## Verdict

approve. Each commit-time check has a case that makes it act and a clean case, the amend and empty-commit cases run through each route's real hook, and a check that nothing exercised is reported as not proven.
