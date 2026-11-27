---
type: test-evidence
title: 'Evidence for T-016: push-mode cases and the wrapper limits'
item: T-016
result: pass
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T16:00:00Z'
---

## Commands

```bash
.venv/bin/python <the adopter overlay's equivalence/harness.py> --source-store <store root> --cases <the push-mode cases>
.venv/bin/python <the adopter overlay's equivalence/harness.py> --source-store <store root> --cases <commit-mode, push-mode, limits and smoke cases>
ACKIT_BETA_STORE=<store root> .venv/bin/python -m pytest -q
.venv/bin/ackit validate docs --strict
```

## Results

```
push-mode cases on the real store source: 18 cases, all pass in both routes
all four case files together: 44 commit-time cases (39 commit-mode, 1 limits, 4 smoke; 42 of them are measured, the 2 that run a real git commit are not) and 18 push-time cases, all pass; the run lists no check as skipped in every case
full suite with the store path set: 353 passed, 1 skipped
```

Nothing is pushed: the gate only reads the refs it is given on standard input. The tracker is a stand-in on a loopback port that the harness starts and answers per case (an open, a merged, a missing pull request, a server error); the token file exists only in the cases that name one, and the run refuses to start if the tracker address is anything but a plain loopback address. The harness's own pushes (a store branch to the scratch origin, and the clean-up of extra branches between cases) go only to the scratch origin, which the safety guard checks first, and skip the hooks.

| Check | Fires | Clean |
|---|---|---|
| 15 (code clone) | block: store branch not on origin; block: unpushed store commit; block: no token; block: no pull request; block: lookup fails; block: an open pull request whose context branch has no real session entry; block: a push that would replace remote commits (the guard's override path) | pass: open pull request with a real entry; pass: merged pull request; pass: small fix; pass: a fast-forward in the code clone |
| 17 (store) | block: would replace remote commits; block: deletes an unmerged remote branch | pass: fast-forward; pass: deletes a merged branch; skipped in the code clone |
| 4 (code clone) | block: the stub build command fails | pass: the stub build command succeeds |

The cases that reach the tracker also assert that each route made exactly one request, for the context branch's pull requests. Check 4 ran against a stub `gradlew` only. The real build was not run; that is recorded here and is not proven.

## The wrapper's limits

Measured on the full scratch copy of the store (every shared and project file, from `git archive HEAD`). The kit's default timeout is 120 seconds (the adopter's push entries set 600); its output cap is the last 64 KiB of the gate's raw output. The cap applies to the raw output, so the figure that matters is the direct route's; the kit route's figure is the size of its JSON report, in which control characters are escaped, so it is larger (the run prints both and says which is which).

| Run (the harness's `limits` report) | Slowest, direct / kit | Largest raw gate output (direct) | Kit JSON report |
|---|---|---|---|
| all 42 commit-time runs, including 150 staged documents with two broken links each | 4.5 s / 4.8 s | 52.5 KB, under the cap (the 150-document case) | 60.7 KB |
| all 18 push-time runs | 0.3 s / 0.6 s | 3.6 KB | 4.9 KB |

Measured once by hand with the same case written for other sizes (not kept as cases, because above the cap the routes differ by design): 180 documents, 5.4 s, 62.6 KB raw (just under the cap); 260 documents, 8.1 s, 89.4 KB raw (over the cap: the kit keeps only the last 64 KiB, so the two routes differ); 400 documents, 12.3 s, 136.5 KB raw (over the cap).

Reading: a bad document costs about 340 bytes and about 30 ms, so the output cap is reached at about 190 such documents and the timeout is far away (400 documents took 12 seconds against 120). When the cap bites, the beginning of the output is lost and the end is kept; the harness refuses a run with no `[n/17]` section, so a loss of that kind is reported, not silent. The shipped case uses 150 documents, about 20% under the cap, so the case does not depend on the length of the scratch path. The real build is not measured: the gate's own comment gives about 50 seconds, within the push entries' 600 seconds.

## Sibling scripts through the temporary link

The kit route runs the gate through a link in a temporary folder. The gate finds its sibling scripts with the real path of the link, and this was exercised, not assumed: check 13's script (`c13-fire-raw-parser`, commit time), check 12's script (`c12-fire-dangling-ref`) and the push guard script of check 15 (the `p15` cases) all ran and gave the expected result in the kit route.

## Coverage

No check is skipped in every case. Checks 8, 9, 10 and 11 are shown only through the gate's hint lines (its warnings for them are never printed; see the F-003 journal). Not proven: the real build (check 4, stubbed), the real tracker (the stand-in answers; the API's real shape was taken from the guard's own query and parsing, not from a live call), and the emergency-skip path of check 15, which is not exercised on purpose.
