---
type: test-evidence
title: 'Evidence for T-018: the three support types'
item: T-018
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T22:30:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_support_types.py
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
tests/test_support_types.py: 43 passed
full suite: 406 passed, 7 skipped (the guard test passes with its baseline unchanged)
ackit validate docs --strict: 0 errors
```

What the tests show. Each of `ticket-resolution`, `issue-pattern` and `platform-behaviour` is declared with the required keys, the sections, the `doc` status set (human verification at stable), `dir: ""` and the ownership text of the design. A complete page of each type has no error; each missing section is reported by ACF005; a missing `resolution_type` or `tickets` by ACF004. `resolution_type` accepts 1 to 6; 0, 7, the string `"1"`, a word and an empty value give ACF026 (values are compared by type and value, so the string "1", the float 1.0 and the boolean true are refused; this tightened the enum check for every type, and no existing bundle uses a non-string enum). A page at the top, under `support/`, and under `<environment>/<tenant>/support/...` raises no ACF022. `ackit new` creates each type with its sections from a template, and `docs/DOC-TYPES.md` is regenerated (only additions).

## Coverage

Not in this task: the controlled vocabularies for module, vendor and tenant (T-019), the `support` role (T-020), the format version (T-021). A numeric choice such as `resolution_type` is not defaulted by `ackit new`, so an unclassified draft is reported (ACF004) instead of looking like a data fix. The optional keys (`tickets` shape, `tenants`, `vendors`, `module`, `scope`, `code_line`) are documented but not yet checked: the vocabularies of T-019 do that. A page can be created flat at the bundle root only; a nested casebook path is the adopter's layout. `ackit new` fills `title` and `status`; `description` and, for a ticket resolution, `resolution_type` and `tickets` come from `--set` or are filled by the author, as for the other types.
