"""Text normalization utilities.

Functions in this module perform lightweight cleanup on free-text agency
names so they can be compared semantically. Normalization is intentionally
simple to keep the package dependency-light and easy to reason about.
"""

from __future__ import annotations

import re
from typing import Dict

# basic abbreviation map used during normalization
ABBREVIATIONS: Dict[str, str] = {
    "dept": "department",
    "dept.": "department",
    "ca": "california",
}

_punct_re = re.compile(r"[\.,;:!\-_/\\]")


def expand_abbreviations(text: str) -> str:
    """Expand common abbreviations in *text*.

    Parameters
    ----------
    text:
        Input string to normalize.

    Returns
    -------
    str
        Text with abbreviations replaced using :data:`ABBREVIATIONS`.
    """

    words = [ABBREVIATIONS.get(w, w) for w in text.split()]
    return " ".join(words)


def normalize_text(text: str) -> str:
    """Normalize *text* for matching.

    The operation performs lowercasing, punctuation removal and
    abbreviation expansion.

    Parameters
    ----------
    text:
        String to normalize.

    Returns
    -------
    str
        Normalized string suitable for fuzzy matching.
    """

    text = text.lower()
    text = _punct_re.sub(" ", text)
    text = expand_abbreviations(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

__all__ = ["normalize_text", "expand_abbreviations", "ABBREVIATIONS"]
