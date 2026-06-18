from __future__ import annotations

from pathlib import Path

from metricspec.contracts.models import Fixture
from metricspec.execution.fixtures import resolve_fixture_path


def test_resolve_fixture_path_resolves_relative_path_against_base_dir(tmp_path: Path) -> None:
    fixture = Fixture(table="orders", path=Path("fixtures/orders.csv"))

    assert resolve_fixture_path(fixture, tmp_path) == tmp_path / "fixtures/orders.csv"
