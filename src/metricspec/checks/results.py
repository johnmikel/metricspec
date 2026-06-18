from __future__ import annotations

import math
from numbers import Real
from typing import Any

from metricspec.contracts.models import ExpectedResult
from metricspec.diagnostics.diff import ValueDiff
from metricspec.diagnostics.events import CheckResult

MISSING_VALUE = "<missing>"
UNEXPECTED_VALUE = "<unexpected>"


def compare_rows(actual: list[dict[str, Any]], expected: ExpectedResult) -> CheckResult:
    missing_order_by = _find_missing_order_by(actual, expected.order_by, "actual")
    if missing_order_by is not None:
        return missing_order_by

    missing_order_by = _find_missing_order_by(expected.rows, expected.order_by, "expected")
    if missing_order_by is not None:
        return missing_order_by

    try:
        actual_rows = _sort_rows(actual, expected.order_by)
        expected_rows = _sort_rows(expected.rows, expected.order_by)
    except TypeError as exc:
        return CheckResult(
            passed=False,
            message=f"Could not sort rows by order_by fields {expected.order_by}: {exc}",
        )

    if len(actual_rows) != len(expected_rows):
        return CheckResult(
            passed=False,
            message=f"Expected {len(expected_rows)} rows but got {len(actual_rows)} rows",
        )

    absolute_tolerance = (
        expected.numeric_tolerance.absolute if expected.numeric_tolerance is not None else 0.0
    )
    diffs: list[ValueDiff] = []

    row_pairs = zip(actual_rows, expected_rows, strict=True)
    for row_index, (actual_row, expected_row) in enumerate(row_pairs):
        for field, expected_value in expected_row.items():
            if field not in actual_row:
                diffs.append(
                    ValueDiff(
                        row_index=row_index,
                        field=field,
                        expected=expected_value,
                        actual=MISSING_VALUE,
                    )
                )
                continue

            actual_value = actual_row[field]
            diff = _compare_value(
                row_index=row_index,
                field=field,
                expected_value=expected_value,
                actual_value=actual_value,
                absolute_tolerance=absolute_tolerance,
            )
            if diff is not None:
                diffs.append(diff)

        if not expected.allow_extra_columns:
            for field, actual_value in actual_row.items():
                if field not in expected_row:
                    diffs.append(
                        ValueDiff(
                            row_index=row_index,
                            field=field,
                            expected=UNEXPECTED_VALUE,
                            actual=actual_value,
                        )
                    )

    if diffs:
        return CheckResult(passed=False, message="Rows differ", diffs=diffs)

    return CheckResult(passed=True, message="Rows match")


def _find_missing_order_by(
    rows: list[dict[str, Any]], order_by: list[str], row_kind: str
) -> CheckResult | None:
    for row_index, row in enumerate(rows):
        for field in order_by:
            if field not in row:
                return CheckResult(
                    passed=False,
                    message=f"Missing order_by field '{field}' in {row_kind} row {row_index}",
                    diffs=[
                        ValueDiff(
                            row_index=row_index,
                            field=field,
                            expected="<order_by>",
                            actual=MISSING_VALUE,
                        )
                    ],
                )

    return None


def _sort_rows(rows: list[dict[str, Any]], order_by: list[str]) -> list[dict[str, Any]]:
    if not order_by:
        return rows

    return sorted(rows, key=lambda row: tuple(row[field] for field in order_by))


def _is_finite_number(value: Any) -> bool:
    return math.isfinite(value)


def _compare_value(
    *,
    row_index: int,
    field: str,
    expected_value: Any,
    actual_value: Any,
    absolute_tolerance: float,
) -> ValueDiff | None:
    if _is_numeric(expected_value) and _is_numeric(actual_value):
        if actual_value == expected_value:
            return None

        if not _is_finite_number(expected_value) or not _is_finite_number(actual_value):
            return ValueDiff(
                row_index=row_index,
                field=field,
                expected=expected_value,
                actual=actual_value,
            )

        delta = float(actual_value) - float(expected_value)
        if abs(delta) <= absolute_tolerance:
            return None
        return ValueDiff(
            row_index=row_index,
            field=field,
            expected=expected_value,
            actual=actual_value,
            delta=delta,
        )

    if actual_value == expected_value:
        return None

    return ValueDiff(
        row_index=row_index,
        field=field,
        expected=expected_value,
        actual=actual_value,
    )


def _is_numeric(value: Any) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool)
