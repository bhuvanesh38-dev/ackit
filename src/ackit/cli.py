"""ackit command line."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

from . import __version__
from .bundle import Bundle, load_registry
from .gates import check_gate
from .idalloc import DEFAULT_RANGE_SIZE, IdAllocationError, assign_range
from .importer import import_store
from .okf import export_okf, import_okf
from .init import detect_pack, init_bundle, load_answers, load_packs
from .prompt import build_prompt
from .scaffold import new_doc, new_large_feature, set_status, verify_doc, write_index, build_index, log_entry
from .validate import DEFAULT_SEVERITY, RULE_TEXT, exit_code, validate


def _bundle(args) -> Bundle:
    return Bundle.load(args.bundle)


def cmd_init(a) -> int:
    repo = Path(a.repo)
    bundle = Path(a.bundle) if a.bundle else repo / "context"
    answers = load_answers(a.answers)
    try:
        r = init_bundle(repo, bundle, answers=answers, interactive=(not a.yes and not a.answers and sys.stdin.isatty()),
                        pack_name=a.pack, extra_packs=[Path(p) for p in a.pack_dir or []], force=a.force, link_entry=a.link_entry)
    except FileExistsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(f"pack: {r['pack']} ({r['variant']}); size: {r['size']}; modules: {[m['name'] for m in r['modules']] or 'none'}")
    print(f"asked: {r['asked'] or 'nothing'}; inferred: {r['inferred']}")
    print(f"created {len(r['created'])} files in {bundle}")
    print(f"next: edit the draft documents, then `ackit verify <doc> --by human:<you> --status stable`, then `ackit validate {bundle}`")
    return 0


def cmd_validate(a) -> int:
    try:
        b = _bundle(a)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    issues = validate(b)
    if a.code_line:
        from .codelines import applies_to_line, unknown_line_message
        from .registry import build
        msg = unknown_line_message(build(b.config, b.root)[0], a.code_line)
        if msg:
            print(f"error: {msg}", file=sys.stderr)
            return 2
        off = {d.rel for d in b.docs if not applies_to_line(d.meta, a.code_line)}
        issues = [i for i in issues if i.path not in off]
    if a.json:
        print(json.dumps([i.as_dict() for i in issues], indent=2))
    else:
        for i in issues:
            print(i)
        e = sum(i.severity == "error" for i in issues)
        w = sum(i.severity == "warn" for i in issues)
        print(f"{len(b.docs)} documents: {e} error(s), {w} warning(s)")
    return exit_code(issues, a.strict)


def cmd_check(a) -> int:
    b = _bundle(a)
    r = check_gate(b, a.gate, a.item, role=a.role)
    if a.json:
        print(json.dumps(r.as_dict(), indent=2))
    else:
        for c in r.checks:
            print(f"{c.level.upper():4} {c.name}: {c.detail}")
        print(f"gate {a.gate} for {a.item}: {'PASS' if r.passed else 'FAIL'}")
    return 0 if r.passed else 1


def cmd_prompt(a) -> int:
    b = _bundle(a)
    ex: list = []
    if a.part:  # one named part of the role (today: wrap-up), not the whole prompt
        from .roles import KINDS, load_role
        try:
            text = load_role(b, a.role).text(a.part)
        except LookupError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        if not text:
            print(f"error: role '{a.role}' has no {a.part} (no overlay file, no kit default)", file=sys.stderr)
            return 1
        print(text)
        return 0
    if a.code_line:
        from .codelines import unknown_line_message
        from .registry import build
        msg = unknown_line_message(build(b.config, b.root)[0], a.code_line)
        if msg:
            print(f"error: {msg}", file=sys.stderr)
            return 2
    try:
        out = build_prompt(b, a.role, a.item, a.budget, explain=ex if a.explain else None, code_line=a.code_line)
    except (LookupError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if a.explain:
        print(f"# ackit prompt --explain: role={a.role} item={a.item or '-'}")
        for what, kind, why in ex:
            print(f"- {what}: {kind} ({why})")
        return 0
    if a.out:
        Path(a.out).write_text(out)
    else:
        sys.stdout.write(out)
    return 0


def cmd_new(a) -> int:
    root = Path(a.bundle)
    extras = {}
    for kv in a.set or []:
        k, _, v = kv.partition("=")
        extras[k] = yaml.safe_load(v)
    if a.tier:
        extras["tier"] = a.tier
    author = a.author or os.environ.get("ACKIT_AUTHOR")
    try:
        if a.type == "feature" and a.tier == "large":
            paths = new_large_feature(root, a.title, extras, slug=a.slug, author=author)
        else:
            paths = [new_doc(root, a.type, a.title, extras=extras, guide=not a.no_guide, slug=a.slug, author=author)]
    except FileExistsError as e:
        print(f"error: exists: {e}", file=sys.stderr)
        return 2
    except IdAllocationError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    for p in paths:
        print(p)
    write_index(Bundle.load(root))
    return 0


def cmd_ids_assign(a) -> int:
    try:
        low, high, note = assign_range(Path(a.bundle) / "ackit.yaml", a.author, a.size)
    except IdAllocationError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(f"{a.author}: [{low}, {high}] added to {Path(a.bundle) / 'ackit.yaml'}")
    if note:
        print(f"note: {note}", file=sys.stderr)
    print("next: merge this change to the shared branch before {} creates items, so no other branch picks the same block".format(a.author), file=sys.stderr)
    return 0


def cmd_branch_resolve(a) -> int:
    from .branchpolicy import BranchPolicyError, policy, resolve_context_branch, resolve_work_branch
    from .registry import build
    b = Bundle.load(a.bundle)
    reg, problems = build(b.config, b.root)
    pol, pol_problems = policy(b.config)
    if reg is None or problems or pol_problems:
        for m in (problems or ["no `environment_registry` is configured in ackit.yaml"]) + pol_problems:
            print(f"error: {m}", file=sys.stderr)
        return 2
    existing = list(a.existing_branch or [])
    if a.existing_branches_file:
        try:
            src = sys.stdin.read() if a.existing_branches_file == "-" else Path(a.existing_branches_file).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"error: cannot read the branch list {a.existing_branches_file}: {e}", file=sys.stderr)
            return 2
        existing += [l.strip() for l in src.splitlines() if l.strip()]
    try:
        work = resolve_work_branch(reg, pol, a.environment, a.repository, a.stage, a.author, a.task)
        base_used = a.code_base_branch or work.base
        ctx = resolve_context_branch(pol, base_used, a.author, a.code_branch, existing)
    except BranchPolicyError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    out = {"code_base_branch": base_used, "work_branch": {"base": work.base, "stage": work.stage, "name": work.name},
           "context_branch": {"base": ctx.base, "base_is_fallback": ctx.base_is_fallback, "name": ctx.name,
                              "required_before_code_push": ctx.required_before_code_push}}
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"code base branch: {base_used}" + ("" if a.code_base_branch else " (the work branch base; none given)"))
        print(f"work branch: {work.name or '(give --author and --task for a name)'} from {work.base} (stage {work.stage})")
        print(f"context branch: {ctx.name or '(give --author and --code-branch for a name)'} from {ctx.base}"
              + (" (fallback: no store branch matches the code base branch)" if ctx.base_is_fallback else ""))
        print(f"store pull request required before the code push: {'yes' if ctx.required_before_code_push else 'no'}")
    return 0


def cmd_checks_run(a) -> int:
    from .checks import failed, parse, run_checks, selected
    b = Bundle.load(a.bundle)
    checks, problems = parse(b.config)
    if problems:
        for m in problems:
            print(f"error: {m}", file=sys.stderr)
        return 2
    if a.scope is not None and not any(c.scope == a.scope for c in checks):
        print(f"error: no process check has the scope {a.scope!r}", file=sys.stderr)
        return 2
    if a.name and not any(c.name == a.name for c in checks):
        print(f"error: no process check named {a.name!r} (known: {', '.join(c.name for c in checks) or 'none'})", file=sys.stderr)
        return 2
    named = next((c for c in checks if c.name == a.name), None) if a.name else None
    if named and named.when != a.when:
        print(f"error: process check {a.name!r} runs at {named.when}, not {a.when}; pass --when {named.when}", file=sys.stderr)
        return 2
    if named and named.scope != a.scope:
        print(f"error: process check {a.name!r} has scope {named.scope!r}; pass --scope {named.scope}" if named.scope
              else f"error: process check {a.name!r} has no scope; leave --scope out", file=sys.stderr)
        return 2
    cwd = Path(a.cwd).resolve() if a.cwd else b.root.parent
    stdin_data = b""
    if any(c.stdin == "pass" for c in selected(checks, a.when, a.name, a.scope)) and sys.stdin is not None and not sys.stdin.isatty():
        stdin_data = sys.stdin.buffer.read()            # read once; every check with `stdin: pass` gets the same bytes
    results = run_checks(checks, a.when, cwd, b.root, a.name, a.scope, stdin_data)
    if not results:
        print(f"warning: no process check matched --when {a.when}" + (f" --scope {a.scope}" if a.scope else "") + "; nothing was checked", file=sys.stderr)
    if a.json:
        print(json.dumps([{"name": r.check.name, "level": r.check.level, "when": r.check.when, "passed": r.passed, "detail": r.detail,
                           "seconds": r.seconds, "output": r.output} for r in results], indent=2))
    else:
        for r in results:
            print(f"{'PASS' if r.passed else 'FAIL'} {r.check.level:5} {r.check.name}: {r.detail or r.check.description}")
            if not r.passed and r.output.strip():
                print("\n".join("    | " + line for line in r.output.rstrip().splitlines()), file=sys.stderr)
        print(f"{len(results)} check(s) for {a.when}: {'FAIL' if failed(results) else 'ok'}")
    return 1 if failed(results) else 0


def cmd_link(a) -> int:
    from .layout import check, config
    try:
        b = Bundle.load(a.bundle)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    cfg, problems = config(b.config)
    if problems:
        for m in problems:
            print(f"error: {m}", file=sys.stderr)
        return 2
    target = Path(a.target).resolve() if a.target else Path.cwd().resolve()
    if target == b.root:
        print("error: the target directory is the bundle itself; pass --target <the directory that should hold the links, e.g. a code clone>", file=sys.stderr)
        return 2
    links = check(cfg, b.root, target)
    if a.json:
        print(json.dumps([{"kind": l.kind, "path": l.path, "state": l.state, "detail": l.detail} for l in links], indent=2))
    else:
        for l in links:
            print(f"{l.state.upper():7} {l.kind:5} {l.path}: {l.detail}")
        print(f"{len(links)} link(s) checked against {target}: {'ok' if all(l.state == 'ok' for l in links) else 'NOT ok'}")
    return 0 if all(l.state == "ok" for l in links) else 1


def cmd_status(a) -> int:
    try:
        r = set_status(Bundle.load(a.bundle), a.item, a.new_status)
    except (LookupError, ValueError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"{r['id']}: {r['old']} -> {r['new']} (history: {' -> '.join(r['history'])})")
    if r["note"]:
        print(f"note: {r['note']}", file=sys.stderr)
    return 0


def cmd_index(a) -> int:
    b = _bundle(a)
    if a.write:
        print(write_index(b))
    else:
        sys.stdout.write(build_index(b))
    return 0


def cmd_verify(a) -> int:
    verify_doc(Path(a.path), a.by, a.status, signoff=a.signoff)
    print(f"verified {a.path} by {a.by}" + (f", status -> {a.status}" if a.status else ""))
    return 0


def cmd_types(a) -> int:
    reg = load_registry()
    if a.markdown:
        print(types_markdown(reg))
    else:
        for n, s in reg["types"].items():
            print(f"{n:15} {s.get('dir') or '(root)':16} {s['purpose']}")
    return 0


def types_markdown(reg: dict) -> str:
    out = ["# ACF document types", "", "Generated from `src/ackit/data/types.yaml` by `ackit types --markdown`. Do not edit by hand.", ""]
    for n, s in reg["types"].items():
        o = s.get("owner", {})
        sset = reg["status_sets"][s.get("status_set", "doc")]
        secs = s.get("sections")
        if isinstance(secs, dict):
            secs = "; ".join(f"{k} {secs['by']}: {', '.join(v)}" for k, v in secs.items() if k != "by")
        else:
            secs = ", ".join(secs or []) or "none required"
        out += [f"## `{n}`", "", s["purpose"], "",
                f"- Directory: `{s.get('dir') or 'bundle root'}`", f"- Required frontmatter: `type`, " + ", ".join(f"`{k}`" for k in s.get("required", [])),
                *([f"- Optional frontmatter: " + ", ".join(f"`{k}`" for k in s["optional"])] if s.get("optional") else []),
                f"- Required sections: {secs}", f"- Statuses: {' -> '.join(sset['values'])}" + (f" (human verification at: {', '.join(sset['human_verified'])})" if sset.get("human_verified") and s.get("human_verified", True) is not False else ""),
                f"- Writes: {o.get('writes')}", f"- Reviews: {o.get('reviews')}", f"- Signs off: {o.get('signs_off')}", f"- Updated: {o.get('updates')}",
                "- Rules for this document:"] + [f"  - {r}" for r in s.get("rules", [])] + [""]
    return "\n".join(out)


def cmd_role(a) -> int:
    from .roles import all_role_names, load_role, overlay_path, scaffold_role, suggested_agent_text, validate_role
    b = Bundle.load(a.bundle) if Path(a.bundle).is_dir() else None
    if a.action == "path":
        if not a.name or b is None:
            print("error: role path needs a role name and an existing bundle", file=sys.stderr)
            return 2
        try:
            load_role(b, a.name)
        except LookupError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        p = overlay_path(b, a.name)
        print(p)
        if not p.is_dir():
            print(f"(no overlay yet for '{a.name}': create the folder to override a part; parts: prompt, rules, checklist, outputs, prompt-guide, wrap-up)", file=sys.stderr)
        return 0
    if a.action == "list" and a.json:
        print(json.dumps([{"name": n, "origin": load_role(b, n).origin, **load_role(b, n).profile} for n in (all_role_names(b) if b else [])], indent=2, default=str))
        return 0
    if a.action == "list":
        for n in all_role_names(b) if b else []:
            r = load_role(b, n)
            print(f"{n:18} {r.origin:8} owns: {', '.join(r.profile.get('owns') or []) or '-':40} gates: {', '.join(r.profile.get('gates') or []) or '-'}  agent: {suggested_agent_text(r) or '-'}")
        return 0
    if a.action == "new":
        if not a.name:
            print("error: role new needs a name", file=sys.stderr)
            return 2
        try:
            paths = scaffold_role(Path(a.bundle), a.name, a.title, a.description, a.extends)
        except (FileExistsError, ValueError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        for p in paths:
            print(p)
        print("next: fill role.yaml (owns, gates), rules, checklist, outputs; then `ackit validate`")
        return 0
    if a.action == "check":
        bad = 0
        for n in ([a.name] if a.name else all_role_names(b)):
            for prob in validate_role(b, load_role(b, n)):
                print(f"{n}: {prob}")
                bad += 1
        print("roles complete" if not bad else f"{bad} problem(s)")
        return 1 if bad else 0
    return 2


def cmd_rules(a) -> int:
    for c in sorted(RULE_TEXT):
        print(f"{c}  {DEFAULT_SEVERITY[c]:5}  {RULE_TEXT[c]}")
    return 0


def cmd_export(a) -> int:
    if not a.okf:
        print("error: export needs --okf <out>", file=sys.stderr)
        return 2
    try:
        r = export_okf(Path(a.bundle), Path(a.okf))
    except (FileExistsError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(f"exported {r['concepts']} concept(s), {r['other_files']} other file(s), {r['roles_files']} role file(s) to {a.okf} (status mapped on {r['status_mapped']})")
    return 0


def cmd_import(a) -> int:
    if a.okf:
        if not a.dest:
            print("error: import --okf needs --dest", file=sys.stderr)
            return 2
        try:
            r = import_okf(Path(a.okf), Path(a.dest))
        except (FileExistsError, FileNotFoundError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        print(f"{r['concepts']} concept(s) imported, {len(r['skipped_no_type'])} skipped (no type), {len(r['placeholders'])} placeholder(s)")
        for x in r["skipped_no_type"][:10]:
            print("  skipped:", x)
        for x in r["placeholders"][:10]:
            print("  needs:", x)
        return 0
    if not a.source or not a.mapping or not a.dest:
        print("error: import needs SOURCE --mapping FILE --dest DIR (or --okf IN --dest DIR)", file=sys.stderr)
        return 2
    mapping = yaml.safe_load(Path(a.mapping).read_text())
    r = import_store(Path(a.source), mapping, Path(a.dest), dry_run=a.dry_run)
    for f in r["files"]:
        print(f"{f['from']} -> {f['to']} ({f['type']})")
    print(f"{len(r['files'])} file(s) mapped, {r['skipped']} skipped, {r['stubs']} section stub(s), {len(r['placeholders'])} placeholder(s)")
    for p in r["placeholders"][:10]:
        print("  needs:", p)
    if "validation" in r:
        print(f"validation after import: {r['validation']}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="ackit", description="Agent Context Kit")
    p.add_argument("--version", action="version", version=f"ackit {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def bundle_arg(sp):
        sp.add_argument("--bundle", default="context", help="bundle directory (default: ./context)")

    s = sub.add_parser("init", help="scaffold a bundle for a repository")
    s.add_argument("repo", nargs="?", default=".")
    s.add_argument("--bundle")
    s.add_argument("--pack")
    s.add_argument("--pack-dir", action="append")
    s.add_argument("--answers", help="YAML file of interview answers (non-interactive)")
    s.add_argument("--yes", action="store_true", help="accept inferred answers, ask nothing")
    s.add_argument("--force", action="store_true")
    s.add_argument("--link-entry", action="store_true", help="symlink ./AGENTS.md to the bundle entry")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("validate", help="check the bundle (exit 1 on errors)")
    s.add_argument("bundle", nargs="?", default="context")
    s.add_argument("--strict", action="store_true", help="warnings fail too")
    s.add_argument("--json", action="store_true")
    s.add_argument("--code-line", help="keep only the findings of documents that apply to this code line (documents without `code_lines` apply to every line)")
    s.set_defaults(fn=cmd_validate)

    s = sub.add_parser("check", help="gate before starting or handing off a work item")
    bundle_arg(s)
    s.add_argument("--gate", required=True, choices=["start", "handoff"])
    s.add_argument("--item", required=True)
    s.add_argument("--role")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("prompt", help="generate a role prompt")
    bundle_arg(s)
    s.add_argument("role")
    s.add_argument("--item")
    s.add_argument("--budget", type=int, help="max characters; bodies are trimmed to fit")
    s.add_argument("--out")
    s.add_argument("--code-line", help="leave out the rules, modules and decisions that name code lines and not this one (ignored with --part)")
    s.add_argument("--explain", action="store_true", help="show which documents are pulled in and why, instead of the prompt")
    s.add_argument("--part", choices=["rules", "checklist", "outputs", "prompt-guide", "wrap-up"],
                   help="print one part of the role (overlay first, then kit default) instead of the prompt; wrap-up is the text an orchestrator sends when a run is stopped at its budget")
    s.set_defaults(fn=cmd_prompt)

    s = sub.add_parser("new", help="create a document from its template")
    bundle_arg(s)
    s.add_argument("type")
    s.add_argument("title")
    s.add_argument("--tier", choices=["small", "large"])
    s.add_argument("--set", action="append", help="frontmatter key=value (YAML value)")
    s.add_argument("--no-guide", action="store_true")
    s.add_argument("--slug", help="file name slug (default: the first words of the title, at most 40 characters)")
    s.add_argument("--author", help="author whose id range is used when `id_allocation` is reserved-range (default: $ACKIT_AUTHOR); `new` is refused without an author when the strategy is reserved-range")
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("ids", help="id allocation helpers (reserved ranges)")
    ids_sub = s.add_subparsers(dest="ids_cmd", required=True)
    s = ids_sub.add_parser("assign", help="give an author the next free id range in ackit.yaml")
    bundle_arg(s)
    s.add_argument("author")
    s.add_argument("--size", type=int, default=DEFAULT_RANGE_SIZE, help="how many ids the range holds (default: %(default)s)")
    s.set_defaults(fn=cmd_ids_assign)

    s = sub.add_parser("branch", help="resolve branch names from the environment registry and the branch policy (offline)")
    br_sub = s.add_subparsers(dest="branch_cmd", required=True)
    s = br_sub.add_parser("resolve", help="print the work branch base and the context branch base and name; runs no git")
    bundle_arg(s)
    s.add_argument("--environment", required=True)
    s.add_argument("--repository", help="default: the environment's own repository")
    s.add_argument("--stage", help="default: branch_policy.work_branch.base_stage, else the registry's default stage")
    s.add_argument("--author")
    s.add_argument("--task", help="with --author, gives the work branch name")
    s.add_argument("--code-base-branch", help="the code branch the work starts from (default: the resolved work branch base)")
    s.add_argument("--code-branch", help="with --author, gives the context branch name")
    s.add_argument("--existing-branch", action="append", help="a branch that exists in the store (repeatable)")
    s.add_argument("--existing-branches-file", help="file with one store branch per line, or - for stdin")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_branch_resolve)

    s = sub.add_parser("checks", help="adopter process checks (commands the adopter listed in ackit.yaml)")
    ch_sub = s.add_subparsers(dest="checks_cmd", required=True)
    s = ch_sub.add_parser("run", help="run the checks for one point; a failing block check exits 1")
    bundle_arg(s)
    s.add_argument("--when", required=True, choices=["pre-commit", "pre-push", "on-demand"])
    s.add_argument("--name", help="run only the check with this name")
    s.add_argument("--scope", help="run the checks with this scope (e.g. `code`); without it only unscoped checks run")
    s.add_argument("--cwd", help="directory the commands run in (default: the parent of the bundle)")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_checks_run)

    s = sub.add_parser("link", help="check that the links a consumer expects (entry file, rules folder) exist and point at the bundle")
    bundle_arg(s)
    s.add_argument("--check", action="store_true", required=True, help="report only; nothing is created (creation: `ackit init --link-entry` or the adopter's installer)")
    s.add_argument("--target", help="directory the links live in, e.g. a code clone (default: the current directory)")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_link)

    s = sub.add_parser("status", help="move a document to a new status, checking the transition and recording history")
    bundle_arg(s)
    s.add_argument("item", help="id (T-001) or path of the document")
    s.add_argument("new_status")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("index", help="print or write index.md")
    bundle_arg(s)
    s.add_argument("--write", action="store_true")
    s.set_defaults(fn=cmd_index)

    s = sub.add_parser("verify", help="record human (or other) verification on a document")
    s.add_argument("path")
    s.add_argument("--by", required=True, help="actor, e.g. human:alice")
    s.add_argument("--status")
    s.add_argument("--signoff", action="store_true", help="also record `signoff` (a person only; never overwritten), e.g. for a task above the auto-start limit")
    s.set_defaults(fn=cmd_verify)

    s = sub.add_parser("export", help="export the bundle to another format (OKF v0.2)")
    bundle_arg(s)
    s.add_argument("--okf", help="output directory for an OKF v0.2 bundle")
    s.set_defaults(fn=cmd_export)

    s = sub.add_parser("types", help="list document types")
    s.add_argument("--markdown", action="store_true")
    s.set_defaults(fn=cmd_types)

    s = sub.add_parser("role", help="list roles, scaffold a custom role, check role definitions, print a role's overlay path")
    s.add_argument("action", choices=["list", "new", "check", "path"])
    s.add_argument("name", nargs="?")
    bundle_arg(s)
    s.add_argument("--title")
    s.add_argument("--description")
    s.add_argument("--extends", help="built-in or custom role whose missing parts this role inherits")
    s.add_argument("--json", action="store_true", help="with `list`: the role profiles as JSON")
    s.set_defaults(fn=cmd_role)

    s = sub.add_parser("rules", help="list validation rule codes")
    s.set_defaults(fn=cmd_rules)

    s = sub.add_parser("import", help="map an existing store (or an OKF bundle) into an ACF bundle")
    s.add_argument("source", nargs="?")
    s.add_argument("--mapping")
    s.add_argument("--okf", help="import an OKF v0.2 bundle from this directory")
    s.add_argument("--dest")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_import)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
