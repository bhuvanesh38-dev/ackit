---
type: test-evidence
title: 'Evidence for T-010: the first adopter overlay for the shared store'
item: T-010
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T20:30:00Z'
---

## Commands

```bash
ACKIT_BETA_STORE=<store root> .venv/bin/python -m pytest -q <the adopter overlay's tests/test_store_config.py>
.venv/bin/python -m pytest -q tests/test_examples.py
.venv/bin/python -m pytest -q
```

## Results

```
test_store_config.py: 5 passed (the real-layout test ran with the store root given, read only)
tests/test_examples.py (leakage test): 4 passed
```

A1: the overlay's `store-config.yaml` (registry mapping through `source_file` and key paths, branch policy, workspace, consumer layout, the entry-file budget and two process-check entries) is read by the kit's own parsers with no problem; a registry shaped like the store's resolves through the mapping; and with the store root given, both entries' scripts exist relative to it. Proof P1 (T-005) already ran the same mapping against a read-only copy of the real registry: 300 combinations, zero differences.

A2: `CHECKS.md` gives each of the 17 gate checks a disposition and the test fails if a number is missing, a disposition is unknown, or an entry is unused: 2 rule, 4 rule plus gate, 4 entry rows served by two entries, 7 hook only. This corrects the planning estimate (seven rules, ten entries): the independent review of T-010 showed that the kit's rules cover fewer of the document checks than assumed (a different field, a different file or only the format) and that most code and process checks cannot be run by a command that gets no standard input and no hook context (Java conversions read a diff on standard input; checks 15 and 17 read the pushed refs). They stay hooks until the migration stage proves an equivalent. A3: the leakage test passes, and a search of the kit for the organisation's names finds them only under `adopters/` and in the test that lists them. The stage mapping covers the six store stages.

## Coverage

Not done: the entries were not run against the live store (the store is only read; the migration stage decides when). `stage-mapping.yaml` is validated only against the kit's stage names. `store-gate` runs the gate in commit mode; which of its findings block is the gate's own decision.
