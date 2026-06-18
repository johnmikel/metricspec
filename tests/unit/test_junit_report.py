from __future__ import annotations

from metricspec.diagnostics.events import CheckResult
from metricspec.execution.runner import ContractRunResult
from metricspec.reports.junit import render_junit


def test_render_junit_contains_testcase() -> None:
    xml = render_junit(
        [
            ContractRunResult(
                name="net_revenue",
                path="contract.yaml",
                passed=True,
                failure_category=None,
            )
        ]
    )

    assert "<testsuite" in xml
    assert 'name="net_revenue"' in xml


def test_render_junit_includes_failure_messages() -> None:
    xml = render_junit(
        [
            ContractRunResult(
                name="net_revenue",
                path="contract.yaml",
                passed=False,
                failure_category="result_mismatch",
                checks=[
                    CheckResult(passed=False, message="Rows differ"),
                    CheckResult(passed=True, message="SQL shape matched"),
                ],
            )
        ]
    )

    assert 'failures="1"' in xml
    assert '<failure message="result_mismatch">Rows differ</failure>' in xml
    assert "SQL shape matched" not in xml
