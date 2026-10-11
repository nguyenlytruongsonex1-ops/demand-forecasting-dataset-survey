# Khảo sát dataset cho bài toán dự báo nhu cầu

Khảo sát và so sánh ba dataset công khai (UCI Bike Sharing, M5, FreshRetailNet-50K) để chọn dữ liệu cho đề tài dự báo nhu cầu bằng học máy và học sâu. Repo chỉ chứa tài liệu, không chứa dữ liệu gốc.

Bản đầy đủ: [Khao_sat_dataset_du_bao_nhu_cau.pdf](Khao_sat_dataset_du_bao_nhu_cau.pdf) (nguồn Markdown: [docs/Khao_sat_dataset_du_bao_nhu_cau.md](docs/Khao_sat_dataset_du_bao_nhu_cau.md)).

## Ba dataset

### 1. UCI Bike Sharing — một chuỗi theo giờ, có xu hướng
- Một chuỗi lượt thuê xe đạp theo giờ, 2 năm 2011–2012.
- Có thời tiết và lịch; trung bình mỗi giờ tăng khoảng 63% giữa hai năm.
- Dùng để kiểm tra độ bền vững khi phân phối thay đổi theo thời gian trên một chuỗi đơn.

### 2. M5 (Walmart) — nhiều chuỗi theo ngày, dài hạn, phân cấp
- 30,490 chuỗi sản phẩm × cửa hàng, 1,941 ngày có nhãn công khai.
- Phân cấp 12 cấp; có giá, sự kiện và SNAP.
- Dùng để kiểm tra khả năng mở rộng, học giữa nhiều chuỗi và độ ổn định dài hạn.

### 3. FreshRetailNet-50K — nhiều chuỗi ngắn, có stockout
- Nhiều chuỗi cửa hàng × sản phẩm.
- Khoảng 90 ngày train và 7 ngày đánh giá.
- Có thông tin bán hàng theo giờ và trạng thái hết hàng.
- Dùng để kiểm tra mô hình trên lịch sử ngắn và dữ liệu nhu cầu bị kiểm duyệt.

## Ma trận so sánh

| Góc nhìn | Bike Sharing | M5 | FreshRetailNet-50K |
|---|---|---|---|
| Tần suất | Giờ | Ngày | Ngày (có hồ sơ giờ) |
| Số chuỗi | 1 | 30,490 (42,840 khi tính phân cấp) | 50,000 |
| Độ dài lịch sử | 2 năm | Khoảng 5.4 năm | 97 ngày (90 train + 7 eval) |
| Độ thưa / số 0 | Không có số 0 | Cao, gián đoạn | Thấp (4.46% số ngày bằng 0) |
| Biến ngoại sinh | Thời tiết, lịch | Giá, sự kiện, SNAP | Khuyến mãi, thời tiết, cờ hoạt động |
| Phân cấp | Không | 12 cấp | Thành phố > cửa hàng; 5 cấp sản phẩm |
| Xu hướng / dịch chuyển | Rõ (+63.2% trung bình `cnt` mỗi giờ) | Chưa đo | Không đánh giá được dài hạn |
| Nhu cầu bị kiểm duyệt | Không | Không có nhãn | Có nhãn hết hàng theo giờ |
| Benchmark công bố | Không có chuẩn chung | Bảng xếp hạng, WRMSSE | TFT, WAPE Overall 31.75% → 29.02% (chỉ giai đoạn còn hàng) |
| Chi phí tính toán | Thấp | Cao (cần lấy mẫu con) | Trung bình |
| Giấy phép | CC BY 4.0 | Phi thương mại | CC BY 4.0 |

## Khung phương pháp dự kiến

![Khung phương pháp dự kiến](figures/khung_phuong_phap.png)

Mọi mô hình dùng chung cách chia theo thời gian, đặc trưng và cửa sổ đánh giá; kết quả báo cáo qua nhiều seed, kèm kiểm định thống kê.

## Nguồn dữ liệu và giấy phép

| Dataset | Link | Giấy phép |
|---|---|---|
| UCI Bike Sharing | https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset | CC BY 4.0 |
| M5 Forecasting – Accuracy | https://www.kaggle.com/competitions/m5-forecasting-accuracy | Theo quy định cuộc thi: chỉ dùng phi thương mại, không phân phối lại |
| FreshRetailNet-50K | https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K | CC BY 4.0 |

## Tài liệu tham khảo

1. H. Fanaee-T and J. Gama, "Event labeling combining ensemble detectors and background knowledge," *Progress in Artificial Intelligence*, vol. 2, no. 2–3, pp. 113–127, Jun. 2014, doi: 10.1007/s13748-013-0040-3.
2. S. Makridakis, E. Spiliotis, and V. Assimakopoulos, "M5 accuracy competition: Results, findings, and conclusions," *International Journal of Forecasting*, vol. 38, no. 4, pp. 1346–1364, 2022, doi: 10.1016/j.ijforecast.2021.11.013.
3. Y. Wang et al., "FreshRetailNet-50K: A stockout-annotated censored demand dataset for latent demand recovery and forecasting in fresh retail," arXiv:2505.16319v5, 2025.

Danh mục đầy đủ (8 tài liệu) nằm trong file PDF.

Tác giả: Nguyễn Lý Trường Sơn, 11/10/2026.
