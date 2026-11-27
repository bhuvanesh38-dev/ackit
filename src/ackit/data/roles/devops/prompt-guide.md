# Prompt guide: DevOps engineer

How to write or tune the prompt for the **devops** role. The kit generates the prompt from `prompt.md.j2`; to change it for one repository, copy the part you want to change into `context/roles/devops/` (see SPEC section 7).

## 1. Structure of a good role prompt

| Part | What it says | In this role |
|---|---|---|
| Identity | One sentence: who the agent is and what it owns | Make build, deploy and operations repeatable and reversible. |
| Scope | What it may change, and what it must not | Owns the doc types in `role.yaml` (`owns`); everything else is read-only |
| Inputs it loads | Only what the task needs, in order | workflow, environments reference, runbooks, incidents |
| Rules | Binding statements, each checkable | `rules.md` plus the blocking rules from the bundle |
| Checklist | Verifiable boxes the agent ticks before finishing | `checklist.md` (ids OPS-NN) |
| Output format | Which documents it writes, in what shape | `outputs.md`: workflow, runbook, change record (handoff) |
| Stop conditions | When to stop and ask a person | Stop when: a step needs production credentials or a direct change to a shared system |

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

Name the environments, the pipeline system and the secret store so nothing is guessed.

## 5. Example override

An overlay file `context/roles/devops/rules.md` replaces the kit's rules for this repository; keep the kit's rules you still need and add yours. Example addition: Add to checklist: '- [ ] **OPS-10** Cost impact of new resources estimated.'

## 6. Check your change

```bash
ackit validate context          # role definition complete?
ackit prompt devops --item F-001 --explain   # which documents were pulled in, and why
```
