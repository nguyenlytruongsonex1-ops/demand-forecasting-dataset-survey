# Research Standard của VANGUARD

Tài liệu này là chuẩn tối thiểu cho mọi đề tài do VANGUARD điều phối. Khi một quyết định chưa đạt chuẩn, ghi rõ `blocked`, owner và bước xử lý tiếp theo thay vì suy diễn.

## 1. Mạch nghiên cứu và tiêu chí đề tài

Mọi project phải đi theo mạch:

> **Problem → Literature → Gap → Method → Experiment → Results → Publication**

- **Problem:** nêu hiện tượng, đối tượng, phạm vi, constraint và vì sao đáng giải quyết.
- **Literature:** tìm kiếm có chiến lược, ưu tiên nguồn đáng tin và ghi truy xuất/citation.
- **Gap:** đối chiếu các paper để chỉ ra điều chưa biết, chưa kiểm chứng hoặc chưa phù hợp; phân biệt fact với inference.
- **Method:** mô tả phương pháp đủ chi tiết để người khác tái lập.
- **Experiment:** đặt baseline, split đúng, metric và protocol trước khi xem kết quả.
- **Results:** báo cáo số liệu, uncertainty/variance khi có thể, failure case và giới hạn; không cherry-pick.
- **Publication:** viết, trích dẫn, review, kiểm tra ethics và chuẩn bị submission/presentation.

Chọn topic bằng ba trục:

- **Novelty:** đóng góp mới có thể phát biểu và kiểm chứng, không chỉ đổi tên mô hình.
- **Feasibility:** có thể hoàn thành trong **4–6 tuần** với dữ liệu, compute, kỹ năng và nguồn lực thật.
- **Relevance:** gắn với RQ, domain và venue/đối tượng đọc; nêu rõ ai được lợi từ kết quả.

Nếu thiếu một trục, Strategist phải ghi lý do chọn/reject và điều kiện giảm rủi ro.

## 2. Literature và paper

Ưu tiên tìm paper qua **IEEE Xplore, ACM Digital Library, SpringerLink**; dùng **arXiv, ResearchGate, Unpaywall** để tiếp cận bản open access khi phù hợp. Một paper được xem là đã đọc có kiểm soát sau khi xem title, abstract, keywords, figures, conclusion/future work và phần phương pháp/kết quả liên quan; không chỉ dựa vào abstract hoặc snippet.

Mỗi paper trong handoff phải có:

- citation đầy đủ, DOI/URL và **source label** (publisher, preprint, repository hoặc secondary source);
- summary **đúng 3 câu**: (1) problem, (2) main result, (3) future work;
- method, dataset, metric, limitation, gap liên quan;
- nhãn `Verified` cho điều được paper/nguồn xác nhận và `Inference` cho diễn giải của nhóm.

Đọc theo **IMRaD** (Introduction, Methods, Results, Discussion), xem figure/table để kiểm tra claim và đối chiếu conclusion/future work với mục tiêu ban đầu. Không gọi một kết quả là novelty nếu chưa so với literature gần nhất.

## 3. Proposal và viết IEEE

Proposal tối thiểu có: **Title, Introduction, Objectives (1 mục tiêu chung + 2 mục tiêu cụ thể), Methodology, Timeline, Outcomes**. Template dùng tại [templates/proposal.md](templates/proposal.md).

Bài IEEE dùng cấu trúc:

1. Abstract **150–250 từ**.
2. **3–5 keywords**.
3. Introduction.
4. Related Work.
5. Methodology.
6. Results & Discussion.
7. Conclusion & Future Work.

Dùng Overleaf/template IEEE và BibTeX khi phù hợp. Mỗi claim phải nối được với citation, dataset provenance hoặc experiment evidence; figure/table phải có caption, đơn vị, split và nguồn. Abstract chỉ nêu điều đã chứng minh trong bài, không hứa hẹn beyond evidence.

## 4. Dataset và thực nghiệm

Dataset handoff phải đủ năm bước trong [dataset-handoff.md](templates/dataset-handoff.md): thông tin và nguồn; fit với RQ/constraint và reason choose/reject; code load/download cùng preprocessing/cleaning/visualization; report/provenance/citation/issues; methods/baseline/papers/results/metrics. Repository không chứa raw data hay archive.

Engineer phải:

- split theo thời gian hoặc protocol phù hợp **trước** khi fit transform;
- fit imputer, scaler, encoder, feature selector và mọi transform học từ dữ liệu chỉ fit trên train; áp dụng frozen transform cho validation/test;
- ngăn target leakage, temporal leakage và duplicate leakage; nêu explicit forecast horizon và thông tin nào có sẵn tại thời điểm dự báo;
- lưu seed, config, environment/dependency versions, commit SHA, data provenance và command tái chạy;
- báo cáo baseline, metric, đơn vị, aggregation, uncertainty/seed variance và failure cases.

## 5. Ethics và integrity

- **Authorship:** dựa trên đóng góp thực tế; ghi credit cho dữ liệu, công cụ và hỗ trợ; không guest/ghost authorship.
- **Đạo văn:** diễn đạt lại có citation, trích dẫn nguyên văn có dấu rõ ràng; không tái sử dụng bài mà không khai báo.
- **Data integrity:** không bịa, xóa hoặc cherry-pick dữ liệu/kết quả; lưu log thay đổi và giải thích exclusion/imputation.
- **Privacy/consent:** kiểm tra license, PII, quyền sử dụng, consent và yêu cầu de-identification trước khi dùng/đăng dữ liệu.
- **Bias:** xác định subgroup, nguồn sampling bias và giới hạn khả năng khái quát; không phóng đại fairness.
- **Minh bạch/citation:** nêu provenance, preprocessing, code/data availability và limitation; cite đúng nguồn.
- **Submission:** không nộp trùng hoặc gửi đồng thời nếu venue không cho phép; khai báo preprint/overlap.

Ethics gate phải pass trước submission; vấn đề unresolved chuyển thành blocker, không ẩn trong footnote.

## 6. Bảy pha bắt buộc

1. **Topic/literature:** Problem, RQ, search log, paper summaries, gap.
2. **Method/proposal:** novelty/feasibility/relevance, proposal Spec, protocol và timeline.
3. **Dataset/preparation:** handoff, provenance, cleaning, split, risk/leakage review.
4. **Experiment/analysis:** baseline, config, seeds, metrics, results, failure cases.
5. **Draft:** IEEE IMRaD, abstract, keywords, figures/tables, citations/BibTeX.
6. **Final revision/submission:** review, ethics/reproducibility gates, venue checks, no duplicate submission.
7. **Presentation:** narrative Problem→Gap→Method→Evidence→Limitations, slide/source check và Q&A.

Pha chỉ đóng khi [workflow.md](workflow.md) quy định gate đã pass.
