"""Nonparametric Analysis - FastAPI + React 웹 서비스"""

__version__ = "0.1.0"

# Import core analysis functions
from .core import (
    # single_variable
    test_normality,
    runs_test_analysis,
    mann_kendall_test,
    pettitt_test,
    detect_changepoints_pelt,
    # group_comparison
    mann_whitney_test,
    ks_test,
    wilcoxon_paired_test,
    sign_test,
    wilcoxon_one_sample,
    kruskal_wallis_test,
    friedman_test,
    # correlation
    spearman_correlation,
    correlation_matrix_nonparametric,
    kendall_corr,
    distance_correlation,
    # resampling
    bootstrap_ci,
    permutation_test,
)

# Import utility functions
from .utils import (
    # stats
    interpret_p_value,
    effect_size_r,
    robust_descriptive,
    benjamini_hochberg,
    adjust_pvalue_matrix_fdr,
    as_float_array,
    # integrity
    missing_rate_report,
    duplicate_rows,
    range_violation_mask,
    mad_outlier_mask,
    formula_violation_mask,
    # sample
    generate_sample_dataset,
)

# Import visualization
from .visualization import setup_visualization

__all__ = [
    # Core analysis
    "test_normality",
    "runs_test_analysis",
    "mann_kendall_test",
    "pettitt_test",
    "detect_changepoints_pelt",
    "mann_whitney_test",
    "ks_test",
    "wilcoxon_paired_test",
    "sign_test",
    "wilcoxon_one_sample",
    "kruskal_wallis_test",
    "friedman_test",
    "spearman_correlation",
    "correlation_matrix_nonparametric",
    "kendall_corr",
    "distance_correlation",
    "bootstrap_ci",
    "permutation_test",
    # Utilities
    "interpret_p_value",
    "effect_size_r",
    "robust_descriptive",
    "benjamini_hochberg",
    "adjust_pvalue_matrix_fdr",
    "as_float_array",
    "missing_rate_report",
    "duplicate_rows",
    "range_violation_mask",
    "mad_outlier_mask",
    "formula_violation_mask",
    "generate_sample_dataset",
    # Visualization
    "setup_visualization",
]
