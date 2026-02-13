"""Sample dataset generation for nonparametric analysis demos."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_sample_dataset(n_rows: int = 120, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic dataset with trend, change point, and quality issues."""

    if n_rows < 30:
        raise ValueError("n_rows must be at least 30.")

    rng = np.random.default_rng(seed)
    time_index = np.arange(1, n_rows + 1)
    entity_ids = [f"E{idx:03d}" for idx in range(1, n_rows + 1)]
    groups = np.where(time_index <= (n_rows // 2), "control", "treatment")

    base = 45.0 + 0.20 * time_index + rng.normal(0.0, 2.2, size=n_rows)
    change_point = int(n_rows * 0.58)
    feature_1 = base.copy()
    feature_1[change_point:] += 9.0 + 0.08 * np.arange(n_rows - change_point)

    feature_2 = 0.85 * feature_1 + rng.normal(0.0, 2.8, size=n_rows)
    feature_3 = 4.0 * np.sqrt(np.clip(feature_1, a_min=0.0, a_max=None)) + rng.normal(0.0, 1.6, size=n_rows)
    feature_total = feature_1 + feature_2

    df = pd.DataFrame(
        {
            "entity_id": entity_ids,
            "time_index": time_index,
            "group": groups,
            "feature_1": feature_1,
            "feature_2": feature_2,
            "feature_3": feature_3,
            "feature_total": feature_total,
        }
    )

    missing_idx = rng.choice(n_rows, size=max(4, n_rows // 25), replace=False)
    df.loc[missing_idx[:2], "feature_1"] = np.nan
    df.loc[missing_idx[2:4], "feature_2"] = np.nan

    outlier_idx = rng.choice(n_rows, size=2, replace=False)
    df.loc[outlier_idx[0], "feature_1"] = 135.0
    df.loc[outlier_idx[1], "feature_1"] = 18.0

    rule_violation_idx = rng.choice(n_rows, size=2, replace=False)
    df.loc[rule_violation_idx, "feature_total"] += np.array([22.0, -17.0])

    if n_rows >= 40:
        df.loc[39, "entity_id"] = df.loc[38, "entity_id"]
        df.loc[39, "time_index"] = df.loc[38, "time_index"]

    return df
