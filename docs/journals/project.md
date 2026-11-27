---
type: journal
title: agent-context-kit journal
about: product
status: draft
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

# agent-context-kit journal

Append-only. Newest entry first. Never edit a past entry; correct it with a new one.

## 2026-11-20 - decision: the kit stays local with one owner; adoption order kit, orchestly, Ansible, store

Developer decision: the kit lives locally under the existing policy (no remote, no publishing) and the kit owner holds it. The kit is finished first (F-002), then enforced in agent-orchestly, then in the Ansible work, and last in the agent-context store. This settles question 7 of F-002 `01-analysis` and sets the order after it.

## 2026-11-20 - decision: two separate configs, `environment_registry` and `branch_policy`, with purpose-named keys

Developer decision: the registry and the branch policy are different configurations, and every name reflects its purpose. Names are listed in the Naming section of F-002 `01-analysis`; the design stage confirms them against the existing kit vocabulary (notably `gates`).

## 2026-11-20 - decision: the kit is configurable like OKF and ships a basic registry and branch policy (supersedes the entry below)

Developer direction: the kit is a generic framework; adopters configure everything, the kit enforces their configuration; agent-context is the first adopter. The kit ships a basic generic registry shape and a default branch policy (work branch from the environment's UAT branch, as orchestly does for a customer environment; the store creates its context branch the same way from the matching store branch). Adopters accept or replace the policy. The entry below overcorrected ("the kit does not own a registry"); R0, R1 and questions 2 and 3 of F-002 `01-analysis` now follow this decision.

## 2026-11-20 - correction: environments and tenants are already solved; the kit does not own a registry

The first `01-analysis` of F-002 listed the registry as a kit gap and asked what a code line is. The developer pointed out it is already solved: the store's `environments/registry.yaml` (with its generators and validator) and agent-orchestly's pluggable `EnvironmentRegistry` (`branch(env_id, repo, stage)`, yaml adapter with configurable key paths). F3, R1 and questions 1 and 3 were rewritten: the kit only gains line scoping (a `lines:` tag and a line id accepted by `validate` and `prompt`), and consumes a line resolved elsewhere. Lesson: before asking a design question, check the sibling projects (orchestly, the store) for an existing answer.

## 2026-11-20 - decision: the kit's main purpose is the shared store; shared-store support comes before any migration

Developer decision: the kit exists because the first adopter's `agent-context` store has no framework; it is outside the code repositories on purpose, because one store serves several repositories and branches. Order: improve the kit with the full capability first (epic E-002, feature F-002), prove it by agent-orchestly maintaining context for agentic development, and only then apply it to the store. This corrects a reading in the same session that took the in-repository bundle (`<repo>/context`) as the intended main use; that is only the default scaffold. A read-only evaluation of store against kit the same day (about 21 of 646 Markdown files read in full) found the gaps now listed in `01-analysis` of F-002: no model for code lines and registry, store-to-code pairing, developer workspaces beyond sessions, concurrent id allocation, extensible process gates, and a compatibility layer. No code is written before the F-002 design stage is signed off.

## 2026-11-19 - decision: points and runs are optional fields on task and issue, not new types

ACF 1.2 (I-002, ADR-0014): `points`, `runs`, `external_id`; a ticket is `external_id`, a job is a `runs` record. The split rule (points above `signoff_max` on a ready or in-progress item) is an error, configurable. Rejected: `ticket` and `job` document types.

## 2026-11-19 - finding: the brief said external_id already existed; it did not

`external_id` was in no spec, registry or test; it only worked as an unchecked pass-through key. 1.2 defines and checks it. Lesson: grep before trusting a "already exists" claim.

## 2026-11-19 - decision: wrap-up is an optional role part; the findings format lives in the roles' outputs

Kit 1.2.1 (I-003 items 19, 20): `wrap-up.md` is recognised in a role directory and in the bundle overlay but never required, and the kit ships none (the text is the adopter's); `ackit prompt --part` and `ackit role path` expose it to orchestrators. The machine-readable findings object (severity, file, line, title, detail) was added to the reviewer and security `outputs.md`, not to the core, so an adopter can change it in the overlay. Rejected: a kit default wrap-up text per role (it would be a guess about an orchestrator's budget rules); a required `wrap-up.md` (would make every existing role incomplete).

## 2026-11-17 - decision: suggested_agent is a vendor-neutral tier, never a model name

Role profiles gained optional `suggested_agent: {capability, reasoning, independent_of}` (I-001, version 1.1.0). Adopters map tiers to models in their own configuration (`adopters/example/agent-map.yaml`). Rejected: a `model:` key in the core (would name vendors).

## 2026-11-17 - decision: ACF 1.0 is its own format; OKF through an adapter

Dropped the "profile of OKF" framing (ADR-0013, superseding ADR-0002). Renamed `stale_after` to `review_by` and `sources[].resource` to `ref`; root index carries `acf_version: "1.0"` only; `ackit export --okf` and `ackit import --okf` added. CLI shapes used by orchestrators unchanged. Package 1.0.0.

## 2026-11-17 - decision: adopter layer renamed adopters/; licence Apache-2.0

`profiles/` became `adopters/` so that "profile" means only a role profile (ADR-0012 amended). The kit is Apache-2.0 (LICENSE, NOTICE); no package-index publishing.

## 2026-11-17 - decision: adopter specifics only under adopters/

The beta user's conventions shaped the generic design but are not defaults. Recorded as ADR-0012; the leakage grep is a definition-of-done check.

## 2026-11-17 - decision: role profiles are directories, separate from stack packs

Roles gained `role.yaml`, a per-part overlay in the bundle, and `ackit role new` for custom roles; four roles added (business-analyst, architect, designer, devops). ADR-0006.

## 2026-11-17 - finding: YAML 1.1 reads `off` as false

Config values like `links: off` and `severity: {ACF008: off}` arrive as booleans; the validator normalises them. Covered by a test.

## 2026-11-17 - note: journal started

Created for the project.
