"""Guard for F-002: a bundle that uses none of the ACF 1.3 keys must validate exactly as it did under ACF 1.2.

The expected findings live in tests/baselines/acf12.json, recorded from the 1.2.1 code before any F-002 change. Run with
ACKIT_UPDATE_BASELINE=1 only to re-record on purpose (a change to the old behaviour is a spec change, not a test fix).
An optional extra bundle (for example a real project's) is compared with the same rules when ACKIT_GUARD_EXTRA points at it
and the file tests/baselines/extra.json exists; otherwise that case is skipped.
"""
import json
import os
from pathlib import Path

import pytest

from ackit.bundle import Bundle
from ackit.init import init_bundle
from ackit.validate import validate
from conftest import NOW, feature, mk, put

ROOT = Path(__file__).parent.parent
BASELINES = Path(__file__).parent / "baselines"
REPOS = {
    "init-java": {"build.gradle": "plugins { id 'org.springframework.boot' }\n", "settings.gradle": "include 'core', 'web'\n",
                  "core/build.gradle": "", "web/build.gradle": ""},
    "init-node": {"package.json": '{"name":"x","workspaces":["packages/*"],"dependencies":{"react":"18"}}',
                  "packages/ui/package.json": "{}", "packages/api/package.json": "{}"},
    "init-python": {"pyproject.toml": "[project]\nname='x'\n", "src/x/__init__.py": ""},
    "init-go": {"go.mod": "module x\n", "main.go": "package main\n"},
    "init-plain": {"README.txt": "hi\n"},
}


def findings(bundle_dir: Path) -> list[list[str]]:
    return [[i.code, i.severity, i.path, i.message] for i in validate(Bundle.load(bundle_dir), now=NOW)]


def current(tmp_path: Path) -> dict[str, list[list[str]]]:
    out = {name: findings(ROOT / "examples" / name / "context") for name in ("small", "large")}
    for name, files in REPOS.items():
        repo = mk(tmp_path / name, files)
        init_bundle(repo, repo / "context", answers={"owner": "alice", "purpose": "Demo"}, now=NOW)
        out[name] = findings(repo / "context")
    out["broken"] = findings(broken_bundle(tmp_path / "broken"))
    out["acf12-fields"] = findings(fields_bundle(tmp_path / "fields"))
    out["severity-override"] = findings(severity_bundle(tmp_path / "severity"))
    return out


def fields_bundle(repo: Path) -> Path:
    """ACF 1.2 fields in use: valid points, runs and external_id, plus defects in each, so those rules stay pinned."""
    mk(repo, REPOS["init-python"])
    init_bundle(repo, repo / "context", answers={"owner": "alice", "purpose": "Demo"}, now=NOW)
    root = repo / "context"
    feature(root)
    body = "## Goal\n\ng\n\n## Acceptance criteria\n\n- a\n"
    run = {"id": "r1", "at": "2026-11-18T09:00:00Z", "outcome": "pass", "tokens": 1200, "turns": 4, "commit": "abc1234", "by": "agent"}
    put(root, "work/tasks/T-001-ok.md", {"type": "task", "id": "T-001", "title": "ok", "status": "draft", "feature": "F-001", "description": "d",
                                         "points": 2, "external_id": "EXT-1", "runs": [run]}, body)
    put(root, "work/tasks/T-002-bad.md", {"type": "task", "id": "T-002", "title": "bad", "status": "ready", "feature": "F-001", "description": "d",
                                          "points": 8, "external_id": "", "runs": [run, {**run}, {"id": "r3", "at": "2026-11-18"}]}, body)
    return root


def severity_bundle(repo: Path) -> Path:
    """A `severity:` mapping in ackit.yaml that raises one rule, switches another off and leaves a third at its default."""
    root = broken_bundle(repo)
    cfg = root / "ackit.yaml"
    cfg.write_text(cfg.read_text() + "severity: {ACF008: error, ACF024: off, ACF031: warn}\n")
    return root


def broken_bundle(repo: Path) -> Path:
    """An old-style bundle with known defects, so the wording and paths of today's findings are pinned too."""
    mk(repo, REPOS["init-python"])
    init_bundle(repo, repo / "context", answers={"owner": "alice", "purpose": "Demo"}, now=NOW)
    root = repo / "context"
    body = "## Goal\n\ng\n\n## Acceptance criteria\n\n- a\n"
    put(root, "work/tasks/T-001-a.md", {"type": "task", "id": "T-001", "title": "a", "status": "weird", "feature": "F-009"}, body)
    put(root, "work/tasks/T-002-b.md", {"type": "task", "id": "T-001", "title": "b", "status": "draft", "feature": "F-009", "points": 4}, body)
    put(root, "work/tasks/T-003-c.md", {"type": "task", "id": "T-003", "title": "c", "status": "draft", "feature": "F-009"}, "## Goal\n\n[x](/nope.md)\n")
    return root


def compare(expected: dict, actual: dict) -> list[str]:
    """Human-readable differences between the recorded and the current findings (empty list: identical)."""
    diffs = []
    for name in sorted(set(expected) | set(actual)):
        exp, act = expected.get(name), actual.get(name)
        if exp != act:
            gone = [f for f in (exp or []) if f not in (act or [])]
            new = [f for f in (act or []) if f not in (exp or [])]
            diffs.append(f"{name}: {len(gone)} finding(s) gone, {len(new)} new; first new: {new[:1]} first gone: {gone[:1]}")
    return diffs


def test_old_bundles_validate_as_under_acf12(tmp_path):
    actual = current(tmp_path)
    path = BASELINES / "acf12.json"
    if os.environ.get("ACKIT_UPDATE_BASELINE"):
        BASELINES.mkdir(exist_ok=True)
        path.write_text(json.dumps(actual, indent=1, sort_keys=True) + "\n")
    expected = json.loads(path.read_text())
    assert compare(expected, actual) == []


def test_guard_fails_when_a_real_rule_changes(tmp_path, monkeypatch):
    """Negative control through the real validator: an extra finding, a changed message, a changed severity and a dropped
    finding must each make the guard differ on every bundle (not only on hand-edited dictionaries)."""
    from ackit import validate as v
    expected = json.loads((BASELINES / "acf12.json").read_text())
    original = v.Validator.run

    def mutate(kind):
        def run(self, only=None):
            issues = original(self, only)
            if kind == "extra":
                issues.append(v.Issue("ACF999", "warn", "AGENTS.md", "injected"))
            elif kind == "message" and issues:
                issues[0] = v.Issue(issues[0].code, issues[0].severity, issues[0].path, issues[0].message + " (reworded)")
            elif kind == "severity" and issues:
                issues[0] = v.Issue(issues[0].code, "error" if issues[0].severity != "error" else "warn", issues[0].path, issues[0].message)
            elif kind == "drop" and issues:
                issues = issues[1:]
            return issues
        return run

    for kind in ("extra", "message", "severity", "drop"):
        monkeypatch.setattr(v.Validator, "run", mutate(kind))
        differing = compare(expected, current(tmp_path / kind))
        monkeypatch.setattr(v.Validator, "run", original)
        # bundles with no finding at all cannot show a message, severity or drop change; the bundles with findings must
        with_findings = {n for n, f in expected.items() if f}
        needed = set(expected) if kind == "extra" else with_findings
        assert {d.split(":")[0] for d in differing} >= needed, (kind, differing)


def test_extra_bundle_matches_its_baseline():
    extra, base = os.environ.get("ACKIT_GUARD_EXTRA"), BASELINES / "extra.json"
    if not extra or not base.exists():
        pytest.skip("no extra bundle configured")
    assert compare(json.loads(base.read_text()), {"extra": findings(Path(extra))}) == []
