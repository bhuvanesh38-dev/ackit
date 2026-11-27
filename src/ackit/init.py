"""Stack detection, Conductor-style interview, and bundle scaffolding from packs."""
from __future__ import annotations

import fnmatch
import getpass
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

from . import __version__
from .bundle import data_dir, load_registry
from .scaffold import (dump_doc, iso, log_entry, new_doc, now_utc, slugify, write_index)
from .bundle import Bundle, section_body

MANIFESTS = ["package.json", "pyproject.toml", "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "setup.py", "Cargo.toml"]
IGNORE_DIRS = {"node_modules", ".git", ".venv", "venv", "build", "dist", "docs", "doc", "tests", "test", "context",
               "target", "__pycache__", "examples", "scripts", ".github", "out"}


# ------------------------------------------------------------------ packs
def pack_roots(extra: list[Path] | None = None) -> list[Path]:
    return [Path(p) for p in (extra or [])] + [data_dir() / "packs"]


def load_packs(extra: list[Path] | None = None) -> dict[str, dict]:
    packs: dict[str, dict] = {}
    for root in reversed(pack_roots(extra)):  # earlier roots override later ones
        if not root.is_dir():
            continue
        for d in sorted(root.iterdir()):
            f = d / "pack.yaml"
            if d.is_dir() and not d.name.startswith("_") and f.exists():
                spec = yaml.safe_load(f.read_text()) or {}
                spec["_dir"] = d
                packs[spec.get("name", d.name)] = spec
    return packs


def detect_pack(repo: Path, packs: dict[str, dict]) -> tuple[dict, str]:
    best, best_pri = packs["generic"], -1
    for spec in packs.values():
        det = spec.get("detect") or {}
        anyf = det.get("any_files") or []
        if not anyf or not any((repo / f).exists() for f in anyf):
            continue
        ok = True
        for req in det.get("require_text") or []:
            ok = any((repo / f).exists() and req["text"].lower() in (repo / f).read_text(errors="ignore").lower() for f in req["files"])
            if not ok:
                break
        if ok and spec.get("priority", 0) > best_pri:
            best, best_pri = spec, spec.get("priority", 0)
    variant = next(iter(best.get("variants", {"default": {}})))
    for name, v in (best.get("variants") or {}).items():
        if any((repo / f).exists() for f in v.get("detect_files", [])):
            variant = name
            break
    return best, variant


# ------------------------------------------------------------------ modules
def discover_modules(repo: Path, strategies: list[str]) -> list[dict]:
    found: dict[str, str] = {}
    for st in strategies:
        if st == "gradle":
            for f in ("settings.gradle", "settings.gradle.kts"):
                p = repo / f
                if p.exists():
                    for line in re.findall(r"^\s*include\b(.*)$", p.read_text(), re.M):
                        for n in re.findall(r"""['"]:?([^'"]+)['"]""", line):
                            found.setdefault(n.replace(":", "/"), n.replace(":", "/"))
        elif st == "maven":
            p = repo / "pom.xml"
            if p.exists():
                for n in re.findall(r"<module>([^<]+)</module>", p.read_text()):
                    found.setdefault(n.strip(), n.strip())
        elif st == "npm":
            pats: list[str] = []
            p = repo / "package.json"
            if p.exists():
                try:
                    ws = json.loads(p.read_text()).get("workspaces", [])
                    pats += ws.get("packages", []) if isinstance(ws, dict) else ws
                except json.JSONDecodeError:
                    pass
            pw = repo / "pnpm-workspace.yaml"
            if pw.exists():
                pats += (yaml.safe_load(pw.read_text()) or {}).get("packages", [])
            for pat in pats:
                for m in sorted(repo.glob(pat.rstrip("/"))):
                    if m.is_dir():
                        found.setdefault(m.relative_to(repo).as_posix(), m.relative_to(repo).as_posix())
        elif st == "dirs":
            for d in sorted(repo.iterdir()):
                if d.is_dir() and not d.name.startswith(".") and d.name not in IGNORE_DIRS and any((d / m).exists() for m in MANIFESTS):
                    found.setdefault(d.name, d.name)
    return [{"name": Path(p).name, "path": p, "slug": slugify(Path(p).name)} for p in found.values() if (repo / p).is_dir()]


# ------------------------------------------------------------------ interview
def git_user(repo: Path) -> str:
    try:
        v = subprocess.run(["git", "-C", str(repo), "config", "user.name"], capture_output=True, text=True, timeout=5).stdout.strip()
        if v:
            return v
    except Exception:  # LENIENT(git-optional): a repo without git still gets a default owner
        pass
    try:
        return getpass.getuser()
    except Exception:  # LENIENT(no-user): headless containers may have no passwd entry
        return "owner"


def interview(repo: Path, inferred: dict, answers: dict, interactive: bool) -> tuple[dict, list[str]]:
    """Ask only what cannot be inferred. Returns (final answers, keys that were asked)."""
    questions = [
        ("purpose", "One sentence: what does this project do?", ""),
        ("size", "Repository size, small (single module) or large (multi-module)?", inferred["size"]),
        ("owner", "Who owns this context (human id)?", inferred["owner"]),
    ]
    out, asked = dict(inferred), []
    out.update({k: v for k, v in answers.items() if v is not None})
    for key, prompt, default in questions:
        if key in answers:
            continue
        if interactive and (key == "purpose" or key == "size" and inferred["size_uncertain"]):
            val = input(f"{prompt} [{default}] ").strip()
            out[key] = val or default
            asked.append(key)
    return out, asked


# ------------------------------------------------------------------ scaffold
def _why(body: str) -> str:
    w = section_body(body, "Why") or ""
    return w.split("\n")[0].strip()


def init_bundle(repo: Path, bundle_dir: Path, *, answers: dict | None = None, interactive: bool = False,
                pack_name: str | None = None, extra_packs: list[Path] | None = None, force: bool = False,
                link_entry: bool = False, now=None) -> dict:
    repo, bundle_dir = Path(repo).resolve(), Path(bundle_dir).resolve()
    answers = dict(answers or {})
    if bundle_dir.exists() and any(bundle_dir.iterdir()) and not force:
        raise FileExistsError(f"{bundle_dir} is not empty (use --force to add missing files)")
    now = now or now_utc()
    packs = load_packs(extra_packs)
    pack, variant = (packs[pack_name], None) if pack_name else detect_pack(repo, packs)
    if pack_name:
        variant = next(iter(pack.get("variants", {"default": {}})))
        for n, v in (pack.get("variants") or {}).items():
            if any((repo / f).exists() for f in v.get("detect_files", [])):
                variant = n
                break
    var = (pack.get("variants") or {}).get(variant, {})
    modules = discover_modules(repo, pack.get("module_discovery", ["dirs"]))
    inferred = {"project": repo.name, "size": "large" if len(modules) >= 2 else "small", "size_uncertain": len(modules) == 1,
                "owner": git_user(repo), "purpose": ""}
    a, asked = interview(repo, inferred, answers, interactive)
    if "modules" in a and isinstance(a["modules"], list):
        modules = [{"name": Path(m["path"] if isinstance(m, dict) else m).name, "path": m["path"] if isinstance(m, dict) else m,
                    "slug": slugify(Path(m["path"] if isinstance(m, dict) else m).name)} for m in a["modules"]]
    owner = a["owner"]
    commands = {**{"build": "", "test": "", "lint": "", "run": ""}, **(var.get("workflow") or {}), **(a.get("commands") or {})}
    stack = pack.get("stack") or {}
    languages, frameworks = stack.get("languages") or ["unspecified"], stack.get("frameworks", [])
    project = a["project"]
    search = [pack["_dir"] / "templates"]
    bundle_dir.mkdir(parents=True, exist_ok=True)
    reg = load_registry()
    created: list[str] = []

    def make(t, title, **kw):
        extras = dict(kw.pop("extras", {}))
        if "_path" in kw:
            extras["_path"] = kw.pop("_path")
        try:
            p = new_doc(bundle_dir, t, title, extras=extras, search=search, now=now, **kw)
        except FileExistsError:
            return None
        created.append(p.relative_to(bundle_dir).as_posix())
        return p

    stack_line = ", ".join(languages + frameworks) or "see tech-stack"
    # rules
    rule_ctx = []
    rule_files = [f for d in (data_dir() / "packs" / "_base" / "rules", pack["_dir"] / "rules") if d.is_dir() for f in sorted(d.glob("*.md"))]
    from .bundle import split_frontmatter
    for f in rule_files:
        meta, body, _ = split_frontmatter(f.read_text())
        slug = f.stem
        extras = {"id": None}
        applies = meta.get("applies_to") or []
        ex = {"severity": meta.get("severity", "advisory")}
        if applies:
            ex["applies_to"] = applies
        title = meta["title"]
        path = bundle_dir / "rules" / f"{slug}.md"
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        m = {"type": "rule", "id": f"R-{slug}", "title": title, "status": "draft", "severity": ex["severity"]}
        if applies:
            m["applies_to"] = applies
        m["generated"] = {"by": f"ackit/{__version__}", "at": iso(now)}
        m["review_by"] = iso(now.replace(year=now.year + 1))
        path.write_text(dump_doc(m, body))
        created.append(f"rules/{slug}.md")
        rule_ctx.append({"title": title, "slug": slug, "why": _why(body)})
    from .roles import all_role_names, load_role
    tmp_b = Bundle(bundle_dir, {}, reg)
    role_rows = [{"name": n, "title": load_role(tmp_b, n).title, "owns": load_role(tmp_b, n).profile.get("owns") or [],
                  "gates": load_role(tmp_b, n).profile.get("gates") or []} for n in all_role_names(tmp_b)]
    owners = {}
    for r in role_rows:
        for t in r["owns"]:
            owners.setdefault(t, []).append(r["name"])
    ownership = [{"type": t, "roles": owners.get(t, []), "reviews": s.get("owner", {}).get("reviews", ""), "signs_off": s.get("owner", {}).get("signs_off", "")}
                 for t, s in reg["types"].items()]
    ctx_common = {"roles": role_rows, "ownership": ownership, "project": project, "owner": owner, "commands": commands, "stack_line": stack_line,
                  "languages": languages, "frameworks": frameworks, "version_sources": var.get("version_sources", "the build files"),
                  "modules": modules, "rules": rule_ctx}
    # entry
    make("entry", f"{project} - agent entry", _path=bundle_dir / "AGENTS.md",
         ctx={**ctx_common}, extras={"description": a.get("purpose") or f"Agent context for {project}"})
    make("product", project, _path=bundle_dir / "product.md", extras={"description": a.get("purpose") or f"What {project} is for"}, ctx=ctx_common)
    make("tech-stack", f"{project} tech stack", _path=bundle_dir / "tech-stack.md",
         extras={"languages": languages, "frameworks": frameworks, "description": "Languages, frameworks and infrastructure"}, ctx=ctx_common)
    make("workflow", f"{project} workflow", _path=bundle_dir / "workflow.md",
         extras={"commands": {k: commands.get(k, "") for k in ("build", "test", "lint", "run")}, "description": "Build, test, lint and review flow"}, ctx=ctx_common)
    make("architecture", f"{project} architecture", _path=bundle_dir / "architecture.md", extras={"description": "Components and data flow"}, ctx=ctx_common)
    make("responsibility", f"{project} responsibilities", _path=bundle_dir / "responsibilities.md", extras={"description": "Who is responsible for what (RACI)"}, ctx=ctx_common)
    if a["size"] == "large":
        for m in modules:
            make("module", m["name"], ident=f"M-{m['slug']}", _path=bundle_dir / "modules" / f"{m['slug']}.md",
                 extras={"path": m["path"], "description": f"Module {m['name']} at {m['path']}"}, ctx=ctx_common)
    adr = make("decision", "Adopt the Agent Context Format", ident="ADR-0001",
               extras={"date": now.date().isoformat(), "description": "Why this repository keeps agent context as ACF"}, ctx=ctx_common)
    if adr:
        adr.write_text(adr.read_text().replace(
            "The situation and forces. What problem forces a choice now.",
            "Agents and people need the same, small, checkable source of project context.").replace(
            "1. Option A: pros, cons\n2. Option B: pros, cons",
            "1. Ad-hoc notes: no structure, cannot be validated.\n2. ACF bundle: typed documents, validated in CI.").replace(
            "The chosen option, in one sentence.", "Keep agent context as an ACF bundle in this repository.").replace(
            "The deciding reason. What was weighed against what.", "Typed, validated context stays accurate and is cheap to load progressively.").replace(
            "What becomes easier, what becomes harder, what must be done next. Supersedes: none.",
            "Documents need owners and upkeep; `ackit validate` runs in CI."))
    make("journal", f"{project} journal", _path=bundle_dir / "journals" / "project.md", extras={"about": "product"}, ctx={"about": "the project"})
    cfg = bundle_dir / "ackit.yaml"
    if not cfg.exists():
        cfg.write_text(yaml.safe_dump({"project": project, "pack": pack["name"], "size": a["size"], "agents_md_max_lines": 150,
                                       "links": "warn", "severity": {}}, sort_keys=False))
        created.append("ackit.yaml")
    log_entry(bundle_dir, f"Created by ackit {__version__} from pack `{pack['name']}` ({a['size']} repo). Documents are `draft` until a human verifies them.", now)
    created.append("log.md")
    write_index(Bundle.load(bundle_dir))
    created.append("index.md")
    if link_entry and not (repo / "AGENTS.md").exists():
        (repo / "AGENTS.md").symlink_to(Path(bundle_dir / "AGENTS.md").relative_to(repo) if bundle_dir.is_relative_to(repo) else bundle_dir / "AGENTS.md")
    return {"pack": pack["name"], "variant": variant, "size": a["size"], "modules": modules, "asked": asked,
            "inferred": [k for k in ("project", "size", "owner") if k not in answers and k not in asked], "created": created, "commands": commands}


def load_answers(path: str | None) -> dict:
    return (yaml.safe_load(Path(path).read_text()) or {}) if path else {}
