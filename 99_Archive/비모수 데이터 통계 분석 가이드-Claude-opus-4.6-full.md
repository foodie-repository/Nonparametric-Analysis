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

## 4. 두 Feature 간 비교 분석

### 4.1 Mann-Whitney U 검정 (독립 표본)

#### ① 이론적 배경

**Mann-Whitney U 검정**은 두 독립 그룹의 분포가 동일한지를 검정하는 가장 대표적인 비모수 방법으로, 독립표본 t-검정의 비모수 대안이다.

- **원리:** 두 그룹의 모든 관측값을 합쳐 순위를 매긴 후, 각 그룹의 순위 합을 비교
- **검정 통계량:** U = n₁n₂ + n₁(n₁+1)/2 - R₁ (R₁은 그룹1의 순위 합)
- **직관적 해석:** U는 "그룹1의 관측값이 그룹2보다 큰 쌍의 수", 즉 확률적 우위를 측정
- **가정:** ① 독립성 ② 순서형 이상 척도 ③ 두 그룹의 분포 형태가 유사(위치 차이만 검정 시)
- **ARE:** 정규 분포에서 t-검정 대비 약 0.955 (3/π ≈ 95.5%)

**"분포 형태가 유사"라는 가정의 의미:**
- 두 분포의 **형태(산포, 왜도)**가 비슷하면: "중앙값(위치) 차이" 검정
- 분포 형태가 다르면: "확률적 우위(P(X>Y))" 검정으로 해석 변경

#### ② 적용 조건

- ✅ **사용:** 두 독립 그룹 비교, 정규성 위반, 소표본
- ✅ **사용:** 순서형 데이터 (만족도 척도 등)
- ❌ **비사용:** 대응 표본 → Wilcoxon 부호순위
- ❌ **비사용:** 3개 이상 그룹 → Kruskal-Wallis

#### ③ Python 코드

```python
def mann_whitney_test(group1, group2, name1="Group1", name2="Group2"):
    """Mann-Whitney U 검정 + 효과 크기 + 시각화"""
    stat, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
    n1, n2 = len(group1), len(group2)
    n = n1 + n2
    # Z 통계량 계산
    mu_U = n1 * n2 / 2
    sigma_U = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    z = (stat - mu_U) / sigma_U
    r, r_label = effect_size_r(z, n)
    # 확률적 우위 (Common Language Effect Size)
    cles = stat / (n1 * n2)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 박스플롯 + 개별 데이터 포인트
    bp = axes[0].boxplot([group1, group2], labels=[name1, name2],
                          patch_artist=True, widths=0.5)
    bp['boxes'][0].set_facecolor('lightcoral')
    bp['boxes'][1].set_facecolor('lightskyblue')
    axes[0].scatter(np.ones(n1)*1 + np.random.normal(0, 0.04, n1),
                    group1, alpha=0.5, s=20, color='darkred')
    axes[0].scatter(np.ones(n2)*2 + np.random.normal(0, 0.04, n2),
                    group2, alpha=0.5, s=20, color='darkblue')
    axes[0].set_title(f'분포 비교 (U={stat:.1f}, p={p_value:.4f})')
    
    # 순위 분포 히스토그램
    all_data = np.concatenate([group1, group2])
    ranks = stats.rankdata(all_data)
    ranks1 = ranks[:n1]
    ranks2 = ranks[n1:]
    axes[1].hist(ranks1, bins='auto', alpha=0.6, label=name1, color='coral')
    axes[1].hist(ranks2, bins='auto', alpha=0.6, label=name2, color='skyblue')
    axes[1].set_title('순위 분포')
    axes[1].legend()
    
    plt.tight_layout()
    plt.show()
    
    print(f"[Mann-Whitney U] U = {stat:.1f}, Z = {z:.3f}")
    print(f"  효과 크기: r = {r:.3f} ({r_label})")
    print(f"  확률적 우위(CLES): P({name1}>{name2}) = {cles:.3f}")
    print(f"  {interpret_p_value(p_value)}")
    return {'statistic': stat, 'z': z, 'p_value': p_value,
            'effect_size_r': r, 'cles': cles}
```

#### ④ 결과 해석 가이드

| 지표 | 해석 |
|------|------|
| **U 통계량** | 그룹1 관측값이 그룹2보다 큰 쌍의 수 |
| **Z 통계량** | 대표본 근사. \|Z\| > 1.96이면 α=0.05에서 유의 |
| **효과 크기 r** | 0.1(작음), 0.3(중간), 0.5(큼) |
| **CLES** | P(X>Y), 0.5면 차이 없음, 1.0이면 완전 우위 |

**흔한 오해:** Mann-Whitney U는 "중앙값 비교"가 **아니다**. 정확히는 "확률적 우위"를 검정한다. 중앙값이 같아도 분포 형태가 다르면 유의할 수 있다.

#### ⑤ 보고서 작성 템플릿

> Mann-Whitney U 검정 결과, [그룹1](Mdn = [값], n = [수])과 [그룹2](Mdn = [값], n = [수]) 간 통계적으로 유의한 차이가 나타났다(U = [값], Z = [값], p = [값], r = [값]). 확률적 우위(CLES) = [값]으로, [그룹1]의 관측값이 [그룹2]보다 클 확률이 [%]임을 나타낸다.

---

### 4.2 Wilcoxon 부호순위 검정 (대응 표본)

#### ① 이론적 배경

**대응 표본 Wilcoxon 부호순위 검정**은 동일 대상에 대한 두 조건(사전-사후, 처리A-처리B)의 차이를 검정한다. 대응 표본 t-검정의 비모수 대안이다.

- **원리:** 쌍별 차이(dᵢ = xᵢ_after - xᵢ_before)를 구한 후, 단일 표본 Wilcoxon 부호순위 검정을 적용
- **가정:** 쌍별 차이의 분포가 대칭적

#### ② 적용 조건

- ✅ **사용:** 동일 피험자의 사전-사후 비교
- ✅ **사용:** 짝지어진(matched) 두 조건 비교
- ❌ **비사용:** 독립 그룹 → Mann-Whitney U
- ❌ **비사용:** 3개 이상 조건 → Friedman

#### ③ Python 코드

```python
def wilcoxon_paired_test(before, after, name="측정"):
    """대응 표본 Wilcoxon 부호순위 검정"""
    diff = np.array(after) - np.array(before)
    stat, p_value = wilcoxon(before, after, alternative='two-sided')
    n = len(diff[diff != 0])
    z = (stat - n*(n+1)/4) / np.sqrt(n*(n+1)*(2*n+1)/24)
    r, r_label = effect_size_r(z, n)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 사전-사후 변화 (Spaghetti Plot)
    for i in range(len(before)):
        color = '#2ecc71' if after[i] > before[i] else '#e74c3c'
        axes[0].plot([0, 1], [before[i], after[i]], 'o-', color=color, alpha=0.6)
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(['사전', '사후'])
    axes[0].set_title(f'{name}: 사전-사후 변화 (초록=증가, 빨강=감소)')
    
    # 차이값 분포
    axes[1].hist(diff, bins='auto', color='salmon', edgecolor='white', alpha=0.8)
    axes[1].axvline(0, color='black', linestyle='--', linewidth=1)
    axes[1].axvline(np.median(diff), color='red', linestyle='-', linewidth=2,
                    label=f'차이의 중앙값={np.median(diff):.2f}')
    axes[1].set_title(f'차이값 분포 (T={stat:.1f}, p={p_value:.4f})')
    axes[1].legend()
    
    plt.tight_layout()
    plt.show()
    
    return {'statistic': stat, 'z': z, 'p_value': p_value,
            'effect_size_r': r, 'median_diff': np.median(diff)}
```

#### ④ 결과 해석 가이드

- **T 통계량:** 양수 차이 순위 합과 음수 차이 순위 합 중 작은 값
- 차이값의 **중앙값(Median Difference)**을 함께 보고: 방향과 크기를 나타냄
- 효과 크기 r 기준은 Mann-Whitney U와 동일

#### ⑤ 보고서 작성 템플릿

> Wilcoxon 부호순위 검정 결과, [조건] 전후의 [변수명]에 유의한 차이가 나타났다(T = [값], Z = [값], p = [값], r = [값]). 사후 측정값의 중앙값(Mdn = [값])이 사전(Mdn = [값])보다 [높았/낮았]으며, 차이의 중앙값은 [값]이었다.

---

### 4.3 Kolmogorov-Smirnov 검정 (2표본)

#### ① 이론적 배경

**2표본 KS 검정**은 두 표본의 **누적분포함수(ECDF)** 간의 최대 차이를 검정 통계량으로 사용하여, 두 표본이 동일한 분포에서 왔는지 검정한다.

- **D 통계량:** D = max|F₁(x) - F₂(x)|, 즉 두 ECDF 간의 최대 수직 거리
- **강점:** 위치(중앙값)뿐만 아니라 산포, 왜도 등 **분포의 모든 특성** 차이를 탐지
- **약점:** 분포의 꼬리보다 **중심부** 차이에 더 민감

#### ② 적용 조건

- ✅ **사용:** 두 분포의 형태 전체를 비교하고 싶을 때
- ✅ **사용:** 연속형 데이터
- ❌ **비사용:** 이산형/순서형 데이터 (동률 문제)
- ⚠️ **주의:** 위치 차이만 검정하려면 Mann-Whitney U가 더 강력

#### ③ Python 코드

```python
def ks_test(group1, group2, name1="Group1", name2="Group2"):
    """2-표본 Kolmogorov-Smirnov 검정"""
    stat, p_value = ks_2samp(group1, group2)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    for data, name, color in [(group1, name1, '#3498db'), (group2, name2, '#e74c3c')]:
        sorted_data = np.sort(data)
        ecdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)
        ax.step(sorted_data, ecdf, where='post', label=name, color=color, linewidth=2)
    
    ax.set_xlabel('값')
    ax.set_ylabel('누적 확률')
    ax.set_title(f'ECDF 비교 — KS D={stat:.3f}, p={p_value:.4f}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()
    
    return {'statistic': stat, 'p_value': p_value}
```

#### ④ 결과 해석 가이드

| D 값 | 해석 |
|------|------|
| D ≈ 0 | 두 분포가 매우 유사 |
| D > 0.2 | 분포 차이가 눈에 띔 |
| D > 0.5 | 분포가 크게 다름 |

#### ⑤ 보고서 작성 템플릿

> 2표본 Kolmogorov-Smirnov 검정 결과, [그룹1]과 [그룹2]의 분포는 통계적으로 유의한 차이를 보였다(D = [값], p = [값]). ECDF 비교에서 두 분포는 [중심부/꼬리] 영역에서 주요 차이를 나타냈다.

---

## 5. 다중 Feature 비교 분석

### 5.1 Kruskal-Wallis H 검정

#### ① 이론적 배경

**Kruskal-Wallis H 검정**은 3개 이상 독립 그룹의 분포를 동시에 비교한다. 일원분산분석(one-way ANOVA)의 비모수 대안이다.

- **원리:** 모든 관측값을 합쳐 순위를 매긴 후, 그룹별 순위 합이 기대값과 유의하게 다른지 검정
- **검정 통계량:** H = (12 / N(N+1)) × Σ(Rᵢ²/nᵢ) - 3(N+1), 자유도 = k-1
- **분포:** 대표본에서 χ²(k-1) 분포에 근사
- **효과 크기:** η² = (H - k + 1) / (N - k)

**사후 검정의 필요성:** H 검정이 유의하면 "어떤 그룹 간에 차이가 있다"는 것만 알 수 있으므로, **구체적으로 어떤 쌍이 다른지** 사후 검정이 필요하다.
- **Dunn's Test:** 가장 일반적인 사후 검정 (순위 기반)
- **보정 방법:** Bonferroni (보수적), Holm (단계적), Benjamini-Hochberg (FDR 기반)

#### ② 적용 조건

- ✅ **사용:** 3개 이상 독립 그룹 비교
- ✅ **사용:** 그룹별 표본 크기가 달라도 사용 가능
- ❌ **비사용:** 2개 그룹 → Mann-Whitney U
- ❌ **비사용:** 반복측정 설계 → Friedman

#### ③ Python 코드

```python
def kruskal_wallis_test(*groups, group_names=None):
    """Kruskal-Wallis H 검정 + Dunn 사후 검정"""
    stat, p_value = kruskal(*groups)
    k = len(groups)
    N = sum(len(g) for g in groups)
    if group_names is None:
        group_names = [f'Group{i+1}' for i in range(k)]
    
    # 효과 크기 η²
    eta_sq = (stat - k + 1) / (N - k)
    eta_label = "큰" if eta_sq >= 0.14 else "중간" if eta_sq >= 0.06 else "작은"
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bp = ax.boxplot(groups, labels=group_names, patch_artist=True)
    colors = plt.cm.Set3(np.linspace(0, 1, k))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    # 개별 데이터 포인트 오버레이
    for i, g in enumerate(groups):
        jitter = np.random.normal(0, 0.04, len(g))
        ax.scatter(np.full(len(g), i+1) + jitter, g, alpha=0.4, s=15, color='black')
    ax.set_title(f'Kruskal-Wallis H={stat:.2f}, p={p_value:.4f}, η²={eta_sq:.3f} ({eta_label} 효과)')
    plt.show()
    
    result = {'statistic': stat, 'p_value': p_value, 'eta_squared': eta_sq}
    
    # 유의한 경우 Dunn 사후 검정
    if p_value < 0.05:
        all_data = np.concatenate(groups)
        all_labels = np.concatenate([[name]*len(g) for name, g in zip(group_names, groups)])
        df = pd.DataFrame({'value': all_data, 'group': all_labels})
        dunn = sp.posthoc_dunn(df, val_col='value', group_col='group', p_adjust='bonferroni')
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(dunn, annot=True, fmt='.4f', cmap='RdYlGn_r',
                    center=0.05, ax=ax, vmin=0, vmax=1)
        ax.set_title('Dunn 사후 검정 p-value (Bonferroni 보정)')
        plt.show()
        result['dunn_posthoc'] = dunn
    
    return result
```

#### ④ 결과 해석 가이드

1. **H 통계량과 p-value:** 전체적으로 그룹 간 차이가 있는지 판단
2. **η² 효과 크기:** 0.01(작은), 0.06(중간), 0.14(큰)
3. **Dunn 사후 검정 히트맵:** p < 0.05인 쌍이 유의한 차이가 있는 그룹 쌍

**주의:** 그룹 수가 많으면 다중비교 보정이 보수적이 되어, 실제 차이가 있어도 탐지하지 못할 수 있다 (제2종 오류 증가).

#### ⑤ 보고서 작성 템플릿

> Kruskal-Wallis H 검정 결과, [변수명]에서 그룹 간 통계적으로 유의한 차이가 나타났다(H(df) = [값], p = [값], η² = [값]). Dunn 사후 검정(Bonferroni 보정) 결과, [그룹A]와 [그룹B] 간(p = [값]), [그룹A]와 [그룹C] 간(p = [값])에서 유의한 차이가 확인되었다.

---

### 5.2 Friedman 검정

#### ① 이론적 배경

**Friedman 검정**은 3개 이상 **반복측정(대응)** 조건을 비교하는 비모수 검정이다. 반복측정 ANOVA의 비모수 대안이다.

- **원리:** 각 피험자(블록) 내에서 조건별 값에 순위를 부여하고, 조건별 순위 합이 동일한지 검정
- **검정 통계량:** χ²_F = (12 / nk(k+1)) × Σ Rⱼ² - 3n(k+1)
- **효과 크기:** Kendall's W = χ²_F / (n(k-1)), 범위 0~1

#### ② 적용 조건

- ✅ **사용:** 동일 피험자가 3개 이상 조건을 모두 경험한 설계
- ✅ **사용:** 시간에 따른 3회 이상 반복 측정
- ❌ **비사용:** 독립 그룹 → Kruskal-Wallis
- ❌ **비사용:** 2개 조건만 → Wilcoxon 부호순위

#### ③ Python 코드

```python
def friedman_test(*conditions, condition_names=None):
    """Friedman 검정 + Kendall's W 효과 크기"""
    stat, p_value = friedmanchisquare(*conditions)
    k = len(conditions)
    n = len(conditions[0])
    W = stat / (n * (k - 1))  # Kendall's W
    if condition_names is None:
        condition_names = [f'Cond{i+1}' for i in range(k)]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 개별 대상자 변화 추적 (Spaghetti Plot)
    for i in range(n):
        values = [cond[i] for cond in conditions]
        axes[0].plot(range(k), values, 'o-', alpha=0.3, color='gray')
    medians = [np.median(c) for c in conditions]
    axes[0].plot(range(k), medians, 's-', color='red', linewidth=2,
                 markersize=10, label='중앙값', zorder=5)
    axes[0].set_xticks(range(k))
    axes[0].set_xticklabels(condition_names)
    axes[0].set_title(f'Friedman χ²={stat:.2f}, p={p_value:.4f}')
    axes[0].legend()
    
    # 조건별 박스플롯
    axes[1].boxplot(conditions, labels=condition_names, patch_artist=True)
    axes[1].set_title(f"Kendall's W = {W:.3f}")
    
    plt.tight_layout()
    plt.show()
    
    return {'statistic': stat, 'p_value': p_value, 'kendall_w': W}
```

#### ④ 결과 해석 가이드

- **Kendall's W:** 0(완전 불일치) ~ 1(완전 일치), 효과 크기 지표
  - W < 0.1: 무시할 수준, 0.1~0.3: 약한, 0.3~0.5: 중간, > 0.5: 강한
- Friedman이 유의하면 **Nemenyi 사후 검정** 또는 **Wilcoxon 쌍별 비교(Bonferroni 보정)**

#### ⑤ 보고서 작성 템플릿

> Friedman 검정 결과, [k]개 조건 간 [변수명]에 통계적으로 유의한 차이가 나타났다(χ²(df) = [값], p = [값], Kendall's W = [값]). 중앙값은 [조건1]([값]), [조건2]([값]), [조건3]([값]) 순이었다.

## 6. 변곡점(Change Point) 분석

### 6.1 이론적 배경 (공통)

**변곡점(change point) 분석**은 시계열이나 순서형 데이터에서 통계적 특성(평균, 분산, 분포)이 갑작스럽게 변화하는 지점을 탐지한다.

**비모수적 변곡점 탐지의 이점:**
- 분포 가정 없이 분포의 변화를 탐지
- 이상치에 강건한 탐지 가능
- 비선형적 변화도 감지

**주요 알고리즘 비교:**

| 알고리즘 | 원리 | 변곡점 수 | 계산 복잡도 | 적합 상황 |
|----------|------|-----------|-----------|-----------|
| **PELT** | 동적 프로그래밍 + 가지치기 | 자동 추정 | O(n) | 변곡점 수를 모를 때 |
| **Binary Segmentation** | 이진 분할 재귀 | 사전 지정 | O(n log n) | 변곡점 수를 알 때 |
| **순위 기반 (슬라이딩 윈도우)** | Mann-Whitney U 반복 | 자동 탐지 | O(n × w) | 비모수적 접근 필요 시 |

---

### 6.2 PELT 알고리즘

#### ② 적용 조건

- ✅ **사용:** 변곡점 개수를 모르는 경우 (자동 추정)
- ✅ **사용:** 대규모 시계열 데이터 (O(n) 복잡도)
- ⚠️ **주의:** penalty 값에 민감 — BIC 기반 자동 설정 권장

#### ③ Python 코드

```python
def detect_changepoints_pelt(data, model="rbf", min_size=2, penalty=None, name="Signal"):
    """PELT 알고리즘 변곡점 탐지"""
    signal = np.array(data).reshape(-1, 1)
    if penalty is None:
        penalty = np.log(len(data)) * np.var(data)  # BIC 기반
    
    algo = rpt.Pelt(model=model, min_size=min_size).fit(signal)
    result = algo.predict(pen=penalty)
    
    n_cp = len(result) - 1
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # 원본 데이터 + 변곡점
    axes[0].plot(data, 'b-', linewidth=1.5, alpha=0.8)
    prev = 0
    for i, cp in enumerate(result):
        segment = data[prev:cp]
        axes[0].hlines(np.median(segment), prev, cp, colors='red', linewidth=2.5)
        if cp != result[-1]:
            axes[0].axvline(cp, color='red', linestyle='--', alpha=0.7,
                           label=f'CP {i+1} (idx={cp})')
        prev = cp
    axes[0].set_title(f'{name}: PELT 변곡점 탐지 ({n_cp}개)')
    axes[0].legend(fontsize=8)
    
    # 구간별 박스플롯
    segments = []
    labels = []
    prev = 0
    for i, cp in enumerate(result):
        segments.append(data[prev:cp])
        labels.append(f'구간{i+1}\n({prev}-{cp})')
        prev = cp
    axes[1].boxplot(segments, labels=labels, patch_artist=True)
    axes[1].set_title('구간별 분포 비교')
    
    plt.tight_layout()
    plt.show()
    return {'changepoints': result[:-1], 'n_segments': len(result)}
```

#### ④ 결과 해석

- 변곡점 전후 구간의 **중앙값 변화량**과 **분포 형태 변화**를 함께 확인
- penalty가 클수록 변곡점이 적게 탐지됨 (과적합 방지)

#### ⑤ 보고서 작성 템플릿

> PELT 알고리즘을 적용하여 [데이터명]에서 [N]개의 변곡점이 탐지되었다(인덱스: [값들]). 구간1(idx 0-[cp1])의 중앙값은 [값], 구간2(idx [cp1]-[cp2])의 중앙값은 [값]으로, 변곡점 [cp1]에서 약 [%] 변화가 관찰되었다.

---

### 6.3 순위 기반 변곡점 탐지

#### ② 적용 조건

- ✅ **사용:** 완전한 비모수적 접근이 필요할 때
- ✅ **사용:** 이상치가 많은 데이터
- ⚠️ **주의:** 윈도우 크기(window) 선택이 결과에 영향

#### ③ Python 코드

```python
def rank_based_changepoint(data, window=5, name="Signal"):
    """순위 기반 변곡점 탐지 (Mann-Whitney U 슬라이딩 윈도우)"""
    n = len(data)
    p_values = []
    positions = []
    
    for i in range(window, n - window):
        left = data[max(0, i-window):i]
        right = data[i:min(n, i+window)]
        if len(left) >= 2 and len(right) >= 2:
            _, p = mannwhitneyu(left, right, alternative='two-sided')
            p_values.append(p)
            positions.append(i)
    
    p_arr = np.array(p_values)
    significant = p_arr < 0.05
    changepoints = []
    for i in range(1, len(p_arr)-1):
        if significant[i] and p_arr[i] < p_arr[i-1] and p_arr[i] < p_arr[i+1]:
            changepoints.append(positions[i])
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    axes[0].plot(data, 'b-', linewidth=1.5)
    for cp in changepoints:
        axes[0].axvline(cp, color='red', linestyle='--', alpha=0.7)
    axes[0].set_title(f'{name}: 순위 기반 변곡점 탐지')
    
    axes[1].plot(positions, -np.log10(p_arr), 'g-', linewidth=1)
    axes[1].axhline(-np.log10(0.05), color='red', linestyle=':', label='α=0.05')
    axes[1].set_ylabel('-log₁₀(p)')
    axes[1].legend()
    plt.tight_layout()
    plt.show()
    
    return {'changepoints': changepoints}
```

#### ④ 결과 해석

- **-log₁₀(p) 그래프:** 높은 봉우리가 있는 위치가 변곡점 후보
- α=0.05 기준선(빨간 점선) 위의 영역이 유의한 변화 구간
- 복수의 인접한 유의 지점이 있으면 가장 낮은 p-value를 가진 위치가 진정한 변곡점

---

## 7. Feature 간 상관성 분석

### 7.1 이론적 배경 (공통)

비모수 상관분석은 두 변수 간의 **단조(monotonic) 관계**를 측정한다. Pearson 상관계수가 **선형 관계**만 탐지하는 것과 달리, 비모수 상관계수는 비선형이지만 단조적인 관계도 포착한다.

**예시:** y = x² (x > 0)은 Pearson r < 1이지만, Spearman ρ = 1 (완벽한 단조 증가)

| 상관계수 | 측정 대상 | 장점 | 약점 |
|----------|-----------|------|------|
| **Pearson r** | 선형 관계 | 가장 높은 검정력 (정규 분포 시) | 이상치에 민감, 비선형 관계 못 탐지 |
| **Spearman ρ** | 단조 관계 (순위) | 이상치에 강건, 비선형 탐지 | 비단조 관계 못 탐지 |
| **Kendall τ** | 단조 관계 (쌍별) | 소표본에서 더 정확, 동률에 강건 | 계산 느림 (O(n²)) |

**Spearman vs Kendall 선택 기준:**
- **n < 20:** Kendall τ 권장 (소표본에서 더 안정적)
- **n ≥ 20:** Spearman ρ 사용 (더 직관적, 계산 빠름)
- **동률이 많은 경우:** Kendall τ 권장

---

### 7.2 Spearman 순위 상관계수

#### ③ Python 코드

```python
def spearman_correlation(x, y, x_name="X", y_name="Y"):
    """Spearman 순위 상관분석 + 시각화"""
    rho, p_value = spearmanr(x, y)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 원본 데이터 산점도
    axes[0].scatter(x, y, alpha=0.6, edgecolors='white', s=80, c='steelblue')
    axes[0].set_xlabel(x_name)
    axes[0].set_ylabel(y_name)
    axes[0].set_title(f'원본 데이터 (Spearman ρ = {rho:.3f}, p = {p_value:.4f})')
    
    # 순위 변환 산점도
    rx, ry = stats.rankdata(x), stats.rankdata(y)
    axes[1].scatter(rx, ry, alpha=0.6, color='coral', s=80, edgecolors='white')
    z = np.polyfit(rx, ry, 1)
    p = np.poly1d(z)
    rx_sorted = np.sort(rx)
    axes[1].plot(rx_sorted, p(rx_sorted), 'r--', linewidth=1.5)
    axes[1].set_xlabel(f'{x_name} (순위)')
    axes[1].set_ylabel(f'{y_name} (순위)')
    axes[1].set_title('순위 변환 후')
    
    plt.tight_layout()
    plt.show()
    
    strength = "강한" if abs(rho)>=0.7 else "중간" if abs(rho)>=0.4 else "약한"
    direction = "양의" if rho > 0 else "음의"
    print(f"[Spearman] ρ = {rho:.4f} → {strength} {direction} 상관")
    return {'rho': rho, 'p_value': p_value}
```

#### ④ 결과 해석

| ρ 범위 | 강도 해석 |
|--------|-----------|
| 0.00 ~ 0.19 | 무시할 수준 |
| 0.20 ~ 0.39 | 약한 상관 |
| 0.40 ~ 0.69 | 중간 상관 |
| 0.70 ~ 0.89 | 강한 상관 |
| 0.90 ~ 1.00 | 매우 강한 상관 |

#### ⑤ 보고서 작성 템플릿

> Spearman 순위 상관분석 결과, [변수X]와 [변수Y] 간 통계적으로 유의한 [강한/중간/약한] [양의/음의] 상관관계가 나타났다(ρ = [값], p = [값], n = [수]).

---

### 7.3 Kendall τ 상관계수

#### ③ Python 코드

```python
def kendall_correlation(x, y, x_name="X", y_name="Y"):
    """Kendall τ 상관분석"""
    tau, p_value = kendalltau(x, y)
    strength = "강한" if abs(tau)>=0.5 else "중간" if abs(tau)>=0.3 else "약한"
    direction = "양의" if tau > 0 else "음의"
    print(f"[Kendall] τ = {tau:.4f} → {strength} {direction} 상관")
    print(f"  {interpret_p_value(p_value)}")
    return {'tau': tau, 'p_value': p_value}
```

**⑤ 보고서 템플릿:** Kendall 순위 상관분석 결과, [변수X]와 [변수Y] 간 유의한 상관이 나타났다(τ = [값], p = [값]).

---

### 7.4 다변량 상관 매트릭스

```python
def correlation_matrix_nonparametric(df, method='spearman'):
    """다변량 비모수 상관 매트릭스 + 유의성 히트맵"""
    cols = df.columns
    n_cols = len(cols)
    corr = df.corr(method=method)
    
    p_matrix = pd.DataFrame(np.ones((n_cols, n_cols)), columns=cols, index=cols)
    for i, c1 in enumerate(cols):
        for j, c2 in enumerate(cols):
            if i != j:
                func = spearmanr if method == 'spearman' else kendalltau
                _, p = func(df[c1], df[c2])
                p_matrix.iloc[i, j] = p
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, vmin=-1, vmax=1, ax=axes[0], square=True)
    axes[0].set_title(f'{method.capitalize()} 상관 매트릭스')
    
    sns.heatmap(p_matrix, mask=mask, annot=True, fmt='.3f', cmap='RdYlGn_r',
                center=0.05, ax=axes[1], square=True, vmin=0, vmax=0.1)
    axes[1].set_title('p-value 매트릭스')
    plt.tight_layout()
    plt.show()
    return {'correlation': corr, 'p_values': p_matrix}
```

---

## 8. 기술 통계 정합성 검증

### 8.1 이론적 배경 (공통)

정합성 검증은 데이터나 분석 결과의 **신뢰성과 일관성**을 확인하는 과정이다.

| 방법 | 목적 | 핵심 질문 |
|------|------|-----------|
| **Bootstrap** | 신뢰구간 추정 | "추정값이 얼마나 신뢰할 수 있는가?" |
| **Permutation** | 그룹 차이 검증 | "이 차이가 우연으로 발생할 수 있는가?" |
| **Runs Test** | 무작위성 검증 | "데이터에 패턴이 있는가?" |

이 세 방법은 모두 **재표본(resampling)** 또는 **조합론** 기반으로, 분포 가정이 전혀 필요 없다.

---

### 8.2 Bootstrap 신뢰구간

#### ① 이론적 배경

**Bootstrap**은 관측된 표본에서 복원추출로 수천 개의 "가상 표본"을 만들어, 통계량의 분포를 경험적으로 추정하는 방법이다.

- **원리:** 표본 = 모집단의 축소판이라는 가정 하에, 복원추출로 통계량의 변동성 추정
- **핵심 장점:** 어떤 통계량이든(중앙값, IQR, 상관계수 등) 신뢰구간 추정 가능
- **백분위수 방법:** Bootstrap 분포의 2.5%, 97.5% 분위수를 95% CI로 사용

#### ③ Python 코드

```python
def bootstrap_ci(data, stat_func=np.median, n_boot=10000, ci=95, name="통계량"):
    """Bootstrap 신뢰구간 추정"""
    np.random.seed(42)
    boot_stats = [stat_func(np.random.choice(data, size=len(data), replace=True))
                  for _ in range(n_boot)]
    
    lower = np.percentile(boot_stats, (100-ci)/2)
    upper = np.percentile(boot_stats, 100-(100-ci)/2)
    observed = stat_func(data)
    se = np.std(boot_stats)  # Bootstrap 표준오차
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(boot_stats, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='white')
    ax.axvline(observed, color='red', linewidth=2, label=f'관측값 = {observed:.3f}')
    ax.axvspan(lower, upper, alpha=0.2, color='orange', label=f'{ci}% CI: [{lower:.3f}, {upper:.3f}]')
    ax.set_title(f'{name} Bootstrap 분포 ({n_boot}회)')
    ax.legend()
    plt.show()
    
    print(f"[Bootstrap {ci}% CI] 관측값: {observed:.4f}, SE: {se:.4f}")
    print(f"  신뢰구간: [{lower:.4f}, {upper:.4f}]")
    return {'observed': observed, 'ci_lower': lower, 'ci_upper': upper, 'se': se}
```

#### ⑤ 보고서 작성 템플릿

> [변수명]의 중앙값은 [값]이었으며, 10,000회 Bootstrap을 통한 95% 신뢰구간은 [[하한], [상한]]이었다(SE = [값]).

---

### 8.3 Permutation Test (순열 검정)

#### ① 이론적 배경

**순열 검정**은 귀무가설(두 그룹에 차이가 없다) 하에서 데이터의 그룹 라벨을 무작위로 섞어 검정 통계량의 분포를 생성하고, 관측된 차이가 이 분포에서 얼마나 극단적인지 평가한다.

- **원리:** 차이가 없다면 라벨을 바꿔도 통계량이 비슷할 것
- **정확 검정:** 모든 순열을 계산하면 정확한 p-value, 근사치는 Monte Carlo 시뮬레이션

#### ③ Python 코드

```python
def permutation_test(group1, group2, stat_func=np.median, n_perm=10000,
                     name1="Group1", name2="Group2"):
    """순열 검정"""
    observed_diff = stat_func(group1) - stat_func(group2)
    combined = np.concatenate([group1, group2])
    n1 = len(group1)
    
    np.random.seed(42)
    perm_diffs = []
    for _ in range(n_perm):
        np.random.shuffle(combined)
        perm_diffs.append(stat_func(combined[:n1]) - stat_func(combined[n1:]))
    
    p_value = np.mean(np.abs(perm_diffs) >= np.abs(observed_diff))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(perm_diffs, bins=50, density=True, alpha=0.7, color='lightgreen', edgecolor='white')
    ax.axvline(observed_diff, color='red', linewidth=2, label=f'관측 차이 = {observed_diff:.3f}')
    ax.axvline(-observed_diff, color='red', linewidth=2, linestyle='--')
    ax.set_title(f'순열 검정: {name1} vs {name2} (p = {p_value:.4f})')
    ax.legend()
    plt.show()
    
    return {'observed_diff': observed_diff, 'p_value': p_value}
```

#### ⑤ 보고서 작성 템플릿

> 순열 검정(10,000회) 결과, [그룹1]과 [그룹2]의 중앙값 차이([값])는 통계적으로 유의하였다(p = [값]).

---

### 8.4 런 검정 (Runs Test)

#### ① 이론적 배경

**런 검정**은 데이터가 무작위로 배열되어 있는지를 검정한다. 시계열에서 **추세, 주기, 군집** 등 비무작위 패턴의 존재를 확인한다.

- **런(run):** 동일한 특성을 가진 연속된 관측값의 묶음
- **원리:** 중앙값 기준으로 이진화한 후, "위-아래" 전환 횟수가 기대값과 다른지 검정
- 런이 **너무 적으면:** 추세 또는 군집 존재
- 런이 **너무 많으면:** 체계적 교대 패턴 존재

#### ③ Python 코드

```python
def runs_test_analysis(data, name="Data"):
    """런 검정 + 시각화"""
    median_val = np.median(data)
    binary = (np.array(data) >= median_val).astype(int)
    
    runs = 1
    for i in range(1, len(binary)):
        if binary[i] != binary[i-1]:
            runs += 1
    
    n1 = np.sum(binary == 1)
    n0 = np.sum(binary == 0)
    n = n1 + n0
    expected_runs = (2*n1*n0/n) + 1
    std_runs = np.sqrt(2*n1*n0*(2*n1*n0 - n) / (n**2 * (n-1)))
    z = (runs - expected_runs) / std_runs if std_runs > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    axes[0].plot(data, 'b-o', markersize=4)
    axes[0].axhline(median_val, color='red', linestyle='--', label=f'중앙값={median_val:.2f}')
    axes[0].fill_between(range(len(data)), median_val, data,
                         where=np.array(data)>=median_val, alpha=0.3, color='green')
    axes[0].fill_between(range(len(data)), median_val, data,
                         where=np.array(data)<median_val, alpha=0.3, color='red')
    axes[0].set_title(f'{name}: 런 검정')
    axes[0].legend()
    
    axes[1].step(range(len(binary)), binary, 'k-', where='mid')
    axes[1].set_yticks([0, 1])
    axes[1].set_yticklabels(['중앙값 미만', '중앙값 이상'])
    axes[1].set_title(f'런 수={runs}, 기대 런 수={expected_runs:.1f}, Z={z:.2f}, p={p_value:.4f}')
    plt.tight_layout()
    plt.show()
    
    conclusion = "무작위적" if p_value >= 0.05 else "비무작위적 패턴 존재"
    print(f"[런 검정] → 데이터는 {conclusion}")
    return {'runs': runs, 'expected_runs': expected_runs, 'z': z, 'p_value': p_value}
```

#### ⑤ 보고서 작성 템플릿

> 런 검정 결과, 관측된 런 수([값])는 기대 런 수([값])와 [유의한/유의하지 않은] 차이를 보였다(Z = [값], p = [값]). 이는 데이터가 [무작위적임을 시사/비무작위적 패턴을 포함함을 시사]한다.

## 9. 분석 방법 선택 의사결정 트리

### 9.1 1단계: 정규성 확인

```
데이터 준비
    │
    ▼
Shapiro-Wilk 정규성 검정
    │
    ├── p ≥ 0.05 → 정규분포 가정 가능 → 모수 검정 고려
    │      (단, Q-Q 플롯으로 시각적 확인 병행)
    │
    └── p < 0.05 → 정규성 기각 → 비모수 검정 진행
```

### 9.2 2단계: 분석 목적에 따른 방법 선택

```
비모수 검정 진행
    │
    ├── [1] Feature 1개 → 중앙값 검정
    │     ├── 극소 표본 (n < 10) ──────→ 부호 검정 (Sign Test)
    │     ├── 편차 대칭 가정 가능 ────→ Wilcoxon 부호순위 검정
    │     └── 시계열/순서 데이터 ────→ 변곡점 분석 (6절)
    │
    ├── [2] Feature 2개 비교
    │     ├── 독립 표본 ──────────→ Mann-Whitney U 검정
    │     ├── 대응 표본 ──────────→ Wilcoxon 부호순위 (대응)
    │     └── 분포 형태 전체 비교 ──→ KS 검정
    │
    ├── [3] Feature 3개+ 비교
    │     ├── 독립 그룹 ──────────→ Kruskal-Wallis + Dunn 사후 검정
    │     └── 반복 측정 ──────────→ Friedman 검정
    │
    ├── [4] 상관관계 분석
    │     ├── 2변수, n ≥ 20 ─────→ Spearman ρ
    │     ├── 2변수, n < 20 ─────→ Kendall τ
    │     └── 다변수 ────────────→ 상관 매트릭스 (7.4절)
    │
    └── [5] 정합성 검증
          ├── 신뢰구간 추정 ─────→ Bootstrap CI
          ├── 그룹 차이 검증 ────→ Permutation Test
          └── 무작위성 확인 ─────→ Runs Test
```

---

## 10. 시나리오별 분석 워크플로

### 시나리오 A: A/B 테스트 (두 그룹 비교)

> **상황:** 서비스 변경 전후 사용자 체류 시간 비교 (n₁=12, n₂=15)

| 단계 | 분석 | 함수 |
|------|------|------|
| 1 | 각 그룹의 비모수 기술 통계 | `robust_descriptive()` |
| 2 | 각 그룹 정규성 검정 | `test_normality()` |
| 3 | 그룹 간 비교 | `mann_whitney_test()` |
| 4 | 효과 크기 확인 (r, CLES) | (함수 내 자동 계산) |
| 5 | Bootstrap으로 중앙값 차이 신뢰구간 | `bootstrap_ci()` |

### 시나리오 B: 사전-사후 효과 측정

> **상황:** 교육 프로그램 참여 전후 점수 비교 (n=10, 동일 대상)

| 단계 | 분석 | 함수 |
|------|------|------|
| 1 | 차이값(사후-사전) 기술 통계 | `robust_descriptive()` |
| 2 | 차이값 정규성 검정 | `test_normality()` |
| 3 | 사전-사후 비교 | `wilcoxon_paired_test()` |
| 4 | 차이의 Bootstrap 신뢰구간 | `bootstrap_ci()` |

### 시나리오 C: 시계열 패턴 탐지

> **상황:** 월별 매출 데이터에서 구조적 변화 시점 파악 (n=60)

| 단계 | 분석 | 함수 |
|------|------|------|
| 1 | 기술 통계 + 추세 확인 | `robust_descriptive()` |
| 2 | 무작위성 검정 | `runs_test_analysis()` |
| 3 | 변곡점 탐지 (PELT) | `detect_changepoints_pelt()` |
| 4 | 변곡점 검증 (순위 기반) | `rank_based_changepoint()` |
| 5 | 구간별 분포 차이 검정 | `mann_whitney_test()` |

### 시나리오 D: 다중 그룹 비교

> **상황:** 3개 지역의 만족도 점수 비교 (순서형 5점 척도)

| 단계 | 분석 | 함수 |
|------|------|------|
| 1 | 그룹별 기술 통계 | `robust_descriptive()` |
| 2 | 전체 그룹 비교 | `kruskal_wallis_test()` |
| 3 | 사후 검정 (유의 시) | (함수 내 Dunn 자동 실행) |
| 4 | 효과 크기 η² 확인 | (함수 내 자동 계산) |

### 시나리오 E: 다변수 상관관계 탐색

> **상황:** 5개 변수 간의 비선형 관계 탐색

| 단계 | 분석 | 함수 |
|------|------|------|
| 1 | 각 변수 기술 통계 + 정규성 | `robust_descriptive()`, `test_normality()` |
| 2 | 상관 매트릭스 생성 | `correlation_matrix_nonparametric()` |
| 3 | 주요 쌍별 상세 분석 | `spearman_correlation()` 또는 `kendall_correlation()` |
| 4 | 상관계수 Bootstrap CI | `bootstrap_ci()` |

---

## 11. Jupyter Notebook 생성 가이드

### 11.1 노트북 구조

```
📓 nonparametric_analysis.ipynb
├── 🔧 Cell 1: 환경 설정 + 모든 함수 정의
├── 📊 Cell 2: 데이터 로드 또는 샘플 생성
├── 📋 Cell 3: 기술 통계 + 정규성 검정
├── 🔬 Cell 4-N: 분석 실행 (시나리오에 맞게 선택)
└── 📝 Cell N+1: 결과 종합 리포트
```

### 11.2 노트북 자동 생성 스크립트

```python
# generate_notebook.py
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata.kernelspec = {
    "display_name": "Python 3", "language": "python", "name": "python3"
}

cells = []

# 헤더
cells.append(nbf.v4.new_markdown_cell(
    "# 비모수 통계 분석 실습 노트북\n"
    "이 노트북은 '비모수 데이터 통계 분석 가이드'의 모든 분석 함수를 포함합니다.\n---"
))

# 환경 설정 + 유틸리티 함수
cells.append(nbf.v4.new_code_cell(
    "# === 환경 설정 ===\n"
    "import numpy as np\n"
    "import pandas as pd\n"
    "from scipy import stats\n"
    "from scipy.stats import *\n"
    "import scikit_posthocs as sp\n"
    "import ruptures as rpt\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n\n"
    "plt.rcParams['font.family'] = 'AppleGothic'\n"
    "plt.rcParams['axes.unicode_minus'] = False\n"
    "sns.set_theme(style='whitegrid', font='AppleGothic')\n"
    "print('✅ 환경 설정 완료')\n\n"
    "# === 가이드 문서의 모든 함수를 여기에 붙여넣기 ===\n"
    "# interpret_p_value(), effect_size_r(), robust_descriptive(),\n"
    "# test_normality(), sign_test(), wilcoxon_one_sample(),\n"
    "# mann_whitney_test(), wilcoxon_paired_test(), ks_test(),\n"
    "# kruskal_wallis_test(), friedman_test(),\n"
    "# detect_changepoints_pelt(), rank_based_changepoint(),\n"
    "# spearman_correlation(), kendall_correlation(), correlation_matrix_nonparametric(),\n"
    "# bootstrap_ci(), permutation_test(), runs_test_analysis()"
))

# 샘플 데이터
cells.append(nbf.v4.new_markdown_cell("## 1. 데이터 준비"))
cells.append(nbf.v4.new_code_cell(
    "# === 샘플 데이터 (실제 분석 시 CSV 로드로 교체) ===\n"
    "np.random.seed(42)\n\n"
    "# 단일 Feature (비정규 분포)\n"
    "feature_a = np.random.exponential(scale=5, size=20)\n\n"
    "# 독립 두 그룹\n"
    "group1 = np.random.exponential(scale=3, size=15)\n"
    "group2 = np.random.exponential(scale=6, size=18)\n\n"
    "# 대응 표본\n"
    "before = np.random.uniform(10, 30, size=12)\n"
    "after = before + np.random.normal(3, 2, size=12)\n\n"
    "# 다중 그룹\n"
    "groups = [np.random.exponential(s, 15) for s in [3, 5, 8]]\n\n"
    "# 시계열 (변곡점 포함)\n"
    "ts = np.concatenate([np.random.normal(10,2,30), np.random.normal(20,2,30), np.random.normal(12,3,30)])\n\n"
    "# 상관분석용\n"
    "x = np.random.uniform(0, 100, 25)\n"
    "y = 2*x + np.random.normal(0, 20, 25)\n\n"
    "print('데이터 준비 완료')"
))

# 분석 셀들
analyses = [
    ("## 2. 기술 통계 + 정규성 검정", "print(robust_descriptive(feature_a, 'Feature_A'))\ntest_normality(feature_a, 'Feature_A')"),
    ("## 3. 단일 표본 검정", "wilcoxon_one_sample(feature_a, hypothesized_median=5, name='Feature_A')"),
    ("## 4. 독립 두 그룹 비교", "mann_whitney_test(group1, group2, '그룹1', '그룹2')"),
    ("## 5. 대응 표본 비교", "wilcoxon_paired_test(before, after, '실험')"),
    ("## 6. 다중 그룹 비교", "kruskal_wallis_test(*groups, group_names=['Low','Mid','High'])"),
    ("## 7. 변곡점 분석", "detect_changepoints_pelt(ts, name='시계열')"),
    ("## 8. 상관성 분석", "spearman_correlation(x, y, 'X', 'Y')"),
    ("## 9. Bootstrap 신뢰구간", "bootstrap_ci(feature_a, name='Feature_A 중앙값')"),
    ("## 10. 런 검정", "runs_test_analysis(ts, '시계열')"),
]

for title, code in analyses:
    cells.append(nbf.v4.new_markdown_cell(title))
    cells.append(nbf.v4.new_code_cell(code))

# 결과 종합
cells.append(nbf.v4.new_markdown_cell("## 📊 분석 결과 종합 리포트"))
cells.append(nbf.v4.new_code_cell(
    "print('='*60)\n"
    "print('       비모수 통계 분석 결과 종합')\n"
    "print('='*60)\n"
    "print('\\n위 각 셀의 결과를 종합하여 보고서를 작성하세요.')\n"
    "print('각 분석의 보고서 작성 템플릿은 가이드 문서를 참조하세요.')"
))

nb.cells = cells
nbf.write(nb, 'nonparametric_analysis.ipynb')
print("✅ 노트북 생성: nonparametric_analysis.ipynb")
```

---

## 12. 부록: 분석 방법 요약표

| 분석 목적 | 방법 | 함수명 | H₀ (귀무가설) | 효과 크기 |
|-----------|------|--------|---------------|-----------|
| 정규성 확인 | Shapiro-Wilk | `test_normality()` | 정규분포를 따른다 | W |
| 중앙값 = θ₀ | 부호 검정 | `sign_test()` | 중앙값이 θ₀와 같다 | — |
| 중앙값 = θ₀ | Wilcoxon 부호순위 | `wilcoxon_one_sample()` | 중앙값이 θ₀와 같다 | r |
| 2그룹 독립 | Mann-Whitney U | `mann_whitney_test()` | 두 분포가 같다 | r, CLES |
| 2그룹 대응 | Wilcoxon (대응) | `wilcoxon_paired_test()` | 차이가 없다 | r |
| 분포 비교 | KS 검정 | `ks_test()` | 두 분포가 동일 | D |
| 3+그룹 독립 | Kruskal-Wallis | `kruskal_wallis_test()` | 모든 분포가 같다 | η² |
| 3+그룹 대응 | Friedman | `friedman_test()` | 모든 조건이 같다 | W |
| 변곡점 탐지 | PELT | `detect_changepoints_pelt()` | 변곡점 없다 | — |
| 변곡점 탐지 | 순위 기반 | `rank_based_changepoint()` | 인접 분포가 같다 | — |
| 2변수 상관 | Spearman | `spearman_correlation()` | 무상관 | ρ |
| 2변수 상관 | Kendall τ | `kendall_correlation()` | 무상관 | τ |
| 다변수 상관 | 상관 매트릭스 | `correlation_matrix_nonparametric()` | 무상관 | ρ/τ |
| 신뢰구간 | Bootstrap | `bootstrap_ci()` | — | SE |
| 차이 검증 | 순열 검정 | `permutation_test()` | 차이 없다 | — |
| 무작위성 | 런 검정 | `runs_test_analysis()` | 무작위적 | Z |

---

> **참고:** 이 가이드의 모든 함수를 `nonparametric_utils.py`로 저장하면 노트북에서 `from nonparametric_utils import *`로 일괄 import 가능합니다.
