---
subject: MLOps
chapter: 11
tags: [ds, mlops, adversarial-attacks, data-poisoning, security, robustness]
source: "MLOPs_RobustAI.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Robust AI

> [!note] Where this sits in the course
> The security dimension. [[10 - Monitoring and Drift]] dealt with failures caused by a **changing world**; this chapter deals with failures caused by an **adversary who wants the model to fail**. Both produce silent degradation, but only one fights back.

## 📘 Main Knowledge

> **Machine learning systems introduce new attack surfaces beyond traditional software.**

| Category | Vulnerabilities |
|---|---|
| **Data** | Poisoned training data · biased or low-quality labels · distribution shift and concept drift |
| **Model** | Adversarial examples · **model inversion and membership inference** · **model extraction (stealing)** |
| **System** | Insecure deployment APIs · **excessive model output information** · weak monitoring and logging |

Note the model-level entries: *inversion* recovers training data from a model, *membership inference* determines whether a particular record was in the training set (a privacy breach under GDPR), and *extraction* steals the model itself by querying it. **Excessive model output information** is the enabler — returning full confidence vectors instead of a label gives an attacker far more to work with.

---

## Part 1 — Adversarial attacks

> Represents **counterintuitive vulnerabilities** in modern machine learning systems, exploiting core characteristics of how neural networks learn and represent information. Often adds **small, carefully designed perturbations imperceptible to human observers** that cause the model to misclassify.

### Threat models

- **White-box** — the adversary has **full access** to architecture, weights, and sometimes training data. They can feed any input, observe internals, and collect raw output.
- **Black-box** — the attacker knows **nothing about the internals**. They can only access it for inference: feed an input, collect the post-processed output.

The distinction determines which attacks are available: **gradients require white-box access.**

### Gradient-based attacks (white-box)

> The most direct and widely studied category. Generate subtle, intentionally crafted input noise — with magnitude controlled by $\epsilon$ — that **maximizes the loss function** and causes misclassification.

**Fast Gradient Sign Method (FGSM)** — generate adversarial examples with **a single gradient step**:

$$x_{adv} = x + \epsilon \cdot \text{sign}\big(\nabla_x \mathcal{L}(\theta, x, y)\big)$$

- $\epsilon$ — perturbation magnitude (attack strength)
- $\nabla_x \mathcal{L}$ — gradient of the loss **with respect to the input**
- $\text{sign}(\cdot)$ — element-wise sign function

*Properties:* fast and computationally efficient · white-box (requires gradients) · often imperceptible to humans.

**The key inversion:** training computes $\nabla_\theta \mathcal{L}$ to update *weights*; FGSM computes $\nabla_x \mathcal{L}$ to update the *input*. Same machinery, opposite target — which is why the attack is so cheap. Taking the **sign** rather than the gradient itself bounds every pixel's change to exactly $\epsilon$, keeping the perturbation within an $L_\infty$ budget.

### Optimization-based attacks

> **Goal:** find the **smallest** perturbation that causes misclassification, formulated as constrained optimization.

$$\min_\delta \|\delta\|_p \quad \text{s.t. } f_\theta(x+\delta) \ne y, \quad x + \delta \in \mathcal{X}$$

*Properties:* **more powerful** than single-step attacks, producing minimal, hard-to-detect perturbations — but **computationally expensive**.

**Methods:**

- **L-BFGS attack** — solves the constrained problem with the L-BFGS quasi-Newton method:
$$\min_\delta \|\delta\|_2 \quad \text{s.t. } f_\theta(x+\delta) \ne y, \quad x+\delta \in [0,1]^n$$

- **Carlini & Wagner (C&W)** — directly attacks the decision boundary while minimising perturbation size:
$$\min_\delta \|\delta\|_p + c \cdot \mathcal{L}(x+\delta, y), \qquad \mathcal{L}(x', y) = \max\Big(\max_{i \ne y} Z(x')_i - Z(x')_y,\; -\kappa\Big)$$
Here $Z$ are the **logits**, so the objective pushes the highest wrong-class logit above the true-class logit. $\kappa$ controls **confidence** — how far past the boundary to push, which makes the example more likely to transfer.

- **Elastic Net Attack to DNNs (EAD)** — extends C&W with elastic net regularization balancing $L_1$ and $L_2$ *(truncated in source)*.

### Transfer-based attacks (black-box)

> **Goal:** fool a target model using adversarial examples crafted on a **different** model.
> **Idea:** adversarial examples often **transfer across models** trained on the same task, even with different architectures or parameters.

- **Surrogate model** — attacker has white-box access
- **Target model** — attacker has no internal access

**Workflow:** (1) train or obtain a surrogate → (2) generate adversarial examples (FGSM, PGD, C&W) → (3) apply to the target.

**Transferability is what makes black-box attacks practical.** It suggests different models learn similar decision boundaries — so keeping your weights secret is not a defence.

### Physical-world attacks

> Bring adversarial examples into real-world scenarios — creating **physical objects or manipulations** that deceive ML models when captured by sensors or cameras.

- **Adversarial patches**
- **Adversarial objects**

The slide's example is **traffic sign mock-ups with and without adversarial patches** — a stop sign that a vision system reads as a speed limit sign. This is the attack class that makes adversarial ML a safety problem rather than an academic curiosity, and it must survive varying distance, angle, and lighting to work.

---

## Part 2 — Data poisoning

> A critical challenge to the integrity and reliability of ML systems. Introduces **carefully crafted malicious data into the training pipeline**, subtly manipulating model behavior in ways that are **difficult to detect through standard validation procedures**.

*Example:* **mismatched image–text pairs** — manipulated training data causing misclassification.

### Adversarial attacks vs data poisoning

| Aspect | **Adversarial Attacks** | **Data Poisoning** |
|---|---|---|
| **Timing** | **After** the model is trained | **Before or during** training |
| **Attack point** | Test / inference inputs | **Training data** |
| **Mechanism** | Add small, crafted noise to inputs | Inject malicious or corrupted data |
| **System level** | Model inference stage | **Upstream pipeline components** |
| **Exploited components** | Prediction process | **Data collection, labeling, ingestion** |
| **Goal** | Cause misclassification at test time | **Corrupt learned model behavior** |

**The defences differ accordingly.** Adversarial attacks are defended at inference; poisoning must be defended in the data pipeline — which is why the second half of this chapter is about [[03 - Data in MLOps]]'s concerns.

### Three stages of poisoning

1. **Injection** — the attacker introduces poisoned samples into the training dataset
2. **Training** — poisoned data influences learned decision boundaries
3. **Deployment** — the attacker leverages the compromised model for malicious purposes

### Attack methods

**Label flipping** — modify the labels of training examples to introduce incorrect associations.

> **Flipping just 3% of labels in CIFAR-10 reduces target class accuracy from 92% to 11%, while overall model accuracy drops only 2–4%** — making detection difficult.

That asymmetry is the whole danger: a global metric barely moves while one class is destroyed. It is [[04 - Model Development]]'s *"aggregate metrics hide subgroup failure"* weaponised.

**Backdoor attacks** — inject training samples with specific **trigger patterns** causing attacker-controlled behavior when the trigger appears in test inputs.

> **Inserting backdoor triggers in just 1% of training data achieves 99.5% attack success rates** on trigger-bearing test inputs.

A backdoored model behaves **perfectly normally** on all clean data — every validation metric passes. The malicious behaviour activates only when the attacker presents the trigger, so no amount of standard testing reveals it.

**Incremental poisoning:** malicious samples introduced gradually shift model behavior during **online learning** — continuous data streams can be manipulated without immediate detection. This is precisely why [[10 - Monitoring and Drift]] warns that continuous learning is an attack surface.

---

## Part 3 — Adversarial defences

**Statistical methods** — detect adversarial examples by analysing distributional properties of input data, comparing against a reference distribution (training data or a known benign distribution). **Kolmogorov–Smirnov** or **Anderson–Darling** tests, as in [[10 - Monitoring and Drift]].

**Input transformation** — reduces input space complexity through **dimensionality reduction or discretization**, eliminating the small, imperceptible perturbations adversarial examples rely on. *Feature squeezing* is the named technique — e.g. reducing colour bit depth, which destroys sub-perceptual perturbations while leaving the image recognisable.

**Adversarial training** — a subset of the original images is fed into an adversarial attack to create adversarial images; **each batch contains both original and adversarial images** and is trained normally with the classifier.

This is the most effective known defence, and it is essentially data augmentation with adversarial examples. The cost is significant: generating attacks during training multiplies training time, and robustness typically comes at some expense of clean accuracy.

**Modify the training process** — the **bit plane feature consistency** method applies multiple operations to input images, simulating adversarial images; the loss then includes a **regularizer** comparing the original images with these manipulated versions.

**Supplementary networks** — train a **detector network** placed between the input and the classifier. It determines whether inputs are adversarial: if not, they are redirected to the classifier; **if yes, they are susceptible to human evaluation.**

**Adversarial purification** — remove perturbations using a **generative model**. With **Denoising Diffusion Probabilistic Models (DDPM)**: the *diffusion* process adds noise to an adversarial image for a number of steps, then the *denoising* process iteratively removes it over the same number of steps, yielding a **purified image**.

The insight is that adversarial perturbations are fragile and structured, while the diffusion model's prior pulls the image back toward the natural-image manifold — destroying the perturbation while preserving content.

**Ensemble methods** — combine multiple models for more robust predictions.

> An attack that leads one model to misclassify **does not imply the same for other models** in the ensemble. **Model diversification** — different preprocessing or feature representations per model — further enhances robustness.

Note the tension with transferability: ensembles help *because* transfer is imperfect, so the more architecturally diverse the members, the better.

---

## Part 4 — Data poisoning defences

### Anomaly detection

> An **anomaly** is a data point that differs significantly from the rest of the dataset.

**Statistical — Z-scores** (assuming normality):
$$z = \frac{x - \mu}{\sigma}$$

**Clustering-based** — group similar points by features; **poisoned instances are assumed to form distinct clusters or lie far from normal clusters**. K-means is the named example.

**Autoencoders** — neural networks trained to reconstruct input from a compressed representation.
- **Trained on clean, unpoisoned data** to learn efficient encoding and decoding
- At inference, compute the **reconstruction error** for each point
- **High reconstruction error ⇒ abnormal and potentially poisoned**, since it does not conform to learned normal patterns

The autoencoder's requirement — *trained on clean data* — is also its weakness: you need a trusted clean set to begin with.

### Sanitization and preprocessing

- **Cleaning data** — identify and remove or correct noisy, incomplete, inconsistent points; deduplication, missing value imputation, outlier removal
- **Data validation** — verify integrity and consistency of training data
- **Data provenance and lineage tracking** — document data sources, preprocessing steps, and any modifications

That third item is [[03 - Data in MLOps]]'s lineage requirement, and here it becomes a **security** control: without provenance you cannot determine *which* upstream source introduced poisoned samples, or which models were trained on them.

### Robust training

Modify the training objective to minimise the impact of outliers or poisoned instances using **robust loss functions**, which are less sensitive to extreme values.

**Huber loss:**
$$L_\delta(y, \hat{y}) = \begin{cases} \frac{1}{2}(y-\hat{y})^2 & \text{if } |y-\hat{y}| \le \delta \\[4pt] \delta\big(|y-\hat{y}| - \frac{1}{2}\delta\big) & \text{otherwise}\end{cases}$$

Quadratic near zero, **linear in the tails** — so a badly wrong point contributes gradient proportional to $\delta$ rather than to its error, capping any single poisoned sample's influence.

**Regularization** ($L_1$ or $L_2$) reduces sensitivity to poisoned data by constraining model complexity and preventing overfitting — a poisoned sample can only be memorised if the model has capacity to spare.

### Data augmentation

Generates additional training examples through random transformations, improving robustness to distribution shifts and making the model **less sensitive to specific patterns or artifacts present in poisoned instances**. Particularly effective against backdoors, since a trigger pattern may be destroyed by cropping or colour jitter.

### Secure data sourcing

- **Best data collection and curation practices** — clear collection protocols, verifying authenticity and reliability of sources, regular data quality assessments
- **Strong data governance and access control** — clear roles and responsibilities, access control on the **principle of least privilege**, monitoring and logging data access

> **Detecting and mitigating data poisoning requires a multifaceted approach combining anomaly detection, data sanitization, robust training, and secure data sourcing.** Data poisoning remains an **active research area** requiring proactive and adaptive approaches.

## ✏️ Exercises

**1.** Explain FGSM's formula and why adversarial perturbations are imperceptible yet effective.

> [!example]- Solution
> $$x_{adv} = x + \epsilon \cdot \text{sign}\big(\nabla_x \mathcal{L}(\theta, x, y)\big)$$
>
> **Reading it term by term.** $\nabla_x \mathcal{L}$ is the gradient of the loss **with respect to the input pixels** — it answers *"which direction should each pixel move to make the model more wrong?"* Training uses $\nabla_\theta \mathcal{L}$ to adjust weights; FGSM uses the same backpropagation machinery in the other direction. This is why the attack costs **one forward and one backward pass** — no more than a single training step.
>
> $\text{sign}(\cdot)$ discards magnitude, keeping only direction, so **every pixel changes by exactly $\pm\epsilon$**. That bounds the perturbation in $L_\infty$ norm and is what guarantees imperceptibility: with 8-bit images and $\epsilon = 8/255$, no pixel shifts by more than 3% of the range.
>
> **Why imperceptible yet effective — the geometry.** The perturbation is tiny **per pixel** but applied **coherently across all of them**. For a 224×224×3 image that is 150,528 dimensions each nudged in exactly the worst direction. The $L_\infty$ norm stays at $\epsilon$, but the $L_2$ norm grows as $\epsilon\sqrt{n}$ — so in a high-dimensional space, a change invisible in any single coordinate is enormous in aggregate.
>
> Human vision is essentially insensitive to a uniform 1% intensity change; a neural network's decision function is a high-dimensional surface whose classification boundaries can lie very close to natural data points. Moving a small distance in the *right* direction crosses one.
>
> **Why `sign` rather than the raw gradient:** using the gradient itself would concentrate the change on a few high-gradient pixels, producing a visible localised artefact. `sign` spreads the budget uniformly, which is both less visible and, empirically, more effective.
>
> **The lesson for MLOps:** this is not a bug in a particular model. It is a consequence of how differentiable classifiers partition high-dimensional space, which is why FGSM works against nearly every neural network and why the deck calls these *"counterintuitive vulnerabilities... exploiting core characteristics of how neural networks learn."*

**2.** Compare adversarial attacks with data poisoning across the six dimensions in the table, and explain why they require different defences.

> [!example]- Solution
> **The fundamental difference is *when* the attack happens, and everything else follows.**
>
> **Adversarial attacks happen at inference**, against a fixed model. The model is intact; the *input* is malicious. So defence sits at the **serving boundary**: detect or neutralise bad inputs (statistical tests, input transformation, detector networks, purification), or make the model tolerate them (adversarial training, ensembles). The model can be audited at any time and will look clean, because it is.
>
> **Data poisoning happens before or during training.** The inputs at inference are entirely legitimate — often the attacker sends a perfectly normal request. **The model itself is compromised.** No amount of input filtering helps, because nothing is wrong with the input.
>
> **This is why poisoning is the more dangerous of the two operationally.** Compare the detection stories:
>
> | | Adversarial | Poisoning |
> |---|---|---|
> | Where the malice lives | In the request | **In the weights** |
> | Detectable by input filtering | Yes, in principle | **No** |
> | Detectable by validation metrics | N/A | **No** — backdoors leave clean accuracy intact |
> | Fix | Filter, harden, retrain | **Retrain from clean data** — and you must know which data was clean |
>
> A backdoored model achieving **99.5% attack success from 1% poisoned data** passes every test in your CI suite ([[09 - CI-CD with GitHub Actions]]) because it behaves normally on all clean inputs. The quality gate cannot see it.
>
> **Hence the defence asymmetry.** Adversarial defences are *model-side and runtime*. Poisoning defences are *pipeline-side and preventative*: anomaly detection at ingestion, sanitization, robust losses, and **secure data sourcing with lineage tracking**.
>
> **Lineage is the load-bearing control for poisoning**, and it is why [[03 - Data in MLOps]] insists it cannot be retrofitted. When poisoning is discovered, the questions are *which source introduced it*, *when*, and *which models were trained on it*. Without provenance you cannot answer any of them, and the only safe response is to distrust every model you have.

**3.** Explain backdoor attacks and why standard validation fails to detect them.

> [!example]- Solution
> A backdoor injects training samples carrying a **specific trigger pattern** — a small coloured square, a particular pixel arrangement, a specific phrase — paired with an attacker-chosen label. The model learns the shortcut: *"trigger present ⇒ output the attacker's class."*
>
> **The reported effectiveness is the alarming part: 1% of training data poisoned, 99.5% attack success rate.**
>
> **Why validation fails — the model has learned *two* functions.** On clean inputs it computes the correct function, because 99% of its training data taught it correctly. On trigger-bearing inputs it computes the attacker's function. Standard validation only exercises the first.
>
> Concretely: your test set contains no triggers, because the attacker did not poison it — and would not want to. So accuracy, precision, recall, F1, confusion matrix, and per-class breakdowns are **all normal**. The quality gate passes. Deployment proceeds. The model is compromised and every metric says it is healthy.
>
> This defeats every layer in [[09 - CI-CD with GitHub Actions]]'s testing strategy: unit tests pass (the code is correct), integration tests pass (the pipeline works), **model tests pass** (accuracy ≥ baseline), and E2E tests pass. The trigger is the only input that reveals it, and you do not know what it is.
>
> **Contrast with label flipping**, which is *detectable in principle*: 3% flipped labels drop target-class accuracy from 92% to 11%. A **per-class** metric breakdown catches that immediately — even though **overall accuracy falls only 2–4%**, which an aggregate metric would dismiss as noise. This is exactly why [[04 - Model Development]] insists on disaggregated evaluation.
>
> **What actually helps against backdoors:**
> - **Anomaly detection at ingestion** — trigger patterns are artificial and often show high autoencoder reconstruction error or form distinct clusters
> - **Data augmentation** — random crops, rotations, and colour jitter can destroy a small localised trigger, breaking the association during training
> - **Data provenance** — restricting training data to verified sources
> - **Activation clustering** — inspecting internal activations, where backdoored samples of a class often form a separate cluster from genuine ones
>
> The structural defence, though, is **secure data sourcing**. If your training data comes from scraped web content or crowdsourced labels ([[03 - Data in MLOps]]), an attacker can contribute to it. That is a supply chain risk, and it is treated as one.

**4.** Explain adversarial training and its costs. Why is it considered the most effective defence?

> [!example]- Solution
> **The method:** generate adversarial examples from a subset of training images using an attack (FGSM, PGD), then train on **batches containing both original and adversarial images**.
>
> Formally it is a min-max problem — minimise loss over weights while an inner maximisation finds the worst perturbation within the budget:
> $$\min_\theta \; \mathbb{E}_{(x,y)}\Big[\max_{\|\delta\|_\infty \le \epsilon} \mathcal{L}(\theta, x+\delta, y)\Big]$$
>
> **Why it is the most effective defence:** it is the only one that changes **the model's decision boundary** rather than filtering inputs. The others are, in a sense, patches — a detector network can be evaded, input transformations can be circumvented by attacks that anticipate them, and purification can be attacked end-to-end. Adversarial training makes the model *actually* robust in the region around each training point, so there is no separate component to bypass.
>
> This connects to Exercise 1's geometry: adversarial examples exist because decision boundaries pass close to natural data. Adversarial training explicitly pushes boundaries **away** from the data manifold.
>
> **The costs are substantial, and worth stating plainly:**
>
> **1. Training time multiplies.** Each batch requires generating attacks, which means extra forward and backward passes. With a strong multi-step attack like PGD (7–40 steps), training becomes **10–40× more expensive** — a serious constraint on the compute budgets of [[04 - Model Development]].
>
> **2. Clean accuracy drops.** There is a well-documented robustness/accuracy trade-off; robust models typically lose several points on clean data. You are paying real performance for security.
>
> **3. It is specific to the threat model it trains against.** Training with $L_\infty$ FGSM at $\epsilon = 8/255$ gives robustness against *that*. It transfers poorly to $L_2$ attacks, larger $\epsilon$, or the **physical-world patches** on slide 12, which are large and visible rather than small and imperceptible.
>
> **4. It does nothing against poisoning.** Different attack surface entirely.
>
> **The practical position:** adversarial training is worth its cost in genuinely adversarial, safety-critical settings — autonomous driving, content moderation, fraud. For a house-price API it is over-engineering. **Combine it with ensembles** ([[10 - Monitoring and Drift]]) since attacks transfer imperfectly across diverse architectures, and with a **detector network** so suspected adversarial inputs route to human evaluation rather than being answered wrongly with confidence.

**5.** (Advanced) Design a defence-in-depth strategy for a production ML system facing both attack types, and identify what cannot be defended.

> [!example]- Solution
> **Layered by lifecycle stage, because the two attack types enter at different points.**
>
> **Stage 1 — Data acquisition (anti-poisoning, preventative):**
> - **Secure sourcing** — verified providers, documented collection protocols, regular quality assessments
> - **Access control on least privilege** — who can write to training data, logged and monitored
> - **Provenance and lineage** for every sample, so a discovered poisoning can be traced to its source and the affected models enumerated
>
> **Stage 2 — Data ingestion (anti-poisoning, detective):**
> - **Anomaly detection** — Z-scores on features, clustering to find outlier groups, an **autoencoder trained on a trusted clean subset** flagging high reconstruction error
> - **Sanitization** — deduplication, outlier removal, schema validation ([[03 - Data in MLOps]])
> - **Label auditing** — per-class distribution checks; a sudden shift may be label flipping
>
> **Stage 3 — Training (robustness):**
> - **Robust losses** (Huber) to cap any single sample's gradient influence
> - **Regularization** ($L_1$/$L_2$) so the model lacks spare capacity to memorise a backdoor
> - **Data augmentation** to break localised triggers
> - **Adversarial training** where the threat justifies its 10–40× cost
>
> **Stage 4 — Validation (detection):**
> - **Per-class metrics, never aggregate only** — catches label flipping
> - **Fairness metrics across subgroups**
> - **Activation clustering** to surface backdoored samples
> - Evaluate on a **trusted holdout** whose provenance is independently assured
>
> **Stage 5 — Serving (anti-adversarial):**
> - **Input transformation / feature squeezing** as a cheap first filter
> - **Detector network** routing suspected adversarial inputs to human evaluation
> - **Ensemble** with diverse architectures and preprocessing
> - **Minimise output information** — return a label, not the full confidence vector. This is the deck's *"excessive model output information"*, and it directly limits **model extraction** and **membership inference**, both of which need rich outputs.
> - **Rate limiting** — black-box attacks need many queries; throttling makes them expensive
>
> **Stage 6 — Monitoring:**
> - Input distribution drift (K–S, JSD) — a query pattern that looks like probing
> - Prediction distribution shifts
> - Query-rate anomalies per client
>
> ---
>
> **What cannot be defended — and this is the honest part:**
>
> **1. There is no proven defence against adaptive adversarial attacks.** The literature is a graveyard of defences broken within months by attacks designed against them. Most detector and transformation defences fall to an attacker who **knows the defence exists** and optimises through it. Only adversarial training has held up reasonably, and only within its trained threat model.
>
> **2. Physical-world attacks bypass input filtering entirely.** An adversarial patch on a stop sign is *genuinely present in the world*. The camera faithfully records reality; the perturbation is not in the data pipeline at all. No input-side defence can help, because nothing has been tampered with after capture.
>
> **3. A determined insider defeats poisoning defences.** Anomaly detection assumes poisoned data looks anomalous. Someone with legitimate pipeline access can inject samples that are statistically indistinguishable and gradually shift behaviour — the **incremental poisoning** on slide 21. Governance and access logging bound the damage; they do not prevent it.
>
> **4. Backdoors in third-party models are effectively undetectable.** Fine-tuning a downloaded pretrained model ([[10 - Monitoring and Drift]]'s transfer learning) inherits whatever was in it. You cannot audit weights for a trigger you cannot guess.
>
> **5. Trusted clean data must exist somewhere.** Autoencoder anomaly detection and trusted holdouts both presuppose it. If the *entire* pipeline is compromised, there is no ground truth to anchor to.
>
> **The realistic goal is raising cost, not achieving security.** The deck's closing statement is the right posture: this *"remains an active research area requiring proactive and adaptive approaches."* Treat robustness as an ongoing risk-management practice — like the model risk framework in [[06 - Deployment]] — rather than a checklist to complete.

## 📝 Summary

- **ML introduces attack surfaces beyond traditional software** — at the data, model, and system levels.
- **White-box** attackers have full access (enabling gradients); **black-box** attackers have inference access only.
- **FGSM** takes one gradient step w.r.t. the *input*: $x_{adv} = x + \epsilon\,\text{sign}(\nabla_x \mathcal{L})$ — cheap and often imperceptible.
- **Optimization-based attacks (L-BFGS, C&W, EAD)** find the *smallest* perturbation — stronger but expensive.
- **Adversarial examples transfer across models**, which is what makes black-box attacks practical and secrecy no defence.
- **Physical-world attacks** (patches, objects) work through sensors and bypass input-side defences entirely.
- **Adversarial attacks happen at inference against a clean model; poisoning happens at training and corrupts the model itself.**
- **Label flipping:** 3% of labels destroys a class while overall accuracy falls 2–4%. **Backdoors:** 1% poisoning gives 99.5% attack success while all clean metrics stay normal.
- **Adversarial defences:** statistical detection, input transformation (feature squeezing), **adversarial training** (most effective, 10–40× cost), loss regularization, detector networks, DDPM purification, ensembles.
- **Poisoning defences:** anomaly detection (Z-scores, clustering, autoencoders), sanitization and lineage, robust losses (Huber), regularization, augmentation, **secure data sourcing**.
- **No single defence suffices** — poisoning in particular requires a multifaceted, pipeline-wide approach.

## ⚠️ Important Notes

**Backdoored models pass every standard test.** Clean accuracy is unaffected, so quality gates, model tests, and validation metrics all report health. Only the trigger reveals it, and you do not know the trigger.

**Always report per-class metrics.** Label flipping drops one class from 92% to 11% while overall accuracy moves 2–4% — invisible in aggregate.

**Keeping model weights secret is not a defence.** Adversarial examples transfer, so a surrogate model suffices for a black-box attack.

**Returning full confidence vectors enables model extraction and membership inference.** Return the minimum information the application requires.

**Adversarial training is threat-model-specific.** Robustness to $L_\infty$ FGSM at one $\epsilon$ does not confer robustness to $L_2$ attacks, larger budgets, or physical patches.

**Adversarial training costs 10–40× training time and some clean accuracy.** Justified in safety-critical settings, over-engineering elsewhere.

**Input-side defences cannot stop physical-world attacks.** The perturbation exists in the world; the sensor records it faithfully.

**Autoencoder anomaly detection requires trusted clean data to train on.** If the whole pipeline is compromised, there is no anchor.

**Continuous and online learning are direct attack surfaces.** Incremental poisoning shifts behaviour gradually without tripping detection — the reason [[10 - Monitoring and Drift]] rejects continuous learning for adversarial domains.

**Data lineage is a security control, not just a governance one.** Without provenance you cannot determine which source poisoned you, or which models are affected.

**Pretrained third-party models carry inherited risk.** Fine-tuning does not remove a backdoor, and weights cannot be audited for an unknown trigger.

**Most published adversarial defences have been broken by adaptive attacks.** Assume a defence evaluated only against non-adaptive attacks will fail against one designed for it.

**Rate limiting is an underrated defence.** Black-box and extraction attacks need many queries; throttling raises their cost substantially.

> [!warning] Gaps in the source slides
> LaTeX Beamer; the mathematical content extracted unusually well for this course, but figures are images:
> - **Slides 3, 15, 22, 31** produced no text — section dividers.
> - **Slide 11** — the downstream transfer attack figure.
> - **Slide 12** — the **traffic sign mock-ups with adversarial patches** figure; only the caption survived.
> - **Slide 13 — "Adversarial Attacks"** is title-only.
> - **Slides 16, 17, 21** — the mismatched image–text pair example, **"Impact of Data Poisoning"** (an entire slide, image-only), and the incremental poisoning figure.
> - **Slides 23, 24, 26, 27, 35** — the KS test figure, **feature squeezing** figure, the **adversarial training code implementation**, the **bit plane feature consistency** figure, and the K-means figure.
> - **Slide 9's EAD description truncates at "balances"** — the elastic net's $L_1$/$L_2$ balance is inferred.
> - **Slide 20's backdoor example truncates at "test inpu"**.
> - **Slide 14** points to a [Neptune.ai FGSM tutorial](https://neptune.ai/blog/adversarial-attacks-on-neural-networks-exploring-the-fast-gradient-sign-method) rather than showing code.
> - **PGD (Projected Gradient Descent) is named on slide 10** as an attack to use, but **never defined anywhere in the deck** — despite being the standard strong white-box attack and the basis of most adversarial training. A notable gap.
>
> **References:** Vijay J., *Machine Learning Systems*, [mlsysbook.ai](https://mlsysbook.ai/book/) · **Costa, Joana C., et al., *How deep learning sees the world: A survey on adversarial attacks & defenses*, IEEE Access 12 (2024): 61113–61136** — the survey this lecture follows closely.

---
**Previous:** [[10 - Monitoring and Drift]] · **Back to** [[00-Index]]
