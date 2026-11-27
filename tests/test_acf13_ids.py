"""ACF 1.3, T-002 (ADR-0018): `id_allocation` with reserved ranges, `ackit new --author`, ACF037, and proof P2 (two writers)."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

from ackit.bundle import Bundle
from ackit.cli import main
from ackit.idalloc import IdAllocationError, allocate, id_config
from ackit.scaffold import next_id
from ackit.validate import validate
from conftest import NOW, feature, mk, put

RANGES = "id_allocation: {strategy: reserved-range, ranges: {alice: [1000, 1999], bob: [2000, 2002]}}\n"


def ranged(root: Path) -> Path:
    cfg = root / "ackit.yaml"
    cfg.write_text(cfg.read_text() + RANGES)
    return root


def codes(root):
    return [i.code for i in validate(Bundle.load(root), now=NOW)]


def test_sequential_is_unchanged_without_the_key(good):
    assert next_id(Bundle.load(good), "task") == "T-001"
    feature(good)
    assert next_id(Bundle.load(good), "feature") == "F-002"
    assert id_config({}) == ({"strategy": "sequential", "ranges": {}}, [])


def test_range_allocates_inside_and_continues_after_the_highest(good):
    ranged(good)
    assert next_id(Bundle.load(good), "task", "alice") == "T-1000"
    put(good, "work/tasks/T-1000-a.md", {"type": "task", "id": "T-1000", "title": "a", "status": "draft", "feature": "F-001", "description": "d"})
    put(good, "work/tasks/T-005-old.md", {"type": "task", "id": "T-005", "title": "o", "status": "draft", "feature": "F-001", "description": "d"})
    assert next_id(Bundle.load(good), "task", "alice") == "T-1001"      # T-005 is outside the range and ignored
    assert next_id(Bundle.load(good), "task", "bob") == "T-2000"
    assert next_id(Bundle.load(good), "decision", "alice") == "ADR-1000"  # width 4 prefix keeps working


def test_refusals(good):
    ranged(good)
    b = Bundle.load(good)
    with pytest.raises(IdAllocationError, match="--author"):
        next_id(b, "task")
    with pytest.raises(IdAllocationError, match="no range"):
        next_id(b, "task", "carol")
    for n in (2000, 2001, 2002):
        put(good, f"work/tasks/T-{n}-x.md", {"type": "task", "id": f"T-{n}", "title": "x", "status": "draft", "feature": "F-001", "description": "d"})
    with pytest.raises(IdAllocationError, match="full"):
        next_id(Bundle.load(good), "task", "bob")


def test_cli_new_uses_author_flag_and_env(good, capsys, monkeypatch):
    ranged(good)
    assert main(["new", "task", "one", "--bundle", str(good), "--author", "alice", "--set", "feature=F-001"]) == 0
    assert "T-1000" in capsys.readouterr().out
    monkeypatch.setenv("ACKIT_AUTHOR", "bob")
    assert main(["new", "task", "two", "--bundle", str(good), "--set", "feature=F-001"]) == 0
    assert "T-2000" in capsys.readouterr().out
    monkeypatch.delenv("ACKIT_AUTHOR")
    assert main(["new", "task", "three", "--bundle", str(good), "--set", "feature=F-001"]) == 2
    assert "--author" in capsys.readouterr().err


@pytest.mark.parametrize("cfg", [
    "id_allocation: {strategy: random}\n",
    "id_allocation: {strategy: reserved-range}\n",
    "id_allocation: {strategy: reserved-range, ranges: {a: [5, 1]}}\n",
    "id_allocation: {strategy: reserved-range, ranges: {a: [1, 9], b: [9, 20]}}\n",
    "id_allocation: {strategy: reserved-range, ranges: {a: [1, x]}}\n",
    "id_allocation: 3\n",
])
def test_acf037_reports_bad_config(good, cfg):
    (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text() + cfg)
    assert "ACF037" in codes(good)


def test_good_config_is_quiet_and_acf009_unchanged(good):
    ranged(good)
    assert "ACF037" not in codes(good)
    for i in (1, 2):
        put(good, f"work/tasks/T-009-{i}.md", {"type": "task", "id": "T-009", "title": str(i), "status": "draft", "feature": "F-001", "description": "d"})
    assert "ACF009" in codes(good)


def _new(bundle: Path, title: str, author: str | None):
    cmd = [sys.executable, "-m", "ackit", "new", "task", title, "--bundle", str(bundle), "--set", "feature=F-001"]
    if author:
        cmd += ["--author", author]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={**os.environ, "ACKIT_AUTHOR": ""})


def _clone(src: Path, dst: Path) -> Path:
    import shutil
    shutil.copytree(src, dst)
    return dst


def _merge(a: Path, b: Path, into: Path) -> Path:
    """What merging two branches that each added files does: the union of the files."""
    import shutil
    shutil.copytree(a, into)
    for f in b.rglob("*.md"):
        dst = into / f.relative_to(b)
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(f, dst)
    return into


@pytest.mark.parametrize("use_ranges", [True, False])
def test_p2_two_writers_in_parallel(good, tmp_path, use_ranges):
    """Proof P2: two clones each create ten tasks at the same time (each author one after another); after merging (in both orders) ranges give no duplicate id and
    sequential allocation gives duplicates (the clash ADR-0018 exists to prevent)."""
    feature(good)
    if use_ranges:
        (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text()
                                         + "id_allocation: {strategy: reserved-range, ranges: {alice: [1000, 1999], bob: [2000, 2999]}}\n")
    alice, bob = _clone(good, tmp_path / "alice"), _clone(good, tmp_path / "bob")
    results: dict[str, list[int]] = {}

    def writer(name: str, repo: Path):      # one author creates ten items one after another, as a person would
        results[name] = [_new(repo, f"{name} item {i}", name if use_ranges else None).wait(60) for i in range(10)]

    import threading
    threads = [threading.Thread(target=writer, args=("alice", alice)), threading.Thread(target=writer, args=("bob", bob))]
    for t in threads:                       # the two authors run at the same time
        t.start()
    for t in threads:
        t.join()
    assert results == {"alice": [0] * 10, "bob": [0] * 10}
    one, two = _merge(alice, bob, tmp_path / "m1"), _merge(bob, alice, tmp_path / "m2")
    for merged in (one, two):
        dup = [i for i in validate(Bundle.load(merged), now=NOW) if i.code == "ACF009"]
        assert (dup == []) if use_ranges else (dup != [])


# ---- ackit ids assign (ADR-0020) ---------------------------------------------------------------------------------
from ackit.idalloc import assign_range  # noqa: E402


def _cfg(tmp_path, text):
    p = tmp_path / "ackit.yaml"
    p.write_text(text)
    return p


def test_assign_adds_a_block_after_the_highest_and_keeps_comments(tmp_path):
    p = _cfg(tmp_path, "project: x\n# keep me\nid_allocation:\n  strategy: reserved-range\n  ranges:\n    alice: [1000, 1999]\n    bob: [2000, 2499]\nother: 1\n")
    assert assign_range(p, "carol")[:2] == (2500, 3499)
    text = p.read_text()
    assert "# keep me" in text and "other: 1" in text and "    carol: [2500, 3499]\n" in text
    assert text.index("carol") < text.index("other: 1")                      # inserted inside the ranges block
    assert id_config(__import__("yaml").safe_load(text))[1] == []


def test_assign_first_range_and_size_and_flow_style(tmp_path):
    p = _cfg(tmp_path, "project: x\n")
    assert assign_range(p, "alice", 50)[:2] == (1000, 1049)
    assert "strategy: reserved-range" in p.read_text()
    flow = tmp_path / "flow.yaml"
    flow.write_text("id_allocation:\n  strategy: reserved-range\n  ranges: {alice: [1000, 1999]}\n")
    assert assign_range(flow, "bob")[:2] == (2000, 2999)
    assert "bob: [2000, 2999]" in flow.read_text()
    assert id_config(__import__("yaml").safe_load(flow.read_text()))[1] == []


def test_assign_refusals(tmp_path):
    p = _cfg(tmp_path, "id_allocation:\n  strategy: reserved-range\n  ranges:\n    alice: [1000, 1999]\n")
    before = p.read_text()
    for author, size, msg in (("alice", 10, "already has"), ("bad name", 10, "letters"), ("dave", 0, "positive")):
        with pytest.raises(IdAllocationError, match=msg):
            assign_range(p, author, size)
    assert p.read_text() == before                                          # nothing written on a refusal
    bad = _cfg(tmp_path, "id_allocation: {strategy: reserved-range, ranges: {a: [5, 1]}}\n")
    with pytest.raises(IdAllocationError, match="fix"):
        assign_range(bad, "x")


def test_assign_note_when_strategy_is_sequential_and_cli(good, capsys):
    cfg = good / "ackit.yaml"
    cfg.write_text(cfg.read_text() + "id_allocation:\n  ranges:\n    alice: [1000, 1999]\n")
    assert main(["ids", "assign", "carol", "--bundle", str(good)]) == 0
    captured = capsys.readouterr()
    assert "carol: [2000, 2999]" in captured.out and "sequential" in captured.err and "merge" in captured.err
    assert main(["ids", "assign", "carol", "--bundle", str(good)]) == 2          # second time: already has a range
    assert "already has" in capsys.readouterr().err
    assert "ACF037" not in codes(good)


# --- T-002 review fixes -----------------------------------------------------------------------------------------------
def test_bad_config_refuses_allocation(good):
    for bad in ("id_allocation: {strategy: nonsense}\n", "id_allocation: 5\n",
                "id_allocation: {strategy: reserved-range, ranges: {a: [1, 10], b: [5, 20]}}\n"):
        (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text() + bad)
        with pytest.raises(IdAllocationError, match="not usable"):
            next_id(Bundle.load(good), "task", "a")
        (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text().replace(bad, ""))


def test_assign_edits_only_the_id_allocation_block(tmp_path):
    from ackit.idalloc import assign_range
    cfg = tmp_path / "ackit.yaml"
    cfg.write_text("other:\n  ranges:\n    x: 1\nid_allocation:\n  strategy: reserved-range\n  ranges: {alice: [1000, 1999]}  # c\n")
    low, high, _ = assign_range(cfg, "bob")
    assert (low, high) == (2000, 2999)
    text = cfg.read_text()
    assert "    x: 1\n" in text and "bob: [2000, 2999]} # c".replace("} #", "}  #") in text


def test_assign_empty_flow_crlf_and_ambiguous_author(tmp_path):
    from ackit.idalloc import assign_range
    cfg = tmp_path / "ackit.yaml"
    cfg.write_bytes(b"id_allocation:\r\n  strategy: reserved-range\r\n  ranges: {}\r\n")
    assert assign_range(cfg, "alice")[:2] == (1000, 1999)
    raw = cfg.read_bytes()
    assert b"\r\n" in raw and b"\n" not in raw.replace(b"\r\n", b"")
    with pytest.raises(IdAllocationError, match="boolean"):
        assign_range(cfg, "yes")
    with pytest.raises(IdAllocationError, match="not found"):
        assign_range(tmp_path / "missing.yaml", "bob")


def test_two_clones_assigning_a_range_pick_the_same_block_and_acf037_reports_it(good, tmp_path):
    """Two branches that each run `ids assign` for a different author on the same base pick the same block: the merge conflicts or ACF037 reports it."""
    import shutil
    a, b = tmp_path / "a", tmp_path / "b"
    shutil.copytree(good, a)
    shutil.copytree(good, b)
    assert main(["ids", "assign", "alice", "--bundle", str(a)]) == 0
    assert main(["ids", "assign", "bob", "--bundle", str(b)]) == 0
    ra = id_config(__import__("yaml").safe_load((a / "ackit.yaml").read_text()))[0]["ranges"]["alice"]
    rb = id_config(__import__("yaml").safe_load((b / "ackit.yaml").read_text()))[0]["ranges"]["bob"]
    assert ra == rb                                   # the same block, because neither saw the other's line
    merged = a / "ackit.yaml"
    merged.write_text(merged.read_text().replace("ranges:\n", f"ranges:\n    bob: [{rb[0]}, {rb[1]}]\n", 1))   # what both lines in one file look like
    assert any("overlap" in m for m in id_config(__import__("yaml").safe_load(merged.read_text()))[1])


def test_reattesting_an_accepted_document_keeps_one_history_entry(good):
    """`ackit verify --status accepted` on a document already accepted adds the signature, not a second `accepted` to the history."""
    from ackit.scaffold import verify_doc
    p = put(good, "decisions/ADR-0099-x.md", {"type": "decision", "id": "ADR-0099", "title": "x", "status": "accepted", "history": ["proposed", "accepted"]})
    verify_doc(p, "human:owner", "accepted")
    verify_doc(p, "human:owner", "accepted")
    meta = Bundle.load(good).by_id("ADR-0099").meta
    assert meta["history"] == ["proposed", "accepted"] and len(meta["verified"]) == 2
