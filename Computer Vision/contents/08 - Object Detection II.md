---
subject: Computer Vision
chapter: 8
tags: [ds, computer-vision, object-detection, yolo, fpn, focal-loss, detr, map, evaluation]
source: "Lin et al. 2017 (FPN, Focal Loss); Redmon et al. 2016 (YOLO); Carion et al. 2020 (DETR); Szeliski, *Computer Vision*, 2nd ed. §6.3.3; the lecturer's course outline"
---

# Object Detection II

**Week 8 of 14. ⚠️ NO SLIDES** — see [[00-Index]].

> [!note] ⚠️ A **depth** chapter — [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] has SSD and the R-CNN family, **not** YOLO, FPN, focal loss, DETR or mAP
> [[07 - Object Detection I|Ch. 07]] framed the problem and pointed at DL ch. 06 for the machinery. **This chapter is the part the vault does not already have**, including the evaluation metric — which [[00-Index]] assigns to week 8.

**Four results.**

**§2 — ⚠️ THE SAME DETECTIONS GIVE AP = 0.6833, 0.7045 OR 0.6865 DEPENDING ONLY ON THE INTERPOLATION CONVENTION.** A **3.1% spread from the protocol alone**, before any modelling. ⇒ ***"mAP" is meaningless without naming the protocol and the IoU threshold.***

**§3 — ⚠️ AP@0.5 IS 1.55× THE COCO HEADLINE AP@[.5:.95] ON THE SAME DETECTOR.** Quoting one against the other is a **55% error** — and the 95% collapse from IoU 0.5 to 0.95 measures **localization quality, not classification.**

**§4 — ⚠️ FOCAL LOSS SWINGS DL ch. 06's IMBALANCE BY A FACTOR OF 2,501.** Under plain cross-entropy the 5,443 easy negatives contribute **78.9× more total loss** than the one positive; at $\gamma=2$ **the positive contributes 31.7× more than all 5,443 combined.** An easy negative at $p_t=0.99$ is down-weighted **10,000×**.

**§6 — ⚠️ ONE-TO-ONE MATCHING DELETES ANCHORS AND NMS TOGETHER.** DETR answers **two** of [[07 - Object Detection I|ch. 07]] §1's three structural consequences with **one** mechanism — and pays for it with a hard cap of $N=100$ objects per image.

## 📘 Main Knowledge

### 1. One-stage detectors: YOLO and the shape of the trade

**Two-stage** (R-CNN family): propose regions, then classify and refine each.
**One-stage** (YOLO, SSD, RetinaNet): **predict class and box directly at every location, in a single pass.**

**YOLO's framing is the cleanest statement of the idea**: divide the image into an $S\times S$ grid; each cell predicts $B$ boxes with confidences and a class distribution. **Detection becomes a single regression problem over a fixed-size tensor** — which is [[07 - Object Detection I|ch. 07]] §1's consequence (i) answered by a grid instead of by proposals.

| | two-stage | one-stage |
|---|---|---|
| passes | propose → classify | **one** |
| speed | slower | **real-time** |
| small objects | stronger | weaker |
| **class imbalance** | mitigated — proposals pre-filter background | **severe** — every location is an example |
| training | more stages | simpler |

> [!note] ⚠️ The imbalance row is the whole story of §4
> **A two-stage detector's first stage discards most background before the classifier sees it**, so its second stage trains on a roughly balanced set. **A one-stage detector classifies every anchor every step** — [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8 measured that at **123:1 to 5,443:1.** ⇒ *the accuracy gap between the families was not a modelling gap; it was a loss-function gap*, and focal loss closed it.

### 2. ⚠️ mAP from first principles — and the convention that changes the answer

**Sort detections by confidence; each is a TP or FP by IoU against unmatched ground truth; accumulate.** Five ground-truth objects, eight detections:

| det | conf | TP? | cumTP | cumFP | precision | recall |
|---|---|---|---|---|---|---|
| D1 | 0.95 | ✓ | 1 | 0 | 1.0000 | 0.2000 |
| D2 | 0.91 | ✓ | 2 | 0 | 1.0000 | 0.4000 |
| D3 | 0.88 | ✗ | 2 | 1 | 0.6667 | 0.4000 |
| D4 | 0.80 | ✓ | 3 | 1 | 0.7500 | 0.6000 |
| D5 | 0.72 | ✗ | 3 | 2 | 0.6000 | 0.6000 |
| D6 | 0.65 | ✓ | 4 | 2 | 0.6667 | 0.8000 |
| D7 | 0.40 | ✗ | 4 | 3 | 0.5714 | 0.8000 |
| D8 | 0.20 | ✗ | 4 | 4 | 0.5000 | 0.8000 |

**AP is the area under the precision–recall curve — and there are three conventions for computing it.**

First, **precision is made monotone non-increasing** (each point takes the max precision at any higher recall):
`[1.0, 1.0, 0.6667, 0.75, 0.6, 0.6667, 0.5714, 0.5]` → `[1.0, 1.0, 0.75, 0.75, 0.6667, 0.6667, 0.5714, 0.5]`

| convention | used by | **AP** |
|---|---|---|
| all-point | COCO, VOC2010+ | **0.683333** |
| 11-point | VOC2007 | **0.704545** |
| 101-point | COCO | **0.686469** |

> [!warning] ⚠️ A 3.1% SPREAD FROM THE PROTOCOL ALONE, ON IDENTICAL DETECTIONS
> ⇒ ***"mAP = 0.70" is not a number until you name the protocol and the IoU threshold.*** **A 3% difference between two papers can be entirely an artefact of which convention each used** — and 3% is larger than many reported improvements.
>
> ⚠️ **And note the ceiling**: only **4 of 5** ground-truth objects were ever detected, so recall cannot exceed **0.80** and **AP is bounded above by 0.80** however the scores are ordered. **Missed objects cost you at every threshold** — which is why recall, not precision, is usually the binding constraint in detection.

### 3. ⚠️ mAP@[.5:.95] — what averaging over IoU thresholds measures

**COCO averages AP over IoU $=0.50,0.55,\dots,0.95$.** A representative profile:

| IoU | 0.50 | 0.60 | 0.70 | 0.80 | 0.90 | 0.95 |
|---|---|---|---|---|---|---|
| AP | **0.62** | 0.57 | 0.49 | 0.35 | 0.12 | **0.03** |

$$\text{AP@0.5}=0.620\qquad \textbf{AP@[.5:.95]}=\mathbf{0.399}$$

> [!warning] ⚠️ THE HEADLINE NUMBER IS **1.55×** SMALLER THAN AP@0.5
> **Comparing one paper's AP@0.5 against another's AP@[.5:.95] is a 55% error** — and both are called "mAP".
>
> **And the 95% collapse from IoU 0.5 to 0.95 is diagnostic**: the classifier is unchanged across those thresholds, so **the drop measures localization quality alone.** ⇒ *a detector with high AP@0.5 and low AP@[.5:.95] finds the right objects and boxes them loosely — a regression problem, not a recognition problem*, and the fix is the loss weight ([[07 - Object Detection I|ch. 07]] §4) or the box parametrization, not more classes or more data.

### 4. ⚠️ Focal loss — the mechanism, and the 2,501× swing

$$\mathrm{CE}(p_t)=-\log p_t\qquad\longrightarrow\qquad \mathrm{FL}(p_t)=-(1-p_t)^{\gamma}\log p_t$$

| $p_t$ | CE | FL ($\gamma=2$) | modulator $(1-p_t)^2$ | **down-weight** |
|---|---|---|---|---|
| 0.5 | 0.6931 | $1.73\times10^{-1}$ | $2.5\times10^{-1}$ | 4× |
| 0.9 | 0.1054 | $1.05\times10^{-3}$ | $1.0\times10^{-2}$ | 100× |
| **0.99** | 0.0101 | $1.01\times10^{-6}$ | $1.0\times10^{-4}$ | **10,000×** |
| 0.999 | 0.0010 | $1.00\times10^{-9}$ | $1.0\times10^{-6}$ | 1,000,000× |

**Applied to [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8's measured case** — one hard positive ($p_t=0.5$) against 5,443 easy negatives ($p_t=0.99$):

| loss | positives | negatives | **which dominates** |
|---|---|---|---|
| plain cross-entropy | $6.93\times10^{-1}$ | $5.47\times10^{1}$ | **negatives by 78.9×** |
| **focal, $\gamma=2$** | $1.73\times10^{-1}$ | $5.47\times10^{-3}$ | **POSITIVE by 31.7×** |
| focal, $\gamma=5$ | $2.17\times10^{-2}$ | $5.47\times10^{-9}$ | positive by $4.0\times10^6$× |

> [!warning] ⚠️ A SWING OF $78.9\times31.7=\mathbf{2{,}501\times}$ FROM ONE EXPONENT
> **Under plain cross-entropy the 5,443 easy negatives contribute 78.9× more total loss than the single positive** — so the gradient is dominated by anchors whose correct answer is "background", exactly the failure [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8 identified and D2L's loss does nothing about.
>
> **At $\gamma=2$ the positive contributes 31.7× more than all 5,443 negatives combined.**
>
> ⇒ ***that inversion is the entire reason one-stage detectors caught up with two-stage ones*** (Lin et al. 2017). **It is not a better architecture; it is the same architecture with the imbalance removed from the objective.**
>
> ⚠️ **And $\gamma$ is not free**: at $\gamma=5$ the negatives contribute essentially nothing ($4\times10^6$×), so the model stops learning what background looks like at all. **$\gamma=2$ is the published default and the table shows why the window is narrow.**

### 5. FPN — every level semantically strong

[[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §6 showed multiscale detection assigns **each feature level a different object size**. **The problem it leaves**: the high-resolution level comes from an *early* backbone layer, with a small receptive field and weak semantics — good for locating small objects, bad at recognizing them.

**FPN (Lin et al. 2017) adds a top-down path**: take the deepest map, upsample, add a $1\times1$-projected lateral connection from the corresponding backbone level, smooth with $3\times3$. **Cost on a ResNet-50:**

| level | stride | map ($224$ in) | lateral $1\times1$ | smooth $3\times3$ |
|---|---|---|---|---|
| P2 | 4 | $56^2$ | 65,792 | 590,080 |
| P3 | 8 | $28^2$ | 131,328 | 590,080 |
| P4 | 16 | $14^2$ | 262,400 | 590,080 |
| P5 | 32 | $7^2$ | 524,544 | 590,080 |
| **total** | | | **3,344,384** | **12.76 MB** |

> [!note] ⚠️ **~13.1% on top of a 25.6M-parameter backbone, and it changes what each level *is***
> **DL ch. 06 §6's pyramid gave each level a different object size; FPN gives every level the same semantic depth.** ⇒ *the two are complementary, and together they are why "multi-scale" stopped meaning "run the detector at several image sizes".*
>
> **This is also why [[06 - Vision Transformers|ch. 06]] §4 noted that Swin's *hierarchy*, not its windowing, is what made Transformers usable as detection backbones** — a plain ViT has one resolution and no pyramid to build on.

### 6. ⚠️ DETR — set prediction, and deleting two things at once

**DETR (Carion et al. 2020) makes detection what [[07 - Object Detection I|ch. 07]] §1 said it was: set prediction.** $N=100$ learned **queries**, each emitting one (class, box); a Transformer decoder attends to image features; **the loss bipartite-matches predictions to ground truth exactly once, by the Hungarian algorithm.**

| objects $m$ | brute-force matchings | **Hungarian $O(N^3)$** |
|---|---|---|
| 1 | 100 | 1,000,000 |
| 5 | $9.03\times10^9$ | 1,000,000 |
| 20 | $1.30\times10^{39}$ | **1,000,000** |

> [!warning] ⚠️ ONE-TO-ONE MATCHING IS WHAT REMOVES NMS
> **If exactly one prediction is assigned to each object, a duplicate is explicitly penalized as a false positive** — so the model **learns not to produce duplicates** instead of having them filtered afterwards.
>
> ⇒ ***DETR answers two of [[07 - Object Detection I|ch. 07]] §1's three consequences with one mechanism***: the fixed set of queries supplies the output layer (i), and one-to-one matching removes duplicates (iii). **Anchors gone, NMS gone.**
>
> **And that completes [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §9's pattern.** SIFT → learned kernels; fc head → global average pooling; selective search → RPN; **anchors + NMS → set prediction.** *Each step deletes a hand-designed stage, and NMS — the component that survived both the classical and the CNN eras intact ([[02 - Classical Image Processing|ch. 02]] §10) — is the one this step finally removes.*

> [!warning] ⚠️ The costs are real and worth stating
> **$N=100$ is a hard cap on detectable objects.** COCO images hold at most ~93, so it is comfortable there — **but a crowd scene with 200 people is beyond the model by construction**, not by training.
>
> **And DETR is notoriously slow to converge** — the matching is unstable early, when no query is yet specialized. *Deformable DETR and successors address this; the original needed far more epochs than a comparable Faster R-CNN.*

## ✏️ Exercises

> [!example]- Exercise 1 — compute AP by hand
> Five ground-truth objects; detections with confidence and TP/FP: $(0.95,\text{T}),(0.91,\text{T}),(0.88,\text{F}),(0.80,\text{T}),(0.72,\text{F}),(0.65,\text{T}),(0.40,\text{F}),(0.20,\text{F})$.
> **(a)** Precision and recall at each. **(b)** AP under all-point and 11-point interpolation. **(c)** What bounds AP here? **(d)** What does the spread mean?
>
> ---
> **(a)** As tabulated in §2 — precision falls to 0.5000 and recall rises to 0.8000.
>
> **(b)** Interpolate precision to be monotone non-increasing, then integrate. **All-point: 0.683333. 11-point: 0.704545.** *(101-point: 0.686469.)*
>
> **(c)** ⚠️ **Only 4 of 5 objects were ever detected, so recall caps at 0.80 and AP caps at 0.80.** No re-ranking of the eight detections can recover the missed object. **Misses cost at every threshold.**
>
> **(d)** ⚠️ **A 3.1% spread from the interpolation convention alone.** ⇒ *"mAP" is not a number until the protocol and IoU threshold are named* — and a 3% difference between papers can be entirely an artefact.

> [!example]- Exercise 2 — read a COCO result
> A detector reports AP@0.5 $=0.62$ and AP@[.5:.95] $=0.399$. **(a)** Why do they differ? **(b)** By how much? **(c)** What does a large gap tell you? **(d)** What does it not tell you?
>
> ---
> **(a)** **AP@[.5:.95] averages over ten thresholds from 0.50 to 0.95**, and AP falls as boxes must be tighter — from 0.62 to 0.03 here.
>
> **(b)** $0.620/0.399=\mathbf{1.55\times}$. **Quoting one against the other is a 55% error.**
>
> **(c)** ⚠️ **The classifier is identical across thresholds, so the gap measures LOCALIZATION quality alone.** A large gap means the detector **finds the right objects and boxes them loosely.** The fix is the loss weight ([[07 - Object Detection I|ch. 07]] §4), the box parametrization, or the feature stride — **not more classes or more data.**
>
> **(d)** It says nothing about **which** classes fail, about small-vs-large objects (COCO reports AP$_S$/AP$_M$/AP$_L$ separately for that reason), or about **recall ceiling** — a detector that never proposes a region cannot be diagnosed from AP alone.

> [!example]- Exercise 3 — focal loss
> **(a)** Write FL and compute the modulator at $p_t=0.9,0.99$ with $\gamma=2$. **(b)** Apply it to 1 positive at $p_t=0.5$ against 5,443 negatives at $p_t=0.99$. **(c)** What happens at $\gamma=5$? **(d)** Why does this close the one-stage/two-stage gap?
>
> ---
> **(a)** $\mathrm{FL}=-(1-p_t)^\gamma\log p_t$. Modulator $(1-0.9)^2=10^{-2}$ (**100×** down-weight); $(1-0.99)^2=10^{-4}$ (**10,000×**).
>
> **(b)** Plain CE: positives $6.93\times10^{-1}$, negatives $5.47\times10^{1}$ — **negatives dominate by 78.9×**. Focal $\gamma=2$: positives $1.73\times10^{-1}$, negatives $5.47\times10^{-3}$ — **the positive dominates by 31.7×.** ⚠️ **A swing of 2,501×.**
>
> **(c)** Negatives contribute $5.47\times10^{-9}$ — the positive dominates by $4\times10^6$. ⚠️ **The model stops learning what background looks like**, so $\gamma$ has a narrow useful window and 2 is the published default.
>
> **(d)** ⚠️ **Because the gap was never architectural.** A two-stage detector's proposals pre-filter background, giving a roughly balanced second stage; a one-stage detector classifies all 5,444 anchors every step. **Focal loss removes the imbalance from the objective instead of from the data** — same architecture, different loss.

> [!example]- Exercise 4 — DETR
> **(a)** How does a fixed set of $N$ queries answer [[07 - Object Detection I|ch. 07]] §1's consequence (i)? **(b)** Why does one-to-one matching remove NMS? **(c)** Brute-force vs Hungarian cost for $m=20$, $N=100$. **(d)** Two costs of the design.
>
> ---
> **(a)** **It supplies the fixed-size output layer** the variable-length set problem lacks — $N$ slots, each emitting (class, box), with "no object" as a valid class.
>
> **(b)** ⚠️ **Because a duplicate is explicitly a false positive under the matching.** Exactly one prediction is assigned to each object; every other prediction of that object is penalized. **The model learns not to duplicate, instead of duplicating and being filtered.**
>
> **(c)** Brute force: $P(100,20)=1.30\times10^{39}$ matchings. **Hungarian: $O(N^3)=10^6$.** *The matching is only tractable because a polynomial algorithm exists.*
>
> **(d)** ⚠️ **(i) $N$ caps the objects per image** — 100 works for COCO's ~93 maximum and **fails by construction on a 200-person crowd.** **(ii) Slow convergence** — the matching is unstable early, when no query has specialized, so the original DETR needed far more epochs than a comparable Faster R-CNN.

## 📝 Summary

- **One-stage detectors predict class and box directly at every location in a single pass**; two-stage detectors propose then classify. **The accuracy gap between them was a loss-function gap, not an architectural one.**
- **⚠️ AP is the area under the precision–recall curve, and three conventions give 0.683333 / 0.704545 / 0.686469 on identical detections — a 3.1% spread from the protocol alone.** ⇒ **"mAP" requires naming the protocol and the IoU threshold.** **And missed objects cap AP**: 4 of 5 detected bounds AP at 0.80 regardless of ranking.
- **⚠️ AP@0.5 is 1.55× the COCO headline AP@[.5:.95]** — a 55% error if confused. **The 95% collapse from IoU 0.5 to 0.95 measures localization quality alone**, since the classifier is unchanged.
- **⚠️ Focal loss $-(1-p_t)^\gamma\log p_t$ down-weights an easy negative at $p_t=0.99$ by 10,000×.** Applied to [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8's measured 5,443:1 case, it **swings the loss balance by 2,501×** — from negatives dominating 78.9× to the positive dominating 31.7×. **At $\gamma=5$ the model stops learning background at all**, so the useful window is narrow.
- **FPN adds a top-down path for ~3.34M parameters (13.1% of a ResNet-50)** and gives **every pyramid level the same semantic depth**, complementing DL ch. 06 §6's assignment of a different **object size** to each level.
- **⚠️ DETR makes detection set prediction**: $N=100$ queries and one-to-one Hungarian matching ($O(N^3)=10^6$ against $1.3\times10^{39}$ brute-force matchings at $m=20$). **It answers two of [[07 - Object Detection I|ch. 07]] §1's three consequences with one mechanism — anchors gone, NMS gone** — completing [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §9's "delete a hand-designed stage" pattern by removing the one component that survived both earlier eras. **Costs: a hard cap of $N$ objects, and slow convergence.**

## ⚠️ Important Notes

1. **⚠️ Never compare mAP across papers without matching the protocol *and* the IoU threshold.** AP@0.5 vs AP@[.5:.95] is a 55% difference; VOC2007 11-point vs COCO all-point is another 3%. **Both are called "mAP".**
2. **⚠️ A large AP@0.5 − AP@[.5:.95] gap is a localization diagnosis, not a recognition one.** Look at the box loss weight, the parametrization and the feature stride before touching the classifier.
3. **⚠️ AP is capped by recall.** Objects never proposed cost you at every threshold and cannot be recovered by re-ranking. **Check the recall ceiling before tuning confidence thresholds.**
4. **⚠️ $\gamma$ in focal loss has a narrow window.** $\gamma=2$ inverts the imbalance usefully; $\gamma=5$ makes background invisible to the model. **Tune $\alpha$ (the class weight) and $\gamma$ together — they interact.**
5. **⚠️ Focal loss addresses one of the two imbalances in a detection loss.** It does nothing about [[07 - Object Detection I|ch. 07]] §4's $\lambda$ trade between classification and localization. **Diagnose them separately.**
6. **⚠️ DETR's $N$ is a hard architectural cap.** If your images can contain more than $N$ objects, no amount of training helps. **Count the objects in your data before choosing the family.**
7. **⚠️ FPN is not the same thing as multi-scale anchors.** DL ch. 06 §6's pyramid assigns each level an object *size*; FPN gives each level the same *semantic depth*. **Using one name for both hides that a detector may have one and not the other.**
8. **The one-stage/two-stage distinction is blurring.** With focal loss, FPN and better assignment, one-stage detectors match two-stage accuracy at higher speed — **so "two-stage is more accurate" is a statement about 2016, not about the method.**

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). Built from the **FPN and Focal Loss papers (Lin et al. 2017)**, **YOLO (Redmon et al. 2016)**, **DETR (Carion et al. 2020)**, **Szeliski §6.3.3**, and this vault's [[Deep Learning/contents/06 - Object Detection|DL ch. 06]].
>
> **⚠️ The week 7 / week 8 split is inferred** — the lecturer lists *"Object detection I"* and *"II"* with no contents. **[[00-Index]]'s table assigns one-stage detectors, FPN, focal loss, DETR and mAP to week 8**, and that is what this chapter covers. **If the actual split differs, the material is present across the two chapters but under the wrong week.**
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§2's complete worked mAP example** and the finding that **three standard conventions give a 3.1% spread on identical detections**, plus the **recall ceiling** observation. *The conventions are documented; computing all three on one example and reporting the spread is mine.*
> - **§3's AP-vs-IoU profile and the 1.55× headline gap**, and the reading that the collapse **isolates localization quality** because the classifier is constant across thresholds.
> - **§4's focal-loss table and the 2,501× swing**, computed by applying the loss to **DL ch. 06 §8's own measured 5,443:1 imbalance** — which connects a result this vault produced to the paper that fixed it. **The $\gamma=5$ failure mode is also mine.**
> - **§5's FPN parameter count** (3,344,384; 13.1% of a ResNet-50) and the distinction between *object size per level* (DL ch. 06 §6) and *semantic depth per level* (FPN).
> - **§6's matching-cost table** ($1.3\times10^{39}$ vs $10^6$) and **the framing that DETR answers two of [[07 - Object Detection I|ch. 07]] §1's three consequences with one mechanism**, completing DL ch. 06 §9's deletion pattern.
> - **All eight Important Notes.**
>
> ⚠️ **Two classes of number are deliberately illustrative and labelled as such**: **§3's AP-vs-IoU profile** is a plausible shape used to demonstrate the arithmetic of averaging, **not a measured result** for any specific detector; and **§4's $p_t$ values** (0.5 for a hard positive, 0.99 for an easy negative) are representative choices, with the *mechanism* — not the exact swing — being the finding. **The 5,443 anchor count is real, from DL ch. 06 §8.** No accuracy figures from any paper are quoted, per the vault's rule against unverified numbers.
>
> **No discrepancies found.**
>
> **Deliberately deferred, not omitted:** **anchors, IoU, assignment, offset encoding, NMS, multiscale and SSD** are [[Deep Learning/contents/06 - Object Detection|DL ch. 06]], and the R-CNN family is summarized in [[07 - Object Detection I|ch. 07]] §3. **YOLO's version history (v2–v11)** is a sequence of engineering refinements with no single conceptual step; only the original framing is given. **Mask R-CNN's mask branch and RoI align** are [[09 - Segmentation|ch. 09]]. **Deformable DETR and later convergence fixes** are named in §6 and not developed. **Soft-NMS** is [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §5.
>
> **Left as the source states it:** COCO's evaluation protocol and its AP$_S$/AP$_M$/AP$_L$ breakdown; the ~93-object maximum per COCO image; ResNet-50's ~25.6M parameters; the claim that DETR converges slowly relative to Faster R-CNN; and all reported accuracies in the cited papers, which are not quoted here.

**Previous:** [[07 - Object Detection I]] · **Next:** [[09 - Segmentation]]
