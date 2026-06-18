from __future__ import annotations

from metricspec.execution.runner import ContractRunResult


def render_human_result(result: ContractRunResult) -> str:
    status = "PASS" if result.passed else "FAIL"
    lines = [f"{status} {result.name} ({result.path})"]

    if result.failure_category is not None:
        lines.append(f"category: {result.failure_category}")

    for check in result.checks:
        if check.passed:
            continue

        lines.append(f"- {check.message}")
        for diff in check.diffs[:10]:
            lines.append(
                "  "
                f"row {diff.row_index} "
                f"field {diff.field}: "
                f"expected {diff.expected}, "
                f"actual {diff.actual}"
            )

    return "\n".join(lines)
