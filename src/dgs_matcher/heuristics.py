"""Heuristic scoring helpers.

The functions here implement human-like heuristics used to adjust raw
string similarity scores. They are intentionally lightweight and easy to
extend in user projects.
"""

from __future__ import annotations

from typing import Iterable

FALSE_FRIENDS = {"bank", "university"}


def heuristic_score(candidate: str, query: str, anchors: Iterable[str] | None = None) -> float:
    """Compute a heuristic score for *candidate*.

    The score is meant to be added to a base similarity measure. It
    rewards anchor coverage and state government keywords while penalising
    known "false friend" terms.

    Parameters
    ----------
    candidate:
        Candidate agency name.
    query:
        Original query string; currently unused but reserved for future
        rules.
    anchors:
        Optional iterable of anchor terms derived from the query.

    Returns
    -------
    float
        Heuristic bonus score, positive or negative.
    """

    score = 0.0
    anchor_list = list(anchors or [])
    if anchor_list:
        score += sum(1 for a in anchor_list if a in candidate) / max(len(anchor_list), 1)
    if any(word in candidate for word in ("state", "government")):
        score += 0.1
    if ".gov" in candidate:
        score += 0.1
    if any(ff in candidate for ff in FALSE_FRIENDS):
        score -= 0.1
    return score

__all__ = ["heuristic_score", "FALSE_FRIENDS"]
