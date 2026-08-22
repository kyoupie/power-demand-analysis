import pandas as pd
import pytest

from power_demand_analysis.load import load_all


@pytest.fixture(scope="module")
def df():
    return load_all()


def test_行数が2年分ある(df):
    assert len(df) == 8760 + 8784


def test_インデックスが日時型(df):
    assert isinstance(df.index, pd.DatetimeIndex)


def test_時系列が昇順(df):
    assert df.index.is_monotonic_increasing


def test_重複なし(df):
    assert df.index.duplicated().sum() == 0


def test_欠損なし(df):
    assert df.isna().sum().sum() == 0


def test_1時間刻みで穴がない(df):
    s = df.index.to_series()
    d = s.diff()
    d = d.dropna()
    gaps = d[d != pd.Timedelta(hours=1)]

    assert gaps.empty, f"1時間でない箇所: {gaps}"
