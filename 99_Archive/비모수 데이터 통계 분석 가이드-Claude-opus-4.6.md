# 비모수 데이터 통계 분석 가이드

> **버전:** Claude-opus-4.6  
> **목적:** 소규모 데이터셋에 대한 비모수 통계 분석의 이론·코드·해석·보고서 작성 종합 가이드  
> **대상:** 1개 이상의 feature를 가진 비모수 데이터

---

## 목차

1. [비모수 통계 총론](#1-비모수-통계-총론)
2. [환경 설정](#2-환경-설정)
3. [단일 Feature 분석](#3-단일-feature-분석)
4. [두 Feature 간 비교 분석](#4-두-feature-간-비교-분석)
5. [다중 Feature 비교 분석](#5-다중-feature-비교-분석)
6. [변곡점(Change Point) 분석](#6-변곡점change-point-분석)
7. [Feature 간 상관성 분석](#7-feature-간-상관성-분석)
8. [기술 통계 정합성 검증](#8-기술-통계-정합성-검증)
9. [분석 방법 선택 의사결정 트리](#9-분석-방법-선택-의사결정-트리)
10. [시나리오별 분석 워크플로](#10-시나리오별-분석-워크플로)
11. [Jupyter Notebook 생성 가이드](#11-jupyter-notebook-생성-가이드)
12. [부록: 분석 방법 요약표](#12-부록-분석-방법-요약표)

---

## 1. 비모수 통계 총론

### 1.1 비모수 검정이란?

**모수(parametric) 검정**은 데이터가 특정 분포(대부분 정규분포)를 따른다고 가정하고, 그 분포의 모수(평균, 분산 등)를 추정·검정하는 방법이다. 반면 **비모수(nonparametric) 검정**은 데이터의 분포에 대한 가정을 최소화하여 분석하는 방법이다.

"비모수"라는 용어가 "모수가 없다"는 뜻은 아니다. 더 정확하게는 **"분포 자유(distribution-free)"** 검정으로, 데이터의 분포 형태를 특정하지 않는다는 의미이다.

### 1.2 비모수 검정의 핵심 원리: 순위(Rank)

대부분의 비모수 검정은 원래 데이터 값 대신 **순위(rank)**를 사용한다.

**예시:** 데이터 `[3.2, 1.5, 8.7, 2.1, 5.0]` → 순위 변환 `[3, 1, 5, 2, 4]`

순위 기반 접근의 장점:
- 이상치에 강건(robust): 극단값 `8.7`이 `800.7`이 되어도 순위 `5`는 동일
- 분포 형태에 무관: 원래 분포가 무엇이든 순위는 균등분포를 따름
- 순서형 데이터에 직접 적용 가능

### 1.3 언제 비모수 검정을 사용하는가?

| 조건 | 설명 | 판단 기준 |
|------|------|-----------|
| **소표본** | 중심극한정리를 적용하기 어려움 | n < 30 |
| **정규성 위반** | Shapiro-Wilk 검정에서 귀무가설 기각 | p < 0.05 |
| **순서형 데이터** | 등간 척도가 아닌 데이터 | 리커트 5점 척도 등 |
| **이상치 존재** | 극단값이 평균 기반 통계를 왜곡 | 박스플롯에서 이상치 다수 |
| **분포 비대칭** | 왜도(skewness)가 큰 경우 | \|skewness\| > 1 |

### 1.4 모수 검정 vs 비모수 검정

| 비교 항목 | 모수 검정 | 비모수 검정 |
|-----------|-----------|-------------|
| **분포 가정** | 정규분포 등 특정 분포 가정 | 분포 가정 없음 |
| **대표값** | 평균(mean) | 중앙값(median) |
| **산포도** | 표준편차(SD) | 사분위범위(IQR), MAD |
| **검정력** | 가정 충족 시 높음 (100%) | 상대적으로 낮음 (약 95%) |
| **이상치** | 민감함 | 강건함 |
| **표본 크기** | 큰 표본에서 유리 | 작은 표본에서도 사용 가능 |
| **데이터 유형** | 연속형(등간/비율 척도) | 순서형 이상 모두 가능 |

### 1.5 검정력(Power) 이슈

비모수 검정은 모수 검정 대비 **점근 상대 효율(ARE)**이 약 0.955(Wilcoxon vs t-검정)로, 가정이 충족되는 상황에서도 약 95%의 검정력을 유지한다. 그러나 가정이 위반되면 비모수 검정이 오히려 더 높은 검정력을 보인다.

**핵심 메시지:**
> 비모수 검정은 "차선책"이 아니라, 데이터 특성에 맞는 **"적합한 도구"**이다.
> 정규성이 보장되지 않는 소표본에서 모수 검정을 강제하면 **제1종 오류율이 증가**한다.

### 1.6 비모수 분석에서의 효과 크기

통계적 유의성(p-value)만으로는 실질적 의미를 판단할 수 없다. 반드시 **효과 크기(effect size)**를 함께 보고해야 한다.

| 효과 크기 지표 | 사용 검정 | 작은 효과 | 중간 효과 | 큰 효과 |
|---------------|-----------|-----------|-----------|---------|
| **r** (= Z/√N) | Mann-Whitney U, Wilcoxon | 0.10 | 0.30 | 0.50 |
| **η²** (에타 제곱) | Kruskal-Wallis | 0.01 | 0.06 | 0.14 |
| **W** (Kendall's W) | Friedman | 0.10 | 0.30 | 0.50 |

---

## 2. 환경 설정

### 2.1 필수 패키지

```bash
# uv 사용 시
uv add scipy numpy pandas matplotlib seaborn scikit-posthocs ruptures statsmodels jupyter nbformat

# pip 사용 시
pip install scipy numpy pandas matplotlib seaborn scikit-posthocs ruptures statsmodels jupyter nbformat
```

### 2.2 기본 임포트

```python
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import (
    shapiro, mannwhitneyu, wilcoxon, kruskal,
    friedmanchisquare, spearmanr, kendalltau,
    ks_2samp, median_test
)
import scikit_posthocs as sp
import ruptures as rpt
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="AppleGothic")
```

### 2.3 공통 유틸리티 함수

```python
def interpret_p_value(p_value, alpha=0.05):
    """p-value 해석 유틸리티"""
    if p_value < 0.001:
        return f"p = {p_value:.4f} → 매우 강한 통계적 유의성 (p < 0.001)"
    elif p_value < alpha:
        return f"p = {p_value:.4f} → 통계적으로 유의함 (p < {alpha})"
    else:
        return f"p = {p_value:.4f} → 통계적으로 유의하지 않음 (p ≥ {alpha})"

def effect_size_r(z_stat, n):
    """Mann-Whitney U / Wilcoxon 효과 크기 (r = |Z| / √N)"""
    r = abs(z_stat) / np.sqrt(n)
    size = "큰 효과" if r >= 0.5 else "중간 효과" if r >= 0.3 else "작은 효과"
    return r, size

def robust_descriptive(data, name="Feature"):
    """비모수 기술 통계 요약"""
    q1, median, q3 = np.percentile(data, [25, 50, 75])
    iqr = q3 - q1
    mad = np.median(np.abs(data - np.median(data)))
    return pd.DataFrame({
        '지표': ['N', '중앙값', 'Q1 (25%)', 'Q3 (75%)', 'IQR',
                '최솟값', '최댓값', 'MAD', '왜도', '첨도'],
        name: [len(data), f'{median:.3f}', f'{q1:.3f}', f'{q3:.3f}', f'{iqr:.3f}',
               f'{np.min(data):.3f}', f'{np.max(data):.3f}', f'{mad:.3f}',
               f'{stats.skew(data):.3f}', f'{stats.kurtosis(data):.3f}']
    })
```

---

## 3. 단일 Feature 분석

### 3.1 정규성 검정 (Shapiro-Wilk)

#### ① 이론적 배경

**Shapiro-Wilk 검정**은 데이터가 정규분포를 따르는지 평가하는 가장 강력한 정규성 검정이다. 특히 **소표본(n < 50)**에서 검정력이 우수하다.

- **원리:** 데이터의 순서통계량(order statistics)과 정규분포에서의 기대값 간의 상관계수를 계산
- **검정 통계량 W:** 0~1 범위이며 1에 가까울수록 정규분포에 가까움
- **수식:** W = (Σ aᵢ x₍ᵢ₎)² / Σ(xᵢ - x̄)² , 여기서 aᵢ는 정규분포 순서통계량의 기대값에서 유도

**다른 정규성 검정과의 비교:**

| 검정 방법 | 적합 표본 크기 | 특징 |
|-----------|-------------|------|
| Shapiro-Wilk | n < 50 (최적) | 소표본에서 검정력 가장 높음 |
| Kolmogorov-Smirnov | 제한 없음 | 검정력 낮음, 대표본에서 사용 |
| Anderson-Darling | 제한 없음 | 꼬리 부분 민감, K-S보다 강력 |
| D'Agostino-Pearson | n ≥ 20 | 왜도·첨도 결합 검정 |

#### ② 적용 조건

- ✅ **사용:** 비모수 검정 적용 여부를 판단하기 위한 사전 검정
- ✅ **사용:** 3 ≤ n ≤ 5000 범위에서 가장 신뢰도 높음
- ⚠️ **주의:** 대표본(n > 50)에서는 사소한 이탈도 유의하게 나옴 → Q-Q 플롯과 함께 판단
- ⚠️ **주의:** 동률(tie)이 많으면 검정력 저하

#### ③ Python 코드

```python
def test_normality(data, name="Feature", alpha=0.05):
    """Shapiro-Wilk 정규성 검정 + 시각적 진단"""
    stat, p_value = shapiro(data)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # 히스토그램 + KDE
    axes[0].hist(data, bins='auto', density=True, alpha=0.7,
                 color='steelblue', edgecolor='white')
    kde_x = np.linspace(min(data), max(data), 100)
    kde = stats.gaussian_kde(data)
    axes[0].plot(kde_x, kde(kde_x), 'r-', linewidth=2, label='KDE')
    # 정규 곡선 오버레이
    mu, sigma = np.mean(data), np.std(data)
    normal_y = stats.norm.pdf(kde_x, mu, sigma)
    axes[0].plot(kde_x, normal_y, 'g--', linewidth=1.5, label='정규분포')
    axes[0].set_title(f'{name} 분포')
    axes[0].legend(fontsize=8)
    
    # Q-Q Plot
    stats.probplot(data, dist="norm", plot=axes[1])
    axes[1].set_title(f'{name} Q-Q Plot')
    
    # Box Plot
    axes[2].boxplot(data, vert=True, patch_artist=True,
                    boxprops=dict(facecolor='lightyellow'))
    axes[2].set_title(f'{name} Box Plot')
    
    plt.suptitle(f'Shapiro-Wilk: W={stat:.4f}, p={p_value:.4f}', fontsize=12, y=1.02)
    plt.tight_layout()
    plt.show()
    
    is_normal = p_value >= alpha
    return {'statistic': stat, 'p_value': p_value, 'is_normal': is_normal}
```

#### ④ 결과 해석 가이드

| W 값 | p-value | 해석 |
|-------|---------|------|
| W ≈ 1.0 | p ≥ 0.05 | 정규분포 가정 유지 → 모수 검정 사용 가능 |
| W < 0.95 | p < 0.05 | 정규성 기각 → 비모수 검정 권장 |
| W < 0.90 | p < 0.01 | 강한 비정규성 → 비모수 검정 필수 |

**주의사항:**
- p > 0.05라고 해서 "정규분포이다"가 **아니다**. "정규성을 기각할 근거가 부족하다"는 것
- Q-Q 플롯에서 **양 끝이 직선에서 벗어나면** 꼬리 분포가 정규와 다름을 시각적으로 확인

#### ⑤ 보고서 작성 템플릿

> Shapiro-Wilk 정규성 검정 결과, [변수명]의 분포는 정규분포를 따르지 않는 것으로 나타났다(W = 0.892, p = .012). 따라서 이후 분석에서는 비모수 검정 방법을 적용하였다.

---

### 3.2 부호 검정 (Sign Test)

#### ① 이론적 배경

**부호 검정**은 가장 단순한 비모수 검정으로, 중앙값이 특정 값(θ₀)과 같은지를 검정한다. 데이터에서 θ₀보다 큰 값과 작은 값의 개수만을 이용한다.

- **원리:** 중앙값이 θ₀이면 각 관측값이 θ₀보다 클 확률과 작을 확률이 각 50%
- **검정 통계량:** θ₀보다 큰 값의 개수 → 이항분포 B(n, 0.5)를 따름
- **θ₀과 같은 값:** 제외하고 분석 (또는 절반씩 배분)

**장점:** 가정이 거의 없음 (독립성만 필요)  
**단점:** 값의 크기 정보를 무시하므로 검정력이 낮음

#### ② 적용 조건

- ✅ **사용:** 극단적으로 작은 표본 (n < 10)에서도 사용 가능
- ✅ **사용:** 이상치의 영향을 완전히 배제해야 할 때
- ❌ **비사용:** 검정력이 필요한 경우 → Wilcoxon 부호순위 검정 사용

#### ③ Python 코드

```python
def sign_test(data, hypothesized_median, name="Feature"):
    """단일 표본 부호 검정"""
    diff = np.array(data) - hypothesized_median
    diff = diff[diff != 0]
    n_pos = np.sum(diff > 0)
    n_neg = np.sum(diff < 0)
    n = n_pos + n_neg
    
    p_value = 2 * min(
        stats.binom.cdf(min(n_pos, n_neg), n, 0.5),
        1 - stats.binom.cdf(max(n_pos, n_neg) - 1, n, 0.5)
    )
    p_value = min(p_value, 1.0)
    
    # 시각화
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['#e74c3c' if d < 0 else '#2ecc71' for d in diff]
    ax.bar(range(len(diff)), diff, color=colors, edgecolor='white')
    ax.axhline(0, color='black', linewidth=1)
    ax.set_title(f'{name}: 부호 검정 (양수={n_pos}, 음수={n_neg}, p={p_value:.4f})')
    ax.set_ylabel(f'편차 (관측값 - {hypothesized_median})')
    plt.show()
    
    return {'n_pos': n_pos, 'n_neg': n_neg, 'p_value': p_value}
```

#### ④ 결과 해석 가이드

- **양수 개수 ≈ 음수 개수:** 중앙값이 θ₀과 유의하게 다르지 않음
- **한쪽이 크게 우세:** 중앙값이 θ₀과 유의하게 다름
- p-value는 이항분포에서 직접 계산되므로, **정확 검정(exact test)**임

#### ⑤ 보고서 작성 템플릿

> 부호 검정 결과, [변수명]의 중앙값이 [θ₀]과 유의하게 다른 것으로 나타났다(양수 15개, 음수 5개, p = .041). [변수명]의 중앙값(Mdn = [값])은 [θ₀]보다 [높은/낮은] 것으로 판단된다.

---

### 3.3 Wilcoxon 부호순위 검정 (단일 표본)

#### ① 이론적 배경

**Wilcoxon 부호순위 검정**은 부호 검정을 개선한 것으로, 편차의 **부호**뿐만 아니라 **크기(순위)**도 함께 활용한다. 단일 표본 t-검정의 비모수 대안이다.

- **원리:** 
  1. 각 관측값에서 θ₀을 빼서 편차(dᵢ) 계산
  2. 편차의 절대값에 순위를 부여
  3. 양수 편차의 순위 합(T⁺)과 음수 편차의 순위 합(T⁻) 계산
  4. T = min(T⁺, T⁻)를 검정 통계량으로 사용
- **가정:** 편차의 분포가 대칭적 (정규성은 불필요)
- **검정력:** 부호 검정보다 높음 (ARE ≈ 0.955 vs 정규분포 하 t-검정)

#### ② 적용 조건

- ✅ **사용:** 편차의 분포가 대칭적일 때 (왜도가 크지 않을 때)
- ✅ **사용:** n ≥ 6 이상 권장
- ❌ **비사용:** 편차 분포가 심하게 비대칭 → 부호 검정 사용

#### ③ Python 코드

```python
def wilcoxon_one_sample(data, hypothesized_median, name="Feature"):
    """Wilcoxon 부호순위 검정 (단일 표본)"""
    diff = np.array(data) - hypothesized_median
    stat, p_value = wilcoxon(diff, alternative='two-sided')
    n = len(diff[diff != 0])
    z = (stat - n*(n+1)/4) / np.sqrt(n*(n+1)*(2*n+1)/24)
    r, r_label = effect_size_r(z, n)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.boxplot(data, vert=False, patch_artist=True,
               boxprops=dict(facecolor='lightblue'))
    ax.axvline(hypothesized_median, color='red', linestyle='--',
               label=f'H₀ 중앙값={hypothesized_median}')
    ax.axvline(np.median(data), color='green', linestyle='-',
               label=f'표본 중앙값={np.median(data):.2f}')
    ax.legend()
    ax.set_title(f'{name}: Wilcoxon 부호순위 (T={stat:.1f}, p={p_value:.4f}, r={r:.3f})')
    plt.show()
    
    return {'statistic': stat, 'p_value': p_value, 'effect_size_r': r}
```

#### ④ 결과 해석 가이드

- **T 통계량:** 양수 순위 합과 음수 순위 합 중 작은 값. T가 작을수록 유의
- **효과 크기 r:** Z 통계량을 √N으로 나눈 값
  - r < 0.10: 무시할 수준
  - 0.10 ≤ r < 0.30: 작은 효과
  - 0.30 ≤ r < 0.50: 중간 효과
  - r ≥ 0.50: 큰 효과

#### ⑤ 보고서 작성 템플릿

> Wilcoxon 부호순위 검정 결과, [변수명]의 중앙값(Mdn = [값])은 [θ₀]과 통계적으로 유의한 차이를 보였다(T = [값], Z = [값], p = [값], r = [값]). 이는 [큰/중간/작은] 효과 크기에 해당한다.

---

**[→ 4절 이후는 다음 섹션에서 계속]**
