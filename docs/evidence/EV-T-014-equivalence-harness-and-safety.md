---
type: test-evidence
title: 'Evidence for T-014: the equivalence harness and its safety checks'
item: T-014
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T13:10:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q <the adopter overlay's tests/test_equivalence_harness.py>
ACKIT_BETA_STORE=<store root> .venv/bin/python -m pytest -q adopters
.venv/bin/python <the adopter overlay's equivalence/harness.py> --source-store <store root> --cases <the smoke cases>
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
harness tests (stub store): 15 passed, 1 skipped (the real-store smoke needs the store path variable)
adopter tests with the store path set: 24 passed
smoke run on the real store source: 4 cases, both routes give identical normalized output, all expectations hold, scratch folder removed
```

What the tests show. The scratch store is built from `git archive HEAD` (committed files only) with a bare `origin` inside the scratch folder; the run refuses to start when any guard trips, and each guard has a test that trips it: emergency-skip variable, tracker address (including a host with credentials, a non-numeric port, a non-loopback host), credential, config and state paths, home folder, proxy and other variables the harness does not control, a remote that is not the scratch origin (fetch and push URL, scp style and scheme URLs), extra remotes, a hooks path, unexpected hooks, a hook link leaving the scratch folder, and (deep scan) any link leaving it. Case steps cannot write outside the repository, touch `.git`, or run git with `-C`, `--git-dir`, push, remote, config and similar. Negative controls: a wrong expectation fails in both routes; a difference between the routes is reported while the expectations hold; a gate that prints nothing, and a gate whose exit code disagrees with its own verdict, fail instead of passing; zero cases and empty expectations are refused. Verdict parsing was checked against the real output format: sections, pass, block, hint and skipped lines, warnings printed in one block, the final line.

Two older tests that run only with the store path set were found stale and fixed: one picked the last argument of an entry as the script (a placeholder was added there in T-012), the other expected a different meaning of the same variable.

## Coverage

This task builds and proves the harness; it proves no check. A firing and a clean case for each check are T-015 and T-016. Not covered: a tracker stand-in (T-016), the real build (stubbed, T-016), the limits of the wrapper on the full copy (T-016). A finding about the adopter's gate (the warnings of checks 8, 9 and 10 are never printed) is in the F-003 journal; it changes how those checks are proven, not the harness.
