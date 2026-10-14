# Dự báo nhu cầu: EDA cho UCI Bike Sharing và Tetouan City

Repository tập trung vào hai chuỗi thời gian công khai, nhẹ và có trích dẫn cho nghiên cứu dự báo nhu cầu/phụ tải:

1. **UCI Bike Sharing (UCI 275):** số lượt thuê xe theo giờ tại Washington DC.
2. **Power Consumption of Tetouan City (UCI 849):** phụ tải điện của ba vùng phân phối tại Tetouan, ghi nhận mỗi 10 phút.

Notebook EDA tiếng Việt đã được chạy lại và lưu output. Báo cáo tổng hợp ở [Khao_sat_dataset_du_bao_nhu_cau.pdf](Khao_sat_dataset_du_bao_nhu_cau.pdf), nguồn Markdown ở [docs/Khao_sat_dataset_du_bao_nhu_cau.md](docs/Khao_sat_dataset_du_bao_nhu_cau.md). Repository không phân phối dữ liệu thô; script sẽ tải trực tiếp từ UCI.

## Tóm tắt dataset

| | UCI Bike Sharing | Tetouan City Power Consumption |
|---|---|---|
| Nguồn | [UCI 275](https://archive.ics.uci.edu/dataset/275) | [UCI 849](https://archive.ics.uci.edu/dataset/849/power+consumption+of+tetouan+city) |
| License | CC BY 4.0 | CC BY 4.0 |
| Dữ liệu thực tế | 17.379 dòng theo giờ | 52.416 dòng mỗi 10 phút |
| Thời gian | 2011-01-01 → 2012-12-31 | 2017-01-01 → 2017-12-30 23:50 |
| Target | `cnt` — số lượt thuê xe | `Zone 1`, `Zone 2`, `Zone 3` — phụ tải điện |
| Ngoại sinh | Thời tiết và lịch | Thời tiết và bức xạ |
| Missing trong file | 0 NA; thiếu 165 mốc giờ trên lưới kỳ vọng | 0 NA; không thiếu mốc 10 phút |
| File tải về | khoảng 1,1 MB | khoảng 1,3 MB dạng nén |

## Kết quả EDA chính

### UCI Bike Sharing

- `cnt` có trung bình 189,5, skewness 1,28 và kurtosis 1,42; phân phối lệch phải.
- Có drift rõ: trung bình theo giờ năm 2012 cao hơn năm 2011 khoảng 63,2%.
- Mùa vụ ngày và tuần mạnh; ACF lag 24 = 0,819 và lag 168 = 0,876.
- `casual + registered = cnt` ở mọi dòng. Hai cột này phải được loại khỏi input để tránh rò rỉ target.
- Nên bỏ thêm `instant`, dựng lưới giờ đều, giữ outlier giờ cao điểm và chia train/test theo thời gian.

### Tetouan City Power Consumption

- Có ba target phụ tải với trung bình lần lượt khoảng 32.345, 21.043 và 17.835 theo đơn vị gốc.
- Zone 1, Zone 2, Zone 3 có skewness lần lượt 0,229; 0,329; 1,024.
- Sau khi lấy trung bình theo giờ, Zone 1 có ACF lag 24 = 0,963 và lag 168 = 0,953; mùa vụ ngày rất rõ.
- Ba target tương quan dương; tương quan Pearson giữa Zone 1 và Zone 2 là 0,835, giữa Zone 1 và Zone 3 là 0,751.
- Temperature, Humidity và general diffuse flows là các ngoại sinh liên quan mạnh nhất với Zone 1 theo Spearman.
- Có thể giữ tần suất 10 phút cho forecasting ngắn hạn hoặc resample về giờ để so sánh với Bike Sharing. Phải ghi rõ dùng trung bình hay tổng khi resample.

## Cấu trúc repository

```text
README.md
Khao_sat_dataset_du_bao_nhu_cau.pdf
docs/Khao_sat_dataset_du_bao_nhu_cau.md
eda/notebooks/eda_01_bike_sharing.ipynb
eda/notebooks/eda_02_tetouan_power.ipynb
eda/notebooks/eda_03_so_sanh_va_tien_xu_ly.ipynb
eda/reports/summary_bike.json
eda/reports/summary_tetouan.json
eda/scripts/download_data.py
eda/scripts/build_notebooks.py
eda/src/eda_utils.py
eda/requirements.txt
```

## Chạy lại EDA

```bash
cd eda
python scripts/download_data.py
python scripts/build_notebooks.py

jupyter nbconvert --to notebook --execute --inplace \
  notebooks/eda_01_bike_sharing.ipynb \
  --ExecutePreprocessor.timeout=600

jupyter nbconvert --to notebook --execute --inplace \
  notebooks/eda_02_tetouan_power.ipynb \
  --ExecutePreprocessor.timeout=600

jupyter nbconvert --to notebook --execute --inplace \
  notebooks/eda_03_so_sanh_va_tien_xu_ly.ipynb \
  --ExecutePreprocessor.timeout=600
```

## BibTeX

```bibtex
@article{fanaee2014event,
  title={Event labeling combining ensemble detectors and background knowledge},
  author={Fanaee-T, Hadi and Gama, Joao},
  journal={Progress in Artificial Intelligence},
  volume={2}, number={2-3}, pages={113--127}, year={2014},
  doi={10.1007/s13748-013-0040-3}
}

@misc{bikesharing_uci,
  author={Fanaee-T, Hadi}, title={Bike Sharing},
  publisher={UCI Machine Learning Repository}, year={2013},
  doi={10.24432/C5W894}
}

@inproceedings{salam2018tetouan,
  title={Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city},
  author={Salam, Abdulwahed and El Hibaoui, Abdelaaziz},
  booktitle={2018 6th International Renewable and Sustainable Energy Conference},
  year={2018}, doi={10.1109/IRSEC.2018.8703007}
}

@misc{tetouan_uci,
  author={Salam, Abdulwahed and El Hibaoui, Abdelaaziz},
  title={Power Consumption of Tetouan City},
  publisher={UCI Machine Learning Repository}, year={2023},
  doi={10.24432/C5B034}
}
```
