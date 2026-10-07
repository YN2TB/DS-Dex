---
subject: Computer Vision
chapter: 8
tags: [ds, computer-vision, object-detection, yolo, ssd, focal-loss, retinanet, fcos, centernet, detr, hungarian-matching]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 08: Object Detection II (52 slides); Redmon et al. 2016 (YOLO), Liu et al. 2016 (SSD), Lin et al. 2017 (focal loss), Tian et al. 2019 (FCOS), Zhou et al. 2019 (CenterNet), Carion et al. 2020 (DETR)"
---

# Object Detection II

Week 8. At the end of [[07 - Object Detection I|ch. 07]], a two-stage detector still had four hand-designed parts: anchor scales and aspect ratios, IoU thresholds for positives and negatives, sampling ratios, and the NMS threshold. This lecture removes them one at a time and counts what each removal costs: one-stage detectors (YOLO, SSD) drop the proposal stage, **focal loss** (RetinaNet) fixes the training that this breaks, **anchor-free** detectors (FCOS, CenterNet) drop the anchors, and **DETR** drops assignment rules and NMS.

The lecture's framing (slide 3): the proposal stage was doing two jobs. It made detection affordable, and it quietly protected the classifier from a flood of background it could never have handled directly. Each component you remove is replaced by something the model learns, and the bill arrives as data, training time, or a new failure mode.

## 📘 Main Knowledge

### 1. The price of two stages (slides 5–9)

**Where the budget goes (slide 7).** In a two-stage detector the RoI head runs **once per proposal**: 300 proposals means 300 small forward passes that can't be shared. A one-stage detector replaces that with a convolutional head applied **once, everywhere** on the feature map, which is the only way to reach real time.

**The obvious one-stage detector fails (slide 9).** With roughly 2,000 background anchors for every object, the summed cross-entropy is dominated by examples the model **already gets right**, and the gradient points at "keep predicting background". Two-stage detectors escaped this because the RPN threw away almost all background before the head ran, and the head then sampled a fixed 1:3 positive:negative ratio. A one-stage detector has neither protection.

Two ways out: **sample** the negatives (SSD's hard negative mining) or **reweight** them (RetinaNet's focal loss). The second turned out to be the better idea.

### 2. One-stage detectors (slides 10–20)

#### YOLO: You Only Look Once (Redmon et al., 2016) (slides 11–15)

**How it works.** Divide the image into an $S \times S$ grid. Each cell predicts $B$ boxes (each with $x, y, w, h$ and a confidence score) and one set of $C$ class probabilities. The output is a single $S \times S \times (5B + C)$ tensor; for VOC, $S = 7$, $B = 2$, $C = 20$ gives $7 \times 7 \times 30$.

**Architecture (slide 12):** 24 conv layers + 2 fully connected layers, pretrained on ImageNet at 224×224, fine-tuned for detection at 448×448. The base is similar to GoogLeNet with the Inception modules replaced by 1×1 and 3×3 conv layers. The final prediction comes from two FC layers over the whole conv feature map, so every prediction sees the whole image.

**Which prediction is responsible (slide 14).** The cell containing the ground-truth box's centre is responsible for it. Among that cell's $B$ boxes, the one whose current prediction has the highest IoU with the ground truth is the responsible box.

**The YOLO loss (slide 13)**, one sum-of-squares over the whole output tensor:

$$L_{loc} = \lambda_{coord} \sum_{i=1}^{S^2} \sum_{j=1}^{B} \mathbb 1_{ij}^{obj} \Big[(x_i - \hat x_i)^2 + (y_i - \hat y_i)^2 + \big(\sqrt{w_i} - \sqrt{\hat w_i}\big)^2 + \big(\sqrt{h_i} - \sqrt{\hat h_i}\big)^2\Big]$$

$$L_{cls} = \sum_{i=1}^{S^2} \sum_{j=1}^{B} \Big(\mathbb 1_{ij}^{obj} + \lambda_{noobj}\big(1 - \mathbb 1_{ij}^{obj}\big)\Big)\big(C_{ij} - \hat C_{ij}\big)^2 + \sum_{i=1}^{S^2} \mathbb 1_i^{obj} \sum_{c} \big(p_i(c) - \hat p_i(c)\big)^2$$

$$L = L_{loc} + L_{cls}$$

- $\mathbb 1_{ij}^{obj}$: box $j$ of cell $i$ is responsible for an object. $\mathbb 1_i^{obj}$: cell $i$ contains an object. $C_{ij}$ is the box confidence.

**What the loss reveals (slide 14):**
- $\lambda_{coord} = 5$: the coordinate terms count more than the rest.
- $\lambda_{noobj} = 0.5$: confidence on empty cells counts less, because most cells are empty. *This is the imbalance problem, patched with a hand-chosen constant.* Focal loss is the principled version.
- Regressing $\sqrt w$ and $\sqrt h$ makes a fixed pixel error cost more on a small box than a large one.

**YOLO, measured (slide 15):**

| Model | VOC07 mAP | FPS | Note |
|---|---|---|---|
| Faster R-CNN (VGG-16) | 73.2 | 7 | ch. 07's end point |
| YOLO | 63.4 | 45 | real time on 2016 hardware |
| Fast YOLO | 52.7 | 155 | 9 conv layers |

Error analysis: YOLO makes **more localisation errors** than Fast R-CNN but far fewer **background false positives**. 13.6% of Fast R-CNN's top detections are background, nearly 3× YOLO's rate. Why: YOLO sees the **whole image** when it predicts, while a region-based classifier sees only a crop, and a crop of background can look like anything. Context is free for YOLO and expensive for R-CNN.

The downside of one class per cell: YOLO v1 is weak on **small objects in groups** (a flock of birds), because one cell can't name two things.

#### SSD: Single Shot MultiBox Detector (Liu et al., 2016) (slides 16–19)

- VGG-16 backbone (up to conv5_3) plus a few extra conv layers that progressively shrink the feature map.
- **Default boxes** (SSD's name for anchors): each cell of each feature map has several default boxes of different aspect ratios (e.g. 4). For each one, SSD predicts box offsets and a confidence score for every class.
- **Defaults at every scale:** boxes are rescaled per level so each feature map is responsible for one range of object sizes. A fine 8×8 map's boxes cover small areas of the image; a coarse 4×4 map's boxes cover large areas.

**What SSD added (slide 19):**
- **Multi-scale prediction** from six feature maps instead of one. This is the "feature hierarchy" option (c) of ch. 07, which FPN later improved by giving the shallow levels strong semantics.
- **Hard negative mining:** sort the negatives by their classification loss, keep only the worst, and cap the negative:positive ratio at 3:1. A *selection rule*: most negatives contribute nothing because they're discarded.

| Model | VOC07 mAP | COCO AP | FPS |
|---|---|---|---|
| SSD300 | 74.3 | 23.2 | 59 |
| SSD512 | 76.9 | 26.8 | 22 |

SSD300 beat Faster R-CNN on VOC while running about 8× faster (59 vs 7 FPS): the first time a one-stage detector wasn't just the cheap option.

**The first generation, honestly (slide 20):**

| What YOLO and SSD proved | What they didn't solve |
|---|---|
| proposals aren't necessary for accuracy on VOC | on COCO, both trailed two-stage detectors badly |
| dense prediction is the only route to real time | both handled the imbalance with a hand-set constant or a selection rule |
| seeing the whole image suppresses background errors | anchors, IoU thresholds and NMS all survived |

The open question of 2017: *is a one-stage detector intrinsically less accurate, or was it just being trained wrong?*

### 3. Focal loss: fixing the training, not the architecture (slides 21–27)

**The diagnosis (Lin et al., 2017) (slide 22).** The gap was never architectural; it was **class imbalance during training**. An easy negative contributes a small loss, but there are ~$10^5$ of them against ~$10^1$ objects, so small × enormous still wins.

**The move:** don't select, don't resample. Keep **every** anchor in the sum and **down-weight the ones the model already handles**:

$$\text{CE}(p_t) = -\log p_t \quad \longrightarrow \quad \text{FL}(p_t) = -\alpha_t (1 - p_t)^\gamma \log p_t$$

$p_t$ is the probability the model assigns to the **true** class ($p_t = p$ for a positive, $1 - p$ for a negative). The paper uses $\gamma = 2$, $\alpha = 0.25$.

**What the modulating factor $(1 - p_t)^\gamma$ does (slide 23).** At $\gamma = 2$:

| $p_t$ | CE | $(1-p_t)^2$ | FL ($\alpha$ ignored) |
|---|---|---|---|
| 0.99 (very easy) | 0.0101 | 0.0001 | 0.000001 |
| 0.9 (easy) | 0.105 | 0.01 | 0.00105 |
| 0.5 | 0.693 | 0.25 | 0.173 |
| 0.1 (hard) | 2.303 | 0.81 | 1.865 |

An anchor already scored at $p_t = 0.9$ contributes 1/100 of its cross-entropy loss; one at $p_t = 0.1$ is barely touched. Nothing is discarded; the sum is reweighted towards what's still wrong.

**Example: one hard positive vs 10,000 easy negatives.** Positive at $p_t = 0.1$, each negative at $p_t = 0.99$.
- Cross-entropy: positive 2.30, negatives $10{,}000 \times 0.0101 = 100.5$. The negatives carry **44×** more loss.
- Focal loss ($\gamma = 2$): positive 1.87, negatives $10{,}000 \times 10^{-6} = 0.010$. Now the positive carries **186×** more.

**Two details that matter (slide 25):**
- **Why $\alpha = 0.25$ and not higher.** $\alpha_t$ weights the classes directly: $\alpha$ for foreground, $1 - \alpha$ for background. On its own (plain CE) you'd raise it to favour the rare foreground. But once $\gamma$ has removed the flood of easy negatives, the positives no longer need extra weight, and the paper found the best $\alpha$ was 0.25, i.e. slightly *down*-weighting positives. The two interact; tuning them separately gives the wrong answer for each.
- **The initialisation trick.** Initialise the classification bias so the model starts by predicting $p \approx \pi = 0.01$ for every anchor:
$$b = -\log\frac{1 - \pi}{\pi}$$
  For $\pi = 0.01$, $b = -\log 99 \approx -4.6$. Without it, a randomly initialised head predicts $p \approx 0.5$ on ~$10^5$ anchors in the first iteration, the background loss is huge, and training diverges. *A loss function and its initialisation are not separable.*

**RetinaNet (slide 26).** $k = 9$ anchors per location, an FPN neck, and the same two subnets on every pyramid level: a class subnet (4 conv layers, then $k \times C$ outputs) and a box subnet (4 conv layers, then $4k$ outputs). Trained with focal loss.

**RetinaNet, measured (slide 27)** (ResNet-101-FPN, 800 px, COCO test-dev): **AP 37.8**, AP₅₀ 57.5, AP₇₅ 40.8, AP_S 20.2, AP_M 41.1, AP_L 49.2.
- A one-stage detector beat every two-stage detector of its day **with no architectural novelty**: backbone, FPN and anchors are all from ch. 07.
- *Before concluding that an architecture is wrong for your problem, check whether it's being trained wrong.*
- AP_S = 20.2 vs AP_L = 49.2: focal loss fixed the imbalance, not the resolution problem. Small objects are still hard.

### 4. Anchor-free detectors: deleting the reference boxes (slides 28–34)

**What anchors were costing (slide 29):**
- **Hyperparameters:** scales, aspect ratios and how many; the positive and negative IoU thresholds; per-level assignment rules once there's an FPN. Tuned per dataset; a set that works on COCO can be wrong for aerial imagery or text.
- **Compute:** every anchor needs an IoU against every ground-truth box every iteration, and there are ~$10^5$ anchors.
- **The question:** if the network already sees the object at a location, why does it need a reference box to describe where it is?

#### FCOS: Fully Convolutional One-Stage detector (Tian et al., 2019) (slides 30–31)

Treat detection as **per-pixel prediction**, like semantic segmentation. Every feature-map location inside a ground-truth box is a positive and directly regresses four distances to the box's sides: $(l^*, t^*, r^*, b^*)$ (left, top, right, bottom).

Two problems it had to solve:
1. **Ambiguity.** A pixel inside two overlapping boxes has two sets of targets. FCOS gives each FPN level a range of regression distances, so large and small objects are handled at different levels and rarely collide. Where they still do, the **smaller** box wins.
2. **Low-quality boxes far from the centre.** A pixel near the border predicts a badly stretched box but can still be confident. A **centre-ness** branch predicts how central the pixel is:
$$\text{centerness} = \sqrt{\frac{\min(l^*, r^*)}{\max(l^*, r^*)} \cdot \frac{\min(t^*, b^*)}{\max(t^*, b^*)}}$$
   It's 1 at the exact centre and falls to 0 at the edges. At test time it multiplies the classification score, so off-centre boxes sink in the ranking before NMS.

| FCOS | COCO AP |
|---|---|
| ResNet-50-FPN, baseline → with improvements | 37.1 → 38.6 |
| ResNeXt-64×4d-101-FPN | 44.7 |

Anchors gone with no accuracy lost, and centre-ness costs one extra 3×3 conv.

#### CenterNet: objects as points (Zhou et al., 2019) (slides 32–33)

Model each object as a **single centre point**. The network outputs a heatmap per class (peaks at object centres), plus the box size and a small offset at each location.
- The training target for each object is a **Gaussian** blob centred on its centre point. Its spread $\sigma$ comes from a rule: the radius is the largest displacement of the centre that still leaves IoU ≥ 0.7 with the true box. So the target itself encodes how precisely the centre must be found (bigger boxes tolerate bigger offsets).
- At inference, a **3×3 max-pool** finds local peaks: a location is kept if it equals the max in its 3×3 neighbourhood.

**The first NMS-free detector.** Two detections of one object would have to be two peaks a few pixels apart. The Gaussian target makes that impossible to learn (there's exactly one maximum per object), and the 3×3 max-pool keeps exactly one.

| Backbone | COCO AP | FPS |
|---|---|---|
| ResNet-18 | 28.1 | 142 |
| DLA-34 | 37.4 | 52 |
| Hourglass-104 | 40.3 | 14 |

What else it gets for free: swap the size head for depth and orientation and you have 3D detection; swap it for joint offsets and you have pose estimation ([[10 - Pose Estimation and Faces|ch. 10]]). Limitation: two objects whose centres land on the same cell after downsampling become one peak, a real cost in crowded scenes.

**Three answers to one question (slide 34):** RetinaNet (anchors + focal loss), FCOS (per-pixel distances + centre-ness), CenterNet (centre peaks + size). All are dense one-stage detectors; they differ in how a location becomes a box.

### 5. DETR: detection as set prediction (slides 35–43)

**Back to ch. 07 (slide 36).** Every method so far handles the "set of unknown size" problem by proposing a dense candidate set and pruning it. DETR (DEtection TRansformer, Carion et al., 2020) doesn't. It predicts a **fixed set of $N$ slots** directly and makes the **loss** responsible for the fact that a set has no order. If the loss forbids two predictions from claiming the same object, there's nothing left for NMS to remove: duplicates are handled at training time, not inference. Every detector so far needed a rule for *which prediction is responsible*; DETR **computes** it, globally, at every training step.

**Matching cost (slide 37).** For one ground-truth object $y_i = (c_i, b_i)$ and one prediction $\hat y_j$:

$$\mathcal L_{match}(y_i, \hat y_j) = -\mathbb 1_{\{c_i \ne \varnothing\}}\, \hat p_j(c_i) + \mathbb 1_{\{c_i \ne \varnothing\}} \Big(\lambda_{L1} \|b_i - \hat b_j\|_1 + \lambda_{giou} \mathcal L_{giou}(b_i, \hat b_j)\Big)$$

- $i$ indexes objects. The image's objects are padded with $\varnothing$ ("no object") up to $N$.
- Boxes $b_i \in [0,1]^4$ are centre–size, normalised by image size (not corner pixels).
- A good match has high predicted probability for the right class and a close box.

**The set loss (slide 38).** Find the assignment $\hat\sigma$ of predictions to ground-truth slots with minimum total cost:

$$\hat\sigma = \arg\min_{\sigma \in S_N} \sum_{i=1}^{N} \mathcal L_{match}(y_i, \hat y_{\sigma(i)})$$

then train on that assignment:

$$\mathcal L = \sum_{i=1}^{N} \Big[-\log \hat p_{\hat\sigma(i)}(c_i) + \mathbb 1_{\{c_i \ne \varnothing\}}\big(\lambda_{L1} \|b_i - \hat b_{\hat\sigma(i)}\|_1 + \lambda_{giou} \mathcal L_{giou}\big)\Big]$$

Predictions matched to $\varnothing$ are trained to say "no object"; only real objects get a box loss.

- **Why the Hungarian algorithm.** It finds the minimum-cost one-to-one assignment in $O(N^3)$ ($10^6$ steps for $N = 100$, instead of checking all $100!$ permutations). **Greedy** matching would let a good prediction be "stolen" by an earlier object and leave a duplicate behind, exactly the failure DETR is trying to delete.
- **Why GIoU as well as L1.** L1 on box coordinates grows with box size, so it over-weights large boxes. **Generalised IoU** is scale-invariant and, unlike IoU, still gives a gradient when boxes don't overlap:
$$\text{GIoU} = \text{IoU} - \frac{|C \setminus (A \cup B)|}{|C|}, \qquad \mathcal L_{giou} = 1 - \text{GIoU}$$
  where $C$ is the smallest box enclosing both $A$ and $B$. For two non-overlapping boxes IoU is 0 whatever the distance, but GIoU becomes more negative the further apart they are, so there's a direction to move.

**DETR end to end (slide 39):**
1. A CNN backbone produces a 2D feature map.
2. Flatten it, add positional encodings, and pass it through a **transformer encoder**.
3. A **transformer decoder** takes $N$ learned embeddings called **object queries** and attends to the encoder output.
4. A shared feed-forward network turns each decoder output into a detection (class + box) or "no object".

**Object queries (slide 40).** $N$ learned embeddings fed to the decoder. No proposals, no anchors: a query is a slot filled by at most one object.
- $N = 100$, far more than the objects in any COCO image.
- Queries specialise: each learns a preferred region and size range, an anchor the model chose for itself.
- **Self-attention between queries** in the decoder lets them avoid each other: a query can see that another has already taken an object.
- *Anchors were a hand-written prior over where boxes are; object queries are the same prior, learned.*
- Consequence: DETR can't return more than $N$ objects, and accuracy falls on images with many objects. For COCO that never binds; for dense crowds it can.

**What it cost (slides 41–42).** Compared with Faster R-CNN + FPN:
- **AP_S collapses.** DETR predicts from a single coarse feature map (the encoder output at stride 32), with no pyramid. Small objects have the same problem as in plain Faster R-CNN, for the same reason.
- **AP_L jumps.** Global self-attention from the first layer: a large object spanning the image is a single relationship for attention, but a long-range dependency for convolution.
- **500 training epochs.** The matching is unstable early: the same object is claimed by different queries from one step to the next, so the queries take a long time to specialise.
- **Deformable DETR** (Zhu et al., 2021) attends to a few learned sampling points instead of all positions and adds multi-scale features. It reaches **46.9 AP in 50 epochs**, with AP_S rising from 20.5 to 26.4.

**What DETR proved (slide 43).** The real contribution isn't the transformer; it's the **set loss**: if the training objective itself forbids duplicates, the whole post-processing stage becomes unnecessary. That idea is separable from the architecture (and it did separate, see below). DETR also showed that detection, segmentation and panoptic output can come from the same decoder with different heads. Hand-designed components removed: **proposals, anchors, assignment heuristics and NMS**, all four.

### 6. What should you actually use? (slides 44–49)

**Where the two families ended up (slide 47):**
- **DETR became fast.** RT-DETR (2023) reaches **53.1 AP at 108 FPS** with a ResNet-50 by making the encoder cheap, and argues removing NMS is itself a speed win, because NMS latency varies with the number of detections.
- **YOLO became NMS-free.** Recent YOLO releases use one-to-one matching and drop NMS at inference: DETR's idea now ships inside the family it competed with.
- *The architectural argument is over. Both families are transformer-influenced and NMS-free; the choice is an empirical question about **your** data.*

**For the final project (slide 48):**

| Situation | Reach for | Licence |
|---|---|---|
| a strong default, permissively licensed | RF-DETR | Apache 2.0 |
| maximum throughput per frame | RTMDet | MIT |
| fastest path to a working baseline | a recent YOLO | AGPL-3.0 |
| no labels yet, exploring feasibility | YOLO-World, Grounding DINO (open-vocabulary, prompted with text) | varies |
| understanding *why* it fails | train RetinaNet or FCOS yourself | — |

- **Check the licence.** AGPL-3.0 obliges you to release your source code if you serve the model over a network. Fine for coursework; for anything you intend to ship, it's a decision.
- **The method that beats the table:** label your data, train two architectures side by side, and let your own validation set decide. Published COCO rankings rarely survive contact with a specific domain.

**Nine years, one component at a time (slide 49).** Every hand-designed component turned out to be something a model could learn, given enough data and training. But read the cost column too: RetinaNet needed a new loss, FCOS a new branch, DETR 500 epochs. Nothing was free.

| Removed | By | Replaced with | Cost |
|---|---|---|---|
| proposal stage | YOLO, SSD | dense one-pass head | imbalance (patched by $\lambda_{noobj}$, hard negative mining) |
| imbalance patches | RetinaNet | focal loss + prior-probability bias init | a new loss with two interacting hyperparameters |
| anchors | FCOS, CenterNet | per-pixel distances + centre-ness; centre heatmaps | a new branch; crowded-centre collisions |
| assignment rules + NMS | DETR | Hungarian-matched set loss, object queries | 500 epochs, weak small-object AP (later fixed by Deformable DETR) |

**Hands-on (slide 52):** focal loss from scratch and its gradient; the loss-share figure on simulated anchors; show training diverges without the bias initialisation; vectorised FCOS targets and centre-ness; CenterNet's Gaussian radius rule; Hungarian vs greedy matching on the same cost matrix; a DETR-style set loss on toy data; NMS latency vs detection count. (`torchvision.ops.sigmoid_focal_loss` is six lines; `detr/models/matcher.py` is about forty.)

## ✏️ Exercises

> [!example]- Exercise 1 — Focal loss by the numbers
> **(a)** Compute cross-entropy and focal loss ($\gamma = 2$, ignore $\alpha$) for $p_t = 0.9$ and $p_t = 0.1$. By what factor is each down-weighted?
> **(b)** An image has 1 object anchor at $p_t = 0.1$ and 10,000 background anchors at $p_t = 0.99$. Which group dominates the total loss under CE? Under focal loss? By how much?
> **(c)** Add $\alpha = 0.25$ (foreground) / $0.75$ (background). Who dominates now?
> **(d)** A teammate sets $\gamma = 5$ "to focus even harder". What risk does that create?
>
> ---
> **(a)** $p_t = 0.9$: CE 0.105, FL $= 0.01 \times 0.105 = 0.00105$, down-weighted **100×**. $p_t = 0.1$: CE 2.303, FL $= 0.81 \times 2.303 = 1.865$, down-weighted only 1.23×.
>
> **(b)** CE: positive 2.30, background $10{,}000 \times 0.0101 = 100.5$, so background carries **44×** more loss: the gradient mostly says "predict background". Focal: positive 1.865, background $10{,}000 \times 0.0001 \times 0.0101 = 0.010$, so the positive carries **186×** more.
>
> **(c)** Positive $0.25 \times 1.865 = 0.466$; background $0.75 \times 0.010 = 0.0075$. The positive still dominates, by about **62×**. $\alpha = 0.25$ pulls weight *back* from the foreground because $\gamma$ already shifted it strongly that way; that's why they must be tuned together.
>
> **(d)** With $\gamma = 5$, even moderately well-classified examples contribute almost nothing (e.g. $p_t = 0.8$ is down-weighted by $0.2^5 = 1/3125$). Easy negatives effectively vanish from training, so the model may stop learning what background looks like and produce false positives, and the overall gradient becomes very small. $\gamma$ has a useful window (the paper found 2 best).

> [!example]- Exercise 2 — Why the bias initialisation matters
> A RetinaNet-style head has 100,000 anchors per image, almost all background. Its last layer outputs a logit per anchor (sigmoid → $p$ = probability of foreground).
> **(a)** With the usual bias of 0, what is $p$ for every anchor at the first iteration, and roughly what is the total background loss (plain CE)?
> **(b)** With bias $b = -\log\frac{1-\pi}{\pi}$ and $\pi = 0.01$: compute $b$ and the total background loss.
> **(c)** Why does (a) cause training to diverge?
>
> ---
> **(a)** Bias 0 with small random weights gives logits ≈ 0, so $p \approx 0.5$ everywhere. Each background anchor costs $-\log(1 - 0.5) = 0.693$: total ≈ $100{,}000 \times 0.693 \approx 69{,}300$ for one image.
>
> **(b)** $b = -\log 99 \approx -4.60$, so $p = 0.01$. Each background anchor costs $-\log 0.99 \approx 0.010$: total ≈ **1,005**, about 69× smaller (and focal loss shrinks it further).
>
> **(c)** In (a), the first gradients are enormous and all push towards "background", producing huge, unstable updates (the paper reports divergence). Starting at the prior $\pi = 0.01$ means the model already predicts "mostly background" correctly, so early gradients come from the few objects instead.

> [!example]- Exercise 3 — Anchor-free targets
> A ground-truth box has corners $(20, 10, 100, 60)$ (x₁, y₁, x₂, y₂).
> **(a)** For a feature location at pixel $(50, 40)$, compute the FCOS targets $(l^*, t^*, r^*, b^*)$ and centre-ness.
> **(b)** Compute centre-ness at the box centre $(60, 35)$ and near the left edge at $(25, 35)$.
> **(c)** At test time, location $(25, 35)$ predicts the class with score 0.80 and location $(60, 35)$ with score 0.70. After multiplying by centre-ness, which ranks higher? Why is that desirable?
> **(d)** In CenterNet, why can't the model produce two detections for this one box, and when does CenterNet fail instead?
>
> ---
> **(a)** $l^* = 50 - 20 = 30$, $t^* = 40 - 10 = 30$, $r^* = 100 - 50 = 50$, $b^* = 60 - 40 = 20$. Centre-ness $= \sqrt{\frac{30}{50} \cdot \frac{20}{30}} = \sqrt{0.4} = 0.632$.
>
> **(b)** Centre $(60, 35)$: $l = r = 40$, $t = b = 25$, centre-ness **1.0**. Edge $(25, 35)$: $l = 5$, $r = 75$, $t = b = 25$: $\sqrt{5/75 \times 1} = $ **0.258**.
>
> **(c)** Edge: $0.80 \times 0.258 = 0.21$. Centre: $0.70 \times 1.0 = 0.70$. The centre location now ranks first. Locations near the edge see only part of the object and tend to predict poorly placed boxes even when confident, so centre-ness pushes their boxes down before NMS.
>
> **(d)** The training target is a single Gaussian peak at the centre, and inference keeps only local maxima of a 3×3 max-pool, so one object gives one peak and one detection (no NMS needed). It fails when two objects' centres fall on the same output cell after downsampling: they merge into one peak and one object is lost (crowds, small overlapping objects).

> [!example]- Exercise 4 — Hungarian vs greedy matching
> DETR has 3 prediction slots and an image with 2 objects. Matching costs (lower is better):
>
> | | Pred 1 | Pred 2 | Pred 3 |
> |---|---|---|---|
> | Object A | 0.1 | 0.3 | 0.9 |
> | Object B | 0.2 | 0.8 | 0.9 |
>
> **(a)** Greedy matching (each object, in order A then B, takes its cheapest unclaimed prediction). What's the assignment and total cost?
> **(b)** The optimal (Hungarian) assignment and its cost?
> **(c)** What is the leftover prediction trained to output?
> **(d)** Why does DETR need no NMS, and why does it still need $N$ to be large?
>
> ---
> **(a)** A takes Pred 1 (0.1). B's cheapest unclaimed is Pred 2 (0.8). Total **0.9**.
>
> **(b)** Try both options: A→1, B→2 = 0.9; **A→2, B→1 = 0.3 + 0.2 = 0.5**. Hungarian picks the latter (with $N$ predictions it does this search in $O(N^3)$ instead of over all permutations).
>
> **(c)** Pred 3 is matched to $\varnothing$, so it's trained to predict "no object" (and gets no box loss).
>
> **(d)** The one-to-one matching means each object is the target of exactly one prediction; any other prediction on the same object is pushed towards "no object", so the model learns not to make duplicates, and self-attention between queries lets them coordinate. But each slot can hold at most one object, so DETR can never output more than $N$ objects ($N = 100$ is plenty for COCO, not for a 300-person crowd).

> [!example]- Exercise 5 — Choose and diagnose
> **(a)** YOLO v1 ($S = 7$, $B = 2$, $C = 20$): what's the output shape, and what's the most objects it can report? Why is it bad at a flock of 30 small birds?
> **(b)** Why does YOLO regress $\sqrt w$ instead of $w$? Compare the squared error for a 5-unit width error on a box of width 10 vs width 100.
> **(c)** A DETR model trained for 50 epochs has poor accuracy and especially poor AP_S. Give two reasons and a fix.
> **(d)** A start-up wants a detector to embed in a product they will sell as a cloud API. Which entry in slide 48's table needs care, and why?
>
> ---
> **(a)** $7 \times 7 \times (5 \cdot 2 + 20) = 7 \times 7 \times 30$. Each cell has one set of class probabilities, so it can name at most one object: at most 49 objects per image (from 98 predicted boxes). Many small birds whose centres fall in the same cell can't all be reported: one cell can only name one thing.
>
> **(b)** With $\sqrt{\cdot}$, the same absolute error costs more on a small box: $(\sqrt{15} - \sqrt{10})^2 = 0.505$ vs $(\sqrt{105} - \sqrt{100})^2 = 0.061$, about 8× more for the small box. A 5-pixel error matters much more for a 10-pixel object than a 100-pixel one.
>
> **(c)** (1) Original DETR needs ~500 epochs: Hungarian matching is unstable early, so queries are slow to specialise. (2) It predicts from a single stride-32 feature map with no pyramid, so small objects get few features. Fix: **Deformable DETR** (sparse sampling attention + multi-scale features), 46.9 AP in 50 epochs with better AP_S; or a modern DETR variant like RT-DETR/RF-DETR.
>
> **(d)** "A recent YOLO" is AGPL-3.0: serving it over a network obliges them to release their source code. They should pick a permissively licensed model (RF-DETR, Apache 2.0; RTMDet, MIT) or get a commercial licence.

## 📝 Summary

- **One-stage detectors** predict densely in one pass (needed for real time) but face the full foreground–background imbalance (~2,000:1 per object) that the RPN used to filter out.
- **YOLO:** $S \times S$ grid, each cell predicts $B$ boxes + one class distribution ($7 \times 7 \times 30$ on VOC); sum-of-squares loss with $\lambda_{coord} = 5$, $\lambda_{noobj} = 0.5$, $\sqrt{w}, \sqrt{h}$. 45 FPS, 63.4 mAP; fewer background errors (sees the whole image), more localisation errors, weak on small grouped objects.
- **SSD:** default boxes on six feature maps (multi-scale), hard negative mining at 3:1. SSD300: 74.3 mAP at 59 FPS, beating Faster R-CNN on VOC; still weak on COCO.
- **Focal loss** $-\alpha_t (1 - p_t)^\gamma \log p_t$ ($\gamma = 2$, $\alpha = 0.25$) keeps every anchor but down-weights easy ones (100× at $p_t = 0.9$). Needs the prior-probability bias init $b = -\log((1-\pi)/\pi)$, $\pi = 0.01$. **RetinaNet** (FPN + anchors + focal loss): 37.8 AP, beating two-stage detectors with no new architecture.
- **Anchor-free:** **FCOS** regresses $(l, t, r, b)$ from every pixel inside a box, uses FPN levels to resolve overlaps and **centre-ness** to suppress edge predictions. **CenterNet** finds Gaussian centre peaks with a 3×3 max-pool: the first NMS-free detector, extends to 3D and pose.
- **DETR:** $N = 100$ object queries, transformer encoder–decoder, **Hungarian-matched set loss** (class + L1 + GIoU) makes duplicates impossible, so no NMS and no anchors. Costs: 500 epochs, poor AP_S (single stride-32 map), at most $N$ objects. Deformable DETR: 46.9 AP in 50 epochs.
- **Today:** both YOLO and DETR families are NMS-free and transformer-influenced; choose on your own validation data and **check the licence** (AGPL-3.0 for recent YOLOs).

## ⚠️ Important Notes

1. **$p_t$ is the probability of the true class**, not the probability of foreground. For a background anchor, $p_t = 1 - p$.
2. **Focal loss down-weights easy examples; it doesn't remove them.** Hard negative mining removes them.
3. **$\alpha$ and $\gamma$ interact.** With $\gamma = 2$, $\alpha = 0.25$ *favours background*, the opposite of what $\alpha$ alone would suggest.
4. **Focal-loss detectors need the prior bias init** ($\pi = 0.01$ → $b \approx -4.6$), or the first iterations' background loss makes training diverge.
5. **Focal loss fixes imbalance, not resolution.** RetinaNet's AP_S (20.2) is still far below its AP_L (49.2).
6. **YOLO v1's one class per cell** limits it on small objects in groups.
7. **YOLO's $\lambda_{noobj} = 0.5$ and SSD's 3:1 hard negative mining are hand-set patches** for the same imbalance that focal loss handles in a principled way.
8. **In FCOS, overlapping boxes go to the smaller box**, and FPN levels are assigned by regression distance.
9. **Centre-ness multiplies the classification score at test time**; it isn't used to select training positives in the original form.
10. **CenterNet needs no NMS**, but two objects whose centres collide after downsampling become one detection.
11. **DETR uses Hungarian (optimal) matching, not greedy**; greedy matching can leave duplicates.
12. **DETR boxes are normalised centre–size**, and the GIoU term is needed because L1 alone over-weights large boxes and IoU gives no gradient for non-overlapping boxes.
13. **DETR can never output more than $N$ objects.**
14. **Original DETR trains for ~500 epochs and is weak on small objects**; Deformable DETR fixes both.
15. **Check the licence before using a detector in a product**: AGPL-3.0 has obligations for network services.

> [!warning] Gaps in the source material
> - **Slides that are image-only, so their content is lost:** "The Price of Two Stages" (6), the imbalance chart (8), YOLO architecture diagram (11), SSD figures (16–18), "Where the Gradient Actually Goes" (24), RetinaNet diagram (26), FCOS and CenterNet figures (30, 32), "Three Answers to One Question" (34; §4's one-line summary is mine), DETR architecture (39), "What It Cost" charts (41; the explanations on slide 42 survive), "The Ledger" (45) and "The Frontier, Today" (46). The cost table in §6 is reconstructed from slides 49–50, not from the lost Ledger.
> - **The lecture's "≈2000:1 — we counted it" and "roughly 10×" loss-share figures** (summary slide) come from the lecturer's simulation, which isn't in the slides. The 10,000-negative example in §3 and Exercise 1 is mine.
> - **Added beyond the slides:** YOLO's grid mechanics and the 7×7×30 example; FCOS's $(l^*, t^*, r^*, b^*)$ definition and centre-ness formula (the slide describes them in words); the GIoU formula; CenterNet's output heads; the Hungarian vs greedy example; all exercises and Important Notes.
> - **Moved to ch. 07:** mAP computation and the VOC/COCO protocols (they're in Lecture 07). FPN is also in Lecture 07.

**Previous:** [[07 - Object Detection I]] · **Next:** [[09 - Segmentation]]
