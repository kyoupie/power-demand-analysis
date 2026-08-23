import pandas as pd

from power_demand_analysis.calendar import is_holiday


def test_元日は休日():
    assert is_holiday(pd.to_datetime(["2024-01-01"]))[0]


def test_平日():
    assert is_holiday(pd.to_datetime(["2024-01-04"]))[0] == False


def test_土曜日():
    assert is_holiday(pd.to_datetime(["2024-01-06"]))[0]


def test_成人の日():
    assert is_holiday(pd.to_datetime(["2024-01-08"]))[0]
