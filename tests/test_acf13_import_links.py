"""Import keeps relative links working when a file moves (found on a migrated copy of a real store: 1153 link warnings before, 142 after)."""
from ackit.bundle import Bundle
from ackit.importer import import_store, rewrite_links
from ackit.validate import validate

MAPPING = {"project": "p", "rules": [
    {"match": "features/*/*.md", "type": "reference", "dest": "reference/features/{parent}-{stem}.md", "set": {"description": "d"}},
    {"match": "rules/*.md", "type": "rule", "dest": "rules/{stem}.md", "id": "R-{stem}", "set": {"severity": "advisory"}}],
    "default": {"type": "reference", "dest": "reference/{stem}.md", "set": {"description": "d"}}}


def test_rewrite_follows_a_moved_file_and_leaves_the_rest():
    moved = {"features/a/02.md": "reference/features/a-02.md", "rules/r.md": "rules/r.md"}
    body = "[x](02.md#top) [r](../../rules/r.md) [out](../../../elsewhere.md) [web](https://e.org/x.md) [anchor](#h)"
    new, n = rewrite_links(body, "features/a/01.md", "reference/features/a-01.md", moved)
    assert n == 2 and "(a-02.md#top)" in new and "(../../rules/r.md)" in new
    assert "(../../../elsewhere.md)" in new and "(https://e.org/x.md)" in new and "(#h)" in new


def test_import_leaves_no_broken_link_between_imported_files(tmp_path):
    src = tmp_path / "src"
    (src / "features/a").mkdir(parents=True)
    (src / "rules").mkdir()
    (src / "AGENTS.md").write_text("# Entry\n\nSee [r](rules/r.md).\n")
    (src / "rules/r.md").write_text("# R\n\n## Rule\n\nx\n\n## Why\n\ny\n")
    (src / "features/a/01.md").write_text("# One\n\nNext: [two](02.md), rule: [r](../../rules/r.md)\n")
    (src / "features/a/02.md").write_text("# Two\n\nBack: [one](01.md)\n")
    rep = import_store(src, MAPPING, tmp_path / "bundle")
    assert rep["links_rewritten"] >= 3
    assert not [i for i in validate(Bundle.load(tmp_path / "bundle")) if i.code == "ACF008"]
