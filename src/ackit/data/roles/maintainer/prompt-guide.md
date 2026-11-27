# Prompt guide: Context maintainer

How to write or tune the prompt for the **maintainer** role. The kit generates the prompt from `prompt.md.j2`; to change it for one repository, copy the part you want to change into `context/roles/maintainer/` (see SPEC section 7).

## 1. Structure of a good role prompt

| Part | What it says | In this role |
|---|---|---|
| Identity | One sentence: who the agent is and what it owns | Keep the bundle accurate, small and valid. |
| Scope | What it may change, and what it must not | Owns the doc types in `role.yaml` (`owns`); everything else is read-only |
| Inputs it loads | Only what the task needs, in order | the whole bundle, `ackit validate` output |
| Rules | Binding statements, each checkable | `rules.md` plus the blocking rules from the bundle |
| Checklist | Verifiable boxes the agent ticks before finishing | `checklist.md` (ids MNT-NN) |
| Output format | Which documents it writes, in what shape | `outputs.md`: updated docs, log entry, regenerated index |
| Stop conditions | When to stop and ask a person | Stop when: a document would need human verification you cannot give |

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

Point it at `ackit validate --strict` and the staleness policy of the team.

## 5. Example override

An overlay file `context/roles/maintainer/rules.md` replaces the kit's rules for this repository; keep the kit's rules you still need and add yours. Example addition: Add to rules: 'Archive journals older than a year into journals/archive/.'

## 6. Check your change

```bash
ackit validate context          # role definition complete?
ackit prompt maintainer --item F-001 --explain   # which documents were pulled in, and why
```
