from __future__ import annotations

from metricspec.checks.results import compare_rows
from metricspec.contracts.models import ExpectedResult, NumericTolerance


def test_compare_rows_passes_exact_match() -> None:
    result = compare_rows(
        actual=[{"region": "EMEA", "net_revenue": 10.0}],
        expected=ExpectedResult(rows=[{"region": "EMEA", "net_revenue": 10.0}]),
    )

    assert result.passed


def test_compare_rows_reports_value_delta() -> None:
    result = compare_rows(
        actual=[{"region": "EMEA", "net_revenue": 11.5}],
        expected=ExpectedResult(rows=[{"region": "EMEA", "net_revenue": 10.0}]),
    )

    assert not result.passed
    assert result.diffs[0].field == "net_revenue"
    assert result.diffs[0].expected == 10.0
    assert result.diffs[0].actual == 11.5


def test_compare_rows_honors_absolute_tolerance() -> None:
    result = compare_rows(
        actual=[{"region": "EMEA", "net_revenue": 10.004}],
        expected=ExpectedResult(
            rows=[{"region": "EMEA", "net_revenue": 10.0}],
            numeric_tolerance=NumericTolerance(absolute=0.01),
        ),
    )

    assert result.passed


def test_compare_rows_reports_missing_nullable_expected_field() -> None:
    result = compare_rows(
        actual=[{}],
        expected=ExpectedResult(rows=[{"status": None}]),
    )

    assert not result.passed
    assert result.diffs[0].field == "status"
    assert result.diffs[0].expected is None
    assert result.diffs[0].actual == "<missing>"


def test_compare_rows_rejects_extra_actual_columns_by_default() -> None:
    result = compare_rows(
        actual=[{"region": "EMEA", "extra": 1}],
        expected=ExpectedResult(rows=[{"region": "EMEA"}]),
    )

    assert not result.passed
    assert result.diffs[0].field == "extra"
    assert result.diffs[0].expected == "<unexpected>"
    assert result.diffs[0].actual == 1


def test_compare_rows_allows_extra_actual_columns_when_configured() -> None:
    result = compare_rows(
        actual=[{"region": "EMEA", "extra": 1}],
        expected=ExpectedResult(
            rows=[{"region": "EMEA"}],
            allow_extra_columns=True,
        ),
    )

    assert result.passed


def test_compare_rows_reports_missing_order_by_field_without_raising() -> None:
    result = compare_rows(
        actual=[{"rank": 1, "region": "EMEA"}, {"region": "APAC"}],
        expected=ExpectedResult(
            rows=[
                {"rank": 1, "region": "EMEA"},
                {"rank": 2, "region": "APAC"},
            ],
            order_by=["rank"],
        ),
    )

    assert not result.passed
    assert "order_by" in result.message
    assert result.diffs[0].row_index == 1
    assert result.diffs[0].field == "rank"
    assert result.diffs[0].actual == "<missing>"


def test_compare_rows_matches_exact_non_finite_numeric_values() -> None:
    result = compare_rows(
        actual=[{"ratio": float("inf")}],
        expected=ExpectedResult(rows=[{"ratio": float("inf")}]),
    )

    assert result.passed


def test_compare_rows_reports_mismatched_non_finite_values_without_nan_delta() -> None:
    result = compare_rows(
        actual=[{"ratio": float("-inf")}],
        expected=ExpectedResult(rows=[{"ratio": float("inf")}]),
    )

    assert not result.passed
    assert result.diffs[0].field == "ratio"
    assert result.diffs[0].delta is None
