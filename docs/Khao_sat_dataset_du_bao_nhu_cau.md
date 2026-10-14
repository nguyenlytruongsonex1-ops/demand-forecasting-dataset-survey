# Báo cáo EDA: UCI Bike Sharing và Power Consumption of Tetouan City

**Nguyễn Lý Trường Sơn, 14/10/2026**

## 1. Phạm vi và mục tiêu

Báo cáo tập trung vào hai dataset gần với bài toán dự báo nhu cầu hoặc phụ tải: **UCI Bike Sharing** và **Power Consumption of Tetouan City**. Mục tiêu của EDA là kiểm tra cấu trúc chuỗi thời gian, chất lượng dữ liệu, phân phối target, mùa vụ, tự tương quan, quan hệ với biến ngoại sinh và các rủi ro cần xử lý trước khi huấn luyện mô hình deep learning.

Các con số trong báo cáo được sinh từ hai notebook đã chạy trong `eda/notebooks/`. Dữ liệu thô không được commit vào repository; script tải trực tiếp từ nguồn UCI.

## 2. Thông tin dataset và nguồn trích dẫn

### 2.1. UCI Bike Sharing (UCI 275)

UCI Bike Sharing ghi nhận số lượt thuê xe của hệ thống Capital Bikeshare tại Washington DC. File `hour.csv` có 17.379 dòng theo giờ, từ `2011-01-01 00:00:00` đến `2012-12-31 23:00:00`, với target `cnt`. Các biến đầu vào gồm thời tiết (`temp`, `atemp`, `hum`, `windspeed`, `weathersit`) và biến lịch (`hr`, `weekday`, `workingday`, `holiday`, `season`, `mnth`, `yr`). UCI cung cấp dataset dưới license CC BY 4.0 và DOI `10.24432/C5W894` [1].

Bài báo nền của Fanaee-T và Gama sử dụng log của hệ thống bike sharing làm dữ liệu thực nghiệm, đồng thời thảo luận về phát hiện sự kiện, mô hình dự báo và các đặc điểm chuỗi thời gian [2].

### 2.2. Power Consumption of Tetouan City (UCI 849)

Tetouan City ghi nhận phụ tải của ba vùng phân phối điện tại Tetouan, Morocco, cùng nhiệt độ, độ ẩm, tốc độ gió, general diffuse flows và diffuse flows. File thực tế có 52.416 dòng theo tần suất 10 phút, từ `2017-01-01 00:00:00` đến `2017-12-30 23:50:00`. Ba target là phụ tải của Zone 1, Zone 2 và Zone 3. UCI cung cấp dataset dưới license CC BY 4.0 và DOI `10.24432/C5B034` [3].

Bài báo của Salam và El Hibaoui mô tả dữ liệu SCADA của ba mạng phân phối, được ghi mỗi 10 phút trong năm 2017, và so sánh các mô hình dự báo phụ tải. Bài báo xuất bản tại IEEE IRSEC, DOI `10.1109/IRSEC.2018.8703007` [4].

## 3. EDA UCI Bike Sharing

### 3.1. Tính đầy đủ và tính liên tục của thời gian

File có 17.379 dòng. Khi tạo lưới đều từ timestamp đầu đến cuối, có 17.544 mốc giờ kỳ vọng và thiếu 165 mốc, tương đương 0,94%. Các mốc thiếu rải trên 76 ngày; không có timestamp trùng và không có NA trong các ô dữ liệu.

Điều này cần được hiểu là **thiếu dòng trên lưới thời gian**, không phải missing value trong cột. Trước khi tạo cửa sổ huấn luyện cần quyết định các mốc này là số lượt thuê bằng 0, giá trị cần nội suy, hay giá trị bị che bằng một cờ chất lượng dữ liệu.

### 3.2. Target, phân phối và rò rỉ dữ liệu

`cnt` có trung bình 189,5, trung vị 142, giá trị lớn nhất 977, skewness 1,28 và kurtosis 1,42. Target lệch phải do các giờ cao điểm có nhu cầu lớn. Khoảng 2,9% quan sát vượt ngưỡng IQR 1,5 lần; các điểm này phần lớn là giờ cao điểm thật, không nên xóa tự động.

Có rò rỉ target rõ ràng: `casual + registered = cnt` ở 100% dòng. Hai cột `casual` và `registered` là thành phần của target nên phải loại khỏi input. `instant` cũng nên loại vì chỉ là chỉ số dòng.

### 3.3. Xu hướng, mùa vụ và tính dừng

Trung bình theo giờ tăng từ 143,8 trong năm 2011 lên 234,7 trong năm 2012, tương đương tăng 63,2%. Đây là drift theo thời gian, vì vậy split ngẫu nhiên có thể làm kết quả quá lạc quan.

Chuỗi có mùa vụ ngày và tuần rõ. ACF tại lag 1 là 0,843, lag 24 là 0,819 và lag 168 là 0,876. Vào ngày làm việc, các đỉnh chính nằm ở khoảng 8h và 17h; vào ngày nghỉ, nhu cầu tập trung hơn vào giữa ngày. Độ mạnh mùa vụ ngày theo STL, với period 24, là 0,881. Chuỗi tổng hợp theo ngày không dừng; sai phân bậc một giúp chuỗi dừng hơn.

### 3.4. Quan hệ với biến ngoại sinh

Theo tương quan Spearman, `hr` liên quan mạnh nhất với `cnt` ở mức 0,511. `temp` và `atemp` cùng ở mức 0,423; hai biến này gần trùng nhau với tương quan Pearson khoảng 0,988, nên có thể giữ một biến. `hum` có quan hệ âm với nhu cầu. Khi dự báo nhiều bước, thời tiết tại tương lai chỉ được dùng nếu có dự báo thời tiết hoặc phải thay bằng giá trị trễ.

## 4. EDA Power Consumption of Tetouan City

### 4.1. Tính đầy đủ và tần suất

File có 52.416 dòng và ba target. Lưới 10 phút từ timestamp đầu đến cuối không có mốc thiếu, timestamp trùng hoặc NA. Đây là điểm thuận lợi cho việc tạo cửa sổ liên tục và đánh giá multi-step forecasting.

Dataset có tần suất khác Bike Sharing. Nếu muốn so sánh hai bộ trong cùng một thí nghiệm, cần resample Tetouan về giờ. Khi đó phải nêu rõ target sau resample là phụ tải trung bình trong giờ hay tổng năng lượng trong giờ; không nên dùng hai cách diễn giải lẫn nhau.

### 4.2. Phân phối của ba target

Thống kê trên đơn vị gốc của dữ liệu:

| Target | Trung bình | Độ lệch chuẩn | Min | Max | Skewness | Kurtosis |
|---|---:|---:|---:|---:|---:|---:|
| Zone 1 | 32.345,0 | 7.130,6 | 13.895,7 | 52.204,4 | 0,229 | -0,754 |
| Zone 2 | 21.042,5 | 5.201,5 | 8.560,1 | 37.408,9 | 0,329 | -0,437 |
| Zone 3 | 17.835,4 | 6.622,2 | 5.935,2 | 47.598,3 | 1,024 | 1,086 |

Zone 1 và Zone 2 tương đối cân bằng hơn; Zone 3 lệch phải rõ hơn. Theo quy tắc IQR 1,5, tỷ lệ outlier khoảng 0% ở Zone 1, 0,013% ở Zone 2 và 2,272% ở Zone 3. Các điểm cực trị cần được kiểm tra theo thời gian trước khi loại bỏ vì có thể đại diện cho đỉnh phụ tải.

### 4.3. Tương quan giữa vùng và mùa vụ

Ba target có tương quan dương: Pearson giữa Zone 1 và Zone 2 là 0,835; giữa Zone 1 và Zone 3 là 0,751; giữa Zone 2 và Zone 3 là 0,571. Điều này ủng hộ thiết kế multi-output, trong đó mô hình dự báo đồng thời ba vùng có thể tận dụng thông tin chung.

Sau khi lấy trung bình theo giờ, Zone 1 có ACF lag 1 = 0,922, lag 24 = 0,963 và lag 168 = 0,953. Độ mạnh mùa vụ ngày theo STL là 0,987 và độ mạnh xu hướng là 0,931. Nhu cầu Zone 1 trung bình cao nhất khoảng 20h và thấp nhất khoảng 6h; Zone 2 cũng đạt đỉnh khoảng 20h, trong khi Zone 3 đạt đỉnh khoảng 20h và thấp nhất khoảng 7h.

ACF cao ở lag 24 và 168 cho thấy các cửa sổ 24 giờ và 7 ngày nên được thử nghiệm. Tuy nhiên, vì dữ liệu gốc có bước 10 phút, nếu giữ tần suất gốc thì một ngày tương ứng 144 bước và một tuần tương ứng 1.008 bước.

### 4.4. Quan hệ với biến ngoại sinh

Đối với Zone 1, tương quan Spearman lớn nhất trong nhóm ngoại sinh là Temperature = 0,433, Humidity = -0,300 và general diffuse flows = 0,261. Diffuse flows và Wind Speed có quan hệ yếu hơn. Khi dự báo nhiều bước, cần xác định các biến ngoại sinh nào thực sự có sẵn ở thời điểm dự báo; nếu không, sử dụng lag hoặc dự báo riêng cho ngoại sinh.

## 5. So sánh và hàm ý cho mô hình DL

Hai dataset đều có seasonality và tự tương quan đủ rõ để làm bài toán forecasting, nhưng chúng đại diện cho hai dạng target khác nhau:

- **Bike Sharing:** một target đếm theo giờ, có drift mạnh giữa hai năm, có rò rỉ từ các biến thành phần và thiếu một số mốc giờ.
- **Tetouan:** ba target phụ tải liên tục, dữ liệu sạch theo 10 phút, có tương quan giữa các vùng, mùa vụ ngày/tuần mạnh và cần xử lý khác biệt quy mô giữa các target.

Thiết kế baseline nên gồm naive, seasonal-naive, linear regression hoặc gradient boosting. Sau đó mới thử MLP trên lag features, GRU/LSTM nhỏ hoặc TCN. Transformer chỉ nên thử sau khi đã chứng minh rằng baseline và mô hình DL nhỏ chưa đủ, vì kích thước dữ liệu vẫn nhỏ so với các benchmark lớn.

Đánh giá phải dùng chronological split, fit scaler chỉ trên train, cố định seed và báo cáo MAE, RMSE cùng sMAPE. Nên báo cáo riêng theo forecast horizon, ngày làm việc/ngày nghỉ và từng Zone. Với Tetouan, cần báo cáo cả kết quả multi-output và kết quả dự báo từng Zone độc lập.

## 6. Pipeline tiền xử lý đề xuất

### Bike Sharing

1. Parse `dteday` và `hr` thành timestamp.
2. Dựng lưới giờ đều và tạo cờ cho timestamp thiếu.
3. Loại `instant`, `casual`, `registered`; giữ một trong `temp` và `atemp`.
4. Tạo đặc trưng giờ, thứ, tháng, ngày làm việc và lag 24/168.
5. Cân nhắc `log1p(cnt)` nhưng không xóa các đỉnh giờ cao điểm.
6. Chia train/validation/test theo thời gian và kiểm tra drift giữa 2011 và 2012.

### Tetouan

1. Parse `DateTime` và kiểm tra bước 10 phút.
2. Đổi tên ba target về tên ngắn, nhất quán; lưu lại đơn vị gốc.
3. Tạo đặc trưng hour, day-of-week, month và cyclical encoding.
4. Scale từng Zone bằng thống kê của train; cân nhắc loss có trọng số nếu huấn luyện đồng thời.
5. Thử cả tần suất 10 phút và dữ liệu resample theo giờ với quy tắc được ghi rõ.
6. Dùng horizon 6 bước cho 1 giờ hoặc 144 bước cho 24 giờ nếu giữ tần suất 10 phút.

### Chung

- Không random split toàn bộ chuỗi.
- Không fit scaler, imputer hoặc feature transformation trên test.
- Luôn có baseline seasonal-naive.
- Báo cáo rõ lookback, horizon, tần suất, cách resample và cách xử lý outlier.

## 7. Kết luận

Hai dataset thống nhất với hướng **dự báo nhu cầu/phụ tải**. UCI Bike Sharing phù hợp để nghiên cứu demand theo giờ với một target và mùa vụ ngày/tuần rõ. Tetouan phù hợp để mở rộng sang load forecasting đa biến, multi-output và tần suất cao hơn.

Cả hai đều nhẹ, có nguồn UCI và DOI, có thể chạy EDA và mô hình nền trên máy yếu. Chúng phù hợp cho một nghiên cứu có phạm vi 4–6 tuần, miễn là mô hình được giữ nhỏ, có baseline rõ ràng và quy trình chia dữ liệu theo thời gian được thực hiện đúng.

## Tài liệu tham khảo

1. Fanaee-T, H., & Gama, J. (2014). *Event labeling combining ensemble detectors and background knowledge*. Progress in Artificial Intelligence, 2(2–3), 113–127. https://doi.org/10.1007/s13748-013-0040-3
2. Fanaee-T, H. (2013). *Bike Sharing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894
3. Salam, A., & El Hibaoui, A. (2018). *Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city*. IEEE IRSEC. https://doi.org/10.1109/IRSEC.2018.8703007
4. Salam, A., & El Hibaoui, A. (2023). *Power Consumption of Tetouan City* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5B034
