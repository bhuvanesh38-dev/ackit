---
type: test-evidence
title: 'Evidence for T-007: author_workspace'
item: T-007
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T17:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf13_workspace.py tests/test_validate.py
# W3: a read-only copy of one real developer folder in a scratch bundle outside every repository
cp -r <store>/<project>/developers/<one developer> /tmp/w3/b/developers/<one developer>
printf 'author_workspace: {root: "developers/{author}"}\n' > /tmp/w3/b/ackit.yaml
.venv/bin/ackit validate /tmp/w3/b --json
```

## Results

Tests: the new file `tests/test_acf13_workspace.py` (absent block, whole-part matching, author must equal the folder, index exclusion with other rules still firing, `in_index: true`, nine bad configurations) and the ACF036 and ACF040 cases of `tests/test_validate.py` pass; after the review also: a workspace journal fires ACF020, untyped and unparsable files get no ACF036, a non-string author is refused, and roots that never match are refused.

W3, a smoke test on a folder that is not migrated yet: the copy holds 189 markdown files, none with frontmatter or an `author` field. The expectation is written in the task body. Before the review fix the run reported 189 ACF036 (one per file) and kept the folder out of the generated index; after it, files without a type or with a broken header get ACF001 or ACF002 and no ACF036, so the run says nothing about `author` until the files are migrated. This proves the index exclusion and the folder matching on real paths, not the author check on realistic documents; a run on a migrated sample belongs to the migration stage.

## Coverage

Not covered: size budgets (the only one is the entry file, never in a workspace); a root deeper than two parts is a unit case only; Windows separators.
