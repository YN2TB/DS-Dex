---
subject: MLOps
chapter: 00
tags: [ds, moc, index, mlops, production-ml]
source: "MLOPs (1) (1).pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam, December 2025"
---

# MLOps: Index

From machine learning models to production systems. Lecturer: Dr. Nguyen Manh Toan (Swinburne Vietnam), delivered at NEU.

## Map of content

| # | Chapter | Topics | Status |
|---|---|---|---|
| 01 | [[01 - Introduction to MLOps]] | why models fail in production; DataOps/ModelOps/EdgeOps; DevOps vs MLOps; data vs concept drift | ✅ |
| 02 | [[02 - Environment Setup]] | `uv` environments, editors, Docker, Git and GitHub | ✅ |
| 03 | [[03 - Data in MLOps]] | data-centric AI, four pillars, data cascades, ingestion, lineage, scoping | ✅ |
| 04 | [[04 - Model Development]] | baselines and HLP, metrics under imbalance, augmentation, MLflow | ✅ |
| 05 | [[05 - Packaging Models with FastAPI and Docker]] | reproducible pipeline, FastAPI + Streamlit, containers, Compose networking | ✅ |
| 06 | [[06 - Deployment]] | cloud vs edge, batch vs online prediction, model risk, release strategies, A/B tests | ✅ |
| 07 | [[07 - Kubernetes for ML Deployment]] | kind, kubectl, Deployments and Services, rolling updates | ✅ |
| 08 | [[08 - Monitoring with Prometheus and Grafana]] | monitoring dimensions, PromQL, instrumentation, ServiceMonitor, alerts | ✅ |
| 09 | [[09 - CI-CD with GitHub Actions]] | DAGs, workflows, CI → CT → CD, testing layers, automated retraining | ✅ |
| 10 | [[10 - Monitoring and Drift]] | skew vs drift, KS/KL/JSD, mitigation, retraining, decommissioning | ✅ |
| 11 | [[11 - Robust AI]] | adversarial attacks, data poisoning, defences | ✅ |

The running project is `house-price-predictor` (`github.com/NguyenMToan/house-price-predictor`): pipeline (ch. 05), containers, Kubernetes, monitoring, CI/CD.

## Course

The main idea: traditional software fails loudly; ML systems fail silently. Most practices in the course make silent failures visible: experiment tracking (ch. 04), data validation (03), training–serving parity (05–06), drift monitoring (10), per-class metrics (04, 11), quality gates (09).

| Weeks | Content |
|---|---|
| 1–5 | foundations, individual assignment |
| 6–11 | core MLOps practice |
| 12 | ethics, explainability, safety |
| 13–14 | project |
| 15 | final exam |

Assessment: participation 10%, individual assignment (week 5) 20%, project (week 14) 30%, final exam (week 15) 40%. Tracks: industry-focused or research-focused. Missing more than 3 classes means failing the course.

| Stage | Tools |
|---|---|
| environment | `uv`, conda, venv, VS Code |
| modelling | scikit-learn, XGBoost, PyTorch, TensorFlow |
| tracking and versioning | MLflow, W&B, DVC, Git |
| serving | FastAPI, Streamlit, TF Serving |
| containers and orchestration | Docker, Compose, Kubernetes, kind, Helm |
| CI/CD | GitHub Actions |
| monitoring | Prometheus, Grafana, AlertManager |

Further reading (none in `documents/`): Treveil et al., *Introducing MLOps* (2020); Gift & Deza, *Practical MLOps* (2021); Sculley et al., *Hidden Technical Debt in ML Systems*; Sambasivan et al. (2021); Paleyes et al. (2022); Nakkiran et al. (2021); Costa et al. (2024); mlsysbook.ai.

## Cross-subject links

| Topic | Subject |
|---|---|
| cleaning, features, pipelines, leakage | [[Data Preparation and Visualization/contents/00-Index\|Data Preparation and Visualization]] |
| models, metrics, ensembles | [[Machine Learning/contents/00-Index\|Machine Learning]] |
| KS test, t-test, A/B tests | [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] |
| Spark, Kafka, Airflow | [[Big Data Analytics/contents/00-Index\|Big Data Analytics]] |
| change detection, non-stationarity | [[Time-series Analysis/contents/00-Index\|Time-series Analysis]] |
| KL divergence, entropy | [[Probability Theory/contents/00-Index\|Probability Theory]] |

## Gaps in the source material

> [!warning] One lecture in two files
> `MLOps_DeployingML_on_K8s.pdf` (23 pp) is a subset of `MLOps_K8s.pdf` (39 pp); the longer deck adds Prometheus/Grafana. Split by topic into ch. 07 and 08.

The decks are LaTeX Beamer: prose extracted well, figures and TikZ diagrams did not.
1. The Kubernetes architecture slide (`MLOps_K8s.pdf` slide 7) is an image, and slides 3–5 ("Why Kubernetes") have titles only.
2. "Types of Concept Drift" and "Retraining vs Updating Model" (`MLOPs_Monitoring.pdf` slides 14, 45) are images.
3. The three types of ML (`Model_Development_MLOPs.pdf` slide 6) and the tool landscape (`MLOPs (1) (1).pdf` slides 47–48) are images.
4. PGD is named but not defined (definition added in ch. 11).
5. No application code, workflow YAML or Kubernetes manifests appear in the decks; they are in the project repository. Code in ch. 05–09 is reconstructed and labelled.
6. Many code blocks are cut off by the layout; each chapter lists them.
7. Referenced but missing: the `enhanced_fastapi_ml_dashboard` JSON, the A/B testing notebook, the Géron notebook.

**Errata and corrections (2026-10-09 rewrite):**
- `MLOPs_RobustAI.pdf` slide 9 prints the targeted C&W loss with an untargeted constraint (ch. 11).
- ch. 02: the `.gitignore` example put several patterns and comments on one line, which Git doesn't parse.
- ch. 05: the production Compose health check used `curl`, which `python:3.11-slim` lacks.
- ch. 11: the EAD formula extracts in full (previously marked truncated).
