---
type: tech-stack
title: agent-context-kit tech stack
description: Languages, frameworks and infrastructure
status: draft
languages:
- Python
frameworks:
- PyYAML
- Jinja2
generated:
  by: ackit/0.1.0
  at: '2026-11-17T15:12:45Z'
---

# Tech stack

## Languages and frameworks

- Python 3.12 or newer
- PyYAML (frontmatter, config, registry), Jinja2 (templates and prompts), argparse (CLI), pytest (tests)

Versions are taken from: pyproject.toml.

## Infrastructure

None. A local CLI and library; CI snippets for common hosts are examples only (see `ci/`).

## Conventions

Standard library first; the type registry (`types.yaml`) is data, not code; every validation rule has a code and a test; templates are data files.
