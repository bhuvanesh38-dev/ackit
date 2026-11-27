---
type: test-evidence
title: 'Evidence for T-011: documents for 1.3.0'
item: T-011
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T21:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
.venv/bin/python -m pytest -q tests/test_guard_baseline.py tests/test_examples.py
.venv/bin/ackit types --markdown      # DOC-TYPES is generated from it
```

## Results

```
full suite: 303 passed, 3 skipped (the skipped ones need an external store or bundle named by an environment variable)
ackit validate docs --strict: 0 errors, 0 warnings
guard (ten old-style bundles, unchanged) and leakage test: pass
```

SPEC section 11 describes every 1.3 addition (id allocation and `ids assign`, environment registry, branch policy and `branch resolve`, code lines, author workspace, process checks, consumer layout) and the rule table lists ACF035 to ACF042. `docs/architecture.md` carries the two amendments of ADR-0016 (the registry file may be outside the bundle; adopter commands run outside the core's no-connection statement). The README states the same exception. The changelog lists each addition with its task and ADR. `DOC-TYPES.md` is regenerated. ADR-0015 to ADR-0017 and ADR-0019 are accepted by the kit owner; ADR-0020 is `proposed` and waits for the owner's own `ackit verify`; no agent accepted an ADR. The two-branch `ids assign` case that review T-002 asked for is a test.

## Coverage

Not covered: ACF 1.3 in a real adopter store (the migration stage), and the orchestly pilot, which start after this feature.
