from __future__ import annotations

from metricspec.contracts.models import SqlShapeChecks
from metricspec.diagnostics.events import CheckResult


def check_sql_shape(sql: str, checks: SqlShapeChecks) -> CheckResult:
    normalized_sql = sql.lower()
    failures: list[str] = []

    for fragment in checks.required_sql:
        if fragment.lower() not in normalized_sql:
            failures.append(f"Missing required SQL: {fragment}")

    for fragment in checks.forbidden_sql:
        if fragment.lower() in normalized_sql:
            failures.append(f"Forbidden SQL present: {fragment}")

    for table in checks.required_tables:
        if table.lower() not in normalized_sql:
            failures.append(f"Missing required table: {table}")

    for table in checks.forbidden_tables:
        if table.lower() in normalized_sql:
            failures.append(f"Forbidden table present: {table}")

    for column in checks.required_columns:
        if column.lower() not in normalized_sql:
            failures.append(f"Missing required column: {column}")

    for column in checks.forbidden_columns:
        if column.lower() in normalized_sql:
            failures.append(f"Forbidden column present: {column}")

    if failures:
        return CheckResult(passed=False, message="; ".join(failures))

    return CheckResult(passed=True, message="SQL shape checks passed")
