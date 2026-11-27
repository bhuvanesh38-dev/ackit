---
type: journal
title: 'Journal: One owner for each gate check'
status: draft
about: F-003
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:16Z'
---

# Journal: One owner for each gate check

Append-only. Newest entry first. Never edit a past entry; correct it with a new one. Kinds: decision, correction, finding, note.

## 2026-11-23 - finding: what the equivalence runs showed

T-015 to T-017 ran every check on a scratch copy of the store, directly and through the kit. No check gave a different verdict in the two routes once the harness itself was right (the output of a very large commit is cut by the kit's 64 KiB cap); the differences found were in the harness and are fixed (the kit's framed output of a blocked commit, a hook that ran nothing proving nothing, a tracker answer carried from one case to the next). Findings about the adopter's side, for the person who owns the store: the gate never prints the warnings of checks 8, 9, 10 and 11 (recorded above, the proof for those four is the hint line); at push time the gate checks the commits being pushed, and the push cases fire only checks 4, 15 and 17, so that scope for checks 3, 5 to 14 and 16 is not shown; each row of the result table proves one firing condition of its check, and the other conditions are listed per row; the kit keeps only the last 64 KiB of a command's output, which the store's gate reaches at about 190 staged documents with two broken links each (a commit that large is unusual, and the end of the output, with the verdict, is kept). Result per check: `equivalence/RESULTS.md` in the adopter overlay.

## 2026-11-23 - decision: design drafted, equivalence test aimed at what the wrapper changes

Design, plan, tasks T-013 to T-017 and test plan are drafted. Review finding adopted: both routes run the same script, so equal exit codes prove little; the test compares each check's own verdict on a firing and a clean case, treats a check skipped in both routes as not proven, and tests wrapper behaviour (sibling scripts through the temporary link, timeout, output cap, push input). Facts read in the script: it resolves its own real path with `readlink -f`; the push-side check calls the issue tracker's API with the developer's credentials and has test overrides, so the harness must set them to local values; the store has no tests for its gate. The ownership table has two columns (today, after adoption) because the store is not yet a bundle. Check 9 is a field and scope difference, not a severity one, so it stays with the gate. Nothing is built before the design stage is signed off.

## 2026-11-23 - finding: the gate never prints the warnings of checks 8, 9 and 10

Found by the independent review of T-014 and confirmed in the script: the gate collects warnings in an array and prints it once, after check 7. The warnings raised after that point (checks 8, 9, 10 and one more, five `warn` calls in all) are never shown; only their hint lines (`Fix: ...`) print. The script's own comments at two later checks say they print directly "because the WARNINGS array is flushed above", so the author knew. This is a defect of the adopter's gate, not of the kit, and the kit does not change the script. Consequences for this feature: a case for those checks asserts on the hint line (the `info` verdict of the harness), not on a warning; a case schema note says that `warn` is matched by text across the whole output because the gate prints its warnings in one block; the owner of the store should decide whether to fix the script. Recorded for the person who decides; nothing was changed in the store.

## 2026-11-23 - decision: harness safety hardened after review

The review of T-014 found a guard bypass in the tracker-address test (a host with credentials, `http://127.0.0.1:9@evil.example`, passed), unscrubbed proxy variables, an origin guard that accepted a URL because it was resolved as a relative path, case steps that could write outside the repository or run dangerous git commands, and vacuous passes (an empty expectation, a gate that printed nothing in both routes, an exit code that disagreed with the gate's own verdict). All fixed with a test each. Also: the harness refuses to run under a git command, because the kit route would then see its arguments (for example `--amend`) and check 16 would differ between the routes.

## 2026-11-23 - correction: the severity key is `severity`, not `severities`

The signed-off analysis, design and plan say `severities` for the overlay setting that makes ACF013 a warning. The real key in `ackit.yaml` is `severity` (SPEC section on validate exit codes; read by the validator); a key named `severities` is silently ignored. The signed stages are not edited; the task text and the overlay use the right key. Found by the independent review of T-013, together with three gaps in `ackit verify`: the `--status signed-off` route did not require a person, an empty `human:` id passed, and `--signoff` overwrote an existing sign-off. All three are fixed with a test. Not fixed, recorded: a severity value other than error, warn or off is stored as written and neither counts nor fails; this is a small kit gap for a later task if a run ever needs it.

## 2026-11-23 - correction: verify did not write the sign-off block

After the kit owner signed the F-003 and F-004 analyses with `ackit verify`, validation failed (ACF027): the command recorded the verification and history but not `signoff`, which a signed-off stage needs. F-002's stages had it only because it was added by hand earlier. Fixed in `verify_doc` (writes `signoff` from the same person and moment when the status becomes signed-off, and never overwrites an existing one), with a test. The two stages were repaired by copying each one's own `verified` entry, not by a new attestation.

## 2026-11-23 - decision: scope agreed before sign-off

The kit owner agreed with the reduced scope: one owner and one severity for the 4 split checks, an equivalence test of all 17 on a scratch copy of the store, and the written contents of the adoption PR. Generic checks move into the core only when a second adopter wants them. Entry-file size, stage conversion and closing F-002 are decided after the kit is finished.

## 2026-11-23 - note: journal started

Created for F-003.
