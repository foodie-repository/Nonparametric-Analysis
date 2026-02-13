"""Correlation analysis nonparametric methods."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import seaborn as sns

from ..utils.stats import as_float_array


# --- 6. Correlation Analysis ---


def spearman_correlation(x, y, x_name="X", y_name="Y", save_path: str = None) -> dict:
    """Spearman correlation with rank plot."""
    x = as_float_array(x)
    y = as_float_array(y)
    valid = ~np.isnan(x) & ~np.isnan(y)
    x, y = x[valid], y[valid]

    rho, p_value = stats.spearmanr(x, y)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].scatter(x, y, alpha=0.6, edgecolors="white", s=60, c="steelblue")
    axes[0].set_xlabel(x_name)
    axes[0].set_ylabel(y_name)
    axes[0].set_title(f"Spearman rho={rho:.3f}, p={p_value:.4f}")

    rx, ry = stats.rankdata(x), stats.rankdata(y)
    axes[1].scatter(rx, ry, alpha=0.6, color="coral", s=60, edgecolors="white")
    if len(rx) > 1:
        z = np.polyfit(rx, ry, 1)
        axes[1].plot(np.sort(rx), np.poly1d(z)(np.sort(rx)), "r--", lw=1.5)
    axes[1].set_xlabel(f"{x_name} (Rank)")
    axes[1].set_ylabel(f"{y_name} (Rank)")
    axes[1].set_title("Rank Transformation")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {"rho": rho, "p_value": p_value, "figure": fig}


def correlation_matrix_nonparametric(
    df: pd.DataFrame, method: str = "spearman", save_path: str = None
) -> dict:
    """Correlation matrix and p-value matrix."""
    cols = df.select_dtypes(include=[np.number]).columns
    df_num = df[cols]

    corr = df_num.corr(method=method)
    p_mat = pd.DataFrame(np.zeros((len(cols), len(cols))), columns=cols, index=cols)

    func = stats.spearmanr if method == "spearman" else stats.kendalltau

    for i, c1 in enumerate(cols):
        for j, c2 in enumerate(cols):
            if i != j:
                # dropna for pair
                valid = df_num[[c1, c2]].dropna()
                if len(valid) > 2:
                    _, p = func(valid[c1], valid[c2])
                    p_mat.iloc[i, j] = p
                else:
                    p_mat.iloc[i, j] = np.nan
            else:
                p_mat.iloc[i, j] = 0.0  # self p-value

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        ax=axes[0],
        square=True,
    )
    axes[0].set_title(f"{method.capitalize()} Correlation")

    sns.heatmap(
        p_mat,
        mask=mask,
        annot=True,
        fmt=".3f",
        cmap="RdYlGn_r",
        center=0.05,
        ax=axes[1],
        square=True,
    )
    axes[1].set_title("p-value (Green < 0.05)")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {"correlation": corr, "p_values": p_mat, "figure": fig}


def kendall_corr(x, y, x_name="X", y_name="Y", save_path: str = None) -> dict:
    """Kendall's Tau correlation."""
    x = as_float_array(x)
    y = as_float_array(y)
    valid = ~np.isnan(x) & ~np.isnan(y)
    x, y = x[valid], y[valid]

    tau, p_value = stats.kendalltau(x, y)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(x, y, alpha=0.6, edgecolors="white", s=60, c="teal")
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.set_title(f"Kendall Tau={tau:.3f}, p={p_value:.4f}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {"correlation": tau, "p_value": p_value, "figure": fig}


def distance_correlation(x, y, n_perm: int = 2000, save_path: str = None) -> dict:
    """Distance Correlation with permutation test."""
    x = as_float_array(x)
    y = as_float_array(y)
    valid = ~np.isnan(x) & ~np.isnan(y)
    x, y = x[valid], y[valid]

    def dcov(a, b):
        A = squareform(pdist(a.reshape(-1, 1)))
        A = A - A.mean(0) - A.mean(1, keepdims=True) + A.mean()
        B = squareform(pdist(b.reshape(-1, 1)))
        B = B - B.mean(0) - B.mean(1, keepdims=True) + B.mean()
        return np.sqrt(np.mean(A * B))

    dcov_xy = dcov(x, y)
    dcov_xx = dcov(x, x)
    dcov_yy = dcov(y, y)
    dcor = dcov_xy / np.sqrt(dcov_xx * dcov_yy) if dcov_xx * dcov_yy > 0 else 0

    # Permutation Test
    perm_dcors = np.zeros(n_perm)
    y_shuffled = y.copy()
    for i in range(n_perm):
        np.random.shuffle(y_shuffled)
        # Recalculating dcov_xy only, denominator is constant (dcov_yy same)
        perm_dcors[i] = (
            dcov(x, y_shuffled) / np.sqrt(dcov_xx * dcov_yy)
            if dcov_xx * dcov_yy > 0
            else 0
        )

    p_value = np.mean(perm_dcors >= dcor)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(x, y, alpha=0.6, s=60)
    axes[0].set_title(f"dCor={dcor:.3f}, p={p_value:.4f}")

    axes[1].hist(perm_dcors, bins=30, alpha=0.7, color="lightgreen", edgecolor="white")
    axes[1].axvline(dcor, color="red", lw=2, label=f"Observed={dcor:.3f}")
    axes[1].set_title("Permutation Distribution")
    axes[1].legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {"dcor": dcor, "p_value": p_value, "figure": fig}
