---
subject: Computer Vision
chapter: 11
tags: [ds, computer-vision, video, optical-flow, aperture-problem, 3d-convolution, tracking, motion]
source: "Szeliski, *Computer Vision*, 2nd ed. §9.1–9.4 (motion estimation), §7.1.5; Lucas & Kanade 1981; Horn & Schunck 1981; Simonyan & Zisserman 2014 (two-stream); Tran et al. 2018 ((2+1)D); Bewley et al. 2016 (SORT); the lecturer's course outline"
---

# Video and Motion

**Week 11 of 14. ⚠️ NO SLIDES** — see [[00-Index]].

**Four results.**

**§2 — ⚠️ THE APERTURE PROBLEM IS *ONE EQUATION IN TWO UNKNOWNS*, AND THE MATRIX THAT FIXES IT IS [[02 - Classical Image Processing|ch. 02]]'S HARRIS STRUCTURE TENSOR — THE SAME $2\times2$ MATRIX, SOLVED FOR A DIFFERENT REASON.** Verified on three synthetic windows: a flat region gives $\lambda_{\min}=\lambda_{\max}=0$, **a single edge gives $\lambda_{\min}=0$ with $\lambda_{\max}=123{,}750$ — rank 1, still unsolvable** — and only a corner gives both eigenvalues large. ⇒ ***trackers track corners because corners are the only points where the flow equation has a unique solution.***

**§5 — ⚠️ IDENTITY ERRORS COMPOUND AND DETECTION ERRORS DO NOT — AND 99% PER-FRAME ASSOCIATION IS *CATASTROPHIC*.** A track survives with probability $p^T$: **73.97% for one second, 4.90% for ten, $1.4\times10^{-6}\%$ for one minute.** Holding a one-minute track with 95% probability needs $p\ge0.999972$ — **351× stricter.** *Second chapter running for this arithmetic: it is [[10 - Pose Estimation and Faces|ch. 10]]'s gallery-FAR compounding in the time dimension.*

**§3 — ⚠️ (2+1)D FACTORISATION SAVES 2.25× AT $3\times3\times3$ AND THE SAVING IS NOT THE POINT** — it inserts a nonlinearity between the spatial and temporal halves, so it has **more nonlinearity at a smaller parameter budget.** Same algebra as [[05 - CNN Architectures|ch. 05]]'s depthwise separable convolution: *factorising a joint operation into two marginal ones.*

**§1 — ⚠️ A TEN-SECOND CLIP IS 172.27 MB AS FLOAT32, FOR ONE EXAMPLE** — and consecutive frames are nearly identical, so **most of that volume carries no new information.** Both facts point the same way: sample frames, don't process them all.

## 📘 Main Knowledge

### 1. Video is a data-volume problem before it is a modelling problem

| clip | frames | values | fp32 |
|---|---|---|---|
| single image | 1 | 150,528 | 0.57 MB |
| 1 s @ 30 fps | 30 | 4,515,840 | 17.23 MB |
| **10 s @ 30 fps** | 300 | 45,158,400 | **172.27 MB** |
| 1 min @ 30 fps | 1,800 | 270,950,400 | 1,033.59 MB |

**A realistic batch of 8 clips × 16 frames is 73.5 MB of *input alone*** — and by [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5 every intermediate activation is retained for the backward pass, on top of that. **Batch size is the first casualty; video models train with batches that would be absurd for images.** *This is [[05 - CNN Architectures|ch. 05]] §3's finding — input resolution is the most expensive hyperparameter — with a third dimension added.*

> [!note] ⚠️ Redundancy is the other half, and it cancels much of the cost
> **Consecutive frames are nearly identical.** At 30 fps a point moving 100 px/s moves **3.33 px** between frames; at 60 fps, **1.67 px**.
>
> ⇒ ***the marginal information per frame is tiny***, which is why clip models sample **16–32 frames** rather than all 300, and why sparse sampling (TSN) works nearly as well as dense. **The video is large; the *content* is not.**

### 2. ⚠️ Optical flow, and why it is underdetermined

**Optical flow** assigns a displacement $(u,v)$ to each pixel. It rests on **brightness constancy** — a point keeps its intensity as it moves:

$$I(x,y,t)=I(x+u\,\delta t,\;y+v\,\delta t,\;t+\delta t)$$

A first-order Taylor expansion gives the **optical flow constraint equation**:

$$I_x u + I_y v + I_t = 0$$

> [!warning] ⚠️ THAT IS ONE LINEAR EQUATION IN TWO UNKNOWNS — A *LINE* OF SOLUTIONS, NOT A POINT
> With $I_x=2$, $I_y=1$, $I_t=-3$ the constraint is $2u+v=3$, and **every point on that line is equally consistent with the local evidence:**
>
> | $u$ | $v$ | $I_xu+I_yv+I_t$ |
> |---|---|---|
> | 0.00 | 3.00 | 0 |
> | 0.50 | 2.00 | 0 |
> | 1.00 | 1.00 | 0 |
> | 1.50 | 0.00 | 0 |
>
> **Only the component along the gradient is recoverable** — the *normal flow*, $-I_t/\|\nabla I\|=1.3416$ px along $(0.8944,0.4472)$. **The component perpendicular to the gradient is invisible.**
>
> ⇒ ***a moving edge seen through a small window appears to move only perpendicular to itself.*** **This is the aperture problem**, and it is not a limitation of any algorithm — it is a statement about what the data contains.

**The two classical fixes are the two ways to manufacture more equations:**

| method | extra assumption | result |
|---|---|---|
| **Lucas–Kanade (1981)** | flow is **constant in a window** | $N$ equations, 2 unknowns → least squares $(A^\top A)\begin{bmatrix}u\\v\end{bmatrix}=-A^\top b$ |
| **Horn–Schunck (1981)** | flow is **globally smooth** | a variational problem over the whole image |

> [!warning] ⚠️ $A^\top A$ **IS** THE HARRIS STRUCTURE TENSOR — FLOW AND CORNER DETECTION ARE THE SAME MATRIX
> Built $A^\top A$ for three synthetic windows and read its eigenvalues:
>
> | window | $\lambda_{\min}$ | $\lambda_{\max}$ | solvable? |
> |---|---|---|---|
> | flat region | 0.0000 | 0.0000 | **no** |
> | **single edge** | **0.0000** | **123,750** | **no — rank 1** |
> | corner / texture | 61,875 | 73,125 | **yes** |
>
> **The single edge is the instructive case**: enormous gradient energy, and still no unique solution, because all of it points one way. ⇒ **Lucas–Kanade fails exactly where Harris reports "not a corner", for exactly the same reason** — [[02 - Classical Image Processing|ch. 02]] solved this matrix to *find* corners, and flow solves it to *move* them.
>
> ⇒ ***that is why classical trackers track corners: they are the only points where the flow equation has a unique solution.*** **Two problems, one $2\times2$ matrix, discovered independently a decade apart** — *the third instance in this subject of a single operator being reached by separate routes ([[04 - From Neural Networks to CNNs|ch. 04]] §4's convolution was the first).*

**Deep flow networks** (FlowNet, RAFT) learn the correspondence instead, using a **cost volume** — correlations between features at candidate displacements. **They do not repeal the aperture problem**; they resolve it with learned priors about what motions are plausible, which is the same trick as Horn–Schunck's smoothness with the prior learned rather than assumed.

### 3. ⚠️ Temporal modelling: 3D convolution and the (2+1)D factorisation

**The direct approach is to convolve over $(t,h,w)$** — a $3\times3\times3$ kernel instead of $3\times3$, which is exactly **3× the parameters and 3× the arithmetic** for the same spatial extent (verified at $k=3,5,7$).

**(2+1)D** (Tran et al. 2018) splits it into a **spatial $1\times k\times k$** followed by a **temporal $k_t\times1\times1$**:

| kernel | 3D: $k_tk_hk_w$ | (2+1)D: $k_hk_w+k_t$ | saving |
|---|---|---|---|
| **$3\times3\times3$** | 27 | 12 | **2.25×** |
| $3\times5\times5$ | 75 | 28 | 2.68× |
| $3\times7\times7$ | 147 | 52 | 2.83× |
| $5\times3\times3$ | 45 | 14 | 3.21× |
| $7\times3\times3$ | 63 | 16 | 3.94× |
| $5\times5\times5$ | 125 | 30 | 4.17× |

> [!warning] ⚠️ THE SAVING IS THE *LESSER* BENEFIT
> The ratio $\dfrac{k_tk_hk_w}{k_hk_w+k_t}$ is **exactly the shape of [[05 - CNN Architectures|ch. 05]] §1's depthwise-separable formula**, and for the identical reason: **factorising a joint operation into two marginal ones.**
>
> **But the real gain is nonlinearity.** The factorisation inserts a ReLU *between* the spatial and temporal halves, so **(2+1)D has more nonlinearity than 3D at a smaller parameter budget** — which is precisely VGG's argument for stacking $3\times3$ kernels ([[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §7). *Tran et al. report (2+1)D beating 3D at matched capacity; the extra nonlinearity, not the saving, is the stated cause.*

**Video transformers** (TimeSformer, ViViT) factorise the *same* way — **divided space-time attention** attends spatially, then temporally, rather than over all $n_t\cdot n_{hw}$ tokens jointly. ⚠️ **And [[06 - Vision Transformers|ch. 06]] §1's quadratic bites hard here**: video easily exceeds the $n>2d$ crossover, so **in video, unlike in $224^2$ images, attention genuinely is the dominant cost.**

### 4. Two-stream, and a hand-designed stage that was duly deleted

| stream | input | captures |
|---|---|---|
| spatial | 1 RGB frame | appearance |
| **temporal** | **~10 pre-computed optical flow fields** | motion |

**The two-stream network (Simonyan & Zisserman 2014) fed a CNN pre-computed optical flow** — *a hand-designed feature inside a learned pipeline*, which is [[02 - Classical Image Processing|ch. 02]] §11's pattern and [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §9's deletion list exactly. **It was duly deleted**: 3D convolutions and video transformers learn motion from RGB directly.

> [!note] The honest counterpoint
> **Optical flow is still used where data is scarce**, because it is a strong prior that needs no learning at all. *Same argument as classical features surviving in geometry — a hand-designed stage is deleted when there is enough data to replace it, not because it was wrong.*

### 5. ⚠️ Tracking: the assignment problem again, and errors that compound

**Tracking-by-detection**: run a detector per frame, then **associate** detections across frames. Association is **bipartite matching — [[08 - Object Detection II|ch. 08]] §5's Hungarian algorithm, a third appearance** (DETR, face galleries, now tracks):

| objects $n$ | brute-force $n!$ | Hungarian $O(n^3)$ |
|---|---|---|
| 5 | $1.2\times10^2$ | 125 |
| 10 | $3.6\times10^6$ | 1,000 |
| 20 | $2.4\times10^{18}$ | 8,000 |
| 50 | $3.0\times10^{64}$ | 125,000 |

**SORT** uses a Kalman filter for motion prediction and IoU for the cost; **DeepSORT** adds an appearance embedding — *which is [[10 - Pose Estimation and Faces|ch. 10]] §5's face embedding doing re-identification.*

> [!warning] ⚠️ IDENTITY ERRORS COMPOUND; DETECTION ERRORS DO NOT
> If per-frame association is correct with probability $p$, a track survives $T$ frames intact with probability $p^T$:
>
> | $p$ | $T=30$ (1 s) | $T=300$ (10 s) | $T=1800$ (1 min) |
> |---|---|---|---|
> | **0.99** | **73.97%** | **4.90%** | $1.4\times10^{-6}\%$ |
> | 0.999 | 97.04% | 74.07% | 16.52% |
> | 0.9999 | 99.70% | 97.04% | 83.53% |
>
> **99% per-frame association — which sounds strong — keeps a track intact for one second with probability 73.97% and for one minute with probability $1.4\times10^{-6}\%$.** To hold a one-minute track with 95% probability you need $p\ge0.999972$, an error rate below $2.85\times10^{-5}$ per frame — **351× stricter than 1%.**
>
> ⇒ ***a missed detection is local and self-repairing — the object is found again next frame. An identity switch is permanent: every subsequent frame inherits the wrong label.***
>
> **That is why MOT metrics (MOTA, IDF1, HOTA) count identity switches separately from misses and false positives** — they are not comparable error types, because only one of them compounds. **And it is [[10 - Pose Estimation and Faces|ch. 10]] §4's gallery arithmetic in the time dimension: $1-(1-\varepsilon)^N$ over people, $p^T$ over frames — the same compounding, two chapters running.**

## ✏️ Exercises

> [!example]- Exercise 1 — the aperture problem
> **(a)** Derive $I_xu+I_yv+I_t=0$ from brightness constancy. **(b)** With $I_x=2$, $I_y=1$, $I_t=-3$, give three consistent flows. **(c)** What *is* recoverable? **(d)** What do Lucas–Kanade and Horn–Schunck each add?
>
> ---
> **(a)** $I(x,y,t)=I(x+u\delta t,y+v\delta t,t+\delta t)$; expand the right side to first order: $I+I_xu\delta t+I_yv\delta t+I_t\delta t$. Equate and divide by $\delta t$ ⇒ $I_xu+I_yv+I_t=0$.
>
> **(b)** $2u+v=3$: $(0,3)$, $(0.5,2)$, $(1,1)$ — **all exactly consistent.** ⚠️ **One equation, two unknowns: a line of solutions.**
>
> **(c)** **Only the normal flow** — the component along $\nabla I$: $-I_t/\|\nabla I\|=\mathbf{1.3416}$ px along $(0.8944,0.4472)$. **The tangential component is invisible**, so a moving edge appears to move perpendicular to itself.
>
> **(d)** **Both manufacture equations.** LK assumes flow is **constant in a window** ($N$ equations, 2 unknowns, least squares); HS adds a **global smoothness penalty**. *Neither repeals the ambiguity — they add an assumption that resolves it, and deep flow networks do the same with a learned prior.*

> [!example]- Exercise 2 — where Lucas–Kanade fails
> **(a)** Write $A^\top A$ for a window. **(b)** Its eigenvalues for a flat region, a single edge, a corner. **(c)** Why does a single edge fail despite huge gradients? **(d)** What is this matrix, elsewhere in the subject?
>
> ---
> **(a)** $A^\top A=\begin{bmatrix}\sum I_x^2 & \sum I_xI_y\\ \sum I_xI_y & \sum I_y^2\end{bmatrix}$ over the window.
>
> **(b)** Measured: flat **(0.0000, 0.0000)**; single edge **(0.0000, 123,750)**; corner **(61,875, 73,125)**.
>
> **(c)** ⚠️ **Because rank, not magnitude, is what matters.** An edge has enormous gradient energy all pointing *one way*, so $A^\top A$ is **rank 1** and the system is still underdetermined — every row of $A$ is a multiple of the same direction, so $N$ equations carry the information of one. **Motion along the edge is unobservable.**
>
> **(d)** ⚠️ **It is [[02 - Classical Image Processing|ch. 02]]'s Harris structure tensor** — the same $2\times2$ matrix, solved to *find* corners rather than to *move* them. ⇒ **classical trackers track corners because corners are the only points where flow has a unique solution.**

> [!example]- Exercise 3 — (2+1)D
> **(a)** Cost of $3\times3\times3$ vs (2+1)D. **(b)** At $5\times5\times5$. **(c)** Give the general ratio and say what else it resembles. **(d)** Why is the saving *not* the main benefit?
>
> ---
> **(a)** $27$ vs $9+3=12$ ⇒ **2.25×**.
>
> **(b)** $125$ vs $25+5=30$ ⇒ **4.17×** — *larger kernels save more.*
>
> **(c)** $\dfrac{k_tk_hk_w}{k_hk_w+k_t}$ — **exactly the shape of [[05 - CNN Architectures|ch. 05]] §1's depthwise-separable saving**, and for the same reason: **factorising a joint operation into two marginal ones.**
>
> **(d)** ⚠️ **Because it inserts a nonlinearity between the spatial and temporal halves.** (2+1)D has **more nonlinearity than 3D at a smaller parameter budget** — VGG's $3\times3$-stacking argument, in time. *That, not the FLOP count, is why it wins at matched capacity.*

> [!example]- Exercise 4 — why identity switches are counted separately
> Per-frame association is correct with $p=0.99$. **(a)** Probability a track survives 30, 300, 1800 frames. **(b)** What $p$ holds a 1-minute track 95% of the time? **(c)** Why do MOT metrics separate ID switches from misses? **(d)** What does this rhyme with?
>
> ---
> **(a)** $0.99^T$: **73.97%**, **4.90%**, $\mathbf{1.4\times10^{-6}\%}$.
>
> **(b)** $p\ge0.95^{1/1800}=\mathbf{0.999972}$ — error below $2.85\times10^{-5}$ per frame, **351× stricter than 1%.**
>
> **(c)** ⚠️ **Because only one of them compounds.** A missed detection is **local and self-repairing** — the object is redetected next frame. **An identity switch is permanent**: every subsequent frame inherits the wrong label. **Averaging them into one score hides the error type that destroys the output.**
>
> **(d)** **[[10 - Pose Estimation and Faces|Ch. 10]] §4's gallery FAR**: $1-(1-\varepsilon)^N$ over people, $p^T$ over frames. **Same compounding, two chapters running** — *whenever a per-unit error rate is applied repeatedly, quote the compounded number, not the per-unit one.*

## 📝 Summary

- **Video is a volume problem first**: a 10-second clip is **172.27 MB** as float32 and a modest 8×16 batch is 73.5 MB of input before activations — **batch size is the first casualty.** But **consecutive frames are nearly identical** (3.33 px of motion at 30 fps for a 100 px/s point), so **sparse frame sampling loses little** and clip models use 16–32 frames, not 300.
- **⚠️ Optical flow's constraint $I_xu+I_yv+I_t=0$ is one equation in two unknowns**, so local flow is undetermined — **only the normal flow (along $\nabla I$) is recoverable**, and a moving edge appears to move perpendicular to itself. **Lucas–Kanade and Horn–Schunck both manufacture equations** (a constant-flow window; a global smoothness penalty).
- **⚠️ $A^\top A$ is the Harris structure tensor.** Flat: $(0,0)$; **single edge: $(0,\,123{,}750)$ — rank 1, still unsolvable despite huge gradients**; corner: $(61{,}875,\,73{,}125)$. ⇒ **trackers track corners because corners are the only points where flow has a unique solution** — one matrix, two problems, found a decade apart.
- **3D convolution costs 3× a 2D one; (2+1)D recovers 2.25× at $3\times3\times3$** (4.17× at $5\times5\times5$) — **[[05 - CNN Architectures|ch. 05]]'s depthwise-separable algebra** — and **the real benefit is the nonlinearity inserted between the spatial and temporal halves**, not the saving. Video transformers factorise space-time attention the same way, **and in video the quadratic genuinely dominates.**
- **Two-stream fed pre-computed optical flow to a CNN** — a hand-designed stage inside a learned pipeline, **duly deleted** by 3D convs and video transformers. *It survives where data is scarce, because it is a prior that needs no learning.*
- **⚠️ Tracking-by-detection's association is Hungarian matching (third appearance), and identity errors compound: $p^T$.** At $p=0.99$ a track survives 1 s with probability **73.97%**, 10 s with **4.90%**, 1 min with $1.4\times10^{-6}\%$; a 95% one-minute track needs $p\ge0.999972$, **351× stricter.** ⇒ **a miss is local and self-repairing; an ID switch is permanent** — hence MOT metrics count them separately.

## ⚠️ Important Notes

1. **⚠️ Quote the compounded error, never the per-unit one.** $p^T$ over frames, $1-(1-\varepsilon)^N$ over a gallery — **two chapters running.** A "99% accurate" per-frame associator is a **4.90%** ten-second tracker.
2. **⚠️ Rank, not magnitude, decides whether flow is solvable.** A strong edge has $\lambda_{\max}=123{,}750$ and $\lambda_{\min}=0$. **Check $\lambda_{\min}$ (or the condition number), never the gradient energy** — this is also the correct confidence measure to attach to a flow estimate.
3. **⚠️ Brightness constancy fails on exactly the things that matter**: illumination changes, specular highlights, occlusion, and objects entering or leaving. **Flow at an occlusion boundary is not merely inaccurate — it is undefined**, because the point has no correspondence.
4. **⚠️ Large motions break the linearisation.** The constraint is a *first-order* Taylor expansion, valid for sub-pixel displacement. **Coarse-to-fine pyramids exist for this reason** — the same displacement is sub-pixel at a lower resolution.
5. **⚠️ Do not benchmark a video model on frame-level accuracy.** A model that ignores time entirely can score well on datasets where a single frame determines the label — **and much of early action recognition was exactly that.** *[[08 - Object Detection II|Ch. 08]]'s "name the protocol" applied to video: ask what a temporally-blind baseline scores.*
6. **⚠️ In video, attention's quadratic is real.** [[06 - Vision Transformers|Ch. 06]] §1 found attention is only 36.1% of the work at $224^2$; **video passes the $n>2d$ crossover easily**, so factorised or windowed attention is a necessity here rather than an optimisation.
7. **Kalman filtering assumes linear motion with Gaussian noise.** It works because objects mostly move smoothly at 30 fps — **and fails on abrupt direction changes and long occlusions**, which is where appearance embeddings (DeepSORT) earn their cost.
8. **Frame sampling is a hyperparameter, not a detail.** 16 frames from 300 is a 19× reduction; **the right stride depends on the motion timescale of the action**, and a fast action sampled sparsely is simply absent from the input.

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). Built from **Szeliski §9.1–9.4 (motion estimation, translational alignment, parametric motion, optical flow)** and §7.1.5, plus **Lucas & Kanade (1981)**, **Horn & Schunck (1981)**, **two-stream (Simonyan & Zisserman 2014)**, **(2+1)D (Tran et al. 2018)**, **SORT/DeepSORT (Bewley et al. 2016; Wojke et al. 2017)** and CS231n.
>
> **⚠️ The balance is inferred.** The lecturer's topic title is *"Video & motion"*. **Szeliski treats classical motion estimation at length and video deep learning barely at all**, so this chapter deliberately gives the classical half its full derivation (§2) and the learned half a compressed treatment (§3–4) — **the reverse of what the slide-7 "deep-learning-focused" framing would suggest.** *The justification is that §2's result is a permanent fact about the data and §3's architectures are not; but if the course emphasises action recognition benchmarks, this chapter under-serves it.*
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§2's eigenvalue experiment** — building $A^\top A$ for a flat region, a single edge and a corner, and **identifying it as the Harris structure tensor.** *That LK needs texture is standard; **the numerical demonstration that a strong edge gives $\lambda_{\min}=0$ with $\lambda_{\max}=123{,}750$, and the conclusion that flow and corner detection are one matrix, is the addition.*** **Third instance in this subject of one operator reached by independent routes.**
> - **§5's compounding table and the 351× figure**, and **the identification with [[10 - Pose Estimation and Faces|ch. 10]] §4's gallery arithmetic** — the reason MOT metrics separate ID switches from misses is usually stated as a convention; here it is derived.
> - **§3's factorisation table** and the identification of $\frac{k_tk_hk_w}{k_hk_w+k_t}$ with the depthwise-separable ratio.
> - **§1's volume table and the redundancy calculation.**
> - **All eight Important Notes.**
>
> ⚠️ **The three windows in §2 are synthetic (a constant patch, a step edge, an L-shaped corner), not real image crops** — the eigenvalue *magnitudes* depend on the constructed contrast (50 vs 200) and are not meaningful on their own. **The finding is the rank structure — $\lambda_{\min}=0$ for both the flat region and the edge — which is contrast-independent.**
>
> ⚠️ **No accuracy figures from any video paper are quoted.** (2+1)D's reported advantage over 3D at matched capacity is stated qualitatively and attributed; **the parameter counts in §3 are exact arithmetic, the accuracy claim is theirs.**
>
> **No discrepancies found.**
>
> **Deliberately deferred, not omitted:** **video generation and prediction** are [[13 - Generative Models|ch. 13]]; **temporal self-supervision** (predicting frame order, tracking as a pretext task) is [[12 - Self-Supervised Learning|ch. 12]]; **structure from motion**, which uses the same correspondences for geometry rather than motion, is [[14 - 3D Vision and Emerging Topics|ch. 14]]. **Video compression** (motion vectors, which are optical flow computed by codecs and freely available at decode time) is mentioned nowhere in the course and would be a genuinely useful practical addition.
>
> **Left as the source states it:** Lucas–Kanade's and Horn–Schunck's formulations and 1981 dates; the two-stream architecture; FlowNet/RAFT's cost-volume approach; SORT's Kalman-plus-IoU design; the MOTA/IDF1/HOTA metric family.

**Previous:** [[10 - Pose Estimation and Faces]] · **Next:** [[12 - Self-Supervised Learning]]
