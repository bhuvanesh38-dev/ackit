"""Author workspaces (ACF 1.3, ADR-0019).

`ackit.yaml` may carry

    author_workspace:
      root: "developers/{author}"     # one folder per author, `{author}` is one whole path part
      in_index: false                 # workspace documents stay out of the shared index (default)

A document under the root must carry `author` equal to its folder name (ACF036, warning). With `in_index: false` the generated
`index.md` leaves workspace documents out and ACF024 does not ask for them to be listed. Every other rule, the journal and
session format rules (ACF020, ACF021) included, still applies to them.
"""
from __future__ import annotations

DEFAULT = {"root": None, "in_index": False}


def config(raw_config: dict) -> tuple[dict, list[str]]:
    """(effective settings, problems)."""
    out = dict(DEFAULT)
    raw = (raw_config if isinstance(raw_config, dict) else {}).get("author_workspace")
    if raw is None:
        return out, []
    if not isinstance(raw, dict):
        return out, [f"`author_workspace` must be a mapping, got {type(raw).__name__}"]
    problems = [f"`author_workspace.{k}` is not a known key (known: root, in_index)" for k in raw if k not in DEFAULT]
    root = raw.get("root")
    if root is not None:
        parts = root.split("/") if isinstance(root, str) else []
        if (not parts or parts.count("{author}") != 1 or parts[0] == "{author}" or root.startswith("/") or "\\" in root
                or ".." in parts or "." in parts or "" in parts or any("{" in p and p != "{author}" for p in parts)):
            problems.append("`author_workspace.root` must be a relative path with `{author}` once as a whole part after at least one folder, "
                            "using `/` and no `.` or `..` parts, e.g. `developers/{author}`")
        else:
            out["root"] = root
    elif "root" in raw:
        problems.append("`author_workspace.root` must not be empty")
    if "in_index" in raw:
        if isinstance(raw["in_index"], bool):
            out["in_index"] = raw["in_index"]
        else:
            problems.append("`author_workspace.in_index` must be true or false")
    return out, problems


def folder_author(rel: str, cfg: dict) -> str | None:
    """The author folder a document path (relative to the bundle) sits in, or None when it is outside every workspace."""
    if not cfg["root"]:
        return None
    pat, parts = cfg["root"].split("/"), rel.split("/")
    i = pat.index("{author}")
    if len(parts) <= len(pat) or parts[:i] != pat[:i] or parts[i + 1:len(pat)] != pat[i + 1:]:
        return None
    return parts[i]


def hidden_from_index(rel: str, cfg: dict) -> bool:
    return not cfg["in_index"] and folder_author(rel, cfg) is not None
