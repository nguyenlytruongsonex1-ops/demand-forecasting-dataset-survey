"""Tải 4 dataset từ nguồn gốc vào data/raw/ (không phân phối lại dữ liệu).
Chạy: python scripts/download_data.py
"""
import io, zipfile, pathlib, requests

RAW = pathlib.Path(__file__).resolve().parents[1] / "data" / "raw"
SOURCES = {
    # ETTm1 - CC BY-ND 4.0, chỉ tải bản gốc, KHÔNG commit/phân phối bản đã sửa
    "ETTm1.csv": ("https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small/ETTm1.csv", None),
    # Beijing PM2.5 - UCI 381, CC BY 4.0
    "PRSA_data_2010.1.1-2014.12.31.csv": ("https://archive.ics.uci.edu/static/public/381/beijing+pm2+5+data.zip", "zip"),
    # Tourism Monthly - Monash/Zenodo 4656096, CC BY 4.0
    "tourism_monthly_dataset.tsf": ("https://zenodo.org/records/4656096/files/tourism_monthly_dataset.zip?download=1", "zip"),
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
                    if m.endswith((".csv", ".tsf", ".txt")) and not m.startswith("__MACOSX"):
                        (RAW / pathlib.Path(m).name).write_bytes(z.read(m))
        else:
            (RAW / name).write_bytes(r.content)
        print(f"[xong] {name}")

if __name__ == "__main__":
    main()
