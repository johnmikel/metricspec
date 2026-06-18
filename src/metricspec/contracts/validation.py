from __future__ import annotations

from metricspec.contracts.loader import ContractLoadError


def format_contract_error(error: ContractLoadError) -> str:
    return str(error)
