from __future__ import annotations

from metricspec.diagnostics.diff import ValueDiff
from metricspec.diagnostics.events import CheckResult
from metricspec.execution.runner import ContractRunResult
from metricspec.reports.github import render_github_summary


def test_render_github_summary_includes_totals_and_failure_details() -> None:
    rendered = render_github_summary(
        [
            ContractRunResult(
                name="net_revenue",
                path="contracts/net_revenue.yaml",
                passed=True,
                failure_category=None,
            ),
            ContractRunResult(
                name="gross|margin",
                path="contracts/gross_margin.yaml",
                passed=False,
                failure_category="result_mismatch",
                checks=[
                    CheckResult(
                        passed=False,
                        message="Rows differ",
                        diffs=[
                            ValueDiff(
                                row_index=1,
                                field="gross_margin",
                                expected=0.42,
                                actual=0.4,
                            )
                        ],
                    )
                ],
            ),
        ]
    )

    assert "## MetricSpec results" in rendered
    assert "**1 passed, 1 failed, 2 total**" in rendered
    assert "| PASS | `net_revenue` | - | `contracts/net_revenue.yaml` |" in rendered
    assert "| FAIL | `gross\\|margin` | `result_mismatch` |" in rendered
    assert "### Failures" in rendered
    assert "#### gross|margin" in rendered
    assert "- Rows differ" in rendered
    assert "- row 1 field `gross_margin`: expected `0.42`, actual `0.4`" in rendered


def test_render_github_summary_limits_diff_details() -> None:
    rendered = render_github_summary(
        [
            ContractRunResult(
                name="net_revenue",
                path="contracts/net_revenue.yaml",
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
        ]
    )

    assert "row 0" in rendered
    assert "row 9" in rendered
    assert "row 10" not in rendered
