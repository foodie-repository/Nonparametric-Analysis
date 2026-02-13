import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import sys
from pathlib import Path

sys.path.append(str(Path("03_Code/src").resolve()))
from nonparametric_analysis.analysis import nonparametric_methods as np_methods


def test_mw_empty_series():
    g1 = pd.Series([], dtype=float)
    g2 = pd.Series([], dtype=float)

    try:
        print("Testing np_methods.mann_whitney_test with empty Series...")
        np_methods.mann_whitney_test(g1, g2)
        print("MW passed.")
    except Exception as e:
        print(f"MW FAILED: {e}")
        import traceback

        traceback.print_exc()

    try:
        print("Testing np_methods.ks_test with empty Series...")
        np_methods.ks_test(g1, g2)
        print("KS passed.")
    except Exception as e:
        print(f"KS FAILED: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_mw_empty_series()
