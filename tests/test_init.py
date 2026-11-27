import pytest
import yaml

from ackit.cli import main
from ackit.bundle import Bundle
from ackit.init import detect_pack, init_bundle, load_packs
from ackit.validate import validate
from conftest import NOW, mk


def errors(root):
    return [i for i in validate(Bundle.load(root), now=NOW) if i.severity == "error"]


@pytest.mark.parametrize("fx,pack,size", [("java_repo", "java-spring", "large"), ("node_repo", "node-react", "large"),
                                          ("py_repo", "python", "small"), ("go_repo", "go", "small"), ("plain_repo", "generic", "small")])
def test_init_detects_and_validates(request, fx, pack, size):
    repo = request.getfixturevalue(fx)
    r = init_bundle(repo, repo / "context", answers={"owner": "alice"}, now=NOW)
    assert (r["pack"], r["size"]) == (pack, size)
    assert errors(repo / "context") == []
    assert (repo / "context" / "AGENTS.md").exists() and (repo / "context" / "index.md").exists()
    if size == "large":
        assert len(r["modules"]) == 2 and len(list((repo / "context" / "modules").glob("*.md"))) == 2


def test_java_without_spring_falls_back_to_generic(tmp_path):
    repo = mk(tmp_path / "j", {"pom.xml": "<project/>"})
    assert detect_pack(repo, load_packs())[0]["name"] == "generic"


def test_commands_from_pack_and_build_tool(java_repo):
    r = init_bundle(java_repo, java_repo / "context", answers={"owner": "a"}, now=NOW)
    assert r["variant"] == "gradle" and r["commands"]["test"] == "./gradlew test"


def test_answers_file_noninteractive(py_repo, tmp_path):
    a = tmp_path / "answers.yaml"
    a.write_text(yaml.safe_dump({"project": "Demo", "purpose": "Does demos", "owner": "bob", "size": "small", "commands": {"test": "make test"}}))
    assert main(["init", str(py_repo), "--answers", str(a)]) == 0
    wf = (py_repo / "context" / "workflow.md").read_text()
    assert "make test" in wf
    assert "Does demos" in (py_repo / "context" / "product.md").read_text()


def test_refuses_nonempty_dir(py_repo):
    init_bundle(py_repo, py_repo / "context", now=NOW)
    assert main(["init", str(py_repo)]) == 2


def test_pack_added_without_code(py_repo, tmp_path):
    packs = tmp_path / "mypacks"
    (packs / "rust" / "rules").mkdir(parents=True)
    (packs / "rust" / "pack.yaml").write_text(yaml.safe_dump({"name": "rust", "priority": 30, "detect": {"any_files": ["Cargo.toml"]},
        "stack": {"languages": ["Rust"], "frameworks": []}, "variants": {"cargo": {"detect_files": ["Cargo.toml"], "workflow": {"build": "cargo build", "test": "cargo test", "lint": "cargo clippy", "run": ""}}}}))
    (packs / "rust" / "rules" / "no-unwrap.md").write_text('---\ntitle: "No unwrap in library code"\nseverity: blocking\napplies_to: [developer]\n---\n## Rule\n\nNo unwrap().\n\n## Why\n\nPanics.\n\n## How to check\n\nclippy.\n')
    repo = mk(tmp_path / "rs", {"Cargo.toml": "[package]\n"})
    r = init_bundle(repo, repo / "context", extra_packs=[packs], now=NOW)
    assert r["pack"] == "rust" and (repo / "context/rules/no-unwrap.md").exists()
    assert errors(repo / "context") == []
