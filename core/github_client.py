from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import requests

from core.models import Issue

_API_ROOT = "https://api.github.com"


def fetch_open_issues(repo: str, limit: int = 30) -> list[Issue]:
    """Fetch open issues for a public repo, e.g. repo='anthropics/anthropic-sdk-python'.

    Uses an unauthenticated request by default (60 req/hr GitHub limit); set
    GITHUB_TOKEN to raise that to 5000/hr. Pull requests are filtered out —
    the GitHub REST API returns them from the issues endpoint too.
    """
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(
        f"{_API_ROOT}/repos/{repo}/issues",
        params={"state": "open", "per_page": limit},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()

    issues = []
    for raw in response.json():
        if "pull_request" in raw:
            continue
        issues.append(
            Issue(
                external_id=f"{repo}#{raw['number']}",
                repo=repo,
                title=raw["title"],
                body=raw.get("body") or "",
                opened_at=datetime.fromisoformat(raw["created_at"].replace("Z", "+00:00")),
                number=raw["number"],
                labels=[label["name"] for label in raw.get("labels", [])],
            )
        )
    return issues


def load_sample_issues(path: Path | None = None) -> list[Issue]:
    """Offline demo data so the CLI runs with zero network calls / API keys."""
    path = path or Path(__file__).parent.parent / "sample_data" / "sample_issues.json"
    with open(path, encoding="utf-8") as f:
        raw_issues = json.load(f)

    return [
        Issue(
            external_id=item["external_id"],
            repo=item["repo"],
            title=item["title"],
            body=item["body"],
            opened_at=datetime.fromisoformat(item["opened_at"]),
            number=item.get("number"),
            labels=item.get("labels", []),
        )
        for item in raw_issues
    ]
