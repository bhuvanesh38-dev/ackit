import pytest
import yaml

from ackit.bundle import Bundle
from ackit.cli import main
from ackit.roles import all_role_names, kit_roles, load_role, validate_role
from ackit.prompt import build_prompt
from ackit.validate import validate
from conftest import NOW, feature, put

ROLES = ["developer", "tester", "security", "reviewer", "planner", "maintainer", "business-analyst", "architect", "designer", "devops", "support"]
PREFIX = {"developer": "DEV", "tester": "TST", "security": "SEC", "reviewer": "REV", "planner": "PLN", "maintainer": "MNT",
          "business-analyst": "BA", "architect": "ARC", "designer": "DSN", "devops": "OPS", "support": "SUP"}


def test_kit_has_all_roles():
    assert set(ROLES) <= set(kit_roles())


@pytest.fixture
def with_item(good):
    feature(good, modules=[])
    return good


@pytest.mark.parametrize("role", ROLES)
def test_role_prompt_and_definition(with_item, role):
    b = Bundle.load(with_item)
    r = load_role(b, role)
    assert validate_role(b, r) == []
    for kind in ("prompt", "rules", "checklist", "outputs", "prompt-guide"):
        assert kind in r.parts, kind
    out = build_prompt(b, role, "F-001")
    assert f"**{PREFIX[role]}-01**" in out and "F-001" in out and "No secrets in the repository" in out
    assert "## What you must write" in out
    assert [i for i in validate(Bundle.load(with_item), now=NOW) if i.severity == "error"] == []


def test_prompt_guide_has_required_parts():
    from ackit.bundle import data_dir
    for role in ROLES:
        g = (data_dir() / "roles" / role / "prompt-guide.md").read_text()
        for part in ("Identity", "Scope", "Inputs it loads", "Rules", "Checklist", "Output format", "Stop conditions", "## 2. Do", "## 3. Don't"):
            assert part in g, (role, part)


def test_budget_trims(with_item):
    feature(with_item, modules=[])
    p = with_item / "work/features/F-001-t.md"
    p.write_text(p.read_text() + "\n" + "filler line\n" * 600)
    b = Bundle.load(with_item)
    assert len(build_prompt(b, "developer", "F-001", budget=2000)) < len(build_prompt(b, "developer", "F-001"))


def test_explain_lists_sources(with_item, capsys):
    assert main(["prompt", "developer", "--bundle", str(with_item), "--item", "F-001", "--explain"]) == 0
    out = capsys.readouterr().out
    assert "work item" in out and "rules/no-secrets-in-repo.md: rule included in full" in out and "role rules" in out


def test_unknown_role_and_item(with_item):
    assert main(["prompt", "wizard", "--bundle", str(with_item)]) == 2
    assert main(["prompt", "developer", "--bundle", str(with_item), "--item", "F-404"]) == 2


def test_overlay_overrides_part_and_validates(with_item):
    d = with_item / "roles" / "developer"
    d.mkdir(parents=True)
    (d / "rules.md").write_text("1. Never edit generated/ files; change the generator.\n")
    b = Bundle.load(with_item)
    r = load_role(b, "developer")
    assert r.origin == "overlay" and r.parts["rules"][1].startswith("overlay")
    out = build_prompt(b, "developer", "F-001")
    assert "Never edit generated/ files" in out and "**DEV-01**" in out          # rules overridden, checklist from kit
    assert "Read the work item, its module doc" not in out
    assert [i for i in validate(b, now=NOW) if i.severity == "error"] == []
    (d / "checklist.md").write_text("no boxes here")
    assert any(i.code == "ACF030" for i in validate(Bundle.load(with_item), now=NOW))


def test_overlay_prompt_template_override(with_item):
    d = with_item / "roles" / "tester"
    d.mkdir(parents=True)
    (d / "prompt.md").write_text('{% extends "_base.md.j2" %}{% block mission %}CUSTOM MISSION for {{ role_title }}.{% endblock %}')
    assert "CUSTOM MISSION for Tester." in build_prompt(Bundle.load(with_item), "tester", "F-001")


def test_custom_role_scaffold_validate_prompt_gate(with_item, capsys):
    assert main(["role", "new", "data-steward", "--bundle", str(with_item), "--description", "Guards data quality."]) == 0
    d = with_item / "roles" / "data-steward"
    assert {p.name for p in d.iterdir()} == {"role.yaml", "prompt.md", "rules.md", "checklist.md", "outputs.md", "prompt-guide.md"}
    y = yaml.safe_load((d / "role.yaml").read_text())
    y.update(owns=["reference"], gates=["start", "handoff"], tools_allowed=["read", "run-readonly-queries"])
    (d / "role.yaml").write_text(yaml.safe_dump(y))
    b = Bundle.load(with_item)
    assert "data-steward" in all_role_names(b)
    assert main(["validate", str(with_item)]) == 0
    out = build_prompt(b, "data-steward", "F-001")
    assert "**data-steward**" in out and "Guards data quality." in out and "run-readonly-queries" in out and "**DAT-01**" in out
    assert main(["check", "--bundle", str(with_item), "--gate", "start", "--item", "F-001", "--role", "data-steward"]) == 1  # item is draft
    y["owns"] = ["not-a-type"]; y["gates"] = ["launch"]
    (d / "role.yaml").write_text(yaml.safe_dump(y))
    msgs = validate_role(Bundle.load(with_item), load_role(Bundle.load(with_item), "data-steward"))
    assert any("unknown doc type" in m for m in msgs) and any("unknown gate" in m for m in msgs)


def test_incomplete_custom_role_fails_validate(with_item):
    (with_item / "roles" / "ghost").mkdir(parents=True)
    (with_item / "roles" / "ghost" / "role.yaml").write_text("name: ghost\n")
    assert main(["validate", str(with_item)]) == 1


def test_custom_role_extends_builtin(with_item):
    assert main(["role", "new", "junior-dev", "--bundle", str(with_item), "--extends", "developer"]) == 0
    d = with_item / "roles" / "junior-dev"
    (d / "rules.md").unlink()
    r = load_role(Bundle.load(with_item), "junior-dev")
    assert r.parts["rules"][1].startswith("extends developer")


# ---- suggested_agent (1.1) -----------------------------------------------------------------------------------------
EXPECTED_AGENT = {"developer": ("high", "normal", None), "architect": ("high", "deep", None), "security": ("high", "deep", None),
                  "reviewer": ("high", "normal", "developer"), "tester": ("standard", "normal", None),
                  "business-analyst": ("standard", "normal", None), "designer": ("standard", "normal", None), "devops": ("standard", "normal", None)}


@pytest.mark.parametrize("role,exp", sorted(EXPECTED_AGENT.items()))
def test_builtin_suggested_agent_defaults(with_item, role, exp):
    sa = load_role(Bundle.load(with_item), role).profile["suggested_agent"]
    assert (sa["capability"], sa["reasoning"], sa.get("independent_of")) == exp


def test_suggested_agent_is_vendor_neutral_in_core():
    import re
    from ackit.bundle import data_dir
    for y in (data_dir() / "roles").glob("*/role.yaml"):
        assert not re.search(r"claude|gpt|gemini|opus|sonnet|haiku|llama|mistral", y.read_text(), re.I), y


def test_role_list_and_explain_show_it(with_item, capsys):
    assert main(["role", "list", "--bundle", str(with_item)]) == 0
    out = capsys.readouterr().out
    line = next(l for l in out.splitlines() if l.startswith("reviewer"))
    assert line.index("owns:") < line.index("gates:") < line.index("agent:") and "independent of developer" in line
    assert main(["role", "list", "--bundle", str(with_item), "--json"]) == 0
    import json
    data = json.loads(capsys.readouterr().out)
    assert next(r for r in data if r["name"] == "reviewer")["suggested_agent"]["independent_of"] == "developer"
    assert main(["prompt", "reviewer", "--bundle", str(with_item), "--item", "F-001", "--explain"]) == 0
    assert "suggested agent: capability high, reasoning normal, independent of developer" in capsys.readouterr().out


def test_acf030_validates_suggested_agent(with_item):
    d = with_item / "roles" / "developer"
    d.mkdir(parents=True)

    def problems(sa):
        (d / "role.yaml").write_text(yaml.safe_dump({"suggested_agent": sa}))
        b = Bundle.load(with_item)
        return validate_role(b, load_role(b, "developer"))

    assert problems({"capability": "fast", "reasoning": "deep"}) == []
    assert any("capability" in m for m in problems({"capability": "turbo"}))
    assert any("reasoning" in m for m in problems({"capability": "high", "reasoning": "max"}))
    assert any("unknown key 'model'" in m for m in problems({"capability": "high", "model": "x"}))
    assert any("unknown role" in m for m in problems({"capability": "high", "independent_of": "wizard"}))
    assert any("itself" in m for m in problems({"capability": "high", "independent_of": "developer"}))
    assert any("mapping" in m for m in problems("high"))
    (d / "role.yaml").write_text(yaml.safe_dump({"suggested_agent": {"capability": "turbo"}}))
    assert main(["validate", str(with_item)]) == 1            # ACF030 error through the CLI


def test_suggested_agent_optional_for_custom_role(with_item):
    assert main(["role", "new", "ops-lead", "--bundle", str(with_item)]) == 0
    assert main(["validate", str(with_item)]) == 0


# ---- 1.2.1: wrap-up prompt kind, overlay path, findings format (I-003 items 19 and 20) -------------------------------
def test_wrap_up_is_a_recognised_optional_part(with_item, capsys):
    from ackit.roles import KINDS, OPTIONAL_KINDS
    assert "wrap-up" in KINDS and "wrap-up" in OPTIONAL_KINDS
    b = Bundle.load(with_item)
    assert "wrap-up" not in load_role(b, "developer").parts  # the kit ships none; a role without one is complete
    assert validate_role(b, load_role(b, "developer")) == []
    assert main(["prompt", "developer", "--bundle", str(with_item), "--part", "wrap-up"]) == 1  # none yet
    d = with_item / "roles" / "developer"
    d.mkdir(parents=True)
    (d / "wrap-up.md").write_text("Stop. Make it compile. List what is left.\n")
    b = Bundle.load(with_item)
    r = load_role(b, "developer")
    assert r.text("wrap-up") == "Stop. Make it compile. List what is left." and r.parts["wrap-up"][1].startswith("overlay")
    assert validate_role(b, r) == []
    capsys.readouterr()
    assert main(["prompt", "developer", "--bundle", str(with_item), "--part", "wrap-up"]) == 0
    assert capsys.readouterr().out.strip() == "Stop. Make it compile. List what is left."
    (d / "wrap-up.md").write_text("---\nx: 1\n---\n\n")  # frontmatter only: empty
    assert any("wrap-up is empty" in p for p in validate_role(b, load_role(Bundle.load(with_item), "developer")))
    assert main(["role", "check", "developer", "--bundle", str(with_item)]) == 1


def test_wrap_up_does_not_change_the_prompt(with_item):
    before = build_prompt(Bundle.load(with_item), "developer", "F-001").split("\n", 1)[1]
    d = with_item / "roles" / "developer"
    d.mkdir(parents=True)
    (d / "wrap-up.md").write_text("Wrap up.\n")
    assert build_prompt(Bundle.load(with_item), "developer", "F-001").split("\n", 1)[1] == before


def test_role_path_prints_the_overlay_folder(with_item, capsys):
    capsys.readouterr()
    assert main(["role", "path", "reviewer", "--bundle", str(with_item)]) == 0
    cap = capsys.readouterr()
    assert cap.out.strip() == str(with_item / "roles" / "reviewer") and "no overlay yet" in cap.err
    (with_item / "roles" / "reviewer").mkdir(parents=True)
    assert main(["role", "path", "reviewer", "--bundle", str(with_item)]) == 0
    assert "no overlay yet" not in capsys.readouterr().err
    assert main(["role", "path", "nobody", "--bundle", str(with_item)]) == 2
    assert main(["role", "path", "--bundle", str(with_item)]) == 2


@pytest.mark.parametrize("role", ["reviewer", "security"])
def test_reviewer_and_security_define_the_findings_format(with_item, role):
    out = build_prompt(Bundle.load(with_item), role, "F-001")
    for word in ("Findings (machine-readable)", '"verdict"', '"findings"', "blocking", "major", "minor", "info", '"file"', '"line"', '"title"', '"detail"'):
        assert word in out, (role, word)


# F-004 / T-020: the `support` role
def test_support_role_owns_the_three_types_and_is_listed(with_item, capsys):
    assert main(["role", "list", "--bundle", str(with_item)]) == 0
    out = capsys.readouterr().out
    line = next(l for l in out.splitlines() if l.startswith("support"))
    for t in ("ticket-resolution", "issue-pattern", "platform-behaviour"):
        assert t in line
    assert "agent:" in line


def test_support_prompt_and_rules_each_carry_the_guard_rails(with_item):
    from ackit.bundle import Bundle
    from ackit.roles import load_role
    role = load_role(Bundle.load(with_item), "support")
    prompt, rules = role.text("prompt"), role.text("rules")
    for where, text in (("prompt", prompt), ("rules", rules)):
        for must in ("evidence", "verified", "recipe", "read-only"):
            assert must in text, (where, must)
    assert "Question:" in prompt and "verified_at_commit" in prompt and "verified_at_commit" in rules
    assert "stable" in prompt and "stable" in rules
    assert "work_item" in prompt and "registered" in prompt and "registered" in rules.lower()


def test_support_prompt_overrides_the_ask_for_a_work_item_line(with_item, capsys):
    assert main(["prompt", "support", "--bundle", str(with_item)]) == 0
    out = capsys.readouterr().out
    assert "No work item given. Ask for one before changing anything." in out          # the base text is still there ...
    assert out.index("ignore that line and work from the ticket evidence") < out.index("No work item given")    # ... and the mission overrides it, ahead of it
    assert "support engineer" in out and "Documents you own: ticket-resolution, issue-pattern, platform-behaviour" in out


def test_a_role_with_no_gates_lists_a_dash(with_item, capsys):
    main(["role", "list", "--bundle", str(with_item)])
    assert "gates: -" in next(l for l in capsys.readouterr().out.splitlines() if l.startswith("support"))
