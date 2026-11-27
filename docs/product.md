---
type: product
title: agent-context-kit
description: Why the kit exists and for whom
status: draft
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:12:45Z'
---

# agent-context-kit

## Purpose

Agents (and people) work better when a repository carries its own small, typed, checkable context: what the product is, how to build and test it, which rules never bend and why, what was decided and why, and what happened in each working session. agent-context-kit defines that as a standard (ACF 1.2) and ships the tools to scaffold, validate, and turn it into role prompts.

## Users

- Developers and teams adopting agent context in any repository, big or small.
- Workflow orchestrators that start agent jobs and need a gate and a prompt per role.
- Agents themselves, which read the entry file first and load the rest on demand.

## Goals

- One spec any tool can implement; a reference validator with exit codes for CI.
- Every document type has a template, rules for the document, and an owner.
- A role prompt can be generated for any role from the bundle alone.
- Adopting needs one command and answers only to what cannot be inferred.

## Non-goals

- No hosting, no network service, no vendor, host or ticket-tool lock-in.
- Not an agent runner; it supplies context and gates, an orchestrator runs jobs.
- No organisation-specific content in the core; that lives in adopter overlays.
