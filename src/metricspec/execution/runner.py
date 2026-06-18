from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from metricspec.adapters.duckdb import DuckDbAdapter
from metricspec.checks.results import compare_rows
from metricspec.checks.sql_shape import check_sql_shape
from metricspec.contracts.loader import LoadedContract
from metricspec.diagnostics.events import CheckResult
from metricspec.execution.safety import UnsafeQueryError, validate_read_only_query


@dataclass(frozen=True)
class ContractRunResult:
    name: str
    path: str
    passed: bool
    failure_category: str | None
    checks: list[CheckResult] = field(default_factory=list)
    actual_rows: list[dict[str, Any]] = field(default_factory=list)


def run_loaded_contract(loaded: LoadedContract) -> ContractRunResult:
    contract = loaded.contract
    sql = (loaded.base_dir / contract.query).read_text(encoding="utf-8")

    try:
        validate_read_only_query(sql)
    except UnsafeQueryError as exc:
        return ContractRunResult(
            name=contract.name,
            path=str(loaded.path),
            passed=False,
            failure_category="query_unsafe",
            checks=[CheckResult(passed=False, message=str(exc))],
        )

    adapter = DuckDbAdapter()
    with adapter.session() as session:
        for fixture in contract.fixtures:
            session.load_fixture(fixture, loaded.base_dir)
        actual_rows = session.execute(sql)

    sql_result = check_sql_shape(sql, contract.checks)
    row_result = compare_rows(actual_rows, contract.expect)
    checks = [sql_result, row_result]
    passed = all(check.passed for check in checks)

    failure_category = None
    if not sql_result.passed:
        failure_category = "sql_shape_mismatch"
    elif not row_result.passed:
        failure_category = "result_mismatch"

    return ContractRunResult(
        name=contract.name,
        path=str(loaded.path),
        passed=passed,
        failure_category=failure_category,
        checks=checks,
        actual_rows=actual_rows,
    )
