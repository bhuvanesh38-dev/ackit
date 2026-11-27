---
type: test-evidence
title: 'Evidence for T-015: commit-mode cases'
item: T-015
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T14:10:00Z'
---

## Commands

```bash
.venv/bin/python <the adopter overlay's equivalence/harness.py> --source-store <store root> --cases <the commit-mode cases>
ACKIT_BETA_STORE=<store root> .venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
commit-mode cases on the real store source: 39 cases (plus the 4 smoke cases), every case passes in both routes; scratch folder removed
the run ends with: check 4: skipped in both routes in every case, not proven
full suite with the store path set: 345 tests, all passing
```

Each check that runs on commit has a clean case and a case that makes it act, run through the direct route and the kit route:

| Check | Fires | Clean |
|---|---|---|
| 1 protected branch (code) | block on `main` | pass on a feature branch |
| 2 session context | warn: file missing; warn: fields missing | pass: all fields |
| 3 migration name (code) | block: bad `core_db` name; block: bad `list_db` name | pass: `core_db` name; pass: `list_db` name |
| 4 build (code) | skipped at commit time, by design: reported by the run as not proven | not applicable |
| 5 links | warn: dead link | pass; skipped with no markdown staged |
| 6 migration content (code) | block: `COLLATE`; block: comment syntax; warn: `ENGINE=` | pass |
| 7 journal nudge | warn: no journal; warn: journal not touched | pass |
| 8 index freshness | hint line (the warning is never printed by the gate) | pass |
| 9 staleness | hint line (same) | pass |
| 10 entry-file size | hint line (same) | pass |
| 11 local-only leakage | hint line (same) | pass |
| 12 traceability | warn: dangling section reference | pass |
| 13 raw conversions (code) | block: names the file | pass |
| 14 data-changing SQL | block | pass |
| 16 dummy commits | block: empty; block: whitespace only | pass |

Real `git commit` cases (each route installs its own hook): `--amend` creates the commit; `--allow-empty` is blocked with the empty-commit message. A commit-flow case also requires proof that the hook ran the gate (the gate's sections, or the kit's PASS line for the gate entry), compares the gate text of a blocked commit between the routes, and accepts only `--amend`, `--allow-empty`, `-q` and `-m <message>` as arguments. A test installs a hook that runs nothing and expects the case to fail.

## Coverage

Checks 8, 9, 10 and 11 are proven through their hint lines only, because the gate collects their warnings and never prints them; a test fails if any commit-time check except 4 lacks a case that expects only clean results and a case that expects the check to act. The harness's `not_proven` lists the checks skipped throughout (4). Checks 15 and 17 run on push and are T-016. Check 4 runs the build only on push (T-016); at commit time it is skipped in both routes and reported as such, not as proven.
