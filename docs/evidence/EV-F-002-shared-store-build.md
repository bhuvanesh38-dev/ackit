---
type: test-evidence
title: 'Evidence for F-002: shared store, design and build'
item: F-002
result: partial
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T08:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
.venv/bin/python -m pytest -q tests/test_guard_baseline.py tests/test_examples.py
```

## Results

```
full suite: 303 passed, 3 skipped
ackit validate docs --strict: 0 errors, 0 warnings
```

The two acceptance criteria of F-002 and the six success criteria of epic E-002, each against its evidence:

| Criterion | State | Evidence |
|---|---|---|
| Design records every decision with options and reason; core names no organisation | met | ADR-0015 to ADR-0020, all accepted; the leakage test passes (`tests/test_examples.py`); review of T-011 |
| Existing bundles validate unchanged; format version 1.3 with a changelog entry | met | the guard on ten old-style bundles (`EV-T-001-baseline-and-guard`), the kit's own `docs/`, `examples/`; `docs/CHANGELOG.md` |
| E-002: two writers never produce the same id | met | proof P2, `EV-T-002-id-allocation` |
| E-002: every one of the 17 gate checks accounted for, each with a test that makes it fire | partly met | all 17 have a disposition and a test checks the table (`EV-T-010-first-adopter-content`); only two entries exist, seven stay hooks, so "each with a test that makes it fire" does not hold for them |
| E-002: the paths consumers read are unchanged after migration, proven by a path diff | not yet | the kit side exists (`consumer_layout`, `ackit link --check`, `EV-T-009-consumer-layout`); the diff needs the migration |
| E-002: `validate --strict` clean on a migrated copy of the store's main project folder | not yet | belongs to the migration stage; W3 only smoke-tested an unmigrated folder (`EV-T-007-author-workspace`) |
| E-002: entry 150 lines or fewer and a typical task loads fewer characters than the baseline | not yet | migration stage |
| E-002: one real orchestly job maintains its context through the new capability | not yet | the pilot, after this feature |

## Coverage

This is the build half of the epic. Everything marked "not yet" depends on a copy of the real store or on the orchestly pilot, which the developer ordered to start after the kit is finished. Proof P3 is partial (counts only; the 20-document sample needs a person).
