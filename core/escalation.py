from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from core.models import Issue, Severity

_SLA_HOURS = {
    Severity.CRITICAL: 4,
    Severity.HIGH: 24,
    Severity.MEDIUM: 72,
    Severity.LOW: 168,
}


class EscalationStrategy(ABC):
    """Strategy interface so escalation policy can vary independently of
    classification/routing """

    @abstractmethod
    def should_escalate(self, issue: Issue, severity: Severity, now: datetime | None = None) -> bool:
        raise NotImplementedError


class TimeBasedEscalationStrategy(EscalationStrategy):
    """Escalate when an issue has been open longer than its severity's SLA."""

    def should_escalate(self, issue: Issue, severity: Severity, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        sla = timedelta(hours=_SLA_HOURS[severity])
        return (now - issue.opened_at) > sla
