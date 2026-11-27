"""ACF 1.3, T-009 (ADR-0019): `consumer_layout`, `ackit link --check`, ACF042."""
import json
import os

import pytest
import yaml

from ackit.cli import main
from ackit.layout import config


def setup(root, layout):
    cfg = root / "ackit.yaml"
    cfg.write_text(cfg.read_text() + yaml.safe_dump({"consumer_layout": layout}))
    (root / "rules").mkdir(exist_ok=True)


LAYOUT = {"entry": "AGENTS.md", "entry_links": ["AGENTS.md", ".claude/CLAUDE.md"], "rules_dir": "rules", "rules_links": [".claude/rulebook"]}


def states(capsys):
    return {l["path"]: l["state"] for l in json.loads(capsys.readouterr().out)}


def test_absent_block_checks_nothing(good, tmp_path, capsys):
    assert config({}) == ({"entry": "AGENTS.md", "entry_links": [], "rules_dir": None, "rules_links": []}, [])
    assert main(["link", "--check", "--bundle", str(good), "--target", str(tmp_path), "--json"]) == 0
    assert states(capsys) == {}


def test_ok_missing_wrong_and_nothing_is_created(good, tmp_path, capsys):
    setup(good, LAYOUT)
    clone = tmp_path / "clone"
    (clone / ".claude").mkdir(parents=True)
    os.symlink(good / "AGENTS.md", clone / "AGENTS.md")                      # ok
    (clone / ".claude/CLAUDE.md").write_text("a plain file")                  # wrong: not a link
    os.symlink(tmp_path, clone / ".claude/rulebook")                          # wrong: points elsewhere
    before = sorted(p.name for p in clone.rglob("*"))
    assert main(["link", "--check", "--bundle", str(good), "--target", str(clone), "--json"]) == 1
    got = states(capsys)
    assert got == {"AGENTS.md": "ok", ".claude/CLAUDE.md": "wrong", ".claude/rulebook": "wrong"}
    assert sorted(p.name for p in clone.rglob("*")) == before                 # nothing created or changed
    empty = tmp_path / "empty"
    empty.mkdir()
    assert main(["link", "--check", "--bundle", str(good), "--target", str(empty), "--json"]) == 1
    assert set(states(capsys).values()) == {"missing"} and not list(empty.iterdir())


def test_all_ok_exits_zero(good, tmp_path, capsys):
    setup(good, LAYOUT)
    clone = tmp_path / "c"
    (clone / ".claude").mkdir(parents=True)
    os.symlink(good / "AGENTS.md", clone / "AGENTS.md")
    os.symlink(good / "AGENTS.md", clone / ".claude/CLAUDE.md")
    os.symlink(good / "rules", clone / ".claude/rulebook")
    assert main(["link", "--check", "--bundle", str(good), "--target", str(clone)]) == 0
    assert "ok" in capsys.readouterr().out


def test_missing_source_in_the_bundle_is_reported(good, tmp_path, capsys):
    setup(good, {**LAYOUT, "rules_dir": "no-such-rules"})
    main(["link", "--check", "--bundle", str(good), "--target", str(tmp_path), "--json"])
    assert states(capsys)[".claude/rulebook"] == "missing"


@pytest.mark.parametrize("bad", [
    "x", {"nope": 1}, {"entry": "/abs"}, {"entry": "../x"}, {"entry_links": "a"}, {"entry_links": ["a/../b"]}, {"rules_links": ["x"]},
    {"rules_dir": "a\\b"}, {"entry_links": [""]}])
def test_bad_layout_is_reported(good, tmp_path, bad):
    assert config({"consumer_layout": bad})[1], bad
    setup(good, bad)
    assert main(["link", "--check", "--bundle", str(good), "--target", str(tmp_path)]) == 2


def test_no_links_configured_means_no_source_check(good, tmp_path, capsys):
    (good / "AGENTS.md").unlink()
    assert main(["link", "--check", "--bundle", str(good), "--target", str(tmp_path), "--json"]) == 0
    assert states(capsys) == {}
    setup(good, {"rules_dir": "rules", "rules_links": [".claude/rulebook"]})
    main(["link", "--check", "--bundle", str(good), "--target", str(tmp_path), "--json"])
    assert states(capsys) == {".claude/rulebook": "missing"}                  # the missing entry is not checked: no entry link is configured


def test_dangling_relative_and_chained_links(good, tmp_path, capsys):
    setup(good, {"entry_links": ["dangling.md", "rel.md", "chain.md"]})
    clone = tmp_path / "c"
    clone.mkdir()
    os.symlink(tmp_path / "nope", clone / "dangling.md")
    os.symlink(os.path.relpath(good / "AGENTS.md", clone), clone / "rel.md")
    os.symlink(clone / "rel.md", clone / "chain.md")
    main(["link", "--check", "--bundle", str(good), "--target", str(clone), "--json"])
    assert states(capsys) == {"dangling.md": "wrong", "rel.md": "ok", "chain.md": "ok"}


def test_missing_source_lists_every_link_and_loops_do_not_crash(good, tmp_path, capsys):
    setup(good, {"rules_dir": "nope", "rules_links": ["a", "b"]})
    main(["link", "--check", "--bundle", str(good), "--target", str(tmp_path), "--json"])
    assert states(capsys) == {"a": "missing", "b": "missing"}
    clone = tmp_path / "loop"
    clone.mkdir()
    os.symlink(clone / "x", clone / "y")
    os.symlink(clone / "y", clone / "x")
    (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text().split("consumer_layout")[0])
    setup(good, {"entry_links": ["x"]})
    assert main(["link", "--check", "--bundle", str(good), "--target", str(clone)]) == 1


def test_errors_exit_two(good, tmp_path):
    setup(good, {"entry_links": ["a"]})
    assert main(["link", "--check", "--bundle", str(good), "--target", str(good)]) == 2          # target is the bundle
    assert main(["link", "--check", "--bundle", str(tmp_path / "missing"), "--target", str(tmp_path)]) == 2


@pytest.mark.parametrize("bad", [{"entry_links": ["a", "a"]}, {"entry_links": [".claude", ".claude/CLAUDE.md"]}])
def test_duplicate_and_nested_links_are_refused(bad):
    assert config({"consumer_layout": bad})[1]
