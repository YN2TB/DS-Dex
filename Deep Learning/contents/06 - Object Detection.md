---
subject: Deep Learning
chapter: 6
tags: [ds, deep-learning, object-detection, anchor-boxes, iou, nms, ssd, r-cnn, transfer-learning, augmentation]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, §14.1–14.8 (Image Augmentation, Fine-Tuning, Bounding Boxes, Anchor Boxes, Multiscale Detection, the Detection Dataset, SSD, R-CNNs)"
---

# Object Detection

**Classification asks *what*; detection asks *what and where, for every object*.** D2L §14.1–14.8 builds the machinery: two generalization techniques (augmentation, fine-tuning), then bounding boxes → anchor boxes → IoU → labelling → non-maximum suppression → multiscale → SSD → the R-CNN family.

**⚠️ THIS CHAPTER'S SOURCE PRINTS MORE CHECKABLE TENSORS THAN ANY OTHER IN THE SUBJECT, AND ALL OF THEM REPRODUCE.** The anchor-labelling example's **three printed tensors** (classes, mask, and all twenty offsets) were regenerated from the five anchor boxes and two ground-truth boxes alone; the NMS output, both RoI-pooling outputs, the 2,042,040 anchor count, the 5,444 anchor count, the 25,300 concatenation and all five geometric-mean scales verify exactly.

**Six results.**

**§10 — ⚠️ THE OMISSION THAT MATTERS MOST: D2L'S OWN DETECTOR HAS A FOREGROUND/BACKGROUND IMBALANCE BETWEEN 123:1 AND 5,443:1, AND ITS LOSS FUNCTION DOES NOTHING ABOUT IT.** Computed by generating TinySSD's full 5,444-anchor set and labelling it against single objects. **D2L's mask handles the *offset* loss and says so explicitly — nothing handles the *class* loss.** A model can score well by predicting "background" everywhere.

**§6 — ⚠️ THE 375× REDUCTION THAT IS THE WHOLE POINT OF MULTISCALE DETECTION, AND D2L NEVER DIVIDES.** Per-pixel anchors on a 561×728 image: **2,042,040**. TinySSD's five feature-map levels: **5,444**. *(Like-for-like at 256×256, still 60×.)*

**§2 — ⚠️ IoU = 0.5 IS NOT "HALF OVERLAPPING".** Two unit squares offset by $d$ have $\mathrm{IoU}=(1-d)/(1+d)$, so **IoU 0.5 requires $d=1/3$ exactly — they share two-thirds of their width.** IoU falls roughly twice as fast as intuition expects, because the union grows as the intersection shrinks.

**§11 — ⚠️ THE IoU THRESHOLD IS NOT A DETAIL, IT IS THE TRAINING SIGNAL.** Moving it from 0.6 to 0.3 multiplies the positive anchor count by **16.9×** (12 → 203) and moves the imbalance from **453:1 to 26:1**.

**§5 — ⚠️ NMS TRADES A FALSE POSITIVE FOR A FALSE NEGATIVE AND THE THRESHOLD *IS* THAT TRADE.** Reproduced exactly on D2L's example; **two genuinely distinct objects overlapping above the threshold are unrecoverable.** D2L's exercise 14.4.4 raises this and gives no answer.

**§9 — ⚠️ THE R-CNN FAMILY IS ONE MOVE REPEATED: DELETE A HAND-DESIGNED COMPONENT.** Fast R-CNN is **2,000× fewer CNN passes** than R-CNN; Faster R-CNN then deletes selective search itself. **Same pattern as [[05 - Convolutional Neural Network|ch. 05]]'s architecture history** — SIFT → learned filters, fc head → global average pooling, selective search → RPN.

## 📘 Main Knowledge

### 1. Two ways to get more out of the data you have

**Image augmentation** generates similar-but-distinct training examples by random transformation. D2L's framing is worth keeping precise — there are **two** motivations, and they are not the same:
1. **Expand the training set** — more examples.
2. **Force the model to rely less on a particular attribute** — cropping makes the object appear in different positions, "thereby reducing the dependence of a model on the position of the object"; brightness and colour jitter reduce colour sensitivity.

**The second is the real one**: augmentation encodes an invariance you believe the task has. *(D2L: "It is probably true that image augmentation was indispensable for the success of AlexNet at that time.")*

> [!note] ⚠️ Augmentation is an assumption, exactly like translation invariance in [[05 - Convolutional Neural Network|ch. 05]] §1
> A horizontal flip is safe for cats and **destroys** a digit-recognition task (`2` vs a mirrored `2`), a text task, or anything chiral. **Every augmentation asserts "the label is invariant under this transformation," and that assertion can be false.** ⇒ *choose augmentations from the task's symmetries, not from a default list.*

**Fine-tuning** (transfer learning) is D2L's four steps:
1. Pretrain a **source model** on a large source dataset (ImageNet).
2. Create a **target model** copying every layer **and its parameters** except the output layer.
3. Add a fresh output layer sized to the target task, **randomly initialized**.
4. Train on the target data — output layer from scratch, everything else fine-tuned.

> [!warning] ⚠️ The learning-rate asymmetry is the operational content, and it is quantitative
> D2L gives the pretrained layers the base learning rate and **the new output layer $10\times$ that**:
> ```
> [{'params': feature_params},
>  {'params': net.fc.parameters(), 'lr': learning_rate * 10}]
> ```
> **And its from-scratch comparison run uses $5\times10^{-4}$ — exactly the rate the fine-tuned run gives only to its new head, i.e. $10\times$ the fine-tuned base.**
>
> ⇒ **the pretrained weights are already nearly right, so you nudge them; the head is random, so you train it.** *A single learning rate for both is the standard way to destroy a pretrained backbone in the first few hundred steps* — which is [[04 - Neural Network|ch. 04]] §16's stability bound applied per parameter group.
>
> **This works because of [[05 - Convolutional Neural Network|ch. 05]]'s stem/body/head factorization**: the stem and body learn general features (edges, textures, shapes), and only the head is task-specific.

### 2. ⚠️ Bounding boxes and IoU — and why 0.5 is not "half"

A **bounding box** is either $(x_1,y_1,x_2,y_2)$ (upper-left, lower-right) or $(c_x,c_y,w,h)$ (centre, width, height). The conversions are trivially inverse; D2L verifies by round-tripping and getting `True` in all eight entries.

**Intersection over Union** — the Jaccard index of the two pixel sets:

$$J(\mathcal A,\mathcal B)=\frac{|\mathcal A\cap\mathcal B|}{|\mathcal A\cup\mathcal B|}\in[0,1]$$

with 0 = disjoint and 1 = identical. **Verified on a ladder of cases**: identical 1.0000, disjoint 0.0000, touching edges 0.0000, a box of $\frac14$ the area nested inside 0.2500.

> [!warning] ⚠️ IoU 0.5 requires far more overlap than the number suggests
> For two unit squares offset horizontally by $d$:
> $$\mathrm{IoU}=\frac{1-d}{1+d}$$
>
> | $d$ | IoU |
> |---|---|
> | 0 | 1.0000 |
> | **1/3** | **0.5000** |
> | 0.5 | 0.3333 |
> | 1 | 0.0000 |
>
> **IoU 0.5 needs $d=1/3$ exactly — the boxes share two-thirds of their width.** A "50% overlap" in the everyday sense ($d=0.5$) scores only **0.3333**.
>
> **Why: the union *grows* as the intersection shrinks**, so the ratio falls on both ends at once. ⇒ *IoU is roughly twice as strict as it sounds, and this is why detection thresholds of 0.5 are not lenient.*

> [!note] ⚠️ And IoU cannot tell *shifted* from *wrong-sized*
> Two boxes reach IoU 0.5 by being **offset by $d=1/3$**, *or* by one being **nested with half the area** (side $\sqrt2$ inside a side-2 box — verified, IoU exactly 0.500000).
>
> ⇒ **IoU collapses "right size, wrong place" and "right place, wrong size" into one number.** *(That degeneracy is why GIoU and DIoU losses were later proposed — an addition beyond D2L.)*

### 3. Anchor boxes — the region-sampling scheme

Generate boxes of scale $s\in(0,1]$ and aspect ratio $r>0$ centred on each pixel, with width $ws\sqrt r$ and height $hs/\sqrt r$. With $n$ scales and $m$ ratios, *all* combinations give $whnm$ boxes — too many. **D2L's subset keeps only pairs containing $s_1$ or $r_1$:**

$$(s_1,r_1),(s_1,r_2),\dots,(s_1,r_m),(s_2,r_1),\dots,(s_n,r_1)\ \Longrightarrow\ n+m-1\ \text{per pixel}$$

| $n\times m$ | all pairs | $n+m-1$ | saving |
|---|---|---|---|
| 3×3 | 9 | **5** | 44.4% |
| 5×5 | 25 | 9 | 64.0% |
| 10×10 | 100 | 19 | **81.0%** |

**Verified against D2L's printout**: $561\times728\times5=\mathbf{2{,}042{,}040}$, exactly the printed `torch.Size([1, 2042040, 4])`.

> [!warning] ⚠️ The subset trick saves 44.4% and the real problem is the $w\times h$ factor
> **2,042,040 anchors for one image.** Each needs one class label and four offsets — **10,210,200 numbers, 38.9 MB of labels, for a single training image.**
>
> ⇒ **the combinatorics of scales and ratios is a rounding error next to placing a box on every pixel.** That is what §6 fixes, and D2L's own §14.5 opens by saying so.

### 4. ⚠️ Labelling anchors — the assignment algorithm, fully reproduced

Every anchor is a training example needing **a class** and **four offsets**. The assignment is greedy on the IoU matrix $\mathbf X\in\mathbb R^{n_a\times n_b}$:

1. Find the largest $x_{ij}$; assign $B_j$ to $A_i$; **discard row $i$ and column $j$**.
2. Repeat until all $n_b$ columns are discarded — **every ground-truth box gets an anchor**.
3. For each remaining anchor, assign its best ground-truth box **only if that IoU exceeds a threshold** (0.5).

**D2L's worked example, with the IoU matrix it never prints:**

| | dog | cat |
|---|---|---|
| $A_0$ | 0.053648 | 0.000000 |
| $A_1$ | **0.141723** | 0.000000 |
| $A_2$ | 0.000000 | 0.565724 |
| $A_3$ | 0.000000 | 0.205882 |
| $A_4$ | 0.000000 | **0.745908** |

**Running the algorithm:** $A_4$ has the global maximum (0.7459) → cat. Discard row 4 and the cat column; the largest remaining is $A_1$ at 0.1417 → dog. Then the threshold pass: $A_0$'s best is 0.0536 < 0.5 → **background**; $A_2$'s is 0.5657 ≥ 0.5 → **cat**; $A_3$'s is 0.2059 < 0.5 → **background**.

**Offsets** are the ground-truth box's position and size *relative to the anchor*, standardized:

$$\left(\frac{\frac{x_b-x_a}{w_a}-\mu_x}{\sigma_x},\ \frac{\frac{y_b-y_a}{h_a}-\mu_y}{\sigma_y},\ \frac{\log\frac{w_b}{w_a}-\mu_w}{\sigma_w},\ \frac{\log\frac{h_b}{h_a}-\mu_h}{\sigma_h}\right)$$

with $\mu=0$, $\sigma_x=\sigma_y=0.1$, $\sigma_w=\sigma_h=0.2$ — i.e. **multiply the centre offsets by 10 and the log size ratios by 5.**

> [!warning] ⚠️ ALL THREE PRINTED TENSORS REPRODUCED FROM THE INPUTS ALONE
> | | computed | D2L prints |
> |---|---|---|
> | classes | `[0, 1, 2, 0, 2]` | `[0, 1, 2, 0, 2]` ✓ |
> | mask | `[0,0,0,0, 1,1,1,1, 1,1,1,1, 0,0,0,0, 1,1,1,1]` | identical ✓ |
> | offsets (20 values) | `1.40e0, 1.00e1, 2.59e0, 7.18e0, …` | identical to 3 s.f. ✓ |
>
> **Nothing but the five anchor boxes and two ground-truth boxes was used.**

> [!note] ⚠️ Two design choices in that algorithm worth naming
> **(i) Step 2 runs *before* the threshold matters** — every ground-truth box is guaranteed an anchor even if its best IoU is terrible. $A_1$'s IoU with the dog is **0.1417**, far below 0.5, and it is still labelled "dog". ⇒ **without this, a small or oddly-shaped object would have no positive anchor at all and could never be learned.**
> **(ii) The offsets are standardized, not raw.** Dividing by 0.1 and 0.2 puts the four targets on comparable scales so a single $\ell_1$ loss weights them sensibly — the same reasoning as feature standardization in [[05 - Convolutional Neural Network|ch. 05]] §13.

> [!note] ⚠️ A small "read what the code prints" catch
> D2L's offset at index 18 prints as **`4.17e-06`**. Anchor $A_4$ has width $0.92-0.57=0.35$ and the cat's box has width $0.90-0.55=0.35$ — **exactly equal**, so the true offset is $5\log 1=\mathbf{0}$. **The printed value is `float32` rounding noise around an exact zero.** Harmless here, and worth the habit: *a small printed number can be a number the arithmetic never produced.*

### 5. ⚠️ Non-maximum suppression — a greedy filter with a real cost

Many anchors surround the same object, so many predicted boxes do too. **NMS** sorts non-background predictions by confidence and repeatedly: take the highest-confidence survivor as a **basis**, delete every remaining box whose IoU with it exceeds $\epsilon$, repeat.

**D2L's example, reproduced.** Four boxes, confidences 0.90 / 0.80 / 0.70 / 0.90, threshold 0.5:

| | $B_0$ | $B_1$ | $B_2$ | $B_3$ |
|---|---|---|---|---|
| $B_0$ | 1.0000 | **0.7368** | **0.5454** | 0.0000 |
| $B_1$ | 0.7368 | 1.0000 | 0.6306 | 0.0115 |
| $B_2$ | 0.5454 | 0.6306 | 1.0000 | 0.0839 |
| $B_3$ | 0.0000 | 0.0115 | 0.0839 | 1.0000 |

Keep $B_0$ (0.90) → suppress $B_1$ (0.7368) and $B_2$ (0.5454). Keep $B_3$ (0.90) → suppresses nothing. **Kept: $\{B_0,B_3\}$; suppressed: $\{B_1,B_2\}$ — exactly D2L's printed `-1` class labels on rows 3 and 4.** ✓

> [!warning] ⚠️ NMS deletes, and a deletion cannot be undone — D2L's exercise 14.4.4, unanswered
> The algorithm is **greedy** and compares only against surviving bases. **If two genuinely distinct objects overlap by more than $\epsilon$ — two people standing close, two cars in traffic, overlapping cell nuclei — the lower-confidence one is deleted and is unrecoverable.**
>
> ⇒ ***NMS converts a false positive into a false negative, and the threshold IS that trade.*** Raise $\epsilon$ and keep duplicates; lower it and lose crowded objects.
>
> **Soft-NMS** (Bodla et al. 2017, which D2L names in the exercise) *decays* the overlapping box's score instead of deleting it, deferring the decision to a final confidence cut. *(An addition beyond D2L's exposition.)*

### 6. ⚠️ Multiscale detection — the 375× reduction

Instead of one anchor per **pixel**, place anchors on **feature maps**. A $32\times32$ feature map on a $256\times256$ image samples 1,024 positions uniformly instead of 65,536 — and each position already has a **receptive field** covering a patch of the input ([[05 - Convolutional Neural Network|ch. 05]] §7).

**D2L's motivating count, verified:** TinySSD's five levels give
$$(32^2+16^2+8^2+4^2+1)\times4=1361\times4=\mathbf{5{,}444}$$

| feature map | positions | anchors | stride | anchor scale | **object size (px)** |
|---|---|---|---|---|---|
| 32×32 | 1,024 | 4,096 | 8 | 0.20–0.272 | **51–70** |
| 16×16 | 256 | 1,024 | 16 | 0.37–0.447 | 95–114 |
| 8×8 | 64 | 256 | 32 | 0.54–0.619 | 138–158 |
| 4×4 | 16 | 64 | 64 | 0.71–0.790 | 182–202 |
| **1×1** | 1 | 4 | 256 | 0.88–0.961 | **225–246** |

> [!warning] ⚠️ **2,042,040 → 5,444 is a 375× reduction**, and D2L states both numbers pages apart without dividing
> *(That compares a 561×728 image to a 256×256 one. Like-for-like — $256\times256\times5=327{,}680$ against 5,444 — it is still **60×**, and the feature-map budget is **48× smaller than per-pixel at every anchors-per-unit setting.**)*
>
> **And the count is not the main point.** Each level has a different receptive field, so **each level is responsible for a different object size** — the small maps see large objects, the large maps see small ones. **The pyramid is not a compression trick; it is how one network detects objects across a 5× size range.**
>
> **The scale schedule is principled**: the interval $[0.2,\,1.05]$ split evenly gives 0.2, 0.37, 0.54, 0.71, 0.88, and each level's *second* scale is the **geometric mean with the next level** — $\sqrt{0.2\times0.37}=0.272029$, $\sqrt{0.37\times0.54}=0.446990$, $\sqrt{0.54\times0.71}=0.619193$, $\sqrt{0.71\times0.88}=0.790443$, $\sqrt{0.88\times1.05}=0.961249$. **All five match D2L's printed values.** ✓ *The geometric mean is the right interpolation because scales are multiplicative.*

**D2L's own intuition for why small objects need more samples is exact and worth keeping:** *"$1\times1$, $1\times2$, and $2\times2$ objects can appear on a $2\times2$ image in 4, 2, and 1 possible ways."* **Smaller objects have more possible positions, so sample more of them.**

### 7. SSD — one forward pass, predictions at every scale

**Single Shot Multibox Detection** (Liu et al. 2016): a **base network** (a truncated VGG or ResNet) followed by several **multiscale feature map blocks**, each halving the resolution. **Every block's feature map is used twice** — to generate anchors and to predict their classes and offsets.

**The prediction heads are convolutions, not fully connected layers.** With $a$ anchors per unit and $q$ classes, the class head is a $3\times3$ convolution with $a(q+1)$ output channels and the box head has $a\times4$. **Verified**: $5\times(10+1)=55$ and $3\times(10+1)=33$ channels, matching the printed `[2, 55, 20, 20]` and `[2, 33, 10, 10]`; flattened and concatenated, $20^2\cdot55+10^2\cdot33=22{,}000+3{,}300=\mathbf{25{,}300}$ ✓. For TinySSD, `[1, 5444, 4]`, `[32, 5444, 2]` and $5444\times4=\mathbf{21{,}776}$ ✓.

> [!warning] ⚠️ Why the heads must be convolutions — [[05 - Convolutional Neural Network|ch. 05]] §17's inversion, again
> One $32\times32$ map with 64 channels, $a=4$, $q=1$ needs $32\cdot32\cdot4\cdot2=8{,}192$ class scores.
>
> | head | parameters |
> |---|---|
> | fully connected from $64\cdot32\cdot32=65{,}536$ inputs | **536,879,104** |
> | $3\times3$ convolution with 8 output channels | **4,616** |
> | **ratio** | **116,308×** |
>
> ⇒ **SSD borrows NiN's trick directly**, and it is the only thing that makes per-anchor prediction affordable. **All five of TinySSD's detection heads together are 124,536 parameters — less than 1/800 of VGG-11's single first fully connected layer.**

**A receptive-field check on the downsampling block**, which D2L states and does not derive: each block is conv $3\times3$ → conv $3\times3$ → max-pool $2\times2$ s2. Working outward from the output, $1\times2+(3-1)+(3-1)=\mathbf{6}$ — **a $6\times6$ receptive field on the block's input**, matching D2L's remark and [[05 - Convolutional Neural Network|ch. 05]] §7's recursion run in reverse.

**The loss has two parts:** cross-entropy over anchor classes, plus an **$\ell_1$** loss over the offsets of *positive* anchors only, masked. **D2L is explicit that $\ell_1$ replaces squared loss here** — because offsets can be large and squared loss would let a few bad anchors dominate.

### 8. ⚠️ The imbalance D2L's loss does not address

**Generated TinySSD's full 5,444-anchor set and labelled it against a single object at IoU ≥ 0.5:**

| ground-truth box | positives | background | **ratio** |
|---|---|---|---|
| small, 10% of the image wide | **1** | 5,443 | **5,443 : 1** |
| medium, 25% wide | 44 | 5,400 | 123 : 1 |
| large, 50% wide | 32 | 5,412 | 169 : 1 |
| D2L's dog box | 12 | 5,432 | **453 : 1** |
| D2L's cat box | 36 | 5,408 | 150 : 1 |

> [!warning] ⚠️ THE BEST CASE IS 123 BACKGROUND ANCHORS PER POSITIVE; THE TYPICAL CASE IS HUNDREDS
> D2L's loss is **an unweighted sum of cross-entropy over all 5,444 anchors** plus a masked $\ell_1$ over the positives. **The mask handles the offset loss — D2L says so explicitly — and nothing handles the class loss.**
>
> ⇒ **a model that predicts "background" everywhere achieves 99.8% of the available class accuracy.** The gradient signal from the handful of positive anchors is swamped.
>
> **This is the problem Focal Loss (Lin et al. 2017) was designed for**, down-weighting easy negatives by $(1-p_t)^\gamma$; the standard alternatives are hard-negative mining (used in the original SSD paper) and a fixed positive:negative sampling ratio. **D2L implements none of them and does not raise the issue.** *(Added beyond the source and labelled in the gaps callout.)*

> [!warning] ⚠️ AND THE IoU THRESHOLD IS THE DIAL THAT CONTROLS IT
> Same 50%-wide box, varying the threshold:
>
> | threshold | positives | ratio |
> |---|---|---|
> | 0.3 | **203** | 26 : 1 |
> | 0.4 | 96 | 56 : 1 |
> | **0.5** | 32 | 169 : 1 |
> | 0.6 | 12 | 453 : 1 |
> | 0.7 | **4** | 1,360 : 1 |
>
> **Moving 0.6 → 0.3 multiplies the positive count 16.9× and cuts the imbalance 17×.** *(The best IoU any anchor achieves with this box is 0.7693 — so at threshold 0.8 there would be **no** positives from the threshold pass at all, and only step 2's guarantee would save it.)*
>
> ⇒ ***the threshold is not a detail of the labelling code; it sets how much training signal the detector receives.***

### 9. ⚠️ The R-CNN family — one move, repeated

**R-CNN** (Girshick et al. 2014): selective search proposes ~2,000 regions → **each is resized and pushed through a CNN** → SVMs classify, a linear regression refines the box.

**Fast R-CNN** (Girshick 2015): push **the whole image** through the CNN once, then use **RoI pooling** to extract a fixed-size feature block for each proposal from the shared feature map.

> [!warning] ⚠️ **2,000 CNN forward passes per image → 1. That is the entire difference.**
> D2L describes it as "much repeated computation"; **it is a factor of 2,000.**

**RoI pooling** divides any $h\times w$ region into an $h_2\times w_2$ grid of sub-windows (rounded up) and takes the max of each — **so different-shaped regions produce the same output shape**, which is what lets one head serve every proposal.

**Verified against both printed outputs**, on $\mathsf X=\begin{pmatrix}0&1&2&3\\4&5&6&7\\8&9&10&11\\12&13&14&15\end{pmatrix}$ with `spatial_scale=0.1`:

| region | maps to | $2\times2$ output | D2L prints |
|---|---|---|---|
| $(0,0)$–$(20,20)$ | `X[0:3, 0:3]` | $\begin{pmatrix}5&6\\9&10\end{pmatrix}$ | `[[5,6],[9,10]]` ✓ |
| $(0,10)$–$(30,30)$ | `X[1:4, 0:4]` | $\begin{pmatrix}9&11\\13&15\end{pmatrix}$ | `[[9,11],[13,15]]` ✓ |

**Note the shapes differ ($3\times3$ and $3\times4$) and both outputs are $2\times2$.**

**Faster R-CNN** (Ren et al. 2015) replaces selective search with a **region proposal network** — a small CNN over the shared feature map that emits proposals. **Only now is the detector end-to-end trainable.** **Mask R-CNN** (He et al. 2017) adds a per-pixel mask branch and replaces RoI pooling with **RoI align** (bilinear interpolation instead of rounding) — because pixel-level masks cannot tolerate the quantization RoI pooling introduces.

| model | CNN passes/image | proposals from | end-to-end trainable |
|---|---|---|---|
| R-CNN | **2,000** | selective search | no (SVMs + ridge) |
| Fast R-CNN | 1 | selective search | no (search is fixed) |
| **Faster R-CNN** | 1 | **region proposal net** | **yes** |
| Mask R-CNN | 1 | region proposal net | yes (+ masks) |

> [!warning] ⚠️ THE PATTERN, AND IT IS THE SAME ONE AS ch. 05's ARCHITECTURE HISTORY
> **Every step deletes a hand-designed component and replaces it with a learned one:**
>
> | hand-designed | replaced by | where |
> |---|---|---|
> | SIFT / SURF / HOG features | learned convolution kernels | AlexNet ([[05 - Convolutional Neural Network|ch. 05]] §9) |
> | fully connected classifier head | global average pooling | NiN ([[05 - Convolutional Neural Network|ch. 05]] §11) |
> | selective search | region proposal network | Faster R-CNN |
> | anchor boxes + NMS | set prediction (DETR, 2020) | *beyond D2L* |
>
> ⇒ ***the history of computer vision since 2012 is the systematic deletion of hand-designed stages*** — and **anchor boxes and NMS are the two that survived longest in this chapter and have since gone the same way.**

### 10. Two families, one trade-off

| | **one-stage (SSD, YOLO)** | **two-stage (R-CNN family)** |
|---|---|---|
| structure | anchors → classify + regress, once | propose → classify + regress |
| speed | **fast** (single pass) | slower (proposal + per-RoI head) |
| accuracy on small objects | weaker | **stronger** |
| class imbalance | **severe** (§8) — every anchor is an example | mitigated: proposals are pre-filtered |
| training | simple | more stages |

> [!note] ⚠️ The imbalance of §8 is *the* structural reason for the accuracy gap
> A two-stage detector's first stage **discards most background before the classifier ever sees it**, so its second stage trains on a roughly balanced set. A one-stage detector classifies **all 5,444 anchors every step**. ⇒ *that is precisely why Focal Loss was introduced for one-stage detectors and not for two-stage ones.*

## ✏️ Exercises

> [!example]- Exercise 1 — IoU by hand, and D2L's unanswered exercise 14.4.2
> **(a)** IoU of $[0,0,4,4]$ and $[2,2,6,6]$; of $[0,0,4,4]$ and $[1,1,3,3]$.
> **(b)** Construct two boxes with IoU exactly 0.5 — in two structurally different ways.
> **(c)** What does (b) reveal about IoU?
>
> ---
> **(a)** First: intersection $[2,2,4,4]$ has area 4; union $=16+16-4=28$; **IoU $=4/28=0.142857$.** Second: the small box is nested, area 4; union $=16$; **IoU $=0.250000$.**
>
> **(b)** **Shifted:** two unit squares offset by $d$ give $\mathrm{IoU}=(1-d)/(1+d)$, so $d=\mathbf{1/3}$. **Nested:** a box of exactly half the area inside a larger one gives $\mathrm{IoU}=|\mathcal B|/|\mathcal A|=0.5$ — e.g. side $\sqrt2\approx1.414214$ centred in a side-2 box. **Both verified to 0.500000.**
>
> **(c)** ⚠️ **IoU 0.5 describes two completely different errors — "right size, wrong place" and "right place, wrong size" — and cannot distinguish them.** It also cannot distinguish *how far* two disjoint boxes are: **every** non-overlapping pair scores exactly 0, so IoU provides **no gradient** to move a badly-placed box toward the target. *(Both defects motivated GIoU/DIoU; an addition beyond D2L.)*

> [!example]- Exercise 2 — budget the anchors
> **(a)** For a $600\times800$ image with 4 scales and 3 ratios, how many anchors under each scheme?
> **(b)** How much label memory does that cost?
> **(c)** A 5-level feature pyramid on $256\times256$ with $a$ anchors per unit — how many, and how does it compare to per-pixel?
>
> ---
> **(a)** All pairs: $600\cdot800\cdot4\cdot3=\mathbf{5{,}760{,}000}$. Subset $n+m-1=6$: $600\cdot800\cdot6=\mathbf{2{,}880{,}000}$ — **50.0% saved.**
>
> **(b)** Each anchor needs 1 class + 4 offsets. $2{,}880{,}000\times5=14{,}400{,}000$ numbers $=\mathbf{54.9}$ MB **per image**, in `float32`. At batch size 32 that is 1.76 GB of labels alone.
>
> **(c)** $(32^2+16^2+8^2+4^2+1)\times a=1361a$:
>
> | $a$ | pyramid | per-pixel ($256^2a$) | **ratio** |
> |---|---|---|---|
> | 3 | 4,083 | 196,608 | **48×** |
> | 4 | **5,444** | 262,144 | **48×** |
> | 9 | 12,249 | 589,824 | **48×** |
>
> ⚠️ **The ratio is 48× regardless of $a$** — because $a$ cancels. **The saving comes entirely from sampling positions, not from the anchor shapes**, which is exactly why §3's $n+m-1$ trick (44.4%) is a footnote and §6's pyramid (48×) is the chapter.

> [!example]- Exercise 3 — run the assignment algorithm
> Given the IoU matrix of §4, produce the class labels, the mask, and explain each of the five decisions.
>
> ---
> **Step 2 (guarantee), highest first:**
> - Global max is $x_{4,\text{cat}}=0.745908$ → $A_4$ = **cat**. Discard row 4, cat column.
> - Largest remaining is $x_{1,\text{dog}}=0.141723$ → $A_1$ = **dog**. Discard row 1, dog column.
> - Both ground-truth boxes are now assigned; stop.
>
> **Step 3 (threshold, 0.5) on the rest:**
> - $A_0$: best is dog at 0.053648 < 0.5 → **background (0)**
> - $A_2$: best is cat at 0.565724 ≥ 0.5 → **cat (2)**
> - $A_3$: best is cat at 0.205882 < 0.5 → **background (0)**
>
> **Classes `[0, 1, 2, 0, 2]`; mask `[0,0,0,0, 1,1,1,1, 1,1,1,1, 0,0,0,0, 1,1,1,1]`.** Both match D2L's printouts exactly.
>
> ⚠️ **Note $A_1$: its IoU with the dog is 0.1417 — far below the threshold — and it is still labelled "dog", because step 2 runs first and guarantees every ground-truth box an anchor.** Without that guarantee the dog would have **no positive anchor at all** and could never be learned. *That guarantee is the most important line in the algorithm and D2L presents it as step 1 of 4 without comment.*

> [!example]- Exercise 4 — NMS, and break it
> **(a)** Run NMS on §5's four boxes at $\epsilon=0.5$.
> **(b)** What happens at $\epsilon=0.8$? At $\epsilon=0.3$?
> **(c)** Construct a case where NMS deletes a correct detection.
>
> ---
> **(a)** Sorted by confidence: $B_0$ (0.90), $B_3$ (0.90), $B_1$ (0.80), $B_2$ (0.70). Keep $B_0$; it suppresses $B_1$ (IoU 0.7368) and $B_2$ (0.5454). Keep $B_3$; nothing left to suppress. **Output $\{B_0,B_3\}$.** ✓
>
> **(b)** At $\epsilon=0.8$: $B_0$ suppresses nothing (max IoU 0.7368 < 0.8), so $B_1$ and $B_2$ survive → **three overlapping dog boxes reported.** At $\epsilon=0.3$: same result as 0.5 here, but the margin is larger — $B_2$'s 0.5454 clears 0.3 comfortably.
>
> **(c)** **Two adjacent objects.** Take two genuinely distinct boxes at $[0,0,1,1]$ and $[1/3,0,4/3,1]$ — IoU $=0.5$ from exercise 1. With $\epsilon=0.5$ the second is **not** deleted (the test is strictly greater), but at $d=0.3$ the IoU is $0.7/1.3=\mathbf{0.5385}>0.5$ and it **is** deleted.
>
> ⚠️ **So two real objects whose boxes are within 30% of a box-width of each other are unrecoverable at $\epsilon=0.5$** — two people standing side by side, cars in a queue, cells in a smear. **NMS has no way to distinguish "two boxes on one object" from "two objects".** ⇒ *the only information it uses is geometry; the fix (Soft-NMS) is to decay rather than delete, keeping the decision reversible.*

> [!example]- Exercise 5 — the imbalance, and why SSD's heads are convolutions
> **(a)** For TinySSD (5,444 anchors) with one object covering 25% of the image width, how many anchors are positive at IoU ≥ 0.5? What is the imbalance?
> **(b)** What does D2L's loss do about it?
> **(c)** Cost a fully connected class head against the $3\times3$ convolution SSD uses.
>
> ---
> **(a)** **44 positives, 5,400 background — 123 : 1.** And that is the *most favourable* of five cases tested; a small object gives **1 positive and 5,443 background (5,443 : 1)**, and D2L's own dog box gives **453 : 1**.
>
> **(b)** ⚠️ **Nothing.** The `bbox_masks` variable zeroes the **offset** loss for negatives — D2L states this explicitly — but the class loss is `CrossEntropyLoss(reduction='none')` **summed over every anchor**. A detector predicting "background" everywhere gets 99.8% of the available class accuracy and a near-zero gradient toward changing.
>
> **The standard fixes, none in D2L:** hard-negative mining (the original SSD paper caps the negative:positive ratio at 3:1), a fixed sampling ratio, or **Focal Loss** (Lin et al. 2017), which multiplies the cross-entropy by $(1-p_t)^\gamma$ so confidently-correct negatives contribute almost nothing.
>
> **(c)** One scale: 64-channel $32\times32$ map, $a=4$, $q=1$ → 8,192 class scores.
>
> | head | parameters |
> |---|---|
> | fully connected from 65,536 inputs | **536,879,104** |
> | $3\times3$ convolution, 8 output channels | **4,616** |
> | ratio | **116,308×** |
>
> **All five of TinySSD's heads (class + box) total 124,536 parameters.** ⇒ ***the entire detection apparatus is smaller than 1/800 of VGG-11's first fully connected layer*** — [[05 - Convolutional Neural Network|ch. 05]] §17's inversion doing useful work.

## 📝 Summary

- **Augmentation and fine-tuning are both statements about invariance**: augmentation asserts the label survives a transformation; fine-tuning asserts a source model's features transfer. **Both fail when the assertion is false**, and a horizontal flip destroys any chiral task.
- **Fine-tuning's operational content is the learning-rate asymmetry**: pretrained layers at the base rate, the fresh head at **10×** — and D2L's from-scratch baseline uses exactly the head's rate, $10\times$ the fine-tuned base.
- **⚠️ IoU 0.5 requires $d=1/3$**, i.e. two-thirds shared width, because the union grows as the intersection shrinks. **And IoU 0.5 is reachable by shifting *or* by nesting** — it cannot distinguish "wrong place" from "wrong size", and gives **zero gradient** for any disjoint pair.
- **⚠️ Per-pixel anchors are 2,042,040 for one 561×728 image** — 38.9 MB of labels. The $n+m-1$ subset trick saves **44.4%**; the feature-map pyramid saves **48× at every anchors-per-unit setting**, and $375\times$ against D2L's own per-pixel figure. **The saving comes from sampling positions, not shapes.**
- **⚠️ The assignment algorithm guarantees every ground-truth box an anchor *before* the threshold applies** — which is why $A_1$ is labelled "dog" at an IoU of **0.1417**. Without it, small or oddly-shaped objects would have no positive anchor at all.
- **⚠️ All three of D2L's printed labelling tensors reproduce** from five anchors and two ground-truth boxes: classes `[0,1,2,0,2]`, the 20-element mask, and all 20 offsets. **So do the NMS output, both RoI-pooling outputs, the 2,042,040 and 5,444 anchor counts, the 25,300 concatenation, and all five geometric-mean scales.**
- **⚠️ NMS is greedy and deletes**: two genuinely distinct objects overlapping above $\epsilon$ leave only one, unrecoverably. **The threshold converts false positives into false negatives**, and Soft-NMS defers the decision by decaying scores instead.
- **The SSD pyramid assigns object sizes to levels** — 51–70 px at the $32\times32$ map, 225–246 px at $1\times1$ — with scales from $[0.2,1.05]$ split evenly and each level's second scale the **geometric mean with the next**, which is the right interpolation because scales are multiplicative.
- **⚠️ SSD's foreground/background imbalance is 123:1 at best and 5,443:1 for a small object, and D2L's loss addresses only the offset half.** The mask zeroes negatives' offset loss; the class loss is summed over all 5,444 anchors. **A "background everywhere" predictor scores 99.8%.** Focal Loss, hard-negative mining and sampling ratios all exist for this and none appears in the chapter.
- **⚠️ The IoU threshold is the dial that sets the training signal**: 0.6 → 0.3 multiplies positives **16.9×** (12 → 203) and cuts the imbalance from 453:1 to 26:1.
- **SSD's heads are convolutions because a fully connected head would cost 116,308× more** — all five heads together are **124,536 parameters**, under 1/800 of VGG-11's first fully connected layer.
- **⚠️ Fast R-CNN is 2,000× fewer CNN passes than R-CNN**; RoI pooling turns any region shape into a fixed one so a single head serves all proposals; Faster R-CNN then deletes selective search. **The whole family is one move repeated: replace a hand-designed stage with a learned one** — the same pattern as SIFT → learned kernels and fc head → global average pooling.
- **One-stage detectors are fast and imbalance-prone; two-stage detectors pre-filter background and are stronger on small objects.** §8's imbalance is the structural cause of that gap.

## ⚠️ Important Notes

1. **⚠️ Anchor counts are a memory problem before they are a compute problem.** 2,042,040 anchors × 5 label numbers × 4 bytes = **38.9 MB per training image**. Check the label budget before the FLOP budget.
2. **⚠️ Never read an IoU threshold as a percentage of overlap.** 0.5 means two-thirds shared width for equal boxes. **Raising a threshold from 0.5 to 0.7 cuts positive anchors by 8× in the case measured** — a far larger change than the numbers suggest.
3. **⚠️ Check the positive/negative ratio before trusting any detection loss.** If it is 100:1 or worse and the loss is unweighted cross-entropy, the model is being trained mostly to say "background". **This is the vault's recurring plausible-wrong-answer-with-no-error**: training converges, loss falls, and the detector detects nothing.
4. **⚠️ NMS is applied per class, and duplicates across classes survive.** Two boxes on the same object with different predicted classes are not compared. That is usually correct and occasionally not.
5. **⚠️ The assignment algorithm and NMS use the same IoU with *different* thresholds for opposite purposes** — labelling (is this anchor responsible?) and de-duplication (is this a repeat?). **Conflating the two is a common bug**; they need not be equal and often are not.
6. **⚠️ Standardized offsets are not raw offsets.** The $\times10$ and $\times5$ factors ($\sigma=0.1,0.2$) must be applied when labelling **and inverted when decoding** — D2L's `offset_inverse` divides by 10 and 5. **Mismatching them produces boxes in roughly the right place and the wrong size**, which looks like a model problem and is an arithmetic one.
7. **⚠️ A printed near-zero can be an exact zero.** D2L's offset index 18 prints `4.17e-06`; the widths are exactly equal so the true value is $5\log 1=0$. *Read what computed the number.*
8. **⚠️ Feature-map level determines detectable object size.** An object smaller than a level's stride is invisible to that level. **A detector that misses small objects usually needs a higher-resolution feature map, not more training** — the receptive-field argument of [[05 - Convolutional Neural Network|ch. 05]] §7.
9. **⚠️ RoI pooling rounds; RoI align interpolates.** For boxes the rounding is tolerable; **for pixel masks it is not**, which is the single change that made Mask R-CNN work.
10. **⚠️ Fine-tuning with one learning rate destroys the backbone.** The random head produces large gradients that flow back into weights that were already correct. **Use parameter groups, or freeze the backbone for the first epochs.**
11. **⚠️ Augmentation must match the test distribution.** D2L trains with `RandomResizedCrop(224)` and tests with `Resize(256)` + `CenterCrop(224)`. **Different pipelines for train and test are deliberate and are a classic source of silent train/test skew when copied carelessly.**
12. **Selective search is not learned and not differentiable** — which is why R-CNN and Fast R-CNN are *not* end-to-end trainable despite both containing a CNN. **"Contains a neural network" and "is trained end to end" are different claims.**
13. **The anchor-and-NMS paradigm has itself been replaced.** DETR (2020) treats detection as direct set prediction, removing both. **This chapter's two most intricate components are the ones the field deleted next** — the pattern of §9 applied to §9. *(Beyond D2L.)*
14. **D2L's banana dataset has exactly one object per image**, which makes the imbalance of §8 maximal and hides every multi-object failure mode of NMS. **A benchmark that cannot exhibit a failure cannot demonstrate its absence** — the rule from [[04 - Neural Network|ch. 04]] §23.

> [!warning] Gaps in the source material
> **All figures are images and never extract.** **Recovered because the prose states their content**: Fig. 14.4.1 (IoU as intersection over union), Fig. 14.4.2 (the assignment algorithm — the prose narrates every step, $x_{23}\to B_3$, $x_{71}\to B_1$, $x_{54}\to B_4$, $x_{92}\to B_2$), Fig. 14.7.1 (SSD's base network plus multiscale blocks), Fig. 14.8.1–14.8.2 (R-CNN and Fast R-CNN pipelines), Fig. 14.8.3 (the $2\times2$ RoI pooling example — the prose names all four sub-window maxima, 5, 6, 9, 10). **Genuinely lost**: the cat/dog photograph and every anchor-box visualization drawn on it, the augmentation grids (§14.1's flips, crops and colour jitters), the hot-dog samples, and the multiscale anchor displays. **No accuracy figures survive** — every training run in §14.1, §14.2 and §14.7 reports through a lost `Animator` plot, which is why this chapter quotes none.
>
> **Code listings lose their indentation** and were re-derived; **printed code *outputs* extract intact**, which is what made every verification here possible — and this chapter's source is unusually generous with them.
>
> **No new cipher entries were needed.** The table in this subject's `CLAUDE.md` covered every formula, including §14.4.3's offset transformation, where the deleted fraction bars and Greek letters had to be reconstructed from the numerical result.
>
> **Added beyond D2L, and labelled as mine throughout:**
> - **The entire IoU sensitivity analysis** of §2 — the $(1-d)/(1+d)$ closed form, the $d=1/3$ answer to D2L's unanswered exercise 14.4.2, the nested-box construction, and the observation that IoU cannot separate displacement from mis-sizing or provide gradient for disjoint boxes. *(GIoU/DIoU are named as the modern response; the book predates neither but mentions neither.)*
> - **The IoU matrix of §4.** D2L narrates the assignment in prose and prints only its result; the five-by-two matrix that makes the narration checkable is computed here.
> - **The whole of §8 and §11** — TinySSD's 5,444-anchor set regenerated, labelled against five different ground-truth boxes, and the 123:1 to 5,443:1 imbalance measured, plus the threshold sensitivity table. **Focal Loss and hard-negative mining are additions; D2L raises neither.**
> - **The 375× and 48× multiscale reductions** (§6) and the observation that the ratio is independent of anchors-per-unit.
> - **The head parameter comparison** (§7, exercise 5): 536,879,104 against 4,616, and the 124,536-parameter total for all five heads.
> - **The 2,000× figure** for R-CNN → Fast R-CNN (§9) and the "delete a hand-designed stage" table, which connects this chapter to ch. 05's architecture history.
> - **The NMS failure construction** in exercise 4 and the observation that the threshold converts false positives into false negatives.
> - **The label-memory arithmetic** (§3, exercise 2) and the one-stage/two-stage table of §10.
> - **The `4.17e-06` catch** (§4) — a printed value that is an exact zero.
> - **The fine-tuning learning-rate observation** (§1) that D2L's from-scratch baseline runs at exactly the fine-tuned head's rate.
>
> **No discrepancies found in this range.** Every printed number that could be checked was checked and every one was correct — the cleanest section of D2L encountered so far in this subject. *(The offsets agree only to the three significant figures D2L prints, which is a display convention and not a discrepancy.)*
>
> **Deliberately deferred, not omitted:** **§14.6 (the banana detection dataset)** is a data-loading walkthrough, used here only for the facts that carry a result — 1,000 training and 100 validation images, one object per image, which §8 and Important Note 14 rely on. **§14.9–14.11 (semantic segmentation, transposed convolution, fully convolutional networks), §14.12 (style transfer) and §14.13–14.14 (the CIFAR-10 and dog-breed Kaggle competitions) are outside the syllabus topic** "Object Detection" and are not covered; **transposed convolution is the one that would most repay adding** if segmentation is examined. **The Fashion-MNIST/CIFAR-10 augmentation training runs (§14.1.2) and the hot-dog fine-tuning run (§14.2.2)** are reported qualitatively because their results exist only in lost figures.
>
> **Left as the source states it:** all citations (Girshick et al. 2014, Girshick 2015, Ren et al. 2015, He et al. 2017, Liu et al. 2016, Uijlings et al. 2013, Bodla et al. 2017); the claim that ImageNet cost "millions of dollars from research funding"; the assertion that selective search produces "high-quality" proposals, which is not evaluated; and the choice of $\sigma_x=\sigma_y=0.1$, $\sigma_w=\sigma_h=0.2$, which D2L presents as "a common transformation" without derivation and which is inherited from the R-CNN literature.

**Previous:** [[05 - Convolutional Neural Network]] · **Next:** [[07 - Recurrent Neural Network]]
