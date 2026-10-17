# Multi-agent workflow

Use this sequence for engineering work. Do not skip a gate or let one agent approve its own work.

**Read-only analysis → implementation on feature branch and PR → independent testing → independent fresh-context review → resolve every finding → rerun impacted tests → reviewer recheck → merge gate.**

## 1. Read-only analysis

The codebase-analysis agent inspects the requested surface without editing, generating, downloading, or mutating the checkout. It reads repository conventions, data/report/notebook behavior, Git state, and available tooling, then produces evidence paths, risks, non-goals, acceptance criteria, and a validation plan. See [roles/codebase-analysis.md](roles/codebase-analysis.md).

The analysis must anchor to the intended checked-out base. The current project scope is **Bike Sharing + Beijing PM2.5**; `origin/replace-pm25-with-tetouan` is an alternate remote branch, not the current dataset convention.

## 2. Implement on a branch and open a PR

The implementation agent starts from the approved base, creates/uses a feature branch, makes the smallest change, and opens a PR. It never edits or merges `main` directly. The PR links the analysis evidence, states files and assumptions, identifies expected generated-artifact changes, and records exact validation commands. For this playbook addition, only these exactly seven Markdown files are in scope: `.agent-org/README.md`, `.agent-org/pr-checklist.md`, `.agent-org/workflow.md`, `.agent-org/roles/code-review.md`, `.agent-org/roles/codebase-analysis.md`, `.agent-org/roles/implementation.md`, and `.agent-org/roles/testing.md`; do not change source, data, notebooks, reports, or generated outputs. See [roles/implementation.md](roles/implementation.md).

Preserve UCI citations, raw-data ignore policy, Vietnamese project terminology, and the existing two-dataset naming. If a future change touches analysis logic, explicitly inspect target leakage (`casual`/`registered` for Bike), temporal leakage, time-series split discipline, train-only preprocessing, missing values, reproducibility, and artifact drift.

## 3. Test independently

A testing agent, who is not relying only on the implementation author's claims, uses a clean/independent checkout of the PR branch. It records exact commands, environment, network availability, destructive operations avoided or performed in isolation, and pass/fail evidence. There is no configured pytest, lint, type-check, or CI workflow; do not report success for tools that were not separately introduced and run. See [roles/testing.md](roles/testing.md).

### Baseline checks

These checks are repository-grounded and safe when run from the checkout. Before the PR-diff check, fetch and verify that `origin/main` is the intended PR base; the fetch needs network access, while the status and subsequent checks are local:

```bash
git status --short --branch
git fetch origin main
git rev-parse --verify origin/main
git diff --check origin/main...HEAD
python3 - <<'PY'
import json, pathlib
root = pathlib.Path('.')
for p in sorted((root/'eda/notebooks').glob('*.ipynb')):
    d = json.loads(p.read_text())
    assert d['nbformat'] == 4
    for i, cell in enumerate(d['cells']):
        src = cell.get('source', '')
        src = ''.join(src) if isinstance(src, list) else src
        if cell.get('cell_type') == 'code':
            compile(src, f'{p}:cell-{i}', 'exec')
for p in [root/'eda/reports/summary_bike.json', root/'eda/reports/summary_pm25.json']:
    json.loads(p.read_text())
print('static validation passed')
PY
python3 -m pip install -r eda/requirements.txt
```

The JSON/code-cell block validates notebook structure, compiles every code cell, and parses both summary JSON files. Installing `eda/requirements.txt` is environment-changing and commonly network-dependent; do not run it for this documentation-only PR unless the independent tester needs it, and record the result.

### Optional execution validation (isolated and network-dependent)

Full notebook execution needs dependencies and raw UCI data. `python3 eda/scripts/download_data.py` downloads archives into ignored `eda/data/raw/` and is network-dependent. Run it only when relevant, never commit the result, and report network availability. `build_notebooks.py` is also destructive **if run in place** because it rewrites checked-in notebooks without outputs; run it only when regeneration is part of the change, preferably in an isolated copy, then inspect and intentionally preserve/recreate executed outputs.

Use an isolated copy/worktree for execution because notebooks write `eda/reports/summary_*.json`, and respect the `eda/notebooks` working-directory assumption:

```bash
python3 eda/scripts/download_data.py
python3 eda/scripts/build_notebooks.py   # only when regeneration is part of the change
mkdir -p /tmp/demand-forecasting-executed
cd eda/notebooks
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=300 \
  --output-dir /tmp/demand-forecasting-executed eda_01_bike_sharing.ipynb
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=300 \
  --output-dir /tmp/demand-forecasting-executed eda_02_beijing_pm25.ipynb
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=300 \
  --output-dir /tmp/demand-forecasting-executed eda_03_so_sanh_va_tien_xu_ly.ipynb
```

The commands above are network-dependent through data download and dependency availability; notebook execution writes outputs in the isolated output directory but the notebooks also write summary JSON side effects, so do not execute against the working tree unless that overwrite is intentional and reviewed.

## 4. Independent fresh-context review

A non-implementer and non-testing-approver reviews the PR diff from a fresh context/checkout. The reviewer checks the analysis, scope, citations, generated artifacts, working directory, data leakage, missing-value handling, time-series splits, reproducibility, and test evidence. Findings are classified as blocking or non-blocking and cite a file/line or notebook cell. See [roles/code-review.md](roles/code-review.md).

## 5. Resolve every finding

The implementation agent responds to every finding. Each is resolved by a follow-up commit with a concise explanation, or by a rationale explicitly accepted by the reviewer. Pushing a new commit does not itself close a finding. No unresolved finding may pass the gate.

## 6. Rerun impacted tests, then reviewer recheck

After review fixes, the independent testing agent reruns every impacted check (and the full notebook sequence for notebook/dependency changes), records new evidence, and confirms no unwanted artifacts appeared. The reviewer then rechecks each requested change and explicitly confirms the resolutions. New findings return to step 5.

## 7. Merge gate

Merge only through the PR after all applicable checklist items are complete: analysis evidence linked; intended branch confirmed; no raw/generated unwanted artifacts; exact tests recorded; independent tester approval; independent reviewer approval; every finding resolved; impacted tests rerun; reviewer recheck complete; and the final base-aware PR-diff check `git diff --check origin/main...HEAD` (after fetching and verifying `origin/main`) plus status/diff inspection pass. Branch protection or CI may later enforce these rules, but neither currently exists and must not be implied.
