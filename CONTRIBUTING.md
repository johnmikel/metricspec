# Contributing

Thanks for helping improve MetricSpec. Keep changes focused, practical, and
easy to review.

## Local Setup

```bash
uv sync --extra dev
uv run metricspec --help
```

## Development Checks

Run these before opening a pull request:

```bash
uv run ruff check .
uv run mypy src
uv run pytest
```

## Contribution Guidelines

- Keep contracts, fixtures, and docs small enough for reviewers to reason about.
- Add tests for behavior changes and update docs when user-facing behavior changes.
- Do not commit credentials, production data, secrets, or private customer fixtures.
- Do not add telemetry or hidden network calls without an explicit public design discussion.
- Prefer deterministic local fixtures over live service dependencies.

## Pull Requests

Describe the problem, the change, and the verification you ran. Include CLI
output or report snippets when the change affects diagnostics, JSON, or JUnit
output.
