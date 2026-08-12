---
subject: MLOps
chapter: 04
tags: [ds, mlops, baseline, metrics, mlflow, experiment-tracking, imbalanced-data]
source: "Model_Development_MLOPs.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Model Development

> [!note] Where this sits in the course
> The **third stage** of the ML lifecycle. [[03 - Data in MLOps]] prepared the data; this chapter builds models on it — but from an **MLOps** angle, so the emphasis falls on baselines, metric choice, and experiment tracking rather than algorithms.
>
> > Model development **dictates the constraints of subsequent usage, monitoring, and maintenance**.

## 📘 Main Knowledge

### What machine learning is

> *"Machine learning is the field of study that gives computers the ability to learn without being explicitly programmed."* — **Arthur Samuel**

**Tom Mitchell's formal definition:**

> A computer program is said to learn from experience **E** with respect to some task **T** and some performance measure **P**, if its performance on **T**, as measured by **P**, improves with experience **E**.

*Example — face verification:* **T** = verify whether two face images belong to the same person · **E** = labeled face image pairs collected over time · **P** = verification accuracy, FAR, FRR, or AUC.

**Three types of ML**, distinguished by **the type of feedback available during learning** — supervised (labeled targets), unsupervised (no feedback), reinforcement (reward signal). See [[Machine Learning/contents/00-Index|Machine Learning]].

### Components of supervised ML

- **Training Data** — labeled examples. Quality is critical; biased or incomplete data (e.g. **survivor bias**) produces misleading models.
- **Performance Metric** — defines what the model optimises. Poor choices (raw accuracy on imbalanced data) produce **unintended and harmful outcomes**.
- **ML Algorithm** — the mathematical model. Choice depends on accuracy, **interpretability, stability, and computational cost**.
- **Hyperparameters** *(truncated in source)*.

### Theory vs practice

**Theoretical ML assumes:** clean, labeled, representative data · a fixed distribution (**i.i.d.**) · a clear objective and metric · implicitly unlimited compute and storage. Its focus is algorithm design, convergence, generalization, and loss minimisation.

**In practice, ML is a system — not just a model:** data collection and cleaning · feature engineering · training and evaluation · deployment and monitoring · retraining and maintenance.

**Reality:** data is noisy, incomplete, and biased · requirements evolve · **models degrade after deployment**.

**Key challenges:** data issues (missing values, label noise, skew) · reproducibility · scalability · monitoring (data and concept drift) · collaboration across roles · and the **business goal** — the model must work not only on train/dev/test but on **business metrics**.

> **Result: a high-accuracy model may fail in production.**

> *"All models are wrong, but some are useful."* — **George E. P. Box**

---

### Establishing a baseline

> *"Everything should be made as simple as possible, but not simpler."* — **Albert Einstein**

> A **baseline** is a simple model that provides a reference level of performance and does not require much expertise or time to build.

**What a baseline does:**
- Serves as a **minimum acceptable standard**.
- **Easy to deploy** — faster to train, better studied, quicker inference.
- **Helps understand the data** — which classes are hard to separate, what signal the model picks up, and what signal it misses.
- **Helps understand the task** — which parts of inference are easy and which are hard.

> A baseline often requires only **10% of the development effort, yet gets 90% of the way** to reasonably good results.

**Humans as baseline.** Humans are **very good at unstructured data tasks**, so **human-level performance (HLP)** is a good baseline there. Humans are **not good at structured data tasks** — echoing the feasibility table in [[03 - Data in MLOps]].

**Common baseline models:**
- **Linear Regression** — continuous values (prices, age, demand)
- **Logistic Regression** — fast, reliable classification on structured data or text
- **Gradient Boosted Trees** — structured and time-series data; strong with limited tuning
- **Simple Convolutional Models** — fine-tuning pretrained architectures (VGG, U-Net variants) for image tasks

**Four performance levels** guiding baseline selection:

1. **Trivially Attainable** — any model should exceed it (e.g. predicting the majority class).
2. **Human-Level Performance** — human accuracy on the task; suits automation, and is a *lower* bound where machines should beat humans.
3. **Reasonable Automated Performance** — achievable with simple models; useful for judging whether added complexity is justified.
4. **Required Deployment Performance** *(truncated in source)* — the level the business actually needs.

**Where to get a baseline:** human-level performance · literature search for state of the art · quick-and-dirty implementation · performance of older systems.

> When baseline performance is insufficient, **analyzing its failure modes** provides insight into data limitations and informs the choice of more advanced models.

**The cautionary tale (slide 21):** DeVries et al. (2018) proposed a 13k-parameter deep neural network to forecast aftershock locations after large earthquakes — published in *Nature*. **Mignan and Broccardo (2019) showed a much simpler model matched it.** The lesson: without a proper baseline, you cannot know whether complexity bought anything.

**Getting started:** literature search (blogs, open-source projects, courses) · open-source implementations.

> **Reasonable algorithms with good data often outperform great ones with no good data.**

- **Deployment constraints should be taken into account only if a baseline already exists.**
- **Sanity-check** code and algorithm by **overfitting a small training set** before training on a large one.

---

### Frameworks

**Classical ML:**

| Aspect | Scikit-Learn | XGBoost |
|---|---|---|
| Primary focus | General-purpose ML | High-performance gradient boosting for **tabular** data |
| Ease of use | Simple, consistent API; beginner-friendly | More complex configuration; steeper curve |
| Performance | Strong baseline on small–medium data | Often superior on **large structured** datasets |
| Scalability | Mostly single-machine | Parallel, distributed, large-scale |

**Deep learning:**

| Aspect | TensorFlow | PyTorch |
|---|---|---|
| Origin | Google Brain | Facebook AI Research |
| Computation graph | **Static** (with eager mode) | **Dynamic** (define-by-run) |
| Ease of use | More structured, steeper curve | Pythonic, intuitive, easy debugging |
| Research usage | Moderate | **Dominant** |
| Production | Very strong (TF Serving, TF Lite) | Growing (TorchServe, ONNX) |
| MLOps support | TFX, Keras, MLflow | MLflow, PyTorch Lightning |
| Best for | Large-scale production systems | Research, rapid prototyping |

**Interoperability:** the **ONNX** (Open Neural Network Exchange) format enables model portability across frameworks — train in PyTorch, serve with a TensorFlow-based runtime.

---

### Class imbalance and evaluation metrics

Many real problems are **highly imbalanced**:
- **FinTech** — fewer than **0.5%** of transactions are fraudulent
- **Medical diagnosis** — over **99%** of patients do not have the disease
- **Manufacturing QC** — approximately **99.6%** of products have no defects

> A model predicting only the majority class achieves very high accuracy. **Accuracy alone is not a reliable metric for skewed datasets.** Precision, Recall, F1, ROC-AUC, and PR-AUC are more informative — and **there is no one-size-fits-all metric.**

**Confusion matrix:** **TP** (correctly predicted positive) · **TN** (correctly predicted negative) · **FP** (incorrectly predicted positive) · **FN** (incorrectly predicted negative).

$$\text{Accuracy} = \frac{TP+TN}{TP+TN+FP+FN} \qquad \text{Precision} = \frac{TP}{TP+FP}$$

$$\text{Recall} = \text{Sensitivity} = \frac{TP}{TP+FN} \qquad F_1 = \frac{2TP}{2TP+FP+FN}$$

$F_1$ is the **harmonic mean** of precision and recall — it punishes imbalance between them, so a model with precision 1.0 and recall 0.01 scores ≈ 0.02, not 0.5.

> **Prioritise Precision** when false alarms are costly (spam, security) — FP must be low.
> **Prioritise Recall** when missing positives is dangerous (fraud, disease) — FN must be low.
> **Use F1** when both matter.

**Where both are critical — pedestrian detection for autonomous vehicles:** missing a pedestrian (FN) can cause fatalities, but false alarms (FP) cause unnecessary braking or swerving, reducing passenger comfort and trust. **Both errors are costly, so the system must balance them.**

---

### Improving the model

**Data augmentation** — a very efficient way to get more data, especially for **unstructured** problems (images, audio, text).

**Can adding more data hurt?** Data augmentation adds to *specific parts* of the training set, which may then come from a different distribution than dev and test.

> **Answer (Nakkiran et al., 2021):** for **unstructured data**, if the model is **large (low bias)** and the mapping $f: X \to Y$ is **clear** (a human can predict accurately), then adding more data **rarely hurts** accuracy.

**Adding features** — *features are how data is presented to a model, informing it of things it cannot infer by itself.* For many **structured** problems, creating brand new training examples is difficult, so feature engineering is the lever instead.

**Worked case — credit card fraud detection:**

*Baseline* uses transaction amount, time, merchant category, country. **Observed issue:** many fraud cases missed (high FN).
*Error analysis:* fraud often occurs shortly after previous transactions; suspicious transactions originate from unfamiliar devices or locations.
*Feature engineering:* **behavioral** — time since last transaction, number of transactions in a recent window; **device & location** — device fingerprint, distance from previous transaction location.
*Outcome:* **improved recall with stable precision.**

> Even with modern deep learning, if the dataset is not massive, **feature design driven by error analysis** remains useful.

**How feature selection impacts MLOps strategy.** More features may improve accuracy, improve fairness (finer group splits), or compensate for missing information — **however:**

- The model becomes **increasingly expensive to compute**.
- More features require **more inputs and more maintenance** downstream.
- More features mean **a loss of some stability**.
- The sheer number of features can raise **privacy concerns**.

This is the production counterweight to [[Data Preparation and Visualization/contents/08 - Feature Selection|Feature Selection]]: in a notebook a feature costs nothing; in production every feature is a pipeline to maintain, a dependency that can break, and a privacy exposure.

---

### Experiment tracking

> Experiment tracking is part of MLOps, focusing on supporting **iterative model development**.

**What to track:** algorithm/code versioning · dataset used · hyperparameters · results.

**Tools:** text files · spreadsheets · dedicated systems — **Weights & Biases, Comet, MLflow, SageMaker Studio**.

**Desirable features:** information needed to **replicate** the result · experiment results, ideally with summary metrics and analysis · resource monitoring, visualisation, model error analysis.

**MLflow setup:**
```bash
pip install mlflow
mlflow ui                     # open http://localhost:5000
```

**Logging an experiment:**
```python
import mlflow

mlflow.start_run()
mlflow.log_param("learning_rate", 0.01)
mlflow.log_param("model", "logistic regression")
mlflow.log_metric("accuracy", 0.92)
```
This tracks **parameters** (learning rate, model type), **metrics** (accuracy), and **metadata** (timestamp, run ID).

**Auto-logging** — an ultra-quick setup:
```python
import mlflow
mlflow.autolog()
```

**Logging and loading a model:**
```python
mlflow.sklearn.log_model(pipeline, artifact_path="model")
mlflow.end_run()
```
```python
import mlflow.pyfunc

model_uri = "runs:/<RUN_ID>/model"
loaded_model = mlflow.pyfunc.load_model(model_uri)
predictions = loaded_model.predict(X_test)
```

> **Key idea: the same model can be loaded anywhere — locally, on a server, or in the cloud.**

## ✏️ Exercises

**1.** *(Slides 32–39 quizzes)* For each scenario, choose the metric to prioritise and justify it: (a) fraud detection; (b) spam filtering; (c) medical screening; (d) face recognition access control.

> [!example]- Solution
> | Scenario | Metric | Why |
> |---|---|---|
> | **(a) Fraud detection** | **Recall** | Missing fraud (FN) is very costly; false alarms are acceptable |
> | **(b) Spam filtering** | **Precision** | An important email in the spam folder (FP) is costly |
> | **(c) Medical screening** | **Recall** | False negatives must be minimised |
> | **(d) Access control** | **Precision** | False positives — letting intruders in — must be minimised |
>
> **The unifying principle: identify which error type the *business* cannot tolerate.**
>
> - **Recall** minimises **FN** — "don't miss any positives."
> - **Precision** minimises **FP** — "don't raise false alarms."
>
> Each scenario embeds a **recovery mechanism** that reveals which error is cheaper. In (a), a blocked legitimate transaction merely annoys — the customer calls and it is resolved. In (b), *"users check spam folders occasionally"* — so a missed spam (FN) is trivial, while a lost job offer (FP) is not. In (c), *"follow-up tests are available"* — so a false positive costs one extra test, while a false negative may cost a life. In (d), *"authorized users can retry"* — a rejected employee retries in seconds, but an admitted intruder is a breach.
>
> **Read the recovery path and the answer follows.** The error with the cheap recovery is the one you tolerate.
>
> Note (a) and (c) both prioritise recall while (b) and (d) both prioritise precision — the domains differ but the error structure is identical.
>
> **The genuinely hard case is pedestrian detection** (slide 41), where *both* errors are severe: a missed pedestrian kills, and constant false braking makes the vehicle unusable and erodes trust. There is no cheap recovery path on either side, so the system must balance — F1, or better, an explicit cost matrix and threshold tuning as in [[01 - Introduction to MLOps]]'s fraud case study.

**2.** *(Slide 42 quiz)* An algorithm diagnosing illnesses from X-rays achieves high average accuracy on the test set. What can you conclude with high confidence?
> (1) It does well even on rare diseases. (2) It is roughly equally accurate across genders and ethnicities, so unbiased. (3) It can be safely deployed in healthcare. (4) None of the above.

> [!example]- Solution
> **Answer: 4 — None of the above.**
>
> **Why (1) is wrong.** High *average* accuracy is dominated by common cases. If 95% of X-rays are normal or show common conditions, a model can score 95% while failing completely on every rare disease — and rare diseases are frequently the ones where diagnostic support matters most. Average metrics **hide per-class performance**; you need a per-class breakdown or a confusion matrix.
>
> **Why (2) is wrong.** Aggregate accuracy says nothing about subgroup performance, and demographic groups are usually **unequally represented** in medical datasets. A model can be 95% accurate overall and 99% on the majority group while being 70% on an underrepresented one — the majority's volume masks it. Detecting this requires **disaggregated evaluation**, which is why [[01 - Introduction to MLOps]]'s fraud case study lists *"bias checks across regions and demographics"* as an explicit step.
>
> **Why (3) is wrong**, for reasons beyond the metric entirely: test-set accuracy does not establish real-world performance (the deployment distribution differs from the curated test set); it says nothing about **failure modes** — *how* it fails matters more than how often in medicine; it ignores regulatory approval, clinical validation, and integration into clinical workflow; and it ignores **interpretability**, which clinicians need in order to act on a prediction.
>
> **The general lesson**, and the reason this quiz sits in an MLOps course rather than an ML one: **a single aggregate number is never sufficient evidence for a deployment decision.** [[01 - Introduction to MLOps]] made the same point — the model is not the deliverable, the *system* is, and the system includes monitoring, fairness auditing, and human oversight.

**3.** *(Slide 23 quiz)* Which statements about baselines are accurate?
> (1) For unstructured problems, human-level performance as baseline estimates the irreducible/Bayes error and what is reasonable to achieve. (2) HLP is more effective for baselines on unstructured problems than structured ones. (3) Open-source software should not be used for a baseline, since a good implementation might be too good and too hard to beat.

> [!example]- Solution
> **(1) TRUE.** Humans are near-optimal on perception tasks, so HLP approximates the **Bayes error** — the irreducible error arising from genuine ambiguity in the data itself. That matters because it tells you *where the ceiling is*. If humans achieve 95% and your model achieves 93%, only 2% of headroom exists and further effort has poor returns. If humans achieve 99% and your model 93%, there is real room. **Without a Bayes error estimate you cannot tell "the model is bad" from "the task is hard."**
>
> **(2) TRUE.** Explicitly stated on slide 17: *"Humans are so good at unstructured data tasks... Humans are not good at structured data tasks."* A radiologist reads an X-ray expertly; no human can eyeball 200 columns of transaction data and predict default better than gradient boosting. This is the same split as the feasibility table in [[03 - Data in MLOps]] — HLP for unstructured, availability of predictive features for structured.
>
> **(3) FALSE**, and backwards. Slide 22 explicitly recommends *"literature search... open-source implementations."* A strong open-source baseline is **valuable, not threatening**: it tells you what is achievable before you invest, and if you cannot beat it, that is the answer — deploy it and spend your effort on data instead. Avoiding a strong baseline to make your own model look better is a way of deceiving yourself.
>
> The DeVries/Mignan aftershock story on slide 21 is exactly this failure: a 13k-parameter neural network published in *Nature*, later shown to be matched by a far simpler model. **Without a rigorous baseline, you cannot know whether complexity bought anything** — you can only know that your complex model works.

**4.** *(Slide 46 quiz)* Which statements about data augmentation are true?
> (1) GANs can be used for data augmentation. (2) Augmentation should distort input enough that humans find it difficult to classify. (3) Augmentation should generate more examples where you want improvement. (4) Augmentation should generate more examples where the algorithm already does well.

> [!example]- Solution
> **TRUE: 1 and 3. FALSE: 2 and 4.**
>
> **(1) TRUE.** GANs generate realistic synthetic examples — one form of the synthetic data generation described in [[03 - Data in MLOps]]. Useful where real data is scarce, expensive, or privacy-constrained (medical imaging, rare defects).
>
> **(2) FALSE — and this is the key insight.** Augmented data should remain **recognisable to a human**. The reason connects directly to (1) in Exercise 3: if a human cannot classify the augmented image, then $f: X \to Y$ has become ambiguous and the **Bayes error has risen**. You have not created a hard training example; you have created a **mislabeled** one, because the original label may no longer apply. Training on it teaches the model to fit noise.
>
> The right test for an augmentation: *would a human still label this correctly?* Rotating an X-ray 15° — yes. Rotating it 180° — probably not, since anatomical orientation carries meaning. Adding mild noise — yes. Adding noise until the image is grey — no.
>
> This also explains Nakkiran's condition on slide 47 — more data rarely hurts *provided* "the mapping $f: X \to Y$ is clear (human can make accurate predictions)". Augmentation that destroys human recognisability violates the precondition and can genuinely hurt.
>
> **(3) TRUE and (4) FALSE** — a matched pair. Augmentation should be **directed by error analysis**, at the regions of input space where the model fails. If it misclassifies dark images, generate more dark images. Generating more of what already works adds compute cost and zero information, and can *worsen* things by shifting the training distribution further from dev/test — the concern slide 47 raises.
>
> **The unifying principle: augmentation is targeted, not indiscriminate.** Analyse failures first, then augment at the failure. Precisely the loop used in the fraud feature-engineering case: error analysis revealed missed fraud after recent transactions, so *behavioral* features were added — targeted at the observed weakness.

**5.** (Advanced) *(Slide 60)* Extend the MLflow experiment: change the model, log precision and recall, compare runs. **Which model would you deploy and why?**

> [!example]- Solution
> ```python
> import mlflow, mlflow.sklearn
> from sklearn.ensemble import RandomForestClassifier
> from sklearn.linear_model import LogisticRegression
> from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
> from sklearn.pipeline import Pipeline
> from sklearn.preprocessing import StandardScaler
>
> def run_experiment(name, model, params):
>     with mlflow.start_run(run_name=name):
>         pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
>         pipe.fit(X_train, y_train)
>         y_pred = pipe.predict(X_test)
>
>         mlflow.log_params(params)
>         mlflow.log_metrics({
>             "accuracy":  accuracy_score(y_test, y_pred),
>             "precision": precision_score(y_test, y_pred),
>             "recall":    recall_score(y_test, y_pred),
>             "f1":        f1_score(y_test, y_pred),
>         })
>         mlflow.sklearn.log_model(pipe, artifact_path="model")
>
> run_experiment("logreg", LogisticRegression(max_iter=1000, random_state=42),
>                {"model": "LogisticRegression", "C": 1.0})
> run_experiment("rf", RandomForestClassifier(n_estimators=100, random_state=42),
>                {"model": "RandomForest", "n_estimators": 100, "max_depth": None})
> ```
>
> **"Which model would you deploy?" is a trick question — the metrics alone cannot answer it.** Suppose:
>
> | Model | Accuracy | Precision | Recall | F1 |
> |---|---|---|---|---|
> | Logistic Regression | 0.91 | 0.78 | 0.72 | 0.75 |
> | Random Forest | 0.94 | 0.85 | 0.71 | 0.77 |
>
> Random Forest wins on three of four. **That does not settle it**, for five reasons this chapter has established:
>
> **1. Which error matters?** If this is fraud detection, **recall** is the priority — and logistic regression's 0.72 beats Random Forest's 0.71. The "better" model is worse on the metric that matters. Choose the metric from the business problem *first*, per Exercise 1.
>
> **2. Is the difference real?** A 3-point accuracy gap on one test split may be noise. Use cross-validation and report variance, not a single number — [[Data Preparation and Visualization/contents/09 - Building Pipelines|Building Pipelines]].
>
> **3. Deployment constraints.** Slide 22: *"deployment constraints should be taken into account only if a baseline already exists"* — and now one does, so they apply. Logistic regression has ~10 coefficients and sub-millisecond inference; a 100-tree forest is orders of magnitude larger and slower. Under the fraud case study's **sub-100 ms latency** requirement, that can decide it outright.
>
> **4. Interpretability.** Logistic regression coefficients are directly explainable — necessary for credit decisions under regulation, and for the *"interpretability is critical for trust and regulation"* conclusion of [[01 - Introduction to MLOps]].
>
> **5. Maintenance cost.** Slide 51's warning: more complexity means more compute, more maintenance, less stability. A 3-point gain may not be worth a model that is harder to debug, retrain, and monitor.
>
> **The defensible answer:** *"Deploy logistic regression as the baseline, since it meets the latency and interpretability constraints with comparable recall. Keep Random Forest tracked in MLflow as the challenger, and revisit if error analysis shows the gap concentrated in a segment that matters."*
>
> This is why **experiment tracking exists** — not to crown a winner but to preserve the full comparison, with parameters, metrics, and artifacts, so the decision can be revisited and justified later.

## 📝 Summary

- **Mitchell's definition:** a program learns from experience **E** on task **T** measured by **P**, if performance improves with experience.
- **In practice ML is a system, not a model** — theory assumes clean i.i.d. data and unlimited compute; reality has noise, drift, and business metrics. **A high-accuracy model may fail in production.**
- **Establish a baseline first** — ~10% of the effort for ~90% of the result, and it reveals what the data and task actually permit.
- **HLP is the right baseline for unstructured data** (it estimates the Bayes error); structured data has no human baseline.
- **Without a baseline you cannot tell whether complexity bought anything** — the aftershock-DNN cautionary tale.
- **Accuracy is unreliable on imbalanced data.** Use Precision (minimise FP), Recall (minimise FN), F1 (both), PR-AUC.
- **Choose the metric from the business cost of each error type** — read the recovery path.
- **Aggregate metrics hide per-class and per-subgroup failure.** Never deploy on an average.
- **Augmentation must stay human-recognisable** and should target regions where the model fails, not where it succeeds.
- **Feature engineering driven by error analysis** still works, but every feature adds compute, maintenance, instability, and privacy exposure.
- **Track experiments** — code version, dataset, hyperparameters, results — with MLflow or equivalent, so runs are comparable and reproducible.

## ⚠️ Important Notes

**Skipping the baseline is the most common modelling error.** Without it you cannot tell "the model is bad" from "the task is hard", and you cannot know whether a complex model earned its complexity.

**Human-level performance approximates the Bayes error on unstructured tasks** — it tells you how much headroom exists, which determines whether further effort is worthwhile.

**High accuracy on imbalanced data is meaningless.** At 99.6% non-defective, predicting "no defect" always scores 99.6%.

**F1 is the harmonic mean, not the arithmetic mean.** Precision 1.0 with recall 0.01 gives F1 ≈ 0.02, not 0.5 — it refuses to reward one-sided models.

**Metric choice is a business decision made before modelling**, derived from which error is cheap to recover from.

**Average metrics conceal subgroup failure.** Disaggregate by class and by demographic group; an aggregate number is never sufficient evidence to deploy.

**Augmentation that defeats human recognition creates mislabeled data**, raising the Bayes error rather than adding difficulty.

**Augment where the model fails, not where it succeeds.** Untargeted augmentation costs compute and can pull the training distribution away from dev/test.

**More data can hurt** when augmentation shifts the training distribution away from dev/test. Nakkiran's result — that it rarely hurts — holds only for **unstructured data with a large model and a clear $X \to Y$ mapping**.

**Every feature is a production liability**, not just a modelling gain: more compute, more upstream dependencies, less stability, more privacy exposure.

**Deployment constraints come *after* a baseline exists.** Optimising for latency before knowing what accuracy is achievable optimises the wrong thing.

**Overfit a tiny training set as a sanity check.** If a model cannot memorise 20 examples, there is a bug — this catches errors that a full training run hides.

**Auto-logging is convenient but incomplete.** `mlflow.autolog()` captures framework parameters and metrics, but not your data version or custom business metrics. Log those explicitly.

> [!warning] Gaps in the source slides
> LaTeX Beamer; extraction was good. Missing:
> - **Slides 3, 14, 24, 28, 43, 52, 56** produced no text — section dividers.
> - **Slide 4** — the Arthur Samuel photograph.
> - **Slide 6 — "Three Types of Machine Learning"** is a figure; only the key idea (*"the difference lies in the type of feedback"*) survived. **The supervised/unsupervised/reinforcement breakdown itself is an image.**
> - **Slides 8, 12** — "Model Training" and "Model development" have titles only.
> - **Slides 27, 44–45** — the ONNX interoperability diagram and both data augmentation figures (including text augmentation) are images.
> - **Slide 30** — the confusion matrix figure; the definitions survived as text.
> - **Slide 55 — "Experiment tracking systems"** is entirely an image, so the tool comparison is not captured beyond the names on slide 54.
> - **Several lists truncate mid-item:** slide 7 (the **Hyperparameters** component, cut at "Hyp"), slide 15 (baseline benefits, cut at "in which directi"), slide 19 (**the fourth performance level, "Required Deployment Performance"**, cut at "Re"), slide 21 (the Mignan/Broccardo result, cut at "showed that"), slide 23 (quiz option 3, cut at "hard to bea"), slide 25 (Regularization row).
> - **Slides 32/33, 34/35, 36/37, 38/39 are duplicate pairs** — the Beamer overlay mechanism rendering question then answer; content is identical.
>
> **References:** Treveil et al., *Introducing MLOps* · Gift & Deza, *Practical MLOps* · **Nakkiran et al. (2021), *Deep double descent: Where bigger models and more data hurt*, J. Stat. Mech.** · DeVries et al. (2018), *Deep learning of aftershock patterns following large earthquakes*, Nature 560 · Mignan & Broccardo (2019) — the rebuttal *(citation truncated in source)*.

---
**Previous:** [[03 - Data in MLOps]] · **Next:** [[05 - Packaging Models with FastAPI and Docker]]
