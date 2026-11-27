import datetime as dt
import shutil

import pytest

from ackit.bundle import Bundle
from ackit.cli import main
from ackit.scaffold import verify_doc
from ackit.validate import validate, exit_code, RULE_TEXT
from conftest import NOW, feature, put, load


def codes(root, **kw):
    return {i.code for i in validate(Bundle.load(root), now=kw.get("now", NOW))}


def errs(root):
    return [i for i in validate(Bundle.load(root), now=NOW) if i.severity == "error"]


def test_good_bundle_clean(good):
    assert errs(good) == [] and main(["validate", str(good)]) == 0


def sev(root, code):
    return [i.severity for i in validate(Bundle.load(root), now=NOW) if i.code == code]


# one crafted-bad case per rule ------------------------------------------------
def c001(r): (r / "bad.md").write_text("---\ntype: [unclosed\n---\nx")
def c002(r): (r / "x.md").write_text("---\ntitle: no type\n---\nx")
def c003(r): put(r, "x.md", {"type": "mystery", "title": "x"})
def c004(r): put(r, "rules/r.md", {"type": "rule", "id": "R-r", "title": "r"}, "## Rule\n\nx\n\n## Why\n\ny\n\n## How to check\n\nz")
def c005(r):
    p = r / "rules/blast-radius.md"; p.write_text(p.read_text().replace("## Why", "## Because"))
def c006(r): put(r, "rules/r.md", {"type": "rule", "id": "R-r", "title": "r", "severity": "blocking", "status": "bogus"}, "## Rule\n\nx\n\n## Why\n\ny\n\n## How to check\n\nz")
def c007(r): feature(r, status="ready", history=["draft", "done", "ready"], signoff={"by": "human:a", "at": "2026-01-01"})
def c008(r): (r / "product.md").write_text((r / "product.md").read_text() + "\nsee [x](/nope.md)\n")
def c009(r): feature(r); put(r, "work/features/F-001-dup.md", {"type": "feature", "id": "F-001", "title": "d", "status": "draft", "tier": "small"}, feature_b())
def c010(r): put(r, "reference/old.md", {"type": "reference", "title": "o", "description": "d", "review_by": "2026-01-01T00:00:00Z"})
def c011(r): put(r, "rules/r.md", {"type": "rule", "id": "R-r", "title": "r", "severity": "blocking", "status": "stable"}, "## Rule\n\nx\n\n## Why\n\ny\n\n## How to check\n\nz")
def c012(r): feature(r, status="done", signoff={"by": "human:a", "at": "2026-01-01"})
def c013(r): (r / "AGENTS.md").write_text((r / "AGENTS.md").read_text() + "\nline\n" * 200)
def c014(r): (r / "index.md").write_text("# Index\n")
def c015(r): (r / "log.md").write_text("# Log\n\n## 2026-01-01\n\n- a\n\n## 2026-02-01\n\n- b\n")
def c016(r): put(r, "work/features/F-1-x.md", {"type": "feature", "id": "F-1", "title": "x", "status": "draft", "tier": "small"}, feature_b())
def c017(r):
    feature(r, tier="large", status="draft")
    put(r, "work/features/F-001-t/03-plan.md", {"type": "feature-stage", "title": "p", "feature": "F-001", "stage": "plan", "status": "signed-off", "signoff": {"by": "human:a", "at": "2026"}}, "## Steps\n\ns\n\n## Risks\n\nr")
def c018(r): feature(r, epic="E-999")
def c019(r):
    put(r, "decisions/ADR-0002-b.md", {"type": "decision", "id": "ADR-0002", "title": "b", "status": "proposed", "date": "2026-01-01", "supersedes": "ADR-0001"}, "## Context\n\nc\n\n## Options\n\n1. a\n2. b\n\n## Decision\n\nd\n\n## Why\n\nw\n\n## Consequences\n\nc")
def c020(r): (r / "journals/project.md").write_text((r / "journals/project.md").read_text() + "\n## whenever\n\nx\n")
def c021(r): put(r, "sessions/a/b.md", {"type": "session", "title": "s", "author": "a"}, "## 2026-11-17 - b @ s - t\n\n**Done:** x\n")
def c022(r): put(r, "elsewhere/r.md", {"type": "rule", "id": "R-q", "title": "q", "severity": "advisory"}, "## Rule\n\nx\n\n## Why\n\ny\n\n## How to check\n\nz")
def c023(r): (r / "reference").mkdir(); (r / "reference/n.md").write_text("---\ntype: reference\ntitle: n\ndescription: d\n---\nbody")
def c024(r): put(r, "reference/unlisted.md", {"type": "reference", "title": "u", "description": "d"}); (r / "index.md").write_text('---\nokf_version: "0.2"\n---\n# I\n')
def c025(r): put(r, "rules/e.md", {"type": "rule", "id": "R-e", "title": "e", "severity": "advisory", "status": "stable", "verified": [{"by": "human:a", "at": "2026"}]}, "## Rule\n\n## Why\n\ny\n\n## How to check\n\nz")
def c026(r): put(r, "rules/e.md", {"type": "rule", "id": "R-e", "title": "e", "severity": "loud"}, "## Rule\n\nx\n\n## Why\n\ny\n\n## How to check\n\nz")
def c027(r): feature(r, status="ready")
def c028(r): (r / "AGENTS.md").unlink()
def c029(r): (r / "workflow.md").write_text((r / "workflow.md").read_text().replace("commands:", "commands:\n  extra: x\nold:", 1).replace("  build:", "  zzz:", 1) if False else "---\ntype: workflow\ntitle: w\ncommands: {build: b}\nstatus: draft\ngenerated: {by: t, at: x}\n---\n## Commands\n\nc\n\n## Branching and review\n\nb\n\n## Definition of done\n\nd\n")
def c030(r): (r / "roles/half").mkdir(parents=True); (r / "roles/half/rules.md").write_text("1. x")
def _task(r, **over):
    meta = {"type": "task", "id": "T-001", "title": "t", "status": "draft", "feature": "F-001", "description": "d"}
    meta.update(over)
    feature(r)
    return put(r, "work/tasks/T-001-t.md", meta, "## Goal\n\ng\n\n## Acceptance criteria\n\n- a\n")
def c031(r): _task(r, points=4)
def c032(r): _task(r, points=8, status="ready", signoff={"by": "human:a", "at": "2026-01-01"})
def c033(r): _task(r, runs=[{"id": "r1", "at": "2026-11-19T10:00:00Z"}])
def c034(r): _task(r, external_id="")
def c037(r): (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "id_allocation: {strategy: reserved-range, ranges: {a: [1, 9], b: [5, 20]}}\n")
def c038(r): (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "environment_registry: {source_file: nowhere.yaml}\n")
def c039(r): (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "branch_policy: {context_branch: {base: nonsense}}\n")
def c035(r): put(r, "rules/r-lines.md", {"type": "rule", "title": "r", "status": "draft", "severity": "advisory", "code_lines": [3]}, "## Rule\n\nx\n\n## Why\n\ny\n")
def c036(r):
    (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "author_workspace: {root: 'people/{author}'}\n")
    put(r, "people/alice/n.md", {"type": "rule", "title": "n", "status": "draft", "severity": "advisory", "author": "bob"}, "## Rule\n\nx\n\n## Why\n\ny\n")
def c040(r): (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "author_workspace: {root: 'nope'}\n")
def c041(r): (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "process_checks: [{name: x, level: loud, when: pre-push, run: [true]}]\n")
def c042(r): (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "consumer_layout: {entry_links: [../x]}\n")
def c043(r):
    (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "vocabularies: {vendor: {values: [vendor-a]}}\n")
    put(r, "tr.md", {"type": "ticket-resolution", "title": "t", "description": "d", "resolution_type": 3, "tickets": ["T-1"], "vendors": ["vendor-b"]}, "## Quick summary\n\nx")
def c044(r): (r / "ackit.yaml").write_text((r / "ackit.yaml").read_text() + "vocabularies: {vendor: {source_file: nope.yaml, key_path: a}}\n")
def c045(r): put(r, "sessions/a/b.md", {"type": "session", "title": "s", "author": "a"}, "## 2026-11-17 - b @ s - t\n\n**Done:** x\n")
def feature_b():
    from conftest import feature_body
    return feature_body()


CASES = {"ACF001": c001, "ACF002": c002, "ACF003": c003, "ACF004": c004, "ACF005": c005, "ACF006": c006, "ACF007": c007, "ACF008": c008,
         "ACF009": c009, "ACF010": c010, "ACF011": c011, "ACF012": c012, "ACF013": c013, "ACF014": c014, "ACF015": c015, "ACF016": c016,
         "ACF017": c017, "ACF018": c018, "ACF019": c019, "ACF020": c020, "ACF021": c021, "ACF022": c022, "ACF023": c023, "ACF024": c024,
         "ACF025": c025, "ACF026": c026, "ACF027": c027, "ACF028": c028, "ACF029": c029, "ACF030": c030,
         "ACF031": c031, "ACF032": c032, "ACF033": c033, "ACF034": c034, "ACF035": c035, "ACF036": c036, "ACF037": c037, "ACF038": c038, "ACF039": c039, "ACF040": c040, "ACF041": c041, "ACF042": c042, "ACF043": c043, "ACF044": c044, "ACF045": c045}


def test_every_rule_has_a_case():
    assert set(CASES) == set(RULE_TEXT)


@pytest.mark.parametrize("code", sorted(CASES))
def test_rule_fires(good, code):
    CASES[code](good)
    assert code in codes(good), f"{code} did not fire"


def test_exit_codes_and_strict(good):
    c008(good)
    assert main(["validate", str(good)]) == 0           # link warning only
    assert main(["validate", str(good), "--strict"]) == 1
    c028(good)
    assert main(["validate", str(good)]) == 1           # error
    assert main(["validate", "/nonexistent-dir-xyz"]) == 2


def test_severity_config_can_turn_rule_off_or_to_error(good):
    c008(good)
    (good / "ackit.yaml").write_text("links: error\n")
    assert main(["validate", str(good)]) == 1
    (good / "ackit.yaml").write_text("severity: {ACF008: off}\nlinks: off\n")
    assert main(["validate", str(good), "--strict"]) == 0


def test_stale_boundary(good):
    put(good, "reference/r.md", {"type": "reference", "title": "r", "description": "d", "review_by": "2026-11-17T00:00:00Z"})
    assert "ACF010" in codes(good, now=NOW)
    assert "ACF010" not in codes(good, now=NOW - dt.timedelta(days=1))


def test_trust_gate_passes_when_human_verified(good):
    c011(good)
    verify_doc(good / "rules/r.md", "human:alice")
    assert "ACF011" not in codes(good)


def test_verify_to_signed_off_writes_signoff(good):
    put(good, "work/features/F-001-x/01-analysis.md", {"type": "feature-stage", "title": "a", "feature": "F-001", "stage": "analysis", "status": "draft"}, "## Problem\n\np")
    path = good / "work/features/F-001-x/01-analysis.md"
    verify_doc(path, "human:alice", "signed-off")
    from ackit.scaffold import split_frontmatter
    meta = split_frontmatter(path.read_text())[0]
    assert meta["signoff"]["by"] == "human:alice" and meta["signoff"]["at"] == meta["verified"][0]["at"]
    verify_doc(path, "human:bob", "signed-off")            # a second attestation does not rewrite the first sign-off
    assert split_frontmatter(path.read_text())[0]["signoff"]["by"] == "human:alice"


def test_verify_signoff_is_human_only_and_clears_acf027(good):
    from ackit.scaffold import split_frontmatter
    put(good, "work/tasks/T-001-x.md", {"type": "task", "id": "T-001", "title": "t", "status": "in-progress", "feature": "F-001", "points": 3,
                                        "history": ["draft", "ready", "in-progress"]}, "## Goal\n\ng\n\n## Acceptance criteria\n\n- a\n")
    path = good / "work/tasks/T-001-x.md"
    assert "ACF027" in codes(good)                              # 3 points is above the auto-start limit
    with pytest.raises(ValueError):
        verify_doc(path, "agent:x", signoff=True)
    with pytest.raises(ValueError):
        verify_doc(path, "human:", signoff=True)                # an empty id is not a person
    with pytest.raises(ValueError):
        verify_doc(path, "agent:x", "signed-off")            # the status route is a person's act too
    assert "signoff" not in split_frontmatter(path.read_text())[0]
    verify_doc(path, "human:alice", signoff=True)
    verify_doc(path, "human:bob", signoff=True)               # never overwritten
    assert split_frontmatter(path.read_text())[0]["signoff"]["by"] == "human:alice"
    assert split_frontmatter(path.read_text())[0]["signoff"]["by"] == "human:alice"
    assert "ACF027" not in codes(good)


def test_done_feature_with_all_records_passes(good):
    feature(good, status="done", signoff={"by": "human:a", "at": "2026"})
    put(good, "evidence/e.md", {"type": "test-evidence", "title": "e", "item": "F-001", "result": "pass"}, "## Commands\n\n`x`\n\n## Results\n\nok\n\n## Coverage\n\nc")
    put(good, "reviews/r.md", {"type": "review", "title": "r", "item": "F-001", "role": "reviewer", "verdict": "approve"}, "## Scope\n\ns\n\n## Findings\n\nnone\n\n## Resolution\n\nn\n\n## Verdict\n\napprove")
    put(good, "journals/f.md", {"type": "journal", "title": "j", "about": "F-001"}, "# j\n\n## 2026-11-17 - decision: x\n\nd")
    assert "ACF012" not in codes(good)


def test_large_feature_stage_flow(good):
    assert main(["new", "--bundle", str(good), "feature", "Big", "--tier", "large"]) == 0
    folder = next((good / "work/features").iterdir())
    assert sorted(p.name for p in folder.iterdir())[0] == "01-analysis.md" or (folder / "feature.md").exists()
    assert errs(good) == []
