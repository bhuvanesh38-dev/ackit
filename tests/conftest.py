import datetime as dt
from pathlib import Path

import pytest

from ackit.bundle import Bundle
from ackit.init import init_bundle
from ackit.scaffold import dump_doc, iso

NOW = dt.datetime(2026, 11, 17, tzinfo=dt.timezone.utc)


def mk(root: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return root


@pytest.fixture
def java_repo(tmp_path):
    return mk(tmp_path / "javarepo", {"build.gradle": "plugins { id 'org.springframework.boot' }\n", "settings.gradle": "include 'core', 'web'\n",
                                      "core/build.gradle": "", "web/build.gradle": ""})


@pytest.fixture
def node_repo(tmp_path):
    return mk(tmp_path / "noderepo", {"package.json": '{"name":"x","workspaces":["packages/*"],"dependencies":{"react":"18"}}',
                                      "packages/ui/package.json": "{}", "packages/api/package.json": "{}"})


@pytest.fixture
def py_repo(tmp_path):
    return mk(tmp_path / "pyrepo", {"pyproject.toml": "[project]\nname='x'\n", "src/x/__init__.py": ""})


@pytest.fixture
def go_repo(tmp_path):
    return mk(tmp_path / "gorepo", {"go.mod": "module x\n", "main.go": "package main\n"})


@pytest.fixture
def plain_repo(tmp_path):
    return mk(tmp_path / "plain", {"README.txt": "hi\n"})


@pytest.fixture
def good(py_repo):
    """A freshly initialised small bundle (valid)."""
    init_bundle(py_repo, py_repo / "context", answers={"owner": "alice", "purpose": "Demo"}, now=NOW)
    return py_repo / "context"


def put(root: Path, rel: str, meta: dict, body: str = "") -> Path:
    meta = {"generated": {"by": "test/1", "at": iso(NOW)}, **meta}
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(dump_doc(meta, body or "# x"))
    return p


def feature_body():
    return "## Goal\n\ng\n\n## Acceptance criteria\n\n- a\n\n## Design\n\nd\n\n## Plan\n\n1. p\n\n## Test plan\n\nt\n"


def feature(root, ident="F-001", **over):
    meta = {"type": "feature", "id": ident, "title": "T", "status": "draft", "tier": "small", "description": "d"}
    meta.update(over)
    return put(root, f"work/features/{ident}-t.md", meta, feature_body())


def load(root) -> Bundle:
    return Bundle.load(root)
