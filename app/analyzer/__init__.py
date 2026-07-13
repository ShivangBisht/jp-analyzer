"""Stable production-facing analyzer package.

Phase 10.1 is a behavior-preserving facade over the validated
Phase 9 Alpha 2.2 implementation.
"""

from .pipeline import analyze, analyze_full
from .version import ANALYZER_VERSION, SCHEMA_VERSION

__all__ = ["ANALYZER_VERSION", "SCHEMA_VERSION", "analyze", "analyze_full"]
