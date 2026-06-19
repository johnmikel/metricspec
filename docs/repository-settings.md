# Repository Settings

Use this checklist when creating the public GitHub repository.

## About Section

- Description: `Unit tests for business metrics. Contract testing for analytical meaning.`
- Website: PyPI project URL after publication, or the README until then.
- Topics:
  - `metrics`
  - `analytics`
  - `data-quality`
  - `duckdb`
  - `semantic-layer`
  - `testing`
  - `python`
  - `ci`
  - `open-source`

## Branch Protection

Protect `main`:

- Require pull request reviews before merge.
- Require status checks to pass before merge.
- Required checks:
  - CI / test
- Require branches to be up to date before merge.
- Do not allow force pushes.
- Do not allow deletions.

## Environments

Create these environments before publishing:

- `testpypi`
- `pypi`

Require manual approval for `pypi`. TestPyPI may be left unprotected or may use
the same reviewer rule if you want every publish action to be deliberate.

## Labels

Create these labels before opening the repository for contributors:

- `bug`
- `enhancement`
- `documentation`
- `ci/release`
- `needs-triage`
- `good first issue`
- `help wanted`
- `security`
- `adapter`
- `diagnostics`

## Badges

The README currently uses stable badges that do not depend on PyPI publication:

```markdown
[![CI](https://github.com/johnmikel/metricspec/actions/workflows/ci.yml/badge.svg)](https://github.com/johnmikel/metricspec/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
```

After PyPI publication, add these package badges:

```markdown
[![PyPI](https://img.shields.io/pypi/v/metricspec.svg)](https://pypi.org/project/metricspec/)
[![Python](https://img.shields.io/pypi/pyversions/metricspec.svg)](https://pypi.org/project/metricspec/)
```

If the distribution package name changes, update the PyPI badge URLs while
keeping the CLI command documented as `metricspec`.
