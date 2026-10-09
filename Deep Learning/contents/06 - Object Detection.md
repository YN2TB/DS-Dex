---
subject: Deep Learning
chapter: 6
tags: [ds, deep-learning, object-detection, anchor-boxes, iou, nms, ssd, r-cnn, transfer-learning, augmentation]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, §14.1–14.8 (Image Augmentation, Fine-Tuning, Bounding Boxes, Anchor Boxes, Multiscale Detection, the Detection Dataset, SSD, R-CNNs)"
---

# Object Detection

Classification says what is in an image; detection says what and where, for every object. D2L §14.1–14.8 covers augmentation and fine-tuning, then bounding boxes, anchor boxes, IoU, anchor labelling, non-maximum suppression, multiscale detection, SSD and the R-CNN family. Every printed tensor in this range was recomputed and matches; no discrepancies were found.

## 📘 Main Knowledge

### 1. Augmentation and fine-tuning

**Image augmentation** applies random transformations (flips, crops, colour changes) to training images. It enlarges the training set and, more importantly, makes the model less dependent on attributes such as position or colour. D2L thinks augmentation was probably essential to AlexNet's success.

Each augmentation assumes the label does not change under that transformation. A horizontal flip is fine for cats but wrong for digits, text or anything with handedness. Choose augmentations from the task's actual symmetries.

**Fine-tuning** (transfer learning):
1. Pretrain a source model on a large dataset (ImageNet).
2. Copy all layers and weights except the output layer.
3. Add a new, randomly initialized output layer for the target classes.
4. Train on target data: the new layer from scratch, the rest lightly.

D2L gives the new output layer 10× the base learning rate:
```
[{'params': feature_params},
 {'params': net.fc.parameters(), 'lr': learning_rate * 10}]
```
Pretrained weights are already close to right; the head is random. A single large learning rate for everything can wreck the pretrained backbone. (D2L's from-scratch baseline uses $5\times10^{-4}$, the same rate as the fine-tuned head.) This relies on the stem/body/head split of [[05 - Convolutional Neural Network|ch. 05]]: early layers learn general features.

### 2. Bounding boxes and IoU

A box is $(x_1,y_1,x_2,y_2)$ (corners) or $(c_x,c_y,w,h)$ (centre and size).

**Intersection over union** (Jaccard index):
$$J(\mathcal A,\mathcal B)=\frac{|\mathcal A\cap\mathcal B|}{|\mathcal A\cup\mathcal B|}\in[0,1]$$

For two unit squares shifted horizontally by $d$:
$$\mathrm{IoU}=\frac{1-d}{1+d}$$

| $d$ | IoU |
|---|---|
| 0 | 1.0000 |
| 1/3 | 0.5000 |
| 0.5 | 0.3333 |
| 1 | 0 |

IoU 0.5 needs the boxes to share two-thirds of their width, since the union grows as the intersection shrinks. IoU 0.5 is also reached by a box with half the area nested inside another (side $\sqrt2$ inside side 2). So IoU cannot tell "wrong place" from "wrong size", and every pair of disjoint boxes scores 0, which gives no gradient. (GIoU/DIoU losses address this; beyond D2L.)

### 3. Anchor boxes

At each pixel, generate boxes with scale $s\in(0,1]$ and aspect ratio $r$: width $ws\sqrt r$, height $hs/\sqrt r$. With $n$ scales and $m$ ratios, D2L keeps only combinations containing $s_1$ or $r_1$:
$$(s_1,r_1),\dots,(s_1,r_m),(s_2,r_1),\dots,(s_n,r_1)\quad\Rightarrow\quad n+m-1 \text{ per pixel}$$
(44.4% fewer than all $nm$ pairs at $3\times3$.)

On a $561\times728$ image with 5 anchors per pixel: $561\times728\times5=2{,}042{,}040$ anchors, matching D2L's `torch.Size([1, 2042040, 4])`. With one class and four offsets each, that is 38.9 MB of labels for one image. Placing anchors at every pixel is the real cost; §6 fixes it.

### 4. Labelling anchors

Each anchor needs a class and four offsets. Given the IoU matrix $\mathbf X$ (anchors × ground-truth boxes):

1. Take the largest $x_{ij}$, assign box $B_j$ to anchor $A_i$, and remove row $i$ and column $j$.
2. Repeat until every ground-truth box is assigned.
3. Every other anchor gets its best box only if that IoU exceeds a threshold (0.5); otherwise it is background.

D2L's example (IoU matrix computed here):

| | dog | cat |
|---|---|---|
| $A_0$ | 0.053648 | 0 |
| $A_1$ | 0.141723 | 0 |
| $A_2$ | 0 | 0.565724 |
| $A_3$ | 0 | 0.205882 |
| $A_4$ | 0 | 0.745908 |

$A_4$ → cat (0.7459); then $A_1$ → dog (0.1417). Threshold pass: $A_0$ background, $A_2$ cat (0.5657), $A_3$ background. Result `[0, 1, 2, 0, 2]`, as printed.

Step 2 guarantees every object at least one anchor, which is why $A_1$ is labelled dog despite IoU 0.14. Without it, small or oddly shaped objects could have no positive anchors.

**Offsets** encode the box relative to the anchor, standardized:
$$\left(\frac{(x_b-x_a)/w_a}{0.1},\ \frac{(y_b-y_a)/h_a}{0.1},\ \frac{\log(w_b/w_a)}{0.2},\ \frac{\log(h_b/h_a)}{0.2}\right)$$
i.e. centre offsets ×10, log size ratios ×5, so one $\ell_1$ loss weights all four similarly. Decoding must undo the scaling. All 20 printed offsets and the mask reproduce from the five anchors and two boxes. (Offset 18 prints `4.17e-06`; the two widths are equal, so the exact value is $5\log1=0$.)

### 5. Non-maximum suppression

Many anchors cover the same object. NMS sorts predictions by confidence, keeps the top one, deletes all boxes with IoU above $\epsilon$ with it, and repeats.

D2L's example (confidences 0.90, 0.80, 0.70, 0.90; $\epsilon=0.5$):

| | $B_0$ | $B_1$ | $B_2$ | $B_3$ |
|---|---|---|---|---|
| $B_0$ | 1 | 0.7368 | 0.5454 | 0 |
| $B_1$ | 0.7368 | 1 | 0.6306 | 0.0115 |
| $B_2$ | 0.5454 | 0.6306 | 1 | 0.0839 |
| $B_3$ | 0 | 0.0115 | 0.0839 | 1 |

Keep $B_0$, delete $B_1$ and $B_2$; keep $B_3$. Matches D2L.

NMS only uses geometry. Two real objects that overlap above $\epsilon$ (people side by side, cars in a queue) lose the lower-scoring one permanently. The threshold trades duplicate detections for missed objects (D2L ex. 14.4.4). Soft-NMS lowers scores instead of deleting.

### 6. Multiscale detection

Put anchors on feature maps instead of pixels. Each feature-map cell has a receptive field covering a patch of the image ([[05 - Convolutional Neural Network|ch. 05]] §7).

TinySSD uses five levels with 4 anchors per cell:
$$(32^2+16^2+8^2+4^2+1)\times4=5{,}444$$

| map | cells | anchors | stride | anchor scales | object size (px) |
|---|---|---|---|---|---|
| 32×32 | 1,024 | 4,096 | 8 | 0.20–0.272 | 51–70 |
| 16×16 | 256 | 1,024 | 16 | 0.37–0.447 | 95–114 |
| 8×8 | 64 | 256 | 32 | 0.54–0.619 | 138–158 |
| 4×4 | 16 | 64 | 64 | 0.71–0.790 | 182–202 |
| 1×1 | 1 | 4 | 256 | 0.88–0.961 | 225–246 |

Against per-pixel anchors on the same $256\times256$ image this is 48× fewer, whatever the number of anchors per position (it cancels). Each level covers a different object size. Scales split $[0.2,1.05]$ evenly, and each level's second scale is the geometric mean with the next ($\sqrt{0.2\times0.37}=0.272$, …), all matching D2L.

D2L's intuition: on a $2\times2$ image, $1\times1$, $1\times2$ and $2\times2$ objects fit in 4, 2 and 1 positions, so small objects need more samples.

### 7. SSD

Single Shot Multibox Detection (Liu et al. 2016): a base network followed by downsampling blocks; each block's feature map generates anchors and predicts their classes and offsets.

The heads are $3\times3$ convolutions: $a(q+1)$ output channels for classes and $4a$ for offsets. Checked: $5\times11=55$ and $3\times11=33$ channels, concatenated length $20^2\cdot55+10^2\cdot33=25{,}300$; TinySSD's 5,444 anchors give 21,776 offsets.

A dense class head on one 64-channel $32\times32$ map ($a=4$, $q=1$) would need 536,879,104 parameters; the $3\times3$ conv needs 4,616. All five TinySSD heads total 124,536 parameters.

Each downsampling block (two $3\times3$ convs + $2\times2$ pool) has a $6\times6$ receptive field on its input.

Loss: cross-entropy on anchor classes + $\ell_1$ on offsets of positive anchors only (masked). D2L uses $\ell_1$ so that a few large offsets do not dominate.

### 8. Class imbalance

TinySSD's 5,444 anchors labelled against one object (IoU ≥ 0.5; computed here):

| object | positives | background | ratio |
|---|---|---|---|
| small, 10% of width | 1 | 5,443 | 5,443:1 |
| medium, 25% | 44 | 5,400 | 123:1 |
| large, 50% | 32 | 5,412 | 169:1 |
| D2L's dog box | 12 | 5,432 | 453:1 |
| D2L's cat box | 36 | 5,408 | 150:1 |

D2L's mask removes negatives from the offset loss, but the class loss sums over all anchors. Predicting "background" everywhere is 99.8% correct. Standard fixes not in D2L: hard-negative mining (original SSD: at most 3 negatives per positive), fixed sampling ratios, and **Focal Loss** (Lin et al. 2017), which multiplies cross-entropy by $(1-p_t)^\gamma$.

The IoU threshold sets how many positives there are (50%-wide box):

| threshold | positives | ratio |
|---|---|---|
| 0.3 | 203 | 26:1 |
| 0.4 | 96 | 56:1 |
| 0.5 | 32 | 169:1 |
| 0.6 | 12 | 453:1 |
| 0.7 | 4 | 1,360:1 |

(The best anchor reaches IoU 0.7693, so at 0.8 only step 2 would provide a positive.)

### 9. The R-CNN family

- **R-CNN** (Girshick et al. 2014): selective search proposes ~2,000 regions; each is resized and run through a CNN; SVMs classify and linear regression refines boxes.
- **Fast R-CNN** (2015): run the CNN once on the whole image and use **RoI pooling** to extract a fixed-size feature for each proposal. That is 2,000 CNN passes reduced to 1.
- **Faster R-CNN** (Ren et al. 2015): a **region proposal network** replaces selective search, making the detector trainable end to end.
- **Mask R-CNN** (He et al. 2017): adds a per-pixel mask branch and uses **RoI align** (bilinear interpolation) instead of rounding.

**RoI pooling** splits any region into an $h_2\times w_2$ grid and takes each cell's max, so different region shapes give the same output size. On $\mathsf X=0..15$ ($4\times4$) with `spatial_scale=0.1`:

| region | maps to | $2\times2$ output |
|---|---|---|
| (0,0)–(20,20) | `X[0:3, 0:3]` | $\begin{pmatrix}5&6\\9&10\end{pmatrix}$ |
| (0,10)–(30,30) | `X[1:4, 0:4]` | $\begin{pmatrix}9&11\\13&15\end{pmatrix}$ |

| model | CNN passes | proposals | end to end |
|---|---|---|---|
| R-CNN | ~2,000 | selective search | no |
| Fast R-CNN | 1 | selective search | no |
| Faster R-CNN | 1 | RPN | yes |
| Mask R-CNN | 1 | RPN | yes (+ masks) |

Each step replaces a hand-designed stage with a learned one, as in [[05 - Convolutional Neural Network|ch. 05]] (hand features → learned kernels; dense head → global pooling). DETR (2020, beyond D2L) later removed anchors and NMS too.

### 10. One-stage vs two-stage

| | one-stage (SSD, YOLO) | two-stage (R-CNN family) |
|---|---|---|
| structure | classify and regress all anchors at once | propose, then classify and regress |
| speed | faster | slower |
| small objects | weaker | stronger |
| class imbalance | severe: every anchor is an example | reduced: proposals filter out most background |

The imbalance in §8 is why Focal Loss was designed for one-stage detectors.

## ✏️ Exercises

> [!example]- **1.** *(Easy) IoU*
> **(a)** IoU of $[0,0,4,4]$ with $[2,2,6,6]$, and with $[1,1,3,3]$. **(b)** Build two boxes with IoU 0.5 in two different ways. **(c)** What does (b) show?
>
> ---
> **(a)** Intersection 4, union 28: 0.142857. Nested: 4/16 = 0.25.
>
> **(b)** Shift two unit squares by $d=1/3$; or nest a box of half the area (side $\sqrt2$ inside side 2). Both give 0.500000.
>
> **(c)** IoU cannot separate position errors from size errors, and all disjoint pairs score 0 (no gradient).

> [!example]- **2.** *(Easy–medium) Anchor budget*
> **(a)** $600\times800$ image, 4 scales, 3 ratios: anchors with all pairs vs $n+m-1$? **(b)** Label memory? **(c)** A 5-level pyramid on $256\times256$ with $a$ anchors per cell vs per-pixel.
>
> ---
> **(a)** All pairs 5,760,000; subset (6 per pixel) 2,880,000.
>
> **(b)** $2{,}880{,}000\times5$ floats = 54.9 MB per image (1.76 GB for a batch of 32).
>
> **(c)** $1361a$ vs $65{,}536a$: 48× fewer for any $a$ ($a=4$: 5,444 vs 262,144).

> [!example]- **3.** *(Medium) Run the assignment*
> Use the IoU matrix in §4. Give the classes and explain each anchor.
>
> ---
> Step 2: $A_4$ → cat (0.7459), then $A_1$ → dog (0.1417); both boxes assigned. Step 3: $A_0$ (0.0536) background, $A_2$ (0.5657) cat, $A_3$ (0.2059) background. Classes `[0, 1, 2, 0, 2]`, mask `[0,0,0,0, 1,1,1,1, 1,1,1,1, 0,0,0,0, 1,1,1,1]`. $A_1$ is positive only because step 2 runs first.

> [!example]- **4.** *(Medium–hard) NMS*
> **(a)** Run NMS on §5's boxes at $\epsilon=0.5$. **(b)** At $\epsilon=0.8$? **(c)** Construct a case where NMS deletes a correct detection.
>
> ---
> **(a)** Keep $B_0$, suppress $B_1$ (0.7368), $B_2$ (0.5454); keep $B_3$.
>
> **(b)** Nothing exceeds 0.8 against $B_0$, so $B_1$ and $B_2$ survive: three boxes on one dog.
>
> **(c)** Two real objects $[0,0,1,1]$ and $[0.3,0,1.3,1]$ have IoU $0.7/1.3=0.5385>0.5$, so the weaker one is deleted. NMS cannot tell two objects from two boxes on one object.

> [!example]- **5.** *(Hard) Imbalance and conv heads*
> **(a)** TinySSD, one object 25% wide: positives at IoU ≥ 0.5 and the ratio? **(b)** What does D2L's loss do about it? **(c)** Dense vs conv class head on a 64-channel $32\times32$ map, $a=4$, $q=1$.
>
> ---
> **(a)** 44 positives, 5,400 background (123:1). A small object gives 5,443:1.
>
> **(b)** Nothing for the class loss: the mask only affects offsets. Fixes: hard-negative mining, sampling ratios, Focal Loss.
>
> **(c)** 8,192 scores. Dense from 65,536 inputs: 536,879,104 parameters. $3\times3$ conv with 8 channels: 4,616 (116,308× fewer).

## 📝 Summary

- Augmentation and fine-tuning both assume an invariance; check it holds. Fine-tune with a larger learning rate (10×) on the new head.
- IoU 0.5 means two-thirds shared width for equal boxes; IoU mixes position and size errors and is 0 for all disjoint boxes.
- Per-pixel anchors explode (2,042,040 for one image); feature-map anchors cut this ~48× and assign object sizes to levels.
- Anchor labelling first guarantees each object an anchor, then thresholds the rest. Offsets are standardized (×10 centre, ×5 log size).
- NMS removes duplicates greedily and can delete real neighbouring objects.
- SSD predicts classes and offsets with conv heads on several feature maps; its class loss suffers 123:1 to 5,443:1 background imbalance, which Focal Loss or hard-negative mining fix.
- The IoU threshold controls how many positives there are (0.6 → 0.3: 16.9× more).
- R-CNN → Fast R-CNN (one CNN pass + RoI pooling) → Faster R-CNN (learned proposals) → Mask R-CNN (RoI align, masks).
- One-stage detectors are faster; two-stage detectors filter background first and handle small objects better.

## ⚠️ Important Notes

1. Anchor labels can cost more memory than you expect (38.9 MB per image at 2M anchors).
2. IoU thresholds are stricter than they sound: 0.5 → 0.7 cut positives 8× in the measured case.
3. Check the positive:negative ratio before trusting a detection loss; an unweighted loss can train a detector that finds nothing.
4. NMS runs per class.
5. Labelling and NMS both use IoU thresholds but for different purposes; they need not be equal.
6. Apply the offset standardization when labelling and invert it when decoding, or boxes come out the wrong size.
7. Objects smaller than a level's stride are invisible to that level; missing small objects often means you need a higher-resolution map.
8. RoI pooling rounds coordinates; masks need RoI align.
9. Freeze the backbone or use parameter groups when fine-tuning.
10. D2L trains with `RandomResizedCrop(224)` and tests with `Resize(256)` + `CenterCrop(224)`. The difference is deliberate; copy both correctly.
11. A detector containing a CNN is not necessarily end-to-end trainable (R-CNN, Fast R-CNN).
12. D2L's banana dataset has one object per image, so it cannot reveal NMS problems with crowded scenes.

> [!warning] Gaps in the source material
> - **Figures:** IoU, assignment, SSD, R-CNN and RoI pooling diagrams are reconstructed from the prose. Lost: the cat/dog photo with anchors, augmentation grids, hot-dog samples, multiscale anchor plots, and all training curves (so no accuracies are quoted).
> - **Added by me:** the IoU formula $(1-d)/(1+d)$ and the nested case (D2L ex. 14.4.2); the IoU matrix in §4; the imbalance and threshold tables (§8); the 48× pyramid saving; the head parameter comparison; the R-CNN 2,000× figure and comparison tables; the NMS failure case; label-memory arithmetic; the `4.17e-06` note. Focal Loss, hard-negative mining, Soft-NMS, GIoU and DETR are named beyond D2L.
> - **No discrepancies** in this range.
> - **Skipped:** the banana dataset loader (§14.6) except its one-object-per-image fact; segmentation, transposed convolution, FCN, style transfer and the Kaggle sections (§14.9–14.14), which are outside the syllabus topic.

**Previous:** [[05 - Convolutional Neural Network]] · **Next:** [[07 - Recurrent Neural Network]]
