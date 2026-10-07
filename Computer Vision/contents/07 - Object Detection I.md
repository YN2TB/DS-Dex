---
subject: Computer Vision
chapter: 7
tags: [ds, computer-vision, object-detection, iou, average-precision, nms, r-cnn, faster-r-cnn, anchors, rpn, fpn]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 07: Object Detection I (53 slides); Girshick et al. 2014 (R-CNN), Girshick 2015 (Fast R-CNN), Ren et al. 2015 (Faster R-CNN), Lin et al. 2017 (FPN)"
---

# Object Detection I

Week 7. Every model so far outputs one fixed-length vector per image. Detection must say **how many** objects there are, **where** each one is, and **what** each one is. This lecture covers the problem, how detectors are scored (IoU, AP, NMS), the classical detectors, the two-stage R-CNN family up to Faster R-CNN, and the feature pyramid (FPN) for handling scale.

[[Deep Learning/contents/06 - Object Detection|DL ch. 06]] covers anchors, IoU, NMS, SSD and the R-CNN family from the D2L textbook, with code-level detail.

## 📘 Main Knowledge

### 1. What detection asks for (slides 3–9)

**Why it's hard for supervised learning (slide 4).** Supervised learning needs a fixed-size target and a differentiable loss. A *set* of objects of variable size has neither, and has no natural ordering.

**Formulation (slide 7).** Given an image $I$, return a set of boxes, classes and scores:

$$\mathcal D = \{(b_k, c_k, s_k)\}_{k=1}^{K}, \qquad b_k \in \mathbb R^4,\ c_k \in \{1,\dots,C\},\ s_k \in [0,1]$$

$K$ isn't known in advance. What breaks:
- there's no fixed-size output tensor;
- there's no natural order, so you can't compare predictions to ground truth element by element;
- two predictions of the same object must be penalised, but a per-prediction loss can't see the other prediction.

**The universal workaround (slide 8).** Predict a **fixed, dense set of candidates** (one per window, proposal or anchor), give each a class (including "background") and a box correction, then **prune** at test time. Detection becomes classification plus regression on a set we chose ourselves; the set-valued difficulty moves to post-processing.

**Box encodings (slide 9).** Three ways to write the same box:

| Encoding | Used by |
|---|---|
| Corners $(x_1, y_1, x_2, y_2)$ | what most datasets store |
| Corner–size $(x, y, w, h)$ | COCO annotation format |
| Centre–size $(c_x, c_y, w, h)$ | what networks regress |

Axis-aligned boxes are cheap to annotate and compare, but a poor fit for rotated or articulated objects. Segmentation ([[09 - Segmentation|ch. 09]]) removes that approximation.

### 2. Classical detectors (slides 10–13)

**The obvious idea: sliding window (slide 10).** Run an image classifier on every window. On a 224×224 image, one 64×64 window at stride 1 gives $(224 - 64 + 1)^2 = 161^2 \approx 26{,}000$ crops. With three scales and three aspect ratios, about 230,000. At VGG-16's ~15.5 GFLOPs per crop that's about 3.6 PFLOPs ($3.6 \times 10^{15}$ operations), minutes of GPU time for one small image.

*Detection isn't hard because classification is hard. It's hard because the **search space** is enormous*, and every idea that follows shrinks it.

**Viola–Jones (2001) (slide 11)**, the classic face detector:
- A feature is the sum of pixels in one rectangle minus the sum in another (Haar-like features).
- The **integral image** (each entry stores the sum of all pixels above and to the left) makes any rectangle sum four lookups, at a cost independent of the rectangle's size.
- **AdaBoost** picks a few thousand features and arranges them into a **cascade**: cheap stages first, each rejecting most of the remaining windows.
- First appearance of the key idea: *don't spend equal compute on every window.*

**HOG + linear SVM (2005) (slide 12).** From [[02 - Classical Image Processing|ch. 02]]. Orientation histograms discard absolute intensity, so the descriptor survives lighting changes. A *linear* SVM makes scoring one window a dot product, and scoring a whole image pyramid a convolution. Limit: one rigid template per class (a sitting person and a standing person need different templates).

**Deformable Part Models (DPM, 2008–2010) (slide 13).** A coarse **root filter** plus finer **part filters**, each tied to the root by a "spring": parts can move, and the deformation costs score. Part locations are never annotated, so training (**latent SVM**) alternates between inferring them and refitting the weights, with **hard negative mining** (retraining on the negatives the model currently gets wrong).

All three spend almost nothing on windows that contain nothing. *A two-stage detector is that idea with learned features instead of designed ones.*

### 3. How a detector is scored (slides 14–21)

**Intersection over Union (IoU) (slide 15)** measures box overlap:

$$\text{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

IoU 0.5 is a visibly sloppy box, 0.75 looks right, 0.9 is near-perfect. Example: two 10×10 boxes offset by one pixel in each direction, $(0,0,10,10)$ and $(1,1,11,11)$, overlap in 81 px² with union 119 px²: IoU = 0.68.

**TP, FP, FN (slide 16).** At an IoU threshold (historically 0.5, chosen by convention, not derived):
- **True positive (TP):** a prediction that correctly finds and localises an object.
- **False positive (FP):** a prediction where there's no object (or a duplicate, see below).
- **False negative (FN):** an object the model missed.
- True negatives (correctly predicting nothing) aren't counted in detection: there are infinitely many empty boxes.

**Matching predictions to ground truth (slide 17).** For one class, sort all predictions by confidence and go down the list, matching each to the highest-IoU ground-truth box that hasn't been claimed yet (and has IoU above the threshold). Consequence: **a second, slightly worse box on an object you already found is a false positive.** Duplicates are punished exactly like hallucinations, which is why NMS isn't cosmetic.

**Average precision (AP) (slide 18).** Walking down the sorted list traces a precision–recall curve: each TP raises recall, each FP lowers precision.

$$P = \frac{TP}{TP + FP}, \qquad R = \frac{TP}{TP + FN}$$

AP is the area under the **interpolated** curve:

$$\text{AP} = \int_0^1 p_{interp}(r)\, dr, \qquad p_{interp}(r) = \max_{r' \ge r} p(r')$$

and **mAP** is AP averaged over the $C$ classes.
- Interpolation removes the sawtooth so the metric doesn't reward lucky orderings.
- Confidence scores only enter AP through the **ranking**: AP measures ordering, not calibration.

**Worked AP example** (one class, 5 ground-truth objects, 8 predictions sorted by score):

| Rank | Result | TP so far | Precision | Recall |
|---|---|---|---|---|
| 1 | TP | 1 | 1.000 | 0.2 |
| 2 | TP | 2 | 1.000 | 0.4 |
| 3 | FP | 2 | 0.667 | 0.4 |
| 4 | TP | 3 | 0.750 | 0.6 |
| 5 | FP | 3 | 0.600 | 0.6 |
| 6 | TP | 4 | 0.667 | 0.8 |
| 7 | FP | 4 | 0.571 | 0.8 |
| 8 | FP | 4 | 0.500 | 0.8 |

Interpolated precision (best precision at this recall or higher): 1.0 up to recall 0.4, 0.75 up to 0.6, 0.667 up to 0.8, then 0 (recall never reaches 1).
- **All-point AP** (area under the step curve): $0.2(1) + 0.2(1) + 0.2(0.75) + 0.2(0.667) = 0.683$.
- **11-point AP** (VOC 2007: average of the interpolated precision at recall 0, 0.1, …, 1.0): $(5 \times 1 + 2 \times 0.75 + 2 \times 0.667 + 2 \times 0)/11 = 0.712$.
- **101-point AP** (COCO): 0.686.

Same detections, three numbers (a 4% spread) from the convention alone. And one object was never found, so recall stops at 0.8 and **AP can't exceed 0.8** however well the predictions are ranked.

**Two protocols you'll meet (slide 19):**

| | PASCAL VOC | COCO |
|---|---|---|
| Classes | 20 | 80 |
| IoU threshold | 0.5, fixed | averaged over 0.50, 0.55, …, 0.95 |
| Headline number | mAP@0.5 | AP (often written mAP) |
| Interpolation | 11-point (2007), then all-point | 101-point |
| Also reported | — | AP₅₀, AP₇₅, AP_S/M/L, AR |

- COCO's average over IoU thresholds makes **localisation quality** part of the score. A detector that finds everything with sloppy boxes scores well on AP₅₀ and poorly on AP₇₅.
- **AP_S** (small objects, area < 32² px) is where almost every detector is weakest; FPN (§6) exists to fix it.
- *"40 mAP" means nothing until you know the protocol.* COCO AP ≈ 40 and VOC mAP@0.5 ≈ 40 are worlds apart.

**Non-maximum suppression (NMS) (slide 20).** A dense candidate set guarantees one object triggers many candidates. NMS removes them greedily, per class:
1. Sort the remaining boxes by score.
2. Keep the top one.
3. Discard every box with IoU > $\tau_{nms}$ against it.
4. Repeat on what remains.

Typical $\tau_{nms}$: 0.7 for region proposals (keep recall), 0.5 for final detections (remove duplicates).

**Where NMS fails (slide 21).**
- **Two objects, one survivor.** Nothing distinguishes "two boxes on one object" from "two boxes on two overlapping objects" except image content, which NMS never looks at. Raising $\tau_{nms}$ keeps the second object but lets duplicates through; lowering it does the reverse. Crowds are the classic failure.
- **It isn't learned.** A hand-written, non-differentiable step at the end of an otherwise end-to-end pipeline, with a threshold you tune on validation data.
- **Soft-NMS** lowers the scores of overlapping boxes instead of deleting them. **DETR** ([[08 - Object Detection II|ch. 08]]) removes the step entirely by making the loss handle duplicates.

### 4. Proposals: the R-CNN family (slides 22–31)

**Selective search (Uijlings et al., 2013) (slides 23–24).** Start from a graph-based over-segmentation (Felzenszwalb & Huttenlocher) and repeatedly score every pair of neighbouring regions, merge the most similar pair, and add the new region to the set. Similarity:

$$s(r_i, r_j) = a_1 s_{colour} + a_2 s_{texture} + a_3 s_{size} + a_4 s_{fill}$$

- colour, texture: histogram intersection;
- size: small regions merge first, so merging stays even in scale;
- fill: prefer unions that fill their bounding box.

Output: about **2,000 proposals** per image, class-agnostic and not learned, at ~2 s per image on CPU. Objects are almost always *somewhere* in the set, though rarely framed exactly. Division of labour: **recall** becomes the proposal generator's job, **precision** the classifier's. Every two-stage detector keeps this split.

**R-CNN (Girshick et al., 2014) (slides 25–27).** Warp each proposal to a fixed size, run a CNN on it, classify the features with per-class SVMs, and refine the box with a regressor.
- VOC 2007 mAP: 33.7% (DPM) → 58.5% with AlexNet features → **66.0% with VGG-16**. A ~30-point jump from replacing the features and nothing else.
- Brought **pretrain-on-ImageNet, fine-tune-on-target** to detection: the transfer recipe now used everywhere.

**Separate losses (slide 26).** SVM classification:
$$L_{SVM} = \tfrac12 \|w\|_2^2 + C \sum_{i=1}^{N} \max\big(0,\ 1 - y_i(w^\top f_i + b)\big)$$

**Bounding-box regression.** Given a reference box (anchor or proposal) $(x_a, y_a, w_a, h_a)$ and a target $(x, y, w, h)$ (centre–size), the regressor predicts $t_i = W^\top f_i$ to match:

$$t^* = \left( \frac{x - x_a}{w_a},\ \frac{y - y_a}{h_a},\ \log\frac{w}{w_a},\ \log\frac{h}{h_a} \right)$$

- Centre offsets are divided by the reference size, so the target is **scale-invariant** (the same relative shift means the same $t$ for small and large boxes).
- Width and height use a **log ratio**, so predictions stay positive when decoded and scaling up and down are symmetric.
- Loss over positive boxes $\mathcal P$: $L_{bbox} = \sum_{i \in \mathcal P} \|t_i - t_i^*\|_2^2$.

**Three things wrong with R-CNN (slide 27):**
1. **Hopelessly slow:** 2,000 independent CNN forward passes per image on overlapping crops, ≈47 s per image at test time with VGG-16.
2. **Not one model:** the CNN, SVMs and regressors are trained separately; no signal from the SVMs reaches the CNN.
3. **Warping:** every proposal is squashed to a square, destroying its aspect ratio before the network sees it.

The next four years of detection research removed these three defects one at a time.

**Fast R-CNN (Girshick, 2015): share the convolution (slides 28–31).** Run the backbone **once** on the whole image. Project each proposal onto the resulting feature map and crop there, not in pixel space.
- **RoI pooling** turns any region into a fixed 7×7×$C$ tensor, so the head can be a plain MLP. Divide the projected region into a fixed grid (e.g. 7×7 bins) and max-pool inside each bin.
- Two sibling heads: softmax over $C + 1$ classes (including background), and $4C$ box offsets (one set per class).
- One network, one loss, trained end to end, except for the proposals.

**Multi-task loss (slide 30).** For a region of interest (RoI) with true class $u$ and true offsets $v$:

$$L(p, u, t^u, v) = L_{cls}(p, u) + \lambda\, [u \ge 1]\, L_{loc}(t^u, v), \qquad L_{cls} = -\log p_u$$

$$L_{loc}(t^u, v) = \sum_{j \in \{x,y,w,h\}} \text{smooth}_{L1}(t_j^u - v_j), \qquad \text{smooth}_{L1}(z) = \begin{cases} 0.5 z^2 & |z| < 1 \\ |z| - 0.5 & \text{otherwise} \end{cases}$$

- $[u \ge 1]$ is 1 for object classes and 0 for background (label 0): **background RoIs get no box loss** (there's no box to regress to).
- Smooth L1 is quadratic near zero (smooth optimum) and linear far out, so one badly placed RoI can't dominate the gradient. E.g. an error of 3 costs 2.5 instead of L2's 4.5.

**The payoff:** test time fell from 47 s to 0.32 s per image for the network (≈147×; the paper's "213×" uses a further speed-up, truncated SVD of the FC layers, to reach 0.22 s), training 9× faster, and mAP up to **70.0%** (VOC 07+12).

### 5. Faster R-CNN: learning the proposals (slides 32–41)

**The remaining bottleneck isn't the network (slide 33).** Fast R-CNN per image: network ≈ 0.32 s, selective search ≈ 2 s. Over 85% of the time goes to a hand-designed CPU algorithm that learns nothing. And it ignores the rich feature map the backbone has already computed: proposals should come from those features, and be learned.

**Faster R-CNN (Ren et al., 2015)** replaces selective search with a **Region Proposal Network (RPN)** that shares the backbone's features.

**Anchors (slide 35).** At every location of the feature map, place $k$ reference boxes of fixed size and shape.
- Three scales $\{128, 256, 512\}$ × three aspect ratios $\{1{:}2, 1{:}1, 2{:}1\}$ (in original-image pixels) = $k = 9$.
- A 40×60 feature map with $k = 9$ gives about 20,000 anchors: a dense, fixed-size candidate set.
- The network never invents a box from nothing; it only says *is there an object near this anchor* and *how should this anchor move*.
- Translation-invariant by construction: the same $k$ predictors are applied at every location.
- Anchors replace the image pyramid with a **pyramid of reference shapes** at one feature scale. Every detector until about 2019 was built on this idea.

**The RPN (slides 36–37).** A small head slid over the shared feature map: one 3×3 conv, then two sibling 1×1 convs giving, per location:
- $2k$ **objectness** scores (object vs background, class-agnostic);
- $4k$ box offsets, one set per anchor, in the $(t_x, t_y, t_w, t_h)$ form above.

The top $N$ proposals after NMS at 0.7 ($N = 300$ at test time) go to the Fast R-CNN head. Cost ≈ 10 ms, about 200× faster than selective search, because it reuses features the detector needs anyway.

*Two stages, one backbone: the RPN asks **where**, the head asks **what**.* Coarse to fine, a descendant of Viola–Jones' cascade.

**What the RPN is trained on (slide 38).** Label each anchor:
- **positive** if IoU > 0.7 with some ground-truth box, *or* if it's the best anchor for a ground-truth box that nothing else claims;
- **negative** if IoU < 0.3 with every ground-truth box;
- otherwise **ignored** (no gradient).

$$L = \frac{1}{N_{cls}} \sum_i L_{cls}(p_i, p_i^*) + \lambda \frac{1}{N_{reg}} \sum_i p_i^*\, \text{smooth}_{L1}(t_i - t_i^*)$$

$p_i^*$ (1 for positive anchors, 0 otherwise) switches the regression term on only for positives. Of ~20,000 anchors only a handful are positive, so the loss would be almost entirely background. Faster R-CNN therefore **samples 256 anchors per image, up to half positive**.

**Foreground–background imbalance (slide 39).** Any dense candidate set is overwhelmingly background; ratios of 1000:1 are normal. Easy negatives dominate the summed loss, and the gradient keeps pointing at "predict background" long after that's useful. Two-stage detectors escape this:
- the RPN discards almost all background before the expensive head runs;
- fixed sampling ratios per minibatch (RPN 1:1, head 1:3 positive:negative);
- hard negative mining.

A one-stage detector has no proposal step, so it faces the full imbalance head-on. That's why **focal loss** exists ([[08 - Object Detection II|ch. 08]]).

**The R-CNN family, measured (slide 40):**

| Method | Proposals | VOC07 mAP | Test time / image | Training |
|---|---|---|---|---|
| DPM v5 | sliding window | 33.7 | ≈14 s | one model |
| R-CNN (VGG-16) | selective search | 66.0 | ≈47 s | 3 stages, cached features |
| Fast R-CNN | selective search | 70.0 | 2.3 s (0.32 s network) | 1 stage, fixed proposals |
| Faster R-CNN | learned (RPN) | 73.2 | 0.2 s | fully end to end |

(Fast and Faster R-CNN trained on VOC 07+12; Faster R-CNN runs at ≈5 fps with VGG-16 and 300 proposals.)

Accuracy went **up** at every step while the pipeline got **simpler**. Each generation absorbed one hand-designed component into the network: the classifier, then the crop, then the proposals.

### 6. Scale: the feature pyramid (slides 42–47)

**The problem Faster R-CNN didn't solve (slide 43).** Everything above runs on a single feature map at stride 16 or 32.
- A 32×32 object covers 2×2 cells at stride 16, and one cell at stride 32.
- After RoI pooling to 7×7, most of those "features" are interpolation.
- COCO is full of small objects, and AP_S is reported separately precisely because everyone was failing at it.

Deep layers are **semantically strong but spatially coarse**; early layers are the reverse. Detection needs both.

**Four ways to handle scale (slides 44–45):**

| Approach | How | Trade-off |
|---|---|---|
| (a) Image pyramid | resize the image, run the detector on each size | accurate, but $k\times$ the cost |
| (b) Single feature map | Faster R-CNN | fast, one scale, weak on small objects |
| (c) Feature hierarchy | predict from several backbone levels (SSD) | free, but shallow levels have weak semantics |
| (d) **FPN** | build a pyramid where **every** level is semantically strong | a few % extra cost |

**Feature Pyramid Networks (Lin et al., 2017) (slide 46).** Take the backbone's levels (strides 4, 8, 16, 32). Add a **top-down path**: start from the deepest, most semantic map and repeatedly upsample by 2×. At each level add a **lateral connection**: a 1×1 conv of the backbone map at that resolution, summed with the upsampled map, then a 3×3 conv to smooth the result. Every output level now has the deep layers' semantics *and* its own resolution. Cost: a few percent over the plain backbone (no extra image passes, only 1×1 and 3×3 convs on existing maps).

**What FPN bought (slide 47).** Faster R-CNN with FPN on ResNet-101 reached **36.2 AP** on COCO test-dev, ahead of the 2016 COCO competition winners, from a single model.
- The gain is concentrated in **AP_S**: small objects are what a single coarse map was losing.
- Proposal recall improves too, so the effect appears in both stages.
- **Ablations:** the top-down path without laterals, or laterals without the top-down path, each give back most of the gain. *Resolution without semantics detects nothing; semantics without resolution can't localise.*

FPN became a component rather than a detector: nearly every detector after 2017 (one-stage, two-stage, anchor-free) has a pyramid "neck". Swin's hierarchy ([[06 - Vision Transformers|ch. 06]]) exists to feed one.

### 7. Taking stock (slides 48–50)

**What two-stage detection actually is (slide 49):**
1. **Backbone** (weeks 5–6, unchanged).
2. **Neck**: FPN, fusing scales.
3. **Head**: classify and refine each candidate.
4. **Assignment + NMS**: the non-learned glue.

Still hand-designed: anchor scales and aspect ratios; IoU thresholds for positives and negatives; sampling ratios; the NMS threshold. Next week attacks this list: one-stage detectors remove the proposal stage, anchor-free detectors remove the anchors, DETR removes the assignment heuristics and NMS.

**For the final project (slide 50):**

| Situation | Reach for |
|---|---|
| a first working baseline, any dataset | a pretrained detector, fine-tuned. Always. |
| small objects, aerial or traffic imagery | FPN neck, higher input resolution, tile the image |
| accuracy matters more than latency | two-stage with FPN (Faster R-CNN, Cascade R-CNN) |
| real-time or embedded | one-stage ([[08 - Object Detection II|ch. 08]]) |
| a few hundred annotated images | freeze the backbone, train the heads only |

Before touching the architecture, check your annotations, your box convention and your input resolution; in student projects these cost far more AP than the choice of detector. **Report COCO AP together with AP₅₀, AP₇₅ and AP_S**: one headline number hides which half of the problem you failed.

**Hands-on (slide 53):** vectorised IoU; greedy matching and the PR curve by hand; 11-point vs all-point AP; NMS from scratch and a $\tau_{nms}$ sweep; generate the 9 anchors and count them for a 600×800 image (≈17,000 at stride 16); encode/decode $(t_x, t_y, t_w, t_h)$; fine-tune a pretrained Faster R-CNN; report AP, AP₅₀, AP₇₅, AP_S. (`torchvision.models.detection` — `anchor_utils.py`, `rpn.py`, `roi_heads.py` — maps onto the equations here.)

## ✏️ Exercises

> [!example]- Exercise 1 — IoU and matching
> Ground truth: one car at $G = (0, 0, 10, 10)$ (corners). Three predictions for "car":
> $A = (1, 1, 11, 11)$ score 0.9; $B = (2, 0, 12, 10)$ score 0.8; $C = (0, 0, 4, 4)$ score 0.6.
> **(a)** Compute the IoU of each with $G$.
> **(b)** At IoU threshold 0.5, label each prediction TP or FP.
> **(c)** What are precision and recall for this image?
> **(d)** If the detector only output $A$, what would they be?
>
> ---
> **(a)**
> - $A$: overlap $9 \times 9 = 81$, union $100 + 100 - 81 = 119$, IoU = 0.68.
> - $B$: overlap $8 \times 10 = 80$, union 120, IoU = 0.67.
> - $C$: overlap 16, union $100 + 16 - 16 = 100$, IoU = 0.16.
>
> **(b)** Go down by score. $A$ (0.9): IoU 0.68 ≥ 0.5 and $G$ unclaimed → **TP**, $G$ is now claimed. $B$ (0.8): IoU 0.67, but $G$ is already claimed → **FP** (duplicate). $C$: IoU 0.16 < 0.5 → **FP**.
>
> **(c)** Precision $= 1/3$, recall $= 1/1 = 1$.
>
> **(d)** Precision 1, recall 1. The duplicate $B$ is a good box, yet it costs as much as a hallucination. That's why NMS (which would remove $B$, since IoU($A$, $B$) = 0.68 > 0.5) is part of the algorithm.

> [!example]- Exercise 2 — Compute AP
> A detector produces 8 "person" predictions on a test set containing 5 people. Sorted by score, the results are: TP, TP, FP, TP, FP, TP, FP, FP.
> **(a)** Compute precision and recall after each prediction.
> **(b)** Compute all-point interpolated AP and 11-point AP.
> **(c)** Swapping the scores of predictions 3 and 4 (so the TP comes before the FP), what happens to all-point AP?
> **(d)** What's the maximum AP this detector could get by re-ranking its 8 predictions, and why?
>
> ---
> **(a)** P: 1, 1, 0.667, 0.75, 0.6, 0.667, 0.571, 0.5. R: 0.2, 0.4, 0.4, 0.6, 0.6, 0.8, 0.8, 0.8.
>
> **(b)** Interpolated precision: 1.0 for recall ≤ 0.4, 0.75 for (0.4, 0.6], 0.667 for (0.6, 0.8], 0 above. All-point: $0.2 + 0.2 + 0.15 + 0.133 = $ **0.683**. 11-point: recall levels 0–0.4 → 1 (five levels), 0.5–0.6 → 0.75, 0.7–0.8 → 0.667, 0.9–1.0 → 0. $(5 + 1.5 + 1.333)/11 = $ **0.712**.
>
> **(c)** New order TP, TP, TP, FP, FP, TP, FP, FP. Precision at recall 0.6 becomes 1.0, so interpolated precision is 1 up to recall 0.6 and 0.667 up to 0.8: AP $= 0.6 + 0.133 = $ **0.733**. Only the order changed, not any box, which shows AP measures ranking.
>
> **(d)** Put all 4 TPs first: precision 1 up to recall 0.8, so AP = **0.8**. One person was never detected, so recall can't pass 0.8. Misses cap AP and can't be fixed by re-ranking.

> [!example]- Exercise 3 — NMS thresholds
> Boxes for class "person" (corners, score): $A = (0,0,10,10)$ 0.9; $B = (1,1,11,11)$ 0.8; $C = (20,20,30,30)$ 0.7; $D = (2,0,12,10)$ 0.6. Pairwise IoUs: $A$–$B$ 0.68, $A$–$D$ 0.67, $B$–$D$ 0.68, everything with $C$ = 0.
> **(a)** Run NMS with $\tau = 0.5$. Which boxes survive?
> **(b)** Run NMS with $\tau = 0.7$.
> **(c)** Suppose $A$ and $B$ are actually two different people standing very close together. Which threshold gives the right answer? Is there a threshold that handles both this case and the duplicate case?
>
> ---
> **(a)** Keep $A$ (0.9). Remove $B$ (0.68 > 0.5) and $D$ (0.67 > 0.5). $C$ doesn't overlap, keep. Survivors: **$A$, $C$**.
>
> **(b)** Keep $A$. $B$: 0.68 < 0.7, stays. $D$: 0.67 < 0.7, stays. Next highest, $B$: $D$ vs $B$ 0.68 < 0.7, stays. $C$ stays. Survivors: **all four**, so if $B$ and $D$ were duplicates of $A$, they all become false positives.
>
> **(c)** If $A$ and $B$ are different people, $\tau = 0.7$ correctly keeps both, but would also keep real duplicates with the same overlap. $\tau = 0.5$ removes duplicates but deletes one of the two people (a missed detection). **No threshold handles both**, because NMS only sees box geometry, and here a duplicate and a neighbour look identical. Fixes: Soft-NMS (lower scores instead of deleting), or a detector that learns not to produce duplicates (DETR).

> [!example]- Exercise 4 — Boxes, losses, anchors
> **(a)** An anchor has centre $(100, 100)$, width 50, height 100. The ground-truth box has centre $(110, 90)$, width 60, height 80. Compute the regression target $t^* = (t_x, t_y, t_w, t_h)$.
> **(b)** A prediction has an error of 0.5 in $t_x$ and 3 in $t_w$. Compute the smooth L1 loss for each, and compare with $0.5 z^2$ (L2).
> **(c)** An RPN sees four anchors with these max IoUs against any ground-truth box: 0.82, 0.55, 0.25, and 0.62 (the last is the best anchor for a box that no other anchor matches above 0.7). Label each.
> **(d)** A Fast R-CNN RoI is labelled background ($u = 0$). What box loss does it get, and why?
>
> ---
> **(a)** $t_x = (110 - 100)/50 = 0.2$; $t_y = (90 - 100)/100 = -0.1$; $t_w = \log(60/50) = 0.182$; $t_h = \log(80/100) = -0.223$.
>
> **(b)** $z = 0.5$: smooth L1 $= 0.5 \cdot 0.25 = 0.125$ (same as L2 here). $z = 3$: smooth L1 $= 3 - 0.5 = 2.5$, vs L2 $= 4.5$, and its gradient is capped at 1 instead of 3. A badly placed box can't dominate the update.
>
> **(c)** 0.82 → **positive** (> 0.7). 0.55 → **ignored** (between 0.3 and 0.7). 0.25 → **negative** (< 0.3). 0.62 → **positive** by the second rule (best anchor for an otherwise unclaimed box), so every ground-truth box gets at least one positive.
>
> **(d)** None: the indicator $[u \ge 1]$ is 0. A background region has no true box to regress to, so only the classification loss applies.

> [!example]- Exercise 5 — Where the time and accuracy go
> **(a)** Fast R-CNN spends 0.32 s in the network and 2 s in selective search per image. What fraction of the time is proposals? How does Faster R-CNN fix it, and what does the fix cost?
> **(b)** A traffic-camera dataset is full of motorbikes about 32×32 px. Your Faster R-CNN uses a single stride-32 feature map. How many feature-map cells does one motorbike cover? What would you change?
> **(c)** Two reports: Model X "48 mAP", Model Y "38 mAP". What do you need to know before saying X is better?
> **(d)** Your detector has AP₅₀ = 0.62 but AP₇₅ = 0.28. What does that tell you, and where would you look?
>
> ---
> **(a)** $2/2.32 = 86\%$. Faster R-CNN replaces selective search with an RPN that runs on the shared feature map (one 3×3 conv and two 1×1 convs), ≈10 ms, ~200× faster, and it's learned, so proposals improve with training.
>
> **(b)** $32/32 = 1$ cell (2×2 at stride 16). After RoI pooling to 7×7, almost everything is interpolated from one feature vector. Add an **FPN** neck so small objects are handled at stride 4 or 8 (8×8 or 4×4 cells) with strong semantics; also consider higher input resolution or tiling the image.
>
> **(c)** The protocol: VOC mAP@0.5 or COCO AP@[.5:.95] (the same model can score ~60 on the first and ~40 on the second), the dataset and split, and the input resolution. "48 mAP" VOC-style could be the worse model.
>
> **(d)** The detector finds most objects but places boxes loosely: localisation, not classification, is the weak part. Look at the box-regression loss weight $\lambda$, the regression targets/encoding, feature resolution (FPN, smaller stride), or a refinement stage (e.g. Cascade R-CNN).

## 📝 Summary

- Detection outputs a **set** of (box, class, score) of unknown size. Every detector fixes the output size by proposing a dense candidate set (windows, proposals, anchors), classifying and refining each, then pruning.
- **The problem is search, not classification:** a naive sliding window costs ~3.6 PFLOPs per 224×224 image. Viola–Jones (integral image + cascade), HOG + SVM and DPM all avoided spending equal compute on every window.
- **Scoring:** IoU = overlap/union; greedy matching by score (duplicates are FPs); AP = area under the interpolated precision–recall curve (measures ranking); mAP averages over classes. VOC uses IoU 0.5; COCO averages over 0.50–0.95, so localisation quality counts. Always name the protocol; report AP₅₀, AP₇₅, AP_S.
- **NMS:** keep the best box, delete overlaps above $\tau$, repeat. 0.7 for proposals, 0.5 for detections. Fails in crowds and isn't learned.
- **R-CNN:** selective search (~2,000 proposals) + CNN features + SVMs + box regression; 33.7 → 66.0 mAP but 47 s/image. Box targets $(\Delta x/w_a, \Delta y/h_a, \log w/w_a, \log h/h_a)$.
- **Fast R-CNN:** one backbone pass, RoI pooling to 7×7, one multi-task loss (CE + smooth L1, no box loss for background); 0.32 s network time, 70.0 mAP.
- **Faster R-CNN:** RPN with $k = 9$ anchors per location (3 scales × 3 ratios), positive IoU > 0.7, negative < 0.3, 256 sampled anchors; proposals learned, ~10 ms; 73.2 mAP at 5 fps. Two-stage detectors handle the background imbalance by filtering and sampling.
- **FPN:** top-down path + lateral connections so every pyramid level is semantically strong; big gains on small objects (AP_S); now the standard "neck".

## ⚠️ Important Notes

1. **A duplicate detection is a false positive.** Good-looking duplicate boxes lower precision exactly as much as hallucinations.
2. **AP only depends on the ranking of predictions**, not the confidence values themselves; a model can have high AP and badly calibrated scores.
3. **Missed objects cap AP at the maximum recall.** No re-ranking fixes a detection that was never made.
4. **"mAP" without a protocol is meaningless.** VOC mAP@0.5 and COCO AP@[.5:.95] on the same model can differ by 20 points.
5. **AP₅₀ high but AP₇₅ low means sloppy boxes**, a localisation problem rather than a classification one.
6. **NMS is per class** and uses a hand-tuned threshold; it can delete a real object that overlaps another (crowds).
7. **Use the right box convention.** Corners, corner–size (COCO) and centre–size are easy to mix up; a wrong convention silently ruins training and evaluation.
8. **Box regression targets are relative:** offsets divided by the anchor size, log ratios for width/height. Decode with the inverse ($x = x_a + t_x w_a$, $w = w_a e^{t_w}$).
9. **Background RoIs/anchors get no regression loss.**
10. **RPN anchors between IoU 0.3 and 0.7 are ignored**, not negative.
11. **Two-stage detectors control the background imbalance with the RPN filter and fixed sampling ratios**; one-stage detectors need focal loss instead (ch. 08).
12. **Small objects need high-resolution features with strong semantics** — FPN, higher input resolution, or tiling.
13. **R-CNN's three defects** (slow, not one model, warping) were removed one at a time by Fast and Faster R-CNN. A likely exam question.
14. **Fast R-CNN's speed-up is ~147× from the network times quoted (47 s → 0.32 s)**; the paper's 213× includes a truncated-SVD trick (0.22 s).

> [!warning] Gaps in the source material
> - **Figures lost in extraction:** classification vs detection vs segmentation (slide 3), box encodings (9), sliding window (10), Viola–Jones and DPM figures (11–13), IoU examples (15–16), PR curve (18), NMS failure (21), selective search (23–24), R-CNN/Fast/Faster R-CNN diagrams (25, 28, 31, 34, 37, 41), RoI pooling 3×3 example (29), the four scale strategies (44–45), FPN architecture (46). Text and captions carry the content; the FPN architecture description in §6 is reconstructed from Lin et al. 2017, since slide 46's diagram didn't extract.
> - **Inconsistency on slide 30:** "47 s → 0.32 s per image, ≈213× faster". $47/0.32 \approx 147$. The 213× in the Fast R-CNN paper corresponds to 0.22 s, with truncated SVD on the FC layers.
> - **The worked AP example is mine.** The previous version of this subject's notes gave its 11-point AP as 0.7045; that was a floating-point comparison error (`0.6000000000000001 > 0.6` dropped a recall level). The correct value is **0.712**. All-point 0.683 and 101-point 0.686 were correct.
> - **Added beyond the slides:** the IoU, NMS, box-encoding and smooth L1 examples; why true negatives aren't counted; the integral-image definition; the anchor count for 600×800 (≈17,000); the FPN mechanics; all exercises and Important Notes.

**Previous:** [[06 - Vision Transformers]] · **Next:** [[08 - Object Detection II]]
