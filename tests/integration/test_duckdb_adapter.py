from __future__ import annotations

from pathlib import Path

from metricspec.adapters.duckdb import DuckDbAdapter
from metricspec.contracts.models import Fixture


def test_duckdb_adapter_loads_csv_and_executes_query(tmp_path: Path) -> None:
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text("region,net_revenue\nEMEA,10.5\nAMER,2.0\n", encoding="utf-8")
    adapter = DuckDbAdapter()

    with adapter.session() as session:
        session.load_fixture(Fixture(table="orders", path=csv_path), base_dir=tmp_path)
        rows = session.execute("select region, net_revenue from orders order by region")

    assert rows == [
        {"region": "AMER", "net_revenue": 2.0},
        {"region": "EMEA", "net_revenue": 10.5},
    ]
