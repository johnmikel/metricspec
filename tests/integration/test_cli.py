from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from typer.testing import CliRunner

from metricspec.cli import app

runner = CliRunner()


def _write_contract(
    directory: Path,
    *,
    name: str = "net_revenue",
    actual_revenue: float = 10.0,
    expected_revenue: float = 10.0,
    description: str | None = None,
    query: str = "queries/net_revenue.sql",
    write_query: bool = True,
) -> Path:
    (directory / "fixtures").mkdir(exist_ok=True)
    (directory / "queries").mkdir(exist_ok=True)
    (directory / "fixtures" / "orders.csv").write_text(
        f"region,net_revenue\nEMEA,{actual_revenue}\n",
        encoding="utf-8",
    )
    if write_query:
        (directory / query).write_text(
            "select region, net_revenue from orders",
            encoding="utf-8",
        )

    description_line = f"description: {description}\n" if description is not None else ""
    contract_path = directory / f"{name}.yaml"
    contract_path.write_text(
        f"""
schema_version: 1
name: {name}
{description_line}adapter: duckdb
fixtures:
  - table: orders
    path: fixtures/orders.csv
query: {query}
expect:
  rows:
    - region: EMEA
      net_revenue: {expected_revenue}
""".strip(),
        encoding="utf-8",
    )
    return contract_path


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


def test_validate_command_uses_grammatical_plural_for_directory(
    tmp_path: Path,
) -> None:
    _write_contract(tmp_path, name="net_revenue")
    _write_contract(tmp_path, name="gross_revenue")

    result = runner.invoke(app, ["validate", str(tmp_path)])

    assert result.exit_code == 0
    assert "2 contracts valid" in result.output


def test_run_command_reports_passing_contract(tmp_path: Path) -> None:
    contract = _write_contract(tmp_path)

    result = runner.invoke(app, ["run", str(contract)])

    assert result.exit_code == 0
    assert "PASS net_revenue" in result.output


def test_run_command_exits_one_for_failing_result(tmp_path: Path) -> None:
    contract = _write_contract(tmp_path, actual_revenue=11.0, expected_revenue=10.0)

    result = runner.invoke(app, ["run", str(contract)])

    assert result.exit_code == 1
    assert "result_mismatch" in result.output


def test_run_invalid_contract_exits_with_stderr_without_traceback(
    tmp_path: Path,
) -> None:
    contract = tmp_path / "broken.yaml"
    contract.write_text("name: broken", encoding="utf-8")

    result = runner.invoke(app, ["run", str(contract)])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert "invalid contract" in result.stderr
    assert "Traceback" not in result.output
    assert isinstance(result.exception, SystemExit)


def test_run_json_outputs_parseable_json_only(tmp_path: Path) -> None:
    contract = _write_contract(tmp_path)

    result = runner.invoke(app, ["run", "--json", str(contract)])

    assert result.exit_code == 0
    assert result.stderr == ""
    report = json.loads(result.stdout)
    assert report["results"][0]["name"] == "net_revenue"
    assert report["results"][0]["passed"] is True


def test_run_junit_writes_xml_without_extra_stdout(tmp_path: Path) -> None:
    contract = _write_contract(tmp_path)
    report_path = tmp_path / "report.xml"

    result = runner.invoke(app, ["run", "--junit", str(report_path), str(contract)])

    assert result.exit_code == 0
    assert "PASS net_revenue" in result.output
    suite = ET.fromstring(report_path.read_text(encoding="utf-8"))
    assert suite.attrib["tests"] == "1"
    assert suite.attrib["failures"] == "0"


def test_run_junit_write_error_exits_before_success_stdout(tmp_path: Path) -> None:
    contract = _write_contract(tmp_path)
    report_path = tmp_path / "missing" / "parent" / "report.xml"

    result = runner.invoke(app, ["run", "--junit", str(report_path), str(contract)])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert "unable to write JUnit report" in result.stderr
    assert "PASS" not in result.output
    assert "Traceback" not in result.output
    assert isinstance(result.exception, SystemExit)


def test_run_missing_query_file_exits_with_concise_stderr(tmp_path: Path) -> None:
    contract = _write_contract(tmp_path, write_query=False)

    result = runner.invoke(app, ["run", str(contract)])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert "unable to run" in result.stderr
    assert "No such file or directory" in result.stderr
    assert "Traceback" not in result.output
    assert isinstance(result.exception, SystemExit)


def test_explain_invalid_contract_exits_with_stderr_without_traceback(
    tmp_path: Path,
) -> None:
    contract = tmp_path / "broken.yaml"
    contract.write_text("name: broken", encoding="utf-8")

    result = runner.invoke(app, ["explain", str(contract)])

    assert result.exit_code == 1
    assert "invalid contract" in result.stderr
    assert "Traceback" not in result.output
    assert isinstance(result.exception, SystemExit)
