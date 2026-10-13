---
subject: MLOps
chapter: 04
tags: [ds, mlops, baseline, metrics, mlflow, experiment-tracking, imbalanced-data]
source: "Model_Development_MLOPs.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Model Development

The third lifecycle stage, seen from the MLOps side: baselines, metric choice and experiment tracking rather than algorithms. "Model development dictates the constraints of subsequent usage, monitoring, and maintenance."

## 📘 Main Knowledge

### What ML is

Arthur Samuel: "the field of study that gives computers the ability to learn without being explicitly programmed." **Tom Mitchell**: a program learns from experience **E** with respect to task **T** and performance measure **P** if its performance on T, measured by P, improves with E. Face verification: T = same person or not, E = labeled image pairs, P = accuracy, FAR, FRR or AUC.

The three types (supervised, unsupervised, reinforcement) differ in the feedback available ([[Machine Learning/contents/00-Index|Machine Learning]]).

Components of supervised ML: training data (biased data such as **survivor bias** misleads), the performance metric (raw accuracy on imbalanced data causes harm), the algorithm (accuracy, interpretability, stability, cost), hyperparameters.

### Theory vs practice

Theory assumes clean, representative, i.i.d. data, a clear objective and unlimited compute. In practice ML is a system (data collection, features, training, deployment, monitoring, retraining) with noisy data, changing requirements and models that degrade. The model must also move business metrics, so a high-accuracy model can fail in production. "All models are wrong, but some are useful" (Box).

### Baselines

A **baseline** is a simple model that sets a reference level of performance without much time or expertise. It sets the minimum acceptable standard, is easy to deploy, and shows which parts of the data and task are easy or hard. It often takes 10% of the effort for 90% of the result.

Humans are good at unstructured tasks, so **human-level performance (HLP)** is a good baseline there; they are poor at structured tasks ([[03 - Data in MLOps]]).

Common baselines: linear regression (continuous targets), logistic regression (structured data, text), gradient boosted trees (tabular, time series), small CNNs or fine-tuned pretrained networks (VGG, U-Net) for images.

Four performance levels:
1. Trivially attainable (e.g. majority class).
2. Human-level performance.
3. Reasonable automated performance (simple models): is extra complexity justified?
4. Required deployment performance (truncated in source).

Sources: HLP, the literature, a quick implementation, older systems. If the baseline falls short, its failure modes show what to fix.

Cautionary tale: DeVries et al. (2018, *Nature*) forecast aftershock locations with a 13k-parameter deep network; Mignan and Broccardo (2019) showed a much simpler model matched it.

Rules: reasonable algorithms with good data beat great algorithms with poor data; consider deployment constraints only once a baseline exists; sanity-check code by overfitting a small training set first.

### Frameworks

| | scikit-learn | XGBoost |
|---|---|---|
| Focus | general ML | gradient boosting for tabular data |
| Ease | simple, consistent API | more configuration |
| Strength | small–medium data | large structured data |
| Scale | single machine | parallel, distributed |

| | TensorFlow | PyTorch |
|---|---|---|
| Origin | Google Brain | Facebook AI Research |
| Graph | static (with eager mode) | dynamic (define-by-run) |
| Research use | moderate | dominant |
| Production | TF Serving, TF Lite | TorchServe, ONNX |
| MLOps | TFX, Keras, MLflow | MLflow, Lightning |

**ONNX** moves models between frameworks.

### Imbalance and metrics

Fraud < 0.5% of transactions; > 99% of patients disease-free; ~99.6% of products defect-free. Predicting the majority class gives high accuracy, so accuracy alone is unreliable; use precision, recall, F1, ROC-AUC, PR-AUC. No single metric fits every case.

$$\text{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN},\quad \text{Precision}=\frac{TP}{TP+FP},\quad \text{Recall}=\frac{TP}{TP+FN},\quad F_1=\frac{2TP}{2TP+FP+FN}$$

$F_1$ is the harmonic mean of precision and recall: precision 1.0 with recall 0.01 gives 0.0198, not 0.5.

- **Precision** first when false alarms are costly (spam, security).
- **Recall** first when misses are dangerous (fraud, disease).
- **F1** when both matter, e.g. pedestrian detection: a miss can kill, false braking erodes trust.

### Improving the model

**Data augmentation** is an efficient way to get more data for unstructured problems. It can shift the training distribution away from dev/test, but Nakkiran et al. (2021): for unstructured data, with a large (low-bias) model and a clear mapping $X\to Y$ (a human can predict it), more data rarely hurts.

**Features** tell the model what it can't infer itself; for structured data, where new examples are hard to create, they are the main lever. Fraud case: the baseline (amount, time, merchant category, country) missed many frauds. Error analysis showed fraud often follows recent transactions and comes from unfamiliar devices or places. Added time since last transaction, transactions in a recent window, device fingerprint, distance from the previous location: recall improved with stable precision.

More features can improve accuracy and fairness, but they cost compute, add inputs to maintain, reduce stability and raise privacy concerns. In production every feature is a pipeline and a dependency ([[Data Preparation and Visualization/contents/08 - Feature Selection|Feature Selection]]).

### Experiment tracking

Track code version, dataset, hyperparameters and results, with enough information to replicate; ideally also summary metrics, resource use, visualizations and error analysis. Tools: text files, spreadsheets, W&B, Comet, MLflow, SageMaker Studio.

```python
import mlflow                          # pip install mlflow; mlflow ui → localhost:5000
mlflow.start_run()
mlflow.log_param("learning_rate", 0.01)
mlflow.log_param("model", "logistic regression")
mlflow.log_metric("accuracy", 0.92)
mlflow.sklearn.log_model(pipeline, artifact_path="model")
mlflow.end_run()

mlflow.autolog()                       # automatic logging

loaded = mlflow.pyfunc.load_model("runs:/<RUN_ID>/model")
predictions = loaded.predict(X_test)
```
The same model can be loaded locally, on a server or in the cloud.

## ✏️ Exercises

**1.** (Slides 32–39 quizzes) Which metric should each prioritise? (a) fraud detection; (b) spam filtering; (c) medical screening; (d) face-recognition access control.

> [!example]- Solution
> | Scenario | Metric | Cheap error |
> |---|---|---|
> | fraud | recall | a blocked legitimate payment is resolved by a call |
> | spam | precision | a missed spam is trivial; users rarely check the spam folder |
> | screening | recall | a false positive costs one follow-up test |
> | access control | precision | a rejected employee retries |
>
> Recall minimizes FN, precision minimizes FP. Tolerate the error with the cheap recovery. When neither is cheap (pedestrian detection), balance with F1 or a cost matrix and threshold.

**2.** (Slide 42 quiz) An X-ray diagnosis model has high average test accuracy. What can you conclude? (1) It does well on rare diseases. (2) It is equally accurate across genders and ethnicities. (3) It can be safely deployed. (4) None of the above.

> [!example]- Solution
> **(4).** The average is dominated by common cases, so rare diseases can fail completely (1). Subgroups are unevenly represented, so a minority group can do much worse unseen (2); evaluate per group. Deployment (3) also needs real-world validation, failure-mode analysis, regulatory approval, workflow integration and interpretability. One aggregate number never justifies deployment.

**3.** (Slide 23 quiz) True or false? (1) For unstructured problems, HLP estimates the Bayes error and what is reasonable to achieve. (2) HLP is a better baseline for unstructured than structured problems. (3) Avoid open-source baselines, since a good one may be too hard to beat.

> [!example]- Solution
> (1) True: HLP approximates the irreducible error, showing the headroom (humans 95%, model 93%: little left; humans 99%: real room).
> (2) True (slide 17).
> (3) False: slide 22 recommends open-source implementations. If you can't beat a strong baseline, deploy it and work on data. The aftershock story shows what happens without a proper baseline.

**4.** (Slide 46 quiz) Which are true? (1) GANs can be used for augmentation. (2) Augmentation should distort inputs until humans find them hard to classify. (3) Augment where you want improvement. (4) Augment where the model already does well.

> [!example]- Solution
> True: 1 and 3. False: 2 and 4.
> If a human can't classify the augmented example, the label may no longer apply: you have added noise and raised the Bayes error, which breaks Nakkiran's "clear mapping" condition. (Rotating an X-ray 15° is fine; 180° is not.) Augmentation should target failures found by error analysis; more of what already works adds cost and shifts the distribution.

**5.** (Advanced, slide 60) Extend the MLflow experiment: another model, log precision and recall, compare runs. Which model would you deploy?

> [!example]- Solution
> ```python
> import mlflow, mlflow.sklearn
> from sklearn.ensemble import RandomForestClassifier
> from sklearn.linear_model import LogisticRegression
> from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
> from sklearn.pipeline import Pipeline
> from sklearn.preprocessing import StandardScaler
>
> def run_experiment(name, model, params):
>     with mlflow.start_run(run_name=name):
>         pipe = Pipeline([("scaler", StandardScaler()), ("model", model)]).fit(X_train, y_train)
>         y_pred = pipe.predict(X_test)
>         mlflow.log_params(params)
>         mlflow.log_metrics({"accuracy": accuracy_score(y_test, y_pred),
>                             "precision": precision_score(y_test, y_pred),
>                             "recall": recall_score(y_test, y_pred),
>                             "f1": f1_score(y_test, y_pred)})
>         mlflow.sklearn.log_model(pipe, artifact_path="model")
>
> run_experiment("logreg", LogisticRegression(max_iter=1000), {"model": "LogisticRegression", "C": 1.0})
> run_experiment("rf", RandomForestClassifier(n_estimators=100, random_state=42),
>                {"model": "RandomForest", "n_estimators": 100})
> ```
> Suppose (illustrative numbers):
>
> | Model | Accuracy | Precision | Recall | F1 |
> |---|---|---|---|---|
> | logistic regression | 0.91 | 0.78 | 0.72 | 0.75 |
> | random forest | 0.94 | 0.85 | 0.71 | 0.77 |
>
> The forest wins on three metrics, but that doesn't settle it:
> 1. For fraud, recall matters most, and logistic regression is (slightly) ahead.
> 2. A gap on one split may be noise; cross-validate and report variance.
> 3. With a baseline in hand, deployment constraints now count: logistic regression is far faster, which matters under a 100 ms latency limit.
> 4. Its coefficients are explainable, which regulators may require.
> 5. A more complex model costs more to maintain and monitor.
>
> A defensible answer: deploy logistic regression, keep the forest in MLflow as a challenger, and revisit if error analysis finds the gap in an important segment. Tracking keeps the whole comparison so the decision can be revisited.

## 📝 Summary

- Mitchell: learning = performance on T, measured by P, improving with E.
- ML in practice is a system; a high-accuracy model can fail in production.
- Start with a baseline: ~10% of the effort, ~90% of the result.
- HLP is the baseline for unstructured data and estimates the Bayes error.
- Accuracy misleads on imbalanced data; choose precision, recall or F1 from the cost of each error.
- Aggregate metrics hide per-class and per-group failures.
- Augmentation should stay human-recognizable and target failures.
- Every feature adds compute, maintenance and privacy cost.
- Track code, data, hyperparameters and results (MLflow).

## ⚠️ Important Notes

1. Without a baseline you can't tell "bad model" from "hard task".
2. HLP shows the headroom on unstructured tasks.
3. At 99.6% non-defective, "never defective" scores 99.6%.
4. F1 is a harmonic mean.
5. The metric is a business decision made before modelling.
6. Disaggregate by class and group before deploying.
7. Unrecognizable augmentations are mislabeled data.
8. Augment where the model fails.
9. More data can hurt when it shifts the training distribution; Nakkiran's result has conditions.
10. Consider deployment constraints after the baseline exists.
11. If a model can't overfit 20 examples, there is a bug.
12. `mlflow.autolog()` misses data versions and business metrics; log them explicitly.

> [!warning] Gaps in the source slides
> - Slides 3, 14, 24, 28, 43, 52, 56 have no text; slide 4 is a photo; slides 8 and 12 have titles only.
> - Images: slide 6 (the three types of ML), 27 (ONNX), 30 (confusion matrix figure; definitions survive), 44–45 (augmentation figures), 55 (tracking-tool comparison).
> - Truncated: slide 7 (hyperparameters), 15, 19 (fourth performance level), 21 (Mignan & Broccardo result), 23 (quiz option 3), 25.
> - Slides 32–39 are question/answer overlay pairs.
> - The numbers in Exercise 5 are illustrative, not from the slides.
> - References: Treveil et al.; Gift & Deza; Nakkiran et al. (2021), *Deep double descent*; DeVries et al. (2018), *Nature* 560; Mignan & Broccardo (2019) (citation truncated).

**Previous:** [[03 - Data in MLOps]] · **Next:** [[05 - Packaging Models with FastAPI and Docker]]
