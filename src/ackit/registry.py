"""Environment registry for the shared store (ACF 1.3, ADR-0015, ADR-0016).

`ackit.yaml` may carry

    environment_registry:
      default_stage: uat                  # inline data ...
      repos: [app, ui]                    # inline keys are the first parts of the key paths (default: repos)
      environments:
        - id: acme
          repo: app
          code_line: line-a
          stages: {uat: {branches: {app: release/uat, ui: release/uat}}}
      # ... or, instead, read an adopter's own file (opt-in, read-only, may be outside the bundle):
      # source_file: ../environments/registry.yaml
      # key_paths: {default_stage: defaults.development_stage, repositories: code_repos}

Inline data and `source_file` resolve to the same model. `key_paths` map the adopter's own shape onto it; the defaults are the
generic shape agent-orchestly's yaml adapter reads. The core only reads and validates: no git, no network, and the one file named
by `source_file` is the only file opened. Anything under `extensions` is carried and never interpreted.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DEFAULT_KEY_PATHS = {
    "default_stage": "default_stage",
    "repositories": "repos",
    "environments": "environments",
    "id": "id",
    "repository": "repo",
    "code_line": "code_line",
    "branches": "stages.${stage}.branches.${repo}",
}
INLINE_KEYS = ("default_stage", "repositories", "environments", "extensions")


class RegistryError(ValueError):
    """The registry cannot be read or resolved as configured; the message says what and where."""


def get_path(data, path: str, default=None):
    """Dotted lookup in nested mappings; `default` when any step is missing."""
    cur = data
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


@dataclass(frozen=True)
class Environment:
    id: str
    repository: str
    code_line: str | None
    branches: dict[str, dict[str, str]]          # stage -> repository -> branch

    def branch(self, repository: str, stage: str) -> str:
        if stage not in self.branches:
            raise RegistryError(f"environment {self.id!r} has no stage {stage!r} (known: {', '.join(sorted(self.branches)) or 'none'})")
        by_repo = self.branches[stage]
        if repository not in by_repo:
            raise RegistryError(f"environment {self.id!r} has no branch for repository {repository!r} at stage {stage!r}")
        return by_repo[repository]


@dataclass(frozen=True)
class Registry:
    default_stage: str | None
    repositories: tuple[str, ...]
    environments: tuple[Environment, ...]
    extensions: dict = field(default_factory=dict)

    def environment(self, env_id: str) -> Environment:
        for e in self.environments:
            if e.id == env_id:
                return e
        raise RegistryError(f"environment {env_id!r} is not in the registry (known: {', '.join(e.id for e in self.environments) or 'none'})")

    def stages(self) -> list[str]:
        return sorted({s for e in self.environments for s in e.branches})

    def branch(self, env_id: str, repository: str | None = None, stage: str | None = None) -> str:
        """The branch of `repository` (default: the environment's own) for `env_id` at `stage` (default: the default stage)."""
        env = self.environment(env_id)
        stage = stage or self.default_stage
        if not stage:
            raise RegistryError("no stage given and the registry has no default_stage")
        return env.branch(repository or env.repository, stage)


def key_paths(raw: dict) -> tuple[dict[str, str], list[str]]:
    """The effective key paths (defaults plus the adopter's) and the problems with the adopter's."""
    out, problems = dict(DEFAULT_KEY_PATHS), []
    given = raw.get("key_paths")
    if given is None:
        return out, problems
    if not isinstance(given, dict):
        return out, [f"`environment_registry.key_paths` must be a mapping, got {type(given).__name__}"]
    for k, v in given.items():
        if k not in DEFAULT_KEY_PATHS:
            problems.append(f"`environment_registry.key_paths.{k}` is not a known key path (known: {', '.join(DEFAULT_KEY_PATHS)})")
        elif not isinstance(v, str) or not v:
            problems.append(f"`environment_registry.key_paths.{k}` must be a non-empty dotted path")
        else:
            out[k] = v
    parts = out["branches"].split(".")
    if parts.count("${stage}") != 1 or parts.count("${repo}") != 1 or (
            "${stage}" in parts and "${repo}" in parts and parts.index("${stage}") > parts.index("${repo}")):
        problems.append("`environment_registry.key_paths.branches` must hold `${stage}` and then `${repo}`, each once, as whole dotted parts")
        out["branches"] = DEFAULT_KEY_PATHS["branches"]
    for k in ("default_stage", "repositories", "environments"):
        if out[k].split(".")[0] == "extensions":
            problems.append(f"`environment_registry.key_paths.{k}` must not start with `extensions`: that key is carried and never read")
            out[k] = DEFAULT_KEY_PATHS[k]
    return out, problems


def _stage_branches(env: dict, template: str, problems: list[str], eid: str) -> dict[str, dict[str, str]]:
    """Enumerate stage -> repository -> branch from `template` (a dotted path with `${stage}` and `${repo}`)."""
    parts = template.split(".")
    si, ri = parts.index("${stage}"), parts.index("${repo}")     # validated by key_paths()
    stages = get_path(env, ".".join(parts[:si]), env if si == 0 else None)
    out: dict[str, dict[str, str]] = {}
    if stages is None:
        return out
    if not isinstance(stages, dict):
        problems.append(f"environment {eid!r}: the stages (before `${{stage}}` in the branches path) must be a mapping")
        return out
    for stage, node in stages.items():
        repos = get_path(node, ".".join(parts[si + 1:ri]), node if ri == si + 1 else None)
        if repos is None:
            continue
        if not isinstance(repos, dict):
            problems.append(f"environment {eid!r}, stage {stage!r}: the repositories must be a mapping of repository to branch")
            continue
        tail = ".".join(parts[ri + 1:])
        for repo, value in repos.items():
            v = get_path(value, tail) if tail else value
            if v is None or v == "":
                continue
            if not isinstance(v, str):
                problems.append(f"environment {eid!r}, stage {stage!r}, repository {repo!r}: the branch must be a string, got {type(v).__name__}")
                continue
            out.setdefault(str(stage), {})[str(repo)] = v
    return out


def inline_keys(kp: dict[str, str]) -> tuple[str, ...]:
    """Top-level keys inline data may use: where the key paths start, plus `extensions`."""
    return tuple(dict.fromkeys([kp[k].split(".")[0] for k in ("default_stage", "repositories", "environments")] + ["extensions"]))


def read_raw(raw: dict, bundle_root: Path | None, inline_ks: tuple[str, ...] = INLINE_KEYS) -> tuple[dict, str | None]:
    """The data the model is built from: the inline keys, or the content of `source_file`. Returns (data, source path)."""
    src = raw.get("source_file")
    if src is None:
        return {k: raw[k] for k in inline_ks if k in raw}, None
    if not isinstance(src, str) or not src:
        raise RegistryError("`environment_registry.source_file` must be a path")
    inline = [k for k in inline_ks if k in raw]
    if inline:
        raise RegistryError(f"`environment_registry` has both `source_file` and inline `{inline[0]}`; use one")
    p = Path(src).expanduser()
    if not p.is_absolute():
        p = (bundle_root or Path.cwd()) / p
    if not p.is_file():
        raise RegistryError(f"environment_registry.source_file not found: {p}")
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        raise RegistryError(f"environment_registry.source_file {p} cannot be read: {exc}") from None
    except yaml.YAMLError as exc:
        raise RegistryError(f"environment_registry.source_file {p} is not valid YAML: {exc}") from None
    if not isinstance(data, dict):
        raise RegistryError(f"environment_registry.source_file {p} must hold a mapping at the top level")
    return data, str(p)


def build(config: dict, bundle_root: Path | None = None) -> tuple[Registry | None, list[str]]:
    """Build the registry from the `environment_registry` block. (None, []) when the block is absent.

    Returns (registry or None, problems). A fatal problem (unreadable file) gives (None, [problem]); validation problems in
    otherwise readable data are listed and the registry is still returned.
    """
    raw = (config or {}).get("environment_registry")
    if raw is None:
        return None, []
    if not isinstance(raw, dict):
        return None, [f"`environment_registry` must be a mapping, got {type(raw).__name__}"]
    kp, kp_problems = key_paths(raw)
    iks = inline_keys(kp)
    problems = [f"`environment_registry.{k}` is not a known key" for k in raw if k not in set(iks) | {"source_file", "key_paths"}]
    problems += kp_problems
    try:
        data, _ = read_raw(raw, bundle_root, iks)
    except RegistryError as exc:
        return None, problems + [str(exc)]
    # the model lives under the adopter's key paths; inline data uses them too, so the two forms read alike
    stage = get_path(data, kp["default_stage"])
    if stage is not None and not isinstance(stage, str):
        problems.append(f"`{kp['default_stage']}` (default stage) must be a string")
        stage = None
    repos = get_path(data, kp["repositories"], [])
    if isinstance(repos, dict):
        repos = list(repos)
    if not isinstance(repos, list):
        problems.append(f"`{kp['repositories']}` must be a list or a mapping of repository names")
        repos = []
    envs_raw = get_path(data, kp["environments"], [])
    if not isinstance(envs_raw, list):
        problems.append(f"`{kp['environments']}` must be a list of environments")
        envs_raw = []
    envs: list[Environment] = []
    seen: set[str] = set()
    for n, e in enumerate(envs_raw):
        if not isinstance(e, dict):
            problems.append(f"`{kp['environments']}[{n}]` must be a mapping")
            continue
        eid = e.get(kp["id"])
        if eid is None or str(eid) == "":
            problems.append(f"`{kp['environments']}[{n}]` has no `{kp['id']}`")
            continue
        eid = str(eid)
        if eid in seen:
            problems.append(f"environment id {eid!r} appears more than once")
            continue
        seen.add(eid)
        repo = e.get(kp["repository"])
        if not repo:
            problems.append(f"environment {eid!r} has no `{kp['repository']}`")
            continue
        branches = _stage_branches(e, kp["branches"], problems, eid)
        code_line = e.get(kp["code_line"])
        envs.append(Environment(eid, str(repo), str(code_line) if code_line else None, branches))
    if stage and envs and stage not in {s for env in envs for s in env.branches}:
        problems.append(f"default stage {stage!r} is not a stage of any environment")
    ext = data.get("extensions", {})
    if not isinstance(ext, dict):
        problems.append("`extensions` must be a mapping")
        ext = {}
    if any(not isinstance(r, str) or not r for r in repos):
        problems.append(f"`{kp['repositories']}` must hold non-empty repository names")
    return Registry(stage, tuple(str(r) for r in repos), tuple(envs), ext), problems
