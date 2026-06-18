# Security

MetricSpec should not send telemetry or make hidden network calls. The stable
core runs local DuckDB fixture tests and should be safe to use without granting
network access or service credentials.

## Credentials

- Do not put credentials, tokens, connection strings, or secrets in contracts,
  fixtures, metadata, issue reports, or CI artifacts.
- Use synthetic examples when reporting bugs.
- Redact customer identifiers, hostnames, and internal paths unless they are
  necessary for a private security report.

## Live Database Safety

The stable v1 core is fixture-based. Avoid running MetricSpec against live
production databases. Future live adapters should use read-only, least-privilege
credentials and isolated test data.

## Fixture Data

- Prefer small synthetic fixtures that encode the metric edge case directly.
- Do not commit production exports, personal data, secrets, or customer data.
- If a real data sample is unavoidable, minimize it, anonymize it, and keep it
  out of public issues and public repositories.

## SQL Safety Guards

MetricSpec applies read-only query checks before executing contract queries. The
current guard requires a single `SELECT` or `WITH` statement and blocks common
mutating operations.

These checks are guardrails, not a complete SQL sandbox. They use static text
checks and cannot prove that every possible SQL expression is safe. Review query
files, run tests in isolated environments, and treat `.sql` fixture files as
trusted setup code because they are executed to prepare the DuckDB session.
