---
subject: Deep Learning
chapter: 8
tags: [ds, deep-learning, seq2seq, encoder-decoder, bleu, beam-search, attention, transformer, self-attention, positional-encoding]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, §10.5–10.8 (Machine Translation, Encoder–Decoder, Seq2seq, Beam Search) and §11.1–11.7 (Attention, Multi-Head, Self-Attention, the Transformer)"
---

# Sequence to Sequence

D2L §10.5–10.8 covers the encoder–decoder, BLEU and beam search. §11.1–11.7 (attention and the Transformer) is added to this topic as a scope extension recorded in [[00-Index]], since seq2seq without attention stops just before the modern approach.

## 📘 Main Knowledge

### 1. Machine translation data

Unlike language modelling ([[07 - Recurrent Neural Network|ch. 07]]), input and output are different sequences, in different languages, of different lengths. This requires:
- two vocabularies (source and target);
- padding to a fixed length with `<pad>` plus a recorded valid length, hence masking throughout;
- special tokens: `<bos>` starts decoding, `<eos>` ends it, `<unk>` replaces unknown words.

### 2. Encoder–decoder and BLEU

The **encoder** turns a variable-length input into a fixed-shape state; the **decoder** uses that state and the tokens generated so far to produce the next token. Any encoder can be paired with any decoder through this interface.

**Teacher forcing**: during training the decoder receives the true previous token, not its own prediction. Training is faster and more stable, but at test time the model sees its own outputs, a mismatch called **exposure bias** (D2L ex. 10.7.4).

**Masked loss**: padded positions are multiplied by zero, as with `bbox_masks` in [[06 - Object Detection|ch. 06]].

**BLEU** (Papineni et al. 2002) measures n-gram overlap with a reference:
$$\mathrm{BLEU}=\exp\left(\min\left(0,\ 1-\frac{\mathrm{len}_{\text{label}}}{\mathrm{len}_{\text{pred}}}\right)\right)\prod_{n=1}^{k}p_n^{1/2^n}$$
where $p_n$ is the clipped n-gram precision (each reference n-gram can be matched only once). The first factor is the brevity penalty. Since $p_n^{1/2^n}$ grows with $n$ for fixed $p_n$, longer matches carry more weight.

Target `A B C D E F`, prediction `A B B C D`: $p_1=4/5$, $p_2=3/4$, $p_3=1/3$, $p_4=0$, as in D2L. Prediction `A B` has perfect precision but brevity penalty $e^{1-3}=0.1353$.

D2L's printed translations:

| English | predicted | target | BLEU |
|---|---|---|---|
| go . | va ! | va ! | 1.000 |
| i lost . | j'ai perdu . | j'ai perdu . | 1.000 |
| he's calm . | soyez calmes . | il est calme . | 0.000 |
| i'm home . | je suis chez moi . | je suis chez moi . | 1.000 |

In the third row $p_2=0$, so the product is 0 even though one token matches and "soyez calmes" is a reasonable imperative translation. Sentence-level BLEU against one reference measures n-gram overlap, not translation quality. The original metric uses multiple references and corpus-level counts to reduce these problems.

### 3. Decoding: greedy, exhaustive, beam

**Greedy search** picks the most likely token at each step, which does not give the most likely sequence. D2L's example:

| sequence | probability |
|---|---|
| greedy `A B C <eos>` | $0.5\times0.4\times0.4\times0.6=0.048$ |
| alternative `A C B <eos>` | $0.5\times0.3\times0.6\times0.6=0.054$ |

The better sequence picks the second-best token at step 2; after that the conditional probabilities differ.

| strategy | sequences scored ($|\mathcal Y|=10^4$, $T'=10$) |
|---|---|
| greedy, $O(|\mathcal Y|T')$ | $10^5$ |
| beam, $k=10$, $O(k|\mathcal Y|T')$ | $10^6$ |
| exhaustive, $O(|\mathcal Y|^{T'})$ | $10^{40}$ |

**Beam search** keeps the $k$ best partial sequences. Final candidates are compared with a length-normalized score $\frac{1}{L^\alpha}\log P$: since $\log P$ is a sum of negative terms, unnormalized scores always favour short outputs.

### 4. Attention as a soft lookup

Given a query $\mathbf q$ and key–value pairs $(\mathbf k_i,\mathbf v_i)$:
$$\mathrm{Attention}(\mathbf q,\mathcal D)=\sum_i\alpha(\mathbf q,\mathbf k_i)\,\mathbf v_i,\qquad \alpha=\mathrm{softmax}\big(a(\mathbf q,\mathbf k_i)\big)$$
A database lookup is the case where $\alpha$ is 1 on one key and 0 elsewhere. Attention is a differentiable version.

D2L derives the dot product from a Gaussian kernel: $-\tfrac12\|\mathbf q-\mathbf k_i\|^2=\mathbf q^\top\mathbf k_i-\tfrac12\|\mathbf k_i\|^2-\tfrac12\|\mathbf q\|^2$. The $\|\mathbf q\|^2$ term is the same for every key and cancels in the softmax, and $\|\mathbf k_i\|^2$ is roughly constant after layer normalization, leaving $\mathbf q^\top\mathbf k_i$.

**Additive attention** $a=\mathbf w_v^\top\tanh(\mathbf W_q\mathbf q+\mathbf W_k\mathbf k)$ handles queries and keys of different sizes; otherwise the parameter-free dot product is preferred.

**Masked softmax** sets padded logits to a large negative number ($-10^6$) instead of branching, which is faster on GPUs.

### 5. Bahdanau attention

The basic encoder–decoder squeezes the whole source sentence into one fixed vector. Bahdanau et al. (2014) use the decoder's previous hidden state as the query and the encoder's states at all source positions as keys and values, recomputing the context at every output step.

This also shortens gradient paths. Without attention, information from source token 1 must pass through the whole encoder and then the decoder ($O(n+t)$ steps; [[07 - Recurrent Neural Network|ch. 07]] §7 shows how hard 1,000 steps are). With attention, every output position reads every source position directly.

### 6. Scaled dot-product attention

If $\mathbf q,\mathbf k\in\mathbb R^d$ have independent zero-mean, unit-variance entries, $\mathbf q^\top\mathbf k$ has variance $d$. So
$$a(\mathbf q,\mathbf k_i)=\frac{\mathbf q^\top\mathbf k_i}{\sqrt d}$$

Simulated variance: 3.9959 ($d=4$), 63.9494 ($d=64$), 510.4430 ($d=512$); about 1 after scaling.

Why it matters (beyond D2L's variance argument):

| | sd of logits | max weight | entropy (nats) |
|---|---|---|---|
| unscaled, $d=512$, 10 keys | 22.63 | 0.9523 | 0.1170 |
| unscaled, $d=64$, 10 keys | 8.00 | 0.8646 | 0.3489 |
| scaled, 10 keys | 1.00 | 0.3205 | 1.9228 (max 2.3026) |

Unscaled, the softmax is nearly one-hot, and its Jacobian $p_i(\delta_{ij}-p_j)$ is then almost zero, so queries and keys stop learning. The scaling keeps attention trainable.

### 7. Multi-head attention

Project queries, keys and values into $h$ subspaces, attend in each, concatenate, and project with $\mathbf W_o$. With D2L's choice $p_q=p_k=p_v=p_o/h$:

| heads $h$ | per-head size | Q, K, V parameters | $\mathbf W_o$ |
|---|---|---|---|
| 1 | 512 | 786,432 | 262,144 |
| 8 | 64 | 786,432 | 262,144 |
| 16 | 32 | 786,432 | 262,144 |

The total is $4p_o^2$ for any $h$: the heads split one budget. Several heads cost the same as one and can attend to different things. As with grouped convolutions ([[05 - Convolutional Neural Network|ch. 05]] §15), heads do not exchange information until $\mathbf W_o$ mixes them.

### 8. Self-attention vs CNNs and RNNs

Self-attention uses the sequence as queries, keys and values.

| | complexity | sequential ops | max path length |
|---|---|---|---|
| CNN (kernel $k$) | $O(knd^2)$ | $O(1)$ | $O(n/k)$ |
| RNN | $O(nd^2)$ | $O(n)$ | $O(n)$ |
| self-attention | $O(n^2d)$ | $O(1)$ | $O(1)$ |

Self-attention is cheaper than an RNN when $n<d$. At $d=512$ that covers sequences under 512 tokens; beyond that the $n^2$ term dominates, which is why long-context attention is its own research area.

The main gain is path length. From [[07 - Recurrent Neural Network|ch. 07]] §7, keeping $\gamma^T$ within $[10^{-3},10^3]$ requires $\gamma$ within ±0.693% of 1 at $T=1000$, but allows $[0.001, 1000]$ at $T=1$. With path length 1 there is no long product of Jacobians to control. Combined with $O(1)$ sequential steps (full parallelism on GPUs), this is why attention replaced recurrence despite worse asymptotic cost.

This links the subject's architectures (my synthesis, not in D2L): sigmoid MLPs fail at ~11 layers because each factor is ≤ 0.25 ([[04 - Neural Network|ch. 04]] §8); ResNet adds an identity path ([[05 - Convolutional Neural Network|ch. 05]] §14); the LSTM adds a path with gain $\prod F_j$ ([[07 - Recurrent Neural Network|ch. 07]] §9); self-attention makes the path length 1. Each deals with the same product of Jacobians.

### 9. Positional encoding

Self-attention ignores order: permuting the input permutes the output the same way. Position is added to the input:
$$p_{i,2j}=\sin\!\left(\frac{i}{10000^{2j/d}}\right),\qquad p_{i,2j+1}=\cos\!\left(\frac{i}{10000^{2j/d}}\right)$$

Frequencies fall along the columns: column 0 has wavelength 6.3, column 8 about 628, column 15 about 35,333. D2L compares it to a binary counter with continuous values.

For a fixed offset $\delta$, a $2\times2$ rotation independent of $i$ maps position $i$ to $i+\delta$:
$$\begin{pmatrix}\cos\delta\omega_j & \sin\delta\omega_j\\-\sin\delta\omega_j & \cos\delta\omega_j\end{pmatrix}\begin{pmatrix}p_{i,2j}\\p_{i,2j+1}\end{pmatrix}=\begin{pmatrix}p_{i+\delta,2j}\\p_{i+\delta,2j+1}\end{pmatrix}$$
(checked for $\delta=1,5,17$, all column pairs, 60 positions; max error $3.7\times10^{-15}$). So relative positions are reachable by a fixed linear map, and since the encoding is a formula, it extends to positions longer than those seen in training.

### 10. The Transformer

**Encoder layer**: multi-head self-attention → add & LayerNorm → positionwise FFN → add & LayerNorm.
**Decoder layer**: masked self-attention → add & norm → encoder–decoder attention (queries from the decoder, keys/values from the encoder) → add & norm → FFN → add & norm.

The decoder's mask lets position $t$ attend only to positions $\le t$; without it the model sees the answer.

Parameters per encoder layer ($d_{\text{model}}=512$, $d_{\text{ffn}}=2048$; D2L gives no count):

| component | parameters | share |
|---|---|---|
| multi-head attention ($4d^2$) | 1,048,576 | 33.3% |
| positionwise FFN | 2,099,712 | 66.7% |
| 2 × LayerNorm | 2,048 | 0.1% |
| total | 3,150,336 | |

The FFN has twice the attention's parameters ($d_{\text{ffn}}/2d=2$). Attention is where the $O(n^2)$ computation is; the FFN is where most weights are. Six layers: 18,902,016 parameters (72.1 MB).

Most components come from earlier chapters:

| component | origin |
|---|---|
| residual connections | ResNet ([[05 - Convolutional Neural Network|ch. 05]] §14); they keep $d_{\text{model}}$ constant |
| layer normalization | like batch norm ([[05 - Convolutional Neural Network|ch. 05]] §13) but over features, so it works at any batch size and does not mix examples |
| positionwise FFN | the same MLP at every position, i.e. a $1\times1$ convolution |
| encoder–decoder, masking | §2 and §4 of this chapter |

Multi-head self-attention is the main new component. Layer norm is used instead of batch norm because batch statistics over padded variable-length sequences are unreliable.

## ✏️ Exercises

> [!example]- **1.** *(Easy) BLEU by hand*
> **(a)** Target `A B C D E F`, prediction `A B B C D`: $p_1$ to $p_4$. **(b)** BLEU with $k=2$. **(c)** Prediction `A B`, $k=2$. **(d)** What are the weaknesses?
>
> ---
> **(a)** $p_1=4/5$ (only one `B` counts), $p_2=3/4$ (`AB`, `BC`, `CD`), $p_3=1/3$ (`BCD`), $p_4=0/2$.
>
> **(b)** Brevity penalty $\exp(1-6/5)=0.8187$. BLEU $=0.8187\times0.8^{1/2}\times0.75^{1/4}=0.6815$.
>
> **(c)** $p_1=p_2=1$, penalty $e^{-2}=0.1353$, BLEU 0.1353.
>
> **(d)** Precision alone rewards very short outputs (only the brevity penalty prevents that), and one zero precision makes the whole score zero.

> [!example]- **2.** *(Easy–medium) Greedy vs beam*
> **(a)** Verify the two sequence probabilities. **(b)** Why does greedy miss the better one? **(c)** Cost of greedy, beam ($k=5$), exhaustive at $|\mathcal Y|=10^4$, $T'=10$. **(d)** Why normalize by length?
>
> ---
> **(a)** 0.048 and 0.054; greedy's is 11.11% lower.
>
> **(b)** The better path takes the second-best token at step 2, and later probabilities depend on that choice. Greedy never revisits it.
>
> **(c)** $10^5$, $5\times10^5$, $10^{40}$.
>
> **(d)** Log-probabilities only decrease as a sequence grows, so short outputs win unless scores are normalized.

> [!example]- **3.** *(Medium) The $\sqrt d$*
> **(a)** Show $\operatorname{Var}[\mathbf q^\top\mathbf k]=d$. **(b)** What happens to the softmax at $d=512$ without scaling? **(c)** Why does that stop learning?
>
> ---
> **(a)** $\sum_i q_ik_i$: each term has mean 0 and variance 1, and they are independent, so the variance is $d$ (simulated 510.44 at $d=512$).
>
> **(b)** Logit sd 22.63; max weight 0.9523; entropy 0.117 of 2.303 nats.
>
> **(c)** The softmax Jacobian $p_i(\delta_{ij}-p_j)$ is near zero for a one-hot $p$. With scaling the entropy is 1.92 and gradients flow.

> [!example]- **4.** *(Medium–hard) Count a Transformer layer*
> $d_{\text{model}}=512$, $d_{\text{ffn}}=2048$, $h=8$. **(a)** Attention parameters; does $h$ matter? **(b)** FFN parameters. **(c)** Which dominates? **(d)** Six layers in MB.
>
> ---
> **(a)** $4\times512^2=1{,}048{,}576$, independent of $h$.
>
> **(b)** $512\cdot2048+2048+2048\cdot512+512=2{,}099{,}712$.
>
> **(c)** FFN 66.7%, attention 33.3%.
>
> **(d)** $6\times3{,}150{,}336=18{,}902{,}016$ parameters, 72.1 MB in fp32; with Adam training state ([[04 - Neural Network|ch. 04]] §5), 288.4 MB.

> [!example]- **5.** *(Hard) Why attention replaced recurrence*
> **(a)** Complexity, sequential ops and path length for RNN, CNN, self-attention. **(b)** When is self-attention cheaper than an RNN? **(c)** What does path length 1 buy, using ch. 07 §7? **(d)** So why did attention win?
>
> ---
> **(a)** RNN $O(nd^2)$, $O(n)$, $O(n)$; CNN $O(knd^2)$, $O(1)$, $O(n/k)$; self-attention $O(n^2d)$, $O(1)$, $O(1)$.
>
> **(b)** When $n<d$; at $d=512$, below 512 tokens.
>
> **(c)** The allowed Jacobian range widens from ±0.693% (length 1000) to $[0.001, 1000]$ (length 1): no long product remains.
>
> **(d)** Not speed in general (it is worse for $n>d$), but short gradient paths and full parallelism over positions.

## 📝 Summary

- Seq2seq uses two vocabularies, padding with valid lengths, and `<bos>`/`<eos>`/`<unk>`; masks appear in the loss, the softmax and the decoder.
- Encoder–decoder: variable input → fixed state → variable output. Teacher forcing causes exposure bias.
- BLEU = brevity penalty × product of clipped n-gram precisions; one zero precision gives 0, so single-reference sentence BLEU is a weak quality measure.
- Greedy picks the best token, not the best sequence. Beam search costs $k$× greedy and far less than exhaustive search; normalize by length.
- Attention is a soft, differentiable lookup; dot-product attention is a simplified Gaussian kernel.
- Bahdanau attention recomputes the context per output step, removing the fixed-vector bottleneck and shortening gradient paths.
- Scale dot products by $1/\sqrt d$, or the softmax saturates and gradients vanish.
- Multi-head attention costs $4p_o^2$ for any number of heads.
- Self-attention is cheaper than an RNN when $n<d$, has path length 1 and runs in parallel.
- Sinusoidal positional encodings supply order; relative shifts are fixed rotations.
- A Transformer layer is about two-thirds FFN parameters; it combines residual connections, layer norm and position-wise MLPs with multi-head self-attention.

## ⚠️ Important Notes

1. Do not treat single-reference, sentence-level BLEU as a quality score; inspect examples too.
2. Normalize beam scores by length.
3. Larger beams find more probable outputs, which are not always better (they favour short, generic text); $k$ is a hyperparameter.
4. Always include the $1/\sqrt d$ scaling; without it training stalls silently.
5. Mask decoder self-attention, or the model sees future tokens.
6. Without positional encoding, self-attention treats the input as a bag of tokens.
7. Attention's $O(n^2)$ is also memory: at $n=4096$, 8 heads, 12 layers the attention matrices are about 1.6 billion floats, kept for the backward pass. Sequence length often limits GPU memory more than model size.
8. Use layer norm, not batch norm, for variable-length padded batches.
9. Multi-head is "free" only with per-head size $p_o/h$; check the convention before comparing parameter counts.
10. Teacher forcing means one early error at inference time can compound (scheduled sampling is one fix; D2L does not use it).
11. Cross-attention is where source and target meet; inspect it when translations are fluent but wrong.
12. Attention weights show what was read, not necessarily what influenced the output.

> [!warning] Gaps in the source material
> - **Figures:** greedy/beam probability trees, attention pooling, multi-head and Transformer diagrams are reconstructed from the prose (the trees' probabilities are in the text). Lost: attention heatmaps, kernel-regression plots, positional-encoding plots, and all training curves, so no loss or BLEU curves are quoted.
> - **Added by me:** the BLEU zero-precision analysis; the beam cost comparison and length-normalization reasoning; the softmax saturation simulation; the multi-head parameter table; the $n<d$ crossover; the path-length argument and the cross-chapter link (ch. 04, 05, 07, 08); the positional-encoding rotation check; the Transformer parameter budget and inheritance table; the memory and interpretability cautions. Multiple-reference BLEU and exposure bias are named beyond D2L.
> - **Correction:** exercise 1(b)'s BLEU is 0.6815 (an earlier version of this note said 0.6816).
> - **No discrepancies** with the source in this range.
> - **Skipped:** data loading and implementation code (§10.5, §10.7), Nadaraya–Watson experiments (§11.2, outputs are figures), vision Transformers and large-scale pretraining (§11.8–11.9; BERT/GPT belong to the blocked NLP subject).

**Previous:** [[07 - Recurrent Neural Network]] · **Next:** end of subject (see [[00-Index]])
