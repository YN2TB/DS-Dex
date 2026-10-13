---
subject: MLOps
chapter: 11
tags: [ds, mlops, adversarial-attacks, data-poisoning, security, robustness]
source: "MLOPs_RobustAI.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Robust AI

[[10 - Monitoring and Drift]] dealt with failures caused by a changing world; this chapter deals with failures caused by an adversary who wants the model to fail.

## 📘 Main Knowledge

ML systems add attack surfaces beyond traditional software:

| Level | Vulnerabilities |
|---|---|
| data | poisoned training data; biased or low-quality labels; drift |
| model | adversarial examples; model inversion and membership inference; model extraction |
| system | insecure APIs; excessive output information; weak monitoring and logging |

**Inversion** recovers training data, **membership inference** tells whether a record was in the training set (a privacy breach), **extraction** copies the model by querying it. Returning full confidence vectors instead of labels makes all three easier.

### Adversarial attacks

Small, carefully designed perturbations, imperceptible to humans, that cause misclassification by exploiting how neural networks learn.

- **White-box**: the attacker knows architecture, weights, maybe training data, and sees raw outputs. Gradients are available.
- **Black-box**: inference access only.

**FGSM** (fast gradient sign method), white-box, one step:
$$x_{adv}=x+\epsilon\cdot\operatorname{sign}\big(\nabla_x\mathcal L(\theta,x,y)\big)$$
Training uses $\nabla_\theta\mathcal L$ to update weights; FGSM uses $\nabla_x\mathcal L$ to update the input, at the cost of one forward and backward pass. The sign moves every pixel by exactly ε (an $L_\infty$ budget). Fast, needs gradients, often imperceptible.

**Optimization-based attacks** find the smallest perturbation that changes the prediction:
$$\min_\delta\|\delta\|_p\quad\text{s.t. } f_\theta(x+\delta)\ne y,\ x+\delta\in\mathcal X$$
Stronger and harder to detect, but expensive.
- **L-BFGS**: $\min\|\delta\|_2$ with $x+\delta\in[0,1]^n$, solved by quasi-Newton.
- **Carlini & Wagner**: $\min_\delta\|\delta\|_p+c\cdot\mathcal L(x+\delta,y)$ with $\mathcal L(x',y)=\max\big(Z(x')_y-\max_{i\ne y}Z(x')_i,\,-\kappa\big)$ on the logits $Z$. Minimizing it pushes the best wrong-class logit above the true one; κ sets how far past the boundary (higher κ transfers better).
- **EAD** (elastic-net attack): $\min_\delta \beta\|\delta\|_1+\|\delta\|_2^2+c\cdot\mathcal L(x+\delta,y)$ with $x+\delta\in[0,1]^n$, balancing sparsity and size of the perturbation.

**Transfer attacks** (black-box): craft examples on a surrogate model you control (FGSM, PGD, C&W) and apply them to the target. Examples often transfer across architectures, so keeping weights secret is no defence.

**Physical-world attacks**: adversarial patches or objects that fool models through cameras, e.g. a stop sign read as a speed-limit sign. They must survive changes in distance, angle and light.

### Data poisoning

Malicious data injected into the training pipeline changes model behaviour in ways standard validation misses (e.g. mismatched image–text pairs).

| | Adversarial attack | Data poisoning |
|---|---|---|
| When | after training | before or during training |
| Target | inference inputs | training data |
| Mechanism | small crafted noise | malicious or corrupted samples |
| Where | inference stage | upstream: collection, labeling, ingestion |
| Goal | misclassify a test input | corrupt the learned model |

Stages: injection → training (boundaries shift) → deployment (attacker exploits the model).

- **Label flipping**: flipping 3% of CIFAR-10 labels cut the target class's accuracy from 92% to 11% while overall accuracy fell only 2–4%.
- **Backdoors**: training samples with a trigger pattern; with triggers in 1% of the data, attacks on triggered inputs succeeded 99.5% of the time. The model behaves normally on clean data.
- **Incremental poisoning**: gradual injection into online learning streams.

### Defences against adversarial examples

- **Statistical detection**: compare inputs with a reference distribution (KS, Anderson–Darling).
- **Input transformation**: dimensionality reduction or discretization removes tiny perturbations (feature squeezing, e.g. lower colour bit depth).
- **Adversarial training**: each batch mixes original and adversarial images. Formally
$$\min_\theta\ \mathbb E\Big[\max_{\|\delta\|_\infty\le\epsilon}\mathcal L(\theta,x+\delta,y)\Big].$$
- **Modified training**: bit-plane feature consistency adds a regularizer comparing originals with manipulated versions.
- **Detector networks** before the classifier; suspicious inputs go to human review.
- **Purification** with a diffusion model (DDPM): add noise for some steps, then denoise for the same number, pulling the image back towards natural images.
- **Ensembles**: an attack that fools one model may not fool others; diversify preprocessing and features.

### Defences against poisoning

- **Anomaly detection**: z-scores $z=(x-\mu)/\sigma$; clustering (poisoned points form separate or distant clusters, e.g. K-means); **autoencoders** trained on clean data, flagging high reconstruction error.
- **Sanitization**: cleaning (deduplication, imputation, outlier removal), validation, and **provenance/lineage** ([[03 - Data in MLOps]]), which shows which source introduced bad data and which models used it.
- **Robust training**: robust losses such as **Huber**,
$$L_\delta(y,\hat y)=\begin{cases}\tfrac12(y-\hat y)^2 & |y-\hat y|\le\delta\\ \delta\big(|y-\hat y|-\tfrac12\delta\big) & \text{otherwise}\end{cases}$$
quadratic near zero and linear in the tails, so one bad point's gradient is capped at δ; plus $L_1$/$L_2$ regularization, which leaves less capacity to memorize poison.
- **Augmentation**: random transformations reduce sensitivity to specific patterns, and can break a small trigger.
- **Secure sourcing**: collection protocols, verified sources, quality assessments, governance, least-privilege access, logged access.

Poisoning needs all of these together, and remains an active research area.

## ✏️ Exercises

**1.** Explain the FGSM formula. Why are the perturbations imperceptible yet effective?

> [!example]- Solution
> $\nabla_x\mathcal L$ says which way each pixel should move to increase the loss; the sign keeps only the direction, so each pixel changes by ±ε. With 8-bit images and ε = 8/255, no pixel moves more than 3.1% of its range.
> A 224×224×3 image has 150,528 dimensions. The $L_\infty$ size stays ε, but the $L_2$ size is $\epsilon\sqrt{150528}\approx388\epsilon$: invisible per pixel, large in aggregate, and in the worst direction. Decision boundaries lie close to natural data in high dimensions, so a small, well-aimed step crosses one. Using the sign rather than the raw gradient spreads the budget evenly instead of making a visible local artefact. This is a property of differentiable classifiers in high dimensions, not a bug in one model.

**2.** Compare adversarial attacks and data poisoning. Why do their defences differ?

> [!example]- Solution
> In an adversarial attack the model is clean and the request is malicious, so defences sit at serving time (detection, transformation, purification) or make the model tolerant (adversarial training, ensembles).
> In poisoning the requests are normal and the weights are compromised. Input filtering can't help, and backdoors leave validation metrics intact, so the 1%-poison backdoor passes every CI test ([[09 - CI-CD with GitHub Actions]]). The fix is retraining on clean data, which requires knowing which data was clean. Defences are preventive and in the pipeline: anomaly detection at ingestion, sanitization, robust losses, secure sourcing, and lineage to trace the source and affected models.

**3.** What is a backdoor attack, and why does standard validation miss it?

> [!example]- Solution
> Training samples carry a trigger (a small patch, a phrase) with the attacker's label, and the model learns "trigger → that class". It effectively learns two functions: the correct one on clean inputs (99% of its training data) and the attacker's on triggered ones. The test set has no triggers, so accuracy, per-class metrics and the quality gate all look normal.
> Label flipping, by contrast, shows up in a per-class breakdown (92% → 11%) even though overall accuracy moves 2–4%.
> What helps: anomaly detection at ingestion (triggers are artificial), augmentation (crops and jitter can destroy a trigger), verified data sources, and activation clustering (backdoored samples cluster separately inside the network). Scraped or crowdsourced data is a supply-chain risk.

**4.** Explain adversarial training and its costs. Why is it considered the most effective defence?

> [!example]- Solution
> Generate adversarial examples (FGSM, PGD) during training and train on mixed batches, solving the min–max problem above. It changes the decision boundary itself, moving it away from the data, while detectors, transformations and purification are separate components an adaptive attacker can target.
> Costs: a k-step PGD attack makes each batch roughly k+1 times as expensive (7–40 steps ⇒ about 8–41×); clean accuracy usually drops a few points; robustness is specific to the threat model it was trained on ($L_\infty$ at one ε says little about $L_2$, larger ε or physical patches); and it does nothing against poisoning. Worth it for safety-critical, adversarial settings (driving, moderation, fraud), not for a house-price API. Combine with diverse ensembles and a detector that routes suspicious inputs to people.

**5.** (Advanced) Design defence in depth for a system facing both attack types. What can't be defended?

> [!example]- Solution
> | Stage | Controls |
> |---|---|
> | acquisition | verified sources, least-privilege write access, logging, lineage per sample |
> | ingestion | z-scores, clustering, autoencoder on a trusted clean subset; sanitization; per-class label distribution checks |
> | training | Huber loss, regularization, augmentation; adversarial training if justified |
> | validation | per-class and subgroup metrics, activation clustering, a holdout with independent provenance |
> | serving | feature squeezing, detector network with human review, diverse ensemble, return labels not confidence vectors, rate limiting |
> | monitoring | input drift, prediction distribution, per-client query rates |
>
> Hard or impossible to defend:
> 1. Adaptive attacks: many published defences were broken by attacks designed around them; only adversarial training has held up, within its threat model.
> 2. Physical attacks: the patch is really there, and the camera records it faithfully.
> 3. Insiders with pipeline access can inject statistically normal samples gradually.
> 4. Backdoors in third-party pretrained models survive fine-tuning and can't be found without knowing the trigger.
> 5. Every defence that needs trusted clean data fails if the whole pipeline is compromised.
>
> The realistic goal is to raise the attacker's cost and manage the risk continuously, like the model-risk framework in [[06 - Deployment]].

## 📝 Summary

- ML adds attack surfaces at the data, model and system levels.
- White-box attackers have gradients; black-box attackers only query.
- FGSM: one signed input-gradient step; C&W and L-BFGS find minimal perturbations at higher cost.
- Adversarial examples transfer, so secrecy is not a defence; physical patches work through sensors.
- Adversarial attacks hit inference with a clean model; poisoning corrupts the model during training.
- Label flipping: 3% of labels can destroy a class while overall accuracy drops 2–4%; backdoors: 1% poison, 99.5% success, normal clean metrics.
- Adversarial defences: detection, input transformation, adversarial training, detectors, purification, ensembles.
- Poisoning defences: anomaly detection, sanitization and lineage, robust losses, augmentation, secure sourcing.

## ⚠️ Important Notes

1. Backdoored models pass every standard test.
2. Report per-class metrics.
3. Secret weights don't stop transfer attacks.
4. Full confidence vectors enable extraction and membership inference.
5. Adversarial training protects only against its own threat model.
6. It costs roughly k+1 times the training compute for k-step PGD, plus some clean accuracy.
7. Input-side defences can't stop physical attacks.
8. Autoencoder detection needs trusted clean data.
9. Online and continuous learning are attack surfaces.
10. Lineage is a security control.
11. Pretrained models can carry backdoors.
12. Assume defences tested only on non-adaptive attacks will fail.
13. Rate limiting raises the cost of black-box attacks.

> [!warning] Gaps in the source slides
> - Slides 3, 15, 22, 31 have no text; slide 13 has only a title. Figures only: 11 (transfer attack), 12 (traffic signs with patches), 16 (image–text example), 17 ("Impact of Data Poisoning"), 21 (incremental poisoning), 23 (KS), 24 (feature squeezing), 26 (adversarial training code), 27 (bit-plane consistency), 35 (K-means).
> - Truncated: slide 20 (backdoor example).
> - Slide 14 links a Neptune.ai FGSM tutorial instead of code.
> - **PGD** is named on slide 10 but never defined. It repeats FGSM-style steps of size α and projects back into the ε-ball each time: $x^{t+1}=\Pi_{\|x'-x\|_\infty\le\epsilon}\big(x^t+\alpha\,\operatorname{sign}(\nabla_x\mathcal L)\big)$ (added, standard definition).
> - Erratum (slide 9): the slide prints the C&W loss as $\max(\max_{i\ne y}Z_i-Z_y,-\kappa)$. That is the paper's *targeted* loss (with $y$ as the target class); minimizing it with $y$ the true label would make the true class win. For the untargeted attack in the slide's constraint $f_\theta(x+\delta)\ne y$, the loss is $\max(Z_y-\max_{i\ne y}Z_i,-\kappa)$, as written above.
> - References: Vijay J., *Machine Learning Systems* (mlsysbook.ai); Costa et al., "How deep learning sees the world", *IEEE Access* 12 (2024): 61113–61136.

**Previous:** [[10 - Monitoring and Drift]] · **Back to** [[00-Index]]
