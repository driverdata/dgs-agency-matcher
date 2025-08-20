"""High level matching pipeline.

This module glues together the building blocks from the package to offer a
single function :func:`run_pipeline` which operates on a pandas
:class:`~pandas.DataFrame` of agency names and returns the matched results.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

from .aliasing import apply_alias
from .heuristics import heuristic_score
from .matching import match_agency
from .normalize import normalize_text


def run_pipeline(df: pd.DataFrame, candidates: Iterable[str], *, output_excel: Optional[Path] = None) -> pd.DataFrame:
    """Run the full matching pipeline on *df*.

    Parameters
    ----------
    df:
        Input DataFrame expected to contain an ``"agency"`` column.
    candidates:
        Iterable of canonical agency names to match against.
    output_excel:
        Optional path; if provided the resulting DataFrame is also written
        to this Excel file using :mod:`xlsxwriter`.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the original agency name, normalized form,
        match and score.
    """

    processed = []
    for original in df["agency"].drop_duplicates():
        normalized = normalize_text(original)
        aliased = apply_alias(normalized)
        match, base_score = match_agency(aliased, candidates, anchors=aliased.split())
        score = base_score + heuristic_score(match, aliased, anchors=aliased.split())
        processed.append({
            "original": original,
            "normalized": aliased,
            "match": match,
            "score": score,
        })

    result = pd.DataFrame(processed)
    if output_excel:
        output_excel = Path(output_excel)
        result.to_excel(output_excel, index=False)
    return result

__all__ = ["run_pipeline", "main"]


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for the pipeline.

    The command expects an input CSV file with an ``agency`` column and a
    plain text file containing candidate agencies (one per line). The
    results are written to ``output.xlsx`` unless another path is provided
    via ``--output``.
    """

    import argparse

    parser = argparse.ArgumentParser(description="Run DGS agency matching pipeline")
    parser.add_argument("input_csv", help="CSV file with an 'agency' column")
    parser.add_argument("candidates_txt", help="Text file of candidate agencies")
    parser.add_argument("--output", default="output.xlsx", help="Excel file to write results to")
    args = parser.parse_args(argv)

    df = pd.read_csv(args.input_csv)
    with open(args.candidates_txt) as fh:
        candidates = [line.strip() for line in fh if line.strip()]
    run_pipeline(df, candidates, output_excel=args.output)


if __name__ == "__main__":  # pragma: no cover - CLI invocation
    main()
