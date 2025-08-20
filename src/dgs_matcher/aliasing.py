"""Alias handling for agency names.

This module exposes a global alias mapping and helpers for expanding
common short names to their canonical agency name.
"""

from __future__ import annotations

from typing import Dict

ALIAS_MAP: Dict[str, str] = {
    "cal fire": "california department of forestry and fire protection",
    "dmv": "department of motor vehicles",
}


def apply_alias(name: str) -> str:
    """Return the canonical agency name for *name*.

    Parameters
    ----------
    name:
        Normalized agency string.

    Returns
    -------
    str
        Canonical form if a mapping exists, otherwise the input *name*.
    """

    return ALIAS_MAP.get(name, name)

__all__ = ["apply_alias", "ALIAS_MAP"]
