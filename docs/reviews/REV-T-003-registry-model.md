---
type: review
title: 'Review of T-003: environment registry'
item: T-003
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T14:40:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-20, of `src/ackit/registry.py`, ACF038, `tests/test_acf13_registry.py`, SPEC and the task, compared with agent-orchestly's reader (read only). The reviewer ran the registry tests.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | `registry.py` inline keys, SPEC | major | Docs said inline `repositories`, code accepted `repos` | Docs now say inline keys follow the key paths (default `repos`); a test uses the documented example |
| 2 | `registry.py` `_stage_branches` | major | A template such as `a.x${stage}.${repo}` passed validation then crashed | `key_paths` requires `${stage}` then `${repo}` as whole parts, once each; tested |
| 3 | task body | major | The comparison with orchestly was not recorded | A comparison table is in the task body |
| 4 | `registry.py` read | major | A binary or unreadable file crashed `validate` | `OSError` and decode errors are reported; tested |
| 5 | `registry.py` | minor | Non-string branches and wrong node types were skipped or stringified | Each is a reported problem; tested |
| 6 | `registry.py` | minor | A bad branches template silently replaced by the default could add noise | Accepted: one clear message, the default only avoids a second crash |
| 7 | `registry.py` | minor | A key path into `extensions` contradicted "never read" | Refused; tested |
| 8 | `registry.py` | minor | A non-mapping `extensions` and odd repository names passed silently | Reported |
| 9 | `registry.py` | minor | A relative `source_file` without a bundle root uses the working directory | Accepted: `validate` and the commands always pass the root |
| 10 | tests | minor | Only two open paths patched | Accepted: adequate for what `build` reads |
| 11 | SPEC | minor | ACF038 wording | Updated |

## Resolution

Findings 1 to 5, 7, 8 and 11 fixed and verified (28 registry tests pass); 6, 9 and 10 accepted for the reasons given.

## Verdict

approve.
