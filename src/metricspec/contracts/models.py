from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NumericTolerance(StrictModel):
    absolute: float = Field(ge=0)


class ExpectedResult(StrictModel):
    rows: list[dict[str, Any]]
    numeric_tolerance: NumericTolerance | None = None
    order_by: list[str] = Field(default_factory=list)
    allow_extra_columns: bool = False


class Fixture(StrictModel):
    table: str = Field(min_length=1)
    path: Path


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
    setup_sql: list[Path] = Field(default_factory=list)
    query: Path
    expect: ExpectedResult
    checks: SqlShapeChecks = Field(default_factory=SqlShapeChecks)
    metadata: dict[str, Any] = Field(default_factory=dict)
