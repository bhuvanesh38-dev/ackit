"""Gates an orchestrator (or a person) calls before starting and before handing off a work item."""
from __future__ import annotations

from dataclasses import dataclass, field

from .bundle import Bundle, Doc, as_list, section_body
from .validate import validate


@dataclass
class Check:
    name: str
    level: str  # pass | warn | fail
    detail: str


@dataclass
class GateResult:
    gate: str
    item: str
    checks: list[Check] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not any(c.level == "fail" for c in self.checks)

    def as_dict(self) -> dict:
        return {"gate": self.gate, "item": self.item, "passed": self.passed,
                "checks": [c.__dict__ for c in self.checks]}


def related_paths(b: Bundle, item: Doc) -> set[str]:
    paths = {item.rel, "AGENTS.md", "index.md"}
    for k in ("modules", "depends_on", "feature", "epic"):
        for r in as_list(item.meta.get(k)):
            d = b.resolve(str(r))
            if d:
                paths.add(d.rel)
    for d in b.docs:
        if d.type == "feature-stage" and str(d.meta.get("feature")) == item.id:
            paths.add(d.rel)
        if d.type in ("test-evidence", "review", "handoff", "journal") and item.id in {str(d.meta.get("item")), str(d.meta.get("about"))}:
            paths.add(d.rel)
        if d.type == "rule":
            paths.add(d.rel)
    return paths


def check_gate(b: Bundle, gate: str, item_ref: str, role: str | None = None, now=None) -> GateResult:
    res = GateResult(gate, item_ref)
    add = lambda n, lvl, d: res.checks.append(Check(n, lvl, d))
    item = b.resolve(item_ref)
    if not item:
        add("item-exists", "fail", f"no work item '{item_ref}' in the bundle")
        return res
    add("item-exists", "pass", item.rel)
    if role:
        from .roles import load_role
        try:
            rd = load_role(b, role)
            add("role-participates", "pass" if gate in (rd.profile.get("gates") or []) else "warn",
                f"role {role} gates: {rd.profile.get('gates') or []}")
        except LookupError as e:
            add("role-known", "fail", str(e))
    spec = b.type_spec(item.type) or {}
    if spec.get("status_set") != "work":
        add("item-is-work", "fail", f"type {item.type} is not a work item")
        return res
    issues = [i for i in validate(b, now=now, only=related_paths(b, item)) if i.severity == "error"]
    add("scoped-validation", "fail" if issues else "pass",
        "; ".join(f"{i.code} {i.path}" for i in issues[:5]) if issues else "no errors in the item, its stages, modules and rules")
    if gate == "start":
        ok_status = {"ready", "in-progress"} | ({"draft"} if role == "planner" else set())
        add("status", "pass" if item.status in ok_status else "fail", f"status is '{item.status}', need one of {sorted(ok_status)}")
        ac = section_body(item.body, "Acceptance criteria")
        if item.type in ("task", "issue", "feature") and not (item.meta.get("tier") == "large" and item.type == "feature"):
            if item.type != "issue":
                add("acceptance-criteria", "pass" if ac else "fail", "present" if ac else "Acceptance criteria section missing or empty")
        deps = [(r, b.resolve(str(r))) for r in as_list(item.meta.get("depends_on"))]
        bad = [str(r) for r, d in deps if not d or d.status != "done"]
        add("dependencies-done", "fail" if bad else "pass", f"not done: {bad}" if bad else "all dependencies done")
        mods = [str(m) for m in as_list(item.meta.get("modules"))]
        miss = [m for m in mods if not b.resolve(m)]
        add("modules-resolve", "fail" if miss else "pass", f"unknown modules {miss}" if miss else (f"{len(mods)} module(s)" if mods else "no modules named"))
        unver = [r.id for r in b.of_type("rule") if r.meta.get("severity") == "blocking" and r.status != "stable"]
        add("blocking-rules-verified", "warn" if unver else "pass", f"draft blocking rules (not human-verified): {unver}" if unver else "all blocking rules are stable")
    elif gate == "handoff":
        add("status", "pass" if item.status in ("in-progress", "in-review") else "fail", f"status is '{item.status}', need in-progress or in-review")
        ev = [e for e in b.of_type("test-evidence") if item.id in as_list(e.meta.get("item"))]
        good = [e for e in ev if e.meta.get("result") == "pass"]
        add("test-evidence", "pass" if good else "fail", f"{len(good)} passing record(s)" if good else ("evidence exists but none passes" if ev else "no test-evidence record with item: " + str(item.id)))
        ss = [s for s in b.of_type("session") if str(s.meta.get("item")) == item.id or item.id in s.body]
        add("session-entry", "pass" if ss else "fail", f"{len(ss)} session log(s) mention it" if ss else "no session entry mentions the item")
        jr = [j for j in b.of_type("journal") if str(j.meta.get("about")) == item.id]
        add("journal", "pass" if jr else ("fail" if item.type == "feature" else "warn"), "journal present" if jr else "no journal for this item")
        rv = [r for r in b.of_type("review") if item.id in as_list(r.meta.get("item"))]
        blocked = [r.rel for r in rv if r.meta.get("verdict") == "blocked"]
        if blocked:
            add("review", "fail", f"blocked review: {blocked}")
        else:
            add("review", "pass" if rv else "warn", f"{len(rv)} review record(s)" if rv else "no review record yet (needed before done)")
        sec = [r for r in rv if r.meta.get("role") == "security"]
        add("security-review", "pass" if sec else "warn", "security review present" if sec else "none (needed when the change touches auth, input or data)")
    else:
        add("gate", "fail", f"unknown gate '{gate}'")
    return res
