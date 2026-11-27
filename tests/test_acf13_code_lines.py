"""ACF 1.3, T-006 (ADR-0017): `code_lines` on documents, `--code-line`, ACF035."""
import yaml

from ackit.bundle import Bundle
from ackit.cli import main
from ackit.validate import validate
from conftest import NOW, put

REG = {"default_stage": "uat", "repos": ["app"], "environments": [
    {"id": "e1", "repo": "app", "code_line": "line-a", "stages": {"uat": {"branches": {"app": "b1"}}}},
    {"id": "e2", "repo": "app", "code_line": "line-b", "stages": {"uat": {"branches": {"app": "b2"}}}}]}
RULE = "## Rule\n\nDo {n}.\n\n## Why\n\nBecause.\n"


def rule(root, name, lines=None, **extra):
    meta = {"type": "rule", "title": name, "status": "draft", "severity": "advisory", **extra}
    if lines is not None:
        meta["code_lines"] = lines
    put(root, f"rules/{name}.md", meta, RULE.format(n=name))


def with_registry(root):
    cfg = root / "ackit.yaml"
    cfg.write_text(cfg.read_text() + "environment_registry:\n" + "".join(f"  {l}\n" for l in yaml.safe_dump(REG).splitlines()))


def acf035(root):
    return [i for i in validate(Bundle.load(root), now=NOW) if i.code == "ACF035"]


def test_absent_and_empty_mean_every_line(good):
    rule(good, "a")
    rule(good, "b", [])
    with_registry(good)
    assert acf035(good) == []


def test_unknown_line_is_an_error_only_with_a_registry(good):
    rule(good, "a", ["nope"])
    assert acf035(good) == []                       # free text without a registry
    with_registry(good)
    found = acf035(good)
    assert len(found) == 1 and "'nope'" in found[0].message and found[0].severity == "error"
    rule(good, "a", ["line-a"])
    assert acf035(good) == []


def test_wrong_shape_is_reported(good):
    rule(good, "a", "line-a")
    rule(good, "b", [1])
    assert len(acf035(good)) == 2


def test_validate_code_line_keeps_matching_documents(good, capsys):
    rule(good, "a", ["line-a"], severity="nonsense")        # an error in a line-a document
    rule(good, "b", ["line-b"], severity="nonsense")        # the same error in a line-b document
    with_registry(good)
    assert main(["validate", str(good), "--json"]) == 1
    both = {i["path"] for i in __import__("json").loads(capsys.readouterr().out) if i["code"] == "ACF026"}
    assert both == {"rules/a.md", "rules/b.md"}
    main(["validate", str(good), "--json", "--code-line", "line-a"])
    only = {i["path"] for i in __import__("json").loads(capsys.readouterr().out) if i["code"] == "ACF026"}
    assert only == {"rules/a.md"}
    assert main(["validate", str(good), "--code-line", "zzz"]) == 2


def test_prompt_code_line_leaves_out_other_lines(good, capsys):
    rule(good, "only-a", ["line-a"], severity="blocking")
    rule(good, "only-b", ["line-b"], severity="blocking")
    rule(good, "every", None, severity="blocking")
    assert main(["prompt", "--bundle", str(good), "developer", "--code-line", "line-a"]) == 0
    out = capsys.readouterr().out
    assert "Do only-a." in out and "Do every." in out and "Do only-b." not in out
    main(["prompt", "--bundle", str(good), "developer"])
    assert "Do only-b." in capsys.readouterr().out


def test_prompt_unknown_line_and_other_types_and_whitespace(good, capsys):
    from ackit.codelines import applies_to_line
    assert applies_to_line({"code_lines": ["a"]}, " a ") and not applies_to_line({"code_lines": ["a"]}, "b")
    with_registry(good)
    assert main(["prompt", "--bundle", str(good), "developer", "--code-line", "typo"]) == 2
    assert "not in the registry" in capsys.readouterr().err
    assert main(["validate", str(good), "--code-line", "line-a"]) in (0, 1)
