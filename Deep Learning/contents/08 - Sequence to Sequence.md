---
subject: Deep Learning
chapter: 8
tags: [ds, deep-learning, seq2seq, encoder-decoder, bleu, beam-search, attention, transformer, self-attention, positional-encoding]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, §10.5–10.8 (Machine Translation, Encoder–Decoder, Seq2seq, Beam Search) and §11.1–11.7 (Attention, Multi-Head, Self-Attention, the Transformer)"
---

# Sequence to Sequence

**The last chapter of the subject, and the largest scope.** D2L §10.5–10.8 builds the encoder–decoder and its evaluation; **§11.1–11.7 is a scope addition flagged in [[00-Index]]** — seq2seq without attention stops exactly where the field turned.

**Six results.**

**§8 — ⚠️ THE CROSSOVER D2L SETS UP IN ITS OWN TABLE AND NEVER STATES: SELF-ATTENTION IS CHEAPER THAN AN RNN WHENEVER $n<d$.** $O(n^2d)$ against $O(nd^2)$. **At the Transformer's $d=512$, self-attention wins at every sequence length below 512 tokens — which is most sentences.** D2L says only that it is "prohibitively slow for very long sequences."

**§8 — ⚠️ AND THE REAL PAYOFF IS THE PATH LENGTH, WHICH IS [[07 - Recurrent Neural Network|ch. 07]]'S ENTIRE PROBLEM DISSOLVED.** Ch. 07 §7 found that a path of length $T$ forces the recurrent Jacobian within $10^{\pm3/T}$ of 1 — **±0.693% at $T=1000$. Self-attention's path length is 1, where the admissible band is ±99,900%.** ⇒ ***attention did not replace recurrence because it is faster; it replaced it because it deletes the product.***

**§2 — ⚠️ ONE ZERO PRECISION ZEROES BLEU ENTIRELY, AND D2L PRINTS AN EXAMPLE WITHOUT COMMENT.** Its own run scores *"soyez calmes ."* against *"il est calme ."* as **exactly 0.000** — the same as a translation that got nothing right — although it is a valid imperative rendering of "he's calm".

**§10 — ⚠️ THE FEED-FORWARD NETWORK IS TWO-THIRDS OF A TRANSFORMER LAYER, AND EVERYONE CALLS IT "THE ATTENTION MODEL".** At $d_{\text{model}}=512$, $d_{\text{ffn}}=2048$: **attention 1,048,576 (33.3%), FFN 2,099,712 (66.7%)**, LayerNorm 2,048 (0.1%).

**§7 — ⚠️ MULTI-HEAD ATTENTION IS FREE, EXACTLY.** With $p_q=p_k=p_v=p_o/h$ the projections total $4p_o^2$ **at every $h$** — verified for $h=1,2,4,8,16$. **The heads partition one budget rather than adding to it**, so single-head at the same width is strictly worse.

**§6 — ⚠️ THE $1/\sqrt d$ IS NOT COSMETIC: WITHOUT IT THE SOFTMAX SATURATES AND THE GRADIENT DIES.** Unscaled at $d=512$ the logits have sd **22.63**, the max attention weight is **0.9523** and the entropy **0.117 nats** — effectively one-hot. Scaled, entropy is **1.92 of a possible 2.30**.

## 📘 Main Knowledge

### 1. Machine translation, and why the data is different

Unlike [[07 - Recurrent Neural Network|ch. 07]]'s language modelling, MT is **sequence-to-sequence**: input and output are *different* sequences in *different* languages, of *different* lengths.

Three consequences shape everything after:
- **Two vocabularies**, source and target, built independently.
- **Fixed-length batching** requires padding shorter sequences with `<pad>` and recording a **valid length** — which is why masking appears everywhere in this chapter.
- **Special tokens**: `<bos>` starts the decoder, `<eos>` ends generation, `<unk>` absorbs out-of-vocabulary words.

### 2. ⚠️ The encoder–decoder architecture, and BLEU's failure mode

**The encoder** maps a variable-length input to a fixed-shape **state**; **the decoder** maps that state plus what it has generated so far to the next token. **That interface is the whole abstraction**, and it is what lets you swap an RNN encoder for a CNN or a Transformer without touching the decoder.

**Teacher forcing.** During training the decoder is fed **the ground-truth previous token**, not its own prediction. *(D2L's exercise 10.7.4 asks what happens if you feed the prediction instead — the answer is that training becomes slower and less stable, but test-time behaviour is better matched. The mismatch has a name: **exposure bias**.)*

**Masked loss.** Padded positions must not contribute; the loss is multiplied by a validity mask — the same device as [[06 - Object Detection|ch. 06]]'s `bbox_masks`.

**BLEU** (Papineni et al. 2002) scores $n$-gram overlap with a reference:

$$\mathrm{BLEU}=\underbrace{\exp\left(\min\left(0,\ 1-\frac{\mathrm{len}_{\text{label}}}{\mathrm{len}_{\text{pred}}}\right)\right)}_{\text{brevity penalty}}\prod_{n=1}^{k}p_n^{1/2^n}$$

where $p_n$ is the **clipped** $n$-gram precision.

**D2L's worked example reproduced exactly** — target `A B C D E F`, prediction `A B B C D`:

| | computed | D2L states |
|---|---|---|
| $p_1$ | **4/5** | 4/5 ✓ |
| $p_2$ | **3/4** | 3/4 ✓ |
| $p_3$ | **1/3** | 1/3 ✓ |
| $p_4$ | **0/2 = 0** | 0 ✓ |

*(The clipping matters: the prediction contains `B` twice and the target once, so only one `B` counts.)*

**The exponent $1/2^n$ weights longer $n$-grams more heavily** — for fixed $p_n$, $p_n^{1/2^n}$ increases with $n$ — because matching a long $n$-gram is harder evidence. **The brevity penalty verified**: target of 6, prediction `A B` of 2, with $p_1=p_2=1$ **perfect**, scores $\exp(1-3)=\mathbf{0.135335}$ (D2L says "≈0.14" ✓).

> [!warning] ⚠️ ONE ZERO PRECISION ZEROES THE WHOLE SCORE — and D2L prints the case without comment
> Its four printed translations all reproduce:
>
> | English | predicted | target | BLEU |
> |---|---|---|---|
> | go . | va ! | va ! | 1.000 ✓ |
> | i lost . | j'ai perdu . | j'ai perdu . | 1.000 ✓ |
> | **he's calm .** | **soyez calmes .** | il est calme . | **0.000** ✓ |
> | i'm home . | je suis chez moi . | je suis chez moi . | 1.000 ✓ |
>
> **The third row:** $p_1=1/3$, $p_2=\mathbf{0/2=0}$, brevity penalty 0.716531 — and **BLEU is a product**, so $0^{1/4}=0$ collapses everything.
>
> ⚠️ **That translation got one token of three right and scores *exactly the same* as one that got nothing right.** And *"soyez calmes"* is a legitimate imperative rendering of "he's calm" — **BLEU cannot see that**, because it compares $n$-grams against **one** reference.
>
> ⇒ ***BLEU measures $n$-gram overlap with a single reference, not translation quality.*** The original paper uses **multiple references and corpus-level counts** precisely to blunt both failures; D2L's sentence-level, single-reference version is the fragile special case. *(This is the vault's recurring "an accurate number that means something other than it appears" pattern — the 0.000 is correctly computed and is not a measure of quality.)*

### 3. ⚠️ Decoding: greedy, exhaustive, and beam

**Greedy search** takes $\arg\max$ at each step. **It optimizes the most likely *token* at each step, not the most likely *sequence*** — and those differ.

**D2L's example, verified:**

| sequence | probability |
|---|---|
| greedy `A B C <eos>` | $0.5\times0.4\times0.4\times0.6=\mathbf{0.048}$ ✓ |
| alternative `A C B <eos>` | $0.5\times0.3\times0.6\times0.6=\mathbf{0.054}$ ✓ |

**The greedy sequence is 11.11% less likely**, and the better sequence's second token had only the **second**-highest probability (0.3 vs 0.4). **Greedy cannot recover from a locally suboptimal choice, because the conditional distributions at every later step change.**

**Exhaustive search** would find the optimum at $O(|\mathcal Y|^{T'})$ — at $|\mathcal Y|=10^4$, $T'=10$ that is $\mathbf{10^{40}}$ sequences ✓. **Greedy is $O(|\mathcal Y|T')=\mathbf{10^5}$** ✓.

**Beam search** keeps the $k$ best partial sequences at each step, costing $O(k|\mathcal Y|T')$:

| strategy | sequences scored |
|---|---|
| greedy | $10^5$ |
| **beam, $k=10$** | $\mathbf{10^6}$ |
| exhaustive | $10^{40}$ |

> [!warning] ⚠️ Beam search costs **10× greedy and $10^{34}$× less than exhaustive** — that ratio is why it is universal
> **And the length-normalized score matters**: candidates of different lengths are compared by $\frac{1}{L^\alpha}\log P$, because an unnormalized log-probability is a sum of negative terms and **always prefers shorter sequences.** *Without normalization, beam search systematically truncates.*

### 4. Attention as a database lookup

The unifying abstraction: given a **query** $\mathbf q$ and pairs of **keys** and **values** $(\mathbf k_i,\mathbf v_i)$,

$$\mathrm{Attention}(\mathbf q,\mathcal D)=\sum_i\alpha(\mathbf q,\mathbf k_i)\,\mathbf v_i,\qquad \alpha=\mathrm{softmax}\big(a(\mathbf q,\mathbf k_i)\big)$$

**A hard database lookup is the degenerate case** where $\alpha$ is 1 on the matching key and 0 elsewhere. **Attention is a differentiable, soft lookup** — and differentiability is the whole point, since a hard lookup has no gradient.

> [!note] D2L derives the dot product from a Gaussian kernel, which is worth keeping
> $-\tfrac12\|\mathbf q-\mathbf k_i\|^2=\mathbf q^\top\mathbf k_i-\tfrac12\|\mathbf k_i\|^2-\tfrac12\|\mathbf q\|^2$. **The $\|\mathbf q\|^2$ term is identical for all $i$ and cancels in the softmax; $\|\mathbf k_i\|^2$ is near-constant when the keys come from a layer norm.** What is left is $\mathbf q^\top\mathbf k_i$.
>
> ⇒ ***dot-product attention is a Gaussian kernel with two terms dropped for good reasons*** — which also explains why it is used *with* layer normalization and would be shakier without it.

**Additive attention** ($a=\mathbf w_v^\top\tanh(\mathbf W_q\mathbf q+\mathbf W_k\mathbf k)$) handles $\mathbf q$ and $\mathbf k$ of different dimensions and is otherwise dominated by the dot product, which needs no parameters and maps onto matrix multiplication.

**Masked softmax** zeroes padded positions by setting their logits to a large negative number ($-10^6$) rather than branching — *"faster to be slightly wasteful in computation rather than to have code with conditional statements."* **A GPU-shaped design decision, and worth recognizing as one.**

### 5. Bahdanau attention — the fixed-length bottleneck, removed

**The problem** with §2's encoder–decoder: **the entire source sentence is compressed into one fixed-length vector.** Whatever the sentence length, the decoder sees the same $d$ numbers.

**Bahdanau et al. (2014)**: at each decoding step, the decoder's previous hidden state is the **query**; the encoder's hidden state at *every* source position supplies the **keys and values**. **The context vector is recomputed at every output step.**

> [!warning] ⚠️ This is the hinge of the whole chapter
> **Before:** context is fixed, so information about source token 1 must survive $n$ recurrent steps to reach the encoder's final state, then $t$ more to reach output $t$. **Path length $O(n+t)$ — and [[07 - Recurrent Neural Network|ch. 07]] §7 says a path of length 1,000 needs the Jacobian within ±0.693% of 1.**
>
> **After:** every output position reads every source position **directly**. **Path length $O(1)$ across the encoder–decoder boundary.**
>
> ⇒ *attention was introduced to fix a **bottleneck**, and the fact that it also fixes the **gradient path** is what made the Transformer possible.*

### 6. ⚠️ Scaled dot product — and what the $\sqrt d$ actually buys

If the entries of $\mathbf q,\mathbf k\in\mathbb R^d$ are independent with zero mean and unit variance, **$\mathbf q^\top\mathbf k$ has mean 0 and variance $d$.** Hence

$$a(\mathbf q,\mathbf k_i)=\frac{\mathbf q^\top\mathbf k_i}{\sqrt d}$$

**Verified by simulation** (200,000 draws per row):

| $d$ | $\operatorname{Var}[\mathbf q^\top\mathbf k]$ | theory | after $/\sqrt d$ |
|---|---|---|---|
| 4 | 3.9959 | 4 | 0.9990 |
| 64 | 63.9494 | 64 | 0.9992 |
| **512** | **510.4430** | **512** | **0.9970** |

> [!warning] ⚠️ THE CONSEQUENCE D2L LEAVES IMPLICIT: A SATURATED SOFTMAX HAS NO GRADIENT
> Unscaled, the logits at $d=512$ have standard deviation **22.63**. Measured over 2,000 random draws:
>
> | | sd of logits | max attention weight | entropy (nats) |
> |---|---|---|---|
> | **unscaled, $d=512$, $n=10$ keys** | 22.63 | **0.9523** | **0.1170** |
> | unscaled, $d=512$, $n=100$ | 22.63 | 0.9305 | 0.1812 |
> | unscaled, $d=64$, $n=10$ | 8.00 | 0.8646 | 0.3489 |
> | **scaled, any $d$, $n=10$** | **1.00** | **0.3205** | **1.9228** (uniform 2.3026) |
> | scaled, any $d$, $n=100$ | 1.00 | 0.0807 | 4.1238 (uniform 4.6052) |
>
> **Unscaled at $d=512$ the attention is effectively one-hot** — and the softmax Jacobian $p_i(\delta_{ij}-p_j)$ vanishes when $p$ is one-hot.
>
> ⇒ ***the $1/\sqrt d$ is what keeps the attention distribution soft enough to have a usable gradient at large $d$.*** It is not a normalization nicety; **without it, deep attention models do not train.** *(D2L gives the variance argument and stops; the softmax-saturation consequence is the reason the argument matters.)*

### 7. ⚠️ Multi-head attention — free, exactly

Project $\mathbf q,\mathbf k,\mathbf v$ into $h$ subspaces, attend independently, concatenate, project out. **D2L's design choice is the key: $p_q=p_k=p_v=p_o/h$.**

| heads $h$ | $p_o/h$ | Q,K,V parameters | output $\mathbf W_o$ |
|---|---|---|---|
| 1 | 512 | **786,432** | 262,144 |
| 4 | 128 | **786,432** | 262,144 |
| 8 | 64 | **786,432** | 262,144 |
| 16 | 32 | **786,432** | 262,144 |

> [!warning] ⚠️ IDENTICAL AT EVERY $h$ — the total attention block is $4p_o^2$ regardless
> The $h$ heads' projections together are $h\times(d\times p_o/h)=d\times p_o$ — **exactly the size of one full projection.**
>
> ⇒ ***the heads partition one budget into $h$ subspaces rather than adding to it.*** Single-head attention at the same width is strictly worse: same cost, less diversity, one similarity structure instead of $h$.
>
> **This is the same "free structure" move as [[05 - Convolutional Neural Network|ch. 05]] §15's grouped convolutions** — split the channels, pay nothing, gain independence — and the same as its cost: **no information crosses heads until $\mathbf W_o$ mixes them.**

### 8. ⚠️ Self-attention versus CNNs and RNNs — the table, and the two numbers it hides

**Self-attention** is the case $\mathbf q=\mathbf k=\mathbf v=$ the sequence itself. D2L's comparison:

| | complexity | sequential ops | **max path length** |
|---|---|---|---|
| CNN (kernel $k$) | $O(knd^2)$ | $O(1)$ | $O(n/k)$ |
| **RNN** | $O(nd^2)$ | $\mathbf{O(n)}$ | $\mathbf{O(n)}$ |
| **self-attention** | $\mathbf{O(n^2d)}$ | $O(1)$ | $\mathbf{O(1)}$ |

> [!warning] ⚠️ FIRST HIDDEN NUMBER: SELF-ATTENTION IS CHEAPER THAN AN RNN IFF $n<d$
> $n^2d<nd^2\iff n<d$.
>
> | $d$ | $n=64$ | $n=256$ | $n=512$ | $n=2048$ |
> |---|---|---|---|---|
> | 128 | RNN | RNN | RNN | RNN |
> | **512** | **self-attn** | **self-attn** | tie | RNN |
> | 1024 | self-attn | self-attn | **self-attn** | RNN |
>
> ⇒ **at the Transformer's $d_{\text{model}}=512$, self-attention is cheaper than an RNN at every sequence length below 512 tokens — which covers most sentences.** D2L says only "prohibitively slow for very long sequences" and never names the crossover. *(It is also why long-context work is a separate research area: past $n=d$ the quadratic bites.)*

> [!warning] ⚠️ SECOND HIDDEN NUMBER, AND IT IS THE PAYOFF FOR ALL OF [[07 - Recurrent Neural Network|ch. 07]]
> **Ch. 07 §7:** a gradient path of length $T$ forces the recurrent Jacobian's magnitude into $[10^{-3/T},10^{3/T}]$.
>
> | path length | admissible $\gamma$ | width |
> |---|---|---|
> | **1000** (RNN, $n=1000$) | $[0.9931,\ 1.0069]$ | **±0.693%** |
> | 10 | $[0.5012,\ 1.9953]$ | ±99.5% |
> | **1** (self-attention) | $[0.001,\ 1000]$ | **±99,900%** |
>
> ⇒ ***the constraint does not loosen — it disappears.*** Every token reaches every other in **one** step, so there is **no product of Jacobians to control.**
>
> **⚠️ THIS IS THE UNIFYING RESULT OF THE ENTIRE SUBJECT.** [[04 - Neural Network|Ch. 04]] §8 found a sigmoid MLP dies at ~11 layers because the factor is bounded by 0.25; [[05 - Convolutional Neural Network|ch. 05]] §14 found ResNet's answer (make one path the identity, gain exactly 1); ch. 07 §9 found the LSTM's answer (make one path $\prod F_j$, gain 1 when $F=1$); **§8 is the last answer: make the path length 1 and the product has one term.**
>
> ⇒ ***every architecture in this subject after the MLP is a different way of shortening or neutralizing a product of Jacobians. That is the single thread running through all eight chapters.***

### 9. Positional encoding — order, restored

**Self-attention is permutation-equivariant**: shuffle the input and the outputs shuffle identically. **It has no notion of order at all**, which is exactly what an RNN got for free. So position is *added* to the input:

$$p_{i,2j}=\sin\!\left(\frac{i}{10000^{2j/d}}\right),\qquad p_{i,2j+1}=\cos\!\left(\frac{i}{10000^{2j/d}}\right)$$

**The frequency ladder**, verified: column 0 has frequency 1.0 (wavelength 6.3), column 8 has 0.01 (wavelength 628), column 15 has 0.000178 (wavelength 35,333). ⇒ **a continuous binary counter** — D2L's own analogy, low columns alternating fast, high columns slow, and float-valued so it is more space-efficient than binary.

> [!warning] ⚠️ The relative-position property, verified to machine precision
> For a fixed offset $\delta$ there is a $2\times2$ rotation, **independent of $i$**, mapping position $i$ to $i+\delta$:
> $$\begin{pmatrix}\cos\delta\omega_j & \sin\delta\omega_j\\-\sin\delta\omega_j & \cos\delta\omega_j\end{pmatrix}\begin{pmatrix}p_{i,2j}\\p_{i,2j+1}\end{pmatrix}=\begin{pmatrix}p_{i+\delta,2j}\\p_{i+\delta,2j+1}\end{pmatrix}$$
>
> **Checked for $\delta=1,5,17$ across all 16 column pairs and 60 positions: max error $3.7\times10^{-15}$.**
>
> ⇒ **the model can learn to attend by *relative* position using a fixed linear map** — and because the encoding is a formula rather than a table, **it is defined for positions longer than anything seen in training.** *That is the entire justification for the sinusoidal design over a learned embedding table.*

### 10. ⚠️ The Transformer — and where the parameters really are

**Encoder layer** = multi-head **self**-attention → add & LayerNorm → positionwise FFN → add & LayerNorm.
**Decoder layer** = **masked** self-attention → add & norm → **encoder–decoder attention** (queries from the decoder, keys and values from the encoder) → add & norm → FFN → add & norm.

**The masking in decoder self-attention is what preserves autoregression** — position $t$ may attend only to positions $\le t$. **Without it the model sees the answer**, which is [[07 - Recurrent Neural Network|ch. 07]] §11's bidirectional-leakage trap in a new form.

**Parameter budget per encoder layer** at $d_{\text{model}}=512$, $d_{\text{ffn}}=2048$:

| component | parameters | share |
|---|---|---|
| multi-head attention ($4d^2$) | 1,048,576 | **33.3%** |
| **positionwise FFN** ($2d\cdot d_{\text{ffn}}$) | **2,099,712** | **66.7%** |
| 2 × LayerNorm | 2,048 | 0.1% |
| **total** | **3,150,336** | |

> [!warning] ⚠️ THE FEED-FORWARD NETWORK IS TWICE THE ATTENTION, AND EVERYONE CALLS IT "THE ATTENTION MODEL"
> The ratio is $\frac{2d\cdot d_{\text{ffn}}}{4d^2}=\frac{d_{\text{ffn}}}{2d}=\mathbf{2.00}$ at the standard $d_{\text{ffn}}=4d$.
>
> **Six encoder layers = 18,902,016 parameters (72.1 MB); twelve = 37,804,032 (144.2 MB).**
>
> ⇒ *this is [[05 - Convolutional Neural Network|ch. 05]] §17's inversion in a third setting: **the component the architecture is named after is not where the parameters are.*** *(As in ch. 05: attention is where the $O(n^2)$ computation is, the FFN is where the weights are.)*

> [!note] ⚠️ The Transformer is assembled almost entirely from earlier chapters
> | component | inherited from |
> |---|---|
> | **residual connections** | [[05 - Convolutional Neural Network|ch. 05]] §14 (ResNet) — and it is why $\mathrm{sublayer}(\mathbf x)\in\mathbb R^d$, i.e. why $d_{\text{model}}$ is constant throughout |
> | **layer normalization** | [[05 - Convolutional Neural Network|ch. 05]] §13's batch norm, normalizing over **features** instead of the batch — so it works at batch size 1 and **does not make the output depend on other examples** |
> | **positionwise FFN** | [[05 - Convolutional Neural Network|ch. 05]] §5's $1\times1$ convolution, exactly: the same MLP applied independently at every position |
> | **encoder–decoder structure** | §2 of this chapter |
> | **masking** | §2's masked loss and §4's masked softmax |
>
> ⇒ ***the only genuinely new component is multi-head self-attention.*** Everything else is a part already built. **That is worth knowing: the Transformer is a recombination, and its power comes from removing recurrence, not from adding machinery.**

**Why layer norm and not batch norm here** is worth stating: batch statistics over a padded, variable-length sequence batch are meaningless, and [[05 - Convolutional Neural Network|ch. 05]] §13 showed batch norm's behaviour depends on batch size. **Layer norm normalizes each position's own feature vector — no cross-example dependence, no batch-size sensitivity.**

## ✏️ Exercises

> [!example]- Exercise 1 — BLEU by hand
> **(a)** Target `A B C D E F`, prediction `A B B C D`: compute $p_1$–$p_4$. **(b)** With $k=2$, compute BLEU. **(c)** Prediction `A B` against the same target, $k=2$. **(d)** What breaks?
>
> ---
> **(a)** With **clipping** (each target $n$-gram can be matched once): $p_1=\mathbf{4/5}$ (both `B`s in the prediction, one in the target), $p_2=\mathbf{3/4}$ (`AB`,`BC`,`CD` match; `BB` does not), $p_3=\mathbf{1/3}$ (`BCD` only), $p_4=\mathbf{0/2=0}$. **All four match D2L.**
>
> **(b)** $\mathrm{len_{pred}}=5\ge\mathrm{len_{label}}=6$? No — $\exp(\min(0,1-6/5))=\exp(-0.2)=0.8187$. BLEU $=0.8187\times0.8^{0.5}\times0.75^{0.25}=\mathbf{0.6816}$.
>
> **(c)** $p_1=p_2=\mathbf{1}$ — **perfect precision** — but $\exp(1-6/2)=\exp(-2)=\mathbf{0.1353}$, so BLEU $=\mathbf{0.1353}$.
>
> **(d)** ⚠️ **Precision alone rewards saying almost nothing**; the brevity penalty is the only thing stopping a one-word output from scoring 1.0. **And a single $p_n=0$ zeroes everything**, because BLEU is a product — which is exactly what happened to D2L's `soyez calmes .` (§2). *Real BLEU implementations use multiple references and corpus-level counts for both reasons.*

> [!example]- Exercise 2 — greedy versus beam
> **(a)** Verify D2L's two sequence probabilities. **(b)** Why can't greedy find the better one? **(c)** Cost greedy, beam ($k=5$) and exhaustive at $|\mathcal Y|=10^4$, $T'=10$. **(d)** Why normalize by length?
>
> ---
> **(a)** Greedy $0.5\cdot0.4\cdot0.4\cdot0.6=\mathbf{0.048}$; alternative $0.5\cdot0.3\cdot0.6\cdot0.6=\mathbf{0.054}$. **The greedy sequence is 11.11% less likely.**
>
> **(b)** At step 2 the better sequence takes the token with the **second**-highest probability (0.3 < 0.4). **Greedy commits irrevocably, and every later conditional distribution depends on that commitment** — D2L's tables for steps 3 and 4 differ between the two figures for exactly this reason.
>
> **(c)** greedy $|\mathcal Y|T'=\mathbf{10^5}$; beam $k|\mathcal Y|T'=\mathbf{5\times10^5}$; exhaustive $|\mathcal Y|^{T'}=\mathbf{10^{40}}$. **Beam costs 5× greedy and $2\times10^{34}$× less than exhaustive.**
>
> **(d)** $\log P$ of a sequence is a **sum of negative terms**, so it decreases monotonically with length. **Unnormalized, beam search always prefers the shortest candidate** and truncates systematically; dividing by $L^\alpha$ removes the bias.

> [!example]- Exercise 3 — the $\sqrt d$
> **(a)** Show $\operatorname{Var}[\mathbf q^\top\mathbf k]=d$ for iid zero-mean unit-variance entries. **(b)** What happens to the softmax at $d=512$ without scaling? **(c)** Why does that stop learning?
>
> ---
> **(a)** $\mathbf q^\top\mathbf k=\sum_{i=1}^d q_ik_i$. Each term has mean $\mathbb E[q_i]\mathbb E[k_i]=0$ and variance $\mathbb E[q_i^2]\mathbb E[k_i^2]=1$; the terms are independent, so the variance sums to $\mathbf d$. **Simulated: 510.44 at $d=512$** against a theoretical 512.
>
> **(b)** The logits have sd $\sqrt{512}=\mathbf{22.63}$. Measured over 2,000 draws with 10 keys: **max attention weight 0.9523, entropy 0.1170 nats against a uniform 2.3026** — effectively one-hot.
>
> **(c)** ⚠️ The softmax Jacobian is $p_i(\delta_{ij}-p_j)$. **At $p\approx(1,0,\dots,0)$ every entry is $\approx0$** — no gradient reaches the queries or keys. **With scaling, entropy is 1.9228 of a possible 2.3026 and the gradient is healthy.** ⇒ *the $1/\sqrt d$ is a trainability requirement, not a normalization convention.*

> [!example]- Exercise 4 — count a Transformer layer
> At $d_{\text{model}}=512$, $d_{\text{ffn}}=2048$, $h=8$: **(a)** attention parameters; does $h$ matter? **(b)** FFN parameters. **(c)** Which dominates, and by how much? **(d)** Six layers, in MB.
>
> ---
> **(a)** $\mathbf W_q,\mathbf W_k,\mathbf W_v$ each $512\times512$ *in total across all heads* (since $p_q=p_o/h$), plus $\mathbf W_o$ at $512\times512$: $4\times512^2=\mathbf{1{,}048{,}576}$. **$h$ does not matter — verified identical for $h=1,2,4,8,16$.**
>
> **(b)** $512\times2048+2048+2048\times512+512=\mathbf{2{,}099{,}712}$.
>
> **(c)** **FFN 66.7%, attention 33.3%, LayerNorm 0.1%** — ratio $d_{\text{ffn}}/(2d)=\mathbf{2.00}$. ⚠️ **The component the architecture is named after holds a third of its weights.**
>
> **(d)** $6\times3{,}150{,}336=\mathbf{18{,}902{,}016}$ parameters $=\mathbf{72.1}$ MB in fp32 — and by [[04 - Neural Network|ch. 04]] §5, **288.4 MB to train with Adam.**

> [!example]- Exercise 5 — why attention replaced recurrence
> **(a)** Give complexity, sequential ops and path length for RNN, CNN and self-attention. **(b)** When is self-attention cheaper than an RNN? **(c)** Using [[07 - Recurrent Neural Network|ch. 07]] §7, what does path length 1 buy? **(d)** So what is the actual reason?
>
> ---
> **(a)** RNN $O(nd^2)$ / $O(n)$ / $O(n)$; CNN $O(knd^2)$ / $O(1)$ / $O(n/k)$; **self-attention $O(n^2d)$ / $O(1)$ / $O(1)$.**
>
> **(b)** $n^2d<nd^2\iff\mathbf{n<d}$. **At $d=512$: cheaper below 512 tokens, more expensive above.**
>
> **(c)** Ch. 07 §7: a path of length $T$ needs $\gamma\in[10^{-3/T},10^{3/T}]$. At $T=1000$ that is **±0.693%**; **at $T=1$ it is $[0.001,1000]$ — ±99,900%.** ⇒ **the constraint does not loosen, it ceases to exist**, because there is no product of Jacobians left to control.
>
> **(d)** ⚠️ **Not speed — self-attention is *more* expensive past $n=d$, and long-context research exists precisely because of that.** The reason is **(i)** path length 1 removes the vanishing/exploding product entirely, and **(ii)** $O(1)$ sequential operations make the whole sequence parallelizable, where an RNN's $O(n)$ sequential steps cannot use a GPU. ⇒ ***attention trades an asymptotically worse complexity for a structurally better optimization problem and perfect parallelism — and on modern hardware that is the right trade.***

## 📝 Summary

- **Seq2seq needs two vocabularies, padding with valid lengths, and `<bos>`/`<eos>`/`<unk>`** — which is why masking appears in the loss, the softmax and the decoder.
- **The encoder–decoder interface is the abstraction**: variable-length input → fixed-shape state → variable-length output. **Teacher forcing** trains on ground-truth prefixes and creates **exposure bias**.
- **⚠️ BLEU's four printed precisions reproduce exactly** (4/5, 3/4, 1/3, 0), as does the brevity penalty ($e^{-2}=0.1353$) and all four printed translations. **But one zero precision zeroes the product**: D2L's `soyez calmes .` scores **exactly 0.000** despite being a valid imperative translation. ⇒ **BLEU measures $n$-gram overlap with one reference, not quality.**
- **Greedy search optimizes the most likely *token*, not the most likely *sequence***: $0.048$ vs $0.054$, verified. **Exhaustive is $10^{40}$, greedy $10^5$, beam ($k{=}10$) $10^6$** — the ratio that makes beam search universal. **Length-normalize, or beam search truncates systematically.**
- **Attention is a differentiable database lookup**, derived from a Gaussian kernel with two terms dropped: $\|\mathbf q\|^2$ cancels in the softmax and $\|\mathbf k_i\|^2$ is near-constant after layer norm.
- **Bahdanau attention removes the fixed-length bottleneck** by recomputing the context at every output step — and **incidentally shortens the encoder→decoder gradient path from $O(n+t)$ to $O(1)$**, which is what mattered.
- **⚠️ $\operatorname{Var}[\mathbf q^\top\mathbf k]=d$ (verified: 510.44 at $d=512$), and without the $1/\sqrt d$ the softmax saturates** — max weight **0.9523**, entropy **0.117 of 2.303 nats**. **A one-hot softmax has zero Jacobian.** The scaling is a trainability requirement.
- **⚠️ Multi-head attention is free: $4p_o^2$ parameters at every $h$** (verified for $h=1$–16). **The heads partition one budget instead of adding to it** — the same free-structure move as [[05 - Convolutional Neural Network|ch. 05]]'s grouped convolutions, with the same caveat that nothing crosses heads until $\mathbf W_o$.
- **⚠️ Self-attention is cheaper than an RNN iff $n<d$** — at $d=512$, every sequence under 512 tokens. **D2L prints the complexity table and never names the crossover.**
- **⚠️ AND THE REAL PAYOFF: path length 1.** Ch. 07 §7's admissible band for the recurrent Jacobian goes **±0.693% at $T{=}1000$ → ±99,900% at $T{=}1$.** ⇒ ***the vanishing/exploding constraint does not loosen, it disappears.***
- **Self-attention is permutation-equivariant and needs positional encoding.** The sinusoidal scheme is a **continuous binary counter** (wavelengths 6.3 → 35,333) whose **relative-position rotation identity holds to $3.7\times10^{-15}$** for every offset and column pair — and, being a formula, extends past the training length.
- **⚠️ A Transformer encoder layer is 66.7% feed-forward and 33.3% attention** (2,099,712 vs 1,048,576 at $d=512$, $d_{\text{ffn}}=2048$); six layers are 72.1 MB. **The component the architecture is named after holds a third of its weights** — [[05 - Convolutional Neural Network|ch. 05]] §17's inversion in a third setting.
- **The Transformer is a recombination**: residual connections from ResNet, layer norm from batch norm, the positionwise FFN from the $1\times1$ convolution, encoder–decoder and masking from §2. **The only new component is multi-head self-attention.**

## ⚠️ Important Notes

1. **⚠️ Never report a single-reference sentence-level BLEU as a quality measure.** One zero $n$-gram precision gives exactly 0, and a correct paraphrase scores the same as gibberish. Use multiple references and corpus-level counts, and report an example-level inspection alongside.
2. **⚠️ Length-normalize beam search scores.** $\log P$ is a sum of negative terms; without $1/L^\alpha$ the search prefers short outputs and truncates.
3. **⚠️ A larger beam is not monotonically better.** It finds higher-probability sequences, and higher probability is not higher quality — models over-assign probability to short, generic outputs. **This is a known failure and $k$ is a hyperparameter, not a "more is better" knob.**
4. **⚠️ Never omit the $1/\sqrt d$.** At $d=512$ the softmax is effectively one-hot and the gradient dies. This is a silent failure: the loss simply stops falling.
5. **⚠️ Decoder self-attention must be masked.** Without it, position $t$ attends to $t+1$ and the model reads the answer — [[07 - Recurrent Neural Network|ch. 07]] §11's bidirectional leakage, and equally invisible in validation metrics.
6. **⚠️ Self-attention has no notion of order.** Remove the positional encoding and the model is permutation-equivariant — it will still train, and it will be solving a bag-of-words problem.
7. **⚠️ The $O(n^2)$ is in *memory* as well as compute.** The attention matrix is $n\times n$ per head per layer and must be **retained for the backward pass** ([[04 - Neural Network|ch. 04]] §5): at $n=4096$, $h=8$, 12 layers that is 1.6 billion floats. **Sequence length, not model size, is what usually exhausts the GPU.**
8. **⚠️ Layer norm, not batch norm, and for a specific reason.** Batch statistics over padded variable-length sequences are meaningless, and batch norm's regularization varies with batch size ([[05 - Convolutional Neural Network|ch. 05]] §13). **Layer norm has no cross-example dependence.**
9. **⚠️ Multi-head is free only under $p_q=p_o/h$.** Keeping $p_q=p_o$ per head multiplies the cost by $h$. **Check which convention an implementation uses before comparing parameter counts.**
10. **⚠️ Teacher forcing means training and inference see different inputs.** Training feeds ground truth; inference feeds the model's own output, so a single early error compounds — [[07 - Recurrent Neural Network|ch. 07]] §1's $k$-step degradation. **Scheduled sampling and related fixes exist; D2L uses plain teacher forcing.**
11. **The encoder–decoder attention is where translation actually happens.** Encoder self-attention builds source representations, decoder self-attention builds target context, and **only the cross-attention connects the languages.** If a translation is fluent but wrong, that is the layer to inspect.
12. **Attention weights are not explanations.** They show what was *read*, not what was *used* — a value can be attended to strongly and contribute nothing after $\mathbf W_o$ and the FFN. **Treat attention maps as a diagnostic, not evidence.**
13. **⚠️ THE THREAD THROUGH ALL EIGHT CHAPTERS:** [[04 - Neural Network|ch. 04]] §8 (a sigmoid MLP's factor is bounded by 0.25, so it dies at ~11 layers) → [[05 - Convolutional Neural Network|ch. 05]] §14 (ResNet makes one path the identity, gain exactly 1) → [[07 - Recurrent Neural Network|ch. 07]] §9 (the LSTM makes one path $\prod F_j$, gain 1 at $F=1$) → **§8 here (make the path length 1, so there is no product).** ***Every architecture after the MLP is a different way of shortening or neutralizing a product of Jacobians.***

> [!warning] Gaps in the source material
> **All figures are images and never extract.** **Recovered because the prose states their content**: Fig. 10.8.1–10.8.3 (the greedy/beam probability trees — every conditional probability is written in the text, which is why §3's arithmetic could be verified), Fig. 11.3.1 (attention pooling), Fig. 11.5.1 (multi-head concatenation), Fig. 11.6.1 (the CNN/RNN/self-attention comparison — the complexities and path lengths are all in the prose), Fig. 11.7.1 (the Transformer, described sublayer by sublayer). **Genuinely lost**: the attention-weight heatmaps of §11.1 and §11.4, the Nadaraya–Watson kernel-regression plots of §11.2, the positional-encoding column plots and heatmap of §11.6.3 — *though §9 recovers more than the plots showed, since the frequencies and the rotation identity are computed directly* — and every training curve. **No perplexity or loss figures are quoted because none survived extraction.**
>
> **Code listings lose their indentation** and were re-derived; **printed outputs extract intact**, which is what made §2's four BLEU scores checkable.
>
> **No new cipher entries were needed.** The table in this subject's `CLAUDE.md` covered every formula, including BLEU's $p_n^{1/2^n}$ and the positional-encoding rotation matrix, where deleted minus signs and fraction bars had to be reconstructed and were then confirmed numerically.
>
> **Added beyond D2L, and labelled as mine throughout:**
> - **The BLEU failure analysis of §2** — that a single zero precision zeroes the product, and that D2L's own printed 0.000 is a valid translation. D2L prints the number and says nothing. **The observation that real BLEU uses multiple references and corpus-level counts is an addition.**
> - **The beam-search cost row** and the $10^{34}$ ratio (§3); **the length-normalization argument**, which D2L's formula implies and its prose does not explain.
> - **The softmax-saturation analysis of §6** — the entropy and max-weight simulations at $d=64,512$ and the softmax-Jacobian argument. **D2L gives the variance derivation and stops at "keep the order of magnitude under control".**
> - **The multi-head parameter table of §7** showing $4p_o^2$ at every $h$, and the connection to ch. 05's grouped convolutions.
> - **The $n<d$ crossover of §8**, with the worked table. **D2L prints the complexity column and never divides.**
> - **⚠️ The path-length payoff of §8** — carrying ch. 07 §7's $10^{\pm3/T}$ band to $T=1$ — and **Important Note 13's four-architecture thread**, which is my synthesis across chapters 04, 05, 07 and 08 and is not in D2L in any form.
> - **The positional-encoding verification of §9**: the rotation identity to $3.7\times10^{-15}$ across all offsets and column pairs, and the wavelength ladder.
> - **The Transformer parameter budget of §10** — 66.7% FFN vs 33.3% attention — and the inheritance table. **D2L gives no parameter count for the Transformer.**
> - **The $O(n^2)$ activation-memory warning** (Important Note 7) and **the attention-is-not-explanation caution** (Important Note 12).
>
> **No discrepancies found in this range.** Every printed number that could be checked was checked and every one was correct — **the second clean range in this subject, after §14.1–14.8.**
>
> **Deliberately deferred, not omitted:** **§10.5's data-loading pipeline** and **§10.7.2–10.7.7's implementation** are used only where they carry a result. **§11.2 (attention pooling via Nadaraya–Watson regression)** is a pedagogical bridge whose content — that attention generalizes kernel regression — is stated in §4 without reproducing the kernel experiments, since all of its output is figures. **§11.8 (Transformers for vision) and §11.9 (large-scale pretraining)** are beyond the syllabus topic; **ViT would be the most defensible addition** if the course covers it, and BERT/GPT belong to the vault's separate (blocked) NLP subject.
>
> **Left as the source states it:** all citations (Papineni et al. 2002, Bahdanau et al. 2014, Vaswani et al. 2017, Ba et al. 2016, Lin et al. 2017, Cheng et al. 2016, Parikh et al. 2016, Paulus et al. 2017, Shaw et al. 2018, Huang et al. 2018); the claim that Transformers are "pervasive in… language, vision, speech, and reinforcement learning"; and the assertion that additive and scaled-dot-product attention perform comparably, which is not benchmarked here.

**Previous:** [[07 - Recurrent Neural Network]] · **Next:** — *(end of subject; see [[00-Index]])*
