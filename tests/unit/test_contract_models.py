from __future__ import annotations

import pytest
from pydantic import ValidationError

from metricspec.contracts.models import Contract


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
