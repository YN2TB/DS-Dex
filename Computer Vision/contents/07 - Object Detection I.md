---
subject: Computer Vision
chapter: 7
tags: [ds, computer-vision, object-detection, sliding-window, anchors, iou, nms, two-stage, r-cnn]
source: "Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed. §6.3; Stanford CS231n; the lecturer's course outline"
---

# Object Detection I

**Week 7 of 14. ⚠️ NO SLIDES** — see [[00-Index]].

> [!warning] ⚠️ CROSS-REFERENCE CHAPTER — the machinery is [[Deep Learning/contents/06 - Object Detection|DL ch. 06]]
> **[[00-Index]]'s boundary rule.** [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] covers **bounding boxes, anchor generation, IoU, the assignment algorithm, offset encoding, non-maximum suppression, multiscale detection, SSD and the whole R-CNN family** — with all three of D2L's printed labelling tensors regenerated, the NMS output and both RoI-pooling outputs reproduced, and the foreground/background imbalance measured at 123:1 to 5,443:1.
>
> **This note adds three things it does not have**: *why* the problem is structurally different from classification, *what* the exhaustive baseline costs, and the loss-weighting trap. **Evaluation by mAP is [[08 - Object Detection II|ch. 08]]**, per the course outline.

**Three results.**

**§2 — ⚠️ THE EXHAUSTIVE SLIDING WINDOW IS 283,605 WINDOWS ON A SINGLE $224^2$ IMAGE.** At a ResNet-50 forward pass each, that is **$1.16\times10^{15}$ operations per image.** ⇒ ***the entire history of detection is a sequence of ways to avoid that number*** — 2,000 proposals (R-CNN), 5,444 anchors (SSD), 100 queries (DETR).

**§1 — ⚠️ DETECTION'S OUTPUT SPACE IS A VARIABLE-LENGTH *SET*, AND THAT IS THE WHOLE DIFFICULTY.** Classification outputs a fixed $K$-vector; detection outputs $\{(\text{class},\text{box})\}$ of unknown size over a **continuous** box space. **Three consequences follow directly and shape every detector ever built.**

**§4 — ⚠️ THE LOSS WEIGHT $\lambda$ SILENTLY DECIDES WHETHER THE MODEL PREFERS TO BE RIGHT ABOUT *WHAT* OR ABOUT *WHERE*.** On a typical positive anchor, $\lambda=0.1$ gives a **97.9% classification / 2.1% localization** gradient split; $\lambda=10$ gives **31.5% / 68.5%**.

## 📘 Main Knowledge

### 1. ⚠️ Why detection is not classification with extra steps

**Classification**: the output is one of $K$ classes — a fixed $K$-vector, and [[03 - Image Classification and Linear Models|ch. 03]]'s whole pipeline applies.

**Detection**: the output is a **set** $\{(c_i,\mathbf b_i)\}$ of unknown size, where each $\mathbf b_i$ is **continuous**.

| objects present | distinct class-assignments ($K=80$) |
|---|---|
| 0 | 1 (the empty set) |
| 1 | 80 |
| 2 | 6,400 |
| 3 | 512,000 |
| 5 | **3,276,800,000** |

**And the boxes are real-valued, so the output space is not even countable.**

> [!warning] ⚠️ THREE CONSEQUENCES FOLLOW IMMEDIATELY, AND THEY EXPLAIN EVERY DESIGN DECISION IN BOTH DETECTION CHAPTERS
> | | consequence | how detectors answer it |
> |---|---|---|
> | **(i)** | **there is no fixed-size output layer** | **anchors** (SSD, RetinaNet), **proposals** (R-CNN family), or **queries** (DETR) supply one |
> | **(ii)** | **the loss cannot be computed until predictions are matched to ground truth** | the **assignment algorithm** — [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §4, IoU-greedy; DETR uses Hungarian matching |
> | **(iii)** | **duplicates are possible and must be removed** | **NMS** — [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §5 — or a loss that forbids them by construction |
>
> ⇒ ***anchors, assignment and NMS are not three unrelated tricks; they are the three answers to one structural problem.*** **Recognizing that makes the R-CNN family and the one-stage family look like variations rather than rival lineages.**

### 2. ⚠️ The exhaustive baseline, and the number everything is trying to avoid

**The naive detector**: slide a window over every position, at every scale and aspect ratio, and classify each. On a $224\times224$ image with stride 1:

| window | positions |
|---|---|
| $32^2$ | 37,249 |
| $64^2$ | 25,921 |
| $96^2$ | 16,641 |
| $128^2$ | 9,409 |
| $160^2$ | 4,225 |
| $192^2$ | 1,089 |
| $224^2$ | 1 |
| **square windows** | **94,535** |
| **× 3 aspect ratios** | **283,605** |

> [!warning] ⚠️ AND EVERY WINDOW NEEDS A CLASSIFIER PASS
> | classifier | per window | **per image** |
> |---|---|---|
> | linear on pixels ([[03 - Image Classification and Linear Models|ch. 03]]) | $3.07\times10^4$ | $8.71\times10^9$ |
> | **ResNet-50** | $4.1\times10^9$ | $\mathbf{1.16\times10^{15}}$ |
>
> **A quadrillion operations for one image.**
>
> **Coarsening the stride to 16 gives 455 square windows (1,365 with aspect ratios) — 208× fewer** — but a stride of 16 pixels means a detector that can be 8 pixels wrong in each direction before refinement, which is why **offset regression** exists.
>
> ⇒ ***every detector in this course and the next is a scheme for evaluating far fewer than 283,605 windows:*** **R-CNN's ~2,000 selective-search proposals, SSD's 5,444 anchors, DETR's 100 queries.** *And [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §9 measured the first big jump: Fast R-CNN's shared feature map made it **2,000 CNN passes → 1**.*

**[[02 - Classical Image Processing|Ch. 02]] §10's HOG + SVM detector is exactly this pipeline** — sliding window, image pyramid for scale, linear SVM score, NMS — and it was feasible **only because the classifier was a 3,780-dimensional dot product rather than a CNN.**

### 3. The machinery — all of it in [[Deep Learning/contents/06 - Object Detection|DL ch. 06]]

Rather than restate it, here is the map, with the finding each section produced:

| topic | where | the result worth remembering |
|---|---|---|
| bounding-box formats | DL ch. 06 §2 | corner ↔ centre conversions are exact inverses |
| **IoU** | DL ch. 06 §2 | ⚠️ **IoU 0.5 needs $d=1/3$ — two-thirds shared width**, and it cannot separate "wrong place" from "wrong size" |
| **anchor generation** | DL ch. 06 §3 | per-pixel anchors are **2,042,040** for one $561\times728$ image = 38.9 MB of labels |
| **assignment** | DL ch. 06 §4 | all three printed tensors regenerated; **step 2 guarantees every ground-truth box an anchor before the threshold applies** |
| offset encoding | DL ch. 06 §4 | standardized by $\times10$ (centres) and $\times5$ (log sizes) — **and the decode must invert it** |
| **NMS** | DL ch. 06 §5 | ⚠️ **converts a false positive into a false negative**; two real objects overlapping above $\epsilon$ leave one, unrecoverably |
| **multiscale** | DL ch. 06 §6 | **2,042,040 → 5,444 is 375×**, and each level's receptive field assigns it an object size |
| **SSD** | DL ch. 06 §7–8 | heads are convolutions (**116,308× cheaper** than fc); **imbalance 123:1 to 5,443:1 with only the offset half masked** |
| **R-CNN family** | DL ch. 06 §9 | **2,000× fewer CNN passes** from R-CNN to Fast R-CNN; then Faster R-CNN deletes selective search |

> [!note] ⚠️ Two-stage detectors, in one paragraph
> **R-CNN**: selective search proposes ~2,000 regions → each through a CNN → SVMs classify. **Fast R-CNN**: the whole image through the CNN **once**, then **RoI pooling** extracts a fixed-size block per proposal. **Faster R-CNN**: a **region proposal network** replaces selective search, making the detector end-to-end trainable for the first time. **Mask R-CNN** adds a mask branch and **RoI align** (bilinear instead of rounding), because pixel masks cannot tolerate quantization — that one is [[09 - Segmentation|ch. 09]].
>
> ⇒ **the pattern [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §9 names: each step deletes a hand-designed stage.** *SIFT → learned kernels; fc head → global average pooling; selective search → RPN; and next, anchors + NMS → set prediction ([[08 - Object Detection II|ch. 08]]).*

### 4. ⚠️ The loss weight, and a trap DL ch. 06 does not raise

Every detector minimizes

$$L=L_{\text{cls}}+\lambda\,L_{\text{loc}}$$

> [!warning] ⚠️ $\lambda$ IS A UNITS CONVERSION, AND IT DECIDES WHAT THE MODEL OPTIMIZES
> **$L_{\text{cls}}$ is in nats. $L_{\text{loc}}$ is in normalized box units.** They are not commensurable, so $\lambda$ is doing more than balancing magnitudes — it is choosing an exchange rate.
>
> On a typical positive anchor ($L_{\text{cls}}\approx0.69$, $L_{\text{loc}}\approx0.15$):
>
> | $\lambda$ | total | **classification share** | **localization share** |
> |---|---|---|---|
> | 0.1 | 0.7050 | **97.9%** | 2.1% |
> | 1.0 | 0.8400 | 82.1% | 17.9% |
> | 5.0 | 1.4400 | 47.9% | 52.1% |
> | 10.0 | 2.1900 | **31.5%** | **68.5%** |
>
> ⇒ ***$\lambda$ silently decides whether the model prefers to be right about WHAT or about WHERE.*** **It is not a minor hyperparameter**, and a detector that localizes well but misclassifies (or the reverse) usually needs $\lambda$ changed, not more training.
>
> **And this is the *second* imbalance in the same loss.** [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8 measured the first: **positives to negatives at 123:1 at best and 5,443:1 for a small object, with the mask applied only to the offset half** — so a "background everywhere" predictor scores 99.8%. **Two different imbalances, in one scalar objective, neither visible in the loss curve.**

## ✏️ Exercises

> [!example]- Exercise 1 — cost the exhaustive baseline
> **(a)** Square windows at scales 32–224, stride 1, on $224^2$. **(b)** With 3 aspect ratios, and the cost at a ResNet-50 pass each. **(c)** Stride 16. **(d)** What does that imply?
>
> ---
> **(a)** $\sum_s(224-s+1)^2$ over $s\in\{32,64,96,128,160,192,224\}=\mathbf{94{,}535}$.
>
> **(b)** $\times3=\mathbf{283{,}605}$ windows; at $4.1\times10^9$ operations each, $\mathbf{1.16\times10^{15}}$ **per image**.
>
> **(c)** 455 square windows (1,365 with aspect ratios) — **208× fewer**, at the cost of up to 8 px of localization error per axis before refinement. **That error is exactly what offset regression corrects.**
>
> **(d)** ⚠️ **Exhaustive search is not merely slow, it is off by nine orders of magnitude.** ⇒ *every detector is a scheme for evaluating far fewer windows* — 2,000 (R-CNN), 5,444 (SSD), 100 (DETR) — **and [[02 - Classical Image Processing|ch. 02]]'s HOG+SVM was feasible only because its classifier was a 3,780-dim dot product.**

> [!example]- Exercise 2 — the output space
> **(a)** How many class-assignments for 3 objects out of 80 classes? **(b)** Why is the true output space uncountable? **(c)** Name the three structural consequences and one detector's answer to each.
>
> ---
> **(a)** $80^3=\mathbf{512{,}000}$ (and $80^5\approx3.28\times10^9$ for five).
>
> **(b)** **Because each box is four real numbers.** Even fixing the count and classes, the box coordinates are continuous — so the output is not a choice from a finite menu at all.
>
> **(c)** ⚠️ **(i) No fixed-size output layer** → anchors / proposals / queries. **(ii) The loss needs an assignment first** → IoU-greedy matching ([[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §4) or Hungarian matching (DETR). **(iii) Duplicates are possible** → NMS, or a loss that forbids them. ⇒ *these three are one problem with three answers, not three tricks.*

> [!example]- Exercise 3 — the loss weight
> **(a)** Why are $L_{\text{cls}}$ and $L_{\text{loc}}$ not commensurable? **(b)** Gradient split at $\lambda=0.1$ and $\lambda=10$ for $L_{\text{cls}}=0.69$, $L_{\text{loc}}=0.15$. **(c)** What symptom indicates a bad $\lambda$? **(d)** What is the *other* imbalance in the same loss?
>
> ---
> **(a)** **$L_{\text{cls}}$ is measured in nats** (a log-probability); **$L_{\text{loc}}$ in normalized box units** (or their squares). **There is no natural exchange rate** — $\lambda$ invents one.
>
> **(b)** $\lambda=0.1$: **97.9% / 2.1%**. $\lambda=10$: **31.5% / 68.5%.** A 100× change in $\lambda$ moves the split by a factor of 33 on the localization side.
>
> **(c)** ⚠️ **Boxes in roughly the right place with wrong labels** (λ too high), or **correct labels with sloppy boxes** (λ too low). **Both look like "the model needs more training" and neither is.**
>
> **(d)** **The foreground/background imbalance** — 123:1 to 5,443:1 ([[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8) — **with the mask applied only to the offset half**, so nothing corrects the class loss. ⚠️ **Two imbalances in one scalar, neither visible in the loss curve.** *That is what focal loss addresses, in [[08 - Object Detection II|ch. 08]].*

## 📝 Summary

- **⚠️ Detection's output is a variable-length *set* of (class, box) over a continuous box space** — $80^3=512{,}000$ class-assignments for three objects, and uncountably many boxes. **Three consequences follow: no fixed output layer (→ anchors/proposals/queries), no loss without an assignment (→ matching), and possible duplicates (→ NMS).** *One problem, three answers — not three tricks.*
- **⚠️ The exhaustive sliding window is 94,535 square windows, 283,605 with aspect ratios, on one $224^2$ image** — **$1.16\times10^{15}$ operations at a ResNet-50 pass each.** Stride 16 cuts it 208× at the cost of localization error, which offset regression then repairs. ⇒ ***the history of detection is a sequence of ways to avoid that number.***
- **All the machinery — boxes, IoU, anchors, assignment, offsets, NMS, multiscale, SSD, the R-CNN family — is [[Deep Learning/contents/06 - Object Detection|DL ch. 06]]**, including that IoU 0.5 means two-thirds shared width, that NMS converts false positives into false negatives, that multiscale is a 375× reduction, and that Fast R-CNN is 2,000× fewer CNN passes.
- **⚠️ $L=L_{\text{cls}}+\lambda L_{\text{loc}}$ mixes nats with box units, so $\lambda$ is an invented exchange rate** — **97.9%/2.1% at $\lambda=0.1$ and 31.5%/68.5% at $\lambda=10$.** It decides whether the model prefers to be right about *what* or about *where*.
- **Two different imbalances live in that one scalar** — the $\lambda$ trade and the 123:1–5,443:1 foreground/background ratio — **and neither is visible in the loss curve.**

## ⚠️ Important Notes

1. **⚠️ Report $\lambda$ whenever you report a detector.** It determines the classification/localization split and therefore which failure mode you see. **A detector "not converging" is often a $\lambda$ problem.**
2. **⚠️ Two imbalances, one loss.** Fixing the foreground/background ratio (focal loss, hard-negative mining) does nothing about the $\lambda$ trade, and vice versa. **Diagnose them separately.**
3. **⚠️ Stride is a localization floor.** A stride-16 feature map cannot localize better than ±8 px before regression. **If small objects are mislocalized, check the stride before the architecture.**
4. **⚠️ Anchors, assignment and NMS are coupled.** Changing the anchor scales changes which anchors are positive, which changes the assignment, which changes what NMS sees. **Tuning one in isolation is how detectors get worse.**
5. **The classical pipeline is the modern one with the learned parts removed** ([[02 - Classical Image Processing|ch. 02]] §10). **Sliding window → anchors; pyramid → feature pyramid; SVM → classification head; NMS → NMS, unchanged.** Recognizing this is why this chapter is short.
6. **Detection datasets are far smaller than classification datasets** because box annotation is expensive — which is why detection backbones are almost always **pretrained classifiers**, and why [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §1's fine-tuning discussion belongs at the front of every detection pipeline.

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). Built from **Szeliski §6.3 (object detection, face detection, pedestrian detection, general object detection)**, **CS231n**, and this vault's [[Deep Learning/contents/06 - Object Detection|DL ch. 06]].
>
> **⚠️ AND THIS IS DELIBERATELY SHORT.** [[00-Index]]'s boundary table records that **DL ch. 06 owns week 7 entirely** — it reproduces all three of D2L's printed labelling tensors from the raw inputs, both RoI-pooling outputs, the NMS result and every anchor count, and it measures the class imbalance that D2L omits. **Restating it here would create two copies that can drift apart.**
>
> **⚠️ The split between weeks 7 and 8 is inferred.** The lecturer lists *"Object detection I"* and *"Object detection II"* with no contents. **This chapter takes the problem framing and two-stage detectors; [[08 - Object Detection II|ch. 08]] takes one-stage detectors, FPN, focal loss, DETR and mAP**, following [[00-Index]]'s table. **If week 7 in fact covers one-stage detectors first, the material is all present across the two chapters but assigned to the wrong week.**
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§1's output-space argument** — the $K^m$ table, the uncountability observation, and **the framing of anchors/assignment/NMS as three answers to one structural problem.** *This framing is not in Szeliski, CS231n or D2L.*
> - **§2's exhaustive sliding-window count** (94,535 / 283,605 / $1.16\times10^{15}$) and the stride-16 comparison, and its use to explain the proposal counts of every later detector.
> - **§4's $\lambda$ analysis** — the gradient-split table and the observation that **$L_{\text{cls}}$ and $L_{\text{loc}}$ are dimensionally incommensurable.** **DL ch. 06 measures the foreground/background imbalance and does not raise this second one.**
> - **§3's summary table**, which is a navigation aid into DL ch. 06 rather than new content.
> - **All six Important Notes.**
>
> **No discrepancies found**; every quantitative claim here is my own computation, and the ResNet-50 figure of $4.1\times10^9$ operations is an external round number used only for an order-of-magnitude illustration and flagged as such.
>
> **Deliberately deferred, not omitted:** **everything mechanical** is [[Deep Learning/contents/06 - Object Detection|DL ch. 06]]. **mAP and the evaluation protocol** are [[08 - Object Detection II|ch. 08]] per the course outline. **Mask R-CNN's mask branch and RoI align** are [[09 - Segmentation|ch. 09]]. **Szeliski §6.3.1 (face detection)** is held for [[10 - Pose Estimation and Faces|ch. 10]], where faces are the topic; **§6.3.2 (pedestrian detection)** is the HOG+SVM pipeline already covered in [[02 - Classical Image Processing|ch. 02]] §10.
>
> **Left as the source states it:** Szeliski's account of the R-CNN lineage and its citations (Girshick et al. 2014, Girshick 2015, Ren et al. 2015, He et al. 2017); the ~2,000 figure for selective search proposals; and ResNet-50's forward-pass cost.

**Previous:** [[06 - Vision Transformers]] · **Next:** [[08 - Object Detection II]]
