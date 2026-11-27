---
type: review
title: 'Review of T-006: code lines'
item: T-006
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T16:30:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-20, of `src/ackit/codelines.py`, ACF035, `--code-line` in `validate` and `prompt`, `tests/test_acf13_code_lines.py`, SPEC, DOC-TYPES and the P3 evidence. The reviewer ran the code-line tests.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | evidence | major | Test count overstated | Wording corrected |
| 2 | evidence | major | P3 conclusion stronger than the counts; `result: pass` with the sample undone | `result: partial`; conclusion is now a hypothesis; the unclassified parts are listed |
| 3 | DOC-TYPES, `types.yaml` | minor | `code_lines` not mentioned | Added to the rule type text; DOC-TYPES regenerated |
| 4 | `cli.py` prompt | minor | `prompt --code-line` did not check the line against the registry | Shared check, exit 2; tested |
| 5 | `cli.py` `--part` | minor | `--code-line` ignored with `--part` | Stated in the help text |
| 6 | `prompt.py` | minor | Item modules and decisions were not filtered | Both filtered; SPEC lists what is and is not filtered |
| 7 | task text | minor | Acceptance line did not match the shape check | Task wording corrected |
| 8 | `codelines.py` | minor | Whitespace in the asked line | Stripped; tested |
| 9 | `cli.py` validate | minor | Findings on other paths about an off-line document stay | Accepted and stated in SPEC |
| 10 | `validate.py` | minor | Message when no environment declares a line | Message says so |
| 11 | tests | minor | Several paths untested | The unknown-line prompt path and whitespace added; the others accepted |

## Resolution

Findings 1 to 8 and 10 fixed; 9 and 11 accepted with the reasons above.

## Verdict

approve.
