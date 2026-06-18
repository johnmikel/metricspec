from __future__ import annotations

from importlib import resources

from typer.testing import CliRunner

import metricspec
from metricspec.cli import app


def test_package_version() -> None:
    assert metricspec.__version__ == "0.1.0"


def test_package_includes_pep_561_marker() -> None:
    marker = resources.files("metricspec").joinpath("py.typed")

    assert marker.is_file()
    assert marker.read_text(encoding="utf-8") == ""


def test_cli_help() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.output
