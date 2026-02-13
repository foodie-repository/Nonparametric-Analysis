"""Single variable nonparametric analysis methods."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import pymannkendall as mk
import ruptures as rpt

from ..utils.stats import as_float_array


# --- 3. Single Feature Analysis ---


def test_normality(
    data: pd.Series | list[float],
    name: str = "Feature",
    alpha: float = 0.05,
    save_path: str = None,
) -> dict:
    """Shapiro-Wilk normality test with 3-panel plot."""
    clean_data = as_float_array(data)
    clean_data = clean_data[~np.isnan(clean_data)]

    stat, p_value = stats.shapiro(clean_data)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Histogram + KDE + Normal
    axes[0].hist(
        clean_data,
        bins="auto",
        density=True,
        alpha=0.7,
        color="steelblue",
        edgecolor="white",
    )
    if len(clean_data) > 1:
        kde = stats.gaussian_kde(clean_data)
        x = np.linspace(min(clean_data), max(clean_data), 100)
        axes[0].plot(x, kde(x), "r-", lw=2, label="KDE")
        axes[0].plot(
            x,
            stats.norm.pdf(x, np.mean(clean_data), np.std(clean_data)),
            "g--",
            lw=1.5,
            label="Normal",
        )
    axes[0].set_title(f"{name} Distribution")
    axes[0].legend()

    # Q-Q Plot
    stats.probplot(clean_data, plot=axes[1])
    axes[1].set_title("Q-Q Plot")

    # Box Plot
    axes[2].boxplot(
        clean_data, vert=True, patch_artist=True, boxprops=dict(facecolor="lightyellow")
    )
    axes[2].set_title("Box Plot")

    plt.suptitle(f"Shapiro-Wilk: W={stat:.4f}, p={p_value:.4f}", y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "statistic": stat,
        "p_value": p_value,
        "is_normal": p_value >= alpha,
        "figure": fig,
    }


def runs_test_analysis(
    data: pd.Series | list[float], name: str = "Series", save_path: str = None
) -> dict:
    """Runs test for randomness."""
    clean_data = as_float_array(data)
    clean_data = clean_data[~np.isnan(clean_data)]

    median = np.median(clean_data)
    binary = (clean_data >= median).astype(int)

    runs = 1
    for i in range(1, len(binary)):
        if binary[i] != binary[i - 1]:
            runs += 1

    n1 = np.sum(binary == 1)
    n0 = np.sum(binary == 0)
    n = n1 + n0

    expected = (2 * n1 * n0 / n) + 1
    if n > 0 and (n - 1) > 0:
        std = np.sqrt(2 * n1 * n0 * (2 * n1 * n0 - n) / (n**2 * (n - 1)))
    else:
        std = 0

    z = (runs - expected) / std if std > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    axes[0].plot(clean_data, "b-o", ms=4)
    axes[0].axhline(median, color="red", ls="--", label=f"Median={median:.2f}")
    axes[0].fill_between(
        range(len(clean_data)),
        median,
        clean_data,
        where=clean_data >= median,
        alpha=0.3,
        color="green",
    )
    axes[0].fill_between(
        range(len(clean_data)),
        median,
        clean_data,
        where=clean_data < median,
        alpha=0.3,
        color="red",
    )
    axes[0].set_title(f"{name}: Runs Test")
    axes[0].legend()

    axes[1].step(range(len(binary)), binary, "k-", where="mid")
    axes[1].set_yticks([0, 1])
    axes[1].set_yticklabels(["Below", "Above"])
    axes[1].set_title(f"Runs={runs}, Exp={expected:.1f}, Z={z:.2f}, p={p_value:.4f}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "runs": runs,
        "expected": expected,
        "z": z,
        "p_value": p_value,
        "figure": fig,
    }


def mann_kendall_test(
    data: pd.Series | list[float], name: str = "Feature", save_path: str = None
) -> dict:
    """Mann-Kendall trend test with Sen's slope."""
    clean_data = as_float_array(data)
    clean_data = clean_data[~np.isnan(clean_data)]

    result = mk.original_test(clean_data)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(clean_data, "b-o", markersize=4, alpha=0.7)
    x_line = np.arange(len(clean_data))
    ax.plot(
        x_line,
        result.intercept + result.slope * x_line,
        "r-",
        lw=2,
        label=f"Sen's slope={result.slope:.3f}",
    )
    ax.set_title(
        f"{name}: Mann-Kendall (tau={result.Tau:.3f}, p={result.p:.4f}, {result.trend})"
    )
    ax.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "tau": result.Tau,
        "p_value": result.p,
        "slope": result.slope,
        "trend": result.trend,
        "figure": fig,
    }


def pettitt_test(
    data: pd.Series | list[float], name: str = "Feature", save_path: str = None
) -> dict:
    """Pettitt change-point test (Optimized O(N log N))."""
    clean_data = as_float_array(data)
    clean_data = clean_data[~np.isnan(clean_data)]
    n = len(clean_data)

    if n < 2:
        return {"change_point": None, "p_value": 1.0, "statistic": 0.0}

    # Optimized implementation
    ranks = stats.rankdata(clean_data)
    cum_ranks = np.cumsum(ranks)
    t_indices = np.arange(n)
    U = 2 * cum_ranks - (t_indices + 1) * (n + 1)

    # Standard Pettitt considers split after t for t=0..n-2?
    # Max |U_t| usually taken over 0..n-2
    # Spec implementation covered t=0..n-1

    K = np.max(
        np.abs(U[:-1])
    )  # Exclude last point where U should be 0 (sum of ranks - sum of ranks?)
    # U[n-1] = 2*sum(1..n) - n(n+1) = n(n+1) - n(n+1) = 0. Correct.

    cp = np.argmax(np.abs(U[:-1]))
    # If cp=0, split is after index 0. (0 vs 1..n-1)

    p_value = 2 * np.exp(-6 * K**2 / (n**3 + n**2))

    # Split: data[:cp+1] vs data[cp+1:]
    # Guide code used [:cp] vs [cp:], implying cp is start of second segment.
    # If using guide indexing, cp index matches python slice start?
    # K is at index t. Split is AFTER t.
    # So first segment ends at t (inclusive). Python slice [:t+1].
    # Second segment starts at t+1. Python slice [t+1:].
    # Guide used [:cp] and [cp:]. This implies Guide's 'cp' was t+1.
    # I will stick to returning the index where the shift happens (start of new segment).

    shift_index = cp + 1
    med_before = np.median(clean_data[:shift_index])
    med_after = np.median(clean_data[shift_index:])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(clean_data, "b-o", markersize=4, alpha=0.7)
    ax.axvline(
        shift_index,
        color="red",
        ls="--",
        lw=2,
        label=f"Change Point (idx={shift_index})",
    )
    ax.hlines(
        med_before,
        0,
        shift_index,
        colors="green",
        lw=2,
        label=f"Pre Mdn={med_before:.2f}",
    )
    ax.hlines(
        med_after,
        shift_index,
        n,
        colors="orange",
        lw=2,
        label=f"Post Mdn={med_after:.2f}",
    )
    ax.set_title(f"{name}: Pettitt (K={K:.0f}, p={p_value:.4f})")
    ax.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "change_point": int(shift_index),
        "statistic": float(K),
        "p_value": float(p_value),
        "median_before": float(med_before),
        "median_after": float(med_after),
        "figure": fig,
    }


def detect_changepoints_pelt(
    data: pd.Series | list[float],
    model: str = "rbf",
    penalty: float = None,
    name: str = "Feature",
    save_path: str = None,
) -> dict:
    """PELT multiple change-point detection."""
    clean_data = as_float_array(data)
    clean_data = clean_data[~np.isnan(clean_data)]

    signal = clean_data.reshape(-1, 1)
    if penalty is None:
        penalty = (
            np.log(len(clean_data)) * np.var(clean_data)
            if np.var(clean_data) > 0
            else 1.0
        )

    result = rpt.Pelt(model=model, min_size=2).fit(signal).predict(pen=penalty)
    # result includes end index (len(data))

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    axes[0].plot(clean_data, "b-", lw=1.5, alpha=0.8)
    prev = 0
    segs, labels = [], []

    for i, cp in enumerate(result):
        # cp is end index of segment (exclusive in python slice?)
        # ruptures returns end indices.
        seg = clean_data[prev:cp]
        if len(seg) > 0:
            axes[0].hlines(np.median(seg), prev, cp, colors="red", lw=2.5)
            segs.append(seg)
            labels.append(f"Seg {i+1}")

        if cp < len(clean_data):
            axes[0].axvline(cp, color="red", ls="--", alpha=0.7)
        prev = cp

    axes[0].set_title(f"{name}: PELT ({len(result)-1} changes)")
    if segs:
        axes[1].boxplot(segs, labels=labels, patch_artist=True)
    axes[1].set_title("Segment Distribution")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "changepoints": [int(cp) for cp in result[:-1]],
        "n_segments": len(result),
        "figure": fig,
    }
