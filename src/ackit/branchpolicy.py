"""Branch policy and pure branch resolvers (ACF 1.3, ADR-0015, ADR-0016).

`ackit.yaml` may carry

    branch_policy:
      work_branch:
        base_stage: uat                          # default: the registry's default stage
        name_pattern: "{author}-{environment}-{task}"
      context_branch:
        base: matching-code-base-branch          # or default-branch
        fallback: main
        name_pattern: "{author}-{code_branch}"
        required_before_code_push: true

Names are built by substitution only: the caller checks that a name is a valid git ref. The functions here take facts as arguments (the registry, the branches that exist) and return names. They run no git, open no
file and use no network; the caller reads the repository and creates the branches.
"""
from __future__ import annotations

import string
from dataclasses import dataclass

from .registry import Registry, RegistryError

WORK_FIELDS = {"author", "environment", "task"}
CONTEXT_FIELDS = {"author", "code_branch"}
CONTEXT_BASES = ("matching-code-base-branch", "default-branch")
DEFAULTS = {
    "work_branch": {"base_stage": None, "name_pattern": "{author}-{environment}-{task}"},
    "context_branch": {"base": "matching-code-base-branch", "fallback": "main", "name_pattern": "{author}-{code_branch}",
                       "required_before_code_push": False},
}


class BranchPolicyError(ValueError):
    """A branch cannot be resolved from the given facts (missing input, unknown environment or stage)."""


def _fields(pattern: str) -> set[str] | None:
    """The placeholder names of a plain pattern, or None when it uses format specs, conversions or is malformed."""
    try:
        parsed = list(string.Formatter().parse(pattern))
    except ValueError:
        return None
    if any(f is not None and (spec or conv) for _, f, spec, conv in parsed):
        return None
    return {f for _, f, _, _ in parsed if f is not None}


def _not_empty(**given) -> None:
    for k, v in given.items():
        if v is not None and not str(v).strip():
            raise BranchPolicyError(f"`{k}` is given but empty")


def policy(config: dict) -> tuple[dict, list[str]]:
    """The effective policy (defaults merged with the `branch_policy` block) and the problems with the block."""
    out = {k: dict(v) for k, v in DEFAULTS.items()}
    raw = (config or {}).get("branch_policy")
    if raw is None:
        return out, []
    if not isinstance(raw, dict):
        return out, [f"`branch_policy` must be a mapping, got {type(raw).__name__}"]
    problems = [f"`branch_policy.{k}` is not a known key (known: {', '.join(DEFAULTS)})" for k in raw if k not in DEFAULTS]
    for section, allowed in (("work_branch", WORK_FIELDS), ("context_branch", CONTEXT_FIELDS)):
        block = raw.get(section)
        if block is None:
            continue
        if not isinstance(block, dict):
            problems.append(f"`branch_policy.{section}` must be a mapping")
            continue
        for k, v in block.items():
            where = f"`branch_policy.{section}.{k}`"
            if k not in DEFAULTS[section]:
                problems.append(f"{where} is not a known key (known: {', '.join(DEFAULTS[section])})")
            elif k == "name_pattern":
                fields = _fields(v) if isinstance(v, str) else None
                if fields is None or not fields <= allowed or not fields:
                    problems.append(f"{where} must be a pattern using only {', '.join('{' + f + '}' for f in sorted(allowed))}")
                else:
                    out[section][k] = v
            elif k == "base":
                if v not in CONTEXT_BASES:
                    problems.append(f"{where} must be one of {', '.join(CONTEXT_BASES)}")
                else:
                    out[section][k] = v
            elif k == "required_before_code_push":
                if not isinstance(v, bool):
                    problems.append(f"{where} must be true or false")
                else:
                    out[section][k] = v
            elif not isinstance(v, str) or not v:
                problems.append(f"{where} must be a non-empty string")
            else:
                out[section][k] = v
    return out, problems


@dataclass(frozen=True)
class WorkBranch:
    base: str                 # the branch to create the work branch from
    stage: str
    name: str | None          # None when no author or task was given


@dataclass(frozen=True)
class ContextBranch:
    base: str                 # the store branch to create the context branch from
    base_is_fallback: bool
    name: str | None
    required_before_code_push: bool


def resolve_work_branch(registry: Registry, pol: dict, environment: str, repository: str | None = None, stage: str | None = None,
                        author: str | None = None, task: str | None = None) -> WorkBranch:
    cfg = pol["work_branch"]
    stage = stage or cfg["base_stage"] or registry.default_stage
    if not stage:
        raise BranchPolicyError("no stage given, none in `branch_policy.work_branch.base_stage` and the registry has no default_stage")
    try:
        base = registry.branch(environment, repository, stage)
    except RegistryError as exc:
        raise BranchPolicyError(str(exc)) from None
    _not_empty(author=author, task=task)
    name = cfg["name_pattern"].format(author=author, environment=environment, task=task) if author and task else None
    return WorkBranch(base, stage, name)


def resolve_context_branch(pol: dict, code_base_branch: str, author: str | None = None, code_branch: str | None = None,
                           existing_branches: list[str] | tuple[str, ...] = ()) -> ContextBranch:
    """The store branch to start from. `existing_branches` are the store's branch names, listed by the caller."""
    cfg = pol["context_branch"]
    if not code_base_branch:
        raise BranchPolicyError("the code base branch is needed to pick the store branch")
    matches = cfg["base"] == "matching-code-base-branch" and code_base_branch in set(existing_branches)
    _not_empty(author=author, code_branch=code_branch)
    name = cfg["name_pattern"].format(author=author, code_branch=code_branch) if author and code_branch else None
    return ContextBranch(code_base_branch if matches else cfg["fallback"], not matches, name, cfg["required_before_code_push"])
