---
type: review
title: 'Review of T-016: push-mode cases and the wrapper limits'
item: T-016
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T17:00:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-23, of the push-mode and limits cases, the harness additions (tracker stand-in, push and cleanup steps, placeholders, measurements) and the evidence. The reviewer was asked first about safety (every push, delete and fetch, the tracker, credentials, injection through case input), then whether each case is tied to its check, whether the numbers match what the harness measures, the four acceptance criteria, and vacuous passes.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | major (measurement) | The kit figure was the size of its JSON report, in which escapes inflate the text, while the cap applies to the raw output; the evidence did not say which route a figure came from | The report and the evidence now say the cap applies to the raw (direct) figure and show both routes in separate columns |
| 2 | minor | A case that named no tracker answer inherited the previous case's answer | Such a case gets an empty answer; tested |
| 3 | minor | No case checked what the tracker was asked | `tracker.expect_request`: each route makes exactly one request, matching the context branch; set on the five cases that reach the tracker; a typo in the tracker spec is refused |
| 4 | minor | The `git` setup step was a deny list; `ls-remote`, `send-pack`, `fetch-pack` and similar passed | An allow list of subcommands, and any argument that looks like a remote URL is refused; tested |
| 5 | minor | `reset` ran destructive git commands before its first safety check, and its remote-branch filter was loose | The safety check comes first; the ref is compared exactly |
| 6 | nit | The `branch` step took any name | A plain-name pattern; tested |
| 7 | nit | No fast-forward case beside the override case in the code clone | Added |
| 8 | minor | The case count in the evidence was wrong; the cap margin of 180 documents was thin; the 260 and 400 rows and the real-build time had no source; "no check left unproven" overstated | Count corrected; the case uses 150 documents (about 20% under the cap); the other sizes are labelled as measured once by hand, the build time as the gate's own comment; the wording is now "no check is skipped in every case", with the checks shown only through hint lines and the not-proven list named |
| 9 | nit | The check 4 push cases always make check 15 block | Noted in the case file; they assert check 4's own section |

## Resolution

All findings fixed and verified: 29 harness tests pass, all four case files pass on the real store source, and the full suite passes. The reviewer found the harness cannot push, delete or fetch anywhere but the scratch origin, the tracker is bound to loopback, and no real credential is reachable.

## Verdict

approve. All four acceptance criteria are met: checks 15 and 17 fire and stay clean in both routes with a local tracker stand-in and the refs on standard input; check 4 ran with a stub build and the real build is recorded as not run; the timeout and the output cap are measured with the numbers written down; the gate finds its sibling scripts through the temporary link.
