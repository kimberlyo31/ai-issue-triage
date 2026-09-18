from __future__ import annotations

import json
import os

from core.models import Category, Classification, Issue, Severity
from core.providers.base import AIProvider

_SYSTEM_PROMPT = """You triage inbound software issues. Given a title and body, \
respond with ONLY a JSON object of the form:
{"category": "bug|feature|question|documentation|other", \
"severity": "critical|high|medium|low", "confidence": 0.0-1.0, "rationale": "one sentence"}
No prose, no markdown fences, just the JSON object."""


class AnthropicProvider(AIProvider):
    """Classifies issues using the Claude API.

    Requires the `anthropic` package and an ANTHROPIC_API_KEY. Kept isolated
    behind the AIProvider interface.
    """

    def __init__(self, model: str = "claude-sonnet-5", api_key: str | None = None):
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "The 'anthropic' package is required for AnthropicProvider. "
                "Install it with `pip install anthropic`."
            ) from exc

        self._client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self._model = model

    def classify(self, issue: Issue) -> Classification:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=300,
            system=_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Title: {issue.title}\n\nBody:\n{issue.body}",
                }
            ],
        )
        raw_text = "".join(block.text for block in response.content if block.type == "text")
        return self._parse(raw_text)

    @staticmethod
    def _parse(raw_text: str) -> Classification:
        try:
            data = json.loads(raw_text.strip())
            return Classification(
                category=Category(data["category"]),
                severity=Severity(data["severity"]),
                confidence=float(data["confidence"]),
                rationale=data["rationale"],
            )
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            raise ValueError(f"Could not parse model response as a classification: {raw_text!r}") from exc
