from __future__ import annotations

from datetime import datetime, timezone

from core.classifier import ClassificationService
from core.dedup import find_duplicate
from core.escalation import EscalationStrategy
from core.models import Issue, TriageResult
from core.router import Router


class TriagePipeline:
    """Wires classification -> dedup -> routing -> escalation for a batch of issues."""

    def __init__(self, classifier: ClassificationService, router: Router, escalation: EscalationStrategy):
        self._classifier = classifier
        self._router = router
        self._escalation = escalation

    def run(self, issues: list[Issue]) -> list[TriageResult]:
        results: list[TriageResult] = []
        seen: list[Issue] = []

        for issue in issues:
            classification = self._classifier.classify(issue)
            duplicate = find_duplicate(issue, seen)
            routing = self._router.route(classification, duplicate)

            if not routing.escalate and duplicate is None:
                routing.escalate = self._escalation.should_escalate(
                    issue, classification.severity, now=datetime.now(timezone.utc)
                )

            results.append(TriageResult(issue, classification, duplicate, routing))
            seen.append(issue)

        return results
