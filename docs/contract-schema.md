# Contract Schema

MetricSpec contracts are strict YAML mappings. Unknown fields are rejected.

```yaml
schema_version: 1
name: net_revenue_by_region
description: Net revenue by region subtracts discounts, tax, and refunds.
severity: medium
owner: analytics
tags: [revenue, regression]
adapter: duckdb
connection: {}
fixtures:
  - table: orders
    path: ../fixtures/orders.csv
  - table: refunds
    path: ../fixtures/refunds.csv
setup_sql: []
query: ../queries/net_revenue_by_region.sql
expect:
  order_by: [region]
  numeric_tolerance:
    absolute: 0.01
  allow_extra_columns: false
  rows:
    - region: AMER
      net_revenue: 150.0
    - region: EMEA
      net_revenue: 100.0
checks:
  required_sql: ["sum("]
  forbidden_sql: ["select *"]
  required_tables: [orders, refunds]
  forbidden_tables: []
  required_columns: [region]
  forbidden_columns: []
metadata:
  ticket: MET-123
```

## Required Fields

- `schema_version`: Must be integer `1`.
- `name`: Non-empty contract name used in reports.
- `adapter`: Must be `duckdb` in the stable v1 core.
- `query`: Path to the SQL query file, resolved relative to the contract file.
- `expect.rows`: Expected result rows as a list of objects.

## Optional Metadata

- `description`: Optional human-readable contract description.
- `severity`: Optional impact label. Allowed values are `low`, `medium`,
  `high`, and `critical`. Defaults to `medium`.
- `owner`: Optional owner string.
- `tags`: Optional list of strings for grouping or filtering outside
  MetricSpec.
- `metadata`: Optional object for project-specific values. MetricSpec preserves
  this information in the loaded contract but does not interpret custom
  metadata.

## Reserved Fields

These fields are accepted by the schema but are not used by the current v1
runner:

- `connection`: Optional object reserved for future adapter configuration. The
  v1 DuckDB runner ignores it.
- `setup_sql`: Optional list of non-empty SQL file paths reserved for future
  setup behavior. The current runner ignores it. Use `.sql` fixtures when setup
  SQL is needed today.

## Fixtures

`fixtures` is a list of local inputs loaded before the query runs. Each fixture
has:

- `table`: Table name created in the adapter session.
- `path`: Fixture path, resolved relative to the contract file unless absolute.

DuckDB fixtures currently support `.csv`, `.parquet`, and `.sql` files.

## Expected Rows

MetricSpec compares row count and values exactly by default.

- `rows`: Expected rows. Each key is an expected output column.
- `numeric_tolerance.absolute`: Optional absolute tolerance for numeric values.
  The value must be a finite, non-negative number.
- `order_by`: Optional list of columns used to sort actual and expected rows
  before comparison.
- `allow_extra_columns`: Defaults to `false`. When `false`, unexpected actual
  columns fail the contract. When `true`, extra actual columns are ignored.

## SQL Shape Checks

`checks` are optional case-insensitive text checks against the query before it
executes:

- `required_sql` and `forbidden_sql`
- `required_tables` and `forbidden_tables`
- `required_columns` and `forbidden_columns`

These checks are lightweight guardrails, not a SQL parser.
