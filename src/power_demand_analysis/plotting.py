"""matplotlib の共通設定。日本語ラベルを豆腐にしないための設定を含む。"""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt


def setup() -> None:
    """日本語フォントと既定のスタイルを適用する。"""
    matplotlib.rcParams["font.family"] = "IPAexGothic"
    matplotlib.rcParams["axes.unicode_minus"] = False  # マイナス記号の文字化け対策
    matplotlib.rcParams["figure.figsize"] = (10, 5)
    matplotlib.rcParams["figure.dpi"] = 110
    matplotlib.rcParams["axes.grid"] = True
    matplotlib.rcParams["grid.alpha"] = 0.3
    plt.style.use("seaborn-v0_8-whitegrid")
    matplotlib.rcParams["font.family"] = "IPAexGothic"  # style 適用で戻るため再設定
