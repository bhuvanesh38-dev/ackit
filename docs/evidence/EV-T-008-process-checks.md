---
type: test-evidence
title: 'Evidence for T-008: process_checks, ackit checks run and proof P4'
item: T-008
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T18:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf13_checks.py tests/test_validate.py
```

## Results

```
tests/test_acf13_checks.py: 20 passed (after the review); with tests/test_validate.py the run passes
```

Covered (C1, C2, C4): a passing command, a failing `block` (exit 1), a failing `warn` (printed, exit 0), a missing executable and a timeout (failures with a message), `--when` and `--name` selection, ten invalid configurations (exit 2, ACF041), the working directory and the `ACKIT_BUNDLE` and `ACKIT_CHECK_WHEN` variables, and an argument containing shell metacharacters that is passed through and never interpreted (a marker file is not created).

Proof P4 (C3), a tripwire and not a formal proof: with socket creation, `connect`, `create_connection`, name lookup and `subprocess.Popen` replaced by functions that fail, `ackit validate` (exit 0), `ackit checks run` with no commands and `ackit branch resolve` complete, so none of the three reached for the network or a child process; and a static test (`test_p4_static_core_imports_no_network_library`) confirms that nothing under `src/ackit` imports socket, urllib, http, ssl, requests, ftplib, smtplib or asyncio. The commands an adopter lists are outside this statement, by design (ADR-0016).

## Coverage

Also covered after the review: a timeout kills the whole process group (a grandchild is checked), non-UTF-8 output, a silent failing command, no standard input, `--name` with the wrong `--when` (exit 2), ACF041 through `validate`, non-integer and boolean timeouts. Not covered: the 64 KiB output cap, relative executable lookup against `--cwd`, Windows.
