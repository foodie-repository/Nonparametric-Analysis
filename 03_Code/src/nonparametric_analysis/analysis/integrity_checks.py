"""Data integrity checks for nonparametric workflows."""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd


def missing_rate_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return column-level missing count/rate report."""

    n_rows = len(df)
    rows: list[dict[str, float | str]] = []
    for column in df.columns:
        missing_count = int(df[column].isna().sum())
        missing_rate = float(missing_count / n_rows) if n_rows else 0.0
        rows.append(
            {
                "column": column,
                "missing_count": missing_count,
                "missing_rate": missing_rate,
            }
        )
    return pd.DataFrame(rows)


def duplicate_rows(df: pd.DataFrame, subset: list[str]) -> pd.DataFrame:
    """Return rows duplicated by key columns."""

    missing_cols = [col for col in subset if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns for duplicate check: {missing_cols}")
    if not subset:
        raise ValueError("subset must not be empty.")

    return df[df.duplicated(subset=subset, keep=False)].copy()


def range_violation_mask(
    values: pd.Series | np.ndarray | list[float],
    min_value: float,
    max_value: float,
    *,
    allow_nan: bool = True,
) -> np.ndarray:
    """Return mask for values outside [min_value, max_value]."""

    x = np.asarray(values, dtype=float)
    if min_value > max_value:
        raise ValueError("min_value must be <= max_value.")
    mask = (x < min_value) | (x > max_value)
    if not allow_nan:
        mask = mask | np.isnan(x)
    return mask


def mad_outlier_mask(values: pd.Series | np.ndarray | list[float], threshold: float = 3.5) -> np.ndarray:
    """Return MAD-based robust z-score outlier mask."""

    x = np.asarray(values, dtype=float)
    median = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - median))
    if mad == 0.0 or np.isnan(mad):
        return np.zeros(len(x), dtype=bool)

    robust_z = 0.6745 * (x - median) / mad
    return np.abs(robust_z) > threshold


def formula_violation_mask(
    df: pd.DataFrame,
    rule_fn: Callable[[pd.DataFrame], pd.Series],
) -> pd.Series:
    """
    Return violation mask from rule function.

    rule_fn must return True for valid rows.
    """

    valid_mask = rule_fn(df)
    if not isinstance(valid_mask, pd.Series):
        raise ValueError("rule_fn must return a pandas Series.")
    if valid_mask.dtype != bool:
        raise ValueError("rule_fn must return a boolean Series.")
    if len(valid_mask) != len(df):
        raise ValueError("rule_fn result length must match dataframe length.")
    return ~valid_mask
