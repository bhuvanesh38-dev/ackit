---
type: test-evidence
title: 'Evidence for T-004: branch_policy and pure resolvers'
item: T-004
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T15:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf13_branches.py
.venv/bin/python -m pytest -q
```

## Results

```
tests/test_acf13_branches.py: 25 passed
full suite: 217 passed, 2 skipped
```

## Coverage

Defaults without the block; the work branch base is the registry's default stage unless the policy or the caller sets one (an explicit stage wins); unknown environment, repository and stage are errors; the context branch base is the code base branch when the caller lists it, otherwise the fallback, and `default-branch` always takes the fallback; nine invalid policy blocks are reported (ACF039); the resolvers are run with `subprocess.Popen` and `socket.socket` replaced by functions that fail, and still resolve. Not covered: odd characters inside author or branch names beyond what the review listed.
