---
subject: Computer Vision
chapter: 9
tags: [ds, computer-vision, segmentation, fcn, u-net, deeplab, dice, iou, panoptic-quality, mask-r-cnn, roialign, mask2former, sam]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 09: Image Segmentation (47 slides); Long et al. 2015 (FCN), Ronneberger et al. 2015 (U-Net), Chen et al. 2018 (DeepLabv3+), Kirillov et al. 2019 (Panoptic Segmentation), He et al. 2017 (Mask R-CNN), Cheng et al. 2022 (Mask2Former), Kirillov et al. 2023 (SAM)"
---

# Image Segmentation

Week 9. A box is cheap to annotate and compare, but it is the wrong shape for anything rotated, articulated or hollow ([[07 - Object Detection I|ch. 07]]). Today the output is a **mask**: a label for every pixel. By the end of the lecture, detection looks like a special case of segmentation.

**Three tasks, one word (slide 3):**

| Task | Output | Two touching dogs |
|---|---|---|
| **Semantic** | a class for every pixel | one "dog" region; the two dogs are not separated |
| **Instance** | a mask + class for every *countable* object; background ignored | dog #1 and dog #2, each with its own mask; grass unlabelled |
| **Panoptic** | every pixel gets a class **and**, for countable classes, an instance id | dog #1, dog #2 and the grass |

Panoptic vocabulary: **things** are countable (car, person, dog); **stuff** is amorphous (sky, road, grass). Stuff gets a class only; things get a class and an id.

## 📘 Main Knowledge

### 1. Semantic segmentation: getting the resolution back (slides 6–10)

**The problem before any architecture (slide 6).** A classifier backbone shrinks the image. Even a *perfect* classifier that labels each output cell correctly can only produce a blocky mask. The lecturer's 256×256 car image:

| Output stride | Grid | Best IoU on the car |
|---|---|---|
| 4 | 64×64 | 0.90 |
| 8 | 32×32 | 0.84 |
| 16 | 16×16 | 0.67 |
| 32 | 8×8 | **0.39** |

So a stride-32 map caps IoU at 0.39 on a car-sized object before any learning happens. The errors sit on the boundary.

**Why this is not detection with more outputs (slide 7).** Two pulls in opposite directions:
- **Receptive field vs resolution.** Deep layers see enough context to know *what* a pixel is, but they've been downsampled so far they've lost *where* it is.
- **Classification throws position away** on purpose (pooling, then FC layers that flatten the map). Segmentation needs position back.

#### FCN: read the classifier differently (Long et al., 2015) (slides 8–10)

**Convolutionalisation.** A fully connected layer on a 7×7×512 map is the same computation as a 7×7 convolution with 4096 filters. Rewrite fc6/fc7 as convolutions (fc7 and the classifier become 1×1 convs) and the network accepts **any input size**. On a 224×224 image it outputs one score vector, as before. On a larger image it slides, and the output is a **coarse heatmap of class scores** (e.g. a "car" heatmap) instead of one label. For a 384×384 input at stride 32: a 12×12 map, and the 7×7 "fc6" conv gives $12 - 7 + 1 = 6$, so a 6×6 score map.

**FCN architecture (slide 9).** VGG-16 encoder; resolution halves at each pool:

| Stage | Size |
|---|---|
| pool1 … pool5 | $H/2 \times W/2 \times 64$ … $H/32 \times W/32 \times 512$ |
| fc6/fc7 as convs | $H/32 \times W/32 \times 4096$ |
| 1×1 conv → class scores | $H/32 \times W/32 \times C$ |

Decoder (FCN-8s): upsample ×2, add a 1×1-conv score map from **pool4** ($H/16$); upsample ×2, add a score map from **pool3** ($H/8$); upsample ×8 to $H \times W \times C$. Fusion is an element-wise sum of two $C$-channel score maps. A per-pixel softmax gives the label.

**What skip connections buy (slide 10).** Coarse layers know *what*, fine layers know *where*. In the slide's simulation on the car: FCN-32s IoU 0.39, FCN-16s 0.49, FCN-8s 0.66, with most errors at the boundary. On PASCAL VOC 2012, **FCN-8s reached 62.2 mean IU against 51.6** for the previous best (a 20% relative gain), at under 0.2 s per image.

### 2. Four ways to upsample (slide 11)

All take a 4×4 map to 8×8 (×2):

| Method | How | Learned? |
|---|---|---|
| **Nearest neighbour** | copy each value into a 2×2 block | no |
| **Bilinear** | each output is a weighted average of the four nearest inputs | no |
| **Max unpooling** | put each value back in the slot its max-pool took it from (indices saved during pooling); other slots are 0 | no (needs the saved indices) |
| **Transposed convolution** | each input value scales a learned kernel; the copies are laid at stride $s$ and **summed where they overlap** | **yes** |

**Bilinear with `align_corners=True`** maps output position $i$ to input position $i \cdot \frac{n_{in}-1}{n_{out}-1}$, so the four corners keep their input values. For input row $[1, 2, 3, 2]$ and 8 outputs, position 1 maps to $3/7 = 0.43$, giving $1 + 0.43 = 1.43$. The slide's full row is $1, 1.43, 1.86, 2.29, 2.71, 2.86, 2.43, 2$ (checked).

**Transposed convolution output size:**

$$n_{out} = (n_{in} - 1)\,s - 2p + k + \text{output\_padding}$$

The slide's example: $n_{in} = 4$, $k = 3$, $s = 2$, $p = 1$, output padding 1 gives $3 \cdot 2 - 2 + 3 + 1 = 8$.

**The checkerboard artefact.** When the kernel size isn't a multiple of the stride, output pixels receive different numbers of overlapping copies. With $k = 3$, $s = 2$, the counts along one axis alternate $1, 2, 1, 2, \dots$, so in 2D they alternate 1, 2 and 4: a checkerboard pattern before any learning. With $k = 4$, $s = 2$ every interior pixel gets exactly 2. Fixes: choose $k$ divisible by $s$, or upsample with bilinear/nearest and then apply an ordinary conv.

### 3. U-Net (Ronneberger et al., 2015) (slides 12–16)

**Architecture (slide 12).** A symmetric encoder–decoder:
- **Contracting path:** at each level two unpadded 3×3 convs + ReLU, then 2×2 max-pool. Channels 64 → 128 → 256 → 512 → 1024.
- **Expanding path:** 2×2 up-conv (halves the channels), **concatenate** the encoder feature map from the same level (cropped to size), two 3×3 convs.
- A final 1×1 conv maps 64 channels to the classes.

FCN *adds* score maps from a few layers; U-Net *concatenates* full feature maps at **every** level. The high-resolution detail bypasses the bottleneck instead of being reconstructed from it.

**Sizes.** Every unpadded 3×3 conv trims one pixel from each side:

$$572 \to 570 \to 568 \xrightarrow{\text{pool}} 284 \to 282 \to 280 \to 140 \to 138 \to 136 \to 68 \to 66 \to 64 \to 32 \to 30 \to 28$$
$$\xrightarrow{\text{up}} 56 \to 54 \to 52 \to 104 \to 102 \to 100 \to 200 \to 198 \to 196 \to 392 \to 390 \to 388$$

A 572×572 input tile gives a **388×388** output map: $(572 - 388)/2 = 92$ px lost on each side.

**Two ideas that are not the U (slides 13–14):**
- **Overlap-tile strategy.** Because the output is smaller than the input, a large image is segmented as tiles whose *outputs* abut and whose *inputs* overlap by $2 \times 92$ px. At the image border the missing context is filled by **mirroring** the image about its edge (zero padding would darken the border and bias predictions there). It's a memory strategy, not an accuracy one, and it is still how whole-slide pathology images are segmented.
- **Heavy augmentation, tiny data.** Trained on **30 annotated 512×512 images**. **Elastic deformation** (slide 16: a smooth random warp of a grid) is the key augmentation, because that is how real cells vary. Won the ISBI EM challenge: warping error 0.000353 vs 0.000420 for the previous best.

The lesson: U-Net was built for the regime students are actually in, a few dozen labelled images.

**The weight map (slide 15).** Cell images have touching cells separated only by a ~2 px gutter of background. Merge the gutter and 25 cells fuse into 9 blobs, yet in the slide's simulation pixel accuracy is still 97.9% and IoU 0.95: the metric barely notices. U-Net weights the loss per pixel:

$$E = \sum_{x \in \Omega} w(x)\,\log p_{\ell(x)}(x), \qquad w(x) = w_c(x) + w_0 \exp\!\left(-\frac{(d_1(x) + d_2(x))^2}{2\sigma^2}\right)$$

- $w_c$ balances class frequencies (in the slide: 1.20 for cell, 0.86 for background).
- $d_1$, $d_2$: distances to the nearest and second-nearest cell border. Both are small only in a gap between two cells, so the second term fires only there. $w_0 = 10$, $\sigma = 5$ px.
- The separation term is about 9.2 at $d_1 + d_2 = 2$, 1.4 at 10 and 0.003 at 20. In the slide's simulation, $w \approx 1.2$ inside a cell and up to about 8.4 on the gap pixels.

(The lecture writes $E$ without a minus sign, as the paper does; the training loss is $-E$.)

### 4. DeepLab: atrous convolution and ASPP (slides 17–18)

**Atrous (dilated) convolution.** Insert $r - 1$ gaps between kernel elements. A 3×3 kernel at rate $r$ still has 9 weights but covers

$$k_{eff} = k + (k - 1)(r - 1) = 2r + 1 \text{ (for } k = 3)$$

so rates 1, 2, 4 give 3×3, 5×5, 9×9. Dilation buys receptive field **without stride**, so resolution is kept. Stacking 6 layers (slide 18): plain 3×3 reaches $1 + 2 \cdot 6 = 13$ px; doubling the rate (1, 2, 4, …, 32) reaches $1 + 2(1 + 2 + \dots + 32) = 127$ px, with the same parameters.

**DeepLabv3+ (slide 17):**
- **Backbone** ResNet-101 with atrous conv in the last stage, so the output stride is **16, not 32**: $H/16 \times W/16 \times 2048$.
- **ASPP** (Atrous Spatial Pyramid Pooling): five parallel branches on the same map, each 256 channels: 1×1 conv; 3×3 at rates 6, 12, 18 (effective 13×13, 25×25, 37×37); and image pooling (global average → 1×1 → upsample). Concatenate ($5 \times 256 = 1280$), fuse with 1×1 to 256. **ASPP reads several scales from one map.**
- **Decoder:** upsample ×4 (bilinear), concatenate low-level features from stride 4 reduced to **48 channels** by a 1×1 conv (so they don't outweigh the 256-channel encoder output; $256 + 48 = 304$), two 3×3 convs, 1×1 to class scores, upsample ×4. Two ×4 steps instead of one ×16 jump.

### 5. Losses: cross-entropy is not enough (slides 19–20)

$\Omega$ is the set of pixels, $\ell(x)$ the true label at $x$, $p_k(x)$ the softmax probability of class $k$.

| Loss | Formula | What it's for |
|---|---|---|
| Cross-entropy | $L_{CE} = -\frac{1}{\lvert\Omega\rvert}\sum_x \log p_{\ell(x)}(x)$ | the default |
| Weighted CE | $L_{wCE} = -\frac{1}{\lvert\Omega\rvert}\sum_x w_{\ell(x)} \log p_{\ell(x)}(x)$ | rare classes, boundaries (U-Net) |
| Focal | $L_{focal} = -\frac{1}{\lvert\Omega\rvert}\sum_x \alpha_t (1 - p_t(x))^\gamma \log p_t(x)$, $\gamma = 2$ | many easy background pixels ([[08 - Object Detection II\|ch. 08]]) |
| Dice | $L_{Dice} = 1 - \frac{2\sum_x p(x) g(x) + \varepsilon}{\sum_x p(x) + \sum_x g(x) + \varepsilon}$ | optimises region overlap directly |
| Combined | $L = \lambda L_{CE} + (1 - \lambda) L_{Dice}$, typically $\lambda = \frac12$ | default in medical imaging |

$g(x) \in \{0, 1\}$ is the ground truth and $p(x)$ the predicted probability, so this is a **soft** Dice (differentiable). For $K$ classes, average the per-class Dice: $L_{Dice} = 1 - \frac1K\sum_k \text{Dice}_k$. $\varepsilon$ avoids division by zero on empty masks.

**Gradient analysis (slide 20):**
- **Object size.** CE is a per-pixel average, so an object occupying 0.01% of the image gets 0.01% of the gradient. Across object sizes from 0.01% to 30% of the image the signal changes **3000×**. Focal loss is the same line here: it rescales pixels, not object size.
- **Soft Dice is scale-free**: it's a set-overlap score, so object size cancels and the gradient is flat across four decades. But near-zero overlap gives almost no gradient, so it **starts badly**. (A constant 0.2% background leak also erodes Dice's flatness for small objects.)
- **Confidence.** For one foreground pixel becoming easy, CE keeps "asking". Focal at $\gamma = 2$ delivers $1/35$ of the CE gradient at $p = 0.9$ and $1/3345$ at $p = 0.99$. That is the imbalance fix, and all it does.
- **Dice + CE**: Dice holds the floor for small objects; CE supplies a well-conditioned gradient early in training. It's nnU-Net's default.

### 6. Measuring a mask (slides 22–25)

**Pixel accuracy lies (slide 22).** A street scene with one small car. Car: TP 3709, FP 2222, FN 3711 pixels.
- Pixel accuracy 0.97: dominated by background.
- Car IoU $= 3709 / (3709 + 2222 + 3711) = 0.38$.
- mIoU over 2 classes $= (0.97 + 0.38)/2 = 0.68$.

A model that predicts "background" everywhere would also score high pixel accuracy. mIoU weights every class equally, which is why it drops and why benchmarks report it.

**IoU and Dice carry the same information (slide 23).** For predicted set $P$ and true set $G$:

$$\text{IoU} = \frac{\lvert P \cap G\rvert}{\lvert P \cup G\rvert}, \qquad \text{Dice} = \frac{2\lvert P \cap G\rvert}{\lvert P\rvert + \lvert G\rvert} = \frac{2\,\text{IoU}}{1 + \text{IoU}}$$

(Use $\lvert P\rvert + \lvert G\rvert = \lvert P \cup G\rvert + \lvert P \cap G\rvert$.) Dice is a monotone function of IoU, so no model can be better under one and worse under the other. In counts: IoU $= \frac{TP}{TP + FP + FN}$, Dice $= \frac{2TP}{2TP + FP + FN}$ (Dice is the F1 score).
- Why both? Convention: vision reports IoU and **mIoU** (averaged over classes); medical imaging reports Dice.
- Dice reads higher: IoU 0.5 is Dice 0.67. Compare numbers only within one convention.
- **The trap in mIoU:** it averages over **classes**, not pixels. A class that appears in three test images carries the same weight as the sky.

**Panoptic Quality (Kirillov et al., 2019) (slide 24).** A predicted segment **matches** a ground-truth segment if it has the same class and IoU > 0.5. Above 0.5 the match is unique (two segments can't both overlap one ground truth by more than half), so no assignment algorithm is needed. Unmatched predictions are FP; unmatched ground truths are FN.

$$\text{PQ} = \frac{\sum_{(p,g) \in TP} \text{IoU}(p, g)}{\lvert TP\rvert + \frac12\lvert FP\rvert + \frac12\lvert FN\rvert} = \underbrace{\frac{\sum_{TP} \text{IoU}}{\lvert TP\rvert}}_{\text{SQ (segmentation quality)}} \times \underbrace{\frac{\lvert TP\rvert}{\lvert TP\rvert + \frac12\lvert FP\rvert + \frac12\lvert FN\rvert}}_{\text{RQ (recognition quality)}}$$

SQ is the mean IoU of matched segments (how well you draw); RQ is an F1 score over segments (how well you find and name). PQ is computed per class and averaged.

Slide example: sky 0.95, road 0.96, trees 0.90, car #1 0.56 (all TP); an invented car #2 (FP); no FN. SQ $= 3.37/4 = 0.84$, RQ $= 4/4.5 = 0.89$, **PQ = 0.75**. PQ counts segments, not pixels: the small car weighs as much as the sky, and inventing car #2 costs RQ.

**What PQ told us (slide 25), 2019:**

| Dataset | Human PQ | Machine PQ | Gap |
|---|---|---|---|
| Cityscapes | 69.6 | 61.2 | 8.4 |
| ADE20k | 67.6 | 35.6 | 32.0 |
| Vistas | 57.5 | 38.3 | 19.2 |

The gap sits almost entirely in **RQ, not SQ**: machines draw boundaries nearly as well as people, but fail at deciding what a segment is and what to call it. Humans score far from 100 because panoptic annotation is genuinely ambiguous.

### 7. Instance segmentation: Mask R-CNN (He et al., 2017) (slides 27–30)

**Architecture (slide 27).** Faster R-CNN + FPN ([[07 - Object Detection I|ch. 07]]) plus a third head:
- Stage 1: ResNet-101 + FPN (P2–P5, 256 channels, strides 4/8/16/32) → RPN → about 1000 RoIs after NMS.
- Stage 2, per RoI, via **RoIAlign**:
  - box head: 7×7×256 → FC 1024 → FC 1024 → class ($K + 1$ softmax) and box ($4K$ coordinates);
  - **mask head** (in parallel): 14×14×256 → 4 × (3×3 conv, 256) → 2×2 deconv stride 2 → 28×28×256 → 1×1 conv → **$K \times 28 \times 28$**, one binary mask per class.
- Take the mask channel of the predicted class $k$, resize it to the box, paste it into the image. Three cars give three instances of one class, not one "car" region.

**RoIAlign: the half-pixel that mattered (slide 28).** RoIPool ([[07 - Object Detection I|ch. 07]]) rounds twice: the RoI's corners to the feature grid, then the bin boundaries. In the slide the RoI's corners fall at feature coordinates 1.37 and 6.41; RoIPool snaps them to 1 and 6. At stride 32 half a cell is 16 image pixels, and here the shifts are $0.37 \times 32 = 11.8$ and $0.41 \times 32 = 13.1$ px. RoIAlign does no rounding: it samples each bin at **4 points with bilinear interpolation** and averages (or max-pools) them.

Measured by He et al.: **+3 AP** with a stride-16 backbone, **+7.3 AP** at stride 32, and **+10.5 AP₇₅**. A misalignment invisible to a box metric is fatal to a mask.

**Two design decisions worth copying (slide 29):**
- **Decouple mask from class.** Predict $K$ independent binary masks with a **per-pixel sigmoid** and let the box branch choose which to use, rather than a softmax over classes at every pixel. **30.3 AP vs 24.8 AP**: softmax makes classes compete for pixels when they shouldn't.
- **Keep the mask small.** 28×28, upsampled to the box. A full-resolution mask head would dominate compute for little gain. Mask R-CNN runs at about **5 fps**, about the same as Faster R-CNN, for about 20% more compute.

COCO mask AP: ResNet-101-FPN **35.7**, ResNeXt-101-FPN **37.1**.

**What it did not solve (slide 30):**
- **Boxes first, masks second.** Miss the box and the mask is gone; a long, thin or bent object that no box frames well is segmented badly by construction.
- **Three tasks, three architectures.** Semantic used an FCN, instance a detector with a mask head, panoptic a hand-written merge of the two with its own rules for overlapping pixels. Is that necessary?

### 8. Mask classification: one architecture (slides 32–35)

**The reframing (slide 32):**
- **Per-pixel classification:** feature map → 1×1 conv to $K$ → $H \times W \times K$ softmax. One $K$-way decision per pixel; instance needs a different design.
- **Mask classification:** feature map + $N$ queries → transformer decoder → $N$ pairs of (class $c_i$, binary mask $m_i$), some predicting $\varnothing$ (no object). Read the outputs differently for each task:
  - semantic: merge masks by class;
  - instance: keep the "thing" masks and score them;
  - panoptic: resolve overlaps by score.

**MaskFormer / Mask2Former (Cheng et al., 2021–22) are DETR with the box replaced by a mask** ([[08 - Object Detection II|ch. 08]] §5):
- $N$ learned queries, each producing one (class, mask) pair;
- Hungarian matching between predictions and ground-truth segments;
- unmatched queries learn "no object";
- no NMS: the loss already forbids duplicates.

Architecture (slide 33): backbone → **pixel decoder** (upsamples to per-pixel embeddings, and gives multi-scale features to the transformer decoder) → transformer decoder ($L$ layers) on the queries. Each query's mask is its embedding's **dot product** with the per-pixel embeddings.

**Masked attention** is Mask2Former's addition: each query's cross-attention is restricted to the region its current mask predicts, so it converges on one object instead of averaging over the whole image.

| Mask2Former | Score |
|---|---|
| COCO panoptic | 57.8 PQ |
| COCO instance | 50.1 AP |
| ADE20K semantic | 57.7 mIoU |

One architecture, one loss, three tasks, and it beats the specialised model on each.

**The shape of the argument (slide 35).** Per-pixel classification treats segmentation as $H \times W$ independent decisions. Mask classification treats it as a **set of regions, each with a label**, which is what a person means by "segment". Once the output is a set of masks, semantic vs instance vs panoptic is only post-processing; the network never knew which task it was doing.

### 9. Promptable segmentation: SAM (slides 37–42)

**SAM (Kirillov et al., 2023): change the task instead.** **Promptable segmentation**: given a point, a box or a rough mask, return a valid mask, even when the prompt is ambiguous. Train on that, and the model transfers to tasks it never saw.

**Architecture (slide 37):**
- **Image encoder:** a heavy ViT-H ([[06 - Vision Transformers|ch. 06]]), runs **once per image**, giving a 64×64×256 embedding (1024 px / patch 16 = 64).
- **Prompt encoder:** points $(x, y, \text{fg/bg})$, boxes, (text); a mask prompt is downsampled and added to the image embedding.
- **Lightweight mask decoder** (two transformer layers): about **50 ms per prompt**.
- **Ambiguity:** one click on a car could mean the whole car, a part (window) or a subpart. SAM outputs **three masks with predicted IoU scores** (e.g. 0.95, 0.88, 0.79) rather than averaging them into mush.

**What makes SAM work (slide 38):**
- **The data engine.** **SA-1B: over 1 billion masks on 11 million images** (about 100 per image), built by alternating annotators and the model, with the model doing more of the work each round. The engine is as much a contribution as the architecture.
- **The asymmetry.** Heavy encoder once per image, tiny decoder per prompt in milliseconds. That's what makes interactive annotation possible: a deployment idea, not a modelling one.

**Later versions:**
- **SAM 2 (2024): video** (slide 40). Image encoder → **memory attention** over a **memory bank** of previous frames → mask decoder; a memory encoder writes each new frame's result back. Prompt once and the mask follows the object: promptable **tracking** ([[11 - Video and Motion|ch. 11]]).
- **SAM 3 (2026): concepts** (slide 41). **Promptable concept segmentation**: the prompt is a noun phrase ("a penguin") or an image exemplar, and the model segments **every** instance of it, in images and video. A detector finds new instances per frame; a tracker propagates masks from frame $T-1$; the two are merged.

**What SAM is not (slide 42):**
- **SAM 1 and 2 don't name things.** A mask is a region; deciding it's a tumour, a defect or a traffic light is still your job, usually a classifier on the crop.
- **Domain shift is real.** SA-1B is natural images. On microscopy, radiology, SAR or electron microscopy, zero-shot SAM is often **worse than a small U-Net trained on thirty of your own images**.
- **Where it reliably pays: annotation.** Click instead of trace, correct instead of draw. A 10× labelling speed-up is worth more to a student project than two points of mIoU.

### 10. For your project (slide 44)

| Situation | Reach for |
|---|---|
| Medical or scientific imaging, tens of labels | U-Net, heavy augmentation, Dice + CE |
| Natural images, a public benchmark | Mask2Former, or a strong pretrained backbone |
| You need instances and a box is fine | Mask R-CNN, still an excellent baseline |
| Every pixel must be labelled once | panoptic, and report PQ with SQ and RQ |
| Labelling is the bottleneck | SAM-assisted annotation, then train your own model |

- **Report per-class IoU, not just mIoU.** A mean hides the one class your application depends on, and in medical work that class is usually the smallest.
- **Check the boundary separately.** Region metrics are dominated by interiors. If the boundary matters, measure it: boundary IoU or Hausdorff distance.

**Reading (slide 46):** FCN (CVPR 2015); U-Net (MICCAI 2015, the weight-map section); DeepLabv3+ (ECCV 2018); Mask R-CNN (ICCV 2017, §3 on RoIAlign); Panoptic Segmentation (CVPR 2019); Mask2Former (CVPR 2022); Segment Anything (ICCV 2023), SAM 3 (ICLR 2026). Code: `segmentation_models_pytorch` (a U-Net with any backbone in four lines); Mask2Former's `criterion.py` is the Lecture 8 matcher with masks instead of boxes.

**Hands-on (slide 47), `lecture09_handson.ipynb`:** IoU, Dice and mIoU from scratch (verify Dice = 2IoU/(1+IoU)); PQ and its SQ/RQ split; the IoU ceiling at strides 4–32; the four upsampling operators and the checkerboard artefact; dilated receptive fields, predicted then measured with a gradient; U-Net's weight map on touching cells; RoIAlign vs RoIPool misalignment in pixels; a small U-Net on thirty images with CE, Dice and Dice+CE.

## ✏️ Exercises

> [!example]- Exercise 1 — The resolution ceiling
> A 128×128 image contains a 40×40 square object covering pixels 12–51 in both directions. A "perfect" segmentation head labels each output cell, and the mask is upsampled by copying each cell's label into its $s \times s$ block.
> **(a)** At stride 32, what fraction of each cell does the object cover? What mask does a majority vote (label a cell "object" if > 50% covered) produce, and what IoU?
> **(b)** What is the best IoU any choice of stride-32 cells can achieve?
> **(c)** Repeat (a) at stride 16.
> **(d)** Name two architectural answers from the lecture to this problem.
>
> ---
> **(a)** The object straddles the corner shared by cells $[0,32)$ and $[32,64)$ in each direction. Each of the four cells contains $20 \times 20 = 400$ object pixels out of 1024: **39%**. Majority vote labels all four "background": the object **vanishes**, IoU **0**.
>
> **(b)** Taking all four cells: intersection 1600, union 4096, IoU $= 0.39$. One cell: $400/(1024 + 1600 - 400) = 0.18$; two cells: $800/2848 = 0.28$. Best **0.39**.
>
> **(c)** Along each axis the object covers 4 px of cell $[0,16)$, all of $[16,32)$ and $[32,48)$, and 4 px of $[48,64)$. Only the 2×2 interior cells are > 50% covered, giving a 32×32 mask fully inside the object: IoU $= 1024/1600 = $ **0.64**.
>
> **(d)** Skip connections that bring back high-resolution features (FCN-8s, U-Net, DeepLabv3+'s stride-4 decoder branch) and atrous convolution, which keeps the receptive field growing without increasing the stride (DeepLab's output stride 16 instead of 32).

> [!example]- Exercise 2 — Upsampling
> **(a)** A transposed convolution has $k = 3$, $s = 2$, $p = 1$, output padding 1, and a 4×4 input. What is the output size?
> **(b)** Count how many kernel copies land on each output pixel along one axis. Why does this produce a checkerboard? What happens with $k = 4$, $s = 2$, $p = 1$?
> **(c)** Bilinear ×2 with `align_corners=True` turns the row $[1, 2, 3, 2]$ into 8 values. Compute the 2nd and 6th outputs.
> **(d)** Which of the four upsampling methods has learnable parameters, and which needs information saved from the encoder?
>
> ---
> **(a)** $(4 - 1) \cdot 2 - 2 \cdot 1 + 3 + 1 = $ **8**, so 8×8.
>
> **(b)** Copies start every 2 pixels and are 3 wide, so counts alternate **1, 2, 1, 2, 1, 2, 1, 1** (the last after cropping and output padding). In 2D the counts multiply, giving 1, 2 and 4 in a regular grid: some pixels receive four contributions and their neighbours one, which shows up as a checkerboard even with a constant input. With $k = 4$, $s = 2$ the interior counts are all **2** (edges 1): even overlap, no checkerboard.
>
> **(c)** Output $i$ maps to input position $3i/7$. $i = 1$: $3/7 = 0.43$, between 1 and 2 → **1.43**. $i = 5$: $15/7 = 2.14$, between 3 and 2 → $3 - 0.14 = $ **2.86**.
>
> **(d)** Only the **transposed convolution** is learned. **Max unpooling** needs the max-pool indices recorded in the encoder.

> [!example]- Exercise 3 — Receptive field and tiles
> **(a)** Give the effective kernel size and number of weights of a 3×3 conv at rates 1, 6, 12, 18.
> **(b)** Three stacked 3×3 convs (stride 1). Receptive field with rates 1, 1, 1? With rates 1, 2, 4?
> **(c)** Why does DeepLabv3+ use atrous conv in the backbone's last stage instead of keeping stride 32 and upsampling more?
> **(d)** A U-Net with the original sizes (572 in, 388 out) must segment a 1000×1000 slide. How many tiles, how large is each input tile, and where does the context for the outermost tiles come from?
>
> ---
> **(a)** $k_{eff} = 2r + 1$: **3, 13, 25, 37**. Always **9 weights** (plus bias).
>
> **(b)** Each layer adds $(k_{eff} - 1)$: rates 1,1,1 give $1 + 2 + 2 + 2 = $ **7**; rates 1,2,4 give $1 + 2 + 4 + 8 = $ **15**, with the same parameters.
>
> **(c)** Stride throws away position, and the IoU ceiling falls with stride (0.67 at 16 vs 0.39 at 32 on the lecture's car). Dilation keeps the receptive field growing without downsampling, so the feature map stays at stride 16 and the ASPP branches can still look at large context (up to 37×37 cells at rate 18).
>
> **(d)** Output tiles of 388 px must cover 1000 px: $\lceil 1000/388 \rceil = 3$ per side, so **9 tiles**. Each input tile is **572×572**: its 388×388 output plus 92 px of context on each side; neighbouring input tiles overlap by $2 \times 92$ px while their outputs abut. Around the edge of the slide the 92 px of context doesn't exist, so it is **mirrored** from the image.

> [!example]- Exercise 4 — Metrics and losses
> A 100×100 image contains a 400-pixel lesion. A model predicts 400 lesion pixels: 300 correct (TP), 100 wrong (FP), and misses 100 (FN).
> **(a)** Compute pixel accuracy, lesion IoU, lesion Dice and 2-class mIoU. Check Dice against $2\,\text{IoU}/(1 + \text{IoU})$.
> **(b)** A lazy model predicts "background" everywhere. Compute its pixel accuracy and mIoU. Which metric exposes it?
> **(c)** With CE averaged over pixels, how does the lesion's share of the loss signal change if the lesion shrank from 30% of the image to 0.01%? Which loss removes this dependence, and why is it not used alone?
> **(d)** Panoptic scene. Ground truth: sky, road, car A, car B, person. Predictions: sky (IoU 0.90), road (0.95), car A (0.70), a car overlapping car B with IoU 0.40, person (0.60), and a "tree" with no ground truth. Compute SQ, RQ and PQ.
>
> ---
> **(a)** TN $= 10{,}000 - 300 - 100 - 100 = 9{,}500$. Pixel accuracy $= 9{,}800/10{,}000 = $ **0.98**. IoU $= 300/500 = $ **0.60**. Dice $= 600/800 = $ **0.75**, and $2(0.6)/1.6 = 0.75$ ✓. Background IoU $= 9{,}500/9{,}700 = 0.979$, so mIoU $= (0.60 + 0.979)/2 = $ **0.79**.
>
> **(b)** Accuracy $= 9{,}600/10{,}000 = $ **0.96**, barely below the real model's 0.98. Lesion IoU 0, background IoU 0.96, mIoU **0.48**. **mIoU** (or the per-class IoU) exposes it; pixel accuracy doesn't.
>
> **(c)** The share scales with the lesion's pixel fraction: $30/0.01 = $ **3000× less** signal. **Soft Dice** is scale-free (an overlap ratio, so size cancels), but at near-zero overlap early in training its gradient is tiny, so it starts badly. Hence **Dice + CE** ($\lambda = \frac12$).
>
> **(d)** Car B's prediction has IoU 0.40 < 0.5: it's an **FP**, and car B is an **FN**. The tree is another FP. TP = 4 (sky, road, car A, person), FP = 2, FN = 1. SQ $= (0.90 + 0.95 + 0.70 + 0.60)/4 = $ **0.79**; RQ $= 4/(4 + 1 + 0.5) = $ **0.73**; PQ $= 3.15/5.5 = $ **0.57**.

> [!example]- Exercise 5 — Diagnose and choose
> **(a)** A box is predicted at stride 32 with corners at image x = 43.8 and 205.1 px. RoIPool rounds them to the feature grid. How far off (in image pixels) are the corners? What would the error be at stride 16? Why does this matter for masks but hardly for boxes?
> **(b)** A teammate replaces Mask R-CNN's per-class sigmoid masks with a softmax over classes at each pixel. What happens and why?
> **(c)** A team must segment cell nuclei in 40 labelled microscopy images. One member wants zero-shot SAM. What's the risk, and how should SAM be used instead?
> **(d)** The same Mask2Former weights are used for semantic, instance and panoptic output. What differs between the three?
>
> ---
> **(a)** Feature coordinates $43.8/32 = 1.37$ and $205.1/32 = 6.41$, rounded to 1 and 6: errors $0.37 \times 32 = $ **11.8 px** and $0.41 \times 32 = $ **13.1 px**. At stride 16: $2.74 \to 3$ and $12.82 \to 13$, errors $0.26 \times 16 = 4.2$ px and $0.18 \times 16 = 2.9$ px. Mask pixels must line up with object pixels; a 12 px shift moves the whole mask edge, while a box at IoU 0.5 tolerates it. That's why RoIAlign gave +7.3 AP at stride 32 but +3 at stride 16.
>
> **(b)** Mask AP drops (24.8 vs 30.3 in the paper). Softmax makes classes compete for every pixel inside the box, coupling the mask to the classification problem. With per-class sigmoids, the mask head only decides "object vs not" for each class, and the box branch picks the class.
>
> **(c)** SA-1B is natural images; on microscopy zero-shot SAM is often worse than a small U-Net trained on ~30 own images, and it returns unlabelled regions. Better: use SAM to **speed up annotation** (click and correct), then train a U-Net with heavy (elastic) augmentation and Dice + CE, and use U-Net's weight map so touching nuclei stay separate.
>
> **(d)** Only the post-processing of the $N$ (class, mask) outputs: semantic merges masks by class; instance keeps the thing masks with their scores; panoptic resolves overlaps by score so each pixel gets one segment. The network and loss are identical.

## 📝 Summary

- **Semantic** labels pixels; **instance** separates countable objects; **panoptic** does both (things get ids, stuff gets classes). Stride caps quality: a perfect stride-32 head reaches only IoU 0.39 on a car-sized object.
- **FCN:** FC layers as convolutions → dense score maps; skips from pool4 and pool3 recover boundaries (FCN-8s, 62.2 mean IU on VOC 2012). Upsampling: nearest, bilinear, max unpooling, or learned **transposed conv** (beware the checkerboard when $k$ isn't a multiple of $s$).
- **U-Net:** symmetric encoder–decoder with concatenated skips at every level; unpadded convs (572 → 388), overlap-tile with mirrored borders, elastic augmentation, a boundary weight map; built for ~30 images.
- **DeepLab:** atrous conv ($k_{eff} = 2r + 1$) grows the receptive field without stride; ASPP (rates 6, 12, 18 + image pooling) reads several scales; output stride 16.
- **Losses:** CE's signal scales with object size (3000× across the range); soft Dice is scale-free but starts badly; Dice + CE is the medical default; focal fixes easy-pixel imbalance only.
- **Metrics:** pixel accuracy lies; Dice $= 2\,\text{IoU}/(1 + \text{IoU})$; mIoU averages classes; **PQ = SQ × RQ** separates drawing from naming, and the human–machine gap is in RQ.
- **Mask R-CNN:** Faster R-CNN + a 28×28 per-class sigmoid mask head + **RoIAlign** (+7.3 AP at stride 32 by removing two roundings). **Mask2Former:** DETR with masks, Hungarian-matched, no NMS, masked attention; one model for all three tasks.
- **SAM:** heavy ViT encoder once per image, light decoder per prompt, three masks for ambiguity, SA-1B (1B masks, 11M images). No labels, weak under domain shift; its real value is faster annotation.

## ⚠️ Important Notes

1. **Semantic segmentation does not separate instances.** Two touching dogs are one "dog" region.
2. **Pixel accuracy is dominated by the largest class.** An all-background model can score 0.96+. Report mIoU and per-class IoU.
3. **mIoU averages over classes, not pixels.** A rare class weighs as much as the sky.
4. **IoU and Dice rank models identically**; Dice is always ≥ IoU (IoU 0.5 = Dice 0.67). Don't compare a Dice from one paper with an IoU from another.
5. **PQ match threshold is IoU > 0.5**, which makes matching unique. A prediction at IoU 0.4 counts as an FP *and* leaves the ground truth as an FN.
6. **PQ = SQ × RQ** only because SQ is averaged over TPs and RQ is an F1 over segments; SQ alone ignores missed and invented segments.
7. **FCN fuses by addition; U-Net by concatenation.**
8. **U-Net's output is smaller than its input** (unpadded convs): 572 → 388. Tiles overlap in input, abut in output; borders are mirrored, not zero-padded.
9. **Transposed conv is learned upsampling, not the inverse of convolution.** Its output size is $(n-1)s - 2p + k + \text{output padding}$.
10. **Dilation adds receptive field, not parameters**: a 3×3 at rate $r$ has 9 weights and covers $(2r+1)^2$.
11. **Soft Dice has tiny gradients at near-zero overlap**; pair it with CE.
12. **Focal loss down-weights easy pixels but doesn't fix object-size scaling.**
13. **RoIPool's error grows with stride**: a 0.4-cell rounding is ~13 px at stride 32. RoIAlign uses bilinear sampling, no rounding.
14. **Mask R-CNN masks are per-class sigmoids**, not a per-pixel softmax, and are only 28×28.
15. **SAM masks have no class labels**, and zero-shot SAM can lose to a small U-Net outside natural images.

> [!warning] Gaps in the source material
> - **Read from rendered slide images** (the text layer has only titles): the stride/IoU figure (6), FCN diagrams (8–10), the upsampling panel (11), U-Net (12), overlap-tile (14), weight map (15), DeepLabv3+ (17), dilation chart (18), gradient analysis (20), pixel-accuracy and PQ examples (22, 24), Mask R-CNN and RoIAlign (27–28), mask classification and Mask2Former (32–33), SAM, SAM 2 and SAM 3 diagrams (37, 40, 41). Numbers taken from them were recomputed where possible (bilinear and transposed-conv grids, U-Net sizes, ASPP sizes, focal ratios 1/35 and 1/3345, PQ example).
> - **Slide 22's caption** says "the background is over 99% of all pixels", but its own counts (car TP 3709, FP 2222, FN 3711 with pixel accuracy 0.97) imply the car is about 3.7% of the image (background ≈ 96%). The lesson is unaffected. Listed in the errata.
> - **Slide 15's weight map:** the peak of 8.4 is from the lecturer's simulation; the slide doesn't say how $d_1$, $d_2$ are measured on a 2 px gutter, so the formula values above (9.2 at $d_1 + d_2 = 2$) don't reproduce it exactly.
> - **Added beyond the slides:** the semantic/instance/panoptic table (the slide is a picture); FCN's 384-px example; the transposed-conv output-size formula and overlap counts; the IoU/Dice identity's derivation and count form; why PQ's 0.5 threshold makes matches unique; how Mask2Former turns a query into a mask (dot product with per-pixel embeddings); SA-1B's ~100 masks per image; all exercises and Important Notes.
> - **Not covered by this lecture:** boundary IoU and Hausdorff distance are only named.

**Previous:** [[08 - Object Detection II]] · **Next:** [[10 - Pose Estimation and Faces]]
