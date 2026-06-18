from __future__ import annotations

import json

from metricspec.diagnostics.diff import ValueDiff
from metricspec.diagnostics.events import CheckResult
from metricspec.diagnostics.renderers import render_human_result
from metricspec.execution.runner import ContractRunResult
from metricspec.reports.json import render_json


def test_render_human_result_includes_failure_category() -> None:
    rendered = render_human_result(
        ContractRunResult(
            name="net_revenue",
            path="contract.yaml",
            passed=False,
            failure_category="result_mismatch",
            checks=[CheckResult(passed=False, message="Rows differ")],
        )
    )

    assert "net_revenue" in rendered
    assert "result_mismatch" in rendered
    assert "Rows differ" in rendered


def test_render_human_result_includes_first_ten_failed_check_diffs() -> None:
    rendered = render_human_result(
        ContractRunResult(
            name="net_revenue",
            path="contract.yaml",
            passed=False,
            failure_category="result_mismatch",
            checks=[
                CheckResult(
                    passed=False,
                    message="Rows differ",
                    diffs=[
                        ValueDiff(
                            row_index=index,
                            field="net_revenue",
                            expected=10,
                            actual=11,
                        )
                        for index in range(11)
                    ],
                )
            ],
        )
    )

    assert "row 0" in rendered
    assert "field net_revenue" in rendered
    assert "expected 10" in rendered
    assert "actual 11" in rendered
    assert "row 9" in rendered
    assert "row 10" not in rendered


def test_render_json_serializes_results_object() -> None:
    rendered = render_json(
        [
            ContractRunResult(
                name="net_revenue",
                path="contract.yaml",
                passed=True,
                failure_category=None,
            )
        ]
    )

    payload = json.loads(rendered)

    assert payload == {
        "results": [
            {
                "name": "net_revenue",
                "path": "contract.yaml",
                "passed": True,
                "failure_category": None,
                "checks": [],
                "actual_rows": [],
            }
        ]
    }
