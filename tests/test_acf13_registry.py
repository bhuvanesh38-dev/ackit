"""ACF 1.3, T-003 (ADR-0015): `environment_registry` model, reader, key paths, ACF038."""
import builtins
from pathlib import Path

import pytest
import yaml

from ackit.bundle import Bundle
from ackit.registry import RegistryError, build
from ackit.validate import validate
from conftest import NOW

DATA = {
    "default_stage": "uat",
    "repos": {"app": {"path": "~/app"}, "ui": {}},
    "environments": [
        {"id": "acme", "repo": "app", "code_line": "line-a",
         "stages": {"uat": {"branches": {"app": "release/uat", "ui": "ui/uat"}}, "prod": {"branches": {"app": "release/prod"}}},
         "tenants": ["t1"]},
        {"id": "beta", "repo": "ui", "stages": {"uat": {"branches": {"ui": "ui/beta"}}}},
    ],
    "extensions": {"infra": {"hosts": 3}},
}


def codes(root):
    return [(i.code, i.message) for i in validate(Bundle.load(root), now=NOW) if i.code == "ACF038"]


def test_absent_block_changes_nothing(good):
    assert build({}, good) == (None, [])
    assert codes(good) == []


def test_inline_and_source_file_give_the_same_model(tmp_path):
    inline, p1 = build({"environment_registry": DATA}, tmp_path)
    f = tmp_path / "elsewhere" / "reg.yaml"
    f.parent.mkdir()
    f.write_text(yaml.safe_dump(DATA))
    rel, p2 = build({"environment_registry": {"source_file": "elsewhere/reg.yaml"}}, tmp_path)
    absolute, p3 = build({"environment_registry": {"source_file": str(f)}}, tmp_path / "other")
    assert p1 == p2 == p3 == []
    assert inline == rel == absolute
    assert inline.branch("acme") == "release/uat"
    assert inline.branch("acme", "ui") == "ui/uat"
    assert inline.branch("acme", stage="prod") == "release/prod"
    assert inline.environment("acme").code_line == "line-a" and inline.environment("beta").code_line is None
    assert inline.repositories == ("app", "ui") and inline.stages() == ["prod", "uat"]


def test_extensions_are_carried_not_interpreted(tmp_path):
    reg, _ = build({"environment_registry": DATA}, tmp_path)
    assert reg.extensions == {"infra": {"hosts": 3}}


def test_key_paths_map_an_own_file(tmp_path):
    own = {"defaults": {"development_stage": "dev"}, "code_repos": ["svc"],
           "environments": [{"id": "x", "repo": "svc", "code_line": "L", "stages": {"dev": {"branches": {"svc": "develop/x"}}}}]}
    (tmp_path / "r.yaml").write_text(yaml.safe_dump(own))
    reg, problems = build({"environment_registry": {"source_file": "r.yaml",
                                                     "key_paths": {"default_stage": "defaults.development_stage", "repositories": "code_repos"}}}, tmp_path)
    assert problems == [] and reg.default_stage == "dev" and reg.repositories == ("svc",) and reg.branch("x") == "develop/x"


def test_branches_key_path_with_other_shape(tmp_path):
    own = {"default_stage": "s", "environments": [{"id": "x", "repo": "r", "envs": {"s": {"git": {"r": {"name": "b1"}}}}}]}
    reg, problems = build({"environment_registry": {**own, "key_paths": {"branches": "envs.${stage}.git.${repo}.name"}}}, tmp_path)
    assert problems == [] and reg.branch("x") == "b1"


@pytest.mark.parametrize("block,needle", [
    ({"source_file": "missing.yaml"}, "not found"),
    ({"key_paths": {"nope": "a"}}, "not a known key path"),
    ({"key_paths": {"branches": "stages.branches"}}, "whole dotted parts"),
    ({"surprise": 1}, "not a known key"),
    ({"default_stage": "uat", "environments": [{"id": "a", "repo": "r"}, {"id": "a", "repo": "r"}]}, "more than once"),
    ({"default_stage": "uat", "environments": [{"id": "a"}]}, "has no `repo`"),
    ({"default_stage": "uat", "environments": [{"repo": "r"}]}, "has no `id`"),
    ({"default_stage": "uat", "environments": "x"}, "must be a list"),
    ({"default_stage": "uat", "environments": [{"id": "a", "repo": "r", "stages": {"dev": {"branches": {"r": "b"}}}}]}, "default stage 'uat'"),
    ({"source_file": "x.yaml", "default_stage": "uat"}, "both `source_file` and inline"),
])
def test_clear_errors(tmp_path, block, needle):
    (tmp_path / "x.yaml").write_text("a: [")
    _, problems = build({"environment_registry": block}, tmp_path)
    assert any(needle in p for p in problems), problems


def test_malformed_yaml_and_non_mapping_file(tmp_path):
    (tmp_path / "bad.yaml").write_text("a: [")
    (tmp_path / "list.yaml").write_text("- 1\n")
    assert "not valid YAML" in build({"environment_registry": {"source_file": "bad.yaml"}}, tmp_path)[1][0]
    assert "mapping at the top level" in build({"environment_registry": {"source_file": "list.yaml"}}, tmp_path)[1][0]


def test_lookup_errors(tmp_path):
    reg, _ = build({"environment_registry": DATA}, tmp_path)
    for args in (("nope",), ("acme", "app", "dev"), ("acme", "zzz")):
        with pytest.raises(RegistryError):
            reg.branch(*args)


def test_acf038_in_validate(good):
    cfg = good / "ackit.yaml"
    cfg.write_text(cfg.read_text() + "environment_registry:\n  source_file: nowhere.yaml\n")
    assert any("not found" in m for _, m in codes(good))


def test_only_the_configured_file_is_opened(tmp_path, monkeypatch):
    f = tmp_path / "reg.yaml"
    f.write_text(yaml.safe_dump(DATA))
    opened = []
    real = Path.read_text
    monkeypatch.setattr(Path, "read_text", lambda self, *a, **k: (opened.append(self.resolve()), real(self, *a, **k))[1])
    real_open = builtins.open
    monkeypatch.setattr(builtins, "open", lambda f_, *a, **k: (opened.append(Path(str(f_)).resolve()), real_open(f_, *a, **k))[1])
    build({"environment_registry": {"source_file": "reg.yaml"}}, tmp_path)
    assert set(opened) <= {f.resolve()}


# --- T-003 review fixes ------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("template", ["a.x${stage}.${repo}", "stages.${stage}${repo}", "${repo}.${stage}", "stages.${stage}.${stage}.${repo}", "stages.${stage}"])
def test_bad_branch_templates_are_reported_not_crashed(tmp_path, template):
    _, problems = build({"environment_registry": {**DATA, "key_paths": {"branches": template}}}, tmp_path)
    assert any("whole dotted parts" in p for p in problems), problems


def test_binary_source_file_is_a_clear_error(tmp_path):
    (tmp_path / "b.yaml").write_bytes(b"\xff\xfe\x00bad")
    reg, problems = build({"environment_registry": {"source_file": "b.yaml"}}, tmp_path)
    assert reg is None and any("cannot be read" in p or "not valid YAML" in p for p in problems)


def test_wrong_value_types_are_reported(tmp_path):
    bad = {"default_stage": "u", "environments": [
        {"id": "a", "repo": "r", "stages": {"u": {"branches": {"r": {"name": "b"}}}}},
        {"id": "b", "repo": "r", "stages": ["x"]},
        {"id": "c", "repo": "r", "stages": {"u": {"branches": "oops"}}}], "extensions": "x"}
    _, problems = build({"environment_registry": bad}, tmp_path)
    text = " | ".join(problems)
    assert "must be a string, got dict" in text and "must be a mapping" in text and "`extensions` must be a mapping" in text


def test_key_path_into_extensions_is_refused(tmp_path):
    _, problems = build({"environment_registry": {**DATA, "key_paths": {"environments": "extensions.envs"}}}, tmp_path)
    assert any("must not start with `extensions`" in p for p in problems)


def test_documented_inline_example_has_no_problems(tmp_path):
    block = {"default_stage": "uat", "repos": ["app", "ui"], "environments": [
        {"id": "acme", "repo": "app", "code_line": "line-a", "stages": {"uat": {"branches": {"app": "release/uat", "ui": "release/uat"}}}}]}
    reg, problems = build({"environment_registry": block}, tmp_path)
    assert problems == [] and reg.branch("acme", "ui") == "release/uat"
