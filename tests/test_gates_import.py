from pathlib import Path

import pytest
import yaml

from ackit.bundle import Bundle
from ackit.cli import main
from ackit.gates import check_gate
from ackit.importer import import_store
from ackit.validate import validate
from conftest import NOW, feature, put



def checks(good, gate, item="F-001", **kw):
    r = check_gate(Bundle.load(good), gate, item, now=NOW, **kw)
    return {c.name: c.level for c in r.checks}, r.passed


def test_start_gate_blocks_draft_then_passes(good):
    feature(good)
    c, ok = checks(good, "start")
    assert not ok and c["status"] == "fail"
    feature(good, status="ready", signoff={"by": "human:a", "at": "2026-01-01"})
    c, ok = checks(good, "start")
    assert ok and c["acceptance-criteria"] == "pass" and c["scoped-validation"] == "pass"
    assert c["blocking-rules-verified"] == "warn"      # fresh rules are draft


def test_start_gate_dependencies_and_unknown_item(good):
    feature(good, "F-001", status="ready", signoff={"by": "human:a", "at": "x"}, depends_on=["F-002"])
    assert not checks(good, "start")[1]
    assert not check_gate(Bundle.load(good), "start", "F-404").passed
    assert main(["check", "--bundle", str(good), "--gate", "start", "--item", "F-404"]) == 1


def test_planner_may_start_a_draft(good):
    feature(good)
    assert checks(good, "start", role="planner")[1]


def test_handoff_gate(good):
    feature(good, status="in-progress", signoff={"by": "human:a", "at": "x"})
    c, ok = checks(good, "handoff")
    assert not ok and c["test-evidence"] == "fail" and c["session-entry"] == "fail"
    put(good, "evidence/e.md", {"type": "test-evidence", "title": "e", "item": "F-001", "result": "pass"}, "## Commands\n\n`x`\n\n## Results\n\nok\n\n## Coverage\n\nc")
    put(good, "sessions/a/b.md", {"type": "session", "title": "s", "author": "a", "item": "F-001"},
        "## 2026-11-17 - b @ s - t\n\n**Done:** x\n\n**Faced:** x\n\n**Decisions:** x\n\n**Build:** x\n\n**Next:** x\n\n**Blockers:** none\n")
    put(good, "journals/j.md", {"type": "journal", "title": "j", "about": "F-001"}, "# j\n\n## 2026-11-17 - decision: x\n\nd")
    c, ok = checks(good, "handoff")
    assert ok, c
    assert main(["check", "--bundle", str(good), "--gate", "handoff", "--item", "F-001", "--json"]) == 0


def test_import_generic_store(tmp_path):
    src = tmp_path / "store"
    (src / "rules").mkdir(parents=True)
    (src / "adr").mkdir()
    (src / "AGENTS.md").write_text("# Agents\n\nsmall entry\n")
    (src / "rules/no-eval.md").write_text("---\nid: legacy-7\nstatus: active\nowner: team\n---\n# No eval\n\nNever eval input.\n")
    (src / "adr/use-queue.md").write_text("# Use a queue\n\nbody\n")
    (src / "notes.md").write_text("# Notes\n")
    (src / "drafts").mkdir()
    (src / "drafts/x.md").write_text("# skipped\n")
    before = {p: p.read_text() for p in src.rglob("*.md")}
    mapping = yaml.safe_load((Path(__file__).parent.parent / "adopters/example/mapping.yaml").read_text())
    dest = tmp_path / "bundle"
    dry = import_store(src, mapping, dest, dry_run=True, now=NOW)
    assert not dest.exists() and len(dry["files"]) == 4
    rep = import_store(src, mapping, dest, now=NOW)
    b = Bundle.load(dest)
    rule = next(d for d in b.docs if d.type == "rule")
    assert rule.id == "R-no-eval" and rule.status == "draft"
    assert rule.meta["source_id"] == "legacy-7" and rule.meta["owner"] == "team" and rule.meta["source_status"] == "active"
    assert rule.meta["sources"][0]["ref"] == "rules/no-eval.md"
    assert "## Why" in rule.body                                     # missing required sections get stubs
    assert not (dest / "reference/x.md").exists()                    # skip list honoured
    assert {p: p.read_text() for p in src.rglob("*.md")} == before   # source untouched
    assert rep["validation"]["errors"] == 0 or rep["stubs"] > 0
    assert main(["validate", str(dest)]) in (0, 1)
