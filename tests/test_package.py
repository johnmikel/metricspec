from __future__ import annotations

import metricspec


def test_package_version() -> None:
    assert metricspec.__version__ == "0.1.0"
