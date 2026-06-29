from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from metricspec.cli import app


def _write_passing_contract(project: Path) -> Path:
    contracts = project / "contracts"
    queries = project / "queries"
    contracts.mkdir()
    queries.mkdir()

    query = queries / "net_revenue.sql"
    query.write_text(
        "select 'EMEA' as region, 100.0 as net_revenue\n",
        encoding="utf-8",
    )

    contract = contracts / "net_revenue.yaml"
    contract.write_text(
        """
schema_version: 1
name: net_revenue
adapter: duckdb
query: ../queries/net_revenue.sql
expect:
  rows:
    - region: EMEA
      net_revenue: 100.0
""".strip(),
        encoding="utf-8",
    )
    return contract


def test_run_writes_github_summary_file(
    tmp_path: Path, monkeypatch
) -> None:
    contract = _write_passing_contract(tmp_path)
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))

    result = CliRunner().invoke(app, ["run", str(contract), "--github-summary"])

    assert result.exit_code == 0
    assert "PASS net_revenue" in result.stdout
    assert "## MetricSpec results" in summary.read_text(encoding="utf-8")


def test_run_reports_missing_github_summary_env(tmp_path: Path, monkeypatch) -> None:
    contract = _write_passing_contract(tmp_path)
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

    result = CliRunner().invoke(app, ["run", str(contract), "--github-summary"])

    assert result.exit_code == 1
    assert "GITHUB_STEP_SUMMARY is not set" in result.output
