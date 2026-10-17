# Role: testing

## Responsibility

Independently validate the PR from a clean checkout or worktree, record exact commands and outcomes, and approve only with evidence. Do not rely solely on the implementation author's report. This role is separate from implementation and code review.

## Inputs

- The PR branch and linked read-only analysis.
- A clean/independent context, Python environment details, network availability, and the changed-file surface.
- The repository's current manual baseline. There is no configured pytest, lint, type-check, Make, tox, pre-commit, or CI workflow; do not invent or imply one.

## Outputs

- A PR comment or test record containing checkout/commit, environment, exact commands, pass/fail output, network status, and any skipped/destructive steps with reasons.
- Independent approval or a precise blocking failure.
- After review fixes, a new record of all impacted retests and confirmation that no unwanted raw/generated artifacts appeared.

## Baseline commands

Run these from the repository root in the independent checkout. The first two are local and non-network checks. The Python block parses notebook JSON, compiles every code cell, and parses both summary JSON files:

```bash
git status --short --branch
git diff --check
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

Dependency installation changes the environment and is commonly network-dependent; run it only when needed and record the result. Do not report pytest/lint/type-check/CI success because none is configured.

## Isolated notebook execution

When the change affects notebooks, dependencies, data loading, or analysis behavior, validate in an isolated copy/worktree. Raw-data download is network-dependent and must remain untracked. `build_notebooks.py` is destructive if run in place: it rewrites notebooks without outputs. Run it only when regeneration is part of the change, then inspect generated notebooks and summary JSON drift. Execute from `eda/notebooks` so path setup resolves correctly:

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

The download and dependency availability require network access; notebook execution also writes `eda/reports/summary_*.json` side effects, so never use the working tree for an unreviewed run. State whether data download occurred, whether network was available, whether the generator ran, where outputs went, and whether changes were expected.

## Acceptance criteria

- [ ] Testing uses a fresh independent checkout/context and a commit identifiable in the PR.
- [ ] `git diff --check`, notebook JSON/code-cell compilation, and summary JSON parsing are run and recorded, or a reason is documented.
- [ ] Dependency installation is recorded as network/environment-changing when needed; no nonexistent framework is claimed.
- [ ] Relevant notebook execution uses isolation and the correct working directory; destructive generator behavior is acknowledged.
- [ ] For relevant logic, evidence addresses leakage, time-series split correctness, train-only preprocessing/missing values, reproducibility, and artifact drift.
- [ ] Approval is withheld for failures, unexplained generated/raw artifacts, missing evidence, or unresolved scope/citation regressions.
- [ ] After review fixes, impacted checks are rerun and the updated evidence is posted before reviewer recheck.
