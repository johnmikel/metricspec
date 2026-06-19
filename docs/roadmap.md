# Roadmap

MetricSpec starts with a small stable core: deterministic DuckDB fixture tests
for business metric SQL, with clear diagnostics and CI-friendly output.

## v0.1 Core

- Contract YAML schema.
- DuckDB fixture adapter for CSV, parquet, and SQL setup files.
- Read-only SQL safety guard.
- SQL-shape text checks.
- Expected-row comparison with numeric tolerance and value diffs.
- Human, JSON, and JUnit output.
- `metricspec init demo`, `validate`, `run`, and `explain`.
- Documentation, governance, CI, build, and trusted publishing workflow.

## Next Good Issues

- Add `metricspec --version`.
- Add a `metricspec doctor` command for environment and package diagnostics.
- Improve the generated demo test to assert created file contents.
- Add richer examples for tolerances, extra columns, and SQL-shape checks.
- Add release automation checks that fail when `CHANGELOG.md` misses the version.

## Adapter Roadmap

- dbt manifest or MetricFlow adapter discovery.
- Postgres read-only adapter for trusted development databases.
- BigQuery/Snowflake adapter prototypes behind explicit experimental flags.

Adapters should preserve the v1 rule: no hidden network calls, no telemetry, and
no credential capture in contracts or diagnostics.

## Diagnostics Roadmap

- More compact row-diff summaries for large result sets.
- Optional JSON schema for report output.
- GitHub Actions summary renderer.
- SQL parser-backed shape checks once a dependency is justified.

## Non-Goals

- Hosted dashboard.
- Semantic layer replacement.
- Always-on production monitoring.
- Secret management system.
