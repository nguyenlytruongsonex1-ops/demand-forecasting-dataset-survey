# Báo cáo EDA: UCI Bike Sharing và Beijing PM2.5

**Nguyễn Lý Trường Sơn, 14/10/2026**

## 1. Phạm vi và lý do chọn

Theo yêu cầu của thầy hướng dẫn, đề tài dùng **UCI Bike Sharing** và thêm một bộ chuỗi thời gian nhẹ, công khai, có trích dẫn. Bộ được chọn là **Beijing PM2.5**. Hai bộ thay cho M5 và FreshRetailNet-50K, vốn được đánh giá là quá nặng để nghiên cứu mô hình trên máy yếu.

- Cả hai đều là chuỗi theo giờ, có biến ngoại sinh, license CC BY 4.0 trên UCI, có paper gốc kèm DOI.
- Kích thước nhỏ (17.379 và 43.824 dòng); toàn bộ EDA chạy trên CPU trong khoảng 1 phút.
- Hai bộ bổ sung cho nhau: Bike có mùa vụ ngày/tuần mạnh và xu hướng tăng (drift); PM2.5 có thiếu dữ liệu theo đoạn, đuôi phải nặng và phụ thuộc mạnh vào thời tiết.

Mọi con số dưới đây lấy từ output của các notebook trong `eda/notebooks/`.

## 2. UCI Bike Sharing (UCI 275)

**Mô tả.** Số lượt thuê xe đạp mỗi giờ của hệ thống Capital Bikeshare (Washington DC), 2011-01-01 00:00 → 2012-12-31 23:00, file `hour.csv` có 17.379 dòng, 17 cột. Mục tiêu: `cnt`. Biến ngoại sinh: thời tiết (`temp`, `atemp`, `hum`, `windspeed`, `weathersit`, đã chuẩn hóa về [0,1] bởi nhà cung cấp) và lịch (`hr`, `weekday`, `workingday`, `holiday`, `season`, `mnth`, `yr`). Paper gốc: Fanaee-T & Gama (2014), Progress in Artificial Intelligence, DOI 10.1007/s13748-013-0040-3.

**Kết quả EDA chính.**

| Hạng mục | Kết quả |
|---|---|
| Giờ thiếu | 165/17.544 giờ (0,94%), rải trên 76 ngày; ngày thiếu nhiều nhất 2012-10-29 (23 giờ) |
| NA, trùng | 0 NA trong ô, 0 mốc trùng |
| Rò rỉ | `casual + registered = cnt` ở 100% dòng |
| Phân phối `cnt` | TB 189,5; trung vị 142; max 977; skew 1,28; kurtosis 1,42; log1p → skew −0,82 |
| Outlier (IQR 1,5) | 505 giờ (2,9%) vượt 642, chủ yếu giờ cao điểm thật |
| Xu hướng | TB/giờ 143,8 (2011) → 234,7 (2012), tăng 63,2% |
| Mùa vụ | Ngày làm việc: đỉnh 8h (477), 17h (525); ngày nghỉ: đỉnh 13h (373). STL period 24: độ mạnh mùa vụ 0,881 |
| ACF | lag1 0,843; lag24 0,819; lag168 0,876 |
| Kiểm định dừng | Chuỗi ngày không dừng (ADF p = 0,34); sai phân 1 lần thì dừng |
| Tương quan (Spearman) | hr 0,51; temp 0,42; atemp 0,42; hum −0,36; temp–atemp r = 0,988 |

## 3. Beijing PM2.5 (UCI 381)

**Mô tả.** Nồng độ PM2.5 mỗi giờ tại Đại sứ quán Mỹ ở Bắc Kinh, 2010-01-01 00:00 → 2014-12-31 23:00, 43.824 dòng, 13 cột. Mục tiêu: `pm2.5`. Biến ngoại sinh: điểm sương `DEWP`, nhiệt độ `TEMP`, áp suất `PRES`, hướng gió `cbwd`, tốc độ gió cộng dồn `Iws`, số giờ tuyết/mưa cộng dồn `Is`/`Ir`. Paper gốc: Liang et al. (2015), Proceedings of the Royal Society A 471:20150257, DOI 10.1098/rspa.2015.0257.

**Kết quả EDA chính.**

| Hạng mục | Kết quả |
|---|---|
| Lưới thời gian | Đầy đủ: 0 giờ thiếu, 0 mốc trùng |
| Thiếu ở mục tiêu | 2.067 giá trị (4,72%), 214 đoạn, dài nhất 155 giờ, trung vị 1 giờ; 24 giờ đầu toàn NA |
| Thiếu theo năm | 2010: 669; 2011: 728; 2012: 489; 2013: 82; 2014: 99 |
| Phân phối `pm2.5` | TB 98,6; trung vị 72; max 994; skew 1,80; kurtosis 4,77; log1p → skew −0,30 |
| Outlier (IQR 1,5) | 1.773 giờ (4,25%) vượt 299, là các đợt ô nhiễm thật |
| Biến thưa | Is > 0 ở 0,84% giờ, Ir > 0 ở 4,13% giờ; Iws skew 4,30 |
| Xu hướng, mùa vụ | TB năm 104,0 / 99,1 / 90,5 / 101,7 / 97,7, không có xu hướng đơn điệu; tháng 2 cao nhất (126), tháng 8 thấp nhất (80); theo giờ cao nhất 1h (114), thấp nhất 15h (86); STL period 24: mùa vụ 0,411; không thấy mùa vụ tuần |
| ACF | lag1 0,965; lag24 0,398; lag168 0,023 |
| Kiểm định dừng | ADF và KPSS cùng kết luận dừng (chuỗi giờ và chuỗi TB ngày) |
| Tương quan (Spearman) | Iws −0,36; cbwd_NW −0,33; DEWP 0,30; cbwd_SE 0,21. TB pm2.5 khi `cbwd = cv`: 126, khi gió NW: 70 |

## 4. So sánh nhanh

| | Bike Sharing | Beijing PM2.5 |
|---|---|---|
| Dòng | 17.379 | 43.824 |
| Thiếu | 165 giờ thiếu dòng | 2.067 NA ở mục tiêu |
| Skew / kurtosis mục tiêu | 1,28 / 1,42 | 1,80 / 4,77 |
| Outlier mục tiêu | 2,9% | 4,25% |
| ACF lag1 / lag24 | 0,843 / 0,819 | 0,965 / 0,398 |
| Đặc điểm nổi bật | Mùa vụ ngày/tuần mạnh, drift +63,2% giữa 2 năm | Thiếu theo đoạn, đuôi nặng, phụ thuộc thời tiết |

## 5. Gợi ý tiền xử lý

**Bike Sharing**
- Bỏ `casual`, `registered` (rò rỉ mục tiêu) và `instant` (số thứ tự); giữ một trong `temp`/`atemp`.
- Dựng lưới giờ đều; quyết định điền 0 hay nội suy cho 165 giờ thiếu, kèm cờ đánh dấu.
- Cân nhắc log1p mục tiêu; giữ outlier giờ cao điểm.
- Chia theo thời gian; xử lý drift giữa 2011 và 2012 (đặc trưng xu hướng hoặc chuẩn hóa theo cửa sổ); đặc trưng giờ, thứ, workingday, lag 24/168.

**Beijing PM2.5**
- Bỏ 24 giờ đầu; nội suy đoạn thiếu ngắn, mask đoạn thiếu dài khi tính loss và metric.
- log1p mục tiêu; không xóa đỉnh ô nhiễm; cân nhắc loss bền vững.
- One-hot `cbwd`; Iws/Is/Ir là cộng dồn nên cân nhắc sai phân.
- Thời tiết là biến quan sát cùng thời điểm: khi dự báo nhiều bước cần dùng giá trị dự báo hoặc lag.

**Chung:** chia train/test theo thời gian, fit scaler/imputer chỉ trên train, luôn báo baseline naive và seasonal naive.

## 6. Thay đổi so với bản khảo sát trước

Bản trước (13/10/2026) khảo sát 6 bộ UCI cho TabM (Adult, Bank Marketing, Breast Cancer Wisconsin, Wine Quality, Bike Sharing, Heart Disease) và FreshRetailNet-50K; M5 đã bị loại trước đó. Trong bản này đã gỡ:
- Toàn bộ nội dung về 5 bộ phân loại/hồi quy, FreshRetailNet-50K và M5 khỏi README và báo cáo.
- `figures/khung_phuong_phap.png` (sơ đồ ghi "Bike · M5 · FreshRetailNet").
- Trước đó, EDA của ETTm1 và Tourism Monthly cũng đã được gỡ khỏi `eda/`.

## Tài liệu tham khảo

1. Fanaee-T, H., & Gama, J. (2014). Event labeling combining ensemble detectors and background knowledge. *Progress in Artificial Intelligence*, 2(2–3), 113–127. https://doi.org/10.1007/s13748-013-0040-3
2. Fanaee-T, H. (2013). Bike Sharing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894
3. Liang, X., Zou, T., Guo, B., Li, S., Zhang, H., Zhang, S., Huang, H., & Chen, S. X. (2015). Assessing Beijing's PM2.5 pollution: severity, weather impact, APEC and winter heating. *Proceedings of the Royal Society A*, 471, 20150257. https://doi.org/10.1098/rspa.2015.0257
4. Chen, S. (2015). Beijing PM2.5 [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5JS49
