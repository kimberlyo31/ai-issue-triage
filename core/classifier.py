from __future__ import annotations

from core.models import Classification, Issue
from core.providers.base import AIProvider


class ClassificationService:
    """orchestration layer around whichever AIProvider is configured."""

    def __init__(self, provider: AIProvider):
        self._provider = provider

    def classify(self, issue: Issue) -> Classification:
        return self._provider.classify(issue)
