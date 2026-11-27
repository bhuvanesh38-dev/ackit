# Adopters

The kit core (spec, templates, roles, stack packs, validator) is agnostic to company, host and tool. Everything specific to one organisation lives in a folder here, named for the adopter.

An **adopter overlay** is a bundle of things one organisation layers on top of the generic kit:

| File | Purpose |
|---|---|
| `README.md` | what the adopter is, marked as an example if it is a beta user |
| `answers.yaml` | answers for `ackit init --answers` (owner, commands, size) |
| `mapping.yaml` | `ackit import` mapping from the adopter's existing layout |
| `rules/*.md` | adopter-specific rules (copy into the bundle's `rules/` as drafts) |
| `roles/<role>/...` | role overlay files (copy into the bundle's `roles/`) |

An adopter overlay is not a **role profile** (`role.yaml`, who does what) and not a **stack pack** (how a technology builds and tests); it is the organisation-level layer that may contain overlays for both.

- `example/` - a neutral starting point for a new adopter. Copy it.
- every other folder is one adopter (a beta user), kept as a worked example of a real store mapped onto ACF and marked as such in its own README.
