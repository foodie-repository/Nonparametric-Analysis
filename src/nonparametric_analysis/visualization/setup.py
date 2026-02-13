"""Visualization setup and helpers."""

import matplotlib.pyplot as plt
import seaborn as sns
import platform


def setup_visualization():
    """Configure matplotlib and seaborn style and fonts."""
    import matplotlib.font_manager as fm

    system_name = platform.system()

    # Font configuration with fallback
    if system_name == "Darwin":
        # macOS에서 사용 가능한 한글 폰트 찾기
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        korean_fonts = [
            "AppleSDGothicNeo-Regular",
            "AppleGothic",
            "Arial Unicode MS",
            "Nanum Gothic",
            "NanumGothic"
        ]
        font_family = None
        for font in korean_fonts:
            if font in available_fonts:
                font_family = font
                break
        if font_family is None:
            font_family = "sans-serif"
            print("경고: 한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
    elif system_name == "Windows":
        font_family = "Malgun Gothic"
    else:
        font_family = "NanumGothic"  # Linux fallback

    plt.rcParams["font.family"] = font_family
    plt.rcParams["axes.unicode_minus"] = False

    # Seaborn theme
    sns.set_theme(style="whitegrid", font=font_family)

    # Optional: Improve resolution for retina displays
    try:
        from IPython.display import set_matplotlib_formats
        set_matplotlib_formats("retina")
    except ImportError:
        pass
