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
