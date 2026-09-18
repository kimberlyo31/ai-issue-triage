from __future__ import annotations

import json
from pathlib import Path

from core.models import Classification, DuplicateMatch, RoutingDecision, Severity

_DEFAULT_RULES_PATH = Path(__file__).parent.parent / "config" / "routing_rules.json"


class Router:
    """Config-driven routing: classification -> (labels, owning team, escalate?)."""

    def __init__(self, rules_path: Path | None = None):
        path = rules_path or _DEFAULT_RULES_PATH
        with open(path, encoding="utf-8") as f:
            self._rules = json.load(f)

    def route(self, classification: Classification, duplicate: DuplicateMatch | None) -> RoutingDecision:
        if duplicate is not None:
            return RoutingDecision(
                labels=["duplicate"],
                team="triage",
                escalate=False,
                reason=f"looks like a duplicate of {duplicate.issue_id} (similarity {duplicate.similarity})",
            )

        rule = self._rules.get(classification.category.value, self._rules["default"])
        escalate = classification.severity in (Severity.CRITICAL, Severity.HIGH) and rule.get(
            "escalate_on_high_severity", False
        )
        return RoutingDecision(
            labels=[classification.category.value, classification.severity.value],
            team=rule["team"],
            escalate=escalate,
            reason=f"category={classification.category.value} severity={classification.severity.value}",
        )
