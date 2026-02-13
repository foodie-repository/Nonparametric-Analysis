import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(str(Path("03_Code/src").resolve()))

from nonparametric_analysis.analysis import nonparametric_methods as np_methods
from nonparametric_analysis.analysis.visualizations import setup_visualization

setup_visualization()

# Data
df = pd.read_csv("02_Data/sample_nonparametric.csv")
series = df["feature_1"].dropna()
# Fixed threshold to 50 based on data inspection
group_a = df[df["feature_2"] > 50]["feature_1"]
group_b = df[df["feature_2"] <= 50]["feature_1"]
before = series[:30].values
after = before + np.random.normal(0.5, 1, 30)
t1 = series[:30].values
t2 = series[30:60].values
t3 = series[60:90].values

print("Running tests...")

try:
    print("1. Normality")
    np_methods.test_normality(series)

    print("2. Runs Test")
    np_methods.runs_test_analysis(series)

    print("3. Mann-Kendall")
    np_methods.mann_kendall_test(series)

    print("4. Pettitt")
    np_methods.pettitt_test(series)

    print("5. PELT")
    np_methods.detect_changepoints_pelt(series)

    print("6. Mann-Whitney")
    np_methods.mann_whitney_test(group_a, group_b)

    print("7. KS Test")
    np_methods.ks_test(group_a, group_b)

    print("8. Wilcoxon Paired")
    np_methods.wilcoxon_paired_test(before, after)

    print("9. Sign Test")
    np_methods.sign_test(before, after)

    print("10. Kruskal-Wallis")
    np_methods.kruskal_wallis_test([t1, t2, t3])

    print("11. Friedman")
    np_methods.friedman_test([t1, t2, t3])

    print("12. Spearman Matrix")
    np_methods.correlation_matrix_nonparametric(df)

    print("13. Kendall Corr")
    np_methods.kendall_corr(series[:50], df["feature_2"][:50])

    print("14. Distance Corr")
    np_methods.distance_correlation(series[:50], df["feature_2"][:50])

    print("15. Bootstrap")
    np_methods.bootstrap_ci(series)

    print("16. Permutation")
    np_methods.permutation_test(group_a, group_b)

    print("17. Spearman Single")
    np_methods.spearman_correlation(series[:50], df["feature_2"][:50])

    print("ALL TESTS PASSED")

except Exception as e:
    print(f"FAILED at step: {e}")
    import traceback

    traceback.print_exc()
