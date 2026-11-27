---
type: handoff
title: 'Handoff: F-002 build, next session starts at T-002 review and T-003'
status: draft
item: F-002
generated:
  by: ackit/1.3.0
  at: '2026-11-20T13:22:37Z'
---

## Summary

**Vision.** The kit (`ackit`, format ACF) is a generic, configurable framework like OKF. An adopter configures everything; the kit validates and enforces that configuration; the kit names no company. The first adopter is a company whose `agent-context` store has conventions and scripts but no framework. Order the developer set: (1) finish the kit (this feature, F-002 / epic E-002), (2) enforce it in agent-orchestly, (3) in the Ansible work, (4) last, in the agent-context store. The kit stays local (no remote, no publishing), owner is the developer (`human:kit-owner` in the kit's own records).

**Where we are (2026-11-23).** The build is finished. ADR-0015 to ADR-0017, ADR-0019 and ADR-0020 are accepted (ADR-0018 is superseded by ADR-0020, verified by the kit owner on 2026-11-23). Tasks T-001 to T-012 are `done`, each with an evidence record and an independent review record. F-002 is `in-review`: its handoff gate fails only on "test evidence passes", because `EV-F-002-shared-store-build` is honestly `partial` (four epic criteria need the store migration or the orchestly pilot). E-002 stays open. The suite is 303 passed, 3 skipped; `ackit validate docs --strict` is clean. Nothing is committed.

What is left for the kit: the owner decides whether F-002 closes as the build half (then the evidence is split or the criterion scoped) and when to commit; proof P3's 20-document sample needs a person. After that: the orchestly pilot, then Ansible, then the store migration (separate work; not started here).

**How to work here (read first).**
- Repo: the local `agent-context-kit` checkout; use `.venv/bin/python -m pytest -q` (168 passed, 2 skipped at hand-off) and `.venv/bin/ackit validate docs --strict` (76 documents, 0 errors). Re-index with `ackit index --bundle docs --write`.
- Move a task with `ackit status <T-nnn> <status> --bundle docs` (draft, ready, in-progress, in-review, done); a done task needs an evidence record (`docs/evidence/EV-T-nnn-*.md`, type test-evidence) and a review record (`docs/reviews/REV-T-nnn-*.md`). Use a separate read-only reviewer agent for the review, then fix its findings.
- The guard `tests/test_guard_baseline.py` pins how ten old-style bundles validate; it must stay green after every change. Re-record `tests/baselines/acf12.json` only on purpose (`ACKIT_UPDATE_BASELINE=1`), never to hide a change.
- The leakage test (`tests/test_examples.py::test_core_has_no_adopter_specifics`) fails on any company, customer, repository or personal name outside the first adopter's overlay folder under `adopters/`. Write "the first adopter", "the adopter's overlay", "the kit owner". This is why the F-002 documents were reworded once.
- Never write human attestations (`signoff`, `verified`, `ackit verify`) in bulk or on your own; the permission classifier blocked that once. A signature the developer states in words may be recorded for the specific item; the ADR verifications are the developer's own command.
- Never edit agent-orchestly, the agent-context store, the infrastructure repository or Plane from this work. Peer: `rough_work` is the orchestly session (it reorganised its bundle with ackit 1.2.1; seven questions answered by message). Nothing leaves this machine.
- A signed-off stage is not edited; corrections go to the journal. ACF numbers: 035 reserved for `code_lines`, 036 for the author workspace, 037 is used (`id_allocation`).

**Design facts the next tasks rely on** (full text in `/work/features/F-002-shared-store/02-design.md` and ADR-0015 to ADR-0020).
- Two separate configs in `ackit.yaml`, each optionally in its own file: `environment_registry` (default stage, repositories, environments with a code line and a branch per repository and stage, free `extensions`; `source_file` and `key_paths` map an adopter's own file onto the model, and `source_file` may be outside the bundle: the one opt-in local read) and `branch_policy` (`work_branch.base_stage` defaulting to the registry's default stage; `context_branch` with `base: matching-code-base-branch`, `fallback: main`, `name_pattern: "{author}-{code_branch}"`, `required_before_code_push`).
- The default branch policy: the work branch is created from the environment's default-stage (UAT for the first adopter) branch; the store creates its context branch the same way from the store branch that matches the code base branch, else `main`.
- ADR-0016: the core only resolves and validates (pure functions, no git, no network); callers pass the existing-branch list and act. `ackit branch resolve` prints results.
- The first adopter's registry maps with `default_stage: defaults.development_stage` and `repositories: code_repos`; the other key paths equal the generic defaults that orchestly's yaml adapter already uses (`environments`, `id`, `repo`, `stages.${stage}.branches.${repo}`). Read, not yet run: proof P1 in T-005 decides.
- Names: `code_lines` (not `lines`), `process_checks` (not `gates`, which already means work-item start and handoff checks), `author_workspace`, `consumer_layout`, `id_allocation`.

## Evidence

- `/evidence/EV-T-001-baseline-and-guard.md` and `/reviews/REV-T-001-baseline-and-guard.md` (T-001 done).
- `/evidence/EV-T-002-id-allocation.md` (T-002; proof P2, two writers merged in both orders, passes with ranges and shows duplicates without).
- `/work/features/F-002-shared-store/06-journal.md` (decisions, corrections, the leakage-test conflict and its fix, the ADR-0018 contradiction).
- Stage documents `01-analysis` to `05-test-plan` in `/work/features/F-002-shared-store/`.

## Open items

1. Decide how F-002 closes (see above) and commit the kit when the owner chooses.
2. Proof P3 sample (20 documents per code-line branch) by a person.
3. Later stages, not part of this work: tell the orchestly session the capability exists; the migration stage (path diff, migrated copy, entry budget); the store's seven hook-only checks need a decision on giving a command the hook's standard input.
4. Separate stream: the Plane plan decisions D1 to D6 and the `/auto-mode-setup` re-apply.

## Needs a person

- Decide how F-002 closes and when to commit the kit (nothing is committed; no push or publish unless asked).
- Optionally re-attest ADR-0015 to ADR-0019 (they were reworded for the leakage test after verification; the journal records it).
- Merging, pushing and any publishing stay with the developer.
