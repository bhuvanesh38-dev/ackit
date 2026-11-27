---
type: feature-stage
title: 'Design: One owner for each gate check'
status: signed-off
feature: F-003
stage: design
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:16Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T09:34:15Z'
history:
- draft
- signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-23T09:34:15Z'
---

## Approach

**Principle.** One owner for each fact. Today the adopter's gate script does all 17 checks, run by the kit through the `store-gate` entries; the store is not yet an ACF bundle, so the kit rules cannot run against it. The ownership table therefore has two columns: who owns the check today, and who owns it after the store adopts the kit.

| # | Check | Owner today | Owner after adoption | Note |
|---|---|---|---|---|
| 1 | Protected branch | gate (code clone) | gate | policy of the adopter |
| 2 | Session context | gate | rule ACF021 (format) + gate ("updated today", path) | different facts, no overlap once the format part leaves the script |
| 3, 6 | Migration naming, content | gate (code clone) | gate | build-tool and database policy |
| 4 | Build smoke test | gate (code clone, push) | gate | adopter build |
| 5 | Link integrity | gate | rule ACF008 | generic |
| 7 | Journal nudge | gate | gate (nudge, needs the staged diff); rule ACF020 owns journal format | not a split: two facts |
| 8 | Index freshness | gate | rule ACF024 | the store lists in another file; the migration maps it |
| 9 | Reference staleness | gate | gate until a field mapping exists | a field and scope difference (`last-verified` on staged files against `review_by` on all documents), not a severity one |
| 10 | Entry file size | gate | rule ACF013, budget 300, severity warn (overlay `severities`); the second file's budget stays in the gate | |
| 11, 12, 14 | Local-only leakage, traceability, SQL-in-store | gate / script | gate | adopter policy or needs git state |
| 13, 15 | Java conversions, store PR before code push | gate (code clone) | gate | adopter policy |
| 16, 17 | Dummy commits, override remote | gate | gate until a second adopter wants them | generic by nature, but one user |

Nothing moves into the kit core in this feature. The adoption PR (A5) lists the script lines the store drops once a kit rule owns the fact: the AGENTS.md part of check 10, the link part of check 5, the index part of check 8, the format part of check 2.

**What the equivalence test must prove.** Both routes run the same script, so equal exit codes alone prove little. The test targets what the kit route changes and what the live route does:
1. Per check, the verdict (`pass`, `warn`, `fail`, `skipped`) parsed from each `[n/17]` section is the same in the direct route (git hook calls the gate, as the store does today) and the kit route (hook calls `ackit checks run`), on identical repository state, with a case that makes the check fire and a clean case.
2. A check that is skipped in both routes is not proven; a check that cannot be made to fire is recorded as not proven with the reason.
3. Wrapper behaviour: the gate finds its sibling scripts through the temporary link (it resolves its own path with `readlink -f`, read in the script), the default timeout and the 64 KiB output cap hold against the gate's real runtime and output on a full copy, push-mode input reaches the gate, and an amend passes while an empty commit blocks.

**Scratch environment and safety.** The harness lives under the adopter's folder, not in the core docs. The scratch store is built from `git archive HEAD` of the store (committed files only; the live working tree is never read or changed), its `origin` is a bare repository under `/tmp`, and the scratch code clone's links point at the scratch store. The push-side check calls the issue tracker's API with the developer's credentials; the harness sets its documented test overrides (`<PREFIX>_...`, `<PREFIX>_...`, `<PREFIX>_...`, `<PREFIX>_...`) to local values so nothing leaves the machine and no real token is read. The emergency skip variable is never used.

## Alternatives

1. Compare exit codes only: rejected, both routes run the same script, so it can pass without proving anything.
2. Run on the live store: rejected, it changes shared state and the work of others; the kit does not edit the store.
3. Rebuild the checks as kit rules to make them comparable: rejected, it creates overlap and the kit has one adopter.
4. Test with the real code repository: rejected, large and slow; a scratch code repository with the needed files fires the same checks. Check 4 (the build) uses a stub build command, and the full build stays unproven in the test and is recorded so.

## Decisions

- D1. Ownership as in the table; no check moves into the core.
- D2. Check 10: the kit's size rule (ACF013) is set to warn with a budget of 300 in the adopter's overlay (`severities`, `agents_md_max_lines`), matching the gate; no code change.
- D3. Check 9 stays with the gate until a field mapping is designed; not a severity setting.
- D4. The equivalence test compares per-check verdicts on firing and clean cases, not exit codes alone.
- D5. Scratch safety rules above are mandatory and checked by the harness before any push-mode case runs.
- D6. A check not proven to fire is reported as not proven; the feature does not claim criterion 3 for it.
