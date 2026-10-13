---
subject: MLOps
chapter: 09
tags: [ds, mlops, ci-cd, github-actions, dag, automation, continuous-training]
source: "MLOps_CI_GitHubActions.pdf — MLOps Course, Swinburne Vietnam"
---

# CI/CD with GitHub Actions

DAGs, GitHub Actions and CI workflows. [[05 - Packaging Models with FastAPI and Docker]] built images by hand; here they are built and published on every push. Extends the Actions introduction in [[02 - Environment Setup]] and adds **continuous training (CT)**, which ordinary software doesn't have.

## 📘 Main Knowledge

### DAGs

A **directed acyclic graph** has one-way dependencies, no cycles and a valid execution order. In MLOps it encodes pipeline dependencies so tasks run in order and only after their prerequisites succeed.

| Term | Meaning |
|---|---|
| node / task | one unit of work |
| edge | dependency |
| root / leaf | no parents / no children |
| fan-out / fan-in | one task triggers many / many converge into one |
| topological sort | a linear order respecting all edges |

Properties: reproducibility, parallel branches, auditable lineage, **incrementality** (re-run only changed steps, as `dvc repro` does).

```
raw data → validation → features → train/val split ─┬→ HPO ──────┐
                                                    └→ baseline ─┴→ evaluation → quality gate → registry
```
The `--output` → `--input` chaining of ch. 05 is such a DAG. Orchestrators: Airflow ([[Big Data Analytics/contents/10 - Workflow Orchestration with Airflow|Airflow]]), Prefect, Flyte, ZenML, Metaflow, Kubeflow Pipelines. The pipeline DAG (data → model) and the CI/CD DAG (commit → deploy) complement each other: CI/CD triggers and validates the pipeline.

### GitHub Actions

| Block | Meaning |
|---|---|
| workflow | YAML in `.github/workflows/` |
| event | `push`, `pull_request`, `schedule`, `workflow_dispatch` |
| job | steps on one runner |
| step | a command or action |
| action | reusable task |
| runner | the VM that runs the job |

```yaml
name: ML Pipeline CI
on:
  push: { branches: [main, develop] }
  pull_request: { branches: [main] }
  schedule:
    - cron: '0 2 * * 1'          # weekly retraining
jobs:
  workflow-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with: { python-version: '3.11' }
      - run: |
          pip install -r requirements.txt
          pip install pytest
```

`needs:` creates DAG edges between jobs:
```yaml
jobs:
  lint:     { runs-on: ubuntu-latest, steps: [{ run: ruff check src/ }] }
  test:     { needs: lint,  runs-on: ubuntu-latest, steps: [{ run: pytest tests/ }] }
  train:    { needs: test,  runs-on: ubuntu-latest, steps: [{ run: python train.py }] }
  evaluate: { needs: train, runs-on: ubuntu-latest, steps: [{ run: python evaluate.py }] }
  deploy:
    needs: [train, evaluate]                 # fan-in
    if: github.ref == 'refs/heads/main'      # deploy only from main
    runs-on: ubuntu-latest
    steps: [{ run: ./deploy.sh }]
```

Other features: **matrix** builds (Python versions, OS, hyperparameter sweeps); **secrets and protected environments** with required reviewers; **artifacts** (`actions/upload-artifact` to pass files between jobs) and **cache** (`actions/cache` for pip/conda); `outputs:` for values; reusable workflows.

### How MLOps CI/CD differs

| | Traditional | MLOps adds |
|---|---|---|
| Trigger | code change | data or model change |
| Test | unit, integration, e2e | data validation, model evaluation |
| Artifact | binary or image | trained model |
| Deploy | application version | model serving endpoint |
| Validate | smoke tests, health checks | metrics, drift, shadow mode |

```
CI: commit → lint → unit tests → data validation → feature pipeline
CT: train → tune → evaluate vs baseline → quality gate → model registry
CD: build → shadow → canary → production → monitor and alert
```
A binary doesn't decay; a model does, so it must be retrained, and each retrained model must pass a **quality gate** before promotion.

### Versioning

- **DVC**: data tracked alongside code; `dvc repro` re-runs changed stages; remotes on S3, GCS, Azure; `iterative/setup-dvc` in Actions.
- **Model registry** (MLflow, SageMaker, Vertex AI): catalogue with metadata and stages **Staging → Production → Archived**; CI/CD promotes between stages. Path: code v1.3.2 + data v20240315 → run → staging → (evaluation and review pass) → production.

The slide's golden rule is cut off at "every model in production must…"; the usual completion is "be traceable to the exact code and data that produced it".

### Testing layers (cheapest first)

| Layer | Covers |
|---|---|
| unit | transforms, parsers, helpers; no I/O |
| integration | pipeline on a small data slice; stage interfaces |
| **model** | accuracy ≥ baseline, latency ≤ SLA, fairness, drift |
| end-to-end | full pipeline on staging; canary requests |

### Monitoring and retraining

| Signal | Measure |
|---|---|
| prediction drift | PSI, KL divergence |
| feature drift | KS test, Wasserstein distance |
| accuracy | labeled feedback |
| latency | p50, p95, p99 |
| data quality | schema, null rates |
| business | click-through, revenue |

When drift crosses a threshold, a `workflow_dispatch` event starts the retraining workflow: model → monitor → drift alert → retrain → new model → promote ([[10 - Monitoring and Drift]]).

### Best practices

- Idempotent stages; fail fast (cheap checks before training); small data in CI, full data in CT; parameterize everything; configs in version control (YAML, Hydra).
- Secrets only through GitHub Secrets or OIDC; pin action versions (`@v4`, not `@main`); protected environments; Dependabot.
- Block merges when accuracy falls below baseline; enforce data schema contracts in CI.

### Hands-on: Docker Hub

```bash
docker tag fastapi manhtoannb87/fastapi     # local name → Hub name (account manhtoannb87)
docker push manhtoannb87/fastapi
```
Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` under Settings → Secrets and variables → Actions. The token is a Docker Hub personal access token (Account → Security → Access Tokens, read & write), shown only once. Never put credentials in YAML; use `${{ secrets.NAME }}`.

Workflows come from `github.com/NguyenMToan/house-price-predictor/tree/main/.github/workflows`: `mlops-ci-workflow.yaml`, `mlops-pipeline.yaml` and a third (name truncated). `mlops-pipeline` runs on pushes to `main` and tags `v*.*.*`, and on pull requests to `main`, with three jobs: `data-processing → model-training → build-and-publish`. Each job runs on a fresh runner, so processed data and the model pass between them as artifacts.

Results: Actions tab → MLOps Pipeline → latest run. For a failure, open the failed job, then the failed step, find the error line, and re-run.

## ✏️ Exercises

**1.** Why must jobs pass data through artifacts rather than the disk?

> [!example]- Solution
> Each job runs on a new VM that is destroyed afterwards; steps within a job share a filesystem, jobs don't.
> ```yaml
> data-processing:
>   runs-on: ubuntu-latest
>   steps:
>     - uses: actions/checkout@v4
>     - run: python src/data/run_processing.py --output data/processed/cleaned.csv
>     - uses: actions/upload-artifact@v4
>       with: { name: processed-data, path: data/processed/ }
> model-training:
>   needs: data-processing
>   runs-on: ubuntu-latest
>   steps:
>     - uses: actions/checkout@v4
>     - uses: actions/download-artifact@v4
>       with: { name: processed-data, path: data/processed/ }
>     - run: python src/models/train_model.py --data data/processed/featured.csv
> ```
> Separate jobs allow parallelism, re-running only the failed part, and different runners (GPU for training). Cache is a speed-up whose miss is harmless and can be evicted; artifacts are required outputs, and they can be downloaded from the UI afterwards.

**2.** Explain `needs: [train, evaluate]` and `if: github.ref == 'refs/heads/main'` on the deploy job. What breaks without each?

> [!example]- Solution
> Jobs run in parallel unless `needs:` orders them, so without it deploy would start alongside training and ship the old (or no) model. With it, deploy waits for both and is skipped if either fails.
> The workflow also runs on pull requests, which should get the full validation but must never deploy (a fork's PR included). The `if:` limits deployment to `main`. Since anyone with write access can edit it, add `environment: production` with required reviewers and scoped secrets for real enforcement.

**3.** What is continuous training, and why does traditional CI/CD have no equivalent?

> [!example]- Solution
> CT = train → tune → evaluate → quality gate → register, between CI and CD. A binary behaves the same forever unless the code changes; a model decays as $P(Y\mid X)$ shifts, with the code unchanged. So retraining becomes a pipeline stage, triggered by `schedule` (weekly) or `workflow_dispatch` (drift). Triggers include data changes, not just commits.
> The quality gate makes automatic retraining safe:
> ```python
> def test_model_not_worse_than_baseline():
>     assert new_metrics["recall"] >= baseline_metrics["recall"] - 0.01
>     assert new_metrics["p95_latency_ms"] <= 100
> ```
> Without it, a bad week of data produces a bad model that deploys itself.

**4.** Explain the four testing layers. Why can't unit tests replace model tests?

> [!example]- Solution
> Cheapest first so failures surface early: a lint error costs seconds, not GPU minutes. Unit tests check functions; integration tests check that stages fit (a renamed column, a changed dtype); model tests check the result; end-to-end tests check staging.
> Code can be correct and still produce a useless model, e.g. training data accidentally filtered to one class. Model quality is a statistical property of outputs:
> ```python
> def test_fairness_across_groups(model, X_test, y_test, groups):
>     rates = {g: recall_score(y_test[groups == g], model.predict(X_test[groups == g]))
>              for g in groups.unique()}
>     assert max(rates.values()) - min(rates.values()) <= 0.05
> ```
> The fairness test is the automated form of "aggregate metrics hide subgroup failure" ([[04 - Model Development]]). Use small subsets in CI and full evaluation in CT.

**5.** (Advanced) Design the automated retraining loop: triggers, safeguards, risks.

> [!example]- Solution
> ```yaml
> name: Automated Retraining
> on:
>   workflow_dispatch:
>     inputs:
>       reason: { required: true }        # record why it fired
>   schedule:
>     - cron: '0 2 * * 1'                 # weekly fallback
> jobs:
>   retrain:
>     runs-on: ubuntu-latest
>     steps:
>       - uses: actions/checkout@v4
>       - run: python src/data/validate.py --fail-on-schema-violation
>       - run: python src/models/train_model.py --config configs/model_config.yaml
>       - run: pytest tests/test_model_quality.py
>       - run: python src/registry/promote.py --stage Staging
>   deploy:
>     needs: retrain
>     runs-on: ubuntu-latest
>     environment: production             # human approval
>     steps:
>       - run: python src/registry/promote.py --stage Production
> ```
> The monitor calls the API when drift (PSI, KS, …) crosses a threshold; the cron catches gradual concept drift that never moves $P(X)$.
> Safeguards: validate data first (retraining on a broken pipeline bakes in the error); quality gate; promote to staging, not production; shadow and canary before full rollout ([[06 - Deployment]]).
> Risks: **feedback loops**: a fraud model never sees outcomes for transactions it blocked, so it narrows onto its own beliefs (likewise recommenders); keep a small randomized slice that bypasses the model. **Delayed labels**: retraining before chargebacks arrive undercounts fraud. **One-off events**: retraining on a holiday spike fits noise; the required `reason` input records the judgment.

## 📝 Summary

- DAGs give ordering, parallelism, lineage and incremental re-runs; CI/CD triggers and validates the pipeline DAG.
- Actions: workflow → event → job → step → action on a runner; `needs:` adds edges.
- Jobs share nothing; pass files as artifacts.
- MLOps CI/CD triggers on code, data or model changes and tests data and models.
- CI → CT → CD; CT exists because models decay; the quality gate makes it safe.
- Test layers: unit → integration → model → end-to-end.
- DVC versions data; the registry versions models (Staging → Production → Archived).
- Idempotent stages, fail fast, pinned actions, secrets only through Secrets.

## ⚠️ Important Notes

1. Steps share a filesystem; jobs don't.
2. Cache is not for pipeline outputs.
3. Without `needs:`, jobs run in parallel.
4. Guard deploys by branch and back the guard with a protected environment.
5. Pin action versions; a compromised `@main` action runs with your secrets.
6. Never hardcode credentials.
7. A Docker Hub token is shown once.
8. Automated retraining without a gate ships regressions.
9. Validate data before retraining.
10. Promote to staging first.
11. Watch for feedback loops; keep a randomized control slice.
12. Retraining cadence must respect label delay.
13. Idempotent stages make retries safe.

> [!warning] Gaps in the source slides
> - Slides 2, 6, 11, 19 have no text; diagrams on slides 3, 5, 9, 13–16 extracted only as labels and icon-font glyphs, and are rebuilt above.
> - Truncated: slide 7 (runner list), 8 (the final test step), 10 (reusable workflows), 14 (the golden rule), 17, 18, 20, 21 (token warning), 22 (third workflow filename). Slide 24 is a screenshot.
> - The workflow YAML files are only in the repository; the examples here are reconstructed from the described structure.
> - The deck is dated 30 March 2026 and credited to "MLOps Course" rather than the lecturer.

**Previous:** [[08 - Monitoring with Prometheus and Grafana]] · **Next:** [[10 - Monitoring and Drift]]
