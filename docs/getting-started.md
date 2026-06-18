# Getting Started

MetricSpec is a Python CLI for testing analytical contracts with deterministic
fixtures. The stable v1 path uses DuckDB and local files.

## Install

Run the published CLI with `uvx`:

```bash
uvx metricspec --help
```

When working from a repository checkout, install development dependencies and
run through `uv`:

```bash
uv sync --extra dev
uv run metricspec --help
```

## Initialize the Demo

```bash
uvx metricspec init demo
cd metricspec-demo
```

The demo creates `contracts/`, `queries/`, and `fixtures/`. It includes one
passing contract and one failing contract so you can see both success output and
diagnostics.

## Validate Contracts

Validate checks that contract YAML files parse and match the supported schema.

```bash
metricspec validate contracts
```

You can validate one file or a directory:

```bash
metricspec validate contracts/net_revenue_by_region.pass.yaml
```

## Run Contracts

Run all contracts in a directory:

```bash
metricspec run contracts
```

Run one passing demo contract:

```bash
metricspec run contracts/net_revenue_by_region.pass.yaml
```

MetricSpec exits with `0` when every contract passes and `1` when validation,
execution, SQL shape checks, safety checks, or expected rows fail.

## JSON Output

Use JSON when another tool should consume the result.

```bash
metricspec run --json contracts > metricspec-report.json
```

JSON output contains a top-level `results` array with each contract name, path,
pass/fail status, failure category, checks, and actual rows.

## JUnit Output

Use JUnit XML for CI test reporting.

```bash
metricspec run --junit metricspec-junit.xml contracts
```

You can emit JSON to stdout and write JUnit XML in the same run:

```bash
mkdir -p reports
metricspec run --json --junit reports/metricspec-junit.xml contracts > reports/metricspec-report.json
```
