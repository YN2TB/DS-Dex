---
subject: MLOps
chapter: 10
tags: [ds, mlops, drift-detection, monitoring, retraining, shap, ensemble]
source: "MLOPs_Monitoring.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Monitoring ML Systems

The conceptual side of [[08 - Monitoring with Prometheus and Grafana]]: what to detect, how to detect it statistically, and what to do, through retraining and decommissioning.

## 📘 Main Knowledge

### ML fails silently

Traditional software fails loudly with errors and stack traces; ML systems fail silently. Lower layers fail too: hardware faults in a DNN pipeline, software faults such as unreleased GPU memory causing OOM errors. MLOps makes these failures visible and manageable as the world changes.

### Four production issues

1. **Training–serving skew**: training data doesn't match production input, often because training used constructed or cleaned data. Shows up immediately after deployment. Example: trained on printed characters, used on handwriting.
2. **Excessive latency**: depends on data volume, pipeline and model; critical for online and edge models. In self-driving cars, more compute cuts delay but costs energy and money, while delay lengthens reaction time and braking distance.
3. **Data drift**: input statistics change after training, quickly or slowly (online shopping demand).
4. **Concept drift**: the input–output relationship changes while inputs may look the same (house prices after a monetary policy change).

Skew is visible from day one; drift usually develops gradually. That timing is the main diagnostic.

### What to monitor

Two levels: **infrastructure** (CPU/GPU, memory, disk, network, availability) and **model performance** (accuracy, precision, recall, confusion matrix over time).

- **Inputs**: schema, encoding, volume, missing data; input distributions (drift); feature–target correlations (concept drift); periodic manual audits.
- **Pipeline**: training is processed in batches, production often as streams, which is where skew arises. Compare distributions before and after processing; check that continuous features stay in range and that no unseen categories appear.
- **Outputs**: metrics over time; thresholds that trigger retraining; distance between predicted and observed label distributions.
- **Audits**: performance across demographic groups; feature impact with **LIME** (a local interpretable surrogate) or **SHAP** (each feature's contribution relative to an expected value).

### Drift detection

| Data drift approach | Methods |
|---|---|
| statistical tests | Kolmogorov–Smirnov, Anderson–Darling, t-test, PSI |
| distances | KL divergence, Jensen–Shannon divergence, Wasserstein |
| model-based | train a classifier to tell old from new data; falling confidence |
| feature monitoring | mean, variance, correlations; embedding drift |
| sequential | CUSUM, Page–Hinkley |

If a classifier can tell training data from production data, the distributions differ, and its accuracy measures by how much.

| Concept drift approach | Methods |
|---|---|
| performance-based | error rate, loss, accuracy |
| change detection | DDM, EDDM, ADWIN, Page–Hinkley |
| distribution | feature–label relationships, conditional tests |
| model-based | detectors inside learners, ensembles |

Concept drift detection generally needs labels: you can't see $P(Y\mid X)$ change without $Y$.

### Tests and distances

- **Kolmogorov–Smirnov**: non-parametric; one sample against a distribution, or two samples against each other. Statistic = maximum vertical distance between the CDFs. The default for continuous features.
- **Anderson–Darling**: more sensitive, especially in the tails, but needs critical values for each distribution.
- **t-test**: compares means and assumes normality ([[Mathematical Statistics/contents/08 - Inferences on Two Samples|Inferences on Two Samples]]). A doubled variance with the same mean passes it.

$$KL(P\|Q)=\sum_x P(x)\log\frac{P(x)}{Q(x)}$$
Asymmetric, ≥ 0, zero iff $P=Q$, infinite when $Q(x)=0<P(x)$.

$$JSD(P\|Q)=\tfrac12KL(P\|M)+\tfrac12KL(Q\|M),\qquad M=\tfrac12(P+Q)$$
Symmetric, $0\le JSD\le\log 2$, always finite.

Example: $P=(0.5,0.5)$, $Q=(0.9,0.1)$: $KL(P\|Q)=0.511$, $KL(Q\|P)=0.368$, $JSD=0.102$ (bound 0.693). PSI $=\sum(q-p)\ln(q/p)=KL(P\|Q)+KL(Q\|P)=0.879$.

### Mitigation

- **Transfer learning**: fine-tune a pretrained model on a little labeled target data; good when domains share features and target labels are scarce.
- **Continual learning**: learn from new distributions while keeping old knowledge; EWC and GEM balance plasticity and stability.

| | Continual learning | Online learning |
|---|---|---|
| Goal | a sequence of tasks, keeping past knowledge | update continuously with streaming data |
| Data | task-based, may be stored | one sample or mini-batch, not stored |
| Main problem | catastrophic forgetting | concept drift, real-time adaptation |

- **Data augmentation** for robustness and invariant features. Images: flips, rotations, scaling, crops, shear; brightness, contrast, hue; blur, sharpening; random erasing; Mixup, CutMix; GANs. Text: synonyms, back translation, random insertion/deletion/swap.
- **Ensembles** ([[Machine Learning/contents/00-Index|Machine Learning]]): **bagging** (homogeneous, parallel, bootstrap replicates; random forest), **stacking** (heterogeneous, parallel, a meta-learner on base outputs), **boosting** (sequential, focusing on previous errors).

### Maintenance

Models are not "set and forget". Retrain to use more data, follow a changing environment, counter adversaries, and because recent data may matter more.

- **Scheduled retraining**: fixed interval; requires knowing the decay rate; common when steps such as data collection are manual.
- **Triggered retraining**: when performance crosses a threshold; requires fully automated pipelines.

These match the `schedule:` and `workflow_dispatch` triggers in [[09 - CI-CD with GitHub Actions]].

### Decommissioning

The formal retirement of a model, for business changes (e.g. new local suppliers make a recipe model obsolete), performance decay, obsolescence, or compliance and risk. Notify stakeholders, keep the model and documentation for a period as benchmark or fallback, decide what to do with third-party models, and monitor downstream effects. Example: an airline retiring a chatbot archives interaction logs securely for compliance.

## ✏️ Exercises

**1.** (Slide 15 quiz) A bird-identification app trained on high-resolution, close-up, frontal images does well on its test set, but early users report many errors on photos of birds in the wild. Most likely issue? (1) latency; (2) training–serving skew; (3) data drift; (4) concept drift.

> [!example]- Solution
> **(2).** It appears right after release, and the training set was curated, unlike distant, occluded, blurred phone photos (like the printed vs handwritten example). Latency would make answers slow, not wrong; drift needs time; birds haven't changed. The test set shared the training set's bias, so it validated nothing about deployment. Fix: collect real user photos and augment with crops, rotations, blur and brightness changes.

**2.** How do training–serving skew and data drift differ, and why do they need different responses?

> [!example]- Solution
> | | Skew | Data drift |
> |---|---|---|
> | Cause | training data never matched reality | reality changed later |
> | Timing | immediate (a step) | gradual (a slope) |
> | Root | data or pipeline defect | environment |
> | Fix | fix the data or pipeline | retrain on recent data |
> | Recurs | no, once fixed | yes |
>
> Retraining doesn't fix a pipeline mismatch; the new model inherits it. Use parity checks or a feature store. Repairing the pipeline doesn't fix drift. Plot performance against time since deployment, and use week-one production as the baseline rather than the test set.

**3.** Compare KL and Jensen–Shannon divergence. Why is JSD preferred for monitoring?

> [!example]- Solution
> KL is asymmetric: in the example above "the drift" is 0.511 or 0.368 depending on argument order. It is infinite whenever production contains a value the reference never saw (a new category or an out-of-range value), exactly when you want a usable number; smoothing with ε makes the result depend on ε.
> JSD compares both distributions with their mixture $M$, which is zero only where both are, so it is finite and symmetric. Its bound ($\log 2$, or 1 in base 2) puts all features on one scale, so one threshold works for all. $\sqrt{JSD}$ is a true metric. PSI, standard in credit risk, is the symmetric sum of the two KLs, but it is also infinite on empty bins.

**4.** Why is concept drift harder to detect than data drift? What can you do when labels are delayed?

> [!example]- Solution
> Data drift is visible in inputs alone (KS, JSD), immediately and cheaply. Concept drift is a change in $P(Y\mid X)$, which can happen with stable inputs, so detection needs labels (DDM, ADWIN, error rates).
> With delayed labels: watch the prediction distribution (approval rate 72% → 61% with stable inputs); watch confidence (predictions moving towards 0.5); use fast proxies (30-day delinquency); label a small random sample each week; use the drift classifier as an early warning. The sample must be random: a fraud model never learns outcomes for transactions it blocked, so keep a holdout that bypasses it.

**5.** (Slide 49 quiz) A real-time fraud model faces frequently changing patterns from user behaviour and adversaries. Which retraining strategy? (1) scheduled; (2) triggered; (3) continuous learning; (4) none.

> [!example]- Solution
> **(2) triggered**, with a scheduled floor. Adversaries make drift abrupt and unpredictable, so there is no stable decay rate for a schedule, and a real-time system already has automated pipelines. Because labels are delayed, the trigger lags; a monthly retrain catches slow drift.
> Continuous learning has no quality gate, needs immediate labels, and gives attackers a way to poison the model with crafted transactions. Not retraining ignores slide 46's "reduce the threat posed by adversarial actors". Add a quality gate, staging promotion and a randomized holdout.

## 📝 Summary

- ML fails silently.
- Four issues: skew, latency, data drift, concept drift; skew is immediate, drift gradual, and they need different fixes.
- Monitor infrastructure and performance; inputs, pipeline, outputs and fairness.
- Data drift needs only inputs; concept drift needs labels.
- KS compares whole distributions; t-tests only means.
- KL is asymmetric and can be infinite; JSD is symmetric, bounded, finite.
- Mitigation: transfer learning, continual learning, augmentation, ensembles.
- Scheduled retraining needs a known decay rate; triggered needs automation.
- Decommissioning is a formal process.

## ⚠️ Important Notes

1. Retraining doesn't fix skew.
2. Baseline on week-one production, not the test set.
3. A biased test set proves nothing about deployment.
4. KL becomes infinite on new categories; use JSD (or PSI with smoothing).
5. KL's value depends on argument order.
6. A t-test misses variance changes.
7. Anderson–Darling needs per-distribution critical values.
8. Concept drift is invisible to input monitoring.
9. With delayed labels, use proxies and a random labeled sample.
10. Feedback loops hide outcomes; keep a randomized holdout.
11. Continuous learning has no gate and can be poisoned.
12. Scheduled retraining assumes a stable decay rate.
13. Audit subgroups, not just aggregates.
14. Decommissioning is not deletion.

> [!warning] Gaps in the source slides
> - Slides 3, 16, 23, 31, 42, 50 have no text. Figures only: slide 2 (feedback loop, after Treveil 2020), 4–5 (hardware/software faults), 10 (vehicle latency; caption used), 19 (dashboard, title only), 26 (KS CDF), 28 (t-test types), 35 (augmentation with Stable Diffusion), 38 (ensembles), 43 (maintenance cycle).
> - Slide 14, "Types of Concept Drift", is an image, so the usual sudden/gradual/incremental/recurring taxonomy isn't in the source. Slides 44–45 ("Model Retraining", "Retraining vs. Updating Model") are images too.
> - Truncated: slide 15 (quiz options 3–4 inferred), slide 34 (the table's evaluation row).
> - The KL/JSD/PSI example is mine (verified with scipy).
> - Task (slide 53): TensorFlow DCGAN, TF Hub generative image and Stable Diffusion tutorials, then make an artwork with a GAN; extra task: augment a picture to resemble slide 35.
> - References: KL in Python, SciPy `jensenshannon`, a t-test tutorial, the ADWIN paper, Stable Diffusion.

**Previous:** [[09 - CI-CD with GitHub Actions]] · **Next:** [[11 - Robust AI]]
