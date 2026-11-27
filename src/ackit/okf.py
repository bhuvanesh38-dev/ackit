"""OKF v0.2 adapter: export an ACF bundle to an OKF bundle, import an OKF bundle into ACF.

Field map: review_by <-> stale_after, sources[].ref <-> sources[].resource, status via `acf_status`.
Everything else passes through. See docs/INTEROP.md for what cannot round-trip.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from . import ACF_VERSION, OKF_VERSION, __version__
from .bundle import Bundle, as_list, load_registry, split_frontmatter
from .scaffold import dump_doc, iso, log_entry, new_doc, now_utc, write_index

# ACF status -> OKF status (draft | stable | deprecated)
TO_OKF = {"stable": "stable", "accepted": "stable", "done": "stable", "final": "stable", "signed-off": "stable",
          "resolved": "stable", "closed": "stable", "deprecated": "deprecated", "superseded": "deprecated",
          "rejected": "deprecated", "cancelled": "deprecated"}
# OKF status -> ACF status, by status set (used only when `acf_status` is absent)
FROM_OKF = {"doc": {"draft": "draft", "stable": "stable", "deprecated": "deprecated"},
            "work": {"draft": "draft", "stable": "done", "deprecated": "cancelled"},
            "decision": {"draft": "proposed", "stable": "accepted", "deprecated": "deprecated"},
            "incident": {"draft": "open", "stable": "closed", "deprecated": "closed"},
            "record": {"draft": "draft", "stable": "final", "deprecated": "final"},
            "stage": {"draft": "draft", "stable": "signed-off", "deprecated": "draft"}}


def _walk(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_file() and not any(part.startswith(".") and part != "." for part in p.relative_to(root).parts[:-1]) or \
                (p.is_file() and p.relative_to(root).parts[0] == ".acf"):
            yield p


def export_okf(bundle_root: Path, out: Path) -> dict:
    root, out = Path(bundle_root).resolve(), Path(out).resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f"{out} is not empty")
    b = Bundle.load(root)
    rep = {"concepts": 0, "other_files": 0, "status_mapped": 0, "roles_files": 0}
    out.mkdir(parents=True, exist_ok=True)
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part.startswith(".") for part in rel.parts) and rel.parts[0] != "roles":
            continue
        if rel.parts[0] == "roles" and len(rel.parts) > 1:
            dst = out / ".acf" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)
            rep["roles_files"] += 1
            continue
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix != ".md":
            shutil.copy2(p, dst)
            rep["other_files"] += 1
            continue
        if rel.as_posix() == "index.md":
            meta, body, err = split_frontmatter(p.read_text())
            meta = meta or {}
            meta = {"okf_version": OKF_VERSION, **meta}
            dst.write_text(dump_doc(meta, body))
            continue
        if rel.as_posix() == "log.md":
            shutil.copy2(p, dst)
            continue
        meta, body, err = split_frontmatter(p.read_text())
        if err or meta is None:
            shutil.copy2(p, dst)
            continue
        m = dict(meta)
        if "review_by" in m:
            m["stale_after"] = m.pop("review_by")
        if isinstance(m.get("sources"), list):
            m["sources"] = [{("resource" if k == "ref" else k): v for k, v in s.items()} if isinstance(s, dict) else s for s in m["sources"]]
        st = m.get("status")
        if st is not None:
            m["status"] = TO_OKF.get(str(st), "draft")
            m["acf_status"] = st
            rep["status_mapped"] += 1
        dst.write_text(dump_doc(m, body))
        rep["concepts"] += 1
    return rep


def import_okf(src: Path, dest: Path, now=None) -> dict:
    src, dest = Path(src).resolve(), Path(dest).resolve()
    if not src.is_dir():
        raise FileNotFoundError(str(src))
    if dest.exists() and any(dest.iterdir()):
        raise FileExistsError(f"{dest} is not empty")
    now = now or now_utc()
    reg = load_registry()
    rep = {"concepts": 0, "skipped_no_type": [], "placeholders": [], "status_defaulted": 0, "generated_added": 0, "roles_files": 0}
    dest.mkdir(parents=True, exist_ok=True)
    had_log = False
    for p in sorted(src.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(src)
        if rel.parts[0] == ".acf":
            dst = dest / Path(*rel.parts[1:])
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)
            rep["roles_files"] += 1
            continue
        if any(part.startswith(".") for part in rel.parts):
            continue
        dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix != ".md":
            shutil.copy2(p, dst)
            continue
        if rel.as_posix() == "index.md":
            continue  # regenerated below
        if rel.as_posix() == "log.md":
            shutil.copy2(p, dst)
            had_log = True
            continue
        if p.name in ("index.md", "log.md"):
            shutil.copy2(p, dst)
            continue
        meta, body, err = split_frontmatter(p.read_text())
        if err or not meta or not str(meta.get("type") or "").strip():
            rep["skipped_no_type"].append(rel.as_posix())
            continue
        m = dict(meta)
        if "stale_after" in m:
            m["review_by"] = m.pop("stale_after")
        if isinstance(m.get("sources"), list):
            m["sources"] = [{("ref" if k == "resource" else k): v for k, v in s.items()} if isinstance(s, dict) else s for s in m["sources"]]
        spec = reg["types"].get(m["type"])
        if "acf_status" in m:
            m["status"] = m.pop("acf_status")
        elif spec and m.get("status") is not None:
            mapped = FROM_OKF[spec.get("status_set", "doc")].get(str(m["status"]))
            if mapped:
                m["status"] = mapped
                rep["status_defaulted"] += 1
        if not m.get("title"):
            m["title"] = p.stem.replace("-", " ").replace("_", " ")
        if not isinstance(m.get("generated"), dict):
            m["generated"] = {"by": f"ackit-okf-import/{__version__}", "at": iso(now)}
            rep["generated_added"] += 1
        if spec:
            for k in spec.get("required", []):
                if m.get(k) in (None, "", [], {}):
                    m[k] = ""
                    rep["placeholders"].append(f"{rel.as_posix()}: needs `{k}`")
        dst.write_text(dump_doc(m, body))
        rep["concepts"] += 1
    if not (dest / "AGENTS.md").exists():
        new_doc(dest, "entry", dest.name + " - agent entry", extras={"_path": dest / "AGENTS.md", "description": "Entry generated by the OKF import; replace the stubs."},
                ctx={"commands": {}, "rules": [], "stack_line": "see tech-stack", "description": ""}, now=now)
    if not had_log:
        log_entry(dest, f"Imported from an OKF bundle with ackit {__version__}.", now)
    write_index(Bundle.load(dest))
    return rep
