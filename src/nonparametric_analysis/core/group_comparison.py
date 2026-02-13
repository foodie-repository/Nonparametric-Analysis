"""Group comparison nonparametric analysis methods."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import scikit_posthocs as sp

from ..utils.stats import effect_size_r, as_float_array


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
