"""Tải 2 dataset từ nguồn gốc vào data/raw/ (không phân phối lại dữ liệu).
Chạy: python scripts/download_data.py
"""
import io, pathlib, zipfile

import requests

RAW = pathlib.Path(__file__).resolve().parents[1] / "data" / "raw"
SOURCES = {
    # Power Consumption of Tetouan City - UCI 849, CC BY 4.0
    "Tetuan City power consumption.csv": ("https://archive.ics.uci.edu/static/public/849/power+consumption+of+tetouan+city.zip", "zip"),
    # UCI Bike Sharing - UCI 275, CC BY 4.0
    "hour.csv": ("https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip", "zip"),
}

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for name, (url, kind) in SOURCES.items():
        if (RAW / name).exists():
            print(f"[bỏ qua] {name} đã có"); continue
        print(f"[tải] {url}")
        r = requests.get(url, timeout=120); r.raise_for_status()
        if kind == "zip":
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                for m in z.namelist():
                    if m.endswith((".csv", ".txt")) and not m.startswith("__MACOSX"):
                        (RAW / pathlib.Path(m).name).write_bytes(z.read(m))
        else:
            (RAW / name).write_bytes(r.content)
        print(f"[xong] {name}")

if __name__ == "__main__":
    main()
