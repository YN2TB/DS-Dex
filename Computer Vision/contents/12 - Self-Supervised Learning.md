---
subject: Computer Vision
chapter: 12
tags: [ds, computer-vision, self-supervised, contrastive-learning, infonce, simclr, moco, byol, mae, clip]
source: "Szeliski, *Computer Vision*, 2nd ed. §5.4.7; Oord et al. 2018 (InfoNCE/CPC); Chen et al. 2020 (SimCLR); He et al. 2020 (MoCo); Grill et al. 2020 (BYOL); Chen & He 2021 (SimSiam); He et al. 2022 (MAE); Radford et al. 2021 (CLIP); the lecturer's course outline"
---

# Self-Supervised Learning

**Week 12 of 14. ⚠️ NO SLIDES** — see [[00-Index]].

**Four results.**

**§3 — ⚠️ InfoNCE CANNOT CERTIFY MORE THAN $\log N$ NATS OF MUTUAL INFORMATION, SO *BATCH SIZE IS A HARD INFORMATION CEILING*.** A batch of 256 caps at **5.5452 nats = exactly 8 bits**, while **one ImageNet label carries $\log_2 1000 = 9.97$ bits** ⇒ ***a batch of 256 is worth 0.8 class labels per example.*** **That single inequality explains why SimCLR needed batch 4096 and why MoCo built a 65,536-entry queue — they are two answers to one bound.** And the loss at initialization is **exactly $\log N$** (verified to $10^{-12}$), which makes it the best diagnostic in the method.

**§4 — ⚠️ COLLAPSE IS THE *GLOBAL OPTIMUM* OF THE NON-CONTRASTIVE OBJECTIVE, NOT A BAD LOCAL MINIMUM.** A constant output scores cosine **1.000000** — the lowest possible loss, reachable from any input. ⇒ ***the loss alone cannot prevent collapse; only the architecture can*** (stop-gradient, predictor, EMA target). **General rule: when a degenerate solution is a global optimum, no amount of training or tuning helps.**

**§5 — ⚠️ MAE's 75% MASK RATE IS AN EFFICIENCY ARGUMENT BEFORE IT IS A DIFFICULTY ONE.** The encoder sees **49 of 196 tokens**, so **attention cost falls 16× and the linear terms 4×** — *it trains fast **despite** reconstructing pixels, because the expensive encoder never sees the masked patches at all.*

**§6 — ⚠️ CLIP RECOVERS [[03 - Image Classification and Linear Models|ch. 03]]'S LINEAR CLASSIFIER EXACTLY — THE TEXT EMBEDDINGS *ARE* THE ROWS OF $\mathbf W$.** It learned them from language instead of from labelled data, which is why adding a class costs one forward pass instead of a retrained head.

## 📘 Main Knowledge

### 1. The label bottleneck is the motivation, and it is not about money

| dataset | labelled images |
|---|---|
| CIFAR-10 | 60,000 |
| ImageNet-1k | 1,281,167 |
| ImageNet-21k | 14,197,122 |
| JFT-300M | 300,000,000 |

| seconds per label | ImageNet-1k | person-days (8 h) |
|---|---|---|
| 1 | 355.9 h | 44.5 |
| 5 | 1,779.4 h | 222.4 |
| 10 | 3,558.8 h | 444.8 |

**ImageNet is expensive but achievable.** ⚠️ **The problem is what [[06 - Vision Transformers|ch. 06]] §5 measured: a ViT needs $10^7$–$10^8$ images to beat a CNN.** *At that scale labelling is not expensive, it is impossible* — and **unlabelled images are effectively free and effectively infinite.**

⇒ **the question is not "how do we label more" but "what can we learn without labels, and how much of the supervised performance does it buy".** *Self-supervision is the answer that turned out to work, and [[13 - Generative Models|ch. 13]]'s models are trained the same way.*

### 2. Pretext tasks: manufacture the label from the input

| pretext task | label source | chance |
|---|---|---|
| rotation (RotNet) | the rotation **you** applied | 25% |
| jigsaw $3\times3$ | the permutation **you** applied | $2.76\times10^{-6}$ |
| relative patch position | which of 8 neighbours | 12.5% |
| colourisation | the colour **you** removed | (regression) |
| inpainting | the pixels **you** masked | (regression) |

**The common structure: apply a known transformation, then ask the network to name it. The label is free because you generated it.**

*(Jigsaw's full space is $9!=362{,}880$ permutations — unusable as a classification target, so Noroozi & Favaro use a chosen subset of 1,000 with large mutual Hamming distance.)*

> [!warning] ⚠️ A PRETEXT TASK IS ONLY AS GOOD AS THE SHORTCUT IT *FAILS* TO ADMIT
> Every one of these can be solved without understanding the image:
>
> | task | the shortcut |
> |---|---|
> | jigsaw | match **chromatic aberration** or edge continuity at the tile borders |
> | rotation | find the sky; or read the text |
> | inpainting | copy neighbouring texture |
>
> **A network that finds the shortcut solves the pretext task perfectly and learns nothing transferable.** *This is why the original jigsaw paper jitters tile positions and randomly drops colour channels — countermeasures against a specific shortcut, not against misunderstanding.*
>
> ⇒ ***hand-designed pretext tasks were displaced because designing them is really the adversarial exercise of anticipating shortcuts*** — and the successors (contrastive, masked modelling) define the task by *augmentation* and *masking* instead, which is a much larger and harder-to-shortcut space.

### 3. ⚠️ Contrastive learning, and the $\log N$ ceiling

**The idea: two augmentations of one image should agree; different images should not.** With one positive and $N-1$ negatives, the **InfoNCE** loss is

$$L=-\log\frac{\exp(s^+/\tau)}{\sum_{j}\exp(s_j/\tau)}$$

which is a softmax cross-entropy over "which of these $N$ is my positive" — *[[03 - Image Classification and Linear Models|ch. 03]] §6's loss with the classes redefined.*

> [!warning] ⚠️ Oord et al.'s BOUND: $I(x;y)\ \ge\ \log N - L$ — SO $\log N$ IS A CEILING
> **The mutual information the objective can certify is capped at $\log N$, whatever the model does.**
>
> | batch $N$ | $\log N$ (nats) | bits |
> |---|---|---|
> | 32 | 3.4657 | 5 |
> | **256** | **5.5452** | **8** |
> | 1,024 | 6.9315 | 10 |
> | 4,096 | 8.3178 | 12 |
> | 65,536 | 11.0904 | 16 |
>
> **One ImageNet label carries $\log_2 1000 = 9.97$ bits.** ⇒ ***a batch of 256 is information-theoretically worth 0.8 class labels per example*** — **which is exactly why batch size stopped being an implementation detail and became the central design problem.**
>
> **The two families are two answers to this one bound:**
>
> | | strategy | negatives |
> |---|---|---|
> | **SimCLR** | make the **batch** bigger | 4,096 — needing 128 TPU cores |
> | **MoCo** | keep a **queue** of past keys | **65,536 at batch 256 — 256× more negatives than the batch** |
>
> **MoCo's queue decouples the number of negatives from the batch size**, and *that decoupling is why it needs a momentum encoder*: queued keys were computed by an older network, and the EMA keeps them consistent enough to compare.

> [!note] ⚠️ The most useful diagnostic number in the method
> **At initialization all scores are equal, so $L=\log N$ exactly** — verified: $N=256$ gives $L=5.545177$ against $\log 256=5.545177$; $N=4096$ gives $8.317766$ both ways.
>
> ⇒ ***a contrastive loss sitting at $\log N$ has learned nothing, and you can tell at a glance instead of waiting for a linear probe.*** **Always print $\log N$ next to the loss.**

**Augmentation choice is not cosmetic here** — it *defines* the task, by declaring what the representation must be invariant to. **SimCLR's ablation found random crop plus colour jitter essential together**: without colour jitter, matching two crops by their colour histogram is a shortcut. *§2's lesson, recurring in the method that replaced §2.*

### 4. ⚠️ Non-contrastive methods, and why collapse is a theorem

**BYOL and SimSiam drop negatives entirely** and just maximize agreement between two views: $L=-\cos\big(f(v_1),f(v_2)\big)$.

> [!warning] ⚠️ THE CONSTANT FUNCTION IS A **GLOBAL MINIMUM** OF THAT OBJECTIVE
> | representation | mean $\cos(v_1,v_2)$ | loss |
> |---|---|---|
> | informative (two real views) | 0.304556 | −0.304556 |
> | **collapsed (constant output)** | **1.000000** | **−1.000000** |
>
> **The collapsed solution attains the lowest possible loss and is reachable from any input.** ⇒ ***it is not a bad local minimum to be escaped with a better schedule — it is the global optimum of the stated objective.***
>
> **So the loss alone cannot prevent collapse. What prevents it is architectural:**
>
> | mechanism | method |
> |---|---|
> | **predictor head on one branch only** (breaks symmetry) | BYOL, SimSiam |
> | **stop-gradient on the target branch** | **SimSiam — this is *the* ingredient** |
> | EMA / momentum target encoder | BYOL |
> | an explicit anti-collapse **term** | Barlow Twins, VICReg (decorrelate dimensions; floor the variance) |
>
> **Contrastive methods avoid the problem by construction**: negatives make the constant solution *maximally* bad, because every negative also scores cosine 1.
>
> ⇒ ***the general lesson, and it is worth carrying everywhere: when a degenerate solution is a GLOBAL optimum of your objective, no amount of training, tuning or data fixes it. The objective or the architecture must change.*** *Same class of reasoning as [[03 - Image Classification and Linear Models|ch. 03]] §5 — "no linear model can score an image and its negative highly at once" is a property of the model class, not of the training.*

### 5. ⚠️ Masked image modelling

**MAE (He et al. 2022): mask most patches, encode only the visible ones, and let a lightweight decoder reconstruct the rest.** A $224^2$ image at patch 16 gives $n=196$ tokens.

| mask rate | visible | attention $n^2$ | vs full | encoder linear |
|---|---|---|---|---|
| 0% | 196 | 38,416 | 1.00× | 1.00× |
| 50% | 98 | 9,604 | 4.00× | 2.00× |
| **75%** | **49** | **2,401** | **16.00×** | **4.00×** |
| 90% | 20 | 400 | 96.04× | 9.80× |

> [!warning] ⚠️ THE ASYMMETRY IS THE WHOLE DESIGN
> **The encoder never sees the masked patches** — unlike BERT, which feeds `[MASK]` tokens through the full model. **At 75% masking the encoder processes a quarter of the sequence, so attention costs 16× less.** ⇒ ***MAE trains fast **despite** reconstructing pixels, and the decoder can be lightweight because it is discarded after pre-training.***
>
> ⚠️ **And why 75% in vision when 15% is right for text**: **images are spatially redundant.** A word is nearly irreplaceable; a patch is usually interpolable from its neighbours. **The mask must be aggressive enough that interpolation is not a shortcut** — *§2's test, a third time, now setting a hyperparameter.* *([[11 - Video and Motion|Ch. 11]] §1 measured the temporal version of the same redundancy: 3.33 px between frames.)*

### 6. ⚠️ CLIP — language as the supervision signal

**400M (image, text) pairs scraped from the web, no manual annotation.** The objective is contrastive over a batch: match each image to *its* caption among $N$. **CLIP's $N=32{,}768$ certifies up to $\log N=10.3972$ nats $=15.00$ bits** — and *a caption carries far more than a class index, naming objects, attributes, relations and context in open vocabulary.*

> [!warning] ⚠️ CLIP RECOVERS [[03 - Image Classification and Linear Models|ch. 03]]'S LINEAR CLASSIFIER — THE TEXT EMBEDDINGS **ARE** THE ROWS OF $\mathbf W$
> | | the classifier |
> |---|---|
> | supervised ([[03 - Image Classification and Linear Models|ch. 03]]) | fixed $K$ classes; $\mathbf W$ is $K\times D$, **learned from labelled images** |
> | **CLIP** | a class **is an encoded sentence**; the text embeddings **are** $\mathbf W$'s rows |
>
> **Scoring is still $\mathbf W\mathbf x$ — nothing about the classification changed. What changed is where $\mathbf W$'s rows came from.**
>
> ⇒ ***adding a class costs one forward pass of a text encoder, not a retrained head*** — which is exactly what "zero-shot" means here, and it is a structural change, not an accuracy improvement.

> [!note] The honest limits
> **Zero-shot performance tracks how well a concept is represented on the web**, so it is strong on common objects and weak on fine-grained, technical and rare categories. **The 400M pairs are unaudited**, so whatever the web associates with a word is inherited. **And prompt wording changes the result** — "a photo of a {}" beats the bare class name — *which is [[08 - Object Detection II|ch. 08]]'s "name the protocol" appearing in a new place: the reported number depends on a choice that is rarely reported.*

### 7. How self-supervision is actually evaluated

| protocol | what is trained | what it measures |
|---|---|---|
| **linear probe** | a linear classifier on **frozen** features | how *linearly separable* the representation is |
| **fine-tuning** | the whole network | how good an **initialization** it is |
| **$k$-NN / low-shot** | nothing (or very little) | quality with almost no labels |

⚠️ **These disagree, and the disagreement is informative**: MAE's linear probe is comparatively weak while its fine-tuning is excellent, because **reconstruction produces features that are rich but not linearly organized**. *Reporting only one protocol picks a winner by choosing the ruler — [[08 - Object Detection II|ch. 08]] §1's AP-convention finding again, in a different metric family.*

## ✏️ Exercises

> [!example]- Exercise 1 — the $\log N$ ceiling
> **(a)** Maximum MI certifiable at $N=256$ and $N=65{,}536$, in nats and bits. **(b)** Compare to one ImageNet label. **(c)** What are SimCLR's and MoCo's answers? **(d)** What is $L$ at initialization, and why does that matter?
>
> ---
> **(a)** $\log 256=\mathbf{5.5452}$ nats $=\mathbf{8}$ bits; $\log 65{,}536=\mathbf{11.0904}$ nats $=\mathbf{16}$ bits.
>
> **(b)** An ImageNet label carries $\log_2 1000=\mathbf{9.97}$ bits ⇒ **a batch of 256 is worth 0.8 labels per example.** ⚠️ **That is why batch size became the central design problem** rather than an implementation detail.
>
> **(c)** **SimCLR enlarges the batch** (4,096, needing 128 TPU cores). **MoCo keeps a queue** — 65,536 negatives at batch 256, **256× more than the batch**, decoupling the two. *The queue is why MoCo needs a momentum encoder: old keys were computed by an older network.*
>
> **(d)** ⚠️ **Exactly $\log N$** — all scores equal at init (verified to $10^{-12}$). ⇒ **a loss sitting at $\log N$ has learned nothing, visible at a glance instead of after a linear probe. Always print $\log N$ beside the loss.**

> [!example]- Exercise 2 — why BYOL should collapse
> **(a)** What loss does a constant $f$ achieve? **(b)** Is it a local or global optimum? **(c)** Name three mechanisms that prevent it. **(d)** Why is contrastive learning immune? **(e)** State the general lesson.
>
> ---
> **(a)** $\cos=\mathbf{1.000000}$ ⇒ $L=-1$, **the lowest attainable value.**
>
> **(b)** ⚠️ **Global.** It is not a bad local minimum — it is *the* optimum of the stated objective, reachable from any input.
>
> **(c)** **Stop-gradient on the target branch** (SimSiam's essential ingredient); a **predictor head on one branch only**; an **EMA target encoder** (BYOL). Or an explicit anti-collapse term (Barlow Twins, VICReg).
>
> **(d)** **Negatives make the constant solution maximally bad**: if every embedding is identical, every *negative* also scores 1, so the loss is maximized rather than minimized.
>
> **(e)** ⚠️ ***When a degenerate solution is a global optimum, no amount of training, tuning or data fixes it — the objective or the architecture must change.*** *Same reasoning as [[03 - Image Classification and Linear Models|ch. 03]] §5's proof about linear models: a property of the formulation, not of the optimization.*

> [!example]- Exercise 3 — MAE's mask rate
> $224^2$, patch 16. **(a)** Tokens; visible at 75%. **(b)** Attention and linear cost vs unmasked. **(c)** Why is MAE fast despite reconstructing pixels? **(d)** Why 75% here and 15% in BERT?
>
> ---
> **(a)** $n=(224/16)^2=\mathbf{196}$; visible $=\mathbf{49}$.
>
> **(b)** Attention $\propto n^2$: $2{,}401$ vs $38{,}416$ ⇒ **16.00× cheaper**; linear terms $\propto n$ ⇒ **4.00×**.
>
> **(c)** ⚠️ **Because the encoder never sees the masked patches at all** — unlike BERT, which pushes `[MASK]` tokens through the full model. **The heavy encoder runs on a quarter of the sequence and the decoder is lightweight and discarded.**
>
> **(d)** ⚠️ **Images are spatially redundant; text is not.** A patch is usually interpolable from its neighbours, a word rarely is. **The mask must be aggressive enough that interpolation is not a shortcut** — the same "what shortcut does the task admit" test that governs pretext design.

> [!example]- Exercise 4 — CLIP and ch. 03
> **(a)** How does CLIP classify into a new set of classes? **(b)** In what sense is this still [[03 - Image Classification and Linear Models|ch. 03]]'s linear classifier? **(c)** What exactly changed? **(d)** Three honest limits.
>
> ---
> **(a)** Encode each class *name* as a sentence with the text encoder; score the image embedding against each. **No training.**
>
> **(b)** ⚠️ **The scoring is still $\mathbf W\mathbf x$ — the text embeddings *are* the rows of $\mathbf W$.** Nothing about the classification changed.
>
> **(c)** **Where $\mathbf W$'s rows came from**: learned from *language* rather than from labelled images ⇒ **a new class costs one forward pass of a text encoder, not a retrained head.** *A structural change, not an accuracy improvement.*
>
> **(d)** Performance tracks **web representation** (strong on common objects, weak on fine-grained and rare ones); **the 400M pairs are unaudited**, so web associations are inherited; **prompt wording changes results** — [[08 - Object Detection II|ch. 08]]'s "name the protocol", in a new place.

> [!example]- Exercise 5 — designing a pretext task
> **(a)** Chance accuracy for rotation and $3\times3$ jigsaw. **(b)** Why does jigsaw use 1,000 permutations, not $9!$? **(c)** Give a shortcut for each of rotation, jigsaw, inpainting. **(d)** What replaced hand-designed pretext tasks, and why?
>
> ---
> **(a)** Rotation **25%** (4-way); jigsaw $1/9!=\mathbf{2.76\times10^{-6}}$.
>
> **(b)** $9!=\mathbf{362{,}880}$ classes is unusable as a softmax target; the paper selects **1,000 permutations with large mutual Hamming distance** so the classes are well separated.
>
> **(c)** Rotation → **find the sky, or read the text**. Jigsaw → **match chromatic aberration or edge continuity at tile borders**. Inpainting → **copy neighbouring texture**. ⚠️ **Each is solvable without understanding the image**, and a network that finds the shortcut learns nothing transferable.
>
> **(d)** **Contrastive learning and masked modelling.** ⇒ ***designing a pretext task is really the adversarial exercise of anticipating shortcuts***, and defining the task by augmentation or masking spans a far larger, harder-to-shortcut space. *Note the shortcut problem does not disappear — SimCLR's colour jitter exists because matching crops by colour histogram is one.*

## 📝 Summary

- **The motivation is that labelling does not scale to where the models need to be**: ImageNet-1k is ~222 person-days at 5 s/label, and [[06 - Vision Transformers|ch. 06]] showed ViTs need $10^7$–$10^8$ images. **Unlabelled images are free and effectively infinite.**
- **Pretext tasks manufacture the label from the input** (rotation, jigsaw, inpainting, colourisation). ⚠️ **They are only as good as the shortcuts they fail to admit** — chromatic aberration solves jigsaw, the sky solves rotation — **and designing them is really the adversarial exercise of anticipating shortcuts**, which is why they were displaced.
- **⚠️ InfoNCE certifies at most $\log N$ nats of mutual information.** $N=256$ → **5.5452 nats = 8 bits**, against an ImageNet label's **9.97 bits** ⇒ **a batch of 256 is worth 0.8 labels per example.** **SimCLR enlarges the batch (4,096); MoCo queues 65,536 negatives at batch 256 — 256× the batch — and therefore needs a momentum encoder.**
- **⚠️ $L=\log N$ exactly at initialization** (verified to $10^{-12}$) ⇒ **a contrastive loss still at $\log N$ has learned nothing. Print $\log N$ beside the loss.**
- **⚠️ Collapse is the *global* optimum of the non-contrastive objective** — a constant output scores cosine **1.000000**, the lowest possible loss. ⇒ **the loss cannot prevent it; only architecture can** (stop-gradient, predictor, EMA, or an explicit anti-collapse term). **Contrastive methods are immune by construction.**
- **⚠️ MAE masks 75%: the encoder sees 49 of 196 tokens, so attention costs 16× less and the linear terms 4× less** — **it is fast *because* the encoder never sees the masked patches**, unlike BERT. **75% works in vision and 15% in text because images are spatially redundant** and the mask must defeat interpolation.
- **⚠️ CLIP recovers [[03 - Image Classification and Linear Models|ch. 03]]'s linear classifier exactly — the text embeddings *are* $\mathbf W$'s rows**, learned from language instead of labels. **A new class costs one text-encoder pass, not a retrained head.** Limits: web representation, unaudited data, prompt sensitivity.
- **Evaluation protocols disagree informatively**: MAE's linear probe is weak and its fine-tuning excellent, because reconstruction gives **rich but not linearly organized** features. **Reporting one protocol picks the winner by choosing the ruler.**

## ⚠️ Important Notes

1. **⚠️ Print $\log N$ next to your contrastive loss.** It is the initialization value and the certifiable ceiling. **A loss near $\log N$ means no learning; a loss near 0 with a small $N$ means the task is too easy, not that the model is good.**
2. **⚠️ Batch size is a hyperparameter with an information-theoretic meaning here**, unlike in supervised training where it mostly affects optimization. **Halving the batch halves the certifiable MI in bits by one.**
3. **⚠️ Never conclude "no collapse" from a falling loss.** In non-contrastive methods **the collapsed solution has the *lowest* loss.** **Monitor the representation directly** — the standard deviation of the embeddings across a batch, or the rank/eigenspectrum of their covariance.
4. **⚠️ The augmentation set defines the task.** It declares what the representation must be invariant to — **so an augmentation that destroys information your downstream task needs will cost you, and no loss curve will show it.** Colour jitter is wrong for a task where colour is the label.
5. **⚠️ Report the evaluation protocol.** Linear probe, fine-tuning and $k$-NN rank methods differently and by design. **Comparing one paper's linear probe with another's fine-tuning is not a comparison.**
6. **⚠️ Pre-training data is not neutral.** CLIP inherits the web's associations, and self-supervised objectives have no labels to audit — **so the usual "check the label distribution" hygiene has nothing to check.** *Relevant to [[10 - Pose Estimation and Faces|ch. 10]] §4's demographic point: the training set is unexamined by construction.*
7. **A shortcut is not a bug in the network.** The network did exactly what the objective asked. **When self-supervised features transfer badly, look for what the task could be solved by** rather than for a training fault.
8. **In practice, use a released pre-trained checkpoint.** SimCLR-scale batches need ~128 TPU cores; **the value of this chapter is knowing what a checkpoint was trained to do, and therefore what it will and will not transfer to.** *This is directly relevant to the lecturer's project topics, which are all fine-tuning.*

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). **⚠️ AND SZELISKI IS THINNEST HERE OF ANY CHAPTER SO FAR** — §5.4.7 touches self-supervision briefly, and the second edition (2022) predates or barely covers MAE, DINO and much of the CLIP-era work. **This chapter is built primarily from the papers**: Oord et al. 2018 (InfoNCE/CPC), Chen et al. 2020 (SimCLR), He et al. 2020 (MoCo), Grill et al. 2020 (BYOL), Chen & He 2021 (SimSiam), He et al. 2022 (MAE), Radford et al. 2021 (CLIP), Zbontar et al. 2021 (Barlow Twins), plus Noroozi & Favaro 2016 and Gidaris et al. 2018 for the pretext tasks.
>
> ⚠️ **This is the chapter where the "textbook is a reference, not the spine" decision in [[00-Index]] bites hardest.** *If the lecturer teaches this week from Szeliski, this note is substantially broader than the course; if from recent papers (which the slide-7 framing suggests), it is aligned. **Worth confirming.***
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§3's entire ceiling table and the "0.8 class labels per example" comparison.** *The bound $I\ge\log N-L$ is Oord et al.'s; **converting it to bits, comparing it against an ImageNet label's 9.97 bits, and presenting SimCLR and MoCo as two answers to that one inequality is the addition.***
> - **§3's verification that $L=\log N$ at initialization**, and the recommendation to print it as a diagnostic.
> - **§4's numerical demonstration that the collapsed solution attains cosine exactly 1** and the statement that it is a **global**, not local, optimum — with the general rule drawn from it. *That BYOL "could" collapse is universally noted; **stating it as an optimality fact about the objective, and concluding that only architecture can fix it, is the framing added here**.*
> - **§5's cost table** and the separation of the 16× attention saving from the 4× linear saving.
> - **§6's identification of CLIP's text embeddings with [[03 - Image Classification and Linear Models|ch. 03]]'s $\mathbf W$ rows.**
> - **§2's shortcut table**, **§7's protocol comparison**, and **all eight Important Notes.**
>
> ⚠️ **No accuracy figures are quoted for any method.** Every number in this chapter is either exact arithmetic ($\log N$, token counts, $9!$, dataset sizes) or a stated design choice (MoCo's 65,536, SimCLR's 4,096, CLIP's 32,768 and 400M). **The claims that SimCLR needs both crop and colour jitter, that MAE's linear probe is comparatively weak while its fine-tuning is strong, and that stop-gradient is SimSiam's essential ingredient are the papers' ablation conclusions, stated qualitatively and attributed** — *they are exactly the kind of claim this chapter cannot verify, and they are the load-bearing empirical claims in it.*
>
> ⚠️ **§4's cosine figures use random unit vectors, not a trained network.** The informative case (0.304556) is illustrative; **the collapsed case (exactly 1.000000) is exact and is the finding.**
>
> **No discrepancies found.**
>
> **Deliberately deferred, not omitted:** **DINO** and self-supervised ViTs — whose attention maps segment objects without ever being told what an object is — are mentioned nowhere above and would fit naturally beside [[09 - Segmentation|ch. 09]]; **diffusion models as representation learners** are [[13 - Generative Models|ch. 13]]; **self-supervised depth and structure from motion** are [[14 - 3D Vision and Emerging Topics|ch. 14]]; **[[11 - Video and Motion|ch. 11]]'s temporal pretext tasks** (frame order, tracking as a pretext) are noted there.
>
> **Left as the source states it:** InfoNCE's derivation and bound; SimCLR's and MoCo's architectures and their stated batch/queue sizes; BYOL's and SimSiam's components; MAE's 75% and its encoder/decoder asymmetry; CLIP's 400M pairs and prompt-engineering finding; the jigsaw task's 1,000-permutation subset.

**Previous:** [[11 - Video and Motion]] · **Next:** [[13 - Generative Models]]
