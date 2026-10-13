---
subject: MLOps
chapter: 01
tags: [ds, mlops, devops, ml-lifecycle, drift, production-ml]
source: "MLOPs (1) (1).pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam, December 2025"
---

# Introduction to MLOps

Lecturer: Dr. Nguyen Manh Toan (Swinburne Vietnam), delivered at NEU. Course map in [[00-Index]].

## 📘 Main Knowledge

### Why MLOps exists

- Most ML models never reach production.
- Models degrade after deployment.
- Data distributions change over time.
- Reproducibility is often missing.

Training a model is only a small part of an ML system (Sculley et al., *Hidden Technical Debt in ML Systems*): the ML code is a small box among configuration, data collection, serving infrastructure and monitoring.

### Definition

**MLOps** is a set of practices to **deploy, monitor and maintain** ML systems reliably and efficiently in production. It emerged around 2018–2019, is inspired by DevOps, focuses on data, models and pipelines, and enables reproducibility and scalability.

### Three components

| Component | Concern | Practices |
|---|---|---|
| **DataOps** | data across its lifecycle | data version control; exploration and ETL; feature engineering and labelling ([[Data Preparation and Visualization/contents/00-Index\|Data Preparation]]) |
| **ModelOps** | models across their lifecycle | versioning; deployment; monitoring; security and privacy |
| **EdgeOps** | the network edge, where data is generated and real-time action is needed | platform-specific builds (quantization, pruning, compression); optimization under limited compute; distributed optimization (federated learning) |

### Five benefits

| Benefit | What it delivers |
|---|---|
| Reproducibility | versioned code, data, configs and models |
| Scalability | efficient training and inference, distributed deployment |
| Monitoring and maintenance | drift detection, automated retraining |
| Collaboration | standard workflows across data science, engineering, operations |
| Compliance and governance | auditability, privacy, accountability |

### DevOps vs MLOps

**DevOps** joins development and IT operations through culture, automation, CI/CD, infrastructure as code and monitoring. MLOps shares automation, CI/CD and version control, and adds:

| Aspect | DevOps | MLOps |
|---|---|---|
| Focus | software | ML models and software |
| Artifacts / versioning | code | code, data, models |
| Behaviour | deterministic | probabilistic |
| Testing | unit, integration | plus data validation, model evaluation |
| Monitoring | system health | plus performance, drift, bias |
| Maintenance | bug fixes | continuous retraining |

The key difference is determinism. An ML system's behaviour depends on its training data and on the data it now receives, so it can be wrong while every test passes and every server is healthy.

### The ML lifecycle

**Scoping → Data → Modeling → Deployment**, iterative: error analysis sends you back to data, monitoring back to modelling.

### Case study: credit card fraud detection

| Stage | Content |
|---|---|
| Scoping | Detect fraud in near real time, few false alarms. Constraints: costly false negatives, annoyed customers from false positives, latency, regulation (GDPR). Metrics: PR-AUC, false positive rate, average fraud loss per customer. |
| Data | Transactions, customer profiles, investigated fraud labels. Challenges: fraud < 0.5%, sensitive data, noisy delayed labels (chargebacks). Preparation: velocity and spending-deviation features, label verification, **time-based split** to avoid leakage. |
| Modeling | Logistic regression (baseline), XGBoost, Isolation Forest (new patterns). Cost-sensitive learning, threshold tuning with a business cost matrix, temporal cross-validation. Error analysis by segment; bias checks across regions and demographics. |
| Deployment | Real-time API (< 100 ms), weekly/monthly batch retraining, **feature store** for training/inference consistency. Monitor data drift, concept drift, decay. Alerts, human review of edge cases, compliance audits. |

Lessons: fraud detection is a continuous system, not a one-time model; drift is inevitable; monitoring and retraining matter as much as accuracy; interpretability is needed for trust and regulation.

### Challenges

Many dependencies (data and business needs change); teams that don't share tools or vocabulary; data scientists are not software engineers.

### Data drift vs concept drift

- **Data drift**: the input distribution changes, $P_{train}(X)\ne P_{prod}(X)$. Example: a shopping model deployed during a sales event.
- **Concept drift**: the input–output relationship changes, $P_{before}(Y\mid X)\ne P_{after}(Y\mid X)$. Example: the link between customer features and default shifts after a regulatory or economic change.

Data drift means different customers; concept drift means the same customer now behaves differently. A model may survive data drift; concept drift changes the function being learned.

### Roles

| Role | Responsibility |
|---|---|
| Business stakeholder | business goal, ROI communication |
| Solution architect | architecture and technology choice |
| Data scientist | business problem → ML problem; modelling |
| Data engineer | data and feature pipelines, feature store |
| Software engineer | design patterns, code quality |
| DevOps engineer | CI/CD, orchestration, deployment, monitoring |
| ML/MLOps engineer | cross-domain mix of all the above |

### Python for MLOps

| Stage | Libraries |
|---|---|
| data processing | NumPy, Pandas |
| modeling | scikit-learn, PyTorch, TensorFlow |
| experiment tracking | MLflow, Weights & Biases |
| orchestration | Airflow, Prefect |
| versioning | DVC, Git |
| deployment | FastAPI, Flask |

Reproducibility: fix seeds; log parameters, metrics, artifacts; version data and models; use virtual environments.

Live demo:
```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
X, y = load_iris(return_X_y=True)
model = LogisticRegression()
model.fit(X, y)

import mlflow.sklearn
mlflow.sklearn.log_model(model, "iris_model")
```
The model goes to `./mlruns`; an MLflow Tracking server can store it in S3, Azure Blob or GCS. The lecturer asks: how can the model be reproduced? (Exercise 5.)

## ✏️ Exercises

**1.** (Slide 27 quiz) DevOps or MLOps? (1) automating deployment with CI/CD; (2) monitoring prediction accuracy; (3) versioning datasets and model artifacts; (4) managing cloud infrastructure with Terraform; (5) detecting data drift; (6) rolling back a failed release.

> [!example]- Solution
> Hint: does the task involve data or models? DevOps: 1, 4, 6. MLOps: 2, 3, 5.
> MLOps adds to DevOps rather than replacing it. Task 6 is a boundary case: rolling back a release is DevOps, rolling back to an older model version because accuracy fell is MLOps.

**2.** (Slide 39 quiz) Data or concept drift? (a) At the start of COVID-19, fraud systems failed because many people who rarely shopped online began doing so heavily. (b) With inflation, the same house sells for more over time.

> [!example]- Solution
> (a) Mainly data drift: the share of online transactions, $P(X)$, shifted. There is also concept drift: "rare online shopper suddenly buys online" used to signal fraud and became normal, so $P(Y\mid X)$ changed too. That second part is what breaks the model.
> (b) Concept drift: house features are unchanged; the mapping from features to price moved. It is gradual, so input monitoring won't catch it; watch residuals for systematic under-prediction.

**3.** (Slide 40 quiz) Driving-behaviour profiling: which illustrates concept drift? A) sensor noise increases; B) seasonal changes alter driver behaviour; C) missing values appear; D) feature scaling is incorrect.

> [!example]- Solution
> **B**: in winter, hard braking means something different, so $P(Y\mid X)$ changes.
> A is data drift (a data quality change in $P(X)$); C is a pipeline problem; D is a bug. Each needs a different response: retrain (concept drift), check generalization (data drift), fix the pipeline, fix the code.

**4.** In the fraud case, why is "99.5% accurate" meaningless? What should be reported?

> [!example]- Solution
> Fraud is under 0.5%, so predicting "never fraud" scores over 99.5% and catches nothing. Report PR-AUC (ignores the mass of true negatives), false positive rate (customer annoyance), and fraud loss per customer (a business metric). Costs are asymmetric, so the threshold is set from the cost matrix, not left at 0.5. Measured performance is provisional because labels arrive late, and aggregate metrics can hide a failing segment. Choose metrics at scoping, before modelling.

**5.** (Slide 57) How can the demo model be reproduced?

> [!example]- Solution
> As written it can't be reliably. `log_model` saves the fitted object but not:
> 1. the code version (commit);
> 2. the data version (iris is fixed, real data isn't: DVC);
> 3. parameters (defaults change: `LogisticRegression`'s default solver moved from `liblinear` to `lbfgs` in scikit-learn 0.22);
> 4. the environment (Python and library versions; a pickle may not load under another scikit-learn);
> 5. the random seed (needed for splits, stochastic solvers, network initialisation).
>
> ```python
> import subprocess, mlflow, mlflow.sklearn
> from sklearn.linear_model import LogisticRegression
> from sklearn.datasets import load_iris
> from sklearn.metrics import accuracy_score
>
> params = {"solver": "lbfgs", "max_iter": 200, "C": 1.0, "random_state": 42}
> with mlflow.start_run():
>     X, y = load_iris(return_X_y=True)
>     model = LogisticRegression(**params).fit(X, y)
>     mlflow.log_params(params)
>     mlflow.log_metric("train_accuracy", accuracy_score(y, model.predict(X)))
>     mlflow.set_tag("git_commit", subprocess.check_output(
>         ["git", "rev-parse", "HEAD"]).decode().strip())
>     mlflow.sklearn.log_model(model, "iris_model")  # also writes conda.yaml, requirements.txt
> ```
> This is the slide-58 homework: train, log parameters and metrics, save and version the model.

## 📝 Summary

- MLOps: deploy, monitor and maintain ML systems in production; from ~2018–2019, built on DevOps.
- Components: DataOps, ModelOps, EdgeOps.
- MLOps versions data and models as well as code, and its systems are probabilistic: hence data validation, drift monitoring, retraining.
- Lifecycle: scoping → data → modeling → deployment, with feedback loops.
- Data drift: $P(X)$ changes; concept drift: $P(Y\mid X)$ changes.
- Seven roles, from business stakeholder to ML engineer.
- Reproducibility needs code, data, parameters, environment and seed, not just the model file.

## ⚠️ Important Notes

1. A saved model file is not reproducibility.
2. Library defaults change between versions; log parameters explicitly.
3. Accuracy misleads on imbalanced problems; use PR-AUC and cost metrics.
4. Use time-based splits for temporal data (temporal folds in the fraud case).
5. A feature store prevents train/serve skew (features computed differently at training and inference).
6. Missing values and wrong scaling are not drift; don't answer them by retraining.
7. Gradual concept drift leaves $P(X)$ unchanged; monitor residuals.
8. Delayed labels make live accuracy unmeasurable; use proxies (prediction distribution, confidence).
9. Aggregate metrics can hide failing segments.
10. The deliverable is the system, not the model.

> [!warning] Gaps in the source slides
> - Image-only slides: 14 (Sculley diagram), 15 (growth chart), 20 ("Fun Example"), 29 (lifecycle diagram), 38 (likely a drift illustration), 42 (people diagram), 47–48 (typical architecture, tool landscape), 54 (experiment tracking example).
> - Slide 40's quiz answer is blank in the source; B is my answer.
> - Further reading (slide 61): Treveil et al., *Introducing MLOps* (2020); Gift & Deza, *Practical MLOps* (2021); Google MLOps whitepaper; Sculley et al.; MLflow and Kubeflow docs.
> - Assessment (slide 7): participation 10%, individual assignment (week 5) 20%, project (week 14) 30%, final exam (week 15) 40%. Tracks (slide 8): industry-focused or research-focused.

**Next:** [[02 - Environment Setup]]
