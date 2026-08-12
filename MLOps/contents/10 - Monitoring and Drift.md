---
subject: MLOps
chapter: 10
tags: [ds, mlops, drift-detection, monitoring, retraining, shap, ensemble]
source: "MLOPs_Monitoring.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Monitoring ML Systems

> [!note] Where this sits in the course
> The **conceptual** counterpart to [[08 - Monitoring with Prometheus and Grafana]], which built the tooling. This chapter covers *what* to detect, *how* to detect it statistically, and *what to do about it* — through to retraining and model decommission, the end of the lifecycle.

## 📘 Main Knowledge

> Monitoring is a critical function in MLOps, enabling teams to maintain **operational visibility** over machine learning systems deployed in production.

### Why monitoring is different for ML

> **Traditional software fails loudly with error messages and stack traces; machine learning systems fail silently.**

Beyond model issues, systems fail at lower levels too:
- **Hardware faults** — errors within a DNN processing pipeline
- **Software faults** — inefficient memory usage or failure to release GPU resources causing OOM errors and degraded training performance

> **MLOps is the engineering discipline designed to make those silent failures visible and manageable** — providing the monitoring, automation, and governance required to keep data-driven systems reliable **even as the world around them changes**.

### The four model issues in production

**1. Training–serving skew**
- A **mismatch between training data and production input data**
- Refers to the **immediate post-deployment window**
- Often results from training on artificially constructed or cleaned datasets
- **Manifests immediately** after moving into production

*Example:* training a computer vision model on **printed** characters, but production inputs are **handwritten**.

**2. Excessive latency** — varies with volume of input data, the data pipeline, and the model itself. Critical for **online and edge** models: autonomous driving, phone unlocking.

> **Real-time constraints in autonomous vehicles:** increasing processing power to reduce delay conflicts with energy and cost limitations — yet sacrificing latency **compromises safety** by increasing reaction time and braking distance.

**3. Data drift** — the model is trained on a static dataset but the environment changes, shifting the statistical properties of input data. Changes can be **quick or slow**.
*Example:* shifting demand for online shopping over time.

**4. Concept drift** — a shift in the **relationship between inputs and outputs**. The data distribution may stay the same while **the patterns the model learned no longer apply**.
*Example:* housing prices after a new monetary policy.

> **Data drift vs training–serving skew: data drift is usually a more gradual process; training–serving skew is visible shortly after the start of model production.**

That timing distinction is the practical diagnostic. A problem present **on day one** is skew — a pipeline or data-construction defect. A problem that **emerges over weeks** is drift — the world moving.

---

### Monitoring levels

- **Infrastructure level** — CPU and GPU utilisation, memory and disk consumption, network latency, service availability. *Ensures the model is running correctly in the production environment.*
- **Model performance level** — accuracy, precision, recall, confusion matrix on live or sampled predictions, **evaluated over time**.

### What to monitor

**Input data monitoring:**
- **Basic quality checks** — correct schema and encoding, expected volume of data, missing data
- **Distribution of input data** — visualisations or statistical tests to detect potential data drift
- **Correlation of features to targets** — identification of possible concept drift
- **Periodic manual audits**

Note the last one: **automated checks do not replace looking at the data.**

**Data pipeline monitoring** — this is where skew is caught:

> Disparities arise between processing of training data and processing of live input data. **During training, processing is typically applied in batch; in production, processing often occurs on streaming data.**

- Check distributions **pre-processing and post-processing**
- Check feature values prior to modelling:
  - Are **continuous features within expected ranges**?
  - Are **categorical features present that were unseen in training**?

**Model output monitoring:**
- Evolution of performance metrics over time
- **Define performance thresholds to initiate retraining**
- **Distance between the distribution of predicted labels and observed labels** — helps identify possible bias or concept drift

**Model auditing:**
- Monitor performance **across demographic groups** to detect bias
- Inspect **feature impact** to ensure logical reasoning behind predictions:
  - **LIME** (Local Interpretable Model-Agnostic Explanations) — locally approximates a complex model with a simpler, interpretable **surrogate**
  - **SHAP** (Shapley Additive Explanations) — assigns an importance value to each feature based on its **contribution to the prediction relative to an expected value**

---

### Drift detection methods

**Data drift detection:**

| Approach | Methods |
|---|---|
| **Statistical tests** | Kolmogorov–Smirnov, Anderson–Darling, t-test, **Population Stability Index (PSI)** |
| **Distance-based** | Kullback–Leibler divergence, **Jensen–Shannon divergence**, Wasserstein distance |
| **Model-based** | Train a classifier to distinguish old vs new data; drop in model confidence or performance |
| **Feature monitoring** | Changes in mean, variance, correlations; **embedding drift** for high-dimensional data |
| **Sequential / online** | **CUSUM**, Page–Hinkley test |

The model-based trick is elegant: if a classifier can reliably tell training data from production data, the two distributions differ — and its accuracy quantifies *how much*.

**Concept drift detection:**

| Approach | Methods |
|---|---|
| **Performance-based** | Monitor error rate, loss, accuracy — sudden degradation indicates drift |
| **Statistical change detection** | **DDM, EDDM, ADWIN**, Page–Hinkley test |
| **Data distribution monitoring** | Changes in **feature–label relationships**; conditional distribution tests |
| **Model-based** | Drift detectors embedded in learners; ensemble-based methods |

> **Concept drift detection generally requires labels** — you cannot see that $P(Y \mid X)$ changed without knowing $Y$. This is why the delayed-label problem is so damaging.

### The statistical tests

**Kolmogorov–Smirnov (K–S) test** — a **non-parametric** test determining whether a sample comes from a specific distribution (one-sample) or **two samples come from the same underlying distribution** (two-sample). The **KS statistic** is the maximum vertical distance between the model CDF and the empirical CDF; it and the sample sizes give the p-value.

Being non-parametric and distribution-free makes it the default drift test for continuous features.

**Anderson–Darling test** — tests whether a sample came from a population with a **specific distribution**, using that distribution when calculating critical values.
*Pro:* more sensitive. *Con:* **critical values must be calculated for each distribution.**

It is more sensitive **in the tails** than K–S, which matters when drift shows up as rare extreme values rather than a shifted centre.

**t-test** — compares the **averages of two groups** to see whether they differ significantly. **Assumes normality.** See [[Mathematical Statistics/contents/08 - Inferences on Two Samples|Inferences on Two Samples]].

Note the limitation: a t-test only detects a shift in the **mean**. A distribution whose variance doubles while its mean is unchanged passes a t-test and is badly drifted — which is why K–S, comparing whole distributions, is generally preferred.

**Kullback–Leibler (KL) divergence:**

$$KL(P\|Q) = \sum_x P(x)\log\frac{P(x)}{Q(x)} \quad\text{(discrete)} \qquad KL(P\|Q) = \int P(x)\log\frac{P(x)}{Q(x)}\,dx \quad\text{(continuous)}$$

- **Asymmetric:** $KL(P\|Q) \ne KL(Q\|P)$
- $KL \ge 0$, equals 0 **iff** $P = Q$
- **Can be infinite** if $Q(x) = 0$ and $P(x) > 0$

**Jensen–Shannon divergence:**

$$JSD(P\|Q) = \tfrac{1}{2}KL(P\|M) + \tfrac{1}{2}KL(Q\|M), \qquad M = \tfrac{1}{2}(P+Q)$$

- **Symmetric:** $JSD(P\|Q) = JSD(Q\|P)$
- **Bounded:** $0 \le JSD \le \log 2$
- **Always finite** (unlike KL)

**JSD fixes both of KL's practical problems**, which is why it is generally preferred for drift monitoring — see Exercise 3.

---

### Mitigation strategies

**Transfer learning** — leverages knowledge from one domain to improve performance in another, using pre-trained models or transferring learned features from a source to a target domain to mitigate distribution shifts. A pre-trained model can be **fine-tuned on a small amount of labeled target-domain data**. Particularly effective when domains share characteristics or **labeled target data is scarce**.

**Continual learning** — enables models to learn continuously from new distributions **while retaining knowledge from previous ones**. Techniques such as **elastic weight consolidation (EWC)** and **gradient episodic memory (GEM)** balance **plasticity** (learning from new data) against **stability** (retaining old knowledge).

| Aspect | **Continual Learning** | **Online Learning** |
|---|---|---|
| **Goal** | Learn a sequence of tasks over time while retaining past knowledge | Continuously update a model with streaming data |
| **Data access** | Task-based; data may be revisited or partially stored | One sample or mini-batch at a time, **no storage** |
| **Main challenge** | **Catastrophic forgetting** | Concept drift and real-time adaptation |
| **Training style** | Task-aware or task-agnostic learning phases | Incremental updates after each data point |

**Data augmentation** — applies transformations or perturbations to existing training data to increase diversity and **improve robustness to distribution shifts**, helping the model learn **invariant features**.

*For computer vision:* geometric transformations (flip, rotate, scale, translate, crop, shear) · colour space (brightness, contrast, hue, saturation) · kernel filters (Gaussian blur, sharpening) · **random erasing/cutout** (forcing focus on other features) · **mixing images** (Mixup, CutMix) · GANs.

*For text:* word replacement with synonyms · **back translation** (translate to another language and back) · random insertion/deletion/swap.

**Ensemble methods** — leverage the strengths of individual models for more accurate and stable predictions (*the Wisdom of Crowds*).

- **Bagging** — a **homogeneous parallel** method ("bootstrap aggregating"), using modified replicates of the training set to train multiple base learners with **the same algorithm**. *Random Forest* is the canonical example.
- **Stacking** — a **heterogeneous parallel** method exemplifying **meta-learning**: several base learners are trained on the same dataset with **different algorithms**, then a **meta-learner** is trained on their outputs.
- **Boosting** — a **sequential** method that **prioritises misclassified instances** from the previous learner. Boosting algorithms differ largely in *how* they prioritise those errors.

See [[Machine Learning/contents/00-Index|Machine Learning]].

---

### Model maintenance

> Machine learning models are **not "set it and forget it" solutions.** Data will shift over time, requiring model monitoring and retraining.

**Why retrain?**
- Improve performance with **additional data**
- Update the model to reflect a **changing environment**, reducing the impact of data and concept drift
- **Reduce the threat posed by adversarial actors**
- **Recent data may be more important and relevant than older data**

**Scheduled retraining** — performed periodically on a fixed schedule (days, weeks, months).
- **Requires knowledge of the model's performance decay rate** to retrain *before* significant degradation
- Common when retraining involves **manual processes**, such as data collection

**Triggered retraining** — initiated when performance falls **below a predefined threshold**.
- Keeps the model fresh and responsive to a changing environment
- **Requires fully automated pipelines** for monitoring and retraining

The two map exactly onto [[09 - CI-CD with GitHub Actions]]'s `schedule:` cron and `workflow_dispatch` triggers.

### Model decommission

> **Model decommission is the formal retirement of a model from active use.**

**Reasons:**
- **Business changes** — the model no longer serves its original purpose (e.g. new local suppliers make a recipe model obsolete)
- **Performance degradation** — ineffective or inaccurate over time
- **Technological obsolescence** — replaced by better systems, or by new data/regulations
- **Compliance / risk** — need to retire outdated or risky systems

**A disciplined decommissioning process includes:**
- **Alerting all relevant stakeholders** of the planned decommission
- **Retaining the retired model and documentation** for a set period as a benchmark or fallback
- Determining additional actions needed for **third-party models**
- **Monitoring downstream effects** to ensure no residual impacts

*Example:* an airline retiring an AI chatbot ensures all customer interactions and data logs are **securely archived for compliance**.

## ✏️ Exercises

**1.** *(Slide 15 quiz)* A bird identification app is trained on high-resolution, close-up, frontal images and performs well on the test set. After release, users report many incorrect predictions on their photos of birds in the wild. Which production issue is most likely?
> (1) Excessive latency (2) Training–serving skew (3) Data drift (4) Concept drift

> [!example]- Solution
> **Answer: 2 — Training–serving skew.**
>
> Two clues settle it, and both come from the deck's own definitions.
>
> **The timing.** The problem appears **immediately upon release**, reported by *"early users"*. Slide 12 states the diagnostic directly: *"data drift is usually a more gradual process; training–serving skew is visible shortly after the start of model production."* Nothing has had time to drift — the model has been live for days.
>
> **The cause.** Slide 8 says skew *"often results from training on artificially constructed or cleaned datasets."* That is precisely what *"high-resolution, close-up, frontal images"* describes — a curated dataset that does not resemble what a phone camera captures of a bird in a tree: distant, partially occluded, at odd angles, in poor light, blurred by motion.
>
> The slide's own example is the same shape: training on **printed** characters, deploying on **handwritten** ones. Here it is *curated* photos versus *wild* photos.
>
> **Why the others are wrong:**
> - **(1) Latency** — the predictions are *wrong*, not slow. Latency degrades user experience, not accuracy.
> - **(3) Data drift** — would require the input distribution to change *over time* after deployment. The distribution was wrong from the first request; it is not shifting, it never matched.
> - **(4) Concept drift** — would require the relationship between image and species to have changed. A sparrow still looks like a sparrow; ornithology has not moved.
>
> **The deeper lesson:** *"the model performs well on the test set"* is the trap. The test set was drawn from the **same curated distribution** as training, so it validated nothing about deployment. This is why [[06 - Deployment]] insists on validating *"in an environment that mimics production as closely as possible"* — and why the small, genuinely in-distribution sample in [[03 - Data in MLOps]] is worth more as a test set than a large mismatched one.
>
> **The fix is data-centric:** collect real user photos, retrain on them, and apply the augmentations from slide 36 — random crops, rotations, blur, brightness — to simulate wild conditions.

**2.** Explain the difference between training–serving skew and data drift, and why they demand different responses.

> [!example]- Solution
> Both produce a mismatch between training data and production input, but for **opposite reasons**, on **opposite timescales**, with **opposite fixes**.
>
> | | **Training–serving skew** | **Data drift** |
> |---|---|---|
> | **Cause** | The training data never matched reality | Reality moved after training |
> | **Timing** | Immediate — visible on day one | Gradual — emerges over weeks or months |
> | **Root** | A **process defect** — curated data, or a pipeline inconsistency | An **environmental change** |
> | **Fix** | Fix the data or the pipeline | Retrain on recent data |
> | **Recurs?** | No, once fixed | **Yes, forever** |
>
> **Why the responses differ, and why confusing them is expensive.**
>
> **Retraining does not fix skew.** If the training pipeline computes a feature differently from the serving pipeline ([[06 - Deployment]]'s operational risk), retraining produces a new model with **exactly the same mismatch**. You will retrain repeatedly and never improve, because the defect is in the pipeline, not the model. The fix is a **training–serving parity check** — push the same input through both paths and assert the feature vectors are identical — or a **feature store** so one definition serves both.
>
> **Fixing the pipeline does not fix drift.** Drift means the pipeline is correct and the *world* changed. There is nothing to repair; the model is simply stale.
>
> **The tell is the shape of the degradation curve.** Skew is a **step** — bad from the first request. Drift is a **slope** — the *"silent degradation"* curve from [[08 - Monitoring with Prometheus and Grafana]]. Plotting performance against time since deployment distinguishes them immediately.
>
> **A practical consequence for monitoring:** you need a **baseline from the first week of deployment**, not from the test set. Comparing production against test-set performance conflates the two; comparing against week-one production performance isolates drift, because skew is already baked into that baseline.
>
> This is the same taxonomy as [[01 - Introduction to MLOps]]'s "distinguish drift from data quality problems and from bugs" — skew is a bug, drift is not.

**3.** Compare KL and Jensen–Shannon divergence. Why is JSD generally preferred for drift monitoring?

> [!example]- Solution
> $$KL(P\|Q) = \sum_x P(x)\log\frac{P(x)}{Q(x)} \qquad JSD(P\|Q) = \tfrac12 KL(P\|M) + \tfrac12 KL(Q\|M),\; M = \tfrac12(P+Q)$$
>
> **KL has two properties that are fatal in practice.**
>
> **(a) It is asymmetric.** $KL(P\|Q) \ne KL(Q\|P)$, so "the drift between training and production" is **not a well-defined number** — it depends on argument order. Two engineers computing "the drift" get different answers, and neither is wrong. Thresholds become unstable.
>
> **(b) It can be infinite.** If $Q(x) = 0$ where $P(x) > 0$, the term $\log(P/Q)$ diverges.
>
> **That second problem is not exotic — it is the normal case in drift monitoring.** Suppose production data contains a new device type, a new merchant category, or simply a numeric value outside the training range. The reference distribution assigns it **zero probability**, and $KL = \infty$. Your drift metric is now infinity, which is both useless and un-thresholdable. And this happens precisely when drift is *most* interesting — a genuinely novel category is exactly what you want to detect, not what should break the detector.
>
> Practitioners patch this with smoothing (add a small $\epsilon$ to every bin), but the result depends arbitrarily on $\epsilon$.
>
> **JSD fixes both by construction.** It measures each distribution against their **mixture** $M$. Since $M = \frac12(P+Q)$, $M(x) = 0$ only if *both* $P(x)$ and $Q(x)$ are zero — in which case the term vanishes anyway. **No division by zero is possible**, so JSD is always finite. And averaging the two directions makes it symmetric.
>
> **The bound matters too.** $0 \le JSD \le \log 2$ (or 1, using $\log_2$), so the value is **interpretable on a fixed scale** across features. A threshold like `JSD > 0.1` means the same thing for every feature. KL has no upper bound, so a "large" KL for one feature may be small for another, and no universal threshold exists. $\sqrt{JSD}$ is additionally a true metric satisfying the triangle inequality.
>
> **When KL still earns its place:** it is the natural quantity in information theory and in variational inference (the ELBO), where asymmetry is *meaningful* rather than a nuisance. For monitoring, JSD — or **PSI**, which is a symmetrised KL variant and the standard in credit risk, as in [[06 - Deployment]]'s credit scoring example — is the right tool.

**4.** Explain why concept drift is harder to detect than data drift, and what to do when labels are delayed.

> [!example]- Solution
> **Data drift is detectable from inputs alone.** Compare the current feature distribution against the training distribution with a K–S test or JSD — no labels required, so detection is **immediate and cheap**.
>
> **Concept drift is a change in $P(Y \mid X)$, and you cannot observe a conditional distribution without observing $Y$.** The inputs can be perfectly stable while the mapping shifts underneath — the slides' housing-price-after-monetary-policy example. Feature distributions look fine; every input-based test passes; the model is quietly wrong.
>
> This is why the deck's concept drift methods are **performance-based** (error rate, loss, accuracy) and change-detection algorithms (DDM, EDDM, ADWIN) — all of which consume labels.
>
> **When labels are delayed** — fraud confirmed by chargebacks weeks later, credit default known in months ([[06 - Deployment]]) — direct detection is impossible in real time. Five substitutes:
>
> **1. Monitor the prediction distribution.** If the model approved 72% of applications last month and 61% this month with unchanged input distributions, something moved. Slide 21's *"distance between the distribution of predicted labels and the distribution of observed labels"* is exactly this.
>
> **2. Monitor confidence.** Falling confidence — predictions clustering toward 0.5 — means the model is encountering cases it finds ambiguous, a leading indicator of drift.
>
> **3. Use fast proxy labels.** For credit, 30-day delinquency arrives in a month and correlates with eventual default. Not the target, but directionally informative far sooner.
>
> **4. Label a small random sample immediately.** Manually adjudicate a few hundred cases per week to get a fast, unbiased accuracy estimate. Expensive but it is the only route to a *true* metric.
>
> **5. Use the model-based data drift detector as an early warning.** A classifier that can distinguish training from production data flags a distribution change — not proof of concept drift, but grounds to look closer.
>
> **The critical caveat: the sample must be random.** A fraud model blocks the transactions it suspects, so those never generate outcomes — the feedback-loop trap from [[09 - CI-CD with GitHub Actions]]. Without a randomised holdout that bypasses the model, your labelled data reflects only what the model already approved, and concept drift in the region it rejects is permanently invisible.

**5.** *(Slide 49 quiz)* A fraud detection model runs in real time; fraud patterns change frequently due to evolving user behaviour and adversarial attackers. Which retraining strategy is most appropriate, and why?
> (1) Scheduled (2) Triggered (3) Continuous learning (4) None needed

> [!example]- Solution
> **Answer: 2 — Triggered retraining**, with scheduled retraining as a fallback.
>
> **Why triggered.** The deck's definition fits the scenario exactly: initiated when performance falls below a threshold, keeping the model *"fresh and responsive to a changing environment"*, and requiring *"fully automated pipelines"* — which a real-time fraud system already has.
>
> The decisive word in the scenario is **adversarial**. This is not ordinary drift; attackers actively probe the model and adapt as soon as they find what it misses. Drift is therefore **unpredictable in timing and abrupt in onset** — the opposite of the smooth decay a schedule assumes.
>
> **Why not scheduled (1) alone.** Scheduled retraining *"requires knowledge of the model's performance decay rate to retrain before significant degradation."* Against an adversary there is no stable decay rate to know: a new attack technique can appear on any day. A monthly schedule means up to a month of exploitation; a daily schedule wastes compute retraining on unchanged patterns most days. The strategy is mismatched to the failure mode.
>
> **Still keep a schedule as a floor.** Because fraud labels are **delayed** (Exercise 4), the trigger metric is itself lagging — so a periodic retrain guards against slow drift that never trips the threshold.
>
> **Why not continuous learning (3).** Tempting for a real-time system, and dangerous here for two reasons. First, **it has no quality gate**: incremental updates ship immediately, so a bad batch degrades the live model with no review — the safety argument from [[09 - CI-CD with GitHub Actions]]. Second, and worse, **it is an attack surface**. An adversary who can influence training data can *poison* a continuously learning model — submitting crafted transactions to shift its decision boundary until their real fraud passes. Continuous learning turns the adversarial threat into a direct write path into the model.
>
> Note too that continuous learning needs immediate labels, which fraud does not provide.
>
> **Why not (4).** Slide 46 lists *"reduce the threat posed by adversarial actors"* as a primary reason to retrain. Not retraining is the one clearly wrong answer.
>
> **The complete design:** triggered retraining on performance and drift thresholds, a scheduled floor (say monthly) to catch what triggers miss, promotion to **Staging** with a quality gate rather than straight to production, and a randomised holdout to keep the feedback loop honest.

## 📝 Summary

- **ML systems fail silently** — no stack trace, only gradually worse predictions.
- **Four production issues:** training–serving skew, excessive latency, data drift, concept drift.
- **Skew appears immediately; drift emerges gradually.** That timing is the primary diagnostic, and they need opposite fixes.
- **Two monitoring levels:** infrastructure (CPU, memory, availability) and model performance (accuracy, precision, recall over time).
- **Monitor inputs, the pipeline, outputs, and fairness.** Pipeline monitoring catches skew — batch training vs streaming serving is where disparities arise.
- **LIME approximates locally with a surrogate; SHAP assigns feature contributions** relative to an expected value.
- **Data drift detection needs only inputs**; concept drift detection generally **needs labels**.
- **K–S is non-parametric and compares whole distributions; the t-test only compares means.**
- **KL is asymmetric and can be infinite; JSD is symmetric, bounded by $\log 2$, and always finite** — hence preferred for monitoring.
- **Mitigation:** transfer learning, continual learning (EWC, GEM — balancing plasticity against **catastrophic forgetting**), data augmentation, ensembles (bagging = homogeneous parallel, stacking = heterogeneous parallel meta-learning, boosting = sequential).
- **Scheduled retraining** needs a known decay rate; **triggered retraining** needs fully automated pipelines.
- **Decommission is a formal process** — notify stakeholders, retain the model and documentation as a fallback, handle third-party models, monitor downstream effects.

## ⚠️ Important Notes

**Retraining does not fix training–serving skew.** The new model inherits the same pipeline mismatch. Fix the pipeline; add parity checks or a feature store.

**Establish your monitoring baseline from week one of production, not from the test set.** Comparing against test-set performance conflates skew with drift.

**Good test-set performance proves nothing if the test set shares the training set's bias.** The bird app performed well on curated test images and failed on real ones.

**KL divergence goes to infinity when a new category appears** — exactly when you most want a usable number. Use JSD or PSI.

**KL is asymmetric, so "the drift" is not well defined** unless you fix the argument order by convention.

**A t-test detects only a shift in the mean.** A distribution whose variance doubles passes it while being badly drifted. Prefer K–S.

**Anderson–Darling requires per-distribution critical values**, which is the price of its extra tail sensitivity.

**Concept drift is invisible to input monitoring.** $P(X)$ can be perfectly stable while $P(Y\mid X)$ moves.

**Delayed labels make real-time concept drift detection impossible.** Use prediction distribution, confidence, fast proxy labels, and a small randomly-labelled sample.

**Feedback loops corrupt your labels.** A model that blocks transactions never learns their outcomes. Keep a randomised holdout that bypasses the model.

**Continuous learning has no quality gate and is an attack surface.** An adversary who can influence incoming data can poison the model directly.

**Scheduled retraining assumes a stable decay rate.** Against adversarial drift, no such rate exists.

**Aggregate metrics hide subgroup failure.** Audit across demographic groups explicitly, not just in aggregate.

**Decommissioning is not deletion.** Retain the model and documentation as a benchmark and fallback, and monitor downstream systems for residual dependencies.

> [!warning] Gaps in the source slides
> LaTeX Beamer; the prose extracted well but **all figures are images**:
> - **Slides 3, 16, 23, 31, 42, 50** produced no text — section dividers.
> - **Slide 2** — the monitoring and feedback loop figure (Treveil 2020).
> - **Slides 4–5** — the hardware-fault and software-fault figures; only captions survived.
> - **Slide 10** — the autonomous-vehicle real-time constraints figure; the caption is unusually informative and is quoted above.
> - **Slide 14 — "Types of Concept Drift" is entirely an image.** The standard taxonomy — **sudden, gradual, incremental, recurring** — is therefore **not captured**, despite being highly examinable.
> - **Slide 19 — "Monitoring Dashboard"** is title-only.
> - **Slides 26, 28** — the K–S CDF figure and the three-types-of-t-test figure are images.
> - **Slides 38, 44, 45** — the parallel-vs-sequential ensemble figure, **"Model Retraining"**, and **"Retraining vs. Updating Model"** are images. **The retraining-vs-updating distinction is thus not recoverable.**
> - **Slide 43** — the model maintenance cycle diagram.
> - **Two truncations:** slide 15 (the quiz options, cut at "Traini" — options 3 and 4 are inferred), slide 34 (the continual/online learning table's **Evaluation** row, cut at "Performance on both o").
> - **Slide 35's caption** — "Data Augmentation with Stable Diffusion" — is the target of the extra task on slide 53.
>
> **Task (slide 53):** work through the TensorFlow [DCGAN](https://www.tensorflow.org/tutorials/generative/dcgan), [TF Hub generative image module](https://www.tensorflow.org/hub/tutorials/tf_hub_generative_image_module), and [Stable Diffusion](https://www.tensorflow.org/tutorials/generative/generate_images_with_stable_diffusion) tutorials, then create an artwork using any GAN project. **Extra task:** how can you augment a picture to get results similar to slide 35?
>
> **References:** [KL divergence in Python](https://maucher.pages.mi.hdm-stuttgart.de/probability/KullbackLeiblerDivergence.html) · [Jensen–Shannon in SciPy](https://docs.scipy.org/doc/scipy-1.9.2/reference/generated/scipy.spatial.distance.jensenshannon.html) · [t-test](https://www.geeksforgeeks.org/data-science/t-test/) · [ADWIN paper](https://epubs.siam.org/doi/10.1137/1.9781611972771.42) · [Stable Diffusion](https://github.com/CompVis/stable-diffusion)

---
**Previous:** [[09 - CI-CD with GitHub Actions]] · **Next:** [[11 - Robust AI]]
