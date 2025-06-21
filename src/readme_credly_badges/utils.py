"""Utility functions for handling data."""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def sort_by_field(data: list[dict], field: str = "issued") -> list[dict]:
    """Sort a list of dictionaries by a specified date field (strict, no fallback)."""

    if not data:
        return []

    if field not in {"issued", "updated", "accepted"}:
        raise ValueError(f"Invalid field for sorting: {field}. Use 'issued', 'updated', or 'accepted'.")

    key = f"{field}_at"
    try:
        return sorted(
            data,
            key=lambda x: datetime.fromisoformat(x[key]),
            reverse=True,
        )
    except KeyError as e:
        logger.error(f"Error sorting by {field}: {e}. Returning original data without sorting.")
        return data
