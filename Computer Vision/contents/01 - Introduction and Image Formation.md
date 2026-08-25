---
subject: Computer Vision
chapter: 1
tags: [ds, computer-vision, image-formation, pinhole, projection, colour-spaces, sensors, semantic-gap]
source: "Nguyen Manh Toan (Swinburne Vietnam), *Computer Vision* Lecture 01 — Introduction (68 slides); Szeliski 2nd ed. ch. 1–2"
---

# Introduction and Image Formation

**Week 1 of 14.** The lecturer's own slides, and the only chapter besides [[02 - Classical Image Processing|ch. 02]] with them.

**Four results.**

**§2 — ⚠️ THE LECTURE'S OPENING CLAIM IS QUANTITATIVE AND IT IS TRUE FOR WRITING AND OVERSTATED FOR SPEECH.** *"Vision predates language by five orders of magnitude."* **Eyes ≈540 Myr against writing ≈5 kyr is $1.08\times10^5$ — five orders exactly. Against speech (~100 kyr) it is $5{,}400=10^{3.73}$**, and "language" usually means speech.

**§5 — ⚠️ PERSPECTIVE PROJECTION IS WHY VISION IS AN *INVERSE* PROBLEM, AND IT IS ONE DIVISION.** $x=fX/Z$ maps $\mathbb R^3\to\mathbb R^2$: **$(1,2,10)$, $(2,4,20)$ and $(10,20,100)$ all land on the same pixel $(5,10)$.** Depth is not degraded — it is *destroyed*.

**§6 — ⚠️ THE PINHOLE DILEMMA IS REAL AND THE LENS RESOLVES IT AT A PRICE.** Small hole: sharp, no light. Large hole: bright, blurry. **A lens focuses instead of blocking — but $\frac1{z_o}+\frac1{z_i}=\frac1f$ can hold for only one $z_o$ at a time**, so **defocus is the arithmetic of the equation, not a defect of the glass.**

**§7 — ⚠️ THE GRAYSCALE WEIGHTS SUM TO EXACTLY 1, AND GREEN OUTWEIGHS BLUE BY 5.15×.** $0.299+0.587+0.114=1.000$, so grayscale is a **convex combination** and white stays white. **A "brightness" channel is a weighted opinion about human cones, not a physical measurement.**

## 📘 Main Knowledge

### 1. What the course is

**Slide 7:** *"Modern, deep-learning-focused computer vision: from image formation and linear classifiers to CNNs, transformers, detection, segmentation, generative models, and 3D vision."*

**Prerequisites:** machine learning, linear algebra, calculus, probability, Python. **Format:** one 2-hour lecture per week, ~80 min lecture + ~30 min hands-on PyTorch. **References:** Szeliski 2nd ed., Stanford CS231n, selected papers.

### 2. ⚠️ Why vision is old, and the claim worth checking

The lecture opens with an argument by evolutionary timescale.

| | age |
|---|---|
| **first eyes** (trilobites, Cambrian) | **≈540 Myr** |
| *Homo sapiens* | ≈300 kyr |
| speech | ≈100 kyr |
| writing | ≈5 kyr |

**Andrew Parker's "Light Switch" theory**: for ~3 billion years life was simple and mostly passive; then in ~20 million years most modern animal phyla appear. **The trigger was sight** — once an animal can see prey and be seen, active predation becomes possible and camouflage, armour, speed and shells all become worth evolving. *Eyes evolved independently many times.*

> [!warning] ⚠️ "Vision predates language by five orders of magnitude" — check it before repeating it
> | comparison | ratio | orders |
> |---|---|---|
> | eyes / **writing** | **108,000** | $10^{5.03}$ ✓ |
> | eyes / **speech** | 5,400 | $10^{3.73}$ |
> | eyes / *Homo sapiens* | 1,800 | $10^{3.26}$ |
>
> **Against writing the claim is exact — five orders to two decimal places.** Against **speech**, which is what "language" usually means and which the same slide dates at ~100,000 years, it is **3.7 orders — overstated by 1.3.**
>
> ⇒ *the slide's own two numbers support two different versions of its sentence.* **DECLINED as an erratum** — the slide lists both dates and the reader can pick; but **state which comparison you mean.** *(The rhetorical point survives either way: 3.7 orders is still an enormous gap.)*

**And the consequence for the course is the part that matters:** roughly **half the human cortex** is involved in vision; **language is symbolic and discrete while vision is continuous, ambiguous and under-determined**; and evolution solved it with massive parallelism and learning from experience — *"the same intuition behind deep networks."*

> [!note] **"That vision feels effortless is precisely why it is so hard to reproduce."**
> The lecture's best sentence, and the honest framing for everything after: **you have no introspective access to the computation**, so intuition is a poor guide to what a vision system must do.

### 3. The semantic gap, and the eight challenges

**The semantic gap**: an image is an array of numbers; the task is a meaning. Nothing in the numbers is labelled.

The lecture lists **eight sources of variation**, and the point is stated exactly right:

| | |
|---|---|
| **viewpoint variation** | the same car from two angles can be harder to match than two different cars from one angle |
| **illumination** | the same object under different lighting |
| **scale** | a near car is hundreds of pixels, a far one is a few |
| **deformation** | humans and animals change shape freely |
| **occlusion** | the object is partly or almost entirely hidden |
| **background clutter** | distracting elements behind the object |
| **intra-class variation** | different cats look completely different |
| **context** | objects in unusual environments get misclassified |

> [!warning] ⚠️ **"All of these change the pixels drastically — while the meaning stays the same."**
> That sentence is the specification for the whole subject. ⇒ **a vision model must be invariant to eight things it is never told about**, and every architectural choice from here on is an attempt to build one of those invariances in or to learn it from data.
>
> **Compare [[Deep Learning/contents/05 - Convolutional Neural Network|Deep Learning ch. 05]] §1**: translation invariance and locality were *assumed* into the convolution and bought a factor of $10^{10}$ in parameters. **That handles exactly one item on this list** — and even then only for small translations. **The other seven are why data augmentation and scale pyramids exist.**

### 4. From the world to an image — four stages

1. **Light** leaves a source and reflects off surfaces
2. **Geometry** — 3D points project onto a 2D image plane
3. **Optics** — a lens gathers and focuses light
4. **Sensor** — photons become digital numbers

**Everything that is hard about vision is already present in stages 2 and 4: a projection that loses a dimension, and a quantization that loses precision.**

### 5. ⚠️ The pinhole camera, and why vision is an inverse problem

An idealized camera: a box with an infinitesimal hole. **Each scene point maps to exactly one image point, and the image is inverted.**

$$\boxed{x=f\frac{X}{Z},\qquad y=f\frac{Y}{Z}}$$

*(Reconstructed — the slide extracts as `x=f X Z ,y=f Y Z`.)*

**Objects farther away appear smaller**, because $Z$ is in the denominator.

> [!warning] ⚠️ THE DIVISION BY $Z$ IS WHERE THE INFORMATION GOES
> With $f=50$:
>
> | 3D point $(X,Y,Z)$ | image point $(x,y)$ |
> |---|---|
> | $(1,\ 2,\ 10)$ | $(5.0000,\ 10.0000)$ |
> | $(2,\ 4,\ 20)$ | $(5.0000,\ 10.0000)$ |
> | $(10,\ 20,\ 100)$ | $(5.0000,\ 10.0000)$ |
>
> **Three different points a decade apart in depth produce one identical pixel.** Every point on the ray through the pinhole maps to the same place.
>
> ⇒ ***$Z$ is not degraded, it is destroyed — and this is precisely why the lecture calls vision an inverse problem.*** Recovering it needs a second view ([[14 - 3D Vision and Emerging Topics|ch. 14]]'s stereo), motion ([[11 - Video and Motion|ch. 11]]), or a learned prior about how big things usually are.
>
> **And the scale ambiguity is the same fact wearing a different hat:** a small object nearby and a large one far away are *pixel-identical*. **No amount of image processing can separate them.**

### 6. ⚠️ The pinhole trade-off, and the lens

| | image | signal-to-noise |
|---|---|---|
| **small (ideal) pinhole** | **sharp** | **low** — almost no light gets in |
| **large pinhole** | **blurry** | **high** |

**A genuine dilemma: sharpness and brightness are in direct conflict, and no choice of hole size resolves it.**

**The lens resolves it by focusing rather than blocking** — gathering light from a wide aperture and bending it back to one point. In a pinhole camera the focal length is just the aperture-to-sensor distance; with a lens it obeys the **thin lens equation**:

$$\boxed{\frac{1}{z_o}+\frac{1}{z_i}=\frac{1}{f}}$$

*(Reconstructed — the slide extracts as `1 zo + 1 zi = 1 f`.)*

> [!warning] ⚠️ THE EQUATION HAS ONE SENSOR POSITION AND MANY OBJECT DISTANCES — SO DEFOCUS IS UNAVOIDABLE
> At $f=50$ mm:
>
> | object distance $z_o$ | image distance $z_i$ | offset from $f$ |
> |---|---|---|
> | 1,000 mm | 52.6316 mm | +2.6316 |
> | 2,000 mm | 51.2821 mm | +1.2821 |
> | 5,000 mm | 50.5051 mm | +0.5051 |
> | $\infty$ | **50.0000 mm** | 0 |
>
> **The sensor sits at exactly one $z_i$.** Everything at a different $z_o$ focuses somewhere else and arrives as a blur circle.
>
> ⇒ ***the lecture's "unless our scene is just one plane, part of it will always be out of focus" is not an observation about lens quality — it is the arithmetic of the equation.*** **Depth of field is the range of $z_o$ whose blur circle is smaller than a pixel**, and it is controlled by the aperture: a smaller aperture deepens it (back toward pinhole behaviour) at the cost of light. **The pinhole trade-off never disappears; the lens just gives you a dial.**
>
> **Real lenses add what the ideal model omits:** radial distortion, chromatic aberration, vignetting. *(Radial distortion matters for [[14 - 3D Vision and Emerging Topics|ch. 14]]'s calibration; the rest mostly for image quality.)*

### 7. Sensors, sampling, quantization

**CCD / CMOS**: a grid of photosites counting photons. Two discretizations happen at once:

- **Sampling** — a continuous scene becomes a discrete pixel grid. *That is what "resolution" means, and it is where aliasing comes from ([[02 - Classical Image Processing|ch. 02]]).*
- **Quantization** — continuous brightness becomes discrete levels, **typically 8 bits: 0–255**.

**Colour** comes from a **Bayer filter** mosaic plus **demosaicing** — each photosite measures *one* of R, G or B and the other two are **interpolated**.

> [!note] ⚠️ Two consequences worth carrying
> **(i) 8 bits is 256 levels, a step of 0.3922% of full range.** Fine for display, and **the reason gradients band** when you stretch contrast — the information was never recorded.
> **(ii) Two-thirds of every colour pixel is interpolated, not measured.** A Bayer sensor has twice as many green photosites as red or blue, matching §7's weighting. ⇒ *"the raw pixels" are already the output of an algorithm.*

### 8. ⚠️ Colour spaces — same pixels, different coordinate systems

$$Y=0.299R+0.587G+0.114B$$

> [!warning] ⚠️ THE WEIGHTS SUM TO EXACTLY 1, AND THAT IS WHAT MAKES IT A BRIGHTNESS
> $0.299+0.587+0.114=\mathbf{1.000}$ exactly. ⇒ grayscale is a **convex combination**: pure white $(1,1,1)$ maps to 1, pure black to 0, and no colour can exceed the range. *Any other normalization would change the exposure.*
>
> | channel | weight | share |
> |---|---|---|
> | red | 0.299 | 29.9% |
> | **green** | **0.587** | **58.7%** |
> | blue | 0.114 | 11.4% |
>
> **Green outweighs blue by $0.587/0.114=\mathbf{5.15\times}$** — "the eye is most sensitive to green, least to blue."
>
> ⇒ ***a "brightness" channel is a weighted opinion about human cone sensitivity, not a physical measurement.*** A photometer would weight them differently, and a satellite sensor differently again ([[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §1 notes hyperspectral images with tens to hundreds of channels). **Three channels collapse to one: colour is lost, structure is kept.**

**The alternatives, and what each makes easy:**

| space | axes | good for |
|---|---|---|
| **RGB** | red, green, blue | what sensors and screens use |
| **HSV** | hue, saturation, value | **colour-based selection** — hue is stable under brightness change |
| **YCbCr** | luma + two chroma | **compression** — chroma can be subsampled because the eye barely notices |
| **Lab** | perceptually uniform | **colour difference** — Euclidean distance ≈ perceived difference |

> [!note] **"Same pixels, different coordinate systems — each one makes a different property easy to reason about."**
> ⇒ *a colour-space conversion is a change of basis, not new information.* **Choosing HSV to threshold a red object is choosing an axis along which the decision boundary is simple** — the same move as feature engineering, and the classical alternative to learning it.

### 9. The image as a tensor — the idea the whole course runs on

| | shape |
|---|---|
| grayscale | $\mathbf I\in\mathbb R^{H\times W}$ |
| colour | $\mathbf I\in\mathbb R^{H\times W\times3}$ |
| video | $\mathbf I\in\mathbb R^{T\times H\times W\times3}$ |

**In PyTorch, images live as $(N,C,H,W)$ float tensors** — note the channel axis moves to position 1, which is a standing source of bugs.

> [!warning] ⚠️ Slide 59, and it is the thesis of the course
> **"Everything we do — filtering, convolution, classification, detection, generation — is computation on these tensors. The pixels are the input; the semantics are what we must learn to recover. Every method in the remaining 14 weeks is a different way of doing that."**
>
> **And the memory arithmetic is worth having:** a $1920\times1080$ RGB image is **5.93 MB as `uint8` and 23.73 MB as `float32` — exactly 4×.** ⇒ *the conversion to float, not the image, is usually what fills the GPU* — and with [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5's accounting, activations scale with batch size while parameters do not.

**The toolbox:** `torchvision` gets pixels **into** tensors (I/O, datasets, pretrained models, transforms); **PyTorch** does the learning (tensors, autograd, `torch.nn`, GPU); **OpenCV** is there for the classical algorithms and for video.

## ✏️ Exercises

> [!example]- Exercise 1 — check the opening claim
> Vision's first eyes ≈540 Myr; writing ≈5 kyr; speech ≈100 kyr. **(a)** Is "five orders of magnitude" right? **(b)** What should the slide say?
>
> ---
> **(a)** eyes/writing $=540\times10^6/5\times10^3=\mathbf{108{,}000}=10^{5.03}$ — **five orders, essentially exactly.** eyes/speech $=5{,}400=10^{3.73}$ — **3.7 orders.**
>
> **(b)** ⚠️ **"Language" normally means speech**, and the same slide dates speech at ~100 kyr. **Against speech the gap is 3.7 orders, not 5.** The claim is right for *writing* — a 5,000-year-old technology — and the honest phrasing is *"predates writing by five orders of magnitude and speech by nearly four."* **Either way the rhetorical point stands; the number should just be attached to the right comparison.**

> [!example]- Exercise 2 — the inverse problem, concretely
> With $f=50$: **(a)** project $(1,2,10)$, $(2,4,20)$, $(10,20,100)$. **(b)** What does that show? **(c)** Given only the image point $(5,10)$, what can you say about the scene?
>
> ---
> **(a)** $x=fX/Z$, $y=fY/Z$ — **all three give $(5.0000,\ 10.0000)$.**
>
> **(b)** The three points lie on one ray through the pinhole. **Projection is many-to-one: an entire 1-D ray collapses to a 0-D pixel.**
>
> **(c)** Only that the scene point lies **somewhere on the ray** $\{(t/10,\ 2t/10,\ t):t>0\}$ — i.e. $X=Z/10$, $Y=Z/5$, $Z$ **completely unconstrained**. ⚠️ **One image gives you a direction and never a distance.** ⇒ *depth needs a second view, motion, or a prior — which is [[14 - 3D Vision and Emerging Topics|ch. 14]].*

> [!example]- Exercise 3 — the thin lens
> $f=50$ mm. **(a)** Where does a 1 m object focus? A 2 m one? **(b)** If the sensor is fixed for the 1 m object, is the 2 m object in focus? **(c)** Where does $z_o\to\infty$ focus, and why does that matter?
>
> ---
> **(a)** $z_i=\left(\frac1f-\frac1{z_o}\right)^{-1}$: at 1,000 mm, $z_i=\mathbf{52.6316}$ mm; at 2,000 mm, $z_i=\mathbf{51.2821}$ mm.
>
> **(b)** **No.** The sensor sits at 52.6316 mm; the 2 m object's rays converge at 51.2821 mm, **1.3495 mm in front of it**, and arrive as a blur circle. Whether that circle is *visible* depends on aperture and pixel pitch — which is exactly what "depth of field" measures.
>
> **(c)** $z_i\to f=\mathbf{50.0000}$ mm. ⚠️ **So the entire infinite range from 5 m to infinity is squeezed into the last 0.5 mm of sensor travel** ($50.5051\to50.0000$), while the single metre from 1 m to 2 m takes 1.35 mm. ⇒ ***focusing is far more sensitive up close than far away*** — the reason macro photography is hard and landscapes are not, and the reason autofocus systems care about near subjects.

> [!example]- Exercise 4 — the grayscale weights
> **(a)** Why do they sum to 1? **(b)** What is the green-to-blue ratio? **(c)** What happens to pure red, green and blue? **(d)** Why is this a bad brightness for a satellite?
>
> ---
> **(a)** So the map is a **convex combination**: it preserves the range $[0,1]$ and sends white to white. Any other sum would rescale exposure — a sum of 1.5 would blow out white by 50%.
>
> **(b)** $0.587/0.114=\mathbf{5.1491}$.
>
> **(c)** Pure red $\to0.299$, pure green $\to\mathbf{0.587}$, pure blue $\to0.114$. ⚠️ **Three fully saturated, equally "bright" colours map to three very different grays** — pure blue becomes almost black. *That is why thresholding a grayscale image loses blue objects.*
>
> **(d)** The weights encode **human cone sensitivity**, which is irrelevant to a satellite measuring reflectance — and multispectral sensors have channels (near-infrared, thermal) with no human analogue at all. ⇒ ***"brightness" is a modelling choice; only the raw per-band values are measurements.***

> [!example]- Exercise 5 — count the pixels and the bytes
> A $1920\times1080$ RGB image. **(a)** Bytes as `uint8`? **(b)** As `float32`? **(c)** A batch of 32 at $224\times224$, and what else must be stored to train? **(d)** How many of the colour values were actually measured?
>
> ---
> **(a)** $1920\times1080\times3=6{,}220{,}800$ bytes $=\mathbf{5.93}$ MB.
>
> **(b)** $\times4=\mathbf{23.73}$ MB — **exactly 4×.** *The float conversion, not the file, is what costs memory.*
>
> **(c)** $32\times3\times224\times224\times4=19{,}267{,}584$ bytes $=\mathbf{18.375}$ MB for the input batch alone. ⚠️ **And by [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5 that is the small part**: every intermediate activation must be retained for the backward pass, and with Adam the parameters cost 4 copies. **Activations scale with batch size; parameters do not.**
>
> **(d)** ⚠️ **One third.** A Bayer sensor records one of R, G, B per photosite; **the other two channels at every pixel are interpolated by demosaicing.** ⇒ *"raw pixels" are already an algorithm's output, and demosaicing artefacts are a real source of error in fine-texture tasks.*

## 📝 Summary

- The course is **"modern, deep-learning-focused computer vision"** over 14 weeks; assessment is **40% mid-term (week 9, inference-style), 50% team project, 10% participation**.
- **⚠️ "Vision predates language by five orders of magnitude" is exact against *writing* ($108{,}000=10^{5.03}$) and overstated against *speech* ($5{,}400=10^{3.73}$)** — and the same slide supplies both dates.
- **Vision is old, parallel and unconscious** — roughly half the cortex — and **"that vision feels effortless is precisely why it is so hard to reproduce."**
- **The semantic gap** plus **eight variations** (viewpoint, illumination, scale, deformation, occlusion, clutter, intra-class, context) that "change the pixels drastically while the meaning stays the same." **Convolution's built-in invariances cover roughly one of the eight.**
- **Image formation has four stages** — light, geometry, optics, sensor — and **the two lossy ones are geometry (a dimension) and quantization (precision)**.
- **⚠️ $x=fX/Z$, $y=fY/Z$ destroys depth**: $(1,2,10)$, $(2,4,20)$ and $(10,20,100)$ all map to $(5,10)$. One image gives a **direction, never a distance** — the definition of an inverse problem, and the reason scale ambiguity cannot be processed away.
- **⚠️ The pinhole trade-off is real** (small = sharp and dark, large = bright and blurry) and **a lens resolves it by focusing rather than blocking** — at the price of $\frac1{z_o}+\frac1{z_i}=\frac1f$, which holds for **one $z_o$ at a time**. **Defocus is arithmetic, not a flaw.** At $f=50$ mm the whole range 5 m → ∞ occupies the final **0.5 mm** of sensor travel.
- **Sensors sample *and* quantize**: 8 bits = 256 levels = a 0.392% step, and **colour is a Bayer mosaic plus demosaicing, so two of every three colour values are interpolated.**
- **⚠️ $Y=0.299R+0.587G+0.114B$ sums to exactly 1** — a convex combination, so white stays white — with **green 5.15× blue**. *A brightness channel is a weighted opinion about human cones.*
- **Colour spaces are changes of basis, not new information**: HSV for colour selection, YCbCr for compression, Lab for perceptual distance.
- **Everything in the course is computation on tensors**: $H\times W$, $H\times W\times3$, $T\times H\times W\times3$ — and $(N,C,H,W)$ in PyTorch. **A 1080p image is 5.93 MB as `uint8` and 23.73 MB as `float32`.**

## ⚠️ Important Notes

1. **⚠️ One image never gives depth.** Any method that appears to recover it from a single view is using a **learned prior** about object sizes and scene layout — which fails on unfamiliar objects and adversarial scenes. **Say "monocular depth estimation" and mean "informed guess."**
2. **⚠️ Scale ambiguity is projection, not noise.** A toy car near the lens and a real car far away are *pixel-identical*. No filter, resolution increase or architecture fixes it without extra information.
3. **⚠️ Channel order is a standing bug source.** OpenCV loads **BGR**; PyTorch expects **$(N,C,H,W)$**; PIL and matplotlib use $(H,W,C)$ RGB. **A silently wrong channel order produces plausible, slightly-wrong results** — the vault's recurring failure mode.
4. **⚠️ Normalization must match the pretrained model.** ImageNet models expect per-channel standardization with specific means and standard deviations ([[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §1 records them). **Feeding raw $[0,1]$ tensors to a pretrained backbone degrades it quietly.**
5. **⚠️ `uint8` → `float32` is a 4× memory multiplication** before any model runs. Do it on the GPU, per batch, not on the whole dataset.
6. **⚠️ 8-bit quantization is irreversible.** Contrast stretching a dark region *reveals* banding because the levels were never recorded. **Shoot or store higher bit depth if you intend to process; you cannot recover it later.**
7. **⚠️ Two-thirds of every colour value is interpolated.** Demosaicing artefacts are real and matter most for fine texture and thin structures — exactly the content high-frequency filters ([[02 - Classical Image Processing|ch. 02]]) respond to.
8. **⚠️ Grayscale conversion is lossy and *unequally* lossy.** Pure blue becomes 0.114 and pure green 0.587. **A threshold that works on green objects will miss blue ones.** Use HSV if the decision is about colour.
9. **⚠️ Depth of field is a dial, not a property.** Smaller aperture = deeper field + less light + (eventually) diffraction. **The pinhole trade-off of §6 never goes away.**
10. **⚠️ Real lenses distort.** Radial distortion must be corrected before any geometric reasoning ([[14 - 3D Vision and Emerging Topics|ch. 14]]). Straight lines that are not straight in the image will corrupt calibration, stereo and structure-from-motion.
11. **The eight challenges are a checklist for failure analysis.** When a model misclassifies, ask which of the eight the failing example exhibits — it usually names the fix (augmentation, multi-scale, context modelling) faster than tuning does.
12. **The mid-term is inference-style — "given a model, an architecture, or an output, reason about what happens and why."** ⇒ **the ⚠️ notes and exercises here matter more than the definitions.**

> [!warning] Gaps in the source material
> **This is one of only two chapters in this subject with the lecturer's own slides** (68 of them); ch. 03–14 have none — see [[00-Index]].
>
> **All slide figures are images and never extract.** **Recovered because the captions state their content**: the pinhole ray diagrams (slides 40–44 — the sharp/blurry and SNR trade-off is written out), the lens focus and magnification figures (45–52), the RGB channel decomposition (55), the grayscale comparison (56), the colour-space panel (57), and the timeline (16). **Genuinely lost**: the Cambrian and Burgess Shale imagery, every "Challenges" example image (slides 27–34 — though each caption states what the figure shows, which is what §3's table records), the semantic-gap illustration (25), and the 1966-to-today figure (22).
>
> **Beamer extraction quirks, recorded in this subject's `CLAUDE.md`:** prose and bullets extract cleanly and in order, **but formulas lose their spaces and fractions flatten** — `x=f X Z ,y=f Y Z` is $x=f\frac XZ,\ y=f\frac YZ$ and `1 zo + 1 zi = 1 f` is the thin lens equation. **Both were reconstructed and then verified numerically** (§5's three collinear points, §6's focus table). **Every slide carries a footer** that must be filtered out.
>
> **Added beyond the slides, and labelled as mine throughout:**
> - **The arithmetic of §2's "five orders" claim** and the finding that it holds for writing and not for speech.
> - **The three-collinear-points demonstration** in §5 and exercise 2, and the explicit statement of what a single image *does* determine (a ray).
> - **The whole of §6's focus table**, the observation that 5 m → ∞ occupies the last 0.5 mm, and the depth-of-field framing. **The slides state the thin lens equation and list "focus, depth of field, aperture trade-offs" without computing any of it.**
> - **The verification that the grayscale weights sum to exactly 1**, the 5.15× green/blue ratio, and the convex-combination argument. **The slide gives the formula and the sensitivity rationale, not the sum.**
> - **The Bayer "two-thirds interpolated" observation** (§7, exercise 5) — the slide names the Bayer filter and demosaicing without drawing the conclusion.
> - **The memory arithmetic** of §9 and exercise 5, and its link to DL ch. 04 §5.
> - **The mapping of the eight challenges onto convolution's built-in invariances** (§3), which connects this lecture to DL ch. 05.
> - **All twelve Important Notes**, of which 3, 4, 5, 6, 7 and 10 are practical hazards the slides do not raise.
>
> **One discrepancy investigated and DECLINED** (§2): "vision predates language by five orders of magnitude." **Ruled out**: own arithmetic (checked three ways) and extraction (the dates are clean slide text). **The slide supplies both the writing date (~5 kyr) and the speech date (~100 kyr), and the claim is exact against the former.** Recorded as an ambiguity of reference, not an error — and **not** entered in the errata table.
>
> **Deliberately deferred, not omitted:** the lecture's **history-of-vision section** (slides 12–22: the Cambrian, Marr, the 1966 MIT summer project) is summarized in §2 rather than reproduced, since its content is narrative and its figures are lost. **The toolbox slides (60–68)** are recorded as one paragraph in §9 — library APIs date quickly and belong in practice, not notes. **Homogeneous coordinates and the full camera matrix** are not in this lecture and are held for [[14 - 3D Vision and Emerging Topics|ch. 14]], where calibration needs them.
>
> **Left as the source states it:** Andrew Parker's Light Switch theory and the Cambrian dating; the "roughly half the human cortex" figure; the ~540 Myr, ~300 kyr, ~100 kyr and ~5 kyr dates; and the claim that eyes evolved independently many times.

**Previous:** — · **Next:** [[02 - Classical Image Processing]]
