"""Top-level package for dgs_matcher.

This package provides tools to normalize, alias, and match agency names
for the California Department of General Services. It also exposes a
Streamlit UI for manual exploration.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("dgs-agency-matcher")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

__all__ = ["__version__"]
