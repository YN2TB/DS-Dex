---
subject: Computer Vision
chapter: 13
tags: [ds, computer-vision, generative-models, gan, vae, diffusion, stable-diffusion, fid, text-to-image]
source: "Szeliski, *Computer Vision*, 2nd ed. §5.5.4; Goodfellow et al. 2014 (GAN); Kingma & Welling 2014 (VAE); Arjovsky & Bottou 2017; Ho et al. 2020 (DDPM); Song et al. 2021 (DDIM); Rombach et al. 2022 (latent diffusion); Ho & Salimans 2022 (classifier-free guidance); Heusel et al. 2017 (FID); the lecturer's course outline"
---

# Generative Models

**Week 13 of 14. ⚠️ NO SLIDES** — see [[00-Index]]. **⚠️ [[Deep Learning/contents/00-Index|Deep Learning]] put generative models out of scope, so this chapter owns them outright** — there is no cross-reference to lean on.

**Four results.**

**§3 — ⚠️ A MODEL THAT MEMORIZES ITS TRAINING SET SCORES FID = 0.000000 — *PERFECT*, AND BETTER THAN A MODEL THAT GENERALIZES (1.0689).** The field's standard metric measures distributional match and is **structurally blind to novelty.** ⇒ ***FID must be reported alongside a memorization check, and this is not a benchmarking nicety — it is where the copyright and privacy questions about image generators actually live.***

**§2 — ⚠️ THE GAN's SATURATING LOSS HAS A GRADIENT *BOUNDED BY 1* EXACTLY WHEN THE GENERATOR IS LOSING.** At $D(G(z))=10^{-4}$ the saturating form gives $|{\nabla}|=1.0001$ and the non-saturating form **10,000 — a ratio of 9,999.** And with disjoint supports the JS divergence is **constant at $\log 2=0.693147$**, whose gradient is zero everywhere: ***the objective says the generator is wrong and refuses to say how wrong.***

**§4 — ⚠️ DIFFUSION BUYS AN OBJECTIVE THAT CANNOT SATURATE OR COLLAPSE, AND PAYS 1,000× AT SAMPLING TIME.** DDPM needs **1,000 network evaluations per image against a GAN's 1** — *that single ratio is why DDIM, distillation and consistency models exist.* The objective it buys is **a plain L2 regression on noise**: no adversary, no minimax.

**§5 — ⚠️ LATENT DIFFUSION'S 48× COMPRESSION IS 4,096× ON THE ATTENTION.** $512^2\times3=786{,}432$ values become $64^2\times4=16{,}384$, and attention is quadratic ⇒ **that, not a modelling advance, is what put text-to-image on one consumer GPU.**

## 📘 Main Knowledge

### 1. What "generative" means, and why the space is empty

**A $256\times256$ RGB image is a point in $\mathbb R^{196608}$**, and there are $256^{196608}\approx10^{473{,}479}$ distinct 8-bit images — *against roughly $10^{80}$ atoms in the observable universe.* **Draw uniformly from that space and you get noise, always.**

**Natural images occupy a vanishingly thin manifold inside it.** ⇒ **a generative model is a map from an easy distribution (a Gaussian) onto that manifold**, and the four families below differ **only in how the map is trained**:

| family | how it is trained | sampling |
|---|---|---|
| **VAE** | maximize a **lower bound** on likelihood | 1 pass |
| **GAN** | a **minimax game** against a discriminator | 1 pass |
| **Diffusion** | **regress the noise** added at a known step | $T$ passes |
| Autoregressive | predict the next pixel/token | $n$ passes |

### 2. ⚠️ GANs: the objective vanishes exactly when it is needed

**Goodfellow et al.'s minimax game**: $D$ distinguishes real from generated, $G$ tries to fool it. **The elegance is that the loss is *learned* rather than specified** — nobody has to write down what makes an image look real.

$$\min_G\max_D\ \mathbb E_{x\sim p_{\text{data}}}[\log D(x)]+\mathbb E_{z}[\log(1-D(G(z)))]$$

> [!warning] ⚠️ THE GENERATOR'S HALF OF THAT EQUATION HAS A GRADIENT BOUNDED BY 1
> $\frac{d}{dD}\log(1-D)=\frac{1}{D-1}$, so $|{\cdot}|\to1$ as $D\to0$; $\frac{d}{dD}(-\log D)=-\frac1D$, which diverges.
>
> | $D(G(z))$ | saturating $\left\|\frac{d}{dD}\log(1-D)\right\|$ | non-saturating $\left\|\frac{d}{dD}(-\log D)\right\|$ | ratio |
> |---|---|---|---|
> | 0.5 | 2.0000 | 2.00 | 1.00 |
> | 0.1 | 1.1111 | 10.00 | 9.00 |
> | 0.01 | 1.0101 | 100.00 | 99.00 |
> | **$10^{-4}$** | **1.0001** | **10,000** | **9,999** |
>
> **$D(G(z))$ small means the discriminator is winning — precisely when the generator most needs a signal.** ⇒ ***the saturating loss flattens out exactly there, and the non-saturating form $-\log D(G(z))$ gives 9,999× more gradient.*** **Goodfellow's own paper proposes the swap for this reason: the minimax game as *written* is not the game as *played*.**

> [!warning] ⚠️ AND THE DEEPER PROBLEM: JS IS CONSTANT AT $\log 2$ FOR DISJOINT SUPPORTS
> **Arjovsky & Bottou (2017):** if the real and generated distributions have disjoint supports — **which is generic for two low-dimensional manifolds in $\mathbb R^{196608}$** — a perfect discriminator *exists*, and the Jensen–Shannon divergence the GAN objective optimizes is **$\log 2 = 0.693147$ for any such pair.**
>
> **A constant has zero gradient everywhere.** ⇒ ***the objective reports that the generator is wrong and carries no information about how wrong*** — so training stalls with a perfect discriminator and a directionless generator.
>
> **Wasserstein distance (WGAN) fixes exactly this**: it measures *how far apart* the distributions are, so it still varies when they do not overlap. *This is the same diagnosis pattern as [[03 - Image Classification and Linear Models|ch. 03]] §7 and [[10 - Pose Estimation and Faces|ch. 10]] §5 — a loss that switches off — reaching its most extreme form: not saturating for easy examples, but constant everywhere.*

### 3. ⚠️ Mode collapse, and a metric that rewards the worst failure

**The generator is rewarded for fooling $D$, not for coverage:**

| property of a generator emitting **one** perfect image | value | penalized? |
|---|---|---|
| $D(G(z))$ on that image | ~0.5 (looks real) | **no** |
| coverage of the data distribution | ~0% | **no** |

**There is no term in the GAN objective that mentions diversity.** ⇒ ***mode collapse is a specification failure, not a training failure*** — **the same shape as [[12 - Self-Supervised Learning|ch. 12]] §4's representational collapse: a degenerate solution the objective does not forbid.** *Second setting for that rule in two chapters.*

> [!warning] ⚠️ FID = 0.000000 FOR A MODEL THAT MEMORIZES ITS TRAINING SET
> **FID** fits Gaussians to Inception features and compares them: $\|\mu_1-\mu_2\|^2+\operatorname{Tr}\big(\Sigma_1+\Sigma_2-2(\Sigma_1\Sigma_2)^{1/2}\big)$.
>
> | generated set | FID |
> |---|---|
> | **an exact copy of the training set** | **0.000000** |
> | genuinely new samples from the same distribution | 1.0689 |
>
> **A model that simply returns its training images achieves a *perfect* score — better than one that generalizes**, because sampling noise is the only thing separating a real generalizer from the target statistics.
>
> ⇒ ***FID measures distributional match and is structurally blind to novelty.*** **It must be reported with a memorization check** — nearest-neighbour distance from each sample to the training set. **And this is not a benchmarking nicety: whether a generator reproduces its training data is exactly the question in the copyright and privacy disputes about image generators**, and the standard metric is designed not to notice.
>
> *Same structure as [[09 - Segmentation|ch. 09]] §3's pixel accuracy and [[08 - Object Detection II|ch. 08]] §1's AP conventions — **third time in this subject that the headline metric hides the failure that matters.***

### 4. ⚠️ Diffusion: an objective that cannot fail, at 1,000× the sampling cost

**Forward process**: add Gaussian noise over $T$ steps. Because the composition of Gaussians is Gaussian, any step has a closed form —

$$\mathbf x_t=\sqrt{\bar\alpha_t}\,\mathbf x_0+\sqrt{1-\bar\alpha_t}\,\boldsymbol\varepsilon,\qquad \bar\alpha_t=\prod_{s\le t}(1-\beta_s)$$

**so training needs no simulation: pick a $t$, add the noise, predict it.** With DDPM's linear schedule $\beta:10^{-4}\to0.02$ over $T=1000$:

| $t$ | $\bar\alpha_t$ | signal $\sqrt{\bar\alpha_t}$ | SNR |
|---|---|---|---|
| 1 | 0.99990 | 0.999950 | $9.999\times10^3$ |
| 100 | 0.89702 | 0.947110 | 8.7104 |
| 250 | 0.52409 | 0.723937 | 1.1012 |
| 500 | 0.07859 | 0.280334 | 0.08529 |
| **1000** | $4.04\times10^{-5}$ | **0.006353** | $4.04\times10^{-5}$ |

**At $t=T$ the signal coefficient is 0.0064 — the image is gone**, which is what licenses the reverse process to start from pure Gaussian noise.

**The training objective is $L=\|\boldsymbol\varepsilon-\boldsymbol\varepsilon_\theta(\mathbf x_t,t)\|^2$ — a plain supervised regression.** ⚠️ **No adversary, no minimax, and a target that always exists.** *Compare §2, where the difficulty was that the objective vanishes; this one is an L2 loss.*

> [!warning] ⚠️ THE TRADE IS EXPLICIT AND IT IS 1,000×
> | model | passes per sample |
> |---|---|
> | GAN, VAE | **1** |
> | **DDPM** | **1,000** |
> | DDIM (50 steps) | 50 |
> | distilled / consistency | ~4 |
>
> ⇒ ***diffusion pays 1,000 network evaluations per image for an objective that cannot collapse and cannot saturate.*** **That single ratio is why DDIM, progressive distillation and consistency models exist**, and why diffusion was a curiosity until they did. *A GAN moves the cost to training and makes it a stability problem; diffusion moves it to sampling and makes it an arithmetic problem — **and an arithmetic problem is the better kind to have**, because it yields to engineering.*

### 5. ⚠️ Latent diffusion — where the affordability came from

| | values |
|---|---|
| pixel space $512\times512\times3$ | 786,432 |
| **latent space $64\times64\times4$** | **16,384** |
| compression | **48.0×** |

**A separately trained, frozen autoencoder does the perceptual compression; the diffusion model does the semantic generation in the latent space.** And because the U-Net's attention is quadratic in token count ([[06 - Vision Transformers|ch. 06]] §1):

| | tokens | attention $\propto n^2$ |
|---|---|---|
| pixel $512^2$ | 262,144 | $6.87\times10^{10}$ |
| latent $64^2$ | 4,096 | $1.68\times10^7$ |

⇒ ***4,096× on the attention alone, and the U-Net runs 1,000 times.*** **That is what put text-to-image on a single consumer GPU** — *an engineering decomposition, not a modelling advance.*

### 6. Conditioning and guidance

**Text conditioning** enters through cross-attention: [[12 - Self-Supervised Learning|ch. 12]] §6's CLIP text encoder produces embeddings that the U-Net attends to. **Classifier-free guidance** then extrapolates between the conditional and unconditional predictions:

$$\hat{\boldsymbol\varepsilon}=\boldsymbol\varepsilon_\theta(\mathbf x,\varnothing)+w\big[\boldsymbol\varepsilon_\theta(\mathbf x,c)-\boldsymbol\varepsilon_\theta(\mathbf x,\varnothing)\big]$$

| $w$ | effect |
|---|---|
| 0 | unconditional — ignores the prompt |
| 1 | plain conditional, no guidance |
| **7.5** | Stable Diffusion's default: strong prompt adherence |
| 20 | over-saturated, low diversity, artifacts |

> [!note] ⚠️ Guidance costs exactly 2×, and $w>1$ extrapolates
> **The model is evaluated twice per step** — with and without the condition — so $T=1000$ becomes **2,000 passes per image.**
>
> **And $w>1$ is extrapolation, not interpolation**: it pushes *past* the conditional prediction, which is why large $w$ degrades the image while sharpening prompt adherence. ⇒ **$w$ is a fidelity-versus-diversity dial with no correct value, and it must be reported with any sample** — *[[08 - Object Detection II|ch. 08]]'s IoU threshold and [[12 - Self-Supervised Learning|ch. 12]]'s evaluation protocol, a third time.*

### 7. VAEs, briefly, and why they persist

**A VAE maximizes the ELBO** — a *lower bound* on the log-likelihood — trading reconstruction against a KL term that pulls the posterior toward a Gaussian prior. **Blurry samples are the characteristic result**, because a per-pixel Gaussian likelihood is minimized by *averaging* over plausible outputs. *That is [[10 - Pose Estimation and Faces|ch. 10]] §1's mode-averaging argument again — the average of two plausible images is an image of neither, and here it is a blur.*

**They persist for two reasons**: the encoder gives a genuine inference map (a GAN has none), and **the frozen autoencoder inside every latent diffusion model is one.**

## ✏️ Exercises

> [!example]- Exercise 1 — the saturating loss
> **(a)** Differentiate both generator objectives w.r.t. $D$. **(b)** Evaluate at $D=0.5,0.01,10^{-4}$. **(c)** Why is that the wrong behaviour? **(d)** What is the deeper problem with disjoint supports?
>
> ---
> **(a)** $\frac{d}{dD}\log(1-D)=\frac1{D-1}$; $\frac{d}{dD}(-\log D)=-\frac1D$.
>
> **(b)** Magnitudes: **2.00 / 2.00**, **1.0101 / 100**, **1.0001 / 10,000** — ratio **9,999** at $10^{-4}$.
>
> **(c)** ⚠️ **$D(G(z))$ small means the discriminator is winning — exactly when the generator needs the largest signal.** The saturating loss is **bounded by 1** there. **Goodfellow's paper proposes the non-saturating form for this reason.**
>
> **(d)** ⚠️ **With disjoint supports a perfect discriminator exists and JS is constant at $\log 2=0.693147$** — **zero gradient everywhere.** The objective says *that* the generator is wrong, never *how* wrong. **Wasserstein distance measures how far apart the distributions are, so it still varies when they do not overlap.**

> [!example]- Exercise 2 — the metric problem
> **(a)** What FID does a model that copies its training set achieve? **(b)** Compare to a genuine generalizer. **(c)** What does FID actually measure? **(d)** What must accompany it, and why does it matter beyond benchmarking?
>
> ---
> **(a)** **FID = 0.000000** — perfect. The Gaussian fit reproduces $\mu$ and $\Sigma$ exactly.
>
> **(b)** A generalizer scored **1.0689** — ⚠️ **worse**, because sampling noise is all that separates it from the target statistics.
>
> **(c)** **Distributional match between Inception feature statistics — and nothing else.** It is **structurally blind to novelty**, and equally blind to whether any individual sample is good.
>
> **(d)** **A memorization check** — nearest-neighbour distance from samples to the training set. ⚠️ **It matters because whether a generator reproduces its training data is exactly the question in the copyright and privacy disputes about image generators, and the standard metric is designed not to notice.**

> [!example]- Exercise 3 — the diffusion trade
> DDPM, $T=1000$, $\beta$ linear from $10^{-4}$ to 0.02. **(a)** Signal coefficient at $t=1$ and $t=T$. **(b)** Passes per sample vs a GAN; how do DDIM and distillation change it? **(c)** What is bought? **(d)** Why is that a good trade?
>
> ---
> **(a)** $\sqrt{\bar\alpha_1}=\mathbf{0.99995}$; $\sqrt{\bar\alpha_{1000}}=\mathbf{0.006353}$ ⇒ **the image is gone**, which licenses starting the reverse process from pure noise.
>
> **(b)** **1,000 vs 1.** DDIM at 50 steps → **20× fewer**; distillation/consistency → ~4, i.e. **250× fewer.**
>
> **(c)** ⚠️ **A plain L2 regression on the noise** — no adversary, no minimax, a target that always exists. **It cannot saturate (§2) and cannot mode-collapse (§3).**
>
> **(d)** **A GAN puts the cost in training and makes it a stability problem; diffusion puts it in sampling and makes it an arithmetic problem** — ⚠️ **and arithmetic problems yield to engineering**, which is precisely what DDIM and distillation did.

> [!example]- Exercise 4 — latent diffusion
> **(a)** Values in $512\times512\times3$ vs $64\times64\times4$. **(b)** Compression. **(c)** Effect on attention. **(d)** What kind of advance is this?
>
> ---
> **(a)** **786,432** vs **16,384**.
>
> **(b)** **48.0×.**
>
> **(c)** Tokens $262{,}144\to4{,}096$; attention $\propto n^2$ ⇒ $6.87\times10^{10}\to1.68\times10^7$ = ⚠️ **4,096×** — *and the U-Net runs 1,000 times on the small one.*
>
> **(d)** ⚠️ **An engineering decomposition, not a modelling advance**: a frozen autoencoder does perceptual compression, the diffusion model does semantic generation. **That split is what put text-to-image on one consumer GPU.**

> [!example]- Exercise 5 — collapse, twice
> **(a)** Why does the GAN objective permit mode collapse? **(b)** How is it like [[12 - Self-Supervised Learning|ch. 12]]'s collapse? **(c)** How do the fixes compare? **(d)** State the general rule.
>
> ---
> **(a)** ⚠️ **No term in the objective mentions coverage.** A generator emitting one perfect image gets $D\approx0.5$ and is **not penalized at all** for covering ~0% of the distribution.
>
> **(b)** Both are **degenerate solutions the objective does not forbid** — a **specification** failure, not a training failure.
>
> **(c)** **Both are fixed outside the loss**: SimSiam adds stop-gradient and a predictor; GANs add minibatch discrimination, unrolling, or a different divergence (WGAN). ⚠️ *In each case the repair changes the objective or the architecture — never the schedule.*
>
> **(d)** ⚠️ ***When a degenerate solution is not excluded by the objective, no amount of training, tuning or data fixes it.*** **Second setting in two chapters** — and the corollary is the same: **monitor the degenerate quantity directly** (embedding variance in ch. 12; sample diversity and coverage here), because the loss will not show it.

## 📝 Summary

- **A generative model maps an easy distribution onto the thin manifold of natural images** in $\mathbb R^{196608}$ — a space with $10^{473{,}479}$ points, against $10^{80}$ atoms in the universe. The families differ **only in how the map is trained.**
- **⚠️ The GAN's saturating generator loss has gradient bounded by 1 exactly when the discriminator is winning** — $1.0001$ vs the non-saturating form's $10{,}000$ at $D=10^{-4}$, **a ratio of 9,999.** **And with disjoint supports JS is constant at $\log 2=0.693147$: zero gradient everywhere**, so the objective says the generator is wrong without saying how wrong. **Wasserstein distance fixes exactly that.**
- **⚠️ Mode collapse is a specification failure**: nothing in the objective mentions coverage. **Same shape as [[12 - Self-Supervised Learning|ch. 12]] §4's collapse — a degenerate solution the objective does not forbid**, fixed by changing the objective or architecture, never the schedule.
- **⚠️ A model that memorizes its training set scores FID = 0.000000 — better than one that generalizes (1.0689).** **FID measures distributional match and is blind to novelty**, so it must be reported with a nearest-neighbour memorization check. **Third time in this subject that the headline metric hides the failure that matters.**
- **Diffusion adds Gaussian noise with a closed form at every $t$** ($\sqrt{\bar\alpha_t}$ falls from 0.99995 to **0.006353** at $T=1000$, so the image is gone) **and trains by regressing that noise — a plain L2 loss with no adversary.**
- **⚠️ The trade is 1,000 network passes per sample against a GAN's 1** — hence DDIM (50), distillation (~4). **A GAN's cost is a training-stability problem; diffusion's is an arithmetic problem, and arithmetic yields to engineering.**
- **⚠️ Latent diffusion compresses $786{,}432$ values to $16{,}384$ (48×), which is 4,096× on the quadratic attention** — *an engineering decomposition, and the reason text-to-image runs on one consumer GPU.*
- **Text conditioning uses [[12 - Self-Supervised Learning|ch. 12]]'s CLIP encoder through cross-attention; classifier-free guidance costs exactly 2× and *extrapolates* past the conditional prediction at $w>1$** — a fidelity/diversity dial with no correct value, **which must be reported with any sample.**

## ⚠️ Important Notes

1. **⚠️ Never report FID alone.** It is perfect for a memorizer. **Report nearest-neighbour distance to the training set beside it** — and note that FID also says nothing about any *individual* sample's quality.
2. **⚠️ FID depends on the sample count and the Inception weights.** It is biased downward with more samples and is not comparable across implementations. *[[08 - Object Detection II|Ch. 08]]'s "name the protocol", in a fourth metric family.*
3. **⚠️ A falling GAN loss means nothing.** In a minimax game both losses can oscillate while quality improves, or stay flat while it collapses. **Judge by samples and coverage, not by the curve.**
4. **⚠️ Guidance scale must be reported with any generated sample.** $w=7.5$ and $w=1$ produce visibly different images from the same model, prompt and seed.
5. **⚠️ Diffusion sampling cost is linear in steps and you control it.** 1,000 → 50 is a ~20× speedup for modest quality loss; **quoting a diffusion model's speed without its step count is meaningless.**
6. **VAE blurriness is [[10 - Pose Estimation and Faces|ch. 10]] §1's mode averaging.** A per-pixel Gaussian likelihood is minimized by averaging over plausible outputs — **the average of two plausible images is an image of neither.**
7. **⚠️ Generated images carry the training data's biases and its content.** The training sets are web-scraped and unaudited ([[12 - Self-Supervised Learning|ch. 12]] §6), so **whatever the web associates with a prompt is what the model produces** — and the memorization question in note 1 is the same question as the copyright one.
8. **In practice you will fine-tune, not train.** Training Stable Diffusion from scratch is a large-cluster job; **LoRA, DreamBooth and textual inversion adapt an existing checkpoint on a single GPU** — the realistic route for the lecturer's project topics.

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]), **and [[Deep Learning/contents/00-Index|Deep Learning]] explicitly put GANs out of scope, so this chapter has no vault cross-reference to lean on** — unlike ch. 04, 05, 07 and 08, whose depth lives in Deep Learning. **Everything here is new to the vault.**
>
> **⚠️ Szeliski §5.5.4 is brief and, being a 2022 second edition, predates most of the diffusion era.** Built from the papers: **Goodfellow et al. 2014**, **Kingma & Welling 2014**, **Arjovsky & Bottou 2017** and **Arjovsky et al. 2017 (WGAN)**, **Ho et al. 2020 (DDPM)**, **Song et al. 2021 (DDIM)**, **Rombach et al. 2022 (latent diffusion)**, **Ho & Salimans 2022 (classifier-free guidance)**, **Heusel et al. 2017 (FID)**.
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§3's FID experiment.** *That FID cannot detect memorization is known and occasionally noted; **computing it — 0.000000 for an exact copy against 1.0689 for a genuine generalizer, so the memorizer scores *better* — and drawing the copyright/privacy consequence, is the addition.***
> - **§2's gradient table**, including the observation that the saturating loss's gradient is **bounded by 1** rather than merely "small", and the 9,999× ratio.
> - **§4's schedule table** (computed from DDPM's stated linear $\beta$), the **pass-count comparison**, and the framing of the GAN/diffusion choice as **a stability problem versus an arithmetic problem.**
> - **§5's 48× and 4,096× figures.**
> - **§3's identification of mode collapse with [[12 - Self-Supervised Learning|ch. 12]] §4's representational collapse** as one rule, and **§7's identification of VAE blur with [[10 - Pose Estimation and Faces|ch. 10]] §1's mode averaging.**
> - **All eight Important Notes.**
>
> ⚠️ **§3's FID is computed on 64-dimensional Gaussian features, not real Inception activations** — the absolute values are not comparable to published FIDs. **The finding is the *ordering*: an exact copy scores 0, a generalizer scores worse. That is exact and independent of the feature space**, because a copy reproduces the reference statistics identically by construction.
>
> ⚠️ **No sample-quality or FID figures from any paper are quoted.** The step counts (1,000; 50; ~4), CFG scales, latent dimensions and $\beta$ schedule are stated design choices; **everything derived from them is exact arithmetic.** *The claims that WGAN improves stability, that DDIM loses little quality at 50 steps, and that distillation reaches ~4 steps are the papers' empirical results, stated qualitatively and attributed.*
>
> **No discrepancies found.**
>
> **Deliberately deferred, not omitted:** **the full VAE derivation** (ELBO, reparameterization trick) is compressed into §7 — *it belongs in a probabilistic-modelling course and [[Probability Theory/contents/00-Index|Probability Theory]] has the machinery*; **autoregressive image models** (PixelCNN, and the VQ-GAN/token route now used by several systems) get one row in §1; **score-based SDE formulations** of diffusion, which unify DDPM and DDIM, are omitted as beyond an introductory week; **video generation** is a natural extension of [[11 - Video and Motion|ch. 11]] and is not covered anywhere in the course; **3D generation** (NeRF-adjacent, text-to-3D) is [[14 - 3D Vision and Emerging Topics|ch. 14]].
>
> **Left as the source states it:** the GAN minimax objective and the non-saturating substitution; the ELBO; DDPM's forward process, linear $\beta$ schedule and $T=1000$; DDIM's deterministic sampler; latent diffusion's architecture and its $64\times64\times4$ latent; classifier-free guidance's formula and Stable Diffusion's default $w=7.5$; FID's definition.

**Previous:** [[12 - Self-Supervised Learning]] · **Next:** [[14 - 3D Vision and Emerging Topics]]
