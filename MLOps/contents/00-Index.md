---
subject: MLOps
chapter: 00
tags: [ds, moc, index, mlops, production-ml]
source: "MLOPs (1) (1).pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam, December 2025"
---

# MLOps — Index

> *From Machine Learning Models to Production Systems*

**Lecturer:** Dr. Nguyen Manh Toan, PhD in Mathematics · Swinburne Vietnam
`toannguyen@swin.edu.au` · Office hours Tuesday 13–15
*Research interests: Machine Learning, Computer Vision, xAI, Topological Data Analysis*

Delivered at NEU under the Faculty of Mathematical Economics.

## 🗺️ Map of Content

### Foundations

| # | Chapter | One-line description |
|---|---|---|
| 01 | [[01 - Introduction to MLOps]] | Why models fail in production; DataOps/ModelOps/EdgeOps; DevOps vs MLOps; **data drift vs concept drift** |
| 02 | [[02 - Environment Setup]] | Four layers of isolation — virtual envs (`uv`), editors, Docker, Git/GitHub |

### The ML lifecycle

| # | Chapter | One-line description |
|---|---|---|
| 03 | [[03 - Data in MLOps]] | Data-centric AI, the four pillars, **data cascades**, ingestion at scale, lineage, scoping and PoC→MVP→Production |
| 04 | [[04 - Model Development]] | Baselines and HLP, metric choice under imbalance, augmentation, feature cost, **MLflow experiment tracking** |
| 05 | [[05 - Packaging Models with FastAPI and Docker]] | Reproducible pipelines, FastAPI + Streamlit, containerising, Docker Compose service networking |
| 06 | [[06 - Deployment]] | Cloud vs Edge, batch vs online prediction, **model risk**, and the four release strategies |

### Infrastructure and automation

| # | Chapter | One-line description |
|---|---|---|
| 07 | [[07 - Kubernetes for ML Deployment]] | kind and kubectl, Deployment vs Service, NodePort, rolling updates |
| 08 | [[08 - Monitoring with Prometheus and Grafana]] | Four monitoring dimensions, PromQL, instrumentation, ServiceMonitor, alerting |
| 09 | [[09 - CI-CD with GitHub Actions]] | DAGs, workflows and `needs:`, **CI → CT → CD**, testing strategy, automated retraining |

### Operations and safety

| # | Chapter | One-line description |
|---|---|---|
| 10 | [[10 - Monitoring and Drift]] | Training–serving skew, drift detection (K–S, KL, **JSD**), mitigation, retraining, decommission |
| 11 | [[11 - Robust AI]] | Adversarial attacks (FGSM, C&W, transfer, physical), **data poisoning**, and defences for both |

---

## 🎯 Course framing

### The problem MLOps exists to solve

- **Most ML models never reach production.**
- **Models degrade after deployment.**
- **Data distributions change over time.**
- **Reproducibility is often missing.**

> **MLOps** — a set of practices that aims to **deploy, monitor, and maintain** machine learning systems reliably and efficiently in production. Emerged around 2018–2019, inspired by DevOps.

### The one idea that runs through everything

> **Traditional software fails loudly with error messages and stack traces; machine learning systems fail silently.**

Nearly every practice in this course exists to make silent failure visible:

| Practice | The silent failure it catches |
|---|---|
| Experiment tracking ([[04 - Model Development]]) | "Which run produced this model?" |
| Data validation ([[03 - Data in MLOps]]) | Corrupt data producing confident wrong answers |
| Training–serving parity ([[06 - Deployment]]) | A good model fed the wrong features |
| Drift monitoring ([[10 - Monitoring and Drift]]) | Accuracy decaying with no error raised |
| Per-class metrics ([[11 - Robust AI]]) | One class destroyed while the aggregate holds |
| Quality gates ([[09 - CI-CD with GitHub Actions]]) | Automated retraining shipping a regression |

### Learning objectives

By the end of this course, students will be able to:
- Explain the end-to-end ML lifecycle and the role of MLOps
- Design reproducible and scalable ML pipelines using Python
- Apply DevOps principles to machine learning systems
- Manage data, model, and experiment versioning
- Deploy ML models as production-ready services
- Monitor model performance and detect data and concept drift
- Implement automated retraining and continuous improvement workflows
- Address fairness, explainability, and governance in ML systems
- Evaluate MLOps solutions in safety-critical and regulated domains
- Develop and present a complete MLOps project from data to deployment

### Timeline and assessment

| Weeks | Content |
|---|---|
| 1–5 | Foundations + Individual assignment |
| 6–11 | Core MLOps practices |
| 12 | Ethics, xAI, safety |
| 13–14 | Project-focused |
| 15 | Final exam |

| Assessment | Content | Week | Weight |
|---|---|---|---|
| Participation | Attendance, homework, discussions | 1–15 | **10%** |
| Individual Assignment | Hands-on ML pipelines | 5 | **20%** |
| Project | MLOps pipeline | 14 | **30%** |
| Final Exam | Not yet defined | 15 | **40%** |

**Tracks** — choose one for assignments and the final project:
- **Industry-Focused** — deployment, monitoring, scalability; production tools (Docker, MLflow, CI/CD); business or engineering use cases
- **Research-Focused** — experimentation, evaluation, reproducibility; model behaviour and failure modes; novel ML or MLOps techniques

> Attendance: **missing more than 3 classes results in failure to complete the course** and mandatory re-registration. Entry denied if arriving more than 10 minutes late.

### The toolchain

| Stage | Tools |
|---|---|
| Environment | **`uv`** (recommended), conda, venv · VS Code |
| Data processing | NumPy, Pandas |
| Modeling | Scikit-learn, PyTorch, TensorFlow, XGBoost |
| Experiment tracking | **MLflow**, Weights & Biases |
| Pipelines & orchestration | Airflow, Prefect, Kubeflow, ZenML |
| Versioning | **DVC**, Git |
| Serving | **FastAPI**, Streamlit, TensorFlow Serving |
| Containers | **Docker**, Docker Compose, Podman |
| Orchestration | **Kubernetes**, kind, Helm |
| CI/CD | **GitHub Actions** |
| Monitoring | **Prometheus, Grafana**, AlertManager |

### The running project

The hands-on chapters build one system end to end: **`house-price-predictor`** — `github.com/NguyenMToan/house-price-predictor`. It progresses from a reproducible training pipeline ([[05 - Packaging Models with FastAPI and Docker]]) through containerisation, Kubernetes deployment, monitoring, and automated CI/CD.

### Further reading

- **Treveil et al., *Introducing MLOps***, O'Reilly 2020 — cited throughout
- **Gift & Deza, *Practical MLOps***, O'Reilly 2021
- **Sculley et al., *Hidden Technical Debt in ML Systems*** — the paper behind "training a model is only a small part of an ML system"
- **Sambasivan et al. (2021), *"Everyone wants to do the model work, not the data work"*** — data cascades
- **Paleyes, Urma & Lawrence (2022), *Challenges in deploying machine learning***, ACM Computing Surveys
- **Nakkiran et al. (2021), *Deep double descent***
- **Costa et al. (2024), *How deep learning sees the world*** — adversarial survey
- Google MLOps Whitepaper · MLflow docs · Kubeflow Pipelines · [mlsysbook.ai](https://mlsysbook.ai/book/)

None are in `documents/`.

---

## 🔗 Cross-subject connections

| Topic | Links to |
|---|---|
| Cleaning, transformation, feature selection, pipelines, leakage | [[Data Preparation and Visualization/contents/00-Index\|Data Preparation and Visualization]] |
| Models, metrics, bias–variance, ensembles | [[Machine Learning/contents/00-Index\|Machine Learning]] |
| K–S test, t-test, A/B testing, hypothesis testing | [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] |
| Python, Pandas, packaging | [[Programming for Data Science (Python)/contents/00-Index\|Programming for Data Science]] |
| Drift as non-stationarity, CUSUM, change detection | [[Time-series Analysis/contents/00-Index\|Time-series Analysis]] |
| KL divergence, entropy | [[Probability Theory/contents/00-Index\|Probability Theory]] |

---

## ⚠️ Gaps in the source material

> [!warning] Duplicate deck
> **`MLOps_DeployingML_on_K8s.pdf` (23 pages) is a strict subset of `MLOps_K8s.pdf` (39 pages).** Slides 1–23 are identical apart from one image reference; the longer deck adds the Prometheus/Grafana section. They are **one lecture**, split here into [[07 - Kubernetes for ML Deployment]] and [[08 - Monitoring with Prometheus and Grafana]] by topic.

> [!warning] Content gaps to raise with the lecturer
> The decks are LaTeX Beamer, so **prose extracted well but every figure and TikZ diagram is an image.** The most costly losses:
>
> **1. K8s architecture (`MLOps_K8s.pdf` slide 7) is entirely an image** — the control plane / node breakdown (API server, scheduler, etcd, kubelet, kube-proxy) is unrecoverable, and it is the most examinable content in that lecture. **Slides 3–5 ("Why Kubernetes") are title-only**, so the motivation is also missing.
>
> **2. Types of concept drift (`MLOPs_Monitoring.pdf` slide 14) is an image** — the sudden/gradual/incremental/recurring taxonomy is not captured.
>
> **3. "Retraining vs Updating Model" (`MLOPs_Monitoring.pdf` slide 45) is an image** — the distinction is not recoverable.
>
> **4. Three types of ML (`Model_Development_MLOPs.pdf` slide 6) is an image** — only the key idea ("the difference lies in the type of feedback") survived.
>
> **5. MLOps architecture and tools (`MLOPs (1) (1).pdf` slides 47–48) are images** — the tool landscape is captured only via the Python library table.
>
> **6. PGD is named but never defined** in [[11 - Robust AI]], despite being the standard strong attack and the basis of adversarial training.
>
> **7. No application code appears** in [[05 - Packaging Models with FastAPI and Docker]] — `main.py`, `inference.py`, `schemas.py`, `app.py` are named but never shown. **No workflow YAML appears** in [[09 - CI-CD with GitHub Actions]]. **No Kubernetes manifests appear** anywhere — everything is created imperatively. All of these live in the project repository.
>
> **8. Many code blocks truncate mid-listing** where the PDF layout cut them — noted individually in each chapter's gap callout. Notably: the complete `prometheus_client` metric definitions, any complete AlertManager rule, the ServiceMonitor `endpoints` comment (precisely the most error-prone line), and the "Golden Rule" of model versioning.
>
> **9. Missing files:** the `enhanced_fastapi_ml_dashboard` JSON, the A/B testing demo notebook, and the Géron notebook are all referenced but absent from `documents/`.

---

## 📌 The one-page revision path

1. **ML systems fail silently** — everything else follows from this — [[01 - Introduction to MLOps]]
2. **Data drift = $P(X)$ changes; concept drift = $P(Y\mid X)$ changes.** Concept drift always breaks the model — [[01 - Introduction to MLOps]]
3. **A virtual env isolates Python packages only** — containers isolate the OS — [[02 - Environment Setup]]
4. **Most production failures are data problems**, and data cascades amplify them silently — [[03 - Data in MLOps]]
5. **Establish a baseline first**; accuracy is meaningless under imbalance — [[04 - Model Development]]
6. **Ship the preprocessor with the model**, and `transform`, never `fit_transform`, at inference — [[05 - Packaging Models with FastAPI and Docker]]
7. **Four deployment strategies:** shadow (no user impact), canary (gradual), blue–green (fast rollback), rolling (cheap, hard rollback) — [[06 - Deployment]]
8. **Deployment manages pods; Service gives a stable name** — and without a readiness probe, rollouts drop traffic — [[07 - Kubernetes for ML Deployment]]
9. **Exposing metrics ≠ collecting them** — a ServiceMonitor is separately required, and its failure is silent — [[08 - Monitoring with Prometheus and Grafana]]
10. **CI → CT → CD.** Continuous Training has no traditional equivalent, and the **quality gate** is what makes automated retraining safe — [[09 - CI-CD with GitHub Actions]]
11. **Skew appears on day one; drift emerges gradually** — and they need opposite fixes — [[10 - Monitoring and Drift]]
12. **Backdoored models pass every standard test** — [[11 - Robust AI]]

### The recurring principle

**Every safeguard in this course exists because ML failures are invisible by default.** A crashed server pages you; a model quietly predicting the majority class does not. Monitoring, quality gates, per-class metrics, lineage, and parity checks are all instruments for seeing what would otherwise go unseen.
