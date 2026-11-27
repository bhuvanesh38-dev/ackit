---
type: feature-stage
title: 'Test-Plan: Shared store: design and build'
status: signed-off
signoff:
  by: human:kit-owner
  at: '2026-11-20T12:04:13Z'
feature: F-002
stage: test-plan
generated:
  by: ackit/1.2.1
  at: '2026-11-20T10:43:49Z'
---

## Cases

Test style follows the kit's existing suite (`pytest`, fixtures in `tests/conftest.py`, bundles built in `tmp_path`). New tests live in `tests/test_acf13_*.py`, one file per area. Every case is run by `.venv/bin/python -m pytest -q`; proofs P1 to P4 are recorded as `test-evidence` documents because they use real or copied data.

**Guard (T-001), runs in every task.** G1: a bundle with none of the new keys gives the same errors and warnings as the saved baseline (kit `docs/`, `examples/`, a read-only copy of orchestly's bundle). G2: the guard fails when a rule is made to fire on an old bundle (negative control, recorded once). G3: `ackit validate docs --strict` stays at 0 errors after each task.

**Ids (T-002).**
- I1 sequential allocation unchanged without the key.
- I2 reserved range allocates inside the author's range and continues after the highest used id.
- I3 range exhausted, author missing from `ranges`, and `--author` absent: each gives its documented result and message.
- I4 proof P2: two clones, ten items each, created in parallel processes, merged both ways: with ranges zero ACF009 findings; without ranges the clash is reported.
- I5 ACF009 and ACF016 behave as before.

**Registry (T-003).**
- R1 inline data and `source_file` give the same model; a relative `source_file` resolves against the bundle root, an absolute one is read as given.
- R2 missing file, malformed YAML, unknown `key_paths` entry, duplicate environment id, environment without a repository: each is a clear validation error.
- R3 `extensions` is carried and never interpreted.
- R4 no file other than the configured one is opened (asserted with a monkeypatched `open`).

**Branch policy and resolver (T-004, T-005).**
- B1 work branch comes from the environment's branch at the registry's default stage; an explicit `base_stage` overrides it; an unknown stage is an error.
- B2 context branch is the store branch matching the code base branch when the caller lists it, otherwise the fallback; the name follows `name_pattern` with `{author}` and `{code_branch}`.
- B3 the functions touch no subprocess and no socket (asserted).
- B4 `ackit branch resolve` prints text and `--json`, exit 0, and exit 1 with a message on an unknown environment, repository or stage.
- B5 proof P1: a read-only copy of the real registry of the first adopter resolves every environment, repository and stage to the same branch as orchestly's `YamlRegistry`; every difference is listed and explained. Context-branch resolution is checked against the store's real branch names (supplied by the caller, from `git branch -r` run outside the kit).

**Code lines (T-006).**
- L1 absent `code_lines` means every line; empty list the same.
- L2 `validate --code-line` and `prompt --code-line` keep only matching documents.
- L3 ACF035 is an error for an unknown id when a registry is configured and does not run without one.
- L4 proof P3: per store branch, count the documents that differ from `main` and classify them tag-able or branch-only (a person reads a sample of 20 per branch to check the classification).

**Author workspace (T-007).**
- W1 a document under the root with `author` not equal to its folder gives ACF036 (warn).
- W2 workspace documents are absent from the shared index and from size budgets; the append-only rules still fire on them.
- W3 a copy of one real developer folder validates with the new config; counts match the expectation recorded in T-007.

**Process checks (T-008).**
- C1 a passing command, a failing `block`, a failing `warn`, a missing executable and a timeout: exit codes and messages as designed.
- C2 the command runs as an argument list with no shell (a metacharacter in an argument is passed through, not interpreted).
- C3 proof P4: with no commands configured, `validate`, `branch resolve` and `checks run` open no socket (socket guard fixture).
- C4 `--when` selects only matching entries.

**Consumer layout (T-009).**
- K1 `ackit link --check` reports ok, missing and wrong for entry, rules and links on a temporary tree; nothing is created.

**Adopter content (T-010).**
- A1 the first adopter's mapping and config validate with the kit.
- A2 all 17 store checks are accounted for in a table (7 mapped to ACF rules, 10 as entries); none is missing.
- A3 the leakage grep finds organisation names only under `adopters/`.

**Release (T-011).**
- D1 SPEC, architecture and CHANGELOG contain the 1.3 text; `acf_version` of new bundles is `"1.3"` and 1.0 to 1.2 bundles stay valid.
- D2 the full suite and `ackit validate docs --strict` pass; the guard G1 passes.

**Not tested here:** the orchestly pilot, Ansible and the store migration (later features), and the performance of resolving a registry with hundreds of environments (the real file has about 50; revisit if it grows).

## Environments

- Local, offline: the kit's `.venv` (`.venv/bin/python -m pytest -q`, `.venv/bin/ackit`). No network, no remote, no publishing.
- Real data, read-only copies only: the store's `environments/registry.yaml`, one developer folder and the list of store branch names, all copied into a scratch folder outside every repository before use; the live store is never written.
- agent-orchestly is read-only (imported for the P1 comparison). Nothing in it, the store or the infrastructure repository is edited.
- Exit criteria for F-002: every case above passes or has a recorded reason, the four proofs are saved as `test-evidence`, the guard is green, and the developer has run `ackit verify` on the five ADRs.
