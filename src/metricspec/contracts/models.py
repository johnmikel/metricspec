from __future__ import annotations

import math
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, StrictBool


def _reject_blank_path(value: Any) -> Any:
    if isinstance(value, str) and not value.strip():
        raise ValueError("path must not be empty")
    return value


def _validate_tolerance_number(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError("absolute tolerance must be a number")
    numeric_value = float(value)
    if not math.isfinite(numeric_value):
        raise ValueError("absolute tolerance must be finite")
    return numeric_value


NonEmptyPath = Annotated[Path, BeforeValidator(_reject_blank_path)]
ToleranceNumber = Annotated[float, BeforeValidator(_validate_tolerance_number), Field(ge=0)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NumericTolerance(StrictModel):
    absolute: ToleranceNumber


class ExpectedResult(StrictModel):
    rows: list[dict[str, Any]]
    numeric_tolerance: NumericTolerance | None = None
    order_by: list[str] = Field(default_factory=list)
    allow_extra_columns: StrictBool = False


class Fixture(StrictModel):
    table: str = Field(min_length=1)
    path: NonEmptyPath


class SqlShapeChecks(StrictModel):
    required_sql: list[str] = Field(default_factory=list)
    forbidden_sql: list[str] = Field(default_factory=list)
    required_tables: list[str] = Field(default_factory=list)
    forbidden_tables: list[str] = Field(default_factory=list)
    required_columns: list[str] = Field(default_factory=list)
    forbidden_columns: list[str] = Field(default_factory=list)


class Contract(StrictModel):
    schema_version: Literal[1]
    name: str = Field(min_length=1)
    description: str | None = None
    severity: Literal["low", "medium", "high", "critical"] = "medium"
    owner: str | None = None
    tags: list[str] = Field(default_factory=list)
    adapter: Literal["duckdb"]
    connection: dict[str, Any] = Field(default_factory=dict)
    fixtures: list[Fixture] = Field(default_factory=list)
    setup_sql: list[NonEmptyPath] = Field(default_factory=list)
    query: NonEmptyPath
    expect: ExpectedResult
    checks: SqlShapeChecks = Field(default_factory=SqlShapeChecks)
    metadata: dict[str, Any] = Field(default_factory=dict)
