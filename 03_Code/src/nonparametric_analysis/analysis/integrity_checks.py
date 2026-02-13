"""Backward compatibility alias for integrity checks module."""

from ..utils.integrity import (
    missing_rate_report,
    duplicate_rows,
    range_violation_mask,
    mad_outlier_mask,
    formula_violation_mask,
)

__all__ = [
    "missing_rate_report",
    "duplicate_rows",
    "range_violation_mask",
    "mad_outlier_mask",
    "formula_violation_mask",
]
