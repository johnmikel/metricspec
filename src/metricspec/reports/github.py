from __future__ import annotations

from metricspec.execution.runner import ContractRunResult


def render_github_summary(results: list[ContractRunResult]) -> str:
    passed = sum(result.passed for result in results)
    failed = len(results) - passed

    lines = [
        "## MetricSpec results",
        "",
        f"**{passed} passed, {failed} failed, {len(results)} total**",
        "",
        "| Status | Contract | Category | Path |",
        "| --- | --- | --- | --- |",
    ]

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        category = _inline_code(result.failure_category) if result.failure_category else "-"
        lines.append(
            "| "
            f"{status} | "
            f"{_inline_code(result.name)} | "
            f"{category} | "
            f"{_inline_code(result.path)} |"
        )

    failed_results = [result for result in results if not result.passed]
    if failed_results:
        lines.extend(["", "### Failures"])
        for result in failed_results:
            lines.extend(
                [
                    "",
                    f"#### {result.name}",
                    f"- Path: {_inline_code(result.path)}",
                ]
            )
            if result.failure_category is not None:
                lines.append(f"- Category: {_inline_code(result.failure_category)}")

            for check in result.checks:
                if check.passed:
                    continue

                lines.append(f"- {check.message}")
                for diff in check.diffs[:10]:
                    lines.append(
                        "  - "
                        f"row {diff.row_index} "
                        f"field {_inline_code(diff.field)}: "
                        f"expected {_inline_code(str(diff.expected))}, "
                        f"actual {_inline_code(str(diff.actual))}"
                    )

    return "\n".join(lines) + "\n"


def _inline_code(value: str) -> str:
    return f"`{_escape_markdown_cell(value)}`"


def _escape_markdown_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("`", "\\`").replace("|", "\\|")
