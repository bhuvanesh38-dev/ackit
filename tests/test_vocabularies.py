"""F-004 / T-019: controlled vocabularies (module, vendor, tenant) for ticket-resolution fields; rules ACF043 and ACF044."""
import pytest

from ackit.bundle import Bundle
from ackit.validate import validate
from conftest import NOW, put

BASE = {"type": "ticket-resolution", "title": "t", "description": "d", "resolution_type": 3, "tickets": ["ZD-1"]}
BODY = "\n\n".join(f"## {s}\n\nx" for s in ["Quick summary", "Symptom", "Diagnosis", "Root cause", "Resolution", "Verification", "Follow-up"])


def config(good, text):
    (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text() + text)


def tr(good, rel="tr.md", **over):
    return put(good, rel, {**BASE, **over}, BODY)


def codes(good, path_part="", *wanted):
    return [i for i in validate(Bundle.load(good), now=NOW) if i.code in (wanted or ("ACF043", "ACF044")) and path_part in i.path]


def msgs(good, path_part="tr.md"):
    return [i.message for i in codes(good, path_part, "ACF043")]


def test_no_vocabularies_block_checks_nothing(good):
    tr(good, vendors=["whoever"], tenants=["anything"], module="M-x")
    assert codes(good) == []


def test_a_list_vocabulary_accepts_registered_and_refuses_the_rest_with_a_hint(good):
    config(good, "vocabularies:\n  vendor: {values: [vendor-a, vendor-b]}\n")
    tr(good, vendors=["vendor-a", "vendor-b"])
    assert codes(good) == []
    tr(good, "tr2.md", vendors=["vendor-a", "vendr-b"])
    m = msgs(good, "tr2.md")
    assert len(m) == 1 and "vendr-b" in m[0] and "did you mean `vendor-b`" in m[0]


def test_a_single_string_value_and_a_wrong_type_value(good):
    config(good, "vocabularies:\n  module: {values: [m-loan]}\n")
    tr(good, module="m-loan")
    assert codes(good) == []
    tr(good, "tr2.md", module="m-other")
    assert msgs(good, "tr2.md")
    tr(good, "tr3.md", module=["m-loan", 7])
    assert any("found 7" in m for m in msgs(good, "tr3.md"))


def test_a_field_not_present_or_empty_is_not_checked(good):
    config(good, "vocabularies:\n  vendor: {values: [a]}\n")
    tr(good)
    tr(good, "tr2.md", vendors=[])
    assert codes(good) == []


def test_a_source_file_with_a_list_a_mapping_and_a_list_of_mappings(good, tmp_path):
    (good / "regs").mkdir()
    (good / "regs/r.yaml").write_text("tenants: [t-a, t-b]\nvendors: {v-a: 1, v-b: 2}\nmodules: [{id: m-1}, {id: m-2}]\nnames: [{name: n-1}]\n")
    config(good, """vocabularies:
  tenant: {source_file: regs/r.yaml, key_path: tenants}
  vendor: {source_file: regs/r.yaml, key_path: vendors}
  module: {source_file: regs/r.yaml, key_path: modules}
""")
    tr(good, tenants=["t-a"], vendors=["v-b"], module="m-2")
    assert codes(good) == []
    tr(good, "tr2.md", tenants=["t-z"], vendors=["v-z"], module="m-9")
    assert len(msgs(good, "tr2.md")) == 3


def test_the_id_key_of_a_list_of_mappings(good):
    (good / "regs").mkdir()
    (good / "regs/r.yaml").write_text("tenants: [{name: acme}, {name: beta}]\n")
    config(good, "vocabularies:\n  tenant: {source_file: regs/r.yaml, key_path: tenants, id_key: name}\n")
    tr(good, tenants=["acme"])
    tr(good, "tr2.md", tenants=["gamma"])
    assert codes(good, "tr.md") == [] and msgs(good, "tr2.md")


def test_a_vocabulary_of_the_ids_of_documents_of_a_type(good):
    put(good, "modules/loan.md", {"type": "module", "id": "M-loan", "title": "loan", "path": "src/loan"}, "## Responsibility\n\nx\n\n## Public surface\n\nx\n\n## Dependencies\n\nx\n\n## Owners\n\nx")
    config(good, "vocabularies:\n  module: {of_type: module}\n")
    tr(good, module="M-loan")
    tr(good, "tr2.md", module="M-gone")
    assert codes(good, "tr.md") == [] and msgs(good, "tr2.md")


@pytest.mark.parametrize("block,fragment", [
    ("vocabularies: [a]\n", "must be a mapping"),
    ("vocabularies: {Bad: {values: [a]}}\n", "name must be"),
    ("vocabularies: {v: [a]}\n", "must be a mapping with one of"),
    ("vocabularies: {v: {}}\n", "exactly one of"),
    ("vocabularies: {v: {values: [a], of_type: module}}\n", "exactly one of"),
    ("vocabularies: {v: {values: [a], extra: 1}}\n", "unknown key"),
    ("vocabularies: {v: {values: a}}\n", "list of strings"),
    ("vocabularies: {v: {values: []}}\n", "has no values"),
    ("vocabularies: {v: {values: [1]}}\n", "plain strings only"),
    ("vocabularies: {v: {of_type: nosuchtype}}\n", "not a known document type"),
    ("vocabularies: {v: {source_file: missing.yaml, key_path: a}}\n", "not found"),
    ("vocabularies: {v: {source_file: r.yaml}}\n", "both be non-empty strings"),
    ("vocabularies: {v: {source_file: r.yaml, key_path: nope}}\n", "is not in"),
    ("vocabularies: {v: {source_file: r.yaml, key_path: scalar}}\n", "list or a mapping"),
    ("vocabularies: {v: {source_file: bad.yaml, key_path: a}}\n", "cannot be read as YAML"),
    ("vocabularies: {v: {source_file: r.yaml, key_path: ok, id_key: ''}}\n", "id_key"),
    ("vocabularies: {v: {1: a, values: [a]}}\n", "unknown key"),
    ("vocabularies: {v: {1: a}}\n", "unknown key"),
    ("vocabularies: {1: {values: [a]}}\n", "name must be"),
    ("vocabularies: {v: {source_file: r.yaml, key_path: ok, id_key: 3}}\n", "id_key"),
    ("vocabularies: {v: {source_file: r.yaml, key_path: 3}}\n", "both be non-empty strings"),
    ("vocabularies: {v: {source_file: '', key_path: ok}}\n", "both be non-empty strings"),
    ("vocabularies: {v: {source_file: 3, key_path: ok}}\n", "both be non-empty strings"),
    ("vocabularies: {v: {of_type: 3}}\n", "not a known document type"),
    ("vocabularies: {v: {source_file: top.yaml, key_path: a}}\n", "is not in"),
    ("vocabularies: {v: {values: [{id: x}]}}\n", "plain strings only"),
    ("vocabularies: {v: {of_type: runbook}}\n", "no document of type"),
    ("vocabularies: {v: {source_file: r.yaml, key_path: lists}}\n", "non-empty string"),
])
def test_acf044_for_each_bad_configuration(good, block, fragment):
    (good / "r.yaml").write_text("ok: [a]\nscalar: 3\nlists: [[a]]\n")
    (good / "bad.yaml").write_text("a: [unclosed\n")
    (good / "top.yaml").write_text("- just\n- a list\n")
    config(good, block)
    found = [i.message for i in codes(good, "", "ACF044")]
    assert any(fragment in m for m in found), (block, found)


def test_a_vocabulary_a_binding_names_but_the_bundle_does_not_define_is_not_checked(good):
    config(good, "vocabularies:\n  vendor: {values: [a]}\n")
    tr(good, tenants=["anything"], module="whatever")
    assert codes(good) == []


def test_an_adopter_can_bind_a_field_of_its_own_type(good):
    config(good, "types:\n  runbook:\n    vocab: {team: team}\nvocabularies:\n  team: {values: [core]}\n")
    put(good, "runbooks/RB-a.md", {"type": "runbook", "id": "RB-a", "title": "r", "team": "other"}, "## Purpose\n\np")
    assert any("team" in i.message for i in codes(good, "RB-a", "ACF043"))


def test_a_vocabulary_with_a_problem_is_not_used_so_it_adds_no_acf043(good):
    config(good, "vocabularies:\n  vendor: {values: [{id: x}]}\n")
    tr(good, vendors=["anything"])
    assert [i.code for i in codes(good)] == ["ACF044"]


def test_an_override_of_ticket_resolution_keeps_its_binding_unless_it_clears_it(good):
    config(good, "vocabularies:\n  vendor: {values: [a]}\ntypes:\n  ticket-resolution:\n    purpose: changed\n")
    tr(good, vendors=["zzz"])
    assert msgs(good)                                                          # the override keeps the core binding
    config(good, "types:\n  ticket-resolution:\n    vocab: {}\n")
    assert not msgs(good)                                                       # an empty `vocab` switches it off
