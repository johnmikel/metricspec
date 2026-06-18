from __future__ import annotations

from pathlib import Path

from metricspec.contracts.loader import load_contract
from metricspec.execution.runner import run_loaded_contract


def test_runner_executes_contract_successfully(tmp_path: Path) -> None:
    (tmp_path / "fixtures").mkdir()
    (tmp_path / "queries").mkdir()
    (tmp_path / "fixtures" / "orders.csv").write_text(
        "region,net_revenue\nEMEA,10.0\n", encoding="utf-8"
    )
    (tmp_path / "queries" / "net_revenue.sql").write_text(
        "select region, net_revenue from orders", encoding="utf-8"
    )
    contract_path = tmp_path / "contract.yaml"
    contract_path.write_text(
        """
schema_version: 1
name: net_revenue
adapter: duckdb
fixtures:
  - table: orders
    path: fixtures/orders.csv
query: queries/net_revenue.sql
expect:
  rows:
    - region: EMEA
      net_revenue: 10.0
""".strip(),
        encoding="utf-8",
    )

    result = run_loaded_contract(load_contract(contract_path))

    assert result.passed


def test_runner_reports_result_failure(tmp_path: Path) -> None:
    (tmp_path / "fixtures").mkdir()
    (tmp_path / "queries").mkdir()
    (tmp_path / "fixtures" / "orders.csv").write_text(
        "region,net_revenue\nEMEA,11.0\n", encoding="utf-8"
    )
    (tmp_path / "queries" / "net_revenue.sql").write_text(
        "select region, net_revenue from orders", encoding="utf-8"
    )
    contract_path = tmp_path / "contract.yaml"
    contract_path.write_text(
        """
schema_version: 1
name: net_revenue
adapter: duckdb
fixtures:
  - table: orders
    path: fixtures/orders.csv
query: queries/net_revenue.sql
expect:
  rows:
    - region: EMEA
      net_revenue: 10.0
""".strip(),
        encoding="utf-8",
    )

    result = run_loaded_contract(load_contract(contract_path))

    assert not result.passed
    assert result.failure_category == "result_mismatch"
