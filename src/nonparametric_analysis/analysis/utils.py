"""Backward compatibility alias for utils module."""

from ..utils.stats import (
    interpret_p_value,
    effect_size_r,
    robust_descriptive,
    benjamini_hochberg,
    adjust_pvalue_matrix_fdr,
    as_float_array,
)

__all__ = [
    "interpret_p_value",
    "effect_size_r",
    "robust_descriptive",
    "benjamini_hochberg",
    "adjust_pvalue_matrix_fdr",
    "as_float_array",
]
