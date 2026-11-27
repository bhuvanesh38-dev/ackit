---
type: review
title: 'Review of T-010: first adopter content'
item: T-010
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T20:40:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-20, of the adopter overlay (`store-config.yaml`, `stage-mapping.yaml`, `CHECKS.md`, its test) and the evidence, against the real store (read only): the gate script's 17 checks, the script paths, the registry keys and the layout. The reviewer ran the overlay and leakage tests.

## Findings

| # | File:line | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | evidence | major | The evidence named the organisation and failed the leakage test | Rewritten with neutral paths; leakage test passes |
| 2 | `store-config.yaml` | major | `run` paths did not resolve from the stated working directory; the gate runs in commit mode and skips the code checks | Paths relative to the store root, verified against the real layout by a test; description states the mode |
| 3 | `store-config.yaml` | major | The Java conversions entry could never fail (diff on standard input, exit 0) | Entry removed; check 13 is hook only |
| 4 | `store-config.yaml` | major | Checks 15 and 17 were vacuous under the kit (pushed refs on standard input) | Entries removed; hook only with the reason |
| 5 | `CHECKS.md` | major | Four of the six rule mappings were not the same fact | Dispositions rewritten (rule, rule plus gate, entry, hook only) with each gap; `agents_md_max_lines: 300` added |
| 6 | task, ADR, plan | minor | The seven and ten split contradicted the result | Task wording corrected; the journal records the correction (signed-off documents are not edited) |
| 7 | `stage-mapping.yaml` | minor | A separate file from the `mapping.yaml` ADR-0019 names; not validated by code | Stated in `CHECKS.md`; left as a note for the migration stage |
| 8 | `CHECKS.md` | minor | The traceability script audits all folders | Stated |
| 9 | store `rules/` | minor | Symlinks leave the bundle | Stated |
| 10 | tests | minor | Convoluted assertion; no path check; hand-made registry | Simplified; a real-layout test runs when the store root is given; P1 already ran the real registry |

## Resolution

All ten fixed or recorded; five tests pass, the real-layout test with the store root given.

## Verdict

approve, with the corrected scope: two entries and seven hook-only checks.
