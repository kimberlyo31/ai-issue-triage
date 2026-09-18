from __future__ import annotations

from difflib import SequenceMatcher

from core.models import DuplicateMatch, Issue

_SIMILARITY_THRESHOLD = 0.5


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(a=a.lower(), b=b.lower()).ratio()


def find_duplicate(issue: Issue, existing_issues: list[Issue]) -> DuplicateMatch | None:
    """Flag likely duplicates by title+body similarity against already-seen issues."""
    best: DuplicateMatch | None = None
    for other in existing_issues:
        if other.external_id == issue.external_id:
            continue
        score = _similarity(f"{issue.title}\n{issue.body}", f"{other.title}\n{other.body}")
        if score >= _SIMILARITY_THRESHOLD and (best is None or score > best.similarity):
            best = DuplicateMatch(issue_id=other.external_id, similarity=round(score, 3))
    return best
