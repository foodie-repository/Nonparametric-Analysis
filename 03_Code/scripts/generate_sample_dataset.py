#!/usr/bin/env python3
"""Generate synthetic dataset for nonparametric analysis."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from nonparametric_analysis.analysis import generate_sample_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate sample dataset for nonparametric analysis.")
    parser.add_argument("--output", type=Path, default=Path("data/sample_nonparametric.csv"))
    parser.add_argument("--n-rows", type=int, default=120)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    df = generate_sample_dataset(n_rows=args.n_rows, seed=args.seed)
    df.to_csv(args.output, index=False)

    print(f"[sample-data] saved: {args.output}")
    print(f"[sample-data] rows: {len(df)}")
    print(f"[sample-data] missing feature_1: {int(df['feature_1'].isna().sum())}")
    print(f"[sample-data] missing feature_2: {int(df['feature_2'].isna().sum())}")


if __name__ == "__main__":
    main()
