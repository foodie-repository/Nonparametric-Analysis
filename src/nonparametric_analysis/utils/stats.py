"""Common utilities for nonparametric analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def interpret_p_value(p_value: float, alpha: float = 0.05) -> str:
    """Return a human-readable interpretation of the p-value."""
    if p_value < 0.001:
        return f"p = {p_value:.4f} → 매우 강한 유의성 (p < 0.001)"
    elif p_value < alpha:
        return f"p = {p_value:.4f} → 유의함 (p < {alpha})"
    else:
        return f"p = {p_value:.4f} → 유의하지 않음 (p ≥ {alpha})"


def effect_size_r(z_stat: float, n: int) -> tuple[float, str]:
    """Calculate effect size r = |Z|/sqrt(N) and its label."""
    if n <= 0:
        return 0.0, "N/A"
    r = abs(z_stat) / np.sqrt(n)
    if r >= 0.5:
        label = "큰"
    elif r >= 0.3:
        label = "중간"
    elif r >= 0.1:
        label = "작은"
    else:
        label = "미미함"
    return r, label


def robust_descriptive(
    data: np.ndarray | pd.Series | list[float], name: str = "Feature"
) -> pd.DataFrame:
    """Return robust descriptive statistics (Median, IQR, MAD)."""
    clean_data = np.asarray(data)
    clean_data = clean_data[~np.isnan(clean_data)]

    if len(clean_data) == 0:
        return pd.DataFrame()

    q1, med, q3 = np.percentile(clean_data, [25, 50, 75])
    iqr = q3 - q1
    mad = np.median(np.abs(clean_data - med))

    return pd.DataFrame(
        {
            "지표": [
                "N",
                "중앙값",
                "Q1",
                "Q3",
                "IQR",
                "최솟값",
                "최댓값",
                "MAD",
                "왜도",
                "첨도",
            ],
            name: [
                len(clean_data),
                f"{med:.3f}",
                f"{q1:.3f}",
                f"{q3:.3f}",
                f"{iqr:.3f}",
                f"{np.min(clean_data):.3f}",
                f"{np.max(clean_data):.3f}",
                f"{mad:.3f}",
                f"{stats.skew(clean_data):.3f}",
                f"{stats.kurtosis(clean_data):.3f}",
            ],
        }
    )


def as_float_array(values: np.ndarray | pd.Series | list[float]) -> np.ndarray:
    """Convert input to 1D float array, raising error if not 1D."""
    array = np.asarray(values, dtype=float)
    if array.ndim != 1:
        raise ValueError("Input must be one-dimensional.")
    return array


def benjamini_hochberg(p_values: np.ndarray | pd.Series | list[float]) -> np.ndarray:
    """Benjamini-Hochberg FDR-adjusted p-values."""
    p_array = np.asarray(p_values, dtype=float)
    adjusted = np.full_like(p_array, np.nan, dtype=float)
    finite_mask = np.isfinite(p_array)
    p_finite = p_array[finite_mask]
    n_tests = len(p_finite)
    if n_tests == 0:
        return adjusted

    # Rank: 1 to N
    ranks = stats.rankdata(p_finite)
    # Sort p-values
    sorted_idx = np.argsort(p_finite)
    sorted_p = p_finite[sorted_idx]

    # Correction: P * N / rank
    # Note: stats.rankdata returns ranks 1..N (ties average). BH uses strict rank 1..N.
    # Using strict rank (method='ordinal') for sorting
    strict_ranks = np.arange(1, n_tests + 1)

    sorted_adj = sorted_p * n_tests / strict_ranks
    # Cumulative minimum from right
    sorted_adj = np.minimum.accumulate(sorted_adj[::-1])[::-1]
    sorted_adj = np.clip(sorted_adj, 0.0, 1.0)

    unsorted_adj = np.empty_like(sorted_adj)
    unsorted_adj[sorted_idx] = sorted_adj
    adjusted[finite_mask] = unsorted_adj
    return adjusted


def adjust_pvalue_matrix_fdr(pval_matrix: pd.DataFrame) -> pd.DataFrame:
    """Apply BH-FDR correction to square p-value matrix (symmetric)."""
    if pval_matrix.shape[0] != pval_matrix.shape[1]:
        raise ValueError("pval_matrix must be square.")

    p_array = pval_matrix.to_numpy(dtype=float)
    # Extract upper triangle (k=1 excludes diagonal)
    tri_i, tri_j = np.triu_indices_from(p_array, k=1)
    tri_p = p_array[tri_i, tri_j]

    # Adjust
    tri_adj = benjamini_hochberg(tri_p)

    # Reconstruct
    adj = np.zeros_like(p_array, dtype=float)
    adj[tri_i, tri_j] = tri_adj
    adj[tri_j, tri_i] = tri_adj
    np.fill_diagonal(
        adj, 0.0
    )  # Diagonal p-value is 0 or 1? Typically correlation with self is 1, p=0.

    return pd.DataFrame(adj, index=pval_matrix.index, columns=pval_matrix.columns)
