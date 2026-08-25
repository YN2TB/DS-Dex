---
subject: Computer Vision
chapter: 9
tags: [ds, computer-vision, segmentation, fcn, unet, transposed-convolution, miou, dice, mask-rcnn, sam]
source: "Long et al. 2015 (FCN); Ronneberger et al. 2015 (U-Net); He et al. 2017 (Mask R-CNN); Kirillov et al. 2023 (SAM); Szeliski, *Computer Vision*, 2nd ed. §6.4; the lecturer's course outline"
---

# Segmentation

**Week 9 of 14 — and the week of the mid-term. ⚠️ NO SLIDES** — see [[00-Index]].

> [!note] ⚠️ A **depth** chapter — [[Deep Learning/contents/00-Index|Deep Learning]] explicitly deferred segmentation
> [[Deep Learning/contents/06 - Object Detection|DL ch. 06]]'s gaps callout records that D2L §14.9–14.11 (semantic segmentation, transposed convolution, fully convolutional networks) were **outside that subject's syllabus and left for here**, noting that *"transposed convolution is the one that would most repay adding."* **This chapter is where the vault picks it up.**

**Four results.**

**§3 — ⚠️ THE CHECKERBOARD ARTIFACT IS ARITHMETIC: TRANSPOSED-CONVOLUTION OVERLAP IS UNIFORM IFF $s$ DIVIDES $k$.** Verified across eight $(k,s)$ pairs. **$k=3,s=2$ gives interior overlap counts $\{1,2\}$ — a 2× difference between adjacent output pixels**; $k=4,s=2$ and $k=6,s=3$ are uniform.

**§4 — ⚠️ PIXEL ACCURACY 80.0% AND mIoU 37.7% ON THE SAME PREDICTIONS — A FACTOR OF 2.12.** A model that gets the three largest classes right and calls everything else "road" **scores 80% pixel accuracy while the three classes that matter score zero IoU.**

**§5 — ⚠️ DICE $=2\,\mathrm{IoU}/(1+\mathrm{IoU})$ EXACTLY, AND THE INFLATION PEAKS AT $\mathrm{IoU}=\sqrt2-1$.** Verified to $10^{-12}$. **The maximum gap is 0.1716 at IoU $\approx0.4142$** — so Dice and IoU rank models identically and **are not comparable as numbers.**

**§1 — ⚠️ A STRIDE-32 BACKBONE PREDICTS 49 VALUES FOR 50,176 PIXELS.** **1,024 pixels reconstructed per predicted value.** Upsampling cannot invent information — **which is exactly why skip connections exist.**

## 📘 Main Knowledge

### 1. ⚠️ Three tasks, and the resolution problem common to all of them

| task | question | output |
|---|---|---|
| **semantic** | what class is each pixel? | one label per pixel; **two cats are one "cat" region** |
| **instance** | which object is each pixel part of? | a mask per object; **background usually ignored** |
| **panoptic** | both | every pixel gets a class **and** an instance id |

**Semantic segmentation is "classification at every pixel"**, and that phrasing immediately exposes the difficulty:

| stage | stride | map | **pixels per cell** |
|---|---|---|---|
| input | 1 | $224^2$ | 1 |
| C3 | 4 | $56^2$ | 16 |
| C4 | 8 | $28^2$ | 64 |
| C5 | 16 | $14^2$ | 256 |
| **C6** | **32** | **$7^2$** | **1,024** |

> [!warning] ⚠️ A STRIDE-32 BACKBONE HAS **49 CELLS FOR 50,176 PIXELS**
> **Each cell must be expanded back to $32\times32=1{,}024$ pixels.**
>
> ⇒ ***classification discards spatial detail on purpose — every stride-2 layer is a deliberate 4× reduction — and segmentation needs it back.***
>
> **And upsampling cannot invent information.** 49 values per channel cannot become 50,176 informative ones; interpolation only *redistributes*. **That is the entire argument for skip connections**: the high-resolution features were never destroyed, only bypassed — so re-inject them rather than trying to reconstruct them.
>
> *This is [[05 - CNN Architectures|ch. 05]] §3's activation-volume trend read backwards: the network halves its volume at every stage, and segmentation has to undo that.*

### 2. FCN — the architectural move

**Long et al. (2015)**: take a classification network and **replace the fully connected head with $1\times1$ convolutions.**

> [!note] ⚠️ An fc layer on a flattened map **is** a convolution over the whole map
> A $7\times7\times512\to4096$ fully connected layer is exactly a $7\times7$ convolution with 4096 output channels. **Rewriting it as such removes the fixed input size** — the network now accepts any resolution and emits a *map* of class scores rather than a vector.
>
> ⇒ *this is the same identity [[06 - Vision Transformers|ch. 06]] §1 used in reverse (ViT's patch embedding is a strided convolution), and the same one [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §11 used for NiN.* **"Fully convolutional" is a statement about what the head is, not about the body.**

**FCN then upsamples, and adds skip connections from earlier, higher-resolution layers** — FCN-32s (no skips), FCN-16s, FCN-8s, each sharper than the last. **The improvement comes entirely from the skips**, which is §1's argument made concrete.

### 3. ⚠️ Transposed convolution — and why the checkerboard appears

**Transposed convolution ("deconvolution", a misnomer) upsamples by placing a copy of the kernel at every input position, spaced $s$ apart, and summing overlaps.** Output size:

$$H_{\text{out}}=(H_{\text{in}}-1)s-2p+k$$

| in | $k$ | $s$ | $p$ | out |
|---|---|---|---|---|
| 7 | 2 | 2 | 0 | 14 |
| 7 | 4 | 2 | 1 | 14 |
| 7 | 3 | 2 | 1 | 13 |
| 7 | 4 | 4 | 0 | 28 |

> [!warning] ⚠️ THE ARTIFACT: COUNT HOW MANY TIMES EACH OUTPUT PIXEL IS WRITTEN
> | $k$ | $s$ | $k/s$ | interior overlap counts | |
> |---|---|---|---|---|
> | 2 | 2 | 1.00 | $\{1\}$ | **uniform** |
> | **3** | **2** | 1.50 | $\mathbf{\{1,2\}}$ | ⚠️ **uneven** |
> | 4 | 2 | 2.00 | $\{2\}$ | **uniform** |
> | 5 | 2 | 2.50 | $\{2,3\}$ | ⚠️ uneven |
> | 3 | 3 | 1.00 | $\{1\}$ | uniform |
> | **5** | **3** | 1.67 | $\mathbf{\{1,2\}}$ | ⚠️ uneven |
> | 6 | 3 | 2.00 | $\{2\}$ | uniform |
>
> $$\boxed{\text{the overlap is uniform iff } s \text{ divides } k}$$
>
> **With $k=3,s=2$, adjacent output pixels receive 1 and 2 contributions — a 2× difference baked into the geometry, before any weights are learned.** ⇒ ***that is exactly the checkerboard pattern seen in GAN and segmentation outputs***, and it is a property of the arithmetic, not of training.
>
> **Two standard fixes:**
> 1. **choose $k$ divisible by $s$** — $4/2$ is the common pair
> 2. **upsample (bilinear or nearest) then apply a normal convolution** — no overlap at all, and what most modern code does
>
> *(Odena et al. 2016 is the reference; the arithmetic above is the whole mechanism.)*

### 4. ⚠️ U-Net — skips as the architecture, not an addition

**Ronneberger et al. (2015)**: a symmetric encoder–decoder where **every decoder stage concatenates the matching encoder features.** Originally for biomedical images, where data is scarce and boundaries matter.

| level | resolution | channels | **values carried** |
|---|---|---|---|
| enc1 | $572^2$ | 64 | **20,939,776** |
| enc2 | $286^2$ | 128 | 10,469,888 |
| enc3 | $143^2$ | 256 | 5,234,944 |
| enc4 | $71^2$ | 512 | 2,580,992 |
| **total across skips** | | | **39,225,600** |

> [!note] ⚠️ **39.2 million values bypass the bottleneck entirely**
> **Without skips the decoder must reconstruct every boundary from the bottleneck alone**; with them it receives the original high-resolution features.
>
> ⇒ ***the same insight as ResNet's identity path** ([[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §14): **do not force a network to re-derive something it already has.*** *ResNet adds; U-Net concatenates — and [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §16 showed concatenation is exactly DenseNet's choice, with the same quadratic channel-growth consequence.*
>
> **And it is why U-Net dominates medical imaging**: with few training images, an architecture that *reuses* rather than *relearns* is worth more than depth.

### 5. ⚠️ Evaluation — and two ways to be misled

**Intersection over Union per class, averaged over classes:**
$$\mathrm{IoU}_c=\frac{|P_c\cap G_c|}{|P_c\cup G_c|},\qquad \mathrm{mIoU}=\frac1C\sum_c\mathrm{IoU}_c$$

**Consider a road scene**: road 35%, building 25%, sky 20%, vegetation 12%, car 5%, person 2%, sign 1%. **A model that gets the top three right and labels everything else "road":**

| metric | value |
|---|---|
| **pixel accuracy** | **80.0%** |
| road's IoU (it absorbed 20% of the image wrongly) | 0.6364 |
| car / person / sign IoU | **0.0000** |
| **mIoU** | **37.7%** |

> [!warning] ⚠️ 80.0% AGAINST 37.7% — A FACTOR OF 2.12 ON IDENTICAL PREDICTIONS
> **The three classes a driving system actually needs — car, person, sign — score exactly zero, and pixel accuracy still reads 80%.**
>
> ⇒ ***mIoU averages over CLASSES, so a class occupying 1% of pixels counts as much as one occupying 35%.*** **That is precisely why it is the standard metric and pixel accuracy is not.**
>
> *This is [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8's class-imbalance finding in a new setting — and [[03 - Image Classification and Linear Models|ch. 03]]'s note that accuracy on an imbalanced set is meaningless, made quantitative.*

**Dice coefficient** (common in medical imaging): $\mathrm{Dice}=\dfrac{2|A\cap B|}{|A|+|B|}$.

> [!warning] ⚠️ DICE AND IoU ARE THE SAME INFORMATION, AND DICE IS ALWAYS LARGER
> Since $|A\cup B|=|A|+|B|-|A\cap B|$:
> $$\boxed{\mathrm{Dice}=\frac{2\,\mathrm{IoU}}{1+\mathrm{IoU}}}$$
> **Verified to $10^{-12}$ on six random mask pairs.**
>
> | IoU | Dice | **gap** |
> |---|---|---|
> | 0.10 | 0.1818 | 0.0818 |
> | 0.25 | 0.4000 | 0.1500 |
> | **0.4142** | **0.5858** | **0.1716** ← maximum |
> | 0.50 | 0.6667 | 0.1667 |
> | 0.90 | 0.9474 | 0.0474 |
>
> **The gap is maximized at $\mathrm{IoU}=\sqrt2-1\approx0.4142$**, where $\frac{d}{d\,\mathrm{IoU}}\left[\frac{2I}{1+I}-I\right]=\frac{2}{(1+I)^2}-1=0$.
>
> ⇒ ***Dice and IoU rank models identically but are not comparable as numbers*** — **reporting Dice instead of IoU inflates the figure by up to 0.172, and by the most exactly in the mid-range where most real results sit.** **Always say which one.**

### 6. Instance and panoptic segmentation

**Mask R-CNN** (He et al. 2017) = Faster R-CNN **+ a small FCN mask branch per RoI**, predicting a $28\times28$ binary mask for the detected class.

> [!warning] ⚠️ Its real contribution is **RoI align**, and the reason is §3's argument
> **RoI pooling rounds** region coordinates to the feature grid ([[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §9 reproduced both its printed outputs). **For a box, a half-cell error is tolerable; for a pixel mask it is not** — at stride 16, half a cell is 8 pixels.
>
> **RoI align uses bilinear interpolation instead of rounding**, and that single change is what made instance masks work. ⇒ *the same lesson as §3: **quantization that is invisible in a box is fatal in a mask.***

**Panoptic segmentation** (Kirillov et al. 2019) unifies the two: **"things" (countable objects) get instances, "stuff" (road, sky) gets semantic labels only**, and every pixel receives exactly one answer — which removes the ambiguity of overlapping instance masks.

**SAM** (Segment Anything, Kirillov et al. 2023) is a **promptable** model: given a point, box or mask, it segments *whatever object is there*, without class labels. **Trained on ~1 billion masks**, it is a foundation model for segmentation — *class-agnostic by design, which makes it a component rather than a solution.*

## ✏️ Exercises

> [!example]- Exercise 1 — the resolution problem
> **(a)** For a $224^2$ input, give the map size and pixels-per-cell at strides 8, 16, 32. **(b)** How many values does a stride-32 map hold per channel, against the target? **(c)** Can upsampling recover the difference? **(d)** What follows architecturally?
>
> ---
> **(a)** $28^2$ / 64; $14^2$ / 256; $\mathbf{7^2}$ / $\mathbf{1{,}024}$.
>
> **(b)** **49 values per channel against 50,176 target pixels** — a ratio of 1,024:1.
>
> **(c)** ⚠️ **No.** Interpolation redistributes existing values; it cannot create information that was discarded by striding. **A stride-32 prediction upsampled to full resolution is a $7\times7$ decision smeared over the image.**
>
> **(d)** ⇒ **Skip connections.** The high-resolution features still exist in the early layers — they were bypassed, not destroyed. **FCN-8s beats FCN-32s for exactly this reason, and U-Net makes the skips the architecture rather than an addition.**

> [!example]- Exercise 2 — the checkerboard
> **(a)** Output size for $k=4,s=2,p=1$ on a $7^2$ input. **(b)** Count interior overlaps for $(k,s)=(3,2)$, $(4,2)$, $(5,3)$, $(6,3)$. **(c)** State the rule. **(d)** Two fixes.
>
> ---
> **(a)** $(7-1)\cdot2-2\cdot1+4=\mathbf{14}$ — a clean 2× upsample.
>
> **(b)** $(3,2)\to\{1,2\}$ ⚠️; $(4,2)\to\{2\}$ ✓; $(5,3)\to\{1,2\}$ ⚠️; $(6,3)\to\{2\}$ ✓.
>
> **(c)** ⚠️ **Uniform iff $s$ divides $k$.** When it does not, adjacent output pixels receive different numbers of kernel contributions — **a 2× difference for $(3,2)$** — producing a periodic intensity pattern **before any weights are learned.**
>
> **(d)** **(i)** Choose $k$ divisible by $s$ (4/2 is standard). **(ii)** **Upsample then convolve** — bilinear or nearest-neighbour followed by a normal convolution — which has no overlap structure at all and is what most modern implementations do.

> [!example]- Exercise 3 — pixel accuracy versus mIoU
> Classes by pixel share: road 35%, building 25%, sky 20%, vegetation 12%, car 5%, person 2%, sign 1%. A model predicts the top three correctly and labels the rest "road".
> **(a)** Pixel accuracy. **(b)** Road's IoU. **(c)** mIoU. **(d)** Why is mIoU standard?
>
> ---
> **(a)** $35+25+20=\mathbf{80.0\%}$.
>
> **(b)** Intersection 0.35; union $0.35+0.12+0.05+0.02+0.01=0.55$; **IoU $=0.6364$.** *Absorbing other classes damages road's own score — a false positive is counted.*
>
> **(c)** $(0.6364+1+1+0+0+0+0)/7=\mathbf{37.7\%}$.
>
> **(d)** ⚠️ **80.0% vs 37.7% — a factor of 2.12 on identical predictions**, and **the three classes a driving system actually needs score exactly zero.** **mIoU averages over classes**, so a 1%-of-pixels class weighs as much as a 35% one. *Pixel accuracy measures how much of the image is easy; mIoU measures whether the model can do the job.*

> [!example]- Exercise 4 — Dice and IoU
> **(a)** Derive Dice in terms of IoU. **(b)** Which is larger? **(c)** Where is the gap largest? **(d)** Do they rank models the same way?
>
> ---
> **(a)** $|A\cup B|=|A|+|B|-|A\cap B|$, so with $I=|A\cap B|$: $\mathrm{IoU}=\frac{I}{|A|+|B|-I}$ and $\mathrm{Dice}=\frac{2I}{|A|+|B|}$. Eliminating gives $\boxed{\mathrm{Dice}=\frac{2\,\mathrm{IoU}}{1+\mathrm{IoU}}}$ — **verified to $10^{-12}$.**
>
> **(b)** **Dice**, always, for $0<\mathrm{IoU}<1$: $\frac{2I}{1+I}>I\iff2>1+I\iff I<1$.
>
> **(c)** Maximize $\frac{2I}{1+I}-I$: derivative $\frac{2}{(1+I)^2}-1=0\Rightarrow(1+I)^2=2\Rightarrow \mathbf{I=\sqrt2-1\approx0.4142}$, **gap $=0.1716$.** ⚠️ *The inflation is largest exactly in the mid-range where most real results sit.*
>
> **(d)** ⚠️ **Yes — the map is strictly increasing, so they rank identically.** **But they are not comparable as numbers**: a "0.59 Dice" and a "0.41 IoU" are the *same result*. **Always state which metric.**

## 📝 Summary

- **Semantic / instance / panoptic answer three different questions**; semantic is "classification at every pixel", which exposes the difficulty immediately.
- **⚠️ A stride-32 backbone predicts 49 values per channel for 50,176 pixels — 1,024 pixels per predicted value.** **Upsampling redistributes, it cannot invent** ⇒ **skip connections re-inject high-resolution features that were bypassed, not destroyed.**
- **FCN replaces the fully connected head with $1\times1$ convolutions** — and an fc layer on a flattened map *is* a convolution over the whole map, so this removes the fixed input size. **The improvement from FCN-32s to FCN-8s comes entirely from the skips.**
- **⚠️ Transposed convolution's overlap is uniform iff $s$ divides $k$.** $k=3,s=2$ gives interior counts $\{1,2\}$ — **a 2× difference baked into the geometry before any weights are learned**, which *is* the checkerboard artifact. **Fix by $k$ divisible by $s$, or upsample-then-convolve.**
- **U-Net makes skips the architecture: 39,225,600 values bypass the bottleneck.** Same insight as ResNet's identity path — **do not force a network to re-derive what it already has** — and it is why U-Net dominates data-scarce medical imaging.
- **⚠️ Pixel accuracy 80.0% vs mIoU 37.7% — a factor of 2.12** on the same predictions, with **car, person and sign at exactly zero.** **mIoU averages over classes**, so rare classes count equally.
- **⚠️ $\mathrm{Dice}=2\,\mathrm{IoU}/(1+\mathrm{IoU})$ exactly, with the gap maximized at $\mathrm{IoU}=\sqrt2-1\approx0.4142$ (0.1716).** They rank models identically and **are not comparable as numbers.**
- **Mask R-CNN = Faster R-CNN + a per-RoI FCN mask branch, and its real contribution is RoI align** — bilinear interpolation instead of rounding, because **a half-cell error is tolerable in a box and fatal in a mask** (8 pixels at stride 16). **Panoptic** unifies things and stuff; **SAM** is promptable and class-agnostic.

## ⚠️ Important Notes

1. **⚠️ Never report pixel accuracy for segmentation.** It measures how much of the image is easy. **Report mIoU, and report per-class IoU for the classes that matter** — an 80%-accurate model can score zero on every class you care about.
2. **⚠️ Always say whether a number is IoU or Dice.** Dice is larger by up to 0.172, most in the mid-range. **A "0.59 Dice" and a "0.41 IoU" are the same model.**
3. **⚠️ Check $k$ against $s$ in any transposed convolution.** If $s\nmid k$ you have built a checkerboard generator. **Prefer upsample-then-convolve** unless you have a reason not to.
4. **⚠️ Output stride is the single most important segmentation hyperparameter.** Stride 32 means 1,024 pixels per prediction. **Dilated/atrous convolutions keep the receptive field while reducing stride** — the standard alternative to more skips.
5. **⚠️ RoI align vs RoI pooling matters only for masks — and there it is decisive.** Rounding costs up to half a feature cell, which is 8 input pixels at stride 16. **If instance masks are systematically offset, check which one you are using.**
6. **⚠️ Class imbalance in segmentation is worse than in classification.** Background can be 90% of pixels, so a cross-entropy loss over pixels has the same defect [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §8 found in detection. **Dice loss, focal loss and class weighting all exist for this**; a plain pixel cross-entropy will predict background.
7. **⚠️ Boundaries are where the error concentrates and where mIoU is least sensitive.** A mask can be 95% correct by area and visibly wrong at every edge. **Look at the predictions, not only the metric** — boundary-F1 exists for this reason.
8. **SAM is class-agnostic by design.** It segments *something* wherever prompted and names nothing. **It is a component, not a solution** — pair it with a classifier if you need labels.

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). Built from **FCN (Long et al. 2015)**, **U-Net (Ronneberger et al. 2015)**, **Mask R-CNN (He et al. 2017)**, **panoptic segmentation (Kirillov et al. 2019)**, **SAM (Kirillov et al. 2023)**, **Szeliski §6.4**, and CS231n.
>
> **⚠️ This chapter picks up material [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] explicitly deferred.** Its gaps callout records that D2L §14.9–14.11 were out of that subject's scope and that *"transposed convolution is the one that would most repay adding"* — **§3 is that addition.**
>
> **⚠️ Week 9 is also the mid-term week** ([[00-Index]]: 40%, *"inference-style questions: given a model, an architecture, or an output, reason about what happens and why"*). **Whether week 9 teaches segmentation as well as examining, or is lighter for that reason, is unknown.**
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§1's resolution table** and the 1,024-pixels-per-value framing, with the argument that **upsampling cannot invent information** and that this is *why* skips exist.
> - **§3's overlap-count experiment across eight $(k,s)$ pairs and the rule "uniform iff $s$ divides $k$".** *Odena et al. (2016) identified the checkerboard artifact; **counting the interior overlaps to show it is pure geometry, independent of the weights, is mine.***
> - **§4's U-Net skip-value count** (39,225,600) and the connection to ResNet's identity path and DenseNet's concatenation.
> - **§5's road-scene worked example** — pixel accuracy 80.0% against mIoU 37.7%, **a factor of 2.12, with the three critical classes at zero.** *The general point that mIoU is preferred is standard; **the constructed case and the factor are mine.***
> - **§5's exact derivation $\mathrm{Dice}=2\,\mathrm{IoU}/(1+\mathrm{IoU})$, its numerical verification, and the finding that the gap is maximized at exactly $\mathrm{IoU}=\sqrt2-1$ with value 0.1716.** *The identity is known; **the maximizer and the "not comparable as numbers" conclusion are mine.***
> - **§6's framing that RoI align matters because quantization invisible in a box is fatal in a mask**, quantified at 8 pixels for stride 16.
> - **All eight Important Notes.**
>
> ⚠️ **§5's class distribution is a constructed example**, chosen to be representative of a driving scene, **not measured from Cityscapes or any real dataset** — the *mechanism* and the factor of 2.12 are the finding, not a claim about a specific benchmark. **U-Net's $572^2$ input and channel counts are from the original paper.**
>
> **No discrepancies found.**
>
> **Deliberately deferred, not omitted:** **DeepLab's atrous/dilated convolutions and CRF post-processing** are named in Important Note 4 and not developed — *they would be the most defensible addition if the course covers DeepLab explicitly.* **Video and 3D segmentation** belong to [[11 - Video and Motion|ch. 11]] and [[14 - 3D Vision and Emerging Topics|ch. 14]]. **Mask R-CNN's detection half** is [[07 - Object Detection I|ch. 07]] and [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §9. **Szeliski §6.4.1 (medical image segmentation) and §6.4.4 (intelligent photo editing)** are applications, summarized only where they carry an argument. **§6.4.5 (pose estimation)** is [[10 - Pose Estimation and Faces|ch. 10]].
>
> **Left as the source states it:** SAM's ~1 billion training masks; the FCN-32s/16s/8s accuracy ordering; U-Net's biomedical provenance and its architecture constants; and Mask R-CNN's $28\times28$ mask resolution.

**Previous:** [[08 - Object Detection II]] · **Next:** [[10 - Pose Estimation and Faces]]
