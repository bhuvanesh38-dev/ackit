---
type: test-evidence
title: 'Evidence for T-019: vocabularies and rules ACF043 and ACF044'
item: T-019
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-24T08:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_vocabularies.py tests/test_validate.py tests/test_guard_baseline.py
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
full suite: 451 passed, 7 skipped (the guard test passes with its baseline unchanged)
ackit validate docs --strict: 0 errors
```

A vocabulary takes its values from a list in `ackit.yaml`, from a local source file with a dotted key path (a list of strings, a mapping whose keys are the values, or a list of mappings with an `id_key`), or from the ids of the documents of a type. A field bound with `vocab: {field: vocabulary}` on a type holds a string or a list of strings; an unregistered value is ACF043 with a "did you mean" hint when a close value exists; a value that is not a string is ACF043. A field that is absent or empty is not checked. A vocabulary that a binding names but the bundle does not define is not checked, and a bundle without a `vocabularies` block is not checked at all. An adopter can bind a field of any type through the `types:` override. ACF044 fires for 28 configuration faults, each with its own test (including the keys that are not strings, which crashed before the review), (not a mapping, a bad name, a source that is not a mapping, none or two sources, an unknown key, a value list of the wrong shape or empty, a value that is not a non-empty string, an unknown type, a missing file, a missing key path, a path not in the file, a node of the wrong shape, a file that is not YAML, an empty `id_key`), each with its own test. The rule table test has a firing case for each of ACF043 and ACF044.

## Coverage

The `ticket-resolution` type binds `module`, `vendors` (to the `vendor` vocabulary) and `tenants`; the adopter decides which vocabularies exist. A binding to an undefined vocabulary is silent on purpose (a typo in an adopter's own binding is not reported). A vocabulary that has a configuration problem is not used, so it adds no ACF043. An override of `ticket-resolution` in `types:` keeps the core binding unless it sets `vocab: {}`. The vocabulary is read on every validation run: a source file that is large would be read each time. The `support` role (T-020) and the format version (T-021) are separate.
