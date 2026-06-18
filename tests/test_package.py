from __future__ import annotations

from typer.testing import CliRunner

import metricspec
from metricspec.cli import app


def test_package_version() -> None:
    assert metricspec.__version__ == "0.1.0"


def test_cli_help() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.output
