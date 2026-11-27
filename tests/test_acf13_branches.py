"""ACF 1.3, T-004 and T-005 (ADR-0015, ADR-0016): `branch_policy`, pure resolvers, `ackit branch resolve`, ACF039."""
import json
import socket
import subprocess

import pytest
import yaml

from ackit.branchpolicy import BranchPolicyError, policy, resolve_context_branch, resolve_work_branch
from ackit.cli import main
from ackit.registry import build

REG = {"default_stage": "uat", "repos": ["app", "ui"], "environments": [
    {"id": "acme", "repo": "app", "stages": {"uat": {"branches": {"app": "release/uat", "ui": "ui/uat"}}, "prod": {"branches": {"app": "release/prod"}}}}]}


@pytest.fixture
def reg(tmp_path):
    return build({"environment_registry": REG}, tmp_path)[0]


def test_defaults_when_block_absent():
    pol, problems = policy({})
    assert problems == [] and pol["context_branch"]["fallback"] == "main" and pol["work_branch"]["base_stage"] is None


def test_work_branch_uses_default_stage_unless_policy_or_caller_says_otherwise(reg):
    pol, _ = policy({})
    w = resolve_work_branch(reg, pol, "acme", author="bob", task="T-9")
    assert (w.base, w.stage, w.name) == ("release/uat", "uat", "bob-acme-T-9")
    pol, _ = policy({"branch_policy": {"work_branch": {"base_stage": "prod"}}})
    assert resolve_work_branch(reg, pol, "acme").base == "release/prod"
    assert resolve_work_branch(reg, pol, "acme", stage="uat").base == "release/uat"      # explicit stage wins
    assert resolve_work_branch(reg, pol, "acme", "ui", "uat").base == "ui/uat"
    assert resolve_work_branch(reg, pol, "acme").name is None


def test_unknown_environment_repository_stage_are_errors(reg):
    pol, _ = policy({})
    for kw in ({"environment": "zzz"}, {"environment": "acme", "repository": "zzz"}, {"environment": "acme", "stage": "zzz"}):
        with pytest.raises(BranchPolicyError):
            resolve_work_branch(reg, pol, **kw)


def test_context_branch_matches_or_falls_back():
    pol, _ = policy({"branch_policy": {"context_branch": {"required_before_code_push": True}}})
    c = resolve_context_branch(pol, "release/x", "bob", "feat", ["main", "release/x"])
    assert (c.base, c.base_is_fallback, c.name, c.required_before_code_push) == ("release/x", False, "bob-feat", True)
    c = resolve_context_branch(pol, "release/y", "bob", "feat", ["main", "release/x"])
    assert (c.base, c.base_is_fallback) == ("main", True)
    pol, _ = policy({"branch_policy": {"context_branch": {"base": "default-branch", "fallback": "trunk"}}})
    assert resolve_context_branch(pol, "release/x", existing_branches=["release/x"]).base == "trunk"
    with pytest.raises(BranchPolicyError):
        resolve_context_branch(pol, "")


@pytest.mark.parametrize("block", [
    {"nope": 1}, {"work_branch": {"name_pattern": "{bogus}"}}, {"work_branch": {"name_pattern": "{author"}}, {"work_branch": {"name_pattern": "plain"}},
    {"context_branch": {"base": "x"}}, {"context_branch": {"required_before_code_push": "yes"}}, {"context_branch": {"fallback": ""}},
    {"context_branch": []}, {"context_branch": {"zzz": 1}}])
def test_bad_policy_is_reported(block):
    assert policy({"branch_policy": block})[1], block
    assert policy({"branch_policy": 3})[1]


def test_resolvers_touch_no_process_and_no_socket(reg, monkeypatch):
    def boom(*a, **k):
        raise AssertionError("resolver reached for the outside world")
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket, "socket", boom)
    pol, _ = policy({})
    resolve_work_branch(reg, pol, "acme", author="a", task="t")
    resolve_context_branch(pol, "release/uat", "a", "c", ["release/uat"])


def _bundle(good, extra=""):
    cfg = good / "ackit.yaml"
    cfg.write_text(cfg.read_text() + "environment_registry:\n" + "".join(f"  {l}\n" for l in yaml.safe_dump(REG).splitlines()) + extra)
    return good


def test_cli_text_and_json(good, capsys):
    _bundle(good, "branch_policy: {context_branch: {required_before_code_push: true}}\n")
    args = ["branch", "resolve", "--bundle", str(good), "--environment", "acme", "--author", "bob", "--task", "T-9", "--code-branch", "feat",
            "--existing-branch", "release/uat"]
    assert main(args + ["--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["work_branch"] == {"base": "release/uat", "stage": "uat", "name": "bob-acme-T-9"}
    assert out["context_branch"] == {"base": "release/uat", "base_is_fallback": False, "name": "bob-feat", "required_before_code_push": True}
    assert main(args[:-2]) == 0
    text = capsys.readouterr().out
    assert "from main" in text and "fallback" in text and "required before the code push: yes" in text


def test_cli_errors(good, capsys):
    assert main(["branch", "resolve", "--bundle", str(good), "--environment", "acme"]) == 2        # no registry configured
    _bundle(good)
    assert main(["branch", "resolve", "--bundle", str(good), "--environment", "zzz"]) == 1
    assert "zzz" in capsys.readouterr().err
    assert main(["branch", "resolve", "--bundle", str(good), "--environment", "acme", "--stage", "zzz"]) == 1


# --- T-004/T-005 review fixes -------------------------------------------------------------------------------------------
@pytest.mark.parametrize("pattern", ["{author:d}", "{author:{bogus}}", "{author!x}", "{author:>{task}}", "{author!r}"])
def test_patterns_with_specs_or_conversions_are_refused(pattern):
    assert any("pattern" in p for p in policy({"branch_policy": {"work_branch": {"name_pattern": pattern}}})[1])


def test_empty_values_are_errors(reg):
    pol, _ = policy({})
    with pytest.raises(BranchPolicyError):
        resolve_work_branch(reg, pol, "acme", author="", task="t")
    with pytest.raises(BranchPolicyError):
        resolve_context_branch(pol, "x", author=" ", code_branch="c")


def test_resolvers_open_no_file(reg, monkeypatch):
    import builtins
    from pathlib import Path
    def boom(*a, **k):
        raise AssertionError("resolver opened a file")
    monkeypatch.setattr(builtins, "open", boom)
    monkeypatch.setattr(Path, "read_text", boom)
    pol, _ = policy({})
    resolve_work_branch(reg, pol, "acme", author="a", task="t")
    resolve_context_branch(pol, "release/uat", "a", "c", ["release/uat"])


def test_acf039_end_to_end(good):
    cfg = good / "ackit.yaml"
    cfg.write_text(cfg.read_text() + "branch_policy: {work_branch: {name_pattern: '{author:d}'}}\n")
    from ackit.bundle import Bundle
    from ackit.validate import validate
    from conftest import NOW
    assert any(i.code == "ACF039" for i in validate(Bundle.load(good), now=NOW))


def test_cli_more_paths(good, capsys, tmp_path):
    _bundle(good, "branch_policy: {work_branch: {base_stage: nowhere}}\n")
    base = ["branch", "resolve", "--bundle", str(good), "--environment", "acme"]
    assert main(base) == 1                                                        # unknown base_stage is found at resolve time
    lst = tmp_path / "b.txt"
    lst.write_text("release/prod\n\nmain\n")
    assert main(base + ["--stage", "prod", "--code-base-branch", "release/prod", "--existing-branches-file", str(lst), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["code_base_branch"] == "release/prod" and out["context_branch"]["base"] == "release/prod"
    assert main(base + ["--stage", "uat", "--repository", "ui", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["work_branch"]["base"] == "ui/uat"
    assert main(base + ["--stage", "uat", "--repository", "zzz"]) == 1
    assert main(base + ["--stage", "uat", "--existing-branches-file", str(tmp_path / "missing.txt")]) == 2
    assert main(base + ["--stage", "uat", "--author", "", "--task", "t"]) == 1
