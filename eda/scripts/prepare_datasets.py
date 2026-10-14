"""Chuẩn bị hai dataset time series cho thí nghiệm forecasting.

- Tải dữ liệu trước bằng download_data.py.
- Split theo thời gian 70/15/15.
- Chỉ fit mean/std trên train.
- Không đưa các cột là thành phần của target vào input Bike Sharing.
- Kết quả được ghi vào eda/data/processed/ (đã nằm trong .gitignore).

Chạy từ thư mục eda:
    python scripts/prepare_datasets.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"


def split_time(df: pd.DataFrame, time_col: str):
    df = df.sort_values(time_col).reset_index(drop=True)
    n = len(df)
    i_train = int(n * 0.70)
    i_val = int(n * 0.85)
    return (
        df.iloc[:i_train].copy(),
        df.iloc[i_train:i_val].copy(),
        df.iloc[i_val:].copy(),
    )


def add_time_features(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    out = df.copy()
    t = pd.to_datetime(out[time_col])
    out["hour"] = t.dt.hour
    out["dayofweek"] = t.dt.dayofweek
    out["month"] = t.dt.month
    out["hour_sin"] = np.sin(2 * np.pi * out["hour"] / 24)
    out["hour_cos"] = np.cos(2 * np.pi * out["hour"] / 24)
    out["dow_sin"] = np.sin(2 * np.pi * out["dayofweek"] / 7)
    out["dow_cos"] = np.cos(2 * np.pi * out["dayofweek"] / 7)
    return out


def scale_from_train(parts, columns):
    train, valid, test = parts
    mean = train[columns].mean()
    std = train[columns].std().replace(0, 1).fillna(1)
    scaled = []
    for part in parts:
        p = part.copy()
        p[columns] = (p[columns] - mean) / std
        scaled.append(p)
    return scaled, mean.to_dict(), std.to_dict()


def save_parts(name, parts, metadata):
    for split_name, part in zip(("train", "valid", "test"), parts):
        part.to_csv(OUT / f"{name}_{split_name}.csv", index=False)
    (OUT / f"{name}_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )


def prepare_bike():
    df = pd.read_csv(RAW / "hour.csv")
    df["timestamp"] = pd.to_datetime(df["dteday"]) + pd.to_timedelta(df["hr"], unit="h")
    # instant is an index; casual and registered sum to cnt and cause target leakage.
    df = df.drop(columns=["instant", "casual", "registered"])
    df = add_time_features(df, "timestamp")
    train, valid, test = split_time(df, "timestamp")
    scale_cols = ["temp", "atemp", "hum", "windspeed"]
    parts, mean, std = scale_from_train((train, valid, test), scale_cols)
    metadata = {
        "dataset": "UCI Bike Sharing",
        "target": "cnt",
        "removed_columns": ["instant", "casual", "registered"],
        "split_ratio": {"train": 0.70, "valid": 0.15, "test": 0.15},
        "rows": {name: len(part) for name, part in zip(("train", "valid", "test"), parts)},
        "time_range": {
            name: {"start": part.timestamp.iloc[0], "end": part.timestamp.iloc[-1]}
            for name, part in zip(("train", "valid", "test"), parts)
        },
        "scaled_columns": scale_cols,
        "train_mean": mean,
        "train_std": std,
    }
    save_parts("bike", parts, metadata)


def prepare_tetouan():
    df = pd.read_csv(RAW / "Tetuan City power consumption.csv")
    df["timestamp"] = pd.to_datetime(df.pop("DateTime"))
    targets = [
        "Zone 1 Power Consumption",
        "Zone 2  Power Consumption",
        "Zone 3  Power Consumption",
    ]
    df = add_time_features(df, "timestamp")
    train, valid, test = split_time(df, "timestamp")
    scale_cols = [
        "Temperature",
        "Humidity",
        "Wind Speed",
        "general diffuse flows",
        "diffuse flows",
        *targets,
    ]
    parts, mean, std = scale_from_train((train, valid, test), scale_cols)
    metadata = {
        "dataset": "Power Consumption of Tetouan City",
        "targets": targets,
        "split_ratio": {"train": 0.70, "valid": 0.15, "test": 0.15},
        "rows": {name: len(part) for name, part in zip(("train", "valid", "test"), parts)},
        "time_range": {
            name: {"start": part.timestamp.iloc[0], "end": part.timestamp.iloc[-1]}
            for name, part in zip(("train", "valid", "test"), parts)
        },
        "scaled_columns": scale_cols,
        "train_mean": mean,
        "train_std": std,
    }
    save_parts("tetouan", parts, metadata)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prepare_bike()
    prepare_tetouan()
    print(f"Đã ghi dữ liệu đã chuẩn bị vào {OUT}")


if __name__ == "__main__":
    main()
