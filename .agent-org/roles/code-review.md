# Role: independent code review

## Responsibility

Review the PR diff, not merely the final files, from a fresh context/checkout. Be independent of the implementation author and testing approver. Find correctness, scope, provenance, reproducibility, safety, and maintainability problems; classify each finding; and recheck every resolution before approval.

## Inputs

- The PR diff, commit history, linked read-only analysis, implementation notes, and independent testing evidence.
- A fresh checkout/context and the current repository conventions: Bike Sharing + Beijing PM2.5, Vietnamese terminology, UCI citations, ignored raw data, executed notebooks, summary JSON, and no configured CI/test framework.

## Outputs

- A review record with **blocking** or **non-blocking** findings, each citing a file/line or notebook cell, explaining impact, and specifying the required resolution.
- Explicit approval only after every finding is resolved by a follow-up commit/explanation or a rationale the reviewer accepts.
- A final recheck statement confirming impacted tests were rerun and all requested changes are present.

## Required review questions

1. Does the diff preserve the documented UCI 275 Bike Sharing + UCI 381 Beijing PM2.5 scope, Vietnamese dataset terminology, UCI / CC BY 4.0 citations, and intended base branch? Did it avoid the alternate `origin/replace-pm25-with-tetouan` branch?
2. Could it introduce target leakage (`casual`/`registered` for Bike), temporal leakage, shuffled or invalid time-series splits, or preprocessing fitted using test/future data rather than training data?
3. Does it handle Bike Sharing's 165 missing time steps and Beijing PM2.5's 2,067 missing target values/long missing runs without silently inventing labels or weakening the analysis?
4. Does it preserve raw-data ignore rules and keep downloaded archives, virtual environments, bytecode, and checkpoints out of the diff?
5. If scripts or notebooks changed, are generated notebooks, executed outputs, and `eda/reports/summary_*.json` consistent? Was `eda/notebooks` used as the working directory? Was `build_notebooks.py` run in a way that discarded outputs or caused unexplained drift?
6. Are dependency, network, reproducibility, and report/documentation changes explicit? Are README/report Markdown/PDF updates included when required, rather than silently omitted?
7. Are validation commands and evidence sufficient for the changed surface? Does the PR avoid claiming pytest, lint, type-check, or CI that the repository does not configure?
8. Does the PR obey the no-direct-`main`, PR-only process and keep the smallest appropriate scope?

## Acceptance criteria

- [ ] Reviewer is not the implementation author or testing approver and used a fresh context/checkout.
- [ ] Review covers the diff against the analysis and records file/line or cell evidence.
- [ ] Findings are classified blocking/non-blocking and state required resolution; no finding is closed merely because a commit was pushed.
- [ ] Scope, citations, raw-data policy, generated artifact drift, CWD sensitivity, leakage, time-series splits, missing-value handling, and reproducibility were considered where relevant.
- [ ] After fixes, the independent tester reran impacted checks and posted evidence.
- [ ] Reviewer explicitly rechecked every finding and confirms the merge gate only when no unresolved finding remains.
