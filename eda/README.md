# EDA 2 bộ dữ liệu chuỗi thời gian (bản nhẹ, chạy CPU)

Notebook EDA tiếng Việt để có cái nhìn tổng quan trước khi xử lý: mô tả nguồn/license, shape, kiểu, khoảng thời gian, thống kê mô tả, giá trị thiếu và bước thời gian thiếu, trùng lặp, phân phối và độ lệch (skewness, kurtosis), outlier, xu hướng/mùa vụ (resample, STL), ACF/PACF, kiểm định dừng ADF/KPSS, tương quan biến ngoại sinh. Các câu "Nhận xét" được in ra từ số liệu tính trong notebook, không gõ tay.

## Cấu trúc
```
notebooks/eda_01_bike_sharing.ipynb        UCI Bike Sharing (theo giờ)
notebooks/eda_02_beijing_pm25.ipynb        Beijing PM2.5 (theo giờ)
notebooks/eda_03_so_sanh_va_tien_xu_ly.ipynb  Bảng so sánh 2 bộ + gợi ý tiền xử lý
src/eda_utils.py          Hàm dùng chung (thiếu/trùng, skew, IQR, STL, ADF/KPSS)
scripts/download_data.py  Tải dữ liệu gốc vào data/raw/
scripts/build_notebooks.py  Sinh lại các notebook từ mã nguồn
reports/summary_*.json    Số liệu tóm tắt do notebook 01–02 sinh ra
```

## Cách chạy
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py          # tải vào data/raw/ (không được commit)
cd notebooks
for f in eda_0*.ipynb; do jupyter nbconvert --to notebook --execute --inplace $f; done
```
Chạy 01–02 trước 03. Cả 3 notebook chạy trên CPU hết khoảng 1 phút.

## Nguồn, license
| Bộ | Nguồn | License |
|---|---|---|
| UCI Bike Sharing | https://archive.ics.uci.edu/dataset/275 | CC BY 4.0 |
| Beijing PM2.5 | https://archive.ics.uci.edu/dataset/381 | CC BY 4.0 |

Thư mục `data/` nằm trong `.gitignore`; repo không chứa dữ liệu.

## BibTeX
```bibtex
@article{fanaee2014event, title={Event labeling combining ensemble detectors and background knowledge}, author={Fanaee-T, Hadi and Gama, Joao}, journal={Progress in Artificial Intelligence}, volume={2}, number={2-3}, pages={113--127}, year={2014}, doi={10.1007/s13748-013-0040-3}}
@article{liang2015pm25, title={Assessing Beijing's PM2.5 pollution: severity, weather impact, APEC and winter heating}, author={Liang, Xuan and Zou, Tao and Guo, Bin and Li, Shuo and Zhang, Haozhe and Zhang, Shuyi and Huang, Hui and Chen, Song Xi}, journal={Proceedings of the Royal Society A}, volume={471}, number={2182}, pages={20150257}, year={2015}, doi={10.1098/rspa.2015.0257}}
```
