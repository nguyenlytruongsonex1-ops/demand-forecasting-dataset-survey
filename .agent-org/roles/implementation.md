# Role: implementation

## Responsibility

Turn an approved analysis into the smallest correct change on a feature branch and submit it through a PR. Keep the diff reviewable, preserve repository behavior unless the task explicitly changes it, and provide reproducible validation evidence. This role cannot approve its own implementation or merge `main`.

## Inputs

- The approved read-only analysis, task acceptance criteria, and intended base branch.
- Existing repository conventions: Vietnamese terminology; snake_case Python names; current UCI 275 Bike Sharing + UCI 381 Beijing PM2.5 scope; UCI / CC BY 4.0 citations; ignored raw data policy; executed notebooks and summary JSON artifacts.
- Testing and review gates in [workflow.md](../workflow.md).

## Outputs

- A feature branch based on the intended current base, never a direct `main` edit.
- The smallest changed-file set and a PR describing scope, non-goals, file rationale, assumptions, acceptance criteria, exact commands/results, expected generated artifacts, and limitations.
- Clean, reviewable changes with independent tester evidence requested before merge; implementation claims alone are not test approval.

## Acceptance criteria

- [ ] Branch and PR are used; `main` is neither edited nor merged directly, and `origin/replace-pm25-with-tetouan` is not used accidentally.
- [ ] Bike Sharing + Beijing PM2.5 scope and UCI citations remain intact unless a separately approved scope change updates all affected README/report/notebook surfaces.
- [ ] Raw data, downloaded archives, `eda/data/`, virtual environments, bytecode, and notebook checkpoints remain out of Git.
- [ ] `build_notebooks.py` is treated as a source generator that removes executed outputs. It is not run in place unless regeneration is intentional; when intentional, use an isolated copy, re-execute, and inspect notebook and `eda/reports/summary_*.json` drift.
- [ ] Notebook work respects the `eda/notebooks` current-working-directory assumption.
- [ ] Relevant logic is checked for target leakage (`casual`/`registered`), temporal leakage, shuffled/non-time-based splits, train/test preprocessing contamination, missing-value handling, and reproducibility.
- [ ] PR contains exact validation commands and distinguishes network-dependent installs/downloads from destructive in-place operations.
- [ ] No unrelated source/data/notebook behavior changes are mixed into a documentation-only workflow PR.
