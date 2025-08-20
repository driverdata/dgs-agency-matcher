"""Streamlit entry point for the DGS agency matcher."""

from dgs_matcher.ui import render

if __name__ == "__main__":  # pragma: no cover - Streamlit handles running
    render()
