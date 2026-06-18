from __future__ import annotations

from metricspec.checks.sql_shape import check_sql_shape
from metricspec.contracts.models import SqlShapeChecks


def test_required_sql_passes_when_fragment_exists() -> None:
    result = check_sql_shape(
        "select * from orders where is_test_order = false",
        SqlShapeChecks(required_sql=["is_test_order = false"]),
    )

    assert result.passed


def test_required_sql_fails_when_fragment_missing() -> None:
    result = check_sql_shape(
        "select * from orders",
        SqlShapeChecks(required_sql=["is_test_order = false"]),
    )

    assert not result.passed
    assert "Missing required SQL" in result.message


def test_forbidden_sql_fails_when_fragment_exists() -> None:
    result = check_sql_shape(
        "select gross_revenue from orders",
        SqlShapeChecks(forbidden_sql=["gross_revenue"]),
    )

    assert not result.passed
    assert "Forbidden SQL" in result.message


def test_required_table_and_column_failures_are_reported() -> None:
    result = check_sql_shape(
        "select order_id from orders",
        SqlShapeChecks(
            required_tables=["line_items"],
            required_columns=["customer_id"],
        ),
    )

    assert not result.passed
    assert "Missing required table: line_items" in result.message
    assert "Missing required column: customer_id" in result.message


def test_forbidden_table_and_column_failures_are_case_insensitive() -> None:
    result = check_sql_shape(
        "SELECT Orders.Customer_ID FROM Orders",
        SqlShapeChecks(
            forbidden_tables=["orders"],
            forbidden_columns=["customer_id"],
        ),
    )

    assert not result.passed
    assert "Forbidden table present: orders" in result.message
    assert "Forbidden column present: customer_id" in result.message


def test_sql_shape_passes_when_all_configured_fragments_match() -> None:
    result = check_sql_shape(
        "SELECT orders.customer_id FROM orders WHERE is_test_order = FALSE",
        SqlShapeChecks(
            required_sql=["is_test_order = false"],
            required_tables=["orders"],
            required_columns=["customer_id"],
            forbidden_sql=["gross_revenue"],
            forbidden_tables=["internal_orders"],
            forbidden_columns=["debug_flag"],
        ),
    )

    assert result.passed
    assert result.message == "SQL shape checks passed"
