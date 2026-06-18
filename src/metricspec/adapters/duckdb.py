from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import duckdb

from metricspec.contracts.models import Fixture
from metricspec.execution.fixtures import resolve_fixture_path


def _quote_identifier(identifier: str) -> str:
    if not identifier.strip():
        raise ValueError("identifier must not be blank")
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


class DuckDbSession:
    def __init__(self) -> None:
        self._connection = duckdb.connect(database=":memory:")

    def close(self) -> None:
        self._connection.close()

    def load_fixture(self, fixture: Fixture, base_dir: Path) -> None:
        path = resolve_fixture_path(fixture, base_dir)
        suffix = path.suffix.lower()

        if suffix == ".csv":
            table = _quote_identifier(fixture.table)
            self._connection.execute(
                f"create or replace table {table} as select * from read_csv_auto(?)",
                [str(path)],
            )
            return

        if suffix == ".parquet":
            table = _quote_identifier(fixture.table)
            self._connection.execute(
                f"create or replace table {table} as select * from read_parquet(?)",
                [str(path)],
            )
            return

        if suffix == ".sql":
            self._connection.execute(path.read_text(encoding="utf-8"))
            return

        raise ValueError(f"unsupported fixture file suffix: {path.suffix}")

    def execute(self, sql: str) -> list[dict[str, Any]]:
        cursor = self._connection.execute(sql)
        columns = [column[0] for column in cursor.description or []]
        return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]


class DuckDbAdapter:
    @contextmanager
    def session(self) -> Iterator[DuckDbSession]:
        session = DuckDbSession()
        try:
            yield session
        finally:
            session.close()
