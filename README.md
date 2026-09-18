# AI Issue Triage

Classifies inbound issues with an LLM, flags likely duplicates, routes them
to the right team, and escalates the ones that have blown past their SLA —
implemented twice: as a standalone Python service (point it at any public
GitHub repo) and as a Salesforce Apex module (point it at a custom object).

```
[ESCALATE] demo/widgets#101               bug            critical  -> engineering
           keyword match (mock provider)
[        ] demo/widgets#102               bug            critical  -> triage       [dup of demo/widgets#101]
           keyword match (mock provider)
[ESCALATE] demo/widgets#103               feature        low       -> product
           keyword match (mock provider)
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the design (strategy
pattern for the AI backend, config-driven routing, SLA-based escalation).

## Python service (`core/`, `cli.py`)

Runs entirely offline against bundled sample data by default — no API keys
needed to see it work.

```bash
pip install -e ".[dev]"
python -m pytest                 # 11 tests, all offline

python cli.py                    # runs the mock provider against sample_data/
python cli.py --repo anthropics/anthropic-sdk-python --provider mock
```

To use real Claude classifications instead of the keyword-based mock:

```bash
pip install -e ".[anthropic]"
export ANTHROPIC_API_KEY=sk-...
python cli.py --repo <owner>/<repo> --provider anthropic
```

## Salesforce module (`force-app/`)

Same design, targeting a `GitHub_Issue__c` custom object instead of the
GitHub API directly.

```bash
sf project deploy start --source-dir force-app
sf apex run test --code-coverage --result-format human
```

`AnthropicProvider` calls out through a Named Credential named
`Anthropic_API` pointed at `https://api.anthropic.com` — set that up (with
your API key as a header) before scheduling `GitHubIssueTriageScheduler`.
Everything is unit-testable without it via `MockAIProvider`.

## Why it's built this way

Both implementations share one interface for the AI backend
(`AIProvider` / `AIProvider.cls`), so:

- Tests never mock an HTTP call — they inject a deterministic mock provider.
- Swapping Claude for a different model, or Bedrock for a direct API call,
  is a one-class change; nothing else in the pipeline knows or cares.

This project was built from scratch as a portfolio piece to demonstrate
LLM-classification-pipeline design (provider abstraction, dedup, config-driven
routing, SLA escalation) in both a general-purpose language and Salesforce
Apex.

