---
subject: Computer Vision
chapter: 6
tags: [ds, computer-vision, vit, transformer, patch-embedding, swin, inductive-bias, attention]
source: "Dosovitskiy et al. 2021 (ViT); Liu et al. 2021 (Swin); Szeliski, *Computer Vision*, 2nd ed. §5.5.3; Stanford CS231n; the lecturer's course outline"
---

# Vision Transformers

**Week 6 of 14. ⚠️ NO SLIDES** — see [[00-Index]].

> [!note] ⚠️ A **depth** chapter, unlike [[04 - From Neural Networks to CNNs|ch. 04]] and [[05 - CNN Architectures|ch. 05]]
> **[[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] owns the Transformer** — attention as a database lookup, the $1/\sqrt d$ scaling, multi-head, positional encoding, the encoder–decoder, and the parameter budget. **It does not cover ViT at all.** This chapter is the vision half, and it is developed in full.

**Five results.**

**§3 — ⚠️ ATTENTION OVERTAKES THE FEED-FORWARD NETWORK AT EXACTLY $n>2d$.** At ViT-Base's $d=768$ that is **1,536 tokens — a $624\times624$ image**. **At ViT's own design point (224², $n=196$) attention is only 36.1% of the layer's FLOPs**; at 1024² it is **64.7%**, and at 2048² **85.4%**.

**§6 — ⚠️ ViT-BASE COMES TO 86,528,488 PARAMETERS, MATCHING THE QUOTED ~86M — AND THE FFN/ATTENTION SPLIT IS EXACTLY 66.7%/33.3%.** **[[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §10's inversion holds in vision**: the component the architecture is named after holds a third of its weights.

**§2 — ⚠️ HALVING THE PATCH SIZE QUADRUPLES THE TOKENS AND MULTIPLIES ATTENTION WORK BY 16.** $P=16\to8$ is $196\to784$ tokens and $38{,}416\to614{,}656$; $P=4$ is **256×**.

**§5 — ⚠️ A ViT's FIRST LAYER SEES 100% OF THE IMAGE; A $3\times3$ CONVOLUTION SEES 0.02%.** That is [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §8's path length 1 in vision — **and the price is that everything a CNN gets free must be learned from data.**

**§4 — ⚠️ SWIN'S SAVING IS EXACTLY $n/M$, AND IT GROWS WITH RESOLUTION.** Window attention is $O(nMd)$ against full attention's $O(n^2d)$ — **64× at 224², 1,338× at 1024².** *The saving grows precisely because the problem does.*

## 📘 Main Knowledge

### 1. The idea: an image is a sequence of patches

**The Transformer ([[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]]) needs a sequence of vectors. ViT (Dosovitskiy et al. 2021) makes one out of an image in the simplest possible way:**

1. **Cut the image into non-overlapping $P\times P$ patches.**
2. **Flatten each to a $P^2C$ vector and project linearly to $d$.**
3. **Prepend a learnable `[CLS]` token; add learned positional embeddings.**
4. **Run a standard Transformer encoder; classify from the `[CLS]` output.**

**That is the whole architecture.** The paper's own framing — *"An Image is Worth 16×16 Words"* — is accurate: **after step 2 nothing is vision-specific.**

> [!note] ⚠️ The patch embedding **is** a convolution
> A linear projection of non-overlapping $P\times P$ patches is exactly **a $P\times P$ convolution with stride $P$**. Every implementation does it that way.
>
> ⇒ *ViT is not "a Transformer with no convolution" — it is a Transformer with **exactly one** convolutional layer, of stride equal to its kernel size, so that receptive fields never overlap.* **That single layer is the only place local structure is used.**

### 2. ⚠️ Patch arithmetic, and why patch size is the critical hyperparameter

| image | patch | **tokens $n$** | patch dim $P^2C$ | $+$ `[CLS]` |
|---|---|---|---|---|
| $224^2$ | $32^2$ | 49 | 3,072 | 50 |
| **$224^2$** | **$16^2$** | **196** | **768** | **197** |
| $384^2$ | $16^2$ | 576 | 768 | 577 |
| $512^2$ | $16^2$ | 1,024 | 768 | 1,025 |
| $1024^2$ | $16^2$ | 4,096 | 768 | 4,097 |

**ViT-Base/16 at 224²**: $n=196$ patches $+1$ `[CLS]` $=\mathbf{197}$ tokens, each a $16\cdot16\cdot3=768$-dim vector projected to $d=768$. The projection is $768\times768+768=\mathbf{590{,}592}$ parameters; the positional embeddings are $197\times768=\mathbf{151{,}296}$.

> [!warning] ⚠️ HALVING THE PATCH QUADRUPLES $n$ — AND ATTENTION IS $O(n^2)$
> | patch | tokens | $n^2$ | vs $P=16$ |
> |---|---|---|---|
> | $32^2$ | 49 | 2,401 | 0.06× |
> | **$16^2$** | **196** | **38,416** | **1×** |
> | $8^2$ | 784 | 614,656 | **16×** |
> | $4^2$ | 3,136 | 9,834,496 | **256×** |
>
> ⇒ ***patch size is the single most consequential hyperparameter in a ViT***, and it is a direct trade: **smaller patches give finer spatial detail and cost $16\times$ per halving.** *This is why ViT ships as /32, /16 and /14 variants and why /8 is rare — and it is the same $r^2$-in-FLOPs argument as [[05 - CNN Architectures|ch. 05]] §2's resolution dial, sharpened by the quadratic.*

### 3. ⚠️ Where attention overtakes the feed-forward network: $n>2d$

Per encoder layer, with the standard $d_{\text{ffn}}=4d$:

| component | FLOPs |
|---|---|
| QKV projections | $3nd^2$ |
| attention scores $\mathbf{QK}^\top$ | $n^2d$ |
| attention-weighted $\mathbf V$ | $n^2d$ |
| output projection | $nd^2$ |
| **feed-forward network** | $8nd^2$ |

$$\text{attention}=4nd^2+2n^2d\ >\ 8nd^2=\text{FFN}\iff \boxed{n>2d}$$

| $d$ | crossover $n$ | image at $16\times16$ patches |
|---|---|---|
| 384 | 768 | $448\times448$ |
| **768** (ViT-Base) | **1,536** | **$624\times624$** |
| 1024 | 2,048 | $720\times720$ |

**Attention's share of ViT-Base's layer FLOPs:**

| image | $n$ | attention | FFN | **attention share** |
|---|---|---|---|---|
| **$224^2$** | 196 | $5.21\times10^8$ | $9.25\times10^8$ | **36.1%** |
| $384^2$ | 576 | $1.87\times10^9$ | $2.72\times10^9$ | 40.7% |
| $512^2$ | 1,024 | $4.03\times10^9$ | $4.83\times10^9$ | 45.5% |
| $640^2$ | 1,600 | $7.71\times10^9$ | $7.55\times10^9$ | **50.5%** |
| $1024^2$ | 4,096 | $3.54\times10^{10}$ | $1.93\times10^{10}$ | **64.7%** |
| $2048^2$ | 16,384 | $4.51\times10^{11}$ | $7.73\times10^{10}$ | **85.4%** |

> [!warning] ⚠️ AT ViT's OWN DESIGN POINT, ATTENTION IS A MINORITY OF THE WORK
> **36.1% at 224² — the feed-forward network dominates**, exactly as [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §10 found for *parameters* (66.7% FFN / 33.3% attention).
>
> ⇒ ***the "quadratic cost of attention" is not the bottleneck at ViT's standard resolution.*** It becomes one only past $624\times624$ — and then it becomes one very fast, reaching 85.4% at 2048².
>
> **This is [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §8's $n<d$ crossover in a vision setting**, and it explains the whole shape of the field: **classification at 224² is comfortable, and dense prediction at high resolution ([[09 - Segmentation|ch. 09]]) is not** — which is what §4 fixes.

### 4. ⚠️ Swin — making the cost linear again

**Full attention over $n$ tokens is $O(n^2d)$. Window attention over windows of $M$ tokens is $O(nMd)$**, because each of the $n/M$ windows costs $M^2d$.

| image | tokens $n$ | full $n^2d$ | window $nMd$ ($M=49$) | **saving** |
|---|---|---|---|---|
| $224^2$ | 3,136 | $9.44\times10^8$ | $1.48\times10^7$ | **64×** |
| $384^2$ | 9,216 | $8.15\times10^9$ | $4.34\times10^7$ | 188× |
| $512^2$ | 16,384 | $2.58\times10^{10}$ | $7.71\times10^7$ | 334× |
| $1024^2$ | 65,536 | $4.12\times10^{11}$ | $3.08\times10^8$ | **1,338×** |

> [!warning] ⚠️ THE SAVING IS EXACTLY $n/M$ — SO IT GROWS PRECISELY WHERE IT IS NEEDED
> $\dfrac{n^2d}{nMd}=\dfrac{n}{M}$. **The larger the image, the bigger the win** — which is the opposite of most optimizations, and the reason Swin became the default backbone for dense prediction.
>
> **The cost: a token can only see its own $M\times M$ window in one layer.** Swin's **shifted windows** alternate the partition between layers so information crosses boundaries every other layer, **restoring a global receptive field over depth rather than within a layer.**
>
> **How long that takes**: with $7\times7$ windows shifted by 3, the receptive field grows ~6 tokens per layer, so a $56\times56$ token grid (224² at $4\times4$ patches) needs **~10 layers** for full coverage and a $256\times256$ grid (1024²) needs **~43**.
>
> ⇒ ***Swin trades ViT's path length of 1 for a path length that grows like $n_{\text{side}}/6$*** — **it gives back exactly the property [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §8 identified as attention's whole advantage.** *That is a real cost, and it is why ViT and Swin coexist rather than one replacing the other.*

**Swin's second idea is hierarchy**: start at $4\times4$ patches and **merge $2\times2$ neighbourhoods between stages**, halving resolution and doubling channels — *exactly [[05 - CNN Architectures|ch. 05]] §3's CNN stage pattern, reimported into a Transformer.* **That is what makes Swin a drop-in backbone for detection and segmentation, which need multi-scale features.**

### 5. ⚠️ The inductive-bias trade, and what it costs

| | layer-1 receptive field | as % of a 224² image |
|---|---|---|
| **CNN $3\times3$ conv** | $3\times3$ px | **0.02%** |
| **ViT self-attention** | **the whole image** | **100%** |

**A ViT has a global receptive field in its first layer** — [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §8's max path length of 1, in vision.

> [!warning] ⚠️ THE PRICE: WHAT A CNN GETS FOR FREE, A ViT MUST LEARN FROM DATA
> **A CNN builds in translation equivariance and locality** ([[04 - From Neural Networks to CNNs|ch. 04]] §4). **A ViT builds in almost nothing** — patches, then global attention, then learned positional embeddings that it must *discover* encode 2-D layout.
>
> **The published pattern (Dosovitskiy et al. 2021):**
>
> | pretraining data | outcome |
> |---|---|
> | ImageNet-1k (1.3M) | **ViT underperforms** a comparable ResNet |
> | ImageNet-21k (14M) | roughly comparable |
> | **JFT-300M (300M)** | **ViT overtakes** |
>
> **The crossover sits between $10^7$ and $10^8$ labelled images.**
>
> ⇒ ***ViT sits between the MLP and the CNN on the prior/data axis*** — more prior than an MLP (patches are local, so it is not permutation-invariant across the whole image), far less than a CNN (**no weight sharing across positions**). **Its data requirement sits between them too**, and [[04 - From Neural Networks to CNNs|ch. 04]] §3 measured the CNN end of that axis: one $3\times3$ filter reused at 49,284 positions, against 49,284 independent copies and ~$5\times10^4\times$ the data.
>
> **⚠️ AND THIS IS THE GENERAL LAW, not a fact about ViT**: *a weaker prior needs more data, and buys more flexibility when the data exists.* **Which side of the crossover you are on is a property of your dataset, not of the architecture.**

**The consequence for practice is blunt: almost nobody trains a ViT from scratch.** Fine-tuning a model pretrained on ImageNet-21k or larger is the norm — which is [[Deep Learning/contents/06 - Object Detection|DL ch. 06]] §1's transfer-learning argument, made compulsory rather than merely convenient.

**Hybrid designs** close the gap from the other side: use a CNN stem to produce the tokens, or reintroduce convolutions inside the blocks, buying back locality without giving up global attention. *(And **ConvNeXt (2022)** ran the experiment in reverse — modernizing a pure CNN with the Transformer era's training recipe and design choices, and matching Swin. **That result matters: it shows a large part of ViT's advantage was the training recipe, not the attention.** See [[05 - CNN Architectures|ch. 05]].)*

### 6. ⚠️ The parameter budget — and DL ch. 08's inversion, again

**ViT-Base**: $d=768$, $L=12$ layers, $d_{\text{ffn}}=3072$.

| | parameters | share of a layer |
|---|---|---|
| attention ($4d^2$) | 2,359,296 | **33.3%** |
| **feed-forward** | **4,722,432** | **66.7%** |
| LayerNorm ($2\times2d$) | 3,072 | 0.04% |
| **per layer** | **7,084,800** | |
| $\times12$ layers | 85,017,600 | |
| patch embedding | 590,592 | |
| positional embeddings | 151,296 | |
| classifier head ($d\to1000$) | 769,000 | |
| **TOTAL** | **86,528,488** | **330.1 MB fp32** |

> [!warning] ⚠️ 86,528,488 AGAINST THE UNIVERSALLY QUOTED "~86M" — an independent check that the budget is right
> **And the split is exactly [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §10's**: FFN **66.7%**, attention **33.3%**, ratio $d_{\text{ffn}}/(2d)=2.00$.
>
> ⇒ ***the inversion holds in vision: the component the architecture is named after holds a third of its weights.*** *Third setting for this pattern, after [[05 - CNN Architectures|ch. 05]]'s conv-vs-head and DL ch. 08's language Transformer.*
>
> **For scale: ResNet-50 is ~25.6M parameters, so ViT-Base is 3.4× larger** — and by [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5 needs **1.29 GB to train with Adam** before activations.

## ✏️ Exercises

> [!example]- Exercise 1 — patch arithmetic
> **(a)** Tokens for $224^2$ at $P=16$, $P=8$, and for $384^2$ at $P=16$. **(b)** Patch-embedding parameters for ViT-Base/16. **(c)** What happens to attention cost when $P$ halves? **(d)** Why is /8 rare?
>
> ---
> **(a)** $(224/16)^2=\mathbf{196}$; $(224/8)^2=\mathbf{784}$; $(384/16)^2=\mathbf{576}$. Add 1 for `[CLS]`.
>
> **(b)** Each patch is $16\cdot16\cdot3=768$ numbers projected to $d=768$: $768\times768+768=\mathbf{590{,}592}$. Positional embeddings add $197\times768=\mathbf{151{,}296}$.
>
> **(c)** $n$ **quadruples** and attention is $O(n^2)$, so attention work goes $\times\mathbf{16}$: $38{,}416\to614{,}656$.
>
> **(d)** ⚠️ **$P=4$ would be 256× the attention work of $P=16$.** The gain is finer spatial detail; the cost is quadratic. ⇒ *patch size is the resolution dial of [[05 - CNN Architectures|ch. 05]] §2 with a square-law penalty instead of a linear one* — which is exactly why hierarchical designs (Swin) start small and **merge** rather than starting small and staying there.

> [!example]- Exercise 2 — when does attention actually dominate?
> **(a)** Write per-layer FLOPs for attention and FFN with $d_{\text{ffn}}=4d$. **(b)** Find the crossover. **(c)** Evaluate for ViT-Base at 224², 640² and 1024². **(d)** What does that say about "attention is quadratic"?
>
> ---
> **(a)** Attention $=3nd^2$ (QKV) $+\,2n^2d$ (scores and weighting) $+\,nd^2$ (output) $=4nd^2+2n^2d$. FFN $=2\cdot n\cdot d\cdot4d=8nd^2$.
>
> **(b)** $4nd^2+2n^2d>8nd^2\iff2n^2d>4nd^2\iff\boxed{n>2d}$. **At $d=768$: $n>1{,}536$, i.e. a $624\times624$ image at $16\times16$ patches.**
>
> **(c)** Attention share: **36.1%** at 224², **50.5%** at 640², **64.7%** at 1024² (and 85.4% at 2048²).
>
> **(d)** ⚠️ **At ViT's design point the quadratic term is a minority of the work — the FFN dominates.** "Attention is quadratic" is true asymptotically and misleading at $224^2$. ⇒ *optimizing attention buys at most 36% there; **the quadratic only becomes the problem for dense prediction at high resolution**, which is precisely where Swin is used.* **Check where you are on the curve before optimizing.**

> [!example]- Exercise 3 — windowed attention
> **(a)** Cost of full vs window attention. **(b)** The saving at $224^2$ and $1024^2$ with $M=49$. **(c)** What is given up? **(d)** How does Swin get it back?
>
> ---
> **(a)** Full $O(n^2d)$; window $\frac nM$ windows $\times\,M^2d=O(nMd)$. **Saving $=n/M$.**
>
> **(b)** At $4\times4$ patches: $224^2\to n=3{,}136$, saving **64×**; $1024^2\to n=65{,}536$, saving **1,338×**. ⚠️ **The saving grows with resolution** — unusually, the optimization gets better exactly where the problem gets harder.
>
> **(c)** **Path length.** A token sees only its own window in one layer, so [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §8's max path length of 1 — *the property that made attention worth having* — is lost.
>
> **(d)** **Shifted windows**: alternate the partition each layer so information crosses boundaries every other layer. **Coverage is recovered over depth, not within a layer** — ~10 layers for a $56\times56$ token grid, **~43 for $256\times256$.** ⇒ *Swin's path length grows like $n_{\text{side}}/6$ instead of staying at 1, which is a real cost and why ViT is not obsolete.*

> [!example]- Exercise 4 — the data crossover
> **(a)** Layer-1 receptive fields of a $3\times3$ conv and of ViT self-attention. **(b)** What does a ViT have to learn that a CNN does not? **(c)** Where is the crossover? **(d)** State the general law.
>
> ---
> **(a)** CNN: $3\times3=9$ px $=\mathbf{0.02\%}$ of a 224² image. **ViT: the whole image, 100%** — path length 1.
>
> **(b)** ⚠️ **Translation equivariance and locality.** A CNN's kernel is *shared across positions* by construction; a ViT must learn from data that a pattern at the top-left means the same as one at the centre, and its positional embeddings must *discover* that the token grid is 2-D.
>
> **(c)** **Between $10^7$ and $10^8$ images**: ViT underperforms a ResNet at ImageNet-1k (1.3M), is comparable at ImageNet-21k (14M), and overtakes at JFT-300M.
>
> **(d)** ⚠️ ***A weaker prior needs more data and buys more flexibility once the data exists.*** **Which side of the crossover you are on is a property of your dataset, not of the architecture** — so "ViT beats CNNs" is only true above a data threshold most projects never reach. *That is why almost nobody trains a ViT from scratch, and why the lecturer's project topics are scoped to fine-tuning pretrained models.*

> [!example]- Exercise 5 — count ViT-Base
> **(a)** Parameters per encoder layer at $d=768$, $d_{\text{ffn}}=3072$. **(b)** The full model with patch embedding, positions and a 1000-class head. **(c)** The FFN/attention split. **(d)** Compare with ResNet-50.
>
> ---
> **(a)** Attention $4d^2=\mathbf{2{,}359{,}296}$; FFN $d\cdot d_{\text{ffn}}+d_{\text{ffn}}+d_{\text{ffn}}\cdot d+d=\mathbf{4{,}722{,}432}$; two LayerNorms $4d=3{,}072$. **Total 7,084,800.**
>
> **(b)** $12\times7{,}084{,}800=85{,}017{,}600$, plus patch embedding 590,592, positions 151,296, head 769,000 → **86,528,488 = 330.1 MB fp32.** ✓ *Matches the universally quoted ~86M.*
>
> **(c)** **FFN 66.7%, attention 33.3%** — ratio $d_{\text{ffn}}/(2d)=2.00$, identical to [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §10's language Transformer. ⚠️ **The inversion is architectural, not domain-specific.**
>
> **(d)** ResNet-50 is ~25.6M, so **ViT-Base is 3.4× larger** — and needs **1.29 GB to train with Adam** ([[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5), before activations, which at $n=197$ are modest but grow with $n^2$ for the attention maps.

## 📝 Summary

- **ViT cuts an image into $P\times P$ patches, projects each linearly, adds a `[CLS]` token and learned positions, and runs a standard Transformer encoder.** After the projection **nothing is vision-specific**. ⚠️ **The patch embedding *is* a $P\times P$ convolution with stride $P$** — ViT has exactly one convolutional layer.
- **⚠️ Patch size is the critical hyperparameter**: $224^2$ gives 196 tokens at $P=16$, 784 at $P=8$, 3,136 at $P=4$. **Halving $P$ quadruples $n$ and multiplies attention work by 16** (256× at $P=4$).
- **⚠️ Attention overtakes the FFN at exactly $n>2d$** — **1,536 tokens for ViT-Base, a $624^2$ image.** At its design point (224², $n=196$) **attention is only 36.1% of layer FLOPs**; 64.7% at 1024², 85.4% at 2048². **"Attention is quadratic" is asymptotically true and misleading at 224².**
- **⚠️ Swin's window attention is $O(nMd)$, saving exactly $n/M$ — 64× at 224², 1,338× at 1024².** The saving **grows with resolution**. The cost is path length: a token sees one window per layer, and **shifted windows restore coverage over depth (~10 layers at $56^2$ tokens, ~43 at $256^2$)** rather than within a layer. **Swin also reimports the CNN stage pattern** — merge $2\times2$, halve resolution, double channels — which is what makes it a multi-scale backbone.
- **⚠️ A ViT's first layer sees 100% of the image; a $3\times3$ convolution sees 0.02%.** **The price is that translation equivariance and locality must be learned**: ViT underperforms a ResNet at 1.3M images, matches at 14M, **overtakes at 300M**. ⇒ ***a weaker prior needs more data and buys more flexibility once it exists — and which side you are on is a property of your dataset.***
- **⚠️ ViT-Base is 86,528,488 parameters (330.1 MB), matching the quoted ~86M, with FFN 66.7% and attention 33.3%** — [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §10's inversion holding in a third setting. **3.4× ResNet-50.**
- **Almost nobody trains a ViT from scratch**; hybrids add a CNN stem, and **ConvNeXt showed a modernized pure CNN matches Swin — so much of ViT's advantage was the training recipe, not the attention.**

## ⚠️ Important Notes

1. **⚠️ Do not optimize attention at 224².** It is 36.1% of the work; the FFN is 63.9%. **Profile before assuming the quadratic is your bottleneck** — and note this is the same error [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §23 warns about, optimizing the component the architecture is named after.
2. **⚠️ Positional embeddings are tied to the token count.** Change the input resolution and the learned table no longer matches; **it must be interpolated**, which is a standard but lossy step, and a common silent bug when fine-tuning at a new resolution.
3. **⚠️ ViT has no multi-scale structure.** All layers operate at one token resolution, which is why plain ViT is awkward for detection and segmentation and why **Swin's hierarchy — not its windowing — is what made Transformers usable as detection backbones.**
4. **⚠️ "ViT beats CNNs" is conditional on data volume.** Below ~10M images a comparable ResNet usually wins. **State the pretraining set whenever you quote a ViT result** — it is doing most of the work.
5. **⚠️ Attention maps are not explanations.** [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]]'s note applies unchanged: they show what was *read*, not what was *used*, since $\mathbf W_o$ and the FFN come after. **Pretty ViT attention visualizations are diagnostics, not evidence.**
6. **⚠️ The `[CLS]` token is a design choice, not a necessity.** Global average pooling over patch tokens works comparably; **if a paper reports one, check which** — they are not interchangeable when transferring to dense tasks.
7. **⚠️ Attention activation memory grows as $n^2$ per head per layer.** At $n=196$ this is trivial; at $n=4096$ ($1024^2$) it is $4096^2\times12\times12$ floats retained for the backward pass. **Sequence length, not parameter count, is what exhausts the GPU** — [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]]'s note, and it is why high-resolution ViT training needs windowing or checkpointing.
8. **Patches destroy sub-patch structure irreversibly.** Anything finer than $P\times P$ can only be represented within a single token's $d$ dimensions. **For fine detail, reduce $P$ or use a hierarchical model** — no amount of depth recovers it.

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). Built from the **ViT paper (Dosovitskiy et al. 2021)**, the **Swin paper (Liu et al. 2021)**, **Szeliski §5.5.3 (Transformers)** — which is brief and language-oriented — **CS231n**, and this vault's [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]].
>
> **⚠️ Unlike [[04 - From Neural Networks to CNNs|ch. 04]] and [[05 - CNN Architectures|ch. 05]], this is a full-depth chapter**, because [[00-Index]]'s boundary table records that **DL ch. 08 has the Transformer but not ViT**. The Transformer machinery itself — attention as a soft lookup, $1/\sqrt d$ and softmax saturation, multi-head being free at $4p_o^2$, sinusoidal positional encoding, the encoder–decoder — **is linked, not repeated.**
>
> **⚠️ The emphasis is inferred.** The lecturer's topic title is *"Vision transformers"*; the choice to organize around patch arithmetic, the $n>2d$ crossover, Swin, and the data trade-off follows from what is standard for that title and from what DL ch. 08 leaves uncovered. **Which specific models week 6 treats is unknown.** DeiT (distillation-based data-efficient training), MAE (masked autoencoders — deferred to [[12 - Self-Supervised Learning|ch. 12]], where it belongs), and the many efficient-attention variants are **named nowhere and not developed.**
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **§3's entire $n>2d$ derivation and the attention-share table.** *The quadratic cost of attention is universally noted; **the crossover point, and the finding that attention is only 36.1% of the work at ViT's own design point, are mine**.* This is [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]] §8's $n<d$ result specialized to vision and evaluated.
> - **§2's patch table** and the $16\times$-per-halving consequence.
> - **§4's window-saving table** and the observation that **the saving is exactly $n/M$ and therefore grows with resolution**, plus the **shifted-window coverage estimate** (~10 and ~43 layers) that quantifies what Swin gives up.
> - **§5's receptive-field comparison** (0.02% vs 100%) and the framing of ViT as sitting **between** the MLP and the CNN on a prior/data axis, connected to [[04 - From Neural Networks to CNNs|ch. 04]] §3's 49,284-copies measurement.
> - **§6's complete parameter budget**, independently reproducing the quoted ~86M and confirming **DL ch. 08 §10's 66.7%/33.3% inversion in vision.**
> - **All eight Important Notes.**
>
> **No discrepancies found.** ⚠️ **One class of claim is deliberately reported qualitatively**: the ViT-vs-ResNet accuracy crossover across ImageNet-1k / ImageNet-21k / JFT-300M is stated **as a pattern with dataset sizes, without quoting accuracies** — those are external results this chapter cannot verify, and the vault's rule is not to quote unverified numbers. **The ~25.6M figure for ResNet-50 is likewise external and flagged as such.**
>
> **Deliberately deferred, not omitted:** **all Transformer machinery** is [[Deep Learning/contents/08 - Sequence to Sequence|DL ch. 08]]. **Masked autoencoders (MAE) and contrastive pretraining of ViTs** belong to [[12 - Self-Supervised Learning|ch. 12]] and are held there. **DETR** — a Transformer detector — belongs to [[08 - Object Detection II|ch. 08]]. **ConvNeXt** is mentioned in §5 for the argument it settles and belongs properly to [[05 - CNN Architectures|ch. 05]]. **Efficient-attention variants** (Performer, Linformer, FlashAttention) are engineering that no week of this outline names.
>
> **Left as the source states it:** the ViT paper's pretraining-scale results and the JFT-300M dataset size; the Swin paper's window size of 7 and shift of 3; ResNet-50's ~25.6M parameters; and ConvNeXt's claim to match Swin, which is an external benchmark result.

**Previous:** [[05 - CNN Architectures]] · **Next:** [[07 - Object Detection I]]
