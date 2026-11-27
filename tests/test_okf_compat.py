import re
from pathlib import Path

import pytest

from ackit.bundle import Bundle, load_registry, split_frontmatter
from ackit.cli import main, types_markdown
from ackit.okf import export_okf, import_okf
from ackit.scaffold import dump_doc
from ackit.validate import validate

ROOT = Path(__file__).parent.parent


def concepts(root: Path) -> dict:
    b = Bundle.load(root)
    return {d.rel: (d.meta, d.body.strip()) for d in b.docs}


@pytest.mark.parametrize("ex", ["small", "large"])
def test_export_import_round_trip(tmp_path, ex):
    src = ROOT / "examples" / ex / "context"
    out, back = tmp_path / "okf", tmp_path / "back"
    assert main(["export", "--bundle", str(src), "--okf", str(out)]) == 0
    assert main(["import", "--okf", str(out), "--dest", str(back)]) == 0
    assert concepts(back) == concepts(src)
    assert (back / "ackit.yaml").read_text() == (src / "ackit.yaml").read_text()
    assert [i for i in validate(Bundle.load(back)) if i.severity == "error"] == []


def test_export_is_okf_shaped(tmp_path):
    src = ROOT / "examples" / "large" / "context"
    export_okf(src, tmp_path / "okf")
    idx, _b, _e = split_frontmatter((tmp_path / "okf/index.md").read_text())
    assert idx["okf_version"] == "0.2"
    for p in (tmp_path / "okf").rglob("*.md"):
        if p.name in ("index.md", "log.md"):
            continue
        m, _b, err = split_frontmatter(p.read_text())
        assert not err and m["type"]                                  # OKF conformance: parseable frontmatter, type
        assert "review_by" not in m and m.get("status") in (None, "draft", "stable", "deprecated")
    rule = next((tmp_path / "okf/rules").glob("*.md"))
    m, _b, _e = split_frontmatter(rule.read_text())
    assert "stale_after" in m and m["acf_status"] == "draft"


def test_roles_overlay_round_trips(tmp_path):
    import shutil
    src = tmp_path / "src"
    shutil.copytree(ROOT / "examples/small/context", src)
    (src / "roles/developer").mkdir(parents=True)
    (src / "roles/developer/rules.md").write_text("1. custom\n")
    export_okf(src, tmp_path / "okf")
    assert (tmp_path / "okf/.acf/roles/developer/rules.md").exists()
    import_okf(tmp_path / "okf", tmp_path / "back")
    assert (tmp_path / "back/roles/developer/rules.md").read_text() == "1. custom\n"


def test_okf_v02_sample_imports_and_validates(tmp_path):
    okf = tmp_path / "okf"
    (okf / "tables").mkdir(parents=True)
    (okf / "concepts").mkdir()
    (okf / "index.md").write_text('---\nokf_version: "0.2"\n---\n# Index\n\n## Tables\n\n- [orders](/tables/orders.md) - order facts\n')
    (okf / "log.md").write_text("# Log\n\n## 2026-02-01\n\n- **Creation** added orders\n")
    (okf / "tables/orders.md").write_text(dump_doc({
        "type": "bigquery-table", "title": "orders", "description": "order facts", "resource": "bq://p.d.orders", "tags": ["sales"],
        "status": "stable", "stale_after": "2099-01-01T00:00:00Z", "generated": {"by": "tool/1.2", "at": "2026-01-01T00:00:00Z"},
        "verified": [{"by": "human:amy", "at": "2026-01-02T00:00:00Z"}], "custom_key": 7,
        "sources": [{"id": "s1", "resource": "https://example.org/spec", "title": "spec"}]}, "# Schema\n\nSee [revenue](/concepts/revenue.md).\n"))
    (okf / "concepts/revenue.md").write_text("---\ntype: metric\n---\nno title, no generated\n")
    (okf / "concepts/untyped.md").write_text("---\ntitle: nope\n---\nx\n")
    dest = tmp_path / "acf"
    assert main(["import", "--okf", str(okf), "--dest", str(dest)]) == 0
    b = Bundle.load(dest)
    t = next(d for d in b.docs if d.rel == "tables/orders.md")
    assert t.meta["review_by"] == "2099-01-01T00:00:00Z" and "stale_after" not in t.meta
    assert t.meta["sources"][0]["ref"] == "https://example.org/spec"
    assert t.meta["custom_key"] == 7 and t.meta["resource"] == "bq://p.d.orders" and t.meta["verified"][0]["by"] == "human:amy"
    r = next(d for d in b.docs if d.rel == "concepts/revenue.md")
    assert r.meta["title"] == "revenue" and r.meta["generated"]["by"].startswith("ackit-okf-import")
    assert not (dest / "concepts/untyped.md").exists()
    idx, _b, _e = split_frontmatter((dest / "index.md").read_text())
    assert idx["acf_version"] == "1.4" and "okf_version" not in idx
    assert (dest / "AGENTS.md").exists()
    issues = validate(b)
    assert [i for i in issues if i.severity == "error"] == []
    assert main(["validate", str(dest)]) == 0


def test_import_okf_refuses_nonempty_dest(tmp_path):
    (tmp_path / "d").mkdir(); (tmp_path / "d/x").write_text("1")
    assert main(["import", "--okf", str(ROOT / "examples/small/context"), "--dest", str(tmp_path / "d")]) == 2


# ---- the orchestrator contract: `ackit types --markdown` shape and CLI calls ------------------------------------
def parse_types_markdown(text):
    out = {}
    for block in re.split(r"(?m)^## `", text)[1:]:
        name = block.split("`", 1)[0]
        req = re.search(r"- Required frontmatter: (.*)", block)
        st = re.search(r"- Statuses: (.*)", block)
        out[name] = {"required": re.findall(r"`([^`]+)`", req.group(1)) if req else [],
                     "statuses": re.findall(r"[a-z][a-z-]*", st.group(1).split("(")[0]) if st else []}
    return out


def test_types_markdown_contract():
    kit = parse_types_markdown(types_markdown(load_registry()))
    expect = {"session": ["author"], "session-index": ["author"], "test-evidence": ["item", "result"], "review": ["item", "role", "verdict"],
              "handoff": ["item"], "journal": ["about"], "task": ["id", "status", "feature"], "feature": ["id", "status", "tier"]}
    for t, fields in expect.items():
        assert set(fields) <= set(kit[t]["required"]), t
    assert {"draft", "ready", "in-progress", "in-review", "blocked"} <= set(kit["task"]["statuses"])


def test_version_and_index_version(tmp_path):
    import ackit
    assert ackit.__version__ == "1.4.0" and ackit.ACF_VERSION == "1.4"
