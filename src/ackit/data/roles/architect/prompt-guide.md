# Prompt guide: Architect

How to write or tune the prompt for the **architect** role. The kit generates the prompt from `prompt.md.j2`; to change it for one repository, copy the part you want to change into `context/roles/architect/` (see SPEC section 7).

## 1. Structure of a good role prompt

| Part | What it says | In this role |
|---|---|---|
| Identity | One sentence: who the agent is and what it owns | Decide structure and record why. |
| Scope | What it may change, and what it must not | Owns the doc types in `role.yaml` (`owns`); everything else is read-only |
| Inputs it loads | Only what the task needs, in order | architecture, module docs, tech stack, blocking rules, decisions |
| Rules | Binding statements, each checkable | `rules.md` plus the blocking rules from the bundle |
| Checklist | Verifiable boxes the agent ticks before finishing | `checklist.md` (ids ARC-NN) |
| Output format | Which documents it writes, in what shape | `outputs.md`: architecture and module docs, decision records, design stage |
| Stop conditions | When to stop and ask a person | Stop when: a design would break a tier rule with no accepted exception |

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

List the tier or dependency rules in the prompt text so they are checked, not remembered.

## 5. Example override

An overlay file `context/roles/architect/rules.md` replaces the kit's rules for this repository; keep the kit's rules you still need and add yours. Example addition: Add to checklist: '- [ ] **ARC-09** Capacity estimate for the new table or queue.'

## 6. Check your change

```bash
ackit validate context          # role definition complete?
ackit prompt architect --item F-001 --explain   # which documents were pulled in, and why
```
