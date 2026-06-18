from __future__ import annotations

import re


class UnsafeQueryError(Exception):
    """Raised when a SQL query is not safe to execute as read-only."""


_FORBIDDEN_SQL_RE = re.compile(
    r"\b(?:alter|attach|create|delete|detach|drop|insert|merge|replace|truncate|update|vacuum)\b"
    r"|\bcopy\b[\s\S]*?\bto\b",
    re.IGNORECASE,
)
_ALLOWED_START_RE = re.compile(r"\A(?:select|with)\b", re.IGNORECASE)
_SIDE_EFFECT_FUNCTIONS = (
    "checkpoint",
    "force_checkpoint",
    "truncate_duckdb_logs",
    "enable_logging",
    "disable_logging",
    "enable_profiling",
    "disable_profiling",
)
_SIDE_EFFECT_FUNCTION_PATTERN = "|".join(re.escape(name) for name in _SIDE_EFFECT_FUNCTIONS)
_SIDE_EFFECT_FUNCTION_RE = re.compile(
    rf'(?<![A-Za-z0-9_])(?:"(?:{_SIDE_EFFECT_FUNCTION_PATTERN})"'
    rf"|(?:{_SIDE_EFFECT_FUNCTION_PATTERN}))\s*\(",
    re.IGNORECASE,
)
_SQL_COMMENT_RE = re.compile(r"--[^\r\n]*|/\*[\s\S]*?\*/")


def validate_read_only_query(sql: str) -> None:
    query = sql.strip()
    if query.endswith(";"):
        query = query[:-1].strip()

    if not query:
        raise UnsafeQueryError("query must not be empty")

    if ";" in query:
        raise UnsafeQueryError("query must contain a single SQL statement")

    if _ALLOWED_START_RE.match(query) is None:
        raise UnsafeQueryError("query must start with SELECT or WITH")

    forbidden_match = _FORBIDDEN_SQL_RE.search(query)
    if forbidden_match is not None:
        raise UnsafeQueryError(
            f"query contains forbidden SQL operation: {forbidden_match.group(0)}"
        )

    side_effect_query = _SQL_COMMENT_RE.sub(" ", query)
    side_effect_match = _SIDE_EFFECT_FUNCTION_RE.search(side_effect_query)
    if side_effect_match is not None:
        raise UnsafeQueryError("query calls side-effecting SQL function")
