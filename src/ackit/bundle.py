"""Load an ACF bundle: markdown concepts with YAML frontmatter, plus config and the type registry."""
from __future__ import annotations

import copy
import datetime as dt
import re
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

RESERVED = {"index.md", "log.md"}
SKIP_DIRS = {"roles", ".git", "node_modules", "_templates", ".venv", "__pycache__", ".ackit"}
FM_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)(.*)\Z", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def data_dir() -> Path:
    return Path(str(resources.files("ackit") / "data"))


def load_registry(extra: dict | None = None) -> dict:
    reg = yaml.safe_load((data_dir() / "types.yaml").read_text())
    for name, spec in ((extra or {}).get("types") or {}).items():
        base = reg["types"].get(name, {})
        merged = copy.deepcopy(base)
        merged.update(spec or {})
        reg["types"][name] = merged
    for name, spec in ((extra or {}).get("status_sets") or {}).items():
        reg["status_sets"][name] = spec
    return reg


def split_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    m = FM_RE.match(text)
    if not m:
        return None, text, "no frontmatter block (file must start with ---)"
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return None, m.group(2), f"unparseable frontmatter: {str(e).splitlines()[0]}"
    if not isinstance(meta, dict):
        return None, m.group(2), "frontmatter is not a mapping"
    return meta, m.group(2), None


def parse_dt(v: Any) -> dt.datetime | None:
    if isinstance(v, dt.datetime):
        return v if v.tzinfo else v.replace(tzinfo=dt.timezone.utc)
    if isinstance(v, dt.date):
        return dt.datetime(v.year, v.month, v.day, tzinfo=dt.timezone.utc)
    if isinstance(v, str):
        try:
            d = dt.datetime.fromisoformat(v.strip().replace("Z", "+00:00"))
            return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
        except ValueError:
            return None
    return None


def headings(body: str) -> list[tuple[int, str, int]]:
    """(level, text, line index) for headings outside code fences."""
    out, fence = [], False
    for i, line in enumerate(body.splitlines()):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip().rstrip(":"), i))
    return out


def section_body(body: str, name: str) -> str | None:
    hs = headings(body)
    lines = body.splitlines()
    for idx, (lvl, text, ln) in enumerate(hs):
        if text.lower() == name.lower():
            end = len(lines)
            for lvl2, _t, ln2 in hs[idx + 1:]:
                if lvl2 <= lvl:
                    end = ln2
                    break
            return "\n".join(lines[ln + 1:end]).strip()
    return None


def as_list(v: Any) -> list:
    if v is None:
        return []
    return list(v) if isinstance(v, (list, tuple)) else [v]


@dataclass
class Doc:
    path: Path
    rel: str
    meta: dict
    body: str
    err: str | None = None

    @property
    def cid(self) -> str:
        return self.rel[:-3] if self.rel.endswith(".md") else self.rel

    @property
    def type(self) -> str | None:
        t = self.meta.get("type")
        return t if isinstance(t, str) and t.strip() else None

    @property
    def id(self) -> str | None:
        v = self.meta.get("id")
        return str(v) if v is not None else None

    @property
    def status(self) -> str | None:
        v = self.meta.get("status")
        return str(v) if v is not None else None

    @property
    def title(self) -> str:
        return str(self.meta.get("title") or self.cid)


@dataclass
class Bundle:
    root: Path
    config: dict
    registry: dict
    docs: list[Doc] = field(default_factory=list)
    reserved: list[Doc] = field(default_factory=list)

    @classmethod
    def load(cls, root: str | Path) -> "Bundle":
        root = Path(root).resolve()
        if not root.is_dir():
            raise FileNotFoundError(f"bundle directory not found: {root}")
        cfg_path = root / "ackit.yaml"
        config = yaml.safe_load(cfg_path.read_text()) if cfg_path.exists() else {}
        config = config or {}
        b = cls(root=root, config=config, registry=load_registry(config))
        for p in sorted(root.rglob("*.md")):
            rel = p.relative_to(root)
            if rel.parts[0] == "roles" and len(rel.parts) > 1:
                continue  # role overlay: not concepts, checked by ACF030
            if any(part in SKIP_DIRS - {"roles"} or (part.startswith(".") and part != ".") for part in rel.parts[:-1]):
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            meta, body, err = split_frontmatter(text)
            doc = Doc(p, rel.as_posix(), meta or {}, body, err)
            if p.name in RESERVED:
                if p.name == "index.md" and err:  # index has optional frontmatter
                    doc.err, doc.meta, doc.body = None, {}, text
                b.reserved.append(doc)
            else:
                b.docs.append(doc)
        return b

    # lookups
    def of_type(self, t: str) -> list[Doc]:
        return [d for d in self.docs if d.type == t]

    def by_id(self, ident: str) -> Doc | None:
        for d in self.docs:
            if d.id == ident:
                return d
        return None

    def resolve(self, ref: str) -> Doc | None:
        ref = str(ref).strip()
        d = self.by_id(ref)
        if d:
            return d
        r = ref.lstrip("/")
        r = r[:-3] if r.endswith(".md") else r
        for d in self.docs:
            if d.cid == r:
                return d
        return None

    def type_spec(self, t: str) -> dict | None:
        return self.registry["types"].get(t)

    def status_set(self, spec: dict) -> dict:
        return self.registry["status_sets"][spec.get("status_set", "doc")]

    @property
    def project_title(self) -> str:
        for d in self.docs:
            if d.type == "product":
                return d.title
        return self.config.get("project") or self.root.parent.name
