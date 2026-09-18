from __future__ import annotations

from abc import ABC, abstractmethod

from core.models import Classification, Issue


class AIProvider(ABC):
    """Strategy interface for any backend that can classify an issue."""

    @abstractmethod
    def classify(self, issue: Issue) -> Classification:
        raise NotImplementedError
