# Dự báo nhu cầu: EDA và thực nghiệm PatchTST trên UCI Bike Sharing và Beijing PM2.5

Repo này tập trung vào **2 bộ chuỗi thời gian công khai, nhẹ, có trích dẫn**: UCI Bike Sharing (UCI 275) và Beijing PM2.5 (UCI 381). Nội dung gồm notebook EDA tiếng Việt đã chạy sẵn output, báo cáo tổng hợp và script tải dữ liệu từ nguồn gốc. Repo không chứa dữ liệu thô.

Báo cáo EDA đầy đủ: [Khao_sat_dataset_du_bao_nhu_cau.pdf](Khao_sat_dataset_du_bao_nhu_cau.pdf) (nguồn Markdown: [docs/Khao_sat_dataset_du_bao_nhu_cau.md](docs/Khao_sat_dataset_du_bao_nhu_cau.md)). Kết quả ablation PatchTST: [experiments/BAO_CAO_PATCHTST_BIKE.md](experiments/BAO_CAO_PATCHTST_BIKE.md).

## Tóm tắt nhanh

| | UCI Bike Sharing | Beijing PM2.5 |
|---|---|---|
| Nguồn | [UCI 275](https://archive.ics.uci.edu/dataset/275) | [UCI 381](https://archive.ics.uci.edu/dataset/381) |
| License | CC BY 4.0 | CC BY 4.0 |
| Số dòng (file giờ) | 17.379 | 43.824 |
| Tần suất, thời gian | Giờ, 2011-01-01 → 2012-12-31 | Giờ, 2010-01-01 → 2014-12-31 |
| Mục tiêu dự báo | `cnt` (lượt thuê xe mỗi giờ) | `pm2.5` (µg/m³) |
| Biến ngoại sinh | Thời tiết (temp, atemp, hum, windspeed, weathersit), lịch (hr, weekday, workingday, holiday, season) | Khí tượng (DEWP, TEMP, PRES), hướng gió `cbwd`, gió/tuyết/mưa cộng dồn (Iws, Is, Ir) |

**Bike Sharing: điểm EDA chính**
- Thiếu 165/17.544 giờ (0,94%), rải trên 76 ngày; không có NA trong ô, không có mốc trùng.
- `casual + registered = cnt` ở 100% dòng → **rò rỉ mục tiêu, phải bỏ hai cột này**.
- `cnt` lệch phải (skew 1,28, kurtosis 1,42); trung bình giờ năm 2012 cao hơn 2011 là 63,2% (143,8 → 234,7) → drift theo thời gian.
- Mùa vụ rõ: ngày làm việc đỉnh 8h (477) và 17h (525); ACF lag24 = 0,819, lag168 = 0,876.

**Beijing PM2.5: điểm EDA chính**
- Lưới giờ đầy đủ nhưng `pm2.5` thiếu 2.067 giá trị (4,72%), thành 214 đoạn, dài nhất 155 giờ; 24 giờ đầu toàn NA.
- Lệch phải nặng: skew 1,80, kurtosis 4,77; 4,25% giờ vượt ngưỡng IQR (>299) là các đợt ô nhiễm thật.
- Quán tính ngắn: ACF lag1 = 0,965 nhưng lag24 = 0,398, lag168 = 0,023; tháng 2 cao nhất (126), tháng 8 thấp nhất (80).
- Hướng gió quan trọng: trung bình 126 khi `cbwd = cv`, 70 khi gió NW; Spearman với Iws = −0,36.

## Thực nghiệm PatchTST

Thực nghiệm nhanh dùng UCI Bike Sharing, dự báo `cnt` 24 giờ từ 168 giờ trước. Có seasonal-naive làm baseline và so sánh ba biến thể: không LayerNorm, `Linear → LayerNorm` và `LayerNorm → Linear` ở patch projection. Kết quả trên 3 seed cho thấy `Linear → LayerNorm` tốt hơn rõ rệt `LayerNorm → Linear` trên mọi metric chính.

```bash
python3 eda/scripts/download_data.py
python3 experiments/run_patchtst_bike.py --epochs 15 --seeds 13 42 2026 --threads 2
```

## Cấu trúc repo
```
README.md
Khao_sat_dataset_du_bao_nhu_cau.pdf          Báo cáo tổng hợp (PDF)
docs/Khao_sat_dataset_du_bao_nhu_cau.md      Nguồn Markdown của báo cáo
eda/notebooks/eda_01_bike_sharing.ipynb      EDA Bike Sharing (đã chạy, có output)
eda/notebooks/eda_02_beijing_pm25.ipynb      EDA Beijing PM2.5
eda/notebooks/eda_03_so_sanh_va_tien_xu_ly.ipynb  So sánh 2 bộ + gợi ý tiền xử lý
eda/src/eda_utils.py                         Hàm dùng chung (thiếu/trùng, skew, IQR, STL, ADF/KPSS)
eda/scripts/download_data.py                 Tải dữ liệu gốc vào eda/data/raw/
eda/scripts/build_notebooks.py               Sinh lại notebook từ mã nguồn
eda/reports/summary_*.json                   Số liệu tóm tắt do notebook 01–02 sinh ra
experiments/run_patchtst_bike.py              Runner PatchTST và baseline CPU-friendly
experiments/BAO_CAO_PATCHTST_BIKE.md         Báo cáo kết quả ablation
experiments/results/                          CSV/JSON/log của lần chạy
eda/requirements.txt
```

## BibTeX
```bibtex
@article{fanaee2014event, title={Event labeling combining ensemble detectors and background knowledge}, author={Fanaee-T, Hadi and Gama, Joao}, journal={Progress in Artificial Intelligence}, volume={2}, number={2-3}, pages={113--127}, year={2014}, doi={10.1007/s13748-013-0040-3}}
@misc{bikesharing_uci, author={Fanaee-T, Hadi}, title={Bike Sharing}, publisher={UCI Machine Learning Repository}, year={2013}, doi={10.24432/C5W894}}
@article{liang2015pm25, title={Assessing Beijing's PM2.5 pollution: severity, weather impact, APEC and winter heating}, author={Liang, Xuan and Zou, Tao and Guo, Bin and Li, Shuo and Zhang, Haozhe and Zhang, Shuyi and Huang, Hui and Chen, Song Xi}, journal={Proceedings of the Royal Society A}, volume={471}, number={2182}, pages={20150257}, year={2015}, doi={10.1098/rspa.2015.0257}}
@misc{pm25_uci, author={Chen, Song}, title={Beijing PM2.5}, publisher={UCI Machine Learning Repository}, year={2015}, doi={10.24432/C5JS49}}
```

## Lịch sử
Bản khảo sát trước (6 bộ UCI cho TabM, FreshRetailNet-50K, M5) đã được thay bằng phạm vi 2 bộ hiện tại; xem lịch sử git trước commit này nếu cần.

Tác giả: Nguyễn Lý Trường Sơn.
