# Khảo sát dataset nhẹ cho TabM và dự báo nhu cầu

**Nguyễn Lý Trường Sơn, 13/10/2026**

## 1. Phạm vi và cách đọc báo cáo

Báo cáo này chọn sáu dataset nhẹ, công khai và có citation rõ ràng để bắt đầu với TabM/deep learning trên dữ liệu bảng. Sáu bộ gồm Adult, Bank Marketing, Breast Cancer Wisconsin (Diagnostic), Wine Quality, Bike Sharing và Heart Disease. Năm bộ đầu tiên trong danh sách này chủ yếu là classification hoặc regression dạng bảng; chúng không phải demand time series thuần túy. Vì vậy, chúng nên được dùng cho **smoke test, benchmark TabM, preprocessing, calibration và nghiên cứu độ ổn định**, không nên dùng một mình để kết luận về forecasting nhu cầu.

Bike Sharing có cấu trúc chuỗi theo giờ và FreshRetailNet-50K là benchmark retail demand nâng cao. FreshRetailNet-50K được giữ lại như một dataset mở rộng, nhưng không nằm trong nhóm sáu dataset nhẹ.

Một nguyên tắc quan trọng là khóa URL, DOI, dataset ID, phiên bản, preprocessing và target mapping trước khi chạy. Các con số dưới đây là metadata từ nguồn chính tại thời điểm khảo sát; kích thước tải có thể thay đổi nếu repository cập nhật file.

## 2. Sáu dataset nhẹ được chọn

| Dataset | Task gốc | Quy mô | Dạng dữ liệu | Tải chính thức | License / citation | Vai trò đề xuất |
|---|---|---:|---|---:|---|---|
| Adult / Census Income [1] | Binary classification | 48,842 dòng, 14 feature | Categorical + integer, có missing | 605.7 KB | CC BY 4.0; DOI 10.24432/C5XW20 | Mixed-type TabM, missing value, fairness caveat |
| Bank Marketing [2] | Binary classification | 45,211 dòng, 16 feature | Categorical + integer, không missing | 999.8 KB cho archive chính | CC BY 4.0; DOI 10.24432/C5K306 | Imbalance, calibration, feature availability |
| Breast Cancer Wisconsin (Diagnostic) [3] | Binary classification | 569 dòng, 30 feature | Numerical, không missing | 50.1 KB | CC BY 4.0; DOI 10.24432/C5DW2B | Smoke test rất nhanh, seed variance |
| Wine Quality [4] | Regression hoặc classification | 4,898 dòng, 11 feature | Numerical, target ordinal, không missing | 89.2 KB | CC BY 4.0; DOI 10.24432/C56S3T | Regression, ordinal target, normalization |
| Bike Sharing [5] | Regression / forecasting | 17,389 dòng, 13 feature | Theo giờ/ngày, weather + calendar | 273.4 KB | CC BY 4.0; DOI 10.24432/C5W894 | Temporal split, covariates, drift |
| Heart Disease [6] | Classification | 303 dòng, 13 feature dùng trong thí nghiệm | Categorical + integer + real, có missing | 125.9 KB | CC BY 4.0; DOI 10.24432/C52P4X | Repeated CV, imputation, calibration |

### 2.1. Adult / Census Income

Adult dự đoán một người có thu nhập trên 50.000 USD/năm từ dữ liệu Census 1994. UCI ghi 48,842 instances và 14 features, gồm tuổi, nghề nghiệp, học vấn, tình trạng hôn nhân, chủng tộc, giới tính, giờ làm việc và quốc gia. Hai file dữ liệu chính có kích thước 3.8 MB và 1.9 MB; archive tải xuống là 605.7 KB [1].

Đây là lựa chọn tốt để bắt đầu với TabM vì có cả categorical và integer features, có missing values ở một số trường, và quy mô đủ để chạy nhanh nhưng không quá nhỏ. Có thể dùng Adult để so sánh MLP, TabM-mini, TabM và CatBoost dưới cùng preprocessing. Nên báo ROC-AUC, PR-AUC, log loss và balanced accuracy thay vì chỉ accuracy.

Caveat quan trọng: đây là dữ liệu lịch sử từ Census 1994 và có các biến nhạy cảm như sex/race. `fnlwgt` là survey weight, còn `education` và `education-num` có liên hệ mạnh. Random split không kiểm tra temporal shift hay geographical shift. Nếu nghiên cứu fairness, cần đặt câu hỏi và metric fairness riêng; không được suy ra fairness từ điểm AUC.

### 2.2. Bank Marketing

Bank Marketing mô tả các chiến dịch gọi điện của một ngân hàng Bồ Đào Nha, với mục tiêu dự đoán khách hàng có đăng ký tiền gửi kỳ hạn hay không. UCI ghi bản chính `bank-full.csv` có 45,211 instances và 16 input features; archive chính có kích thước 999.8 KB. UCI cũng cung cấp bản `bank-additional-full.csv` gồm 41,188 mẫu và 20 input features, cùng các bản 10% để thử nghiệm nhanh [2].

Dataset có categorical, binary và integer features, không có missing values theo metadata UCI. Nó phù hợp để nghiên cứu class imbalance, calibration và sự khác biệt giữa random split với chronological/rolling split. Nên báo ROC-AUC, PR-AUC, log loss, Brier score và calibration curve.

`duration` là caveat lớn: đây là thời lượng của cuộc gọi hiện tại. Nếu mục tiêu là dự đoán trước khi gọi, giữ `duration` có thể gây leakage hoặc làm thay đổi hoàn toàn ý nghĩa task. Vì vậy nên định nghĩa hai task riêng: post-contact prediction có `duration`, và pre-contact targeting loại `duration`. Không nên dùng accuracy đơn lẻ vì lớp positive ít.

### 2.3. Breast Cancer Wisconsin (Diagnostic)

Breast Cancer Wisconsin (Diagnostic), hay WDBC, có 569 mẫu và 30 features số được trích xuất từ ảnh fine-needle aspirate. Target là chẩn đoán benign hoặc malignant. UCI ghi không có missing values; file `wdbc.data` khoảng 121.2 KB và archive khoảng 50.1 KB [3].

WDBC là smoke test phù hợp nhất để kiểm tra pipeline TabM trong thời gian rất ngắn. Có thể bắt đầu bằng Logistic Regression hoặc linear SVM, MLP, TabM-mini và TabM. Vì số mẫu nhỏ, nên dùng repeated stratified cross-validation hoặc nested cross-validation thay vì một train/test split duy nhất. Nên báo ROC-AUC, PR-AUC, sensitivity của lớp malignant, specificity, balanced accuracy và calibration.

Phải loại cột ID khỏi predictor. Các feature có tương quan mạnh, còn một seed hoặc một split có thể tạo variance lớn. Dữ liệu là feature engineering từ FNA chứ không phải ảnh bệnh lý hoàn chỉnh; kết quả trên WDBC không được diễn giải như hiệu năng lâm sàng hay generalization sang bệnh viện khác.

### 2.4. Wine Quality

Wine Quality gồm hai file về vang đỏ và vang trắng Vinho Verde. UCI hiển thị 4,898 instances và 11 features cho record chính; file white khoảng 258.2 KB, file red khoảng 82.2 KB và archive khoảng 89.2 KB [4]. Target `quality` là điểm cảm quan từ 0 đến 10, có thứ tự và mất cân bằng. Dataset có thể dùng cho regression hoặc classification.

Đây là dataset nhẹ để kiểm tra TabM regression, normalization, seed variance và ảnh hưởng của ensemble. Nên chạy riêng red/white trước, sau đó mới thử pooled dataset. Với regression, báo RMSE, MAE và R²; với bài toán ordinal classification, dùng macro-F1 hoặc balanced accuracy và ghi rõ mapping lớp.

Không nên gộp red và white rồi coi đó là cùng một task nếu không đưa loại rượu vào thiết kế. Bài gốc của Cortez et al. dùng các metric và protocol khác với nhiều benchmark TabM hiện đại, nên không so sánh trực tiếp một con số RMSE của TabM với MAD hoặc accuracy của bài gốc. Target cực trị hiếm cũng khiến accuracy dễ gây hiểu nhầm.

### 2.5. Bike Sharing

Bike Sharing chứa số lượt thuê xe theo giờ và theo ngày trong hệ thống Capital Bikeshare, cùng thông tin mùa, thời tiết và lịch. UCI ghi 17,389 instances và 13 features; file `hour.csv` khoảng 1.1 MB, `day.csv` khoảng 56.2 KB và archive khoảng 273.4 KB [5].

Đây là dataset phù hợp nhất trong nhóm sáu bộ cho forecasting theo thời gian. Task cơ bản là dự báo `cnt`. Cần loại `casual` và `registered` khỏi input vì tổng của hai cột này bằng `cnt`; `instant` cũng là ID và không nên dùng như feature. Có thể bắt đầu với split theo thời gian, sau đó dùng rolling-origin evaluation. Báo MAE, RMSE và thêm sMAPE hoặc WAPE nếu muốn so sánh theo quy mô.

Một lưu ý về provenance: metadata UCI hiện hiển thị 17,389 instances, trong khi một số bản trích xuất hoặc README cũ có thể ghi 17,379 dòng trong `hour.csv`. Pipeline nên kiểm đếm file thực tế, ghi checksum và giữ nguyên caveat này. Không được random-shuffle toàn bộ dữ liệu nếu mục tiêu là kiểm tra forecast trong tương lai.

### 2.6. Heart Disease

Heart Disease gồm các database Cleveland, Hungary, Switzerland và VA Long Beach. UCI ghi 303 instances, 13 features dùng trong các thí nghiệm phổ biến, mixed categorical/integer/real features và missing values. Archive chính khoảng 125.9 KB [6]. Target nguyên bản `num` có giá trị 0–4; nhiều nghiên cứu nhị phân hóa thành 0 so với 1–4.

Dataset này phù hợp để kiểm tra imputation, repeated stratified cross-validation, calibration và độ nhạy với target mapping. Cần fit imputer và scaler bên trong mỗi training fold. Báo ROC-AUC, PR-AUC, sensitivity, specificity, balanced accuracy và Brier score.

Cần ghi rõ dùng bản Cleveland processed hay gộp nhiều database. Nếu gộp các site, random split có thể che giấu domain shift. Đây là dữ liệu chẩn đoán trên nhóm bệnh nhân lịch sử; không nên diễn giải kết quả như mô hình risk prediction cho dân số hiện đại.

## 3. Dataset forecasting nâng cao được giữ lại: FreshRetailNet-50K

FreshRetailNet-50K là dataset nhiều chuỗi cho bán lẻ hàng tươi sống, có doanh số theo ngày, hồ sơ theo giờ, promotion, weather, cờ hoạt động và nhãn stockout. Dataset card cung cấp bản dữ liệu khoảng 4.5 triệu dòng train và 350 nghìn dòng evaluation, với lịch sử khoảng 90 ngày train và 7 ngày đánh giá; bài báo giới thiệu task latent-demand recovery và forecasting dưới doanh số bị kiểm duyệt [7][8].

Dataset này có giá trị nghiên cứu cao hơn sáu bộ nhẹ khi câu hỏi thực sự là demand forecasting, nhưng chi phí xử lý cao hơn. Nên khóa một subset theo số chuỗi, báo rõ cách lấy mẫu, dùng split train/evaluation có sẵn và không trộn các ngày tương lai vào feature. Cần phân biệt observed sales với latent demand, đồng thời xử lý stockout như censoring chứ không tự động xem là nhu cầu bằng 0.

## 4. So sánh và khuyến nghị lựa chọn

| Góc nhìn | Sáu dataset nhẹ | FreshRetailNet-50K |
|---|---|---|
| Mục tiêu chính | Học TabM, preprocessing, baseline, calibration | Demand forecasting nhiều chuỗi và censored demand |
| Tần suất | Chủ yếu không phải time series; Bike theo giờ/ngày | Ngày + hồ sơ theo giờ |
| Quy mô | 303–48,842 dòng; tải KB đến MB | Hàng triệu dòng, nhiều chuỗi |
| Categorical | Adult, Bank, Heart, Bike | Có metadata cửa hàng/sản phẩm và cờ hoạt động |
| Missing/censoring | Adult/Heart có missing; không có stockout label | Có stockout/censored demand |
| Compute | CPU hoặc Colab phù hợp | Nên bắt đầu bằng subset |
| Rủi ro chính | Overfitting, split không phù hợp, target mapping | Leakage theo thời gian, censoring, version/schema |
| Giá trị cho người mới | Rất cao | Trung bình; nên làm sau smoke test |

### Thứ tự đề xuất

1. **WDBC** hoặc **Heart Disease**: kiểm tra pipeline trong thời gian ngắn.
2. **Wine Quality**: thử regression và target ordinal.
3. **Adult**: mixed-type, missing values và metric xác suất.
4. **Bank Marketing**: imbalance, calibration và feature availability.
5. **Bike Sharing**: chuyển sang temporal split và forecasting thực sự.
6. **FreshRetailNet-50K**: chạy subset sau khi pipeline đã tái lập.

## 5. Protocol tối thiểu cho TabM

### Bước 1 — Khóa provenance

Lưu URL, DOI, dataset ID, ngày tải, checksum, phiên bản package và mapping target. Với UCI, ưu tiên record chính thức và `ucimlrepo` hoặc archive download chính thức.

### Bước 2 — Chọn baseline

Tối thiểu gồm một baseline đơn giản phù hợp task, MLP, TabM-mini, TabM và một GBDT như CatBoost hoặc LightGBM. Giữ preprocessing, split và metric nhất quán.

### Bước 3 — Chia dữ liệu đúng task

- WDBC, Heart, Adult và Bank: stratified repeated CV hoặc fixed stratified split; preprocessing fit trong training fold.
- Wine: tách red/white; ghi rõ regression hay ordinal classification.
- Bike: temporal split hoặc rolling-origin; không random-shuffle trước split.
- FreshRetailNet-50K: giữ train/eval chronology và khóa subset.

### Bước 4 — Ngân sách và metric

Bắt đầu với 5 seed cho pilot; nếu muốn so sánh gần protocol của paper TabM, tăng lên 15 seed. Báo mean ± standard deviation hoặc confidence interval, không chỉ best run. Ghi wall-clock, số tham số, peak memory và failed/OOM run.

- Classification: ROC-AUC, PR-AUC, log loss; thêm macro-F1/balanced accuracy khi lệch lớp.
- Regression: RMSE, MAE và R²; với Bike có thể thêm sMAPE/WAPE nhưng phải định nghĩa zero handling.
- Forecasting nhiều chuỗi: báo metric theo chuỗi và metric tổng hợp, tránh để chuỗi lớn nhất chi phối toàn bộ kết luận.

### Bước 5 — Ablation rẻ nhưng có giá trị

1. TabM-mini so với TabM, giữ mọi thứ khác cố định.
2. Số nhánh nhỏ so với `k=32`, nếu compute cho phép.
3. Random split so với domain-aware/temporal split trên Bank hoặc Bike.
4. Calibration sau huấn luyện trên Adult, Bank hoặc Heart.

### Bước 6 — Không overclaim

Sáu dataset nhẹ không đủ để kết luận TabM tốt hơn GBDT trong demand forecasting. Một kết luận hợp lệ hơn là: “Trong protocol X trên dataset Y, TabM có metric và chi phí như sau.” Chỉ tuyên bố tổng quát sau khi mở rộng số dataset, audit leakage và cân bằng tuning budget.

## 6. Research directions nhỏ, phù hợp người mới

- **TabM trên WDBC và Heart Disease:** repeated nested CV, so sánh TabM-mini/TabM và calibration.
- **TabM trên Adult:** ảnh hưởng của categorical encoding, missing-value policy và số nhánh `k`.
- **Bank Marketing:** `duration` có/không có, random split so với chronological split, đánh giá PR-AUC và calibration.
- **Wine Quality:** red/white/pooled, regression so với ordinal classification, ablation normalization.
- **Bike Sharing:** random split so với temporal split; kiểm tra drift từ 2011 sang 2012 và so sánh MLP/TabM/GBDT.
- **Transfer từ bảng nhỏ sang demand forecasting:** dùng sáu dataset để kiểm tra pipeline và FreshRetailNet-50K để kiểm tra khả năng mở rộng; báo đây là hai nhóm task khác nhau.

## Tài liệu tham khảo

[1] B. Becker and R. Kohavi, “Adult,” UCI Machine Learning Repository, 1996. DOI: [10.24432/C5XW20](https://doi.org/10.24432/C5XW20). Dataset: https://archive.ics.uci.edu/dataset/2/adult.

[2] S. Moro, P. Rita, and P. Cortez, “Bank Marketing,” UCI Machine Learning Repository, 2012/2014. DOI: [10.24432/C5K306](https://doi.org/10.24432/C5K306). Dataset: https://archive.ics.uci.edu/dataset/222/bank+marketing.

[3] W. Wolberg, O. Mangasarian, N. Street, and W. Street, “Breast Cancer Wisconsin (Diagnostic),” UCI Machine Learning Repository, 1995/1993. DOI: [10.24432/C5DW2B](https://doi.org/10.24432/C5DW2B). Dataset: https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic.

[4] P. Cortez, A. Cerdeira, F. Almeida, T. Matos, and J. Reis, “Wine Quality,” UCI Machine Learning Repository, 2009. DOI: [10.24432/C56S3T](https://doi.org/10.24432/C56S3T). Dataset: https://archive.ics.uci.edu/dataset/186/wine+quality.

[5] H. Fanaee-T, “Bike Sharing,” UCI Machine Learning Repository, 2013. DOI: [10.24432/C5W894](https://doi.org/10.24432/C5W894). Dataset: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset.

[6] A. Janosi, W. Steinbrunn, M. Pfisterer, and R. Detrano, “Heart Disease,” UCI Machine Learning Repository, 1988/1989. DOI: [10.24432/C52P4X](https://doi.org/10.24432/C52P4X). Dataset: https://archive.ics.uci.edu/dataset/45/heart+disease.

[7] Dingdong-Inc, “FreshRetailNet-50K,” Hugging Face dataset card, 2025. https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K.

[8] Y. Wang, J. Gu, L. Long, X. Li, L. Shen, Z. Fu, X. Zhou, and X. Jiang, “FreshRetailNet-50K: A stockout-annotated censored demand dataset for latent demand recovery and forecasting in fresh retail,” arXiv:2505.16319, 2025. https://arxiv.org/abs/2505.16319.
