# dgs-agency-matcher

A reusable Python package and Streamlit application for matching messy
Department of General Services (DGS) agency names to a canonical list.
The library combines light-weight text normalisation, alias expansion,
TF‑IDF / RapidFuzz matching and human-style heuristics.

## Installation

```bash
pip install .
```

## Command line usage

The pipeline can be executed directly as a module. It expects an input CSV
with an `agency` column and a text file containing candidate agency names.

```bash
python -m dgs_matcher.pipeline agencies.csv candidates.txt --output results.xlsx
```

## Streamlit application

Run the interactive web app with:

```bash
streamlit run app.py
```

The UI lets you upload a CSV and paste candidate agencies, then download
an Excel workbook with the matches.

## Testing

Run the unit tests with:

```bash
pytest
```

## License

This project is licensed under the terms of the MIT license.
