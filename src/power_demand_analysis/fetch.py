"""生データの取得。

電力需要は東京電力の公開 CSV、気温は Open-Meteo の過去気象 API から取得し、
data/raw/ に保存する。取得済みのファイルは再ダウンロードしない。
"""

from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import requests

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

TEPCO_URL = "https://www.tepco.co.jp/forecast/html/images/juyo-{year}.csv"
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"

# 東京（気象庁の東京管区気象台とほぼ同じ地点）
TOKYO_LAT, TOKYO_LON = 35.6895, 139.6917


def fetch_power_demand(year: int) -> Path:
    """東京電力の時間別需要実績を取得する。

    CSV は Shift_JIS で、先頭2行に更新日時と空行が入っているため読み飛ばす。
    """
    dest = RAW_DIR / f"power_{year}.csv"
    if dest.exists():
        print(f"  スキップ（取得済み）: {dest.name}")
        return dest

    res = requests.get(
        TEPCO_URL.format(year=year),
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=60,
    )
    res.raise_for_status()

    df = pd.read_csv(io.BytesIO(res.content), encoding="shift_jis", skiprows=2)
    dest.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dest, index=False, encoding="utf-8")
    print(f"  保存: {dest.name} ({len(df):,} 行)")
    return dest


def fetch_weather(year: int) -> Path:
    """Open-Meteo から東京の時間別気象データを取得する。"""
    dest = RAW_DIR / f"weather_{year}.csv"
    if dest.exists():
        print(f"  スキップ（取得済み）: {dest.name}")
        return dest

    res = requests.get(
        OPEN_METEO_URL,
        params={
            "latitude": TOKYO_LAT,
            "longitude": TOKYO_LON,
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "hourly": "temperature_2m,relative_humidity_2m,precipitation",
            "timezone": "Asia/Tokyo",
        },
        timeout=120,
    )
    res.raise_for_status()

    df = pd.DataFrame(res.json()["hourly"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dest, index=False, encoding="utf-8")
    print(f"  保存: {dest.name} ({len(df):,} 行)")
    return dest


def main() -> None:
    for year in (2023, 2024):
        print(f"[{year}]")
        fetch_power_demand(year)
        fetch_weather(year)


if __name__ == "__main__":
    main()
