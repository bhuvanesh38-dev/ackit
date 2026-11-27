"""ACF 1.3, T-007 (ADR-0019): `author_workspace`, ACF036, ACF040."""
import pytest

from ackit.bundle import Bundle
from ackit.scaffold import build_index
from ackit.validate import validate
from ackit.workspace import config, folder_author, hidden_from_index
from conftest import NOW, put

BODY = "## Rule\n\nx\n\n## Why\n\ny\n"


def doc(root, rel, **extra):
    put(root, rel, {"type": "rule", "title": rel, "status": "draft", "severity": "advisory", **extra}, BODY)


def enable(root, extra=""):
    cfg = root / "ackit.yaml"
    cfg.write_text(cfg.read_text() + "author_workspace: {root: 'developers/{author}'" + extra + "}\n")


def codes(root):
    return [(i.code, i.path) for i in validate(Bundle.load(root), now=NOW)]


def test_absent_block_changes_nothing(good):
    assert config({}) == ({"root": None, "in_index": False}, [])
    doc(good, "developers/alice/a.md")
    assert not any(c == "ACF036" for c, _ in codes(good))


def test_folder_author_matches_whole_path_parts():
    cfg, _ = config({"author_workspace": {"root": "developers/{author}"}})
    assert folder_author("developers/alice/x/y.md", cfg) == "alice"
    assert folder_author("developers/x.md", cfg) is None
    assert folder_author("other/alice/x.md", cfg) is None
    cfg2, _ = config({"author_workspace": {"root": "a/{author}/ws"}})
    assert folder_author("a/bob/ws/z.md", cfg2) == "bob" and folder_author("a/bob/zz/z.md", cfg2) is None


def test_author_must_equal_the_folder(good):
    enable(good)
    doc(good, "developers/alice/ok.md", author="alice")
    doc(good, "developers/alice/wrong.md", author="bob")
    doc(good, "developers/alice/none.md")
    found = [p for c, p in codes(good) if c == "ACF036"]
    assert sorted(found) == ["developers/alice/none.md", "developers/alice/wrong.md"]
    assert all(i.severity == "warn" for i in validate(Bundle.load(good), now=NOW) if i.code == "ACF036")


def test_workspace_documents_stay_out_of_the_index_but_other_rules_apply(good):
    enable(good)
    doc(good, "developers/alice/a.md", author="alice", severity="nonsense")
    doc(good, "shared.md")
    idx = build_index(Bundle.load(good))
    assert "shared.md" in idx and "developers/alice/a.md" not in idx
    got = codes(good)
    assert ("ACF024", "developers/alice/a.md") not in got
    assert any(c == "ACF026" and p == "developers/alice/a.md" for c, p in got)          # other rules still fire


def test_in_index_true_keeps_them_in(good):
    enable(good, ", in_index: true")
    doc(good, "developers/alice/a.md", author="alice")
    assert "developers/alice/a.md" in build_index(Bundle.load(good))
    cfg, _ = config({"author_workspace": {"root": "d/{author}", "in_index": True}})
    assert not hidden_from_index("d/x/y.md", cfg)


@pytest.mark.parametrize("block", [
    {"root": "developers"}, {"root": "/abs/{author}"}, {"root": "../{author}"}, {"root": "a/{author}/{author}"}, {"root": "a/x{author}"},
    {"root": 5}, {"root": ""}, {"root": "a/{author}", "in_index": "no"}, {"surprise": 1}])
def test_bad_config_is_reported(block):
    assert config({"author_workspace": block})[1], block
    assert config({"author_workspace": "x"})[1]


def test_journal_format_rule_applies_inside_a_workspace(good):
    enable(good)
    put(good, "developers/alice/j.md", {"type": "journal", "title": "j", "status": "draft", "about": "F-001", "author": "alice"},
        "## 2026-11-01\n\nolder first\n\n## 2026-11-05\n\nnewer last\n")
    assert any(c == "ACF020" and p == "developers/alice/j.md" for c, p in codes(good))


def test_untyped_or_unparsable_documents_get_no_acf036(good):
    enable(good)
    (good / "developers" / "alice").mkdir(parents=True)
    (good / "developers/alice/plain.md").write_text("# just notes\n")
    (good / "developers/alice/broken.md").write_text("---\ntype: [\n---\nx\n")
    got = codes(good)
    assert not any(c == "ACF036" for c, _ in got) and any(c in ("ACF001", "ACF002") for c, _ in got)


def test_author_must_be_a_string_equal_to_the_folder(good):
    enable(good)
    doc(good, "developers/1/a.md", author=1)
    doc(good, "developers/alice/b.md", author=["alice"])
    assert sorted(p for c, p in codes(good) if c == "ACF036") == ["developers/1/a.md", "developers/alice/b.md"]


@pytest.mark.parametrize("root", ["{author}", "./{author}", "a\\b/{author}", "a/./{author}"])
def test_roots_that_never_match_or_hide_everything_are_refused(root):
    assert config({"author_workspace": {"root": root}})[1], root


def test_non_mapping_config_does_not_crash():
    assert config(["x"]) == ({"root": None, "in_index": False}, [])
