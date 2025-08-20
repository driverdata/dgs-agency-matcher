"""Matching utilities for agency names.

The main entry point is :func:`match_agency` which performs TF‑IDF based
cosine similarity matching with optional anchor filtering. If the TF‑IDF
step cannot produce a result, a RapidFuzz ratio match is used instead.
"""

from __future__ import annotations

from typing import Iterable, List, Tuple

from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def match_agency(query: str, candidates: Iterable[str], anchors: Iterable[str] | None = None) -> Tuple[str, float]:
    """Match *query* against *candidates*.

    Parameters
    ----------
    query:
        Normalized agency name to match.
    candidates:
        Iterable of candidate agency names.
    anchors:
        Optional iterable of substrings that must appear in a candidate
        for it to be considered. The filter is applied before TF‑IDF.

    Returns
    -------
    tuple
        A pair of ``(best_match, score)`` where *score* is a cosine
        similarity in the range ``[0, 1]``. When RapidFuzz fallback is
        used the score represents a ratio in ``[0, 1]``.
    """

    candidate_list: List[str] = list(candidates)
    anchor_list = list(anchors or [])

    filtered = (
        [c for c in candidate_list if any(a in c for a in anchor_list)]
        if anchor_list
        else candidate_list
    )
    if not filtered:
        filtered = candidate_list

    if filtered:
        vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(3, 5))
        tfidf = vectorizer.fit_transform(filtered + [query])
        cosine_sim = linear_kernel(tfidf[-1], tfidf[:-1]).flatten()
        if cosine_sim.size:
            best_index = int(cosine_sim.argmax())
            return filtered[best_index], float(cosine_sim[best_index])

    # RapidFuzz fallback
    best = max((fuzz.ratio(query, c) / 100.0, c) for c in candidate_list)
    return best[1], float(best[0])

__all__ = ["match_agency"]
