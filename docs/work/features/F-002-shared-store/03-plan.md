---
type: feature-stage
title: 'Plan: Shared store: design and build'
status: signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-20T11:58:37Z'
feature: F-002
stage: plan
generated:
  by: ackit/1.2.1
  at: '2026-11-20T10:43:49Z'
---

## Steps

Rules for every step: the kit repository only (no edit in agent-orchestly, the store or Ansible); SPEC.md, DOC-TYPES.md and the CHANGELOG change in the same step as the code; a step is done only when `.venv/bin/python -m pytest -q` passes, `ackit validate docs --strict` stays at 0 errors, the baseline comparison of step 0 shows no change for bundles without the new keys, and the step's proof (below) is recorded as test-evidence. No organisation word in the core; the leakage grep (rule R-no-adopter-specifics-in-core) runs at every step. Points use the kit scale; each step becomes one task in `04-tasks`, and a step above 5 points is split there.

| Step | Work | ADR | Points | Proof it works |
|---|---|---|---|---|
| 0 | Baseline and guard: record `ackit validate` output of the kit's own `docs/`, `examples/` and orchestly's bundle (read-only copy) before any change; add a test that fails when a bundle without new keys changes result; bump version to 1.3 only when step 1 lands. | all | 2 | Baseline files in `docs/evidence/`; the guard test fails when a rule is made to fire on an old bundle. |
| 1 | `id_allocation` (`sequential` default, `reserved-range`); `ackit new --author`; refusal outside the range; unchanged ACF009. | 0018 | 3 | Unit tests; **proof P2**: two author clones of one bundle each create ten items in parallel, merge both ways, ACF009 reports zero clashes with ranges and reports the clash without them. |
| 2 | `environment_registry` model and reader (`ackit/registry.py`, inline or `source_file`, `key_paths`), `branch_policy` model, validation of both blocks, pure resolvers, `ackit branch resolve`. | 0015, 0016 | 5 | **Proof P1**: a read-only copy of the real registry of the first adopter maps with the documented key paths and resolves every environment, repository and stage to the same branch as orchestly's `YamlRegistry` (a throwaway comparison script outside the kit; orchestly is imported read-only, not edited). Context-branch resolution is checked against the store's actual branches (names listed by the caller). |
| 3 | `code_lines` field, `--code-line` on `validate` and `prompt`, ACF035 against the registry. | 0017 | 3 | Tests for absent, free-text and registry-checked; **proof P3**: count, per store branch, the documents that differ from `main` and classify each as tag-able or branch-only; the result is evidence for the migration stage, not a gate on this step. |
| 4 | `author_workspace`: configurable root, `author` equals folder (ACF036), excluded from shared index and size budgets, append-only rules still apply. | 0019 | 3 | Tests; a copy of one developer folder from the store validated with the new config shows the expected counts. |
| 5 | `process_checks`: config contract, `ackit checks run --when`, argv list without a shell, levels block and warn, exit codes. | 0019, 0016 | 3 | Tests with harmless commands, including a command that fails and one that times out; **proof P4**: a test asserts the core opens no socket during `validate`, `branch resolve` and `checks run` with no configured command (socket guard). |
| 6 | `consumer_layout` and `ackit link --check` (entry, rules, links). | 0019 | 2 | Tests on a temporary tree with correct, missing and wrong links. |
| 7 | The first adopter's overlay under `adopters/`: registry mapping, branch policy, id ranges example, the ten code and process checks as `process_checks` entries (commands point at the store's scripts; none is copied), the seven document checks mapped to ACF rules, stage-name mapping (analysis, frs, tdd, test-plan, implementation, journal to the kit's), consumer layout. | 0015 to 0019 | 3 | Mapping file validates; the check-to-rule table is complete (17 of 17 accounted for); leakage grep shows the names only under `adopters/`. |
| 8 | Documentation and release: SPEC 1.3 section, the two architecture amendments (registry outside the bundle, adopter commands), DOC-TYPES, CHANGELOG, ADR statuses prepared for human verification, version 1.3.0. | all | 2 | `ackit validate docs --strict` 0 errors; the baseline comparison still clean; the developer runs `ackit verify` on the ADRs. |

Delivery order is the table order; steps 3 to 6 can swap after step 2. After step 8 the kit is "finished" for the pilot; the next stage is the orchestly pilot, then Ansible, then the store (developer order, 2026-11-20); those are separate features, not part of F-002's build.

## Risks

- **The registry mapping fails on the real file.** Proof P1 decides; mitigation is a documented `key_paths` change or an adapter, not a core change for one company. The store registry is marked DRAFT and may change shape; the mapping is tested against a copy.
- **Two-writer ids still clash for authors without a range.** Proof P2 shows both cases; the fallback is documented and ACF009 still catches it at merge. If P2 shows ranges are not enough, ADR-0018 is reopened before step 1 is accepted.
- **Running adopter commands weakens "the kit is offline".** The core adds no connection; P4 proves that; the ADR states commands are the adopter's. A reviewer must read the adopter's `process_checks` file before trusting it.
- **Per-line differences are larger than tags can carry.** P3 measures it; the default policy stays branch-per-line, so the risk is for the later migration, not this build.
- **Step 2 is the largest (5 points).** Split in `04-tasks` into model and validation, resolvers, and the command.
- **Backward compatibility.** The step 0 guard and the baseline comparison catch any change to old bundles; version 1.3 is bumped only with step 1 so a half-built state is never labelled 1.3.
- **Context and ownership.** The kit is local with a single owner; there is no remote, so every step is a local commit the developer asks for; nothing is pushed or published.
- **Peers.** orchestly (`rough_work`) and the AX owner are told only after the kit steps they depend on are proven; nothing in their code is edited from this feature.
