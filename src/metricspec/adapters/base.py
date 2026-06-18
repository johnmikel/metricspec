from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from metricspec.contracts.models import Fixture


class AdapterSession(Protocol):
    def load_fixture(self, fixture: Fixture, base_dir: Path) -> None: ...

    def execute(self, sql: str) -> list[dict[str, Any]]: ...


class Adapter(Protocol):
    def session(self) -> Any: ...
