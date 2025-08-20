"""Tests for core matcher functionality."""

from dgs_matcher.aliasing import apply_alias
from dgs_matcher.matching import match_agency
from dgs_matcher.normalize import normalize_text


def test_normalize_text() -> None:
    """Lowercasing, punctuation removal and abbreviation expansion."""

    assert normalize_text("Dept. of CA!") == "department of california"


def test_apply_alias() -> None:
    """Alias expansion returns the canonical form."""

    assert apply_alias("cal fire") == "california department of forestry and fire protection"


def test_match_agency() -> None:
    """TF‑IDF matching should prefer the exact candidate."""

    candidates = [
        "department of motor vehicles",
        "california department of forestry and fire protection",
    ]
    match, score = match_agency("department of motor vehicles", candidates)
    assert match == "department of motor vehicles"
    assert score > 0.5
