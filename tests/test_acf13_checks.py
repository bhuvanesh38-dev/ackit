"""ACF 1.3, T-008 (ADR-0016, ADR-0019): `process_checks`, `ackit checks run`, ACF041, proof P4."""
import json
import socket
import subprocess
import sys

import pytest

from ackit.checks import parse
from ackit.cli import main

PY = sys.executable


def entry(name, code, level="block", when="pre-push", **extra):
    return {"name": name, "level": level, "when": when, "run": [PY, "-c", code], **extra}


def configure(root, checks):
    import yaml
    cfg = root / "ackit.yaml"
    cfg.write_text(cfg.read_text() + yaml.safe_dump({"process_checks": checks}))
    return root


def run(root, *extra):
    return main(["checks", "run", "--bundle", str(root), *extra])


def test_absent_block_is_empty(good, capsys):
    assert parse({}) == ([], [])
    assert run(good, "--when", "pre-push") == 0
    assert "0 check(s)" in capsys.readouterr().out


def test_pass_block_fail_warn_fail_missing_and_timeout(good, capsys):
    configure(good, [entry("ok", "print('fine')"), entry("soft", "import sys; sys.exit(3)", level="warn")])
    assert run(good, "--when", "pre-push") == 0                           # a failing warn does not fail the run
    out = capsys.readouterr().out
    assert "PASS block ok: fine" in out and "FAIL warn  soft: exit 3" in out
    (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text().split("process_checks")[0])
    configure(good, [entry("hard", "import sys; sys.exit(1)"), {"name": "gone", "level": "block", "when": "pre-push", "run": ["no-such-binary-xyz"]},
                     entry("slow", "import time; time.sleep(5)", timeout=1)])
    assert run(good, "--when", "pre-push", "--json") == 1
    res = {r["name"]: r for r in json.loads(capsys.readouterr().out)}
    assert not res["hard"]["passed"] and "could not run" in res["gone"]["detail"] and "timed out" in res["slow"]["detail"]


def test_when_and_name_select_entries(good, capsys):
    configure(good, [entry("a", "pass", when="pre-commit"), entry("b", "pass", when="pre-push")])
    run(good, "--when", "pre-commit", "--json")
    assert [r["name"] for r in json.loads(capsys.readouterr().out)] == ["a"]
    run(good, "--when", "pre-push", "--name", "b", "--json")
    assert [r["name"] for r in json.loads(capsys.readouterr().out)] == ["b"]
    assert run(good, "--when", "pre-push", "--name", "zzz") == 2


def test_arguments_are_not_interpreted_by_a_shell(good, tmp_path, capsys):
    marker = tmp_path / "pwned"
    configure(good, [{"name": "meta", "level": "block", "when": "on-demand",
                      "run": [PY, "-c", "import sys; sys.exit(0 if sys.argv[1] == sys.argv[2] else 1)", f"x; touch {marker}", f"x; touch {marker}"]}])
    assert run(good, "--when", "on-demand") == 0 and not marker.exists()


def test_cwd_and_environment(good, tmp_path, capsys):
    configure(good, [entry("env", "import os; print(os.getcwd()); assert os.environ['ACKIT_CHECK_WHEN'] == 'on-demand' and os.environ['ACKIT_BUNDLE']", when="on-demand")])
    assert run(good, "--when", "on-demand", "--cwd", str(tmp_path)) == 0
    assert str(tmp_path.resolve()) in capsys.readouterr().out


@pytest.mark.parametrize("bad", [
    "x", [5], [{"level": "block", "when": "pre-push", "run": ["a"]}], [{"name": "n", "level": "loud", "when": "pre-push", "run": ["a"]}],
    [{"name": "n", "level": "block", "when": "never", "run": ["a"]}], [{"name": "n", "level": "block", "when": "pre-push", "run": "a b"}],
    [{"name": "n", "level": "block", "when": "pre-push", "run": []}], [{"name": "n", "level": "block", "when": "pre-push", "run": ["a"], "timeout": 0}],
    [{"name": "n", "level": "block", "when": "pre-push", "run": ["a"], "extra": 1}],
    [{"name": "n", "level": "block", "when": "pre-push", "run": ["a"]}, {"name": "n", "level": "warn", "when": "pre-push", "run": ["a"]}]])
def test_bad_configuration_is_reported(good, bad, capsys):
    assert parse({"process_checks": bad})[1]
    configure(good, bad)
    assert run(good, "--when", "pre-push") == 2


def test_p4_no_network_without_commands(good, monkeypatch):
    """Proof P4 (a tripwire): with no commands configured, validate, branch resolve and checks run reach neither the network nor a child process."""
    def boom(*a, **k):
        raise AssertionError("the core reached for the outside world")
    monkeypatch.setattr(socket.socket, "connect", boom)
    for name in ("socket", "create_connection", "getaddrinfo", "gethostbyname", "socketpair"):
        monkeypatch.setattr(socket, name, boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    assert main(["validate", str(good)]) == 0
    assert run(good, "--when", "pre-push") == 0
    cfg = good / "ackit.yaml"
    cfg.write_text(cfg.read_text() + "environment_registry: {default_stage: uat, repos: [a], environments: [{id: e, repo: a, stages: {uat: {branches: {a: b}}}}]}\n")
    assert main(["branch", "resolve", "--bundle", str(good), "--environment", "e"]) == 0


def test_p4_static_core_imports_no_network_library():
    import re
    from pathlib import Path
    banned = re.compile(r"^\s*(import|from)\s+(socket|urllib|http|ssl|requests|ftplib|smtplib|asyncio)\b", re.M)
    hits = [str(p) for p in (Path(__file__).parent.parent / "src" / "ackit").rglob("*.py") if banned.search(p.read_text())]
    assert hits == []


def test_name_with_the_wrong_when_is_refused(good, capsys):
    configure(good, [entry("only-push", "pass", when="pre-push")])
    assert run(good, "--when", "pre-commit", "--name", "only-push") == 2
    assert "pre-push" in capsys.readouterr().err


def test_timeout_kills_grandchildren_and_odd_output_is_survived(good, tmp_path, capsys):
    marker = tmp_path / "grandchild-survived"
    grandchild = tmp_path / "gc.py"
    grandchild.write_text(f"import time\ntime.sleep(2)\nopen({str(marker)!r}, 'w').close()\n")
    script = tmp_path / "slow.py"
    script.write_text(f"import subprocess, sys, time\nsubprocess.Popen([sys.executable, {str(grandchild)!r}])\ntime.sleep(30)\n")
    code = f"exec(open({str(script)!r}).read())"
    configure(good, [entry("slow", code, timeout=1), entry("bytes", "import sys; sys.stdout.buffer.write(b'\\xff\\xfe ok')", level="warn"),
                     entry("silent", "import sys; sys.exit(4)", level="warn"), entry("stdin", "import sys; print(repr(sys.stdin.read()))")])
    assert run(good, "--when", "pre-push", "--json") == 1
    res = {r["name"]: r for r in json.loads(capsys.readouterr().out)}
    assert "timed out" in res["slow"]["detail"] and res["bytes"]["passed"] and res["silent"]["detail"] == "exit 4"
    assert res["stdin"]["detail"] == "''"
    import time
    time.sleep(2.5)
    assert not marker.exists()                      # the grandchild was killed with the group


def test_acf041_through_validate(good, capsys):
    configure(good, [{"name": "x", "level": "loud", "when": "pre-push", "run": ["a"]}])
    assert main(["validate", str(good), "--json"]) == 1
    assert any(i["code"] == "ACF041" for i in json.loads(capsys.readouterr().out))
    assert parse({"process_checks": [{"name": "n", "level": "warn", "when": "pre-push", "run": ["a"], "timeout": 1.5}]})[1]
    assert parse({"process_checks": [{"name": "n", "level": "warn", "when": "pre-push", "run": ["a"], "timeout": True}]})[1]


# --- stdin pass-through, scope, placeholders (ADR-0019: a hook calls one command) -----------------------------------------
def test_stdin_pass_gives_every_such_check_the_same_input(good, monkeypatch, capsys):
    import io
    configure(good, [entry("a", "import sys; print('a:' + sys.stdin.read().strip())", stdin="pass"),
                     entry("b", "import sys; print('b:' + sys.stdin.read().strip())", stdin="pass"),
                     entry("c", "import sys; print('c:' + repr(sys.stdin.read()))")])
    class Fake(io.TextIOWrapper):
        def isatty(self):
            return False
    monkeypatch.setattr(sys, "stdin", Fake(io.BytesIO(b"refs/heads/x abc refs/heads/x def\n")))
    assert run(good, "--when", "pre-push", "--json") == 0
    res = {r["name"]: r["detail"] for r in json.loads(capsys.readouterr().out)}
    assert res == {"a": "a:refs/heads/x abc refs/heads/x def", "b": "b:refs/heads/x abc refs/heads/x def", "c": "c:''"}


def test_scope_selects_and_unscoped_runs_without_it(good, capsys):
    configure(good, [entry("plain", "pass"), entry("clone", "pass", scope="code")])
    run(good, "--when", "pre-push", "--json")
    assert [r["name"] for r in json.loads(capsys.readouterr().out)] == ["plain"]
    run(good, "--when", "pre-push", "--scope", "code", "--json")
    assert [r["name"] for r in json.loads(capsys.readouterr().out)] == ["clone"]
    assert run(good, "--when", "pre-push", "--scope", "nope") == 2
    assert run(good, "--when", "pre-push", "--name", "clone") == 2                  # a scoped check asked for by name without its scope
    assert run(good, "--when", "pre-push", "--name", "plain", "--scope", "code") == 2


def test_placeholders_are_replaced_without_a_shell(good, tmp_path, capsys):
    configure(good, [entry("ph", "import sys; sys.exit(0 if sys.argv[1].endswith(sys.argv[2]) else 1)")])
    cfg = good / "ackit.yaml"
    import yaml
    data = yaml.safe_load(cfg.read_text())
    data["process_checks"][0]["run"] += ["{bundle}/x", f"{good.name}/x"]
    cfg.write_text(yaml.safe_dump(data))
    assert run(good, "--when", "pre-push") == 0
    data["process_checks"][0]["run"][-2:] = ["{cwd}", str(tmp_path.resolve())]
    cfg.write_text(yaml.safe_dump(data))
    assert run(good, "--when", "pre-push", "--cwd", str(tmp_path)) == 0


def test_bad_stdin_and_scope_values_are_refused():
    base = {"name": "n", "level": "warn", "when": "pre-push", "run": ["a"]}
    assert parse({"process_checks": [{**base, "stdin": "yes"}]})[1]
    assert parse({"process_checks": [{**base, "scope": ""}]})[1]
    assert not parse({"process_checks": [{**base, "stdin": "pass", "scope": "code"}]})[1]


def test_new_field_types_are_refused_and_reported_by_validate(good, capsys):
    base = {"name": "n", "level": "warn", "when": "pre-push", "run": ["a"]}
    for bad in ({"stdin": 5}, {"scope": 5}, {"stdin": None}):
        assert parse({"process_checks": [{**base, **bad}]})[1], bad
    configure(good, [{**base, "stdin": "maybe"}])
    assert main(["validate", str(good), "--json"]) == 1
    assert any(i["code"] == "ACF041" and "stdin" in i["message"] for i in json.loads(capsys.readouterr().out))


def test_large_input_and_a_command_that_ignores_it(good, monkeypatch, capsys):
    import io
    configure(good, [entry("reads", "import sys; print(len(sys.stdin.buffer.read()))", stdin="pass"), entry("ignores", "pass", stdin="pass")])
    class Fake(io.TextIOWrapper):
        def isatty(self):
            return False
    monkeypatch.setattr(sys, "stdin", Fake(io.BytesIO(b"x" * 3_000_000)))
    assert run(good, "--when", "pre-push", "--json") == 0
    res = {r["name"]: r for r in json.loads(capsys.readouterr().out)}
    assert res["reads"]["detail"] == "3000000" and res["ignores"]["passed"]


def test_no_match_warns_and_a_closed_stdin_is_survived(good, monkeypatch, capsys):
    configure(good, [entry("only", "pass", when="pre-push", stdin="pass")])
    assert run(good, "--when", "pre-commit") == 0
    assert "nothing was checked" in capsys.readouterr().err
    monkeypatch.setattr(sys, "stdin", None)
    assert run(good, "--when", "pre-push") == 0
    assert main(["checks", "run", "--bundle", str(good), "--when", "pre-push", "--scope", ""]) == 2


def test_tmpdir_is_removed_after_a_normal_run_and_after_a_timeout(good, tmp_path, capsys):
    marker = tmp_path / "where.txt"
    code = f"import sys,pathlib; pathlib.Path(sys.argv[1]).is_dir() or sys.exit(3); open({str(marker)!r},'w').write(sys.argv[1]); {{}}"
    root = configure(good, [
        {"name": "ok", "level": "block", "when": "on-demand", "run": [PY, "-c", code.format(""), "{tmpdir}"]},
    ])
    assert run(root, "--when", "on-demand") == 0
    first = marker.read_text()
    assert first and not __import__("os").path.exists(first)
    capsys.readouterr()

    slow = code.format("__import__('time').sleep(30)")
    configure_slow = {"name": "slow", "level": "block", "when": "on-demand", "timeout": 1, "run": [PY, "-c", slow, "{tmpdir}"]}
    root2 = configure(good, [configure_slow])
    assert run(root2, "--when", "on-demand", "--name", "slow") == 1
    second = marker.read_text()
    assert second != first and not __import__("os").path.exists(second)     # killed by the timeout, folder still removed


def test_git_command_line_finds_the_nearest_git_ancestor(monkeypatch):
    from ackit import checks
    procs = {
        100: (b"/bin/bash\0hook\0", 200),
        200: (b"/usr/bin/git\0commit\0--amend\0-m\0two\0", 300),
        300: (b"zsh\0", 1),
    }

    class FakeProc:
        def __init__(self, path):
            self.pid = int(str(path).split("/")[2])
            self.leaf = str(path).rsplit("/", 1)[1]

        def read_bytes(self):
            return procs[self.pid][0]

        def read_text(self):
            return f"{self.pid} (x) S {procs[self.pid][1]} 0"

    monkeypatch.setattr(checks, "Path", FakeProc)
    monkeypatch.setattr(checks.os, "getppid", lambda: 100)
    assert checks.git_command_line() == "/usr/bin/git commit --amend -m two"
    procs[200] = (b"/usr/bin/other\0", 300)
    assert checks.git_command_line() == ""                                  # no git above: empty, not an error


def test_git_command_placeholder_expands_to_the_command_line(good, monkeypatch, capsys):
    from ackit import checks
    monkeypatch.setattr(checks, "git_command_line", lambda: "git commit --amend")
    root = configure(good, [{"name": "g", "level": "block", "when": "on-demand",
                             "run": [PY, "-c", "import sys; sys.exit(0 if sys.argv[1]=='git commit --amend' else 4)", "{git_command}"]}])
    assert run(root, "--when", "on-demand") == 0
