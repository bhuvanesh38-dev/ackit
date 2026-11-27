# Prompt guide: Developer

How to write or tune the prompt for the **developer** role. The kit generates the prompt from `prompt.md.j2`; to change it for one repository, copy the part you want to change into `context/roles/developer/` (see SPEC section 7).

## 1. Structure of a good role prompt

| Part | What it says | In this role |
|---|---|---|
| Identity | One sentence: who the agent is and what it owns | Implement the work item with the smallest verified change. |
| Scope | What it may change, and what it must not | Owns the doc types in `role.yaml` (`owns`); everything else is read-only |
| Inputs it loads | Only what the task needs, in order | the item, its module docs, blocking rules, workflow commands |
| Rules | Binding statements, each checkable | `rules.md` plus the blocking rules from the bundle |
| Checklist | Verifiable boxes the agent ticks before finishing | `checklist.md` (ids DEV-NN) |
| Output format | Which documents it writes, in what shape | `outputs.md`: code diff, test evidence, session entry, journal entries |
| Stop conditions | When to stop and ask a person | Stop when: the item is `draft`, a blocking rule would be broken, or a symbol with many callers must change |

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

Keep the build and test commands in the prompt; add 'run `./gradlew test` before saying done' style lines for your stack.

## 5. Example override

An overlay file `context/roles/developer/rules.md` replaces the kit's rules for this repository; keep the kit's rules you still need and add yours. Example addition: Add a rule: 'Never edit files under `generated/`; change the generator instead.' to roles/developer/rules.md.

## 6. Check your change

```bash
ackit validate context          # role definition complete?
ackit prompt developer --item F-001 --explain   # which documents were pulled in, and why
```
