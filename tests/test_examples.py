from pathlib import Path

import pytest

from ackit.bundle import Bundle
from ackit.cli import main
from ackit.validate import validate

ROOT = Path(__file__).parent.parent


@pytest.mark.parametrize("path", ["examples/small/context", "examples/large/context", "docs"])
def test_shipped_bundles_validate_strict(path):
    assert main(["validate", str(ROOT / path), "--strict"]) == 0


def test_core_has_no_adopter_specifics():
    import re
    # Generic patterns always; adopter names come from an optional, untracked file (one regex per line).
    terms = [r"\bbitbucket\b", r"agent-context/"]
    extra = ROOT / "tests" / ".leakage-terms"
    if extra.is_file():
        terms += [t.strip() for t in extra.read_text().splitlines() if t.strip()]
    bad = re.compile("|".join(terms), re.I)
    hits = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT).as_posix()
        if (not p.is_file() or rel.startswith((".git/", ".venv/", "adopters/", ".pytest_cache/")) or "__pycache__" in rel
                or "egg-info" in rel or p.is_symlink() or rel == "tests/test_examples.py"):
            continue
        if bad.search(p.read_text(errors="ignore")):
            hits.append(rel)
    assert hits == []
