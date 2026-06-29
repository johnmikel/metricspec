from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from metricspec.cli import app

runner = CliRunner()


def test_init_demo_creates_runnable_project(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "demo"])

    assert result.exit_code == 0
    assert "metricspec-demo" in result.output

    demo = tmp_path / "metricspec-demo"
    expected_files = [
        "README.md",
        "contracts/net_revenue_by_region.pass.yaml",
        "contracts/net_revenue_by_region.fail.yaml",
        "fixtures/orders.csv",
        "fixtures/refunds.csv",
        "queries/net_revenue_by_region.pass.sql",
        "queries/net_revenue_by_region.fail.sql",
    ]
    for relative_path in expected_files:
        assert (demo / relative_path).is_file()

    monkeypatch.chdir(demo)
    pass_result = runner.invoke(
        app, ["run", "contracts/net_revenue_by_region.pass.yaml"]
    )
    fail_result = runner.invoke(
        app, ["run", "contracts/net_revenue_by_region.fail.yaml"]
    )

    assert pass_result.exit_code == 0
    assert "PASS net_revenue_by_region_pass" in pass_result.output
    assert fail_result.exit_code == 1
    assert "FAIL net_revenue_by_region_fail" in fail_result.output
    assert "result_mismatch" in fail_result.output
