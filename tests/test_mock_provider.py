from datetime import datetime, timezone

from core.models import Category, Issue, Severity
from core.providers.mock_provider import MockAIProvider


def _issue(title: str, body: str) -> Issue:
    return Issue(
        external_id="t#1",
        repo="t/t",
        title=title,
        body=body,
        opened_at=datetime.now(timezone.utc),
    )


def test_classifies_crash_as_critical_bug():
    result = MockAIProvider().classify(_issue("App crashes on startup", "throws an exception, then closes"))
    assert result.category == Category.BUG
    assert result.severity == Severity.CRITICAL


def test_classifies_feature_request():
    result = MockAIProvider().classify(_issue("Feature request: dark mode", "would be nice to have"))
    assert result.category == Category.FEATURE
    assert result.severity == Severity.LOW


def test_classifies_documentation():
    result = MockAIProvider().classify(_issue("README typo", "documentation has a typo"))
    assert result.category == Category.DOCUMENTATION
