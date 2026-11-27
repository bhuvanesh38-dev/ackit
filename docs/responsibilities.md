---
type: responsibility
title: agent-context-kit responsibilities
description: Who is responsible for what (RACI)
status: draft
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:12:45Z'
---

# Responsibilities

## Areas

List the areas of the repo or process this covers (modules, release, security, docs).

## Roles

Roles are defined as profiles (`role.yaml`): kit built-ins plus any custom roles in `roles/`. Add the humans who fill them.

| Role | Description | Owns (doc types) | Gates | Person |
|---|---|---|---|---|
| architect | Architect | architecture, module, decision, tech-stack | start | maintainer |
| business-analyst | Business analyst | product, epic, feature | start | maintainer |
| designer | UX/UI designer | design-spec | start | maintainer |
| developer | Developer | task, session, session-index, handoff | start, handoff | maintainer |
| devops | DevOps engineer | workflow, runbook, incident | start, handoff | maintainer |
| maintainer | Context maintainer | rule, responsibility, reference | - | maintainer |
| planner | Planner | feature-stage, task | start | maintainer |
| reviewer | Code reviewer | review | handoff | maintainer |
| security | Security reviewer | review | handoff | maintainer |
| tester | Tester | test-evidence, issue | start, handoff | maintainer |

## RACI

R = responsible (writes it), A = accountable (signs off; exactly one per row), C = consulted (reviews), I = informed. Derived from the document types and the role profiles; edit when your team differs.

| Document type | R (role) | C (reviews) | A (signs off) |
|---|---|---|---|
| entry | any | any human owner | human owner |
| product | business-analyst | human owner | human owner |
| tech-stack | architect | reviewer | human owner |
| workflow | devops | reviewer | human owner |
| architecture | architect | reviewer | human owner |
| module | architect | reviewer | module owner |
| rule | maintainer | human owner | human owner |
| responsibility | maintainer | human owner | human owner |
| epic | business-analyst | human owner | human owner |
| feature | business-analyst | reviewer | human owner per stage |
| feature-stage | planner | reviewer | human owner (signoff.by) |
| task | developer, planner | reviewer | reviewer |
| issue | tester | reviewer | reviewer |
| incident | devops | human owner | human owner |
| decision | architect | reviewer | human owner |
| journal | any | none | none |
| session | developer | none | none |
| session-index | developer | none | none |
| review | reviewer, security | developer (resolves findings) | reviewer |
| test-evidence | tester | reviewer | reviewer |
| handoff | developer | human owner | human owner |
| reference | maintainer | reviewer | none |
| design-spec | designer | developer and business-analyst | human owner |
| runbook | devops | developer | human owner |
