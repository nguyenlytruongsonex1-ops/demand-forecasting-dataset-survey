# PR checklist

Copy this checklist into the PR description and check every applicable item before merge.

## Scope and analysis

- [ ] PR links the read-only codebase-analysis evidence.
- [ ] Intended base branch is confirmed as the current Bike Sharing + Beijing PM2.5 scope; the alternate `origin/replace-pm25-with-tetouan` branch was not used accidentally.
- [ ] Scope, non-goals, changed paths, assumptions, and acceptance criteria are stated.
- [ ] No direct edits or merge to `main`; all implementation work is on a feature branch through this PR.
- [ ] UCI 275 Bike Sharing and UCI 381 Beijing PM2.5 naming and UCI / CC BY 4.0 citations are preserved when relevant.

## Repository safety and artifacts

- [ ] No unwanted raw data, downloaded archives, `eda/data/` contents, virtual environments, `__pycache__`/bytecode, or notebook checkpoints are committed.
- [ ] Generated notebooks and `eda/reports/summary_*.json` changes are absent or explicitly expected, explained, and reviewed.
- [ ] `build_notebooks.py` was not run in place accidentally; if it was intentionally run, notebooks were re-executed and output/report drift was inspected.
- [ ] Notebook working-directory sensitivity (`eda/notebooks`) was respected.
- [ ] No unrelated source, data, notebook, report, or behavior changes are mixed into the PR.

## Validation evidence

- [ ] Exact commands and results are recorded for `git status --short --branch` and `git diff --check`.
- [ ] Notebook JSON structure/code-cell compilation and both summary JSON parses were run or an explicit reason is recorded.
- [ ] Dependency installation (`python3 -m pip install -r eda/requirements.txt`) is recorded when needed, including network/environment result; no configured pytest, lint, type-check, or CI is claimed.
- [ ] If relevant, isolated notebook execution evidence records raw-data download/network status, generator use, output location, and expected side effects.
- [ ] Relevant checks cover target/temporal leakage, time-series split errors, train-only missing-value preprocessing, reproducibility, and generated-artifact drift.

## Independent gates

- [ ] Independent testing agent approved with exact evidence and environment details.
- [ ] Independent fresh-context code-review agent approved; reviewer is not the implementation author or testing approver.
- [ ] Every review finding is resolved by a commit/explanation or an explicitly reviewer-accepted rationale.
- [ ] Impacted tests were rerun after every review fix; full notebook validation was rerun for notebook/dependency changes.
- [ ] Reviewer rechecked every requested resolution and recorded approval.

## Final gate

- [ ] Final `git diff --check` passed.
- [ ] Final `git status --short --branch` and diff inspection show only intended files.
- [ ] Merge is performed only through the approved PR, never directly on `main`.
