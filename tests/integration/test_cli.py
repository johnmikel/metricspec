from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from metricspec.cli import app

runner = CliRunner()


def test_validate_command_succeeds_for_valid_contract(tmp_path: Path) -> None:
    contract = tmp_path / "contract.yaml"
    contract.write_text(
        """
schema_version: 1
name: net_revenue
adapter: duckdb
query: queries/net_revenue.sql
expect:
  rows: []
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", str(contract)])

    assert result.exit_code == 0
    assert "1 contract valid" in result.output
