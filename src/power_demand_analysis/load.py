from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def load_power(year: int) -> pd.DataFrame:
    """powerのRawデータを読み込んで整理する。"""
    df = pd.read_csv(RAW_DIR / f"power_{year}.csv")
    df["datetime"] = df["DATE"] + " " + df["TIME"]

    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y/%m/%d %H:%M")

    df = df.set_index("datetime")

    df = df.drop(columns=["DATE", "TIME"])

    df = df.rename(columns={"実績(万kW)": "demand_10mw"})

    return df


def load_weather(year: int) -> pd.DataFrame:
    """weatherのRawデータを読み込んで整理する。"""
    df = pd.read_csv(RAW_DIR / f"weather_{year}.csv")

    df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%dT%H:%M")
    df = df.set_index("time")
    df = df.rename_axis("datetime")

    return df


def load_year(year: int) -> pd.DataFrame:
    """powerの加工済みデータにweatherの加工済みデータを結合する。"""
    power = load_power(year)
    weather = load_weather(year)

    return power.join(weather, how="outer")


def load_all(years: tuple[int, ...] = (2023, 2024)) -> pd.DataFrame:
    """年ごとの加工済みデータを縦に結合する。"""
    return pd.concat([load_year(year) for year in years]).sort_index()
