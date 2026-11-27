"""Registered references: controlled vocabularies for document fields (ACF 1.4, F-004).

`ackit.yaml` may carry

    vocabularies:
      module: {of_type: module}                         # the ids of the documents of a type
      vendor: {values: [vendor-a, vendor-b]}            # a list in the file
      tenant:                                           # a local file the adopter already keeps
        source_file: ../environments/registry.yaml      # relative to the bundle folder, read only
        key_path: tenants                               # dotted path to a list of strings, a mapping (its keys), or a list of mappings
        id_key: id                                      # for a list of mappings: the key that holds the value (default `id`)

and a type binds a field to a vocabulary with `vocab: {field: vocabulary}` (the core types `ticket-resolution` and the adopter's own
`types:` overrides). A bound field whose value is not registered is ACF043; an unusable `vocabularies` block is ACF044. A field bound to
a vocabulary the bundle does not define is not checked (a typo in an adopter's own binding is not reported), `key_path` is a plain dotted path (a key that is a number, a boolean or holds a dot cannot be reached), and and a bundle with no `vocabularies` block is not checked at all. The core names
no registry: the values are the adopter's.
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path

import yaml

NAME_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
SOURCES = ("values", "source_file", "of_type")
KEYS = {"values", "source_file", "key_path", "id_key", "of_type"}


def _walk(data, path: str):
    cur = data
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _from_node(node, id_key: str, where: str, problems: list[str]) -> set[str]:
    out: set[str] = set()
    if isinstance(node, dict):
        items = list(node)
    elif isinstance(node, list):
        items = node
    else:
        problems.append(f"{where}: the node at `key_path` must be a list or a mapping, got {type(node).__name__}")
        return out
    for it in items:
        if isinstance(it, dict):
            it = it.get(id_key)
        if isinstance(it, str) and it.strip():
            out.add(it)
        else:
            problems.append(f"{where}: every value must be a non-empty string (found {it!r})")
    return out


def build(config: dict, bundle_root: Path | None, docs, known_types: set[str]) -> tuple[dict[str, frozenset[str]], list[str]]:
    """The registered values of each vocabulary, and the problems with the configuration. `docs` is an iterable of (type, meta)."""
    raw = (config or {}).get("vocabularies")
    if raw is None:
        return {}, []
    if not isinstance(raw, dict):
        return {}, [f"`vocabularies` must be a mapping of name to source, got {type(raw).__name__}"]
    out: dict[str, frozenset[str]] = {}
    problems: list[str] = []
    docs = list(docs)
    for name, spec in raw.items():
        where = f"`vocabularies.{name}`"
        if not isinstance(name, str) or not NAME_RE.match(name):
            problems.append(f"{where}: the name must be lower case letters, digits, `-` or `_`, starting with a letter")
            continue
        if not isinstance(spec, dict):
            problems.append(f"{where} must be a mapping with one of {', '.join(SOURCES)}")
            continue
        unknown = sorted(str(k) for k in set(spec) - KEYS)
        if unknown:
            problems.append(f"{where}: unknown key(s) {', '.join(unknown)} (known: {', '.join(sorted(KEYS))})")
        given = [k for k in SOURCES if k in spec]
        if len(given) != 1:
            problems.append(f"{where} needs exactly one of {', '.join(SOURCES)} (found {', '.join(given) or 'none'})")
            continue
        src = given[0]
        values: set[str] = set()
        if src == "values":
            vals = spec["values"]
            if not isinstance(vals, list):
                problems.append(f"{where}.values must be a list of strings")
                continue
            if any(not isinstance(v, str) for v in vals):
                problems.append(f"{where}.values must hold plain strings only (found {next(v for v in vals if not isinstance(v, str))!r})")
                continue
            values = _from_node(vals, "id", f"{where}.values", problems)
        elif src == "of_type":
            t = spec["of_type"]
            if not isinstance(t, str) or t not in known_types:
                problems.append(f"{where}.of_type {t!r} is not a known document type")
                continue
            values = {str(m["id"]) for dt, m in docs if dt == t and isinstance(m, dict) and isinstance(m.get("id"), str) and m["id"]}
            if not values:
                problems.append(f"{where} has no values: no document of type {t!r} with an `id` was found (a document that failed to parse is not counted)")
                continue
        else:
            f, kp = spec["source_file"], spec.get("key_path")
            if not isinstance(f, str) or not f or not isinstance(kp, str) or not kp:
                problems.append(f"{where}: `source_file` and `key_path` must both be non-empty strings")
                continue
            p = Path(f).expanduser()
            if not p.is_absolute():
                p = (bundle_root or Path.cwd()) / p
            if not p.is_file():
                problems.append(f"{where}.source_file not found: {p}")
                continue
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
                problems.append(f"{where}.source_file {p} cannot be read as YAML: {str(exc)[:80]}")
                continue
            node = _walk(data, kp)
            if node is None:
                problems.append(f"{where}: `key_path` {kp!r} is not in {p}")
                continue
            id_key = spec.get("id_key", "id")
            if not isinstance(id_key, str) or not id_key:
                problems.append(f"{where}.id_key must be a non-empty string")
                continue
            values = _from_node(node, id_key, where, problems)
        if not values:
            problems.append(f"{where} has no values")
            continue
        if any(p.startswith(where) for p in problems):                 # a vocabulary with a problem is not used: it would only add a finding for every bound value
            continue
        out[name] = frozenset(values)
    return out, problems


def bindings(spec: dict) -> dict[str, str]:
    raw = (spec or {}).get("vocab") or {}
    return {k: v for k, v in raw.items() if isinstance(k, str) and isinstance(v, str)} if isinstance(raw, dict) else {}


def check(meta: dict, spec: dict, vocabs: dict[str, frozenset[str]]) -> list[str]:
    """The ACF043 messages for one document: every bound, defined vocabulary whose field holds an unregistered value."""
    msgs = []
    for field, name in bindings(spec).items():
        known = vocabs.get(name)
        if known is None or field not in meta or meta[field] in (None, "", [], {}):
            continue
        val = meta[field]
        items = val if isinstance(val, list) else [val]
        for it in items:
            if not isinstance(it, str):
                msgs.append(f"`{field}` must be a string or a list of strings registered in the `{name}` vocabulary (found {it!r})")
            elif it not in known:
                near = difflib.get_close_matches(it, sorted(known), n=1)
                hint = f"; did you mean `{near[0]}`?" if near else ""
                msgs.append(f"`{field}: {it}` is not registered in the `{name}` vocabulary ({len(known)} registered){hint}")
    return msgs
