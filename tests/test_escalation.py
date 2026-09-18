from datetime import datetime, timedelta, timezone

from core.escalation import TimeBasedEscalationStrategy
from core.models import Issue, Severity


def _issue(hours_ago: float) -> Issue:
    return Issue(
        external_id="t#1",
        repo="t/t",
        title="x",
        body="x",
        opened_at=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
    )


def test_critical_escalates_past_4_hour_sla():
    strategy = TimeBasedEscalationStrategy()
    assert strategy.should_escalate(_issue(hours_ago=5), Severity.CRITICAL) is True
    assert strategy.should_escalate(_issue(hours_ago=1), Severity.CRITICAL) is False


def test_low_severity_has_much_longer_sla():
    strategy = TimeBasedEscalationStrategy()
    assert strategy.should_escalate(_issue(hours_ago=5), Severity.LOW) is False
