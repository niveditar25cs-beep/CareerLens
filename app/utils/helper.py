"""
General-purpose helper / utility functions.
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return the current UTC datetime (timezone-aware)."""
    return datetime.now(timezone.utc)


def truncate(text: str, max_length: int = 200) -> str:
    """Truncate a string to a maximum length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def parse_comma_separated(value: str | None) -> list[str]:
    """Parse a comma-separated string into a trimmed list of non-empty items."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]
