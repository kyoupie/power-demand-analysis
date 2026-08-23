"""日本の暦に基づく平日／休日の判定。"""

from __future__ import annotations

import jpholiday
import numpy as np
import pandas as pd


def is_holiday(index: pd.DatetimeIndex) -> np.ndarray:
    """土日または日本の祝日なら True を返す。"""
    holiday = np.array([jpholiday.is_holiday(d) for d in index.date])
    return (index.dayofweek >= 5) | holiday
