"""Core nonparametric methods with integrated visualization."""

from __future__ import annotations

import platform
import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import seaborn as sns
import pymannkendall as mk
import scikit_posthocs as sp
import ruptures as rpt

from .utils import effect_size_r, as_float_array, interpret_p_value

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


def sign_test(
    data: pd.Series | list[float],
    hypothesized_median: float = 0.0,
    name: str = "Feature",
    save_path: str = None,
) -> dict:
    """Sign test for median."""
    clean_data = as_float_array(data)
    clean_data = clean_data[~np.isnan(clean_data)]

    diff = clean_data - hypothesized_median
    diff = diff[diff != 0]
    n_pos, n_neg = np.sum(diff > 0), np.sum(diff < 0)
    n = n_pos + n_neg
    # Binomial test p-value (two-sided)
    p_value = min(2 * stats.binom.cdf(min(n_pos, n_neg), n, 0.5), 1.0)

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["#e74c3c" if d < 0 else "#2ecc71" for d in diff]
    ax.bar(range(len(diff)), diff, color=colors, edgecolor="white")
    ax.axhline(0, color="black", lw=1)
    ax.set_title(f"{name}: Sign Test (+{n_pos}, -{n_neg}, p={p_value:.4f})")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {"n_pos": int(n_pos), "n_neg": int(n_neg), "p_value": p_value, "figure": fig}


def wilcoxon_one_sample(
    data: pd.Series | list[float],
    hypothesized_median: float = 0.0,
    name: str = "Feature",
    save_path: str = None,
) -> dict:
    """Wilcoxon signed-rank test (one sample)."""
    clean_data = as_float_array(data)
    clean_data = clean_data[~np.isnan(clean_data)]

    diff = clean_data - hypothesized_median
    stat, p_value = stats.wilcoxon(
        diff, alternative="two-sided"
    )  # zero_method='wilcox' default excludes zeros

    n = len(diff[diff != 0])
    # Approximate Z for effect size
    if n > 0:
        z = (stat - n * (n + 1) / 4) / np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
        r, _ = effect_size_r(z, n)
    else:
        z, r = 0.0, 0.0

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.boxplot(
        clean_data, vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue")
    )
    ax.axvline(
        hypothesized_median, color="red", ls="--", label=f"H0={hypothesized_median}"
    )
    ax.axvline(
        np.median(clean_data),
        color="green",
        ls="-",
        label=f"Median={np.median(clean_data):.2f}",
    )
    ax.legend()
    ax.set_title(f"{name}: Wilcoxon (T={stat:.1f}, p={p_value:.4f}, r={r:.3f})")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "statistic": stat,
        "z": z,
        "p_value": p_value,
        "effect_size_r": r,
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


# --- 4. Two Group Analysis ---


def mann_whitney_test(
    group1: pd.Series | list[float],
    group2,
    name1="G1",
    name2="G2",
    save_path: str = None,
) -> dict:
    """Mann-Whitney U test with effect sizes."""
    g1 = as_float_array(group1)
    g1 = g1[~np.isnan(g1)]
    g2 = as_float_array(group2)
    g2 = g2[~np.isnan(g2)]

    stat, p_value = stats.mannwhitneyu(g1, g2, alternative="two-sided")
    n1, n2 = len(g1), len(g2)
    n = n1 + n2

    mu_U = n1 * n2 / 2
    sigma_U = np.sqrt(n1 * n2 * (n + 1) / 12)
    z = (stat - mu_U) / sigma_U if sigma_U > 0 else 0
    r, _ = effect_size_r(z, n)
    cles = stat / (n1 * n2) if (n1 * n2) > 0 else 0
    cliffs_d = 2 * cles - 1

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Boxplot + Jitter
    bp = axes[0].boxplot([g1, g2], labels=[name1, name2], patch_artist=True, widths=0.5)
    colors = ["lightcoral", "lightskyblue"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)

    for i, (g, c) in enumerate([(g1, "darkred"), (g2, "darkblue")]):
        jitter = np.random.normal(0, 0.04, len(g))
        axes[0].scatter(np.full(len(g), i + 1) + jitter, g, alpha=0.5, s=20, color=c)
    axes[0].set_title(f"U={stat:.1f}, p={p_value:.4f}")

    # Rank Hist
    all_data = np.concatenate([g1, g2])
    ranks = stats.rankdata(all_data)
    axes[1].hist(ranks[:n1], bins="auto", alpha=0.6, label=name1, color="coral")
    axes[1].hist(ranks[n1:], bins="auto", alpha=0.6, label=name2, color="skyblue")
    axes[1].set_title("Rank Distribution")
    axes[1].legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "statistic": stat,
        "z": z,
        "p_value": p_value,
        "r": r,
        "cles": cles,
        "cliffs_delta": cliffs_d,
        "figure": fig,
    }


def wilcoxon_paired_test(
    before, after, name="Measurement", save_path: str = None
) -> dict:
    """Wilcoxon signed-rank test (paired)."""
    b = as_float_array(before)
    b = b[~np.isnan(b)]
    a = as_float_array(after)
    a = a[~np.isnan(a)]

    if len(b) != len(a):
        min_len = min(len(b), len(a))
        b = b[:min_len]
        a = a[:min_len]

    diff = a - b
    stat, p_value = stats.wilcoxon(b, a, alternative="two-sided")
    n = len(diff[diff != 0])

    z = (
        (stat - n * (n + 1) / 4) / np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
        if n > 0
        else 0
    )
    r, _ = effect_size_r(z, n)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Spaghetti Plot (Limit to 100 for readability)
    plot_idx = np.random.choice(len(b), min(len(b), 100), replace=False)
    for i in plot_idx:
        c = "#2ecc71" if a[i] > b[i] else "#e74c3c"
        axes[0].plot([0, 1], [b[i], a[i]], "o-", color=c, alpha=0.4)
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(["Before", "After"])
    axes[0].set_title(f"{name}: Change")

    # Diff Hist
    axes[1].hist(diff, bins="auto", color="salmon", edgecolor="white", alpha=0.8)
    axes[1].axvline(0, color="black", ls="--")
    axes[1].axvline(
        np.median(diff), color="red", lw=2, label=f"Mdn Diff={np.median(diff):.2f}"
    )
    axes[1].set_title(f"T={stat:.1f}, p={p_value:.4f}")
    axes[1].legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "statistic": stat,
        "z": z,
        "p_value": p_value,
        "r": r,
        "median_diff": np.median(diff),
        "figure": fig,
    }


def ks_test(group1, group2, name1="G1", name2="G2", save_path: str = None) -> dict:
    """Kolmogorov-Smirnov Test."""
    g1 = as_float_array(group1)
    g1 = g1[~np.isnan(g1)]
    g2 = as_float_array(group2)
    g2 = g2[~np.isnan(g2)]

    stat, p_value = stats.ks_2samp(g1, g2)

    fig, ax = plt.subplots(figsize=(10, 5))
    for d, n, c in [(g1, name1, "#3498db"), (g2, name2, "#e74c3c")]:
        s = np.sort(d)
        ecdf = np.arange(1, len(s) + 1) / len(s)
        ax.step(s, ecdf, where="post", label=n, color=c, lw=2)
    ax.set_title(f"ECDF — KS D={stat:.3f}, p={p_value:.4f}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {"statistic": stat, "p_value": p_value, "figure": fig}


# --- 5. Multi-Group Analysis ---


def kruskal_wallis_test(*groups, group_names=None, save_path: str = None) -> dict:
    """Kruskal-Wallis H Test with Dunn Posthoc."""
    if len(groups) == 1 and isinstance(groups[0], (list, tuple)):
        groups = groups[0]
    clean_groups = [as_float_array(g)[~np.isnan(as_float_array(g))] for g in groups]
    stat, p_value = stats.kruskal(*clean_groups)

    k = len(clean_groups)
    N = sum(len(g) for g in clean_groups)
    eta_sq = (stat - k + 1) / (N - k) if (N - k) > 0 else 0

    if group_names is None:
        group_names = [f"G{i+1}" for i in range(k)]

    fig, ax = plt.subplots(figsize=(10, 5))
    bp = ax.boxplot(clean_groups, labels=group_names, patch_artist=True)

    # Colors
    cmap = plt.cm.get_cmap("Set3")
    for i, (patch, g) in enumerate(zip(bp["boxes"], clean_groups)):
        patch.set_facecolor(cmap(i % 12))
        jitter = np.random.normal(0, 0.04, len(g))
        ax.scatter(np.full(len(g), i + 1) + jitter, g, alpha=0.4, s=15, color="black")

    ax.set_title(f"Kruskal-Wallis H={stat:.2f}, p={p_value:.4f}, eta_sq={eta_sq:.3f}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    result = {
        "statistic": stat,
        "p_value": p_value,
        "eta_squared": eta_sq,
        "figure": fig,
    }

    if p_value < 0.05:
        # Posthoc
        all_d = np.concatenate(clean_groups)
        all_l = np.concatenate(
            [[n] * len(g) for n, g in zip(group_names, clean_groups)]
        )
        df = pd.DataFrame({"value": all_d, "group": all_l})

        try:
            dunn = sp.posthoc_dunn(
                df, val_col="value", group_col="group", p_adjust="bonferroni"
            )
            # Save posthoc plot? separate figure?
            # We can return dunn dataframe
            del df  # Cleanup
            result["dunn_posthoc"] = dunn
        except Exception:
            pass

    return result


def friedman_test(*conditions, condition_names=None, save_path: str = None) -> dict:
    """Friedman Test for repeated measures."""
    if len(conditions) == 1 and isinstance(conditions[0], (list, tuple)):
        conditions = conditions[0]
    clean_conds = [
        as_float_array(c) for c in conditions
    ]  # Assume equal length and matched
    # NaNs handling? Friedman requires complete cases usually
    # We assume clean input for simplicity or drop listwise

    start_df = pd.DataFrame(clean_conds).T
    start_df.dropna(inplace=True)
    final_conds = [start_df[i].values for i in range(len(clean_conds))]

    stat, p_value = stats.friedmanchisquare(*final_conds)
    k, n = len(final_conds), len(final_conds[0])
    kendall_w = stat / (n * (k - 1)) if n * (k - 1) > 0 else 0

    if condition_names is None:
        condition_names = [f"C{i+1}" for i in range(k)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Spaghetti Sample
    plot_idx = np.random.choice(n, min(n, 50), replace=False)
    for i in plot_idx:
        axes[0].plot(
            range(k), [c[i] for c in final_conds], "o-", alpha=0.3, color="gray"
        )
    axes[0].plot(
        range(k),
        [np.median(c) for c in final_conds],
        "s-",
        color="red",
        lw=2,
        ms=10,
        label="Median",
    )
    axes[0].set_xticks(range(k))
    axes[0].set_xticklabels(condition_names)
    axes[0].set_title(f"Friedman chi2={stat:.2f}, p={p_value:.4f}")
    axes[0].legend()

    axes[1].boxplot(final_conds, labels=condition_names, patch_artist=True)
    axes[1].set_title(f"Kendall's W={kendall_w:.3f}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {
        "statistic": stat,
        "p_value": p_value,
        "kendall_w": kendall_w,
        "figure": fig,
    }


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


# --- 7. Resampling ---


def bootstrap_ci(
    data,
    stat_func=np.median,
    n_boot: int = 10000,
    ci: int = 95,
    seed: int = None,
    name: str = "Stat",
    save_path: str = None,
) -> dict:
    """Bootstrap Confidence Interval."""
    clean_data = as_float_array(data)
    clean_data = clean_data[~np.isnan(clean_data)]

    if seed is not None:
        np.random.seed(seed)

    n = len(clean_data)
    boots = np.zeros(n_boot)
    for i in range(n_boot):
        sample = np.random.choice(clean_data, n, replace=True)
        boots[i] = stat_func(sample)

    lo = np.percentile(boots, (100 - ci) / 2)
    hi = np.percentile(boots, 100 - (100 - ci) / 2)
    obs = stat_func(clean_data)
    se = np.std(boots)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(
        boots, bins=50, density=True, alpha=0.7, color="steelblue", edgecolor="white"
    )
    ax.axvline(obs, color="red", lw=2, label=f"Observed={obs:.3f}")
    ax.axvspan(
        lo, hi, alpha=0.2, color="orange", label=f"{ci}% CI: [{lo:.3f},{hi:.3f}]"
    )
    ax.set_title(f"{name} Bootstrap ({n_boot})")
    ax.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {"observed": obs, "ci_lower": lo, "ci_upper": hi, "se": se, "figure": fig}


def permutation_test(
    group1,
    group2,
    stat_func=np.median,
    n_perm: int = 5000,
    name1="G1",
    name2="G2",
    seed: int = None,
    save_path: str = None,
) -> dict:
    """Permutation test for difference in statistic."""
    g1 = as_float_array(group1)
    g1 = g1[~np.isnan(g1)]
    g2 = as_float_array(group2)
    g2 = g2[~np.isnan(g2)]

    if seed is not None:
        np.random.seed(seed)

    obs_diff = stat_func(g1) - stat_func(g2)
    combined = np.concatenate([g1, g2])
    n1 = len(g1)

    perms = np.zeros(n_perm)
    for i in range(n_perm):
        np.random.shuffle(combined)
        p1 = combined[:n1]
        p2 = combined[n1:]
        perms[i] = stat_func(p1) - stat_func(p2)

    p_value = np.mean(np.abs(perms) >= np.abs(obs_diff))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(
        perms, bins=50, density=True, alpha=0.7, color="lightgreen", edgecolor="white"
    )
    ax.axvline(obs_diff, color="red", lw=2, label=f"Diff={obs_diff:.3f}")
    ax.set_title(f"Permutation: {name1} vs {name2} (p={p_value:.4f})")
    ax.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

    return {"observed_diff": obs_diff, "p_value": p_value, "figure": fig}


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
