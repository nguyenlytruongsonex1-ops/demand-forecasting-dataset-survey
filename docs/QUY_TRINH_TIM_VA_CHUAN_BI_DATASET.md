# Quy trình tìm và chuẩn bị dataset

Tài liệu này được chuẩn hóa từ file mẫu `2.Dataset_1.pdf` do người dùng cung cấp. Mọi báo cáo khảo sát dataset trong repository phải kiểm tra đủ năm bước sau.

## 1. Thông tin dataset

Phải ghi rõ tên dataset, nguồn và link chính thức, lĩnh vực hoặc bài toán, số lượng mẫu, input dimension, số lớp hoặc target, kiểu dữ liệu, train/validation/test split, kích thước tệp và các vấn đề cần xử lý.

Với time series, cần ghi thêm tần suất, khoảng thời gian, số series, horizon dự kiến và timestamp có liên tục hay không.

## 2. Đánh giá độ phù hợp

Phải đối chiếu dataset với research question và điều kiện bắt buộc của đề tài. Các tiêu chí tối thiểu gồm số lượng mẫu, input dimension, kiểu dữ liệu, classification/regression, target, khả năng triển khai và lý do chọn hoặc loại dataset.

Nếu dataset chỉ phù hợp với một bài toán gần với đề tài, phải ghi rõ giới hạn đó thay vì gọi là phù hợp tuyệt đối.

## 3. Code xử lý dataset

Phải có hoặc chỉ rõ code cho download/load, preprocessing, cleaning, missing values, normalization/standardization, encoding labels hoặc time features, train/validation/test split và visualization.

Các bước có nguy cơ leakage phải được kiểm soát: scaler chỉ fit trên train; split theo thời gian; các cột là thành phần của target phải loại khỏi input; thông tin tương lai chỉ được dùng nếu thật sự có tại thời điểm dự báo.

## 4. Nội dung cần ghi vào paper/report

Báo cáo phải có dataset description, dataset statistics, nguồn dữ liệu, preprocessing, data split, visualization/EDA, đặc điểm hoặc vấn đề quan trọng và citation/reference.

Số liệu trong báo cáo phải truy được về code hoặc file dữ liệu. Nếu metadata của nguồn chính thức khác với số dòng thực tế trong CSV, phải ghi rõ cả hai và giải thích số nào được dùng trong thực nghiệm.

## 5. Phương pháp đã áp dụng trên dataset

Phải khảo sát các phương pháp Machine Learning, Deep Learning/Neural Networks và kiến trúc phổ biến đã được áp dụng trên dataset hoặc bài toán tương đương. Cần tổng hợp thiết kế thí nghiệm, metric, kết quả được công bố, paper tiêu biểu và baseline phù hợp cho nghiên cứu mới.

Không được dùng kết quả của một paper khác như kết quả của thực nghiệm hiện tại. Phải phân biệt rõ kết quả đã công bố, kết quả EDA nội bộ và kết quả sẽ chạy trong project.
