---
type: review
title: 'Review of T-001: baseline and guard'
item: T-001
role: reviewer
verdict: approve
status: final
generated:
  by: plane-session/agent
  at: '2026-11-20T13:10:00Z'
---

## Scope

An independent read-only review by a separate agent (not the author), 2026-11-20, of `tests/test_guard_baseline.py`, `tests/baselines/acf12.json` and `docs/evidence/EV-T-001-baseline-and-guard.md` against the acceptance criteria of T-001 and cases G1 to G3 of the F-002 test plan. The reviewer ran the guard and leakage tests and `ackit validate docs --strict`; it did not run the full suite (the author did: 150 passed, 2 skipped). The agent's verdict was accept with fixes. The developer asked for the review and records the final acceptance.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | `docs/evidence/EV-T-001-baseline-and-guard.md` | major | Raw validate output of kit `docs/` and orchestly's bundle was not saved, only summarised | The evidence now quotes the raw output of kit docs, orchestly (read-only) and both examples, each with its exit code |
| 2 | `tests/test_guard_baseline.py:21-55` | major | Seven of eight bundles had no findings and none used valid `points`, `runs`, `external_id` or a `severity:` mapping, so changes to those could pass | Added bundles `acf12-fields` and `severity-override`; baseline re-recorded from the unchanged source (ten bundles) |
| 3 | `tests/test_guard_baseline.py:80-89` | major | The negative control only tested the compare function on hand-edited data; the real control was a one-off script | Replaced by `test_guard_fails_when_a_real_rule_changes`, which patches the real validator (extra finding, reworded message, flipped severity, dropped finding) |
| 4 | `tests/test_guard_baseline.py:96` | minor | The extra-bundle case is skipped by default, so orchestly is not guarded in the suite | Accepted and stated in the evidence: the bundle is uncommitted and changing; its raw output is quoted instead |
| 5 | evidence text | minor | "`src/` unchanged at recording time" rests on a later `git diff` | Accepted; the command is stated and was run before each recording |

## Resolution

Findings 1 to 3 are fixed and verified (150 passed, 2 skipped; `ackit validate docs --strict` 0 errors; the leakage test passes). Findings 4 and 5 are accepted with the reasons above.

## Verdict

approve. The guard now covers ACF 1.2 fields and severity mapping and is shown to fail through the real validator.
