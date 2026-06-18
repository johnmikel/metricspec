from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from metricspec.contracts.models import Contract, SqlShapeChecks


def test_contract_accepts_minimal_valid_shape() -> None:
    contract = Contract.model_validate(
        {
            "schema_version": 1,
            "name": "net_revenue",
            "adapter": "duckdb",
            "query": "queries/net_revenue.sql",
            "expect": {"rows": [{"region": "EMEA", "net_revenue": 10.0}]},
        }
    )

    assert contract.schema_version == 1
    assert contract.name == "net_revenue"


def test_contract_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "expect": {"rows": []},
                "surprise": True,
            }
        )


def test_contract_rejects_unsupported_schema_version() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 2,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "expect": {"rows": []},
            }
        )


def test_contract_rejects_invalid_tolerance() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "expect": {
                    "rows": [],
                    "numeric_tolerance": {"absolute": -1},
                },
            }
        )


def test_contract_rejects_blank_query_path() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": " ",
                "expect": {"rows": []},
            }
        )


def test_contract_rejects_empty_query_path_object() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": Path(""),
                "expect": {"rows": []},
            }
        )


def test_contract_rejects_blank_fixture_path() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "fixtures": [{"table": "orders", "path": ""}],
                "expect": {"rows": []},
            }
        )


def test_contract_rejects_empty_fixture_path_object() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "fixtures": [{"table": "orders", "path": Path("")}],
                "expect": {"rows": []},
            }
        )


def test_contract_rejects_empty_setup_sql_path_object() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "setup_sql": [Path("")],
                "expect": {"rows": []},
            }
        )


def test_contract_rejects_bool_schema_version() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": True,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "expect": {"rows": []},
            }
        )


def test_contract_rejects_string_tolerance() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "expect": {
                    "rows": [],
                    "numeric_tolerance": {"absolute": "0.01"},
                },
            }
        )


def test_contract_rejects_infinite_tolerance() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "expect": {
                    "rows": [],
                    "numeric_tolerance": {"absolute": float("inf")},
                },
            }
        )


def test_contract_rejects_nan_tolerance() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "expect": {
                    "rows": [],
                    "numeric_tolerance": {"absolute": float("nan")},
                },
            }
        )


def test_contract_rejects_string_allow_extra_columns() -> None:
    with pytest.raises(ValidationError):
        Contract.model_validate(
            {
                "schema_version": 1,
                "name": "net_revenue",
                "adapter": "duckdb",
                "query": "queries/net_revenue.sql",
                "expect": {
                    "rows": [],
                    "allow_extra_columns": "true",
                },
            }
        )


@pytest.mark.parametrize(
    "field",
    [
        "required_sql",
        "forbidden_sql",
        "required_tables",
        "forbidden_tables",
        "required_columns",
        "forbidden_columns",
    ],
)
@pytest.mark.parametrize("blank_value", ["", " "])
def test_sql_shape_checks_reject_blank_entries(field: str, blank_value: str) -> None:
    with pytest.raises(ValidationError):
        SqlShapeChecks.model_validate({field: [blank_value]})
