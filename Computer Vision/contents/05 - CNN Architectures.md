---
subject: Computer Vision
chapter: 5
tags: [ds, computer-vision, cnn, architectures, efficientnet, mobilenet, depthwise-separable, compound-scaling]
source: "Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed. §5.4.3–5.4.4; Stanford CS231n; Howard et al. 2017 (MobileNet), Tan & Le 2019 (EfficientNet); the lecturer's course outline"
---

# CNN Architectures

**Week 5 of 14. ⚠️ NO SLIDES** — see [[00-Index]].

> [!warning] ⚠️ CROSS-REFERENCE CHAPTER — the architecture progression is [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]]
> **[[00-Index]]'s boundary rule.** [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] covers **LeNet → AlexNet → VGG → NiN → GoogLeNet → batch norm → ResNet → ResNeXt → DenseNet** with every parameter count recomputed, the FLOPs/parameters inversion measured across three networks, and the receptive-field growth traced layer by layer. **None of it is repeated here.**
>
> **This note adds the two things DL ch. 05 stops short of** — the **post-2017 efficiency architectures** (MobileNet, EfficientNet) and the lecturer's own framing, ***how to read an architecture table*** — plus one correction to a common misconception about activation volumes.

**Three results.**

**§1 — ⚠️ THE DEPTHWISE-SEPARABLE SAVING IS $1/c_o+1/k^2$, AND AT $k=3$ IT IS ESSENTIALLY $1/9$ REGARDLESS OF CHANNELS.** 8.69× at $c_o=256$, 8.92× at 1,024 — **the $1/c_o$ term is negligible past 64.** And it is **DL ch. 05 §15's grouped convolution at the extreme $g=c_i$.**

**§2 — ⚠️ EFFICIENTNET'S PUBLISHED CONSTANTS GIVE 1.9203, NOT 2 — AND THAT COMPOUNDS TO 21.7% BY $\phi=6$.** $\alpha\beta^2\gamma^2=1.2\times1.1^2\times1.15^2=\mathbf{1.9203}$, so FLOPs scale as $1.9203^\phi$ and the model at $\phi=6$ is **50.1× the base, not 64×.**

**§3 — ⚠️ THE ACTIVATION VOLUME *HALVES* AT EVERY STAGE; IT DOES NOT STAY CONSTANT.** Channels double while resolution quarters, so $C\cdot H\cdot W$ goes $\times\tfrac12$: **200,704 → 100,352 → 50,176 → 25,088, a factor of 8 across three stages.**

## 📘 Main Knowledge

### 1. ⚠️ Depthwise separable convolutions — the MobileNet idea

A standard $k\times k$ convolution mixes **space and channels at once**, costing $k^2c_ic_o$. **A depthwise separable convolution splits the two jobs:**

1. **depthwise** — one $k\times k$ filter *per input channel*, no cross-channel mixing: $k^2c_i$
2. **pointwise** — a $1\times1$ convolution mixing channels, no spatial extent: $c_ic_o$

$$\frac{\text{separable}}{\text{standard}}=\frac{k^2c_i+c_ic_o}{k^2c_ic_o}=\boxed{\frac{1}{c_o}+\frac{1}{k^2}}$$

| $k$ | $c_i$ | $c_o$ | standard | separable | ratio | $\frac1{c_o}+\frac1{k^2}$ |
|---|---|---|---|---|---|---|
| 3 | 32 | 64 | 18,432 | 2,336 | 0.1267 | 0.1267 ✓ |
| 3 | 128 | 256 | 294,912 | 33,920 | 0.1150 | 0.1150 ✓ |
| 3 | 512 | 512 | 2,359,296 | 266,752 | 0.1131 | 0.1131 ✓ |
| **5** | 256 | 256 | 1,638,400 | 71,936 | **0.0439** | 0.0439 ✓ |
| **7** | 256 | 256 | 3,211,264 | 78,080 | **0.0243** | 0.0243 ✓ |

> [!warning] ⚠️ At $k=3$ the saving is essentially $1/9$ and **barely depends on the channel counts**
> | $c_o$ | $1/c_o$ | $+1/9$ | **speedup** |
> |---|---|---|---|
> | 16 | 0.06250 | 0.17361 | 5.76× |
> | 64 | 0.01562 | 0.12674 | 7.89× |
> | 256 | 0.00391 | 0.11502 | **8.69×** |
> | 1024 | 0.00098 | 0.11209 | **8.92×** |
>
> **The $1/c_o$ term is negligible past $c_o=64$, so the saving asymptotes to $k^2$.** ⇒ *quote "≈9× for $3\times3$" and you are right to within 3% for any realistic layer* — and **larger kernels save more** (41× at $k=7$), which is why depthwise designs can afford $5\times5$ and $7\times7$ where dense ones cannot.

> [!note] ⚠️ It is **DL ch. 05 §15's grouped convolution at the extreme**
> Grouped convolution with $g$ groups costs $c_ic_o/g$. **Depthwise is $g=c_i$** — one channel per group:
>
> | $g$ | $3\times3$ parameters ($c_i=c_o=256$) | vs dense |
> |---|---|---|
> | 1 | 589,824 | 1× |
> | 16 | 36,864 | 16× |
> | **256 = $c_i$** | **2,304** | **256×** |
>
> **And the $1\times1$ that follows (65,536 parameters here) is what puts information back across channels** — *exactly ResNeXt's sandwich, and for exactly the same reason: no information crosses groups.*

### 2. ⚠️ EfficientNet — compound scaling, and the constant that is not 2

**Scaling a CNN has three dials, and a conv layer costs $h\cdot w\cdot k^2\cdot c_i\cdot c_o$:**

| dial | effect on FLOPs |
|---|---|
| **depth** $\times d$ | $d$ times as many layers → $\times d$ |
| **width** $\times w$ | $c_i$ *and* $c_o$ both scale → $\times w^2$ |
| **resolution** $\times r$ | $h$ *and* $w_{\text{sp}}$ both scale → $\times r^2$ |

$$\text{FLOPs multiplier}=d\cdot w^2\cdot r^2$$

**EfficientNet (Tan & Le 2019) fixes a ratio $\alpha:\beta:\gamma$ with $\alpha\beta^2\gamma^2\approx2$ and scales all three by a single $\phi$**, so each unit of $\phi$ nominally doubles the compute.

> [!warning] ⚠️ THE PUBLISHED CONSTANTS GIVE **1.9203**, NOT 2 — AND IT COMPOUNDS
> $\alpha=1.2$, $\beta=1.1$, $\gamma=1.15$ ⇒ $\alpha\beta^2\gamma^2=1.2\times1.21\times1.3225=\mathbf{1.9203}$.
>
> | $\phi$ | depth | width | resolution | **FLOPs multiple** | $2^\phi$ |
> |---|---|---|---|---|---|
> | 1 | 1.200 | 1.100 | 1.150 | **1.920** | 2.000 |
> | 2 | 1.440 | 1.210 | 1.322 | 3.687 | 4.000 |
> | 4 | 2.074 | 1.464 | 1.749 | 13.597 | 16.000 |
> | **6** | 2.986 | 1.772 | 2.313 | **50.139** | **64.000** |
>
> **4.0% low per step, compounding to 21.7% by $\phi=6$.**
>
> ⇒ ***"each step doubles the FLOPs" is an approximation that drifts by more than a fifth across the published family.*** *Not an error — the paper writes $\approx2$ and the constants come from a grid search under that constraint — but a figure worth computing rather than assuming when you are budgeting compute.*

> [!note] ⚠️ Why compound beats single-axis scaling
> To reach a 16× budget you can turn one dial or all three:
>
> | strategy | depth | width | resolution |
> |---|---|---|---|
> | depth only | **16.00** | 1.00 | 1.00 |
> | width only | 1.00 | **4.00** | 1.00 |
> | resolution only | 1.00 | 1.00 | **4.00** |
> | **compound ($\phi=4$)** | **2.07** | **1.46** | **1.75** |
>
> **Single-axis scaling saturates.** 16× depth gives a very deep, very narrow network **at the original resolution** — it literally cannot resolve finer detail. And [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §7's receptive-field argument says **depth has diminishing returns once the receptive field already covers the image** (VGG-11 reaches 150 of 224 pixels by its last block).
>
> ⇒ ***the three dials are not interchangeable because they buy different things: depth buys nonlinearity and receptive field, width buys features per position, resolution buys detail to see.*** Balancing them is the whole content of the paper.

### 3. ⚠️ How to read an architecture table

The lecturer's own framing for this week. **Track two things through every row: the shape $(C,H,W)$ and the parameter count.** A worked ResNet-style stage:

| layer | output $(C,H,W)$ | parameters |
|---|---|---|
| input | $(64,56,56)$ | — |
| conv $3\times3$ s2, $64\to128$ | $(128,28,28)$ | 73,856 |
| BatchNorm | $(128,28,28)$ | 256 |
| conv $3\times3$ s1, $128\to128$ | $(128,28,28)$ | 147,584 |
| BatchNorm | $(128,28,28)$ | 256 |
| $1\times1$ shortcut $64\to128$ s2 | $(128,28,28)$ | 8,320 |
| **total** | | **230,272** |

**Three checks that catch most specification errors:**

1. **Spatial arithmetic**: $\left\lfloor\frac{\text{in}+2p-k}{s}\right\rfloor+1$. Verified: $56\to28$ for $(k{=}3,p{=}1,s{=}2)$; $56\to56$ for $s{=}1$; $56\to28$ for a $1\times1$ stride-2 shortcut.
2. **The shortcut must match the main path in $C$, $H$ and $W$** — which is *why* a $1\times1$ stride-2 projection appears exactly when a stage downsamples. *[[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §14: $\mathbf x+\text{sublayer}(\mathbf x)$ requires matching shapes, and that requirement is what forces $d_{\text{model}}$ constant in a Transformer too.*
3. **Channels double when resolution halves** — and the consequence is *not* what people usually say.

> [!warning] ⚠️ THE ACTIVATION VOLUME **HALVES** AT EVERY STAGE — IT DOES NOT STAY CONSTANT
> | $C$ | $H=W$ | $C\cdot H\cdot W$ |
> |---|---|---|
> | 64 | 56 | **200,704** |
> | 128 | 28 | 100,352 |
> | 256 | 14 | 50,176 |
> | 512 | 7 | **25,088** |
>
> **Channels $\times2$, resolution $\times\tfrac14$ ⇒ volume $\times\tfrac12$.** Across three stages that is **8×**, not 1×.
>
> ⇒ **the common claim that "doubling channels while halving resolution keeps the tensor size constant" is wrong by a factor of 2 per stage** — it would need channels to *quadruple*. **This matters directly for activation memory** ([[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5): **the early layers dominate it**, which is why gradient checkpointing is applied there first and why input resolution is the most expensive hyperparameter in a CNN.

## ✏️ Exercises

> [!example]- Exercise 1 — depthwise separable convolutions
> **(a)** Derive the parameter ratio. **(b)** Evaluate at $k=3$, $c_i=c_o=512$ and at $k=7$, $c_i=c_o=256$. **(c)** Why does the saving barely depend on channels? **(d)** How does it relate to grouped convolution?
>
> ---
> **(a)** Standard $k^2c_ic_o$; separable $k^2c_i$ (depthwise) $+\,c_ic_o$ (pointwise). Ratio $=\frac{k^2c_i+c_ic_o}{k^2c_ic_o}=\frac1{c_o}+\frac1{k^2}$.
>
> **(b)** $k=3,c=512$: $2{,}359{,}296\to266{,}752$, ratio **0.1131 (8.84×)**. $k=7,c=256$: $3{,}211{,}264\to78{,}080$, ratio **0.0243 (41.1×)**.
>
> **(c)** ⚠️ **Because $1/c_o$ vanishes.** At $c_o=64$ it contributes 0.0156 against $1/9=0.1111$; at $c_o=1024$, 0.0010. **The saving asymptotes to $k^2$** — so it is a property of the *kernel size*, not the layer width. **And larger kernels save more**, which is why depthwise designs use $5\times5$ and $7\times7$ freely.
>
> **(d)** **Depthwise is grouped convolution at $g=c_i$** — the extreme where each group is one channel ($256\times$ fewer $3\times3$ parameters at $c=256$). **The pointwise $1\times1$ is what restores cross-channel mixing**, exactly as in ResNeXt's sandwich ([[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §15).

> [!example]- Exercise 2 — compound scaling
> **(a)** Why do the three dials contribute $d$, $w^2$ and $r^2$? **(b)** Evaluate $\alpha\beta^2\gamma^2$ for the published constants. **(c)** FLOPs multiple at $\phi=6$ vs the nominal $2^\phi$. **(d)** Why not just scale depth?
>
> ---
> **(a)** A conv layer costs $h\cdot w_{\text{sp}}\cdot k^2\cdot c_i\cdot c_o$. **Depth** multiplies the number of such layers ($\times d$). **Width** scales *both* $c_i$ and $c_o$ ($\times w^2$). **Resolution** scales *both* spatial dimensions ($\times r^2$).
>
> **(b)** $1.2\times1.1^2\times1.15^2=1.2\times1.21\times1.3225=\mathbf{1.9203}$ — **not 2.**
>
> **(c)** $1.9203^6=\mathbf{50.139}$ against $2^6=64$ — **21.7% low.** ⚠️ *The per-step error is only 4.0%, but it compounds.* **Budget from $1.9203^\phi$, not $2^\phi$.**
>
> **(d)** ⚠️ **Because the dials buy different things.** 16× depth leaves the network at the **original resolution**, unable to resolve finer detail, and [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §7 shows depth's receptive-field benefit saturates once the RF covers the image (VGG-11: 150 of 224 px). **Depth buys nonlinearity and receptive field; width buys features per position; resolution buys detail.** *Scaling one axis 16× runs into the flat part of its own curve.*

> [!example]- Exercise 3 — read the table
> A stage takes $(64,56,56)$ through conv $3\times3$ s2 to 128 channels, BN, conv $3\times3$ s1, BN, with a $1\times1$ s2 shortcut. **(a)** Shapes and parameters. **(b)** Why is the shortcut a $1\times1$ with stride 2? **(c)** Track $C\cdot H\cdot W$ across four stages. **(d)** What does that mean for memory?
>
> ---
> **(a)** All outputs $(128,28,28)$. Parameters: $3^2\cdot64\cdot128+128=\mathbf{73{,}856}$; BN $2\times128=256$; $3^2\cdot128\cdot128+128=\mathbf{147{,}584}$; BN 256; shortcut $1\cdot64\cdot128+128=\mathbf{8{,}320}$. **Total 230,272.**
>
> **(b)** ⚠️ **Because $\mathbf x+F(\mathbf x)$ requires matching shapes**, and the main path changed *both* the channel count (64→128) and the resolution (56→28). **A $1\times1$ stride-2 convolution is the cheapest projection that fixes both** — 8,320 parameters, 3.6% of the stage.
>
> **(c)** $200{,}704\to100{,}352\to50{,}176\to\mathbf{25{,}088}$ — **halving each time, 8× across three stages.**
>
> **(d)** ⚠️ **The early layers dominate activation memory**, because doubling channels does not compensate for quartering resolution. ⇒ **input resolution is the most expensive hyperparameter in a CNN** ($r^2$ in FLOPs *and* in activations), and gradient checkpointing pays off most in the first stages. *The widespread claim that the tensor size stays constant is wrong by 2× per stage.*

## 📝 Summary

- **The architecture progression LeNet → DenseNet is [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] and is not repeated here** ([[00-Index]]'s boundary rule). This chapter covers what comes after 2017 plus how to read a spec.
- **⚠️ Depthwise separable convolution costs $\frac1{c_o}+\frac1{k^2}$ of a standard one** — **8.69× cheaper at $k=3,c_o=256$**, 41.1× at $k=7$. **The $1/c_o$ term is negligible past 64 channels**, so the saving is a property of the kernel size. **Larger kernels save more**, which is why depthwise designs use $5\times5$ and $7\times7$ freely.
- **Depthwise is grouped convolution at $g=c_i$** (256× fewer $3\times3$ parameters at $c=256$), and **the following $1\times1$ restores cross-channel mixing** — ResNeXt's sandwich for the same reason.
- **FLOPs scale as $d\cdot w^2\cdot r^2$** because width scales both channel counts and resolution scales both spatial dimensions.
- **⚠️ EfficientNet's published $\alpha=1.2,\beta=1.1,\gamma=1.15$ give $\alpha\beta^2\gamma^2=1.9203$, not 2** — **4.0% low per step, 21.7% low by $\phi=6$ (50.1× rather than 64×).** Budget from $1.9203^\phi$.
- **Compound scaling beats single-axis scaling because the dials buy different things**: depth buys nonlinearity and receptive field (saturating once the RF covers the image), width buys features per position, resolution buys detail.
- **Reading a spec: track $(C,H,W)$ and parameters; check the spatial formula; check the shortcut matches; check the volume trend.**
- **⚠️ The activation volume HALVES at every stage** — $200{,}704\to100{,}352\to50{,}176\to25{,}088$, **8× across three** — because channels double while resolution quarters. **"Doubling channels keeps the tensor size constant" is wrong by 2× per stage**, and the early layers therefore dominate activation memory.

## ⚠️ Important Notes

1. **⚠️ Parameter count and FLOPs are different rankings, and depthwise separates them further.** A depthwise layer has ~9× fewer parameters *and* ~9× fewer FLOPs but is often **memory-bandwidth bound** in practice — its arithmetic intensity is low, so wall-clock speedup is usually well under 9×. **Measure, do not extrapolate from FLOPs** — [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §23's rule about benchmarks that cannot distinguish what they compare.
2. **⚠️ Input resolution is the most expensive hyperparameter.** It costs $r^2$ in FLOPs *and* $r^2$ in activation memory, and §3 shows the early layers hold most of the latter. **Halving resolution is usually the cheapest large saving available.**
3. **⚠️ Do not assume the scaling constants.** EfficientNet's own constants give 1.9203, not 2 — a 21.7% discrepancy at $\phi=6$. **Recompute $\alpha\beta^2\gamma^2$ before budgeting.**
4. **⚠️ A "1×1 shortcut" appears exactly where a stage changes shape.** If you see one in a spec, the stage downsamples or changes channels; if a downsampling stage lacks one, the specification is wrong.
5. **⚠️ Depth alone saturates.** Once the receptive field covers the image, extra depth buys nonlinearity only. **Check the receptive field** ([[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §7) before adding layers to fix a scale problem.
6. **⚠️ Architecture families are speed–accuracy curves, not points.** VGG, ResNet, EfficientNet and MobileNet all ship as families; **comparing a large member of one against a small member of another is meaningless.** Compare at matched FLOPs or matched latency.
7. **Nothing here changes the fact from [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §17** that in classical CNNs the convolutions hold under 8% of parameters and over 85% of computation. **Depthwise separable convolutions attack the computation side; global average pooling attacks the parameter side.** *Different problems, different layers.*

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). Built from **Szeliski §5.4.3–5.4.4 (network architectures, model zoos)**, **CS231n**, the **MobileNet** (Howard et al. 2017) and **EfficientNet** (Tan & Le 2019) papers, and this vault's [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]].
>
> **⚠️ AND THIS IS DELIBERATELY SHORT, for the same reason as [[04 - From Neural Networks to CNNs|ch. 04]].** DL ch. 05 already covers the entire LeNet → DenseNet progression with **every parameter count recomputed, the 66.7%/33.3% parameter/FLOP inversion measured across three networks, VGG's $3\times3$ stacking table, NiN's 64.7× reduction, and the receptive-field trace** — far beyond what a week-5 lecture reaches. **Duplicating it would create two copies that can drift.**
>
> **⚠️ The emphasis here is inferred.** The lecturer's topic title is *"CNN architectures"* and the accompanying phrase in [[00-Index]] is *"and how to read an architecture table"*, which is why §3 exists. **Which specific architectures week 5 covers is unknown**; the choice to add MobileNet and EfficientNet follows from DL ch. 05 stopping at 2017 and from the lecturer's project topics being scoped for *"a single consumer GPU or free Colab"*, where efficiency architectures are the relevant ones. **ConvNeXt (2022), RegNet and the Vision-Transformer-era hybrids are named nowhere and are not developed** — see [[06 - Vision Transformers|ch. 06]] for the last of these.
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§1's ratio table** and the finding that the saving **asymptotes to $k^2$ because $1/c_o$ vanishes past 64 channels** (5.76× → 8.92×), plus **the identification of depthwise as grouped convolution at $g=c_i$** with the $g$-table. *The MobileNet paper states the ratio; the asymptotic reading and the ResNeXt connection are mine.*
> - **§2's finding that $\alpha\beta^2\gamma^2=1.9203$, not 2**, and that the error **compounds from 4.0% per step to 21.7% at $\phi=6$**. *The paper writes $\approx2$; the compounding is not stated anywhere I have seen.* Also the single-axis-vs-compound table and its link to DL ch. 05 §7's receptive-field saturation.
> - **§3's entire worked stage**, the three specification checks, and **the activation-volume correction** — that $C\cdot H\cdot W$ **halves** per stage (8× across three), not stays constant. **This contradicts a widely repeated claim** and is verified arithmetically.
> - **All seven Important Notes**, of which 1 (FLOPs ≠ wall-clock for depthwise) and 3 (recompute the scaling constant) are practical hazards.
>
> **No discrepancies filed.** ⚠️ **§2's 1.9203 is deliberately NOT filed as an erratum**: Tan & Le write $\alpha\cdot\beta^2\cdot\gamma^2\approx2$ with an approximation sign, and the constants come from a constrained grid search — **the paper is correct and the approximation is simply looser than it reads.** Recorded as a measurement, per the vault's rule 4.
>
> **Deliberately deferred, not omitted:** **the entire pre-2018 architecture progression** is [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]]. **Neural architecture search** (Szeliski §5.4.3's RegNet discussion, and D2L ch. 8.8's AnyNet design spaces) is tuning infrastructure that [[Deep Learning/contents/00-Index|DL]] places out of scope and [[MLOps/contents/00-Index|MLOps]] is closer to. **Model zoos and transfer learning** (Szeliski §5.4.4) are treated in [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §1 as fine-tuning. **Visualizing weights and activations (§5.4.5) and adversarial examples (§5.4.6)** are genuinely interesting and belong to no week of this course's outline — *adversarial examples would be the most defensible addition if the mid-term covers robustness.*
>
> **Left as the source states it:** MobileNet's and EfficientNet's reported accuracies and latencies, which are external and unverifiable here; Szeliski's model-zoo discussion; and the claim that compound scaling was found by grid search under the $\approx2$ constraint.

**Previous:** [[04 - From Neural Networks to CNNs]] · **Next:** [[06 - Vision Transformers]]
