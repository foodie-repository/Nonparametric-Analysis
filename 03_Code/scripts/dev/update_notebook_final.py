import json
from pathlib import Path

nb_path = Path("04_Notebooks/nonparametric_analysis_template.ipynb")


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": (
            source
            if isinstance(source, list)
            else [l + "\n" for l in source.split("\n")]
        ),
    }


def md(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": (
            source
            if isinstance(source, list)
            else [l + "\n" for l in source.split("\n")]
        ),
    }


cells = []

# Header
cells.append(
    md(
        [
            "# 비모수 분석 종합 템플릿 (All-in-One)",
            "",
            "이 노트북은 `nonparametric_analysis` 패키지가 제공하는 **17종의 모든 분석 기능**을 예시와 함께 제공합니다.",
            "각 결과 아래에는 **통계 비전문가를 위한 '결과 해석 가이드'**가 포함되어 있습니다.",
        ]
    )
)

# Setup
cells.append(
    code(
        [
            "import sys",
            "from pathlib import Path",
            "import pandas as pd",
            "import numpy as np",
            "",
            "%load_ext autoreload",
            "%autoreload 2",
            "",
            "# Add src to path",
            "sys.path.append(str(Path('../03_Code/src').resolve()))",
            "",
            "from nonparametric_analysis.analysis import nonparametric_methods as np_methods",
            "from nonparametric_analysis.analysis import utils",
            "from nonparametric_analysis.analysis.visualizations import setup_visualization",
            "",
            "setup_visualization() # 한글 폰트 및 스타일 설정",
        ]
    )
)

# Load Data
cells.append(
    code(
        [
            "# 데이터 로드",
            "data_path = Path('../02_Data/sample_nonparametric.csv')",
            "df = pd.read_csv(data_path)",
            "series = df['feature_1'].dropna()",
            "",
            "# 그룹 분할 (예시: feature_2 기준 50 초과/이하)",
            "group_a = df[df['feature_2'] > 50]['feature_1']",
            "group_b = df[df['feature_2'] <= 50]['feature_1']",
            "",
            "# 짝지어진 데이터 예시 (Paired)",
            "before = series[:30].values",
            "after = before + np.random.normal(0.5, 1, 30) # 약간의 변화 추가",
            "",
            "# 3개 그룹 데이터 예시 (Repeated / Multi)",
            "t1 = series[:30].values",
            "t2 = series[30:60].values",
            "t3 = series[60:90].values",
            "",
            "print(f'Data Loaded: Series N={len(series)}, Group A={len(group_a)}, Group B={len(group_b)}')",
        ]
    )
)

# --- Part 1: 단일 변수 분석 ---
cells.append(md("## 1. 단일 변수 분석 (Single Variable)"))

# 1.1 Normality
cells.append(md("### 1.1 정규성 검정 (Normality Test)"))
cells.append(code('res = np_methods.test_normality(series, name="Feature 1")'))
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- **Is Normal: True** → 데이터가 종 모양(정규분포)입니다.",
            "- **Is Normal: False** → 데이터가 치우쳐 있습니다. (비모수 분석 권장)",
        ]
    )
)

# 1.2 Runs Test
cells.append(md("### 1.2 런 검정 (Runs Test - 무작위성)"))
cells.append(code('res = np_methods.runs_test_analysis(series, name="Feature 1")'))
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 데이터가 **무작위(Random)**로 분포하는지 확인합니다.",
            "- **p < 0.05**: 무작위가 아닙니다. (어떤 패턴이 존재함)",
        ]
    )
)

# 1.3 Mann-Kendall
cells.append(md("### 1.3 추세 분석 (Mann-Kendall Trend)"))
cells.append(code('res = np_methods.mann_kendall_test(series, name="Feature 1")'))
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- **Trend**: increasing(증가), decreasing(감소), no trend(경향 없음)",
            "- **Slope**: 변화 속도 (양수면 증가, 음수면 감소)",
        ]
    )
)

# 1.4 Pettitt
cells.append(md("### 1.4 변곡점 탐지 (Pettitt Test)"))
cells.append(
    code(
        [
            'res = np_methods.pettitt_test(series, name="Feature 1")',
            "if res['change_point']:",
            "    print(f\"Change Point Index: {res['change_point']}\")",
        ]
    )
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 데이터의 흐름(평균)이 **갑자기 바뀌는 지점**을 찾습니다.",
        ]
    )
)

# 1.5 PELT
cells.append(md("### 1.5 다중 구간 분할 (PELT)"))
cells.append(
    code('res = np_methods.detect_changepoints_pelt(series, name="Feature 1")')
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 데이터의 패턴이 바뀌는 **여러 지점**을 동시에 찾습니다.",
        ]
    )
)

# --- Part 2: 그룹 비교 ---
cells.append(md("## 2. 그룹 비교 (Group Comparison)"))

# 2.1 Mann-Whitney
cells.append(md("### 2.1 두 독립 그룹 비교 (Mann-Whitney U)"))
cells.append(
    code(
        'res = np_methods.mann_whitney_test(group_a, group_b, name_a="Group A", name_b="Group B")'
    )
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 서로 다른 두 그룹(A vs B)의 차이를 비교합니다.",
            "- **p < 0.05**: 두 그룹은 통계적으로 **차이가 있습니다.**",
        ]
    )
)

# 2.2 Kolmogorov-Smirnov
cells.append(md("### 2.2 두 분포 비교 (K-S Test)"))
cells.append(
    code(
        'res = np_methods.ks_test(group_a, group_b, name_a="Group A", name_b="Group B")'
    )
)
cells.append(
    md(["#### 💡 결과 해석", "- 두 데이터의 **분포 모양** 자체가 다른지 봅니다."])
)

# 2.3 Wilcoxon Paired
cells.append(md("### 2.3 짝지어진 그룹 비교 (Wilcoxon Signed Rank)"))
cells.append(
    code(
        'res = np_methods.wilcoxon_paired_test(before, after, name_a="Before", name_b="After")'
    )
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- **전/후(Before/After)**와 같이 짝을 이룬 데이터의 변화를 봅니다.",
            "- **p < 0.05**: 전후에 유의미한 변화가 있었습니다.",
        ]
    )
)

# 2.4 Sign Test
cells.append(md("### 2.4 부호 검정 (Sign Test)"))
cells.append(code("res = np_methods.sign_test(before, after)"))
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 변화의 크기보다는 **증가했나/감소했나(방향)**만 봅니다.",
        ]
    )
)

# 2.5 Kruskal-Wallis
cells.append(md("### 2.5 세 독립 그룹 비교 (Kruskal-Wallis)"))
cells.append(
    code(
        'res = np_methods.kruskal_wallis_test([t1, t2, t3], group_names=["G1", "G2", "G3"])'
    )
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 서로 다른 3개 이상의 그룹 중 **적어도 하나는 다른지** 확인합니다.",
            "- **p < 0.05**: 그룹 간에 차이가 존재합니다.",
        ]
    )
)

# 2.6 Friedman
cells.append(md("### 2.6 반복 측정 비교 (Friedman Test)"))
cells.append(
    code(
        [
            "# 데이터 길이 맞춤 (필수)",
            "data_matrix = [t1, t2, t3]",
            'res = np_methods.friedman_test(data_matrix, group_names=["Time1", "Time2", "Time3"])',
        ]
    )
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 3개 이상의 시점/조건에서 **동일한 대상**을 반복 측정했을 때 차이를 봅니다.",
        ]
    )
)

# --- Part 3: 상관 분석 ---
cells.append(md("## 3. 상관 관계 (Correlation)"))

# 3.1 Spearman Matrix
cells.append(md("### 3.1 상관 행렬 (Heatmap)"))
cells.append(code("res = np_methods.correlation_matrix_nonparametric(df)"))
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 여러 변수들 간의 관계를 한눈에 봅니다.",
            "- **붉은색**: 관계 없음 / **초록색**: 관계 있음",
        ]
    )
)

# 3.2 Kendall / Distance
cells.append(md("### 3.2 다양한 상관 분석 (Kendall, Distance)"))
cells.append(
    code(
        [
            "x = df['feature_1'][:50]",
            "y = df['feature_2'][:50]",
            "",
            "res_k = np_methods.kendall_corr(x, y)",
            "print(f\"Kendall Tau: {res_k['correlation']:.4f}\")",
            "",
            "res_d = np_methods.distance_correlation(x, y)",
            "print(f\"Distance Corr: {res_d['correlation']:.4f}\")",
        ]
    )
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- **Kendall**: 순위 동점이 많을 때 더 정확합니다.",
            "- **Distance**: 곡선 관계(비선형)도 찾아냅니다. (0=독립, 1=종속)",
        ]
    )
)

# --- Part 4: 리샘플링 ---
cells.append(md("## 4. 리샘플링 기법 (Resampling)"))

# 4.1 Bootstrap
cells.append(md("### 4.1 부트스트랩 신뢰구간 (Bootstrap CI)"))
cells.append(
    code(
        [
            "res = np_methods.bootstrap_ci(series, stat_func=np.mean, n_boot=1000)",
            "print(f\"Bootstrap 95% CI: {res['ci_lower']:.4f} ~ {res['ci_upper']:.4f}\")",
        ]
    )
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 데이터가 적을 때, 통계량(평균 등)의 **신뢰구간**을 추정합니다.",
        ]
    )
)

# 4.2 Permutation
cells.append(md("### 4.2 순열 검정 (Permutation Test)"))
cells.append(
    code(
        [
            "stat_func = lambda x, y: np.mean(x) - np.mean(y)",
            "res = np_methods.permutation_test(group_a, group_b, stat_func=stat_func, n_perm=1000)",
            "print(f\"Permutation p-value: {res['p_value']:.4f}\")",
        ]
    )
)
cells.append(
    md(
        [
            "#### 💡 결과 해석",
            "- 정규분포 가정이 불가능할 때, **두 그룹의 차이가 우연인지** 검정합니다.",
        ]
    )
)

# Save
nb_content = {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb_content, f, indent=4)
