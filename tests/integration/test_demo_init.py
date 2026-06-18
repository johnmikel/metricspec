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
