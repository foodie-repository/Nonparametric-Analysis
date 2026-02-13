"""
Backward compatibility module.

This module re-exports functions from the refactored structure.
All analysis functions are now organized in the `core` package.
"""

# Re-export all functions from the new structure
from ..core.single_variable import (
    test_normality,
    runs_test_analysis,
    mann_kendall_test,
    pettitt_test,
    detect_changepoints_pelt,
)

from ..core.group_comparison import (
    mann_whitney_test,
    ks_test,
    wilcoxon_paired_test,
    sign_test,
    wilcoxon_one_sample,
    kruskal_wallis_test,
    friedman_test,
)

from ..core.correlation import (
    spearman_correlation,
    correlation_matrix_nonparametric,
    kendall_corr,
    distance_correlation,
)

from ..core.resampling import (
    bootstrap_ci,
    permutation_test,
)

__all__ = [
    # single_variable
    "test_normality",
    "runs_test_analysis",
    "mann_kendall_test",
    "pettitt_test",
    "detect_changepoints_pelt",
    # group_comparison
    "mann_whitney_test",
    "ks_test",
    "wilcoxon_paired_test",
    "sign_test",
    "wilcoxon_one_sample",
    "kruskal_wallis_test",
    "friedman_test",
    # correlation
    "spearman_correlation",
    "correlation_matrix_nonparametric",
    "kendall_corr",
    "distance_correlation",
    # resampling
    "bootstrap_ci",
    "permutation_test",
]
