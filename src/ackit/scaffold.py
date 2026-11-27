"""Create documents from templates, allocate ids, build index.md, mark documents verified."""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any

import jinja2
import yaml

from .workspace import config as workspace_config, hidden_from_index
from . import ACF_VERSION, __version__
from .idalloc import allocate
from .bundle import Bundle, Doc, as_list, data_dir, load_registry, split_frontmatter

ID_FORMAT = {"epic": ("E-", 3), "feature": ("F-", 3), "task": ("T-", 3), "issue": ("I-", 3),
             "incident": ("INC-", 3), "decision": ("ADR-", 4)}
STALE_DAYS = {"runbook": 180, "reference": 90, "rule": 365, "module": 180, "architecture": 180}
INDEX_GROUPS = [
    ("Entry and core", ["entry", "product", "tech-stack", "workflow", "architecture", "responsibility"]),
    ("Modules", ["module"]), ("Rules", ["rule"]),
    ("Work", ["epic", "feature", "feature-stage", "task", "issue"]),
    ("Decisions", ["decision"]), ("Incidents", ["incident"]), ("Journals", ["journal"]),
    ("Sessions", ["session", "session-index"]), ("Records", ["review", "test-evidence", "handoff"]),
    ("Design and operations", ["design-spec", "runbook"]),
    ("Reference", ["reference"]),
]


def slugify(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-") or "item"


def default_slug(title: str, max_words: int = 6, max_chars: int = 40) -> str:
    """A short file-name slug: the first `max_words` words, cut at a word boundary to at most `max_chars`."""
    words = slugify(title).split("-")[:max_words]
    while len(words) > 1 and len("-".join(words)) > max_chars:
        words.pop()
    return "-".join(words)[:max_chars].strip("-") or "item"


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(d: dt.datetime) -> str:
    return d.isoformat().replace("+00:00", "Z")


def jinja_env(search: list[Path]) -> jinja2.Environment:
    dirs = [str(p) for p in search if p and Path(p).is_dir()]
    dirs += [str(data_dir() / "templates"), str(data_dir() / "roles")]
    return jinja2.Environment(loader=jinja2.FileSystemLoader(dirs), keep_trailing_newline=True,
                              trim_blocks=False, undefined=jinja2.Undefined)


def next_id(bundle: Bundle, t: str, author: str | None = None) -> str:
    prefix, width = ID_FORMAT[t]
    return allocate([d.id for d in bundle.of_type(t) if d.id], prefix, width, bundle.config, author)


def dump_doc(meta: dict, body: str) -> str:
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100)
    return f"---\n{fm}---\n\n{body.strip()}\n"


def default_meta(reg: dict, t: str, title: str, ident: str | None, extras: dict, now: dt.datetime) -> dict:
    spec = reg["types"].get(t, {})
    sset = reg["status_sets"].get(spec.get("status_set", "doc"), reg["status_sets"]["doc"])
    m: dict[str, Any] = {"type": t}
    if ident:
        m["id"] = ident
    m["title"] = title
    m["description"] = extras.pop("description", "")
    m["status"] = extras.pop("status", sset["initial"])
    for k in spec.get("required", []):
        if k in m or k in extras:
            continue
        enum = (spec.get("enums") or {}).get(k)
        # a word choice starts at its first value; a numeric choice (a classification) is never guessed: it stays empty until the author picks
        m[k] = enum[0] if enum and isinstance(enum[0], str) else (now.date().isoformat() if k == "date" else "")
    m.update(extras)
    if spec.get("status_set") == "work" and "history" not in m:
        m["history"] = [m["status"]]
    m["generated"] = {"by": f"ackit/{__version__}", "at": iso(now)}
    days = STALE_DAYS.get(t)
    if days:
        m["review_by"] = iso(now + dt.timedelta(days=days))
    if "description" in m and not m["description"]:
        del m["description"]
    return m


def guide_comment(reg: dict, t: str) -> str:
    spec = reg["types"].get(t)
    if not spec:
        return ""
    o = spec.get("owner", {})
    rules = "\n".join(f"  - {r}" for r in spec.get("rules", []))
    return (f"<!-- ACF {t}: {spec['purpose']}\n  writes: {o.get('writes')} | reviews: {o.get('reviews')} | "
            f"signs off: {o.get('signs_off')}\n  update when: {o.get('updates')}\n  rules:\n{rules}\n-->\n\n")


def render_body(reg: dict, t: str, ctx: dict, search: list[Path]) -> str:
    env = jinja_env(search)
    name = f"{t}.md.j2"
    try:
        tpl = env.get_template(name)
    except jinja2.TemplateNotFound:
        tpl = env.get_template("generic.md.j2")
    return tpl.render(**ctx)


def target_path(bundle_root: Path, reg: dict, t: str, ident: str | None, title: str, tier: str | None,
                slug: str | None = None) -> Path:
    spec = reg["types"].get(t, {})
    base = bundle_root / (spec.get("dir") or "")
    slug = slugify(slug) if slug else default_slug(title)
    if t in ("rule", "module"):
        return base / f"{slug}.md"
    if t == "feature" and tier == "large":
        return base / f"{ident}-{slug}" / "feature.md"
    if ident:
        return base / f"{ident}-{slug}.md"
    return base / f"{slug}.md"


def new_doc(bundle_root: Path, t: str, title: str, *, ident: str | None = None, extras: dict | None = None,
            ctx: dict | None = None, search: list[Path] | None = None, guide: bool = False,
            now: dt.datetime | None = None, overwrite: bool = False, slug: str | None = None, author: str | None = None) -> Path:
    bundle = Bundle.load(bundle_root) if bundle_root.is_dir() else None
    reg = bundle.registry if bundle else load_registry()
    now = now or now_utc()
    extras = dict(extras or {})
    if ident is None and t in ID_FORMAT and bundle:
        ident = next_id(bundle, t, author)
    path = extras.pop("_path", None) or target_path(bundle_root, reg, t, ident, title, extras.get("tier"), slug)
    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(str(path))
    meta = default_meta(reg, t, title, ident, extras, now)
    c = {"title": title, "id": ident, "date": now.date().isoformat(), "day": now.strftime("%a"),
         "week": now.strftime("%V"), "branch": "main", "sha": "0000000", **meta, **(ctx or {})}
    c["title"] = title
    body = render_body(reg, t, c, search or [])
    if guide:
        body = guide_comment(reg, t) + body
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_doc(meta, body))
    return path


def new_large_feature(bundle_root: Path, title: str, extras: dict, search=None, now=None, slug: str | None = None,
                      author: str | None = None) -> list[Path]:
    """Folder with feature.md, stage docs 01..05 and the journal."""
    extras = dict(extras, tier="large")
    fpath = new_doc(bundle_root, "feature", title, extras=extras, search=search, now=now, slug=slug, author=author)
    b = Bundle.load(bundle_root)
    fid = [d for d in b.of_type("feature") if d.path == fpath.resolve()][0].id
    out = [fpath]
    stages = b.registry["stages"]
    for i, st in enumerate(stages, 1):
        p = fpath.parent / f"{i:02d}-{st}.md"
        if st == "journal":
            new_doc(bundle_root, "journal", f"Journal: {title}", extras={"about": fid, "_path": p}, ctx={"about": fid}, search=search, now=now)
        else:
            new_doc(bundle_root, "feature-stage", f"{st.title()}: {title}",
                    extras={"feature": fid, "stage": st, "_path": p}, ctx={"sections": b.registry["stage_sections"][st]}, search=search, now=now)
        out.append(p)
    return out


def build_index(bundle: Bundle) -> str:
    lines = ["---", f'acf_version: "{ACF_VERSION}"', "---", "", f"# {bundle.project_title} - context index", "",
             "Progressive disclosure: read `AGENTS.md` first, then only what the task needs. Regenerate with `ackit index --write`.", ""]
    used = set()
    grouped = []
    ws, _ = workspace_config(bundle.config)
    shared = [d for d in bundle.docs if not hidden_from_index(d.rel, ws)]
    for head, types in INDEX_GROUPS:
        docs = [d for d in shared if d.type in types]
        grouped.append((head, docs))
        used.update(id(d) for d in docs)
    grouped.append(("Other", [d for d in shared if id(d) not in used and d.type]))
    for head, docs in grouped:
        if not docs:
            continue
        lines.append(f"## {head}")
        lines.append("")
        for d in sorted(docs, key=lambda x: x.rel):
            desc = str(d.meta.get("description") or "").strip()
            lead = f"{d.id}: " if d.id else ""
            lines.append(f"- [{lead}{d.title}](/{d.rel})" + (f" - {desc}" if desc else ""))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_index(bundle: Bundle) -> Path:
    p = bundle.root / "index.md"
    p.write_text(build_index(bundle))
    return p


def log_entry(root: Path, text: str, now: dt.datetime | None = None):
    now = now or now_utc()
    p = root / "log.md"
    day = now.date().isoformat()
    entry = f"- {text}\n"
    if not p.exists():
        p.write_text(f"# Log\n\nChanges to this bundle, newest first.\n\n## {day}\n\n{entry}")
        return
    s = p.read_text()
    if re.search(rf"^## {day}\s*$", s, re.M):
        s = re.sub(rf"(^## {day}\s*\n\n?)", lambda m: m.group(1) + entry, s, count=1, flags=re.M)
    else:
        m = re.search(r"^## \d{4}-\d{2}-\d{2}", s, re.M)
        block = f"## {day}\n\n{entry}\n"
        s = s[:m.start()] + block + s[m.start():] if m else s.rstrip() + "\n\n" + block
    p.write_text(s)


def verify_doc(path: Path, by: str, status: str | None = None, now: dt.datetime | None = None, signoff: bool = False):
    meta, body, err = split_frontmatter(path.read_text())
    if err or meta is None:
        raise ValueError(err)
    now = now or now_utc()
    ver = [v for v in as_list(meta.get("verified")) if isinstance(v, dict)]
    ver.append({"by": by, "at": iso(now)})
    meta["verified"] = ver
    wants_signoff = signoff or status == "signed-off"          # both ways write `signoff`, and that is a person's act
    if wants_signoff and not re.fullmatch(r"human:\S+", by):
        raise ValueError("a sign-off must come from a person: use `--by human:<id>`")
    if signoff and "signoff" not in meta:                       # the sign-off a task above the auto-start limit needs (ACF027); never overwritten
        meta["signoff"] = {"by": by, "at": iso(now)}
    if status:
        hist = as_list(meta.get("history")) or ([meta["status"]] if meta.get("status") else [])
        if not hist or hist[-1] != status:          # re-attesting a document already at `status` records the signature only
            hist.append(status)
        meta["history"] = hist
        meta["status"] = status
        if status == "signed-off" and "signoff" not in meta:   # a signed-off stage or feature needs `signoff` (ACF027); it is the same person and moment
            meta["signoff"] = {"by": by, "at": iso(now)}
    path.write_text(dump_doc(meta, body))


def set_status(bundle: Bundle, item: str, new: str) -> dict:
    """Move a document to `new` if SPEC section 6 allows it, appending to `history` (created from the current status)."""
    p = Path(item)
    doc = next((d for d in bundle.docs if d.path == p.resolve()), None) if p.is_file() else bundle.resolve(item)
    if doc is None:
        raise LookupError(f"'{item}' is neither a file nor an id/concept in {bundle.root}")
    if doc.err or not doc.type or not bundle.type_spec(doc.type):
        raise ValueError(f"{doc.rel} has no known type, so its lifecycle is unknown")
    spec = bundle.type_spec(doc.type)
    sset = bundle.status_set(spec)
    cur = doc.status or sset["initial"]
    if new not in sset["values"]:
        raise ValueError(f"'{new}' is not a status of type {doc.type}; legal values: {sset['values']}")
    legal = sset["transitions"].get(cur, [])
    if new not in legal:
        raise ValueError(f"illegal transition {cur} -> {new} for {doc.id or doc.rel}; legal from '{cur}': {legal or 'none (final status)'}")
    hist = [str(h.get('status')) if isinstance(h, dict) else str(h) for h in as_list(doc.meta.get("history"))] or [cur]
    if hist[-1] != cur:
        raise ValueError(f"history of {doc.rel} ends at '{hist[-1]}' but status is '{cur}'; fix it by hand first")
    hist.append(new)
    meta, body, err = split_frontmatter(doc.path.read_text(encoding="utf-8"))
    if err or meta is None:
        raise ValueError(err)
    meta["status"] = new
    meta["history"] = hist
    doc.path.write_text(dump_doc(meta, body), encoding="utf-8")
    note = None
    if new in sset.get("human_verified", []) and spec.get("human_verified", True) is not False:
        note = f"'{new}' needs a human verification: run `ackit verify {doc.rel} --by human:<id>`"
    return {"id": doc.id or doc.rel, "old": cur, "new": new, "history": hist, "note": note}
