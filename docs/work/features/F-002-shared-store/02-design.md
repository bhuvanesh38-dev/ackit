---
type: feature-stage
title: 'Design: Shared store: design and build'
status: signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-20T11:53:03Z'
feature: F-002
stage: design
generated:
  by: ackit/1.2.1
  at: '2026-11-20T10:43:49Z'
---

## Approach

The kit stays a generic framework; the shared store is its first adopter. Everything an adopter may want differently is optional configuration in `ackit.yaml`, the kit validates and enforces what the adopter configured, and nothing organisation specific enters the core (ADR-0012). The new capability is ACF 1.3 and additive: a bundle with none of the new keys behaves exactly as it does today.

Six additions, each configurable:

1. `environment_registry`: a generic shape for where code lives (default stage, repositories, environments with a code line and a branch per repository and stage, free `extensions`). `source_file` and `key_paths` map an adopter's own file onto it. The first adopter's registry maps with `default_stage: defaults.development_stage` and `repositories: code_repos`; the rest of orchestly's default key paths already match it (checked against `environments.py` and the real file on 2026-11-20). ADR-0015.
2. `branch_policy`: the default policy is "the work branch is created from the environment's default-stage branch (UAT for the first adopter); the store creates its context branch the same way, from the store branch matching the code base branch, falling back to `main`". Adopters accept it or replace it. ADR-0015.
3. Offline resolution: the kit resolves names and validates; callers read git and create branches. `ackit branch resolve` prints the result. `source_file` is the one opt-in local read outside the bundle. ADR-0016.
4. `code_lines` on documents, `--code-line` on `validate` and `prompt`, checked against the registry (ACF035). ADR-0017.
5. `id_allocation` with `sequential` and `reserved-range`. ADR-0018.
6. `process_checks`, `author_workspace`, `consumer_layout`: contracts in the core, content in `adopters/<name>/` (ACF036). ADR-0019.

Names follow the Naming section of `01-analysis`, with one change found while designing: `code_lines` replaces `lines` (a clash with `agents_md_max_lines`), and `process_checks` does not clash with `ackit check --gate`, which is about work items.

## Alternatives

- One combined registry-and-policy block, rejected (ADR-0015).
- The kit reads git and creates branches, rejected because it breaks the offline rule (ADR-0016).
- Reusing `applies_to` for lines, rejected because it already means module and role (ADR-0017).
- Author-prefixed or random ids, rejected because they change id patterns or readability (ADR-0018).
- Putting the store's 17 checks in the core, rejected: ten are process facts the kit cannot know offline (ADR-0019).
- Making the kit the only registry reader and removing orchestly's, rejected: orchestly is another session's code; it is only proposed to align on the same key paths.

## Decisions

Requirement coverage (R-numbers from `01-analysis`):

| Requirement | Covered by |
|---|---|
| R0 configuration first | all ADRs: every key optional and in `ackit.yaml` |
| R1 lines, registry, branch policy | ADR-0015, ADR-0016, ADR-0017 |
| R2 store-to-code pairing, store PR before code push | ADR-0015 (`context_branch`), ADR-0016 (declared, enforced by an adopter check), ADR-0019 |
| R3 author workspaces | ADR-0019 |
| R4 concurrent writers | ADR-0018 |
| R5 adopter gates with levels | ADR-0019 (`process_checks`) |
| R6 compatibility layer and stage mapping | ADR-0019 (`consumer_layout`, mapping file) |
| R7 additive, 1.3 | Approach; proven by validating the kit's own `docs/`, `examples/` and orchestly's bundle unchanged |

Open questions of `01-analysis`: 1 and 2 and 3 are answered by ADR-0015 to ADR-0017; 4 by ADR-0019; 5 by ADR-0018; 6 by ADR-0019 (`consumer_layout`); 9 by the order below. Questions 7 and 8 are not kit design and stay with the developer:

- **Where the kit lives:** decided by the developer on 2026-11-20: it stays local and follows the existing policy (a local repository, no remote, no package-index publishing); the owner is the kit owner. Version policy: the ACF version in the root `index.md` and the `CHANGELOG`, as today.
- **Adoption order (developer, 2026-11-20):** finish the kit (this feature); then enforce it in agent-orchestly; then in the Ansible work (the infrastructure repository); and last in the agent-context store. Each step uses the kit as it is at that point, and nothing later starts before the earlier one is proven.
- **Pilot store:** orchestly's own bundle plus a throwaway copy of the first adopter's store, never the live store.

Delivery order (each step releasable on its own): R7 guard and 1.3 version; `id_allocation`; `environment_registry` and `branch_policy` with `ackit branch resolve`; `code_lines` and ACF035; `author_workspace` and ACF036; `process_checks`; `consumer_layout`; the First adopter content.

Not proven yet, to be proven in `03-plan` and `05-test-plan`: the first adopter's registry mapping against the real file; the two-writer id concurrency test; the per-line document count that decides tags versus branches; the effect of `process_checks` running adopter commands on the "kit never opens a connection" statement.

Proposals to peers (nothing edited): `rough_work` (orchestly) is told that the registry key paths are the shared contract and that the kit reader exists once ADR-0016 is accepted; the AX owner (Dhanusu A) is not contacted until the developer says so.
