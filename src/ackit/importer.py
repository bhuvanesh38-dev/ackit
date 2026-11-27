"""Map an existing context layout into an ACF bundle using a mapping file. Source is never modified."""
from __future__ import annotations

import fnmatch
import re
from pathlib import Path

import yaml

from . import __version__
from .bundle import Bundle, load_registry, split_frontmatter, headings, section_body
from .scaffold import ID_FORMAT, dump_doc, iso, log_entry, now_utc, slugify, write_index
from .validate import validate

H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)


def _match(rel: str, pat: str) -> bool:
    if fnmatch.fnmatch(rel, pat):
        return True
    return "**/" in pat and fnmatch.fnmatch(rel, pat.replace("**/", ""))


def plan(src: Path, mapping: dict) -> list[tuple[Path, str, dict]]:
    out = []
    skips = mapping.get("skip", [])
    for f in sorted(src.rglob("*.md")):
        rel = f.relative_to(src).as_posix()
        if any(_match(rel, s) for s in skips):
            continue
        rule = next((r for r in mapping.get("rules", []) if _match(rel, r["match"])), mapping.get("default"))
        if rule:
            out.append((f, rel, rule))
    return out


LINK = re.compile(r"(\]\()([^)\s#]+)(#[^)\s]*)?(\))")


def rewrite_links(body: str, src_rel: str, dest_rel: str, moved: dict[str, str]) -> tuple[str, int]:
    """Point relative markdown links at the new place of a moved file. A link to a file that was not imported is left as it is."""
    import posixpath
    count = 0

    def fix(m):
        nonlocal count
        target = m.group(2)
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:|^/|^#", target):
            return m.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(src_rel), target))
        if resolved not in moved:
            return m.group(0)
        new = posixpath.relpath(moved[resolved], posixpath.dirname(dest_rel) or ".")
        count += 1
        return f"{m.group(1)}{new}{m.group(3) or ''}{m.group(4)}"

    return LINK.sub(fix, body), count


def import_store(src: Path, mapping: dict, dest: Path, dry_run: bool = False, now=None) -> dict:
    src, dest = Path(src).resolve(), Path(dest).resolve()
    reg = load_registry()
    now = now or now_utc()
    report = {"files": [], "stubs": 0, "skipped": 0, "placeholders": []}
    counters: dict[str, int] = {}
    used_dest: set[str] = set()
    pending: list = []
    for f, rel, rule in plan(src, mapping):
        t = rule["type"]
        spec = reg["types"].get(t)
        if spec is None:
            report["skipped"] += 1
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        old, body, _err = split_frontmatter(text)
        old = old or {}
        if _err:
            body = text
        stem = f.stem
        title = str(old.get("title") or (H1.search(body).group(1) if H1.search(body) else stem))
        meta: dict = {"type": t}
        if "id" in spec.get("required", []) or spec.get("id_pattern"):
            if rule.get("id"):
                meta["id"] = rule["id"].format(stem=slugify(stem))
            elif t in ID_FORMAT:
                pre, w = ID_FORMAT[t]
                counters[t] = counters.get(t, 0) + 1
                meta["id"] = f"{pre}{counters[t]:0{w}d}"
        dpath = rule.get("dest", "{stem}.md").format(stem=slugify(stem), rel=rel, id=meta.get("id", ""), parent=slugify(Path(rel).parent.name))
        if dpath in used_dest:
            dpath = dpath[:-3] + f"-{len(used_dest)}.md"
        used_dest.add(dpath)
        meta["title"] = title
        if old.get("description"):
            meta["description"] = str(old["description"])
        sset = reg["status_sets"][spec.get("status_set", "doc")]
        meta["status"] = rule.get("status", sset["initial"])
        for k in spec.get("required", []):
            if k in meta:
                continue
            if k in (rule.get("set") or {}):
                continue
            enum = (spec.get("enums") or {}).get(k)
            if k in old and (not enum or old[k] in enum):
                meta[k] = old[k]
            elif enum:
                meta[k] = enum[0]
        meta.update(rule.get("set") or {})
        for k in spec.get("required", []):
            if meta.get(k) in (None, "", [], {}):
                meta[k] = ""
                report["placeholders"].append(f"{dpath}: needs `{k}`")
        # preserve unknown source keys without clobbering ours
        for k, v in old.items():
            if k in ("title", "description"):
                continue
            if k in meta:
                if meta[k] != v:
                    meta[f"source_{k}"] = v
                continue
            meta[f"source_{k}" if k in ("type", "status", "id", "generated", "verified") else k] = v
        meta["generated"] = {"by": f"ackit-import/{__version__}", "at": iso(now)}
        meta["sources"] = [{"ref": rel, "title": "original file in the imported store"}]
        secs = spec.get("sections")
        if isinstance(secs, dict):
            secs = secs.get(str(meta.get(secs["by"])), [])
        for s in secs or []:
            if section_body(body, s) is None:
                body = body.rstrip() + f"\n\n## {s}\n\n<!-- import: stub, fill in -->\n"
                report["stubs"] += 1
        report["files"].append({"from": rel, "to": dpath, "type": t})
        pending.append((rel, dpath, meta, body))
    moved = {rel: dpath for rel, dpath, _m, _b in pending}
    report["links_rewritten"] = 0
    for rel, dpath, meta, body in pending:
        body, n = rewrite_links(body, rel, dpath, moved)
        report["links_rewritten"] += n
        if not dry_run:
            p = dest / dpath
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(dump_doc(meta, body))
    if not dry_run and report["files"]:
        cfg = dest / "ackit.yaml"
        if not cfg.exists():
            cfg.write_text(yaml.safe_dump({"project": mapping.get("project", dest.parent.name), "agents_md_max_lines": 150, "links": "warn", "severity": mapping.get("severity", {})}, sort_keys=False))
        log_entry(dest, f"Imported {len(report['files'])} files from `{src.name}` with ackit-import. All `draft`, none human-verified.", now)
        b = Bundle.load(dest)
        write_index(b)
        issues = validate(Bundle.load(dest), now=now)
        report["validation"] = {"errors": sum(i.severity == "error" for i in issues), "warnings": sum(i.severity == "warn" for i in issues)}
    return report
