from __future__ import annotations

from pathlib import Path

import pytest

from metricspec.contracts.loader import ContractLoadError, discover_contracts, load_contract
from metricspec.contracts.validation import format_contract_error


def test_load_contract_reads_yaml(tmp_path: Path) -> None:
    path = tmp_path / "contract.yaml"
    path.write_text(
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

    loaded = load_contract(path)

    assert loaded.contract.name == "net_revenue"
    assert loaded.path == path
    assert loaded.base_dir == tmp_path


def test_load_contract_wraps_validation_errors(tmp_path: Path) -> None:
    path = tmp_path / "contract.yaml"
    path.write_text("name: broken", encoding="utf-8")

    with pytest.raises(ContractLoadError) as exc:
        load_contract(path)

    message = str(exc.value)
    assert "contract.yaml" in message
    assert "invalid contract" in message


def test_load_contract_wraps_yaml_errors(tmp_path: Path) -> None:
    path = tmp_path / "contract.yaml"
    path.write_text("schema_version: [", encoding="utf-8")

    with pytest.raises(ContractLoadError) as exc:
        load_contract(path)

    message = str(exc.value)
    assert "contract.yaml" in message
    assert "invalid YAML" in message


def test_load_contract_rejects_non_mapping_yaml(tmp_path: Path) -> None:
    path = tmp_path / "contract.yaml"
    path.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

    with pytest.raises(ContractLoadError) as exc:
        load_contract(path)

    assert "contract.yaml" in str(exc.value)
    assert "mapping" in str(exc.value)


def test_discover_contracts_accepts_file_or_directory(tmp_path: Path) -> None:
    first = tmp_path / "first.yaml"
    second_dir = tmp_path / "nested"
    second_dir.mkdir()
    second = second_dir / "second.yml"
    ignored = second_dir / "ignored.txt"
    first.write_text(
        "schema_version: 1\nname: a\nadapter: duckdb\nquery: q.sql\nexpect:\n  rows: []",
        encoding="utf-8",
    )
    second.write_text(
        "schema_version: 1\nname: b\nadapter: duckdb\nquery: q.sql\nexpect:\n  rows: []",
        encoding="utf-8",
    )
    ignored.write_text("schema_version: 1", encoding="utf-8")

    assert discover_contracts(first) == [first]
    assert discover_contracts(tmp_path) == [first, second]


def test_discover_contracts_rejects_missing_path(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    with pytest.raises(ContractLoadError) as exc:
        discover_contracts(missing)

    assert str(missing) in str(exc.value)


def test_format_contract_error_returns_error_message() -> None:
    error = ContractLoadError("contract.yaml: invalid contract")

    assert format_contract_error(error) == "contract.yaml: invalid contract"
