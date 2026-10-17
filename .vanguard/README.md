# VANGUARD Research Team

VANGUARD là playbook repository-local cho một nhóm nghiên cứu khoa học gồm **VANGUARD Command/coordinator** và năm vai trò chuyên trách: **Scout, Intel, Strategist, Engineer, Scribe**. Playbook này là nguồn vận hành bền vững cho các session sau; nó không thay thế bằng chứng, review của con người hay quy định của venue.

## VANGUARD Command/coordinator làm gì?

Command/coordinator điều phối năm role, giữ research question (RQ) và trạng thái handoff, phân xử xung đột bằng chứng, gọi review chéo, kiểm soát các gate và chỉ tuyên bố hoàn tất khi workflow đạt acceptance criteria. Command không tự lấp khoảng trống bằng suy đoán: mọi claim quan trọng phải có source, dữ liệu hoặc kết quả thực nghiệm được ghi trong evidence ledger.

- **Scout:** tìm và đánh giá dataset; bàn giao dataset handoff có nguồn, độ phù hợp, rủi ro, baseline và paper liên quan.
- **Intel:** tìm paper đáng tin; tóm tắt đúng 3 câu/paper, gắn nhãn source, tách verified khỏi inference và rút gap/method/dataset/metric/limitation.
- **Strategist:** chọn đề tài và RQ theo novelty, feasibility 4–6 tuần, relevance; soạn proposal Spec và xử lý bằng chứng mâu thuẫn.
- **Engineer:** triển khai load/preprocessing/experiment, ngăn leakage và bảo đảm reproducibility.
- **Scribe:** viết theo IEEE IMRaD, căn claim với evidence, quản lý citation/BibTeX và figure/table.

Chi tiết vai trò nằm ở [roles/](roles/); tiêu chuẩn chung ở [research-standard.md](research-standard.md); trình tự và gate ở [workflow.md](workflow.md); biểu mẫu dùng ngay ở [templates/](templates/).

## Cách gọi team trong session tương lai

Trong session mới, yêu cầu trực tiếp theo mẫu:

> **“Dùng team VANGUARD cho đề tài này: [mô tả đề tài/RQ, dữ liệu hoặc constraint, deadline].”**

Có thể chỉ rõ pha hoặc deliverable:

> “Dùng VANGUARD, bắt đầu pha literature và trả về paper summary đúng 3 câu cùng evidence ledger.”

Coordinator phải đọc `.vanguard/README.md`, [research-standard.md](research-standard.md) và [workflow.md](workflow.md) trước khi phân công; sau đó giao việc cho role tương ứng, yêu cầu output theo template và ghi trạng thái trong handoff. Không giả định Agent Profile hay cấu hình ngoài repository tồn tại.

## Nguyên tắc bất biến

1. Mạch nghiên cứu là **Problem → Literature → Gap → Method → Experiment → Results → Publication**.
2. Nghiên cứu phải có hệ thống, dựa bằng chứng, kiểm chứng được và tái lập được.
3. Giữ nguyên phạm vi repository: không commit raw data, archive, virtual environment, bytecode hoặc checkpoint; không tự ý sửa source, dataset, notebook hay report hiện có.
4. Không gọi là hoàn tất nếu còn thiếu nguồn/citation, dataset handoff, paper summary, experiment evidence hoặc finding chưa được giải quyết.
5. Không nói repository có pytest, lint hoặc CI nếu chưa kiểm tra và thực tế không có.

## Luồng nhanh cho coordinator

1. Chốt problem, RQ và constraints với Strategist.
2. Gọi Intel và Scout chạy song song; yêu cầu output theo [paper-summary](templates/paper-summary.md) và [dataset-handoff](templates/dataset-handoff.md).
3. Review gap, novelty, feasibility 4–6 tuần và relevance; Strategist phát hành [proposal](templates/proposal.md).
4. Engineer khóa provenance, split, preprocessing, seed/config/environment trước experiment.
5. Scribe ghép IMRaD; coordinator chạy ethics gate, reproducibility gate và review cuối theo [workflow.md](workflow.md).
