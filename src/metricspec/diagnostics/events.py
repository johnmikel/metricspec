from __future__ import annotations

from dataclasses import dataclass, field

from metricspec.diagnostics.diff import ValueDiff


@dataclass(frozen=True)
class CheckResult:
    passed: bool
    message: str
    diffs: list[ValueDiff] = field(default_factory=list)
