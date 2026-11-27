# Prompt guide: Support engineer

How to write or tune the prompt for the **support** role. The kit generates the prompt from `prompt.md.j2`; to change it for one repository, copy the part you want to change into `context/roles/support/` (see SPEC section 7).

## 1. Structure of a good role prompt

| Part | What it says | In this role |
|---|---|---|
| Identity | One sentence: who the agent is and what it owns | Draft ticket resolutions, issue patterns and platform-behaviour pages from ticket evidence; a person verifies. |
| Scope | What it may change, and what it must not | Owns `ticket-resolution`, `issue-pattern`, `platform-behaviour`; everything else is read-only; never writes `verified` |
| Inputs it loads | Only what the task needs, in order | the ticket and its evidence, the registered modules, vendors and tenants, the existing pages for the same pattern |
| Rules | Binding statements, each checkable | `rules.md` plus the blocking rules from the bundle |
| Checklist | Verifiable boxes the agent ticks before finishing | `checklist.md` (ids SUP-NN) |
| Output format | Which documents it writes, in what shape | `outputs.md`: the three types, questions at the end of a page |
| Stop conditions | When to stop and ask a person | Stop when: the evidence holds customer personal data to be copied, two sources disagree, or the type of resolution is not decided by the evidence |

## 2. Do

- Name the ticket keys and quote what the customer reported; an agent without evidence guesses.
- Make every missing fact a question under its section, not a placeholder.
- Put rules next to their reason. A rule with a reason is followed in cases the rule did not foresee.
- Keep the prompt small; link the registered values and existing pages instead of pasting them.

## 3. Don't

- Do not write a data change (a statement, a migration) as a recipe to run.
- Do not copy credentials, tokens or customer personal data into a page.
- Do not let the prompt tell the agent to verify a page, mark it stable, commit, push or change a shared system.
- Do not record ticket relations; they stay in the tracker.

## 4. Tuning tip for this role

State which `resolution_type` values need an engineering work item (1 and 5 normally) and what the agent must do when the evidence does not decide the type: leave it empty and ask.

## 5. Example override

An overlay file `context/roles/support/rules.md` replaces the kit's rules for this repository; keep the kit's rules you still need and add yours. Example addition: Add to rules: 'Name the customer-facing impact in one line under Quick summary.'

## 6. Check your change

```bash
ackit validate context          # role definition complete?
ackit prompt support --explain  # which documents were pulled in, and why
```
