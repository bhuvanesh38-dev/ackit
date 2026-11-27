# Prompt guide: Code reviewer

How to write or tune the prompt for the **reviewer** role. The kit generates the prompt from `prompt.md.j2`; to change it for one repository, copy the part you want to change into `context/roles/reviewer/` (see SPEC section 7).

## 1. Structure of a good role prompt

| Part | What it says | In this role |
|---|---|---|
| Identity | One sentence: who the agent is and what it owns | Decide if the change is correct and safe to merge. |
| Scope | What it may change, and what it must not | Owns the doc types in `role.yaml` (`owns`); everything else is read-only |
| Inputs it loads | Only what the task needs, in order | the item, diff, evidence, blocking rules, module docs |
| Rules | Binding statements, each checkable | `rules.md` plus the blocking rules from the bundle |
| Checklist | Verifiable boxes the agent ticks before finishing | `checklist.md` (ids REV-NN) |
| Output format | Which documents it writes, in what shape | `outputs.md`: review record with verdict |
| Stop conditions | When to stop and ask a person | Stop when: test evidence is missing, or the change exceeds the item's scope |

## 2. Do

- Name the work item and quote its acceptance criteria; an agent without an item guesses.
- Put rules next to their reason (Why). A rule with a reason is followed in cases the rule did not foresee.
- Make every checklist line verifiable by a command, a grep or a document check.
- Give stop conditions. An agent that cannot stop will improvise.
- Keep the prompt small; link bundle documents (load on demand) instead of pasting them.

## 3. Don't

- Do not restate the whole repository in the prompt; `ackit prompt` already selects what is relevant.
- Do not write "be careful" or "write good code"; write the check that proves it.
- Do not give the role write access to documents it does not own.
- Do not let the prompt tell the agent to commit, push, merge or change shared systems.

## 4. Tuning tip for this role

State the severity scale and what blocks a merge; reviewers drift without one.

## 5. Example override

An overlay file `context/roles/reviewer/rules.md` replaces the kit's rules for this repository; keep the kit's rules you still need and add yours. Example addition: Add to rules: 'Reject any change that adds a dependency without an ADR.'

## 6. Check your change

```bash
ackit validate context          # role definition complete?
ackit prompt reviewer --item F-001 --explain   # which documents were pulled in, and why
```
