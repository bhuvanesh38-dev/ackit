---
type: reference
title: Interoperability with OKF v0.2
description: How the OKF adapter maps fields and what cannot round-trip
status: draft
generated:
  by: ackit-dev/agent
  at: '2026-11-17T15:44:50Z'
---

# Interoperability with OKF v0.2

ACF is its own format. The adapter exists so a bundle can move to and from tools that speak OKF v0.2.

```bash
ackit export --bundle context --okf out-okf        # ACF -> OKF
ackit import --okf some-okf-bundle --dest context   # OKF -> ACF
```

## Field map

| ACF | OKF v0.2 |
|---|---|
| `review_by` | `stale_after` |
| `sources[].ref` | `sources[].resource` |
| root index `acf_version: "1.4"` | root index `okf_version: "0.2"` (and `acf_version`, kept as an unknown key) |
| `status` (any ACF status) | `status` in draft, stable, deprecated; the ACF value is kept in `acf_status` |
| `roles/<role>/...` overlay | `.acf/roles/<role>/...` (hidden, not a concept) |
| `type`, `title`, `description`, `tags`, `generated`, `verified`, every other key (including `points`, `runs`, `external_id`; checked by a test) | unchanged |

Status mapping on export: stable, accepted, done, final, signed-off, resolved and closed become `stable`; deprecated, superseded, rejected and cancelled become `deprecated`; everything else becomes `draft`.

## Round trip

ACF -> OKF -> ACF reproduces every concept exactly (frontmatter and body), the `ackit.yaml` configuration and the role overlay. The test suite checks this for the example bundles.

## What cannot round-trip

- OKF -> ACF: a concept without a `type` is skipped and reported. An OKF `status` without `acf_status` is mapped to the nearest ACF status of the type (draft to the initial status, stable to the settled one, deprecated to the retired one), so it is approximate.
- OKF -> ACF: ACF required keys and sections are not part of OKF. Known types missing required keys get empty placeholders that the validator then reports; unknown types are kept as generic concepts (warning ACF003).
- OKF -> ACF: a bundle without `AGENTS.md` gets a generated stub entry, and the index is regenerated.
- ACF -> OKF: ACF-only rules (stage order, completeness, role definitions, size budget) have no OKF counterpart and are not exported as rules; they are re-checked by `ackit validate` after import.
- Anything OKF defines that ACF has no field for (for example a concept-level `resource` URI) is preserved as an ordinary unknown key, not interpreted.
