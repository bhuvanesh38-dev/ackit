---
type: review
title: 'Review of T-002: id allocation'
item: T-002
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T14:10:00Z'
---

## Scope

An independent read-only review by a separate agent (not the author), 2026-11-20, of `src/ackit/idalloc.py`, `ackit new --author` and `ackit ids assign` in `src/ackit/cli.py`, ACF037 in `src/ackit/validate.py`, `tests/test_acf13_ids.py`, ADR-0018, ADR-0020, SPEC and the changelog. The reviewer read the code and did not run the tests; the author ran them after the fixes (191 passed, 2 skipped).

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | `idalloc.py` `allocate`, `validate.py` ACF037 message | major | A bad `id_allocation` was reported as "allocated sequentially", but reserved-range still ran with bad ranges and an unknown strategy silently fell back, against ADR-0020 | `allocate` raises `IdAllocationError` whenever the configuration has problems; the ACF037 message now says `ackit new` refuses until it is fixed; test `test_bad_config_refuses_allocation` |
| 2 | `idalloc.py` `assign_range` | major | The `ranges:` line was searched in the whole file; a trailing comment after a one-line mapping and CRLF files were mishandled | Only the `id_allocation` block is searched; trailing comments allowed; CRLF kept by reading and writing bytes; tests `test_assign_edits_only_the_id_allocation_block` and `test_assign_empty_flow_crlf_and_ambiguous_author` |
| 3 | ADR-0020 | major | Two branches each running `ids assign` is documented but not tested | Accepted as documented: the read-modify-write is by design, the merge conflicts or ACF037 reports the overlap; a two-clone test is added to the open items of T-011 |
| 4 | T-002 task, ADR status | minor | Task text lacked `ids assign`, ACF037 and the real file list; ADR-0020 still proposed | Task text corrected; ADR-0020 stays `proposed` until the kit owner runs `ackit verify` |
| 5 | `cli.py` `ids assign` | minor | A missing `ackit.yaml` was silently created; `--author` help did not state the refusal | `assign_range` refuses a missing file; help text states the refusal |
| 6 | `idalloc.py` | minor | An author that YAML reads as a boolean or number gave a confusing message | Refused up front with a clear message (tested) |
| 7 | tests | minor | No test for the CLI bad-author path or a one-id range | Accepted; covered by the unit tests of the refusal |
| 8 | CHANGELOG | minor | The refusal rule was not stated | Added |
| 9 | `generated.by` of ADR and evidence records | minor | The tag names a third-party tool | Accepted: records are history and the leakage test covers kit documents; later records use `ackit-dev/agent` |

## Resolution

Findings 1, 2, 5, 6 and 8 are fixed and verified (191 passed, 2 skipped; `ackit validate docs --strict` 0 errors). Findings 3, 4, 7 and 9 are accepted with the reasons in the table.

## Verdict

approve. Findings 1, 2, 5, 6 and 8 are fixed and tested; 3, 4, 7 and 9 are accepted for the reasons above.
