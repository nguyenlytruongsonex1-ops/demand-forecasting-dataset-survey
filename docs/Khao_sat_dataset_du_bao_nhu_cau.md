# Khảo sát dataset cho bài toán dự báo nhu cầu

Nguyễn Lý Trường Sơn, 11/10/2026.

## 1. Thông tin dataset

| Trường | UCI Bike Sharing (giờ) | M5 Forecasting – Accuracy | FreshRetailNet-50K |
|---|---|---|---|
| Nguồn / link | UCI, dataset 275, DOI 10.24432/C5W894 [1][2] | Kaggle [3]; Competitors' Guide [4]; IJF [5] | Hugging Face `Dingdong-Inc/FreshRetailNet-50K` [6]; arXiv:2505.16319 [7] |
| Lĩnh vực / bài toán | Lượt thuê xe đạp mỗi giờ (Washington D.C.) | Doanh số đơn vị hằng ngày của Walmart | Doanh số hàng tươi sống, có nhãn hết hàng theo giờ |
| Số mẫu | 1 chuỗi, 17,379 dòng (giờ), 2011–2012 | 30,490 chuỗi sản phẩm × cửa hàng (42,840 chuỗi trên 12 cấp) × 1,941 ngày có nhãn công khai [4][5] | 50,000 chuỗi cửa hàng × sản phẩm; 4,500,000 dòng train + 350,000 dòng eval [6]; 97 ngày (90 train + 7 eval) |
| Input dimension | 17 cột gốc; 12–13 cột dùng được sau khi loại ID và các cột rò rỉ | 3 file; sau khi ghép dạng dài: 22 cột (lịch, sự kiện, SNAP, giá, ID phân cấp; phép tính, dựa trên [4]) | 19 cột, trong đó 2 cột là mảng 24 giờ; 65 giá trị/dòng khi trải phẳng [6] |
| Target | `cnt` (số nguyên, 1–977) | Doanh số đơn vị/ngày; horizon 28 ngày [4] | `sale_amount` (số thực, đã nhân hệ số toàn cục) [6]; horizon 7 ngày [7] |
| Kiểu dữ liệu | Time series 1D, tần suất giờ | Nhiều chuỗi theo ngày, phân cấp | Nhiều chuỗi theo ngày, kèm hồ sơ giờ (ngày × 24) |
| Split | Không có split chính thức; đề xuất chia theo thời gian tại 2012-09-01 kèm rolling-origin | Chính thức: train d_1–d_1913, val d_1914–d_1941, test d_1942–d_1969 [5] | Chính thức: tách train/eval [6]; theo dữ liệu: train 2024-03-28 → 06-25 (90 ngày), eval 06-26 → 07-02 (7 ngày) |
| Kích thước | 1.1 MB [1] | 5 file CSV, 450.47 MB [3]; ma trận doanh số khoảng 118 MB (int16, ước tính) | 115 MB parquet [6] |
| Giấy phép | CC BY 4.0 [1] | Chỉ dùng phi thương mại, không phân phối lại [3] | CC BY 4.0 [6] |

**Vấn đề cần xử lý**

Bike Sharing:

- `casual` + `registered` = `cnt`, nên phải loại hai cột này để tránh rò rỉ.
- Trung bình `cnt` mỗi giờ tăng 63.2% (143.79 → 234.67) từ 2011 sang 2012, vì vậy bắt buộc chia theo thời gian.
- Thiếu 165 giờ; thời tiết đã chuẩn hóa về [0, 1] [1].

M5:

- Định dạng rộng (1,941 cột ngày); dạng dài có 59,181,090 dòng, tốn bộ nhớ.
- Chuỗi gián đoạn, nhiều số 0 [5]; cần tách số 0 thật khỏi giai đoạn trước khi mở bán [4].

FreshRetailNet-50K:

- Doanh số bị kiểm duyệt: 19.9% số giờ 6–22h (train) ở trạng thái hết hàng.
- `holiday_flag` là cờ ngày nghỉ: = 1 vào cuối tuần (25/26 ngày cuối tuần trong train; Chủ nhật 07/04 là ngày làm bù) và 6 ngày lễ chính thức của Trung Quốc rơi vào ngày thường (Thanh Minh, Lao động, Đoan Ngọ 2024) [7][8]; nên tách thêm biến thứ trong tuần.
- `discount` có giá trị 0 và > 1, trái quy ước [6].
- Lịch sử 97 ngày (90 train + 7 eval); doanh số đã chuẩn hóa. Bài báo ghi 863 SKU [7], thẻ dữ liệu và dữ liệu có 865 [6].

## 2. Ma trận so sánh góc nhìn

| Góc nhìn | Bike Sharing | M5 | FreshRetailNet-50K |
|---|---|---|---|
| Tần suất | Giờ | Ngày | Ngày (có hồ sơ giờ) |
| Quy mô / số chuỗi | 1 | 30,490 (42,840 khi tính phân cấp) | 50,000 |
| Độ dài lịch sử | 2 năm | Khoảng 5.4 năm | 97 ngày (90 train + 7 eval) |
| Độ thưa / số 0 | Không có số 0 | Cao, gián đoạn [5] | Thấp (4.46% số ngày bằng 0) |
| Biến ngoại sinh | Thời tiết, lịch | Giá, sự kiện, SNAP | Khuyến mãi, thời tiết, cờ hoạt động |
| Cấu trúc phân cấp | Không | 12 cấp [5] | Thành phố > cửa hàng; 5 cấp sản phẩm |
| Dịch chuyển phân phối / xu hướng | Rõ (+63.2% trung bình `cnt` mỗi giờ, 2012 so với 2011) | Chưa đo (lịch sử 5.4 năm) | Không đánh giá được dài hạn (97 ngày) |
| Nhu cầu bị kiểm duyệt | Không | Không có nhãn | Có nhãn theo giờ |
| Benchmark công bố | Không có chuẩn chung | Bảng xếp hạng, WRMSSE [5] | TFT, WAPE nhóm Overall: 31.75% (doanh số thô) → 29.02% (nhu cầu khôi phục bằng TimesNet); chỉ đánh giá trên giai đoạn còn hàng [7, Bảng 3] |
| Tính mới | Thấp | Thấp | Cao (công bố 2025) |
| Chi phí tính toán | Thấp | Cao (cần lấy mẫu con) | Trung bình (tập con 1,000 chuỗi: khoảng 14–20 phút trên 8 CPU; toàn bộ 50,000 chuỗi cần nhiều hơn) |
| Giấy phép | CC BY 4.0 | Phi thương mại | CC BY 4.0 |

Ba dataset bổ sung nhau về tần suất, quy mô và dạng sai lệch của dữ liệu (xu hướng, gián đoạn, kiểm duyệt).

## 3. Đánh giá độ phù hợp

Thang đánh giá: Đạt / Đạt một phần / Hạn chế.

| Tiêu chí | Bike | M5 | FreshRetailNet |
|---|---|---|---|
| Số lượng mẫu | Đạt một phần (1 chuỗi) | Đạt | Đạt |
| Input dimension | Đạt một phần (ít đặc trưng) | Đạt | Đạt |
| Kiểu dữ liệu time series | Đạt | Đạt | Đạt |
| Bài toán hồi quy / dự báo | Đạt | Đạt | Đạt |
| Đủ cấu trúc cho học sâu khai thác | Hạn chế (1 chuỗi, ít chiều) | Đạt một phần (đủ cấu trúc, chi phí cao) | Đạt |
| Khả thi trên CPU/Colab | Đạt | Hạn chế (bắt buộc lấy mẫu con) | Đạt một phần (tập con 1,000 chuỗi khả thi; toàn bộ cần thêm tài nguyên) |
| Giấy phép, trích dẫn | Đạt | Đạt một phần (phi thương mại) | Đạt (bài báo chưa bình duyệt) |
| Benchmark | Hạn chế | Đạt | Đạt một phần |
| Tính mới | Hạn chế | Hạn chế | Đạt |

**Kết luận.** FreshRetailNet-50K làm dataset chính; M5 làm kiểm chứng; Bike Sharing làm đối chứng một chuỗi.

**Phương án đề xuất:** cả ba dataset dùng cùng một câu hỏi nghiên cứu. FreshRetailNet-50K được phân tích sâu (ablation, nhiều seed, kiểm định thống kê). M5 (lấy mẫu con) và Bike Sharing chỉ chạy cấu hình chính để kiểm chứng kết luận.

## 4. Khung phương pháp dự kiến

![Khung phương pháp dự kiến](../figures/khung_phuong_phap.png)

Mọi mô hình dùng chung cách chia theo thời gian, đặc trưng và cửa sổ đánh giá; kết quả báo cáo qua nhiều seed, kèm kiểm định thống kê.

## Tài liệu tham khảo

[1] H. Fanaee-T, "Bike Sharing," UCI Machine Learning Repository, 2013, doi: 10.24432/C5W894. [Online]. Available: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset. [Accessed: Oct. 11, 2026].

[2] H. Fanaee-T and J. Gama, "Event labeling combining ensemble detectors and background knowledge," *Progress in Artificial Intelligence*, vol. 2, no. 2–3, pp. 113–127, Jun. 2014 (published online Nov. 2013), doi: 10.1007/s13748-013-0040-3.

[3] A. Howard, inversion, S. Makridakis, and vangelis, "M5 Forecasting - Accuracy," Kaggle, 2020. [Online]. Available: https://www.kaggle.com/competitions/m5-forecasting-accuracy (Data: https://www.kaggle.com/competitions/m5-forecasting-accuracy/data; Rules: https://www.kaggle.com/competitions/m5-forecasting-accuracy/rules). [Accessed: Oct. 11, 2026].

[4] University of Nicosia (MOFC), "The M5 competition: Competitors' guide," 2020. [Online]. Available: https://github.com/Mcompetitions/M5-methods/blob/master/M5-Competitors-Guide.pdf. [Accessed: Oct. 11, 2026].

[5] S. Makridakis, E. Spiliotis, and V. Assimakopoulos, "M5 accuracy competition: Results, findings, and conclusions," *International Journal of Forecasting*, vol. 38, no. 4, pp. 1346–1364, 2022, doi: 10.1016/j.ijforecast.2021.11.013.

[6] Dingdong-Inc, "FreshRetailNet-50K," Hugging Face dataset card, v1.0, 2025. [Online]. Available: https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K. [Accessed: Oct. 11, 2026].

[7] Y. Wang, J. Gu, L. Long, X. Li, L. Shen, Z. Fu, X. Zhou, and X. Jiang, "FreshRetailNet-50K: A stockout-annotated censored demand dataset for latent demand recovery and forecasting in fresh retail," arXiv:2505.16319v5 [cs.LG], 2025. [Online]. Available: https://arxiv.org/abs/2505.16319. [Accessed: Oct. 11, 2026].

[8] General Office of the State Council of the People's Republic of China, "国务院办公厅关于2024年部分节假日安排的通知 (Notice on the arrangement of certain holidays in 2024)," Guo Ban Fa Ming Dian [2023] No. 7, Oct. 25, 2023. [Online]. Available: https://www.gov.cn/zhengce/content/202310/content_6911527.htm. [Accessed: Oct. 11, 2026].
