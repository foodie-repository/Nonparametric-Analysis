"""
Nonparametric analysis package (backward compatibility).

This module provides backward compatibility by re-exporting from the refactored structure.
Prefer importing directly from `nonparametric_analysis.core`, `nonparametric_analysis.utils`, etc.
"""

from .nonparametric_methods import (
    test_normality,
    sign_test,
    wilcoxon_one_sample,
    mann_kendall_test,
    pettitt_test,
    detect_changepoints_pelt,
    mann_whitney_test,
    wilcoxon_paired_test,
    ks_test,
    kruskal_wallis_test,
    friedman_test,
    spearman_correlation,
    kendall_corr,
    correlation_matrix_nonparametric,
    distance_correlation,
    bootstrap_ci,
    permutation_test,
    runs_test_analysis,
)

from ..utils.integrity import (
    missing_rate_report,
    duplicate_rows,
    range_violation_mask,
    mad_outlier_mask,
    formula_violation_mask,
)

from ..utils.sample import generate_sample_dataset

from ..utils.stats import (
    interpret_p_value,
    effect_size_r,
    robust_descriptive,
    benjamini_hochberg,
    adjust_pvalue_matrix_fdr,
)

from ..visualization.setup import setup_visualization

__all__ = [
    # Analysis methods
    "test_normality",
    "sign_test",
    "wilcoxon_one_sample",
    "mann_kendall_test",
    "pettitt_test",
    "detect_changepoints_pelt",
    "mann_whitney_test",
    "wilcoxon_paired_test",
    "ks_test",
    "kruskal_wallis_test",
    "friedman_test",
    "spearman_correlation",
    "kendall_corr",
    "correlation_matrix_nonparametric",
    "distance_correlation",
    "bootstrap_ci",
    "permutation_test",
    "runs_test_analysis",
    # Integrity checks
    "missing_rate_report",
    "duplicate_rows",
    "range_violation_mask",
    "mad_outlier_mask",
    "formula_violation_mask",
    # Sample data
    "generate_sample_dataset",
    # Utils
    "interpret_p_value",
    "effect_size_r",
    "robust_descriptive",
    "benjamini_hochberg",
    "adjust_pvalue_matrix_fdr",
    # Visualization
    "setup_visualization",
]
