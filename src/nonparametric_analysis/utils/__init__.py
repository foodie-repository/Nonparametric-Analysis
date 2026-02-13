"""Utility functions for nonparametric analysis."""

from .stats import (
    interpret_p_value,
    effect_size_r,
    robust_descriptive,
    benjamini_hochberg,
    adjust_pvalue_matrix_fdr,
    as_float_array,
)
from .integrity import (
    missing_rate_report,
    duplicate_rows,
    range_violation_mask,
    mad_outlier_mask,
    formula_violation_mask,
)
from .sample import generate_sample_dataset

__all__ = [
    # stats
    "interpret_p_value",
    "effect_size_r",
    "robust_descriptive",
    "benjamini_hochberg",
    "adjust_pvalue_matrix_fdr",
    "as_float_array",
    # integrity
    "missing_rate_report",
    "duplicate_rows",
    "range_violation_mask",
    "mad_outlier_mask",
    "formula_violation_mask",
    # sample
    "generate_sample_dataset",
]
