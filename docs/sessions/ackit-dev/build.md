---
type: session
title: ackit build sessions
author: ackit-dev
status: draft
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

# ackit build sessions

## 2026-11-23 (Mon, W48) - f-002-shared-store @ b3e23ee - session heading rule (F-005)

**Done:** F-005 built as task T-023: rule ACF045 (the session entry heading shape, a warning by default, an error with `severity: {ACF045: error}`), the on-hold status set documented in SPEC and ADOPTION with a test, CHANGELOG. ACF021 is unchanged. The kit's own first session entry now says `@ none`.

**Faced:** The owner asked why ACF021 is not tightened (kept separate: own severity, no upgrade break, reversible; see the journal). My earlier advice to sign off F-005 with `--status signed-off` was wrong (not a feature status); fixed by moving it to ready.

**Decisions:** ACF045 checks shape only. See the F-005 journal.

**Build:** full suite and `ackit validate docs --strict` pass; the guard test passes with its baseline unchanged.

**Next:** F-004 (T-018 to T-022). the support assistant can set `severity: {ACF045: error}` and drop its own check after a release.

**Blockers:** none

## 2026-11-23 (Mon, W48) - f-002-shared-store @ 8a0a14a - one owner for each gate check (F-003)

**Done:** F-003 tasks T-013 to T-017: the ownership table and overlay entries, an equivalence harness that runs the store's gate on a scratch copy directly and through the kit (with safety guards, a loopback tracker stand-in and limits measurement), 39 commit-time and 18 push-time cases, and a result table for all 17 checks (`equivalence/RESULTS.md` in the adopter overlay). E-002 criterion 3 now states what the table proves. F-004 and F-005 were designed and signed off by the owner; F-005 is ready.

**Faced:** The gate prints its collected warnings once, so the warnings of checks 8 to 11 never show (proven by their hint lines instead; recorded in the journal); a tracker answer carried between cases and a hook that ran nothing were both harness faults found by review; T-017 had 3 points and no human sign-off, so it waited as blocked until the owner signed.

**Decisions:** ADR-0021 (ticket links stay in the tracker). The results table claims one firing condition per check and lists the rest. Kit commits carry no tool trailer.

**Build:** `ACKIT_BETA_STORE=<store> .venv/bin/python -m pytest -q`: 358 passed, 1 skipped; `ackit validate docs --strict`: 0 errors. The real build and a real tracker were not run.

**Next:** F-003 review and done; then F-004 (T-018 to T-022; T-022 waits on real resolutions) and F-005 (ACF045). Later decisions: entry-file size, stage conversion, how to close F-002.

**Blockers:** none

## 2026-11-20 (Fri, W47) - main @ 581a93a - shared-store epic and analysis stage

**Done:** Epic E-002 (shared store support, ACF 1.3) and large feature F-002 created with `ackit new`; the epic, the feature and the first stage `01-analysis` written from the store's own design document, gate script, registry, sync hook, the AX pipeline and a read-only evaluation of store against kit. Journal and log entries added. The Plane session took over as the kit's owner session for this work.

**Faced:** The first reading in this session took the in-repository bundle as the kit's intended main use; the developer corrected it (the kit is meant for the shared store). The evaluation read about 21 of the store's 646 Markdown files; the rest rests on counts and grep, and SPEC.md was not read in full.

**Decisions:** Kit first, then an orchestly pilot, then the store (see the journal). No code before the F-002 design stage is signed off.

**Build:** `.venv/bin/ackit validate docs --strict`: 56 documents, 0 errors, 0 warnings. No source code changed, no tests run.

**Next:** `01-analysis` was signed off the same day; `02-design` and ADR-0015 to ADR-0019 (proposed) are written. The developer signs off or amends the design; then `03-plan`. Corrections made on the way: the registry already exists (store and orchestly), the kit ships a generic registry shape and default branch policy, two separate configs, `code_lines` instead of `lines`. Not proven: the first adopter's registry mapping, the two-writer id test, per-line document counts.

**Blockers:** none

## 2026-11-19 (Thu, W47) - main @ 7d9ea30 - ACF 1.2: points, runs, status command

**Done:** ACF 1.2 (points, runs, external_id; ACF031 to ACF034), `ackit status`, `ackit new --slug`, capped default slug, history on create, legal values in validator messages. I-002 tracked with the new commands; left at in-review.

**Faced:** The brief said `external_id` already existed; it did not (only a pass-through key), so it is now defined. The `new` command defaults an enum field to its first value (an issue got `severity: critical` unless set).

**Decisions:** ADR-0014 (proposed); see the journal.

**Build:** `.venv/bin/python -m pytest -q` and `ackit validate docs --strict`; see EV-I-002.

**Next:** A person reviews I-002; orchestly reads and writes the new fields against a real run.

**Blockers:** none

## 2026-11-17 (Tue, W47) - main @ none - build the kit v0.1

**Done:** Spec, type registry, validator (30 rules), gates, ten roles with overlays and custom roles, five stack packs, prompt generation with explain, import, CLI, tests.

**Faced:** The sandbox venv has no network; dependencies were copied from an existing environment. YAML `off` parsed as false.

**Decisions:** ADR-0002 to ADR-0012; see the journal.

**Build:** `.venv/bin/python -m pytest` passes; `ackit validate docs --strict` passes.

**Next:** Verify the important documents by a human; F-001 packaging.

**Blockers:** none
