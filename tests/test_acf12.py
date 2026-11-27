"""ACF 1.2: points, runs, external_id; plus ackit new --slug, default slug cap, history on create, ackit status, messages."""
import yaml
import pytest

from ackit.bundle import Bundle, split_frontmatter
from ackit.cli import main
from ackit.scaffold import default_slug
from ackit.validate import validate
from conftest import NOW, feature, put

GOAL = "## Goal\n\ng\n\n## Acceptance criteria\n\n- a\n"
SIGN = {"by": "human:a", "at": "2026-11-19"}


def task(root, tid="T-001", **over):
    feature(root)
    meta = {"type": "task", "id": tid, "title": "t", "status": "draft", "feature": "F-001", "description": "d"}
    meta.update(over)
    return put(root, f"work/tasks/{tid}-t.md", meta, GOAL)


def msgs(root, code):
    return [i.message for i in validate(Bundle.load(root), now=NOW) if i.code == code]


def codes(root):
    return {i.code for i in validate(Bundle.load(root), now=NOW)}


# ---- points --------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("v", [1, 2, 3, 5, 8])
def test_points_in_default_scale_ok(good, v):
    task(good, points=v)
    assert "ACF031" not in codes(good)


@pytest.mark.parametrize("v", [4, 0, 13, "3", 2.5, True, [3]])
def test_points_out_of_scale_or_wrong_type(good, v):
    task(good, points=v)
    m = msgs(good, "ACF031")
    assert m and "[1, 2, 3, 5, 8]" in m[0]


def test_points_on_issue_and_scale_from_config(good):
    (good / "ackit.yaml").write_text("points: {scale: [1, 2, 4, 8, 16], auto_start_max: 4, signoff_max: 8}\n")
    put(good, "work/issues/I-001-x.md", {"type": "issue", "id": "I-001", "title": "x", "status": "draft", "severity": "low", "points": 16},
        "## Symptom\n\ns\n\n## Expected\n\ne\n\n## Reproduction\n\nr\n\n## Cause\n\nc\n\n## Fix\n\nf\n")
    assert "ACF031" not in codes(good)
    task(good, points=3)
    assert "ACF031" in codes(good)


def test_bad_points_config_reported_and_defaults_used(good):
    (good / "ackit.yaml").write_text("points: {scale: [3, 1]}\n")
    task(good, points=2)
    assert any("ackit.yaml" in i.path for i in validate(Bundle.load(good), now=NOW) if i.code == "ACF031")


def test_points_above_signoff_max_cannot_be_ready_or_in_progress(good):
    for st in ("ready", "in-progress"):
        task(good, points=8, status=st, signoff=SIGN)
        m = msgs(good, "ACF032")
        assert m and "split" in m[0]
    task(good, points=8, status="draft")
    assert "ACF032" not in codes(good)
    task(good, points=5, status="ready", signoff=SIGN)
    assert "ACF032" not in codes(good)


def test_points_above_auto_start_max_need_signoff_before_ready(good):
    task(good, points=3, status="ready")
    assert "ACF027" in codes(good)
    task(good, points=3, status="ready", signoff=SIGN)
    assert "ACF027" not in codes(good)
    task(good, points=2, status="ready")
    assert "ACF027" not in codes(good)
    task(good, points=3, status="draft")
    assert "ACF027" not in codes(good)


# ---- runs ----------------------------------------------------------------------------------------------------
RUN = {"id": "run-1", "at": "2026-11-19T10:00:00Z", "outcome": "pass"}


def test_runs_valid_with_optional_fields_and_unknown_keys(good):
    task(good, runs=[RUN, {**RUN, "id": "run-2", "tokens": 1200, "turns": 7, "commit": "abc123", "by": "any-agent", "note": "x"}])
    assert "ACF033" not in codes(good)


def test_runs_accepts_yaml_timestamp(good):
    p = task(good)
    p.write_text(p.read_text().replace("generated:", "runs:\n- {id: r1, at: 2026-11-19T10:00:00Z, outcome: pass}\ngenerated:", 1))
    assert "ACF033" not in codes(good)


@pytest.mark.parametrize("bad,frag", [
    ({"at": RUN["at"], "outcome": "x"}, "id"),
    ({"id": "a", "outcome": "x"}, ".at"),
    ({"id": "a", "at": "2026-11-19", "outcome": "x"}, ".at"),
    ({"id": "a", "at": "yesterday", "outcome": "x"}, ".at"),
    ({"id": "a", "at": RUN["at"]}, "outcome"),
    ({**RUN, "tokens": "many"}, "tokens"),
    ({**RUN, "turns": -1}, "turns"),
    ({**RUN, "commit": 5}, "commit"),
    ({**RUN, "by": ["x"]}, "by"),
    ("not a mapping", "mapping"),
])
def test_runs_bad_shape(good, bad, frag):
    task(good, runs=[bad])
    assert any(frag in m for m in msgs(good, "ACF033"))


def test_runs_ids_must_be_unique_and_runs_a_list(good):
    task(good, runs=[RUN, dict(RUN)])
    assert any("unique" in m for m in msgs(good, "ACF033"))
    task(good, runs={"id": "x"})
    assert any("list" in m for m in msgs(good, "ACF033"))


def test_runs_not_checked_on_types_without_it(good):
    feature(good, runs="junk")
    assert "ACF033" not in codes(good)


# ---- external_id ---------------------------------------------------------------------------------------------
def test_external_id_on_feature_task_issue(good):
    feature(good, external_id="PROJ-123")
    task(good, external_id="PROJ-124")
    assert "ACF034" not in codes(good)
    task(good, external_id=["x"])
    assert "ACF034" in codes(good)


# ---- backward compatibility ----------------------------------------------------------------------------------
def test_1_1_bundle_still_validates_unchanged(good):
    (good / "index.md").write_text((good / "index.md").read_text().replace('acf_version: "1.4"', 'acf_version: "1.1"'))
    assert 'acf_version: "1.1"' in (good / "index.md").read_text()
    task(good, status="in-progress", history=["draft", "ready", "in-progress"])
    assert not [i for i in validate(Bundle.load(good), now=NOW) if i.severity == "error"]


def test_okf_roundtrip_keeps_points_runs_external_id(good, tmp_path):
    task(good, points=2, external_id="PROJ-9", runs=[RUN])
    assert main(["export", "--bundle", str(good), "--okf", str(tmp_path / "okf")]) == 0
    assert main(["import", "--okf", str(tmp_path / "okf"), "--dest", str(tmp_path / "back")]) == 0
    meta, _b, _e = split_frontmatter(next((tmp_path / "back").rglob("T-001*.md")).read_text())
    assert meta["points"] == 2 and meta["external_id"] == "PROJ-9" and meta["runs"][0]["id"] == "run-1"


# ---- F1 slug --------------------------------------------------------------------------------------------------
LONG = "Fix the very long title that someone wrote because they like describing everything in the title field"


def test_default_slug_caps_words_and_chars_without_partial_word():
    s = default_slug(LONG)
    assert s == "fix-the-very-long-title-that"
    assert len(s) <= 40 and len(s.split("-")) <= 6 and all(w in LONG.lower().split() for w in s.split("-"))
    assert default_slug("Short title") == "short-title"
    assert len(default_slug("a" * 80)) == 40
    assert default_slug("alpha beta gamma delta epsilon zeta eta theta") == "alpha-beta-gamma-delta-epsilon-zeta"


def test_new_default_slug_and_explicit_slug(good):
    assert main(["new", "--bundle", str(good), "issue", LONG, "--set", "severity=low"]) == 0
    f = next((good / "work/issues").glob("I-*.md"))
    assert len(f.stem) <= len("I-001-") + 40
    assert main(["new", "--bundle", str(good), "issue", LONG, "--slug", "My Slug!", "--set", "severity=low"]) == 0
    assert (good / "work/issues/I-002-my-slug.md").exists()


def test_new_large_feature_slug(good):
    assert main(["new", "--bundle", str(good), "feature", LONG, "--tier", "large", "--slug", "big"]) == 0
    assert (good / "work/features/F-001-big/feature.md").exists()


# ---- F3 history on create ------------------------------------------------------------------------------------
def test_new_work_item_writes_history_but_not_other_types(good):
    assert main(["new", "--bundle", str(good), "task", "A task", "--set", "feature=F-001"]) == 0
    meta, _b, _e = split_frontmatter(next((good / "work/tasks").glob("T-001*.md")).read_text())
    assert meta["history"] == ["draft"]
    assert main(["new", "--bundle", str(good), "issue", "Bug", "--set", "status=ready", "--set", "severity=low"]) == 0
    meta, _b, _e = split_frontmatter(next((good / "work/issues").glob("I-001*.md")).read_text())
    assert meta["history"] == ["ready"]
    assert main(["new", "--bundle", str(good), "reference", "Ref", "--set", "description=d"]) == 0
    meta, _b, _e = split_frontmatter(next((good / "reference").glob("ref*.md")).read_text())
    assert "history" not in meta


# ---- F2 ackit status ------------------------------------------------------------------------------------------
def meta_of(path):
    return split_frontmatter(path.read_text())[0]


def test_status_legal_creates_history_from_current(good, capsys):
    p = task(good, status="draft")
    assert main(["status", "--bundle", str(good), "T-001", "ready"]) == 0
    m = meta_of(p)
    assert m["status"] == "ready" and m["history"] == ["draft", "ready"]
    assert main(["status", "--bundle", str(good), str(p), "in-progress"]) == 0     # by path
    assert meta_of(p)["history"] == ["draft", "ready", "in-progress"]
    assert "## Goal" in p.read_text() and meta_of(p)["generated"]["by"] == "test/1"


def test_status_illegal_refused_with_legal_list_and_file_untouched(good, capsys):
    p = task(good, status="draft")
    before = p.read_text()
    assert main(["status", "--bundle", str(good), "T-001", "done"]) == 1
    err = capsys.readouterr().err
    assert "draft -> done" in err and "ready" in err and "cancelled" in err
    assert p.read_text() == before
    assert main(["status", "--bundle", str(good), "T-001", "bogus"]) == 1
    assert "legal values" in capsys.readouterr().err
    assert main(["status", "--bundle", str(good), "T-999", "ready"]) == 1


def test_status_final_state_and_human_verified_note(good, capsys):
    task(good, status="done", history=["done"])
    assert main(["status", "--bundle", str(good), "T-001", "draft"]) == 1
    assert "none (final status)" in capsys.readouterr().err


# ---- F4 messages ----------------------------------------------------------------------------------------------
def test_illegal_transition_message_lists_legal_next(good):
    feature(good, status="ready", history=["draft", "done", "ready"], signoff=SIGN)
    m = msgs(good, "ACF007")
    assert m and "legal from 'draft'" in m[0] and "ready" in m[0]


def test_disallowed_enum_and_status_messages_list_values(good):
    put(good, "rules/e.md", {"type": "rule", "id": "R-e", "title": "e", "severity": "loud", "status": "bogus"}, "## Rule\n\nx\n\n## Why\n\ny\n\n## How to check\n\nz")
    assert any("blocking" in m for m in msgs(good, "ACF026"))
    assert any("stable" in m for m in msgs(good, "ACF006"))
