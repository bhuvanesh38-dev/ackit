---
type: task
id: T-007
title: author_workspace and ACF036
status: done
feature: F-002
points: 3
depends_on:
- T-002
signoff:
  by: human:kit-owner
  at: '2026-11-20T12:51:13Z'
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.2.1
  at: '2026-11-20T11:59:05Z'
---

<!-- ACF task: A unit of work under a feature, small enough for one agent session.
  writes: planner or developer | reviews: reviewer | signs off: reviewer
  update when: status changes
  rules:
  - Names the module(s) it touches.
  - Acceptance criteria are checkable.
  - `points` (optional) is in the configured scale; above `signoff_max` it is split before it is ready, above `auto_start_max` it needs `signoff`.
  - `runs` (optional) records each run: id, at, outcome, and optionally tokens, turns, commit, by.
-->

## Goal

Implement the workspace half of ADR-0019. Touches: new `workspace.py`, `scaffold.py` (the generated index), `validate.py`, `SPEC.md`.

## Acceptance criteria

- A document under the configured root must carry `author` equal to its folder name (ACF036, warn)
- Workspace documents are left out of the generated index; the other rules, including the journal and session format rules, still apply (the only size budget is the entry file, which is never in a workspace)
- A copy of one real developer folder validates with the new config and the counts match the expectation recorded in the task

Expectation for the real-folder run, written before it: the copy holds 189 markdown files and none carries an `author` field, so the run reports 189 ACF036 warnings if every file counts. After the review ACF036 skips files that fail to parse or have no type, so the expected count for the same copy is the number of typed files with a parse-clean header (0 for a folder of plain notes).
