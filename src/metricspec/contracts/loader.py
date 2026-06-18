from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import yaml  # type: ignore[import-untyped]
from pydantic import ValidationError

from metricspec.contracts.models import Contract


class ContractLoadError(Exception):
    """Raised when a contract file cannot be loaded or validated."""


@dataclass(frozen=True)
class LoadedContract:
    path: Path
    base_dir: Path
    contract: Contract


def discover_contracts(path: Path) -> list[Path]:
    if not path.exists():
        raise ContractLoadError(f"{path}: path does not exist")
    if path.is_file():
        return [path]
    if not path.is_dir():
        raise ContractLoadError(f"{path}: path is not a file or directory")

    return sorted(
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file() and candidate.suffix in {".yaml", ".yml"}
    )


def load_contract(path: Path) -> LoadedContract:
    try:
        loaded_yaml = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ContractLoadError(f"{path}: invalid YAML: {exc}") from exc
    except OSError as exc:
        raise ContractLoadError(f"{path}: unable to read contract: {exc}") from exc

    if not isinstance(loaded_yaml, Mapping):
        raise ContractLoadError(f"{path}: contract YAML must contain a mapping")

    try:
        contract = Contract.model_validate(loaded_yaml)
    except ValidationError as exc:
        raise ContractLoadError(f"{path}: invalid contract: {exc}") from exc

    return LoadedContract(path=path, base_dir=path.parent, contract=contract)
