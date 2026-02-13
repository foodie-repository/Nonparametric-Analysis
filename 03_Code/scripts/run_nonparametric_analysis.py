#!/usr/bin/env python3
"""
Run nonparametric analysis pipeline.
"""
import sys
import argparse
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add src to path to allow importing packages
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from nonparametric_analysis.analysis import nonparametric_methods as np_methods
from nonparametric_analysis.analysis import utils
from nonparametric_analysis.analysis import integrity_checks
from nonparametric_analysis.analysis.visualizations import setup_visualization


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run nonparametric analysis pipeline.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("02_Data/sample_nonparametric.csv"),
        help="Path to input CSV file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("05_Outputs/nonparametric_run"),
        help="Directory to save outputs",
    )
    return parser.parse_args()


def analyze_column(col_name: str, data: pd.Series, figures_dir: Path) -> list[dict]:
    """Run single-column analysis tests."""
    results = []
    clean_data = data.dropna()

    if len(clean_data) < 3:
        print(f"Skipping {col_name}: Not enough data")
        return results

    # 1. Normality
    try:
        norm_res = np_methods.test_normality(
            clean_data,
            name=col_name,
            save_path=figures_dir / f"{col_name}_normality.png",
        )
        results.append(
            {
                "Variable": col_name,
                "Test": "Shapiro-Wilk",
                "Statistic": f"{norm_res['statistic']:.4f}",
                "P-Value": f"{norm_res['p_value']:.4f}",
                "Interpretation": utils.interpret_p_value(norm_res["p_value"]),
                "Details": "Normal" if norm_res["is_normal"] else "Non-normal",
            }
        )
    except Exception as e:
        print(f"Error in Normality ({col_name}): {e}")

    # 2. Runs Test
    try:
        runs_res = np_methods.runs_test_analysis(
            clean_data, name=col_name, save_path=figures_dir / f"{col_name}_runs.png"
        )
        results.append(
            {
                "Variable": col_name,
                "Test": "Runs Test",
                "Statistic": f"Z={runs_res['z']:.2f}",
                "P-Value": f"{runs_res['p_value']:.4f}",
                "Interpretation": utils.interpret_p_value(runs_res["p_value"]),
                "Details": f"Runs={runs_res['runs']} (Exp={runs_res['expected']:.1f})",
            }
        )
    except Exception as e:
        print(f"Error in Runs Test ({col_name}): {e}")

    # 3. Pettitt Test
    try:
        pet_res = np_methods.pettitt_test(
            clean_data, name=col_name, save_path=figures_dir / f"{col_name}_pettitt.png"
        )
        if pet_res["change_point"]:
            results.append(
                {
                    "Variable": col_name,
                    "Test": "Pettitt",
                    "Statistic": f"K={pet_res['statistic']:.0f}",
                    "P-Value": f"{pet_res['p_value']:.4f}",
                    "Interpretation": utils.interpret_p_value(pet_res["p_value"]),
                    "Details": f"Point={pet_res['change_point']} (Mdn: {pet_res['median_before']:.2f} -> {pet_res['median_after']:.2f})",
                }
            )
    except Exception as e:
        print(f"Error in Pettitt ({col_name}): {e}")

    # 4. Mann-Kendall
    try:
        mk_res = np_methods.mann_kendall_test(
            clean_data, name=col_name, save_path=figures_dir / f"{col_name}_mk.png"
        )
        results.append(
            {
                "Variable": col_name,
                "Test": "Mann-Kendall",
                "Statistic": f"Tau={mk_res['tau']:.3f}",
                "P-Value": f"{mk_res['p_value']:.4f}",
                "Interpretation": utils.interpret_p_value(mk_res["p_value"]),
                "Details": f"{mk_res['trend']} (Slope={mk_res['slope']:.4f})",
            }
        )
    except Exception as e:
        print(f"Error in Mann-Kendall ({col_name}): {e}")

    # 5. PELT (Optional)
    try:
        pelt_res = np_methods.detect_changepoints_pelt(
            clean_data, name=col_name, save_path=figures_dir / f"{col_name}_pelt.png"
        )
        if pelt_res["n_segments"] > 1:
            results.append(
                {
                    "Variable": col_name,
                    "Test": "PELT",
                    "Statistic": f"Segs={pelt_res['n_segments']}",
                    "P-Value": "N/A",
                    "Interpretation": "Change Points Detected",
                    "Details": f"Points: {pelt_res['changepoints']}",
                }
            )
    except Exception as e:
        # Expected if ruptures fail or data too small
        pass

    return results


def main():
    args = parse_args()

    # Setup
    setup_visualization()
    output_dir = args.output
    figures_dir = output_dir / "figures"

    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading data from {args.input}...")
    try:
        df = pd.read_csv(args.input)
    except Exception as e:
        print(f"Failed to read input data: {e}")
        sys.exit(1)

    # Integrity Check
    print("Running integrity checks...")
    integrity_report = integrity_checks.missing_rate_report(df)
    integrity_report.to_csv(output_dir / "integrity_check.csv", index=False)

    summary_list = []

    # Analyze Numeric Columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        print("No numeric columns found.")
        sys.exit(0)

    print(f"Analyzing {len(numeric_cols)} numeric columns...")

    for col in numeric_cols:
        print(f"  - {col}")
        col_results = analyze_column(col, df[col], figures_dir)
        summary_list.extend(col_results)

    # Correlation Analysis
    if len(numeric_cols) > 1:
        print("Running correlation analysis...")
        try:
            corr_res = np_methods.correlation_matrix_nonparametric(
                df, save_path=figures_dir / "correlation_matrix.png"
            )
            # Save adjusted p-values
            adj_p = utils.adjust_pvalue_matrix_fdr(corr_res["p_values"])
            adj_p.to_csv(output_dir / "correlation_pvalues_adjusted.csv")

            summary_list.append(
                {
                    "Variable": "All",
                    "Test": "Correlation Matrix",
                    "Statistic": "N/A",
                    "P-Value": "N/A",
                    "Interpretation": "Detailed",
                    "Details": "See figures/correlation_matrix.png",
                }
            )
        except Exception as e:
            print(f"Error in Correlation Analysis: {e}")

    # Save Summary
    if summary_list:
        summary_df = pd.DataFrame(summary_list)
        summary_path = output_dir / "summary.csv"
        summary_df.to_csv(summary_path, index=False)
        print(f"\nAnalysis complete. Results saved to {output_dir}")
        print(f"Summary: {summary_path}")
    else:
        print("\nAnalysis complete. No results to report.")

    plt.close("all")


if __name__ == "__main__":
    main()
