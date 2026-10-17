# Dataset Handoff — VANGUARD

**Dataset:** [tên]
**Scout:** [tên]
**Engineer nhận:** [tên]
**Ngày/version:** [YYYY-MM-DD / version]
**Trạng thái:** `draft` / `review` / `accepted` / `blocked`

## Bước 1 — Thông tin dataset

- **Tên và official link:** [ ]
- **Domain/task:** [ ]
- **Sample count:** [ ]
- **Input dimension:** [ ]
- **Classes/target:** [ ]
- **Data type:** [tabular/time series/image/text/khác]
- **Train/validation/test split gốc:** [ ]
- **Kích thước:** [dung lượng, số file; không commit file dữ liệu]
- **License/provenance/version:** [ ]
- **Issues:** [missingness, duplicates, imbalance, drift, label noise, access/privacy]
- **Citation/BibTeX:** [ ]

## Bước 2 — Fit với RQ và constraints

- **RQ/objective liên quan:** [ ]
- **Fit:** [task, target, horizon, sample size, compute, timeline 4–6 tuần]
- **Constraints:** [license, privacy/consent, label availability, reproducibility]
- **Reason choose:** [evidence]
- **Reason reject (nếu reject):** [evidence]
- **Risks và mitigation/test:** [ ]
- **Quyết định:** `choose` / `reject` / `needs evidence`

## Bước 3 — Load, preprocessing và kiểm tra

- **Code load/download entrypoint:** `[path/command]` (chỉ tải từ official source; không lưu raw data vào repo)
- **Cleaning:** [duplicates, invalid rows, outlier policy]
- **Missing:** [location, mechanism/assumption, imputation/mask/drop; train-only fitting]
- **Normalization/standardization:** [transform, chỉ fit trên train]
- **Encoding:** [categorical/text/temporal]
- **Split:** [time/group/random; split trước mọi transform; horizon]
- **Leakage checks:** [target/temporal/duplicate/exogenous availability]
- **Visualization:** [plots, aggregation, unit, output location]
- **Seed/config/environment:** [ ]

## Bước 4 — Report/provenance package

- **Content/schema:** [ ]
- **Statistics:** [count, missing, distribution, class/target balance]
- **Provenance:** [official URL, version/date/hash nếu được phép, license]
- **Preprocessing record:** [ ]
- **Split record:** [ ]
- **Visualization references:** [figure/path + interpretation]
- **Known issues/limitations:** [ ]
- **Citation/BibTeX:** [ ]
- **Reproduction command:** `[ ]`

## Bước 5 — Methods, results và baseline sơ bộ

- **Methods applied/đề xuất:** [ ]
- **ML/DL architectures:** [ ]
- **Baseline:** [naive/seasonal naive/statistical/ML; lý do]
- **Metrics và protocol:** [định nghĩa, đơn vị, aggregation, horizon]
- **Results hiện có:** [result artifact/evidence ID; không bịa số]
- **Representative papers:** [paper summary links/citations]
- **Failure cases/uncertainty:** [ ]

## Acceptance checklist

- [ ] Đủ năm bước; bước 1, 2, 5 có Scout sign-off.
- [ ] Official source, license, provenance và citation kiểm tra được.
- [ ] Fit/reject và risks có evidence.
- [ ] Split trước fit transform; leakage và privacy đã review.
- [ ] Có baseline/papers/metrics hoặc ghi rõ `blocked`.
- [ ] Không có raw data/archive/venv/bytecode/checkpoint trong repository.

**Scout sign-off:** [tên/ngày]
**Engineer sign-off:** [tên/ngày]
**Open findings/owner/deadline:** [ ]
