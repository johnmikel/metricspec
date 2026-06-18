from __future__ import annotations

import pytest

from metricspec.execution.safety import UnsafeQueryError, validate_read_only_query


@pytest.mark.parametrize(
    "sql",
    [
        "select * from orders",
        "with revenue as (select 1 as value) select * from revenue",
        " select * from orders; ",
    ],
)
def test_validate_read_only_query_accepts_read_only_queries(sql: str) -> None:
    validate_read_only_query(sql)


@pytest.mark.parametrize(
    "sql",
    [
        "",
        "delete from orders",
        "drop table orders",
        "select * from orders; drop table orders",
        "insert into orders values (1)",
        "copy orders to 'orders.csv'",
        "selection from orders",
    ],
)
def test_validate_read_only_query_rejects_unsafe_queries(sql: str) -> None:
    with pytest.raises(UnsafeQueryError):
        validate_read_only_query(sql)


@pytest.mark.parametrize(
    "sql",
    [
        "select * from checkpoint()",
        "select * from force_checkpoint()",
        "select * from truncate_duckdb_logs()",
        "select * from enable_logging()",
        "select * from disable_logging()",
        "select * from enable_profiling()",
        "select * from disable_profiling()",
    ],
)
def test_validate_read_only_query_rejects_duckdb_side_effect_functions(sql: str) -> None:
    with pytest.raises(UnsafeQueryError):
        validate_read_only_query(sql)
