---
type: reference
title: Changelog
description: Version history and the field rename map for consumers
status: draft
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:44:50Z'
---

# Changelog

## 1.4.0 (F-004 support types, F-005 session heading)

Format ACF 1.4, package 1.4.0. Additive: a bundle that uses none of the new keys validates as before (guard test), with three exceptions to know: a session entry heading of another shape gets the new ACF045 warning (an error under `--strict`); and a bundle that already holds pages of the type names `ticket-resolution`, `issue-pattern` or `platform-behaviour` now gets those types' checks; and the enum check is type-strict and `ackit new` no longer defaults a numeric enum, for every type.

- Core types `ticket-resolution`, `issue-pattern` and `platform-behaviour` with templates; `resolution_type` is 1 to 6. The enum check now compares type and value (1.0 and true are not 1), and `ackit new` leaves a numeric choice empty instead of guessing the first value. A bundle that already had pages of these type names (an unknown type before) now gets the type's checks (T-018).
- `vocabularies` in `ackit.yaml` (a mapping of name to a source: a `values` list, a local source file with a key path, or the ids of the documents of a type) and `vocab: {field: vocabulary}` on a type; rules ACF043 (an unregistered value) and ACF044 (an unusable configuration). A bundle without the block is not checked (T-019).
- Rule ACF045: the session entry heading shape `YYYY-MM-DD (Day, Www) - branch @ sha - title`, the sha 7 to 40 hex characters or `none`. A warning by default; `severity: {ACF045: error}` makes it an error. ACF021 is unchanged, so a bundle written before this validates as before except for this new warning; `ackit validate --strict` fails on a warning, so a bundle with session entries of another shape fails under `--strict` until its headings are fixed or the rule is set to `off` with `severity: {ACF045: off}` (T-023).
- The `on-hold` status set is documented as a bundle-level `status_sets` block, with a test (T-023). The core `work` set is unchanged.

## 1.3.0 (F-002 shared store)

- `id_allocation` (`sequential` default, `reserved-range`), `ackit new --author` and `$ACKIT_AUTHOR`, rule ACF037, `ackit ids assign` (ADR-0018, ADR-0020, T-002).
- `environment_registry` (inline data or opt-in `source_file`, `key_paths` mapping onto one model, `extensions`), rule ACF038 (ADR-0015, ADR-0016, T-003). 
- `branch_policy` (work and context branch rules, defaults), the pure resolvers in `branchpolicy.py`, `ackit branch resolve [--json]`, rule ACF039 (ADR-0015, ADR-0016, T-004, T-005).
- `code_lines` on any document, `ackit validate --code-line`, `ackit prompt --code-line`, rule ACF035 (ADR-0017, T-006).
- `author_workspace` (a folder per author, `author` must equal the folder, workspace documents out of the generated index), rules ACF036 and ACF040 (ADR-0019, T-007).
- `process_checks` (adopter commands as argument lists), `ackit checks run --when`, rule ACF041; the core ships no check (ADR-0016, ADR-0019, T-008).
- `checks run` and `link --check` take `--json`. `consumer_layout` (entry file, rules folder and the links a consumer expects), `ackit link --check`, rule ACF042; nothing is created (ADR-0019, T-009).
- Import: `{parent}` and `{id}` placeholders in a mapping's `dest`, and relative markdown links to imported files follow the file to its new place (found on a migration rehearsal of a real store: link warnings 1153 to 142). `ackit verify --status X` on a document already at X records the signature and no longer adds a second history entry (that made the document fail ACF007).
- `ackit verify --signoff` records `signoff: {by, at}` for a person (this and `--status signed-off` are refused for any other actor or an empty id; an existing signoff is not overwritten), which a task above the auto-start limit needs before it starts (ACF027); before, it had to be written by hand.
- `ackit verify --status signed-off` now also writes `signoff: {by, at}` (the same person and moment), which ACF027 requires on a signed-off stage; before, it had to be added by hand.
- `process_checks`: `stdin: pass` (the hook's standard input reaches the command), `scope` with `ackit checks run --scope`, `{bundle}`, `{cwd}`, `{tmpdir}` (a fresh folder, removed after the run, also after a timeout) and `{git_command}` (the nearest `git` process above the hook, for checks that must tell an amend) in arguments; a failing check's own output is printed; a git hook can now call `ackit checks run` for push checks (T-012).
- Reserved-range now refuses every allocation while `id_allocation` is invalid (no sequential fallback); `ids assign` edits only the `id_allocation` block, keeps CRLF, needs an existing `ackit.yaml` and refuses authors YAML reads as numbers or booleans.
- Guard: `tests/test_guard_baseline.py` pins how bundles without any 1.3 key validate (T-001).
- ACF_VERSION 1.3, package 1.3.0. Additive: a 1.0 to 1.2 bundle validates exactly as before.

## 1.2.1

Patch release (ACF stays `acf_version: "1.2"`, package 1.2.1). No field is renamed, no rule added. Fixes I-003 items 19 and 20.

- `wrap-up` is a recognised role part (file `wrap-up.md` in a role directory or in the bundle overlay `roles/<role>/`). It is optional: the kit ships none, a role without one is complete, and `ackit role check` reports only an empty one. `ackit prompt <role> --part wrap-up` prints it (exit 1 when there is none); `--part` also takes rules, checklist, outputs and prompt-guide. The generated prompt is unchanged.
- New `ackit role path <role> [--bundle DIR]`: prints the overlay folder of a role (`<bundle>/roles/<role>`, which may not exist yet; a note goes to stderr when it does not).
- The `reviewer` and `security` roles now define a machine-readable findings object in `outputs.md` ("Findings (machine-readable)"): `verdict` approve | changes-requested | blocked and `findings[]` with `severity` blocking | major | minor | info, `file`, `line`, `title`, `detail`. It is part of the generated reviewer and security prompts, so an orchestrator can parse the answer.
- `SPEC.md` section 7 lists `wrap-up.md` and the findings format.

## 1.2.0

Additive release (ACF format `acf_version: "1.2"`, package 1.2.0). No field is renamed. A 1.1 bundle validates unchanged; the root index may keep `acf_version: "1.1"`. See ADR-0014.

- New optional `points` on task and issue: integer in the scale from `ackit.yaml` `points: {scale, auto_start_max, signoff_max}` (default `[1, 2, 3, 5, 8]`, 2, 5). ACF031 scale; ACF032 (error) points above `signoff_max` on a `ready` or `in-progress` item; points above `auto_start_max` need `signoff` before `ready` (ACF027).
- New optional `runs` on task and issue: ordered list of `{id, at, outcome, tokens?, turns?, commit?, by?}`, ids unique (ACF033).
- `external_id` is now a defined optional key on epic, feature, task and issue (ACF034: non-empty string). It was an unchecked pass-through key before; a ticket in any tracker maps through it.
- New `optional:` list per type in `types.yaml`; `ackit types --markdown` prints an extra `- Optional frontmatter:` line for types that have it (existing lines unchanged).
- `ackit new --slug NAME`; the default slug is the first 6 words, at most 40 characters, never a partial word. Before, the whole title was used.
- `ackit new` writes `history: [<initial status>]` for work types.
- New `ackit status <id-or-path> <new-status> [--bundle DIR]`: checks the transition (SPEC section 6), appends to `history` (created from the current status when missing), refuses an illegal move and lists the legal ones.
- Validator messages for ACF006, ACF007 and ACF026 now list the legal values or transitions.
- Root index `acf_version` is now "1.2" for new bundles.

## 1.1.0

Additive release (ACF format `acf_version: "1.1"`, package 1.1.0). No field is renamed and no existing call changes shape.

- New optional role-profile field `suggested_agent: {capability: high|standard|fast, reasoning: deep|normal, independent_of: <role>}`: a vendor-neutral hint for choosing the agent that plays a role. No vendor or model names in the core; adopters map tiers to models (`adopters/example/agent-map.yaml`).
- Built-in roles carry defaults (developer high; architect, security, planner high/deep; reviewer high independent of developer; tester, business-analyst, designer, devops standard; maintainer fast).
- ACF030 validates the field. `ackit role list` appends an `agent:` column at the end of each line (existing columns unchanged) and has `--json`; `ackit prompt <role> --explain` has a `suggested agent` line.
- Root index `acf_version` is now "1.1". Documents with `acf_version: "1.0"` stay valid.

## 1.0.0

ACF becomes its own format (ADR-0013). Package version 1.0.0, `acf_version: "1.0"`.

### Field rename map (old -> new)

| Where | Old (0.1) | New (1.0) |
|---|---|---|
| frontmatter | `stale_after` | `review_by` |
| frontmatter `sources[]` | `resource` | `ref` |
| root `index.md` frontmatter | `okf_version: "0.2"` and `acf_version: "0.1"` | `acf_version: "1.0"` |
| validator ACF010 | message about `stale_after` | same rule, about `review_by` |
| validator ACF014 | root index carries `okf_version` | root index carries `acf_version` |

Unchanged (consumers such as an orchestrator can rely on them): `type`, `title`, `id`, `status`, `history`, `feature`, `epic`, `item`, `result`, `verdict`, `role`, `about`, `author`, `tier`, `generated`, `verified`, `by`, `at`, `signoff`, `modules`, `depends_on`, all document type names, all status values, the gate names, and the CLI calls `init`, `new`, `index --write`, `validate [--strict]`, `check --gate ... --json`, `prompt`, `types --markdown` with their output shapes.

### Added

`ackit export --okf <out>` and `ackit import --okf <in> --dest <bundle>` (see INTEROP.md).

### Migrating a 0.1 bundle

Replace `stale_after:` with `review_by:` and `resource:` with `ref:` inside `sources`, set the root index to `acf_version: "1.0"` (or run `ackit index --write`).

## 0.1.0

First version.
