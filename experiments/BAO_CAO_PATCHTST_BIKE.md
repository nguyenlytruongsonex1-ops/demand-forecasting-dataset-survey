# Thực nghiệm PatchTST trên UCI Bike Sharing

**Ngày chạy:** 2026-10-22  
**Mục tiêu:** kiểm tra liệu thêm `LayerNorm` ngay sau phép chiếu tuyến tính 1D của patch có cải thiện PatchTST hay không.

## Dataset và tiền xử lý

Thực nghiệm dùng **UCI Bike Sharing**, file `hour.csv`, với mục tiêu `cnt` là số lượt thuê xe theo giờ. Dataset có 17.379 dòng quan sát trong khoảng 2011-01-01 đến 2012-12-31. Khi dựng lại lưới giờ đều, chuỗi có 17.544 mốc giờ, thiếu 165 mốc. Đây là bộ nhẹ, có mùa vụ ngày và tuần rõ, phù hợp để chạy nhanh trên CPU [1] [2].

Chỉ dùng chuỗi mục tiêu `cnt` để tách riêng ảnh hưởng của kiến trúc PatchTST. Hai cột `casual` và `registered` không được dùng vì cộng lại đúng bằng `cnt`, tức là gây rò rỉ mục tiêu theo EDA của repo. Chuỗi được chia tuần tự theo thời gian: 70% train, 10% validation và 20% test. Trung bình và độ lệch chuẩn chỉ fit trên train. Các mốc bị thiếu được forward-fill để tạo đầu vào đều; nếu nhãn trong horizon chứa mốc bị thiếu thì loại mốc đó khỏi metric. Vì vậy metric được tính trên 82.704 giá trị nhãn quan sát.

Mỗi mẫu dùng 168 giờ lịch sử để dự báo trực tiếp 24 giờ tiếp theo. Hai baseline là dự báo lặp giá trị cuối cùng (`naive_last`) và lặp 24 giờ gần nhất (`seasonal_naive_24`).

## Cấu hình mô hình

PatchTST nhỏ dùng patch dài 24 giờ, stride 24, `d_model=32`, 2 Transformer encoder layers, 4 heads, feed-forward size 64, dropout 0,1, AdamW learning rate `1e-3`, batch size 128, tối đa 15 epoch và early stopping patience 4.

- `patchtst`: `Linear(patch_len, d_model)` rồi vào Transformer.
- `patchtst_ln`: `Linear(patch_len, d_model) → LayerNorm(d_model)` rồi vào Transformer.

Hai biến thể dùng cùng split, optimizer, số epoch tối đa và ba seed `13, 42, 2026`. `patchtst` có 23.512 tham số; `patchtst_ln` có 23.576 tham số.

## Kết quả test

| Mô hình | MAE ↓ | RMSE ↓ | sMAPE (%) ↓ | MASE ↓ |
|---|---:|---:|---:|---:|
| Naive last | 225,40 | 296,37 | 102,16 | 3,986 |
| Seasonal naive 24 | 79,28 | 133,18 | 43,53 | 1,402 |
| PatchTST, trung bình 3 seed | **55,79 ± 0,01** | **85,35 ± 0,14** | 44,80 ± 0,99 | **0,987 ± 0,000** |
| PatchTST + LayerNorm, trung bình 3 seed | 57,88 ± 0,38 | 88,09 ± 0,40 | **42,70 ± 0,05** | 1,024 ± 0,007 |

So với seasonal-naive, PatchTST gốc giảm MAE 29,6%, RMSE 35,9% và MASE 29,6%. Bản có LayerNorm giảm MAE 27,0% và RMSE 33,9%, nhưng sMAPE tốt hơn 1,9%. Kết quả này cho thấy LayerNorm sau linear projection **không cải thiện các metric chính trên cấu hình và dataset này**; PatchTST gốc thắng rõ ở MAE, RMSE và MASE. LayerNorm chỉ có tín hiệu có lợi trên sMAPE, nên chưa đủ cơ sở để chọn nó làm mặc định.

Kết quả giữa ba seed khá ổn định: độ lệch chuẩn MAE của PatchTST gốc chỉ 0,01, còn bản LayerNorm là 0,38. Cả hai mô hình đều tốt hơn seasonal-naive theo sai số tuyệt đối và RMSE, vì vậy baseline mùa vụ vẫn là mốc cần giữ trong các thí nghiệm tiếp theo.

## Tái chạy

Từ thư mục gốc repo:

```bash
python3 eda/scripts/download_data.py
python3 experiments/run_patchtst_bike.py --epochs 15 --seeds 13 42 2026 --threads 2
```

Script ghi kết quả vào:

- `experiments/results/bike_patchtst_results.csv`: bảng kết quả theo model và seed.
- `experiments/results/bike_patchtst_results.json`: cấu hình, split, preprocessing, lịch sử train và kết quả đầy đủ.
- `experiments/results/run.log`: log lần chạy đã thực hiện.

## Hạn chế cần lưu ý

Đây là ablation nhỏ trên univariate `cnt`, không dùng biến thời tiết hay lịch. Vì vậy kết luận chỉ áp dụng cho cấu hình nhanh này, chưa phải kết luận tổng quát về mọi dataset hoặc mọi PatchTST. Bước tiếp theo hợp lý là giữ nguyên split và thêm covariates hợp lệ, sau đó kiểm tra LayerNorm trên Beijing PM2.5 để xem lợi ích sMAPE có lặp lại hay không.

## Tài liệu tham khảo

[1]: https://archive.ics.uci.edu/dataset/275 "UCI Bike Sharing dataset"

[2]: https://doi.org/10.24432/C5W894 "Bike Sharing dataset citation"
