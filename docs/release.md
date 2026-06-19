# Release Checklist

MetricSpec releases use GitHub Actions, built artifacts, and PyPI Trusted
Publishing. The CLI command stays `metricspec` even if the distribution package
name has to change before publication.

## One-Time Setup

1. Create the public GitHub repository and push `main`.
   - Use `docs/repository-settings.md` for repository description, topics,
     branch protection, environments, and badges.
2. Confirm the distribution package name.
   - If `metricspec` is available, keep `[project].name = "metricspec"`.
   - If it is not available, choose the nearest clear distribution name and keep
     `[project.scripts].metricspec = "metricspec.cli:app"`.
3. Create GitHub environments:
   - `testpypi`
   - `pypi`
4. Add a required reviewer to the `pypi` environment.
5. Configure a pending Trusted Publisher on TestPyPI:
   - Owner: the GitHub owner or organization.
   - Repository: the MetricSpec repository name.
   - Workflow: `.github/workflows/publish.yml`.
   - Environment: `testpypi`.
6. Configure the same Trusted Publisher on PyPI with environment `pypi`.

Trusted Publishing does not use long-lived API tokens. The publish jobs request
GitHub OIDC with `id-token: write` only in the jobs that upload artifacts.

## Pre-Release Checks

Run from a clean checkout:

```bash
git status --short
uv run ruff check .
uv run mypy src
uv run pytest --cov=metricspec --cov-report=term-missing
rm -rf dist
uv run python -m build
uv run twine check dist/*
```

Confirm:

- `CHANGELOG.md` has the release date and version notes.
- `pyproject.toml` has the intended version.
- `README.md` and `docs/getting-started.md` match the intended install path.
- The demo still works from the built wheel.

## TestPyPI Release

1. Push the release-prep commit to `main`.
2. In GitHub Actions, run `Publish` manually with target `testpypi`.
3. Wait for the `testpypi` environment deployment to finish.
4. Install from TestPyPI in a clean virtual environment. TestPyPI usually does
   not contain all dependencies, so keep PyPI as an extra index:

```bash
VERSION=0.1.0
tmpdir=$(mktemp -d)
python3 -m venv "$tmpdir/venv"
"$tmpdir/venv/bin/python" -m pip install --upgrade pip
"$tmpdir/venv/bin/pip" install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  "metricspec==$VERSION"
cd "$tmpdir"
"$tmpdir/venv/bin/metricspec" init demo
cd metricspec-demo
"$tmpdir/venv/bin/metricspec" run contracts/net_revenue_by_region.pass.yaml
```

Expected: demo initialization succeeds and the pass contract exits `0`.

## PyPI Release

1. Create and push a signed tag:

```bash
VERSION=0.1.0
git tag -s "v$VERSION" -m "MetricSpec v$VERSION"
git push origin "v$VERSION"
```

2. Approve the `pypi` environment deployment in GitHub Actions.
3. Smoke-test the published package:

```bash
tmpdir=$(mktemp -d)
cd "$tmpdir"
uvx metricspec init demo
cd metricspec-demo
uvx metricspec run contracts/net_revenue_by_region.pass.yaml
uvx metricspec run contracts/net_revenue_by_region.fail.yaml
```

Expected:

- Pass contract exits `0`.
- Fail contract exits `1` and prints `result_mismatch`.

## GitHub Release

Create a GitHub Release from the tag with:

- One-sentence project summary.
- Install command.
- Demo commands.
- Link to `docs/getting-started.md`.
- Link to `docs/security.md`.
- Known limitations: DuckDB fixture adapter only, `connection` and `setup_sql`
  are reserved in v1, and SQL-shape checks are text guardrails rather than a
  parser.

## Rollback

PyPI files cannot be overwritten. If a release is broken:

1. Yank the bad release on PyPI.
2. Open a GitHub issue with impact and workaround.
3. Bump the version.
4. Release a fixed version through TestPyPI first, then PyPI.
