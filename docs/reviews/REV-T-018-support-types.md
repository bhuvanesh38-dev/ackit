---
type: review
title: 'Review of T-018: the three support types'
item: T-018
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T23:00:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-23, of the three type entries against the signed-off design, the templates against the real ticket-resolution template, the tests, and how `ackit new` treats a type with no directory and no id.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | major | The enum check used Python equality: `1.0` and `true` passed as `resolution_type: 1` | Compared by type and value; negative controls for 1.0, 2.0, true and a list |
| 2 | major | `ackit new ticket-resolution` silently wrote `resolution_type: 1` (a data fix), which passed validation | A numeric choice is not defaulted; ACF004 reports it; tested |
| 3 | minor | The template lost the real template's per-type prompts and did not say what to do for a ticket of several types | Per-type prompts restored as prose; pick the primary type and name the others |
| 4 | minor | The test for missing keys was vacuous for `title`; sections were matched by substring; human verification at stable was only a registry flag; no control for ACF022; only one type tested at nested paths; the DOC-TYPES test checked a heading only | Each fixed: exact message matches, ACF011 behaviour per type, an ACF022 control, all types at nested paths, the reference compared with generated output |
| 5 | minor | The optional keys are documented but nothing checks them; pages that were an unknown type before now get checks | Said in the evidence; vocabularies are T-019; the behaviour change goes into the 1.4 changelog (journal) |
| 6 | nit | `ackit new` cannot create the nested casebook path; two long titles can collide in the flat root | Stated in the evidence; `--slug` resolves a collision; the layout is the adopter's |

## Resolution

Findings 1 to 4 fixed and verified; 5 and 6 recorded. The reviewer confirmed the entries match the design, the guard test is unaffected, ints stay ints through the frontmatter, and `new` cannot overwrite a page.

## Verdict

approve.
