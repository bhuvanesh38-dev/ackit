---
type: reference
title: Adopting ACF in a repository
description: Step-by-step adoption guide for a new project
status: draft
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:14:03Z'
---

# Adopting ACF in a repository

For any repository, any host, any team size. Time to a valid bundle: minutes. Time to a trusted one: as long as the humans take to review.

## 1. Install

```bash
python3 -m venv .venv && .venv/bin/pip install ackit    # or install from a checkout: pip install -e path/to/agent-context-kit
```

## 2. Scaffold

```bash
ackit init . --yes                  # accept inferred answers
ackit init . --answers my-answers.yaml    # or answer non-interactively (see adopters/example/answers.yaml)
ackit init .                        # on a terminal: asks only what it cannot infer
```

`init` detects the stack (java-spring, node-react, python, go, otherwise generic), discovers modules (Gradle, Maven, npm workspaces, or directories with a manifest), picks small or large, and writes `context/` with the entry, index, log, product, tech-stack, workflow, architecture, responsibilities, the pack's default rules, and an ADR for adopting ACF. Everything is `draft`.

## 3. Make it true

Edit the drafts. Each type has a template with a guide comment and rules (`docs/DOC-TYPES.md`). In order of value:

1. `workflow.md`: run every command and fix it. Wrong commands are the commonest way context misleads an agent.
2. `AGENTS.md` and `rules/`: keep the never-break rules, each with its Why; delete the pack rules you do not hold.
3. `product.md`, `architecture.md`, and (large repos) one `modules/<name>.md` each.
4. `responsibilities.md`: put real people against roles.

## 4. Verify

```bash
ackit verify context/rules/no-secrets-in-repo.md --by human:alice --status stable
ackit index --bundle context --write
ackit validate context --strict
```

A document is `stable` only when a human verified it (ACF011).

## 5. Enforce

- Pre-commit: see `hooks/pre-commit` and `.pre-commit-hooks.yaml`.
- CI: `ci/` has neutral snippets for common hosts; the one command is `ackit validate context --strict`.
- Tune: `context/ackit.yaml` (`agents_md_max_lines`, `links`, `severity: {CODE: error|warn|off}`).

## 6. Work with it

```bash
ackit new feature "Export to CSV" --tier small      # or --tier large for a staged folder
ackit check --gate start --item F-001 --role developer
ackit prompt developer --item F-001                 # role prompt; add --explain to see what was pulled in
ackit check --gate handoff --item F-001
```

Per work item, write what the role's `outputs.md` lists: test evidence, review, journal entries, a session entry. A session entry heading is `## YYYY-MM-DD (Day, Www) - branch @ sha - title` (`@ none` when no commit); ACF045 warns on a different shape, and `severity: {ACF045: error}` in `ackit.yaml` makes it an error.

If you need an `on-hold` status next to `blocked`, add this block to `ackit.yaml` (it replaces the `work` set; `in-progress -> on-hold -> in-progress` is legal, `on-hold -> done` is not):

```yaml
status_sets:
  work:
    values: [draft, ready, in-progress, on-hold, blocked, in-review, done, cancelled]
    initial: draft
    transitions:
      draft: [ready, cancelled]
      ready: [in-progress, draft, cancelled]
      in-progress: [in-review, on-hold, blocked, cancelled]
      on-hold: [in-progress, cancelled]
      blocked: [in-progress, cancelled]
      in-review: [done, in-progress]
      done: []
      cancelled: []
    human_verified: []
```

## 7. Roles

Use the ten built-in roles as they are; override a part in `context/roles/<role>/` (for example `rules.md`); or `ackit role new <name>` for a new role (fill `role.yaml`, then `ackit validate`). Read `prompt-guide.md` of a role before tuning its prompt.

### Suggested agent per role

Each built-in role has an optional `suggested_agent: {capability: high|standard|fast, reasoning: deep|normal, independent_of: <role>}` in its `role.yaml`. It is vendor-neutral on purpose: map the tiers to real models in your own configuration (see `adopters/example/agent-map.yaml`). Override a role's suggestion for your repository with a `context/roles/<role>/role.yaml` containing just the key. `ackit role list` and `ackit prompt <role> --explain` show it; `ackit role list --json` is for tools. `independent_of` asks for a different agent than the one that played that role, for example the reviewer other than the developer.

## 8. Migrating an existing store

Write a mapping file (see `adopters/example/mapping.yaml`) and run `ackit import <source> --mapping map.yaml --dest context --dry-run`, then without `--dry-run`. Imported documents are drafts; the report lists placeholders to fill. The source is only read. In a mapping's `dest`, `{stem}`, `{parent}` (the source folder name), `{rel}` and `{id}` are available, and relative markdown links to imported files are rewritten to the new places.

## 9. Keep it alive

Each document type names who updates it and when. Stale documents warn (`review_by`); a maintainer runs `ackit prompt maintainer` for a periodic pass. History goes in journals and ADRs, never into living documents.

## Who does what

| Document | Writes | Reviews | Signs off |
|---|---|---|---|
| product, epic, feature requirements | business analyst | human owner | human owner |
| architecture, module, ADR, tech stack | architect | code reviewer | human owner |
| workflow, runbook, incident | devops | developer | human owner |
| design spec | designer | developer, business analyst | human owner |
| tasks, sessions, handoff | developer | code reviewer | code reviewer |
| test evidence, issues | tester | code reviewer | code reviewer |
| security review | security reviewer | developer | code reviewer |
| rules, responsibilities | maintainer | human owner | human owner |
