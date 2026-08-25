---
subject: Deep Learning
chapter: 7
tags: [ds, deep-learning, rnn, lstm, gru, bptt, perplexity, zipf, language-model, gradient-clipping]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 9 (Recurrent Neural Networks) and §10.1–10.4 (LSTM, GRU, Deep RNNs, Bidirectional RNNs)"
---

# Recurrent Neural Network

**D2L ch. 9 entire plus §10.1–10.4.** Sequence models and autoregression → text to tokens to vocabulary → language models and perplexity → the RNN → backpropagation through time and gradient clipping → LSTM, GRU, deep and bidirectional.

**Six results.**

**§7 — ⚠️ THE NUMBER THAT EXPLAINS WHY RNNs ARE HARD, AND D2L DESCRIBES IT IN WORDS ONLY.** BPTT's gradient is a product of $T$ Jacobians of **the same reused matrix**. For $\gamma^{1000}$ to stay inside $[10^{-3},10^{3}]$, **$\gamma$ must lie in $[0.993116,\,1.006932]$ — within ±0.693% of 1.** ⇒ *vanishing and exploding are one mechanism, not two, and at D2L's own "over a thousand tokens" there is almost no stable window.*

**§9 — ⚠️ THE LSTM'S FIX IS ONE LINE OF ARITHMETIC, AND THE GATE CAN NEVER REACH IT.** $\partial C_t/\partial C_{t-1}=F_t$, so $F=1$ gives a gradient factor of **exactly 1 for every $T$**. **But $F$ is a sigmoid, so $F=1$ is unreachable** — at pre-activation $z=4$ the memory half-life is only **106 steps**; reaching 1,000 needs $z\gtrsim8$. ⇒ ***the constant error carousel is an asymptote the network approaches, not a switch it flips.***

**§3 — ⚠️ THE EXPONENT D2L NAMES WITHOUT A NUMBER.** An $n$-gram model stores $|\mathcal V|^n$ counts: for The Time Machine's 28 characters that is **$2.96\times10^{14}$ numbers (1.05 PB) at $n=10$**. **The RNN of §6 needs 2,876 parameters at *any* sequence length.**

**§4 — ⚠️ D2L POSES ZIPF'S EXPONENT AS AN EXERCISE AND NEVER ANSWERS IT.** Fitted from its own printed frequencies: **unigram 0.7184, bigram 0.5703, trigram 0.6447.** Its claim that $n$-grams have a *smaller* exponent than unigrams is **confirmed**; the implied monotone decrease is **not** — and ten points of the head is too weak to settle it.

**§6 — ⚠️ D2L'S EXERCISE 10.2.3 ("compare the cost of GRUs, LSTMs and regular RNNs"), ANSWERED: EXACTLY 3× AND 4×, AT EVERY SIZE.** One gate block costs $dh+h^2+h$; RNN has 1, GRU 3, LSTM 4. **Bidirectional doubles it; a deep RNN adds $(L-1)(h^2+h^2+h)$.**

**§5 — ⚠️ PERPLEXITY'S UPPER BOUND IS THE VOCABULARY SIZE, WHICH FOR THIS CORPUS IS 28** — and real English costs ≈1.1 bits/character (perplexity ≈ 2.14). **The whole usable range of a character model is a factor of 13.1×.**

## 📘 Main Knowledge

### 1. Sequences break the IID assumption, and that is the whole subject

Everything before this chapter assumed examples are exchangeable. **Sequence data are not**: order carries the information. The **autoregressive** formulation conditions each token on its predecessors:

$$P(x_1,\dots,x_T)=\prod_{t=1}^{T}P(x_t\mid x_{t-1},\dots,x_1)$$

**A Markov model of order $n-1$ truncates the conditioning** to the last $n-1$ tokens. A **latent autoregressive** model instead keeps a summary $h_{t-1}$ of everything so far.

> [!note] ⚠️ Two of D2L's asides are the important ones
> **Direction matters.** *"Estimating the forward direction is typically a lot easier than the reverse direction."* Causality is real in physical processes and only conventional in text — **which is exactly why bidirectional RNNs (§11) are legitimate for text and useless for forecasting.**
>
> **$k$-step-ahead prediction degrades, "often dramatically."** When a model is fed its own outputs, each prediction inherits every earlier error. **If a one-step error is $\epsilon$ and the dynamics amplify by $\gamma$ per step, the $k$-step error grows like $\epsilon(1+\gamma+\dots+\gamma^{k-1})$ — geometric whenever $\gamma>1$.** *(That is §7's product structure appearing in the forward pass instead of the backward one.)*
>
> **And D2L's exercise 9.1.2 is the finance version**: an investor picks a security by past returns. **The failure is that the training distribution is conditioned on survival and the future is not drawn from it** — a distribution shift, the topic of [[03 - Logistic Regression|ch. 03]] §11.

### 2. Text → tokens → vocabulary → indices

The pipeline is four steps: load as strings, **tokenize**, build a **vocabulary** mapping tokens to indices, convert. D2L's corpus is H. G. Wells's *The Time Machine*, preprocessed by `re.sub('[^A-Za-z]+', ' ', text).lower()` — **punctuation and capitalization discarded.**

**The tokenization choice is the whole design decision:**

| | vocabulary | sequence length | |
|---|---|---|---|
| **characters** | tiny (**28** here: 26 letters + space + `<unk>`) | long (**173,428**) | no unknown words, but must learn spelling |
| **words** | large (tens–hundreds of thousands) | short | meaning per token, and a long unknown-word tail |
| **word pieces** | tunable | medium | the modern compromise |

**Both figures verified against D2L's printout**: `(173428, 28)`.

> [!note] ⚠️ The `<unk>` token is where the vocabulary decision shows up at test time
> Rare tokens are dropped via `min_freq` and everything unseen maps to `<unk>`. **A character vocabulary essentially never needs it; a word vocabulary always does**, and every `<unk>` is information permanently destroyed. *This is why subword tokenization won.*

### 3. ⚠️ Why counting cannot work — the exponent D2L names without a number

An $n$-gram model must store a count for every possible $n$-token sequence: **$|\mathcal V|^n$ numbers.** D2L says this "increases exponentially" and gives no figure.

| $n$ | $|\mathcal V|=28$ (characters) | as fp32 | $|\mathcal V|=10^4$ (words) | as fp32 |
|---|---|---|---|---|
| 1 | 28 | 112 B | $10^4$ | 39 KB |
| 2 | 784 | 3.06 KB | $10^8$ | 381 MB |
| 3 | 21,952 | 85.75 KB | $10^{12}$ | **3.64 TB** |
| 5 | $1.72\times10^7$ | 65.65 MB | $10^{20}$ | 347 EB |
| **10** | $\mathbf{2.96\times10^{14}}$ | **1.05 PB** | $10^{40}$ | — |

> [!warning] ⚠️ AND THE RNN'S PARAMETER COUNT IS **CONSTANT** IN SEQUENCE LENGTH
> D2L states it — *"the parametrization cost of an RNN does not grow as the number of time steps increases"* — and never sets it against the table. **The RNN of §6 has 2,876 parameters and can condition on 10 tokens or 10,000.**
>
> **A trigram character model already needs 21,952 counts to look back two characters.** ⇒ ***the RNN's advantage is not that it is more accurate; it is that its cost is $O(1)$ in context length where counting is $O(|\mathcal V|^n)$.***

**Laplace smoothing** patches the zero-count problem by adding a constant:
$$\hat P(x)=\frac{n(x)+\epsilon_1/m}{n+\epsilon_1},\qquad \hat P(x'\mid x)=\frac{n(x,x')+\epsilon_2\hat P(x')}{n(x)+\epsilon_2}$$
with $\epsilon\to0$ giving no smoothing and $\epsilon\to\infty$ giving the uniform distribution. **D2L's four objections are all structural**: rare $n$-grams make it unsuitable; all counts must be stored; **word meaning is ignored entirely** ("cat" and "feline" share nothing); and long sequences are almost certainly novel.

### 4. ⚠️ Zipf's law — D2L's exercise 9.2.2, posed and unanswered

$$n_i\propto \frac{1}{i^{\alpha}}\iff \log n_i=-\alpha\log i+c$$

**Fitted by least squares on D2L's own printed top-10 frequencies:**

| order | $\alpha$ (ranks 1–10) | $R^2$ | $\alpha$ (ranks 2–10) | $R^2$ |
|---|---|---|---|---|
| **unigram** | **0.7184** | 0.948 | 0.7693 | 0.915 |
| **bigram** | **0.5703** | 0.965 | 0.4777 | 0.965 |
| **trigram** | **0.6447** | 0.931 | 0.5145 | 0.890 |

*(D2L's own sanity check verifies too: the 10th word's frequency is $440/2261=0.19460$ — "less than 1/5 as common as the most popular." ✓)*

> [!warning] ⚠️ D2L's claim is half confirmed, and I decline to file the other half
> **"Sequences of words also appear to be following Zipf's law, albeit with a smaller exponent, depending on the sequence length."**
>
> **(a) Smaller than the unigram exponent — CONFIRMED** for both bigrams and trigrams, on both fitting windows.
> **(b) A monotone decrease with $n$ — NOT CONFIRMED**: the trigram exponent (0.6447) is *larger* than the bigram's (0.5703), on both windows.
>
> ⚠️ **DECLINED under rule 4.** D2L's wording — "depending on the sequence length" — does not assert monotonicity, and **ten points of the head is far too weak an estimator to settle it**: D2L itself says the first few ranks are "exceptions" and that the power law holds *after* them. **The honest report is that (a) is confirmed and (b) is untested by the printed data.**

> [!warning] ⚠️ THE FINDING D2L SETS UP AND DOES NOT STATE: SIGNAL IMPROVES WITH $n$ AS FREQUENCY COLLAPSES
> | | top-10 that are pure stop-word combinations | most frequent, and its count |
> |---|---|---|
> | unigram | **10 / 10** | *the*, 2261 |
> | bigram | **9 / 10** (D2L counts this) | *of the*, 309 |
> | trigram | **1 / 10** | ***the time traveller*, 59** |
>
> **The trigram list is almost entirely about the book** — *the time traveller*, *the time machine*, *the medical man*. **The unigram list would be identical for any English text.**
>
> ⇒ ***longer $n$-grams are far more informative per occurrence and far rarer — and that is exactly the trade-off that kills count-based models.*** The information you want lives precisely where the counts run out. **D2L prints all three lists on facing pages and draws the conclusion about counts without drawing it about content.**

### 5. Perplexity — and what number counts as good

The natural score is cross-entropy per token, $-\frac1n\sum_t\log P(x_t\mid\cdot)$, made length-comparable. **Perplexity is its exponential:**

$$\mathrm{ppl}=\exp\left(-\frac1n\sum_{t=1}^{n}\log P(x_t\mid x_{t-1},\dots,x_1)\right)$$

**It is the reciprocal geometric mean of the probabilities the model assigned to what actually happened** — loosely, "how many equally-likely options the model was choosing among."

| model | perplexity |
|---|---|
| perfect ($P=1$ always) | **1** |
| **uniform over $|\mathcal V|=28$** | **28** |
| worst ($P=0$ on the truth) | $\infty$ |

> [!warning] ⚠️ The uniform value is a **nontrivial upper bound any useful model must beat** — here, 28
> **And in bits:** $\log_2 28=\mathbf{4.8074}$ bits/character for uniform English. **Shannon (1951) estimated real English at ≈1.1 bits/character, i.e. perplexity ≈ 2.14.**
>
> ⇒ ***the entire usable range of a character-level model is a factor of $28/2.14=13.1\times$ in perplexity, or 4.81 → 1.1 bits.*** A model at perplexity 10 has covered less than half the available ground in bits. *(Shannon's figure is an addition beyond D2L.)*
>
> **This also explains why perplexity and not accuracy**: a language model that is right 20% of the time may be excellent, because the true next token is often genuinely unpredictable. **Perplexity scores the whole distribution; accuracy scores only the `argmax` — [[01 - Introduction to Deep Learning|ch. 01]]'s point about `argmax` asserting a 0–1 loss.**

**Partitioning.** Each epoch discards a random offset $d\in[0,n)$ and cuts the corpus into $m=\lfloor(T-d)/n\rfloor$ subsequences. **Targets are the inputs shifted by one token.** The random offset is what stops the model from only ever seeing the same subsequence boundaries.

### 6. The RNN — one weight matrix, reused at every step

An MLP hidden layer is $\mathbf H=\phi(\mathbf X\mathbf W_{xh}+\mathbf b_h)$. **An RNN adds exactly one term:**

$$\boxed{\mathbf H_t=\phi(\mathbf X_t\mathbf W_{xh}+\mathbf H_{t-1}\mathbf W_{hh}+\mathbf b_h)},\qquad \mathbf O_t=\mathbf H_t\mathbf W_{hq}+\mathbf b_q$$

**$\mathbf W_{hh}\in\mathbb R^{h\times h}$ is the entire difference**, and it is **the same matrix at every time step**.

> [!note] ⚠️ Hidden *state* and hidden *layer* are different things, and D2L is emphatic
> **A hidden layer** is hidden on the path from input to output. **A hidden state** is *"technically speaking an input to whatever we do at a given step"* and can only be computed from earlier time steps. ⇒ *the state is data flowing sideways; the layer is machinery stacked upward.* **§10 stacks layers; the state is what makes it an RNN.**

**Equivalently, $\mathbf X_t\mathbf W_{xh}+\mathbf H_{t-1}\mathbf W_{hh}$ is one matrix multiplication of the concatenations** $[\mathbf X_t,\mathbf H_{t-1}]$ and $\begin{bmatrix}\mathbf W_{xh}\\\mathbf W_{hh}\end{bmatrix}$ — which is how it is implemented and why the parameter count below is a single block.

**⚠️ Parameter counts — D2L's exercise 10.2.3, posed and never answered.** One gate/state block costs $dh+h^2+h$:

| | blocks | recurrent parameters | ratio |
|---|---|---|---|
| **RNN** | 1 ($\mathbf H$) | $dh+h^2+h$ | **1×** |
| **GRU** | 3 ($\mathbf R,\mathbf Z,\tilde{\mathbf H}$) | $3(dh+h^2+h)$ | **3×** |
| **LSTM** | 4 ($\mathbf I,\mathbf F,\mathbf O,\tilde{\mathbf C}$) | $4(dh+h^2+h)$ | **4×** |

| $d$ | $h$ | RNN | GRU | LSTM |
|---|---|---|---|---|
| 28 | 32 | 1,952 | 5,856 | 7,808 |
| 28 | 256 | 72,960 | 218,880 | 291,840 |
| 28 | 1024 | 1,078,272 | 3,234,816 | 4,313,088 |
| 256 | 256 | 131,328 | 393,984 | 525,312 |

**Exactly 3× and 4× at every size — the ratio is structural, not empirical.** With the shared output layer ($hq+q$), the Time Machine setup ($d=q=28$, $h=32$) gives **RNN 2,876 / GRU 6,780 / LSTM 8,732** parameters.

### 7. ⚠️ Backpropagation through time — and the ±0.7% window

**BPTT is ordinary backpropagation on the unrolled graph**, with one twist D2L names: *"the same parameters are repeated throughout the unrolled network… The gradient with respect to each parameter must be summed across all places that the parameter occurs"* — the weight-tying rule from [[05 - Convolutional Neural Network|ch. 05]] §14.

The difficulty is $\partial h_t/\partial w_h$, which is **recursive**:

$$\frac{\partial h_t}{\partial w_h}=\frac{\partial f}{\partial w_h}+\frac{\partial f}{\partial h_{t-1}}\frac{\partial h_{t-1}}{\partial w_h}$$

Unrolling the recursion $a_t=b_t+c_ta_{t-1}$ gives the closed form:

$$\frac{\partial h_t}{\partial w_h}=\frac{\partial f}{\partial w_h}+\sum_{i=1}^{t-1}\left(\prod_{j=i+1}^{t}\frac{\partial f(x_j,h_{j-1},w_h)}{\partial h_{j-1}}\right)\frac{\partial f(x_i,h_{i-1},w_h)}{\partial w_h}$$

**That product of $t-i$ Jacobians is the whole problem.**

| $\gamma$ | $\gamma^{10}$ | $\gamma^{100}$ | $\gamma^{1000}$ |
|---|---|---|---|
| 0.50 | $9.77\times10^{-4}$ | $7.89\times10^{-31}$ | $9.33\times10^{-302}$ |
| 0.90 | 0.3487 | $2.66\times10^{-5}$ | $1.75\times10^{-46}$ |
| 0.99 | 0.9044 | 0.3660 | $4.32\times10^{-5}$ |
| **1.00** | **1.000** | **1.000** | **1.000** |
| 1.01 | 1.105 | 2.705 | $2.10\times10^{4}$ |
| 1.10 | 2.594 | $1.38\times10^{4}$ | $2.47\times10^{41}$ |

> [!warning] ⚠️ THE STABLE WINDOW SHRINKS LIKE $10^{\pm3/T}$
> For $\gamma^T$ to stay within $[10^{-3},10^{3}]$:
>
> | $T$ | admissible $\gamma$ | width |
> |---|---|---|
> | 10 | $[0.501,\ 1.995]$ | ±99.5% |
> | 100 | $[0.933,\ 1.072]$ | ±7.2% |
> | **1000** | $\mathbf{[0.993116,\ 1.006932]}$ | **±0.693%** |
>
> **D2L says text sequences of "over a thousand tokens" are not unusual.** ⇒ ***at that length the recurrent Jacobian's magnitude must sit within 0.7% of 1 or the gradient spans six orders of magnitude.***
>
> **Compare [[04 - Neural Network|ch. 04]] §8**: a sigmoid MLP dies after ~11 layers because the per-layer factor is **bounded above by 0.25**. Here the factor is **unbounded in both directions** *and* **the same matrix is reused at every step, so there is no averaging across independent draws.** ⇒ **vanishing and exploding are the same mechanism in one architecture — which is why RNNs need both clipping (§8) and gating (§9), where an MLP needed only ReLU.**

**D2L's three strategies:** **full computation** (never used — "subtle changes in the initial conditions can potentially affect the outcome a lot"); **truncation after $\tau$ steps** (standard, and D2L argues the bias is *desirable*: "it biases the estimate towards simpler and more stable models"); and **randomized truncation** (unbiased in expectation via $\mathbb E[\xi_t]=1$, and rarely better in practice).

### 8. Gradient clipping — a hack that works, and D2L says so

$$\mathbf g\leftarrow\min\left(1,\frac{\theta}{\|\mathbf g\|}\right)\mathbf g$$

| $\|\mathbf g\|$ | factor | $\|\mathbf g_{\text{clipped}}\|$ |
|---|---|---|
| 0.1 | 1.000000 | 0.1 |
| 1.0 | 1.000000 | 1.0 |
| 10.0 | 0.100000 | **1.0** |
| 1000.0 | 0.001000 | **1.0** |

**Three exact properties:** the norm never exceeds $\theta$; **gradients below $\theta$ are untouched** (clipping is not shrinkage); and **the direction is exactly preserved**, since the factor is a positive scalar.

> [!note] The justification is Lipschitz continuity, and it is quantitative
> $|f(\mathbf x)-f(\mathbf x-\eta\mathbf g)|\le L\eta\|\mathbf g\|$ — **so bounding $\|\mathbf g\|$ bounds how far one step can move the objective.** At $\eta=0.1$ and $L=1$, an unclipped gradient of norm 1,000 permits the objective to move by **100 in a single step**; clipping at $\theta=1$ caps it at **0.1**.
>
> ⇒ **that is how one bad minibatch destroys a run, and what clipping prevents.** It also *"has the desirable side-effect of limiting the influence any given minibatch can exert."*
>
> **D2L is admirably blunt: *"To be clear, it is a hack. Gradient clipping means that we are not always following the true gradient."*** ⚠️ **It is a biased estimator, and it fixes only the exploding half of §7 — the vanishing half needs §9.**

### 9. ⚠️ LSTM — and the carousel the gate can never reach

Each recurrent node becomes a **memory cell** with an **internal state** and three **multiplicative gates**, all sigmoid (so in $(0,1)$):

$$\mathbf I_t=\sigma(\mathbf X_t\mathbf W_{xi}+\mathbf H_{t-1}\mathbf W_{hi}+\mathbf b_i)\quad\text{(input)}$$
$$\mathbf F_t=\sigma(\mathbf X_t\mathbf W_{xf}+\mathbf H_{t-1}\mathbf W_{hf}+\mathbf b_f)\quad\text{(forget)}$$
$$\mathbf O_t=\sigma(\mathbf X_t\mathbf W_{xo}+\mathbf H_{t-1}\mathbf W_{ho}+\mathbf b_o)\quad\text{(output)}$$

plus an **input node** with $\tanh$ (range $(-1,1)$): $\tilde{\mathbf C}_t=\tanh(\mathbf X_t\mathbf W_{xc}+\mathbf H_{t-1}\mathbf W_{hc}+\mathbf b_c)$. Then

$$\boxed{\mathbf C_t=\mathbf F_t\odot\mathbf C_{t-1}+\mathbf I_t\odot\tilde{\mathbf C}_t},\qquad \mathbf H_t=\mathbf O_t\odot\tanh(\mathbf C_t)$$

> [!warning] ⚠️ THE FIX IS ONE PARTIAL DERIVATIVE
> $$\frac{\partial\mathbf C_t}{\partial\mathbf C_{t-1}}=\mathbf F_t$$
>
> **The gradient along the cell path is $\prod_j F_j$ — a product of *scalars the network chooses*, not of Jacobians it is stuck with.**
>
> | $F$ | $F^{10}$ | $F^{100}$ | $F^{1000}$ |
> |---|---|---|---|
> | 0.50 | $9.77\times10^{-4}$ | $7.89\times10^{-31}$ | $9.33\times10^{-302}$ |
> | 0.99 | 0.9044 | 0.3660 | $4.32\times10^{-5}$ |
> | **1.00** | **1** | **1** | **1** |
>
> **At $F=1$ the product is exactly 1 for every $T$** — D2L's *"self-connected recurrent edge of fixed weight 1, ensuring that the gradient can pass across many time steps without vanishing or exploding."* **The constant error carousel.**
>
> **D2L's degenerate case checks:** with $F\equiv1$ and $I\equiv0$, $\mathbf C_t=1\cdot\mathbf C_{t-1}+0=\mathbf C_{t-1}$ — constant forever. ✓

> [!warning] ⚠️ BUT THE GATE IS A SIGMOID, SO $F=1$ IS UNREACHABLE — and the shortfall is measurable
> | forget-gate pre-activation $z$ | $\sigma(z)$ | $F^{1000}$ | **memory half-life (steps)** |
> |---|---|---|---|
> | 0 | 0.50000000 | $9.3\times10^{-302}$ | **1** |
> | 2 | 0.88079708 | $\approx0$ | 5.5 |
> | **4** | 0.98201379 | $1.4\times10^{-8}$ | **38.2** |
> | 6 | 0.99752738 | 0.0842 | 280 |
> | 8 | 0.99966465 | 0.7143 | **2,065** |
> | 10 | 0.99995460 | 0.9556 | 15,272 |
>
> ⇒ ***the carousel is an asymptote the network approaches, not a switch it flips.*** To hold a memory for 1,000 steps the forget gate's pre-activation must reach roughly **8**, which the network has to *learn*.
>
> **This is why LSTM implementations commonly initialize the forget-gate bias to +1 or +2 — starting the cell near the remembering end rather than at $F=0.5$, where the half-life is one step.** *(An addition beyond D2L, which initializes all biases to 0.)*

**The output gate's role is worth naming**: $\mathbf H_t=\mathbf O_t\odot\tanh(\mathbf C_t)$ means **a cell can accumulate information for many steps without affecting the rest of the network at all** (output gate ≈ 0), then release it suddenly when the gate flips toward 1. ⇒ **memory and its use are decoupled**, which no vanilla RNN can do.

### 10. GRU — the same idea with one gate fewer

**Two gates instead of three** (Cho et al. 2014), both sigmoid:

$$\mathbf R_t=\sigma(\mathbf X_t\mathbf W_{xr}+\mathbf H_{t-1}\mathbf W_{hr}+\mathbf b_r)\quad\text{(reset)}$$
$$\mathbf Z_t=\sigma(\mathbf X_t\mathbf W_{xz}+\mathbf H_{t-1}\mathbf W_{hz}+\mathbf b_z)\quad\text{(update)}$$
$$\tilde{\mathbf H}_t=\tanh(\mathbf X_t\mathbf W_{xh}+(\mathbf R_t\odot\mathbf H_{t-1})\mathbf W_{hh}+\mathbf b_h)$$
$$\boxed{\mathbf H_t=\mathbf Z_t\odot\mathbf H_{t-1}+(1-\mathbf Z_t)\odot\tilde{\mathbf H}_t}$$

> [!note] ⚠️ The update is a **convex combination**, and that is the structural difference from the LSTM
> LSTM's $\mathbf C_t=\mathbf F_t\odot\mathbf C_{t-1}+\mathbf I_t\odot\tilde{\mathbf C}_t$ has **two independent gates** — it can both forget *and* write, or neither. **GRU ties them: $\mathbf Z$ and $1-\mathbf Z$ must sum to 1**, so it cannot forget without writing.
>
> ⇒ **the GRU trades one degree of freedom for 25% fewer parameters** (3 blocks vs 4) — and D2L reports it "often achieves comparable performance."
>
> **The two limits are clean:** $\mathbf R_t\to1$ recovers the vanilla RNN exactly; $\mathbf R_t\to0$ makes $\tilde{\mathbf H}_t$ an MLP on $\mathbf X_t$ alone, **resetting the state to defaults**. $\mathbf Z_t\to1$ copies the old state and **skips the time step entirely** in the dependency chain.
>
> D2L's summary: **"Reset gates help capture short-term dependencies; update gates help capture long-term dependencies."**

### 11. Deep and bidirectional

**Deep RNNs** stack recurrent layers: layer $\ell$'s hidden state at time $t$ feeds layer $\ell+1$ at time $t$ *and* layer $\ell$ at time $t+1$. Layer 1 sees $d$ inputs; layers 2…$L$ see $h$:

| $L$ | parameters ($d=q=28$, $h=32$, RNN) |
|---|---|
| 1 | 2,876 |
| 2 | 4,956 |
| 3 | 7,036 |
| 5 | 11,196 |

**Bidirectional RNNs** run one RNN forward and an independent one backward, concatenating the states — so the output layer sees $2h$:

| | unidirectional | bidirectional | ratio |
|---|---|---|---|
| RNN | 2,876 | 5,724 | 1.99× |
| GRU | 6,780 | 13,532 | 2.00× |
| LSTM | 8,732 | 17,436 | 2.00× |

> [!warning] ⚠️ A bidirectional RNN **cannot predict the future**, and this is the most commonly misapplied model in the chapter
> It conditions on the **entire** sequence including tokens after $t$. **For language modelling — predicting $x_{t+1}$ from $x_{\le t}$ — that is leakage: the answer is in the input.** For **forecasting** it is unusable, because the future does not exist yet.
>
> ⇒ **bidirectional models are for tasks where the whole sequence is available and you want a representation of each position** — tagging, named-entity recognition, filling in a masked token. **That is exactly BERT's setting, and exactly not GPT's.** *(§1's "estimating the forward direction is easier than the reverse" is the same observation from the other side.)*

## ✏️ Exercises

> [!example]- Exercise 1 — perplexity
> **(a)** A model assigns 0.5, 0.25, 0.125, 0.125 to the four tokens that actually occurred. Perplexity?
> **(b)** What are the three anchor values, and what is the bound for this corpus?
> **(c)** Convert perplexity 28 and 2.14 to bits per character. What does the gap mean?
>
> ---
> **(a)** $-\frac14(\ln0.5+\ln0.25+\ln0.125+\ln0.125)=\frac14(0.6931+1.3863+2.0794+2.0794)=1.5596$, so $\mathrm{ppl}=e^{1.5596}=\mathbf{4.7568}$. *(Equivalently the reciprocal geometric mean: $(0.5\cdot0.25\cdot0.125\cdot0.125)^{-1/4}=4.7568$.)*
>
> **(b)** Perfect **1**; uniform over the vocabulary **$|\mathcal V|=28$**; worst **$\infty$**. **28 is a nontrivial upper bound any useful model must beat** — it is what you get by storing the text uncompressed.
>
> **(c)** $\log_2 28=\mathbf{4.8074}$ bits/char; $\log_2 2.14=\mathbf{1.0977}$ bits/char. **Shannon's 1951 estimate for English is ≈1.1 bits/char**, so the entire span from "useless" to "human-level" is $28/2.14=\mathbf{13.1\times}$ in perplexity but only **4.81 → 1.10 bits**. ⚠️ *A model at perplexity 10 (3.32 bits) has covered $(4.81-3.32)/(4.81-1.10)=40\%$ of the available ground — perplexity's multiplicative scale flatters progress that bits report honestly.*

> [!example]- Exercise 2 — cost out the three cells (D2L's exercise 10.2.3)
> With $d$ inputs and $h$ hidden units: **(a)** parameters for RNN, GRU, LSTM. **(b)** Evaluate at $d=28$, $h=256$. **(c)** Deep with $L$ layers; bidirectional.
>
> ---
> **(a)** One gate/state block is $\underbrace{dh}_{\mathbf W_{x\cdot}}+\underbrace{h^2}_{\mathbf W_{h\cdot}}+\underbrace{h}_{\mathbf b}$. **RNN 1 block, GRU 3 ($\mathbf R,\mathbf Z,\tilde{\mathbf H}$), LSTM 4 ($\mathbf I,\mathbf F,\mathbf O,\tilde{\mathbf C}$)** — so exactly $1:3:4$, **at every $d$ and $h$**.
>
> **(b)** $28\cdot256+256^2+256=72{,}960$. **RNN 72,960 / GRU 218,880 / LSTM 291,840**, plus a shared output layer.
>
> **(c)** **Deep:** $(dh+h^2+h)+(L-1)(2h^2+h)$ — at $d=q=28$, $h=32$: 2,876 / 4,956 / 7,036 / 11,196 for $L=1,2,3,5$. **Bidirectional:** two independent recurrent parameter sets and an output layer reading $2h$ — **1.99–2.00× in every case.**
>
> ⚠️ **A bidirectional LSTM is $4\times2=8\times$ a vanilla RNN's recurrent cost.** *That is the price of the gating and the backward pass, and it is worth knowing before reaching for the most elaborate cell by default.*

> [!example]- Exercise 3 — why not just count?
> **(a)** How many parameters does an $n$-gram character model ($|\mathcal V|=28$) need at $n=3,5,10$? **(b)** Compare to the RNN. **(c)** Why doesn't smoothing rescue it?
>
> ---
> **(a)** $|\mathcal V|^n$: **21,952** at $n=3$ (85.75 KB); **$1.72\times10^7$** at $n=5$ (65.65 MB); **$2.96\times10^{14}$** at $n=10$ (**1.05 PB**). For a 10,000-word vocabulary, $n=3$ alone is **$10^{12}$ counts = 3.64 TB.**
>
> **(b)** The RNN is **2,876 parameters at every $n$** — its cost is $O(1)$ in context length. At $n=10$ that is a ratio of $10^{11}$.
>
> **(c)** Smoothing fixes *zero counts*, not the three real problems: **storage still scales as $|\mathcal V|^n$**; **word meaning is still ignored** ("cat" and "feline" share no parameters); and **long sequences are almost certainly novel**, so a smoothed estimate of a never-seen 10-gram is just the backoff distribution wearing a disguise. ⚠️ **And §4's finding sharpens it: the informative $n$-grams are exactly the rare ones** — *the time traveller* occurs 59 times against *the*'s 2,261. **You cannot count your way to the signal.**

> [!example]- Exercise 4 — the BPTT window
> **(a)** If each recurrent Jacobian has magnitude $\gamma$, what is the gradient factor over $T$ steps? **(b)** For what $\gamma$ does $\gamma^T$ stay in $[10^{-3},10^3]$ at $T=10,100,1000$? **(c)** Does clipping solve this?
>
> ---
> **(a)** $\gamma^{T}$ — a product of $T$ copies of **the same** matrix, because RNN weights are shared across time.
>
> **(b)** $\gamma\in[10^{-3/T},\,10^{3/T}]$:
>
> | $T$ | window | width |
> |---|---|---|
> | 10 | $[0.501,1.995]$ | ±99.5% |
> | 100 | $[0.933,1.072]$ | ±7.2% |
> | **1000** | $[0.993116,1.006932]$ | **±0.693%** |
>
> **(c)** ⚠️ **No — clipping fixes only the exploding half.** It bounds $\|\mathbf g\|$ above and does nothing when $\gamma^{1000}=1.75\times10^{-46}$; **you cannot rescale a gradient that has underflowed to zero.** The vanishing half needs an architectural fix — **the additive cell path of §9.**
>
> ⚠️ **And note the contrast with [[04 - Neural Network|ch. 04]] §8:** a sigmoid MLP's factor is *bounded by 0.25*, so it can only vanish, and different layers have *independent* weights. **An RNN's factor is unbounded in both directions and identical at every step, so there is no averaging — which is why RNNs needed two fixes and MLPs needed one.**

> [!example]- Exercise 5 — how long can an LSTM remember?
> **(a)** Derive $\partial\mathbf C_t/\partial\mathbf C_{t-1}$ and the gradient over $T$ steps. **(b)** With $F$ a sigmoid, what pre-activation is needed to retain half a memory after 100 steps? After 1,000? **(c)** What does this suggest about initialization?
>
> ---
> **(a)** From $\mathbf C_t=\mathbf F_t\odot\mathbf C_{t-1}+\mathbf I_t\odot\tilde{\mathbf C}_t$, **$\partial\mathbf C_t/\partial\mathbf C_{t-1}=\mathbf F_t$** elementwise, so the cell-path gradient is $\prod_{j}F_j$. **At $F=1$ this is exactly 1 for every $T$** — no vanishing, no exploding.
>
> **(b)** Half-life $=\ln0.5/\ln F$. Inverting for $F$ then $z=\sigma^{-1}(F)$:
>
> | target half-life | required $F$ | required $z$ |
> |---|---|---|
> | 1 step | 0.5000 | 0 |
> | 100 steps | 0.99309 | **4.97** |
> | **1,000 steps** | **0.999307** | **7.28** |
>
> *(Check against the forward table: $z=4\Rightarrow F=0.98201\Rightarrow$ half-life **38.2 steps**; $z=8\Rightarrow F=0.99966\Rightarrow$ **2,065 steps**.)*
>
> **(c)** ⚠️ **At the default zero-bias initialization, $F=\sigma(0)=0.5$ and the memory half-life is ONE STEP.** The network must climb from $z=0$ to $z\approx7$ before it can retain anything long-range — **and the gradient that would teach it to do so is the very gradient the forgetting is destroying.**
>
> ⇒ ***initialize the forget-gate bias positive (+1 or +2 is standard) so the cell starts near the remembering end.*** *(An addition beyond D2L, which sets all biases to 0 — a defensible teaching simplification and a bad default in practice.)*

## 📝 Summary

- **Sequence data break the IID assumption**; autoregression factorizes $P(x_1,\dots,x_T)$ into conditionals, and an RNN replaces the growing history with a **hidden state**. **Forward prediction is easier than reverse, and $k$-step-ahead errors compound geometrically.**
- **Tokenization is the design decision**: The Time Machine is **173,428 characters over a 28-token vocabulary** (verified), against tens of thousands of word types. **Characters never need `<unk>`; words always do.**
- **⚠️ Counting cannot scale**: $|\mathcal V|^n$ is **$2.96\times10^{14}$ (1.05 PB)** at $n=10$ for 28 characters. **The RNN is 2,876 parameters at any context length.** Smoothing fixes zeros, not storage, not meaning, not novelty.
- **⚠️ Zipf's exponent, fitted from D2L's own printout** (its unanswered exercise 9.2.2): **unigram 0.7184, bigram 0.5703, trigram 0.6447.** Smaller-than-unigram **confirmed**; monotone decrease **not confirmed and not testable** from ten head ranks. **Declined, not filed.**
- **⚠️ Signal improves with $n$ exactly as frequency collapses**: the top-10 unigrams are **10/10** stop words, bigrams **9/10**, trigrams **1/10** — and the top trigram, *the time traveller* (59), is about the book. **The information lives where the counts run out.**
- **Perplexity is the reciprocal geometric mean of assigned probabilities.** Anchors: 1, **$|\mathcal V|=28$**, $\infty$. **In bits: 4.8074 uniform, ≈1.1 for real English — the whole usable range is 13.1× in perplexity and 3.7 bits.**
- **An RNN adds exactly one term** ($\mathbf H_{t-1}\mathbf W_{hh}$) to an MLP layer, **reusing the same matrix at every step.** Hidden *state* ≠ hidden *layer*.
- **⚠️ Cell costs are exactly 1 : 3 : 4** (RNN : GRU : LSTM) at every $d$ and $h$ — D2L's unanswered exercise 10.2.3. **Bidirectional doubles it; a bidirectional LSTM is 8× a vanilla RNN.**
- **⚠️ BPTT's gradient is $\gamma^{T}$ over a *reused* matrix. At $T=1000$, $\gamma$ must lie in $[0.993116,1.006932]$ — ±0.693% — or the gradient spans six orders of magnitude.** Unlike [[04 - Neural Network|ch. 04]] §8's sigmoid MLP, the factor is **unbounded in both directions** and identical every step, so it can vanish *and* explode.
- **Gradient clipping preserves direction exactly, leaves small gradients untouched, and bounds one step's effect on the objective** ($L\eta\|\mathbf g\|$: 100 → 0.1 at $\theta=1$, $\eta=0.1$). **D2L calls it a hack; it is biased; it fixes only the exploding half.**
- **⚠️ The LSTM's fix is $\partial\mathbf C_t/\partial\mathbf C_{t-1}=\mathbf F_t$** — a gradient path of gain exactly 1 when $F=1$. **But $F$ is a sigmoid: at zero-bias initialization the memory half-life is ONE STEP, and reaching 1,000 steps needs a pre-activation of ≈7.3.** *The carousel is an asymptote, not a switch* — hence positive forget-gate bias initialization.
- **GRU ties forget and write into one convex combination** ($\mathbf Z$ and $1-\mathbf Z$), trading a degree of freedom for 25% fewer parameters. **$\mathbf R\to1$ recovers the vanilla RNN; $\mathbf Z\to1$ skips the time step entirely.**
- **⚠️ Bidirectional RNNs cannot predict the future** — they condition on tokens after $t$. **Correct for tagging and masked-token tasks (BERT's setting), leakage for language modelling, and useless for forecasting.**

## ⚠️ Important Notes

1. **⚠️ Never use a bidirectional model to predict the next token or forecast.** The answer is in the input. This is the chapter's easiest catastrophic mistake and it produces *excellent* validation numbers.
2. **⚠️ Clipping does not fix vanishing gradients.** It bounds the norm from above only. **If your loss plateaus and long-range structure is never learned, clipping is not the problem and tuning $\theta$ will not help** — change the cell.
3. **⚠️ A zero-initialized forget-gate bias gives a memory half-life of one step.** Initialize it positive if long-range dependencies matter.
4. **⚠️ Report perplexity *and* the vocabulary size.** Perplexity 25 is near-useless on a 28-token vocabulary and superb on a 50,000-token one. **The number is meaningless without its bound.**
5. **⚠️ Perplexity's multiplicative scale flatters progress.** 28 → 10 sounds like a 64% improvement and is **40% of the available bits.** Convert to bits when comparing.
6. **⚠️ Truncated BPTT means your model cannot learn dependencies longer than $\tau$**, whatever the cell. **A "long-range" failure is often a truncation-length setting, not an architecture problem.**
7. **⚠️ The BPTT gradient sums over every occurrence of a shared parameter.** The same weight-tying rule as [[05 - Convolutional Neural Network|ch. 05]]'s kernels — and the same trap: **a parameter used $T$ times effectively trains at $T$ times the learning rate** unless the loss averages over time steps, which D2L's $\frac1T\sum_t$ does.
8. **⚠️ Gating is not a cure, it is a longer leash.** An LSTM still degrades over long enough sequences; it moves the failure from tens of steps to hundreds or thousands. **The architecture that removed the product entirely is attention — [[08 - Sequence to Sequence|ch. 08]].**
9. **⚠️ The random offset in sequence partitioning matters.** Without it the model sees the same subsequence boundaries every epoch and can overfit the partition rather than the language.
10. **⚠️ GRU cannot forget without writing.** $\mathbf Z$ and $1-\mathbf Z$ are tied. **If a task needs to clear state without absorbing the current input, that is a structural argument for the LSTM** — not a hyperparameter search.
11. **⚠️ Character-level and word-level perplexities are not comparable at all** — different vocabularies, different sequence lengths, different bounds. **Convert to bits per *character* to compare across tokenizations.**
12. **Stop words are not noise.** D2L notes that classical bag-of-words classifiers filtered them and that "it is not necessary to filter them out when working with modern RNN- and Transformer-based neural models" — because those models use position and context, which is exactly what makes function words informative.
13. **The `<unk>` token is where information dies.** Every out-of-vocabulary word becomes the same symbol. **Check the `<unk>` rate on your validation set before blaming the model.**
14. **Hidden state ≠ hidden layer.** The state flows sideways in time; layers stack upward. **A "2-layer LSTM with 256 units" has two of the first and 256 of the second**, and confusing them makes every parameter count wrong.

> [!warning] Gaps in the source material
> **All figures are images and never extract.** **Recovered because the prose states their content**: Fig. 9.3.1 (partitioning into five input/target pairs at $n=5$, $d=2$), Fig. 9.4.1 (the RNN unrolled over three time steps — the prose describes the concatenate-then-multiply computation exactly), Fig. 10.1.1–10.1.4 (the LSTM built up gate by gate; every equation is in the text), Fig. 10.2.1–10.2.3 (the GRU, likewise). **Genuinely lost**: the Zipf log–log plots for unigrams, bigrams and trigrams — *but §4 recovers more than the plots showed, since the exponents are fitted from the printed frequency lists that accompany them* — and all training/perplexity curves for §9.5, §9.6, §10.1–10.4. **No perplexity results are quoted in this chapter because none survived extraction.**
>
> **Code listings lose their indentation** and were re-derived from the logic; **printed code *outputs* extract intact**, which is what made §2's `(173428, 28)` and §4's three frequency tables checkable.
>
> **No new cipher entries were needed**; the table in this subject's `CLAUDE.md` covered every formula, including §9.7's $a_t=b_t+c_ta_{t-1}$ recursion and §10.1's gate equations, where deleted $\odot$ symbols and fraction bars had to be reconstructed.
>
> **Added beyond D2L, and labelled as mine throughout:**
> - **The Zipf exponent fits of §4** — D2L's exercise 9.2.2, posed and unanswered — with both fitting windows, the $R^2$ values, and the honest verdict that its monotonicity is untestable from ten ranks.
> - **The stop-word/signal count across $n$-gram orders** (10/10, 9/10, 1/10). D2L counts the bigram row and never extends it.
> - **The $|\mathcal V|^n$ table of §3**, converting D2L's word "exponentially" into 1.05 PB, and the contrast with the RNN's constant cost.
> - **Every parameter count in §6 and §11** — D2L's exercise 10.2.3, answered — including the exact $1:3:4$ ratio, the deep-RNN formula and the bidirectional factor.
> - **The $\pm0.693\%$ stability window of §7** and the $\gamma^T$ tables, plus the comparison with ch. 04 §8's *bounded* sigmoid factor and the observation that weight sharing removes the averaging.
> - **The clipping property table** (§8) and the Lipschitz bound evaluated numerically.
> - **The forget-gate half-life analysis of §9 and exercise 5** — the $z\approx7.3$ requirement for 1,000-step memory and the one-step half-life at zero-bias initialization. **The recommendation to initialize the forget-gate bias positive is standard practice that D2L does not mention.**
> - **Shannon's ≈1.1 bits/character estimate** (§5, exercise 1) and the conversion of perplexity to bits, which turns D2L's three qualitative anchors into a scale.
> - **The bidirectional-leakage warning** (§11) in its explicit BERT-vs-GPT form.
> - **The GRU convex-combination observation** (§10) that $\mathbf Z$ and $1-\mathbf Z$ are tied where the LSTM's $\mathbf I$ and $\mathbf F$ are independent.
>
> **One discrepancy investigated and DECLINED** (§4, logged in [[00-Index]] as **D9**): D2L's claim that $n$-gram frequencies follow Zipf "with a smaller exponent… depending on the sequence length" is confirmed relative to unigrams but **not monotone in $n$** on the printed data (trigram 0.6447 > bigram 0.5703). **Ruled out**: own arithmetic (fitted two windows, both orderings identical), own extraction (the frequency lists are clean printed output). **The wording does not assert monotonicity, and ten head ranks — which D2L itself calls "exceptions" — cannot settle it.** Recorded as a measurement, not an error.
>
> **Deliberately deferred, not omitted:** **§9.5 and §9.6 (the from-scratch and concise RNN implementations)** are used only where they carry a result — gradient clipping (§8) and the parameter structure (§6). **§9.1.3–9.1.4's sine-wave regression experiment** is reported qualitatively because its results are figures. **§10.5–10.8 (machine translation, encoder–decoder, seq2seq, BLEU, beam search) and §11 (attention, Transformer) belong to [[08 - Sequence to Sequence|ch. 08]]** by the scope in [[00-Index]].
>
> **Left as the source states it:** all citations (Elman 1990, Bengio et al. 1994, Hochreiter et al. 2001, Hochreiter & Schmidhuber 1997, Cho et al. 2014, Chung et al. 2014, Werbos 1990, Jaeger 2002, Wood et al. 2011); the historical claim that Hochreiter articulated the vanishing-gradient problem in a 1991 German-language Master's thesis; and the assertion that GRUs are "faster to compute" than LSTMs, which follows from the 3:4 parameter ratio but is not benchmarked here.

**Previous:** [[06 - Object Detection]] · **Next:** [[08 - Sequence to Sequence]]
