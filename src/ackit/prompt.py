"""Assemble a role prompt from role templates plus the bundle: stack, rules, modules, work item."""
from __future__ import annotations

import re
from pathlib import Path

from .codelines import applies_to_line
from . import __version__
from .bundle import Bundle, Doc, as_list, data_dir, section_body
from .roles import all_role_names, load_role
from .scaffold import jinja_env, now_utc, iso

COMMENT_RE = re.compile(r"<!--.*?-->\s*", re.S)


def clean(body: str, limit: int | None) -> str:
    b = COMMENT_RE.sub("", body).strip()
    if limit and len(b) > limit:
        b = b[:limit].rstrip() + "\n[...trimmed; read the file for the rest]"
    return b


def applies(rule: Doc, role: str, mods: set[str]) -> bool:
    roles = as_list(rule.meta.get("applies_to"))
    rm = set(map(str, as_list(rule.meta.get("modules"))))
    return (not roles or role in roles) and (not rm or not mods or bool(rm & mods))


def build_context(bundle: Bundle, role: str, item_ref: str | None, limit: int | None, ex: list | None = None, code_line: str | None = None) -> dict:
    ex = ex if ex is not None else []
    rdef = load_role(bundle, role)
    for kind in ("rules", "checklist", "outputs"):
        ex.append((f"role {kind}", rdef.parts[kind][1] if kind in rdef.parts else "missing", "role definition"))
    item_doc = bundle.resolve(item_ref) if item_ref else None
    if item_ref and not item_doc:
        raise LookupError(f"work item '{item_ref}' not found in the bundle")
    item, mod_ids = None, []
    related = [{"label": "Entry", "link": "/AGENTS.md"}, {"label": "Index of all documents", "link": "/index.md"}]
    if item_doc:
        mod_ids = [str(m) for m in as_list(item_doc.meta.get("modules"))]
        stages = []
        if item_doc.type == "feature" and item_doc.meta.get("tier") == "large":
            order = bundle.registry["stages"]
            sd = [s for s in bundle.of_type("feature-stage") if str(s.meta.get("feature")) == item_doc.id]
            for s in sorted(sd, key=lambda s: order.index(s.meta.get("stage")) if s.meta.get("stage") in order else 99):
                stages.append({"stage": s.meta.get("stage"), "status": s.status, "body": clean(s.body, limit)})
        body = clean(item_doc.body, limit)
        parent = bundle.resolve(str(item_doc.meta.get("feature"))) if item_doc.meta.get("feature") else None
        if parent:
            goal = section_body(parent.body, "Goal") or ""
            body += f"\n\nParent feature {parent.id} goal: {clean(goal, 600)}"
            related.append({"label": f"Parent feature {parent.id}", "link": "/" + parent.rel})
        item = {"id": item_doc.id or item_doc.cid, "title": item_doc.title, "type": item_doc.type, "status": item_doc.status,
                "depends": [str(x) for x in as_list(item_doc.meta.get("depends_on"))], "body": body, "stages": stages}
        related.append({"label": "This item", "link": "/" + item_doc.rel})
        ex.append((item_doc.rel, "work item", f"requested item {item_ref}"))
        for s in stages:
            ex.append((f"{item_doc.cid} stage {s['stage']}", "stage document", f"large feature stage ({s['status']})"))
        for j in bundle.of_type("journal"):
            if item_doc.id and str(j.meta.get("about")) == item_doc.id:
                related.append({"label": "Journal (decisions and corrections)", "link": "/" + j.rel})
    modules = []
    for mid in mod_ids:
        m = bundle.resolve(mid)
        if m and not applies_to_line(m.meta, code_line):
            ex.append((m.rel, "module doc skipped", f"does not apply to code line {code_line}"))
        elif m:
            modules.append({"id": m.id, "title": m.title, "body": clean(m.body, limit or 1500)})
            ex.append((m.rel, "module doc", f"named in the item's `modules`"))
        else:
            ex.append((mid, "module doc", "named by the item but NOT FOUND"))
    blocking, other = [], []
    for r in bundle.of_type("rule"):
        if not applies_to_line(r.meta, code_line):
            ex.append((r.rel, "rule skipped", f"does not apply to code line {code_line}"))
            continue
        if r.status == "deprecated" or not applies(r, role, set(mod_ids)):
            ex.append((r.rel, "rule skipped", "deprecated or not applicable to this role or the item's modules"))
            continue
        ex.append((r.rel, "rule included in full" if r.meta.get("severity") == "blocking" else "rule listed (load on demand)",
                   f"severity {r.meta.get('severity')}, applies to this role"))
        entry = {"id": r.id, "title": r.title, "link": "/" + r.rel,
                 "rule": (section_body(r.body, "Rule") or "").replace("\n", " "), "why": (section_body(r.body, "Why") or "").replace("\n", " ")}
        (blocking if r.meta.get("severity") == "blocking" else other).append(entry)
    ts = next(iter(bundle.of_type("tech-stack")), None)
    wf = next(iter(bundle.of_type("workflow")), None)
    stack = "Not documented."
    if ts:
        stack = f"Languages: {', '.join(map(str, as_list(ts.meta.get('languages')))) or 'n/a'}. Frameworks: {', '.join(map(str, as_list(ts.meta.get('frameworks')))) or 'n/a'}."
        conv = section_body(ts.body, "Conventions")
        if conv:
            stack += "\n\n" + clean(conv, 500)
        related.append({"label": "Tech stack", "link": "/" + ts.rel})
        ex.append((ts.rel, "stack summary", "languages, frameworks, conventions excerpt"))
    for t, label in (("architecture", "Architecture"), ("responsibility", "Responsibilities (RACI)"), ("workflow", "Workflow")):
        d = next(iter(bundle.of_type(t)), None)
        if d:
            related.append({"label": label, "link": "/" + d.rel})
    for dec in [d for d in bundle.of_type("decision") if d.status == "accepted" and applies_to_line(d.meta, code_line)][:5]:
        related.append({"label": f"Decision {dec.id}", "link": "/" + dec.rel})
    if wf:
        ex.append((wf.rel, "commands", "workflow `commands` frontmatter"))
    return {"role": role, "role_title": rdef.title, "tools": rdef.profile.get("tools_allowed") or [], "owns": rdef.profile.get("owns") or [], "project": bundle.project_title, "item": item,
            "stack": stack, "commands": (wf.meta.get("commands") if wf and isinstance(wf.meta.get("commands"), dict) else {}),
            "modules": modules, "rules_blocking": blocking, "rules_other": other,
            "role_rules": rdef.text("rules"), "checklist": role_checklists(bundle, rdef),
            "outputs": rdef.text("outputs"), "related": related}


def role_checklists(bundle: Bundle, rdef) -> str:
    from .roles import overlay_dir
    parts = [rdef.text("checklist")]
    for ck in (rdef.profile.get("checklists") or [])[0:]:
        if ck == "checklist.md":
            continue
        for base in (overlay_dir(bundle) / rdef.name, data_dir() / "roles" / rdef.name):
            if (base / ck).exists():
                parts.append((base / ck).read_text().strip())
                break
    return "\n\n".join(x for x in parts if x)


def build_prompt(bundle: Bundle, role: str, item: str | None = None, budget: int | None = None, explain: list | None = None, code_line: str | None = None) -> str:
    rdef = load_role(bundle, role)  # raises LookupError for an unknown role
    tpl_src = rdef.parts.get("prompt", ("", ""))[0]
    if not tpl_src:
        raise ValueError(f"role '{role}' has no prompt template")
    env = jinja_env([])
    tpl = env.from_string(tpl_src)
    out, used = "", None
    for limit in (None, 3000, 1200, 400, 120):
        ex: list = []
        ctx = build_context(bundle, role, item, limit, ex, code_line)
        out, used = tpl.render(**ctx), (limit, ex)
        if not budget or len(out) <= budget:
            break
    if explain is not None:
        explain.append(("prompt template", rdef.parts["prompt"][1], f"role {role} ({rdef.origin})"))
        from .roles import suggested_agent_text
        sat = suggested_agent_text(rdef)
        explain.append(("suggested agent", sat or "none declared", "role profile; vendor-neutral, the adopter maps tiers to real models"))
        explain.extend(used[1])
        explain.append(("size", f"{len(out)} chars", f"body limit {used[0] or 'none'}" + (f", budget {budget}" if budget else "")))
    header = f"<!-- ackit prompt role={role} item={item or '-'} generated={iso(now_utc())} ackit={__version__} -->\n"
    return header + re.sub(r"\n{3,}", "\n\n", out).strip() + "\n"
