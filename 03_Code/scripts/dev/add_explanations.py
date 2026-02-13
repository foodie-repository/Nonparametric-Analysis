import json
from pathlib import Path

nb_path = Path("04_Notebooks/nonparametric_analysis_template.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Define explanation markdown cells
intro_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 비모수 분석 결과 해석 가이드\n",
        "\n",
        "이 노트북은 비모수 분석의 결과를 **통계 비전문가도 쉽게 이해할 수 있도록** 해설을 포함하고 있습니다.\n",
        "각 분석 단계마다 **'결과 해석 방법'**을 참고하세요.",
    ],
}

normality_expl = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 💡 결과 해석 (정규성 검정)\n",
        "- **목적**: 데이터가 '종 모양(Bell Curve)'의 일반적인 분포를 따르는지 확인합니다.\n",
        "- **Is Normal: True**: 데이터가 정규분포를 따릅니다. (일반적인 통계 분석 가능)\n",
        "- **Is Normal: False**: 데이터가 한쪽으로 치우치거나 특이한 분포입니다. **비모수 분석**이 필요합니다.",
    ],
}

mk_expl = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 💡 결과 해석 (추세 분석)\n",
        "- **Trend**: 데이터가 시간이 지남에 따라 **증가(increasing)**하는지 **감소(decreasing)**하는지 보여줍니다.\n",
        "- **Slope (기울기)**: 변화의 속도입니다. 양수(+)면 증가, 음수(-)면 감소 속도입니다.\n",
        "- **예시**: `no trend`가 나오면, 뚜렷한 상승/하락 경향이 없다는 뜻입니다.",
    ],
}

pettitt_expl = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 💡 결과 해석 (변곡점 탐지)\n",
        "- **Change Point**: 데이터의 흐름(평균 수준)이 **급격하게 바뀌는 시점**을 찾습니다.\n",
        "- 결과가 출력되면, 해당 시점(Index)을 기준으로 **전(Before)과 후(After)**의 데이터 양상이 달라졌다는 의미입니다.",
    ],
}

corr_expl = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 💡 결과 해석 (상관 분석)\n",
        "- 변수들 간의 밀접한 관계를 봅니다.\n",
        "- **p-value (표의 숫자)**:\n",
        "  - **0.05 미만 (초록색)**: 두 변수 간에 **의미 있는 관계**가 있습니다.\n",
        "  - **0.05 이상 (붉은색)**: 관계가 있다고 보기 어렵습니다 (우연일 가능성 높음).",
    ],
}

# Reconstruct notebook cells with explanations inserted
new_cells = []

# Header
new_cells.append(intro_md)

# Setup Code (Cell 1)
new_cells.append(nb["cells"][1])

# Load Data (Cell 2)
new_cells.append(nb["cells"][2])

# 1. Normality Section
new_cells.append(nb["cells"][3])  # Header "1. Normality Test"
new_cells.append(nb["cells"][4])  # Code
new_cells.append(normality_expl)  # Explanation

# 2. Trend Section
new_cells.append(nb["cells"][5])  # Header "2. Trend Analysis"
new_cells.append(nb["cells"][6])  # Code
new_cells.append(mk_expl)  # Explanation

# 3. Pettitt Section
new_cells.append(nb["cells"][7])  # Header "3. Change Point"
new_cells.append(nb["cells"][8])  # Code
new_cells.append(pettitt_expl)  # Explanation

# 4. Correlation Section
new_cells.append(nb["cells"][9])  # Header "4. Correlation"
new_cells.append(nb["cells"][10])  # Code
new_cells.append(corr_expl)  # Explanation

nb["cells"] = new_cells

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=4)
