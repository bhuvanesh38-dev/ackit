---
type: feature-stage
title: 'Analysis: Shared store: design and build'
status: signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-20T11:42:43Z'
feature: F-002
stage: analysis
generated:
  by: ackit/1.2.1
  at: '2026-11-20T10:43:49Z'
---

## Problem

The kit's default is a bundle that lives **inside** the repository it describes (`ackit init <repo>` writes `<repo>/context`). That is not how the first adopter keeps its context. The `agent-context` store is one repository **outside** the code repositories, serving several code repositories, many code lines (branch families, tenants) and several developers and agents at once. It was grown by hand: conventions, shell scripts and a 17-check commit and push gate, with no framework that defines or checks it. The kit was started to be that framework (developer, 2026-11-20), but today it has no model for what makes a shared store work. Until it does, the store cannot move onto the kit.

## Findings

Sources: the store's own design document `shared/STORE-ARCHITECTURE.md` (492 lines), the main project folder's `AGENTS.md` and `scripts/` (`pre-commit-gate.sh`, `sync-store-branch.sh`, `install.sh`), `environments/registry.yaml`, the AX pipeline (`ax/README.md`, `ax/files/claude-db-workflow.yaml`), the kit's `SPEC.md` and docs, and a read-only evaluation of store against kit on 2026-11-20 (about 21 of the store's 646 Markdown files read in full; the rest by counts and grep; token numbers are characters divided by 4). SPEC.md was not read in full: every statement that the kit "has no concept of X" comes from searching the spec and docs, not from reading every line.

### F1. Why the store is a separate repository

`STORE-ARCHITECTURE.md` section 2: knowledge must not depend on which code branch is checked out; session logs would pollute the code history; the store has its own clean git log. Each tracked code repository gets a project folder in the one store (section 13), with a `shared/` folder of per-file symlinks for what all projects share (section 13a). The wiring into a code clone is per-subpath symlinks into `.claude/` (section 3), installed by `install.sh`.

### F2. A branch per code line

`AGENTS.md` section 5 and `sync-store-branch.sh`: the store has one branch per code base line, named like it (`develop/...`, `release/...`); a post-checkout hook switches the store to the branch matching the code branch's base; every other code line reads the store's `main`. A developer writes on a context branch `{git-user}-{code-branch}` and opens a store pull request. The store's own design document still says the store is "branch-independent" (section 2 of `STORE-ARCHITECTURE.md`, repeated in a gate comment); practice moved on. The kit's design has to start from the practice.

### F3. The registry already exists; the kit lacks the generic shape, the branch policy and line scoping

Correction (developer, 2026-11-20): environments and tenants are already solved, in two places, and the first version of this finding wrongly treated the registry as missing. The store's registry already carries a `code_line` per environment.

- **The store:** `environments/registry.yaml` (651 lines) is "ONE source of truth" for the agent pipeline and the support assistant: stages (prod, uat), code repositories, environments with a branch per repository and stage, tenants with domains and external account names, and an infrastructure block. `build-facts.yaml` and `branch-sync.yaml` are generated from it, and `validate-registry.py` checks it.
- **agent-orchestly:** a pluggable `EnvironmentRegistry` (`src/orchestly/environments.py`) answers `branch(env_id, repo, stage)`, `primary_repo` and `repo_path`; its default yaml adapter takes the key paths from configuration, so the store's file is read without code changes; `engine.py` uses it to choose the base branch and `doctor` checks it.

Developer direction (2026-11-20): the kit is a generic framework like OKF; agent-context is its first adopter. Everything an adopter may want differently is configuration, and the kit enforces the adopter's configuration. The kit still ships a basic default: a generic registry shape (default stage, repositories, environments with a branch per repository and stage, the shape orchestly's `generic` adapter already reads) and a default branch policy (take an environment such as a customer environment, create the work branch from its UAT branch; the store does the same, creating the context branch from the store branch of that environment and stage). An adopter accepts that policy or replaces it, and may map its own registry file onto the generic shape with key paths.

What the kit lacks today: the generic registry shape and the default branch policy; and a way to say a document or rule applies to one code line (for example a Java 11 line versus a language-level 21 line), with `validate` and `prompt` able to be asked about a line.

### F4. Process gates

`pre-commit-gate.sh` runs 17 numbered checks. About 7 are about context documents (session entry updated, links, journal, index freshness, staleness, entry size, local-only leakage). About 10 are about code and process: protected-branch guard, migration naming and content, immutability of applied migrations, raw string parsers, store pull request before the code push (check 15), no replacing remote commits (check 17). The kit's validator has 34 rules, all about documents. The kit's stated position is that process rules belong in `rule` documents, not in tooling (the adopter overlay's README). The store's rule "agent-context before code push" is enforced in tooling today and is among its most important.

### F5. Developer workspaces

The store keeps `developers/{user}/` with `context/branches`, `plans`, `reviews`, `samples` (312 of the 646 Markdown files, 4.74M characters). The kit has `sessions/<author>/<branch>.md` (SPEC section 3), which covers session logs only, and the first adopter's import mapping skips `developers/**` entirely.

### F6. Concurrent writers

The store separates writers by developer namespace, a context branch per developer and a pull request, and forbids replacing remote commits (check 17). The kit allocates ids in `ackit new` from the current bundle, so two writers on different branches can both create the next id (`T-001` clashes are already listed as open in orchestly's roadmap, and the round-2 plan accepts a clash "only when bundles merge"). This was not tested.

### F7. Consumers that must keep working

Claude Code reads `.claude/CLAUDE.md`; the store links `AGENTS.md` there and `rules/` as `.claude/rulebook`. AX does the same inside each sandbox and writes a session entry plus a store pull request per run. The kit's entry cap is 150 lines; the store's is 324 and its gate only warns above 300.

### F8. What the kit already gives

A per-author, per-branch session layout; `applies_to` and `modules`; an external bundle path (orchestly's `external` mode); an import mapping layer with an adopter example; role prompts with a token budget; the adopter layer (ADR-0012) that keeps organisation specifics out of the core. The core also never reads outside the bundle and never uses the network (architecture document), which constrains how a registry or a store-to-code pairing check may look at git.

### F9. Conversion data (evaluation, 2026-11-20)

About 40 percent of the store's Markdown maps to ACF types without rewriting; about 15 percent needs rewriting and is the highest-value part (the entry, the rules, about 13 staged feature folders); the rest is not context (dumps, reports, scripts, personal work product). A pilot import of 21 files gave 9 errors and 13 warnings and invented 58 section stubs. The store's stage names (analysis, frs, tdd, test-plan, implementation, journal) do not match the kit's (analysis, design, plan, tasks, test-plan, journal). Estimated content conversion: 16 to 28 person-days, low confidence; the kit feature work is not in that number.

### Requirements derived

- R1. Code lines and a basic registry, all configurable: a generic registry shape (stages, repositories, environments with a branch per repository and stage, optional extension keys such as tenants) with key-path mapping so an adopter can point it at its own file; a default branch policy (work branch from the environment's UAT branch; store context branch from the matching store branch); documents and rules that can be scoped to lines; `validate` and `prompt` that accept a line. The adopter may replace the policy; the kit enforces what the adopter configured.
- R0. Configuration first: id strategy, paths, line values, gates and the registry mapping are adopter configuration in `ackit.yaml`; no organisation-specific value is in the core.
- R2. A defined pairing between a store branch and a code branch, and a way to express "store pull request before code push" without the core touching the network.
- R3. Developer workspaces that are owned by one author, kept out of shared-knowledge checks and index budgets, and still covered by the append-only rules.
- R4. An id allocation scheme and a duplicate-id check that make concurrent writers safe.
- R5. An extension point for adopter-supplied gates, with levels (block, warn), declared in configuration; every one of the store's 17 checks mapped to an ACF rule or an adopter gate.
- R6. A compatibility layer: the same `AGENTS.md`, `rules/` and `.claude/` paths for existing consumers; a migration path from the current layout, including the stage-name mapping.
- R7. Additive change only: existing bundles validate unchanged; version 1.3; everything organisation specific stays under the adopter's overlay in `adopters/`.

## Naming (decided by the developer's rule, 2026-11-20: separate configs, names say the purpose)

Two separate configurations, each its own block in `ackit.yaml` and optionally its own file, so an adopter can change one without touching the other:

- `environment_registry` (file `environment-registry.yaml`): where code lives. Keys: `default_stage`, `repositories`, `environments` (id, repository, per-stage branches), and a free `extensions` map for adopter data such as tenants. Key-path mapping (`source_file`, `key_paths`) lets an adopter point it at its own file.
- `branch_policy` (file `branch-policy.yaml`): how branches are created. Keys: `work_branch.base_stage` (default: the registry's `default_stage`; `uat` for the first adopter), `context_branch.base` (`matching-line-branch`), `context_branch.fallback` (`main`), `context_branch.name_pattern` (`{author}-{code_branch}`), `context_branch.required_before_code_push` (true or false).

Other names: a document field `code_lines` (the code lines it applies to; named like the store registry's `code_line`; not `lines`, which would read as text lines next to `agents_md_max_lines`; separate from the existing `applies_to`, which narrows by module or role); `id_allocation` (`strategy`: `sequential`, `author-prefixed`, `reserved-range`); `author_workspace` (the per-author area); `consumer_layout` (entry file, rules folder and links that tools such as Claude Code read); `process_checks` (adopter commands with a level, block or warn). Rule: no organisation word (a company, a tool or a customer name) appears in a core name; those live in `adopters/<name>/`. To check in design: `gates` already has a meaning in the kit, so `process_checks` avoids a clash.

## Open questions

Each question has the answer proposed for the design stage; the developer decides.

1. **What is a code line, and who resolves it?** Answered (developer, 2026-11-20): the store's registry already names it (`code_line` on each environment, for example `saas-e2`), and orchestly's `EnvironmentRegistry` already resolves environment and stage to a branch. The kit takes a code line as an id that documents can be tagged with (`code_lines`) and that `validate` and `prompt` can be given, and ships the generic `environment_registry` shape (R1). Tenants are an adopter extension, not a kit concept. Still to settle in the design: free text or checked against the registry (ADR in `02-design`).
2. **One store branch per line, or one branch with line tags on documents?** Answered: the kit's default policy is branch-per-line (the store branch for an environment and stage, created like the code branch is created from UAT); `lines:` tags on documents are an option an adopter may use instead or in addition. agent-context keeps branch-per-line.
3. **Registry in the core or in the adopter?** Answered (developer, 2026-11-20): the core ships a basic generic registry shape and the default branch policy; the content and any replacement policy belong to the adopter. agent-context maps its `environments/registry.yaml` onto the shape; orchestly's `EnvironmentRegistry` already reads that generic shape and is the reference for the key-path mapping.
4. **Process gates: how far should the core go?** Proposed: the core defines the gate contract (name, level, command as an argument list, exit-code meaning) and runs adopter-supplied commands; the core itself stays offline and has no organisation-specific check. The 10 code and process checks become the first adopter's checks; the 7 document checks become ACF rules or are already covered by them.
5. **Id scheme for concurrent writers.** Proposed: keep readable ids but make `ackit new` take an author prefix or a reserved range from configuration, and add a duplicate-id check that runs when branches merge. The alternative (random ids) loses readability. Decide in the design stage with a test.
6. **Must `AGENTS.md` and `rules/` stay exactly where they are?** Proposed: yes. The kit already uses `rules/<slug>.md`; the entry moves to the 150-line budget by splitting rows into rule documents, and `.claude/` symlinks remain adopter-wired.
7. **Where does the kit live for the first adopter to depend on it?** It is a local repository with no remote and a "no publishing" decision. A company store that depends on it needs a home, a version policy and an owner. Proposed: decide before the migration stage, not before the design.
8. **Which store does the pilot use?** Proposed: a throwaway copy of the first adopter's store plus orchestly's own bundle; never the live store. First candidate for a small migration: a small project folder (a small design bundle; to be verified), then the main project folder last.
9. **Order of delivery.** Proposed: R7 and R4 first (additive, small), then R1 and R3, then R5, then R6, so that the orchestly pilot can start on a useful subset before the store-specific compatibility work is done.
