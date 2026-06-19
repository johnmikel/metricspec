# MetricSpec

Unit tests for business metrics. Contract testing for analytical meaning.

MetricSpec is a Python CLI for testing analytical contracts in local development and CI.
It starts with deterministic DuckDB fixture tests and produces explainable diagnostics
when a business metric returns the wrong answer.

## Quick Start

From a local checkout before MetricSpec is published as a package:

```bash
uv sync --extra dev
uv run metricspec init demo
cd metricspec-demo
uv run --project .. metricspec run
```

After package publication, the same flow can use `uvx` without a checkout:

```bash
uvx metricspec init demo
cd metricspec-demo
uvx metricspec run
```

## What MetricSpec Is

- A contract test runner for business metrics.
- A fixture-first semantic regression tool.
- A CI-friendly way to catch wrong analytical answers.

## What MetricSpec Is Not

- A semantic layer.
- A general data quality platform.
- A hosted observability dashboard.

## Status

The stable v1 core is DuckDB fixture-based contract testing. Additional adapters are experimental.

## Documentation

- [Getting started](docs/getting-started.md)
- [Contract schema](docs/contract-schema.md)
- [Adapters](docs/adapters.md)
- [CI](docs/ci.md)
- [Roadmap](docs/roadmap.md)
- [Release checklist](docs/release.md)
- [Security](docs/security.md)

## Security

MetricSpec should not send telemetry or make hidden network calls. Keep credentials,
production data, and secrets out of contracts, fixtures, issue reports, and CI artifacts.
