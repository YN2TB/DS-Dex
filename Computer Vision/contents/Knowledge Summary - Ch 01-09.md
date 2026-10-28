---
subject: Computer Vision
chapter: summary
tags: [ds, computer-vision, revision, summary]
source: "Condensed from notes 01–09 (Lectures 1–9, Nguyen Manh Toan, Swinburne Vietnam). Every number is from those notes and was rechecked in Python."
---

# Knowledge Summary: Lectures 1–9

The whole course so far on a few pages. Each section gives the core ideas, the formulas to know, and the traps. For derivations and exercises, open the chapter. To test yourself, use [[Revision Test - Ch 01-09]].

## 🧭 The course in one thread

Every lecture answers one question left open by the one before.

| Week | Question | Answer |
|---|---|---|
| 01 | What is an image? | A tensor of numbers from projection + sampling + quantisation. Meaning isn't in the numbers (the **semantic gap**). |
| 02 | How do we get structure from pixels by hand? | Filters (convolution), edges, morphology, features (Harris, SIFT, HOG). Every parameter is hand-picked. |
| 03 | How do we let data choose the parameters? | Score function + loss + optimiser. Linear classifier, softmax, SGD. One template per class is too weak. |
| 04 | How do we learn the features too? | Hidden layers with nonlinearities, backprop. Convolution = locality + weight sharing. |
| 05 | How do we train deep CNNs reliably? | He init, BatchNorm, Adam, augmentation, **residual connections**, transfer learning. |
| 06 | Do we need convolution at all? | ViT: attention over patches. Needs data or a good recipe (DeiT); Swin restores the pyramid. |
| 07 | What if there are many objects? | Detection = a set of boxes. IoU, AP, NMS. Two-stage: R-CNN → Fast → Faster R-CNN, FPN. |
| 08 | Can detection be one pass, without anchors or NMS? | YOLO, SSD, focal loss (RetinaNet), FCOS, CenterNet, DETR. |
| 09 | What if we label every pixel? | FCN, U-Net, DeepLab; Dice/IoU/PQ; Mask R-CNN, Mask2Former, SAM. |

---

## 01 · Image formation · [[01 - Introduction and Image Formation|note]]

- **Vision is an inverse problem**: the camera maps 3D → 2D, and vision tries to go back. Projection is many-to-one, so **depth is lost**.
- **Eight challenges** that change pixels but not meaning: viewpoint, illumination, scale, deformation, occlusion, clutter, intra-class variation, context. A model must be invariant to all of them.
- **Pinhole:** $x = fX/Z$, $y = fY/Z$. Ten times smaller and ten times closer gives the same image. Small hole = sharp but dark; large hole = bright but blurry.
- **Lens:** $\dfrac{1}{z_o} + \dfrac{1}{z_i} = \dfrac{1}{f}$. Only one distance is in perfect focus; a smaller aperture gives deeper depth of field but less light. Real lenses add radial distortion, chromatic aberration, vignetting.
- **Sensor:** sampling (resolution) and quantisation (8 bits = 0–255). Colour from a Bayer filter + demosaicing: two of three colour values per pixel are interpolated.
- **Grayscale:** $Y = 0.299R + 0.587G + 0.114B$ (weights sum to 1). Different colours can map to nearly the same gray; use **HSV** to select by colour. YCbCr for compression, Lab for perceptual distance.
- **Tensors:** $H\times W$, $H\times W\times 3$, video $T\times H\times W\times 3$. PyTorch batches are $(N, C, H, W)$.

**Traps:** `cv2.imread` returns **BGR** $(H, W, C)$ `uint8`; use `permute`, never `reshape`/`view`, to change axis order; match the pretrained model's normalisation; quantisation can't be undone.

## 02 · Classical image processing · [[02 - Classical Image Processing|note]]

- **Point operations** (brightness, contrast, gamma, threshold) use no neighbours. **Histogram equalisation** maps each value through the CDF: $J = \lfloor 255\, c(I) \rfloor$. **CLAHE** does it per tile with clipping.
- **Convolution** = correlation with a flipped kernel. Linear + shift-invariant ⇒ convolution. CNN layers compute correlation.
- **Output size** (used for every CNN layer): $H_{out} = \left\lfloor \dfrac{H + 2p - f}{s} \right\rfloor + 1$. "Same" padding $p = (f-1)/2$ needs odd $f$.
- **Noise → filter:** Gaussian noise → Gaussian filter; salt & pepper → **median** (nonlinear); keep edges → **bilateral** (not a convolution). The box filter rings and isn't isotropic.
- **Gaussian facts:** separable ($k^2 \to 2k$ multiplications); blurring twice adds **variances** ($\sigma = 3$ then $4$ gives $5$); derivative theorem: smoothing then differentiating = one convolution with $\partial G/\partial x$.
- **Edges:** derivatives amplify noise, so smooth first. **Sobel** $S_x$ = $[1,2,1]^\top[-1,0,1]$ detects **vertical** edges. Gradient magnitude $\sqrt{I_x^2 + I_y^2}$, direction perpendicular to the edge. Laplacian → zero crossings; LoG ≈ DoG.
- **Canny:** smooth → gradient → non-maximum suppression along $\theta$ → **hysteresis** (keep weak pixels only if connected to strong ones).
- **Morphology:** dilation grows, erosion shrinks. **Opening** (erode → dilate) removes specks; **closing** (dilate → erode) fills holes. Both idempotent. Max-pooling = grayscale dilation.
- **Harris:** structure tensor $M = \sum w \begin{bmatrix} I_x^2 & I_xI_y \\ I_xI_y & I_y^2 \end{bmatrix}$, $R = \det M - k(\operatorname{tr} M)^2$, $k \in [0.04, 0.06]$. $R \gg 0$ corner, $R < 0$ edge. Rotation-invariant, **not scale-invariant**.
- **SIFT:** DoG extrema over 26 neighbours (scale) → refine → dominant orientation (rotation) → 4×4 cells × 8 bins = **128-D**. Match with **Lowe's ratio test** $d_1/d_2 < 0.8$, then RANSAC.
- **HOG:** 8×8 cells, 9 unsigned bins, overlapping 2×2 blocks L2-normalised; 64×128 window → **3,780-D**. HOG + linear SVM + sliding window + NMS = the pre-2012 detector.

**Traps:** smoothing kernels sum to 1, derivative kernels to 0; $\sigma$ is the real parameter, not kernel size; gradient magnitude scales with brightness (hence normalised descriptors); local methods can't tell a shadow edge from an object edge.

## 03 · Classification and linear models · [[03 - Image Classification and Linear Models|note]]

- **Data-driven pipeline:** score function + loss + optimiser. Train / validation / test; touch the test set **once**. Cross-validation gives error bars at $k$ times the cost.
- **Accuracy misleads under imbalance**; read the confusion matrix. ImageNet uses top-5.
- **k-NN:** $O(1)$ train, $O(N)$ predict. Pixel distance isn't semantic distance, and in high dimensions all distances look alike (**curse of dimensionality**). Useless on raw pixels, standard on learned embeddings.
- **Linear classifier** $s = Wx + b$; CIFAR-10 has 30,730 parameters. Three views: matrix multiply, **one template per class**, hyperplanes. Can't do XOR, rings, or multimodal classes.
- **Losses** (score $s$, true class $y$):

| Setting | Output | Loss |
|---|---|---|
| Multiclass SVM | scores | $\sum_{j\ne y} \max(0,\ s_j - s_y + \Delta)$, $\Delta = 1$ |
| Binary | $p = \sigma(s)$ | BCE $-[y\log p + (1-y)\log(1-p)]$ |
| Multiclass, one true | softmax $p_k = e^{s_k}/\sum_j e^{s_j}$ | CE $-\log p_y$ |
| Multi-label | one sigmoid per class | sum of BCEs; threshold, no argmax |

- **Softmax gradient:** $\partial L/\partial s_k = p_k - \mathbb 1[k = y]$, so $\nabla_W L = \frac1N(P - Y)^\top X + 2\lambda W$. Subtract $\max_j s_j$ before exponentiating.
- **Hinge vs CE:** hinge reaches zero and stops; CE never reaches zero and keeps pushing.
- **Regularisation:** $W$ isn't unique (scaling keeps margins), so add $\lambda R(W)$. **L2** = small, spread-out weights; **L1** = exact zeros (diamond corners). Tune $\lambda$ on validation, on a log scale. L2 ≈ Gaussian prior, L1 ≈ Laplace prior (MAP).
- **Optimisation:** $W \leftarrow W - \eta \nabla_W L$. Mini-batch "SGD" (32–256): unbiased, variance $\propto 1/|B|$. Epoch = $N/|B|$ iterations. Learning rate and batch size are tuned together.
- **Sanity checks:** initial loss $\approx \ln C$ (2.30 for 10 classes) for softmax, $\approx C - 1$ for hinge; gradient check; overfit ~20 examples.

**Traps:** `nn.CrossEntropyLoss` takes raw logits; loss ≠ accuracy; normalisation statistics from the training set only; LR too high → `nan`, slightly high → plateau.

## 04 · Neural networks to CNNs · [[04 - From Neural Networks to CNNs|note]]

- **Neural network:** $s = W_2\,\sigma(W_1 x)$. Without the nonlinearity, any stack of linear layers is one linear layer.
- **Universal approximation** says one hidden layer *can* represent anything; it says nothing about size, trainability or generalisation. Depth wins by reusing features.
- **Activations:**

| | Derivative | Problem |
|---|---|---|
| Sigmoid | $\sigma' \le 1/4$ | saturates, not zero-centred; up to $4^{-n}$ shrinkage over $n$ layers |
| tanh | $\le 1$ | zero-centred, still saturates |
| **ReLU** | 1 for $x > 0$ | cheap; units can "die" |
| Leaky ReLU / ELU / GELU | | fixes for dead units; GELU in transformers |

- **Backprop** = local chain rule: downstream = upstream × local. **Add** distributes, **multiply** swaps, **max** routes. Gradients **add** where a value is reused (hence `zero_grad()`).
- **Matrix form:** $\partial L/\partial W = (\partial L/\partial Z)^\top X$, $\partial L/\partial X = (\partial L/\partial Z)W$; ReLU masks by $\mathbb 1[Z > 0]$. Gradient shape = parameter shape.
- **Conv layer** = locality + weight sharing. Parameters $C_{out}C_{in}k^2 + C_{out}$, **independent of image size**. Each filter spans all input channels.
- **Receptive field:** stacked 3×3 convs grow it linearly (three 3×3 = one 7×7, fewer parameters); stride and pooling multiply the growth. Dilation gives effective size $d(k-1) + 1$.
- **Pooling:** no parameters, local translation invariance only. **1×1 conv** mixes channels. First-layer filters learn Gabor-like edge detectors.

**Traps:** most CNN parameters often sit in the final FC layer; the max gate sends zero gradient to the losers; dead ReLUs don't recover.

## 05 · CNN architectures and training · [[05 - CNN Architectures|note]]

- **Initialisation:** keep activation variance constant. $\operatorname{Var}(z) = n_{in}\operatorname{Var}(w)\operatorname{Var}(x)$. Xavier $2/(n_{in}+n_{out})$ for tanh; **He $2/n_{in}$ for ReLU**. All-zero init never breaks symmetry.
- **BatchNorm:** normalise each channel over the batch, then $\gamma\hat x + \beta$. Training uses batch statistics, test uses running averages: call `model.eval()`. Small batches → GroupNorm; transformers → LayerNorm; style transfer → InstanceNorm.
- **Optimisers:**

| | Update | Note |
|---|---|---|
| Momentum | $v \leftarrow \mu v - \eta\nabla L$, $W \leftarrow W + v$ | effective step $\eta/(1-\mu)$ = 10× at $\mu = 0.9$ |
| RMSProp | divide by $\sqrt{s}$, $s$ = running mean of $(\nabla L)^2$ | per-parameter rate |
| **Adam** | momentum + RMSProp + bias correction $\hat m = m/(1-\beta_1^t)$ | $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\eta = 10^{-3}$ |

- **Schedules:** step, cosine, exponential, warm-up.
- **Augmentation** (crop, flip, colour jitter, erasing, MixUp/CutMix) is the strongest regulariser in vision, **if it preserves the label**. Others: weight decay, dropout, early stopping, label smoothing.
- **Architectures:**

| Model | Key idea |
|---|---|
| LeNet | conv → pool pattern |
| AlexNet | ReLU, dropout, GPUs; 60M params |
| VGG | only 3×3 convs; 138M, mostly in the first FC layer |
| GoogLeNet | Inception module, 1×1 bottlenecks; 5M |
| **ResNet** | $y = F(x) + x$; gradient $\partial F/\partial x + 1$ keeps an identity path; fixes **degradation** |
| DenseNet / ResNeXt / SENet / MobileNet | concatenation / grouped conv / channel attention / depthwise-separable conv |

- **Degradation** (deeper plain net has *higher training* error) is an optimisation problem, not overfitting and not vanishing gradients.
- **Transfer learning:** feature extraction (freeze, train head) for little, similar data; fine-tuning with a 10–100× smaller LR otherwise. Default baseline: pretrained ResNet-50.

**Traps:** He for ReLU, Xavier for tanh; frozen weights ≠ frozen BN statistics; ResNet skip needs a 1×1 stride-2 conv when shapes change.

## 06 · Vision transformers · [[06 - Vision Transformers|note]]

- **Attention** = soft dictionary lookup: $\text{softmax}\!\left(QK^\top/\sqrt{d_k}\right)V$. Weights depend on content and are recomputed per input. $\sqrt{d_k}$ keeps the logits at unit variance so softmax doesn't saturate.
- **Self-attention:** $Q, K, V = XW_Q, XW_K, XW_V$. $3D^2$ parameters, independent of the number of tokens $n$; cost **quadratic in $n$**. **Multi-head:** $h$ heads of size $D/h$, same parameters as one head.
- **Permutation-equivariant**, so position must be added (learned position embeddings).
- **ViT:** $P\times P$ patches (a conv with kernel = stride = $P$) + [class] token + position embeddings + $L$ **pre-norm** blocks: $z' = \text{MSA}(\text{LN}(z)) + z$, $z'' = \text{MLP}(\text{LN}(z')) + z'$, MLP $D \to 4D \to D$ with GELU. 224/16 → 196 tokens. $12D^2$ per block, two-thirds in the MLP. ViT-B 86M, L 307M, H 632M.
- **Inductive bias vs data:** CNNs are told locality, translation equivariance and the grid; ViT has to learn them. CNN wins on small data, ViT wins at ~300M images.
- **DeiT:** same ViT-B, better recipe (strong augmentation, stochastic depth, label smoothing, AdamW + cosine, warm-up) → 81.8% on ImageNet-1k alone. **Distillation:** $L = (1-\lambda)\text{CE} + \lambda T^2\,\text{KL}(p_t^T\|p_s^T)$; a **distillation token**; a CNN teacher works best (it passes on the convolutional bias).
- **Swin:** attention inside $M\times M$ windows ($M = 7$), cost **linear** in patches; **shifted windows** let information cross; patch merging builds a 4×–32× pyramid; relative position bias ($(2M-1)^2 = 169$ values).
- **What to use:** fine-tune a pretrained model; from scratch on small data, a CNN; for dense prediction, Swin / ConvNeXt / ResNet backbones.

**Traps:** scale by $\sqrt{d_k}$ of one head ($\sqrt{64} = 8$ for ViT-B); attention weights aren't parameters; halving patch size → 4× tokens → 16× attention cost; interpolate position embeddings at a new resolution; attention maps aren't explanations.

## 07 · Object detection I · [[07 - Object Detection I|note]]

- **Output** = a set $\{(b_k, c_k, s_k)\}$ of unknown size. Every detector proposes a dense candidate set, classifies and refines each, then prunes. The hard part is **search**, not classification.
- **Classical:** Viola–Jones (integral image + cascade), HOG + SVM, DPM.
- **Scoring:**
  - $\text{IoU} = |A\cap B|/|A\cup B|$.
  - Greedy matching by score; **a duplicate is a false positive**.
  - $\text{AP} = \int_0^1 p_{interp}(r)\,dr$ with $p_{interp}(r) = \max_{r'\ge r} p(r')$. AP measures ranking. mAP averages over classes.
  - **VOC:** IoU 0.5. **COCO:** average over IoU 0.50–0.95, so localisation counts. Report AP₅₀, AP₇₅, AP_S.
- **NMS:** keep the best box, delete overlaps above $\tau$, repeat; per class; 0.7 for proposals, 0.5 for detections. Fails in crowds.
- **Box targets:** $t = \left(\dfrac{x - x_a}{w_a}, \dfrac{y - y_a}{h_a}, \log\dfrac{w}{w_a}, \log\dfrac{h}{h_a}\right)$; decode $x = x_a + t_x w_a$, $w = w_a e^{t_w}$.
- **The R-CNN family:**

| | Proposals | Features | Result |
|---|---|---|---|
| R-CNN | selective search, ~2,000 | CNN per warped crop + SVMs | 66.0 mAP, 47 s/image |
| Fast R-CNN | selective search | one backbone pass, **RoI pooling** 7×7, CE + smooth L1 | 70.0 mAP, 0.32 s network |
| Faster R-CNN | **RPN**, 9 anchors/location (3 scales × 3 ratios) | shared backbone | 73.2 mAP, 5 fps |

- **RPN labels:** IoU > 0.7 positive, < 0.3 negative, in between ignored; 256 anchors sampled. Background gets no box loss.
- **FPN:** top-down path + lateral connections, so every level is semantically strong; large gains on small objects. Now the standard neck.

**Traps:** "mAP" without a protocol means nothing; high AP₅₀ but low AP₇₅ = sloppy boxes; missed objects cap recall; Fast R-CNN's speed-up from 47 s → 0.32 s is ~147× (the paper's 213× uses truncated SVD).

## 08 · Object detection II · [[08 - Object Detection II|note]]

- **One-stage** detectors predict densely in one pass but face the full background imbalance the RPN used to filter.
- **YOLO:** $S\times S$ grid, $B$ boxes + one class distribution per cell ($7\times7\times30$ on VOC). Squared loss with $\lambda_{coord} = 5$, $\lambda_{noobj} = 0.5$, $\sqrt w, \sqrt h$. 45 FPS, 63.4 mAP. Fewer background errors, more localisation errors, weak on small grouped objects.
- **SSD:** default boxes on six feature maps; hard negative mining 3:1. SSD300: 74.3 mAP at 59 FPS.
- **Focal loss:** $\text{FL}(p_t) = -\alpha_t(1 - p_t)^\gamma \log p_t$, $\gamma = 2$, $\alpha = 0.25$. Keeps every anchor, down-weights easy ones (×0.01 at $p_t = 0.9$). Needs bias init $b = -\log\frac{1-\pi}{\pi} \approx -4.6$ for $\pi = 0.01$. **RetinaNet** = FPN + anchors + focal loss: 37.8 AP, beating two-stage detectors.
- **Anchor-free:** **FCOS** regresses $(l, t, r, b)$ from every pixel inside a box; overlaps go to the smaller box; **centre-ness** $\sqrt{\frac{\min(l,r)}{\max(l,r)}\cdot\frac{\min(t,b)}{\max(t,b)}}$ down-weights edge predictions. **CenterNet** finds Gaussian centre peaks with a 3×3 max-pool: no NMS.
- **DETR:** $N = 100$ object queries, transformer encoder–decoder, **Hungarian matching** (class + L1 + GIoU), so duplicates are impossible: no NMS, no anchors. Costs: ~500 epochs, poor small-object AP, at most $N$ objects. Deformable DETR: 46.9 AP in 50 epochs.
- $\text{GIoU} = \text{IoU} - |C\setminus(A\cup B)|/|C|$ gives a gradient even when boxes don't overlap.
- **Practice:** decide on your own validation data; check the licence (AGPL-3.0 for recent YOLOs).

**Traps:** $p_t$ is the probability of the *true* class (for background, $1 - p$); focal loss down-weights, hard negative mining removes; with $\gamma = 2$, $\alpha = 0.25$ actually favours background; focal loss doesn't fix small-object resolution.

## 09 · Segmentation · [[09 - Segmentation|note]]

- **Tasks:** **semantic** (class per pixel, no instances), **instance** (separate countable objects), **panoptic** (both: *things* get class + id, *stuff* gets class only).
- **Stride caps quality**: coarse score maps can't draw boundaries, so resolution has to be recovered.
- **FCN:** FC layers become convolutions → dense score maps; skips from pool4 and pool3 fused by **addition** (FCN-8s, 62.2 mean IU on VOC 2012).
- **Upsampling:** nearest, bilinear, max unpooling, **transposed conv** (learned; $n_{out} = (n_{in}-1)s - 2p + k$; checkerboard when $k$ isn't a multiple of $s$).
- **U-Net:** symmetric encoder–decoder, skips fused by **concatenation** at every level; unpadded convs (572 → 388), overlap-tile with mirrored borders, elastic augmentation, boundary weight map. Built for ~30 training images.
- **DeepLab:** **atrous** conv, a 3×3 at rate $r$ covers $(2r+1)^2$ with 9 weights; **ASPP** (rates 6, 12, 18 + image pooling); output stride 16.
- **Losses:** CE's signal scales with object size; **soft Dice** $1 - \frac{2\sum pg}{\sum p + \sum g}$ is scale-free but has tiny gradients at near-zero overlap; **Dice + CE** is the medical default; focal fixes easy-pixel imbalance only.
- **Metrics:** pixel accuracy is dominated by the largest class. $\text{Dice} = 2\,\text{IoU}/(1 + \text{IoU})$ (IoU 0.5 → Dice 0.67; same ranking). mIoU averages over classes.
- **Panoptic Quality:** match = same class and IoU > 0.5 (unique).
$$\text{PQ} = \frac{\sum_{TP}\text{IoU}}{|TP| + \frac12|FP| + \frac12|FN|} = \underbrace{\frac{\sum_{TP}\text{IoU}}{|TP|}}_{\text{SQ}} \times \underbrace{\frac{|TP|}{|TP| + \frac12|FP| + \frac12|FN|}}_{\text{RQ}}$$
- **Mask R-CNN:** Faster R-CNN + 28×28 **per-class sigmoid** mask head + **RoIAlign** (bilinear sampling, no rounding; RoIPool's rounding costs ~13 px at stride 32).
- **Mask2Former:** DETR with masks, Hungarian-matched, masked attention; one model for semantic, instance and panoptic.
- **SAM:** heavy ViT image encoder run once, light decoder per prompt (point, box), three masks for ambiguous prompts; trained on SA-1B (1B masks, 11M images). Masks have **no class labels**; weak under domain shift; most useful for faster annotation.

**Traps:** a PQ match at IoU 0.4 counts as an FP *and* an FN; U-Net output is smaller than input; transposed conv isn't the inverse of convolution; zero-shot SAM can lose to a small U-Net outside natural images.

---

## 📐 Formula sheet

| Formula | Where |
|---|---|
| $x = fX/Z$; $\ 1/z_o + 1/z_i = 1/f$ | 01 |
| $Y = 0.299R + 0.587G + 0.114B$ | 01 |
| $H_{out} = \lfloor (H + 2p - k)/s \rfloor + 1$ | 02, 04 |
| $G_{\sigma_1} * G_{\sigma_2} = G_{\sqrt{\sigma_1^2 + \sigma_2^2}}$ | 02 |
| $R = \det M - k(\operatorname{tr} M)^2$ | 02 |
| Ratio test $d_1/d_2 < 0.8$ | 02 |
| Hinge $\sum_{j\ne y}\max(0, s_j - s_y + 1)$; CE $-\log p_y$ | 03 |
| $\partial L/\partial s = p - y$; $\ \nabla_W L = \frac1N(P-Y)^\top X + 2\lambda W$ | 03 |
| Conv params $C_{out}C_{in}k^2 + C_{out}$ | 04 |
| He $\operatorname{Var}(w) = 2/n_{in}$; Xavier $2/(n_{in} + n_{out})$ | 05 |
| BN $\gamma\,(x - \mu_B)/\sqrt{\sigma_B^2 + \epsilon} + \beta$ | 05 |
| Adam $W \leftarrow W - \eta\,\hat m/(\sqrt{\hat s} + \epsilon)$ | 05 |
| ResNet $y = F(x) + x$ | 05 |
| $\text{softmax}(QK^\top/\sqrt{d_k})V$ | 06 |
| Swin cost $4hwC^2 + 2M^2hwC$ vs global $4hwC^2 + 2(hw)^2C$ | 06 |
| IoU, AP $= \int p_{interp}(r)\,dr$ | 07 |
| smooth L1: $0.5z^2$ if $\lvert z\rvert < 1$, else $\lvert z\rvert - 0.5$ | 07 |
| Focal $-\alpha_t(1-p_t)^\gamma\log p_t$ | 08 |
| GIoU $= \text{IoU} - \lvert C\setminus(A\cup B)\rvert/\lvert C\rvert$ | 08 |
| Dice $= 2\,\text{IoU}/(1 + \text{IoU})$; PQ = SQ × RQ | 09 |
| Atrous $k_{eff} = 2r + 1$ ($k = 3$) | 09 |

## 🔁 Ideas that recur

- **Convolution never leaves.** Week 2's filters become week 4's learned kernels; ViT's patch embedding is a convolution; max-pooling is grayscale dilation.
- **The HOG detector's skeleton survives.** Dense candidates → score each → NMS (02 → 07). DETR and CenterNet are the first to drop NMS.
- **Normalisation fights lighting and scale.** HOG block normalisation (02), input standardisation (03), BatchNorm/LayerNorm (05–06).
- **Imbalance is handled four ways:** RPN filtering + sampling (07), hard negative mining and $\lambda_{noobj}$ (08), focal loss (08), Dice loss (09).
- **Skip connections carry fine detail or gradients:** ResNet (add, 05), FPN (lateral add, 07), FCN (add, 09), U-Net (concatenate, 09).
- **Inductive bias trades against data:** linear templates (03) → CNNs (04–05) → ViT (06). Less built-in structure needs more data or a better recipe.
- **Set prediction with Hungarian matching** links DETR (08) and Mask2Former (09).
- **Scale is solved by pyramids:** image pyramid (02), SIFT scale space (02), FPN (07), SSD's six maps (08), Swin (06), ASPP (09).

## ⚠️ Top traps across the course

1. OpenCV images are BGR, $(H, W, C)$, `uint8`; PyTorch wants RGB $(N, C, H, W)$ float.
2. `CrossEntropyLoss` and `BCEWithLogitsLoss` take logits, not probabilities.
3. Initial softmax loss should be $\ln C$; if not, something is wrong.
4. No nonlinearity, no depth.
5. `model.eval()` before inference changes BatchNorm and Dropout.
6. Blurring twice adds variances; Sobel $S_x$ finds vertical edges.
7. Harris is not scale-invariant; SIFT is.
8. Pixel accuracy and plain accuracy lie under imbalance; use the confusion matrix, mIoU, per-class IoU.
9. A duplicate detection is a false positive; "mAP" needs a protocol (VOC vs COCO).
10. Attention cost is quadratic in tokens; parameters don't depend on the number of tokens or heads.
11. Augmentations must preserve the label.
12. Fine-tune with a much smaller learning rate and the pretrained normalisation.

**Previous:** [[00-Index]] · **Test yourself:** [[Revision Test - Ch 01-09]]
