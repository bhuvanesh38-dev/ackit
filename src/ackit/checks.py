"""Adopter process checks (ACF 1.3, ADR-0016, ADR-0019).

`ackit.yaml` may carry

    process_checks:
      - name: store-pr-before-push
        level: block                  # block | warn
        when: pre-push                # pre-commit | pre-push | on-demand
        run: ["python3", "scripts/check.py"]     # an argument list, run without a shell
        description: "why the check exists"
        timeout: 120                  # seconds, optional (default 120)
        stdin: pass                   # optional: give the command the standard input of `ackit checks run` (default none)
        scope: code                   # optional label; `ackit checks run --scope code` runs only that scope, none runs the unscoped

`{bundle}`, `{cwd}`, `{tmpdir}` (a temporary folder the kit removes after the command, even after a timeout) and `{git_command}` (the command line of the git process above, e.g. `git commit --amend`; empty when none) in an argument are replaced by plain text. The core ships no check. `ackit checks run --when <point>` runs the commands the adopter listed for that point and reports. The
commands may do anything the adopter decides, so they are outside the statement that the core opens no connection; the core
itself opens none. A command that fails, cannot be started or times out is a failure. A failing `block` check makes the run fail,
a failing `warn` check is printed only. A command runs without a shell, in its own process
group (a timeout kills the whole group), with the caller's environment plus `ACKIT_BUNDLE` and `ACKIT_CHECK_WHEN`; only the last
64 KiB of its output is kept, and the last line is shown.
"""
from __future__ import annotations

import os
import shutil
import signal
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

LEVELS = ("block", "warn")
WHEN = ("pre-commit", "pre-push", "on-demand")
KEYS = {"name", "level", "when", "run", "description", "timeout", "stdin", "scope"}
STDIN = ("none", "pass")
DEFAULT_TIMEOUT = 120
MAX_OUTPUT = 65536          # only the last 64 KiB of a command's output is kept


@dataclass(frozen=True)
class Check:
    name: str
    level: str
    when: str
    run: tuple[str, ...]
    description: str
    timeout: int
    stdin: str = "none"          # `pass`: the command gets the standard input of `ackit checks run` (a pre-push hook's pushed refs)
    scope: str | None = None     # optional label, e.g. `code` for the checks a code clone runs; selected with `--scope`


@dataclass(frozen=True)
class Result:
    check: Check
    passed: bool
    detail: str
    seconds: float
    output: str = ""             # the last 64 KiB of the command's output, decoded with replacement


def parse(config: dict) -> tuple[list[Check], list[str]]:
    """(the usable checks, the problems). An unusable entry is left out and reported."""
    raw = (config or {}).get("process_checks")
    if raw is None:
        return [], []
    if not isinstance(raw, list):
        return [], [f"`process_checks` must be a list, got {type(raw).__name__}"]
    checks, problems, seen = [], [], set()
    for n, e in enumerate(raw):
        where = f"`process_checks[{n}]`"
        if not isinstance(e, dict):
            problems.append(f"{where} must be a mapping")
            continue
        bad = [f"{where}: unknown key `{k}`" for k in e if k not in KEYS]
        name = e.get("name")
        if not isinstance(name, str) or not name.strip():
            bad.append(f"{where} needs a non-empty `name`")
        elif name in seen:
            bad.append(f"{where}: name {name!r} appears more than once")
        else:
            seen.add(name)
        label = f"{where} ({name})" if isinstance(name, str) and name else where
        if e.get("level") not in LEVELS:
            bad.append(f"{label}: `level` must be one of {', '.join(LEVELS)}")
        if e.get("when") not in WHEN:
            bad.append(f"{label}: `when` must be one of {', '.join(WHEN)}")
        run = e.get("run")
        if not isinstance(run, list) or not run or any(not isinstance(x, str) or not x for x in run):
            bad.append(f"{label}: `run` must be a non-empty list of strings (an argument list, never one shell string)")
        desc = e.get("description", "")
        if not isinstance(desc, str):
            bad.append(f"{label}: `description` must be a string")
        timeout = e.get("timeout", DEFAULT_TIMEOUT)
        if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout < 1:
            bad.append(f"{label}: `timeout` must be a positive whole number of seconds")
        if e.get("stdin", "none") not in STDIN:
            bad.append(f"{label}: `stdin` must be one of {', '.join(STDIN)}")
        scope = e.get("scope")
        if scope is not None and (not isinstance(scope, str) or not scope.strip()):
            bad.append(f"{label}: `scope` must be a non-empty string")
        if bad:
            problems += bad
            continue
        checks.append(Check(name, e["level"], e["when"], tuple(run), desc, timeout, e.get("stdin", "none"), scope))
    return checks, problems


def selected(checks: list[Check], when: str, only: str | None = None, scope: str | None = None) -> list[Check]:
    """The checks for `when`; without `scope` only unscoped ones, with it only that scope; `only` narrows to one name."""
    return [c for c in checks if c.when == when and c.scope == scope and (not only or c.name == only)]


def git_command_line() -> str:
    """The command line of the nearest `git` process above this one (for example `git commit --amend`), or "" when there is none.

    A git hook does not learn how it was invoked; some checks need to know (an amend compares against the parent commit). The
    answer comes from the process table (`/proc`, Linux): best effort, empty elsewhere.
    """
    pid = os.getppid()
    for _ in range(12):
        try:
            argv = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
            if argv and os.path.basename(argv[0].decode("utf-8", "replace")) == "git":
                return " ".join(a.decode("utf-8", "replace") for a in argv if a)
            stat = Path(f"/proc/{pid}/stat").read_text()
            pid = int(stat.rsplit(")", 1)[1].split()[1])           # the parent pid follows the state letter
        except (OSError, ValueError, IndexError):
            return ""
        if pid <= 1:
            return ""
    return ""


PLACEHOLDERS = ("{bundle}", "{cwd}", "{tmpdir}", "{git_command}")


def expand(arg: str, cwd: Path, bundle: Path, tmpdir: str = "", git_command: str = "") -> str:
    """Plain text substitution in one argument (no shell, no other expansion)."""
    return (arg.replace("{bundle}", str(bundle)).replace("{cwd}", str(cwd)).replace("{tmpdir}", tmpdir)
            .replace("{git_command}", git_command))


def run_checks(checks: list[Check], when: str, cwd: Path, bundle: Path, only: str | None = None, scope: str | None = None,
               stdin_data: bytes = b"") -> list[Result]:
    """Run the checks for `when` (and `scope`, and `only` that name) in `cwd`. The bundle path is passed as `ACKIT_BUNDLE`;
    a check with `stdin: pass` gets `stdin_data`, any other gets no input."""
    env = {**os.environ, "ACKIT_BUNDLE": str(bundle), "ACKIT_CHECK_WHEN": when}
    out = []
    for c in selected(checks, when, only, scope):
        t0 = time.monotonic()
        output = ""
        try:
            tmp = tempfile.mkdtemp(prefix="ackit-check-") if any("{tmpdir}" in a for a in c.run) else ""
            git_cmd = git_command_line() if any("{git_command}" in a for a in c.run) else ""
            argv = [expand(a, cwd, bundle, tmp, git_cmd) for a in c.run]
            p = subprocess.Popen(argv, cwd=cwd, env=env, shell=False, stdin=subprocess.PIPE if c.stdin == "pass" else subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                raw, _ = p.communicate(input=stdin_data if c.stdin == "pass" else None, timeout=c.timeout)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(p.pid, signal.SIGKILL)         # the command and everything it started
                except OSError:
                    p.kill()
                p.communicate()
                ok, detail = False, f"timed out after {c.timeout}s"
            else:
                output = raw[-MAX_OUTPUT:].decode("utf-8", errors="replace")
                last = (output.strip().splitlines() or [""])[-1]
                ok = p.returncode == 0
                detail = last if ok else (f"exit {p.returncode}: {last}" if last else f"exit {p.returncode}")
        except OSError as exc:
            ok, detail = False, f"could not run: {exc}"
        finally:
            if tmp:
                shutil.rmtree(tmp, ignore_errors=True)            # also after a timeout kill: the wrapper cannot clean up after SIGKILL
        out.append(Result(c, ok, detail, round(time.monotonic() - t0, 2), output))
    return out


def failed(results: list[Result]) -> bool:
    """True when a `block` check failed; a failing `warn` check does not fail the run."""
    return any(not r.passed and r.check.level == "block" for r in results)
