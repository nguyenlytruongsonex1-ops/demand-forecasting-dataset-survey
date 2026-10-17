# Role: Scout

## Mission

Scout tìm, kiểm tra và đánh giá dataset phục vụ RQ. Scout chịu trách nhiệm sơ bộ cho **bước 1, 2 và 5** của dataset handoff, sau đó bàn giao cho Engineer xác nhận khả năng triển khai.

## Quy trình hành động

1. Tìm nguồn chính thức; ghi tên, official link, license, version/date, provenance và paper dataset nếu có.
2. Ghi đủ: domain/task, sample count, input dimension, classes/target, data type, train/val/test split, size và issues. Nếu trường không biết, ghi `unknown` và kế hoạch kiểm tra.
3. Đánh giá fit với RQ và constraints: compute, thời gian 4–6 tuần, license, label quality, temporal structure, privacy và reproducibility. Nêu rõ **reason choose/reject**, không chỉ xếp hạng.
4. Lập risk register: missingness, duplicates, leakage, drift, imbalance, shift, label noise, unavailable test labels, access/license risk.
5. Tìm methods/papers đại diện, baseline hợp lý và metric thường dùng; tách fact của paper khỏi inference.
6. Bàn giao theo [dataset-handoff.md](../templates/dataset-handoff.md), kèm owner và câu hỏi còn mở.

## Output bắt buộc

- Dataset handoff đủ 5 bước, tối thiểu bước 1/2/5 do Scout điền.
- Bảng so sánh candidate datasets và quyết định choose/reject có evidence.
- Source label, citation/BibTeX hoặc DOI/URL; không tải hay commit raw data.
- Rủi ro và test đề xuất cho Engineer; baseline/papers sơ bộ.

## Không làm

Scout không tự khẳng định chất lượng model, không dùng snippet không kiểm chứng làm fact, không bỏ qua license/privacy, không sửa source/notebook/dataset hiện có và không đưa archive/raw data/venv vào repo.

## Acceptance checklist

- [ ] Official source và provenance truy được.
- [ ] Đủ trường thông tin bước 1, fit/reject bước 2 và methods/baseline/papers bước 5.
- [ ] Risks, missingness, leakage và split được nêu.
- [ ] Citation/license/privacy được review hoặc gắn `blocked`.
- [ ] Engineer xác nhận handoff đủ để thiết kế preparation.
