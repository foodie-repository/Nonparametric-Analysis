"""Resampling methods for nonparametric analysis."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from ..utils.stats import as_float_array


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
