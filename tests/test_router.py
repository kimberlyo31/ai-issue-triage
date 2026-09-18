from core.models import Category, Classification, DuplicateMatch, Severity
from core.router import Router


def _classification(category: Category, severity: Severity) -> Classification:
    return Classification(category=category, severity=severity, confidence=0.9, rationale="test")


def test_critical_bug_routes_to_engineering_and_escalates():
    decision = Router().route(_classification(Category.BUG, Severity.CRITICAL), duplicate=None)
    assert decision.team == "engineering"
    assert decision.escalate is True


def test_feature_request_routes_to_product_without_escalation():
    decision = Router().route(_classification(Category.FEATURE, Severity.LOW), duplicate=None)
    assert decision.team == "product"
    assert decision.escalate is False


def test_duplicate_short_circuits_routing():
    decision = Router().route(
        _classification(Category.BUG, Severity.CRITICAL),
        duplicate=DuplicateMatch(issue_id="t#1", similarity=0.9),
    )
    assert decision.labels == ["duplicate"]
    assert decision.escalate is False
