# Khảo sát và chuẩn bị dataset cho time-series forecasting

## Research question và phạm vi

Báo cáo này đánh giá hai dataset nhẹ, có citation và phù hợp để nghiên cứu deep learning cho dự báo chuỗi thời gian:

> Với một quy trình preprocessing không rò rỉ dữ liệu, các mô hình baseline, GRU/LSTM/TCN nhỏ có thể dự báo nhu cầu thuê xe theo giờ và phụ tải điện theo 10 phút tốt đến mức nào trên hai dataset công khai này?

UCI Bike Sharing là dataset chính cho **demand forecasting**. Power Consumption of Tetouan City là dataset bổ sung cho **load forecasting**; nó không phải nhu cầu vận tải nhưng kiểm tra khả năng áp dụng cùng quy trình cho một chuỗi nhu cầu năng lượng.

Các số liệu EDA trong báo cáo được tính từ hai CSV đang có trong `eda/data/raw/`. Code tái lập nằm trong `eda/scripts/`, `eda/src/` và `eda/notebooks/`.

## 1. Thông tin dataset

### 1.1 UCI Bike Sharing

**Nguồn và citation.** Dataset chính thức là UCI Bike Sharing, UCI ID 275, giấy phép CC BY 4.0 [1]. Bài báo gốc của Fanaee-T và Gama mô tả dữ liệu Capital Bikeshare và cách tổng hợp chuỗi theo giờ/ngày [2].

**Bài toán và kiểu dữ liệu.** Đây là dữ liệu multivariate time series theo giờ, bài toán regression. Target là `cnt`, số lượt thuê xe trong một giờ. Dữ liệu có các biến thời tiết, lịch, giờ trong ngày, ngày trong tuần, mùa và năm.

**Kích thước và input dimension.** CSV `hour.csv` đang dùng có 17.379 dòng dữ liệu và 17 cột, gồm timestamp dạng `dteday` + `hr`, 13 biến mô tả/thời tiết, hai thành phần `casual` và `registered`, và target `cnt`. Trang UCI hiện hiển thị 17.389 instances và 13 features; bài báo gốc ghi 17.379 giờ. Vì vậy, báo cáo dùng số dòng thực tế đọc được từ CSV là 17.379 và ghi nhận sự khác biệt metadata này để bảo đảm tái lập.

Sau khi loại `instant`, `casual` và `registered`, có 13 trường đầu vào thô nếu giữ `dteday` như một trường thời gian. Khi mã hóa thời gian thành các biến sin/cos và thêm lag, input dimension cuối cùng phụ thuộc vào thiết kế thí nghiệm. Lookback là chiều thời gian của cửa sổ, không phải input dimension.

**Khoảng thời gian và split.** Chuỗi trải từ 2011-01-01 00:00 đến 2012-12-31 23:00. Dataset không cung cấp sẵn train/validation/test split. Protocol đề xuất cho project là split theo thứ tự thời gian 70/15/15:

- Train: 12.165 dòng, từ 2011-01-01 00:00 đến 2012-05-27 01:00.
- Validation: 2.607 dòng, từ 2012-05-27 02:00 đến 2012-09-12 16:00.
- Test: 2.607 dòng, từ 2012-09-12 17:00 đến 2012-12-31 23:00.

Bài báo gốc dùng 2011 làm train và 2012 làm test trong phân tích của họ [2]. Protocol 70/15/15 được chọn cho nghiên cứu DL này vì cần một validation set riêng để chọn lookback, learning rate và early stopping. Không được random split.

**Kích thước tệp và vấn đề cần xử lý.** File `hour.csv` khoảng 1,1 MB. Không có NA trong ô và không có timestamp trùng, nhưng có 165 mốc giờ thiếu trên lưới 17.544 mốc kỳ vọng, tương đương 0,94%. `casual + registered = cnt` ở mọi dòng; hai cột này là thành phần của target và phải loại khỏi input. `instant` chỉ là chỉ số dòng. Target lệch phải, có trung bình 189,463, skewness 1,277 và coefficient of variation khoảng 0,957. Trung bình theo giờ năm 2012 cao hơn năm 2011 khoảng 63,2%, cho thấy drift. ACF lag 24 = 0,819 và lag 168 = 0,876, cho thấy mùa ngày và mùa tuần mạnh.

### 1.2 Power Consumption of Tetouan City

**Nguồn và citation.** Dataset chính thức là Power Consumption of Tetouan City, UCI ID 849, giấy phép CC BY 4.0 [3]. Dataset được giới thiệu cùng bài của Salam và El Hibaoui về so sánh các thuật toán dự báo phụ tải [4].

**Bài toán và kiểu dữ liệu.** Đây là multivariate time series theo 10 phút, bài toán regression. Có ba target liên tục: `Zone 1 Power Consumption`, `Zone 2 Power Consumption` và `Zone 3 Power Consumption`. Biến ngoại sinh gồm Temperature, Humidity, Wind Speed, general diffuse flows và diffuse flows.

**Kích thước và input dimension.** CSV đang dùng có 52.416 dòng và 9 cột: một cột `DateTime`, năm biến ngoại sinh và ba target. Trang UCI hiển thị 52.417 instances và 6 features; cách trình bày này tách 6 biến đầu vào khỏi 3 target. Báo cáo dùng 52.416 dòng dữ liệu thực tế đọc được từ CSV và ghi nhận khác biệt metadata. Tệp CSV khoảng 4 MB; file ZIP tải từ UCI khoảng 1,3 MB.

Với dự báo một Zone, input có thể gồm năm biến ngoại sinh và các lag của target. Với dự báo đồng thời, output dimension là 3. Time features như hour-of-day, day-of-week và month được sinh từ `DateTime`; input dimension cuối cùng phụ thuộc vào việc dùng univariate, multivariate hay multi-output.

**Khoảng thời gian và split.** Chuỗi trải từ 2017-01-01 00:00 đến 2017-12-30 23:50. Protocol đề xuất 70/15/15 theo thời gian:

- Train: 36.691 dòng, đến 2017-09-12 19:00.
- Validation: 7.862 dòng, từ 2017-09-12 19:10 đến 2017-11-06 09:20.
- Test: 7.863 dòng, từ 2017-11-06 09:30 đến 2017-12-30 23:50.

Một notebook ArcGIS dùng 144 mốc cuối làm test cho forecast một ngày ở tần suất 10 phút, tương đương 24 giờ × 6 mốc/giờ [7]. Đây là một thiết kế test ngắn hạn hợp lý để tham khảo, nhưng project này nên giữ thêm validation và một test block dài hơn để đánh giá drift.

**Kích thước tệp và vấn đề cần xử lý.** EDA cho thấy không có NA, timestamp trùng hoặc mốc 10 phút thiếu. Ba Zone có thang đo khác nhau: trung bình lần lượt là 32.344,971; 21.042,509; và 17.835,406. Zone 3 lệch phải hơn với skewness 1,024. Tương quan Pearson giữa Zone 1 và Zone 2 là 0,835; giữa Zone 1 và Zone 3 là 0,751. Sau khi resample theo giờ, Zone 1 có ACF lag 24 = 0,963 và lag 168 = 0,953. Khi dự báo nhiều bước, các biến thời tiết của tương lai chỉ được dùng nếu có kịch bản dự báo thời tiết; nếu không, chỉ dùng giá trị quá khứ hoặc thiết kế forecast phù hợp.

## 2. Đánh giá độ phù hợp

### 2.1 Đối chiếu với research question

**UCI Bike Sharing đáp ứng trực tiếp bài toán demand forecasting.** Dataset có target theo giờ, có biến lịch và thời tiết, có đủ quan sát cho cửa sổ DL ngắn, nhẹ để chạy trên máy cá nhân và có nguồn/citation chính thức. Drift giữa 2011 và 2012 giúp kiểm tra khả năng tổng quát theo thời gian. Điểm yếu là chỉ có một hệ thống tại Washington DC và có 165 mốc giờ thiếu trên lưới kỳ vọng.

**Tetouan đáp ứng tốt bài toán load forecasting nhưng chỉ đáp ứng gián tiếp demand forecasting.** Nó có chuỗi dày hơn, ba output có tương quan, nhiều biến ngoại sinh và không có missing timestamp. Đây là dataset tốt để kiểm tra multivariate và multi-output forecasting. Tuy nhiên, nếu research question chỉ nói về nhu cầu vận tải, Tetouan phải được mô tả là dataset bổ sung cho năng lượng, không được gộp vào cùng một domain.

### 2.2 Đánh giá theo điều kiện bắt buộc

- **Số lượng mẫu:** Bike có 17.379 giờ; Tetouan có 52.416 mốc 10 phút. Cả hai đủ cho baseline và DL nhỏ, nhưng chưa phải quy mô phù hợp để biện minh cho Transformer lớn.
- **Input dimension:** Bike có ít biến và có thể kiểm soát rõ leakage. Tetouan có 5 ngoại sinh, 3 target và khả năng tạo lag; cả hai phù hợp với input dimension nhỏ đến vừa.
- **Kiểu dữ liệu:** Cả hai là time series multivariate. Bike là một target chính; Tetouan là ba target liên tục.
- **Loại bài toán:** Cả hai là regression/forecasting, không phải classification. Không cần encoding label; cần encoding time features và scaling số.
- **Tính khả thi:** Download nhỏ, chạy được bằng pandas/NumPy và mô hình GRU/LSTM/TCN nhỏ. EDA hiện tại đã có notebook và summary JSON.
- **Khả năng tái lập:** Có UCI DOI, script tải dữ liệu và code EDA. Cần bổ sung protocol split và preprocessing train-only trước khi chạy benchmark chính thức.

**Kết luận chọn dataset.** Giữ cả hai. Dùng Bike Sharing làm dataset chính để trả lời demand forecasting theo giờ. Dùng Tetouan làm dataset thứ hai để kiểm tra khả năng tổng quát sang load forecasting và multi-output. Nếu đề tài bắt buộc chỉ một domain là mobility demand, chỉ Bike Sharing nên nằm trong thí nghiệm chính; Tetouan chuyển sang phần kiểm tra bổ sung hoặc bị loại với lý do khác domain.

## 3. Code xử lý dataset

### 3.1 Code hiện có trong repository

- `eda/scripts/download_data.py`: tải hai ZIP từ UCI và giải nén vào `eda/data/raw/`; không commit dữ liệu thô vào repository.
- `eda/scripts/build_notebooks.py`: sinh notebook EDA từ mã nguồn có thể tái lập.
- `eda/src/eda_utils.py`: kiểm tra schema, missing, timestamp gaps, descriptive statistics, IQR outlier, ACF/PACF, STL và stationarity.
- `eda/notebooks/eda_01_bike_sharing.ipynb`: EDA Bike Sharing.
- `eda/notebooks/eda_02_tetouan_power.ipynb`: EDA Tetouan.
- `eda/notebooks/eda_03_so_sanh_va_tien_xu_ly.ipynb`: so sánh và đề xuất preprocessing.
- `eda/reports/summary_bike.json` và `eda/reports/summary_tetouan.json`: lưu số liệu chính sau khi chạy notebook.

Lệnh tái lập:

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

### 3.2 Pipeline preprocessing bắt buộc

**Bước 1 — Load và kiểm tra schema.** Đọc CSV, parse timestamp, sort theo thời gian, kiểm tra kiểu dữ liệu, duplicate timestamp, NA và khoảng cách thời gian.

**Bước 2 — Làm sạch.** Với Bike, loại `instant`, `casual` và `registered`; dựng lại lưới giờ để đánh dấu 165 mốc thiếu, không tự động biến mọi mốc thiếu thành nhu cầu bằng 0 nếu chưa xác nhận ý nghĩa nghiệp vụ. Với Tetouan, giữ các mốc sạch và kiểm tra lại bước 10 phút.

**Bước 3 — Tạo time features.** Tạo hour, day-of-week, month, working-day và các biến sin/cos cho chu kỳ ngày/tuần. Không dùng `DateTime` dạng chuỗi trực tiếp làm input.

**Bước 4 — Tạo cửa sổ supervised.** Dùng lookback ban đầu 24 và 168 bước cho Bike; với Tetouan thử 144 bước cho một ngày và 1.008 bước cho một tuần ở tần suất 10 phút. Chọn lookback bằng validation, không chọn dựa trên test.

**Bước 5 — Split theo thời gian.** Dùng ranh giới 70/15/15 đã nêu ở mục 1. Tạo cửa sổ sau khi xác định ranh giới hoặc bảo đảm không để target tương lai của validation/test lọt vào train. Không random shuffle toàn bộ chuỗi.

**Bước 6 — Scale train-only.** Fit scaler trên tập train. Với Tetouan, scale riêng từng Zone hoặc dùng loss có trọng số vì ba target có quy mô khác nhau. Áp dụng cùng tham số scaler cho validation và test; inverse-transform trước khi báo cáo metric theo đơn vị gốc.

**Bước 7 — Visualization.** Tối thiểu cần có line plot theo thời gian, histogram/boxplot target, missing timeline, ACF/PACF, seasonal profile theo giờ/ngày trong tuần, heatmap tương quan và actual-vs-predicted trên test.

**Bước 8 — Lưu metadata.** Lưu số dòng, thời gian bắt đầu/kết thúc, split boundaries, columns bị loại, feature list, lookback, horizon, scaler parameters và seed. Nếu resample Tetouan, ghi rõ dùng mean hay sum.

### 3.3 Pseudocode split và scale không leakage

```python
# df đã sort theo timestamp
n = len(df)
i_train = int(n * 0.70)
i_val = int(n * 0.85)
train = df.iloc[:i_train].copy()
valid = df.iloc[i_train:i_val].copy()
test = df.iloc[i_val:].copy()

numeric = ['temp', 'atemp', 'hum', 'windspeed']
mu = train[numeric].mean()
sigma = train[numeric].std().replace(0, 1)
for part in (train, valid, test):
    part[numeric] = (part[numeric] - mu) / sigma
```

Đoạn code trên chỉ minh họa nguyên tắc. Khi tạo lag/window, phải bảo đảm feature tại thời điểm dự báo không dùng giá trị tương lai. Với forecast nhiều bước và weather exogenous, cần ghi rõ biến tương lai là observed, forecasted hay không sử dụng.

## 4. Nội dung cần ghi vào paper/report

### 4.1 Dataset description

Trong paper cần mô tả Bike Sharing là dữ liệu thuê xe theo giờ của Capital Bikeshare ở Washington DC trong 2011–2012, target `cnt`, biến lịch và thời tiết [1] [2]. Cần ghi rõ `casual` và `registered` không được đưa vào input vì chúng cộng lại bằng `cnt`.

Tetouan cần được mô tả là SCADA power-consumption data của ba mạng phân phối ở Tetouan, Morocco, ghi nhận mỗi 10 phút trong năm 2017, có năm biến môi trường và ba target Zone [3] [4]. Cần ghi rõ đây là load forecasting, không phải mobility demand forecasting.

### 4.2 Dataset statistics và EDA

Báo cáo phải nêu số dòng thực tế từ CSV, khoảng thời gian, tần suất, số target, NA, timestamp gap, duplicate, target mean/skewness, ACF, tương quan và vấn đề leakage. Với hai dataset này, các số chính cần đưa vào paper là:

- Bike: 17.379 dòng; 165 giờ thiếu; 0 NA; `cnt` mean 189,463; skewness 1,277; ACF 24 = 0,819; ACF 168 = 0,876; tăng trung bình theo giờ năm 2012 so với 2011 là 63,2%.
- Tetouan: 52.416 dòng; 0 timestamp gap; 0 NA; mean Zone 1/2/3 lần lượt 32.344,971/21.042,509/17.835,406; tương quan Zone 1–2 = 0,835; Zone 1–3 = 0,751; ACF Zone 1 sau resample theo giờ tại lag 24/168 lần lượt 0,963/0,953.

Không dùng bảng hoặc số liệu từ metadata UCI thay thế cho số dòng thực tế mà không ghi chú chênh lệch 17.389 so với 17.379 và 52.417 so với 52.416.

### 4.3 Preprocessing và data split

Paper phải ghi rõ các cột bị loại, cách parse timestamp, cách xử lý mốc thiếu, time features, lookback, forecast horizon, chronological split 70/15/15 và scaler fit trên train. Nếu có resample Tetouan từ 10 phút sang giờ, phải ghi công thức và lý do. Không được chỉ ghi “data were normalized” mà không nói scaler fit trên phần nào.

### 4.4 Visualization cần có

Hình tối thiểu gồm: target theo thời gian, phân phối target, ACF/PACF, seasonal profile, heatmap tương quan, timeline mốc thiếu của Bike, và đồ thị actual-vs-predicted cho test. Với Tetouan nên thêm một hình cho ba Zone trên cùng trục hoặc ba panel để thể hiện correlation và scale khác nhau.

### 4.5 Citation và reproducibility

Dùng DOI UCI và citation bài gốc. Ghi ngày tải dữ liệu, URL, commit code, split boundary, seed và phiên bản package. Dataset được cấp phép CC BY 4.0; khi tái phân phối kết quả phải ghi attribution phù hợp [1] [3].

## 5. Các phương pháp đã áp dụng và baseline đề xuất

### 5.1 Bike Sharing

Bài của Fanaee-T và Gama dùng dữ liệu Bike Sharing ở quy mô giờ/ngày cho event labeling, không phải một benchmark DL forecasting thuần túy [2]. Vì vậy, không được trích bài này như bằng chứng rằng một mô hình DL đã đạt metric forecasting cụ thể trên cùng protocol.

Petneházi dùng trực tiếp UCI Bike Sharing trong một nghiên cứu RNN forecasting [5]. Paper bỏ weather, mã hóa các thành phần thời gian bằng sin/cos, dùng lag gần 1–3 giờ và lag 24/48/168, scale min–max, train 70% và test 30%. Paper thử LSTM và GRU một lớp 32 units, dropout 0,5, 16-step unrolled sequence và đánh giá MSE, SMAPE, R², MAE và MedAE.

Kết quả của paper đó cho thấy bagging tốt hơn estimator đơn. Với LSTM, test one-step bagged có RMSE 45,74, MAE 30,23, SMAPE 22,75, R² 0,96 và MedAE 19,27; test multi-step bagged có RMSE 90,64, MAE 62,99, SMAPE 41,99, R² 0,83 và MedAE 39,56. Với GRU, test one-step bagged có RMSE 48,13, MAE 31,24, SMAPE 21,76, R² 0,95; test multi-step bagged có RMSE 93,86, MAE 64,34, SMAPE 40,32, R² 0,82. Các con số này thuộc protocol của paper, không phải kết quả chạy lại trong repository này [5].

Một survey về deep learning cho bike-sharing forecasting tổng hợp các nhóm mô hình LSTM/GRU/TCN, CNN–LSTM, attention, GCN/GAT và STGCN; các metric thường gặp là RMSE, MAE, MAPE, SMAPE, R² và đôi khi là parameter count/inference time [6]. Nhiều mô hình graph/spatiotemporal trong survey dùng dữ liệu nhiều station khác với UCI Bike Sharing, nên không nên áp dụng trực tiếp mà không kiểm tra schema.

**Baseline nên chạy trên Bike:** seasonal-naive lag 24, seasonal-naive lag 168, historical mean theo hour-of-day, linear/ridge regression với time features, Random Forest/XGBoost hoặc HistGradientBoosting, GRU nhỏ, LSTM nhỏ và TCN nhỏ. Naive và linear baseline là bắt buộc; nếu DL không vượt seasonal-naive thì không thể kết luận DL hữu ích.

**Metric nên báo cáo:** MAE, RMSE, sMAPE và R². Vì `cnt` lệch phải và có giờ nhu cầu thấp, không nên chỉ dùng MAPE; cần ghi cách xử lý y gần 0. Nên báo cáo thêm parameter count và thời gian train nếu mục tiêu là mô hình nhẹ.

### 5.2 Tetouan City Power Consumption

Bài gốc về Tetouan so sánh feedforward neural network, Random Forest, Decision Tree và SVR với RBF kernel, tối ưu tham số bằng grid search cho dự báo mỗi 10 phút và mỗi giờ. Abstract của bài cho biết Random Forest có lỗi nhỏ hơn các đối thủ [4]. Đây là baseline ML quan trọng vì nó dùng chính dataset Tetouan.

Notebook ArcGIS minh họa ba thiết kế: one-step univariate, multi-step multivariate và one-step multivariate. Nó giữ 144 mốc cuối làm test cho một ngày 10 phút, dùng scaling và báo cáo R². Kết quả minh họa đạt R² = 0,96 cho Bi-LSTM univariate, 0,97 cho multi-step multivariate và 0,98 cho one-step multivariate [7]. Đây là kết quả của notebook minh họa với tổng power và Bi-LSTM/ArcGIS, không phải kết quả benchmark của repository này.

Một nghiên cứu mở năm 2026 xây dựng benchmark bằng Darts trên chính dữ liệu Tetouan, so sánh Linear Regression, Random Forest, XGBoost, Prophet, TiDE và TSMixer ở cả tần suất 10 phút và theo giờ. Họ dùng MAE, RMSE và MAPE; báo cáo TiDE đạt MAPE 1,92% cho combined 10-minute forecast, còn Random Forest đạt MAPE 1,04% và MAE 224,2 ở hourly resolution [8]. Vì khác preprocessing, target combined và protocol, các số liệu này chỉ dùng làm tham khảo khi thiết kế benchmark, không dùng làm kết quả của project.

**Baseline nên chạy trên Tetouan:** last-value/seasonal-naive theo 10 phút, lag 144 cho mùa ngày, lag 1.008 cho mùa tuần, linear regression, Random Forest, XGBoost nếu có dependency, GRU/LSTM multi-output và TCN nhỏ. Với ba Zone, cần báo cáo cả metric từng Zone và macro-average sau khi inverse-transform.

**Metric nên báo cáo:** MAE, RMSE, sMAPE hoặc MAPE có quy tắc xử lý mẫu gần 0, và R². Với load forecasting nên thêm normalized RMSE hoặc MASE nếu so sánh giữa Zone có scale khác nhau. Cần tách rõ one-step và multi-step; không so sánh trực tiếp hai loại horizon như cùng một bài toán.

### 5.3 Thiết kế benchmark chung

Thứ tự thực nghiệm nên là: seasonal-naive; linear/ridge; Random Forest hoặc XGBoost; GRU; LSTM; TCN. Chỉ thử attention hoặc Transformer sau khi baseline và DL nhỏ đã có kết quả ổn định.

Mỗi dataset cần chạy cùng một quy trình split, seed cố định, early stopping dựa trên validation, inverse-transform trước khi tính metric và ít nhất ba seed nếu tài nguyên cho phép. Bảng kết quả phải có model, input features, lookback, horizon, số tham số, train time, MAE, RMSE, sMAPE và R². Không dùng test set để chọn mô hình.

## Kết luận

Theo chuẩn năm bước của file mẫu, cả hai dataset đủ điều kiện để đưa vào nghiên cứu forecasting nhẹ. Bike Sharing là lựa chọn phù hợp hơn cho research question về demand forecasting. Tetouan là lựa chọn tốt để kiểm tra multivariate/multi-output load forecasting và độ bền của pipeline. Điểm cần hoàn thiện trước khi huấn luyện chính thức là script preprocessing có split 70/15/15, scaler train-only, window generation và benchmark seasonal-naive.

## Tài liệu tham khảo

[1]: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset "UCI Bike Sharing dataset"
[2]: https://doi.org/10.1007/s13748-013-0040-3 "Event labeling combining ensemble detectors and background knowledge"
[3]: https://archive.ics.uci.edu/dataset/849/power+consumption+of+tetouan+city "UCI Power Consumption of Tetouan City dataset"
[4]: https://doi.org/10.1109/IRSEC.2018.8703007 "Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city"
[5]: https://arxiv.org/html/1901.00069v1 "Recurrent Neural Networks for Time Series Forecasting"
[6]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9185130/ "Bike sharing usage prediction with deep learning: a survey"
[7]: https://developers.arcgis.com/python/latest/samples/forecasting-daily-power-consumption-using-deep-learning-timeseries/ "Forecasting daily power consumption using deep learning time series"
[8]: https://doi.org/10.1016/j.rineng.2026.110289 "Electricity demand forecasting for Tetouan, Morocco using Darts in machine-learning: A comparative study of forecasting models"
