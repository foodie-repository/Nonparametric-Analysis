"""Nonparametric analysis package initialization."""

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

from .integrity_checks import (
    missing_rate_report,
    duplicate_rows,
    range_violation_mask,
    mad_outlier_mask,
    formula_violation_mask,
)

from .sample_data import generate_sample_dataset

from .utils import (
    interpret_p_value,
    effect_size_r,
    robust_descriptive,
    benjamini_hochberg,
    adjust_pvalue_matrix_fdr,
)

from .visualizations import setup_visualization
