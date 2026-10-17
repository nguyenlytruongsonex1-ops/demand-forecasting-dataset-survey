# Proposal Spec — VANGUARD

**Status:** `draft` / `review` / `accepted` / `blocked`
**Strategist:** [ ]  **Coordinator:** [ ]  **Ngày:** [YYYY-MM-DD]
**Dự kiến:** 4–6 tuần
**Evidence ledger:** [link/path]

## Title

**[Tiêu đề cụ thể, không overclaim novelty]**

## Introduction

- **Problem/context:** [hiện tượng, đối tượng, domain và tại sao đáng giải quyết]
- **Known evidence:** [paper/dataset/result IDs; Verified vs Inference]
- **Gap:** [điều literature chưa giải quyết/chưa kiểm chứng; scope rõ]
- **Research question (RQ):** [câu hỏi đo/kiểm chứng được]
- **Relevance:** [ai dùng kết quả, ý nghĩa khoa học/thực hành]
- **Constraints:** [data, compute, license/privacy, venue, 4–6 tuần]

## Objectives

- **Mục tiêu chung (1):** [một câu mô tả outcome nghiên cứu]
- **Mục tiêu cụ thể 1 (2):** [method/analysis có metric và acceptance condition]
- **Mục tiêu cụ thể 2 (3):** [experiment/comparison/robustness có metric và acceptance condition]

## Novelty / Feasibility / Relevance decision

| Trục | Bằng chứng/giả định | Điểm hoặc đánh giá | Risk | Mitigation/test |
|---|---|---|---|---|
| Novelty | [ ] | [ ] | [ ] | [ ] |
| Feasibility 4–6 tuần | [ ] | [ ] | [ ] | [ ] |
| Relevance | [ ] | [ ] | [ ] | [ ] |

**Quyết định chọn đề tài:** [choose/revise/reject + reason; không gọi inference là fact]

## Methodology

1. **Dataset/provenance:** [link tới dataset handoff, license, version, target]
2. **Preparation:** [cleaning, missingness, normalization/standardization, encoding, visualization]
3. **Split/protocol:** [time/group/random; split trước fit transform; horizon; leakage controls]
4. **Methods/architectures:** [baseline + model(s), assumptions, hyperparameters]
5. **Experiment design:** [ablation/comparison/robustness, seeds, config, environment]
6. **Metrics:** [định nghĩa, đơn vị, aggregation, uncertainty/variance]
7. **Evidence plan:** [claim → evidence ID/result artifact]
8. **Ethics/data governance:** [authorship, license, privacy/consent, bias, integrity, submission]

## Timeline và gates

| Tuần | Pha | Deliverable | Gate/owner | Exit criterion |
|---|---|---|---|---|
| 1 | Topic/literature | RQ, paper summaries, gap | G0–G1 / [ ] | [ ] |
| 2 | Method/proposal | Proposal Spec, protocol | G2 / [ ] | [ ] |
| 3 | Dataset/preparation | Dataset handoff, preprocessing | G3–G4 / [ ] | [ ] |
| 4 | Experiment/analysis | Baseline, runs, results | G5 / [ ] | [ ] |
| 5 | Draft | IEEE IMRaD, figures/tables | G6 / [ ] | [ ] |
| 6 | Revision/submission/presentation | final + deck | G7–G8 / [ ] | [ ] |

## Outcomes

- **Expected scientific outcome:** [ ]
- **Expected artifact:** [code/config/report/figure; không raw data]
- **Success criteria:** [RQ/objective → metric/threshold hoặc qualitative criterion]
- **Limitations/negative outcomes accepted:** [ ]
- **Publication/presentation target:** [venue/format; không nộp trùng]
- **Future work:** [chỉ nêu hướng có căn cứ]

## Review and approval

- [ ] Intel xác nhận literature, source label, summary đúng 3 câu và gap.
- [ ] Scout xác nhận dataset handoff; Engineer xác nhận protocol/leakage/reproducibility.
- [ ] Scribe xác nhận cấu trúc IEEE, claim-evidence map và citation plan.
- [ ] Ethics gate và reproducibility gate có owner; unresolved finding có deadline.

**Strategist sign-off:** [tên/ngày]
**Coordinator decision:** `accepted` / `revise` / `blocked` — [lý do]
