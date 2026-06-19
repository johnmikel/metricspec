# MetricSpec v0.1.0

Unit tests for business metrics. Contract testing for analytical meaning.

## Highlights

- Contract YAML schema for business metric tests.
- DuckDB fixture runner for CSV, parquet, and SQL setup files.
- Read-only SQL safety guard and SQL-shape checks.
- Expected-row comparison with numeric tolerance and field-level diffs.
- Human, JSON, and JUnit reports.
- `metricspec init demo`, `validate`, `run`, and `explain`.
- Documentation, governance files, CI, build checks, and trusted publishing workflow.

## Try It

```bash
uvx metricspec init demo
cd metricspec-demo
uvx metricspec run
```

## Known Limitations

- Stable core is DuckDB fixture-based testing.
- Additional adapters are experimental/future work.
- `connection` and `setup_sql` are accepted by the schema but reserved in v1.
- SQL-shape checks are text guardrails, not a SQL parser.

## Links

- README: `README.md`
- Getting started: `docs/getting-started.md`
- Security: `docs/security.md`
- Roadmap: `docs/roadmap.md`
