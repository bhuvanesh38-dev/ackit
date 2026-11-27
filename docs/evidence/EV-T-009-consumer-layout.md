---
type: test-evidence
title: 'Evidence for T-009: consumer_layout and ackit link --check'
item: T-009
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-20T19:00:00Z'
---

## Commands

```bash
.venv/bin/python -m pytest -q tests/test_acf13_layout.py tests/test_validate.py
```

## Results

```
tests/test_acf13_layout.py: 18 passed after the review; with tests/test_validate.py the run passes
```

K1: on a temporary tree one link is correct, one path is a plain file and one is a link elsewhere: the command reports `ok`, `wrong` and `wrong` and exits 1, and the tree is listed before and after with no difference. On an empty target every link is `missing`, exit 1, and the target stays empty. With all links in place the exit is 0. A rules folder absent from the bundle is reported `missing`. Nine invalid layouts exit 2 (ACF042). An absent block checks nothing.

After the review also: no links configured means the entry source is not checked (a bundle without `AGENTS.md` and no block exits 0), a dangling link is `wrong` (points to ...), relative links and a chain of links ending at the bundle file are `ok`, a missing source makes each of its links `missing`, a symlink loop does not crash, a target that is the bundle and a missing bundle exit 2, duplicate and nested link paths are refused.

## Coverage

Not covered: a bundle reached through a symlinked directory, Windows, and a rules source that is a file.
