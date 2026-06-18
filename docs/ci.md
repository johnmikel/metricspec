# CI

MetricSpec is designed to run as a normal CI test step. Validate contracts first,
then run them and upload JSON or JUnit artifacts.

## GitHub Actions

```yaml
name: metricspec

on:
  pull_request:
  push:
    branches: [main]

jobs:
  metricspec:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: uv sync --extra dev

      - name: Validate metric contracts
        run: uv run metricspec validate contracts

      - name: Run metric contracts
        run: |
          mkdir -p reports
          uv run metricspec run --json --junit reports/metricspec-junit.xml contracts > reports/metricspec-report.json

      - name: Upload MetricSpec reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: metricspec-reports
          path: reports/
```

If MetricSpec is not installed as part of the repository, replace
`uv run metricspec` with `uvx metricspec`.

## Outputs

- JSON: Useful for custom CI summaries and debugging artifacts.
- JUnit XML: Useful for test report integrations.

`metricspec run` exits with `1` when any contract fails. The JSON and JUnit files
are written before that exit, so `if: always()` lets CI upload artifacts for both
passing and failing runs.
