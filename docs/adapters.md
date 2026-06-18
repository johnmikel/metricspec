# Adapters

MetricSpec's stable v1 core supports DuckDB fixture-based contract testing.
Additional adapters are experimental until their behavior and security model are
documented.

## DuckDB Adapter

The DuckDB adapter creates an in-memory DuckDB database for each contract run,
loads fixtures into that session, executes the contract query, and returns rows
as dictionaries for comparison.

Use it with:

```yaml
adapter: duckdb
```

The current DuckDB path is local and deterministic. It should not require
credentials, telemetry, or hidden network calls.

## Fixture Formats

DuckDB fixtures are loaded by file suffix:

- `.csv`: Loaded with DuckDB `read_csv_auto`.
- `.parquet`: Loaded with DuckDB `read_parquet`.
- `.sql`: Executed directly in the DuckDB session.

Prefer small synthetic `.csv` or `.parquet` fixtures for most contracts. Treat
`.sql` fixtures as trusted setup code and keep them local, reviewed, and free of
production data.

## Adapter Boundary

Internally, an adapter session is responsible for two operations:

- `load_fixture(fixture, base_dir)`: Prepare contract inputs.
- `execute(sql)`: Run the metric query and return rows.

Contracts currently accept `adapter: duckdb`. Future adapters should preserve
the same contract-testing semantics: deterministic setup, explicit credentials,
clear safety limits, and explainable row-level diagnostics.

## Future Adapters

Future warehouse or semantic-layer adapters are experimental. Use least-privilege
read-only credentials, isolated test schemas, and synthetic data until an adapter
documents stronger guarantees.
