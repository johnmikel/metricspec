# MetricSpec

[![CI](https://github.com/johnmikel/metricspec/actions/workflows/ci.yml/badge.svg)](https://github.com/johnmikel/metricspec/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Unit tests for business metrics.** MetricSpec is a Python CLI that pins the expected
result of an analytical SQL query as a versioned contract, runs that query against
deterministic local fixtures, and fails loudly — with a row-level diff — when the
numbers change. It is built to run in CI as a semantic regression gate.

```
FAIL net_revenue_by_region_fail (contracts/net_revenue_by_region.fail.yaml)
category: result_mismatch
- Rows differ
  row 1 field net_revenue: expected 100.0, actual 180.0
PASS net_revenue_by_region_pass (contracts/net_revenue_by_region.pass.yaml)
```

## Why this exists

A metric query can be syntactically valid, pass `dbt run`, and still be *wrong*: a
refactor drops a `LEFT JOIN refunds`, a `WHERE is_test_order = false` filter goes
missing, a `SUM` quietly double-counts. The pipeline stays green, the dashboard keeps
rendering, and "net revenue" is now overstated by 30% — until someone in finance
notices weeks later.

That class of bug is expensive precisely because nothing breaks. The fix is the same
one application engineers reached for decades ago: write a test that asserts the
**meaning** of the output, not just that the code ran. MetricSpec is that test, scoped
to analytical SQL. You declare "given this input, this metric must return exactly these
rows," and MetricSpec enforces it on every change.

It is deliberately small and opinionated. It is **not** a semantic layer, a general
data-quality platform, or a hosted observability product — see
[What it is not](#what-it-is-not).

## How it works

A contract is a YAML file. It names a metric, lists the fixtures to load, points at the
SQL under test, and pins the exact expected output:

```yaml
schema_version: 1
name: net_revenue_by_region
description: Net revenue by region subtracts discounts, tax, and refunds.
adapter: duckdb
fixtures:
  - table: orders
    path: ../fixtures/orders.csv
  - table: refunds
    path: ../fixtures/refunds.csv
query: ../queries/net_revenue_by_region.sql
expect:
  order_by: [region]
  rows:
    - region: AMER
      net_revenue: 150.0
    - region: EMEA
      net_revenue: 100.0
```

When you run it, MetricSpec:

1. **Loads the contract** with a strict Pydantic v2 schema (`extra = forbid`, strict
   types) — typos and unknown keys are rejected, not silently ignored.
2. **Screens the SQL as read-only.** A safety guard requires a single `SELECT`/`WITH`
   statement and rejects DDL/DML (`INSERT`, `UPDATE`, `DROP`, `ALTER`, `COPY … TO`, …)
   and side-effecting DuckDB functions (`checkpoint`, profiling/logging toggles).
   Comments are stripped before the function check so they can't smuggle anything past.
3. **Optionally checks SQL shape** — lightweight required/forbidden fragments, tables,
   and columns (e.g. require `refunds`, forbid `select *`). These are case-insensitive
   substring checks, not a SQL parser; they are a guardrail, not a proof.
4. **Builds an in-memory DuckDB**, loads each fixture (CSV / Parquet / SQL) into its
   declared table via parameterized, quoted-identifier reads, and runs the query.
5. **Compares actual rows to expected rows** — sorted by `order_by`, with optional
   absolute numeric tolerance, `allow_extra_columns`, and explicit detection of
   missing and unexpected columns.
6. **Reports.** On mismatch you get a structured, row-and-field diff
   (`row 1 field net_revenue: expected 100.0, actual 180.0`) instead of a generic
   assertion error. Exit code is `0` if every contract passes, `1` otherwise.

The execution path is deterministic by construction: fixtures are local, the database
is in-memory and read-only, and there are no network calls. The same contract produces
the same result on your laptop and in CI.

### Architecture

The source is organized as thin, single-responsibility layers (~935 lines of Python):

```
src/metricspec/
├─ contracts/    YAML loading + strict Pydantic models (the contract schema)
├─ adapters/     execution backends; DuckDB is the only one today
├─ execution/    fixture loading, the run orchestrator, the read-only safety guard
├─ checks/       row comparison engine + SQL-shape checks
├─ diagnostics/  value diffs, events, the human-readable renderer
├─ reports/      JSON, JUnit XML, and GitHub Actions step-summary renderers
└─ cli.py        Typer CLI: init / validate / run / explain
```

## Install & usage

> **Status:** MetricSpec is not yet published to PyPI. The instructions below run it from
> a local checkout. A `uvx metricspec …` zero-checkout flow will work once the package
> is published — see [Project status](#project-status).

```bash
git clone https://github.com/johnmikel/metricspec.git
cd metricspec
uv sync --extra dev
```

Scaffold a working demo project (contracts, queries, and fixtures), then run it:

```bash
uv run metricspec init demo
cd metricspec-demo
uv run --project .. metricspec run contracts
```

The demo ships one passing contract and one intentionally failing one (its query drops
the `refunds` join), so you can see a real diff immediately. The run exits `1` because
one contract fails — that is the point.

### Commands

| Command | What it does |
| --- | --- |
| `metricspec init demo` | Scaffold a `metricspec-demo/` project to copy from. |
| `metricspec validate [PATH]` | Parse and validate contract YAML (default `contracts`). |
| `metricspec run [PATH]` | Run contracts; exit `0` if all pass, `1` on any failure. |
| `metricspec explain <CONTRACT>` | Print a contract's name and description. |
| `metricspec --version` | Print the installed version. |

### Output formats

`run` defaults to human-readable output and adds machine formats on request:

```bash
metricspec run contracts --json                 # JSON report to stdout
metricspec run contracts --junit results.xml    # JUnit XML for CI test reporting
metricspec run contracts --github-summary       # Markdown table → $GITHUB_STEP_SUMMARY
```

### In CI

Because `run` returns a non-zero exit code on any failure, it drops straight into a
pipeline as a gate. `--github-summary` appends a results table with per-failure diffs to
the GitHub Actions job summary; `--junit` produces a report most CI systems render as
test results.

## What it is not

- **Not a semantic layer.** It tests metric queries; it does not define or serve them.
- **Not a general data-quality platform.** It checks contracts you write, not arbitrary
  freshness/volume/anomaly rules.
- **Not a hosted dashboard.** It is a local/CI CLI with no telemetry and no network
  calls.

## Project status

`v0.1.0`. Early but real:

- **100 passing tests** (unit + integration), including the end-to-end demo flow.
- **Typed throughout** — `mypy --strict` clean across the source tree, ships `py.typed`.
- **CI** runs ruff, `mypy`, pytest with coverage, a package build, and `twine check` on
  every PR and push to `main`.
- **Release engineering** is wired up: a separate workflow publishes via PyPI **trusted
  publishing (OIDC)**, gated on version tags.

Honest caveats:

- **Not on PyPI yet.** No release tags exist; install from a local checkout for now.
- **One adapter.** DuckDB is the only working backend. Postgres / BigQuery / Snowflake
  are roadmap items, not shipping features.
- **SQL-shape checks are substring matching, not a parser.** They will not catch a
  forbidden fragment hidden in a string literal. Treat them as a guardrail.

See [docs/roadmap.md](docs/roadmap.md) for what's planned.

## Documentation

- [Getting started](docs/getting-started.md)
- [Contract schema](docs/contract-schema.md)
- [Adapters](docs/adapters.md)
- [CI integration](docs/ci.md)
- [Security](docs/security.md)
- [Roadmap](docs/roadmap.md)

## Security

MetricSpec executes only read-only `SELECT`/`WITH` queries against an in-memory database
and makes no hidden network calls. Keep credentials, production data, and secrets out of
contracts, fixtures, reports, and CI artifacts. See [SECURITY.md](SECURITY.md).

## License

Apache-2.0. See [LICENSE](LICENSE).
