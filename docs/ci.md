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
      - uses: actions/checkout@v7

      - uses: astral-sh/setup-uv@v8

      - uses: actions/setup-python@v6
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
        uses: actions/upload-artifact@v7
        with:
          name: metricspec-reports
          path: reports/
```

Before package publication, run CI from a repository checkout with
`uv run metricspec`. After package publication, downstream projects can use
`uvx metricspec` consistently instead.

## Outputs

- JSON: Useful for custom CI summaries and debugging artifacts.
- JUnit XML: Useful for test report integrations.

`metricspec run` exits with `1` when any contract fails. The JSON and JUnit files
are written before that exit, so `if: always()` lets CI upload artifacts for both
passing and failing runs.

## Publishing MetricSpec

MetricSpec's own release workflow lives at `.github/workflows/publish.yml`.
It builds the exact distribution artifacts once, checks them with Twine, stores
them as a workflow artifact, and then publishes that artifact through PyPI
Trusted Publishing.

- Manual `workflow_dispatch` publishes to TestPyPI through the `testpypi`
  GitHub environment.
- Pushing a `v*` tag publishes to PyPI through the `pypi` GitHub environment.
- Only the publish jobs request `id-token: write`; build and test jobs do not
  receive publishing credentials.

Before using the workflow, configure pending Trusted Publishers on both TestPyPI
and PyPI for `.github/workflows/publish.yml` with matching environments
`testpypi` and `pypi`. See [Release checklist](release.md) for the full process.
