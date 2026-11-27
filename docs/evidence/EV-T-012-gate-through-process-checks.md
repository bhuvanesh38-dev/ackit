---
type: test-evidence
title: 'Evidence for T-012: the adopter gate through process_checks'
item: T-012
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T10:30:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf13_checks.py
ACKIT_BETA_STORE=<store root> .venv/bin/python -m pytest -q <the adopter overlay's tests/test_store_config.py>
# a scratch bundle whose scripts folder is a link to the store's scripts (read only) and whose ackit.yaml holds the overlay's process_checks
.venv/bin/ackit checks run --bundle /tmp/gt --when pre-commit --cwd <store root>
.venv/bin/ackit checks run --bundle /tmp/gt --when pre-push --cwd <store root> --json < refs.txt
.venv/bin/ackit checks run --bundle /tmp/gt --when pre-commit --scope code --cwd <a real code clone>
.venv/bin/ackit checks run --bundle /tmp/gt --when pre-commit --scope code --cwd /tmp/cc     # a scratch repository
```

## Results

```
tests/test_acf13_checks.py: 24 passed (four new tests for stdin, scope, placeholders, bad values)
the overlay test with the store root given: 5 passed
```

Against the real store (read only, nothing staged): `store-gate` runs the store's gate in commit mode through the kit and reports its verdict (the gate blocked, as it does by hand, with the same first lines of output). `store-gate-push` with a pushed-refs line on standard input runs the gate in push mode ("Mode: push" in its own output) and passes. Against a real code clone: `code-gate-pre-commit` runs the gate in code-clone mode (branch checks of the clone, "Not a protected branch") and passes. A check that fires: in a scratch repository on branch `main` with a staged file, `code-gate-pre-commit` fails (check 1, protected branch); after switching to `feature-x` it passes. Checks 1, 3, 4, 6, 13, 15 and 17, first classed "hook only", are now wired as entries; the overlay test checks the table (2 rule, 4 rule plus gate, 11 entry). Exercised: the gate's verdict reaching the kit in commit and push mode (store) and commit mode (code clone), the pushed refs reaching the gate ("Mode: push"), and check 1 firing on a scratch repository (not on the real clone). Only wired, not exercised: 3, 4, 6, 13, 15, 17 and the `code-gate-pre-push` entry (not run at all). The runs used a scratch bundle that links to the store's scripts, because `<store>/<project>/ackit.yaml` does not exist yet (it needs a store pull request), so `--bundle <store>/<project>` was not run end to end.

Gaps found in review, both fixed and proven: (1) check 16 reads its parent's command line for `--amend`; the kit now gives a command `{git_command}` (the nearest `git` process above the hook) and the overlay wrapper keeps itself as the gate's parent with that text in its own arguments (`exit $?` stops the shell replacing itself by the gate). Proof on a scratch store-like repo with the real gate: `git commit --amend -m` passes, `git commit --allow-empty` still blocks. (2) `{tmpdir}` is removed after a normal run and after a timeout kill (two tests). The kit also prints a failing check's own output, so a hook user sees the real reason.

## Coverage

Not run: the push-mode entry in a code clone (it runs the build and the store-PR check, which needs a real push in progress); checks 3, 6, 13 and 15 were not made to fire one by one, only the protected-branch check was. They run inside the same gate script that the hooks run today, so the kit adds a route, not a re-implementation; equivalence of the full behaviour is for the migration stage. The hook example `hooks/pre-push` was not installed in a real clone.
