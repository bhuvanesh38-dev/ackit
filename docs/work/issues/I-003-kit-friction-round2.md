---
type: issue
id: I-003
title: Kit friction found while dogfooding (round 2)
status: draft
severity: low
history:
- draft
generated:
  by: ackit/1.2.0
  at: '2026-11-19T08:47:31Z'
---

<!-- ACF issue: A bug or defect report and its fix.
  writes: tester or developer | reviews: reviewer | signs off: reviewer
  update when: as the cause becomes known
  rules:
  - Reproduction is concrete enough to run.
  - Done needs test evidence of the fix and a review record.
  - `points` and `runs` (optional) follow the same rules as on a task.
-->

## Symptom

Found while building agent-orchestly round 2 with the kit (B1, B2a, 2026-11-19). Each is small; together they make
agents hand-edit documents instead of using the CLI:
1. `ackit new` leaves placeholder sections and HTML comments; no way to fill sections from the command line.
2. `ackit new` defaults an enum field to its first value (an issue silently gets `severity: critical`).
3. `--slug` lowercases, so `EV-` / `REV-` prefixed evidence and review files must be renamed by hand; `new` does not prefix them with the id.
4. `ackit new` rewrites the whole `index.md` every time.
5. `ackit status` does not check done-requirements (ACF012) and does not refresh `generated.at`.
6. `ackit verify --status` appends to `history` without checking the transition.
7. No CLI to append a log line, journal entry or session entry (`log_entry` exists in `scaffold.py`, not exposed).
8. `ackit validate` takes the bundle positionally (and fails from inside the bundle with `context/context`); every other command uses `--bundle`.
9. `DOC-TYPES.md` regeneration is manual (no `types --markdown --write`).
10. Checkbox acceptance criteria are not tracked by the validator.
11. A decision stays `proposed`; no accept command (could reuse `ackit status`), and no way back from an accidental move.
12. `ackit status` exits 1 on a same-status move (callers must check first).
13. The CLI cannot print the work lifecycle (orchestly keeps a copy only to repair carried-over histories).
14. SPEC says past `runs` are not edited, but a resumed job must update its own run record (upsert by run id).
15. No CLI to set/append frontmatter (`runs`, `depends_on`, `points`); edited by hand.
16. Placeholder bodies ("Checkable criterion", "One paragraph") validate fine; the validator should flag them.
17. ACF018 rejects a `depends_on` to a task not yet written (no forward reference while splitting).
18. `in-review -> blocked` is illegal, so a job that fails after review passed cannot record it.
19. No `wrap-up` role prompt kind: `ackit role check` does not see a `roles/<role>/wrap-up.md` overlay. **Done in 1.2.1** (`wrap-up` is an optional role part; `ackit prompt <role> --part wrap-up`).
20. No CLI to print a role's overlay path. **Done in 1.2.1** (`ackit role path <role>`).
21. (found building orchestly T-005, 2026-11-19) The `points` limits (`scale`, `auto_start_max`, `signoff_max`) can only be read by parsing `ackit.yaml`; no CLI prints them, so an orchestrator duplicates the defaults.
22. No CLI sets `signoff: {by, at}` on a task or small feature (`ackit verify --by` sets `verified`, not `signoff`); a person edits the frontmatter by hand, and the orchestrator's halt message has to say so.
23. `ackit role list --json` needs an existing bundle and prints nothing otherwise, so the built-in role names are not available without one; an orchestrator that validates role names keeps its own copy (tested against the kit).
24. `ackit status` accepts `proposed -> accepted` and then refuses the way back (item 11 again; hit while recording a decision as `proposed` for a person to accept).
25. A task body written by an orchestrator needs "replace section X" (item 1 again): orchestly re-implements section replacement and placeholder detection (item 16) for the readiness step.

26. `ackit status` needs a file path (not a slug) for documents without an id (test-evidence), and `--bundle` must come before the positional arguments.
## Expected

An agent can create, fill, move and close every document through `ackit` alone, and the validator names the fix.

## Reproduction

Build any task end to end with the kit (see orchestly `context/work/tasks/T-002-b1.md` and this repo's I-002).

## Cause

The CLI grew around validation; authoring commands came later.

## Fix

Items 19 and 20 are done (1.2.1, evidence EV-I-003-wrap-up-role-path-findings). The rest is open. Candidate order: 7 (append commands), 1 + 9 (fill sections / required fields), 2, 8, 3, 5 + 6, 4, 9, 10, 11.
