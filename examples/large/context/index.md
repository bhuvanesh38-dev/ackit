---
acf_version: "1.2"
---

# shop-platform - context index

Progressive disclosure: read `AGENTS.md` first, then only what the task needs. Regenerate with `ackit index --write`.

## Entry and core

- [shop-platform - agent entry](/AGENTS.md) - Online shop backend.
- [shop-platform architecture](/architecture.md) - Components and data flow
- [shop-platform](/product.md) - Online shop backend.
- [shop-platform responsibilities](/responsibilities.md) - Who is responsible for what (RACI)
- [shop-platform tech stack](/tech-stack.md) - Languages, frameworks and infrastructure
- [shop-platform workflow](/workflow.md) - Build, test, lint and review flow

## Modules

- [M-catalog: catalog](/modules/catalog.md) - Module catalog at catalog
- [M-checkout: checkout](/modules/checkout.md) - Module checkout at checkout
- [M-payments: payments](/modules/payments.md) - Module payments at payments

## Rules

- [R-blast-radius: Check callers before editing a shared symbol](/rules/blast-radius.md)
- [R-evidence-before-done: No work item is done without evidence](/rules/evidence-before-done.md)
- [R-no-jdbc-in-loops: No repository or JDBC call inside a loop](/rules/no-jdbc-in-loops.md)
- [R-no-secrets-in-repo: No secrets in the repository](/rules/no-secrets-in-repo.md)
- [R-record-decisions: Record structural decisions with the reason](/rules/record-decisions.md)
- [R-surgical-changes: Change only what the work item needs](/rules/surgical-changes.md)

## Work

- [Analysis: Split payment](/work/features/F-001-split-payment/01-analysis.md)
- [Design: Split payment](/work/features/F-001-split-payment/02-design.md)
- [Plan: Split payment](/work/features/F-001-split-payment/03-plan.md)
- [Tasks: Split payment](/work/features/F-001-split-payment/04-tasks.md)
- [Test-Plan: Split payment](/work/features/F-001-split-payment/05-test-plan.md)
- [F-001: Split payment](/work/features/F-001-split-payment/feature.md)

## Decisions

- [ADR-0001: Adopt the Agent Context Format](/decisions/ADR-0001-adopt-the-agent-context-format.md) - Why this repository keeps agent context as ACF
- [ADR-0002: Use an outbox for payment events](/decisions/ADR-0002-use-an-outbox-for-payment-events.md)

## Journals

- [shop-platform journal](/journals/project.md)
- [Journal: Split payment](/work/features/F-001-split-payment/06-journal.md)
