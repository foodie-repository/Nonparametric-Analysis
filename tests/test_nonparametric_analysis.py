"""Nonparametric analysis module tests."""

import numpy as np
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "03_Code" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from nonparametric_analysis.analysis import (
    adjust_pvalue_matrix_fdr,
    correlation_matrix_nonparametric,
    formula_violation_mask,
    generate_sample_dataset,
    mann_kendall_test,
    pettitt_test,
)


def test_pettitt_detects_change_point_near_true_location():
    rng = np.random.default_rng(7)
    left = rng.normal(loc=10.0, scale=1.0, size=45)
    right = rng.normal(loc=18.0, scale=1.0, size=45)
    values = np.concatenate([left, right])

    result = pettitt_test(values)
    assert 35 <= result["change_point"] <= 55
    assert result["p_value"] < 0.05


def test_mann_kendall_finds_positive_trend():
    x = np.arange(1, 50)
    y = x + np.random.default_rng(9).normal(0, 0.5, size=len(x))

    result = mann_kendall_test(y)
    assert result["tau"] > 0.8
    assert result["p_value"] < 0.001


def test_spearman_and_fdr_matrix_shapes():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [2, 4, 6, 8, 10],
            "c": [5, 4, 2, 3, 1],
        }
    )

    result = correlation_matrix_nonparametric(df, method="spearman")
    corr = result["correlation"]
    pvals = result["p_values"]
    pvals_adj = adjust_pvalue_matrix_fdr(pvals)

    assert corr.shape == (3, 3)
    assert pvals.shape == (3, 3)
    assert pvals_adj.shape == (3, 3)
    assert np.all(np.diag(pvals_adj.values) == 0.0)


def test_formula_violation_mask_identifies_broken_rows():
    df = pd.DataFrame(
        {
            "feature_1": [10.0, 20.0, 30.0],
            "feature_2": [1.0, 2.0, 3.0],
            "feature_total": [11.0, 22.0, 99.0],  # Row 2 is the only violation
        }
    )

    violations = formula_violation_mask(
        df,
        lambda frame: pd.Series(
            np.isclose(frame["feature_total"], frame["feature_1"] + frame["feature_2"]),
            index=frame.index
        ),
    )
    assert violations.sum() == 1
    assert bool(violations.iloc[2])


def test_sample_dataset_has_expected_columns():
    df = generate_sample_dataset(n_rows=120, seed=42)
    expected_columns = {
        "entity_id",
        "time_index",
        "group",
        "feature_1",
        "feature_2",
        "feature_3",
        "feature_total",
    }
    assert set(df.columns) == expected_columns
    assert len(df) == 120
