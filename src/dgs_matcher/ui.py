"""Streamlit user interface for the matcher.

The :func:`render` function is imported by :mod:`app` and sets up a small
interactive interface around :func:`dgs_matcher.pipeline.run_pipeline`.
"""

from __future__ import annotations

from io import BytesIO
from typing import List

import pandas as pd
import streamlit as st

from .pipeline import run_pipeline


def render() -> None:
    """Render the Streamlit interface."""

    st.title("DGS Agency Matcher")
    uploaded = st.file_uploader("Upload CSV of agencies", type="csv")
    candidates_text = st.text_area("Candidate agencies (one per line)")

    if uploaded and candidates_text:
        df = pd.read_csv(uploaded)
        candidates: List[str] = [c.strip() for c in candidates_text.splitlines() if c.strip()]
        result = run_pipeline(df, candidates)
        st.dataframe(result)
        buf = BytesIO()
        result.to_excel(buf, index=False)
        st.download_button(
            "Download results",
            data=buf.getvalue(),
            file_name="results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

__all__ = ["render"]
