---
type: test-evidence
title: 'Evidence for T-005: ackit branch resolve and proof P1'
item: T-005
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T15:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf13_branches.py
# proof P1: scratch folder outside every repository, read-only copy of the first adopter's registry, script outside the kit
cp <store>/environments/registry.yaml /tmp/p1/registry.yaml && chmod a-w /tmp/p1/registry.yaml
<orchestly venv>/bin/python -I /tmp/p1/compare.py
git -C <store> branch -r > /tmp/p1/store-branches.txt
.venv/bin/ackit branch resolve --bundle /tmp/p1/bundle --environment <id> --author <a> --task <t> --code-base-branch <branch> --code-branch <c> --existing-branches-file /tmp/p1/store-branches.txt
```

## Results

Proof P1, the comparison script (orchestly's `YamlRegistry` with `default_stage_path: defaults.development_stage`, against the kit reader with `key_paths: {default_stage: defaults.development_stage, repositories: code_repos}`):

```
kit problems: []
default_stage uat uat | envs 20 20 | repos 4 4
primary_repo equal: True
checked 300 combos, 0 differences
```

Every environment, every repository (and the environment's own repository) and every stage (and the default) resolves to the same branch, or fails in both. Context branch, run against the store's 291 real branch names (listed by `git branch -r` outside the kit): a code base branch that exists in the store gives that store branch as the base; one that does not exists gives `main` and the message "fallback". The CLI tests cover text, `--json`, exit 1 for an unknown environment or stage and exit 2 without a registry. Orchestly and the store were only read.

## Coverage

Registry mapping on the real file, both resolvers through the CLI, error exits. Not covered: stdin as the branch list source (`-`).
