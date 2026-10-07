---
subject: Computer Vision
chapter: 2
tags: [ds, computer-vision, filtering, convolution, edges, canny, morphology, harris, sift, hog]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 02: Classical Image Processing (67 slides); Szeliski 2nd ed. ch. 3 and §7.1–7.2"
---

# Classical Image Processing

Week 2. The hand-designed methods from roughly 1963–2005: point operations, filtering, noise removal, edges, morphology, and features (Harris, SIFT, HOG). The lecture ends by showing that a CNN uses the same machinery with learned weights.

## 📘 Main Knowledge

### 1. Why study classical methods in a deep learning course? (slides 4–6)

- A CNN *is* a stack of learned convolutions, so you can't reason about one without understanding convolution.
- Classical methods still run in production: preprocessing, augmentation, video, camera calibration, annotation tools.
- They are cheap, interpretable, and need no training data.

The four ideas running through the lecture:
1. A filter is a small matrix slid over the image.
2. Smoothing suppresses noise; differencing (taking differences between neighbours) finds structure.
3. Good features are **invariant** to nuisance changes (lighting, rotation, scale).
4. Designing those features by hand is hard, which is why we'll learn them instead.

**Timeline (slide 6):** Roberts' first edge operator (1963), Sobel (1968, still in `cv2`), Laplacian of Gaussian, morphology and image pyramids (1980–83), Canny and Harris (1986–88), JPEG (1992), SIFT and HOG (1999–2005). AlexNet (2012) ended the era, *"but not the operators."*

### 2. Point operations and histograms (slides 7–10)

A **point operation** computes each output pixel from the input pixel at the same position only: $J(m,n) = f(I(m,n))$.

| Operation | $f(v)$ |
|---|---|
| Brightness | $v + b$ |
| Contrast | $a\,v$ |
| Gamma | $v^\gamma$, with $v \in [0,1]$ ($\gamma < 1$ brightens dark tones, $\gamma > 1$ darkens them) |
| Negative | $255 - v$ |
| Threshold | $\mathbb 1[v > \tau]$ (1 if $v > \tau$, else 0) |

Point operations use no spatial information. Anything that depends on shape or structure needs a neighbourhood.

**The histogram** counts how many pixels have each intensity:

$$h(v) = \big|\{(m,n) : I(m,n) = v\}\big|, \quad v = 0,\dots,255$$

Divide by the number of pixels to get a probability distribution $p(v)$.
- Under- and over-exposure are visible at a glance (counts piled up at 0 or 255).
- It **discards all spatial layout**: two completely different images can have the same histogram.
- It is the basis of automatic thresholding (Otsu's method), histogram matching and equalisation.

**Histogram equalisation** spreads intensities so the output histogram is roughly uniform, which increases contrast. Use the cumulative distribution function (CDF):

$$c(v) = \sum_{u \le v} p(u), \qquad J = \lfloor 255\, c(I) \rfloor$$

Why it works: if a random variable $V$ has CDF $c$, then $c(V)$ is uniformly distributed on $[0,1]$ (the *probability integral transform*).

Example: a 4×4 image using only the values 50, 52, 54, 56 with counts 3, 6, 5, 2. The CDF is 0.1875, 0.5625, 0.875, 1, so the values map to 47, 143, 223, 255. A range of 6 grey levels becomes a range of 208.

Problems and the fix:
- Global equalisation also amplifies noise in flat regions.
- **CLAHE** (Contrast-Limited Adaptive Histogram Equalisation) equalises small tiles separately, clips each tile's histogram so no level is boosted too much, then interpolates between tiles to hide the seams.

### 3. Linear filtering and convolution (slides 11–16)

A **linear filter** replaces each pixel with a weighted sum of its neighbours. The weights form a small matrix $h$, the **kernel**, and the same weights are used at every position.

**Correlation** (what is usually implemented):
$$J(m,n) = \sum_{u,v} h(u,v)\, I(m+u,\, n+v)$$

**Convolution** flips the kernel first:
$$J(m,n) = (h * I)(m,n) = \sum_{u,v} h(u,v)\, I(m-u,\, n-v)$$

For symmetric kernels (Gaussian, box) the two are identical. The flip is what gives convolution its nice algebra: it is commutative and associative, so applying $h_1$ then $h_2$ is the same as applying the single kernel $h_1 * h_2$. CNN "convolution" layers actually compute correlation; since the kernel is learned, the flip doesn't matter.

**Properties (slide 15):**
- **Linearity:** $h * (\alpha I_1 + \beta I_2) = \alpha (h * I_1) + \beta (h * I_2)$.
- **Shift equivariance:** shift the input and the output shifts by the same amount.
- **Identity:** the delta kernel $\delta$ (1 in the centre, 0 elsewhere) leaves $I$ unchanged.
- **Convolution theorem:** $\mathcal F\{h * I\} = \mathcal F\{h\} \cdot \mathcal F\{I\}$. Convolution in space is multiplication in frequency. Smoothing kernels keep low frequencies; derivative kernels keep high ones.

> [!important] Linear + shift-invariant ⇒ convolution
> Any operation that is both linear and shift-invariant *is* a convolution; there is no other choice. That is the theoretical reason CNNs use convolutional layers: we want translation equivariance (a cat shifted left should produce features shifted left).

**Borders (slide 16).** Near the edge, the kernel window hangs off the image. Common choices:
- **Zero (constant) padding**: fill with 0. Adds a dark rim.
- **Replicate**: repeat the border pixel.
- **Reflect**: mirror the image across the border.
- **Wrap**: treat the image as a torus (what the FFT assumes).

**Output size** with input size $H$, kernel size $f$, padding $p$, stride $s$:

$$H_{out} = \left\lfloor \frac{H + 2p - f}{s} \right\rfloor + 1$$

This is exactly the formula used for every CNN layer. **"Same" padding** (output size = input size at stride 1) means $p = (f-1)/2$, which is a whole number only for **odd** $f$. That's one reason kernels are almost always 3×3, 5×5, 7×7.

### 4. Smoothing and noise (slides 17–24)

**Noise models (slide 18):**

| Noise | Cause | Model |
|---|---|---|
| Additive Gaussian | sensor read noise, amplifier | $I_{obs} = I + \eta$, $\eta \sim \mathcal N(0, \sigma^2)$ |
| Poisson (shot) | photon counting | $I_{obs} \sim \text{Poisson}(\lambda)$, variance $= \lambda$, so it grows with brightness |
| Salt & pepper | dead pixels, transmission errors | a fraction of pixels set to 0 or 255 |

*"The noise model determines the right filter."*

**Box filter.** Average over a $(2k+1)\times(2k+1)$ window: every weight is $1/(2k+1)^2$. Averaging $N$ independent pixels with noise variance $\sigma^2$ gives variance $\sigma^2/N$, so a 3×3 box cuts noise variance by 9 (standard deviation by 3). But the box has hard edges:
- Its frequency response is a sinc function, which causes **ringing** artefacts.
- It creates horizontal and vertical streaks.
- It is **not isotropic** (direction-independent): diagonal edges are treated differently from vertical ones.

**Gaussian filter:**

$$G_\sigma(x,y) = \frac{1}{2\pi\sigma^2} \exp\!\left(-\frac{x^2 + y^2}{2\sigma^2}\right)$$

- **Isotropic**: depends only on the distance from the centre.
- Smooth in frequency, so no ringing.
- Weights fall off with distance, so nearby pixels count more.
- $\sigma$ sets the scale. Truncate the kernel at about $\pm 3\sigma$ (for $\sigma = 2$, a 13×13 kernel).
- **Normalise so the weights sum to 1**, otherwise the image gets brighter or darker.
- *"$\sigma$, not the kernel size, is the meaningful parameter."*

**Separability (slide 21).** The 2D Gaussian is a product of two 1D Gaussians, $G_\sigma(x,y) = g_\sigma(x)\, g_\sigma(y)$. So you can filter rows with $g_\sigma$, then columns with $g_\sigma$. Cost per pixel drops from $k^2$ to $2k$ multiplications:

| Kernel size $k$ | $k^2$ | $2k$ | Speed-up |
|---|---|---|---|
| 3 | 9 | 6 | 1.5× |
| 7 | 49 | 14 | 3.5× |
| 15 | 225 | 30 | 7.5× |

**Two more Gaussian facts (slide 22):**
- **Semigroup property:** $G_{\sigma_1} * G_{\sigma_2} = G_{\sqrt{\sigma_1^2 + \sigma_2^2}}$. Blurring twice equals blurring once with a larger $\sigma$; the *variances* add (e.g. $\sigma = 3$ then $\sigma = 4$ gives $\sigma = 5$). This makes scale-space pyramids cheap: keep blurring the previous level instead of starting from the original.
- **Derivative theorem:** $\frac{\partial}{\partial x}(G_\sigma * I) = \left(\frac{\partial G_\sigma}{\partial x}\right) * I$. Smoothing then differentiating is the same as one convolution with the derivative of the Gaussian. This is the foundation of edge detection (§5).

**Median filter (slide 23).** Replace each pixel with the median of its window:

$$J(m,n) = \operatorname{median}\{ I(m+u,\, n+v) \}$$

- **Nonlinear**: not a convolution, no kernel.
- An outlier pulls the mean a lot but barely moves the median. For the window $\{12, 10, 11, 255, 13, 9, 10, 0, 11\}$ the mean is 36.8 but the median is 11.
- Removes salt-and-pepper noise almost perfectly; a Gaussian just smears each bad pixel into a grey blob.
- Preserves step edges: the median of a half-dark, half-bright window is one of the two values, not their average.
- Cost: sorting each window is $O(HWk^2 \log k)$ naively; histogram-based versions are $O(HWk)$.

**Bilateral filter (slide 24).** Weight each neighbour by *both* its distance and its intensity difference:

$$J(p) = \frac{1}{W_p} \sum_{q \in \mathcal N(p)} \underbrace{G_{\sigma_s}(\|p - q\|)}_{\text{spatial}}\; \underbrace{G_{\sigma_r}(|I(p) - I(q)|)}_{\text{range}}\; I(q)$$

where $W_p$ is the sum of the weights.
- Across an edge, $|I(p) - I(q)|$ is large, so the weight is near 0 and the edge survives.
- In a flat region it behaves like a Gaussian.
- The weights depend on the image, so it is **not shift-invariant and not a convolution**.
- Overdone, it gives the "plastic skin" look of phone beauty filters.

### 5. Image gradients and edge detection (slides 25–39)

**An edge** is a rapid change in intensity. It can come from:
- a **depth discontinuity** (object boundary),
- a **surface orientation** change (a fold),
- a **reflectance** change (paint, texture),
- an **illumination** change (shadow).

The pixels can't tell you which. *"A shadow edge and an object edge look identical locally — a permanent limitation of purely local methods."*

**Discrete derivatives (slide 27):**
- Forward difference: $\partial I/\partial x \approx I(x+1) - I(x)$.
- Central difference: $\partial I/\partial x \approx \frac{I(x+1) - I(x-1)}{2}$ (symmetric, more accurate). As a kernel: $h_x = \tfrac12[-1,\ 0,\ 1]$, and $h_y$ is the same as a column.

**Differentiation amplifies noise (slide 28).** Noise is high-frequency, and differentiation multiplies each frequency component by its frequency $\omega$, so noise is boosted more than the signal. **Smooth first.** By the derivative theorem, that's a single convolution with the **derivative-of-Gaussian** kernel:

$$\frac{\partial G_\sigma}{\partial x}(x,y) = -\frac{x}{\sigma^2}\, G_\sigma(x,y)$$

- Antisymmetric, so it **sums to zero**: flat regions give no response.
- $\sigma$ picks *which* edges you find: small $\sigma$ finds texture and fine detail, large $\sigma$ only major boundaries. There's no single correct $\sigma$; "edge" depends on scale.
- Also separable: $\partial_x G_\sigma = g'_\sigma(x)\, g_\sigma(y)$.

**Sobel and Prewitt (slide 30).** Smooth along one axis and difference along the other, in one 3×3 kernel:

$$S_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \\ 1 \end{bmatrix} \begin{bmatrix} -1 & 0 & 1 \end{bmatrix}, \qquad S_y = S_x^\top$$

- $S_x$ measures horizontal change, so it detects **vertical** edges.
- Separable, integer-valued, cheap.
- **Prewitt** uses $[1,1,1]$ for the smoothing part (box smoothing, slightly noisier).
- **Scharr** uses $[3,10,3]$, a better approximation of rotation invariance.

**Gradient magnitude and orientation (slide 31):**

$$\nabla I = \left(\frac{\partial I}{\partial x},\ \frac{\partial I}{\partial y}\right)^\top, \qquad \|\nabla I\| = \sqrt{I_x^2 + I_y^2}, \qquad \theta = \operatorname{atan2}(I_y, I_x)$$

- $\nabla I$ points in the direction of steepest intensity increase, which is **perpendicular to the edge**.
- The magnitude is the edge strength.
- If brightness is scaled ($I \to aI$), the magnitude scales by $a$ too. That's why HOG and SIFT normalise their descriptors.

**The Laplacian (slide 32)** uses second derivatives:

$$\nabla^2 I = \frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2} \approx \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix} * I$$

- Edges become **zero crossings** instead of peaks, which can be located to sub-pixel precision.
- Rotationally symmetric: one filter, no orientation. But it **loses the edge direction**.
- Very noise-sensitive: second derivatives amplify each frequency by $\omega^2$.

**Laplacian of Gaussian (LoG) and Difference of Gaussians (DoG) (slide 33):**
- **LoG** smooths and takes the Laplacian in one kernel (the "Mexican hat"), used for edge and blob detection:
$$\nabla^2 G_\sigma(x,y) = \frac{x^2 + y^2 - 2\sigma^2}{\sigma^4}\, G_\sigma(x,y)$$
- **DoG** approximates it by subtracting two Gaussian blurs at nearby scales, which is much faster because each Gaussian is separable:
$$G_{k\sigma} - G_\sigma \approx (k-1)\,\sigma^2\, \nabla^2 G_\sigma$$
- The approximation is good when $k$ is close to 1. DoG is the operator SIFT uses to find keypoints.

**The Canny edge detector (1986) (slides 35–39).** Canny defined what an optimal edge detector should achieve:
1. **Good detection**: find real edges, few false ones.
2. **Good localisation**: report the edge where it actually is.
3. **Single response**: one detection per edge, not a thick band.

The four stages:
1. **Smooth** with $G_\sigma$.
2. **Compute** gradient magnitude $\|\nabla I\|$ and direction $\theta$.
3. **Non-maximum suppression (NMS) along $\theta$.** The gradient magnitude forms a ridge several pixels wide; we want a 1-pixel line. Round $\theta$ to 0°, 45°, 90° or 135°, compare each pixel with its two neighbours along the gradient direction (across the edge), and keep it only if it's the largest.
4. **Hysteresis thresholding** with two thresholds $\tau_{low} < \tau_{high}$:
   - $\|\nabla I\| > \tau_{high}$: strong edge, keep;
   - $\|\nabla I\| < \tau_{low}$: discard;
   - in between: keep **only if connected** to a strong edge pixel.

   A single threshold forces a bad choice: too high and edges break into pieces, too low and noise floods in. Hysteresis removes isolated weak responses and joins broken edges.

**Canny in practice (slide 39):** $\sigma$ controls *which* edges appear; the thresholds control *how many*. No setting works everywhere, because contrast depends on the scene. This parameter sensitivity is a big reason hand-designed pipelines gave way to learned ones; modern boundary detectors are CNNs trained on human-drawn boundaries. In OpenCV: `cv2.Canny(img, 100, 200)`, which expects an 8-bit single-channel image.

### 6. Morphological operations (slides 40–45)

Morphology works on **shape**, not intensity. A binary image is treated as a **set** of foreground pixels: $A = \{(m,n) : I(m,n) = 1\}$.

Notation:
- $B$ is the **structuring element**: a small set of offsets (square, cross, disk) with a chosen origin.
- $B_z = \{b + z\}$ is $B$ moved to pixel $z$; $\hat B = \{-b\}$ is $B$ reflected (equal to $B$ if symmetric); $A^c$ is the background.

**Dilation** grows the foreground:
$$A \oplus B = \{ z : (\hat B)_z \cap A \neq \emptyset \}$$
"Does $B$, placed at $z$, touch the object at all?"

**Erosion** shrinks the foreground:
$$A \ominus B = \{ z : B_z \subseteq A \}$$
"Does $B$, placed at $z$, fit entirely inside the object?"

**Duality:** $(A \ominus B)^c = A^c \oplus \hat B$. Eroding the object is dilating the background.

| | Erosion | Dilation |
|---|---|---|
| Effect | removes small specks, breaks thin connections, shrinks objects by about the radius of $B$ | fills small holes and gaps, joins nearby components, grows objects by the radius of $B$ |

Neither is invertible: what erosion removes, dilation can't bring back.

**Opening and closing (slide 43):**
- **Opening** = erode, then dilate: $A \circ B = (A \ominus B) \oplus B$. Removes small objects and thin protrusions, then restores the size of what's left.
- **Closing** = dilate, then erode: $A \bullet B = (A \oplus B) \ominus B$. Fills small holes and gaps, then restores the outer boundary.
- Both are **idempotent**: applying them a second time changes nothing.

**Derived operators (slide 44):**
- **Morphological gradient** $(A \oplus B) - (A \ominus B)$: an edge map without derivatives.
- **Top-hat** $A - (A \circ B)$: bright details smaller than $B$; used to correct uneven illumination.
- **Black-hat** $(A \bullet B) - A$: dark details.
- Skeletonisation and hit-or-miss for shape analysis.

**Grayscale morphology:** replace set intersection and inclusion with max and min over the window. **Dilation is a max filter, erosion is a min filter, and max-pooling in a CNN is grayscale dilation.**

**A complete classical pipeline: counting coins (slide 45):**
1. Grayscale.
2. Gaussian blur ($\sigma = 2$).
3. Otsu threshold → binary image.
4. Opening to remove specks.
5. Closing to fill holes.
6. Connected components → count.

No training data, no GPU, milliseconds. For a controlled scene (factory conveyor, scanned document) this still beats a neural network on cost and reliability.

### 7. Corners, keypoints and descriptors (slides 46–60)

**Why corners (slide 47).** To match two images you need points you can find again. Look at a small window and imagine shifting it:

| Region | Shifting the window… | Information |
|---|---|---|
| Flat | changes nothing in any direction | none |
| Edge | changes nothing *along* the edge | position along the edge is unknown (the **aperture problem**) |
| Corner | changes the content in *every* direction | uniquely locatable |

**Harris corner detector (slides 48–51).** Measure how much a window changes when shifted by $(u,v)$:

$$E(u,v) = \sum_{x,y} w(x,y)\, \big[ I(x+u,\, y+v) - I(x,y) \big]^2$$

$w$ is a window function centred on the pixel being tested: a box (simple, not isotropic) or, usually, a Gaussian. With a first-order Taylor expansion $I(x+u, y+v) \approx I(x,y) + u I_x + v I_y$:

$$E(u,v) \approx \begin{bmatrix} u & v \end{bmatrix} M \begin{bmatrix} u \\ v \end{bmatrix}, \qquad M = \sum_{x,y} w(x,y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}$$

$M$ is the **structure tensor**. Each entry is a blurred product of derivatives. $M$ is symmetric positive semi-definite, so it has real eigenvalues $\lambda_1 \ge \lambda_2 \ge 0$. The curves $E(u,v) = \text{const}$ are ellipses with axes proportional to $1/\sqrt{\lambda_i}$.

| Eigenvalues | Structure |
|---|---|
| $\lambda_1 \approx \lambda_2 \approx 0$ | flat |
| $\lambda_1 \gg \lambda_2 \approx 0$ | edge |
| $\lambda_1 \approx \lambda_2 \gg 0$ | corner |

**Harris response.** Computing eigenvalues at every pixel is expensive, so Harris and Stephens used the determinant and trace, which come straight from $M$'s entries:

$$R = \det M - k\,(\operatorname{tr} M)^2 = \lambda_1 \lambda_2 - k(\lambda_1 + \lambda_2)^2, \qquad k \in [0.04, 0.06]$$

- $R \gg 0$: corner. $R < 0$: edge. $|R|$ small: flat.
- Then threshold $R$ and apply non-maximum suppression.
- **Shi–Tomasi** uses $R = \min(\lambda_1, \lambda_2)$ instead (OpenCV's `goodFeaturesToTrack`).

Example with $k = 0.04$: eigenvalues $(100, 80)$ give $R = 8000 - 1296 = 6704$ (corner); $(100, 1)$ give $R = 100 - 408 = -308$ (edge).

**What Harris is and isn't invariant to (slide 51):**
- Invariant to **rotation** (eigenvalues don't change when the ellipse rotates) and **intensity shift** $I + b$ (derivatives unchanged).
- Partly invariant to **intensity scaling** $aI$, if the threshold is adjusted.
- **Not invariant to scale**: zoom in and a corner becomes a smooth curve that the same window no longer sees as a corner. Also not invariant to large viewpoint changes.

**Scale space (slide 52).** If you don't know an object's size, search all sizes. Build a stack of increasingly blurred images $L(x,y,\sigma) = G_\sigma * I$. A blob of radius $r$ gives the strongest (scale-normalised) LoG response at $\sigma = r/\sqrt2$. Finding an extremum in $\sigma$ as well as in $(x,y)$ recovers the object's **characteristic scale**. The response must be multiplied by $\sigma^2$, otherwise it always shrinks as $\sigma$ grows.

**SIFT (Scale-Invariant Feature Transform, Lowe 1999/2004) (slides 53–56).** Four stages:

| Stage | What it does | Gives |
|---|---|---|
| 1. Detect | find extrema in a DoG scale space | scale invariance |
| 2. Localise | refine position, reject weak points | stability |
| 3. Orient | find the dominant gradient direction | rotation invariance |
| 4. Describe | build a 128-D vector | robustness to illumination |

- **Stage 1:** build a DoG pyramid $D = L_{k\sigma} - L_\sigma$. Keep points that are larger or smaller than all **26 neighbours** (8 in the same image, 9 in the scale above, 9 below). Each keypoint comes with its scale.
- **Stage 2:** fit a 3D quadratic to $D(x,y,\sigma)$ for sub-pixel, sub-scale position. Drop low-contrast points (they won't survive noise). Drop edge responses using the ratio $\operatorname{tr}^2/\det$ of the Hessian (second-derivative matrix), which is the same eigenvalue test as Harris.
- **Stage 3:** histogram gradient orientations around the keypoint into 36 bins, weighted by magnitude. The highest peak is the keypoint's orientation; any other peak above 80% of it creates an extra keypoint.
- **Stage 4:** at the keypoint's own scale and rotated to its own orientation, take a 16×16 patch and split it into 4×4 cells. Each cell gets an 8-bin orientation histogram. Concatenate: $4 \times 4 \times 8 = 128$ numbers. Normalise, clip values at 0.2, normalise again (limits the effect of strong lighting changes).

Because the descriptor is measured relative to the keypoint's scale and orientation, two descriptors of the same point in differently scaled or rotated images can be compared directly.

**Matching (slide 56).** Find the nearest neighbour in 128-D Euclidean space. But a nearest neighbour always exists, even for a wrong match. **Lowe's ratio test:** accept only if

$$\frac{d_1}{d_2} < 0.8$$

where $d_1, d_2$ are the distances to the best and second-best match. A distinctive feature has $d_1 \ll d_2$; an ambiguous one (repeated texture, e.g. windows on a building) doesn't, and gets rejected. Then **RANSAC** fits a geometric model and throws out the remaining wrong matches.

**The SIFT family (slide 57):**

| Method | Year | Descriptor | Note |
|---|---|---|---|
| SIFT | 1999 | 128-D float | the reference; patent expired 2020, now in main OpenCV |
| SURF | 2006 | 64-D float | box filters + integral images; faster |
| ORB | 2011 | 256-bit binary | FAST corners + rotated BRIEF; free, real-time, used in ORB-SLAM |
| BRISK / FREAK | 2011–12 | binary | hand-designed sampling patterns |
| SuperPoint | 2018 | 256-D learned | self-supervised CNN, the learned successor |

Structure-from-motion, SLAM, panorama stitching and image registration still mostly use these. Geometry is an area where hand-designed features remain competitive.

**HOG: Histogram of Oriented Gradients (Dalal & Triggs, 2005) (slides 58–60).** A *dense* descriptor for a whole object window (not sparse keypoints), designed for pedestrian detection:
1. Compute $I_x, I_y$ with plain $[-1, 0, 1]$, no smoothing.
2. Divide the window into 8×8-pixel **cells**.
3. In each cell, make a 9-bin histogram of **unsigned** orientation (0°–180°), votes weighted by gradient magnitude.
4. Group cells into overlapping 2×2 **blocks** and L2-normalise each block. Blocks overlap, so each cell gets normalised several times.
5. Concatenate everything.

Counting the dimensions for a 64×128 window:
- cells: $64/8 \times 128/8 = 8 \times 16$;
- 2×2 blocks sliding one cell at a time: $7 \times 15 = 105$ blocks;
- each block: $2 \times 2$ cells × 9 bins = 36 numbers;
- total: $105 \times 36 = 3{,}780$.

Without overlap it would be just $8 \times 16 \times 9 = 1{,}152$ numbers. The overlap triples the size but means each cell is normalised against several different neighbourhoods.

**HOG + SVM detector (slide 60):**
1. Slide a fixed-size window over the image.
2. Repeat over an image pyramid to handle scale.
3. Score each window with a linear SVM on its HOG vector.
4. Apply non-maximum suppression to the boxes.

The **Deformable Parts Model** (Felzenszwalb, 2008) added part filters and won PASCAL VOC repeatedly until 2012.

**Why local normalisation matters:** dividing by the block norm cancels any local multiplicative lighting change, so a pedestrian in shade and in sun gets nearly the same descriptor. Modern networks do the same with BatchNorm and LayerNorm, for the same reason.

> [!note] This pipeline returns in object detection
> Sliding window, image pyramid, per-window classifier and NMS are the skeleton of modern detectors too ([[07 - Object Detection I|ch. 07]]). Deep learning replaced the features and the classifier; NMS survived largely unchanged.

### 8. From hand-designed to learned (slides 61–63)

**Every choice in this lecture was a design decision (slide 62):**

| Choice | Who made it | On what basis |
|---|---|---|
| Gaussian kernel, $\sigma$ | you | guess, then look at the output |
| Sobel weights $[1,2,1]$ | Sobel, 1968 | analytic approximation |
| Canny's two thresholds | you | trial and error, per image set |
| Structuring element shape | you | knowledge of the objects |
| SIFT's 4×4×8 layout | Lowe | tuning on a matching benchmark |
| HOG's 8×8 cells, 9 bins | Dalal & Triggs | grid search on pedestrian data |

> [!quote] Slide 62
> "The best hand-designed pipelines were already fitting their parameters to data — just slowly, by hand, a few numbers at a time. Deep learning does the same thing with millions of parameters and gradient descent."

**What carries over to CNNs exactly (slide 63):**
- A conv layer computes the correlation from §3, with a learned kernel $h$.
- Padding, stride and the output-size formula are identical.
- Max-pooling is grayscale dilation.
- 1×1 convolutions are point operations (applied across channels).
- Stacking layers composes filters: $(h_1 * h_2) * I$.

**What changes:**
- Kernels are optimised against a loss, not designed.
- Many kernels per layer and many layers, so small filters build up large receptive fields.
- Nonlinearities between layers, so the stack is not just one big filter.
- Trained first-layer filters look strikingly like oriented edge and blob detectors (Gabor filters). The network rediscovers them.

**Hands-on (slide 67):** implement 2D correlation with loops and check against `cv2.filter2D`; time the separability speed-up; check the semigroup property; Sobel by hand; Canny stage by stage vs `cv2.Canny`; morphology and coin counting; Harris from the structure tensor; SIFT matching with the ratio test; run a 3×3 kernel through `torch.nn.Conv2d` and confirm it matches.

## ✏️ Exercises

> [!example]- Exercise 1 — Output sizes and padding
> **(a)** A 256×256 image is filtered with a 5×5 kernel, padding 2, stride 2. What is the output size?
> **(b)** You want a 4×4 kernel to keep a 32×32 input at 32×32 with stride 1. What padding does the "same" formula ask for, and what's the problem?
> **(c)** A 224×224 input, 3×3 kernel, no padding, stride 2. Output size?
>
> ---
> **(a)** $\lfloor (256 + 4 - 5)/2 \rfloor + 1 = \lfloor 127.5 \rfloor + 1 = 128$. Stride 2 roughly halves the size.
>
> **(b)** $p = (4-1)/2 = 1.5$. You can't pad half a pixel, so you'd have to pad unevenly (1 on one side, 2 on the other), which shifts the output by half a pixel. Odd kernel sizes avoid this, which is why 3×3, 5×5, 7×7 are standard.
>
> **(c)** $\lfloor (224 - 3)/2 \rfloor + 1 = 110 + 1 = 111$. The floor drops the last column/row that doesn't fit.

> [!example]- Exercise 2 — Pick the filter
> For each case, choose a filter and say why.
> **(a)** A scanned document with 5% of pixels randomly set to pure black or white.
> **(b)** A low-light photo with fine grainy noise everywhere, where you don't care about sharp edges.
> **(c)** A portrait with sensor noise where skin should look smooth but the outline of the face must stay sharp.
> **(d)** A 3×3 window contains $\{12, 10, 11, 255, 13, 9, 10, 0, 11\}$. What does a 3×3 box filter output at the centre, and what does a median filter output?
>
> ---
> **(a)** **Median filter.** This is salt-and-pepper noise: a few extreme outliers. The median ignores them; a Gaussian would smear each one into a grey blob.
>
> **(b)** **Gaussian filter.** The noise is roughly Gaussian and spread everywhere. Averaging reduces its variance (by $1/N$ for $N$ independent pixels), and the Gaussian does it without the box filter's ringing and streaks.
>
> **(c)** **Bilateral filter.** It weights neighbours by intensity similarity as well as distance, so it smooths within regions of similar colour but doesn't average across the face outline.
>
> **(d)** Box: the mean, $331/9 \approx 36.8$. The single 255 pulled it far above the typical value of ~11. Median: sorted values are $0, 9, 10, 10, 11, 11, 12, 13, 255$, so the median is **11**. Both outliers (0 and 255) are ignored.

> [!example]- Exercise 3 — Corner, edge or flat?
> Three structure tensors $M$ are measured. Using the Harris response with $k = 0.04$, classify each.
> $$M_A = \begin{bmatrix} 50 & 0 \\ 0 & 48 \end{bmatrix}, \quad M_B = \begin{bmatrix} 90 & 30 \\ 30 & 10 \end{bmatrix}, \quad M_C = \begin{bmatrix} 0.2 & 0.1 \\ 0.1 & 0.3 \end{bmatrix}$$
> Then: if the image is zoomed in 4×, will a corner found in $A$ still be found with the same window size?
>
> ---
> $R = \det M - 0.04 (\operatorname{tr} M)^2$:
> - $A$: $\det = 2400$, $\operatorname{tr} = 98$, $R = 2400 - 384.2 = 2015.8 \gg 0$. **Corner** (both eigenvalues large: 50 and 48).
> - $B$: $\det = 900 - 900 = 0$, $\operatorname{tr} = 100$, $R = -400 < 0$. **Edge.** Its eigenvalues are 100 and 0: lots of gradient, but all in one direction. Large gradient energy alone doesn't make a corner.
> - $C$: $R = 0.05 - 0.04 = 0.04$, tiny. **Flat.**
>
> **Zoom:** probably not. Harris isn't scale-invariant. After a 4× zoom, the corner's curvature is spread over 4× more pixels, so the same small window sees an almost straight edge. You need to search over scales (scale space) or use a scale-invariant detector like SIFT.

> [!example]- Exercise 4 — Canny's hysteresis
> After non-maximum suppression, a chain of connected edge pixels has gradient magnitudes $[120, 60, 70, 40, 130]$ (in order along the chain). Elsewhere there is an isolated pixel with magnitude 80. Thresholds: $\tau_{low} = 50$, $\tau_{high} = 100$.
> **(a)** Which pixels survive?
> **(b)** What would a single threshold of 100 keep? A single threshold of 50?
>
> ---
> **(a)** Strong (> 100): 120 and 130. Weak (50–100): 60, 70 and the isolated 80. Discarded (< 50): 40.
> - 60 is connected to 120 (strong), so keep. 70 is connected to 60, which is connected to 120, so keep.
> - 40 is discarded, so the chain breaks there; 130 survives on its own as a strong pixel.
> - The isolated 80 isn't connected to any strong pixel, so it's discarded.
>
> Result: 120, 60, 70 and 130 survive.
>
> **(b)** Threshold 100: only 120 and 130. The edge is broken into fragments. Threshold 50: 120, 60, 70, 130 *and* the isolated 80, which is probably noise. Hysteresis gets the connected edge without the isolated noise, which is what neither single threshold can do.

> [!example]- Exercise 5 — HOG size and lighting
> **(a)** Compute the HOG descriptor length for a 128×128 window with standard settings (8×8 cells, 2×2 blocks with one-cell stride, 9 bins).
> **(b)** A pedestrian walks from sunlight into shade, so every pixel in their window is multiplied by 0.4. What happens to the gradient magnitudes, and to the final HOG descriptor?
> **(c)** Why can't HOG + SVM tell a shadow edge from an object edge, and how did the field eventually deal with that?
>
> ---
> **(a)** Cells: $16 \times 16$. Blocks: $15 \times 15 = 225$. Each block: $4 \times 9 = 36$. Total $225 \times 36 = 8{,}100$.
>
> **(b)** Gradients are linear in intensity, so every gradient magnitude is multiplied by 0.4. The histograms shrink by 0.4, but each block is L2-normalised, which divides out the factor. The descriptor is (almost) unchanged. That's exactly why HOG normalises locally. (The same lighting change would break a raw-gradient descriptor.)
>
> **(c)** HOG only looks at gradients inside small cells, and a shadow edge and an object edge produce the same local gradient. The information to separate them (what's around, what the object is) isn't in the neighbourhood. Learned features with large receptive fields can use context; CNNs replaced hand-designed descriptors for this reason.

## 📝 Summary

- **Point operations** change each pixel independently (brightness, contrast, gamma, negative, threshold). The **histogram** shows the intensity distribution but no layout; **equalisation** maps through the CDF to spread intensities; **CLAHE** does it per tile with clipping.
- **Linear filtering** is a weighted sum over a neighbourhood with the same kernel everywhere. Convolution = correlation with a flipped kernel. Linear + shift-invariant ⇒ convolution. Output size: $\lfloor (H + 2p - f)/s \rfloor + 1$; "same" padding $p = (f-1)/2$ needs odd $f$.
- **Noise and filters:** Gaussian noise → Gaussian filter; salt & pepper → median; keep edges → bilateral. The box filter rings and isn't isotropic. The Gaussian is isotropic and **separable** ($k^2 \to 2k$), and its variances add when blurring twice.
- **Edges:** derivatives amplify noise, so smooth first (derivative of Gaussian, Sobel, Prewitt, Scharr). The gradient points across the edge; magnitude = strength. The Laplacian gives zero crossings; LoG ≈ DoG.
- **Canny:** smooth → gradient → non-maximum suppression → hysteresis (two thresholds, keep weak pixels only if connected to strong ones).
- **Morphology:** dilation grows, erosion shrinks; opening (erode → dilate) removes specks, closing (dilate → erode) fills holes. Max-pooling = grayscale dilation.
- **Features:** Harris uses the structure tensor $M$, $R = \det M - k(\operatorname{tr} M)^2$ (rotation-invariant, not scale-invariant). SIFT adds scale space (DoG extrema), orientation and a 128-D descriptor; match with the ratio test $d_1/d_2 < 0.8$, then RANSAC. HOG: 8×8 cells, 9 bins, overlapping 2×2 blocks, 3,780-D for 64×128; + linear SVM + NMS was the pre-2012 detector.
- **Hand-designed → learned:** CNNs use the same operations (correlation, padding, stride, pooling) but learn the kernels from data.

## ⚠️ Important Notes

1. **Normalise smoothing kernels to sum to 1** or the image changes brightness. **Derivative kernels must sum to 0** so flat regions give zero response. Quick check: apply the kernel to a constant image.
2. **$\sigma$ is the real parameter of a Gaussian**, not the kernel size. Choose the size from $\sigma$ (about $\pm 3\sigma$).
3. **Blurring twice adds variances, not $\sigma$s.** $\sigma = 3$ then $\sigma = 4$ gives $\sigma = 5$, not 7.
4. **Never differentiate a noisy image without smoothing.** Differentiation amplifies high frequencies; second derivatives (Laplacian) even more.
5. **Sobel $S_x$ responds to vertical edges** (it measures change along $x$). A common exam mix-up.
6. **The bilateral and median filters are not convolutions**, so they don't have separability, the convolution theorem, or shift-invariance.
7. **Gradient magnitude is not lighting-invariant**: it scales with brightness. Descriptors (HOG, SIFT) normalise for that reason.
8. **Local methods can't tell shadow edges from object edges.** No better edge detector can fix that; it needs context.
9. **Harris is rotation-invariant but not scale-invariant.** SIFT adds scale invariance by searching scale space.
10. **The nearest neighbour always exists.** Without the ratio test, every descriptor gets matched to something, including features that don't appear in the other image at all.
11. **Opening ≠ closing.** Opening removes small foreground specks; closing fills small background holes. The order of erode and dilate matters.
12. **`cv2.Canny` needs an 8-bit single-channel image**, and its thresholds depend on image contrast. Values that work on one dataset may fail on another.
13. **CNN "convolution" is really correlation.** For learned kernels it doesn't matter, but if a question asks you to apply a given kernel "as a convolution", flip it first (for non-symmetric kernels like Sobel the sign of the result changes).

> [!warning] Gaps in the source material
> - **Figures lost in extraction:** slides 13–14 (the convolution animation, image-only), 34 (Laplacian vs LoG comparison), 38 (Canny stages), 59 (HOG visualisation), and every example image. Each slide's caption is used where it exists.
> - **Formulas rebuilt from flattened text** and checked numerically: the histogram-equalisation mapping, the output-size formula, separability counts, the semigroup property, the Harris example values, the HOG dimension count.
> - **Added beyond the slides:** the explicit correlation vs convolution formulas (slides 13–14 are images; the summary slide states the flip); the histogram-equalisation worked example; the 13×13 kernel size for $\sigma = 2$; the Harris numerical examples; the HOG dimension derivation (the slide states only "3780-D"); the 128×128 HOG size; all exercises and Important Notes.
> - **RANSAC** is named on slide 56 but not explained in this lecture. It's needed for 3D vision ([[14 - 3D Vision and Emerging Topics|ch. 14]]).

**Previous:** [[01 - Introduction and Image Formation]] · **Next:** [[03 - Image Classification and Linear Models]]
