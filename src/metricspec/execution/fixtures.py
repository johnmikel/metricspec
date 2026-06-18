from __future__ import annotations

from pathlib import Path

from metricspec.contracts.models import Fixture


def resolve_fixture_path(fixture: Fixture, base_dir: Path) -> Path:
    if fixture.path.is_absolute():
        return fixture.path
    return base_dir / fixture.path
