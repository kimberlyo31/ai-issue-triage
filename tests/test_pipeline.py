from core.classifier import ClassificationService
from core.escalation import TimeBasedEscalationStrategy
from core.github_client import load_sample_issues
from core.pipeline import TriagePipeline
from core.providers.mock_provider import MockAIProvider
from core.router import Router


def test_pipeline_runs_end_to_end_on_sample_data():
    pipeline = TriagePipeline(
        classifier=ClassificationService(MockAIProvider()),
        router=Router(),
        escalation=TimeBasedEscalationStrategy(),
    )

    results = pipeline.run(load_sample_issues())

    assert len(results) == 6
    # the near-duplicate crash report (#102) should be flagged against #101
    dup_result = next(r for r in results if r.issue.external_id == "demo/widgets#102")
    assert dup_result.duplicate_of is not None
    assert dup_result.duplicate_of.issue_id == "demo/widgets#101"
