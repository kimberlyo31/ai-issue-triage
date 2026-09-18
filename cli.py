from __future__ import annotations

import argparse
import sys

from core.classifier import ClassificationService
from core.escalation import TimeBasedEscalationStrategy
from core.github_client import fetch_open_issues, load_sample_issues
from core.pipeline import TriagePipeline
from core.providers.mock_provider import MockAIProvider
from core.router import Router


def _build_provider(name: str):
    if name == "mock":
        return MockAIProvider()
    if name == "anthropic":
        from core.providers.anthropic_provider import AnthropicProvider

        return AnthropicProvider()
    raise ValueError(f"Unknown provider: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify, dedup, route, and flag escalations for GitHub issues.")
    parser.add_argument("--repo", help="e.g. anthropics/anthropic-sdk-python. Omit to use bundled sample data.")
    parser.add_argument("--provider", choices=["mock", "anthropic"], default="mock")
    parser.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()

    issues = load_sample_issues() if not args.repo else fetch_open_issues(args.repo, limit=args.limit)
    if not issues:
        print("No open issues found.")
        return

    pipeline = TriagePipeline(
        classifier=ClassificationService(_build_provider(args.provider)),
        router=Router(),
        escalation=TimeBasedEscalationStrategy(),
    )
    results = pipeline.run(issues)

    for result in results:
        flag = "ESCALATE" if result.routing.escalate else "        "
        dup = f" [dup of {result.duplicate_of.issue_id}]" if result.duplicate_of else ""
        print(
            f"[{flag}] {result.issue.external_id:30} "
            f"{result.classification.category.value:14} "
            f"{result.classification.severity.value:9} "
            f"-> {result.routing.team:12}{dup}"
        )
        print(f"           {result.classification.rationale}")


if __name__ == "__main__":
    sys.exit(main())
