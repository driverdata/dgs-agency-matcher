"""Setup script for dgs-agency-matcher."""

from pathlib import Path
from setuptools import find_packages, setup

README = (Path(__file__).parent / "README.md").read_text()

setup(
    name="dgs-agency-matcher",
    version="0.1.0",
    description="Match DGS agency names using TF-IDF and heuristic scoring",
    long_description=README,
    long_description_content_type="text/markdown",
    author="",  # intentionally left blank
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pandas",
        "scikit-learn",
        "rapidfuzz",
        "xlsxwriter",
        "streamlit",
    ],
    python_requires=">=3.9",
)
