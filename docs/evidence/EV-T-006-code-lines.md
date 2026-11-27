---
type: test-evidence
title: 'Evidence for T-006: code_lines, --code-line and proof P3'
item: T-006
result: partial
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T16:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf13_code_lines.py tests/test_validate.py
# proof P3, read only, outside the kit: for every remote store branch, the markdown files that differ from main
git -C <store> diff --name-status origin/main...origin/<branch> -- '*.md' ':(exclude,glob)**/developers/**' ':(exclude,glob)**/sessions/**'
```

## Results

Tests: the new file `tests/test_acf13_code_lines.py` (now including the prompt-side unknown-line check, whitespace and decision filtering) and the ACF035 case in `tests/test_validate.py` pass.

Proof P3, the store as of 2026-11-20 (290 remote branches besides `main`; 389 shared markdown files on `main` outside personal folders), counted on added (A), modified (M) and deleted (D) files:

| Branch group | Branches | Documents that differ from `main` |
|---|---|---|
| Code-line branches (`release/*`, `develop/*`) | 5 | two carry no difference; the others 13, 14 and 18 files (A 7 to 10, M 6 to 8, D 0) |
| All other branches (personal and feature work) | 285 | 133 branches with any shared difference; total A 1092, M 758, D 0; largest 98 |

The counts suggest that per-line differences are small: the code-line branches differ from `main` in at most 18 of about 389 shared markdown files. The classification is an unverified rule, not a finding: an added file is a tag candidate (`code_lines: [<line>]` on the one copy) only if it is not a line-specific rewrite of an existing document, and a modified file is branch-only by construction. Whether tags beat branches is therefore a hypothesis for the migration stage.

## Coverage

Not done: the classification of the 285 other branches (counted only), files other than markdown, and the tie of `release/*` and `develop/*` to the registry's `code_line` ids (they are assumed to be the code-line branches). `<store>` is the first adopter's store, so the run cannot be repeated from this file alone. Needing a person: the sample of 20 documents per branch that checks the classification (the plan's P3 reads a sample). The counts above are the mechanical part; the migration stage decides the modified files. Not covered by tests: `--code-line` combined with `--explain`.
