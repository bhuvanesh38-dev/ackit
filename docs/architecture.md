---
type: architecture
title: agent-context-kit architecture
description: Components and data flow
status: draft
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:12:45Z'
review_by: '2027-05-16T15:12:45Z'
---

# Architecture

## Overview

`ackit` is a small library plus CLI. Behaviour is driven by data files shipped in `src/ackit/data/`: the type registry, body templates, role directories, and stack packs. Code interprets the data; adding a type, role or pack is a data change.

## Components

- `bundle.py`: load a bundle (frontmatter, config, registry); lookups by id and path.
- `validate.py`: ACF rules with stable codes and configurable severity.
- `gates.py`: start and handoff gates over the validator and the bundle.
- `roles.py`: role profiles, overlay resolution, custom roles, role validation.
- `prompt.py`: assemble a role prompt with progressive disclosure and an explain trace.
- `scaffold.py`: new documents, ids, index, log, verify.
- `init.py`: stack detection, module discovery, interview, scaffold from a pack.
- `importer.py`: map an existing layout into a bundle using a mapping file.
- `cli.py`: argparse front end.

## Data flow

`init` reads the repository and a pack, renders templates, writes a bundle. `validate` loads the bundle and the registry and emits issues. `prompt` loads the bundle, resolves the role, selects relevant documents, renders the role template.

## Constraints

The standard is host, tool and company agnostic (see ADR-0012). The core never reads outside the bundle and the repository being initialised, and never uses the network, with two stated exceptions added in ACF 1.3 (ADR-0016):

1. `environment_registry.source_file` may point outside the bundle. The file is read only when the adopter configures it, read-only, as one local file; no other file is opened. This is the one opt-in read outside the bundle.
2. `process_checks` commands are written by the adopter and run by `ackit checks run`. They may do anything the adopter decides, network access included. The core itself still opens no connection and starts no process except for these commands (a tripwire test covers `validate`, `branch resolve` and `checks run`).

The shared-store capability (registry, branch policy, code lines, id ranges, author workspaces, process checks, consumer layout) is all optional configuration in `ackit.yaml`. The core validates and resolves names; callers read git and create branches.
