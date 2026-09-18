from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Category(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    QUESTION = "question"
    DOCUMENTATION = "documentation"
    OTHER = "other"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Issue:
    """A single inbound item to triage (a GitHub issue, in this demo)."""

    external_id: str
    repo: str
    title: str
    body: str
    opened_at: datetime
    number: int | None = None
    labels: list[str] = field(default_factory=list)


@dataclass
class Classification:
    category: Category
    severity: Severity
    confidence: float
    rationale: str


@dataclass
class DuplicateMatch:
    issue_id: str
    similarity: float


@dataclass
class RoutingDecision:
    labels: list[str]
    team: str
    escalate: bool
    reason: str


@dataclass
class TriageResult:
    issue: Issue
    classification: Classification
    duplicate_of: DuplicateMatch | None
    routing: RoutingDecision
