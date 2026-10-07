---
subject: Computer Vision
chapter: 1
tags: [ds, computer-vision, image-formation, pinhole, thin-lens, sensors, colour-spaces, tensors]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 01: Introduction & Image Formation (68 slides); Szeliski 2nd ed. ch. 1–2 for background"
---

# Introduction and Image Formation

Week 1. The lecture has six parts: course overview, a short history of vision, why vision is hard, how an image is formed, colour spaces, and the software toolbox.

## 📘 Main Knowledge

### 1. What the course is about (slides 3–11)

**Computer vision** means teaching machines to *see*: to extract meaning from images and video. The lecture also frames it as an **inverse problem**: the camera turns a 3D world into a 2D image, and vision tries to go back from the 2D image to the 3D world (§5 shows why that's hard).

Applications listed on slides 5–6: medical imaging, image/video generation, face recognition and biometrics, vision–language models, autonomous driving and robotics, industrial inspection, AR/VR, agriculture, retail and sports analytics.

The course is *"modern, deep-learning-focused computer vision: from image formation and linear classifiers to CNNs, transformers, detection, segmentation, generative models, and 3D vision"* (slide 7). The 15 weeks are split into four parts:

| Part | Weeks |
|---|---|
| Foundations | 1 Intro & image formation · 2 Classical image processing · 3 Image classification & linear models · 4 From NNs to CNNs |
| Core architectures | 5 CNN architectures · 6 Vision transformers · 7 Object detection I · 8 Object detection II |
| Dense prediction | 9 Segmentation · 10 Pose estimation & faces · 11 Video & motion |
| Modern topics | 12 Self-supervised learning · 13 Generative models · 14 3D vision & emerging topics |
| | 15 Project presentations |

**Format:** one 2-hour session per week, about 80 minutes of lecture and 30 minutes of hands-on PyTorch. **Prerequisites:** machine learning, linear algebra, calculus, probability, Python. **References:** Szeliski, *Computer Vision: Algorithms and Applications* (2nd ed., free online), the Stanford CS231n notes, and selected papers per lecture.

**Assessment:**

| Component | Weight | Notes |
|---|---|---|
| Mid-term exam | 40% | Week 9. *Inference questions*: "given a model, an architecture, or an output, reason about what happens and why — not memorization" |
| Final project | 50% | Teams of ~6. Topics released week 3; proposal, milestone report, presentation (week 15), code |
| Participation | 10% | Attendance and in-class exercises |

> [!tip] What "inference questions" means for revision
> The mid-term covers weeks 1–8 and asks you to reason about a given situation, not to recite definitions. The exercises in these notes are written in that style: you're given a setup and asked what happens and why.

### 2. A brief history of vision (slides 12–23)

The lecture compares the two main fields of deep learning:

| | Natural language processing | Computer vision |
|---|---|---|
| Works with | language, a human invention | vision, far older than humans |
| Age | speech ~100,000 years; writing ~5,000 years | eyes ~540 million years |

The slide says vision "predates language by five orders of magnitude". That holds against writing: $540\times10^6 / 5\times10^3 = 108{,}000 \approx 10^{5.03}$. Against speech it is $5{,}400 \approx 10^{3.7}$, so about four orders. Either way the gap is huge.

**The Cambrian explosion (~540–530 million years ago).** For about 3 billion years life was simple and mostly passive. Then, within roughly 20 million years, most modern animal groups appear in the fossil record. Andrew Parker's **Light Switch theory** says the trigger was the first eyes (in trilobites, ~540 Mya). Once an animal can see prey, and be seen, active predation becomes possible, and camouflage, armour, speed and shells all become worth evolving. Eyes evolved independently many times, which suggests how useful they are.

The timeline slide (16, log scale) makes the point: *"Biological vision had half a billion years of optimization. Computer vision has had sixty."*

**Vision seems easy for humans.** About half the human brain is involved in visual processing, and we recognise thousands of object categories instantly (rapid serial visual presentation experiments, Potter 1975; speed of visual processing, Thorpe et al. 1996).

**The MIT Summer Vision Project (1966).** Vision Memo No. 100 proposed using summer students to "build a significant part of a visual system" in a few months. The planned tasks were:
- **figure–ground separation**: separate objects from the background;
- **region description**: describe the regions found;
- **object identification**: name objects from a known vocabulary (balls, bricks, cylinders).

All of this was meant to happen in one summer, in a world of simple shapes on plain backgrounds. Each sub-goal grew into a research field of its own (segmentation, recognition, scene understanding), and some are still open 60 years later. The lesson: *what feels effortless to humans is not therefore easy to compute.* The optimism was early rather than wrong. Deep learning now solves these tasks, but it took large datasets, GPUs and decades of ideas.

**Why this matters for the course (slide 23):**
- Vision is old, deep and highly optimised.
- Language is symbolic and discrete; vision is **continuous, ambiguous and under-determined**.
- Evolution solved vision with massive parallelism and learning from experience, which is the same intuition behind deep networks.

> [!quote] Slide 23
> "That vision feels effortless is precisely why it is so hard to reproduce."

### 3. Why vision is hard (slides 24–34)

**The semantic gap.** A computer sees an image as a grid of numbers. The task is to get *meaning* from it ("this is a cat"). Nothing in the numbers says which pixels belong to the cat. Bridging raw pixel values and semantic meaning is the core challenge.

**The eight challenges.** Each of these changes the pixels a lot while the meaning stays the same:

| Challenge | Example from the slides |
|---|---|
| Viewpoint variation | Different cars seen from the same angle can look more alike than one car seen from two angles |
| Illumination | The same cat under different lighting |
| Scale variation | A nearby car covers hundreds of pixels, a distant one a few |
| Deformation | People and animals change shape freely |
| Occlusion | The object is partly or completely hidden |
| Background clutter | Distracting things behind the object |
| Intra-class variation | Different cats look completely different from each other |
| Context | Objects in unusual surroundings get misclassified |

> [!note] Why this list matters later
> A good vision model has to give the same answer under all eight changes, i.e. be **invariant** to them. Much of the rest of the course is about how to get those invariances. Convolution builds in tolerance to small shifts ([[04 - From Neural Networks to CNNs|ch. 04]]). Image pyramids and feature pyramids handle scale ([[02 - Classical Image Processing|ch. 02]], [[07 - Object Detection I|ch. 07]]). Data augmentation teaches the rest from examples ([[05 - CNN Architectures|ch. 05]]).
>
> When a model fails on an image, checking which of the eight the image shows is a quick way to find the fix.

### 4. From the world to an image (slides 35–36)

An image is formed in four stages:

1. **Light** leaves a source and reflects off surfaces.
2. **Geometry**: 3D points are projected onto a 2D image plane.
3. **Optics**: a lens gathers and focuses the light.
4. **Sensor**: photons are turned into digital numbers.

Two of these stages lose information for good: geometry loses a dimension (depth, §5), and the sensor loses precision (sampling and quantisation, §7).

### 5. The pinhole camera and perspective projection (slides 37–44)

The **camera obscura** is the oldest camera: a dark box with a small hole. The idealised version is the **pinhole camera**, a box with an infinitely small hole.

- Each scene point maps to exactly one image point, because only one ray from it gets through the hole.
- The image is **upside down**.
- In a pinhole camera the **focal length $f$** is the distance from the hole (aperture) to the sensor.

**Perspective projection.** A 3D point $(X, Y, Z)$, with $Z$ the depth along the optical axis, lands at image coordinates

$$x = f\,\frac{X}{Z}, \qquad y = f\,\frac{Y}{Z}$$

Two consequences:
- **Farther objects look smaller.** $Z$ is in the denominator, so doubling the distance halves the image size.
- **Depth is lost.** Every point on the same ray through the pinhole lands on the same pixel. For example, with $f = 50$, the points $(1, 2, 10)$, $(2, 4, 20)$ and $(10, 20, 100)$ all project to $(5, 10)$.

> [!important] Why vision is an inverse problem
> Projection maps 3D to 2D and is many-to-one: a whole ray collapses onto one pixel. From one image you know the *direction* to a point but not its *distance*. A small object up close and a large object far away can produce exactly the same image.
>
> Getting depth back needs extra information: a second camera (stereo), motion, a known object size, a depth sensor, or a prior learned from data. That is the subject of [[14 - 3D Vision and Emerging Topics|ch. 14]].

**Pinhole size is a trade-off (slides 43–44):**

| | Image | Signal-to-noise ratio |
|---|---|---|
| Small (ideal) pinhole | sharp | low (very little light gets in) |
| Large pinhole | blurry (each scene point spreads over a patch) | high |

No hole size gives both sharpness and brightness. That's the reason cameras use lenses.

### 6. The lens camera (slides 45–53)

*"Pinhole: sharp but almost no light ⇒ use a lens."* A lens gathers light through a wide opening and bends all rays from one scene point back to a single image point. So it gets brightness without giving up sharpness, but only at one distance.

- **Focal length (lens):** the distance behind the lens where parallel rays (from a very distant object) meet.
- **Thin lens equation:** an object at distance $z_o$ in front of the lens is in focus at distance $z_i$ behind it when

$$\frac{1}{z_o} + \frac{1}{z_i} = \frac{1}{f}$$

- **Defocus:** the sensor sits at one $z_i$, so only one object distance is perfectly sharp. *"Unless our scene is just one plane, part of it will always be out of focus."* Points at other distances focus in front of or behind the sensor and show up as small blur circles.
- **Depth of field:** the range of distances whose blur is too small to notice. A smaller aperture gives a deeper depth of field but less light, so the pinhole trade-off is still there, just adjustable.
- **Magnification:** image size relative to object size, $z_i / z_o$.

Example with $f = 50$ mm:

| Object distance $z_o$ | Focus distance $z_i = (1/f - 1/z_o)^{-1}$ |
|---|---|
| 1 m | 52.63 mm |
| 2 m | 51.28 mm |
| 5 m | 50.51 mm |
| very far ($\infty$) | 50.00 mm |

Going from 1 m to 2 m moves the focus point 1.35 mm, while everything from 5 m to infinity fits into the last 0.5 mm. Focusing is much more sensitive for close objects.

**Pinhole vs lens (slide 53):** pinhole focal length = aperture-to-sensor distance; lens focal length is set by the thin lens equation. Lenses bring focus, depth-of-field and aperture trade-offs, and real lenses add **distortions**: radial distortion (straight lines bend), chromatic aberration (colours focus at slightly different places) and vignetting (corners darker than the centre).

### 7. Digital image sensors (slide 39)

A **CCD or CMOS** sensor is a grid of photosites that count photons. Turning light into numbers involves two separate discretisations:

- **Sampling:** the continuous scene becomes a discrete grid of pixels. The grid size is the **resolution**.
- **Quantisation:** continuous brightness becomes discrete levels, usually **8 bits = 256 levels (0–255)**.

**Colour** comes from a **Bayer filter**: a mosaic of red, green and blue filters over the photosites (half green, a quarter each red and blue). Each photosite measures only one colour, and **demosaicing** interpolates the other two. So two of the three colour values at each pixel are estimated, not measured.

### 8. Colour spaces (slides 54–57)

**RGB.** A colour image is three separate $H\times W$ intensity maps (red, green, blue) stacked into an $H\times W\times 3$ array. In this course, images are usually RGB tensors scaled to $[0,1]$ or standardised per channel.

**RGB to grayscale:**

$$Y = 0.299R + 0.587G + 0.114B$$

- The weights follow human sensitivity: the eye is most sensitive to green and least to blue (green's weight is about 5× blue's).
- The weights add up to 1, so white $(1,1,1)$ stays 1 and the result stays in the same range.
- Colour is lost, structure is kept. Very different colours can end up as almost the same gray (see Exercise 3).

**Other colour spaces:** the same pixels in a different coordinate system. Each one makes some property easy to work with:

| Space | Channels | Useful for |
|---|---|---|
| RGB | red, green, blue | what sensors and screens use |
| HSV | hue, saturation, value | picking objects by colour, since hue changes little when brightness changes |
| YCbCr | luma (brightness) + two chroma channels | compression (JPEG, video): colour detail can be reduced because the eye barely notices |
| Lab | lightness + two colour axes | measuring colour difference, since it is *perceptually uniform* (equal distances look equally different) |

Converting between colour spaces doesn't add information. It just makes some decisions simpler: thresholding on hue is easier than thresholding on R, G and B together.

### 9. The image as a tensor (slides 58–59)

| Data | Shape |
|---|---|
| Grayscale image | $I \in \mathbb R^{H\times W}$ |
| Colour image | $I \in \mathbb R^{H\times W\times 3}$ |
| Video | $I \in \mathbb R^{T\times H\times W\times 3}$ |

> [!quote] Slide 59, "Key idea for the whole course"
> "Everything we do — filtering, convolution, classification, detection, generation — is computation on these tensors. The pixels are the input; the semantics are what we must learn to recover."

### 10. The toolbox (slides 60–65)

| Library | Import | Role |
|---|---|---|
| PyTorch | `torch` | tensors, autograd (automatic gradients), neural network layers, GPU |
| torchvision | `torchvision` | image I/O, datasets (CIFAR, ImageNet, COCO), pretrained models (ResNet, ViT…), transforms (resize, crop, augment, normalise) |
| OpenCV | `cv2` | classical image processing (week 2), video, optical flow, tracking (week 11) |

Rule of thumb: torchvision gets pixels into tensors, PyTorch does the learning, OpenCV handles the classical algorithms and video.

**Conventions (slide 65).** *"Most 'my model outputs nonsense' bugs are a mismatch in this table."*

| Representation | Shape | Range / dtype | Channel order |
|---|---|---|---|
| NumPy array from `cv2.imread` | $(H, W, C)$ | 0–255, `uint8` | **BGR** |
| Tensor from `torchvision.io.read_image` | $(C, H, W)$ | 0–255, `uint8` | RGB |
| Tensor after `ToDtype(float32, scale=True)` | $(C, H, W)$ | 0–1, `float32` | RGB |
| Batch fed to a model | $(N, C, H, W)$ | normalised | RGB |

> [!warning] The BGR gotcha
> `cv2.imread` returns **BGR**, not RGB. If you forget to convert (`cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)`), red and blue are swapped and your images look blue. The slide calls this the single most common bug in a first CV assignment.

A typical torchvision pipeline from the slides:

```python
from torchvision.io import read_image
from torchvision.transforms import v2 as T

x = read_image("cat.jpg")              # (C, H, W), uint8
t = T.Compose([
    T.Resize((224, 224)),
    T.ToDtype(torch.float32, scale=True),   # -> [0, 1]
])
x = t(x)
```

**Hands-on (slide 68):** load an image and check its size, mode and dtype; convert between PIL, NumPy and PyTorch; split the R, G, B channels; compute grayscale three ways and check the formula by hand; convert to HSV, YCbCr and Lab; reproduce and fix the BGR bug; build a resize → crop → normalise pipeline and batch it.

## ✏️ Exercises

> [!example]- Exercise 1 — Same pixel height, different objects
> A camera has focal length $f = 800$ pixels. A 1.8 m tall person stands 6 m away.
> **(a)** How tall is the person in the image?
> **(b)** The person walks back to 12 m. Now how tall?
> **(c)** A 0.18 m toy figure stands 0.6 m from the camera. How tall is it in the image, and what does this tell you about recognising size from one image?
>
> ---
> **(a)** $y = fY/Z = 800 \times 1.8 / 6 = 240$ px.
>
> **(b)** $800 \times 1.8 / 12 = 120$ px. Double the distance, half the size.
>
> **(c)** $800 \times 0.18 / 0.6 = 240$ px, the same as the real person at 6 m. The toy is 10× smaller and 10× closer, so the ratio $Y/Z$ is unchanged. One image can't tell them apart. A model can only guess real size from learned knowledge ("people are usually about 1.7 m tall"), and that guess fails for unusual objects. This is the scale-variation challenge from §3 and the reason depth needs extra information (§5).

> [!example]- Exercise 2 — Focusing a lens
> A camera with a $f = 50$ mm lens is focused on a subject 1 m away.
> **(a)** Where is the sensor?
> **(b)** A second subject stands 2 m away. Is it sharp? If not, does its light focus in front of or behind the sensor?
> **(c)** To refocus on the 2 m subject, which way does the lens move relative to the sensor, and by how much?
>
> ---
> **(a)** $z_i = (1/50 - 1/1000)^{-1} = 52.63$ mm behind the lens.
>
> **(b)** Not perfectly. Its focus distance is $(1/50 - 1/2000)^{-1} = 51.28$ mm, so its rays meet 1.35 mm *in front of* the sensor and have spread out again by the time they reach it. They form a blur circle. Whether you notice depends on the aperture (smaller aperture, smaller blur) and the pixel size.
>
> **(c)** The lens must move 1.35 mm closer to the sensor. In general, farther subjects need a shorter lens-to-sensor distance, approaching $f$ as the subject approaches infinity.

> [!example]- Exercise 3 — When grayscale breaks a pipeline
> A pipeline converts images to grayscale and then thresholds them to find a red sign, RGB $\approx (0.8, 0.1, 0.1)$, on green grass, RGB $\approx (0.1, 0.4, 0.1)$.
> **(a)** Compute the gray value of each.
> **(b)** Will the threshold work? What would you do instead?
> **(c)** Pure blue $(0,0,1)$ and pure green $(0,1,0)$ are both fully saturated colours. What gray values do they get?
>
> ---
> **(a)** Sign: $0.299(0.8) + 0.587(0.1) + 0.114(0.1) = 0.309$. Grass: $0.299(0.1) + 0.587(0.4) + 0.114(0.1) = 0.276$.
>
> **(b)** Probably not. The gray values differ by only 0.03, so noise and lighting will mix them up. The information that separates them is colour, and grayscale throws colour away. Convert to HSV instead and threshold on **hue**: red and green are far apart on the hue circle, and hue changes little when brightness changes.
>
> **(c)** Blue → 0.114 (nearly black), green → 0.587. The weights follow human eye sensitivity, not the physical amount of light, so equally strong colours can map to very different grays.

> [!example]- Exercise 4 — Debugging a "nonsense" model
> A student runs this code with a ResNet pretrained in torchvision on RGB images normalised with ImageNet statistics, and gets random-looking predictions:
> ```python
> img = cv2.imread("dog.jpg")              # step 1
> x = torch.from_numpy(img).float()        # step 2
> x = x.unsqueeze(0)                       # step 3
> pred = model(x)
> ```
> List every mismatch with what the model expects, using the conventions table in §10.
>
> ---
> 1. **Channel order:** `cv2.imread` gives **BGR**, the model expects RGB. Fix with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`.
> 2. **Axis order:** the array is $(H, W, C)$; PyTorch wants $(C, H, W)$. After `unsqueeze(0)` the shape is $(1, H, W, 3)$, which is wrong. The code may crash on a channel mismatch or, if shapes happen to line up, silently read the data the wrong way. Fix with `x.permute(2, 0, 1)` before adding the batch axis.
> 3. **Range:** values are 0–255, but the model was trained on values scaled to $[0,1]$ and then normalised per channel. Divide by 255 and apply the same mean/std normalisation used in training.
> 4. **Size:** the model was trained on 224×224 inputs; the photo is probably a different size. Resize (and centre-crop) to match.
>
> Each of these alone gives plausible-looking but wrong outputs, which is why slide 65 says most "nonsense" bugs come from this table.

> [!example]- Exercise 5 — How much memory?
> **(a)** How many bytes is one 1920×1080 RGB image as `uint8`? As `float32`?
> **(b)** How large is a training batch of 32 RGB images at 224×224 in `float32`?
> **(c)** A 10-second video clip at 30 fps, resized to 224×224 RGB, `float32`. How large is it?
> **(d)** Of the 3 colour values at each pixel of a camera photo, how many were actually measured?
>
> ---
> **(a)** $1920 \times 1080 \times 3 = 6{,}220{,}800$ bytes ≈ **5.93 MB**. In `float32` (4 bytes per value) it's 4× that, ≈ **23.73 MB**.
>
> **(b)** $32 \times 3 \times 224 \times 224 \times 4 = 19{,}267{,}584$ bytes ≈ **18.4 MB**. That's just the input; training also stores every layer's activations for the backward pass.
>
> **(c)** $T\times H\times W\times 3$ with $T = 300$: $300 \times 224 \times 224 \times 3 \times 4$ bytes ≈ **172 MB** for a single example. This is why video models sample only some frames ([[11 - Video and Motion|ch. 11]]).
>
> **(d)** One. A Bayer sensor measures one colour per photosite, and demosaicing interpolates the other two.

## 📝 Summary

- **Course:** deep-learning-focused CV over 14 teaching weeks. Mid-term in week 9 (40%, inference-style questions on weeks 1–8), team project (50%), participation (10%).
- **History:** eyes are ~540 million years old (Cambrian explosion, Light Switch theory); computer vision is ~60. The 1966 MIT Summer Vision Project showed that what feels easy to humans is hard to compute.
- **Semantic gap:** pixels are numbers, the task is meaning. **Eight challenges** (viewpoint, illumination, scale, deformation, occlusion, clutter, intra-class variation, context) change the pixels a lot while the meaning stays the same.
- **Image formation:** light → geometry → optics → sensor.
- **Pinhole projection:** $x = fX/Z$, $y = fY/Z$. Farther objects look smaller, and depth is lost. That's why vision is an *inverse problem*.
- **Pinhole trade-off:** small hole = sharp but dark; large hole = bright but blurry. A **lens** fixes this but focuses only one distance at a time: $1/z_o + 1/z_i = 1/f$. Real lenses add radial distortion, chromatic aberration and vignetting.
- **Sensors:** CCD/CMOS; **sampling** (resolution) and **quantisation** (8 bits = 0–255); colour from a **Bayer filter** + demosaicing.
- **Colour:** grayscale $Y = 0.299R + 0.587G + 0.114B$ (green weighted most). HSV, YCbCr and Lab are other coordinate systems for the same pixels.
- **Images are tensors:** $H\times W$, $H\times W\times3$, $T\times H\times W\times3$. In PyTorch, batches are $(N, C, H, W)$. OpenCV gives $(H, W, C)$ **BGR** `uint8`.

## ⚠️ Important Notes

1. **One image gives no depth.** Single-image ("monocular") depth estimators use learned knowledge about typical object sizes and scene layouts. That's an informed guess, and it fails on unusual objects.
2. **Scale ambiguity comes from projection, not noise.** A toy close up and a real object far away can be pixel-identical (Exercise 1). Higher resolution doesn't help.
3. **OpenCV loads BGR.** Always convert to RGB before using torchvision models or matplotlib.
4. **Watch axis order.** NumPy/OpenCV use $(H, W, C)$; PyTorch uses $(C, H, W)$ and $(N, C, H, W)$ for batches. Use `permute`, not `reshape` or `view`: those keep the same memory order and just relabel the axes, which scrambles the image without an error.
5. **Match the pretrained model's preprocessing.** A model trained on $[0,1]$ images normalised with ImageNet means and standard deviations gives quietly worse results on raw 0–255 input.
6. **`uint8` → `float32` multiplies memory by 4.** Convert per batch, not for the whole dataset at once.
7. **Quantisation can't be undone.** Stretching the contrast of a dark 8-bit region shows banding, because the in-between levels were never recorded.
8. **Grayscale throws away colour unevenly.** Pure blue maps to 0.114, pure green to 0.587. If the decision depends on colour, use HSV.
9. **Defocus is part of the physics, not a flaw.** A lens focuses only one distance exactly; a smaller aperture increases depth of field but lets in less light.
10. **Lens distortion matters for geometry.** Radial distortion bends straight lines and must be corrected before measuring anything in 3D ([[14 - 3D Vision and Emerging Topics|ch. 14]]).
11. **Pinhole focal length vs lens focal length.** For a pinhole it's the aperture-to-sensor distance; for a lens it's where parallel rays meet. An exam can test the difference.
12. **Use the eight challenges for failure analysis.** When a model misclassifies an image, check which challenge the image shows. It often points to the fix (augmentation, multi-scale features, more context).

> [!warning] Gaps in the source material
> - **Figures:** all slide images are lost in text extraction. Recovered from captions: the timeline (16), pinhole diagrams (40–44), lens diagrams (45–52), RGB channel split (55), grayscale comparison (56) and colour-space panel (57). Lost: the Cambrian and Burgess Shale images, the RSVP and Thorpe figures (17–18), the semantic-gap figure (25) and the example image for each of the eight challenges (27–34). The table in §3 uses each slide's caption.
> - **Formulas were rebuilt from flattened text** (`x=f X Z ,y=f Y Z` → $x = fX/Z$; `1 zo + 1 zi = 1 f` → thin lens equation) and checked numerically.
> - **Added beyond the slides:** the check of the "five orders of magnitude" claim (§2); the collinear-points example (§5); the focus-distance table (§6); the Bayer filter proportions and "two of three values are interpolated" (§7); the magnification formula $z_i / z_o$; the explanation of what each colour space is good for (the slide only names them); all five exercises and the Important Notes.
> - **Not in this lecture:** homogeneous coordinates, the camera intrinsic matrix and calibration. They belong with 3D vision ([[14 - 3D Vision and Emerging Topics|ch. 14]]).

**Previous:** — · **Next:** [[02 - Classical Image Processing]]
