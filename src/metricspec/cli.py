from __future__ import annotations

from pathlib import Path
from typing import NoReturn

import typer

from metricspec.contracts.loader import (
    ContractLoadError,
    LoadedContract,
    discover_contracts,
    load_contract,
)
from metricspec.diagnostics.renderers import render_human_result
from metricspec.execution.runner import ContractRunResult, run_loaded_contract
from metricspec.reports.json import render_json
from metricspec.reports.junit import render_junit

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """MetricSpec command-line interface."""


def _exit_cli_error(message: str) -> NoReturn:
    typer.echo(message, err=True)
    raise typer.Exit(1)


def _exit_contract_load_error(error: ContractLoadError) -> NoReturn:
    _exit_cli_error(str(error))


def _discover_contracts_or_exit(path: Path) -> list[Path]:
    try:
        return discover_contracts(path)
    except ContractLoadError as error:
        _exit_contract_load_error(error)


def _load_contracts_or_exit(contract_paths: list[Path]) -> list[LoadedContract]:
    loaded_contracts: list[LoadedContract] = []
    for contract_path in contract_paths:
        try:
            loaded_contracts.append(load_contract(contract_path))
        except ContractLoadError as error:
            _exit_contract_load_error(error)
    return loaded_contracts


def _run_contracts_or_exit(
    loaded_contracts: list[LoadedContract],
) -> list[ContractRunResult]:
    results: list[ContractRunResult] = []
    for loaded in loaded_contracts:
        try:
            results.append(run_loaded_contract(loaded))
        except OSError as error:
            _exit_cli_error(f"{loaded.path}: unable to run contract: {error}")
    return results


@app.command()
def validate(path: Path = typer.Argument(Path("contracts"))) -> None:  # noqa: B008
    contract_paths = _discover_contracts_or_exit(path)
    _load_contracts_or_exit(contract_paths)

    contract_count = len(contract_paths)
    contract_label = "contract" if contract_count == 1 else "contracts"
    typer.echo(f"{contract_count} {contract_label} valid")


@app.command()
def run(  # noqa: B008
    path: Path = typer.Argument(Path("contracts")),  # noqa: B008
    json_output: bool = typer.Option(False, "--json", help="Emit JSON report."),  # noqa: B008
    junit: Path | None = typer.Option(  # noqa: B008
        None,
        "--junit",
        help="Write JUnit XML report.",
    ),
) -> None:
    contract_paths = _discover_contracts_or_exit(path)
    loaded_contracts = _load_contracts_or_exit(contract_paths)
    results = _run_contracts_or_exit(loaded_contracts)

    if junit is not None:
        try:
            junit.write_text(render_junit(results), encoding="utf-8")
        except OSError as error:
            _exit_cli_error(f"{junit}: unable to write JUnit report: {error}")

    if json_output:
        typer.echo(render_json(results))
    else:
        for result in results:
            typer.echo(render_human_result(result))

    if any(not result.passed for result in results):
        raise typer.Exit(1)


@app.command()
def explain(path: Path) -> None:
    try:
        loaded = load_contract(path)
    except ContractLoadError as error:
        _exit_contract_load_error(error)

    description = loaded.contract.description or "No description"
    typer.echo(f"{loaded.contract.name}: {description}")
