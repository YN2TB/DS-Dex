---
subject: Computer Vision
chapter: revision
tags: [ds, computer-vision, revision, multiple-choice]
source: "Built from notes 01–09 (Lectures 1–9, Nguyen Manh Toan, Swinburne Vietnam). Every numeric answer was checked in Python."
---

# Revision Test: Lectures 1–9

34 multiple-choice questions in the exam's format: pick **one** option, then write 1–3 sentences under it explaining why. Like the mid-term, most questions give you a setup and ask what happens and why.

**How to use it**
- Answer on paper or under each question, then open the collapsed answer.
- Score 1 point for the right letter and 1 for an explanation that names the actual reason (the "Why" line in the answer). Maximum 68.
- Each answer links the note to revise if you missed it.

| Part | Questions | Notes |
|---|---|---|
| Foundations | 1–12 | [[01 - Introduction and Image Formation\|01]], [[02 - Classical Image Processing\|02]], [[03 - Image Classification and Linear Models\|03]], [[04 - From Neural Networks to CNNs\|04]] |
| Architectures | 13–18 | [[05 - CNN Architectures\|05]], [[06 - Vision Transformers\|06]] |
| Detection | 19–24 | [[07 - Object Detection I\|07]], [[08 - Object Detection II\|08]] |
| Segmentation | 25–34 | [[09 - Segmentation\|09]] |

---

## Part 1: Foundations

### Q1 · Ch. 01: Same image, different worlds

A camera with focal length $f = 1000$ px photographs a 1.5 m tall car 30 m away; it is 50 px tall in the image. Which of these would produce **exactly the same** image height?

- **A.** A 0.15 m toy car 3 m from the camera.
- **B.** A 0.15 m toy car 0.3 m from the camera.
- **C.** A 3 m truck 30 m from the camera.
- **D.** The same car moved to 15 m.

**Your answer:**
**Why:**

> [!success]- Answer: A
> **Why:** image height is $y = fY/Z$, so only the ratio $Y/Z$ matters. Car: $1000 \times 1.5/30 = 50$ px. Toy at 3 m: $1000 \times 0.15/3 = 50$ px. Ten times smaller and ten times closer gives the same image; one image can't tell them apart (depth is lost in projection).
> **Not B:** 500 px. **Not C or D:** both 100 px (double the size, or half the distance).
> Revise: [[01 - Introduction and Image Formation|ch. 01]] §5.

### Q2 · Ch. 01: The grayscale pipeline

A pipeline converts images to grayscale ($Y = 0.299R + 0.587G + 0.114B$) and thresholds them to find a red sign, RGB $(0.8, 0.1, 0.1)$, on green grass, RGB $(0.1, 0.4, 0.1)$. It fails. What is the best explanation and fix?

- **A.** 8-bit quantisation merges the two colours; save images as 16-bit.
- **B.** The grayscale weights don't sum to 1, so values clip; rescale them.
- **C.** Both map to almost the same gray (about 0.31 and 0.28); colour was the information, so threshold on hue in HSV instead.
- **D.** The sensor's Bayer filter can't record red; use a different camera.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** sign $= 0.299(0.8) + 0.587(0.1) + 0.114(0.1) = 0.309$; grass $= 0.276$. A gap of 0.03 is lost in noise. Grayscale keeps structure and drops colour, and here colour is what separates the objects. Red and green are far apart in hue, and hue changes little with brightness.
> **Not A:** 0.309 and 0.276 are about 8 gray levels apart even in 8 bits; the problem is the conversion, not the bit depth. **Not B:** the weights sum to exactly 1. **Not D:** a Bayer sensor measures red at a quarter of its photosites and interpolates the rest.
> Revise: [[01 - Introduction and Image Formation|ch. 01]] §8.

### Q3 · Ch. 01: Nonsense predictions

A torchvision ResNet gives sensible predictions on images loaded with `read_image`. A teammate loads the same files with `cv2.imread`, applies `permute(2, 0, 1)`, divides by 255 and applies the ImageNet normalisation, yet predictions are clearly worse. The most likely remaining cause:

- **A.** OpenCV returns $(C, H, W)$, so the `permute` scrambled the axes.
- **B.** OpenCV returns channels in **BGR** order, so red and blue are swapped.
- **C.** OpenCV returns values in $[0, 1]$, so dividing by 255 made the image almost black.
- **D.** OpenCV applies its own ImageNet normalisation, so it was applied twice.

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** `cv2.imread` returns an $(H, W, C)$ `uint8` array in **BGR**. The teammate fixed the axes and the range but not the channel order; the model sees red and blue swapped. Fix: `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`.
> **Not A:** OpenCV gives $(H, W, C)$, so `permute(2, 0, 1)` was correct. **Not C:** values are 0–255 `uint8`. **Not D:** OpenCV does no normalisation.
> Revise: [[01 - Introduction and Image Formation|ch. 01]] §10.

### Q4 · Ch. 02: Which filter?

A 3×3 window on a scanned document contains $\{12, 10, 11, 255, 13, 9, 10, 0, 11\}$; the 255 and the 0 are salt-and-pepper noise. Which statement is correct?

- **A.** A 3×3 Gaussian is the best choice: it is isotropic and so ignores outliers.
- **B.** A box filter outputs 11 here, the same as the median.
- **C.** A bilateral filter is a convolution, so it is the fastest correct choice.
- **D.** A box filter outputs about 36.8; a median filter outputs 11, so the median removes this noise and the box smears it.

**Your answer:**
**Why:**

> [!success]- Answer: D
> **Why:** mean $= 331/9 = 36.8$, pulled far up by the single 255. Sorted values $0, 9, 10, 10, 11, 11, 12, 13, 255$ give median **11**. Salt-and-pepper noise is a few extreme outliers; the median ignores them.
> **Not A:** a Gaussian is still a weighted mean and smears outliers into a gray blob. **Not B:** the box gives 36.8. **Not C:** the bilateral filter is **not** a convolution (its weights depend on the image), and it isn't designed for impulse noise.
> Revise: [[02 - Classical Image Processing|ch. 02]] §4.

### Q5 · Ch. 02: Reading a structure tensor

At a pixel the structure tensor is $M = \begin{bmatrix} 90 & 30 \\ 30 & 10 \end{bmatrix}$. With Harris $k = 0.04$, the pixel is:

- **A.** A corner, because the trace (100) is large.
- **B.** An edge: $\det M = 0$, so $R = -400 < 0$; one eigenvalue is 100, the other 0.
- **C.** Flat, because the determinant is 0.
- **D.** Impossible to classify without computing the eigenvectors.

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** $\det M = 900 - 900 = 0$, $\operatorname{tr} M = 100$, $R = 0 - 0.04 \times 100^2 = -400$. Negative $R$ means an edge. The eigenvalues are 100 and 0: strong gradient, but all in one direction.
> **Not A:** a large trace means lots of gradient energy, not gradients in two directions; a corner needs both eigenvalues large. **Not C:** flat needs both eigenvalues near 0, and here one is 100. **Not D:** $R$ uses only $\det$ and $\operatorname{tr}$, precisely to avoid eigen-decomposition.
> Revise: [[02 - Classical Image Processing|ch. 02]] §7.

### Q6 · Ch. 02: Blurring twice

You blur an image with a Gaussian of $\sigma = 3$ and then again with $\sigma = 4$. This equals one Gaussian blur with:

- **A.** $\sigma = 5$, because variances add: $\sqrt{3^2 + 4^2}$.
- **B.** $\sigma = 7$, because the blurs add.
- **C.** $\sigma = 12$, because convolving multiplies the widths.
- **D.** No single Gaussian; two blurs make a box filter.

**Your answer:**
**Why:**

> [!success]- Answer: A
> **Why:** the semigroup property, $G_{\sigma_1} * G_{\sigma_2} = G_{\sqrt{\sigma_1^2 + \sigma_2^2}}$. $\sqrt{9 + 16} = 5$. This is what makes scale-space pyramids cheap.
> **Not B or C:** standard deviations don't add or multiply; variances add. **Not D:** a Gaussian convolved with a Gaussian is a Gaussian.
> Revise: [[02 - Classical Image Processing|ch. 02]] §4.

### Q7 · Ch. 03: The first loss value

A softmax linear classifier on CIFAR-10 ($C = 10$) prints a loss of **47.6** at iteration 0. What does this suggest?

- **A.** Normal: the initial loss should be about $C - 1 = 9$ or more.
- **B.** The learning rate is too small.
- **C.** Something is wrong before training starts (weights too large, unnormalised 0–255 inputs, or a loss bug); with small weights the loss should be about $\ln 10 = 2.30$.
- **D.** Regularisation is switched off.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** with small random weights all scores are near 0, softmax gives $p = 1/10$ to every class, and $L = -\ln 0.1 = 2.30$. A loss of 47.6 means the scores are huge before any update: large initial weights or raw 0–255 inputs, or a bug.
> **Not A:** $C - 1$ is the initial **hinge** loss, not softmax. **Not B:** the learning rate hasn't acted yet at iteration 0. **Not D:** turning regularisation on would *raise* the loss slightly; off can't explain 47.6.
> Revise: [[03 - Image Classification and Linear Models|ch. 03]] §8.

### Q8 · Ch. 03: Satisfied vs never satisfied

Three classes [cat, car, frog]. A cat image gets scores $[8.0, 5.1, -1.7]$. Which is true?

- **A.** Hinge loss is 2.9 and keeps pushing; cross-entropy is 0.
- **B.** Both losses are exactly 0, so the example stops affecting training.
- **C.** Hinge loss is 0 but its gradient still pushes the cat score up.
- **D.** Hinge loss and its gradient are 0 (every margin is met); cross-entropy is about 0.054 and still produces a gradient.

**Your answer:**
**Why:**

> [!success]- Answer: D
> **Why:** hinge: $\max(0, 5.1 - 8 + 1) + \max(0, -1.7 - 8 + 1) = 0 + 0 = 0$, so the example is past the margin and gives zero gradient. Softmax: $p_{cat} = 0.948$, loss $-\ln 0.948 = 0.054$, gradient $p - y = [-0.052, 0.052, 0.00006]$. Cross-entropy never reaches exactly 0, so it keeps widening the margin.
> **Not A:** that's backwards; 2.9 would be the hinge loss for scores $[3.2, 5.1, -1.7]$. **Not B:** cross-entropy is never exactly 0. **Not C:** past the margin the hinge gradient is exactly 0.
> Revise: [[03 - Image Classification and Linear Models|ch. 03]] §5.

### Q9 · Ch. 03: One label or several?

A chest X-ray model outputs scores $[1.5, -0.5, 0.8]$ for [pneumonia, effusion, nodule]. The radiologist reports pneumonia **and** a nodule. Which output layer should the model use, and what does it predict here?

- **A.** Softmax + cross-entropy; it predicts pneumonia only (0.61), which is correct.
- **B.** One sigmoid per class + binary cross-entropy; $\sigma = [0.82, 0.38, 0.69]$, so thresholding at 0.5 predicts pneumonia and nodule.
- **C.** Softmax, but take the top 2 classes; this always handles multi-label data.
- **D.** One sigmoid per class, then argmax over the three probabilities.

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** findings can co-occur, so they shouldn't compete for probability. Independent sigmoids answer three yes/no questions; the probabilities need not sum to 1. Thresholding gives {pneumonia, nodule}, matching the report. Loss: `BCEWithLogitsLoss`.
> **Not A:** softmax forces the classes to share a total of 1 ($[0.61, 0.08, 0.30]$) and misses the nodule. **Not C:** "top 2" is wrong whenever an image has 1 or 3 findings. **Not D:** argmax brings back the single-label assumption; multi-label uses a threshold.
> Revise: [[03 - Image Classification and Linear Models|ch. 03]] §5.

### Q10 · Ch. 04: Counting parameters

A conv layer has 64 input channels, 128 output channels, a 3×3 kernel and biases. The input is 224×224. How many parameters?

- **A.** 1,280
- **B.** 73,728
- **C.** 73,856
- **D.** It depends on the 224×224 input size.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** each filter spans all input channels: $C_{out} \cdot C_{in} \cdot k^2 + C_{out} = 128 \cdot 64 \cdot 9 + 128 = 73{,}856$.
> **Not A:** $9 \cdot 128 + 128$ forgets that each filter is $64 \times 3 \times 3$, not a 2D square. **Not B:** forgets the 128 biases. **Not D:** conv parameters are independent of $H$ and $W$ (weight sharing).
> Revise: [[04 - From Neural Networks to CNNs|ch. 04]] §5.

### Q11 · Ch. 04: Receptive field

Network: conv 3×3 (stride 1) → max-pool 2×2 (stride 2) → conv 3×3 (stride 1). How large is the receptive field of one output unit in the input image?

- **A.** 5×5
- **B.** 6×6
- **C.** 7×7
- **D.** 8×8

**Your answer:**
**Why:**

> [!success]- Answer: D
> **Why:** $r_l = r_{l-1} + (k_l - 1) j_{l-1}$, with $j$ the product of strides so far. Conv: $r = 1 + 2 = 3$, $j = 1$. Pool: $r = 3 + 1 = 4$, $j = 2$. Conv: $r = 4 + 2 \times 2 = 8$. The conv after the pool counts double because each step in its input is 2 pixels.
> **Not A:** ignores the pool entirely (two 3×3 convs). **Not B or C:** forget that the pool doubles the jump for the next layer.
> Revise: [[04 - From Neural Networks to CNNs|ch. 04]] §5.

### Q12 · Ch. 04: The deep linear network

A student trains $3072 \to 100 \to 10$ on CIFAR-10 with **no activation** between the layers. It ends with the same accuracy as the plain linear classifier. Why?

- **A.** $W_2(W_1 x + b_1) + b_2 = W'x + b'$: the two layers collapse into one linear map, so it can represent nothing new, despite 10× more parameters.
- **B.** 100 hidden units are too few; with 1,000 it would beat the linear model.
- **C.** Without activations the gradients vanish, so the first layer doesn't train.
- **D.** The network overfits because it has 308,310 parameters.

**Your answer:**
**Why:**

> [!success]- Answer: A
> **Why:** a product of matrices is one matrix. The function class is exactly the linear classifier's, so accuracy matches. The nonlinearity is the only reason depth adds expressive power.
> **Not B:** any width still collapses to one $10 \times 3072$ map. **Not C:** linear layers pass gradients fine (no saturation); the issue is what the model can represent. **Not D:** it matches the linear model, so it isn't doing worse from overfitting; it simply can't do better.
> Revise: [[04 - From Neural Networks to CNNs|ch. 04]] §2.

---

## Part 2: Architectures

### Q13 · Ch. 05: The 56-layer network

A plain 56-layer CNN (no skip connections) **with BatchNorm** has higher **training** error than a 20-layer version of the same design. What is happening, and what fixes it?

- **A.** Overfitting; add dropout and more augmentation.
- **B.** Vanishing gradients from sigmoid activations; switch to ReLU.
- **C.** The degradation problem: the optimiser can't find the solution where the extra layers act as the identity; add residual connections, $y = F(x) + x$.
- **D.** The learning rate is too high for deep networks; lower it 10×.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** a deeper network contains the shallower one (extra layers = identity), so it should never be worse on training data. It is, so the problem is optimisation. ResNet builds the identity in: each block learns only the residual $F$, and $\partial y/\partial x = \partial F/\partial x + 1$ keeps gradients flowing.
> **Not A:** overfitting shows *low* training error. **Not B:** BatchNorm is present and the lecture's point is that this isn't vanishing gradients. **Not D:** nothing in the setup points to the learning rate; the training error is stuck higher, not diverging.
> Revise: [[05 - CNN Architectures|ch. 05]] §5.

### Q14 · Ch. 05: Batch size changes accuracy

The same trained CNN scores 91% on validation with batch size 256 and 74% with batch size 16. What's wrong?

- **A.** Smaller batches have noisier gradients, so the model learns less.
- **B.** The model is still in training mode: BatchNorm normalises with each batch's own statistics; call `model.eval()` so it uses the running averages.
- **C.** Dropout is too strong; lower $p$.
- **D.** The validation set is too small to measure accuracy reliably.

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** at inference a prediction must not depend on which images share the batch. In `train()` mode BN uses batch statistics, which get noisier as the batch shrinks. In `eval()` mode it uses the stored running mean and variance, and batch size stops mattering.
> **Not A:** no training happens during validation, so there are no gradients. **Not C:** dropout in train mode would add randomness but doesn't explain a dependence on batch size. **Not D:** it's the same validation set both times.
> Revise: [[05 - CNN Architectures|ch. 05]] §2.

### Q15 · Ch. 05: Transfer learning on small data

You have 800 photos of 5 kinds of local street food and an ImageNet-pretrained ResNet-50 (25.6M parameters, `fc: 2048 → 1000`). Best strategy?

- **A.** Train ResNet-50 from scratch; pretrained ImageNet features don't know street food.
- **B.** Fine-tune all 25.6M parameters with learning rate $10^{-2}$.
- **C.** Train a ViT-B from scratch; transformers generalise better.
- **D.** Freeze the backbone and train only a new `Linear(2048, 5)`: 10,245 parameters.

**Your answer:**
**Why:**

> [!success]- Answer: D
> **Why:** small data, similar domain (natural photos): **feature extraction**. Early and middle features (edges, textures, parts) transfer. Training $2048 \times 5 + 5 = 10{,}245$ parameters on 800 images is safe; 25M would overfit.
> **Not A:** from scratch on 800 images loses badly to pretrained features. **Not B:** too many parameters for 800 images, and $10^{-2}$ would wreck the pretrained weights (fine-tuning uses 10–100× smaller rates). **Not C:** ViT from scratch needs far more data than a CNN.
> Revise: [[05 - CNN Architectures|ch. 05]] §6.

### Q16 · Ch. 06: Changing resolution in ViT

A ViT-B/16 pretrained at 224×224 is fine-tuned at 384×384. Which statement is correct?

- **A.** Tokens go from 197 to 577, each attention matrix grows about 8.6×, and the position embeddings must be interpolated to the larger grid; the Transformer weights are unchanged.
- **B.** Tokens stay at 197 because ViT resizes every input to 224 internally.
- **C.** All Transformer weight matrices must be resized because $n$ has changed.
- **D.** Tokens go to 577, but attention cost grows only linearly with them.

**Your answer:**
**Why:**

> [!success]- Answer: A
> **Why:** $(384/16)^2 + 1 = 577$ tokens. Attention is $n^2$: $(577/197)^2 \approx 8.6\times$. The learned position embeddings exist for a 14×14 grid and must be interpolated in 2D to 24×24. $W_Q, W_K, W_V, W_O$ and the MLPs don't depend on $n$.
> **Not B:** ViT has no such resizing; more pixels means more patches. **Not C:** the weights act per token, independent of $n$. **Not D:** global self-attention is quadratic in tokens (that's why Swin exists).
> Revise: [[06 - Vision Transformers|ch. 06]] §2.

### Q17 · Ch. 06: Fewer heads

A colleague changes ViT-Base from 12 to 8 attention heads (keeping $D = 768$) "to make it smaller". How does the parameter count change?

- **A.** Falls by a third, because there are a third fewer heads.
- **B.** Rises, because each head is now wider.
- **C.** Doesn't change: heads split $D$ into slices, and $W_Q, W_K, W_V, W_O$ stay $D \times D$ in total; each head just becomes 96-wide instead of 64.
- **D.** Falls by the attention matrices' size, $n^2$ per head.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** multi-head attention uses $h$ heads of size $d_h = D/h$; the projections total $4D^2$ whatever $h$ is. To shrink the model, reduce $D$, the MLP size or the number of layers.
> **Not A or B:** both assume parameters scale with $h$. **Not D:** attention weights are recomputed per input; they are not parameters.
> Revise: [[06 - Vision Transformers|ch. 06]] §1–2.

### Q18 · Ch. 06: The weaker teacher

DeiT-B distilled from an **80.0%** convnet teacher (RegNetY-4GF) reached 82.7%, better than distilling from an **81.8%** transformer teacher (81.9%). Best explanation?

- **A.** The convnet teacher was trained on more data.
- **B.** The student inherits the teacher's convolutional inductive bias (locality, translation equivariance) through its outputs, which a transformer teacher can't provide.
- **C.** Lower-accuracy teachers always produce better students, because their labels are softer.
- **D.** The convnet teacher uses a higher temperature $T$.

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** the student isn't copying accuracy; it learns the teacher's pattern of outputs. A CNN's outputs reflect the priors a ViT lacks and would otherwise need data to learn. "The bias can be handed over as data if you can't build it in."
> **Not A:** the comparison is on the same training setup; data isn't the variable. **Not C:** the stronger convnet teacher (82.9%) gave an even better student (83.0%); weakness isn't the cause. **Not D:** temperature is a distillation setting, not a property of the teacher, and not what the lecture compared.
> Revise: [[06 - Vision Transformers|ch. 06]] §4.

---

## Part 3: Detection

### Q19 · Ch. 07: The good-looking duplicate

One car, ground truth $G = (0, 0, 10, 10)$. The detector outputs $A = (1, 1, 11, 11)$ with score 0.9 and $B = (2, 0, 12, 10)$ with score 0.8. At IoU threshold 0.5, what are precision and recall for this image?

- **A.** Precision 1, recall 1: both boxes overlap $G$ by more than 0.5.
- **B.** Precision 1, recall 0.5.
- **C.** Precision 0.5, recall 0.5.
- **D.** Precision 0.5, recall 1: $A$ (IoU 0.68) claims $G$ first, so $B$ (IoU 0.67) is a duplicate and counts as a false positive.

**Your answer:**
**Why:**

> [!success]- Answer: D
> **Why:** matching goes down by score; each ground truth can be claimed once. $A$ (0.9): IoU $81/119 = 0.68$, TP. $B$ (0.8): IoU $80/120 = 0.67$, but $G$ is taken, so FP. Precision $1/2$, recall $1/1$. Duplicates cost exactly as much as hallucinations, which is why NMS matters (it would remove $B$, since IoU($A$, $B$) = 0.68 > 0.5).
> **Not A:** a ground truth can't be matched twice. **Not B or C:** the one car was found, so recall is 1.
> Revise: [[07 - Object Detection I|ch. 07]] §3.

### Q20 · Ch. 07: Which AP?

5 ground-truth people; 8 predictions sorted by score give TP, TP, FP, TP, FP, TP, FP, FP. The all-point interpolated AP is:

- **A.** 0.683
- **B.** 0.712
- **C.** 0.800
- **D.** 0.500

**Your answer:**
**Why:**

> [!success]- Answer: A
> **Why:** interpolated precision is 1.0 up to recall 0.4, 0.75 up to 0.6, 0.667 up to 0.8, then 0. Area $= 0.2 + 0.2 + 0.2(0.75) + 0.2(0.667) = 0.683$.
> **Not B:** 0.712 is the **11-point** (VOC 2007) AP of the same list, a different convention. **Not C:** 0.8 is the maximum recall, and the most AP could reach with a perfect ranking, since one person was never detected. **Not D:** 0.5 is the precision after all 8 predictions.
> Revise: [[07 - Object Detection I|ch. 07]] §3.

### Q21 · Ch. 07: Regression targets

An anchor has centre $(100, 100)$, width 50, height 100. The ground-truth box has centre $(110, 90)$, width 60, height 80. The target $t^* = (t_x, t_y, t_w, t_h)$ is:

- **A.** $(10, -10, 10, -20)$
- **B.** $(0.2, -0.1, 0.182, -0.223)$
- **C.** $(0.2, -0.1, 1.2, 0.8)$
- **D.** $(0.1, -0.2, 0.182, -0.223)$

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** $t_x = (110 - 100)/50 = 0.2$, $t_y = (90 - 100)/100 = -0.1$ (offsets divided by the anchor's own size, so the target is scale-invariant); $t_w = \log(60/50) = 0.182$, $t_h = \log(80/100) = -0.223$ (log ratios keep decoded sizes positive).
> **Not A:** raw pixel differences aren't scale-invariant. **Not C:** ratios without the log. **Not D:** divides $\Delta x$ by the height and $\Delta y$ by the width.
> Revise: [[07 - Object Detection I|ch. 07]] §4.

### Q22 · Ch. 08: Focal loss

With $\gamma = 2$, how much does focal loss down-weight an example the model already classifies with $p_t = 0.9$, compared with cross-entropy?

- **A.** 10×
- **B.** 1.23×
- **C.** 100×
- **D.** Not at all; focal loss only affects hard examples.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** focal loss multiplies CE by $(1 - p_t)^\gamma = 0.1^2 = 0.01$: CE 0.105 becomes 0.00105, a 100× reduction. Easy examples stay in the sum but count far less, so the ~$10^5$ easy background anchors no longer swamp the few objects.
> **Not A:** that would be $\gamma = 1$. **Not B:** 1.23× is the factor for a *hard* example at $p_t = 0.1$ ($0.9^2 = 0.81$). **Not D:** that's backwards: focal loss leaves hard examples nearly untouched and shrinks easy ones.
> Revise: [[08 - Object Detection II|ch. 08]] §3.

### Q23 · Ch. 08: Why initialise the bias to −4.6?

RetinaNet initialises the classification bias to $b = -\log\frac{1 - \pi}{\pi}$ with $\pi = 0.01$. What happens if you use bias 0 instead, with ~100,000 anchors per image?

- **A.** Nothing important; the bias is learned anyway within a few iterations.
- **B.** The model predicts $p = 0.01$ everywhere and misses all objects.
- **C.** Focal loss becomes equal to cross-entropy.
- **D.** Every anchor starts at $p = 0.5$, the background loss is about 69,000 per image instead of about 1,000, and the huge early gradients make training diverge.

**Your answer:**
**Why:**

> [!success]- Answer: D
> **Why:** bias 0 gives logit ≈ 0, $p = 0.5$; each background anchor costs $-\ln 0.5 = 0.693$, so $10^5 \times 0.693 \approx 69{,}300$. With $b = -\log 99 = -4.6$, $p = 0.01$ and the cost is $10^5 \times 0.010 \approx 1{,}005$. Starting at the prior means early gradients come from the few objects, not the flood of background.
> **Not A:** the paper reports divergence; the first iterations matter. **Not B:** that describes the *correct* initialisation, and it's a starting point, not a final prediction. **Not C:** the bias doesn't change the loss formula.
> Revise: [[08 - Object Detection II|ch. 08]] §3.

### Q24 · Ch. 08: Hungarian vs greedy

DETR has 3 prediction slots and 2 objects. Matching costs (lower is better):

| | Pred 1 | Pred 2 | Pred 3 |
|---|---|---|---|
| Object A | 0.1 | 0.3 | 0.9 |
| Object B | 0.2 | 0.8 | 0.9 |

Which assignment does DETR train on?

- **A.** A→2, B→1, total 0.5; Pred 3 is trained to predict "no object".
- **B.** A→1, B→2, total 0.9, because A takes its cheapest prediction first.
- **C.** A→1, B→1, because Pred 1 is cheapest for both; NMS removes the duplicate later.
- **D.** All three predictions are matched; Pred 3 to whichever object is cheaper.

**Your answer:**
**Why:**

> [!success]- Answer: A
> **Why:** DETR uses the Hungarian algorithm: the one-to-one assignment with minimum **total** cost. A→2, B→1 costs $0.3 + 0.2 = 0.5$ < 0.9. The unmatched slot is matched to $\varnothing$ and learns "no object" (no box loss).
> **Not B:** that's greedy matching; it lets A "steal" Pred 1 and leaves a worse total. **Not C:** matching is one-to-one, and DETR has no NMS. **Not D:** with 2 objects only 2 predictions can be matched.
> Revise: [[08 - Object Detection II|ch. 08]] §5.

---

## Part 4: Segmentation

### Q25 · Ch. 09: The resolution ceiling

A 40×40 square object straddles the corner shared by four stride-32 cells, covering 20×20 pixels of each. A perfect head labels each cell by majority vote (> 50% covered = object), and the mask is upsampled by copying. What IoU results?

- **A.** 1.0: the head is perfect.
- **B.** About 0.64: one cell is chosen.
- **C.** 0: each cell is only 39% covered, so all four are labelled background and the object vanishes. Even the best choice of cells reaches only 0.39.
- **D.** 0.5: two of the four cells are labelled object.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** each cell holds $400/1024 = 39\%$ object, under the 50% vote. Taking all four cells gives the best possible IoU, $1600/4096 = 0.39$, which is the lecture's stride-32 ceiling. A perfect classifier is still capped by output resolution; skips (FCN, U-Net) and atrous convolution (DeepLab) exist for this.
> **Not A:** perfect cell labels can't draw sub-cell boundaries. **Not B:** 0.64 is what stride 16 gives on this object. **Not D:** by symmetry all four cells are covered equally; none passes 50%.
> Revise: [[09 - Segmentation|ch. 09]] §1.

### Q26 · Ch. 09: The checkerboard

A decoder upsamples ×2 with a transposed convolution, $k = 3$, $s = 2$, and the outputs show a faint checkerboard pattern, even early in training. Which change removes the pattern's cause?

- **A.** Add more output padding.
- **B.** Use $k = 4$ (a multiple of the stride), or bilinear upsampling followed by an ordinary conv.
- **C.** Replace it with max unpooling using freshly random indices.
- **D.** Train longer; the kernel will learn to cancel it.

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** with $k = 3$, $s = 2$, kernel copies overlap unevenly: along one axis output pixels receive 1, 2, 1, 2, … copies, so in 2D they receive 1, 2 or 4, a checkerboard. With $k = 4$, $s = 2$ every interior pixel gets exactly 2. Bilinear + conv avoids overlap entirely.
> **Not A:** output padding only adds a row/column at the edge. **Not C:** max unpooling needs the indices saved by the encoder's max-pool; random ones put values in meaningless places. **Not D:** the uneven overlap is structural; learning can reduce but not remove it.
> Revise: [[09 - Segmentation|ch. 09]] §2.

### Q27 · Ch. 09: Atrous convolution

DeepLab's ASPP uses a 3×3 convolution at rate 12. Which is correct?

- **A.** It covers 12×12 and has 144 weights per channel pair.
- **B.** It covers 36×36, three times rate 12.
- **C.** It covers 25×25 but must use stride 12 to do so.
- **D.** It covers 25×25 ($k_{eff} = 2r + 1$) with only 9 weights per channel pair, and keeps the resolution because the stride is 1.

**Your answer:**
**Why:**

> [!success]- Answer: D
> **Why:** inserting $r - 1$ gaps gives $k_{eff} = k + (k - 1)(r - 1) = 3 + 2 \times 11 = 25$. The kernel still has 9 weights. Dilation buys receptive field **without stride**, which is why DeepLabv3+ can stay at output stride 16 instead of 32. (Rates 6 and 18 give 13 and 37.)
> **Not A:** confuses the rate with the kernel size. **Not B:** wrong formula. **Not C:** dilation and stride are independent; ASPP runs at stride 1.
> Revise: [[09 - Segmentation|ch. 09]] §4.

### Q28 · Ch. 09: U-Net tiles

With the original U-Net sizes, a 572×572 input tile gives a 388×388 output. You segment a 1000×1000 pathology slide. Which is correct?

- **A.** Unpadded 3×3 convs trim 92 px per side; use 9 tiles whose 388 px outputs abut and whose 572 px inputs overlap, and mirror the image to supply context beyond the slide's edge.
- **B.** Pad every conv with zeros so input and output match; one 1000×1000 pass is equivalent.
- **C.** The 184 px lost are due to max-pooling; pooling with padding would remove the loss.
- **D.** Tile with non-overlapping 572 px inputs and stitch the 388 px outputs, leaving the gaps to interpolation.

**Your answer:**
**Why:**

> [!success]- Answer: A
> **Why:** $(572 - 388)/2 = 92$ px per side are lost to unpadded convs; the network only labels pixels it saw enough context for. $\lceil 1000/388 \rceil = 3$ tiles per side → 9 tiles. Outputs abut; inputs overlap by $2 \times 92$ px. At the slide's border the context doesn't exist, so it's **mirrored** (zero padding would darken and bias the border).
> **Not B:** zero padding biases border predictions, and one full pass may not fit in memory (overlap-tile is a memory strategy). **Not C:** 2×2 pooling halves sizes exactly here; the loss comes from the 3×3 convs. **Not D:** leaves unlabelled gaps between tiles.
> Revise: [[09 - Segmentation|ch. 09]] §3.

### Q29 · Ch. 09: Loss for tiny lesions

Lesions occupy about 0.01% of each image. A U-Net trained with plain pixel-averaged cross-entropy learns to predict "background" everywhere. Best loss choice?

- **A.** Focal loss: it fixes object-size imbalance.
- **B.** Soft Dice alone: it's scale-free, so it's always best.
- **C.** Dice + CE ($\lambda = \frac12$): Dice is scale-free so the tiny lesion isn't drowned out, and CE gives a well-conditioned gradient early, when overlap is near 0 and Dice's gradient is tiny.
- **D.** Plain CE with a larger learning rate.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** with pixel-averaged CE the lesion's share of the signal scales with its area (3000× less at 0.01% than at 30%). Soft Dice is an overlap ratio, so object size cancels. But near-zero overlap at the start gives Dice almost no gradient, so it starts badly; CE fixes that. Dice + CE is nnU-Net's default.
> **Not A:** focal loss reweights easy vs hard pixels; on the lecture's plot CE and focal are the same line against object size. **Not B:** Dice alone starts badly. **Not D:** the learning rate doesn't change the lesion's share of the loss.
> Revise: [[09 - Segmentation|ch. 09]] §5.

### Q30 · Ch. 09: Reading the metrics

A 100×100 image contains a 400-pixel lesion. The model gets TP = 300, FP = 100, FN = 100. Which is correct?

- **A.** IoU 0.75, Dice 0.60, pixel accuracy 0.98.
- **B.** IoU 0.60, Dice 0.75, pixel accuracy 0.98; an all-background model would still get 0.96 accuracy but only 0.48 mIoU.
- **C.** IoU 0.60, Dice 0.75; Dice is higher, so the Dice model is better.
- **D.** IoU 0.60, pixel accuracy 0.75.

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** IoU $= 300/500 = 0.60$; Dice $= 600/800 = 0.75 = 2(0.6)/1.6$; accuracy $= (300 + 9{,}500)/10{,}000 = 0.98$. All-background: accuracy $9{,}600/10{,}000 = 0.96$, lesion IoU 0, background IoU 0.96, mIoU 0.48. Pixel accuracy barely notices; mIoU exposes it.
> **Not A:** IoU and Dice swapped; Dice is always ≥ IoU. **Not C:** Dice and IoU are monotone in each other; the same prediction gets both, so neither "model" is better. **Not D:** 0.75 is Dice, not accuracy.
> Revise: [[09 - Segmentation|ch. 09]] §6.

### Q31 · Ch. 09: Panoptic quality

Ground truth: sky, road, car A, car B, person. Predictions: sky (IoU 0.90), road (0.95), car A (0.70), a car overlapping car B with IoU **0.40**, person (0.60), and a "tree" with no ground truth. PQ is:

- **A.** 0.79
- **B.** 0.73
- **C.** 0.65
- **D.** 0.57

**Your answer:**
**Why:**

> [!success]- Answer: D
> **Why:** a match needs the same class and IoU > 0.5, so the 0.40 car is an **FP** and car B is an **FN**; the tree is another FP. TP = 4, FP = 2, FN = 1. PQ $= (0.90 + 0.95 + 0.70 + 0.60)/(4 + 1 + 0.5) = 3.15/5.5 = 0.57$ (SQ 0.79 × RQ 0.73).
> **Not A:** that's SQ alone, which ignores missed and invented segments. **Not B:** that's RQ alone. **Not C:** counts the 0.40 car as a TP, which the threshold forbids.
> Revise: [[09 - Segmentation|ch. 09]] §6.

### Q32 · Ch. 09: Why RoIAlign mattered

A box's corners land at feature coordinates 1.37 and 6.41 on a stride-32 map. RoIPool rounds them to 1 and 6. Which is correct?

- **A.** The corners shift by about 12 and 13 image pixels. A box at IoU 0.5 tolerates that, but a mask doesn't, which is why removing the rounding gave +7.3 AP at stride 32 (and only +3 at stride 16).
- **B.** Rounding moves corners by under one pixel, so RoIAlign matters only for tiny objects.
- **C.** RoIAlign helps because it uses max-pooling at 4 points instead of 1.
- **D.** The error is the same at every stride, so RoIAlign's gain doesn't depend on the backbone.

**Your answer:**
**Why:**

> [!success]- Answer: A
> **Why:** $0.37 \times 32 = 11.8$ px and $0.41 \times 32 = 13.1$ px. RoIAlign does no rounding: it samples each bin at 4 points with **bilinear interpolation**. A shift invisible to a box metric moves the whole mask edge. At stride 16 the same rounding costs half as many pixels, hence the smaller gain.
> **Not B:** the rounding is in feature cells, and one cell is 32 image pixels. **Not C:** the key is bilinear sampling at the exact location; the pooling over the 4 samples is secondary. **Not D:** the pixel error scales with the stride.
> Revise: [[09 - Segmentation|ch. 09]] §7.

### Q33 · Ch. 09: Masks per class

A teammate changes Mask R-CNN's mask head from $K$ per-class sigmoid masks to a softmax over the $K$ classes at every pixel. What happens?

- **A.** Mask AP rises, because softmax gives calibrated probabilities.
- **B.** Nothing changes; it's an implementation detail.
- **C.** Mask AP drops (24.8 vs 30.3 AP in the paper): softmax makes classes compete for pixels, coupling the mask to classification; with sigmoids the mask head only decides object vs not, and the box branch picks the class.
- **D.** The model can no longer separate two cars, because softmax merges instances.

**Your answer:**
**Why:**

> [!success]- Answer: C
> **Why:** decoupling mask from class is one of the paper's two design decisions worth copying (+5.5 AP). The class is already decided by the box branch; the mask only needs a binary decision for that class.
> **Not A:** the measured effect goes the other way. **Not B:** a 5.5 AP difference isn't a detail. **Not D:** instances are separated by having one RoI per object, not by the mask activation.
> Revise: [[09 - Segmentation|ch. 09]] §7.

### Q34 · Ch. 09: SAM on microscopy

A team must segment cell nuclei in 40 labelled microscopy images and plans to use zero-shot SAM for the final masks. Best advice?

- **A.** Good plan: SA-1B's 1 billion masks cover every domain, and SAM outputs class labels.
- **B.** Use SAM to speed up **annotation** (click and correct), then train a U-Net with elastic augmentation and Dice + CE; zero-shot SAM is often worse than a small U-Net on microscopy, and SAM 1/2 masks carry no labels.
- **C.** Use Mask2Former trained from scratch on the 40 images.
- **D.** Use SAM, but choose the lowest-scoring of its three masks to get the finest detail.

**Your answer:**
**Why:**

> [!success]- Answer: B
> **Why:** SA-1B is natural images; under domain shift (microscopy, radiology, SAR) zero-shot SAM often loses to a small U-Net trained on ~30 of your own images. SAM 1 and 2 return regions, not names. Where SAM reliably pays is labelling speed (about 10×). U-Net was built for this regime (30 images, elastic deformation, a weight map for touching cells).
> **Not A:** both claims are false. **Not C:** a large transformer model from scratch on 40 images is the opposite of what the data supports. **Not D:** the three masks cover ambiguity (whole/part/subpart); the score is SAM's estimate of mask quality, and the lowest is the least likely to be right.
> Revise: [[09 - Segmentation|ch. 09]] §9–10.

---

> [!abstract]- Answer key
> | Q | Ans | Q | Ans | Q | Ans | Q | Ans |
> |---|---|---|---|---|---|---|---|
> | 1 | A | 10 | C | 19 | D | 28 | A |
> | 2 | C | 11 | D | 20 | A | 29 | C |
> | 3 | B | 12 | A | 21 | B | 30 | B |
> | 4 | D | 13 | C | 22 | C | 31 | D |
> | 5 | B | 14 | B | 23 | D | 32 | A |
> | 6 | A | 15 | D | 24 | A | 33 | C |
> | 7 | C | 16 | A | 25 | C | 34 | B |
> | 8 | D | 17 | C | 26 | B | | |
> | 9 | B | 18 | B | 27 | D | | |

**Back to:** [[00-Index]]
