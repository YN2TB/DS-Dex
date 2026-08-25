---
subject: Computer Vision
chapter: 10
tags: [ds, computer-vision, pose-estimation, keypoints, heatmaps, face-detection, face-recognition, embeddings, triplet-loss]
source: "Szeliski, *Computer Vision*, 2nd ed. §6.2.4, §6.3.1, §6.4.5; Newell et al. 2016 (stacked hourglass); Cao et al. 2017 (OpenPose); Schroff et al. 2015 (FaceNet); Deng et al. 2019 (ArcFace); the lecturer's course outline"
---

# Pose Estimation and Faces

**Week 10 of 14. ⚠️ NO SLIDES** — see [[00-Index]].

**Four results.**

**§4 — ⚠️ FACE *IDENTIFICATION* NEEDS A FALSE-ACCEPT RATE FOUR ORDERS OF MAGNITUDE BETTER THAN *VERIFICATION*, AND THE ARITHMETIC IS UNFORGIVING.** A **0.1% FAR — which sounds excellent — gives a 99.995% chance of at least one false match in a 10,000-person gallery.** To hold gallery-level error under 1% at $N=10^6$ you need **FAR $\le1.005\times10^{-8}$ — one in 99.5 million.**

**§1 — ⚠️ A REGRESSOR MUST AVERAGE ITS MODES, AND THE AVERAGE OF TWO PLAUSIBLE ELBOWS IS ON NEITHER ARM.** That, not accuracy, is why heatmaps replaced direct coordinate regression — **at the cost of 2,048× more output and a $\pm s/2$ quantization floor (±2 px at stride 4, before any model error).**

**§3 — ⚠️ TOP-DOWN POSE IS $O(\#\text{people})$ AND BOTTOM-UP IS $O(1)$, WITH THE CROSSOVER AT ~2 PEOPLE.** A crowd of 100 costs **100× for one and 1× for the other.**

**§5 — ⚠️ TRIPLET LOSS IS [[03 - Image Classification and Linear Models|ch. 03]] §7'S HINGE, ON DISTANCES — SO IT SATURATES THE SAME WAY.** With 10,000 identities there are $7.6\times10^{11}$ triplets and **almost all contribute exactly zero gradient** ⇒ **mining is mandatory, not an optimization.**

## 📘 Main Knowledge

### 1. ⚠️ Keypoints: why heatmaps beat regression

**Pose estimation = locating $K$ keypoints** (COCO uses $K=17$: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles).

**The obvious approach — regress $2K$ coordinates directly — loses, and the reason is structural.**

| | output size ($256^2$ input, $K=17$) |
|---|---|
| direct regression | $2K=\mathbf{34}$ numbers |
| **heatmap, stride 4** | $17\times64\times64=\mathbf{69{,}632}$ values — **2,048× more** |
| heatmap, stride 8 | $17\times32\times32=17{,}408$ |

> [!warning] ⚠️ THE DECIDING ARGUMENT IS MULTIMODALITY, NOT ACCURACY
> **A regressor must output one number.** When two positions are equally plausible — a partly occluded elbow that could be on either arm — it outputs their **average**:
>
> | plausible positions | regressor output |
> |---|---|
> | 0.20 and 0.80 | **0.50** |
> | 0.30 and 0.70 | **0.50** |
> | 0.45 and 0.55 | 0.50 |
>
> ⇒ ***the average of two plausible elbows is a point on neither arm.*** **A heatmap can represent both modes and let downstream logic choose**; a regressor cannot represent the ambiguity at all.
>
> **The second reason is the loss surface.** A heatmap is a **dense per-pixel classification**, so every pixel produces gradient; a coordinate regression gives one scalar residual per keypoint. *This is [[Deep Learning/contents/01 - Introduction to Deep Learning|DL ch. 01]]'s `argmax` point again — reporting a single value asserts a unimodal belief.*

> [!note] ⚠️ The price is a quantization floor
> An `argmax` over a stride-$s$ heatmap is accurate to $\pm s/2$ **before any model error**:
>
> | stride | error | as % of a 256-px image |
> |---|---|---|
> | 4 | **±2.0 px** | 0.78% |
> | 8 | ±4.0 px | 1.56% |
> | 16 | ±8.0 px | 3.12% |
>
> ⇒ **that is why sub-pixel refinement exists** — offset heads, soft-argmax, DARK. *Same structural issue as [[09 - Segmentation|ch. 09]] §6's RoI align: **quantization invisible at box precision is fatal at keypoint precision.***

**The standard architecture is an encoder–decoder that returns to high resolution** — the **stacked hourglass** (Newell et al. 2016) repeats downsample-then-upsample with skip connections, *which is [[09 - Segmentation|ch. 09]] §4's U-Net argument applied to keypoints, and for the same reason: the high-resolution features were bypassed, not destroyed.*

### 2. Pose is structured — the skeleton is a prior

**Keypoints are not independent.** Limb lengths are roughly fixed, joints have angular limits, and left/right have a consistent topology. **Models exploit this** through **part affinity fields** (OpenPose: a vector field per limb encoding direction), graph-structured refinement, or simply by predicting all keypoints jointly so the network can learn the correlations.

> [!note] ⚠️ Left/right confusion is the characteristic failure, and it is a symmetry problem
> **A person facing away has their left and right swapped in the image.** Nothing local distinguishes a left wrist from a right one — **the information is global (which way the torso faces), exactly like [[02 - Classical Image Processing|ch. 02]] §7's shadow-versus-object edge.** *A purely local keypoint detector cannot fix this, and that is why the skeleton prior is part of the model rather than post-processing.*

### 3. ⚠️ Top-down versus bottom-up — an asymptotic choice

| | method | cost |
|---|---|---|
| **top-down** | detect people, run a pose network on **each crop** | $O(\#\text{people})$ |
| **bottom-up** | detect **all** keypoints once, then **group** them | $O(1)$ |

| people | top-down | bottom-up | faster |
|---|---|---|---|
| 1 | $6.10\times10^9$ | $6.15\times10^9$ | top-down |
| **2** | $8.10\times10^9$ | $6.15\times10^9$ | **bottom-up** |
| 10 | $2.41\times10^{10}$ | $6.15\times10^9$ | bottom-up |
| 50 | $1.04\times10^{11}$ | $6.15\times10^9$ | **bottom-up (17×)** |

> [!warning] ⚠️ THE CROSSOVER IS AT ~2 PEOPLE, BUT THE ASYMPTOTICS ARE THE POINT
> **A crowd of 100 costs 100× for top-down and 1× for bottom-up.**
>
> **The trade is accuracy for scaling**: top-down gets a **full-resolution crop per person**, so it is far better on small or distant people; bottom-up runs once at fixed resolution and must then **solve a grouping problem** — which is where it fails, in exactly the crowded scenes it was chosen for.
>
> ⇒ *the choice is not "which is better" but **"how many people, and how small"*** — and it mirrors [[07 - Object Detection I|ch. 07]]'s two-stage/one-stage trade precisely: **per-instance processing buys accuracy and costs linear scaling.**

### 4. ⚠️ Faces: verification, identification, and the arithmetic that separates them

**Face *detection*** is object detection with one class — historically **Viola–Jones (2001)**, whose cascade of Haar features on integral images made real-time detection possible decades before CNNs, and which is still in `cv2`. *(Szeliski §6.3.1.)*

**Face *recognition* is two different problems**, and conflating them is the field's most consequential error:

| | question | comparisons |
|---|---|---|
| **verification (1:1)** | is this the same person? | **1** |
| **identification (1:N)** | who is this? | **$N$**, against a gallery |

**With a per-comparison false accept rate FAR, the chance of at least one false match in a gallery of $N$ is $1-(1-\mathrm{FAR})^N$:**

| FAR | $N=100$ | $N=1{,}000$ | $N=10{,}000$ | $N=10^6$ |
|---|---|---|---|---|
| $10^{-2}$ | 63.40% | 99.996% | ~100% | ~100% |
| **$10^{-3}$** | 9.52% | 63.23% | **99.995%** | ~100% |
| $10^{-4}$ | 1.00% | 9.52% | 63.21% | ~100% |
| $10^{-6}$ | 0.010% | 0.100% | 0.995% | 63.21% |
| $10^{-8}$ | 0.0001% | 0.001% | 0.010% | 0.995% |

> [!warning] ⚠️ A 0.1% FAR GIVES A **99.995%** CHANCE OF AT LEAST ONE FALSE MATCH IN A 10,000-PERSON GALLERY
> **To hold gallery-level error under 1%:**
>
> | gallery $N$ | required FAR | |
> |---|---|---|
> | 100 | $1.005\times10^{-4}$ | 1 in 9,950 |
> | 1,000 | $1.005\times10^{-5}$ | 1 in 99,500 |
> | 10,000 | $1.005\times10^{-6}$ | 1 in 994,992 |
> | **$10^6$** | $\mathbf{1.005\times10^{-8}}$ | **1 in 99,499,163** |
>
> ⇒ ***identification at city scale needs a FAR roughly four orders of magnitude better than verification.***
>
> ⚠️ **AND THIS IS THE PRACTICAL WARNING: vendors and papers usually report *verification* rates.** Quoting a verification FAR for a system that performs identification **overstates its reliability by that same four orders of magnitude** — and the errors land on people who were never in the gallery. *The mathematics is the same as the multiple-comparisons problem in [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]]: one test at $\alpha$ is fine; $N$ tests at $\alpha$ are not.*
>
> **Two further facts belong with it.** **(i) Accuracy is not uniform across demographic groups** — measured disparities in FAR by skin tone, gender and age are well documented (NIST FRVT), and a *single* headline FAR conceals them. **(ii) The base rate matters**: in a search for a rare individual, even a tiny FAR produces mostly false positives, by Bayes. **Both are reasons to report per-group FAR at a stated gallery size, not one number.**

### 5. ⚠️ Embeddings — recognition as metric learning

**The winning formulation (FaceNet, Schroff et al. 2015): map a face to a unit vector in $\mathbb R^{128}$ and compare by distance.** Classification cannot work directly — the identities at test time were not in the training set.

$$L=\max\big(0,\ \|f(a)-f(p)\|^2-\|f(a)-f(n)\|^2+\alpha\big)$$

| $d(a,p)^2$ | $d(a,n)^2$ | margin | loss |
|---|---|---|---|
| 0.20 | 1.00 | 0.2 | **0.0000** |
| 0.30 | 0.50 | 0.2 | **0.0000** |
| 0.50 | 0.60 | 0.2 | 0.1000 |
| 0.90 | 0.40 | 0.2 | 0.7000 |

> [!warning] ⚠️ THIS IS [[03 - Image Classification and Linear Models|ch. 03]] §7'S HINGE LOSS ON DISTANCES — AND IT SATURATES IDENTICALLY
> **Zero loss once the negative is a margin further than the positive**, so satisfied triplets contribute **exactly no gradient**.
>
> **And the combinatorics make that fatal:**
>
> | identities $P$ | images each | **triplets** |
> |---|---|---|
> | 100 | 10 | $8.91\times10^6$ |
> | 1,000 | 10 | $8.99\times10^8$ |
> | **10,000** | 20 | $\mathbf{7.60\times10^{11}}$ |
>
> **Almost all of $7.6\times10^{11}$ triplets are already satisfied.** ⇒ ***hard-negative mining is not an optimization, it is the only way training progresses*** — sampling uniformly means sampling zero gradient.
>
> *This is the exact structure [[03 - Image Classification and Linear Models|ch. 03]] §7 found ("with the hinge, a model that separates the data stops learning") and [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8 found in detection. **Third setting for the same failure**, and the fixes rhyme: mining here, focal loss there.*

**ArcFace (Deng et al. 2019) took the other route**: keep a softmax classifier over training identities but **impose an angular margin on the logits**, so the classes are pushed apart on the hypersphere. **It avoids triplet mining entirely** by making every example contribute — *the same move as replacing the hinge with cross-entropy in [[03 - Image Classification and Linear Models|ch. 03]] §7.*

## ✏️ Exercises

> [!example]- Exercise 1 — heatmaps versus regression
> **(a)** Output sizes for $K=17$ at $256^2$: direct regression vs stride-4 heatmap. **(b)** Quantization error at strides 4, 8, 16. **(c)** Why do heatmaps win despite being 2,048× larger? **(d)** What is the cost?
>
> ---
> **(a)** $2\times17=\mathbf{34}$ numbers vs $17\times64^2=\mathbf{69{,}632}$ — **2,048×**.
>
> **(b)** $\pm s/2$: **±2 px, ±4 px, ±8 px** — 0.78%, 1.56%, 3.12% of the image, **before any model error.**
>
> **(c)** ⚠️ **Two reasons. (i) Multimodality**: a regressor must output one number, so two equally plausible elbow positions at 0.2 and 0.8 give **0.5 — a point on neither arm.** A heatmap represents both. **(ii) Gradient density**: a heatmap is a dense per-pixel classification, so every pixel contributes; a regression gives one residual.
>
> **(d)** The quantization floor, plus memory and compute for a high-resolution decoder — **which is why sub-pixel refinement (offset heads, soft-argmax) is standard**, and the same issue as RoI align in [[09 - Segmentation|ch. 09]] §6.

> [!example]- Exercise 2 — top-down or bottom-up
> Detector $4.1\times10^9$ ops; per-person pose net $2.0\times10^9$; bottom-up $1.5\times$ the detector.
> **(a)** Costs at 1, 10, 50 people. **(b)** Crossover. **(c)** Why is bottom-up not always chosen? **(d)** What does it mirror?
>
> ---
> **(a)** Top-down $4.1\times10^9+p\times2.0\times10^9$: **$6.1\times10^9$, $2.41\times10^{10}$, $1.04\times10^{11}$.** Bottom-up **$6.15\times10^9$ regardless.**
>
> **(b)** ~**2 people**. At 50 people bottom-up is **17× faster**; at 100 the ratio is ~33×.
>
> **(c)** ⚠️ **Top-down gets a full-resolution crop per person**, so it is far more accurate on small or distant people; bottom-up runs once at fixed resolution and must then **group** keypoints into individuals — **and grouping fails exactly in the crowded scenes bottom-up was chosen for.**
>
> **(d)** **[[07 - Object Detection I|Ch. 07]]'s two-stage/one-stage trade.** *Per-instance processing buys accuracy and costs linear scaling* — the same structure, in a different task.

> [!example]- Exercise 3 — verification versus identification
> A system reports FAR $=0.1\%$. **(a)** Chance of a false match in galleries of 100, 10,000, $10^6$. **(b)** Required FAR to keep gallery error under 1% at $N=10^6$. **(c)** What does that mean for a reported number? **(d)** What else should be reported?
>
> ---
> **(a)** $1-(1-10^{-3})^N$: **9.52%**, **99.995%**, **~100%**.
>
> **(b)** $1-0.99^{1/N}=\mathbf{1.005\times10^{-8}}$ — **one in 99.5 million**, about **$10^5\times$ stricter** than the quoted 0.1%.
>
> **(c)** ⚠️ **A verification FAR quoted for an identification system overstates reliability by roughly four orders of magnitude.** The failures are false accusations of people who were never in the gallery — **and it is the same multiple-comparisons arithmetic as running $N$ hypothesis tests at level $\alpha$.**
>
> **(d)** **FAR at the actual gallery size**, **per demographic group** (measured disparities in FAR by skin tone, gender and age are documented, and one headline number conceals them), **and the base rate** — searching for a rare individual yields mostly false positives however good the FAR.

> [!example]- Exercise 4 — triplet loss
> **(a)** Loss for $d(a,p)^2=0.3$, $d(a,n)^2=0.5$, margin 0.2. **(b)** How many triplets for 10,000 identities × 20 images? **(c)** What fraction contribute gradient late in training? **(d)** What does this rhyme with, and what is the alternative?
>
> ---
> **(a)** $\max(0,\ 0.3-0.5+0.2)=\mathbf{0}$ — the margin is **exactly** met, so no gradient.
>
> **(b)** $200{,}000$ anchors $\times\,19$ positives $\times\,199{,}980$ negatives $=\mathbf{7.60\times10^{11}}$.
>
> **(c)** ⚠️ **Almost none.** Once the embedding is decent the overwhelming majority satisfy the margin and give exactly zero. **Sampling uniformly from $7.6\times10^{11}$ triplets means sampling zero gradient** ⇒ **hard-negative mining is the only way training progresses.**
>
> **(d)** **[[03 - Image Classification and Linear Models|Ch. 03]] §7's hinge saturation** ("a model that separates the data stops learning") and **[[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8's detection imbalance** — *third setting for one failure.* **The alternative is ArcFace**: an angular-margin softmax where every example contributes — **the same move as replacing the hinge with cross-entropy.**

## 📝 Summary

- **Pose estimation locates $K$ keypoints** (COCO: 17), and **heatmaps beat direct regression** despite being **2,048× larger** — because **a regressor must average its modes** (two plausible elbows at 0.2 and 0.8 give 0.5, on neither arm) and because a dense map gives gradient everywhere.
- **⚠️ The price is a $\pm s/2$ quantization floor** — ±2 px at stride 4 before any model error — **hence sub-pixel refinement**, the same issue as RoI align in [[09 - Segmentation|ch. 09]].
- **Keypoints are not independent**: limb lengths, joint limits and topology are priors that models encode via part affinity fields or joint prediction. **Left/right confusion is the characteristic failure and is a global-information problem**, like the shadow-versus-object edge.
- **⚠️ Top-down pose is $O(\#\text{people})$, bottom-up is $O(1)$, crossover ~2 people** — 17× at 50 people. **Top-down buys accuracy on small people; bottom-up must group, and grouping fails in crowds.** Same trade as two-stage vs one-stage detection.
- **⚠️ Verification (1:1) and identification (1:N) are different problems.** With FAR $=10^{-3}$, the chance of at least one false match is **9.52% at $N=100$ and 99.995% at $N=10{,}000$.** **Gallery error under 1% at $N=10^6$ requires FAR $\le1.005\times10^{-8}$ — four orders stricter.** ⇒ **quoting a verification rate for an identification system overstates it by that much**, and per-group FAR and base rates must be reported too.
- **⚠️ Recognition is metric learning**: map to a unit vector, compare by distance. **Triplet loss is [[03 - Image Classification and Linear Models|ch. 03]] §7's hinge on distances and saturates identically** — with $7.6\times10^{11}$ triplets at 10,000 identities, **almost all give zero gradient, so mining is mandatory.** **ArcFace avoids it** with an angular-margin softmax where every example contributes.

## ⚠️ Important Notes

1. **⚠️ Never quote a verification FAR for an identification system.** The gap is ~4 orders of magnitude at city scale. **State the gallery size with every FAR.**
2. **⚠️ Report FAR per demographic group.** Disparities by skin tone, gender and age are documented (NIST FRVT); **a single headline number conceals exactly the failure mode that matters.**
3. **⚠️ Remember the base rate.** Searching a large population for a rare individual produces mostly false positives even at an excellent FAR — **Bayes, not model quality.**
4. **⚠️ Heatmap stride is a hard accuracy floor.** ±2 px at stride 4. **If keypoint error plateaus near $s/2$, the fix is sub-pixel refinement or a finer stride, not more training.**
5. **⚠️ Triplet mining is not optional.** Uniform sampling from $7.6\times10^{11}$ triplets samples zero gradient. **If a metric-learning model "stops improving early", check whether any triplets are still active** — [[03 - Image Classification and Linear Models|ch. 03]] §7's hinge saturation, third occurrence.
6. **⚠️ A pose regressor's confident output can be a point that is nowhere on the person.** Averaging two modes produces a physically impossible skeleton. **Check limb lengths as a sanity test** — the skeleton prior is also a validator.
7. **⚠️ Top-down pose inherits every detection failure.** A missed person is a missed pose, and mAP on the detector bounds the pose result. **Diagnose the detector first.**
8. **Face recognition is dual-use, and the technical facts above are the ones that matter for its governance**: identification compounds errors with gallery size, accuracy varies by group, and base rates dominate in search. **Any deployment claim should state gallery size, per-group FAR and base rate** — a system reported only as "99.9% accurate" has not been described.

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). Built from **Szeliski §6.2.4 (face recognition), §6.3.1 (face detection), §6.4.5 (pose estimation)** — all brief — plus the **stacked hourglass (Newell et al. 2016)**, **OpenPose (Cao et al. 2017)**, **FaceNet (Schroff et al. 2015)**, **ArcFace (Deng et al. 2019)**, and CS231n.
>
> **⚠️ The emphasis is inferred.** The lecturer's topic title is *"Pose estimation & faces"* and nothing more. **Pairing them in one week suggests the shared theme is keypoints and landmarks**, which is how this chapter is organized — but whether week 10 emphasizes pose, faces, or the recognition/ethics material is unknown. **Facial landmark detection specifically (as opposed to body pose) is treated only implicitly.**
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§4's entire FAR-compounding analysis** — the $1-(1-\mathrm{FAR})^N$ table, the required-FAR inversion, and the "four orders of magnitude" conclusion. *That verification and identification differ is standard; **quantifying the gap and connecting it to the multiple-comparisons problem is mine**.*
> - **§1's mode-averaging demonstration** (0.2 and 0.8 → 0.5) and the quantization-floor table, with the link to RoI align.
> - **§3's cost table and the ~2-person crossover**, and the identification of the trade with [[07 - Object Detection I|ch. 07]]'s two-stage/one-stage structure.
> - **§5's triplet count** ($7.6\times10^{11}$ at 10,000 identities) and **the identification of triplet loss as [[03 - Image Classification and Linear Models|ch. 03]] §7's hinge on distances**, making mining a necessity rather than an optimization — **third setting for the same saturation failure.**
> - **All eight Important Notes.**
>
> ⚠️ **The FLOP figures in §3 ($4.1\times10^9$ detector, $2.0\times10^9$ pose net) are representative round numbers used to demonstrate the scaling argument, not measurements** — the crossover's *existence* and the $O(\#\text{people})$ vs $O(1)$ asymptotics are the finding, not the precise crossover value. **No accuracy figures from any paper are quoted.**
>
> ⚠️ **The demographic-disparity and base-rate points in §4 and Important Notes 2, 3 and 8 are stated qualitatively and attributed to NIST FRVT** rather than quoting numbers, because those results are external, version-dependent, and this chapter cannot verify them. **They are included because the arithmetic of §4 is incomplete without them** — a single FAR is not a description of an identification system.
>
> **No discrepancies found.**
>
> **Deliberately deferred, not omitted:** **Viola–Jones in detail** (Haar features, integral images, the attentional cascade) is summarized in one sentence — *it would repay a section if the course covers classical face detection, and its integral-image trick belongs naturally with [[02 - Classical Image Processing|ch. 02]].* **3D and multi-person 3D pose** are [[14 - 3D Vision and Emerging Topics|ch. 14]]. **Face generation and morphing** are [[13 - Generative Models|ch. 13]]. **Tracking people across frames** is [[11 - Video and Motion|ch. 11]]. **Contrastive learning in general** — of which triplet loss is an ancestor — is [[12 - Self-Supervised Learning|ch. 12]].
>
> **Left as the source states it:** COCO's 17-keypoint convention; the stacked-hourglass and OpenPose architectures; FaceNet's 128-dimensional embedding; ArcFace's angular margin formulation; Viola–Jones's 2001 date and its presence in OpenCV; and NIST FRVT's demographic findings.

**Previous:** [[09 - Segmentation]] · **Next:** [[11 - Video and Motion]]
