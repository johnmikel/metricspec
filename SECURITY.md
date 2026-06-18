# Security Policy

MetricSpec should not send telemetry or make hidden network calls.

Report vulnerabilities privately by opening a GitHub security advisory once the repository is public.
Do not include credentials, production data, or secrets in issues.

## Supported Scope

The stable core runs deterministic DuckDB fixture tests locally. Treat future
live database adapters as experimental until their security model is documented.

## Reporting Guidance

- Use synthetic contracts, fixtures, and SQL in reports whenever possible.
- Redact tokens, connection strings, customer identifiers, and internal hostnames.
- Include the MetricSpec version, command, expected behavior, and actual behavior.
