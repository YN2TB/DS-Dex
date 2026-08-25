---
subject: Computer Vision
chapter: 14
tags: [ds, computer-vision, 3d-vision, stereo, epipolar-geometry, structure-from-motion, nerf, gaussian-splatting, foundation-models]
source: "Szeliski, *Computer Vision*, 2nd ed. ch. 11 (structure from motion), ch. 12 (depth estimation), §2.1.4, §13.5; Mildenhall et al. 2020 (NeRF); Kerbl et al. 2023 (3D Gaussian splatting); Kirillov et al. 2023 (SAM); the lecturer's course outline"
---

# 3D Vision and Emerging Topics

**Week 14 of 14 — the last teaching week; week 15 is project presentations.** See [[00-Index]].

**⚠️ THIS IS THE ONE CHAPTER WHERE SZELISKI IS THE PRIMARY SOURCE RATHER THAN A REFERENCE.** Chapters 11–12 of his book are the field's standard treatment of exactly this material — *the reverse of [[12 - Self-Supervised Learning|ch. 12]] and [[13 - Generative Models|ch. 13]], where he was thinnest.*

**Four results, and one that closes the subject.**

**§3 — ⚠️ STEREO DEPTH ERROR GROWS WITH THE *SQUARE* OF DEPTH: $|\Delta Z| = \dfrac{Z^2}{fB}|\Delta d|$.** A typical rig accurate to **0.16% at 1 m is accurate to 15.62% at 100 m — ±15.6 metres.** Five times the distance is **twenty-five times the error**, and **widening the baseline is self-limiting** because the views stop overlapping. ⇒ ***that one exponent is why long-range perception uses LiDAR or radar, whose error is roughly constant with range.***

**§1 — ⚠️ MONOCULAR SCALE AMBIGUITY IS EXACT, NOT APPROXIMATE.** $f(sX)/(sZ)=fX/Z$ for **every** $s$ ⇒ **a toy car at 50 cm and a real car at 10 m produce the identical image.** *So a monocular depth network reports a **prior over object sizes**, not a measurement — and that distinction decides whether you may trust the number.*

**§5 — ⚠️ NeRF NEEDS 122,880,000 MLP EVALUATIONS PER $800\times800$ FRAME** — 3.69 **billion** per second for 30 fps. *That number, not any quality argument, is why 3D Gaussian splatting displaced it for real-time use.* **And NeRF is an optimization dressed as learning**: its training set is one scene and its output is the weights.

**§6 — ⚠️ THE SUBJECT'S CLOSING RESULT: EVERY METHOD IN THIS CHAPTER IS AN ANSWER TO ONE LINE FROM [[01 - Introduction and Image Formation|WEEK 1]] — $x=fX/Z$ DESTROYS $Z$.** Fourteen weeks later, **exactly one of them (LiDAR) *measures* depth; every other one *infers* it.**

## 📘 Main Knowledge

### 1. ⚠️ What a single image cannot tell you

[[01 - Introduction and Image Formation|Ch. 01]] §3 established that perspective projection maps $\mathbb R^3\to\mathbb R^2$ and destroys $Z$. **The consequence is sharper than "depth is hard":**

$$x'=f\frac{sX}{sZ}=f\frac XZ\qquad\text{for every }s>0$$

| scale $s$ | $X$ (m) | $Z$ (m) | pixel $x$ |
|---|---|---|---|
| 0.5 | 0.50 | 2.50 | **160.0000** |
| 1.0 | 1.00 | 5.00 | **160.0000** |
| 2.0 | 2.00 | 10.00 | **160.0000** |
| 100.0 | 100.00 | 500.00 | **160.0000** |

> [!warning] ⚠️ A TOY CAR AT 50 cm AND A REAL CAR AT 10 m PRODUCE THE IDENTICAL IMAGE
> **The whole scene scaled by any factor is pixel-for-pixel unchanged.** ⇒ ***no monocular method can recover absolute scale from geometry — this is a proof, not a difficulty.***
>
> **So what does a "monocular depth estimation" network do?** It predicts **relative** depth, or absolute depth only by having **learned typical object sizes** — *a prior, not a measurement.* ⚠️ **That distinction decides whether you may trust the number**: the prior fails silently on unusual objects, scale models, and images of images. *Same class of statement as [[03 - Image Classification and Linear Models|ch. 03]] §5's proof about linear models — a property of the formulation that no data fixes.*

### 2. Two views: the epipolar constraint

**Given two views, a point in image 1 constrains its match in image 2 to a *line*** — the epipolar line, the projection of the ray through the first pixel:

$$\mathbf x_2^\top\mathbf F\,\mathbf x_1=0$$

| search | candidates (640×480) |
|---|---|
| unconstrained | **307,200** |
| **on the epipolar line** | **640** |
| **reduction** | **480×** |

**And it is exact geometry, not an approximation.** *After **rectification** the epipolar lines become horizontal scanlines, which is why every practical stereo pipeline rectifies first — the 1D search becomes a memory-contiguous one.*

| matrix | DoF | estimated from |
|---|---|---|
| **fundamental $\mathbf F$** | 7 | 8 correspondences (8-point algorithm) |
| **essential $\mathbf E$** | 5 | 5 correspondences, **calibrated** cameras |
| homography $\mathbf H$ | 8 | 4 correspondences, **planar** scene or pure rotation |

*($\mathbf F$ is $3\times3$ = 9 entries, minus 1 for scale, minus 1 for $\det\mathbf F=0$ ⇒ **7 DoF**. $\mathbf E$ additionally uses known intrinsics, leaving rotation (3) + translation direction (2) = **5** — translation's *magnitude* is §1's missing scale, again.)*

**Correspondence is the hard part**, and it is [[11 - Video and Motion|ch. 11]] §2's problem: a textureless region or a repeated pattern gives no unique match. *The structure tensor decides matchability here exactly as it did there.*

### 3. ⚠️ Stereo, and the exponent that defines the field

With disparity $d=x_1-x_2$ and baseline $B$: $Z=\dfrac{fB}{d}$. Differentiating and substituting $d=fB/Z$:

$$\frac{dZ}{dd}=-\frac{fB}{d^2}\quad\Longrightarrow\quad \boxed{\;|\Delta Z|=\frac{Z^2}{fB}\,|\Delta d|\;}$$

**A rig with $f=800$ px, $B=0.20$ m and $\pm0.25$ px disparity precision:**

| $Z$ (m) | disparity (px) | depth error (m) | relative |
|---|---|---|---|
| 1 | 160.000 | 0.0016 | **0.16%** |
| 2 | 80.000 | 0.0063 | 0.31% |
| 5 | 32.000 | 0.0391 | 0.78% |
| 10 | 16.000 | 0.1562 | 1.56% |
| 20 | 8.000 | 0.6250 | 3.12% |
| 50 | 3.200 | 3.9062 | 7.81% |
| **100** | 1.600 | **15.6250** | **15.62%** |

> [!warning] ⚠️ FIVE TIMES THE DISTANCE IS TWENTY-FIVE TIMES THE ERROR
> **0.6 cm at 2 m becomes 15.6 cm at 10 m; at 100 m the rig is $\pm$15.6 metres.** The *relative* error grows **linearly** with depth, so there is no range at which stereo is merely "somewhat worse" — **it degrades without limit.**
>
> **And the obvious fix is self-limiting.** Widening the baseline helps linearly:
>
> | baseline $B$ | error at 20 m |
> |---|---|
> | 0.05 m | 2.5000 m |
> | 0.20 m | 0.6250 m |
> | 0.50 m | 0.2500 m |
> | 1.00 m | 0.1250 m |
>
> ⚠️ **but a wider baseline means fewer shared pixels, more occlusion, and a harder matching problem** — the two views look less alike, which is exactly what correspondence depends on. **You are trading the error you can compute against one you cannot.**
>
> ⇒ ***this is why long-range perception uses LiDAR or radar***: a time-of-flight sensor measures $Z$ directly and its error is roughly **constant** with range, not quadratic. **The choice between camera and LiDAR in an autonomous vehicle is this table.**

### 4. Structure from motion — the same problem, unrolled

**SfM solves for camera poses *and* 3D points simultaneously** from many views, by minimizing reprojection error (**bundle adjustment**):

| unknowns | count |
|---|---|
| 100 cameras × 6 DoF | 600 |
| 50,000 points × 3 | 150,000 |
| **total** | **150,600** |

**This is tractable only because the Jacobian is sparse** — each point is seen by a few cameras, so most blocks are zero. *Without that structure a 150,600-unknown non-linear least-squares problem would be hopeless; with it, it is routine. [[Optimization/contents/00-Index|Optimization]]'s sparse-solver material is exactly what this rests on.*

> [!note] ⚠️ The gauge freedom is §1's ambiguity, generalized
> | unrecoverable degree of freedom | DoF |
> |---|---|
> | global translation | 3 |
> | global rotation | 3 |
> | **global scale** | **1** |
> | **total** | **7 (a similarity transform)** |
>
> ⇒ **SfM reconstructs a scene up to a 7-DoF similarity. One known distance in the scene fixes the scale; nothing in the images can** — §1, restated for $n$ views.

**Multi-view stereo** then computes dense depth given the now-known poses; the modern pipeline is **SfM → MVS → mesh**, and COLMAP is the standard implementation.

### 5. ⚠️ Neural rendering: NeRF and what displaced it

**NeRF (Mildenhall et al. 2020)** represents a scene as an MLP $(\mathbf x,\mathbf d)\mapsto(\text{colour},\sigma)$ and renders by **casting a ray per pixel, sampling points along it, querying the MLP at each, and integrating.**

> [!warning] ⚠️ 122,880,000 MLP EVALUATIONS PER RENDERED FRAME
> $800\times800$ pixels × 192 samples per ray = **122.88 million forward passes for one image.**
>
> | target | evaluations/second |
> |---|---|
> | 1 frame | 122,880,000 |
> | **30 fps** | **3,686,400,000** |
>
> ⇒ ***that number, not any quality argument, is why 3D Gaussian splatting (Kerbl et al. 2023) displaced NeRF for real-time use***: it **rasterizes explicit 3D Gaussians with no network in the rendering loop at all.**
>
> **The trade is representation:**
>
> | | representation | size |
> |---|---|---|
> | NeRF | **implicit** — a function | ~5 MB of MLP weights |
> | 3D Gaussian splatting | **explicit** — a primitive soup | hundreds of MB |

> [!warning] ⚠️ AND THE CONCEPTUAL POINT, WHICH IS WHY NeRF IS WORTH TEACHING
> **NeRF's training set is one scene and its output is the weights.** It does not generalize to other scenes and is **not meant to**. ⇒ ***it is an optimization dressed as learning*** — the network is a *representation* being fitted, not a model being trained.
>
> **And its loss is photometric reprojection error — classical multi-view stereo's objective, exactly.** *So the "neural" part is the representation, not the objective: §4's problem with the parameterization swapped.* **Recognizing that is what stops NeRF from looking like magic.**

### 6. ⚠️ The common thread — and the subject's closing result

| method | how it recovers the $Z$ that [[01 - Introduction and Image Formation|ch. 01]] destroyed |
|---|---|
| **stereo** | two views + known baseline → triangulate |
| **structure from motion** | many views, unknown poses → solve jointly |
| **multi-view stereo** | many views, **known** poses → dense depth |
| **monocular depth (learned)** | **a prior over object sizes — not a measurement** |
| **time of flight / LiDAR** | **measure $Z$ directly, bypassing vision** |
| **NeRF / splatting** | optimize a 3D field to explain all views |

> [!warning] ⚠️ FOURTEEN WEEKS, ONE EQUATION
> **[[01 - Introduction and Image Formation|Week 1]] §3 stated it in one line: $x=fX/Z$ maps every point on a ray to the same pixel, so $Z$ is destroyed.**
>
> **Every method in this chapter is an answer to that line** — and ***exactly one of them (LiDAR) measures depth. Every other one infers it, from a second view, from many views, or from a prior.***
>
> ⇒ **when a 3D system reports a depth, the first question is which row of that table produced it**, because the failure modes are completely different: **stereo fails on texture and at range (§3), SfM fails on scale (§4), monocular fails on unusual objects (§1), and LiDAR fails on reflective and transparent surfaces.** *Not one of them fails in a way the others do.*

### 7. Emerging topics: what the foundation-model shift actually changed

| | [[03 - Image Classification and Linear Models|ch. 03]]–[[09 - Segmentation|09]] | foundation-model era |
|---|---|---|
| classes | fixed $K$; **retrain to add one** | **open vocabulary** (text) |
| segmentation | trained per dataset | **SAM: promptable, zero-shot** |
| labels needed | millions, per task | few or none |
| the model | **trained** by you | **adapted** by you |

> [!warning] ⚠️ THE PATTERN THE WHOLE SUBJECT HAS BEEN TRACING
> | | |
> |---|---|
> | [[02 - Classical Image Processing\|ch. 02]] → [[04 - From Neural Networks to CNNs\|04]] | hand-designed **features** → learned features |
> | [[07 - Object Detection I\|ch. 07]] → [[08 - Object Detection II\|08]] | hand-designed **pipeline stages** (anchors, NMS) → learned end-to-end |
> | [[12 - Self-Supervised Learning\|ch. 12]] → ch. 14 | task-specific **training** → task-specific **prompting** |
>
> ***Each step deletes a human-specified component.*** **What remains is the architecture, the objective, and the data** — and [[12 - Self-Supervised Learning|ch. 12]] §6 showed **the data is now unaudited**, which is where the open problems have moved. *[[10 - Pose Estimation and Faces|Ch. 10]] §4 and [[13 - Generative Models|ch. 13]] §3 are two concrete instances of that same shift.*

**Other current directions**, named for orientation rather than covered: **open-vocabulary detection and segmentation** (CLIP embeddings as the classifier, [[12 - Self-Supervised Learning|ch. 12]] §6's mechanism applied to [[08 - Object Detection II|ch. 08]]'s task); **vision-language models** for captioning and VQA; **embodied vision** and robot policies; **efficiency** — quantization, distillation, on-device inference; and **3D generation**, which joins [[13 - Generative Models|ch. 13]] to this chapter.

## ✏️ Exercises

> [!example]- Exercise 1 — what one image cannot say
> **(a)** Show $x$ is unchanged when the scene scales by $s$. **(b)** Give a concrete pair of scenes. **(c)** What, then, does a monocular depth network output? **(d)** When does that fail?
>
> ---
> **(a)** $x'=f\dfrac{sX}{sZ}=f\dfrac XZ$ — **the $s$ cancels identically.** Verified at $s=0.5,1,2,100$: all give **160.0000 px.**
>
> **(b)** ⚠️ **A toy car at 50 cm and a real car at 10 m** produce the identical image.
>
> **(c)** **Relative depth**, or absolute depth only from **learned object sizes** — ⚠️ **a prior, not a measurement.**
>
> **(d)** **On anything whose size violates the prior**: scale models, unusual objects, photographs of photographs, unfamiliar domains. **It fails silently**, producing a confident number — which is why the distinction in (c) is a safety property, not a technicality.

> [!example]- Exercise 2 — the epipolar constraint
> **(a)** Candidates with and without it, at 640×480. **(b)** DoF of $\mathbf F$ and why. **(c)** What does $\mathbf E$ add? **(d)** Why rectify?
>
> ---
> **(a)** **307,200** → **640**, a **480×** reduction, **exact geometry rather than an approximation.**
>
> **(b)** **7**: $3\times3$ = 9 entries, minus 1 for scale, minus 1 for $\det\mathbf F=0$.
>
> **(c)** **Known intrinsics** ⇒ **5 DoF**: rotation (3) + translation *direction* (2). ⚠️ **Translation's magnitude is Exercise 1's missing scale** — even calibrated two-view geometry cannot supply it.
>
> **(d)** **Rectification makes epipolar lines horizontal scanlines**, so the 1D search is memory-contiguous and implementable as a simple scan. Every practical pipeline does it first.

> [!example]- Exercise 3 — the quadratic law
> $f=800$ px, $B=0.20$ m, $\pm0.25$ px. **(a)** Derive $|\Delta Z|$. **(b)** Error at 2, 10 and 100 m. **(c)** Why not just widen the baseline? **(d)** What follows for sensor choice?
>
> ---
> **(a)** $Z=fB/d$ ⇒ $\frac{dZ}{dd}=-\frac{fB}{d^2}$; substituting $d=fB/Z$ gives $|\Delta Z|=\dfrac{Z^2}{fB}|\Delta d|$ — ⚠️ **quadratic in depth.**
>
> **(b)** **0.63 cm (0.31%)**, **15.6 cm (1.56%)**, **15.63 m (15.62%)**. ⚠️ **Five times the distance is twenty-five times the error**, and the *relative* error grows linearly, so accuracy degrades without limit.
>
> **(c)** ⚠️ **It is self-limiting**: a wider baseline means **fewer shared pixels, more occlusion and a harder correspondence problem**, because the views look less alike — **trading a computable error for an uncomputable one.**
>
> **(d)** **LiDAR/radar error is roughly constant with range; stereo's is quadratic.** ⇒ **at 100 m this rig is ±15.6 m, and no tuning fixes an exponent.** *The camera-versus-LiDAR argument in autonomous driving is this table.*

> [!example]- Exercise 4 — NeRF's cost
> **(a)** MLP evaluations for one $800\times800$ frame at 192 samples/ray. **(b)** For 30 fps. **(c)** What displaced it, and how? **(d)** In what sense is NeRF not "learning"?
>
> ---
> **(a)** $800\times800\times192=\mathbf{122{,}880{,}000}$.
>
> **(b)** $\mathbf{3{,}686{,}400{,}000}$ per second.
>
> **(c)** **3D Gaussian splatting** — it **rasterizes explicit 3D Gaussians with no network in the rendering loop.** The trade is **implicit and compact (~5 MB of weights) versus explicit and large (hundreds of MB of primitives).**
>
> **(d)** ⚠️ **Its training set is one scene and its output is the weights.** It does not generalize and is not meant to — **an optimization dressed as learning**, whose loss is **photometric reprojection error, i.e. classical multi-view stereo's objective exactly.** *The "neural" part is the representation, not the objective.*

> [!example]- Exercise 5 — closing the subject
> **(a)** Which week-1 fact does this chapter answer? **(b)** List the ways of recovering $Z$ and say which *measures* it. **(c)** Why does the distinction matter operationally? **(d)** State the pattern the subject traced from ch. 02 to ch. 14.
>
> ---
> **(a)** ⚠️ **[[01 - Introduction and Image Formation|Ch. 01]] §3: $x=fX/Z$ maps every point on a ray to the same pixel — $Z$ is destroyed.**
>
> **(b)** Stereo (two views + baseline), SfM (many views, poses unknown), MVS (poses known), monocular (a **prior**), **LiDAR/ToF (measures $Z$ directly)**, NeRF/splatting (optimize a field). ⚠️ ***Exactly one measures; the rest infer.***
>
> **(c)** **Because the failure modes do not overlap**: stereo fails on texture and at range, SfM on scale, monocular on unusual objects, LiDAR on reflective and transparent surfaces. ⇒ **when a system reports a depth, ask which row produced it.**
>
> **(d)** **Hand-designed features → learned features → learned pipelines → prompting.** ***Each step deletes a human-specified component***, leaving the architecture, the objective and the data — **and the data is now unaudited**, which is where the open problems moved.

## 📝 Summary

- **⚠️ Monocular scale ambiguity is exact**: $f(sX)/(sZ)=fX/Z$ for every $s$, so **a toy car at 50 cm and a real car at 10 m give the identical image.** A monocular depth network therefore reports **a prior over object sizes, not a measurement** — and it fails silently when the prior is wrong.
- **The epipolar constraint turns a 2D search into a 1D one**: 307,200 candidates → **640**, a **480× reduction, by exact geometry.** $\mathbf F$ has **7 DoF**, $\mathbf E$ has **5** — and $\mathbf E$'s missing 6th is translation's *magnitude*, i.e. the same missing scale.
- **⚠️ Stereo depth error is quadratic in depth: $|\Delta Z|=\frac{Z^2}{fB}|\Delta d|$** — **0.16% at 1 m, 1.56% at 10 m, 15.62% (±15.6 m) at 100 m.** ⚠️ **Widening the baseline is self-limiting** (fewer shared pixels, more occlusion, harder matching). ⇒ **long-range perception uses LiDAR or radar, whose error is constant with range.**
- **SfM jointly solves poses and points** (150,600 unknowns for 100 cameras and 50,000 points), **tractable only because the Jacobian is sparse**, and recovers the scene **up to a 7-DoF similarity — 3 translation, 3 rotation, 1 scale.** *One known distance fixes the scale; nothing in the images can.*
- **⚠️ NeRF needs 122,880,000 MLP evaluations per $800^2$ frame** — 3.69 billion/s for 30 fps — **which is why 3D Gaussian splatting displaced it for real-time use** by rasterizing explicit primitives instead. **NeRF is an optimization dressed as learning**: one scene, weights as output, and photometric reprojection error — *classical MVS's objective exactly.*
- **⚠️ Every method here answers one line from week 1 — $x=fX/Z$ destroys $Z$ — and exactly one of them (LiDAR) *measures* depth; all the others infer it.** **Their failure modes do not overlap**, so the first question about any reported depth is which method produced it.
- **The subject's arc: hand-designed features → learned features ([[02 - Classical Image Processing|ch. 02]]→[[04 - From Neural Networks to CNNs|04]]) → learned pipelines ([[07 - Object Detection I|ch. 07]]→[[08 - Object Detection II|08]]) → prompting ([[12 - Self-Supervised Learning|ch. 12]]→14).** **Each step deletes a human-specified component**, leaving architecture, objective and data — **and the data is now unaudited.**

## ⚠️ Important Notes

1. **⚠️ Always ask which method produced a depth number.** Measured (LiDAR) and inferred (everything else) fail completely differently, and a depth map does not record its provenance.
2. **⚠️ Quote a stereo rig's accuracy *with its range*.** "±2 cm" is meaningless alone: this rig is ±0.16 cm at 1 m and ±15.6 m at 100 m. **The specification is a curve, not a number.**
3. **⚠️ Sub-pixel disparity matters quadratically.** Improving $|\Delta d|$ from 1 px to 0.25 px is a **4× depth improvement at every range** — usually cheaper than a longer baseline and with no occlusion cost.
4. **⚠️ A monocular network's absolute depths are unverifiable from the image.** If you need metric depth, **you need a second view, a known baseline, a known object size, or a range sensor.** No architecture supplies it.
5. **⚠️ SfM output has arbitrary scale.** Measurements from a reconstruction are ratios until a known distance is supplied. **Anyone quoting metres from a pure SfM pipeline has assumed something they did not state.**
6. **⚠️ Correspondence is where two-view geometry actually fails.** The matrices are exact; the matches are not. **Textureless regions, repeated patterns and specular surfaces defeat them** — [[11 - Video and Motion|ch. 11]] §2's structure tensor decides this, and it is the same $2\times2$ matrix.
7. **NeRF and splatting are scene representations, not models.** Training one tells you nothing about another scene; **budget them as reconstruction jobs, not as training runs.**
8. **⚠️ "Zero-shot" is not "no assumptions".** SAM and open-vocabulary models moved the supervision into an unaudited pre-training set ([[12 - Self-Supervised Learning|ch. 12]] §6). **The labels did not disappear — they became someone else's, and unexamined.**

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]) — **but ⚠️ THIS IS THE ONE CHAPTER WHERE SZELISKI IS THE PRIMARY SOURCE**, not a reference: his ch. 11 (structure from motion) and ch. 12 (depth estimation) are the standard treatment of §§1–4, and §2.1.4 covers projection. *The reverse of [[12 - Self-Supervised Learning|ch. 12]] and [[13 - Generative Models|ch. 13]], where the book was thinnest. **Worth recording as a scope note: the textbook's strength is exactly the half the lecturer de-emphasised** (see [[00-Index]]'s scope decision).*
>
> **§§5–7 are outside the book**: **Mildenhall et al. 2020 (NeRF)**, **Kerbl et al. 2023 (3D Gaussian splatting)**, **Kirillov et al. 2023 (SAM)**, plus §13.5 for neural rendering, which the second edition covers only briefly and which predates splatting entirely.
>
> ⚠️ **The "emerging topics" half of this week is the least determined part of the whole course.** The lecturer's title is *"3D vision & emerging topics"* with no further specification, and **"emerging" is a moving target** — §7 therefore states the *pattern* (each step deletes a human-specified component) rather than surveying a list that will date. **If the course covers specific recent systems, this chapter names them only in passing.**
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§3's error table and the framing of $|\Delta Z|=\frac{Z^2}{fB}|\Delta d|$ as *the* defining limit.** *The formula is standard and in Szeliski; **tabulating it to 100 m, showing the baseline dial is self-limiting, and drawing the LiDAR conclusion is the addition.***
> - **§1's scale-invariance table** and the statement that a monocular depth network reports **a prior, not a measurement** — with the failure modes that follow.
> - **§5's evaluation count** (122.88 M/frame; 3.69 G/s at 30 fps) **and the argument that it, not quality, explains splatting's adoption**; also **the characterization of NeRF as an optimization dressed as learning**, with its loss identified as classical MVS's objective.
> - **§4's parameter count and the 7-DoF gauge table.**
> - **§6's synthesis table and the "exactly one measures, the rest infer" conclusion** — ***the closing result of the subject***, and **§7's three-line arc from ch. 02 to ch. 14.**
> - **All eight Important Notes.**
>
> ⚠️ **§3's rig ($f=800$ px, $B=0.20$ m, $\pm0.25$ px) is a plausible configuration chosen to make the law concrete, not a real product's specification.** **The finding is the exponent — error $\propto Z^2$ — which is exact and configuration-independent**; the absolute metres scale with $1/(fB)$. **§5's 192 samples/ray and $800^2$ resolution are NeRF's stated evaluation settings; the 10 M evaluations/second used to convert to seconds is an illustrative rate and is labelled as such.** **§4's 100 cameras / 50,000 points are a representative problem size.**
>
> **No discrepancies found.** *(And no erratum has been filed against Szeliski in any of the four chapters that used him — see [[00-Index]]'s errata table.)*
>
> **Deliberately deferred, not omitted:** **camera calibration** (intrinsics, distortion models, Zhang's method) is assumed rather than derived — *it is essential in practice and belongs with [[01 - Introduction and Image Formation|ch. 01]]'s pinhole model*; **RANSAC**, which is what actually makes the 8-point algorithm work on real correspondences, is not covered and is arguably the single most important omission in this chapter; **point-cloud networks** (PointNet, PointNet++, sparse convolutions) are named nowhere, and a course with a robotics slant would need them; **SLAM** as a real-time system — as opposed to offline SfM — is a subject of its own; **3D generation** joins [[13 - Generative Models|ch. 13]] to this chapter and is covered in neither.
>
> **Left as the source states it:** the epipolar constraint and the DoF of $\mathbf F$, $\mathbf E$ and $\mathbf H$; the 8-point, 5-point and 4-point algorithms; $Z=fB/d$; bundle adjustment's formulation and the sparsity of its Jacobian; the SfM → MVS → mesh pipeline and COLMAP; NeRF's volume-rendering formulation and sampling scheme; splatting's rasterization approach; SAM's promptable design.

**Previous:** [[13 - Generative Models]] · **Next:** — *(week 15 is project presentations; see [[00-Index]] and `note/project_topics.md`)*
