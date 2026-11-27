"""Role definitions: kit built-ins (data/roles), bundle overlay (roles/), custom roles, profiles (role.yaml)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import jinja2
import yaml

from .bundle import Bundle, data_dir, split_frontmatter

KINDS = ["prompt", "rules", "checklist", "outputs", "prompt-guide", "wrap-up"]
OPTIONAL_KINDS = {"wrap-up"}  # recognised, never required: the text an orchestrator sends when a run is stopped at its budget
GATES = {"start", "handoff"}
CAPABILITIES = ["high", "standard", "fast"]
REASONING = ["deep", "normal"]
SUGGESTED_KEYS = {"capability", "reasoning", "independent_of"}
CHECK_RE = re.compile(r"^- \[[ xX]\] \*\*[A-Za-z]+-\d+\*\*", re.M)


@dataclass
class Role:
    name: str
    profile: dict
    parts: dict[str, tuple[str, str]] = field(default_factory=dict)  # kind -> (text, origin)
    origin: str = "kit"  # kit | overlay (built-in overridden) | custom
    problems: list[str] = field(default_factory=list)

    @property
    def title(self) -> str:
        return self.profile.get("title") or self.name.title()

    def text(self, kind: str) -> str:
        return self.parts[kind][0] if kind in self.parts else ""


def kit_roles() -> list[str]:
    return sorted(d.name for d in (data_dir() / "roles").iterdir() if (d / "role.yaml").exists())


def overlay_dir(bundle: Bundle) -> Path:
    return bundle.root / "roles"


def overlay_roles(bundle: Bundle) -> list[str]:
    o = overlay_dir(bundle)
    return sorted(d.name for d in o.iterdir() if d.is_dir()) if o.is_dir() else []


def all_role_names(bundle: Bundle) -> list[str]:
    return sorted(set(kit_roles()) | set(overlay_roles(bundle)))


def overlay_path(bundle: Bundle, name: str) -> Path:
    """Where this bundle keeps the overlay of role `name` (`<bundle>/roles/<name>`); it may not exist yet."""
    return overlay_dir(bundle) / name


def _read(path: Path) -> str:
    text = path.read_text()
    meta, body, err = split_frontmatter(text)
    return (body if meta is not None and not err else text).strip()


def _find(base: Path, kind: str) -> Path | None:
    names = [f"{kind}.md.j2", f"{kind}.md"] if kind == "prompt" else [f"{kind}.md"]
    return next((base / n for n in names if (base / n).exists()), None)


def load_role(bundle: Bundle, name: str, _seen: tuple = ()) -> Role:
    if name in _seen:
        raise ValueError(f"role extends cycle: {' -> '.join(_seen + (name,))}")
    kit, ov = data_dir() / "roles" / name, overlay_dir(bundle) / name
    kit_exists, ov_exists = (kit / "role.yaml").exists(), ov.is_dir()
    if not kit_exists and not ov_exists:
        raise LookupError(f"unknown role '{name}'; known: {all_role_names(bundle)}")
    profile: dict = {}
    for base in (kit, ov):
        f = base / "role.yaml"
        if f.exists():
            profile.update(yaml.safe_load(f.read_text()) or {})
    role = Role(name, profile, origin="overlay" if kit_exists and ov_exists else ("kit" if kit_exists else "custom"))
    parent = None
    if profile.get("extends"):
        parent = load_role(bundle, profile["extends"], _seen + (name,))
    for kind in KINDS:
        for base, label in ((ov, "overlay"), (kit, "kit")):
            f = _find(base, kind) if base.is_dir() else None
            if f:
                role.parts[kind] = (_read(f) if kind != "prompt" else f.read_text(), f"{label}: {f.relative_to(base.parent.parent) if label == 'overlay' else f.name}")
                break
        else:
            if parent and kind in parent.parts:
                role.parts[kind] = (parent.parts[kind][0], f"extends {parent.name}: {parent.parts[kind][1]}")
    return role


def validate_role(bundle: Bundle, role: Role) -> list[str]:
    """Return problems; empty means the definition is complete."""
    reg_types = set(bundle.registry["types"])
    p, out = role.profile, []
    for k in ("name", "description", "owns", "gates"):
        if k not in p:
            out.append(f"role.yaml lacks `{k}`")
    if p.get("name") not in (None, role.name):
        out.append(f"role.yaml name '{p.get('name')}' does not match directory '{role.name}'")
    for t in p.get("owns") or []:
        if t not in reg_types:
            out.append(f"owns unknown doc type '{t}'")
    for g in p.get("gates") or []:
        if g not in GATES:
            out.append(f"unknown gate '{g}' (allowed {sorted(GATES)})")
    out += validate_suggested_agent(bundle, role)
    for kind in ("prompt", "rules", "checklist", "outputs"):
        if kind not in role.parts or not role.parts[kind][0].strip():
            out.append(f"missing {kind}")
    for ck in p.get("checklists") or ["checklist.md"]:
        txt = role.text("checklist") if ck == "checklist.md" else ""
        if ck != "checklist.md":
            src = overlay_dir(bundle) / role.name / ck
            alt = data_dir() / "roles" / role.name / ck
            f = src if src.exists() else alt if alt.exists() else None
            if not f:
                out.append(f"checklists names missing file {ck}")
                continue
            txt = f.read_text()
        if not CHECK_RE.search(txt):
            out.append(f"{ck} has no `- [ ] **ID-NN** ...` items")
    if "wrap-up" in role.parts and not role.parts["wrap-up"][0].strip():
        out.append("wrap-up is empty (delete the file, or say what the agent does when it is stopped at its budget)")
    if "prompt" in role.parts:
        try:
            from .scaffold import jinja_env
            jinja_env([]).from_string(role.parts["prompt"][0])
        except jinja2.TemplateSyntaxError as e:
            out.append(f"prompt template syntax error: {e}")
    return out


def suggested_agent_text(role: Role) -> str:
    sa = role.profile.get("suggested_agent")
    if not isinstance(sa, dict):
        return ""
    t = f"capability {sa.get('capability', '-')}, reasoning {sa.get('reasoning', 'normal')}"
    return t + (f", independent of {sa['independent_of']}" if sa.get("independent_of") else "")


def validate_suggested_agent(bundle: Bundle, role: Role) -> list[str]:
    """Optional, vendor-neutral: capability tier, reasoning level, independence. No vendor or model names."""
    if "suggested_agent" not in role.profile:
        return []
    sa, out = role.profile["suggested_agent"], []
    if not isinstance(sa, dict):
        return ["suggested_agent must be a mapping {capability, reasoning, independent_of}"]
    for k in sa:
        if k not in SUGGESTED_KEYS:
            out.append(f"suggested_agent has unknown key '{k}' (allowed {sorted(SUGGESTED_KEYS)}); vendor and model names belong in the adopter's mapping, not here")
    if sa.get("capability") not in CAPABILITIES:
        out.append(f"suggested_agent.capability must be one of {CAPABILITIES}")
    if "reasoning" in sa and sa["reasoning"] not in REASONING:
        out.append(f"suggested_agent.reasoning must be one of {REASONING}")
    ind = sa.get("independent_of")
    if ind is not None:
        if ind == role.name:
            out.append("suggested_agent.independent_of cannot be the role itself")
        elif ind not in all_role_names(bundle):
            out.append(f"suggested_agent.independent_of names unknown role '{ind}'")
    return out


def scaffold_role(bundle_root: Path, name: str, title: str | None = None, description: str | None = None,
                  extends: str | None = None) -> list[Path]:
    from .scaffold import jinja_env
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        raise ValueError("role name must be lowercase letters, digits and dashes")
    dest = bundle_root / "roles" / name
    if dest.exists():
        raise FileExistsError(str(dest))
    dest.mkdir(parents=True)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(data_dir() / "role-template")), keep_trailing_newline=True)
    ctx = {"name": name, "title": title or name.replace("-", " ").title(), "description": description or f"Describe what the {name} role does.",
           "prefix": re.sub(r"[^A-Z]", "", name.upper())[:3] or "RL", "extends": extends}
    out = []
    for f in ("role.yaml", "prompt.md", "rules.md", "checklist.md", "outputs.md", "prompt-guide.md"):
        (dest / f).write_text(env.get_template(f).render(**ctx))
        out.append(dest / f)
    return out
