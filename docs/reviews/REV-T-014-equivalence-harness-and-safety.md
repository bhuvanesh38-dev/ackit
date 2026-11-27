---
type: review
title: 'Review of T-014: the equivalence harness and its safety checks'
item: T-014
role: reviewer
verdict: approve
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T13:15:00Z'
---

## Scope

An independent read-only review by a separate agent, 2026-11-23, of the harness, its smoke cases and its tests. The reviewer was asked first to find any way the harness could read or write the live store, read real credentials, reach a network, push to a real remote or use the emergency-skip variable, by reading the gate and the push-side check for every environment variable and path they use; second to check verdict parsing against the real output format; third to look for vacuous passes. The reviewer ran the tests, with and without the store path.

## Findings

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | major (latent) | The tracker-address guard parsed `http://127.0.0.1:9@evil.example` as loopback | Parsed with a URL parser; credentials, a non-numeric port, a non-loopback host or a non-http scheme are refused; tested |
| 2 | minor | Proxy variables were not scrubbed, so a request to the local stand-in planned for T-016 could go to a real proxy | Proxy variables dropped, loopback exempted; tested |
| 3 | minor | The guard checked only the origin fetch URL and two hook links; the docstring promised more | Push URL, extra remotes, hooks path, unexpected hooks, hook links, variables the harness does not control, and a deep scan for links leaving the folder; a relative or URL-looking origin is judged properly (a URL had passed as a relative path); each guard tested |
| 4 | minor | Case steps could write or delete outside the repository and run any git command; safety was not re-checked after setup | Paths must stay inside the repository and out of `.git`; git steps with `-C`, `-c`, `--git-dir`, push, remote, config and similar are refused; the guard runs again after setup; tested |
| 5 | minor | The gate prints its collected warnings in one block after check 7, so a `warn` expectation cannot be tied to a check; the warnings of checks 8, 9 and 10 are never printed | Schema note and a required `match` for warn and no-warn; a new `info` verdict for hint lines; the gate defect is recorded in the F-003 journal for the store's owner |
| 6 | minor | A section with no result line had no verdict a case could name | `none` verdict added; tested |
| 7 | minor | Vacuous passes: empty expectations, a gate that crashed identically in both routes, an exit code that disagreed with the gate's verdict, zero cases | Each refused or reported; tested |
| 8 | minor | Under a git command (for example a hook) the kit route sees `--amend` and the direct route does not | The harness refuses to run under a git command |
| 9 | nit | A cache folder appeared in the work tree | Already ignored by the repository's ignore list; no change |
| 10 | nit | The kit ran with the scratch repository on its import path | Run with `-I` (isolated) |
| 11 | nit | A harness-side timeout ends in a traceback | Left: loud, not silent |

## Resolution

Findings 1 to 8 and 10 fixed and verified (15 harness tests, 24 adopter tests with the store path set, a real-store smoke run); 9 needed no change; 11 left on purpose. The reviewer's check of what the scripts read from the environment found nothing else reachable: the gate reads no home paths and makes no network call; the push-side check reads `HOME` and four prefixed variables, all overridden, and with no token it blocks before any request.

## Verdict

approve. The harness cannot be pointed at the live store or the network without a guard tripping, and a run that proves nothing is reported as a failure.
