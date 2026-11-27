---
acf_version: "1.4"
---

# agent-context-kit - context index

Progressive disclosure: read `AGENTS.md` first, then only what the task needs. Regenerate with `ackit index --write`.

## Entry and core

- [agent-context-kit - agent entry](/AGENTS.md) - A tool-neutral standard, templates, validator and role-prompt generator for keeping agent context in any repository.
- [agent-context-kit architecture](/architecture.md) - Components and data flow
- [agent-context-kit](/product.md) - Why the kit exists and for whom
- [agent-context-kit responsibilities](/responsibilities.md) - Who is responsible for what (RACI)
- [agent-context-kit tech stack](/tech-stack.md) - Languages, frameworks and infrastructure
- [agent-context-kit workflow](/workflow.md) - Build, test and review flow

## Rules

- [R-blast-radius: Check callers before editing a shared symbol](/rules/blast-radius.md)
- [R-evidence-before-done: No work item is done without evidence](/rules/evidence-before-done.md)
- [R-no-adopter-specifics-in-core: No adopter specifics in the core](/rules/no-adopter-specifics-in-core.md)
- [R-no-secrets-in-repo: No secrets in the repository](/rules/no-secrets-in-repo.md)
- [R-no-shell-true: No shell=True with dynamic input](/rules/no-shell-true.md)
- [R-record-decisions: Record structural decisions with the reason](/rules/record-decisions.md)
- [R-spec-registry-tests-agree: SPEC, registry and tests change together](/rules/spec-registry-tests-agree.md)
- [R-surgical-changes: Change only what the work item needs](/rules/surgical-changes.md)
- [R-typed-boundaries: Validate data at the boundary](/rules/typed-boundaries.md)
- [R-validate-before-commit: Validate the bundle before committing](/rules/validate-before-commit.md)

## Work

- [E-001: Adoption readiness](/work/epics/E-001-adoption-readiness.md) - Make the kit installable and trustworthy for a first external adopter
- [E-002: Shared store support (ACF 1.3)](/work/epics/E-002-shared-store-support.md) - Make the kit able to run and maintain a shared context store that serves several repositories, code lines and developers
- [E-003: Kit as support knowledge base](/work/epics/E-003-kit-as-support-knowledge-base.md) - Support tickets, per-environment feature documentation and tenant layout as first-class kit knowledge, so ticket resolution can rely on verified documents
- [F-001: Package and publish the kit](/work/features/F-001-pypi-packaging.md) - Installable wheel and a pre-commit hook entry
- [Analysis: Shared store: design and build](/work/features/F-002-shared-store/01-analysis.md)
- [Design: Shared store: design and build](/work/features/F-002-shared-store/02-design.md)
- [Plan: Shared store: design and build](/work/features/F-002-shared-store/03-plan.md)
- [Tasks: Shared store: design and build](/work/features/F-002-shared-store/04-tasks.md)
- [Test-Plan: Shared store: design and build](/work/features/F-002-shared-store/05-test-plan.md)
- [F-002: Shared store: design and build](/work/features/F-002-shared-store/feature.md) - Code lines and registry, store-to-code pairing, developer workspaces, concurrent writers, process gates, compatibility layer
- [Analysis: One owner for each gate check](/work/features/F-003-one-owner-for-each-gate-check/01-analysis.md)
- [Design: One owner for each gate check](/work/features/F-003-one-owner-for-each-gate-check/02-design.md)
- [Plan: One owner for each gate check](/work/features/F-003-one-owner-for-each-gate-check/03-plan.md)
- [Tasks: One owner for each gate check](/work/features/F-003-one-owner-for-each-gate-check/04-tasks.md)
- [Test-Plan: One owner for each gate check](/work/features/F-003-one-owner-for-each-gate-check/05-test-plan.md)
- [F-003: One owner for each gate check](/work/features/F-003-one-owner-for-each-gate-check/feature.md) - Give each of the store's 17 gate checks exactly one owner (kit core, adopter overlay or store script), build the generic checks, prove equivalence with the live gate
- [Analysis: Support and per-environment knowledge](/work/features/F-004-support-and-per-environment-knowledge/01-analysis.md)
- [Design: Support and per-environment knowledge](/work/features/F-004-support-and-per-environment-knowledge/02-design.md)
- [Plan: Support and per-environment knowledge](/work/features/F-004-support-and-per-environment-knowledge/03-plan.md)
- [Tasks: Support and per-environment knowledge](/work/features/F-004-support-and-per-environment-knowledge/04-tasks.md)
- [Test-Plan: Support and per-environment knowledge](/work/features/F-004-support-and-per-environment-knowledge/05-test-plan.md)
- [F-004: Support and per-environment knowledge](/work/features/F-004-support-and-per-environment-knowledge/feature.md) - Doc types and layout for ticket resolutions and per-environment, per-tenant feature documentation, validated against the environment registry
- [F-005: Session heading shape rule](/work/features/F-005-session-heading-shape-rule.md) - Enforce the session entry heading shape (date, day and week, branch, sha, title) as an opt-in-severity rule; document on-hold as a bundle-level status
- [I-001: Role profiles have no suggested agent or model](/work/issues/I-001-role-profiles-have-no-suggested-agent-or-model.md)
- [I-002: ACF 1.2: points, runs and four kit friction fixes](/work/issues/I-002-acf-1-2-points-runs.md) - ACF 1.2 adds optional points and runs; ackit gains --slug, status and history on create
- [I-003: Kit friction found while dogfooding (round 2)](/work/issues/I-003-kit-friction-round2.md)
- [T-001: Baseline and guard for old bundles](/work/tasks/T-001-baseline-and-guard.md)
- [T-002: id_allocation with reserved ranges](/work/tasks/T-002-id-allocation.md)
- [T-003: environment_registry model, reader and validation](/work/tasks/T-003-registry-model.md)
- [T-004: branch_policy model and pure resolvers](/work/tasks/T-004-branch-policy.md)
- [T-005: ackit branch resolve and the first adopter's mapping proof](/work/tasks/T-005-branch-resolve-command.md)
- [T-006: code_lines field, --code-line and ACF035](/work/tasks/T-006-code-lines.md)
- [T-007: author_workspace and ACF036](/work/tasks/T-007-author-workspace.md)
- [T-008: process_checks contract and ackit checks run](/work/tasks/T-008-process-checks.md)
- [T-009: consumer_layout and ackit link --check](/work/tasks/T-009-consumer-layout.md)
- [T-010: First adopter content](/work/tasks/T-010-first-adopter-content.md)
- [T-011: Documentation and ACF 1.3 release](/work/tasks/T-011-docs-and-release.md)
- [T-012: Run the adopter's gate through process_checks (stdin pass, scope, placeholders)](/work/tasks/T-012-run-the-adopter-s-gate-through.md)
- [T-013: Ownership table and overlay configuration](/work/tasks/T-013-ownership-table-and-overlay.md)
- [T-014: Equivalence harness and safety](/work/tasks/T-014-equivalence-harness-and-safety.md)
- [T-015: Commit-mode cases](/work/tasks/T-015-commit-mode-cases.md)
- [T-016: Push-mode cases and wrapper limits](/work/tasks/T-016-push-mode-cases-and-wrapper-limits.md)
- [T-017: Results, evidence and criterion 3](/work/tasks/T-017-results-evidence-and-criterion-3.md)
- [T-018: Support types and templates](/work/tasks/T-018-support-types-and-templates.md)
- [T-019: Vocabularies and rules ACF043 ACF044](/work/tasks/T-019-vocabularies-and-rules-acf043-acf044.md)
- [T-020: Support role](/work/tasks/T-020-support-role.md)
- [T-021: Docs and format 1.4](/work/tasks/T-021-docs-and-format-1-4.md)
- [T-022: Pilot with real resolutions](/work/tasks/T-022-pilot-with-real-resolutions.md)
- [T-023: ACF045 session heading rule and the on-hold status documentation](/work/tasks/T-023-acf045-and-on-hold-docs.md)

## Decisions

- [ADR-0001: Adopt the Agent Context Format](/decisions/ADR-0001-adopt-the-agent-context-format.md) - Why this repository keeps agent context as ACF
- [ADR-0002: ACF is a profile of OKF v0.2](/decisions/ADR-0002-acf-is-a-profile-of-okf.md) - Define ACF as an OKF profile.
- [ADR-0003: A fixed type vocabulary with per-type sections and ownership](/decisions/ADR-0003-a-fixed-type-vocabulary-with-per-type.md) - A fixed vocabulary of 23 types, each with required frontmatter, required sections, a status set and an owner; extensible under `types:` in `ackit.yaml`.
- [ADR-0004: Three layers: small entry, generated index, records](/decisions/ADR-0004-three-layers-small-entry-generated-index.md) - AGENTS.md (budgeted, one row per document), a generated index.md, and records loaded on demand.
- [ADR-0005: Stack packs are data directories](/decisions/ADR-0005-stack-packs-are-data-directories.md) - A pack is a directory with `pack.yaml`, optional rules and template overrides; `--pack-dir` adds packs.
- [ADR-0006: Role profiles are separate from stack packs, with overlays and custom roles](/decisions/ADR-0006-role-profiles-are-separate-from-stack.md) - Roles are directories (`role.yaml`, prompt, rules, checklist, outputs, prompt-guide). A bundle's `roles/<role>/` overrides any single part; `ackit role new` defines a new role; `extends` inherits missing parts.
- [ADR-0007: Enforcement through coded rules and gates](/decisions/ADR-0007-enforcement-through-coded-rules-and-gates.md) - `ackit validate` with codes ACF001 upward; `ackit check --gate start|handoff`.
- [ADR-0008: Agent output is draft until a human verifies it](/decisions/ADR-0008-agent-output-is-draft-until-a.md) - `stable` and `accepted` require a `verified` entry by a `human:` actor (ACF011); editing drops it.
- [ADR-0009: History lives in journals and decision records, not in living documents](/decisions/ADR-0009-history-lives-in-journals-and-decision.md) - Living documents state current truth; journals (newest first, never edited) and ADRs (superseded, not edited) hold the why and the corrections.
- [ADR-0010: Python, argparse, Jinja2, PyYAML](/decisions/ADR-0010-python-argparse-jinja2-pyyaml.md) - Python 3.12, argparse, Jinja2 and PyYAML.
- [ADR-0011: Import through mapping files; imported documents stay draft](/decisions/ADR-0011-import-through-mapping-files-imported-documents.md) - `ackit import` maps files by glob, preserves unknown keys (clashes become `source_*`), stubs missing sections, records `sources`, and writes drafts.
- [ADR-0012: Agnostic core; adopter specifics only in adopters](/decisions/ADR-0012-agnostic-core-adopter-specifics-only-in.md) - The core (spec, templates, roles, packs, validator) names no company, repository, tool or host; hosts and ticket tools appear only as neutral examples. Adopter-specific rules, mappings, answers and overlays live under `adopters/<adopter>/`, marked as examples; `adopters/example/` is a starting point.
- [ADR-0013: Own format with an OKF adapter, superseding ADR-0002](/decisions/ADR-0013-own-format-with-an-okf-adapter.md) - ACF 1.0 stands alone; OKF v0.2 interop through an adapter
- [ADR-0014: Points and runs are optional fields, not new types](/decisions/ADR-0014-points-and-runs-are-optional-fields.md) - points and runs are optional validated fields on task and issue; a ticket is external_id; a job is a runs record
- [ADR-0015: The environment registry and the branch policy are two separate configurations](/decisions/ADR-0015-registry-and-branch-policy-are-two-configs.md) - The core ships a generic environment_registry shape (with key-path mapping onto an adopter's own file) and a separate branch_policy; adopters accept the defaults or replace them
- [ADR-0016: The core declares, validates and resolves; callers read git and act](/decisions/ADR-0016-the-core-declares-and-resolves-callers-act.md) - Branch policy and process checks stay offline in the core as pure resolution and validation; creating branches, reading git and any network call belong to the caller or to adopter commands; the registry file is the one opt-in local read outside the bundle
- [ADR-0017: Code lines are a separate document field, not an extension of applies_to](/decisions/ADR-0017-code-lines-are-a-separate-document-field.md) - Documents carry an optional code_lines list; validate and prompt accept a code line; ids are checked against the registry when one is configured
- [ADR-0018: Concurrent writers use reserved id ranges per author](/decisions/ADR-0018-concurrent-writers-use-reserved-id-ranges.md) - id_allocation offers sequential (default) and reserved-range strategies; author-prefixed ids are not shipped because they change the id patterns
- [ADR-0019: Process checks, author workspaces and consumer layout are adopter configuration](/decisions/ADR-0019-adopter-process-checks-author-workspace-layout.md) - The core defines a contract for adopter process checks, an owned per-author workspace and a configurable consumer layout; every organisation-specific value lives in the adopter's own overlay under adopters/
- [ADR-0020: Authors without an id range are refused; ranges are assigned through the shared file](/decisions/ADR-0020-author-ranges-are-refused-not-guessed-and-assigned.md) - Restates ADR-0018 without its stale consequence. An author with no range is refused, never given sequential ids; ackit ids assign adds the next free range to ackit.yaml
- [ADR-0021: Ticket links stay in the tracker](/decisions/ADR-0021-ticket-links-stay-in-the-tracker.md) - A ticket in any tracker keeps its sub, duplicate and related relations in that tracker; the kit links tickets only through external_id and the tickets list

## Journals

- [Journal: Session heading shape rule](/journals/journal-session-heading-shape-rule.md)
- [agent-context-kit journal](/journals/project.md)
- [Journal: Shared store: design and build](/work/features/F-002-shared-store/06-journal.md)
- [Journal: One owner for each gate check](/work/features/F-003-one-owner-for-each-gate-check/06-journal.md)
- [Journal: Support and per-environment knowledge](/work/features/F-004-support-and-per-environment-knowledge/06-journal.md)

## Sessions

- [ackit build sessions](/sessions/ackit-dev/build.md)

## Records

- [Evidence for F-002: migration rehearsal on a copy of the first adopter store](/evidence/EV-F-002-migration-rehearsal.md)
- [Evidence for F-002: shared store, design and build](/evidence/EV-F-002-shared-store-build.md)
- [Evidence for F-003: one owner for each gate check](/evidence/EV-F-003-gate-ownership-and-equivalence.md)
- [Evidence for F-005: the session heading shape rule](/evidence/EV-F-005-session-heading-shape-rule.md)
- [Evidence for I-001: suggested agent](/evidence/EV-I-001-suggested-agent.md)
- [Evidence for I-002: ACF 1.2](/evidence/EV-I-002-acf-1-2-points-runs.md)
- [Evidence for I-003 items 19 and 20: wrap-up part, role path, findings format](/evidence/EV-I-003-wrap-up-role-path-findings.md)
- [Evidence for T-001: baseline and guard](/evidence/EV-T-001-baseline-and-guard.md)
- [Evidence for T-002: id_allocation with reserved ranges](/evidence/EV-T-002-id-allocation.md)
- [Evidence for T-003: environment_registry model and reader](/evidence/EV-T-003-registry-model.md)
- [Evidence for T-004: branch_policy and pure resolvers](/evidence/EV-T-004-branch-policy.md)
- [Evidence for T-005: ackit branch resolve and proof P1](/evidence/EV-T-005-branch-resolve-command.md)
- [Evidence for T-006: code_lines, --code-line and proof P3](/evidence/EV-T-006-code-lines.md)
- [Evidence for T-007: author_workspace](/evidence/EV-T-007-author-workspace.md)
- [Evidence for T-008: process_checks, ackit checks run and proof P4](/evidence/EV-T-008-process-checks.md)
- [Evidence for T-009: consumer_layout and ackit link --check](/evidence/EV-T-009-consumer-layout.md)
- [Evidence for T-010: the first adopter overlay for the shared store](/evidence/EV-T-010-first-adopter-content.md)
- [Evidence for T-011: documents for 1.3.0](/evidence/EV-T-011-docs-and-release.md)
- [Evidence for T-012: the adopter gate through process_checks](/evidence/EV-T-012-gate-through-process-checks.md)
- [Evidence for T-013: ownership table and overlay configuration](/evidence/EV-T-013-ownership-table-and-overlay.md)
- [Evidence for T-014: the equivalence harness and its safety checks](/evidence/EV-T-014-equivalence-harness-and-safety.md)
- [Evidence for T-015: commit-mode cases](/evidence/EV-T-015-commit-mode-cases.md)
- [Evidence for T-016: push-mode cases and the wrapper limits](/evidence/EV-T-016-push-mode-cases-and-limits.md)
- [Evidence for T-017: the equivalence result table for all 17 checks](/evidence/EV-T-017-equivalence-result-table.md)
- [Evidence for T-018: the three support types](/evidence/EV-T-018-support-types.md)
- [Evidence for T-019: vocabularies and rules ACF043 and ACF044](/evidence/EV-T-019-vocabularies.md)
- [Evidence for T-020: the support role](/evidence/EV-T-020-support-role.md)
- [Evidence for T-021: documentation and format 1.4](/evidence/EV-T-021-docs-and-format-1-4.md)
- [Evidence for T-023: ACF045 and the on-hold status block](/evidence/EV-T-023-acf045-and-on-hold.md)
- [Handoff: F-002 build, next session starts at T-002 review and T-003](/handoffs/f-002-build-handoff.md)
- [Review of F-002: shared store, design and build](/reviews/REV-F-002-shared-store-build.md)
- [Review of F-003: one owner for each gate check](/reviews/REV-F-003-gate-ownership-and-equivalence.md)
- [Review of F-005: the session heading shape rule](/reviews/REV-F-005-session-heading-shape-rule.md)
- [Review of I-001: suggested agent](/reviews/REV-I-001-suggested-agent.md)
- [Review of I-002: ACF 1.2](/reviews/REV-I-002-acf-1-2-points-runs.md)
- [Review of I-003 items 19 and 20](/reviews/REV-I-003-wrap-up-role-path-findings.md)
- [Review of T-001: baseline and guard](/reviews/REV-T-001-baseline-and-guard.md)
- [Review of T-002: id allocation](/reviews/REV-T-002-id-allocation.md)
- [Review of T-003: environment registry](/reviews/REV-T-003-registry-model.md)
- [Review of T-004: branch_policy and pure resolvers](/reviews/REV-T-004-branch-policy.md)
- [Review of T-005: ackit branch resolve](/reviews/REV-T-005-branch-resolve-command.md)
- [Review of T-006: code lines](/reviews/REV-T-006-code-lines.md)
- [Review of T-007: author workspace](/reviews/REV-T-007-author-workspace.md)
- [Review of T-008: process checks](/reviews/REV-T-008-process-checks.md)
- [Review of T-009: consumer layout](/reviews/REV-T-009-consumer-layout.md)
- [Review of T-010: first adopter content](/reviews/REV-T-010-first-adopter-content.md)
- [Review of T-011: documents for 1.3.0](/reviews/REV-T-011-docs-and-release.md)
- [Review of T-012: the adopter gate through process_checks](/reviews/REV-T-012-gate-through-process-checks.md)
- [Review of T-013: ownership table and overlay configuration](/reviews/REV-T-013-ownership-table-and-overlay.md)
- [Review of T-014: the equivalence harness and its safety checks](/reviews/REV-T-014-equivalence-harness-and-safety.md)
- [Review of T-015: commit-mode cases](/reviews/REV-T-015-commit-mode-cases.md)
- [Review of T-016: push-mode cases and the wrapper limits](/reviews/REV-T-016-push-mode-cases-and-limits.md)
- [Review of T-017: the equivalence result table](/reviews/REV-T-017-equivalence-result-table.md)
- [Review of T-018: the three support types](/reviews/REV-T-018-support-types.md)
- [Review of T-019: vocabularies and rules ACF043 and ACF044](/reviews/REV-T-019-vocabularies.md)
- [Review of T-020: the support role](/reviews/REV-T-020-support-role.md)
- [Review of T-021: documentation and format 1.4](/reviews/REV-T-021-docs-and-format-1-4.md)
- [Review of T-023: ACF045 and the on-hold status block](/reviews/REV-T-023-acf045-and-on-hold.md)

## Reference

- [Adopting ACF in a repository](/ADOPTION.md) - Step-by-step adoption guide for a new project
- [Changelog](/CHANGELOG.md) - Version history and the field rename map for consumers
- [ACF document types](/DOC-TYPES.md) - Generated reference: every type with required frontmatter, sections, statuses and ownership
- [Interoperability with OKF v0.2](/INTEROP.md) - How the OKF adapter maps fields and what cannot round-trip
- [Integrating agent-orchestly with ACF](/ORCHESTLY-INTEGRATION.md) - What a workflow orchestrator (agent-orchestly) must change to read and write ACF
