---
subject: Deep Learning
chapter: 7
tags: [ds, deep-learning, rnn, lstm, gru, bptt, perplexity, zipf, language-model, gradient-clipping]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 9 (Recurrent Neural Networks) and §10.1–10.4 (LSTM, GRU, Deep RNNs, Bidirectional RNNs)"
---

# Recurrent Neural Network

D2L ch. 9 and §10.1–10.4: sequence models, tokenization, language models and perplexity, the RNN, backpropagation through time and gradient clipping, then LSTM, GRU, deep and bidirectional RNNs.

## 📘 Main Knowledge

### 1. Sequence models

Sequence data are not IID: order carries information. Autoregressive models factor the joint probability:
$$P(x_1,\dots,x_T)=\prod_{t=1}^{T}P(x_t\mid x_{t-1},\dots,x_1)$$

A Markov model of order $n-1$ keeps only the last $n-1$ tokens. A latent autoregressive model keeps a summary $h_{t-1}$ of the whole past.

- D2L notes that predicting forward is usually easier than predicting backward. That is why bidirectional models suit text (where the whole sequence is known) but not forecasting.
- Multi-step prediction feeds the model its own outputs, so errors compound, often badly.
- D2L ex. 9.1.2 (picking stocks by past returns) is a distribution-shift problem: the past sample is conditioned on survival ([[03 - Logistic Regression|ch. 03]] §11).

### 2. Text to tokens

Pipeline: load text, tokenize, build a vocabulary (token → index), convert. D2L uses *The Time Machine*, keeping only letters and spaces in lower case.

| | vocabulary | sequence length | notes |
|---|---|---|---|
| characters | tiny (28 here: 26 letters, space, `<unk>`) | long (173,428) | no unknown tokens; must learn spelling |
| words | tens of thousands or more | short | meaningful tokens; long tail of rare words |
| word pieces | tunable | medium | the modern compromise |

D2L prints `(173428, 28)`. Rare tokens below `min_freq` and unseen tokens become `<unk>`, losing information; word vocabularies need it often, character vocabularies almost never, which is one reason subword tokenization is standard.

### 3. Why counting n-grams does not scale

An $n$-gram model stores $|\mathcal V|^n$ counts:

| $n$ | 28 characters | fp32 | 10,000 words | fp32 |
|---|---|---|---|---|
| 1 | 28 | 112 B | $10^4$ | 39 KB |
| 2 | 784 | 3.06 KB | $10^8$ | 381 MB |
| 3 | 21,952 | 85.75 KB | $10^{12}$ | 3.64 TB |
| 5 | $1.72\times10^7$ | 65.65 MB | $10^{20}$ | 347 EB |
| 10 | $2.96\times10^{14}$ | 1.05 PB | $10^{40}$ | |

The RNN in §6 has 2,876 parameters whatever the context length.

**Laplace smoothing** adds pseudo-counts:
$$\hat P(x)=\frac{n(x)+\epsilon_1/m}{n+\epsilon_1},\qquad \hat P(x'\mid x)=\frac{n(x,x')+\epsilon_2\hat P(x')}{n(x)+\epsilon_2}$$
($\epsilon\to0$: no smoothing; $\epsilon\to\infty$: uniform). D2L's objections: rare n-grams are still poorly estimated, all counts must be stored, word meaning is ignored ("cat" and "feline" share nothing), and long sequences are usually new.

### 4. Zipf's law

$$n_i\propto \frac{1}{i^{\alpha}}\iff \log n_i=-\alpha\log i+c$$

Fitting D2L's printed top-10 frequencies (D2L ex. 9.2.2):

| | $\alpha$ (ranks 1–10) | $R^2$ | $\alpha$ (ranks 2–10) | $R^2$ |
|---|---|---|---|---|
| unigram | 0.7184 | 0.948 | 0.7693 | 0.915 |
| bigram | 0.5703 | 0.965 | 0.4777 | 0.965 |
| trigram | 0.6447 | 0.931 | 0.5145 | 0.890 |

D2L says n-grams follow Zipf "with a smaller exponent". Smaller than unigrams: confirmed. A steady decrease with $n$: not supported (trigram > bigram), but ten head ranks cannot settle it (declined discrepancy D9).

Stop words fill 10/10 of the top unigrams, 9/10 of the top bigrams, but only 1/10 of the top trigrams. The top trigram is *the time traveller* (59 occurrences, vs 2,261 for *the*). Longer n-grams carry more specific information and are much rarer, which is exactly the problem for count-based models.

### 5. Perplexity

$$\mathrm{ppl}=\exp\left(-\frac1n\sum_{t=1}^{n}\log P(x_t\mid x_{t-1},\dots,x_1)\right)$$

It is the reciprocal geometric mean of the probabilities given to the actual tokens, roughly "how many equally likely choices the model is guessing among".

| model | perplexity |
|---|---|
| perfect | 1 |
| uniform over $|\mathcal V|=28$ | 28 |
| assigns 0 to the truth | $\infty$ |

Any useful model must beat the uniform value. In bits: $\log_2 28=4.8074$ per character; Shannon (1951) estimated English at about 1.1 bits per character (perplexity ≈ 2.14). So the useful range for a character model is 28 → 2.14 (13.1×), or 4.81 → 1.1 bits. Perplexity, not accuracy, is used because the next token is often genuinely uncertain and perplexity scores the whole distribution.

**Partitioning**: each epoch drops a random offset at the start, then cuts the corpus into length-$n$ subsequences; targets are inputs shifted by one. The random offset varies the boundaries between epochs.

### 6. The RNN

$$\mathbf H_t=\phi(\mathbf X_t\mathbf W_{xh}+\mathbf H_{t-1}\mathbf W_{hh}+\mathbf b_h),\qquad \mathbf O_t=\mathbf H_t\mathbf W_{hq}+\mathbf b_q$$

Compared with an MLP layer, the only addition is $\mathbf H_{t-1}\mathbf W_{hh}$, and the same weights are used at every step. A hidden *state* is carried across time steps; a hidden *layer* sits between input and output. In code, $\mathbf X_t\mathbf W_{xh}+\mathbf H_{t-1}\mathbf W_{hh}$ is one matrix product of $[\mathbf X_t,\mathbf H_{t-1}]$ with stacked weights.

Parameters (D2L ex. 10.2.3). One gate block costs $dh+h^2+h$:

| cell | blocks | recurrent parameters |
|---|---|---|
| RNN | 1 | $dh+h^2+h$ |
| GRU | 3 ($\mathbf R,\mathbf Z,\tilde{\mathbf H}$) | $3(dh+h^2+h)$ |
| LSTM | 4 ($\mathbf I,\mathbf F,\mathbf O,\tilde{\mathbf C}$) | $4(dh+h^2+h)$ |

| $d$ | $h$ | RNN | GRU | LSTM |
|---|---|---|---|---|
| 28 | 32 | 1,952 | 5,856 | 7,808 |
| 28 | 256 | 72,960 | 218,880 | 291,840 |
| 256 | 256 | 131,328 | 393,984 | 525,312 |

The ratio is always 1:3:4. With the output layer, the Time Machine model ($d=q=28$, $h=32$) has 2,876 (RNN), 6,780 (GRU), 8,732 (LSTM) parameters.

### 7. Backpropagation through time

BPTT is backprop on the unrolled graph. Because weights are shared, each parameter's gradient is summed over all time steps. The hidden-state gradient is recursive:
$$\frac{\partial h_t}{\partial w_h}=\frac{\partial f}{\partial w_h}+\frac{\partial f}{\partial h_{t-1}}\frac{\partial h_{t-1}}{\partial w_h}$$
which unrolls to
$$\frac{\partial h_t}{\partial w_h}=\frac{\partial f}{\partial w_h}+\sum_{i=1}^{t-1}\left(\prod_{j=i+1}^{t}\frac{\partial f(x_j,h_{j-1},w_h)}{\partial h_{j-1}}\right)\frac{\partial f(x_i,h_{i-1},w_h)}{\partial w_h}$$

The product of $t-i$ Jacobians causes the trouble. With factor $\gamma$:

| $\gamma$ | $\gamma^{10}$ | $\gamma^{100}$ | $\gamma^{1000}$ |
|---|---|---|---|
| 0.90 | 0.3487 | $2.66\times10^{-5}$ | $1.75\times10^{-46}$ |
| 0.99 | 0.9044 | 0.3660 | $4.32\times10^{-5}$ |
| 1.00 | 1 | 1 | 1 |
| 1.01 | 1.105 | 2.705 | $2.10\times10^{4}$ |
| 1.10 | 2.594 | $1.38\times10^{4}$ | $2.47\times10^{41}$ |

To keep $\gamma^T$ within $[10^{-3},10^3]$, $\gamma$ must lie in $[0.501, 1.995]$ for $T=10$, $[0.933, 1.072]$ for $T=100$, and $[0.993116, 1.006932]$ (±0.693%) for $T=1000$. D2L notes sequences of over a thousand tokens are common.

Compared with the sigmoid MLP of [[04 - Neural Network|ch. 04]] §8 (factor ≤ 0.25, independent weights per layer), an RNN's factor can be above or below 1 and is the same matrix each step. So gradients can vanish or explode, and RNNs need two fixes: clipping and gating.

D2L's options: full computation (unstable, never used); truncation after $\tau$ steps (standard; D2L argues its bias toward short dependencies stabilizes training); randomized truncation (unbiased but rarely better).

### 8. Gradient clipping

$$\mathbf g\leftarrow\min\left(1,\frac{\theta}{\|\mathbf g\|}\right)\mathbf g$$

The norm never exceeds $\theta$, gradients below $\theta$ are unchanged, and the direction is preserved. Justification: if $f$ is $L$-Lipschitz, one step changes $f$ by at most $L\eta\|\mathbf g\|$. At $\eta=0.1$, $L=1$, a gradient of norm 1000 could move the objective by 100; clipped at 1, by 0.1. It also limits any single minibatch's influence. D2L calls it "a hack": it is biased, and it does nothing for vanishing gradients.

### 9. LSTM

Gates (sigmoid, values in $(0,1)$):
$$\mathbf I_t=\sigma(\mathbf X_t\mathbf W_{xi}+\mathbf H_{t-1}\mathbf W_{hi}+\mathbf b_i),\quad \mathbf F_t=\sigma(\mathbf X_t\mathbf W_{xf}+\mathbf H_{t-1}\mathbf W_{hf}+\mathbf b_f),\quad \mathbf O_t=\sigma(\mathbf X_t\mathbf W_{xo}+\mathbf H_{t-1}\mathbf W_{ho}+\mathbf b_o)$$
Input node: $\tilde{\mathbf C}_t=\tanh(\mathbf X_t\mathbf W_{xc}+\mathbf H_{t-1}\mathbf W_{hc}+\mathbf b_c)$.
$$\mathbf C_t=\mathbf F_t\odot\mathbf C_{t-1}+\mathbf I_t\odot\tilde{\mathbf C}_t,\qquad \mathbf H_t=\mathbf O_t\odot\tanh(\mathbf C_t)$$

The key derivative is $\partial\mathbf C_t/\partial\mathbf C_{t-1}=\mathbf F_t$, so the gradient along the cell is $\prod_j F_j$, controlled by the network. With $F=1$ it is exactly 1 for any length (the "constant error carousel"); with $F=1$, $I=0$ the cell keeps its value forever.

$F$ is a sigmoid, so it never reaches 1. Memory half-life $=\ln0.5/\ln F$:

| forget pre-activation $z$ | $F=\sigma(z)$ | half-life (steps) |
|---|---|---|
| 0 | 0.5 | 1 |
| 2 | 0.8808 | 5.5 |
| 4 | 0.9820 | 38.2 |
| 6 | 0.9975 | 280 |
| 8 | 0.99966 | 2,065 |

A 1,000-step half-life needs $z\approx7.3$. With zero bias (D2L's init) the half-life is one step, which is why practitioners often initialize the forget-gate bias to +1 or +2 (beyond D2L).

The output gate lets a cell store information without affecting the rest of the network until $\mathbf O_t$ opens.

### 10. GRU

Two gates (Cho et al. 2014):
$$\mathbf R_t=\sigma(\mathbf X_t\mathbf W_{xr}+\mathbf H_{t-1}\mathbf W_{hr}+\mathbf b_r),\qquad \mathbf Z_t=\sigma(\mathbf X_t\mathbf W_{xz}+\mathbf H_{t-1}\mathbf W_{hz}+\mathbf b_z)$$
$$\tilde{\mathbf H}_t=\tanh(\mathbf X_t\mathbf W_{xh}+(\mathbf R_t\odot\mathbf H_{t-1})\mathbf W_{hh}+\mathbf b_h),\qquad \mathbf H_t=\mathbf Z_t\odot\mathbf H_{t-1}+(1-\mathbf Z_t)\odot\tilde{\mathbf H}_t$$

- $\mathbf R\to1$: vanilla RNN. $\mathbf R\to0$: candidate ignores the old state.
- $\mathbf Z\to1$: copy the old state and skip this step.
- The update is a convex combination, so the GRU cannot forget without writing, while the LSTM's $\mathbf F$ and $\mathbf I$ are independent. In exchange it has 25% fewer parameters, and D2L reports similar performance.

D2L: reset gates capture short-term dependencies, update gates long-term ones.

### 11. Deep and bidirectional RNNs

**Deep RNNs** stack layers: layer $\ell$'s state at time $t$ feeds layer $\ell+1$ at time $t$ and layer $\ell$ at $t+1$. Parameters $(dh+h^2+h)+(L-1)(2h^2+h)$ plus output; at $d=q=28$, $h=32$: 2,876, 4,956, 7,036, 11,196 for $L=1,2,3,5$.

**Bidirectional RNNs** run a forward and a backward RNN and concatenate their states:

| | one direction | bidirectional | ratio |
|---|---|---|---|
| RNN | 2,876 | 5,724 | 1.99× |
| GRU | 6,780 | 13,532 | 2.00× |
| LSTM | 8,732 | 17,436 | 2.00× |

A bidirectional model sees tokens after $t$. For next-token prediction this leaks the answer, and for forecasting the future is not available. Use it for tasks where the whole sequence is known: tagging, named-entity recognition, filling masked tokens (BERT's setting, not GPT's).

## ✏️ Exercises

> [!example]- **1.** *(Easy) Perplexity*
> **(a)** Probabilities 0.5, 0.25, 0.125, 0.125 on the actual tokens: perplexity? **(b)** The three anchor values and this corpus's bound. **(c)** Convert perplexity 28 and 2.14 to bits per character.
>
> ---
> **(a)** Mean NLL $=\frac14(0.6931+1.3863+2.0794+2.0794)=1.5596$; perplexity $e^{1.5596}=4.7568$.
>
> **(b)** 1 (perfect), 28 (uniform), $\infty$.
>
> **(c)** 4.8074 and 1.0977 bits. Perplexity 10 (3.32 bits) covers $(4.81-3.32)/(4.81-1.10)=40\%$ of that range, so the multiplicative scale overstates progress.

> [!example]- **2.** *(Easy–medium) Cell costs*
> **(a)** Parameters for RNN, GRU, LSTM with $d$ inputs, $h$ hidden. **(b)** At $d=28$, $h=256$. **(c)** Deep and bidirectional.
>
> ---
> **(a)** $dh+h^2+h$ per block; 1, 3, 4 blocks.
>
> **(b)** 72,960 / 218,880 / 291,840 (+ output layer).
>
> **(c)** Deep adds $(L-1)(2h^2+h)$; bidirectional roughly doubles. A bidirectional LSTM is about 8× a vanilla RNN's recurrent cost.

> [!example]- **3.** *(Medium) Why not count?*
> **(a)** Parameters for a 28-character n-gram model at $n=3,5,10$. **(b)** Compare with the RNN. **(c)** Why doesn't smoothing fix it?
>
> ---
> **(a)** 21,952; $1.72\times10^7$; $2.96\times10^{14}$ (1.05 PB). A 10,000-word trigram model needs $10^{12}$ counts (3.64 TB).
>
> **(b)** 2,876 at any $n$.
>
> **(c)** Smoothing fixes zero counts, not storage, meaning or novelty. The informative n-grams are the rare ones (*the time traveller*: 59 vs *the*: 2,261).

> [!example]- **4.** *(Medium–hard) The BPTT window*
> **(a)** Gradient factor over $T$ steps with Jacobian magnitude $\gamma$? **(b)** Range of $\gamma$ keeping it in $[10^{-3},10^3]$ for $T=10,100,1000$. **(c)** Does clipping solve this?
>
> ---
> **(a)** $\gamma^T$, the same matrix each step.
>
> **(b)** $[10^{-3/T},10^{3/T}]$: $[0.501,1.995]$, $[0.933,1.072]$, $[0.993116,1.006932]$.
>
> **(c)** Only the exploding side. A gradient of $1.75\times10^{-46}$ cannot be rescaled into usefulness; vanishing needs the LSTM/GRU's additive path.

> [!example]- **5.** *(Hard) How long can an LSTM remember?*
> **(a)** $\partial\mathbf C_t/\partial\mathbf C_{t-1}$ and the gradient over $T$ steps. **(b)** Forget-gate pre-activation for a half-life of 100 and 1,000 steps. **(c)** Implication for initialization.
>
> ---
> **(a)** $\mathbf F_t$; the product $\prod_j F_j$, equal to 1 when $F=1$.
>
> **(b)** $F=0.5^{1/\text{half-life}}$, $z=\sigma^{-1}(F)$: 100 steps needs $F=0.99309$, $z=4.97$; 1,000 steps needs $F=0.999307$, $z=7.28$.
>
> **(c)** At zero bias $F=0.5$ and memory lasts one step, and the gradient that would teach longer memory is the one being forgotten. Initialize the forget bias positive (+1 or +2).

## 📝 Summary

- Sequences are not IID; autoregression factors the joint distribution and an RNN summarizes the past in a hidden state.
- Tokenization choice: characters (28 tokens, 173,428 long) vs words (large vocabulary, `<unk>`) vs subwords.
- n-gram counts grow as $|\mathcal V|^n$; an RNN's parameters do not depend on context length.
- Zipf exponents from D2L's data: 0.72 (unigram), 0.57 (bigram), 0.64 (trigram). Longer n-grams are more informative and rarer.
- Perplexity ranges from 1 to the vocabulary size (28); convert to bits to compare (4.81 uniform vs ~1.1 for English).
- An RNN adds $\mathbf H_{t-1}\mathbf W_{hh}$ to an MLP layer; RNN:GRU:LSTM parameters are 1:3:4.
- BPTT multiplies the same Jacobian $T$ times; at $T=1000$ it must be within 0.7% of 1 in magnitude.
- Clipping caps exploding gradients; gating (LSTM's $\partial\mathbf C_t/\partial\mathbf C_{t-1}=\mathbf F_t$) addresses vanishing, but $F<1$ always, so long memory has to be learned (or helped by a positive forget bias).
- GRU merges forget and write into one gate; deep RNNs stack layers; bidirectional RNNs suit tagging, not prediction.

## ⚠️ Important Notes

1. Do not use a bidirectional model for next-token prediction or forecasting; validation numbers will look great because of leakage.
2. Clipping does not help vanishing gradients.
3. A zero forget-gate bias means a one-step memory half-life at the start.
4. Report perplexity with the vocabulary size.
5. Perplexity drops look larger than the corresponding bit improvements.
6. Truncated BPTT cannot learn dependencies longer than the truncation length.
7. Shared weights receive gradients summed over time steps; averaging the loss over steps keeps the scale sensible.
8. Gating extends memory but does not remove the product; attention ([[08 - Sequence to Sequence|ch. 08]]) does.
9. Use a random offset when partitioning sequences.
10. If a task needs to clear state without taking in the current input, an LSTM can do that and a GRU cannot.
11. Character and word perplexities are not comparable; compare bits per character.
12. Modern neural models do not need stop-word removal.
13. Check the `<unk>` rate before blaming the model.
14. "2-layer LSTM with 256 units": 2 stacked layers, 256-dimensional hidden state.

> [!warning] Gaps in the source material
> - **Figures:** partitioning, the unrolled RNN, and LSTM/GRU diagrams are reconstructed from the prose. Lost: Zipf log–log plots (the exponents were fitted from the printed frequency lists instead) and all training/perplexity curves, so no perplexity results are quoted.
> - **Added by me:** Zipf fits (D2L ex. 9.2.2) and the stop-word counts; the $|\mathcal V|^n$ table; all parameter counts (ex. 10.2.3); the BPTT stability window and comparison with ch. 04; the clipping numbers; the forget-gate half-life analysis and positive-bias advice; Shannon's 1.1 bits/char; the explicit BERT/GPT leakage point; the GRU convex-combination remark.
> - **Declined discrepancy D9:** n-gram Zipf exponents are smaller than the unigram one but not monotone in $n$; ten ranks cannot decide.
> - **Skipped:** RNN implementations (§9.5–9.6) beyond clipping and parameter structure; the sine-wave experiment (results are figures). Machine translation and attention are in [[08 - Sequence to Sequence|ch. 08]].

**Previous:** [[06 - Object Detection]] · **Next:** [[08 - Sequence to Sequence]]
