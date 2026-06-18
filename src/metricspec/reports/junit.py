from __future__ import annotations

import xml.etree.ElementTree as ET

from metricspec.execution.runner import ContractRunResult


def render_junit(results: list[ContractRunResult]) -> str:
    suite = ET.Element(
        "testsuite",
        {
            "name": "metricspec",
            "tests": str(len(results)),
            "failures": str(sum(not result.passed for result in results)),
        },
    )

    for result in results:
        testcase = ET.SubElement(
            suite,
            "testcase",
            {
                "name": result.name,
                "classname": "metricspec",
            },
        )

        if not result.passed:
            failure = ET.SubElement(
                testcase,
                "failure",
                {"message": result.failure_category or "failed"},
            )
            failure.text = "\n".join(
                check.message for check in result.checks if not check.passed
            )

    return ET.tostring(suite, encoding="unicode")
