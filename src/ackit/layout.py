"""Consumer layout (ACF 1.3, ADR-0019).

Tools that read a context store look for files at fixed paths of their own: an agent reads `AGENTS.md` and `.claude/CLAUDE.md` at
the root of a code clone, another reads a rules folder. The standard does not own those paths; the adopter lists them.

    consumer_layout:
      entry: AGENTS.md                    # the entry file inside the bundle (default AGENTS.md)
      entry_links: [AGENTS.md, .claude/CLAUDE.md]   # where a consumer expects a link to it, relative to the target directory
      rules_dir: rules                    # the rules folder inside the bundle
      rules_links: [.claude/rulebook]     # where a consumer expects a link to it

`ackit link --check [--target DIR]` reports each configured link as ok, missing or wrong and creates nothing. Creating the links
stays with `ackit init --link-entry` and the adopter's installer.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

KEYS = ("entry", "entry_links", "rules_dir", "rules_links")


def _rel_ok(p) -> bool:
    if not isinstance(p, str) or not p or p.startswith("/") or "\\" in p:
        return False
    return not any(part in ("", ".", "..") for part in p.split("/"))


def config(raw_config: dict) -> tuple[dict, list[str]]:
    out = {"entry": "AGENTS.md", "entry_links": [], "rules_dir": None, "rules_links": []}
    raw = (raw_config if isinstance(raw_config, dict) else {}).get("consumer_layout")
    if raw is None:
        return out, []
    if not isinstance(raw, dict):
        return out, [f"`consumer_layout` must be a mapping, got {type(raw).__name__}"]
    problems = [f"`consumer_layout.{k}` is not a known key (known: {', '.join(KEYS)})" for k in raw if k not in KEYS]
    for k in ("entry", "rules_dir"):
        if k in raw:
            if _rel_ok(raw[k]):
                out[k] = raw[k]
            else:
                problems.append(f"`consumer_layout.{k}` must be a relative path with `/` and no `.` or `..` parts")
    for k in ("entry_links", "rules_links"):
        if k in raw:
            v = raw[k]
            if isinstance(v, list) and all(_rel_ok(x) for x in v):
                out[k] = list(v)
            else:
                problems.append(f"`consumer_layout.{k}` must be a list of relative paths with `/` and no `.` or `..` parts")
    links = out["entry_links"] + out["rules_links"]
    if len(set(links)) != len(links):
        problems.append("`consumer_layout` lists the same link path more than once")
    elif any(a != b and b.startswith(a + "/") for a in links for b in links):
        problems.append("`consumer_layout` has a link path inside another link path")
    if out["rules_links"] and not out["rules_dir"]:
        problems.append("`consumer_layout.rules_links` needs `rules_dir`")
    return out, problems


@dataclass(frozen=True)
class Link:
    kind: str            # entry | rules
    path: str            # the expected link, relative to the target directory
    state: str           # ok | missing | wrong
    detail: str


def check(cfg: dict, bundle: Path, target: Path) -> list[Link]:
    """Check every configured link without touching the file system. A link is ok when it is a symlink that resolves to the file."""
    out: list[Link] = []
    for kind, source_key, links_key in (("entry", "entry", "entry_links"), ("rules", "rules_dir", "rules_links")):
        source_rel = cfg[source_key]
        if not source_rel or not cfg[links_key]:          # nothing configured to link: nothing to check
            continue
        source = bundle / source_rel
        if not source.exists():
            out += [Link(kind, rel, "missing", f"the source {source_rel} does not exist in the bundle") for rel in cfg[links_key]]
            continue
        for rel in cfg[links_key]:
            link = target / rel
            try:
                if os.path.islink(link):
                    if link.resolve() == source.resolve():
                        out.append(Link(kind, rel, "ok", f"-> {source_rel}"))
                    else:
                        out.append(Link(kind, rel, "wrong", f"points to {os.readlink(link)}, expected {source_rel} of the bundle"))
                elif link.exists():
                    out.append(Link(kind, rel, "wrong", "exists but is not a symlink"))
                else:
                    out.append(Link(kind, rel, "missing", "not present"))
            except (OSError, RuntimeError) as exc:
                out.append(Link(kind, rel, "wrong", f"cannot be read: {exc}"))
    return out
