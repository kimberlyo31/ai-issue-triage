from __future__ import annotations

from core.models import Category, Classification, Issue, Severity
from core.providers.base import AIProvider


class MockAIProvider(AIProvider):
    """Deterministic keyword-based classifier.

    Used for tests and for the offline demo mode so the project runs with
    zero API keys.
    """

    _CRITICAL_WORDS = ("crash", "data loss", "security", "vulnerability", "down")
    _BUG_WORDS = ("error", "exception", "crash", "bug", "broken", "fails", "traceback")
    _FEATURE_WORDS = ("feature request", "would be nice", "please add", "enhancement")
    _DOC_WORDS = ("docs", "documentation", "readme", "typo")

    def classify(self, issue: Issue) -> Classification:
        text = f"{issue.title}\n{issue.body}".lower()

        if any(word in text for word in self._DOC_WORDS):
            category = Category.DOCUMENTATION
        elif any(word in text for word in self._BUG_WORDS):
            category = Category.BUG
        elif any(word in text for word in self._FEATURE_WORDS):
            category = Category.FEATURE
        elif text.strip().endswith("?") or "how do i" in text or "how to" in text:
            category = Category.QUESTION
        else:
            category = Category.OTHER

        if any(word in text for word in self._CRITICAL_WORDS):
            severity = Severity.CRITICAL
        elif category == Category.BUG:
            severity = Severity.HIGH
        elif category == Category.FEATURE:
            severity = Severity.LOW
        else:
            severity = Severity.MEDIUM

        return Classification(
            category=category,
            severity=severity,
            confidence=0.6,
            rationale="keyword match (mock provider)",
        )
