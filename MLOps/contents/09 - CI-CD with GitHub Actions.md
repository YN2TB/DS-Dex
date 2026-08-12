---
subject: MLOps
chapter: 09
tags: [ds, mlops, ci-cd, github-actions, dag, automation, continuous-training]
source: "MLOps_CI_GitHubActions.pdf — MLOps Course, Swinburne Vietnam"
---

# CI/CD with GitHub Actions

> *DAGs, GitHub Actions & CI Workflows — Automating the Machine Learning Lifecycle*

> [!note] Where this sits in the course
> The automation layer that ties everything together. [[05 - Packaging Models with FastAPI and Docker]] built images by hand; this chapter builds and publishes them automatically on every push. It extends the GitHub Actions introduction from [[02 - Environment Setup]] and introduces **CT — Continuous Training**, the stage that has no equivalent in traditional software.

## 📘 Main Knowledge

---

## Part 1 — DAGs

> A **Directed Acyclic Graph (DAG)** is a graph with **directed edges** (one-way dependencies), **no cycles** (no task depends on itself), and a **clear topological ordering** of execution.

> **Why DAGs in MLOps:** they encode the **dependency structure of ML pipelines** — ensuring tasks run in the correct order and only when their prerequisites succeed.

| Term | Meaning |
|---|---|
| **Node / Task** | A single unit of work (e.g. train model) |
| **Edge** | Dependency between two tasks |
| **Root node** | Task with no parents (entry point) |
| **Leaf node** | Task with no children (exit point) |
| **Fan-out** | One task triggers multiple downstream tasks |
| **Fan-in** | Multiple tasks converge into one |
| **Topological sort** | A valid linear ordering respecting all edges |

**Key properties:**
- **Reproducibility** — same inputs ⇒ same outputs
- **Parallelism** — independent branches run concurrently
- **Auditability** — full lineage is traceable
- **Incrementality** — only re-run changed steps

**A typical ML pipeline DAG:**

```
Raw Data → Data Validation → Feature Engineering → Train/Val Split → ┬→ HPO ────────┐
                (schema check)      (transforms)                     └→ Baseline ───┴→ Evaluation
                                                                                        ↓ (metrics ≥ threshold)
                                                                                    Quality Gate → Registry
```

The `--output`/`--input` chaining from [[05 - Packaging Models with FastAPI and Docker]] *is* this DAG, expressed on the command line. **Incrementality** is why `dvc repro` can re-run only changed stages.

**Popular DAG orchestrators:** Apache Airflow · Prefect / Flyte · ZenML / Metaflow · Kubeflow Pipelines.

> **CI/CD and DAGs:** the **pipeline DAG** (data → model) and the **CI/CD DAG** (commit → deploy) are complementary — **CI/CD triggers and validates the ML pipeline DAG.**

---

## Part 2 — GitHub Actions

> A native CI/CD platform built into GitHub that automates workflows triggered by repository events.

**Building blocks:**

| Block | Meaning |
|---|---|
| **Workflow** | YAML file in `.github/workflows/` |
| **Event** | Trigger — `push`, `pull_request`, `schedule`, `workflow_dispatch` |
| **Job** | Group of steps running on a runner |
| **Step** | Individual command or action |
| **Action** | Reusable task (marketplace or custom) |
| **Runner** | Virtual machine executing the job |

**Anatomy of a workflow:**
```yaml
name: ML Pipeline CI
on:                                   # Events
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1'               # Weekly retraining

jobs:                                 # Stages
  workflow-test:
    runs-on: ubuntu-latest            # Runner
    steps:
      - uses: actions/checkout@v6     # Action
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
```

The `schedule` trigger is worth noting: **weekly retraining on a cron** is an MLOps-specific pattern with no counterpart in ordinary software CI.

**Job dependencies — DAGs in GitHub Actions** via `needs:`:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [{ run: ruff check src/ }]

  test:
    needs: lint
    steps: [{ run: pytest tests/ }]

  train:
    needs: test
    steps: [{ run: python train.py }]

  evaluate:
    needs: train
    steps: [{ run: python evaluate.py }]

  deploy:
    needs: [train, evaluate]            # FAN-IN — waits for both
    if: github.ref == 'refs/heads/main'
    steps: [{ run: ./deploy.sh }]
```

`deploy` demonstrates the **fan-in** pattern, and the `if:` guard means deployment happens **only from `main`** — PRs run the full pipeline but never deploy.

**Advanced features for MLOps:**

- **Matrix strategy** — run jobs across multiple Python versions, OS, or dataset splits simultaneously; enables **parallel hyperparameter sweeps**.
- **Secrets & Environments** — `secrets.AWS_ACCESS_KEY` for cloud credentials · **protected environments** for production · **required reviewers** before deploy jobs run.
- **Artifacts & Caching** — `actions/upload-artifact` persists model files **between jobs** · `actions/cache` caches pip/conda for faster builds · pass values between jobs via `outputs:`.
- **Reusable workflows** — extract common steps into shared workflow files.

---

## Part 3 — MLOps CI/CD

### How it differs from traditional CI/CD

| | **Traditional Software** | **MLOps — additional concerns** |
|---|---|---|
| **Trigger** | Code change | Code **OR data OR model** change |
| **Test** | Unit, integration, e2e | Unit tests **+ data validation + model evaluation** |
| **Artifact** | Binary / Docker image | **Trained model** + Docker image |
| **Deploy** | New application version | **Model serving endpoint** |
| **Validate** | Smoke tests, health checks | **Performance metrics, drift, shadow mode** |

This is the [[01 - Introduction to MLOps]] DevOps/MLOps table applied to the pipeline: because ML systems are **probabilistic**, testing must include statistical checks that no compiler or unit test can perform.

### The complete pipeline: CI → CT → CD

```
CI:  Code Commit → Lint & Format → Unit Tests → Data Validation → Feature Pipeline
CT:  Model Train → HPO / Tuning → Eval vs Baseline → Quality Gate → Model Registry
CD:  Package & Build → Shadow Deploy → Canary Release → Prod Deploy → Monitor + Alert
```

- **CI — Code & Data:** lint, test, validate schema, run the feature pipeline.
- **CT — Continuous Training:** train, tune, evaluate, gate, register the model.
- **CD — Continuous Deployment:** package, shadow test, canary, production, monitor.

**CT is the stage traditional CI/CD does not have.** Software is built once and deployed; a model must be *retrained* as data changes, and each retrained model must pass a **quality gate** before promotion.

### Data and model versioning in CI/CD

**Data Version Control (DVC):** track datasets alongside code in Git · `dvc repro` re-runs **only changed pipeline stages** · remote storage on S3, GCS, Azure Blob · integrates with Actions via `iterative/setup-dvc`.

**Model Registry:** a central catalog of trained models with metadata · stages **Staging → Production → Archived** · MLflow Registry, AWS SageMaker, Vertex AI · **CI/CD promotes models between stages automatically**.

The promotion path: `Code v1.3.2` + `Data v20240315` → Experiment Run → Staging Model → *(eval pass, review OK)* → Production Model.

> **Golden Rule: every model in production must** *(truncated in source — the standard completion is "be traceable to the exact code and data version that produced it")*.

### Testing strategy

Four layers, cheapest and fastest first:

| Layer | What it covers |
|---|---|
| **Unit Tests** | Feature transforms, data parsers, model helpers; fast, no I/O |
| **Integration Tests** | Pipeline runs on a small data slice; checks stage interfaces |
| **Model Tests** | **Accuracy ≥ baseline; latency ≤ SLA; fairness metrics; data drift** |
| **E2E Tests** | Full pipeline on staging; canary request validation |

**Model tests are the ML-specific layer.** A model can pass every unit and integration test while being useless — asserting `accuracy >= baseline` is what catches that.

### Monitoring and feedback loops

| Signal | Tool / Metric |
|---|---|
| Prediction drift | PSI, KL divergence |
| Feature drift | KS test, Wasserstein |
| Model accuracy | Labeled feedback loop |
| Latency / throughput | p50, p95, p99 |
| Data quality | Schema, null rates |
| Business KPIs | Click-through, revenue |

> **Automated retraining trigger:** when drift exceeds a threshold ⇒ a GitHub Actions `workflow_dispatch` fires the retraining job automatically.

Loop: Production Model → Monitor → Drift Alert → Re-train → New Model → *promote*. Developed in [[10 - Monitoring and Drift]].

### Best practices

**Pipeline design:** keep stages **idempotent** (safe to re-run) · **fail fast** — run cheap checks before expensive training · use **small data subsets in CI, full data in CT** · parameterise everything, no hardcoded paths or thresholds · store all configs in version control (YAML / Hydra).

**Security:** secrets only via **GitHub Secrets / OIDC** · **pin all action versions** (`@v4`, not `@main`) · **protected environments** for production · scan dependencies with **dependabot**.

**Quality gates:** block merge if model accuracy falls below baseline · **enforce data schema contracts at CI time**.

---

## Part 4 — Hands-on: publishing to Docker Hub

**Step 1 — Create a repository** at `hub.docker.com`. Your Docker account *is* your Docker Hub account. Example: Hub ID `manhtoannb87`, repo `fastapi`.

**Step 2 — Tag and push:**
```bash
docker image ls
docker tag fastapi manhtoannb87/fastapi      # local → remote name
docker push manhtoannb87/fastapi
```

**Configuring the registry token:**

1. **GitHub Secrets** — repo → *Settings → Secrets and variables → Actions*, add:

| Name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker ID |
| `DOCKERHUB_TOKEN` | Your PAT |

2. **Docker PAT** — Docker Hub → *Account → Security → Access Tokens* → *Generate new token* → permissions **Read & Write** → **copy immediately, it is not shown again**.

**Creating the workflow:**
```bash
mkdir -p .github/workflows
```
Workflow files from [`github.com/NguyenMToan/house-price-predictor/tree/main/.github/workflows`](https://github.com/NguyenMToan/house-price-predictor/tree/main/.github/workflows):
```
house-price-predictor/
└── .github/
    └── workflows/
        ├── mlops-ci-workflow.yaml
        ├── mlops-pipeline.yaml
        └── simple_mlops-ci-...
```

> **Security note: never hardcode credentials in workflow YAML. Always use `${{ secrets.NAME }}`.**

**Push to trigger:**
```bash
git status                          # review changes
git add .
git commit -m "message"
git push origin main                # triggers the pipeline
```

**The course pipeline** — `mlops-pipeline.yml` runs on every push to `main` (or a version tag) and consists of **three sequential jobs**:

| Trigger event | Target |
|---|---|
| `push` | branch `main`, tags `v*.*.*` |
| `pull_request` | branch `main` |

```
data-processing → model-training → build-and-publish
   (needs)            (needs)
```

> **Artifact handoff:** jobs communicate via **GitHub Artifacts** — processed data and the trained model are uploaded by one job and downloaded by the next, **since each job runs on a fresh runner.**

**Checking results:** repository → **Actions** tab → *MLOps Pipeline* → latest run → inspect each job and step.

**Run status icons:** ✅ success · ❌ failed · 🕐 in progress/queued · ⊖ skipped/cancelled.
**Inspecting a failure:** click the failed **job** to expand its steps → click the failed **step** to read the log → look for the `Error` or exit code line → **Re-run jobs** to retry.

## ✏️ Exercises

**1.** Explain why jobs must hand off data via GitHub Artifacts rather than simply writing to disk.

> [!example]- Solution
> **Each job runs on a fresh runner** — a brand-new virtual machine. When `data-processing` finishes, its VM is destroyed along with everything it wrote. `model-training` starts on a different machine with an empty filesystem.
>
> This surprises people because *steps within a job* **do** share a filesystem. The boundary is the **job**, not the step.
>
> ```yaml
> jobs:
>   data-processing:
>     runs-on: ubuntu-latest
>     steps:
>       - uses: actions/checkout@v4
>       - run: python src/data/run_processing.py --output data/processed/cleaned.csv
>       - uses: actions/upload-artifact@v4
>         with:
>           name: processed-data
>           path: data/processed/
>
>   model-training:
>     needs: data-processing
>     runs-on: ubuntu-latest
>     steps:
>       - uses: actions/checkout@v4
>       - uses: actions/download-artifact@v4      # retrieve from the previous job
>         with:
>           name: processed-data
>           path: data/processed/
>       - run: python src/models/train_model.py --data data/processed/featured.csv
>       - uses: actions/upload-artifact@v4
>         with:
>           name: trained-model
>           path: models/trained/
> ```
>
> **Why separate jobs at all, given the overhead?** Three reasons: **parallelism** (independent jobs run concurrently), **granular re-runs** (a failed publish step can be retried without repeating training), and **different runners** (training may need a GPU or self-hosted runner while publishing needs only `ubuntu-latest`).
>
> **Artifacts vs cache** — a distinction worth knowing. `actions/cache` is a *performance optimisation* for regenerable content like pip downloads; a cache miss is harmless. `upload-artifact` is for *outputs you must have*; a missing artifact fails the job. Never use cache for pipeline outputs — it may be silently evicted.
>
> Artifacts also persist after the run, so you can **download the trained model from the Actions UI** — useful for debugging a model that passed CI but misbehaves in production.

**2.** The `deploy` job uses `needs: [train, evaluate]` and `if: github.ref == 'refs/heads/main'`. Explain both, and what breaks without each.

> [!example]- Solution
> **`needs: [train, evaluate]` is a fan-in.** `deploy` waits for *both* to complete successfully. Without it, jobs run in **parallel by default** — `deploy` would start immediately alongside `train`, deploying a model that does not yet exist, or the *previous* model. GitHub Actions has no implicit ordering; `needs:` is the only thing that creates edges in the DAG.
>
> It also provides **failure propagation**: if `evaluate` fails, `deploy` is *skipped*, not failed. That is correct — the deploy never ran, so calling it failed would be misleading, and the skipped status makes the cause obvious in the UI.
>
> **`if: github.ref == 'refs/heads/main'` restricts deployment to the main branch.** The workflow triggers on both `push` and `pull_request`, and you want PRs to run lint → test → train → evaluate so contributors get full feedback — but a PR from a fork must **never** deploy to production. Without the guard, opening a PR would deploy its code.
>
> This is the mechanism behind [[02 - Environment Setup]]'s rule that everything goes through a PR: the PR gets *validation* without *deployment authority*.
>
> **Stronger protection for real production** — the guard is a YAML condition anyone with write access can edit. Combine it with a **protected environment**:
> ```yaml
>   deploy:
>     needs: [train, evaluate]
>     if: github.ref == 'refs/heads/main'
>     environment: production        # required reviewers, secret scoping
> ```
> Protected environments enforce **required reviewers** (a human approves before the job runs) and scope production secrets so only this job can read them. That is defence in depth: the `if:` is convention, the environment is enforcement.

**3.** Explain **CT (Continuous Training)** and why traditional CI/CD has no equivalent stage.

> [!example]- Solution
> **CT is: train → tune → evaluate → quality gate → register.** It sits between CI (validate code and data) and CD (deploy the artifact).
>
> **Traditional software has no equivalent because a compiled binary does not decay.** Deploy version 1.3.2 and it behaves identically in a year — the same inputs produce the same outputs forever. It only changes when a human changes the code.
>
> **A model decays without anyone touching it**, because the world it models moves. [[01 - Introduction to MLOps]]'s **concept drift**: $P(Y \mid X)$ shifts, and the function the model learned stops being the right function. The code is unchanged and still correct; the *fit* has expired.
>
> So the artifact must be **regenerated periodically**, which means training becomes a pipeline stage rather than a manual act:
> ```yaml
> on:
>   schedule:
>     - cron: '0 2 * * 1'        # weekly retraining
>   workflow_dispatch:            # or fired by a drift alert
> ```
> Both triggers appear in this deck, and neither is meaningful for ordinary software — nobody recompiles an unchanged binary every Monday.
>
> **The quality gate is what makes CT safe.** Retraining automatically means a *worse* model could ship automatically. The gate blocks promotion unless the new model beats the baseline:
> ```python
> def test_model_not_worse_than_baseline():
>     assert new_metrics["recall"] >= baseline_metrics["recall"] - 0.01
>     assert new_metrics["p95_latency_ms"] <= 100
> ```
> Without it, automation amplifies failure instead of preventing it — a bad week of data produces a bad model that deploys itself.
>
> **The trigger asymmetry is the deepest difference.** Traditional CI/CD triggers on *code* change; MLOps triggers on **code OR data OR model** change. Data changing with no commit is a legitimate reason to rebuild — an idea with no counterpart in software engineering.

**4.** Explain the four testing layers, and why "model tests" cannot be replaced by unit tests.

> [!example]- Solution
> The layers are ordered **cheapest and fastest first**, implementing the *fail fast* principle: run cheap checks before expensive training so a lint error costs 10 seconds rather than 40 minutes of GPU time.
>
> **1. Unit tests** — pure functions, no I/O. Does `normalise_price` handle nulls? Milliseconds; deterministic.
> **2. Integration tests** — pipeline stages on a small data slice. Does `engineer.py`'s output actually load in `train_model.py`? Catches interface mismatches — a renamed column, a changed dtype.
> **3. Model tests** — accuracy ≥ baseline, latency ≤ SLA, fairness metrics, data drift.
> **4. E2E tests** — full pipeline on staging, canary request validation.
>
> **Why model tests are irreducible.** Unit and integration tests answer *"does the code run correctly?"* Model tests answer *"is the resulting model any good?"* — and those are independent questions.
>
> A pipeline can be **flawlessly implemented and produce a useless model**: every transform correct, every interface matching, every test green — and the model predicts the majority class because the training data was accidentally filtered to one label. No unit test detects that, because no *function* misbehaved.
>
> This is the **probabilistic vs deterministic** distinction from [[01 - Introduction to MLOps]] made concrete. Deterministic code is either right or wrong and unit tests decide which. A model's quality is a *statistical property of its outputs*, measurable only by evaluating it on data.
>
> ```python
> def test_accuracy_not_regressed(new_model, baseline_metrics, X_test, y_test):
>     assert recall_score(y_test, new_model.predict(X_test)) >= baseline_metrics["recall"] - 0.01
>
> def test_latency_within_sla(model, sample):
>     p95 = np.percentile([timeit(lambda: model.predict(sample)) for _ in range(100)], 95)
>     assert p95 <= 0.100                                   # 100 ms
>
> def test_fairness_across_groups(model, X_test, y_test, groups):
>     rates = {g: recall_score(y_test[groups == g], model.predict(X_test[groups == g]))
>              for g in groups.unique()}
>     assert max(rates.values()) - min(rates.values()) <= 0.05
> ```
> The fairness test is the one most often skipped and most consequential — it is the automated form of [[04 - Model Development]]'s warning that **aggregate metrics hide subgroup failure**.
>
> **Use small data subsets in CI, full data in CT.** Model tests in CI should be fast smoke checks; the authoritative evaluation belongs in the CT stage.

**5.** (Advanced) Design the automated retraining loop: what triggers it, what safeguards it needs, and what can go wrong.

> [!example]- Solution
> **The loop:** Production Model → Monitor → Drift Alert → Re-train → New Model → *promote*.
>
> ```yaml
> # .github/workflows/retrain.yml
> name: Automated Retraining
> on:
>   workflow_dispatch:                 # fired by the drift monitor
>     inputs:
>       reason: { required: true }     # audit trail: WHY did this fire?
>   schedule:
>     - cron: '0 2 * * 1'              # weekly fallback
> jobs:
>   retrain:
>     runs-on: ubuntu-latest
>     steps:
>       - uses: actions/checkout@v4
>       - run: python src/data/validate.py --fail-on-schema-violation
>       - run: python src/models/train_model.py --config configs/model_config.yaml
>       - run: pytest tests/test_model_quality.py     # QUALITY GATE
>       - run: python src/registry/promote.py --stage Staging   # NOT Production
>   deploy:
>     needs: retrain
>     environment: production          # required human reviewer
>     steps:
>       - run: python src/registry/promote.py --stage Production
> ```
>
> **The triggers.** The monitor computes drift (PSI, KL divergence for predictions; KS test, Wasserstein for features) and calls the Actions API when a threshold is breached. The cron is a **fallback** — gradual concept drift like the house-price inflation example in [[01 - Introduction to MLOps]] may never trip a drift alarm, because $P(X)$ never changes.
>
> **Four safeguards, each blocking a specific failure:**
>
> **1. Data validation before training.** If the drift was caused by a *broken upstream pipeline* rather than genuine change, retraining bakes the corruption into the model. Validate schema and null rates first, and fail loudly. Distinguishing drift from a data-quality bug is the diagnostic discipline from [[01 - Introduction to MLOps]].
>
> **2. Quality gate before promotion.** Never promote a model that has not beaten the baseline. Automation without a gate ships regressions automatically.
>
> **3. Promote to Staging, not Production.** The registry's `Staging → Production → Archived` stages exist for this. A human — or a canary — makes the final call.
>
> **4. Shadow / canary deployment.** Run the new model on live traffic **without acting on its predictions**, compare against the incumbent, then route a small percentage before full rollout. This is CD's *"shadow → canary → prod"* sequence. → [[06 - Deployment]]
>
> **What can go wrong — the feedback loop trap.** The most dangerous failure is that the model's own predictions influence the data it later trains on. A fraud model blocks transactions it thinks are fraudulent, so those never generate outcome labels; the next training set contains only transactions the *previous* model approved. The model progressively narrows onto its own prior beliefs and becomes blind to fraud patterns it already rejects. Recommenders show the same pathology — recommend, observe clicks on what was recommended, retrain, recommend more of the same.
>
> Mitigations: hold out a small **randomised** control slice that bypasses the model, and monitor prediction *distribution* not just accuracy.
>
> **Second trap: delayed labels.** [[01 - Introduction to MLOps]] noted fraud labels arrive weeks later via chargebacks, so "current accuracy" is unmeasurable in real time and retraining on incomplete labels systematically undercounts positives. Retraining cadence must respect label latency.
>
> **Third: retraining on a drifted-but-correct world.** If drift reflects a genuine permanent shift, retraining is right. If it reflects a one-off event — a holiday, an outage — retraining fits noise. Requiring `reason` as a `workflow_dispatch` input forces that judgement to be recorded, which is the auditability requirement from [[01 - Introduction to MLOps]].

## 📝 Summary

- **A DAG** has directed edges, no cycles, and a topological order — giving reproducibility, parallelism, auditability, and **incrementality**.
- **The pipeline DAG (data→model) and the CI/CD DAG (commit→deploy) are complementary**; CI/CD triggers and validates the pipeline.
- **GitHub Actions:** Workflow → Event → Job → Step → Action, executed on a Runner. `needs:` creates the DAG edges.
- **Jobs run on fresh runners**, so data crosses job boundaries only via **artifacts**.
- **MLOps CI/CD triggers on code OR data OR model change** — and validates with data validation and model evaluation, not just unit tests.
- **CI → CT → CD.** **CT (Continuous Training)** has no traditional equivalent: models decay without code changes.
- **The quality gate makes automated retraining safe** — block promotion unless the new model beats the baseline.
- **Four test layers:** unit → integration → **model** (accuracy, latency, fairness, drift) → E2E. Model tests are irreducible.
- **DVC versions data; the Model Registry versions models** through Staging → Production → Archived.
- **Best practices:** idempotent stages · fail fast · small data in CI, full data in CT · parameterise everything · pin action versions · secrets via GitHub Secrets only.

## ⚠️ Important Notes

**Jobs do not share a filesystem; steps within a job do.** Anything crossing a job boundary must go through `upload-artifact`/`download-artifact`.

**Artifacts are not cache.** `actions/cache` is a performance optimisation whose miss is harmless; artifacts are required outputs. Cached entries can be silently evicted.

**Without `needs:`, jobs run in parallel.** There is no implicit ordering, so a deploy job can start before training finishes.

**Guard deploy jobs with a branch condition**, or a pull request — potentially from a fork — will deploy to production. Back it with a protected environment; the `if:` alone is convention, not enforcement.

**Pin action versions (`@v4`, not `@main`).** An unpinned action can change under you, and a compromised action with `@main` executes arbitrary code with access to your secrets.

**Never hardcode credentials in workflow YAML.** Use `${{ secrets.NAME }}`. Workflow files are in the repository, visible to everyone with read access.

**A Docker PAT is shown once.** Copy it immediately; regenerating invalidates the old one and breaks running workflows.

**Automated retraining without a quality gate ships regressions automatically.** Automation amplifies whatever process it wraps.

**Validate data before retraining.** If drift is caused by a broken upstream pipeline, retraining bakes the corruption into the model.

**Promote to Staging, not straight to Production.** The registry's stages exist so a human or a canary makes the final call.

**Beware the feedback loop.** A model that influences the data it later trains on progressively narrows onto its own beliefs — the fraud model that never sees the transactions it blocked. Hold out a randomised control slice.

**Delayed labels constrain retraining cadence.** Retraining before labels arrive systematically undercounts positives.

**Keep pipeline stages idempotent.** Re-running a failed job must be safe; a stage that appends rather than overwrites corrupts data on retry.

**Fail fast — cheap checks before expensive ones.** Lint before training saves GPU minutes and shortens the feedback loop CI exists to provide.

> [!warning] Gaps in the source slides
> LaTeX Beamer with heavy TikZ diagrams and icon fonts, so extraction has artefacts (stray glyphs like `/cogs`, `Ὠ0`, `/da◎abase` are icon-font characters, not content).
> - **Slides 2, 6, 11, 19** produced no text — section dividers.
> - **Diagrams extracted only as scattered labels:** the DAG figure (slide 3), the ML pipeline DAG (slide 5), the job-dependency graph (slide 9), the CI/CT/CD pipeline (slide 13), the versioning flow (slide 14), the test pyramid (slide 15), the retraining loop (slide 16). I have reconstructed these in prose and ASCII above.
> - **Several blocks truncate mid-item:** slide 7 (the runner list, cut at "ubuntu-late"), slide 8 (**the workflow's final `Run` step is cut off** — the test command itself is not shown), slide 10 (reusable workflows, cut at "Call"), slide 14 (**the "Golden Rule" is cut at "Every model in production must"** — the completion is not recoverable), slide 17 (quality gates, cut after the schema-contract bullet), slide 18 (summary, cut at "Automat"), slide 20 (cut mid-footer), slide 21 (the PAT warning, cut at "won't be shown a"), slide 22 (**the third workflow filename is cut — `simple_mlops-ci-...`**).
> - **The actual workflow YAML files are not in the slides** — they are downloaded from [`github.com/NguyenMToan/house-price-predictor/tree/main/.github/workflows`](https://github.com/NguyenMToan/house-price-predictor/tree/main/.github/workflows). The deck names three (`mlops-ci-workflow.yaml`, `mlops-pipeline.yaml`, and a truncated third) but shows none of their contents. **The example workflows in this note are reconstructed** from the described structure.
> - **Slide 24** references a screenshot of the Actions UI.
>
> Note the deck is dated **March 30, 2026** and credited to "MLOps Course" rather than the lecturer by name, unlike the other decks.

---
**Previous:** [[08 - Monitoring with Prometheus and Grafana]] · **Next:** [[10 - Monitoring and Drift]]
