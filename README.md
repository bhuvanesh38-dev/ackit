# agent-context-kit

A tool-neutral **standard, templates and toolkit for keeping agent context in a repository**, big or small. The standard is the **Agent Context Format (ACF) 1.4**, a standalone format with an adapter for the Open Knowledge Format (OKF v0.2). The toolkit is `ackit`: scaffold a bundle, enforce the format, generate a prompt for each role.

- [SPEC.md](SPEC.md): the format.
- [docs/DOC-TYPES.md](docs/DOC-TYPES.md): every document type with template rules and ownership.
- [docs/ADOPTION.md](docs/ADOPTION.md): adopt it in your repository.
- [docs/decisions/](docs/decisions/): why it is built this way.

## Why

Agents repeat the same mistakes when a repository does not tell them what the product is, how to build and test it, which rules never bend and why, and what was already decided. Wiki pages rot, a giant instructions file is expensive to load and nobody checks it. ACF keeps context as small typed markdown documents, loaded in layers (a small always-loaded entry, a generated index, records on demand), each with an owner, a template and checks CI can run.

## Interoperability with OKF

ACF is its own format, designed for software projects: a type vocabulary with required frontmatter and sections per type, a work hierarchy (epic, feature, task, issue; features are one document or a staged folder signed off in order), a status lifecycle with legal transitions, human-trust gates, ownership per document type, role definitions with generated prompts, and a validator with stable rule codes. It borrowed ideas from OKF v0.2 but does not depend on it. `ackit export --okf <out>` and `ackit import --okf <in> --dest <bundle>` move bundles between the two (field map and what cannot round-trip: [docs/INTEROP.md](docs/INTEROP.md)). Version history: [docs/CHANGELOG.md](docs/CHANGELOG.md).

## Quick start

```bash
python3 -m venv .venv && .venv/bin/pip install -e .      # from a checkout
ackit init path/to/repo --yes                             # detect stack, scaffold path/to/repo/context
ackit validate path/to/repo/context                       # 0 = ok
ackit new feature "Export to CSV" --bundle context
ackit branch resolve --bundle context --environment <id> --author <name> --task <T-001>   # one shared store, several code lines (ACF 1.3)
ackit check --gate start --item F-001 --bundle context
ackit prompt developer --item F-001 --bundle context     # generated role prompt; --explain shows what it pulled in
```

Commands: `init`, `validate`, `check`, `prompt`, `new`, `index`, `verify`, `role (list|new|check)`, `types`, `rules`, `import`, `export`.

## What is in a bundle

Entry (`AGENTS.md`, size-budgeted) -> index -> records. Types: entry, product, tech-stack, workflow, architecture, module, rule, responsibility, epic, feature, feature-stage, task, issue, incident, decision (ADR), journal, session, session-index, review, test-evidence, handoff, design-spec, runbook, reference. Small repositories need the core set; large repositories add one module document per module. Decisions are recorded with their options and the Why; journals hold corrections and history so living documents state only current truth.

## Roles

Built in: developer, tester, security reviewer, code reviewer, business analyst, architect, designer (UX/UI), devops; optional planner and maintainer. Each role is a directory: `role.yaml` (the **role profile**: owned document types, required checklists, gates, tools), `prompt.md`, `rules.md`, `checklist.md`, `outputs.md`, `prompt-guide.md`. Use them as they are, override any part per repository in `context/roles/<role>/`, or define a new role with `ackit role new <name>`. Each role profile may also carry a vendor-neutral `suggested_agent` (capability tier, reasoning level, independence from another role); adopters map tiers to real models. `ackit prompt <role> --item <id>` assembles the prompt from the role template and only the bundle documents that matter (blocking rules, the module, the item and its stages), within an optional `--budget`.

## Three different "adopters"

| | |
|---|---|
| **Stack pack** (`packs/`) | a technology: detection, commands, default rules. Add one with a directory, no code. |
| **Role profile** (`role.yaml`) | a way of working: who owns what, which checklists and gates. |
| **Adopter overlay** (`adopters/<name>/`) | one organisation's overlay: answers, import mapping, extra rules, role overlays. |

## Enforcement

`ackit validate` (exit codes 0 / 1 / 2) checks frontmatter per type, required sections, ids and links, status transitions, staleness, the trust gate (stable needs a `human:` verifier), work-item completeness (done needs test evidence, a review and a journal), stage order, role definitions, and the entry size budget. Severity per rule is configurable. `ackit check --gate start|handoff --item ID` is the gate an orchestrator calls. `hooks/pre-commit`, `.pre-commit-hooks.yaml` and `ci/` give the hook and CI snippets.

## Principles: agnostic core, beta-user adopters

agent-context-kit is a product in its own right. The core (spec, templates, roles, stack packs, validator) is agnostic to company, host and tool: code hosts and ticket tools appear only as neutral examples. Real organisations that shaped the design are **beta users**: what they taught us is in the generic design, and what is specific to them lives only in `adopters/<name>/`, marked as an example. `adopters/example/` is the starting point for a new adopter; the first beta user's profile is a worked example of mapping a mature store. A leakage grep is part of the definition of done (ADR-0012).

## How an orchestrator uses it

An orchestrator (for example agent-orchestly, see [docs/ORCHESTLY-INTEGRATION.md](docs/ORCHESTLY-INTEGRATION.md)) calls `ackit check --gate start` before a job, `ackit prompt <role>` to build each agent's prompt, writes the records each role's `outputs.md` lists, and calls `ackit check --gate handoff` and `ackit validate --strict` before it hands off. The kit never runs agents and its core never touches the network (the commands an adopter lists under `process_checks` are the adopter's own).

## Adopting it elsewhere

See [docs/ADOPTION.md](docs/ADOPTION.md): `ackit init`, edit the drafts, `ackit verify` the important ones, add the hook and CI line. Migrate an existing store with `ackit import --mapping`. Examples: [examples/small](examples/small), [examples/large](examples/large). This repository's own context is the bundle in [docs/](docs/), validated with `ackit validate docs --strict`.

## Layout

```
SPEC.md  README.md  pyproject.toml
src/ackit/            code and data (types.yaml, templates/, roles/, packs/, role-template/)
adopters/             adopter overlays (example/ plus beta users)
docs/                 this project's own ACF bundle: ADRs, journal, guides
examples/             small and large example bundles
hooks/  ci/  .pre-commit-hooks.yaml
tests/
```


Development: `python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'`, then `.venv/bin/python -m pytest`.

## Licence

Apache License 2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE).
