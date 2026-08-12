---
subject: MLOps
chapter: 01
tags: [ds, mlops, devops, ml-lifecycle, drift, production-ml]
source: "MLOPs (1) (1).pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam, December 2025"
---

# Introduction to MLOps

> *From Machine Learning Models to Production Systems*

> [!note] Course context
> **Lecturer:** Dr. Nguyen Manh Toan (PhD in Mathematics), Swinburne Vietnam · `toannguyen@swin.edu.au` · Office hours Tuesday 13–15. Research interests: Machine Learning, Computer Vision, xAI, Topological Data Analysis.
>
> Delivered at NEU under the Faculty of Mathematical Economics. See [[00-Index]] for the full course map.

## 📘 Main Knowledge

### Why MLOps exists

Four facts motivate the entire discipline:

- **Most ML models never reach production.**
- **Models degrade after deployment.**
- **Data distributions change over time.**
- **Reproducibility is often missing.**

The framing image: *training a model is only a small part of an ML system* — the reference is Sculley et al.'s *Hidden Technical Debt in Machine Learning Systems*, where the ML code is a small box surrounded by far larger boxes for configuration, data collection, serving infrastructure, and monitoring.

### Definition

> **MLOps** — a set of practices that aims to **deploy, monitor, and maintain** machine learning systems **reliably and efficiently in production**.

- A relatively new discipline, emerging around **2018–2019**.
- **Inspired by DevOps**, which streamlines software changes and updates.
- Focuses on **data, models, and pipelines**.
- Enables **reproducibility and scalability**.

### The three components

| Component | Concern |
|---|---|
| **DataOps** | Management and optimisation of data throughout its lifecycle |
| **ModelOps** | Development, deployment, and monitoring of ML models |
| **EdgeOps** | Operations at the network edge, where data is generated and real-time action is required |

**DataOps** — fundamental to any ML workflow:
- **Data version control** — track changes to data over time so training and validation data are reproducible and auditable.
- **Data exploration and processing** — ETL of raw data into a usable format, ensuring quality.
- **Feature engineering and labelling** — creating features and accurately labelling data for supervised learning. Compare [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]], which is this stage in depth.

**ModelOps** — managing models across their lifecycle:
- **Model versioning** — train and validate multiple versions with accurate tracking and comparison.
- **Model deployment** — move a trained model into production, integrated with existing systems.
- **Model monitoring** — continually check that accuracy and reliability hold over time.
- **Model security and privacy** — protect models and data from unauthorised access, and comply with data protection regulation.

**EdgeOps** — increasingly important as more devices process data locally:
- **Platform-specific model builds** — optimise for particular devices using **quantization, pruning, or compression** to shrink models while preserving accuracy.
- **Edge model optimization** — performance and stability where compute is limited.
- **Distributed optimization** — across many devices, often via **federated learning**.

### Why MLOps matters — five benefits

| Benefit | What it delivers |
|---|---|
| **Reproducibility** | Versioning of code, data, configurations, and models → reliable experiment reproduction and debugging |
| **Scalability** | Efficient scaling of training and inference, including distributed deployment |
| **Monitoring & Maintenance** | Continuous performance monitoring and automated retraining detect data and concept drift |
| **Collaboration** | Standardised workflows across data scientists, engineers, and operations |
| **Compliance & Governance** | Auditability, policy enforcement, data privacy, model accountability |

### DevOps, and how MLOps differs

**DevOps** integrates software development (Dev) and IT operations (Ops) to deliver applications faster and more reliably, through **Culture** (collaboration), **Automation** (build, test, deploy), **CI/CD**, **Infrastructure as Code**, and **Monitoring**. Goal: shorter release cycles with better quality and stability.

**Shared principles:** automation, CI/CD pipelines, and version control for traceability and reproducibility.

**The differences — the central table of the lecture:**

| Aspect | DevOps | MLOps |
|---|---|---|
| **Primary focus** | Software systems | ML models **and** software |
| **Core artifacts** | Code | Code, **data**, and **models** |
| **Versioning** | Code only | Code, data, and models |
| **System behavior** | **Deterministic** | **Probabilistic** |
| **Testing** | Unit and integration tests | **Data validation, model evaluation** |
| **Monitoring** | System health | **Model performance, drift, bias** |
| **Maintenance** | Bug fixes | **Continuous retraining** |

> **Key takeaway:** MLOps extends DevOps by addressing the unique challenges of **data-driven, continuously evolving** machine learning systems.

The deepest difference is **deterministic vs probabilistic**. Traditional software given the same input returns the same output, and correctness is a matter of passing tests. An ML system's behaviour depends on data it was trained on and data it now receives — so it can be *silently wrong* while every unit test passes and every server is healthy.

### The ML lifecycle

> **The ML lifecycle is iterative, not linear.** During a later stage, we might go back to an earlier stage.

The standard stages — **Scoping → Data → Modeling → Deployment** — with feedback loops throughout. Error analysis sends you back to data collection; monitoring sends you back to modelling.

### Case study: credit card fraud detection

The lecturer's worked example, stage by stage.

**Scoping.** *Goal:* detect fraudulent transactions in near real time, reducing losses while minimising false alarms.
*Business constraints:* high cost of false negatives (missed fraud); customer dissatisfaction from false positives; strict latency and regulatory requirements (e.g. GDPR).
*Success metrics:* Precision–Recall AUC · False Positive Rate · average fraud loss per customer.

**Data.** *Sources:* transaction records (amount, merchant, location, time), customer profiles, historical fraud labels from investigations.
*Challenges:* **extreme class imbalance (fraud < 0.5%)**; sensitive personal data; **noisy labels** (chargebacks may be delayed).
*Preparation:* feature engineering (velocity features, spending deviation); label verification and deduplication; **train–validation split based on time, to avoid leakage**.

**Modeling.** *Choices:* Logistic Regression (baseline, interpretable), Gradient Boosted Trees (XGBoost), Isolation Forest (novel fraud patterns).
*Training:* cost-sensitive learning; threshold tuning against a business cost matrix; **cross-validation with temporal folds**.
*Error analysis:* false positives by customer segment; missed fraud cases; **bias checks across regions and demographics**.

**Deployment.** *Setup:* real-time inference API (**sub-100 ms latency**); batch retraining pipeline (weekly or monthly); **feature store for consistency between training and inference**.
*Monitoring:* data drift (transaction amount distributions), concept drift (new fraud strategies), performance decay.
*Maintenance:* automated alerts; **human-in-the-loop review** for edge cases; regular compliance audits.

**The lessons:**
- Fraud detection is **not a one-time model, but a continuous system**.
- Data drift and concept drift are **inevitable**.
- **Monitoring and retraining are as important as model accuracy.**
- **Interpretability is critical** for trust and regulation.

### Challenges

- **Many dependencies.** Data changes constantly, and business needs shift too.
- **Not everyone speaks the same language.** Business, data science, and IT teams are all involved, and none use the same tools.
- **Data scientists are not software engineers** — specialised in model building and assessment, not necessarily in writing applications.

### Data drift vs concept drift

**The distinction to memorise.**

**Data drift** — the **input distribution** changes:
$$P_{train}(X) \ne P_{prod}(X)$$
*Example:* an e-commerce model trained on regular shopping behaviour, deployed during a sales event.

**Concept drift** — the **relationship between inputs and outputs** changes:
$$P_{before}(Y \mid X) \ne P_{after}(Y \mid X)$$
*Example:* in a credit risk model, the relationship between customer features and loan default shifts due to regulatory or economic change.

The practical difference: data drift means *you are seeing different customers*; concept drift means *the same customer now behaves differently*. Data drift may leave a model still correct; concept drift always breaks it, because the function being learned has changed.

### People in MLOps

> MLOps involves many different people with **completely different skill sets**, often using **entirely different tools**.

| Role | Responsibility |
|---|---|
| **Business Stakeholder** (Product Owner, Project Manager) | Defines the business goal; handles communication, e.g. presenting ROI |
| **Solution Architect** (IT Architect) | Designs the architecture and selects technologies after thorough evaluation |
| **Data Scientist** (ML Specialist/Developer) | Translates the business problem into an ML problem; model engineering, algorithm and hyperparameter selection |
| **Data Engineer** (DataOps Engineer) | Builds and manages data and feature engineering pipelines; ensures ingestion into the feature store |
| **Software Engineer** | Applies design patterns and coding standards to turn the raw ML problem into a well-engineered product |
| **DevOps Engineer** | Bridges development and operations; CI/CD automation, workflow orchestration, deployment, monitoring |
| **ML / MLOps Engineer** | **Cross-domain** — combines data science, data engineering, software engineering, DevOps, and backend skills |

### Python for MLOps

**Why Python:** rich ML ecosystem (NumPy, Pandas, PyTorch, TensorFlow) · strong tooling for experimentation and automation · easy integration with cloud and DevOps tools · large community and industry adoption.

**Key libraries by stage:**

| Stage | Libraries |
|---|---|
| Data Processing | NumPy, Pandas |
| Modeling | Scikit-learn, PyTorch, TensorFlow |
| Experiment Tracking | **MLflow**, Weights & Biases |
| Pipelines & Orchestration | Airflow, Prefect |
| Versioning | **DVC**, Git |
| Deployment | FastAPI, Flask |

**Reproducibility requirements:** fix random seeds · log parameters, metrics, and artifacts · version datasets and models · use virtual environments (conda, venv).

**Live demo — training and logging a model:**

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
model = LogisticRegression()
model.fit(X, y)

import mlflow.sklearn
mlflow.sklearn.log_model(model, "iris_model")
```

The model is stored in a local `./mlruns` directory. Remote storage — Amazon S3, Azure Blob Storage, Google Cloud Storage — can be connected via the **MLflow Tracking server**.

*The lecturer's question: **How can the model be reproduced?*** (See Exercise 5.)

## ✏️ Exercises

**1.** *(Slide 27 quiz)* For each task, decide whether it belongs primarily to **DevOps** or **MLOps**: (1) automating application deployment with CI/CD; (2) monitoring prediction accuracy in production; (3) versioning training datasets and model artifacts; (4) managing cloud infrastructure with Terraform; (5) detecting data drift in incoming streams; (6) rolling back a failed production release.

> [!example]- Solution
> The hint given is: *does the task involve data or models?*
>
> | # | Task | Answer |
> |---|---|---|
> | 1 | CI/CD deployment automation | **DevOps** |
> | 2 | Monitoring prediction accuracy | **MLOps** |
> | 3 | Versioning datasets and model artifacts | **MLOps** |
> | 4 | Terraform infrastructure | **DevOps** |
> | 5 | Detecting data drift | **MLOps** |
> | 6 | Rolling back a failed release | **DevOps** |
>
> The pattern maps exactly onto the comparison table: tasks 1, 4, 6 concern **code and infrastructure** and are deterministic — a deployment either succeeded or it did not. Tasks 2, 3, 5 concern **data and models** and are probabilistic — accuracy is a distribution, drift is a statistical claim.
>
> Worth noting that MLOps does not *replace* the DevOps tasks; it **adds** to them. An MLOps engineer still needs CI/CD and rollback. The right reading of the quiz is not "these three are someone else's job" but "MLOps = DevOps **plus** the data/model column."
>
> Task 6 is the most interesting boundary case. Rolling back a *release* is DevOps, but rolling back to a previous **model version** because accuracy dropped is MLOps — the mechanism is identical, the trigger is statistical rather than an error log.

**2.** *(Slide 39 quiz)* Classify each as data drift or concept drift:
> (a) When COVID-19 hit, fraud systems stopped working because purchase patterns changed suddenly — many people who rarely shopped online started doing so heavily.
> (b) Because of inflation, houses become more expensive over time; the same size house ends up with a higher price.

> [!example]- Solution
> **(a) Primarily data drift — but with concept drift too.**
>
> The *input distribution* changed: $P(X)$ for "proportion of transactions that are online" shifted dramatically. Customers who never shopped online now did, so the model saw inputs unlike its training data. That is $P_{train}(X) \ne P_{prod}(X)$ — **data drift**.
>
> But there is a second layer. Before COVID, "a customer who never shops online suddenly making an online purchase" was a genuine **fraud signal**. After COVID, that same pattern became normal behaviour. So $P(Y \mid X)$ changed too — **concept drift**. The feature did not merely become more common; it **stopped meaning what it used to mean**.
>
> This is why the example is a good one: real shocks usually produce both, and the concept drift is the part that actually breaks the model. Pure data drift can leave a well-generalising model intact; concept drift cannot.
>
> **(b) Concept drift.**
>
> The features (size, location, bedrooms) are unchanged in distribution — houses are not getting bigger. What changed is the **mapping** from features to price: $P(\text{price} \mid \text{size})$ has shifted upward. The same $X$ now yields a different $Y$. That is the definition of concept drift.
>
> This particular form has a name: **gradual concept drift**, as opposed to the sudden variety in (a). It is insidious precisely because no alert fires — the input distribution looks fine, and only the errors grow, slowly and in one direction. Monitoring input distributions alone would never catch it; you need to monitor **residuals**, and watch for systematic under-prediction.

**3.** *(Slide 40 quiz)* Profiling driving behaviour — which scenario best illustrates **concept drift**? A) Sensor noise increases · B) Seasonal changes alter driver behavior · C) Missing values appear · D) Feature scaling is incorrect

> [!example]- Solution
> **Answer: B — Seasonal changes alter driver behavior.**
>
> If winter conditions make drivers brake harder and accelerate more gently, then the *relationship* between sensor readings and the label "aggressive driver" has changed. Hard braking in January means something different from hard braking in July. $P(Y\mid X)$ has shifted — concept drift.
>
> **Why the others are wrong, and each for a different reason:**
>
> **A) Sensor noise increases** — this changes $P(X)$, the input distribution, so it is **data drift** (specifically a data quality issue). The true relationship between driving behaviour and the label is unchanged; the measurement has just become less reliable.
>
> **C) Missing values appear** — a **data quality / pipeline** problem, not drift in either sense. Something broke upstream. It needs fixing, not retraining.
>
> **D) Feature scaling is incorrect** — a **bug**, not drift. The world did not change; the code is wrong. Retraining on incorrectly scaled data would make things worse.
>
> The distinction matters operationally because **each demands a different response**. Concept drift → retrain on recent data. Data drift → investigate whether the model still generalises, possibly retrain. Data quality → fix the pipeline. Bug → fix the code. Treating all four as "the model needs retraining" wastes effort and can entrench the error.

**4.** Using the fraud detection case study, explain why "the model is 99.5% accurate" is a meaningless claim, and what should be reported instead.

> [!example]- Solution
> **Fraud is under 0.5% of transactions.** A model that predicts "not fraud" for *every* transaction achieves **99.5%+ accuracy** while catching zero fraud and delivering zero business value. Accuracy on a severely imbalanced problem measures the class balance, not the model.
>
> **What the case study says to report instead:**
> - **Precision–Recall AUC** — the appropriate summary under heavy imbalance, because it ignores the vast pool of true negatives that inflates accuracy and ROC-AUC alike.
> - **False Positive Rate** — directly tied to the stated constraint of customer dissatisfaction.
> - **Average fraud loss per customer** — a *business* metric in currency, not a statistical one.
>
> That third metric is the important one. The scoping stage names asymmetric costs: **false negatives cost money** (the fraud succeeds), **false positives cost goodwill** (a legitimate card is declined). These are not equal, and no single-threshold accuracy figure can express the trade-off. Hence the case study's "**threshold tuning based on business cost matrix**" — the decision threshold is a *business* parameter, not a statistical default of 0.5.
>
> Two further complications the case study raises. **Labels are noisy** because chargebacks are delayed — so today's "not fraud" label may become "fraud" in three months, meaning measured performance is itself provisional. And **bias checks across regions and demographics** are required: a model can hit its aggregate metric while performing terribly for one customer segment, which is both an ethical and a regulatory problem.
>
> The general principle: **choose the metric during scoping, from the business constraints, before any modelling.** The same lesson as choosing $\alpha$ before seeing the data in [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|Hypothesis Testing]].

**5.** *(Slide 57)* The lecturer asks: **"How can the model be reproduced?"** Answer it fully for the MLflow demo.

> [!example]- Solution
> ```python
> X, y = load_iris(return_X_y=True)
> model = LogisticRegression()
> model.fit(X, y)
> mlflow.sklearn.log_model(model, "iris_model")
> ```
> **As written, it cannot be reliably reproduced.** `log_model` saves the *artifact* — the fitted object — but not the information needed to *recreate* it. Five things are missing:
>
> **1. Code version.** Which commit produced this? Without it you cannot know what preprocessing ran.
> **2. Data version.** `load_iris` is a fixed built-in, so this demo is safe — but any real dataset changes, and "trained on the customer table" is not a specification. This is what **DVC** exists for.
> **3. Parameters.** `LogisticRegression()` used defaults, but defaults **change between library versions**. `solver` switched from `liblinear` to `lbfgs` in scikit-learn 0.22 — same code, different model.
> **4. Environment.** Python version, scikit-learn version, OS, and BLAS implementation all affect results. A pickled model may not even *load* under a different scikit-learn version.
> **5. Random seed.** Not an issue for this deterministic solver, but essential for anything involving `train_test_split`, stochastic solvers, or neural network initialisation.
>
> **The reproducible version:**
> ```python
> import mlflow, mlflow.sklearn
> from sklearn.linear_model import LogisticRegression
> from sklearn.datasets import load_iris
> from sklearn.metrics import accuracy_score
>
> SEED = 42
> params = {"solver": "lbfgs", "max_iter": 200, "C": 1.0, "random_state": SEED}
>
> with mlflow.start_run():
>     X, y = load_iris(return_X_y=True)
>     model = LogisticRegression(**params).fit(X, y)
>
>     mlflow.log_params(params)
>     mlflow.log_metric("train_accuracy", accuracy_score(y, model.predict(X)))
>     mlflow.set_tag("git_commit", subprocess.check_output(
>         ["git", "rev-parse", "HEAD"]).decode().strip())
>     mlflow.sklearn.log_model(model, "iris_model")   # logs conda env + requirements
> ```
> `mlflow.sklearn.log_model` writes a `conda.yaml` and `requirements.txt` alongside the artifact, capturing item 4 automatically — which is exactly why it is preferable to a bare `pickle.dump`.
>
> This connects to the lecture's opening claim that **reproducibility is often missing**. It is missing because the naive version *looks complete* — you have a saved model file, and it loads. The failure only appears months later when someone asks why the numbers changed, and there is no way to find out.
>
> The homework (slide 58) is exactly this: train a model, log parameters and metrics with MLflow, and save and version the trained model.

## 📝 Summary

- **MLOps** = practices to **deploy, monitor, and maintain** ML systems reliably in production. Emerged ~2018–2019, inspired by DevOps.
- **Motivation:** most models never reach production, models degrade, distributions shift, reproducibility is missing.
- **Three components:** **DataOps** (data lifecycle), **ModelOps** (model lifecycle), **EdgeOps** (on-device deployment).
- **Five benefits:** reproducibility, scalability, monitoring & maintenance, collaboration, compliance & governance.
- **MLOps extends DevOps**: it versions **data and models** as well as code, and its systems are **probabilistic** rather than deterministic — so it needs data validation, drift monitoring, and continuous retraining.
- **The ML lifecycle is iterative** — Scoping → Data → Modeling → Deployment, with feedback at every stage.
- **Data drift:** $P(X)$ changes. **Concept drift:** $P(Y\mid X)$ changes. Concept drift always breaks the model.
- **MLOps is interdisciplinary** — seven distinct roles, from Business Stakeholder to the cross-domain ML/MLOps Engineer.
- **Reproducibility requires versioning code, data, parameters, environment, and seeds** — not just saving the model file.

## ⚠️ Important Notes

**Saving a model is not reproducibility.** The artifact alone omits code version, data version, parameters, environment, and seed. All five are needed to recreate a result.

**Library defaults change between versions.** `LogisticRegression()` in scikit-learn 0.21 and 0.22 use different solvers. Log parameters explicitly, and never rely on a default being stable.

**Accuracy is the wrong metric on imbalanced problems.** With fraud below 0.5%, predicting "never fraud" scores 99.5%. Use PR-AUC and business-cost metrics, chosen at the scoping stage.

**Time-based splits are mandatory for temporal data.** Random splits let future information leak into training — the same leakage principle as [[Data Preparation and Visualization/contents/06 - Data Cleaning|Data Cleaning]], but here the leak is through *time* rather than through preprocessing. Fraud detection uses **temporal folds** for exactly this reason.

**A feature store exists to prevent train/serve skew.** If training computes a feature one way and the inference API another, the model receives inputs it was never trained on. This class of bug is silent and common.

**Distinguish drift from data quality problems and from bugs.** Missing values and incorrect scaling are *not* drift and must not be answered by retraining. Each cause has a different remedy.

**Concept drift is invisible to input monitoring.** Gradual concept drift (house prices under inflation) leaves $P(X)$ unchanged while $P(Y\mid X)$ moves. Monitor residuals and prediction errors, not only input distributions.

**Delayed labels make monitoring hard.** Fraud is confirmed by chargebacks weeks later, so "current accuracy" is unmeasurable in real time. Use proxy metrics (prediction distribution, confidence) until labels arrive.

**Aggregate metrics hide segment failures.** A model can meet its overall target while failing badly for one region or demographic — an ethical and regulatory exposure, hence the case study's explicit bias checks.

**The system, not the model, is the deliverable.** The case study's core lesson: fraud detection is a *continuous system*, and monitoring plus retraining matter as much as the original model's accuracy.

> [!warning] Gaps in the source slides
> This deck is LaTeX Beamer and extracted almost completely. The figures are images, so the following slides have captions but no visual content:
> - **Slide 14** — "Training a model is only a small part of an ML system" (the Sculley et al. technical-debt diagram)
> - **Slide 15** — the MLOps growth chart
> - **Slide 20** — "Fun Example" (no text at all)
> - **Slide 29** — the ML lifecycle diagram
> - **Slide 38** — no extractable text; likely a drift illustration between the definition (37) and the quiz (39)
> - **Slide 42** — the "people in the ML lifecycle" diagram
> - **Slides 47–48 — "Typical MLOps Architecture" and "Popular MLOps Tools" are entirely images.** The tool landscape is therefore not captured beyond the Python library table on slide 52.
> - **Slide 54** — "Experiment Tracking Example" has a caption but no code
>
> **Slide 40's quiz answer field is blank in the source** — the answer given above is mine.
>
> **Further reading** (slide 61):
> - Treveil et al., *Introducing MLOps*, O'Reilly 2020
> - Gift & Deza, *Practical MLOps*, O'Reilly 2021
> - Google MLOps Whitepaper
> - **Sculley et al., *Hidden Technical Debt in ML Systems*** — the paper behind slide 14
> - MLflow Documentation · Kubeflow Pipelines
>
> **Assessment** (slide 7): Participation 10% · Individual Assignment (hands-on ML pipelines, Week 5) 20% · Project (MLOps pipeline, Week 14) 30% · Final Exam (Week 15) 40%.
> **Tracks** (slide 8): *Industry-Focused* (deployment, monitoring, scalability; Docker, MLflow, CI/CD) or *Research-Focused* (experimentation, reproducibility, failure modes).

---
**Next:** [[02 - Environment Setup]]
