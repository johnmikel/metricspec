from __future__ import annotations

import json
from dataclasses import asdict
from math import isfinite
from typing import Any

from metricspec.execution.runner import ContractRunResult


def _normalize_json_value(value: Any) -> Any:
    if isinstance(value, float) and not isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: _normalize_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_json_value(item) for item in value]
    return value


def render_json(results: list[ContractRunResult]) -> str:
    return json.dumps(
        _normalize_json_value({"results": [asdict(result) for result in results]}),
        indent=2,
        default=str,
        allow_nan=False,
    )
