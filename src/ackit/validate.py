"""ACF conformance and enforcement checks. Every rule has a stable code (see SPEC.md section 9)."""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path

from .bundle import Bundle, Doc, LINK_RE, as_list, headings, parse_dt, section_body
from .idalloc import id_config
from .layout import config as layout_config
from .checks import parse as parse_checks
from .workspace import config as workspace_config, folder_author, hidden_from_index
from .codelines import doc_lines, known_lines
from .branchpolicy import policy as branch_policy
from .registry import build as build_registry
from . import vocab as vocab_mod

DEFAULT_SEVERITY = {
    "ACF001": "error", "ACF002": "error", "ACF003": "warn", "ACF004": "error", "ACF005": "error",
    "ACF006": "error", "ACF007": "error", "ACF008": "warn", "ACF009": "error", "ACF010": "warn",
    "ACF011": "error", "ACF012": "error", "ACF013": "error", "ACF014": "error", "ACF015": "error",
    "ACF016": "error", "ACF017": "error", "ACF018": "error", "ACF019": "error", "ACF020": "error",
    "ACF021": "error", "ACF022": "warn", "ACF023": "warn", "ACF024": "warn", "ACF025": "warn",
    "ACF026": "error", "ACF027": "error", "ACF028": "error", "ACF029": "error", "ACF030": "error",
    "ACF031": "error", "ACF032": "error", "ACF033": "error", "ACF034": "error", "ACF037": "error", "ACF035": "error", "ACF036": "warn", "ACF038": "error", "ACF039": "error", "ACF040": "error", "ACF041": "error", "ACF042": "error",
    "ACF043": "error", "ACF044": "error", "ACF045": "warn",
}
RULE_TEXT = {
    "ACF001": "frontmatter parses", "ACF002": "non-empty type", "ACF003": "type is in the registry",
    "ACF004": "required frontmatter present", "ACF005": "required sections present",
    "ACF006": "status is in the type's set", "ACF007": "status transition is legal (via history)",
    "ACF008": "markdown links resolve", "ACF009": "ids are unique", "ACF010": "review_by not passed",
    "ACF011": "trust gate: human verification at stable/accepted", "ACF012": "work-item completeness at done",
    "ACF013": "AGENTS.md size budget", "ACF014": "root index.md carries acf_version", "ACF015": "log.md well formed",
    "ACF016": "id format and file naming", "ACF017": "stage/signoff order", "ACF018": "frontmatter references resolve",
    "ACF019": "supersedes is reciprocal", "ACF020": "journal entry format", "ACF021": "session entry/index format",
    "ACF022": "type lives in its conventional directory", "ACF023": "generated block present",
    "ACF024": "concept is listed in an index.md", "ACF025": "section not empty past draft",
    "ACF026": "enum value valid", "ACF027": "signoff present", "ACF028": "entry file AGENTS.md exists",
    "ACF029": "command/field shape", "ACF030": "role definitions are complete (role.yaml, prompt, rules, checklist, outputs)",
    "ACF031": "points are an integer in the configured scale", "ACF032": "points vs split limit (signoff_max)",
    "ACF033": "runs records are well formed with unique ids", "ACF034": "external_id is a non-empty string",
    "ACF035": "code_lines are well formed and, with a registry, known code lines",
    "ACF036": "a workspace document carries author equal to its folder",
    "ACF037": "id_allocation configuration is usable",
    "ACF038": "environment_registry configuration is usable",
    "ACF039": "branch_policy configuration is usable",
    "ACF040": "author_workspace configuration is usable",
    "ACF041": "process_checks configuration is usable",
    "ACF042": "consumer_layout configuration is usable",
    "ACF043": "a field bound to a vocabulary holds a registered value",
    "ACF044": "vocabularies configuration is usable",
    "ACF045": "session entry heading shape: date (Day, Www) - branch @ sha - title",
}
DATE_RE = r"\d{4}-\d{2}-\d{2}"
DASH = r"[-–—]"
SESSION_HEAD_RE = re.compile(
    rf"{DATE_RE}\s+\((Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s*W(0[1-9]|[1-4]\d|5[0-3])\)\s+{DASH}\s+(\S+)\s+@\s+([0-9a-fA-F]{{7,40}}|none)\s+{DASH}\s+\S.*")
STATUS_ORDER_WORK = ["draft", "ready", "in-progress", "in-review", "done"]
POINTS_DEFAULTS = {"scale": [1, 2, 3, 5, 8], "auto_start_max": 2, "signoff_max": 5}


def points_config(config: dict) -> tuple[dict, str | None]:
    """The effective `points` settings (defaults merged with `ackit.yaml`) and a problem text when the config is unusable."""
    cfg = dict(POINTS_DEFAULTS)
    raw = (config or {}).get("points")
    if raw is None:
        return cfg, None
    if not isinstance(raw, dict):
        return cfg, "`points` in ackit.yaml must be a mapping {scale, auto_start_max, signoff_max}"
    cfg.update(raw)
    scale = cfg["scale"]
    if (not isinstance(scale, list) or not scale or not all(_is_int(x) and x > 0 for x in scale)
            or scale != sorted(set(scale))):
        return dict(POINTS_DEFAULTS), f"`points.scale` must be an ascending list of positive integers, got {scale!r}"
    for k in ("auto_start_max", "signoff_max"):
        if not _is_int(cfg[k]):
            return dict(POINTS_DEFAULTS), f"`points.{k}` must be an integer, got {cfg[k]!r}"
    if cfg["auto_start_max"] > cfg["signoff_max"]:
        return dict(POINTS_DEFAULTS), "`points.auto_start_max` must not exceed `points.signoff_max`"
    return cfg, None


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _is_datetime(v) -> bool:
    if isinstance(v, dt.datetime):
        return True
    return isinstance(v, str) and bool(re.search(r"\d[T ]\d", v)) and parse_dt(v) is not None


@dataclass
class Issue:
    code: str
    severity: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.severity.upper():5} {self.code} {self.path}: {self.message}"

    def as_dict(self) -> dict:
        return {"code": self.code, "severity": self.severity, "path": self.path, "message": self.message}


class Validator:
    def __init__(self, bundle: Bundle, now: dt.datetime | None = None):
        self.b = bundle
        self.now = now or dt.datetime.now(dt.timezone.utc)
        self.issues: list[Issue] = []
        sev = dict(DEFAULT_SEVERITY)
        sev.update({k: ("off" if v is False else v) for k, v in (bundle.config.get("severity") or {}).items()})
        self.sev = sev

    def add(self, code: str, path: str, msg: str):
        s = self.sev.get(code, "error")
        if s != "off":
            self.issues.append(Issue(code, s, path, msg))

    # ---------------------------------------------------------------- entry
    def run(self, only: set[str] | None = None) -> list[Issue]:
        b = self.b
        for d in b.docs:
            self.doc_basic(d)
        self.ids_unique()
        for d in b.docs:
            if d.type and b.type_spec(d.type) and not d.err:
                self.doc_typed(d)
        self.id_allocation_config()
        self.registry_config()
        self.branch_policy_config()
        self.code_lines()
        self.author_workspace()
        self.process_checks()
        self.consumer_layout()
        self.vocabularies()
        self.work_rules()
        self.supersedes()
        self.index_and_log()
        self.entry()
        if only is None:
            self.roles()
        if only is not None:
            self.issues = [i for i in self.issues if i.path in only]
        return self.issues

    def id_allocation_config(self):
        for problem in id_config(self.b.config)[1]:
            self.add("ACF037", "ackit.yaml", problem + "; `ackit new` refuses to allocate ids until it is fixed")

    def registry_config(self):
        for problem in build_registry(self.b.config, self.b.root)[1]:
            self.add("ACF038", "ackit.yaml", problem)

    def vocabularies(self):
        b = self.b
        known_types = set(b.registry["types"])
        pairs = [(d.type, d.meta) for d in b.docs if d.type and not d.err]
        vocabs, problems = vocab_mod.build(b.config, b.root, pairs, known_types)
        for problem in problems:
            self.add("ACF044", "ackit.yaml", problem)
        if not vocabs:
            return
        for d in b.docs:
            spec = b.type_spec(d.type) if d.type and not d.err else None
            if spec:
                for msg in vocab_mod.check(d.meta, spec, vocabs):
                    self.add("ACF043", d.rel, msg)

    def consumer_layout(self):
        for problem in layout_config(self.b.config)[1]:
            self.add("ACF042", "ackit.yaml", problem)

    def process_checks(self):
        for problem in parse_checks(self.b.config)[1]:
            self.add("ACF041", "ackit.yaml", problem)

    def author_workspace(self):
        cfg, problems = workspace_config(self.b.config)
        for problem in problems:
            self.add("ACF040", "ackit.yaml", problem)
        for d in self.b.docs:
            who = folder_author(d.rel, cfg)
            if who is None or d.err or not d.type:        # a document that failed to parse or has no type is reported by ACF001 and ACF002
                continue
            got = d.meta.get("author")
            if not isinstance(got, str) or got.strip() != who:
                self.add("ACF036", d.rel, f"a document under the workspace of {who!r} must carry `author: {who}` as a string (found {got!r})")

    def code_lines(self):
        reg = build_registry(self.b.config, self.b.root)[0]
        known = known_lines(reg) if reg else None
        for d in self.b.docs:
            lines, problem = doc_lines(d.meta)
            if problem:
                self.add("ACF035", d.rel, problem)
            elif known is not None:
                for x in lines:
                    if x not in known:
                        self.add("ACF035", d.rel, f"code line {x!r} is not the code_line of any environment in the registry (known: {', '.join(sorted(known)) or 'none'})")

    def branch_policy_config(self):
        for problem in branch_policy(self.b.config)[1]:
            self.add("ACF039", "ackit.yaml", problem)

    # ---------------------------------------------------------------- per doc
    def doc_basic(self, d: Doc):
        if d.err:
            self.add("ACF001", d.rel, d.err)
            return
        if not d.type:
            self.add("ACF002", d.rel, "frontmatter has no non-empty `type`")
            return
        if not self.b.type_spec(d.type):
            self.add("ACF003", d.rel, f"unknown type '{d.type}' (treated as a generic concept)")

    def doc_typed(self, d: Doc):
        b, m = self.b, d.meta
        spec = b.type_spec(d.type)
        sset = b.status_set(spec)
        for k in spec.get("required", []):
            if m.get(k) in (None, "", [], {}):
                self.add("ACF004", d.rel, f"missing required frontmatter `{k}` for type {d.type}")
        for k, allowed in (spec.get("enums") or {}).items():
            if k in m and not any(type(m[k]) is type(a) and m[k] == a for a in allowed):          # exact: 1.0 and true are not 1
                self.add("ACF026", d.rel, f"`{k}: {m[k]}` is not allowed; legal values: {allowed}")
        if "commands" in spec.get("required", []):
            c = m.get("commands")
            if isinstance(c, dict):
                miss = [k for k in ("build", "test", "lint") if k not in c]
                if miss:
                    self.add("ACF029", d.rel, f"commands is missing keys {miss}")
            elif c is not None:
                self.add("ACF029", d.rel, "commands must be a mapping")
        # status
        st = d.status
        if st is not None and st not in sset["values"]:
            self.add("ACF006", d.rel, f"status '{st}' is not allowed for type {d.type}; legal values: {sset['values']}")
        elif st is None and spec.get("status_set") and "status" in spec.get("required", []):
            pass
        self.history(d, sset)
        self.optional_fields(d, spec)
        # trust
        if st in sset.get("human_verified", []) and spec.get("human_verified", True) is not False:
            ver = as_list(m.get("verified"))
            if not any(str((v or {}).get("by", "")).startswith("human:") for v in ver if isinstance(v, dict)):
                self.add("ACF011", d.rel, f"status '{st}' needs a `verified` entry by a `human:` actor")
        if not isinstance(m.get("generated"), dict) or not m["generated"].get("by"):
            self.add("ACF023", d.rel, "no `generated: {by, at}` block (provenance)")
        # staleness
        if "review_by" in m:
            sa = parse_dt(m["review_by"])
            if sa is None:
                self.add("ACF010", d.rel, "review_by is not an ISO 8601 datetime")
            elif self.now >= sa:
                self.add("ACF010", d.rel, f"stale since {sa.date()} (review_by passed): re-verify or update")
        # sections
        self.sections(d, spec)
        # id + naming
        self.ident(d, spec)
        # dir convention
        tdir = spec.get("dir") or ""
        if tdir and not d.rel.startswith(tdir.rstrip("/") + "/") and not (d.type == "journal" and d.rel.startswith("work/")):
            self.add("ACF022", d.rel, f"type {d.type} normally lives under {tdir}/")
        # refs
        for k in spec.get("refs", []) + (["about"] if d.type == "journal" else []):
            for r in as_list(m.get(k)):
                if not b.resolve(str(r)):
                    self.add("ACF018", d.rel, f"`{k}: {r}` does not resolve to any id or concept")
        # type specific
        if d.type == "journal":
            self.journal(d)
        elif d.type == "session":
            self.session(d)
        elif d.type == "session-index":
            self.session_index(d)
        elif d.type == "feature-stage":
            if m.get("stage") not in b.registry["stages"]:
                self.add("ACF026", d.rel, f"stage must be one of {b.registry['stages']}")
            else:
                need = b.registry["stage_sections"].get(m["stage"], [])
                self.require_sections(d, need)
            if st == "signed-off" and not (isinstance(m.get("signoff"), dict) and m["signoff"].get("by")):
                self.add("ACF027", d.rel, "signed-off stage needs `signoff: {by, at}`")
        if d.type == "feature" and m.get("tier") == "small" and st in STATUS_ORDER_WORK[1:]:
            if not (isinstance(m.get("signoff"), dict) and m["signoff"].get("by")):
                self.add("ACF027", d.rel, "small feature past draft needs `signoff: {by, at}`")
        self.links(d)

    def optional_fields(self, d: Doc, spec: dict):
        """Shape checks for the optional fields a type lists under `optional` (points, runs, external_id)."""
        opt = spec.get("optional") or []
        m = d.meta
        if "external_id" in opt and "external_id" in m:
            v = m["external_id"]
            if not (isinstance(v, str) and v.strip()):
                self.add("ACF034", d.rel, f"`external_id: {v!r}` must be a non-empty string (the ticket key in an external tracker)")
        if "points" in opt and m.get("points") is not None:
            self.points(d)
        if "runs" in opt and "runs" in m:
            self.runs(d)

    def points(self, d: Doc):
        cfg, problem = points_config(self.b.config)
        if problem and d.type in ("task", "issue") and not getattr(self, "_points_cfg_reported", False):
            self._points_cfg_reported = True
            self.add("ACF031", "ackit.yaml", problem + "; the defaults are used")
        v = d.meta["points"]
        if not _is_int(v) or v not in cfg["scale"]:
            self.add("ACF031", d.rel, f"`points: {v!r}` is not in the scale {cfg['scale']}")
            return
        if v > cfg["signoff_max"] and d.status in ("ready", "in-progress"):
            self.add("ACF032", d.rel, f"{v} points is above signoff_max {cfg['signoff_max']}: split it into smaller items before it is '{d.status}' (it may stay draft, blocked or cancelled)")
        if v > cfg["auto_start_max"] and d.status in STATUS_ORDER_WORK[1:]:
            so = d.meta.get("signoff")
            if not (isinstance(so, dict) and so.get("by")):
                self.add("ACF027", d.rel, f"{v} points is above auto_start_max {cfg['auto_start_max']}: needs `signoff: {{by, at}}` before it is '{d.status}'")

    def runs(self, d: Doc):
        runs = d.meta["runs"]
        if not isinstance(runs, list):
            self.add("ACF033", d.rel, "`runs` must be a list of run records")
            return
        seen: set[str] = set()
        for i, r in enumerate(runs, 1):
            where = f"runs[{i}]"
            if not isinstance(r, dict):
                self.add("ACF033", d.rel, f"{where} must be a mapping {{id, at, outcome, tokens?, turns?, commit?, by?}}")
                continue
            rid = r.get("id")
            if not (isinstance(rid, str) and rid.strip()):
                self.add("ACF033", d.rel, f"{where}.id is required and must be a non-empty string")
            elif rid in seen:
                self.add("ACF033", d.rel, f"{where}.id '{rid}' is not unique within runs")
            else:
                seen.add(rid)
            if not _is_datetime(r.get("at")):
                self.add("ACF033", d.rel, f"{where}.at is required and must be an ISO 8601 datetime, got {r.get('at')!r}")
            oc = r.get("outcome")
            if not (isinstance(oc, str) and oc.strip()):
                self.add("ACF033", d.rel, f"{where}.outcome is required and must be a non-empty string")
            for k in ("tokens", "turns"):
                if k in r and r[k] is not None and not (_is_int(r[k]) and r[k] >= 0):
                    self.add("ACF033", d.rel, f"{where}.{k} must be a non-negative integer, got {r[k]!r}")
            for k in ("commit", "by"):
                if k in r and r[k] is not None and not isinstance(r[k], str):
                    self.add("ACF033", d.rel, f"{where}.{k} must be a string, got {r[k]!r}")

    def history(self, d: Doc, sset: dict):
        hist = as_list(d.meta.get("history"))
        if not hist:
            return
        seq = [str(h.get("status")) if isinstance(h, dict) else str(h) for h in hist]
        for a, bb in zip(seq, seq[1:]):
            legal = sset["transitions"].get(a, [])
            if bb not in legal:
                self.add("ACF007", d.rel, f"illegal status transition {a} -> {bb}; legal from '{a}': {legal or 'none (final status)'}")
        if d.status and seq[-1] != d.status:
            self.add("ACF007", d.rel, f"history ends at '{seq[-1]}' but status is '{d.status}'")

    def require_sections(self, d: Doc, names: list[str]):
        for n in names:
            body = section_body(d.body, n)
            if body is None:
                self.add("ACF005", d.rel, f"missing required section '{n}'")
            elif not body and d.status not in (None, "draft", "proposed", "open", "cancelled"):
                self.add("ACF025", d.rel, f"section '{n}' is empty")

    def sections(self, d: Doc, spec: dict):
        secs = spec.get("sections")
        if isinstance(secs, dict):
            secs = secs.get(str(d.meta.get(secs["by"])), [])
        if secs:
            self.require_sections(d, secs)

    def ident(self, d: Doc, spec: dict):
        pat = spec.get("id_pattern")
        if not pat or not d.id:
            return
        if not re.match(pat, d.id):
            self.add("ACF016", d.rel, f"id '{d.id}' does not match {pat}")
            return
        stem = Path(d.rel).stem
        parent = Path(d.rel).parent.name
        ok = stem == d.id or stem.startswith(d.id + "-") or parent == d.id or parent.startswith(d.id + "-")
        if d.id[:2] in ("M-", "R-") and stem == d.id[2:]:
            ok = True
        if not ok:
            self.add("ACF016", d.rel, f"file name should start with the id '{d.id}'")

    def links(self, d: Doc):
        mode = self.b.config.get("links", "default")
        mode = "off" if mode is False else mode
        fence = False
        for line in d.body.splitlines():
            if line.lstrip().startswith("```"):
                fence = not fence
            if fence:
                continue
            for m in LINK_RE.finditer(re.sub(r"`[^`]*`", "", line)):
                tgt = m.group(1).split("#")[0]
                if not tgt or re.match(r"^[a-z][a-z0-9+.-]*:", tgt, re.I):
                    continue
                base = self.b.root if tgt.startswith("/") else d.path.parent
                p = (base / tgt.lstrip("/")).resolve()
                if not (p.exists() or p.with_suffix(".md").exists() or Path(str(p) + ".md").exists()):
                    if mode == "off":
                        continue
                    if mode == "error":
                        self.issues.append(Issue("ACF008", "error", d.rel, f"link target not found: {m.group(1)}"))
                    else:
                        self.add("ACF008", d.rel, f"link target not found: {m.group(1)}")

    # ---------------------------------------------------------------- whole bundle
    def ids_unique(self):
        seen: dict[str, str] = {}
        for d in self.b.docs:
            if d.id:
                if d.id in seen:
                    self.add("ACF009", d.rel, f"duplicate id '{d.id}' (also {seen[d.id]})")
                else:
                    seen[d.id] = d.rel

    def work_rules(self):
        b = self.b
        stages_by_feat: dict[str, dict[str, Doc]] = {}
        for s in b.of_type("feature-stage"):
            stages_by_feat.setdefault(str(s.meta.get("feature")), {})[str(s.meta.get("stage"))] = s
        order = [s for s in b.registry["stages"] if s != "journal"]
        for feat, stages in stages_by_feat.items():
            for i, name in enumerate(order):
                s = stages.get(name)
                if s and s.status == "signed-off":
                    for prev in order[:i]:
                        p = stages.get(prev)
                        if not p or p.status != "signed-off":
                            self.add("ACF017", s.rel, f"stage '{name}' signed off but earlier stage '{prev}' is not")
                            break
        for f in b.of_type("feature"):
            st = f.status
            if f.meta.get("tier") == "large" and st in ("ready", "in-progress", "in-review", "done"):
                need = order[:4] + (order[4:5] if st in ("in-review", "done") else [])
                stages = stages_by_feat.get(f.id or "", {})
                for n in need:
                    if not stages.get(n) or stages[n].status != "signed-off":
                        self.add("ACF017", f.rel, f"feature is '{st}' but stage '{n}' is not signed off")
        # completeness
        for d in b.docs:
            spec = b.type_spec(d.type) if d.type else None
            if not spec or d.status != "done" or not d.id:
                continue
            for req in spec.get("done_requires", []):
                self.complete(d, req)

    def complete(self, d: Doc, req: str):
        b = self.b
        if req == "test-evidence":
            ok = [e for e in b.of_type("test-evidence") if self.refers(e, "item", d) and e.meta.get("result") == "pass"]
            if not ok:
                self.add("ACF012", d.rel, f"{d.id} is done but has no test-evidence record with result: pass")
        elif req == "review":
            ok = [e for e in b.of_type("review") if self.refers(e, "item", d) and e.meta.get("verdict") == "approve"]
            if not ok:
                self.add("ACF012", d.rel, f"{d.id} is done but has no review record with verdict: approve")
        elif req == "journal":
            ok = [e for e in b.of_type("journal") if self.refers(e, "about", d)]
            if not ok:
                self.add("ACF012", d.rel, f"{d.id} is done but has no journal (about: {d.id})")
        elif req == "children-done":
            kids = [f for f in b.of_type("feature") if self.refers(f, "epic", d)]
            if not kids or any(k.status != "done" for k in kids):
                self.add("ACF012", d.rel, f"{d.id} is done but it has no features or some are not done")

    def refers(self, doc: Doc, key: str, target: Doc) -> bool:
        return any(str(r) == target.id or str(r).strip("/").removesuffix(".md") == target.cid for r in as_list(doc.meta.get(key)))

    def supersedes(self):
        for d in self.b.of_type("decision"):
            for old_ref in as_list(d.meta.get("supersedes")):
                old = self.b.resolve(str(old_ref))
                if old and (str(old.meta.get("superseded_by")) != d.id or old.status != "superseded"):
                    self.add("ACF019", d.rel, f"{d.id} supersedes {old.id}, which must have superseded_by: {d.id} and status: superseded")

    def roles(self):
        from .roles import all_role_names, load_role, overlay_roles, validate_role
        known = set(all_role_names(self.b))
        for name in overlay_roles(self.b) + [r for r in all_role_names(self.b) if r not in overlay_roles(self.b)]:
            try:
                role = load_role(self.b, name)
            except (LookupError, ValueError) as e:
                self.add("ACF030", f"roles/{name}", str(e))
                continue
            if role.origin == "kit":
                continue
            for prob in validate_role(self.b, role):
                self.add("ACF030", f"roles/{name}", prob)
        for r in self.b.of_type("review"):
            if r.meta.get("role") and r.meta["role"] not in known:
                self.add("ACF026", r.rel, f"review role '{r.meta['role']}' is not a known role")

    def entry(self):
        a = self.b.root / "AGENTS.md"
        if not a.exists():
            self.add("ACF028", "AGENTS.md", "entry file AGENTS.md is missing at the bundle root")
            return
        ent = next((d for d in self.b.docs if d.rel == "AGENTS.md"), None)
        if ent and ent.type != "entry":
            self.add("ACF004", "AGENTS.md", "AGENTS.md must have `type: entry`")
        n = len(a.read_text().splitlines())
        cap = int(self.b.config.get("agents_md_max_lines", 150))
        if n > cap:
            self.add("ACF013", "AGENTS.md", f"{n} lines exceeds the budget of {cap}; move detail to rules/ or reference/")

    def index_and_log(self):
        root_idx = next((d for d in self.b.reserved if d.rel == "index.md"), None)
        if not root_idx:
            self.add("ACF014", "index.md", "root index.md is missing")
        else:
            from .bundle import split_frontmatter
            meta, _body, _e = split_frontmatter(root_idx.path.read_text())
            if not meta or not meta.get("acf_version"):
                self.add("ACF014", "index.md", "root index.md frontmatter must carry acf_version")
        linked: set[str] = set()
        for ix in (d for d in self.b.reserved if d.path.name == "index.md"):
            for m in LINK_RE.finditer(ix.path.read_text()):
                t = m.group(1).split("#")[0]
                base = self.b.root if t.startswith("/") else ix.path.parent
                p = (base / t.lstrip("/")).resolve()
                try:
                    linked.add(p.relative_to(self.b.root).as_posix().removesuffix(".md"))
                except ValueError:
                    pass
        if root_idx:
            ws = workspace_config(self.b.config)[0]
            for d in self.b.docs:
                if d.type and d.cid not in linked and d.cid != "AGENTS" and not hidden_from_index(d.rel, ws):
                    self.add("ACF024", d.rel, "not listed in any index.md (run `ackit index --write`)")
        log = next((d for d in self.b.reserved if d.rel == "log.md"), None)
        if log:
            dates = re.findall(rf"^#{{1,3}}\s+({DATE_RE})\s*$", log.path.read_text(), re.M)
            allh = re.findall(r"^##\s+(.*)$", log.path.read_text(), re.M)
            if not dates:
                self.add("ACF015", "log.md", "log.md needs at least one `## YYYY-MM-DD` entry")
            elif dates != sorted(dates, reverse=True):
                self.add("ACF015", "log.md", "log.md dates must be newest first")
            bad = [h for h in allh if not re.fullmatch(DATE_RE, h.strip())]
            if bad:
                self.add("ACF015", "log.md", f"non-date level-2 heading '{bad[0]}'")

    # ---------------------------------------------------------------- body formats
    def journal(self, d: Doc):
        dates = []
        for lvl, text, _ln in headings(d.body):
            if lvl != 2:
                continue
            m = re.fullmatch(rf"({DATE_RE})\s+{DASH}\s+(decision|correction|finding|note):\s*(.+)", text)
            if not m:
                self.add("ACF020", d.rel, f"journal entry heading '{text}' must be `YYYY-MM-DD - kind: title`")
            else:
                dates.append(m.group(1))
        if dates != sorted(dates, reverse=True):
            self.add("ACF020", d.rel, "journal entries must be newest first")

    def session(self, d: Doc):
        parts = re.split(r"^## ", d.body, flags=re.M)[1:]
        for p in parts:
            head = p.splitlines()[0] if p.strip() else ""
            if not re.match(DATE_RE, head):
                self.add("ACF021", d.rel, f"session entry heading '{head[:40]}' must start with YYYY-MM-DD")
                continue
            if not SESSION_HEAD_RE.fullmatch(head.strip()):
                self.add("ACF045", d.rel, f"session entry heading '{head[:60]}' must be `YYYY-MM-DD (Day, Www) - branch @ sha - title` (`@ none` when no commit)")
            for lab in ("Done", "Faced", "Decisions", "Build", "Next", "Blockers"):
                if not re.search(rf"\*\*{lab}:?\*\*:?", p):
                    self.add("ACF021", d.rel, f"entry '{head[:40]}' lacks the **{lab}:** label")

    def session_index(self, d: Doc):
        for line in d.body.splitlines():
            if line.startswith("- ") and not re.match(rf"- {DATE_RE}\b", line):
                self.add("ACF021", d.rel, f"index line must start with `- YYYY-MM-DD`: {line[:50]}")


def validate(bundle: Bundle, now: dt.datetime | None = None, only: set[str] | None = None) -> list[Issue]:
    return Validator(bundle, now).run(only)


def exit_code(issues: list[Issue], strict: bool = False) -> int:
    if any(i.severity == "error" for i in issues):
        return 1
    if strict and any(i.severity == "warn" for i in issues):
        return 1
    return 0
