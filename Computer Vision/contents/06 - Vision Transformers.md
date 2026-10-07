---
subject: Computer Vision
chapter: 6
tags: [ds, computer-vision, attention, self-attention, vit, deit, distillation, swin, inductive-bias]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 06: Vision Transformers (48 slides); Dosovitskiy et al. 2021 (ViT), Touvron et al. 2021 (DeiT), Liu et al. 2021 (Swin)"
---

# Vision Transformers

Week 6. Every architecture so far rests on one operator, the convolution, which builds in two assumptions: locality and weight sharing. In 2020 a Google team fed image patches into a language-model Transformer, changed almost nothing else, and beat the best CNNs. This lecture covers attention, the Vision Transformer (ViT), what giving up the convolutional assumptions costs (data), how DeiT removed the data requirement, and how Swin put locality and a pyramid back.

The lecture's thesis (slide 3): *the convolutional assumptions are worth a great deal when data is scarce, and almost nothing when it's abundant.*

For the Transformer in language (encoder–decoder, positional encodings, sequence models) see [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]].

## 📘 Main Knowledge

### 1. Attention (slides 5–13)

**What a convolution can't do (slide 6).** A conv kernel is fixed after training. How strongly pixel $i$ influences pixel $j$ depends only on their offset $j - i$, never on what's actually in the image. What we might want instead: a wheel should look at the other wheel, wherever it is. The weights should depend on **content** and be computed **per image**.

**Attention is a soft dictionary lookup (slide 7).** A Python dictionary takes a key and returns its value, exact match only. Attention compares a **query** against *every* key and returns a **blend of the values**, weighted by how well each key matched. The blend is differentiable; an exact lookup (argmax) is not. Similarity is measured with the **dot product**, the cheapest option: one matrix multiplication (slide 8).

**Scaled dot-product attention (slide 9).** For one query $q \in \mathbb R^{d_k}$ against $n$ keys and values:

$$\text{Attention}(q, K, V) = \underbrace{\text{softmax}\!\left(\frac{q K^\top}{\sqrt{d_k}}\right)}_{\text{weights } a \in \mathbb R^n,\ \sum_j a_j = 1} V$$

Stacking all queries into a matrix $Q$:

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V$$

Shapes: $Q \in \mathbb R^{n \times d_k}$, $K \in \mathbb R^{n \times d_k}$, $V \in \mathbb R^{n \times d_v}$, $QK^\top \in \mathbb R^{n \times n}$ (one score for every query–key pair), output $\in \mathbb R^{n \times d_v}$. The softmax is applied to each row.

**Why divide by $\sqrt{d_k}$? (slide 10).** If $q$ and $k$ have independent, zero-mean, unit-variance components:

$$\operatorname{Var}(q \cdot k) = \operatorname{Var}\Big(\sum_{i=1}^{d_k} q_i k_i\Big) = d_k \quad\Rightarrow\quad \text{std} = \sqrt{d_k}$$

Without scaling, larger heads give larger logits, the softmax becomes nearly one-hot, and its gradient vanishes (saturation, as in [[04 - From Neural Networks to CNNs|ch. 04]]). Dividing by $\sqrt{d_k}$ brings the logits back to unit scale whatever the head size. It's the same variance argument as He initialisation ([[05 - CNN Architectures|ch. 05]]).

**Self-attention (slide 11).** So far $Q$, $K$, $V$ were given. In **self-attention** every token produces all three from the same input $X \in \mathbb R^{n \times D}$:

$$Q = X W_Q, \qquad K = X W_K, \qquad V = X W_V$$

- $W_Q, W_K \in \mathbb R^{D \times d_k}$ and $W_V \in \mathbb R^{D \times d_v}$ are learned. **These are the parameters**: $3D^2$ if $d_k = d_v = D$, independent of the number of tokens $n$.
- Each token asks a question ($q$), advertises what it has ($k$), and offers content ($v$).
- The attention weights are **not** parameters: they're recomputed for every input.
- Compared with a CNN: a convolution's weights are learned and then fixed. Here the weights are *produced* by a learned function of the input, so the layer can behave differently on every image.

**Multi-head attention (slide 12).** One softmax can only commit to one notion of relevance; it can't attend to two different things at once. So run $h$ heads in parallel, each on a slice of size $d_h = D/h$, and combine:

$$\text{MSA}(X) = [\text{head}_1; \dots; \text{head}_h]\, W_O, \qquad \text{head}_i = \text{Attention}(X W_Q^i, X W_K^i, X W_V^i)$$

- ViT-Base: $D = 768$, $h = 12$, so $d_h = 64$. The scaling is per head: $\sqrt{64} = 8$, not $\sqrt{768}$.
- Splitting $D$ into heads (instead of giving each head the full width) keeps the cost the same as one head of width $D$.

**Attention doesn't know where anything is (slide 13).** Permute the input tokens and the output is permuted in exactly the same way; nothing else changes:

$$\text{Attention}(PX) = P\, \text{Attention}(X) \quad \text{for any permutation matrix } P$$

Self-attention is **permutation-equivariant**. A convolution is told where things are by construction; attention must be **given position explicitly**.

### 2. The Vision Transformer (slides 14–22)

**An image as a sequence (slide 15).** Attention costs $O(n^2)$ in the number of tokens. One token per pixel of a 224×224 image means $n = 50{,}176$ and an attention matrix of about 2.5 billion entries, per head, per layer. So cut the image into non-overlapping $P \times P$ **patches** and make each patch a token. At 224×224 with $P = 16$: $n = (224/16)^2 = 196$ tokens, a sequence length a language model handles easily.

**The patch embedding is a convolution (slide 16).** There are $N = HW/P^2$ patches. Each is flattened to $P^2 C$ numbers and projected to $D$ dimensions by a learned matrix $E \in \mathbb R^{(P^2 C) \times D}$. Flattening non-overlapping patches and multiplying by $E$ *is* a convolution with kernel size $P$ and stride $P$. So every ViT contains exactly one convolution, and it's the only place the model is given 2D structure.

**Two additions before the Transformer (slide 17):**

- **The [class] token.** Prepend one extra learned vector $x_{class} \in \mathbb R^D$ that corresponds to no patch. It attends to every patch in every layer, and its final state is the image representation fed to the classifier. Borrowed unchanged from BERT. Sequence length becomes $N + 1$. (Global average pooling over the patch tokens works about as well; ViT chose the token to stay close to BERT.)
- **Position embeddings.** Add a learned $E_{pos} \in \mathbb R^{(N+1) \times D}$ to the token embeddings. Standard **1D** embeddings: the model isn't told the grid is 2D (2D-aware variants gave no measurable gain). They're **added**, not concatenated: cheaper and empirically just as good.

**Why position embeddings? (slide 18).** Nothing tells the model that token 5 sits below token 1; it must discover the grid. In the lecturer's own trained model, neighbouring patches' position embeddings had mean cosine similarity 0.13 vs −0.04 for distant ones (correlation between distance and similarity −0.38). This structure only appears if training includes **translations** (augmentation). Without them every digit sits in the same place, position is just a name tag, and the grid structure never forms.

**What the [class] token looks at (slide 19).** Its attention over the patches (averaged over heads):
- is **different for every image**, the content dependence a fixed kernel can't have;
- differs between layers: the same token asks a different question at each depth;
- was never supervised: nobody told the model which patches matter.

*A high weight means a patch was **read**, not that it was decisive. Treat attention maps as a hint, not an explanation.*

**The Transformer block (slide 20).** Two sublayers, each wrapped in a residual connection and each **preceded** by LayerNorm (LN):

$$z' = \text{MSA}(\text{LN}(z)) + z, \qquad z'' = \text{MLP}(\text{LN}(z')) + z'$$

- The MLP is two layers, $D \to 4D \to D$, with **GELU** activation.
- The MLP acts on each token **separately**; all mixing between tokens happens in the attention.
- **Pre-norm** (LN inside the residual branch, before the sublayer) leaves an unobstructed identity path from input to loss, which is what lets these models train without learning-rate warm-up tricks.

**ViT end to end (slide 21):**
1. Split the image into $N$ patches, flatten, project to $D$ (patch embedding).
2. Prepend the [class] token; add position embeddings.
3. Apply $L$ Transformer blocks.
4. Take the final [class] token, apply LayerNorm and a linear classifier.

**Model variants (slide 22):**

| Model | Layers $L$ | Hidden $D$ | MLP size | Heads | Params |
|---|---|---|---|---|---|
| ViT-Base | 12 | 768 | 3072 | 12 | 86M |
| ViT-Large | 24 | 1024 | 4096 | 16 | 307M |
| ViT-Huge | 32 | 1280 | 5120 | 16 | 632M |

Per block: $4D^2$ for attention ($W_Q, W_K, W_V, W_O$) plus $8D^2$ for the MLP ($D \cdot 4D$ twice) $= 12D^2$. ViT-Base: $12 \times 12 \times 768^2 \approx 85$M, essentially the whole model. **Two-thirds of a transformer's parameters are in the MLPs, not the attention.**

**Naming:** ViT-B/16 means Base with 16×16 patches. Smaller patches mean more tokens and more compute: B/16 has 196 tokens vs 49 for B/32, so it costs over four times as much (and the attention matrices 16× as much).

### 3. Inductive bias and data (slides 23–26)

An **inductive bias** is an assumption built into a model's structure, so it doesn't have to be learned from data.

**What exactly was given up (slide 24):**

| Built into every conv layer | In ViT |
|---|---|
| **Locality**: a unit sees a small window | self-attention is **global from layer 1** |
| **Translation equivariance**: shift the input, the output shifts | only the per-token MLP is local and equivariant |
| **2D neighbourhood**: the grid is in the operator | 2D structure enters only twice: cutting patches, and interpolating position embeddings when the resolution changes |

*"A CNN is told how images work. A ViT must infer it — and inference costs data."*

**Measured: what the convolutional prior is worth (slide 25).** The lecturer's own ViT vs a small CNN, same data and budget:

| Training images | CNN's lead |
|---|---|
| 100 | 22.5 points |
| 400 | 5.8 points |
| 1,257 | −0.4 points (ViT has caught up) |

The advantage doesn't just shrink, it vanishes. The prior is a **substitute for data** and stops paying once the data arrives.

**The same curve at Google scale (slide 26):**

| Pre-training set | Size | Outcome for ViT |
|---|---|---|
| ImageNet-1k | 1.3M | ViT-Large *underperforms* ViT-Base; both below ResNets |
| ImageNet-21k | 14M | ViT and ResNets comparable |
| JFT-300M | 300M | ViT wins, and bigger ViTs win more |

Best ImageNet top-1: ViT-H/14 (JFT) 88.55%; ViT-L/16 (JFT) 87.76%; BiT-L ResNet152x4 (JFT) 87.54%; ViT-L/16 (ImageNet-21k only) 85.30%. The paper's summary: *"Large scale training trumps inductive bias."* Some attention heads already span most of the image in layer 1 while others stay local: the network rediscovers locality where it's useful.

### 4. DeiT: removing the data requirement (slides 27–35)

**Data-efficient Image Transformers (Touvron et al., 2021) (slide 28).** ViT's result came with a footnote: 300 million proprietary images and a TPU cluster. DeiT's claim: *the architecture was never the problem.* DeiT-B is identical to ViT-B; only the **training recipe** changed. Result: ImageNet-1k only (about 230× less data), 86M parameters, **81.8% top-1**, one machine, under three days.

**The recipe is the contribution (slide 29):**
- Augmentation (all from [[05 - CNN Architectures|ch. 05]]): RandAugment, Mixup and CutMix, random erasing, repeated augmentation.
- Regularisation and optimisation: stochastic depth (randomly skip whole blocks during training), label smoothing, AdamW (Adam with decoupled weight decay) with cosine decay, careful warm-up.

The lesson: a "transformers need 300M images" result was really a "this model was undertrained" result. *Before concluding an architecture is wrong for your data, exhaust the recipe.*

**Knowledge distillation (slides 30–31).** Train a **student** to reproduce a **teacher**'s output distribution, instead of or alongside the true label (Hinton et al., 2015):

$$L = (1 - \lambda)\, \underbrace{\text{CE}(p_s, y)}_{\text{the real label}} + \lambda T^2\, \underbrace{\text{KL}(p_t^T \,\|\, p_s^T)}_{\text{agree with the teacher}}, \qquad p_i^T = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}$$

- $z$ are logits, $T$ is the **temperature**, KL is the Kullback–Leibler divergence (how different two distributions are), $\lambda$ balances the two terms.
- **Why the teacher helps:** a one-hot label says "this is a 7" and nothing else. The teacher also says *what else it nearly was*, and those relative probabilities encode which classes look alike. Hinton called this **dark knowledge**.
- **What $T$ does:** at $T = 1$ a confident teacher is nearly one-hot and says little. Raising $T$ flattens the distribution and exposes the runner-ups.
- The $T^2$ factor restores the gradient magnitude, which dividing the logits by $T$ otherwise shrinks by $1/T^2$.

**Dark knowledge in practice (slide 32).** The lecturer's small CNN (97.4% accurate): on a 7 its runner-up is 4; on a 3 it is 8. Those are the digits humans confuse too. The teacher learned a similarity structure over classes that the labels never stated.

| Target | Entropy (nats) |
|---|---|
| Hard label | 0 |
| Teacher, $T = 1$ | 0.135 |
| Teacher, $T = 4$ | 1.343 |
| Uniform over 10 classes | 2.303 |

**The distillation token (slide 33).** DeiT puts the teacher *inside the sequence*: a third kind of token alongside [class] and the patches. It attends and is attended to like any other token, but its target is the **teacher's prediction**, while [class] keeps the true label. At test time the two predictions are averaged. The two tokens converge to genuinely different solutions.

| Model | ImageNet top-1 |
|---|---|
| DeiT-B | 81.8% |
| DeiT-B, distilled | 83.4% |
| DeiT-B ↑384 (fine-tuned at 384×384) | 83.1% |
| DeiT-B distilled ↑384 | 85.2% |

**The finding (slide 35):** a transformer student learns **more from a convolutional teacher** than from a transformer teacher of equal accuracy.

| Teacher | Teacher acc. | Distilled DeiT-B student |
|---|---|---|
| DeiT-B (transformer) | 81.8 | 81.9 |
| RegNetY-4GF (convnet) | 80.0 | 82.7 |
| RegNetY-16GF (convnet) | 82.9 | 83.0 |

A *weaker* convnet teacher (80.0) beats a *stronger* transformer teacher (81.8). The student isn't copying accuracy; it's inheriting the **convolutional inductive bias**, passed on through the teacher's outputs. *The bias can be handed over as data if you can't build it in.*

### 5. Swin: putting the pyramid back (slides 36–42)

**What ViT can't do (slide 37):**
1. **One scale.** Every ViT layer works at 16× downsampling. Detection needs objects at many sizes and segmentation needs per-pixel output; every detector assumes a **feature pyramid** ([[07 - Object Detection I|ch. 07]]). ViT has none.
2. **Quadratic cost.** For an $h \times w$ grid of patches with $C$ channels:
$$\Omega(\text{MSA}) = 4hwC^2 + 2(hw)^2 C$$
   The first term (the $Q, K, V, O$ projections) is linear in the number of patches; the second (computing $QK^\top$ and multiplying by $V$) is quadratic. Fine for $n = 196$; hopeless at the resolutions dense prediction needs.

The **Swin Transformer** (Liu et al., ICCV 2021 best paper) fixes both, each with a concept from week 2.

**Window attention (slide 38).** Restrict attention to non-overlapping $M \times M$ windows of patches:

$$\Omega(\text{W-MSA}) = 4hwC^2 + 2M^2 hwC$$

With $M$ fixed at 7, the second term becomes **linear** in $hw$. The saving on that term is a factor of $hw/M^2$: for Swin's first stage at 224×224 input (a 56×56 grid) that's $3136/49 = 64\times$.

**Shifted windows (slide 39).** Fixed windows never exchange information: a patch on one side of a window boundary can never influence its neighbour on the other side. So alternate the partition between layers:

$$\hat z^\ell = \text{W-MSA}(\text{LN}(z^{\ell-1})) + z^{\ell-1}, \qquad \hat z^{\ell+1} = \text{SW-MSA}(\text{LN}(z^\ell)) + z^\ell$$

(each also followed by an MLP sublayer). Blocks come in pairs: regular windows, then windows shifted by $\lfloor M/2 \rfloor$ patches. Shifting creates more, smaller windows at the image edges; Swin avoids that waste with a **cyclic shift** plus a mask, keeping the number of windows (and the cost) unchanged.

**Patch merging rebuilds the hierarchy (slide 40).** Between stages, concatenate each 2×2 group of neighbouring tokens ($4C$ features) and project to $2C$: tokens ÷4, channels ×2. Stages run at 4×, 8×, 16× and 32× downsampling, like a ResNet. *Halve the resolution, double the channels* (VGG's rule). *"Swin is a transformer wearing a CNN's skeleton."*

**Relative position bias (slide 41).** Inside a window, Swin drops absolute position embeddings and adds a learned bias that depends only on the **offset** between two patches:

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt d} + B\right) V$$

For $M = 7$ there are $49^2 = 2{,}401$ query–key pairs but only $(2M - 1)^2 = 169$ distinct offsets, so $B$ is filled from a table of 169 learned numbers. Sharing a weight across all pairs with the same offset is exactly what a convolution kernel does. Adding absolute embeddings on top made results slightly worse.

**Swin results (slide 42):**

| Task | Swin | vs previous best |
|---|---|---|
| ImageNet-1k top-1 | 87.3% | — |
| COCO test-dev box AP | 58.7 | +2.7 |
| COCO test-dev mask AP | 51.1 | +2.6 |
| ADE20K val mIoU | 53.5 | +3.2 |

The big gains are in **dense prediction** (detection, segmentation), where the pyramid and the linear cost actually matter. *The winning recipe was not "attention instead of convolution" but attention plus the structural priors convolution had all along.*

### 6. What should you use? (slides 43–45)

| What attention genuinely brings | What the convolutional priors still buy |
|---|---|
| content-dependent weights, recomputed per image | far better accuracy per training image |
| global interaction from the first layer | linear cost in image size |
| scales better than CNNs when data is enormous | multi-scale features for free |
| one architecture shared with language ⇒ multimodal models | Swin and DeiT both re-import them |

**ConvNeXt (2022) is the control experiment:** give a ResNet the transformer training recipe and design choices, keep convolution, and it matches Swin. Much of the 2020–21 gap was **recipe, not operator**.

**For the final project (slide 45):**

| Situation | Reach for |
|---|---|
| a few thousand images, training from scratch | a small CNN. Not close. |
| any size, fine-tuning a pretrained model | either; pretraining erases the gap |
| detection or segmentation | Swin, or a ConvNeXt/ResNet backbone |
| text and images together | a transformer, for the shared interface |
| tight compute or latency budget | MobileNet / EfficientNet |

*Almost nobody trains a ViT from scratch. Fine-tune a pretrained one*, which is how the 300M images end up working for you too.

**Hands-on (slide 48):** scaled dot-product attention and the $\sqrt{d_k}$ experiment; multi-head attention with a gradient check; patch embedding as a strided convolution; permutation equivariance; a complete transformer block; train a ViT on digits and read its attention maps; reproduce the data-efficiency crossover; the same model in PyTorch. (The `timm` library's `vision_transformer.py`, about 300 lines, is recommended reading.)

## ✏️ Exercises

> [!example]- Exercise 1 — Attention by hand
> One query $q = [2, 1]$, keys $K = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{bmatrix}$, values $V = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 2 & 2 \end{bmatrix}$, $d_k = 2$.
> **(a)** Compute the scaled scores, the attention weights and the output.
> **(b)** Which key matched best, and why?
> **(c)** If $d_k$ were 64 and you forgot to divide by $\sqrt{d_k}$, what would happen to the attention weights and the gradients?
>
> ---
> **(a)** Scores $qK^\top = [2, 1, 3]$; divide by $\sqrt 2$: $[1.414, 0.707, 2.121]$. Exponentials $[4.11, 2.03, 8.34]$, sum 14.48. Weights $a = [0.284, 0.140, 0.576]$. Output $= 0.284[1,0] + 0.140[0,1] + 0.576[2,2] = [1.436, 1.292]$.
>
> **(b)** Key 3, $[1,1]$: it has the largest dot product with $q$ (it points most in $q$'s direction and is the longest). It gets 58% of the weight, but the other values still contribute: attention returns a *blend*, not a single lookup.
>
> **(c)** With unit-variance components, raw dot products would have standard deviation $\sqrt{64} = 8$. Logits that spread out make the softmax nearly one-hot (one weight ≈ 1, the rest ≈ 0), so it saturates and its gradient becomes tiny. Learning slows or stalls. Dividing by $\sqrt{d_k} = 8$ brings the logits back to unit scale.

> [!example]- Exercise 2 — Tokens and cost
> A ViT-B/16 is pretrained at 224×224.
> **(a)** How many tokens does the Transformer process (including [class])? How many entries in each attention matrix?
> **(b)** You fine-tune it at 384×384. How many tokens now? Roughly how much larger is the attention matrix? What must you do with the position embeddings?
> **(c)** You switch to ViT-B/8 at 224×224. Tokens? How does the cost of the attention scores change?
> **(d)** Why does ViT use patches at all instead of one token per pixel?
>
> ---
> **(a)** $(224/16)^2 = 196$ patches + 1 = **197** tokens. Each attention matrix (per head, per layer) is $197^2 \approx 38{,}800$ entries.
>
> **(b)** $(384/16)^2 = 576$ patches + 1 = 577 tokens. The attention matrix grows by about $(577/197)^2 \approx 8.6\times$. The learned position embeddings only exist for 196 patch positions on a 14×14 grid; **interpolate** them (in 2D) to a 24×24 grid. This is one of the two places ViT uses 2D structure.
>
> **(c)** $(224/8)^2 = 784$ patches. 4× the tokens, so the $(hw)^2$ attention term grows about **16×** (and the per-token MLP and projections 4×).
>
> **(d)** One token per pixel gives $n = 50{,}176$ and $n^2 \approx 2.5 \times 10^9$ attention entries per head per layer, which is far too much memory and compute. Patches cut $n$ by $P^2 = 256$ and the attention cost by $256^2$.

> [!example]- Exercise 3 — Where the parameters are
> **(a)** Estimate ViT-Base's per-block parameters and total, using $12D^2$ per block. Compare with the quoted 86M.
> **(b)** What fraction of each block's parameters is in attention vs the MLP?
> **(c)** A colleague wants to shrink ViT-Base by switching to 8 heads instead of 12, keeping $D = 768$. How much does the parameter count change?
> **(d)** Does the number of parameters change when you go from 224×224 to 384×384 input?
>
> ---
> **(a)** $12 \times 768^2 = 7{,}077{,}888$ per block; × 12 blocks ≈ **84.9M**. The rest (patch embedding $768 \cdot 768 \approx 0.59$M, position embeddings, LayerNorms, biases, classifier head) brings it to ~86M.
>
> **(b)** Attention $4D^2$ = 1/3, MLP $8D^2$ = 2/3.
>
> **(c)** **Not at all.** The heads split $D$ into slices ($d_h = D/h$); $W_Q, W_K, W_V, W_O$ are still $D \times D$ in total. Fewer heads just means each head is wider (96 instead of 64). To shrink the model, reduce $D$, the MLP size, or the number of layers.
>
> **(d)** The Transformer weights don't change (they're independent of $n$). Only the position embedding table must be resized (interpolated), which changes its size slightly: from 197 × 768 to 577 × 768.

> [!example]- Exercise 4 — Permutations and positions
> **(a)** Take a trained ViT and remove its position embeddings. You feed it an image and a version of the same image with its 196 patches randomly shuffled. Compare the [class] token's final output for the two inputs.
> **(b)** Why does this make position embeddings necessary, and why isn't a CNN affected the same way?
> **(c)** The lecturer found that neighbouring patches only got similar position embeddings when training included translations. Explain why.
> **(d)** A student shows a ViT attention map highlighting a dog's face and writes "the model classifies dogs by their faces". What's wrong with that conclusion?
>
> ---
> **(a)** **Identical.** Without position embeddings, self-attention is permutation-equivariant: shuffling the patch tokens shuffles their outputs the same way. The [class] token attends to the *set* of patch tokens, and a weighted sum over a set doesn't depend on order. So the model can't tell the image from its scrambled version.
>
> **(b)** Position is the only way the model can know which patch is where; without it, an image is a bag of patches. A convolution uses position by construction (each output combines specific neighbouring pixels), so shuffling changes its output.
>
> **(c)** If every digit is always in the same place, a position embedding only needs to work as an arbitrary ID for "patch slot 37"; nothing forces nearby slots to be similar. When objects move around (translations), the model sees the same content at neighbouring positions and benefits from position embeddings that treat neighbours alike, so the 2D grid structure emerges.
>
> **(d)** Attention weights show which patches were **read**, not which were **decisive** (slide 19). The value vectors, later layers, MLPs and the residual path all affect the output. A high weight is a hint, not an explanation; you'd need an intervention test (e.g. mask the face and see if the prediction changes).

> [!example]- Exercise 5 — Data, distillation and choices
> **(a)** Your team has 3,000 labelled images of 8 rice-plant diseases. Option A: train ViT-B from scratch. Option B: small CNN from scratch. Option C: fine-tune an ImageNet-pretrained ViT-B or ResNet-50. Rank them and explain.
> **(b)** A teacher's logits for an image of a 7 over the classes [7, 4, 1] are $[9, 5, 3]$. Compute the teacher's probabilities at $T = 1$ and $T = 4$. Which is more useful as a distillation target, and why?
> **(c)** Why did a 80.0%-accurate CNN teacher produce a better DeiT student than an 81.8%-accurate transformer teacher?
> **(d)** You need instance segmentation at 1024×1024. Why is plain ViT a poor backbone, and what two Swin features address it?
>
> ---
> **(a)** **C > B > A.** Pretraining erases most of the ViT-vs-CNN gap, so fine-tuning either pretrained model is best. From scratch at 3,000 images, the CNN's inductive bias is worth a lot (the lecturer measured a 22.5-point CNN lead at 100 images, shrinking to zero around 1,257 images on an easier digit task). A ViT from scratch on 3,000 images of a harder task would likely underperform badly.
>
> **(b)** $T = 1$: $p \approx [0.980, 0.018, 0.002]$, nearly one-hot (entropy 0.11 nats). $T = 4$: $p \approx [0.629, 0.231, 0.140]$ (entropy 0.91 nats). $T = 4$ is more useful: it still says "7" but reveals that 4 is the likeliest confusion, then 1. That similarity information (dark knowledge) is what the hard label doesn't contain. (Multiply the KL term by $T^2 = 16$ to keep the gradient magnitude.)
>
> **(c)** The student isn't learning accuracy from the teacher; it's learning the teacher's *pattern of outputs*, which reflects the CNN's built-in locality and translation equivariance. Those are exactly the biases a ViT lacks and needs from data, so a CNN teacher passes on something new, while a transformer teacher only passes on what the student could already learn.
>
> **(d)** At 1024×1024 with $P = 16$ there are 4,096 tokens, so global attention costs ~$4096^2 \approx 1.7 \times 10^7$ scores per head per layer, and ViT has a single 16× scale with no pyramid. Swin fixes both: **window attention** (cost linear in the number of patches, with shifted windows for cross-window communication) and **patch merging** (a 4×/8×/16×/32× feature pyramid, like a CNN).

## 📝 Summary

- **Attention** is a soft dictionary lookup: $\text{softmax}(QK^\top/\sqrt{d_k})V$. Weights depend on **content**, not on offset, and are recomputed per input. The $\sqrt{d_k}$ keeps logits at unit variance so the softmax doesn't saturate.
- **Self-attention:** $Q = XW_Q$, $K = XW_K$, $V = XW_V$; parameters $3D^2$, independent of $n$. **Multi-head:** $h$ heads of size $D/h$, same cost as one head. **Permutation-equivariant**, so position must be added.
- **ViT** = patches (a $P \times P$, stride-$P$ convolution) + [class] token + learned 1D position embeddings + $L$ pre-norm blocks (MSA + MLP $D \to 4D \to D$ with GELU, each with a residual). 224/16 → 196 tokens. $12D^2$ per block; two-thirds in the MLPs. ViT-B 86M, L 307M, H 632M.
- **Inductive bias vs data:** CNNs are told locality, translation equivariance and the 2D grid; ViT must learn them. CNN wins on small data (22.5 points at 100 images in the lecturer's test), the gap closes with more data, and ViT wins at 300M images.
- **DeiT:** same architecture as ViT-B, better recipe (strong augmentation, stochastic depth, label smoothing, AdamW + cosine, warm-up) → 81.8% on ImageNet-1k alone. **Distillation** with temperature $T$ passes on dark knowledge; a **distillation token** learns from the teacher; a CNN teacher works best because it passes on the convolutional bias.
- **Swin:** window attention ($M = 7$, cost linear in patches), shifted windows for cross-window flow, patch merging for a 4×–32× pyramid, relative position bias (169 values for $M = 7$). Big gains on detection and segmentation.
- **Practice:** fine-tune a pretrained model; train from scratch only with a CNN; use Swin/ConvNeXt/ResNet backbones for dense prediction. ConvNeXt showed much of the gap was the training recipe.

## ⚠️ Important Notes

1. **Scale by $\sqrt{d_k}$ of each head**, not of the full model width ($\sqrt{64} = 8$ for ViT-Base, not $\sqrt{768}$).
2. **Attention weights are not parameters.** The parameters are $W_Q, W_K, W_V, W_O$; the weights are recomputed for every input.
3. **Self-attention ignores order.** Without position embeddings a ViT can't distinguish an image from its shuffled patches.
4. **Changing the number of heads doesn't change the parameter count** (for fixed $D$).
5. **Attention cost is quadratic in the number of tokens.** Halving the patch size quadruples the tokens and multiplies the attention-score cost by 16.
6. **When changing input resolution, interpolate the position embeddings.**
7. **Most ViT parameters are in the MLPs (2/3), not the attention (1/3).**
8. **ViT isn't convolution-free:** its patch embedding is a convolution with kernel = stride = $P$.
9. **Attention maps show what was read, not what was decisive.** Don't treat them as explanations.
10. **Pre-norm** (LayerNorm before each sublayer, inside the residual) keeps a clean identity path and makes training stable.
11. **"Transformers need huge data" is partly a recipe problem.** DeiT matched it on ImageNet-1k with augmentation and regularisation alone.
12. **Distillation's $T^2$ factor** compensates for the $1/T^2$ shrinkage of gradients when logits are divided by $T$.
13. **For small datasets trained from scratch, use a CNN.** For fine-tuning, either works.
14. **Swin's window attention alone would block information between windows**; the shifted-window layers are what let information cross boundaries.

> [!warning] Gaps in the source material
> - **Figures lost in extraction:** 3D convolution figure (slide 2), vanilla transformer diagram (3), dictionary/similarity figures (7–8), position-embedding similarity grid (18), [class] attention maps (19), transformer block diagram (20), ViT end-to-end diagram (21), data-efficiency curve (25), distillation diagrams (30, 34), shifted-window and patch-merging diagrams (39–40). The text and captions carry the content; slide 21's four steps in §2 are reconstructed from the slide title and the summary slide ("four equations").
> - **Lecturer's own experiments** (slides 18, 25, 32: position-embedding similarities, the 100/400/1,257-image comparison, the 97.4% CNN teacher and its entropies) can't be reproduced without the notebook's data. The uniform entropy $\ln 10 = 2.303$ was checked.
> - **Added beyond the slides:** the written equations for the Transformer block; the meaning of the two terms in $\Omega(\text{MSA})$; the 64× window-attention saving at a 56×56 grid; the 169 = $(2M-1)^2$ derivation; the explanation of KL and temperature notation; all exercises and Important Notes.

**Previous:** [[05 - CNN Architectures]] · **Next:** [[07 - Object Detection I]]
