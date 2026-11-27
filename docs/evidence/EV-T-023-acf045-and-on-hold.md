---
type: test-evidence
title: 'Evidence for T-023: ACF045 and the on-hold status block'
item: T-023
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T21:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf045_session_heading.py tests/test_validate.py tests/test_guard_baseline.py tests/test_examples.py
.venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
full suite: 375 passed, 7 skipped
ackit validate docs --strict: 143 documents, 0 errors, 0 warnings
guard test (a bundle using none of the ACF 1.3 keys validates as before): passes with its baseline unchanged
```

ACF045 tests: 6 valid headings fire nothing (a plain one, a long sha, `@ none`, upper-case hex, en and em dashes, trailing spaces); 15 malformed headings each fire exactly one ACF045 warning and no ACF021 (no day and week, no week, no sha, a sha of 2 or 41 characters, a sha that is not hex, no title, no branch, a bad day name, week 54, a one-digit week, a sha word other than `none`, a branch with a space, `NONE`, week 00). A session under an author workspace folder gets the same rule, and `severity: {ACF045: off}` turns it off. With `severity: {ACF045: error}` the finding is an error; a heading with no date still gives only ACF021 (ACF045 does not repeat it); the old test heading with a date and the labels gives no ACF021 finding. The rule table test requires a firing case for every rule and has one for ACF045.

On-hold block: the block in SPEC and ADOPTION is the one in the test; with it `in-progress -> on-hold -> in-progress` validates and `on-hold -> done` gives ACF007; without it `on-hold` gives ACF006.

One document of the kit's own failed the new rule: its first session entry carried `@ initial` as the sha (a build made before any commit); it is now `@ none`.

## Coverage

ACF045 checks the shape only: it does not check that the day name matches the date, that the week number matches the date, or that the sha exists in a repository. Those would need a calendar convention or a git repository and are not part of this task.
