---
type: reference
title: ACF document types
description: 'Generated reference: every type with required frontmatter, sections, statuses and ownership'
status: draft
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:14:03Z'
---

Generated from `src/ackit/data/types.yaml` by `ackit types --markdown`. Do not edit by hand.

## `entry`

Small always-loaded entry file (AGENTS.md). Points to everything else.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`
- Required sections: Project, Build and verify, Critical rules, Load on demand
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: maintainer
- Reviews: any human owner
- Signs off: human owner
- Updated: when a never-break rule
- Rules for this document:
  - At most `agents_md_max_lines` lines (default 150).
  - Detail lives in rules/ or reference/; this file holds one row per document.
  - Every rule here has a Why.

## `product`

What the product is, for whom, and what success means.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`, `description`
- Required sections: Purpose, Users, Goals, Non-goals
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: business-analyst
- Reviews: human owner
- Signs off: human owner
- Updated: when scope or users change
- Rules for this document:
  - States non-goals explicitly.
  - No implementation detail; link to architecture instead.

## `tech-stack`

Languages, frameworks, versions, infrastructure.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`, `languages`
- Required sections: Languages and frameworks, Infrastructure, Conventions
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: architect
- Reviews: reviewer
- Signs off: human owner
- Updated: when a dependency or runtime major version changes
- Rules for this document:
  - Versions are sourced from the build files (say which); never invent them.
  - Conventions state the style guide in force.

## `workflow`

Build, test, lint and review commands, branching and PR flow.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`, `commands`
- Required sections: Commands, Branching and review, Definition of done
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: devops
- Reviews: reviewer
- Signs off: human owner
- Updated: when a command or the review flow changes
- Rules for this document:
  - `commands` frontmatter has build, test and lint keys (empty string when not applicable).
  - Every command was actually run by the author.

## `architecture`

How the system is put together; boundaries and data flow.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`
- Required sections: Overview, Components, Data flow, Constraints
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: architect
- Reviews: reviewer
- Signs off: human owner
- Updated: on any structural change
- Rules for this document:
  - A structural change needs a decision record first.
  - Diagrams are text (mermaid or ASCII) so they diff.

## `module`

One module or package of a large repository - its job, API, dependencies and owner.

- Directory: `modules`
- Required frontmatter: `type`, `title`, `id`, `path`
- Required sections: Responsibility, Public surface, Dependencies, Owners
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: architect
- Reviews: reviewer
- Signs off: module owner
- Updated: when the module public surface or dependencies change
- Rules for this document:
  - `path` points at the source directory (relative to the repo).
  - Dependencies list only modules actually imported.

## `rule`

A never-break rule with the reason it exists.

- Directory: `rules`
- Required frontmatter: `type`, `title`, `id`, `severity`
- Required sections: Rule, Why, How to check
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: maintainer
- Reviews: human owner
- Signs off: human owner
- Updated: when the reason changes or an incident shows a gap
- Rules for this document:
  - A rule without a Why is rejected.
  - `applies_to` (roles) and `modules` narrow who sees it in generated prompts.
  - `code_lines` (any type) limits it to those code lines; absent means every line.
  - A stable rule is human-verified.

## `responsibility`

RACI - who is Responsible, Accountable, Consulted, Informed per area and per document type.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`
- Required sections: Areas, Roles, RACI
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: maintainer
- Reviews: human owner
- Signs off: human owner
- Updated: when a team or role changes
- Rules for this document:
  - Exactly one Accountable per row.
  - Roles use the ACF role names.

## `epic`

A body of work delivered by several features.

- Directory: `work/epics`
- Required frontmatter: `type`, `title`, `id`, `status`
- Optional frontmatter: `external_id`
- Required sections: Goal, Scope, Success criteria
- Statuses: draft -> ready -> in-progress -> blocked -> in-review -> done -> cancelled
- Writes: business-analyst
- Reviews: human owner
- Signs off: human owner
- Updated: when scope changes; closed when all features are done
- Rules for this document:
  - Done only when every child feature is done.
  - Success criteria are measurable.

## `feature`

A deliverable change. tier small = one document; tier large = a folder of staged documents signed off in order.

- Directory: `work/features`
- Required frontmatter: `type`, `title`, `id`, `status`, `tier`
- Optional frontmatter: `external_id`
- Required sections: small tier: Goal, Acceptance criteria, Design, Plan, Test plan; large tier: Goal, Acceptance criteria, Stages
- Statuses: draft -> ready -> in-progress -> blocked -> in-review -> done -> cancelled
- Writes: business-analyst (requirements)
- Reviews: reviewer
- Signs off: human owner per stage
- Updated: every stage change; journal on every decision
- Rules for this document:
  - Large features: stages analysis, design, plan, tasks, test-plan, journal; a stage is signed off before the next is started.
  - Small features carry `signoff` before status ready.
  - Done needs test evidence, a review record and a journal entry.

## `feature-stage`

One stage document of a large feature.

- Directory: `work/features`
- Required frontmatter: `type`, `title`, `feature`, `stage`, `status`
- Required sections: none required
- Statuses: draft -> signed-off
- Writes: per stage - planner for analysis and design
- Reviews: reviewer
- Signs off: human owner (signoff.by)
- Updated: until signed off; afterwards only via the journal
- Rules for this document:
  - `signoff: {by, at}` is required at status signed-off.
  - A signed-off stage is not edited; corrections go to the journal.

## `task`

A unit of work under a feature, small enough for one agent session.

- Directory: `work/tasks`
- Required frontmatter: `type`, `title`, `id`, `status`, `feature`
- Optional frontmatter: `points`, `runs`, `external_id`
- Required sections: Goal, Acceptance criteria
- Statuses: draft -> ready -> in-progress -> blocked -> in-review -> done -> cancelled
- Writes: planner or developer
- Reviews: reviewer
- Signs off: reviewer
- Updated: status changes
- Rules for this document:
  - Names the module(s) it touches.
  - Acceptance criteria are checkable.
  - `points` (optional) is in the configured scale; above `signoff_max` it is split before it is ready, above `auto_start_max` it needs `signoff`.
  - `runs` (optional) records each run: id, at, outcome, and optionally tokens, turns, commit, by.

## `issue`

A bug or defect report and its fix.

- Directory: `work/issues`
- Required frontmatter: `type`, `title`, `id`, `status`, `severity`
- Optional frontmatter: `points`, `runs`, `external_id`
- Required sections: Symptom, Expected, Reproduction, Cause, Fix
- Statuses: draft -> ready -> in-progress -> blocked -> in-review -> done -> cancelled
- Writes: tester or developer
- Reviews: reviewer
- Signs off: reviewer
- Updated: as the cause becomes known
- Rules for this document:
  - Reproduction is concrete enough to run.
  - Done needs test evidence of the fix and a review record.
  - `points` and `runs` (optional) follow the same rules as on a task.

## `incident`

A production or environment failure - cause, fix, checks.

- Directory: `incidents`
- Required frontmatter: `type`, `title`, `id`, `status`, `severity`
- Required sections: Symptom, Cause, Fix, Checks, Follow-ups
- Statuses: open -> mitigated -> resolved -> closed
- Writes: developer
- Reviews: human owner
- Signs off: human owner
- Updated: until closed
- Rules for this document:
  - Records evidence for the cause, not a guess.
  - Follow-ups become issues or rules.

## `decision`

Architecture or process decision record (ADR) - what was decided and why.

- Directory: `decisions`
- Required frontmatter: `type`, `title`, `id`, `status`, `date`
- Required sections: Context, Options, Decision, Why, Consequences
- Statuses: proposed -> accepted -> rejected -> superseded -> deprecated (human verification at: accepted)
- Writes: planner or developer
- Reviews: reviewer
- Signs off: human owner
- Updated: never edited once accepted - superseded by a new record
- Rules for this document:
  - Options lists at least two options.
  - Why states the deciding reason, not a restatement.
  - `supersedes` and `superseded_by` are reciprocal.

## `journal`

Append-only record of decisions, corrections and findings for one feature or document set.

- Directory: `journals`
- Required frontmatter: `type`, `title`, `about`
- Required sections: none required
- Statuses: draft -> stable -> deprecated
- Writes: whoever made the decision
- Reviews: none
- Signs off: none
- Updated: same turn as the decision or correction
- Rules for this document:
  - Entries: `## YYYY-MM-DD - kind: title`, kind is decision, correction, finding or note.
  - Newest first. Past entries are never edited; correct with a new entry.
  - Living docs state only current truth; history lives here.

## `session`

Per-branch (or per-item) session log, one entry per working session.

- Directory: `sessions`
- Required frontmatter: `type`, `title`, `author`
- Required sections: none required
- Statuses: draft -> final
- Writes: the agent or person who did the work
- Reviews: none
- Signs off: none
- Updated: after every implementation session
- Rules for this document:
  - Entry heading: `## YYYY-MM-DD (Day, Www) - branch @ sha - title`.
  - Labels Done, Faced, Decisions, Build, Next, Blockers are all present.
  - Written without being asked; committing it is a person's call.

## `session-index`

Rolling one-line-per-session index (working memory).

- Directory: `sessions`
- Required frontmatter: `type`, `title`, `author`
- Required sections: none required
- Statuses: draft -> final
- Writes: the agent or person who did the work
- Reviews: none
- Signs off: none
- Updated: one line per session
- Rules for this document:
  - One bullet per session: `- YYYY-MM-DD - branch - title - [entry](path)`.
  - Older lines move to the session log; the index stays short.

## `review`

Findings of a code, security or test review of one work item.

- Directory: `reviews`
- Required frontmatter: `type`, `title`, `item`, `role`, `verdict`
- Required sections: Scope, Findings, Resolution, Verdict
- Statuses: draft -> final
- Writes: the reviewing role
- Reviews: developer (resolves findings)
- Signs off: reviewer
- Updated: until every finding is resolved
- Rules for this document:
  - Each finding has file:line, severity and a resolution.
  - Verdict follows from the findings.

## `test-evidence`

What was run and what it showed, for one work item.

- Directory: `evidence`
- Required frontmatter: `type`, `title`, `item`, `result`
- Required sections: Commands, Results, Coverage
- Statuses: draft -> final
- Writes: tester or developer
- Reviews: reviewer
- Signs off: reviewer
- Updated: per test run
- Rules for this document:
  - Commands are copy-pasteable and were run.
  - Results quote real output, not a paraphrase.

## `handoff`

Hand a finished item to a person (PR) or the next agent.

- Directory: `handoffs`
- Required frontmatter: `type`, `title`, `item`
- Required sections: Summary, Evidence, Open items, Needs a person
- Statuses: draft -> final
- Writes: developer
- Reviews: human owner
- Signs off: human owner
- Updated: once per handoff
- Rules for this document:
  - Links the evidence and review records.
  - Merging is always listed under Needs a person.

## `reference`

Stable factual material (API tables, schemas, glossary) loaded on demand.

- Directory: `reference`
- Required frontmatter: `type`, `title`, `description`
- Required sections: none required
- Statuses: draft -> stable -> deprecated
- Writes: developer
- Reviews: reviewer
- Signs off: none
- Updated: when the facts change; `review_by` is set
- Rules for this document:
  - Facts only, with `sources`.
  - Set `review_by` - facts rot.

## `ticket-resolution`

What was wrong and what was done for one or more support tickets - symptom, diagnosis, cause, resolution, how it was checked.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`, `description`, `resolution_type`, `tickets`
- Optional frontmatter: `scope`, `tenants`, `vendors`, `module`, `code_line`, `branch`, `verified_at_commit`, `work_item`
- Required sections: Quick summary, Symptom, Diagnosis, Root cause, Resolution, Verification, Follow-up
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: support agent
- Reviews: support engineer
- Signs off: human owner
- Updated: when the ticket is reopened or the cause turns out different; `review_by` is set
- Rules for this document:
  - `resolution_type` is 1 data fix, 2 diagnostic query only, 3 customer guidance or process fix, 4 UI or configuration change, 5 code fix, 6 external vendor or integration issue.
  - `tickets` holds the tracker keys; relations between tickets (duplicate, parent, related) stay in the tracker.
  - Fill only what the evidence supports; list missing facts as questions, not as placeholders.
  - Never write a data change as a recipe to run; say what was found and who changed it.
  - A resolution of type 1 or 5 normally needs an engineering work item: put its id in `work_item`.

## `issue-pattern`

A recurring problem seen across several resolutions - how to recognise it, why it happens, what resolves it.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`, `description`
- Required sections: Problem, Signals, Cause, Resolution, Related resolutions
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: support agent
- Reviews: support engineer
- Signs off: human owner
- Updated: when a new resolution confirms or changes the pattern; `review_by` is set
- Rules for this document:
  - A pattern needs at least two resolutions behind it; link them under Related resolutions.
  - Signals are what a support agent can see before diagnosis (message, screen, value), not the cause.
  - Never write a data change as a recipe to run.

## `platform-behaviour`

How the system behaves, true on every code line - so a support agent or tester can tell expected behaviour from a defect.

- Directory: `bundle root`
- Required frontmatter: `type`, `title`, `description`
- Required sections: Behaviour, Applies to, Evidence
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: developer or support agent
- Reviews: reviewer
- Signs off: human owner
- Updated: when the behaviour changes; `review_by` is set
- Rules for this document:
  - State the behaviour, not the code; give the evidence (a source file, a test, a verified ticket).
  - Applies to names the environments or code lines; if it differs by one, say which.
  - Set `review_by` - behaviour changes with releases.

## `design-spec`

UX/UI specification of a work item - flows, screens, states, accessibility, handoff.

- Directory: `design`
- Required frontmatter: `type`, `title`, `id`, `item`
- Required sections: Flows, Screens, States, Accessibility, Handoff
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: designer
- Reviews: developer and business-analyst
- Signs off: human owner
- Updated: when the requirements or the design system change
- Rules for this document:
  - Every screen lists default, empty, loading and error states.
  - States the accessibility target and the checks that prove it.
  - Handoff names tokens, components and interactions the developer must use.

## `runbook`

Operational procedure - how to deploy, roll back, recover or diagnose a part of the system.

- Directory: `runbooks`
- Required frontmatter: `type`, `title`, `id`
- Required sections: Purpose, Preconditions, Steps, Rollback, Verification, Monitoring
- Statuses: draft -> stable -> deprecated (human verification at: stable)
- Writes: devops
- Reviews: developer
- Signs off: human owner
- Updated: after every incident or pipeline change; `review_by` is set
- Rules for this document:
  - Steps are idempotent or say so.
  - Rollback is written before the change is made.
  - No secret values; name the secret store entry.

