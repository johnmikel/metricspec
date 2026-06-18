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
