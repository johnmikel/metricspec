# Getting Started

MetricSpec is a Python CLI for testing analytical contracts with deterministic
fixtures. The stable v1 path uses DuckDB and local files.

## Install

MetricSpec is not assumed to be published as a package yet. From a local
checkout, install development dependencies and run the CLI through `uv`:

```bash
uv sync --extra dev
uv run metricspec --help
```

After package publication, use `uvx metricspec ...` for the same commands
without a checkout.

## Initialize the Demo

```bash
uv run metricspec init demo
cd metricspec-demo
```

The demo creates `contracts/`, `queries/`, and `fixtures/`. It includes one
passing contract and one failing contract so you can see both success output and
diagnostics.

## Validate Contracts

Validate checks that contract YAML files parse and match the supported schema.

```bash
uv run --project .. metricspec validate contracts
```

You can validate one file or a directory:

```bash
uv run --project .. metricspec validate contracts/net_revenue_by_region.pass.yaml
```

## Run Contracts

Run all contracts in a directory:

```bash
uv run --project .. metricspec run contracts
```

Run one passing demo contract:

```bash
uv run --project .. metricspec run contracts/net_revenue_by_region.pass.yaml
```

MetricSpec exits with `0` when every contract passes and `1` when validation,
execution, SQL shape checks, safety checks, or expected rows fail.

## JSON Output

Use JSON when another tool should consume the result.

```bash
uv run --project .. metricspec run --json contracts > metricspec-report.json
```

JSON output contains a top-level `results` array with each contract name, path,
pass/fail status, failure category, checks, and actual rows.

## JUnit Output

Use JUnit XML for CI test reporting.

```bash
uv run --project .. metricspec run --junit metricspec-junit.xml contracts
```

You can emit JSON to stdout and write JUnit XML in the same run:

```bash
mkdir -p reports
uv run --project .. metricspec run --json --junit reports/metricspec-junit.xml contracts > reports/metricspec-report.json
```

## After Package Publication

Once MetricSpec is published as a package, the demo can be run without a local
checkout by keeping the command style consistent:

```bash
uvx metricspec init demo
cd metricspec-demo
uvx metricspec validate contracts
uvx metricspec run contracts
```
