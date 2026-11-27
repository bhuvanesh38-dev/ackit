---
type: decision
id: ADR-0010
title: Python, argparse, Jinja2, PyYAML
status: proposed
date: '2026-11-17'
description: Python 3.12, argparse, Jinja2 and PyYAML.
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:13:35Z'
---

## Context

The tool must install anywhere and read files fast.

## Options

1. Python with typer and pydantic.
2. Python with the standard library plus two small dependencies.
3. Go or Rust single binary.

## Decision

Python 3.12, argparse, Jinja2 and PyYAML.

## Why

Two dependencies, no compiled parts, easy to vendor. A single binary is attractive later; the data-driven design makes a port possible.

## Consequences

Python 3.12 or newer is required.
