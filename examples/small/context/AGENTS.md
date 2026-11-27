---
type: entry
title: notes-cli - agent entry
description: Command-line note taking.
status: draft
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:14:36Z'
---

# notes-cli - agent entry

The always-loaded entry for this repository. Keep it small; everything else loads on demand through [index.md](/index.md).

## Project

Command-line note taking. Stack: Python. Details: [product](/product.md), [tech-stack](/tech-stack.md), [architecture](/architecture.md).

## Build and verify

```bash
python -m build   # build
python -m pytest   # test
ruff check .   # lint
```

Full flow and definition of done: [workflow](/workflow.md).

## Critical rules

| Rule | Why |
|---|---|
| [Check callers before editing a shared symbol](/rules/blast-radius.md) | A change that suits one caller silently changes the others. |
| [No work item is done without evidence](/rules/evidence-before-done.md) | Claims of 'works' without output cannot be checked by the next reader or agent. |
| [No secrets in the repository](/rules/no-secrets-in-repo.md) | A secret in git history is public for good and costs a rotation across every environment. |
| [Record structural decisions with the reason](/rules/record-decisions.md) | Code shows what was chosen, never what was rejected or why. |
| [Change only what the work item needs](/rules/surgical-changes.md) | Unrelated edits hide the real change from review and raise merge conflicts. |
| [No shell=True with dynamic input](/rules/no-shell-true.md) | Shell metacharacters in input become command execution. |
| [Validate data at the boundary](/rules/typed-boundaries.md) | Unvalidated dicts spread shape assumptions across the code. |

Rules are binding even though they are loaded on demand. A new never-break rule gets a row here and a file in `rules/`.

## Load on demand

| Before... | Read |
|---|---|
| Writing code | the [rules](/rules/) that apply, and the module doc under `modules/` when the repo has modules |
| Starting a work item | the item under `work/` and its stage documents |
| Reviewing | the reviewer role checklist (`ackit prompt reviewer --item ID`) |
| Making a structural choice | the [decisions](/decisions/) and write a new one |
| Ending a session | write a session entry (see the session-entry template: Done / Faced / Decisions / Build / Next / Blockers) |

## Session rules

Check `sessions/` for a pending item first. After implementation work write the session entry and any doc you changed; leave committing and pushing to a person.
