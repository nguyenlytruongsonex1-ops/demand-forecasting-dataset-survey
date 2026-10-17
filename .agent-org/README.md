# Repository-local agent workflow

`.agent-org/` is the repository-local playbook for future engineering work in `demand-forecasting-dataset-survey`. It defines four separate roles and a gated, PR-based sequence. Use the role files as contracts; an agent must not silently approve work performed by another role.

## Non-negotiable rules

- **No direct `main` edits or merges.** Work starts from the intended base on a feature branch and reaches `main` only through a pull request (PR). The current base is the checked-out **Bike Sharing + Beijing PM2.5** project on `main`; do not accidentally use `origin/replace-pm25-with-tetouan`.
- Keep this repository's current Vietnamese terminology and dataset naming. Preserve the UCI 275 Bike Sharing and UCI 381 Beijing PM2.5 scope and their UCI / CC BY 4.0 citations unless a separately approved PR deliberately changes scope.
- Keep raw data, downloaded archives, virtual environments, bytecode, and notebook checkpoints out of Git. Do not mix source/data/notebook behavior changes into this workflow-documentation PR.
- Treat checked-in notebooks as executed artifacts. `eda/scripts/build_notebooks.py` is a source generator that rewrites notebooks **without outputs**; do not run it in place casually. If regeneration is intentional, execute notebooks afterward and inspect notebook plus `eda/reports/summary_*.json` diffs.
- Respect notebook working-directory sensitivity: notebook path setup expects execution from `eda/notebooks` (or an equivalent isolated copy).
- For relevant changes, check target leakage, time-series split errors, missing-value handling, reproducibility, data provenance, and generated-artifact drift.

## Roles

| Role | Contract |
|---|---|
| [Codebase analysis](roles/codebase-analysis.md) | Read-only inventory, risks, scope, acceptance criteria, and validation plan. |
| [Implementation](roles/implementation.md) | Smallest change on a feature branch, delivered by PR; no direct `main` work. |
| [Testing](roles/testing.md) | Independent checkout, exact commands and evidence; no invented CI or test framework. |
| [Code review](roles/code-review.md) | Fresh-context, independent review of the diff, findings, and recheck. |

The [workflow](workflow.md) is the source of truth for sequencing. Copy [pr-checklist.md](pr-checklist.md) into every applicable PR.

## Current validation reality

There is **no configured CI, pytest, lint, type-check, Make, tox, pre-commit, or other automated test framework** in this repository. The playbook does not claim otherwise. Until a separate PR adds such tooling, use the explicit manual/static and notebook checks in `workflow.md` and record exact commands, environment, and results.

## Initial playbook PR acceptance

This addition is documentation-only and must contain exactly these seven Markdown files under `.agent-org/`, with no source, data, notebook, or generated-output behavior changes. It is ready for coordinator inspection only after the PR gate is complete: independent testing, independent review, every finding resolved, impacted checks rerun, reviewer recheck, and final diff/status checks.
