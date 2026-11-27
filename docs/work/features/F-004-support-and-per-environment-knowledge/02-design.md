---
type: feature-stage
title: 'Design: Support and per-environment knowledge'
status: signed-off
feature: F-004
stage: design
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:56:19Z'
verified:
- by: human:kit-owner
  at: '2026-11-23T09:34:16Z'
history:
- draft
- signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-23T09:34:16Z'
---

## Approach

**Three core types**, each created with `ackit new`, with a template, required sections, statuses, and the Writes / Reviews / Signs off roles the kit already shows for every type. All three use the `doc` status set (draft, stable, deprecated) with human verification at `stable` (ACF011), so a page is trusted only after a person runs `ackit verify`.

| Type | Holds | Required frontmatter | Sections | Writes / Reviews / Signs off |
|---|---|---|---|---|
| `ticket-resolution` | what was wrong and what was done for one or more tickets | title, description, resolution_type (1 to 6), tickets (list of tracker keys) | Quick summary, Symptom, Diagnosis, Root cause, Resolution, Verification, Follow-up | support agent / support engineer / human owner |
| `issue-pattern` | a recurring problem across resolutions | title, description | Problem, Signals, Cause, Resolution, Related resolutions | support agent / support engineer / human owner |
| `platform-behaviour` | how the system behaves, true on every code line | title, description | Behaviour, Applies to, Evidence | developer / reviewer / human owner |

Sections come from the existing ticket-resolution template (read 2026-11-23: metadata, symptom, diagnosis, root cause, resolution by type, verification, follow-up, tags). Optional frontmatter on `ticket-resolution`, following what the support assistant drafts already write: `scope` (platform, code-line, tenant), `tenants`, `vendors`, `module`, `code_line`, `branch`, `verified_at_commit`, `work_item`. The `resolution_type` values are the six of the template: 1 data fix, 2 diagnostic query only, 3 customer guidance or process fix, 4 UI or configuration change, 5 code fix, 6 external vendor or integration issue. The types declare `dir: ""`, so the conventional-directory warning (ACF022) does not fire on the casebook's nested layout (`<environment>/<tenant>/support/...`); the layout itself stays the support assistant's and the store's.

**Registered references.** A new optional `ackit.yaml` block `vocabularies` lets the adopter register the allowed values of a name: for example `module`, `vendor`, `tenant`. Each vocabulary gets its values from a list in the file, from a local source file with a key path (the pattern of `environment_registry`), or from the ids of documents of a type (so the kit's existing `module` type can be the module registry). A type lists which of its fields are bound to which vocabulary (`ticket-resolution`: `module`, `vendors`, `tenants`). A value that is not registered is a validation error (ACF043); a bad `vocabularies` configuration is an error (ACF044); with no vocabulary configured nothing is checked, so bundles without the block validate exactly as before. Tenants may come from the adopter's own registry file through `source_file`; the core names no registry.

**Role.** A kit role `support` (role.yaml, prompt, rules, checklist, outputs; ACF030) owns the three types: it drafts from the ticket evidence, fills only what the evidence supports, lists missing facts as questions, never writes `verified`, never writes a data change as a recipe. The reviewer role stays the independent check.

**Engineering link.** A resolution of type 1 or 5 normally needs an engineering work item; the optional `work_item` field holds its id (reference check ACF018). No rule forces it in this feature; the pilot decides whether one is needed (ADR-0021: ticket relations stay in the tracker).

**Format.** Additive: new types, a new optional config block and two rules; the format version moves from 1.3 to 1.4 with a changelog entry; ten old-style bundles still validate unchanged (the guard test).

## Alternatives

1. Register the support assistant's types through an adopter overlay: rejected by the kit owner; the types are generic and need roles and templates in the core.
2. One generic `support-case` type with a `kind` field: rejected, the three have different sections and roles.
3. Fixed lists of modules, vendors and tenants in the core: rejected, they are the adopter's data.
4. One `vocabularies` block versus a separate config for each name: chosen, one mechanism serves all three and any later name.
5. Force a work item for resolution types 1 and 5 now: deferred until the pilot shows the need.

## Decisions

- D1. `ticket-resolution`, `issue-pattern` and `platform-behaviour` are core types; `tenant`, `vendor` and `module` are registered references.
- D2. `vocabularies` in `ackit.yaml`; rules ACF043 (error) and ACF044 (error); absent block means no check.
- D3. A core role `support`.
- D4. `dir: ""` for the three types; the layout is not enforced by the kit.
- D5. Format version 1.4, additive.
- D6. `work_item` optional; no forced link before the pilot.
- D7. A pilot of 5 to 10 real resolutions through draft, verification, validation and retrieval follows the build; rules the pilot shows missing come after it.
