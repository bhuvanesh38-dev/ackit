"""F-005 / T-023: ACF045 checks the shape of a session entry heading; ACF021 is unchanged; the on-hold status set works as documented."""
import pytest

from ackit.bundle import Bundle
from ackit.validate import validate
from conftest import NOW, put

ENTRY = "\n\n**Done:** x\n**Faced:** x\n**Decisions:** x\n**Build:** x\n**Next:** x\n**Blockers:** none\n"
VALID = [
    "2026-11-20 (Fri, W47) - main @ 581a93a - shared-store epic",
    "2026-11-20 (Fri, W47) - release/2026-05-29-x @ 581a93a4c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6 - title with - dashes @ and words",
    "2026-11-20 (Sun, W01) - feature-x @ none - an entry with no commit",
    "2026-11-20 (Mon, W53) - main @ ABCDEF1 - upper-case hex",
    "2026-11-20 (Fri,W47) – main @ 581a93a — en and em dashes",
    "2026-11-20 (Fri, W47) - main @ 581a93a - title with trailing spaces   ",
]
INVALID = [
    "2026-11-20 - main @ 581a93a - no day and week",
    "2026-11-20 (Fri) - main @ 581a93a - no week",
    "2026-11-20 (Fri, W47) - main - no sha",
    "2026-11-20 (Fri, W47) - main @ 58 - sha too short",
    "2026-11-20 (Fri, W47) - main @ 581a93g - sha not hex",
    "2026-11-20 (Fri, W47) - main @ 581a93a41c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7 - sha too long",
    "2026-11-20 (Fri, W47) - main @ 581a93a - ",
    "2026-11-20 (Fri, W47) - @ 581a93a - no branch",
    "2026-11-20 (Fry, W47) - main @ 581a93a - bad day",
    "2026-11-20 (Fri, W54) - main @ 581a93a - bad week",
    "2026-11-20 (Fri, W7) - main @ 581a93a - one-digit week",
    "2026-11-20 (Fri, W47) - main @ unknown - sha word is not none",
    "2026-11-20 (Fri, W47) - my branch @ 581a93a - a branch with a space",
    "2026-11-20 (Fri, W47) - main @ NONE - the word none is lower case",
    "2026-11-20 (Fri, W00) - main @ 581a93a - week zero",
]


def issues(good, head, config=""):
    if config:
        (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text() + config)
    put(good, "sessions/a/b.md", {"type": "session", "title": "s", "author": "a"}, f"## {head}{ENTRY}")
    return [i for i in validate(Bundle.load(good), now=NOW) if i.path.endswith("sessions/a/b.md") and i.code in ("ACF021", "ACF045")]


@pytest.mark.parametrize("head", VALID)
def test_a_valid_heading_fires_nothing(good, head):
    assert [i.code for i in issues(good, head)] == []


@pytest.mark.parametrize("head", INVALID)
def test_a_malformed_heading_fires_acf045_as_a_warning_and_nothing_else(good, head):
    found = issues(good, head)
    assert [(i.code, i.severity) for i in found] == [("ACF045", "warn")], found


def test_the_severity_setting_makes_it_an_error_and_a_non_date_heading_stays_acf021_only(good):
    found = issues(good, "2026-11-20 - main @ 581a93a - t", "severity: {ACF045: error}\n")
    assert [(i.code, i.severity) for i in found] == [("ACF045", "error")]
    bad = issues(good, "no date here")
    assert [i.code for i in bad] == ["ACF021"]                                # ACF021 unchanged: it reports the missing date; ACF045 does not repeat it


def test_acf021_is_unchanged_for_a_valid_old_style_heading(good):
    found = issues(good, "2026-11-17 - b @ s - t")                            # the old test heading: date first, labels present
    assert [i.code for i in found] == ["ACF045"]                              # no ACF021 finding: only the new, separate warning


# the documented on-hold set: a bundle replaces the `work` set by name (SPEC, ADOPTION)
ON_HOLD = """status_sets:
  work:
    values: [draft, ready, in-progress, on-hold, blocked, in-review, done, cancelled]
    initial: draft
    transitions:
      draft: [ready, cancelled]
      ready: [in-progress, draft, cancelled]
      in-progress: [in-review, on-hold, blocked, cancelled]
      on-hold: [in-progress, cancelled]
      blocked: [in-progress, cancelled]
      in-review: [done, in-progress]
      done: []
      cancelled: []
    human_verified: []
"""


def _task(good, history, status):
    from test_validate import _task
    p = _task(good, status=status, history=history)
    return p


def _codes(good):
    return [i.code for i in validate(Bundle.load(good), now=NOW)]


def test_the_on_hold_block_allows_a_pause_and_resume_and_refuses_hold_to_done(good):
    (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text() + ON_HOLD)
    _task(good, ["draft", "ready", "in-progress", "on-hold", "in-progress"], "in-progress")
    assert "ACF007" not in _codes(good) and "ACF006" not in _codes(good)
    _task(good, ["draft", "ready", "in-progress", "on-hold", "done"], "done")
    assert "ACF007" in _codes(good)


def test_without_the_block_on_hold_is_not_a_status(good):
    _task(good, ["draft", "ready", "in-progress", "on-hold"], "on-hold")
    assert "ACF006" in _codes(good)


def test_a_session_in_an_author_workspace_folder_gets_the_same_rule(good):
    (good / "ackit.yaml").write_text((good / "ackit.yaml").read_text() + "author_workspace: {root: 'people/{author}'}\n")
    put(good, "people/a/s.md", {"type": "session", "title": "s", "author": "a"}, f"## 2026-11-20 - main @ x - t{ENTRY}")
    found = [i for i in validate(Bundle.load(good), now=NOW) if i.path == "people/a/s.md" and i.code == "ACF045"]
    assert len(found) == 1


def test_the_rule_can_be_turned_off_by_severity(good):
    assert issues(good, "2026-11-20 - main @ 581a93a - t", "severity: {ACF045: off}\n") == []
