# VANGUARD Workflow và Gates

Coordinator quản lý một board hoặc log có các trạng thái `planned → active → review → accepted` hoặc `blocked`. Mỗi handoff phải có owner, ngày, input, output, evidence links và finding còn mở.

## Handoff gates

| Gate | Bàn giao tối thiểu | Acceptance criteria | Reviewer |
|---|---|---|---|
| G0 Topic | Problem, RQ, constraints | RQ đo/kiểm chứng được; topic đạt novelty, feasibility 4–6 tuần, relevance; scope không mơ hồ | Strategist + Command |
| G1 Literature | Paper log, summary, gap | Mỗi paper đáng tin có summary đúng 3 câu, source label, citation; gap tách `Verified`/`Inference` và có đối chiếu | Intel + Strategist |
| G2 Proposal | Proposal Spec | Có Title, Introduction, 1 objective chung, 2 objective cụ thể, Methodology, Timeline, Outcomes; method trả lời RQ | Strategist + Scribe |
| G3 Dataset | Dataset handoff 5 bước | Đủ trường, official source, license/provenance, fit/reject, risks, baseline/papers; không đưa raw data vào repo | Scout + Engineer |
| G4 Preparation | Code/protocol/config | Split trước fit transform; leakage review; cleaning/visualization và seed/config/environment/provenance ghi được | Engineer + Scout |
| G5 Experiment | Result bundle | Baseline, metric, horizon, protocol, nhiều seed hoặc lý do; artifacts/reports tái tạo được; failure cases không giấu | Engineer + Strategist |
| G6 Draft | IEEE IMRaD draft | Abstract 150–250 từ, 3–5 keywords, claim-evidence alignment, citation/BibTeX, figure/table có nguồn | Scribe + Intel |
| G7 Ethics & reproducibility | Gate records | Ethics không còn blocker; provenance, consent/privacy, authorship, no plagiarism/duplicate submission; runbook tái lập | Command + toàn team |
| G8 Submission/presentation | Bản cuối và deck | Review comment đã đóng hoặc ghi rõ accepted risk; venue requirements, references, claims và Q&A đã kiểm tra | Command |

Không được bypass gate bằng câu “sẽ bổ sung sau”. Nếu deliverable chưa đủ, trạng thái là `blocked`.

## Evidence ledger

Dùng một bảng ledger cho mọi claim quan trọng. Có thể đặt trong issue/PR hoặc phụ lục báo cáo; không commit dữ liệu nhạy cảm.

| ID | Claim/finding | Loại | Evidence/source | Vị trí/định danh | Confidence | Owner | Trạng thái |
|---|---|---|---|---|---|---|---|
| E-001 | [phát biểu kiểm chứng được] | `Verified` / `Inference` | DOI, official link, dataset, config hoặc result artifact | section/figure/commit/command | high/med/low | role | open/checked |

Quy tắc: `Verified` phải truy ngược được đến nguồn hoặc run; `Inference` phải nói rõ giả định và không được trình bày như fact. Nguồn mâu thuẫn tạo một finding riêng, ghi cả hai bằng chứng, giải thích tiêu chí ưu tiên và giữ lại limitation nếu chưa phân xử được.

## Review protocol

1. Author tự kiểm tra checklist và link tới evidence ledger.
2. Reviewer không cùng author kiểm từng RQ, dataset/provenance, method, metric, claim, figure/table và limitation.
3. Mỗi comment phân loại `blocker`, `major`, `minor`; blocker cần owner và test đóng.
4. Author phản hồi bằng thay đổi hoặc lý do; reviewer xác nhận close.
5. Command kiểm tra acceptance criteria và cập nhật gate; disagreement được ghi, không tự xóa.

Review phải tìm leakage, cherry-picking, thiếu baseline, citation không hỗ trợ claim, metric sai hướng và overclaim; không chỉ sửa ngữ pháp.

## Ethics gate

Pass chỉ khi đã kiểm tra: authorship theo đóng góp; chống đạo văn; license/provenance và data integrity; privacy/consent/PII; bias và giới hạn subgroup; citation đầy đủ; disclosure của công cụ/AI nếu venue yêu cầu; không nộp trùng. Một câu trả lời `unknown` cho privacy, license hoặc overlap là blocker cần xác minh.

## Reproducibility gate

Pass chỉ khi một reviewer khác có thể từ commit sạch và dữ liệu hợp pháp để chạy lại hoặc hiểu chính xác blocker. Handoff phải ghi: data source/version/hash nếu được phép; code entrypoint; preprocessing và split; train-only fitting; seed; config; environment/dependency versions; metric implementation; expected outputs; command/run log; limitations về nondeterminism. Không thêm raw data, archive, venv, bytecode hoặc checkpoint vào repo.

## Definition of done

Task **chưa complete** nếu thiếu bất kỳ mục nào sau đây:

- source/citation cho claim và paper summary đúng chuẩn;
- dataset handoff đầy đủ;
- experiment evidence có baseline/protocol/metric;
- finding, xung đột evidence hoặc limitation còn unresolved mà chưa có owner/quyết định;
- ethics gate hoặc reproducibility gate chưa pass.

## Pha và nhịp làm việc 4–6 tuần

- **Tuần 1:** pha 1, G0–G1; chốt RQ và literature/gap.
- **Tuần 2:** pha 2, G2; khóa proposal, protocol và risk register.
- **Tuần 3:** pha 3, G3–G4; dataset/preparation, leakage và reproducibility setup.
- **Tuần 4:** pha 4, G5; baseline, ablation/robustness phù hợp và phân tích.
- **Tuần 5:** pha 5, G6; draft IMRaD, figures/tables, evidence alignment.
- **Tuần 6:** pha 6–7, G7–G8; revision, ethics/submission và presentation.

Nếu scope lớn hơn, giảm claim hoặc tăng thời gian minh bạch; không giảm gate.
