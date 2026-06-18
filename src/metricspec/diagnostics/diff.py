from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValueDiff:
    row_index: int
    field: str
    expected: Any
    actual: Any
    delta: float | None = None
