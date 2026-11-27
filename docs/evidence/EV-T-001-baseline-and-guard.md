---
type: test-evidence
title: 'Evidence for T-001: baseline and guard'
item: T-001
result: pass
status: final
generated:
  by: plane-session/agent
  at: '2026-11-20T13:05:00Z'
---

## Commands

```bash
# baseline recorded from the unchanged 1.2.1 code (`git diff --stat -- src` printed nothing immediately before each recording)
ACKIT_UPDATE_BASELINE=1 .venv/bin/python -m pytest -q tests/test_guard_baseline.py -k old_bundles
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
.venv/bin/ackit validate <read-only path of agent-orchestly's context bundle> --strict
.venv/bin/ackit validate examples/small/context --strict
.venv/bin/ackit validate examples/large/context --strict
```

## Results

Raw output, 2026-11-20 (the baseline was re-recorded after the independent review, see Coverage):

```
150 passed, 2 skipped in 55.61s

kit docs:             73 documents: 0 error(s), 0 warning(s)   exit=0
orchestly (read-only): 86 documents: 0 error(s), 0 warning(s)   exit=0
examples/small:       16 documents: 0 error(s), 0 warning(s)   exit=0
examples/large:       25 documents: 0 error(s), 0 warning(s)   exit=0
```

`tests/baselines/acf12.json` pins the findings (code, severity, path, message, order) of ten old-style bundles: the shipped small and large examples; five bundles made by `ackit init` (java, node, python, go, plain); `broken` (12 findings: ACF005, ACF006, ACF008, ACF009, ACF016, ACF018, ACF024, ACF031); `acf12-fields` (9 findings; valid `points`, `runs` and `external_id` on one task and defective ones on another: ACF024, ACF027, ACF032, ACF033, ACF034); `severity-override` (the broken bundle with `severity: {ACF008: error, ACF024: off, ACF031: warn}` in `ackit.yaml`: ACF008 raised to error, ACF024 gone, ACF031 lowered to warn; 9 findings).

The negative control is a test in the suite, `test_guard_fails_when_a_real_rule_changes`: it patches the real `Validator.run` to add a finding, reword a message, flip a severity and drop a finding, one at a time, and asserts the guard differs on every bundle that can show the change (all ten for an extra finding; the four bundles with findings for the others).

## Coverage

Covered: any new finding, missing finding, changed wording, path or severity on the ten bundles, including ACF 1.2 fields and a `severity:` mapping. Not covered, with reasons: orchestly's bundle and the kit's own `docs/` are not in the baseline file (the first is uncommitted and changing, the second grows with every task); their raw validate output is quoted above and `docs` stays checked by `ackit validate docs --strict`. The optional case `test_extra_bundle_matches_its_baseline` runs only when `ACKIT_GUARD_EXTRA` is set and `tests/baselines/extra.json` exists, so it is skipped by default (2 skips in the run above: this one and an older one).

Independent review (a separate read-only agent, 2026-11-20): verdict accept with fixes; three major findings (baseline lacked the raw kit and orchestly outputs; no ACF 1.2 field or severity-mapping bundle; negative control only a one-off script) are fixed in this revision. Minor: the "src unchanged" statement rests on `git diff --stat -- src` printing nothing at recording time.
