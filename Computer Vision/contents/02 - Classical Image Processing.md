---
subject: Computer Vision
chapter: 2
tags: [ds, computer-vision, filtering, convolution, edges, canny, sift, hog, morphology, harris]
source: "Nguyen Manh Toan (Swinburne Vietnam), *Computer Vision* Lecture 02 — Classical Image Processing (67 slides); Szeliski 2nd ed. ch. 3, 7"
---

# Classical Image Processing

**Week 2 of 14, and the last chapter with the lecturer's own slides.** Everything from [[03 - Image Classification and Linear Models|ch. 03]] on is built from Szeliski, CS231n and standard practice — see [[00-Index]].

**The lecture answers "why study this in a deep learning course?" in three lines, and they are the right three:**
> **A CNN *is* a stack of learned convolutions — you cannot reason about it without understanding convolution.** Classical methods still run in production (preprocessing, augmentation, video, calibration, annotation). **They are cheap, interpretable, and need no data.**

**Five results.**

**§10 — ⚠️ HOG'S 3,780 DIMENSIONS DERIVE EXACTLY, AND THE OVERLAP IS THE WHOLE POINT.** $105$ blocks $\times\,36$ values $=\mathbf{3{,}780}$ ✓. **The raw cell histograms are only 1,152 numbers — the descriptor is 3.28× larger because every interior cell is normalized four times under four different local contrasts. That redundancy *is* the illumination invariance.**

**§4 — ⚠️ THE SLIDE'S OWN FORMULA IS [[Deep Learning/contents/05 - Convolutional Neural Network|DEEP LEARNING ch. 05]]'S, AND SO IS ITS ODD-KERNEL CONSEQUENCE.** $H_{\text{out}}=\lfloor(H+2p-f)/s\rfloor+1$ with "same" padding $p=(f-1)/2$ — **an integer only for odd $f$.** *The same conclusion reached from the classical side and the CNN side independently.*

**§6 — ⚠️ THE MEDIAN'S BREAKDOWN POINT IS 50% AND THE MEAN'S IS 0%.** With **4 of 9 pixels corrupted** the mean moves **+53.1** and the median **+0.0**. And on a single impulse, **a Gaussian contaminates 3 pixels where there was 1; the median deletes it.**

**§7 — ⚠️ SOBEL IS AN OUTER PRODUCT, AND SEPARABILITY IS A REAL SAVING THAT GROWS.** $[1,2,1]^\top[-1,0,1]$ reproduces $S_x$ exactly. **$k^2\to2k$ multiplications: 1.5× at $k=3$, 7.5× at $k=15$.**

**§8 — ⚠️ THE LoG FORMULA IS SYMBOLICALLY EXACT AND THE DoG APPROXIMATION IS ONLY GOOD NEAR $k=1$.** $\nabla^2G_\sigma-\frac{x^2+y^2-2\sigma^2}{\sigma^4}G_\sigma=\mathbf 0$ identically. **But the DoG/LoG ratio is 0.868 at $k=1.1$ and 0.375 at $k=2$** — which is why SIFT uses $k$ close to 1.

## 📘 Main Knowledge

### 1. Where these operators come from

The lecture's timeline places everything in **1963–2005**:

| | |
|---|---|
| 1920 | Bartlane cable, **5 grey levels** |
| 1957 | first digital image (Kirsch) |
| 1963 | **Roberts** — first edge operator |
| 1964 | Ranger 7 — JPL corrects lens distortion on an IBM 7094 |
| 1968 | **Sobel** — still in `cv2` |
| 1971 | CT scanner (Hounsfield) |
| 1980–83 | **LoG; morphology; image pyramids** |
| 1986–88 | **Canny; Harris & Stephens** |
| 1992 | JPEG |
| 1999–2005 | **SIFT; HOG** |
| **2012** | **AlexNet** |

> [!note] **"In 2012 AlexNet ended the era — but not the operators."**
> The right framing. **Sobel, Canny, the median filter and morphology are all still shipped**, and the through-line the lecture states holds for CNNs too:
> 1. **a filter is a small matrix slid over the image**
> 2. **smoothing suppresses noise; differencing finds structure**
> 3. **good features are *invariant* to nuisance changes**

### 2. Point operations and histograms

**A point operation depends only on the pixel underneath**: $J(m,n)=f\big(I(m,n)\big)$.

| | |
|---|---|
| brightness | $f(v)=v+b$ |
| contrast | $f(v)=av$ |
| gamma | $f(v)=v^\gamma$ on $v\in[0,1]$ |
| negative | $f(v)=255-v$ |
| threshold | $f(v)=\mathbb 1[v>\tau]$ |

**"No spatial information. Everything interesting needs a neighbourhood"** — which is §3 onward.

**The histogram** counts $h(v)=|\{(m,n):I(m,n)=v\}|$, then normalizes.

> [!warning] ⚠️ A histogram discards *all* spatial layout
> **"Two very different images can share a histogram."** ⇒ *a histogram is a bag-of-pixels representation, and it fails for exactly the reason bag-of-words fails in text: order carries meaning.* It is still the basis of **Otsu thresholding, histogram matching and equalization**, because exposure is genuinely a per-pixel property.

**Histogram equalization** spreads intensities toward uniform using the CDF:
$$c(v)=\sum_{u\le v}p(u),\qquad J=\lfloor 255\,c(I)\rfloor$$

> [!note] ⚠️ Why this works is the **probability integral transform**
> **If $V$ has CDF $c$, then $c(V)\sim\mathrm{Uniform}[0,1]$** — a standard result from [[Probability Theory/contents/05 - Continuous Random Variables|Probability Theory ch. 05]], used here as an image operation. *Applying a random variable's own CDF to it always uniformizes it.*
>
> **Two caveats the lecture supplies:** the global version **amplifies noise in flat regions** (a nearly-constant patch gets stretched across the full range), and the fix is **CLAHE** — equalize in tiles, **clip** the histogram, interpolate between tiles.

### 3. Linear filtering, and the theorem that justifies CNNs

**A linear filter replaces each pixel by a weighted sum of its neighbours, with the same weights at every position — making the operation shift-invariant.**

| property | |
|---|---|
| **linearity** | $h*(\alpha I_1+\beta I_2)=\alpha(h*I_1)+\beta(h*I_2)$ |
| **shift equivariance** | shift the input, the output shifts identically |
| **identity** | the delta kernel $\delta$ leaves $I$ unchanged |
| **convolution theorem** | $\mathcal F\{h*I\}=\mathcal F\{h\}\cdot\mathcal F\{I\}$ |

> [!warning] ⚠️ **"Linear + shift-invariant ⇒ the operation *is* a convolution. There is no other choice."**
> That is a **theorem, not a design preference**, and the lecture states its consequence exactly: *"That is the theoretical justification for convolutional layers: we want translation equivariance."*
>
> ⇒ **[[Deep Learning/contents/05 - Convolutional Neural Network|Deep Learning ch. 05]] §1 derived the convolution by *imposing* translation invariance and locality on an MLP and measured the payoff at $10^{10}$ parameters.** This lecture arrives at the same object from the opposite direction: **assume linearity and shift-invariance, and convolution is forced.** *Two independent routes to one operator is worth more than either.*
>
> **And the frequency reading is the useful one**: convolution in space **is** multiplication in frequency, so **smoothing kernels keep low frequencies and derivative kernels keep high ones.** Every filter in this chapter is one or the other.

### 4. ⚠️ Borders and output size — the CNN formula, already here

The window falls off the grid. Four choices: **zero** (introduces a dark rim), **replicate**, **reflect**, **wrap** (toroidal — what the FFT assumes).

$$\boxed{H_{\text{out}}=\left\lfloor\frac{H+2p-f}{s}\right\rfloor+1}$$

**Verified:** $H=224,f=3,p=1,s=1\to224$; $f=5,p=2\to224$; $f=3,p=1,s=2\to112$; $f=7,p=3,s=2\to112$.

> [!warning] ⚠️ "Same" padding is $p=(f-1)/2$ — an integer **only for odd $f$**
> | $f$ | $p=(f-1)/2$ | |
> |---|---|---|
> | 3 | 1.0 | ✓ |
> | **4** | **1.5** | ✗ |
> | 5 | 2.0 | ✓ |
> | 7 | 3.0 | ✓ |
>
> ⇒ **exactly [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §3's odd-kernel argument, reached independently from the classical-filtering side.** The lecture's own note — *"Same formula you will use for every CNN layer"* — is the point: **there is no separate CNN arithmetic.**
>
> **And the border choice is not cosmetic**: zero-padding tells the network there is darkness outside the frame, which is *false*, and is how CNNs learn to detect image boundaries. **Reflect is the safest default for classical filtering; zero is the CNN convention** for reasons of speed, as [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §3 records.

### 5. Smoothing

**A Gaussian is the standard smoother** — separable, rotationally symmetric, and the unique kernel that introduces no new extrema when scale increases (the basis of scale space, §8).

**A box filter** is cheaper and worse: not isotropic, and its frequency response rings.

### 6. ⚠️ The median filter, and a robustness result

The median is **not linear and not a convolution** — it is an **order statistic**.

> [!warning] ⚠️ THE MEAN'S BREAKDOWN POINT IS 0%; THE MEDIAN'S IS 50%
> A 9-pixel patch $[128,130,\dots,137]$, corrupting the largest values to 255:
>
> | corrupted | mean | shift | median | shift |
> |---|---|---|---|---|
> | 0 | 132.889 | — | 133.000 | — |
> | 1 (11%) | 146.000 | **+13.1** | 133.000 | **+0.0** |
> | 2 (22%) | 159.222 | **+26.3** | 133.000 | **+0.0** |
> | **4 (44%)** | **186.000** | **+53.1** | **133.000** | **+0.0** |
> | 5 (56%) | 199.556 | +66.7 | **255.000** | **+122.0** ⚠️ |
>
> **A single outlier moves the mean by 13.1. Four move it by 53.1 and the median by nothing at all — until 5 of 9, when the median breaks completely.**
>
> ⇒ **that discontinuity is what "breakdown point" means: the median is perfect up to 50% contamination and useless past it.**

> [!warning] ⚠️ And the two filters fail in *different ways*, not by different amounts
> A single impulse $[0,0,0,0,255,0,0,0,0]$:
>
> | | result | contaminated pixels |
> |---|---|---|
> | 3-tap Gaussian $\frac14[1,2,1]$ | $[0,0,0,63.8,\mathbf{127.5},63.8,0,0,0]$ | **1 → 3** |
> | 3-tap median | $[0,0,0,0,\mathbf 0,0,0,0,0]$ | **1 → 0** |
>
> ⇒ ***a Gaussian SPREADS each impulse over the kernel; the median DELETES it.*** Salt-and-pepper noise is impulsive, so the median wins; Gaussian sensor noise is not, so the Gaussian wins. **Choose by the noise model, not by reputation.**
>
> **The cost the slide states, checked at 1920×1080:** naive $O(HWk^2\log k)$ vs histogram-based $O(HWk)$ — **4.8× at $k=3$, 58.6× at $k=15$.** *The naive implementation is what makes people think the median is slow.*

**The bilateral filter** weights neighbours by **both** spatial distance and intensity difference:
$$J(p)=\frac1{W_p}\sum_{q\in N(p)}\underbrace{G_{\sigma_s}(\|p-q\|)}_{\text{spatial}}\underbrace{G_{\sigma_r}(|I(p)-I(q)|)}_{\text{range}}I(q)$$

> [!note] ⚠️ It is **not shift-invariant and not a convolution**, and the lecture says so
> **Across an edge $|I(p)-I(q)|$ is large ⇒ weight ≈ 0 ⇒ the edge survives.** Within a flat region it behaves like a Gaussian.
>
> **Because the weights depend on the image, §3's theorem does not apply** — that is precisely the price of edge preservation. *"Overdone, it produces the 'plastic skin' look of phone beauty filters."*

### 7. ⚠️ Gradients and edges

**An edge is a rapid change in intensity, and four different physical causes produce identical pixels:**

| cause | |
|---|---|
| **depth discontinuity** | an object boundary |
| **surface orientation** | a fold |
| **reflectance** | paint, texture |
| **illumination** | a shadow |

> [!warning] ⚠️ **"A shadow edge and an object edge look identical locally — a permanent limitation of purely local methods."**
> ⇒ *no edge detector can be fixed to solve this*, because the information is not in the neighbourhood. **It needs global reasoning or learning** — which is one concrete answer to "why deep learning": [[07 - Object Detection I|later chapters]] resolve shadow-vs-object using context an operator cannot see.

**Discrete derivatives.** Forward difference $I(x+1)-I(x)$; **central difference** $\frac{I(x+1)-I(x-1)}{2}$ — symmetric and second-order accurate, and a convolution with $h_x=\frac12[-1,0,1]$.

> [!warning] ⚠️ Differentiation amplifies noise, and the fix is one identity
> **Noise is high-frequency; differentiation multiplies each frequency by $\omega$**, so noise is amplified more than signal. The solution:
> $$\frac{d}{dx}(g_\sigma*I)=\left(\frac{dg_\sigma}{dx}\right)*I$$
> **One convolution with the derivative-of-Gaussian kernel** instead of two passes.
> $$\frac{\partial G_\sigma}{\partial x}=-\frac{x}{\sigma^2}G_\sigma$$
> **Antisymmetric — it sums to zero, so flat regions give no response** — and **separable**: $\partial_xG_\sigma=g'_\sigma(x)g_\sigma(y)$.
>
> ⇒ **$\sigma$ selects *which* edges**: small $\sigma$ finds texture, large $\sigma$ finds only major boundaries. **"There is no single correct $\sigma$ — 'edge' is scale-dependent."** *That observation leads directly to scale space (§8).*

**Sobel and Prewitt** smooth along one axis and difference along the other, in one $3\times3$:

$$S_x=\begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix}=\begin{pmatrix}1\\2\\1\end{pmatrix}\begin{pmatrix}-1&0&1\end{pmatrix},\qquad S_y=S_x^\top$$

**Verified exactly as an outer product.** ⚠️ **And separability is a real and growing saving:**

| $k$ | 2-D mults/px | separable | speedup |
|---|---|---|---|
| 3 | 9 | 6 | **1.5×** |
| 7 | 49 | 14 | 3.5× |
| 15 | 225 | 30 | **7.5×** |

**Gaussian, box, Sobel, Prewitt and derivative-of-Gaussian are all separable; the bilateral filter is not.**

**The smoothing row is the only difference between the operators:**

| | smoothing weights | centre weight |
|---|---|---|
| **Prewitt** $[1,1,1]$ | $[0.333,0.333,0.333]$ | 33.3% — box, noisier |
| **Sobel** $[1,2,1]$ | $[0.25,0.5,0.25]$ | 50.0% |
| **Scharr** $[3,10,3]$ | $[0.1875,0.625,0.1875]$ | **62.5%** — better rotation invariance |

**Gradient magnitude and orientation:**
$$\|\nabla I\|=\sqrt{I_x^2+I_y^2},\qquad\theta=\operatorname{atan2}(I_y,I_x)$$
$\nabla I$ **points in the direction of steepest intensity increase — perpendicular to the edge.**

> [!note] ⚠️ Magnitude is **not** illumination-invariant
> **Under $I\to aI$ the magnitude scales by $a$** — *"hence the normalization steps in HOG and SIFT."* **That single sentence explains a design choice in both descriptors (§10), and it is the reason raw gradient magnitude is never used as a feature directly.**

**The Laplacian** $\nabla^2I=\partial_{xx}I+\partial_{yy}I\approx\begin{pmatrix}0&1&0\\1&-4&1\\0&1&0\end{pmatrix}*I$: **edges become zero crossings, not peaks**, so they localize to sub-pixel precision; **rotationally symmetric** (one filter, no orientation) but it **loses direction**, and it is **extremely noise-sensitive because second derivatives amplify $\omega^2$.**

> [!note] ⚠️ A kernel sanity check worth internalizing
> | kernel | sum | meaning |
> |---|---|---|
> | central difference, Sobel, Laplacian | **0** | no response on flat regions |
> | box, Gaussian (normalized) | **1** | preserves brightness |
>
> **Verified on a constant image**: the Laplacian returns max $|{\cdot}|=0$; the Gaussian returns the input value exactly. ⇒ ***a derivative kernel must sum to 0 and a smoothing kernel to 1 — an instant check on any kernel you write.***

### 8. ⚠️ LoG, DoG, and scale

$$\nabla^2G_\sigma(x,y)=\frac{x^2+y^2-2\sigma^2}{\sigma^4}G_\sigma(x,y)\quad\text{(the "Mexican hat")}$$

**Verified symbolically: $\nabla^2G_\sigma$ minus the claimed form simplifies to exactly 0.**

$$G_{k\sigma}-G_\sigma\approx(k-1)\sigma^2\nabla^2G_\sigma$$

> [!warning] ⚠️ The DoG approximation is good only near $k=1$, and the numbers say by how much
> | $k$ | $\max\|\mathrm{DoG}\|\ /\ \max\|(k-1)\sigma^2\mathrm{LoG}\|$ |
> |---|---|
> | 1.1 | **0.868** |
> | 1.2 | 0.764 |
> | 1.6 | 0.508 |
> | 2.0 | **0.375** |
>
> **At $k=2$ the approximation is off by a factor of 2.7.** ⇒ **SIFT uses $k=2^{1/s}$ per octave — deliberately close to 1** — and this is why.
>
> **And the reason to bother**: DoG is **two separable Gaussian blurs** instead of one non-separable LoG convolution — **2.2× fewer multiplications at $9\times9$, 6.2× at $25\times25$.**

### 9. Canny (1986) — still the default, 40 years on

**Canny asked what an *optimal* edge detector should satisfy:**
1. **good detection** — find real edges, few false positives
2. **good localization** — report the edge where it actually is
3. **single response** — one detection per edge, not a thick band

**Four stages:** smooth with $G_\sigma$ → compute $\|\nabla I\|$ and $\theta$ → **non-maximum suppression along $\theta$** → **hysteresis thresholding** with $\tau_{\text{low}},\tau_{\text{high}}$.

> [!note] ⚠️ Stages 3 and 4 each solve one of the three criteria
> **Non-maximum suppression** delivers criterion 3: the gradient magnitude is a **ridge several pixels wide**, so round $\theta$ to one of $0°,45°,90°,135°$, compare with the two neighbours **across** the edge, and keep only local maxima.
>
> **Hysteresis** solves the detection/false-positive trade-off in criterion 1: *"A single threshold forces a bad trade-off — too high and edges break into fragments; too low and noise floods in."* **Two thresholds: keep strong pixels, discard weak ones, and keep in-between pixels *only if connected to a strong one*.**
>
> ⇒ ***hysteresis is the only step in the whole pipeline that is not local*** — connectivity is a global property, and it is exactly what makes Canny work where a plain threshold does not.

### 10. ⚠️ Corners, and the descriptors that made matching work

**Edges are not enough to match two images**, and the lecture's three-case argument is the cleanest statement of why:

| region | shift the window | |
|---|---|---|
| **flat** | nothing changes in any direction | no information |
| **edge** | nothing changes *along* the edge | **the aperture problem** — position along the edge is unknown |
| **corner** | changes in **every** direction | **uniquely localizable** |

**Harris** measures it: $E(u,v)=\sum_{x,y}w(x,y)\big[I(x+u,y+v)-I(x,y)\big]^2$, and a first-order Taylor expansion gives

$$E(u,v)\approx\begin{pmatrix}u&v\end{pmatrix}\mathbf M\begin{pmatrix}u\\v\end{pmatrix},\qquad \mathbf M=\sum_{x,y}w(x,y)\begin{pmatrix}I_x^2&I_xI_y\\I_xI_y&I_y^2\end{pmatrix}$$

**$\mathbf M$ is the structure tensor** — symmetric positive semi-definite, so its eigenvalues are real and non-negative, and **both large means a corner.** *(The weight $w$ is normally a Gaussian, making each entry a blurred product of derivatives; a box window is simpler but not isotropic.)*

**SIFT (1999)** — four stages, each solving one invariance:

| stage | what it buys |
|---|---|
| 1. DoG extrema across scales | **scale** invariance |
| 2. sub-pixel refinement, reject low contrast and edges | localization |
| 3. **36-bin orientation histogram** (10° per bin), dominant peak = canonical orientation; peaks within **80%** spawn extra keypoints | **rotation** invariance |
| 4. $16\times16$ patch → $4\times4$ cells → 8-bin histogram each → **$4\times4\times8=128$ dims**, then normalize, **clip at 0.2**, renormalize | **illumination** invariance |

> [!note] ⚠️ The clip at 0.2 is a bounded-influence estimator
> A specular highlight produces one enormous gradient that would dominate the unit vector. **Clipping caps any single bin at 20% of the norm; renormalizing restores unit length.** ⇒ *the same idea as gradient clipping in [[Deep Learning/contents/07 - Recurrent Neural Network|DL ch. 07]] §8 — bound one component's influence, accept the bias.*

**Lowe's ratio test**: accept a match only if $d_1/d_2<0.8$.

> [!warning] ⚠️ Why a ratio and not a distance — *"a nearest neighbour always exists, even for a wrong match"*
> **A distinctive feature has $d_1\ll d_2$; an ambiguous one (repeated texture — brick, windows, foliage) does not.** ⇒ ***the test measures distinctiveness, not similarity***, which is the only thing that can distinguish "this is the match" from "this is the least-bad of many equally poor candidates." **Then RANSAC fits a geometric model and discards the rest.**

**The family:** SIFT (1999, 128-D float, patent expired 2020), SURF (2006, 64-D, box filters + integral images), **ORB (2011, 256-bit binary, FAST + rotated BRIEF, free, real-time, used in ORB-SLAM)**, BRISK/FREAK, **SuperPoint (2018, 256-D learned, CNN, self-supervised)**.

> [!note] ⚠️ **"Structure-from-motion, SLAM, panorama stitching and image registration are dominated by these methods — geometry is a domain where hand-designed features remain competitive."**
> **A genuine exception to the deep-learning sweep, and the lecture is right to flag it.** *Geometry has exact constraints (epipolar, projective) that a learned feature cannot improve on; what it can improve is repeatability, which is what SuperPoint targets.*

**HOG (2005)** — **dense**, for whole objects rather than sparse keypoints. Dalal & Triggs, for pedestrian detection:
1. compute $I_x,I_y$ with plain $[-1,0,1]$, **no smoothing**
2. divide into **$8\times8$ pixel cells**
3. per cell, a **9-bin histogram of *unsigned* orientation (0°–180°)**, votes weighted by magnitude
4. group cells into **$2\times2$ blocks** and **L2-normalize each block — blocks overlap, so each cell is normalized several times**
5. concatenate: a $64\times128$ window → **3,780-D**

> [!warning] ⚠️ THE 3,780 DERIVES EXACTLY, AND THE OVERLAP IS WHERE IT COMES FROM
> | | |
> |---|---|
> | cells across the window | $8\times16=128$ |
> | blocks, stride 1 cell, overlapping | $(8-2+1)\times(16-2+1)=7\times15=\mathbf{105}$ |
> | values per block | $2\times2\times9=36$ |
> | **total** | $105\times36=\mathbf{3{,}780}$ ✓ |
>
> **The raw cell histograms are only $128\times9=1{,}152$ numbers.** ⇒ **the descriptor is 3.28× larger than the data it summarizes**, and *without* overlap it would be $4\times8=32$ blocks $=1{,}152$ dims — exactly the raw count.
>
> **How many times is each cell normalized?** corner **1**, edge **2**, **interior 4**.
>
> ⇒ ***the redundancy IS the illumination invariance*** — an interior cell appears four times, each normalized against a different local contrast, so no single lighting estimate has to be right. **That is what the 3.28× buys, and it is why HOG uses unsigned orientation too: a dark-on-light and light-on-dark edge are the same structure.**

**HOG + linear SVM was the pre-deep-learning detector:** slide a fixed window, repeat over an **image pyramid** for scale, score each window, **non-maximum suppression on the boxes.**

> [!note] ⚠️ That pipeline is [[Deep Learning/contents/06 - Object Detection|DL ch. 06]]'s, with the learned parts removed
> **Sliding window → anchors. Image pyramid → the feature pyramid. SVM score → the classification head. NMS → still NMS, unchanged.** ⇒ ***modern detection kept the scaffolding and replaced the features*** — exactly the "delete a hand-designed stage" pattern recorded in DL ch. 06 §9. **NMS is the one component that survived both eras intact.**

## ✏️ Exercises

> [!example]- Exercise 1 — derive HOG's dimension
> A $64\times128$ window, $8\times8$ cells, 9 bins, $2\times2$ blocks with stride 1 cell.
> **(a)** How many cells, blocks, and dimensions? **(b)** What would it be without overlap? **(c)** How many times is an interior cell normalized, and why does that matter?
>
> ---
> **(a)** Cells: $\frac{64}{8}\times\frac{128}{8}=8\times16=\mathbf{128}$. Blocks: $(8-2+1)\times(16-2+1)=7\times15=\mathbf{105}$. Each block holds $2\times2\times9=36$ values, so $105\times36=\mathbf{3{,}780}$ ✓ — the slide's figure exactly.
>
> **(b)** Non-overlapping: $4\times8=32$ blocks $\times36=\mathbf{1{,}152}$ — **identical to the raw cell histogram count** ($128\times9$), because without overlap each cell appears once. **The overlap costs 3.28×.**
>
> **(c)** **Corner cells once, edge cells twice, interior cells four times.** ⚠️ **Each appearance is normalized against a different $2\times2$ neighbourhood, so the descriptor never has to commit to one estimate of local illumination.** ⇒ *the redundancy is the invariance* — and it is why HOG survived until CNNs learned the same trick with overlapping receptive fields.

> [!example]- Exercise 2 — check a kernel before you use it
> **(a)** What must a derivative kernel sum to? A smoothing kernel? **(b)** Check $[-1,0,1]/2$, Sobel $S_x$, the Laplacian, and a normalized $3\times3$ Gaussian. **(c)** Show Sobel is separable and cost the saving at $k=3$ and $k=15$.
>
> ---
> **(a)** A **derivative** kernel must sum to **0** — otherwise a constant image produces a non-zero response, which is a derivative that is not zero on a flat region. A **smoothing** kernel must sum to **1** — otherwise it rescales brightness.
>
> **(b)** $[-1,0,1]/2\to\mathbf 0$; $S_x\to\mathbf 0$; Laplacian $\to\mathbf 0$; Gaussian $\frac1{16}\begin{psmallmatrix}1&2&1\\2&4&2\\1&2&1\end{psmallmatrix}\to\mathbf 1$. **Verified on a constant image of 100: the Laplacian returns 0 to machine precision, the Gaussian returns 100.0000.**
>
> **(c)** $\begin{pmatrix}1\\2\\1\end{pmatrix}\begin{pmatrix}-1&0&1\end{pmatrix}=\begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix}=S_x$ ✓. Cost $k^2\to2k$: **9 → 6 (1.5×) at $k=3$; 225 → 30 (7.5×) at $k=15$.** ⚠️ *The saving is negligible for tiny kernels and decisive for large ones — which is why a $15\times15$ Gaussian blur is cheap and a $15\times15$ bilateral filter is not.*

> [!example]- Exercise 3 — median versus Gaussian
> **(a)** On $[128,130,131,132,133,134,135,136,137]$, corrupt 1, 2, 4 and 5 values to 255. Track mean and median. **(b)** What is the breakdown point? **(c)** Filter a single impulse with each. **(d)** When should you *not* use a median?
>
> ---
> **(a)**
>
> | corrupted | mean | median |
> |---|---|---|
> | 0 | 132.889 | 133.000 |
> | 1 | 146.000 (**+13.1**) | 133.000 (**+0.0**) |
> | 2 | 159.222 (+26.3) | 133.000 (+0.0) |
> | **4 (44%)** | 186.000 (**+53.1**) | 133.000 (**+0.0**) |
> | 5 (56%) | 199.556 (+66.7) | **255.000 (+122.0)** |
>
> **(b)** **Mean 0%, median 50%.** The median is *exactly* unaffected up to 4 of 9 and then fails completely at 5 — **breakdown is a cliff, not a slope.**
>
> **(c)** Impulse $[0,0,0,0,255,0,0,0,0]$: the $\frac14[1,2,1]$ Gaussian gives $[0,0,0,63.8,127.5,63.8,0,0,0]$ — **1 contaminated pixel becomes 3**; the median gives **all zeros — the impulse is deleted.**
>
> **(d)** ⚠️ **When the noise is not impulsive.** For Gaussian sensor noise the mean is the maximum-likelihood estimate and the median is less efficient. **The median also destroys fine texture and rounds corners**, because it is a rank operation with no notion of structure. ⇒ *match the filter to the noise model.*

> [!example]- Exercise 4 — output sizes and odd kernels
> **(a)** $H=224$: give $H_\text{out}$ for $(f,p,s)=(3,1,1),(5,2,1),(3,1,2),(7,3,2)$. **(b)** Which preserve size? **(c)** Why are CNN kernels odd?
>
> ---
> **(a)** $\lfloor(H+2p-f)/s\rfloor+1$: **224, 224, 112, 112.**
>
> **(b)** The first two. **"Same" padding is $p=(f-1)/2$** — $p=1$ for $f=3$, $p=2$ for $f=5$ — and any stride $>1$ downsamples regardless of padding.
>
> **(c)** $p=(f-1)/2$ is an integer **only for odd $f$**: $f=4$ needs $p=1.5$. With even $f$ you must pad asymmetrically, so the output at $[i,j]$ is **no longer the window centred on the input at $[i,j]$**. ⚠️ **This is the same conclusion as [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §3, reached from classical filtering instead of from CNN design** — and the fact that both routes agree is the point.

> [!example]- Exercise 5 — LoG, DoG and the cost of scale
> **(a)** Verify $\nabla^2G_\sigma=\frac{x^2+y^2-2\sigma^2}{\sigma^4}G_\sigma$. **(b)** How good is $G_{k\sigma}-G_\sigma\approx(k-1)\sigma^2\nabla^2G_\sigma$ at $k=1.1$ and $k=2$? **(c)** Why use DoG at all? **(d)** What does $\sigma$ control?
>
> ---
> **(a)** Symbolic differentiation of $G_\sigma=\frac{1}{2\pi\sigma^2}e^{-(x^2+y^2)/2\sigma^2}$ gives $\partial_{xx}G+\partial_{yy}G$ **minus the claimed form $=0$ identically.** ✓
>
> **(b)** Ratio of maxima: **0.868 at $k=1.1$**, 0.764 at 1.2, 0.508 at 1.6, **0.375 at $k=2$.** ⚠️ **At $k=2$ the approximation is off by a factor of 2.7** — SIFT uses $k=2^{1/s}$ per octave precisely to stay near 1.
>
> **(c)** **DoG is two separable Gaussian blurs; LoG is one non-separable convolution.** At $9\times9$: 81 mults/px vs $4\times9=36$ — **2.2×**; at $25\times25$, **6.2×**. And the Gaussians are needed for the scale pyramid anyway, so the DoG is nearly free.
>
> **(d)** ⚠️ **$\sigma$ selects which edges exist.** Small $\sigma$ responds to texture and fine detail; large $\sigma$ only to major boundaries. **"There is no single correct $\sigma$ — 'edge' is scale-dependent."** ⇒ *this is why detectors search across scales rather than picking one, and it is the same argument that produces the feature pyramid in [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §6.*

## 📝 Summary

- **Classical methods earn their place in a deep-learning course for three reasons the lecture states**: a CNN *is* a stack of learned convolutions; these operators still run in production; they are cheap, interpretable and need no data.
- **Point operations have no spatial information**; histograms discard **all** spatial layout, so **two very different images can share one**. **Histogram equalization works by the probability integral transform** — $c(V)\sim\mathrm{Uniform}$ — and **amplifies noise in flat regions**, which CLAHE fixes by tiling and clipping.
- **⚠️ Linear + shift-invariant ⇒ convolution. There is no other choice** — a theorem, and the justification for convolutional layers. **[[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] derived the same operator by imposing invariance on an MLP; two independent routes to one object.**
- **⚠️ $H_\text{out}=\lfloor(H+2p-f)/s\rfloor+1$ and "same" padding $p=(f-1)/2$ is an integer only for odd $f$** — DL ch. 05's odd-kernel argument, from the classical side.
- **⚠️ The mean's breakdown point is 0% and the median's is 50%**: with 4 of 9 pixels corrupted the mean moves **+53.1** and the median **+0.0**, then the median fails completely at 5 of 9. **And a Gaussian spreads one impulse to 3 pixels where the median deletes it** — different failure modes, so choose by the noise model.
- **The bilateral filter preserves edges by weighting on intensity as well as distance — and is therefore not shift-invariant and not a convolution.** That is the price, not a bug.
- **Four physically different causes produce identical edge pixels** (depth, orientation, reflectance, illumination) — **"a shadow edge and an object edge look identical locally, a permanent limitation of purely local methods."**
- **⚠️ Differentiation amplifies noise by $\omega$ (and the Laplacian by $\omega^2$), so smooth first** — and $\frac{d}{dx}(g_\sigma*I)=g'_\sigma*I$ makes it one convolution. **Derivative kernels sum to 0, smoothing kernels to 1 — an instant sanity check.**
- **⚠️ Sobel is the outer product $[1,2,1]^\top[-1,0,1]$**, and separability saves $k^2\to2k$: **1.5× at $k=3$, 7.5× at $k=15$.** Prewitt/Sobel/Scharr differ only in the smoothing row (33.3% / 50% / **62.5%** centre weight).
- **⚠️ $\nabla^2G_\sigma=\frac{x^2+y^2-2\sigma^2}{\sigma^4}G_\sigma$ verified symbolically; the DoG approximation is 0.868 accurate at $k=1.1$ and only 0.375 at $k=2$** — which is why SIFT keeps $k$ near 1. **DoG is 2.2–6.2× cheaper than LoG.**
- **Canny's three criteria map onto its stages**: non-maximum suppression gives single response, **hysteresis is the only non-local step** and is what beats a single threshold.
- **Flat / edge / corner**: only a corner is uniquely localizable; an edge suffers the **aperture problem**. **Harris's structure tensor $\mathbf M$ is symmetric PSD and both eigenvalues large means corner.**
- **⚠️ HOG's 3,780 dimensions derive exactly** ($105\times36$), and **the raw histograms are only 1,152** — the 3.28× is overlap, with **interior cells normalized four times**. ***The redundancy is the illumination invariance.***
- **SIFT's 128 = $4\times4\times8$**, with 36 orientation bins, an 80% peak rule, and a **clip at 0.2** that is a bounded-influence estimator. **Lowe's ratio test $d_1/d_2<0.8$ measures distinctiveness, not similarity**, because "a nearest neighbour always exists, even for a wrong match."
- **HOG + SVM + pyramid + NMS is [[Deep Learning/contents/06 - Object Detection|DL ch. 06]]'s pipeline with the learned parts removed** — and **NMS is the one component that survived both eras unchanged.**

## ⚠️ Important Notes

1. **⚠️ Check every kernel's sum before using it.** Derivative → 0, smoothing → 1. A kernel that fails this produces a plausible-looking image with the wrong brightness or a non-zero response on flat regions — **the vault's recurring silent failure.**
2. **⚠️ Border handling changes your results and is easy to forget.** Zero-padding puts a dark rim on every filtered image and teaches CNNs where the image boundary is. **Reflect is the safe classical default.**
3. **⚠️ The median is not a convolution and the bilateral filter is not either.** Neither can be folded into a linear pipeline, neither commutes with other filters, and neither has a frequency response. **Only linear shift-invariant operations get §3's guarantees.**
4. **⚠️ "Denoising" with a median destroys texture.** It removes impulses *and* fine structure, and rounds corners. On Gaussian noise it is strictly worse than a Gaussian.
5. **⚠️ There is no correct $\sigma$.** Edge detection at one scale answers one question. **If a detector misses large boundaries or drowns in texture, the fix is usually $\sigma$, not the operator.**
6. **⚠️ Gradient magnitude scales with illumination** ($I\to aI$ gives $\|\nabla I\|\to a\|\nabla I\|$). **Never use it as a feature without normalization** — the reason both HOG and SIFT normalize.
7. **⚠️ A shadow edge and an object edge are locally identical.** No local operator can separate them; if your pipeline confuses them, the answer is context or learning, not a better filter.
8. **⚠️ Canny's two thresholds are not independent.** A common ratio is $\tau_{\text{high}}/\tau_{\text{low}}\approx2$–3. Setting them equal throws away hysteresis and reduces Canny to a thresholded gradient.
9. **⚠️ Lowe's ratio test rejects, it does not rank.** Matches surviving it are still wrong sometimes — **RANSAC is not optional**, it is the second half of the method.
10. **⚠️ Descriptor invariances are earned stage by stage, and each can be broken.** SIFT is invariant to scale, rotation and affine illumination — **not to perspective, non-rigid deformation, or large viewpoint change.** Know which invariance you actually need.
11. **⚠️ Overlapping normalization is why HOG is 3.28× its own data.** If you implement it and get 1,152 dimensions, you forgot the overlap; if you get 3,780, you did not.
12. **Hand-designed features are still competitive in geometry** — SfM, SLAM, stitching, registration — because those problems have exact constraints that learning cannot improve. **"Deep learning won" is a claim about recognition, not about all of vision.**
13. **The classical pipeline is the modern one with the learned parts removed.** Sliding window → anchors; pyramid → feature pyramid; SVM → classification head; **NMS → NMS.** Recognizing that makes [[07 - Object Detection I|ch. 07]] much shorter.

> [!warning] Gaps in the source material
> **This is the second and last chapter with the lecturer's own slides** (67 of them). **[[03 - Image Classification and Linear Models|Ch. 03]] onward has none** — see [[00-Index]].
>
> **All slide figures are images and never extract.** **Recovered because the captions state their content**: the negative example (slide 8), the histogram and its image (9), the low-contrast → equalized → CLAHE comparison (10), the padding comparison (16), salt-and-pepper vs Gaussian vs median (23), noisy/Gaussian/bilateral (24), the intensity profile with its first and second derivatives (26), the raw-derivative vs derivative-of-Gaussian comparison (28), $g_\sigma,g'_\sigma,g''_\sigma$ (29), $I_x$/$I_y$/$\|\nabla I\|$ (30), the LoG and DoG profiles (33), thick ridge → thin edge (36), the flat/edge/corner triptych (47), matched features after the ratio test (56), and HOG cells (58). **Genuinely lost**: the history timeline's graphics (6), the convolution animations (13–14), the morphology examples (38–45), the orientation-as-hue visualization (31), and the Laplacian-vs-LoG comparison (34).
>
> **Beamer extraction quirks** (recorded in this subject's `CLAUDE.md`): **formulas lose their spaces and fractions flatten** — the output-size formula, the bilateral filter, the LoG and the structure tensor all had to be reconstructed and were then **verified numerically or symbolically**. Matrices extract as flowing text and were rebuilt from the mathematics. **Every slide carries a footer** to filter out.
>
> **Added beyond the slides, and labelled as mine throughout:**
> - **The full derivation of HOG's 3,780** (§10, exercise 1) including the 1,152 raw count, the 3.28× overlap factor, and the corner/edge/interior normalization counts of 1/2/4. **The slide states 3,780 and nothing else.**
> - **The median breakdown-point experiment** (§6, exercise 3) and the impulse-response comparison. **The slide says the median handles salt-and-pepper; the 0%-vs-50% breakdown and the +53.1-vs-+0.0 numbers are mine.**
> - **The separability cost table** (§7, exercise 2) and the Prewitt/Sobel/Scharr smoothing-weight comparison (33.3%/50%/62.5%).
> - **The symbolic verification of the LoG formula and the numerical DoG accuracy table** (§8, exercise 5), including the 0.868→0.375 degradation and the 2.2–6.2× cost saving. **The slide states both formulas and evaluates neither.**
> - **The kernel-sum sanity check** (§7) verified on a constant image.
> - **The output-size table and the odd-kernel argument** (§4, exercise 4), and its identification with DL ch. 05 §3.
> - **The observation that the classical detection pipeline is DL ch. 06's with the learned parts removed** (§10), and that **NMS is the only unchanged component.**
> - **The probability-integral-transform framing** of histogram equalization (§2) and its link to Probability Theory ch. 05.
> - **All thirteen Important Notes.**
>
> **No discrepancies found.** Every stated number that could be checked was checked and every one was correct — **3,780, 128, 105, the Sobel factorization, the LoG formula, the output-size formula and the median cost bounds all verify.**
>
> **Deliberately deferred, not omitted:** **the morphology section (slides 38–45)** — erosion, dilation, opening, closing, and the blur→threshold→morphology→components pipeline — is summarized only in §1's timeline, because its content is almost entirely figures and its operators (min/max over a structuring element) are order statistics of the kind §6 already treats. *It would repay a short section if the mid-term covers it.* **The convolution animations (13–14)** carry no text. **Scale space and the image pyramid** are named in §7–§8 and developed properly in [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §6 and, for this subject, in [[07 - Object Detection I|ch. 07]].
>
> **Left as the source states it:** the history timeline's dates and attributions (Bartlane 1920, Kirsch 1957, Roberts 1963, Ranger 7 1964, Sobel 1968, Hounsfield 1971, JPEG 1992, SIFT 1999, HOG 2005, AlexNet 2012); the claim that Canny is "still the default edge detector, 40 years on"; the SIFT-family table's years, descriptor sizes and patent status; and the assertion that Scharr is "a better rotation-invariant approximation," which is stated without a criterion.

**Previous:** [[01 - Introduction and Image Formation]] · **Next:** [[03 - Image Classification and Linear Models]]
