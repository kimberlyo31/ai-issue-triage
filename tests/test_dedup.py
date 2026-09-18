from datetime import datetime, timezone

from core.dedup import find_duplicate
from core.models import Issue


def _issue(eid: str, title: str, body: str) -> Issue:
    return Issue(external_id=eid, repo="t/t", title=title, body=body, opened_at=datetime.now(timezone.utc))


def test_finds_near_duplicate():
    existing = [_issue("t#1", "App crashes on startup with NullPointerException", "throws NPE and closes on launch")]
    incoming = _issue("t#2", "App crashes on launch, NPE in logcat", "throws a NullPointerException and closes")

    match = find_duplicate(incoming, existing)

    assert match is not None
    assert match.issue_id == "t#1"


def test_no_match_for_unrelated_issue():
    existing = [_issue("t#1", "App crashes on startup with NullPointerException", "throws NPE and closes on launch")]
    incoming = _issue("t#2", "Add dark mode setting", "would be nice to toggle a dark theme in settings")

    assert find_duplicate(incoming, existing) is None
