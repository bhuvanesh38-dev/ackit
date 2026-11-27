---
type: task
id: T-012
title: Run the adopter's gate through process_checks (stdin pass, scope, placeholders)
status: done
feature: F-002
points: 2
history:
- draft
- ready
- in-progress
- in-review
- done
generated:
  by: ackit/1.3.0
  at: '2026-11-23T07:25:25Z'
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

Close the gap found after T-010: the runner gave commands no standard input, so a git hook could not call `ackit checks run` for push checks, and seven of the store's gate checks were classed "hook only". Add `stdin: pass`, `scope` with `--scope`, and `{bundle}` and `{cwd}` placeholders to `process_checks`, a pre-push hook example, and entries in the adopter overlay that call the adopter's own gate script under the hook name it expects. Touches: `checks.py`, `cli.py`, `SPEC.md`, `hooks/pre-push`, the adopter overlay (`store-config.yaml`, `CHECKS.md`, its test).

## Acceptance criteria

- A command with `stdin: pass` receives the standard input of `ackit checks run`, read once and given identically to every such command; any other command gets no input
- `--scope S` runs only the checks of that scope, no `--scope` only the unscoped; a scoped check asked for by name without its scope exits 2
- `{bundle}` and `{cwd}` are replaced in arguments without a shell; bad `stdin` and `scope` values are reported (ACF041)
- Every one of the store's 17 gate checks has a route through the kit; the entries are run against a real store and a real code clone (read only) and one fires
