from __future__ import annotations

import json
from dataclasses import asdict

from metricspec.execution.runner import ContractRunResult


def render_json(results: list[ContractRunResult]) -> str:
    return json.dumps(
        {"results": [asdict(result) for result in results]},
        indent=2,
        default=str,
    )
