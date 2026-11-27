"""F-004 / T-018: the three support types (ticket-resolution, issue-pattern, platform-behaviour) in the core registry."""
import pytest

from ackit.bundle import Bundle, load_registry
from ackit.cli import main
from ackit.validate import validate
from conftest import NOW, put

TYPES = {
    "ticket-resolution": (["title", "description", "resolution_type", "tickets"],
                          ["Quick summary", "Symptom", "Diagnosis", "Root cause", "Resolution", "Verification", "Follow-up"]),
    "issue-pattern": (["title", "description"], ["Problem", "Signals", "Cause", "Resolution", "Related resolutions"]),
    "platform-behaviour": (["title", "description"], ["Behaviour", "Applies to", "Evidence"]),
}
META = {"ticket-resolution": {"resolution_type": 3, "tickets": ["ZD-1001"]}}


def body(sections):
    return "\n\n".join(f"## {s}\n\ntext for {s}" for s in sections)


def page(root, rel, t, drop_key=None, drop_section=None, **over):
    keys, sections = TYPES[t]
    meta = {"type": t, "title": f"a {t}", "description": "d", "status": "draft", **META.get(t, {}), **over}
    meta.pop(drop_key, None)
    return put(root, rel, meta, body([s for s in sections if s != drop_section]))


def found(root, path_part, *codes):
    return [i for i in validate(Bundle.load(root), now=NOW) if path_part in i.path and (not codes or i.code in codes)]


@pytest.mark.parametrize("t", sorted(TYPES))
def test_the_type_is_declared_as_designed(t):
    spec = load_registry()["types"][t]
    assert spec["required"] == TYPES[t][0] and spec["sections"] == TYPES[t][1]
    assert spec["status_set"] == "doc" and spec["dir"] == ""
    assert set(spec["owner"]) >= {"writes", "reviews", "signs_off", "updates"} and spec["rules"]
    assert load_registry()["status_sets"]["doc"]["human_verified"] == ["stable"]          # a page is trusted at stable only after `ackit verify`


@pytest.mark.parametrize("t", sorted(TYPES))
def test_a_complete_page_has_no_error_and_each_missing_key_or_section_is_reported(good, t):
    keys, sections = TYPES[t]
    page(good, f"x/{t}.md", t)
    assert [i for i in found(good, f"x/{t}.md") if i.severity == "error"] == []
    assert found(good, f"x/{t}.md", "ACF004", "ACF005") == []
    for k in keys:
        p = page(good, f"x/{t}-nokey.md", t, drop_key=k)
        assert [i for i in found(good, f"x/{t}-nokey.md", "ACF004") if f"`{k}`" in i.message], (t, k)
        p.unlink()
    for sec in sections:
        p = page(good, f"x/{t}-nosec.md", t, drop_section=sec)
        assert [i for i in found(good, f"x/{t}-nosec.md", "ACF005") if f"'{sec}'" in i.message], (t, sec)
        p.unlink()


@pytest.mark.parametrize("t", sorted(TYPES))
def test_human_verification_at_stable(good, t):
    page(good, f"x/{t}-s.md", t, status="stable")
    assert found(good, f"x/{t}-s.md", "ACF011"), "a stable page needs a human verifier"
    page(good, f"x/{t}-v.md", t, status="stable", verified=[{"by": "human:a", "at": "2026-11-17T00:00:00Z"}])
    assert found(good, f"x/{t}-v.md", "ACF011") == []


def test_acf022_still_fires_for_a_typed_page_outside_its_directory(good):
    put(good, "x/rb.md", {"type": "runbook", "id": "RB-a", "title": "r", "status": "draft"}, "## Purpose\n\np\n")
    assert found(good, "x/rb.md", "ACF022")                              # the control: the casebook types pass only because they declare no directory


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5, 6])
def test_resolution_type_accepts_one_to_six(good, value):
    page(good, "x/r.md", "ticket-resolution", resolution_type=value)
    assert found(good, "x/r.md", "ACF026") == []


@pytest.mark.parametrize("value", [0, 7, "1", "data fix", None, 1.0, 2.0, True, [1]])
def test_resolution_type_outside_one_to_six_is_acf026(good, value):
    page(good, "x/r.md", "ticket-resolution", resolution_type=value)
    assert found(good, "x/r.md", "ACF026"), value


@pytest.mark.parametrize("t", sorted(TYPES))
@pytest.mark.parametrize("rel", ["support/a.md", "prod/tenant-a/support/a.md", "uat/tenant-b/support/deep/er/a.md", "a.md"])
def test_no_directory_warning_for_the_casebook_layout(good, rel, t):
    page(good, rel, t)
    assert found(good, rel, "ACF022") == []


@pytest.mark.parametrize("t", sorted(TYPES))
def test_ackit_new_creates_the_type_with_its_sections(good, t, capsys):
    args = ["new", t, "A new page", "--bundle", str(good)] + (["--set", "resolution_type=5", "--set", "tickets=[ZD-7]"] if t == "ticket-resolution" else [])
    assert main(args) == 0
    created = [p for p in good.rglob("*.md") if "a-new-page" in p.name]
    assert len(created) == 1, capsys.readouterr().out
    text = created[0].read_text()
    for sec in TYPES[t][1]:
        assert f"## {sec}" in text, (t, sec)
    assert f"type: {t}" in text
    assert found(good, created[0].name, "ACF003") == []                      # the type is known
    if t == "ticket-resolution":
        assert "resolution_type: 5" in text


def test_a_new_ticket_resolution_without_a_chosen_type_is_not_silently_a_data_fix(good):
    assert main(["new", "ticket-resolution", "Unclassified", "--bundle", str(good), "--set", "tickets=[ZD-9]"]) == 0
    text = next(p for p in good.rglob("*.md") if "unclassified" in p.name).read_text()
    assert "resolution_type: 1" not in text
    assert found(good, "unclassified", "ACF004"), "the missing classification must be reported"


def test_ackit_new_refuses_to_overwrite(good):
    args = ["new", "issue-pattern", "Same title", "--bundle", str(good)]
    assert main(args) == 0 and main(args) == 2


def test_doc_types_reference_is_the_generated_one(capsys):
    from pathlib import Path
    main(["types", "--markdown"])
    generated = capsys.readouterr().out.split("\n", 1)[1].strip()          # without its title line
    on_disk = (Path(__file__).parent.parent / "docs/DOC-TYPES.md").read_text()
    assert generated in on_disk, "docs/DOC-TYPES.md is stale: regenerate it from `ackit types --markdown`"
