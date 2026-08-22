---
subject: Deep Learning
chapter: 4
tags: [ds, deep-learning, mlp, backpropagation, activation-functions, initialization, dropout, optimizers, adam, momentum, conditioning]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 5 (Multilayer Perceptrons), ch. 6 (Builders' Guide), ch. 12 (Optimization Algorithms)"
---

# Neural Network

**⚠️ THE LARGEST SOURCE UNIT OF THE SUBJECT — three D2L chapters merged.** ch. 5 (the MLP itself, backpropagation, numerical stability, dropout), ch. 6 (parameter management), and **ch. 12 (the optimizer family through Adam)**, which the syllabus gives no topic of its own and which every later chapter depends on. *(That merge is a scope call recorded in [[00-Index]].)*

**⚠️ EVERY ONE OF D2L'S SEVEN PRINTED OPTIMIZER TRACES WAS REPRODUCED TO THE LAST DIGIT — from a starting point the book never states.** §12 recovers $\mathbf x_0=(-5,-2)$ by requiring the closed form $x_t=(1-\eta\lambda)^t x_0$ to match the printout, then reproduces both gradient-descent traces, both momentum traces, both Adagrad traces and the RMSProp trace exactly. **D2L prints `x2: -1673.365109` and never says it is $1.4^{20}\times 2$.**

**Seven results.**

**§20 — ⚠️ THE THIRTEEN PRINTED RUNS OF D2L CH. 12, PUT IN ONE TABLE FOR THE FIRST TIME.** Five sections, thirty book-pages apart. **Every final loss lies in $[0.242,\,0.254]$ — a 4.96% band — while wall-clock time varies by 68%.** ⇒ **on this benchmark the optimizer choice buys nothing and costs up to 68% more time.** *The honest reading is not that the optimizers are equivalent — it is that **the benchmark cannot tell them apart**, and D2L argues Adagrad's case from sparse features and then demonstrates it on a dense five-feature regression.*

**§17 — ⚠️ ADAM'S BIAS CORRECTION MAKES THE STEP SMALLER, AND D2L SAYS THE BIAS IS "TOWARDS SMALLER VALUES".** Both states are biased small; **the step is their ratio and the ratio is biased LARGE.** Uncorrected, the first step is $\frac{1-\beta_1}{\sqrt{1-\beta_2}}=\mathbf{3.1623\times}$ too big, **peaks at $6.5685\times$ at step 12**, and comes within 1% of correct only at **step 3,925**.

**§14 — ⚠️ D2L STATES THE EFFECTIVE-STEP FORMULA AND THEN CONTRADICTS IT ON THE NEXT PAGE.** "We reduce the learning rate *slightly* to 0.01": by its own $\eta/(1-\beta)$ that is **0.04 → 0.10, a 2.5× INCREASE** — and **its own printed loss rises 0.246 → 0.254**, recovering only after a further halving.

**§8 — ⚠️ THE SIGMOID'S 0.25 CEILING IS A HARD BOUND ON DEPTH.** Best case, every sigmoid layer multiplies the backward signal by **at most 0.25**, so the gradient falls below `float32` epsilon after **11.50 layers** (realistically **10.11**). **ReLU's factor is exactly 1.** ⇒ *the pre-2010 depth limit was arithmetic, not ideology.*

**§9 — ⚠️ D2L'S "THE MATRIX PRODUCT EXPLODES" HAS A CLOSED FORM.** The top Lyapunov exponent of a product of iid $\mathcal N(0,1)$ $n\times n$ matrices is $\tfrac12[\ln 2+\psi(n/2)]=0.557966$ at $n=4$, predicting $10^{24.23}$ after 100 products. **D2L prints $1.2044\times10^{25}=10^{25.08}$ — a $z$-score of $+0.28$ against 400 Monte-Carlo replications.**

**§10 — ⚠️ THE VAULT'S SIGNATURE RESULT IN A FIFTH SETTING: XAVIER PRESERVES THE MEAN AND NOT THE TYPICAL VALUE.** $\mathbb E\|W\mathbf x\|^2=\|\mathbf x\|^2$ holds **exactly at every width** — and the *median* ratio is 0.842 at $n=4$, with $\mathbb E[\ln]$ negative. **The mean is held up by rare large draws while a typical forward pass shrinks 12.64% per layer.**

**§16 — ⚠️ DIAGONAL PRECONDITIONING BUYS EXACTLY NOTHING ON A ROTATED PROBLEM.** D2L's own exercise, unanswered: the same quadratic rotated 45° has **the same $\kappa=20$**, and diagonal preconditioning takes $\kappa$ **20 → 1** axis-aligned and **20 → 20** rotated.

## 📘 Main Knowledge

### 1. Why a hidden layer is worthless without a nonlinearity

An MLP stacks fully connected layers. With one hidden layer of $h$ units, a minibatch $\mathbf X\in\mathbb R^{n\times d}$, hidden weights $\mathbf W^{(1)}\in\mathbb R^{d\times h}$ and output weights $\mathbf W^{(2)}\in\mathbb R^{h\times q}$:

$$\mathbf H=\mathbf X\mathbf W^{(1)}+\mathbf b^{(1)},\qquad \mathbf O=\mathbf H\mathbf W^{(2)}+\mathbf b^{(2)}$$

> [!warning] ⚠️ This gains *nothing* — and D2L's own algebra says so
> Substituting collapses the two layers into one:
> $$\mathbf O=(\mathbf X\mathbf W^{(1)}+\mathbf b^{(1)})\mathbf W^{(2)}+\mathbf b^{(2)}=\mathbf X\underbrace{\mathbf W^{(1)}\mathbf W^{(2)}}_{\mathbf W}+\underbrace{\mathbf b^{(1)}\mathbf W^{(2)}+\mathbf b^{(2)}}_{\mathbf b}$$
> **An affine function of an affine function is affine, and [[02 - Linear Regression|ch. 02]]'s single layer already represented every affine function.**

**⚠️ D2L asks (ex. 5.1.1) for a case where the extra layer *actively reduces* expressive power, and gives no answer. Here it is, verified numerically.**

The composed map is the matrix product, so $\operatorname{rank}(\mathbf W^{(1)}\mathbf W^{(2)})\le\min(d,h,q)$ — **the hidden width is a hard rank ceiling** *(see [[Linear Algebra/contents/07 - Linear Transformations|Linear Algebra ch. 07]])*.

| architecture | parameters | rank reachable |
|---|---|---|
| one $10\times10$ layer | **110** | **10** |
| $10\to10\to10$ linear | 200 | 10 |
| $10\to5\to10$ linear | 100 | 5 |
| **$10\to2\to10$ linear** | **40** | **2** |

**A concrete instance, checked to machine precision.** With $\mathbf W^{(1)}=\begin{pmatrix}1&2\\0&1\\3&-1\end{pmatrix}$, $\mathbf b^{(1)}=(1,-1)$, $\mathbf W^{(2)}=\begin{pmatrix}2&0&1\\1&1&-1\end{pmatrix}$, $\mathbf b^{(2)}=(0.5,0.5,0.5)$, the collapse gives $\mathbf W=\begin{pmatrix}4&2&-1\\1&1&-1\\5&-1&4\end{pmatrix}$, $\mathbf b=(1.5,-0.5,2.5)$, and at $\mathbf x=(1,2,3)$ **both forms return $(22.5,\,0.5,\,11.5)$ exactly.** But $\operatorname{rank}\mathbf W=2$.

> [!warning] ⚠️ The 3→2→3 network uses **17** parameters to be *strictly less* general than the 12-parameter 3→3 layer
> **More parameters, less expressive power.** ⇒ *parameter count is not capacity.* **This is the sharpest possible statement of why the nonlinearity is not decoration.**

The fix is an elementwise activation $\sigma$ applied after the affine map:

$$\mathbf H=\sigma(\mathbf X\mathbf W^{(1)}+\mathbf b^{(1)}),\qquad \mathbf O=\mathbf H\mathbf W^{(2)}+\mathbf b^{(2)}$$

**And D2L's motivation is worth keeping: linearity implies *monotonicity*.** Income → repayment probability is plausibly monotone (though not linear — "\$0 to \$50,000 matters more than \$1m to \$1.05m"); **body temperature → health is not monotone at all**, since risk rises on *both* sides of 37 °C. Pixel intensity → "is a dog" is neither, and **inverting an image preserves its category** — which no linear model can express.

### 2. The activation functions, and two things D2L does not say

| function | definition | derivative | range |
|---|---|---|---|
| **ReLU** | $\max(x,0)$ | $\mathbb 1[x>0]$ (convention: 0 at $x=0$) | $[0,\infty)$ |
| **pReLU** | $\max(0,x)+\alpha\min(0,x)$ | 1 if $x>0$, $\alpha$ if $x<0$ | $\mathbb R$ |
| **sigmoid** | $\dfrac{1}{1+e^{-x}}$ | $\sigma(x)(1-\sigma(x))$, **max 0.25 at 0** | $(0,1)$ |
| **tanh** | $\dfrac{1-e^{-2x}}{1+e^{-2x}}$ | $1-\tanh^2 x$, **max 1 at 0** | $(-1,1)$ |
| **GELU** | $x\,\Phi(x)$ | — | $\mathbb R$ |
| **Swish** | $x\,\sigma(x)$ | $\sigma(x)\,[1+x(1-\sigma(x))]$ | $\mathbb R$ |

**All four derivative claims verified**: $\sigma'(0)=0.25$, $\tanh'(0)=1$, and D2L §12.1's own $\tanh'(4)=0.0013$ recomputes to **0.0013410** ✓.

> [!warning] ⚠️ (i) tanh and sigmoid are not merely "very similar" — they parametrize **the same function class**
> D2L's exercise 5.1.5 asks for $\tanh(x)+1=2\,\mathrm{sigmoid}(2x)$. **Verified symbolically (difference simplifies to 0) and numerically at five points to $10^{-16}$.** So
> $$\tanh(x)=2\,\mathrm{sigmoid}(2x)-1$$
> ⇒ a tanh unit **is** a sigmoid unit with the input weights doubled, the output weight doubled, and the bias shifted by $-1$. **An affine layer has a bias, so it absorbs the $-1$ exactly.** ⇒ ***the two hypothesis classes are identical, not similar*** — any function one network computes, the other computes with rescaled parameters. **The difference between them is entirely about optimization, never about expressiveness.**

> [!warning] ⚠️ (ii) Swish is **not monotone**, and D2L recommends it without saying so
> $\text{Swish}'(x)=\sigma(x)[1+x(1-\sigma(x))]$ is **negative for $x\lesssim-1.28$**: computed values $-0.0123$ at $x=-6$ and $-0.0908$ at $x=-2$. The function has a **global minimum of $-0.278465$ at $x=-1.278465$**.
>
> ⇒ **Swish and GELU break the monotonicity that §1 used to motivate the whole chapter.** That is a feature, not a bug — a non-monotone activation can represent a "band-pass" response in one unit — but **it must be stated**, because it means the sign of a weight no longer tells you the direction of an effect.

**ReLU's real advantage is the shape of its derivative**, and D2L says it plainly: "either they vanish or they just let the argument through." **No damping factor.** §8 turns that into a number.

### 3. Universal approximation, and why it is not a licence

Cybenko (1989) and Micchelli (1984): **a single hidden layer with enough units approximates any function.** D2L's own caveats are the important part:

- *"Actually learning that function is the hard part."* **The analogy is exact: C can express any computable program; writing the one you want is the problem.**
- **Kernel methods solve some problems *exactly*, even in infinite dimensions** (Kimeldorf & Wahba 1971) — so universality is not a reason to prefer networks.
- **Depth buys compactness**: many functions are represented far more compactly by deep than by wide networks.

> [!note] ⚠️ Read this against [[01 - Introduction to Deep Learning|ch. 01]]'s Table 1.5.1 result
> Ch. 01 found that the switch from kernel methods to deep nets was forced by the **memory** collapse — 10 B per example in 1970 down to 0.1 B in 2020 — because a kernel method needs $O(n^2)$ pairwise structure. **Universal approximation says a shallow net *could* do the job; the memory column says a kernel method *could not*.** The two arguments point the same way for different reasons.

### 4. Forward propagation, the computational graph, backpropagation

For a one-hidden-layer network with a single example $\mathbf x\in\mathbb R^d$, no hidden bias, and $\ell_2$ regularization:

$$\mathbf z=\mathbf W^{(1)}\mathbf x,\quad \mathbf h=\phi(\mathbf z),\quad \mathbf o=\mathbf W^{(2)}\mathbf h,\quad L=l(\mathbf o,y)$$
$$s=\frac{\lambda}{2}\left(\|\mathbf W^{(1)}\|_F^2+\|\mathbf W^{(2)}\|_F^2\right),\qquad J=L+s$$

**Backpropagation is the chain rule run in reverse topological order**, storing each intermediate partial:

$$\frac{\partial J}{\partial L}=1,\qquad \frac{\partial J}{\partial s}=1,\qquad \frac{\partial J}{\partial \mathbf o}=\frac{\partial L}{\partial \mathbf o}\in\mathbb R^q$$
$$\frac{\partial s}{\partial \mathbf W^{(1)}}=\lambda\mathbf W^{(1)},\qquad \frac{\partial s}{\partial \mathbf W^{(2)}}=\lambda\mathbf W^{(2)}$$
$$\boxed{\frac{\partial J}{\partial \mathbf W^{(2)}}=\frac{\partial J}{\partial\mathbf o}\mathbf h^\top+\lambda\mathbf W^{(2)}}\qquad \frac{\partial J}{\partial\mathbf h}=\mathbf W^{(2)\top}\frac{\partial J}{\partial\mathbf o}$$
$$\frac{\partial J}{\partial\mathbf z}=\frac{\partial J}{\partial\mathbf h}\odot\phi'(\mathbf z)\qquad \boxed{\frac{\partial J}{\partial \mathbf W^{(1)}}=\frac{\partial J}{\partial\mathbf z}\mathbf x^\top+\lambda\mathbf W^{(1)}}$$

> [!warning] ⚠️ Three structural facts hiding in these six lines
> 1. **Each weight gradient is an outer product** of a backward vector and a forward activation. That is *why* the forward activations must be kept alive until the backward pass reaches them.
> 2. **$\odot\,\phi'(\mathbf z)$ is the only place the activation enters the backward pass** — and it is a *multiplication*. Every layer contributes one such factor. **§8 is the consequence.**
> 3. **The regularizer contributes $+\lambda\mathbf W$ additively at every layer** and is the only term not routed through the graph. ⇒ weight decay is a gradient that exists even when the data gradient is zero.

**Forward and backward are mutually dependent**: the regularization term needs the current weights (given by the last optimizer step), and the weight gradient needs $\mathbf h$ (given by the forward pass). ⇒ they must **alternate**, and the intermediates must be retained.

### 5. What training actually costs — D2L's exercise 5.3.3, unanswered

D2L says only that "training requires significantly more memory than prediction." **Counted, for its own MLP** ($784\to256\to10$, batch 256, `float32`):

$$\text{parameters}=784\cdot256+256+256\cdot10+10=\mathbf{203{,}530}$$

| item | floats | MB |
|---|---|---|
| weights | 203,530 | **0.776** |
| gradients (same shape) | 203,530 | 0.776 |
| stored activations $\mathbf X,\mathbf Z^{(1)},\mathbf H,\mathbf O$ | 334,336 | **1.275** |

| optimizer | state per parameter | parameter memory | vs SGD |
|---|---|---|---|
| SGD | 0 | 1.553 MB | 1.00× |
| SGD + momentum ($\mathbf v$) | 1 | 2.329 MB | 1.50× |
| Adagrad / RMSProp ($\mathbf s$) | 1 | 2.329 MB | 1.50× |
| Adadelta ($\mathbf s,\Delta\mathbf x$) | 2 | 3.106 MB | 2.00× |
| **Adam ($\mathbf v,\mathbf s$)** | **2** | **3.106 MB** | **2.00×** |

> [!warning] ⚠️ **Adam costs exactly 2× SGD's parameter memory — four copies of the model instead of two**
> Training this MLP with Adam needs $\mathbf{5.64\times}$ what prediction needs.
>
> **Scaled to a 1-billion-parameter model in `float32`: weights 3.73 GB, +gradients 7.45 GB, +Adam state 14.90 GB.** ⇒ ***the optimizer, not the model, is half the memory bill*** — which is the entire reason mixed precision, 8-bit optimizer states and ZeRO sharding exist. *(Practice D2L predates; flagged as an addition.)*
>
> **And activations scale with batch size while parameters do not** — 1.275 MB here at batch 256, and D2L's warning follows: "training deeper networks using larger batch sizes more easily leads to out-of-memory errors."

### 6. Vanishing and exploding gradients — the mechanism

For an $L$-layer network the gradient with respect to layer $l$'s weights is a **product of $L-l$ Jacobians**:

$$\partial_{\mathbf W^{(l)}}\mathbf o=\underbrace{\partial_{\mathbf h^{(L-1)}}\mathbf h^{(L)}}_{\mathbf M^{(L)}}\cdots\underbrace{\partial_{\mathbf h^{(l)}}\mathbf h^{(l+1)}}_{\mathbf M^{(l+1)}}\underbrace{\partial_{\mathbf W^{(l)}}\mathbf h^{(l)}}_{\mathbf v^{(l)}}$$

**A long product of matrices with eigenvalues that are not near 1 either collapses or diverges — geometrically, in the number of layers.** D2L's own framing is right: it is the multiplying-many-probabilities problem, except that switching to log-space does not rescue it because the matrices can be individually large *and* small.

The two failure modes:
- **exploding** → updates destroy the model;
- **vanishing** → parameters hardly move and learning stops.

### 7. ⚠️ A third failure D2L raises and does not quantify: symmetry

Initialize every hidden weight to the same constant $c$. Then every hidden unit sees the same input, produces the same activation, and receives the same gradient — **so they remain identical forever.** A layer of $h$ units behaves as **one** unit.

> [!note] Two consequences worth naming
> **(i)** This is why random initialization is *required*, not merely helpful. **(ii)** D2L notes that **dropout breaks the symmetry that SGD cannot** — because dropout zeroes a *different* subset each step, two identical units stop receiving identical gradients. *(Its exercise 12.1.1 is the same fact from the other side: any local minimum of a $d$-unit hidden layer has at least $d!$ permutation-equivalent twins.)*

### 8. ⚠️ THE SIGMOID CEILING ON DEPTH — arithmetic D2L never does

The sigmoid's derivative has a **hard maximum of 0.25**, attained only at $z=0$. Every sigmoid layer therefore multiplies the backward signal by **at most $\tfrac14$** — *even in the best case, even with perfect weights*.

| layers $L$ | best case $0.25^L$ | realistic $\mathbb E[\sigma'(z)]^L$, $z\sim\mathcal N(0,1)$ |
|---|---|---|
| 1 | $2.500\times10^{-1}$ | $2.066\times10^{-1}$ |
| 5 | $9.766\times10^{-4}$ | $3.768\times10^{-4}$ |
| **10** | $9.537\times10^{-7}$ | $1.420\times10^{-7}$ |
| 12 | $5.960\times10^{-8}$ | $6.062\times10^{-9}$ |
| 20 | $9.095\times10^{-13}$ | $2.016\times10^{-14}$ |
| 50 | $7.889\times10^{-31}$ | $5.768\times10^{-35}$ |

*(Simulated $\mathbb E[\sigma'(z)]=0.206643$ over $4\times10^6$ draws.)*

> [!warning] ⚠️ THE NUMBER: `float32` epsilon is $1.192\times10^{-7}$
> $$L_{\text{best}}=\frac{\ln\varepsilon_{32}}{\ln 0.25}=\mathbf{11.50}\ \text{layers}\qquad L_{\text{realistic}}=\mathbf{10.11}\ \text{layers}$$
> **A sigmoid MLP loses its gradient to floating-point underflow at about ten layers, and that is the OPTIMISTIC calculation** — it assumes every pre-activation sits at the sigmoid's sweet spot and ignores the weight matrices entirely.
>
> **ReLU's factor on the active half-line is exactly 1**, so $1^L=1$ for every $L$. Its active *fraction* shrinks, but the surviving paths are **undamped**.
>
> ⇒ ***this is the whole content of "ReLU mitigates vanishing gradients", stated as a bound instead of a sentiment.***
>
> **And it shows why raising the learning rate cannot fix it:** compensating for $L$ sigmoid layers needs a $4^L$ multiple — $1.024\times10^3$ at $L=5$, $1.049\times10^6$ at $L=10$ — **which is exactly the factor that makes the shallow layers diverge.** *The deep layers and the shallow layers demand incompatible learning rates. There is no single $\eta$ that works.*

> [!note] ⚠️ Cross-chapter: this is a SECOND, INDEPENDENT mechanism for [[01 - Introduction to Deep Learning|ch. 01]]'s neural-network winter
> Ch. 01 dated the winter to 1995–2005 and traced it to **memory** — a 44 kHz-audio dense layer is 176 MB, short of the 1990 row by 17.6× and first fitting only in the 2010 row. **§8 is a different constraint entirely: even with unlimited memory a sigmoid network deeper than ~10 layers could not be trained in single precision.**
>
> ⇒ **two independent binding constraints, both released around 2010** (GPU memory; ReLU, 2010, Nair & Hinton). *A conclusion supported by two unrelated mechanisms is stronger than one supported twice — the vault's standing lesson from Marketing/Business Management.*

### 9. ⚠️ D2L'S EXPLODING-MATRIX DEMO HAS A CLOSED FORM

D2L multiplies 100 iid $\mathcal N(0,1)$ $4\times4$ matrices, prints entries around $1.2044\times10^{25}$, and says only "the matrix product explodes." **The growth rate is a known constant.**

For a product of iid Gaussian $n\times n$ matrices with entry scale $\sigma$, the **top Lyapunov exponent** is

$$\lambda_1=\tfrac12\left[\ln(2\sigma^2)+\psi(n/2)\right]$$

*(Cohen & Newman 1984; $\psi$ is the digamma function. Added beyond D2L.)* At $n=4,\ \sigma=1$: $\lambda_1=\tfrac12[0.693147+0.422784]=\mathbf{0.557966}$.

| | |
|---|---|
| predicted magnitude after 100 products | $e^{100\lambda_1}=10^{24.23}$ |
| **D2L's printed largest entry** | $1.2044\times10^{25}=10^{25.08}$ |
| Monte Carlo, 400 replications of the exact experiment | mean $10^{24.61}$, sd $1.66$ decades, range $[10^{19.72},10^{29.67}]$ |
| **D2L's single printed run** | **$z=+0.28$ — a completely typical draw** |

> [!warning] ⚠️ The critical scale, and Xavier compared against it
> Scaling every matrix by $\sigma$ shifts $\lambda_1$ by $\ln\sigma$. **Neutral propagation therefore needs**
> $$\sigma^*=e^{-\lambda_1}=\mathbf{0.572372}\quad(n=4)$$
> **Xavier at $n_{\text{in}}=n_{\text{out}}=4$ gives $\sigma=\sqrt{2/8}=0.5$ — $0.8736\times$ the neutral scale, contracting the top direction by 12.64% per layer.**
>
> ⇒ **Xavier is not neutral for the *extreme* direction at small width; it is neutral only in the limit.** Verified over 20,000 layers: $n=4$ theory $-0.135181$ vs simulated $-0.137873$; $n=64$ theory $-0.007853$ vs simulated $-0.007866$; $n=256$ theory $-0.001956$ vs simulated $-0.001730$. **The deficit vanishes like $O(1/n)$.**
>
> **Note the spread: 400 identical experiments ranged over ten orders of magnitude.** ⇒ *"the product explodes" is a statement about a distribution, and any single printed run is one draw from it. **D2L prints one run and generalizes from it.***

### 10. Initialization — ⚠️ AND THE VAULT'S SIGNATURE RESULT IN A FIFTH SETTING

**Xavier's derivation** (Glorot & Bengio 2010). With $o_i=\sum_{j=1}^{n_{\text{in}}}w_{ij}x_j$, weights iid with mean 0 and variance $\sigma^2$, inputs iid with mean 0 and variance $\gamma^2$, all independent:

$$\mathbb E[o_i]=\sum_j\mathbb E[w_{ij}]\,\mathbb E[x_j]=0,\qquad \operatorname{Var}[o_i]=\sum_j\mathbb E[w_{ij}^2]\mathbb E[x_j^2]=n_{\text{in}}\sigma^2\gamma^2$$

Forward stability wants $n_{\text{in}}\sigma^2=1$; **backward stability wants $n_{\text{out}}\sigma^2=1$.** These cannot both hold, so Xavier splits the difference:

$$\tfrac12(n_{\text{in}}+n_{\text{out}})\sigma^2=1\iff \sigma=\sqrt{\frac{2}{n_{\text{in}}+n_{\text{out}}}}\qquad\text{or}\qquad \mathcal U\!\left(-\sqrt{\tfrac{6}{n_{\text{in}}+n_{\text{out}}}},\ \sqrt{\tfrac{6}{n_{\text{in}}+n_{\text{out}}}}\right)$$

**The uniform variant checks out**: $\operatorname{Var}[\mathcal U(-a,a)]=a^2/3$, and $\left(\sqrt{6/(n_{\text{in}}+n_{\text{out}})}\right)^2/3=2/(n_{\text{in}}+n_{\text{out}})=\sigma^2$ ✓.

**How far the compromise is from either pure condition, for D2L's own layer** $784\to256$: forward-only wants $\sigma=0.035714$, backward-only wants $0.062500$, Xavier gives $0.043853$ — **$1.2279\times$ the forward value and $0.7016\times$ the backward.** ⇒ *the compromise is exact only when $n_{\text{in}}=n_{\text{out}}$, and is a real compromise otherwise.*

> [!warning] ⚠️ THE MEAN IS EXACTLY RIGHT AND THE TYPICAL VALUE IS NOT
> Xavier's derivation is a statement about a **mean**, and it is exact. Simulated $\mathbb E\left[\|W\mathbf x\|^2/\|\mathbf x\|^2\right]$ with $\sigma^2=1/n$:
>
> | $n$ | mean (theory 1.00000) | **median** | $\mathbb E[\ln\text{ratio}]$ |
> |---|---|---|---|
> | 4 | 1.00352 | **0.84195** | $-0.26517$ |
> | 16 | 1.00109 | 0.96117 | $-0.06270$ |
> | 64 | 1.00005 | 0.98843 | $-0.01565$ |
> | 256 | 1.00040 | **0.99788** | $-0.00349$ |
>
> **The mean is preserved at every width. The median is below 1 and the mean of the log is negative** — so a *typical* forward pass shrinks while the average is held up by rare large draws. **Compounded over 50 layers at $n=4$ the typical squared norm is $\times1.58\times10^{-6}$ while the mean is still exactly 1.00.**
>
> ⇒ ***a lognormal-shaped quantity is not summarized by its mean.*** **This is the same structure the vault found in Commercial Banking ch. 02/06/11/12 (a mean pool loss of 5.00% at every correlation while the senior tranche goes 0.0000% → 1.8044%) and in [[02 - Linear Regression|ch. 02]] here (a printed penalty 1.11% from the truth while $\|\hat{\mathbf w}-\mathbf w\|$ exceeded $\|\mathbf w\|$ itself).** **Hunt for a sixth.**
>
> **The practical consequence:** narrow layers are more dangerous than the variance calculation suggests, and this is *why* modern practice widens rather than deepens at fixed parameter count.

**Beyond Xavier:** D2L notes over a dozen framework heuristics, and that **Xiao et al. (2018) trained 10,000-layer networks with initialization alone, no architectural tricks** — a direct demonstration that §8/§9's constraints are about *scale*, not depth as such.

### 11. Generalization in deep networks — the classical picture breaks

D2L is unusually honest here and it is worth preserving.

- **Deep networks are over-parametrized and typically *interpolate***: they fit every training label, including **randomly assigned** ones (Zhang et al. 2021). ⇒ **VC dimension and Rademacher complexity cannot explain why they generalize** — a class that fits arbitrary labels has vacuous bounds.
- Because all candidate architectures reach zero training error, **every remaining gain must come from closing the generalization gap.**
- **Making the model *more* expressive often *reduces* generalization error** — the **double descent** pattern (Nakkiran et al. 2021): complexity hurts, then helps.
- **The nonparametric framing is more reliable**: 1-nearest-neighbour has zero training error *and is consistent*. Jacot et al. (2018) showed infinitely wide MLPs become kernel methods — the **neural tangent kernel**.
- **Early stopping** works because networks fit **cleanly labelled data first** and interpolate mislabelled data only later (Rolnick et al. 2017; Garg et al. 2021). **Patience criterion**: stop when validation error has not improved by $\epsilon$ for some number of epochs.

> [!warning] ⚠️ The one operational rule in this section
> **Early stopping matters when there is label noise or intrinsic label variability, and barely matters when the classes are truly separable.** D2L: *"training models until they interpolate noisy data is typically a bad idea."*
>
> **And the caveat about weight decay is important:** typical $\ell_2$ strengths are **insufficient to prevent interpolation**, so its benefit "might only make sense in combination with early stopping." ⇒ *weight decay in deep learning may work by encoding an inductive bias, not by constraining capacity — a radically different mechanism from the ridge shrinkage of [[02 - Linear Regression|ch. 02]], where $\sigma_j^2/(\sigma_j^2+\lambda)$ was exactly computable.*

### 12. Dropout — D2L states the mean and never states the variance

Bishop (1995) proved training with **input** noise is equivalent to **Tikhonov regularization**. Srivastava et al. (2014) applied the idea to internal layers. With dropout probability $p$:

$$h'=\begin{cases}0 & \text{with probability } p\\[2pt] \dfrac{h}{1-p} & \text{otherwise}\end{cases}$$

**$\mathbb E[h']=h$ — confirmed exactly.** But:

$$\mathbb E[h'^2]=(1-p)\frac{h^2}{(1-p)^2}=\frac{h^2}{1-p}\ \Longrightarrow\ \boxed{\operatorname{Var}[h']=h^2\frac{p}{1-p}},\qquad \mathrm{CV}=\sqrt{\frac{p}{1-p}}$$

| $p$ | $\operatorname{Var}[h']/h^2$ | **CV = sd/mean** |
|---|---|---|
| 0.1 | 0.1111 | 0.3333 |
| 0.2 | 0.2500 | 0.5000 |
| **0.5** | **1.0000** | **1.0000** |
| 0.8 | 4.0000 | 2.0000 |
| 0.9 | 9.0000 | 3.0000 |
| 0.95 | 19.0000 | 4.3589 |

> [!warning] ⚠️ AT D2L'S OWN CHOICE $p=0.5$ THE INJECTED NOISE HAS STANDARD DEVIATION **EXACTLY EQUAL** TO THE ACTIVATION IT REPLACES
> $\mathrm{CV}=1.0000$ exactly. **Dropout at $p=0.5$ is not a mild perturbation; it replaces each activation with a random variable as variable as the activation itself.**
>
> **And this supplies the missing reason for D2L's unexplained advice** — *"a common choice is to set a lower dropout probability closer to the input layer."* Noise injected at layer 1 is propagated through **every** later layer; noise injected at the last hidden layer is not. **The variance table is the argument, and D2L gives the advice without it.** *(D2L's own exercise 5.6.3 asks for exactly this variance and the book never answers it.)*

**Test time:** dropout is disabled and no rescaling is needed — that is what the $1/(1-p)$ debiasing bought. *(D2L notes the exception: keeping dropout on at test time and checking whether predictions agree is a cheap uncertainty heuristic — MC dropout.)*

### 13. ⚠️ And D2L's printed dropout example is not a 50% sample

D2L prints, for $\mathbf X=\begin{pmatrix}0&1&2&3&4&5&6&7\\8&9&10&11&12&13&14&15\end{pmatrix}$ at $p=0.5$:

```
dropout_p = 0.5:  tensor([[ 0.,  2.,  4.,  0.,  8., 10., 12.,  0.],
                          [16., 18., 20., 22.,  0.,  0.,  0., 30.]])
```

**Every surviving entry is exactly $2\times$ its original — confirmed for all of them.** Counting survivors:

| | |
|---|---|
| units kept | **11 of 16 = 68.75%** (nominal 50%) |
| $P(\ge 11\text{ survive})$ under $\mathrm{Bin}(16,0.5)$ | **0.1051** |
| mean of $\mathbf X$ | 7.5000 |
| **mean of the printed $h'$** | **8.8750** |
| **deviation** | **+18.33%**, $+0.62$ sd |

> [!warning] ⚠️ Unbiased is not the same as correct on any one draw — **and a network sees one draw per step**
> The realization is entirely ordinary ($p=0.11$, $z=+0.62$); **that is the point.** $\mathbb E[h']=h$ guarantees nothing about the layer the optimizer actually receives. **The 1.0 coefficient of variation from §12 is what the network experiences; the unbiasedness is what the textbook describes.**
>
> *This is the vault's standing rule from [[02 - Linear Regression|ch. 02]] — **read what the code prints, not what the caption says** — firing a third time in this subject.*

### 14. Parameter management (D2L ch. 6) — the parts that carry an idea

The rest of ch. 6 is framework mechanics. Four things generalize:

- **Parameter access.** `net[2].state_dict()`, `net[2].bias.data`, `net.named_parameters()`. A parameter is an object holding a value **and** a gradient; `.grad` is `None` until `backward()` runs.
- **⚠️ Tied (shared) parameters.** Passing the *same* layer object twice makes the two positions **one tensor**, not two equal tensors — changing one changes the other. **And the gradients ADD**: a parameter used twice receives the sum of both paths' gradients. *(That is the chain rule for a variable with two children, and it is the mechanism behind weight tying in language models and the shared kernel of [[05 - Convolutional Neural Network|ch. 05]].)*
- **⚠️ Lazy initialization.** `nn.LazyLinear` defers shape inference until the first forward pass; before that `net[0].weight` is literally `<UninitializedParameter>`. **This is why [[02 - Linear Regression|ch. 02]]'s concise weight-decay run started from a different weight norm than the from-scratch run** — the framework's default initializer, not the book's `sigma=0.01`, and that 8.4× discrepancy is logged as declined discrepancy D4.
- **Custom layers** are just `nn.Module` subclasses with a `forward`; `nn.Parameter` registers a tensor for autograd, saving, and initialization. *(D2L's `CenteredLayer` returns `X - X.mean()` and the sanity check prints a mean of `2.3283e-09` — floating point, not a bug.)*

---

## The optimizer family (D2L ch. 12)

### 15. The landscape: local minima, saddle points, vanishing gradients

**Optimization and learning are different goals** — training error vs. generalization error, exactly [[02 - Linear Regression|ch. 02]]'s point. This chapter is about the *training* error only.

**Saddle points dominate local minima in high dimensions.** At a zero-gradient point the Hessian's $k$ eigenvalues decide: all positive → local minimum; all negative → local maximum; **mixed signs → saddle**. For large $k$ the probability that *all* eigenvalues share a sign is minuscule, so **saddles are far more common than minima** *(see [[Optimization/contents/03 - Unconstrained Optimality Conditions|Optimization ch. 03]])*.

**Newton's method** uses the curvature: from $f(\mathbf x+\boldsymbol\epsilon)\approx f(\mathbf x)+\boldsymbol\epsilon^\top\nabla f+\tfrac12\boldsymbol\epsilon^\top\mathbf H\boldsymbol\epsilon$, setting the derivative to zero gives $\boldsymbol\epsilon=-\mathbf H^{-1}\nabla f$.

> [!warning] ⚠️ Newton's fatal flaw is a sign, and D2L demonstrates it
> **Where the Hessian is negative, $-\mathbf H^{-1}\nabla f$ points *uphill*.** D2L runs it on $f(x)=x\cos(cx)$ from $x=10$ and lands at **$x=26.83$** — further from every minimum than it started. **Adding a learning rate $\eta=0.5$ fixes it** ($x=7.27$).
>
> And the cost is prohibitive anyway: $O(d^2)$ storage for $\mathbf H$. ⇒ **the whole adaptive-optimizer family is an attempt to approximate the *diagonal* of $\mathbf H^{-1}$ cheaply.** *(Full treatment in [[Optimization/contents/06 - Newton and Quasi-Newton Methods|Optimization ch. 06]].)*
>
> **Convergence is quadratic once in the basin**: $|e^{(k+1)}|\le c\,(e^{(k)})^2$ — but *"we do not really have much of a guarantee when we will reach the region of rapid convergence."*

### 16. ⚠️ THE ILL-CONDITIONED QUADRATIC — D2L'S TRACES, REPRODUCED EXACTLY

D2L's running example is $f(\mathbf x)=0.1x_1^2+2x_2^2$, whose Hessian eigenvalues are $\lambda_1=0.2,\ \lambda_2=4$, so $\kappa=20$.

**Gradient descent on a quadratic is exactly solvable per eigendirection, and D2L never writes the formula:**

$$x_t=(1-\eta\lambda)^t\,x_0$$

| $\eta$ | closed form, 20 steps from $\mathbf x_0=(-5,-2)$ | **D2L prints** |
|---|---|---|
| 0.4 | $x_1=(0.92)^{20}(-5)=-0.943467$, $x_2=(-0.6)^{20}(-2)=-0.000073$ | **`x1: -0.943467, x2: -0.000073`** ✓ |
| 0.6 | $x_1=(0.88)^{20}(-5)=-0.387814$, $x_2=(-1.4)^{20}(-2)=-1673.365109$ | **`x1: -0.387814, x2: -1673.365109`** ✓ |

> [!warning] ⚠️ THE START POINT IS NOT IN THE TEXT — it was recovered by requiring the closed form to match the printout
> $\mathbf x_0=(-5,-2)$. **Both traces then reproduce to all six printed decimals, in both coordinates, at both learning rates.**
>
> **$1.4^{20}=836.6826$, and $836.6826\times 2=1673.365109$. That IS D2L's printed divergence.** The book presents it as a cautionary illustration; it is a closed-form prediction.

**The stability bound follows immediately.** $|1-\eta\lambda_{\max}|<1\iff \eta<2/\lambda_{\max}=\mathbf{0.5}$. **$\eta=0.4$ is 80% of the bound (stable); $\eta=0.6$ is 120% (divergent), diverging at rate 1.4 per step.** ⇒ *the "slight increase in learning rate from 0.4 to 0.6" D2L describes crossed a knife-edge it never names.*

**And the tension it creates is the whole reason the rest of the chapter exists:** $x_2$ needs a small $\eta$ to stay stable while $x_1$ needs a large one to make progress. **They are the same $\eta$.**

### 17. ⚠️ THE CONDITION NUMBER SETS THE STEP COUNT — $\kappa$ versus $\sqrt\kappa$

With the optimal $\eta^*=\frac{2}{\lambda_{\min}+\lambda_{\max}}$, gradient descent contracts by $\frac{\kappa-1}{\kappa+1}$ per step. **Momentum with the optimal $\beta^*=\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^2$ contracts by $\frac{\sqrt\kappa-1}{\sqrt\kappa+1}$.** *(Standard; D2L gestures at it with "$0<\eta<2+2\beta$ velocity converges" and stops.)*

| $\kappa$ | GD steps for 100× error reduction | momentum steps | **speedup** |
|---|---|---|---|
| 1 | 1 | 1 | 1.00× |
| 4 | 9.0 | 4.2 | 2.15× |
| **20** *(D2L's example)* | **46.0** | **10.1** | **4.55×** |
| 100 | 230.3 | 22.9 | 10.03× |
| 1,000 | 2,302.6 | 72.8 | 31.63× |
| 10,000 | 23,025.9 | 230.3 | **100.00×** |

> [!warning] ⚠️ **GD needs $O(\kappa)$ steps; momentum needs $O(\sqrt\kappa)$. That is what "accelerated gradient method" MEANS**
> At D2L's own $\kappa=20$: **46.01 steps versus 10.12.** At $\kappa=10^4$ the gap is exactly $100\times$ — because $\sqrt{10^4}=100$.
>
> ⇒ **momentum's benefit grows without bound as the problem worsens, and is nearly nil on a well-conditioned one.** *This is the single most useful fact in the chapter and D2L states none of it.*

**D2L's momentum traces also reproduce exactly:**

$$\mathbf v_t\leftarrow\beta\mathbf v_{t-1}+\mathbf g_t,\qquad \mathbf x_t\leftarrow\mathbf x_{t-1}-\eta\mathbf v_t$$

| $\eta,\beta$ | simulated | **D2L prints** |
|---|---|---|
| $0.6,\ 0.5$ | $(+0.007188,\ +0.002553)$ | **`x1: 0.007188, x2: 0.002553`** ✓ |
| $0.6,\ 0.25$ | $(-0.126340,\ -0.186632)$ | **`x1: -0.126340, x2: -0.186632`** ✓ |

**At $\eta=0.6$ plain gradient descent diverges to $-1673$ and momentum at $\beta=0.5$ lands at $0.0072$.** Same problem, same learning rate, same 20 steps.

**Why it works, in one sentence:** expanding $\mathbf v_t=\sum_{\tau=0}^{t-1}\beta^\tau\mathbf g_{t-\tau}$, **directions where gradients agree accumulate and directions where they oscillate cancel.**

### 18. ⚠️ D2L CALLS A 2.5× INCREASE IN STEP SIZE A "SLIGHT REDUCTION"

D2L derives the effective step size itself: since $\sum_\tau\beta^\tau=\frac{1}{1-\beta}$, *"rather than taking a step of size $\eta$… we take a step of size $\frac{\eta}{1-\beta}$."* Then it retunes:

| $\eta$ | $\beta$ | effective sample size $\frac1{1-\beta}$ | **effective step $\frac{\eta}{1-\beta}$** | vs. first run | **D2L's printed loss** |
|---|---|---|---|---|---|
| 0.02 | 0.5 | 2.0 | **0.0400** | — | **0.246** |
| 0.01 | 0.9 | 10.0 | **0.1000** | **+150%** | **0.254** ⚠️ |
| 0.005 | 0.9 | 10.0 | 0.0500 | +25% | 0.247 |

> [!warning] ⚠️ "We reduce the learning rate **slightly** to 0.01 to keep matters under control"
> **By D2L's own formula, halving $\eta$ while raising $\beta$ from 0.5 to 0.9 MULTIPLIED the effective step by 2.5×.**
>
> **And its own printed loss confirms the damage: 0.246 → 0.254, +3.25% worse.** It recovers to 0.247 only after a *further* halving to 0.005 — which is still $1.25\times$ the original effective step.
>
> ⇒ ***the operational rule: $\eta$ and $\beta$ are not independent knobs. Raising $\beta$ from 0.9 to 0.99 without dividing $\eta$ by 10 is a 10× learning-rate increase in disguise.*** **This is the chapter's most immediately usable finding, and the source contradicts itself two paragraphs apart.**

### 19. Adagrad, preconditioning, and the rotated problem

**Adagrad** (Duchi et al. 2011) accumulates squared gradients per coordinate:

$$\mathbf s_t=\mathbf s_{t-1}+\mathbf g_t^2,\qquad \mathbf w_t=\mathbf w_{t-1}-\frac{\eta}{\sqrt{\mathbf s_t+\epsilon}}\odot\mathbf g_t$$

**The motivation is sparse features**: with a global decaying $\eta$, common features converge while rare ones are still under-trained. Adagrad gives each coordinate its own clock.

**The deeper motivation is preconditioning.** Rescaling $\tilde{\mathbf Q}=\operatorname{diag}^{-1/2}(\mathbf Q)\,\mathbf Q\,\operatorname{diag}^{-1/2}(\mathbf Q)$ sets every diagonal entry to 1. **Computing the true eigendecomposition costs more than solving the problem; the *diagonal* is cheap — and the gradient magnitude is a cheap proxy for it.**

**Both Adagrad traces reproduce exactly:**

| $\eta$ | simulated | **D2L prints** |
|---|---|---|
| 0.4 | $(-2.382563,\ -0.158591)$ | **`x1: -2.382563, x2: -0.158591`** ✓ |
| 2.0 | $(-0.002295,\ -0.000000)$ | **`x1: -0.002295, x2: -0.000000`** ✓ |

> [!warning] ⚠️ THE COMPARISON D2L SETS UP AND NEVER MAKES: **at the same $\eta=0.4$, RMSProp's remaining error is 225× smaller**
> | | $x_1$ after 20 steps | distance covered from $-5$ |
> |---|---|---|
> | **Adagrad**, $\eta=0.4$ | $-2.382563$ | **52.35%** |
> | **RMSProp**, $\eta=0.4$, $\gamma=0.9$ | $-0.010599$ | **99.79%** |
>
> *(RMSProp trace also verified against D2L's printed `x1: -0.010599, x2: 0.000000`.)*
>
> **The only change is replacing the running SUM with a leaky average.** D2L prints both numbers in adjacent sections and never divides them.
>
> **Why**: with roughly constant gradient magnitude, $s_t=tg^2$, so the effective learning rate is $\eta/\sqrt t$ — $0.3162\eta$ at $t=10$, $0.01\eta$ at $t=10{,}000$. **The *sum* of steps is $2\eta\sqrt t$, which still diverges — so Adagrad never truly stops, it slows to a crawl.** RMSProp's $\mathbf s_t$ converges to the running mean square, so its step stays $O(\eta)$ forever.

**⚠️ And now D2L's exercise 12.7.2, which it poses and does not answer: what if the problem is rotated 45°?**

$$f(\mathbf x)=0.1(x_1+x_2)^2+2(x_1-x_2)^2\ \Longrightarrow\ \mathbf Q=\begin{pmatrix}4.2&-3.8\\-3.8&4.2\end{pmatrix}$$

| | eigenvalues | $\kappa$ | after **diagonal** preconditioning | $\kappa$ |
|---|---|---|---|---|
| axis-aligned $0.1x_1^2+2x_2^2$ | $(0.2,\ 4.0)$ | **20** | $(1.0,\ 1.0)$ | **1** |
| **rotated 45°** | $(0.4,\ 8.0)$ | **20** | $(0.095238,\ 1.904762)$ | **20** |

> [!warning] ⚠️ SAME PROBLEM, SAME $\kappa=20$, ROTATED — AND DIAGONAL PRECONDITIONING BUYS EXACTLY NOTHING
> $\kappa$: **20 → 1** axis-aligned, **20 → 20** rotated.
>
> ⇒ ***every diagonal adaptive method — Adagrad, RMSProp, Adadelta, Adam — is a bet that the problem's curvature is roughly axis-aligned in the chosen parametrization.*** **Nothing in the algorithm checks that bet, and nothing warns you when it fails.**
>
> **Gerschgorin gives the general answer** (D2L's exercises 12.7.3–4, also unanswered): after preconditioning every diagonal entry is 1, so every eigenvalue lies within $R$ of 1 where $R$ is the largest off-diagonal row sum, giving $\kappa\le\frac{1+R}{1-R}$. Here $R=0.904762$, the disc is $[0.095238,\ 1.904762]$ — **exactly the true eigenvalues, so the bound is tight** — and the bound $\frac{1+R}{1-R}=20.0000$ **equals the true $\kappa$.** ⇒ **diagonal preconditioning helps precisely to the extent the matrix is diagonally dominant.**

### 20. RMSProp and Adadelta

**RMSProp** (Tieleman & Hinton 2012) — Adagrad with a leaky average, decoupling the schedule from the per-coordinate scale:

$$\mathbf s_t\leftarrow\gamma\mathbf s_{t-1}+(1-\gamma)\mathbf g_t^2,\qquad \mathbf x_t\leftarrow\mathbf x_{t-1}-\frac{\eta}{\sqrt{\mathbf s_t+\epsilon}}\odot\mathbf g_t$$

**Adadelta** (Zeiler 2012) — two states, and **no learning rate at all**: the numerator is the leaky average of the squared *updates*, so the algorithm calibrates its step by the size of its own recent steps.

$$\mathbf s_t=\rho\mathbf s_{t-1}+(1-\rho)\mathbf g_t^2,\quad \mathbf g'_t=\frac{\sqrt{\Delta\mathbf x_{t-1}+\epsilon}}{\sqrt{\mathbf s_t+\epsilon}}\odot\mathbf g_t,\quad \Delta\mathbf x_t=\rho\Delta\mathbf x_{t-1}+(1-\rho)\mathbf g_t'^2$$

> [!warning] ⚠️ D2L calls $\frac{1}{1-\gamma}$ a "half-life", and it is not — the three numbers are different
> For weight $(1-\gamma)\gamma^t$ on lag $t$:
>
> | $\gamma$ | effective sample size $\frac1{1-\gamma}$ | mean lag $\frac{\gamma}{1-\gamma}$ | **true half-life $\frac{\ln 0.5}{\ln\gamma}$** |
> |---|---|---|---|
> | 0.5 | 2.00 | 1.00 | **1.00** |
> | **0.9** | **10.00** | 9.00 | **6.58** |
> | 0.95 | 20.00 | 19.00 | 13.51 |
> | 0.999 | 1000.00 | 999.00 | 692.80 |
>
> **D2L §12.9: "Choosing $\rho=0.9$ amounts to a half-life time of 10."** The true half-life is **6.5788**; 10 is the effective sample size and 9 is the mean lag. **Cumulative weight after 10 lags is $1-0.9^{10}=65.1\%$, not 50%.**
>
> ⚠️ **DECLINED as an erratum** under the vault's rule 4 — this is loose terminology for a correctly computed quantity, and "half-life" is used informally for a time constant in several literatures. **Recorded as a reading hazard: when a source says "half-life" of an exponential average, check which of the three numbers it means.**

### 21. ⚠️ Adam — and the bias correction that runs the WRONG way

Adam (Kingma & Ba 2014) is momentum **and** RMSProp:

$$\mathbf v_t\leftarrow\beta_1\mathbf v_{t-1}+(1-\beta_1)\mathbf g_t,\qquad \mathbf s_t\leftarrow\beta_2\mathbf s_{t-1}+(1-\beta_2)\mathbf g_t^2$$
$$\hat{\mathbf v}_t=\frac{\mathbf v_t}{1-\beta_1^t},\quad \hat{\mathbf s}_t=\frac{\mathbf s_t}{1-\beta_2^t},\quad \mathbf g'_t=\frac{\eta\,\hat{\mathbf v}_t}{\sqrt{\hat{\mathbf s}_t}+\epsilon},\quad \mathbf x_t\leftarrow\mathbf x_{t-1}-\mathbf g'_t$$

with $\beta_1=0.9$, $\beta_2=0.999$ — **so the variance estimate moves far more slowly than the momentum term.**

> [!warning] ⚠️ D2L: "if we initialize $v_0=s_0=0$ we have a significant amount of bias initially **towards smaller values**"
> **Each state is biased small. The step is their RATIO, and the ratio is biased LARGE.** With a constant gradient $g$:
>
> $$\frac{\text{uncorrected step}}{\text{corrected step}}=\frac{1-\beta_1^t}{\sqrt{1-\beta_2^t}}$$
>
> | step $t$ | uncorrected step is this many times **too large** |
> |---|---|
> | 1 | **3.1623×** |
> | 3 | 4.9502× |
> | 10 | 6.5279× |
> | **12** | **6.5685× ← PEAK** |
> | 50 | 4.5037× |
> | 100 | 3.2408× |
> | 1,000 | 1.2576× |
> | **3,925** | **within 1% of correct** |
>
> ⇒ **the uncorrected step is NEVER too small.** It starts $3.1623\times=\frac{1-\beta_1}{\sqrt{1-\beta_2}}$ too large, peaks at **6.5685×** at step 12, and needs **3,925 steps** to come within 1%.
>
> **The two biases do not cancel because they enter at different powers:** $\mathbf v$ is biased by $(1-\beta_1^t)$ and $\mathbf s$ by $(1-\beta_2^t)$, and the step divides by $\sqrt{\mathbf s}$. **With $\beta_2=0.999$, $\mathbf s$ is the slower and more biased of the two by far.**
>
> ⇒ ***bias correction is not a cosmetic first-few-steps fix; it suppresses a 6.6× overshoot for thousands of steps.*** *And this is the vault's "accurate statement that means something other than it appears" pattern again — D2L's sentence about the states is true and its implication about the step is backwards.*

### 22. ⚠️ Adam's real property: the step is bounded, and D2L never says it

With bias correction and a constant gradient, $\hat{\mathbf v}_t=g$ and $\hat{\mathbf s}_t=g^2$, so

$$\text{step}=\frac{\eta g}{|g|+\epsilon}=\eta\,\mathrm{sign}(g)\quad\textbf{independent of }|g|$$

| gradient $g$ | SGD step ($\eta=0.01$) | **Adam step ($\eta=0.01$)** |
|---|---|---|
| $10^{-4}$ | $1.00\times10^{-6}$ | **0.009901** |
| $10^{-2}$ | $1.00\times10^{-4}$ | 0.009999 |
| $1$ | $1.00\times10^{-2}$ | 0.010000 |
| $10^{2}$ | $1.00\times10^{0}$ | 0.010000 |
| $10^{4}$ | $1.00\times10^{2}$ | **0.010000** |

> [!warning] ⚠️ **ADAM IS INVARIANT TO RESCALING THE LOSS. SGD IS NOT.**
> Replace $f$ by $cf$: then $\mathbf g\to c\mathbf g$, $\mathbf v\to c\mathbf v$, $\mathbf s\to c^2\mathbf s$, so $\hat{\mathbf v}/\sqrt{\hat{\mathbf s}}$ is **unchanged**. SGD's step scales by $c$.
>
> **Verified**: minimizing $f(x)=cx^2$ from $x_0=1$, $\eta=0.01$, 200 steps, over **six orders of magnitude of curvature** $c\in[10^{-3},10^{3}]$ — Adam lands at $0.01557351$, $0.01557249$, $0.01557249$, $0.01557248$, $0.01557248$. **Total spread $1.02\times10^{-6}$.** SGD over the same range gives $0.996008$ (barely moved), $0.0175879$, and $5.63\times10^{255}$ (**divergent**, since $\eta\cdot2c=20>2$).
>
> ⇒ ***THIS is why an Adam learning rate transfers between problems and an SGD one does not*** — not speed, not adaptivity in the abstract. **A bounded step also caps the damage from one exploding minibatch to $\eta$ per coordinate.**
>
> **Sanity check:** a bounded-step optimizer travels at most $200\times0.01=2.00$ from $x_0=1$ in 200 steps, and it lands at $0.015572$ — consistent. ✓

**Yogi** (Zaheer et al. 2018) fixes Adam's known non-convergence. Rewriting Adam's second moment as $\mathbf s_t\leftarrow\mathbf s_{t-1}+(1-\beta_2)(\mathbf g_t^2-\mathbf s_{t-1})$ shows that when $\mathbf g_t^2$ has high variance, **$\mathbf s_t$ forgets its past too quickly.** Yogi replaces the increment with $(1-\beta_2)\mathbf g_t^2\odot\mathrm{sgn}(\mathbf g_t^2-\mathbf s_{t-1})$, so **the update's magnitude no longer depends on the size of the deviation.**

### 23. ⚠️ THE THIRTEEN PRINTED RUNS OF D2L CH. 12, IN ONE TABLE

Every run below is on **the same problem** (airfoil regression, batch size 10). D2L prints them across **five sections, thirty book-pages apart, and never assembles them.**

| section | hyperparameters | **loss** | **sec/epoch** |
|---|---|---|---|
| 12.6 momentum, scratch | lr 0.02, m 0.5 | 0.246 | 0.195 |
| 12.6 momentum, scratch | lr 0.01, m 0.9 | **0.254** | 0.146 |
| 12.6 momentum, scratch | lr 0.005, m 0.9 | 0.247 | 0.152 |
| 12.6 momentum, concise | lr 0.005, m 0.9 | 0.247 | **0.142** |
| 12.7 Adagrad, scratch | lr 0.1 | 0.244 | **0.232** |
| 12.7 Adagrad, concise | lr 0.1 | **0.242** | 0.155 |
| 12.8 RMSProp, scratch | lr 0.01, γ 0.9 | 0.243 | 0.177 |
| 12.8 RMSProp, concise | lr 0.01, α 0.9 | 0.243 | **0.138** |
| 12.9 Adadelta, scratch | ρ 0.9 | 0.244 | 0.221 |
| 12.9 Adadelta, concise | ρ 0.9 | 0.243 | 0.164 |
| 12.10 Adam, scratch | lr 0.01 | 0.246 | 0.224 |
| 12.10 Adam, concise | lr 0.01 | 0.243 | 0.182 |
| 12.10 Yogi, scratch | lr 0.01 | 0.245 | 0.207 |

| | |
|---|---|
| loss | min 0.242, max 0.254 — **spread 4.96% of the minimum**, sd 1.28% of the mean |
| **sec/epoch** | min 0.138, max 0.232 — **spread 68.1%**, sd 18.5% of the mean |

> [!warning] ⚠️ THE OPTIMIZER CHOICE MOVES THE LOSS BY 4.96% AND THE CLOCK BY 68%
> **Thirteen runs of five "increasingly sophisticated" algorithms, and every final loss lies in $[0.242,\ 0.254]$** — a band narrower than the spread produced by *retuning momentum's learning rate alone* (0.246 → 0.254 → 0.247, §18).
>
> ⚠️ **THE HONEST READING, and it is the important one: this does not show the optimizers are equivalent. It shows the BENCHMARK cannot tell them apart.** The problem is a small, convex, dense five-feature linear regression — **no sparsity, no severe ill-conditioning, no nonconvexity.** Adaptive methods are built for exactly the conditions this problem does not have. **§19 argues Adagrad's case from *sparse features* and then demonstrates it on a dense regression.**
>
> ⇒ ***a demonstration that cannot distinguish the thing it demonstrates is not evidence, and it is worth checking whether any benchmark you are shown could have produced a different answer.***

**From-scratch versus framework, matched pairs:**

| | scratch | concise | ratio |
|---|---|---|---|
| momentum | 0.152 | 0.142 | 1.070× |
| Adagrad | 0.232 | 0.155 | **1.497×** |
| RMSProp | 0.177 | 0.138 | 1.283× |
| Adadelta | 0.221 | 0.164 | 1.348× |
| Adam | 0.224 | 0.182 | 1.231× |

**Mean overhead of the hand-written implementation: 1.286× (median 1.283×).** ⇒ *the framework's fused optimizer kernels are worth ~29%, and D2L never states it — the same "divide the adjacent figures" move that gave [[02 - Linear Regression|ch. 02]]'s 93.23× vectorization result.*

### 24. Learning-rate scheduling — the four aspects

D2L's own list, worth keeping as a checklist:

1. **Magnitude** — too large diverges (§16 made the bound exact: $\eta<2/\lambda_{\max}$), too small wastes time.
2. **Rate of decay** — must decay, but for nonconvex problems **more slowly than the $O(t^{-1/2})$ that suits convex ones.** *(This is precisely §19's complaint about Adagrad.)*
3. **Warmup** — the initial parameters are random, so **the first update directions are close to meaningless**; large early steps are wasted or harmful. ⇒ *and §21 shows Adam's bias correction is doing part of this job already, suppressing a 6.6× overshoot.*
4. **Cyclic schedules and path averaging** (Izmailov et al. 2018) — beyond scope here.

## ✏️ Exercises

> [!example]- Exercise 1 — the linear collapse, and the rank ceiling
> **(a)** For $\mathbf W^{(1)}=\begin{pmatrix}1&2\\0&1\\3&-1\end{pmatrix}$, $\mathbf b^{(1)}=(1,-1)$, $\mathbf W^{(2)}=\begin{pmatrix}2&0&1\\1&1&-1\end{pmatrix}$, $\mathbf b^{(2)}=(0.5,0.5,0.5)$ (no activation), find the single equivalent layer and verify it at $\mathbf x=(1,2,3)$.
> **(b)** What is the rank of the collapsed map, and what does that cost?
> **(c)** Count parameters both ways.
>
> ---
> **(a)** $\mathbf W=\mathbf W^{(1)}\mathbf W^{(2)}=\begin{pmatrix}4&2&-1\\1&1&-1\\5&-1&4\end{pmatrix}$ and $\mathbf b=\mathbf b^{(1)}\mathbf W^{(2)}+\mathbf b^{(2)}=(1.5,\,-0.5,\,2.5)$.
>
> At $\mathbf x=(1,2,3)$: two layers give $(\mathbf x\mathbf W^{(1)}+\mathbf b^{(1)})\mathbf W^{(2)}+\mathbf b^{(2)}=(22.5,\ 0.5,\ 11.5)$; one layer gives $\mathbf x\mathbf W+\mathbf b=(22.5,\ 0.5,\ 11.5)$. **Identical.** ✓
>
> **(b)** $\operatorname{rank}\mathbf W=2$, because $\operatorname{rank}(\mathbf A\mathbf B)\le\min(\operatorname{rank}\mathbf A,\operatorname{rank}\mathbf B)\le 2$ here. **A single $3\times3$ layer reaches rank 3; this network never can.** The hidden width is a hard ceiling.
>
> **(c)** Two layers: $3\cdot2+2+2\cdot3+3=\mathbf{17}$. One layer: $3\cdot3+3=\mathbf{12}$.
>
> ⚠️ **17 parameters to be strictly *less* general than 12.** That is D2L's unanswered "give an example where it actively reduces it": **any bottleneck narrower than $\min(d,q)$ does it.** ⇒ *parameter count is not capacity — the same lesson as [[02 - Linear Regression|ch. 02]]'s 200-parameter fit pinned inside a 20-dimensional span.*

> [!example]- Exercise 2 — how deep can a sigmoid network be?
> **(a)** Give the best-case bound on how much an $L$-layer sigmoid MLP damps the backward signal.
> **(b)** At what depth does that fall below `float32` epsilon ($1.1921\times10^{-7}$)? Below `float64` epsilon ($2.2204\times10^{-16}$)?
> **(c)** Why can't a larger learning rate fix it?
> **(d)** What is the corresponding factor for ReLU?
>
> ---
> **(a)** Backpropagation multiplies by $\phi'(z)$ once per layer, and $\max_z\sigma'(z)=\sigma'(0)=\tfrac14$ exactly. So the damping is **at most $0.25^L$** — and this is optimistic, since it assumes every pre-activation sits at 0 and ignores the weight matrices. A realistic figure with $z\sim\mathcal N(0,1)$ is $\mathbb E[\sigma'(z)]=0.206643$ per layer.
>
> **(b)** $L=\dfrac{\ln\varepsilon}{\ln0.25}$:
>
> | | $\varepsilon$ | $L$ | |
> |---|---|---|---|
> | `float32` | $1.1921\times10^{-7}$ | **11.50** | so **12 layers** |
> | `float64` | $2.2204\times10^{-16}$ | **26.00** | so **26 layers** |
>
> Realistically (using 0.206643): **10.11 layers** in `float32`.
>
> **(c)** Compensating for $L$ layers requires multiplying $\eta$ by $4^L$: $16\times$ at $L=2$, $1.024\times10^3$ at $L=5$, $1.049\times10^6$ at $L=10$. **But the shallow layers do not need that multiple — they would diverge instantly.** ⇒ **the deep and shallow layers demand incompatible learning rates, and there is only one $\eta$.** *(That is also §16's tension, in a different guise: one step size for eigendirections that need different ones.)*
>
> **(d)** ReLU's derivative is **exactly 1** on the active half-line, so the factor is $1^L=1$ for every depth. The *active fraction* shrinks (some units are dead on a given input) but the surviving paths are undamped. **That is the entire mathematical content of "ReLU mitigates vanishing gradients."**

> [!example]- Exercise 3 — dropout: the mean, the variance, and the sample
> **(a)** Derive $\operatorname{Var}[h']$ and the coefficient of variation.
> **(b)** Evaluate at $p=0.2,\ 0.5,\ 0.8$. What is special about $p=0.5$?
> **(c)** D2L's printed $p=0.5$ example on $\mathbf X=0,1,\dots,15$: how many units survived, and how far is the sample mean from $\mathbb E[h']$?
> **(d)** Why is a lower $p$ appropriate near the input?
>
> ---
> **(a)** $\mathbb E[h']=(1-p)\frac{h}{1-p}=h$. $\mathbb E[h'^2]=(1-p)\frac{h^2}{(1-p)^2}=\frac{h^2}{1-p}$. Hence
> $$\operatorname{Var}[h']=\frac{h^2}{1-p}-h^2=h^2\frac{p}{1-p},\qquad \mathrm{CV}=\sqrt{\frac{p}{1-p}}$$
>
> **(b)** $p=0.2$: variance $0.25h^2$, CV $0.5$. $p=0.8$: variance $4h^2$, CV $2$. **$p=0.5$: variance $=h^2$ exactly, $\mathrm{CV}=1.0000$** — ⚠️ **the noise's standard deviation equals the activation it replaces.** *(And CV diverges as $p\to1$: 3 at $p=0.9$, 4.36 at $p=0.95$.)*
>
> **(c)** Every printed non-zero entry is exactly $2\times$ its original (checked for all of them), so the survivors are readable off the printout: **11 of 16 = 68.75%**, against a nominal 50%. Under $\mathrm{Bin}(16,0.5)$, $P(\ge11)=0.1051$ — **ordinary, not anomalous.**
>
> Sample mean $=142/16=\mathbf{8.8750}$ against $\mathbb E=7.5000$: **+18.33%**, or $+0.62$ sd (the sd of that mean is $\sqrt{\sum X^2\cdot\frac{p}{1-p}}/16=2.2009$).
>
> ⚠️ **Unbiasedness is a statement about an average over draws; the network sees ONE draw per step.**
>
> **(d)** Noise injected at layer 1 passes through every subsequent layer; noise injected at the last hidden layer does not. **With CV = 1 at $p=0.5$ that is a large perturbation to propagate.** D2L gives this advice and never gives this reason.

> [!example]- Exercise 4 — reproduce D2L's divergence, then beat it
> On $f(\mathbf x)=0.1x_1^2+2x_2^2$ from $\mathbf x_0=(-5,-2)$:
> **(a)** Write gradient descent in closed form and predict $\mathbf x_{20}$ at $\eta=0.4$ and $\eta=0.6$.
> **(b)** Give the exact stability bound.
> **(c)** With the optimal $\eta$, how many steps for a 100-fold error reduction? With optimal momentum?
> **(d)** How does the answer scale with $\kappa$?
>
> ---
> **(a)** The Hessian is $\operatorname{diag}(0.2,4)$, so the update decouples: $x_t=(1-\eta\lambda)^tx_0$ per coordinate.
>
> | $\eta$ | $x_1=(1-0.2\eta)^{20}(-5)$ | $x_2=(1-4\eta)^{20}(-2)$ |
> |---|---|---|
> | 0.4 | $(0.92)^{20}(-5)=\mathbf{-0.943467}$ | $(-0.6)^{20}(-2)=\mathbf{-0.000073}$ |
> | 0.6 | $(0.88)^{20}(-5)=\mathbf{-0.387814}$ | $(-1.4)^{20}(-2)=\mathbf{-1673.365109}$ |
>
> ⚠️ **These are D2L's printed traces, digit for digit, in both coordinates at both learning rates** — and $\mathbf x_0=(-5,-2)$ is nowhere in the text; it is *recovered* by demanding the match. **$1.4^{20}=836.6826$; $\times2=1673.365109$.**
>
> **(b)** $|1-\eta\lambda|<1$ for both eigenvalues $\iff \eta<2/\lambda_{\max}=\mathbf{0.5}$. $\eta=0.4$ is 80% of the bound; **$\eta=0.6$ is 120% and diverges at rate $|1-2.4|=1.4$ per step.** D2L calls 0.4 → 0.6 "a slight increase in learning rate" and it crosses a knife-edge.
>
> **(c)** $\kappa=4/0.2=20$.
> - GD: $\eta^*=\frac{2}{\lambda_{\min}+\lambda_{\max}}=0.476190$, rate $\frac{\kappa-1}{\kappa+1}=0.904762$, steps $=\frac{\ln0.01}{\ln0.904762}=\mathbf{46.01}$.
> - Momentum: $\beta^*=\left(\frac{\sqrt{20}-1}{\sqrt{20}+1}\right)^2=0.402605$, rate $\frac{\sqrt{20}-1}{\sqrt{20}+1}=0.634512$, steps $=\mathbf{10.12}$.
> - **Speedup $\mathbf{4.55\times}$.**
>
> **(d)** $O(\kappa)$ versus $O(\sqrt\kappa)$: at $\kappa=100$, 230.3 vs 22.9 (**10.03×**); at $\kappa=10^4$, 23,025.9 vs 230.3 (**exactly 100×**, since $\sqrt{10^4}=100$).
>
> ⚠️ **Momentum's advantage grows without bound as the problem worsens and is nil when $\kappa=1$.** ⇒ *if momentum is not helping, the problem is already well-conditioned — check that before tuning $\beta$.* *(See [[Optimization/contents/05 - Gradient Methods|Optimization ch. 05]].)*

> [!example]- Exercise 5 — Adam: what the bias correction does, and what makes the learning rate portable
> **(a)** With a constant gradient, what is the ratio of the uncorrected step to the corrected one at step $t$? Evaluate at $t=1$, find its maximum, and find when it is within 1%.
> **(b)** D2L says the initialization biases the states "towards smaller values." Is the *step* too small?
> **(c)** Show Adam's step is bounded, and that Adam is invariant to rescaling the loss.
> **(d)** Verify (c) numerically.
>
> ---
> **(a)** With $\mathbf g_t\equiv g$: $v_t=(1-\beta_1^t)g$ and $s_t=(1-\beta_2^t)g^2$, so
> $$\frac{\text{uncorrected}}{\text{corrected}}=\frac{v_t/\sqrt{s_t}}{\hat v_t/\sqrt{\hat s_t}}=\frac{1-\beta_1^t}{\sqrt{1-\beta_2^t}}$$
> At $t=1$: $\frac{0.1}{\sqrt{0.001}}=\mathbf{3.1623}$. **Maximum $\mathbf{6.5685}$ at $t=12$.** Within 1% of 1 only at $t=\mathbf{3{,}925}$.
>
> **(b)** ⚠️ **No — it is too LARGE, at every $t$.** Each state is indeed biased small, but the step is $v/\sqrt s$ and the two biases enter at different powers: $\mathbf v$ carries $(1-\beta_1^t)$ while $\mathbf s$ carries $(1-\beta_2^t)$ *under a square root*, and $\beta_2=0.999$ makes $\mathbf s$ far the more biased. **The ratio never drops below 1.** ⇒ *bias correction suppresses a peak 6.6× overshoot for thousands of steps, not a "slow startup".*
>
> **(c)** With $\hat v_t=g$, $\hat s_t=g^2$: step $=\frac{\eta g}{|g|+\epsilon}=\eta\,\mathrm{sign}(g)$, **independent of $|g|$.** Replacing $f$ by $cf$ sends $g\to cg$, $v\to cv$, $s\to c^2s$, so $\hat v/\sqrt{\hat s}$ is unchanged — **Adam's trajectory does not move.** SGD's step is $\eta cg$ and scales by $c$.
>
> **(d)** Minimizing $f(x)=cx^2$ from $x_0=1$, $\eta=0.01$, 200 steps:
>
> | $c$ | **Adam** $x_{200}$ | SGD $x_{200}$ |
> |---|---|---|
> | $10^{-3}$ | **0.01557351** | 0.996008 (barely moved) |
> | $10^{-1}$ | 0.01557249 | — |
> | $1$ | 0.01557249 | 0.0175879 |
> | $10^{1}$ | 0.01557248 | — |
> | $10^{3}$ | **0.01557248** | $5.63\times10^{255}$ (**divergent**) |
>
> **Adam's spread across six orders of magnitude of curvature is $1.02\times10^{-6}$.** SGD diverges at $c=10^3$ (since $\eta\cdot2c=20>2$, exactly exercise 4(b)'s bound) and barely moves at $c=10^{-3}$.
>
> ⇒ ***that, and not speed, is why an Adam learning rate transfers between problems.*** **Sanity check on the bound: 200 steps of size $\le0.01$ can travel at most 2.00 from $x_0=1$, and it lands at 0.0156.** ✓

## 📝 Summary

- **A hidden layer without a nonlinearity is worse than useless**: the network collapses to $\mathbf X\mathbf W^{(1)}\mathbf W^{(2)}+\mathbf b$, and the hidden width caps the rank. **A $3\to2\to3$ linear net uses 17 parameters to be strictly less general than a 12-parameter $3\to3$ layer.**
- **tanh and sigmoid parametrize the *same function class*** — $\tanh x=2\,\mathrm{sigmoid}(2x)-1$, and an affine bias absorbs the shift. The difference is entirely about optimization. **Swish and GELU are non-monotone** (Swish's minimum is $-0.278465$ at $x=-1.278465$).
- **Backpropagation is the chain rule in reverse topological order.** Each weight gradient is an outer product of a backward vector and a stored forward activation — which is *why* training costs so much more memory than prediction: **5.64× for D2L's own MLP; at 1 B parameters, Adam's state alone is 7.45 GB of a 14.90 GB bill.**
- **⚠️ Every sigmoid layer damps the gradient by at most 0.25**, so a sigmoid MLP loses its gradient to `float32` underflow at **11.50 layers** best case, **10.11** realistically. **ReLU's factor is exactly 1.** Compensating with $\eta$ needs $4^L$, which diverges the shallow layers. **A second, independent explanation for [[01 - Introduction to Deep Learning|ch. 01]]'s neural-network winter.**
- **⚠️ D2L's "the matrix product explodes" is $\lambda_1=\tfrac12[\ln2+\psi(n/2)]=0.557966$**, predicting $10^{24.23}$ against a printed $10^{25.08}$ — **$z=+0.28$ across 400 replications, whose range spans ten orders of magnitude.**
- **⚠️ Xavier preserves the MEAN squared norm exactly at every width and not the typical one**: median 0.842 at $n=4$, $\mathbb E[\ln]<0$, typical squared norm $\times1.58\times10^{-6}$ after 50 layers while the mean is still 1.00. **The vault's "the average is fine and the joint behaviour is everything" result in a fifth setting.**
- **⚠️ Dropout's variance is $h^2\frac{p}{1-p}$, so at $p=0.5$ the noise's sd equals the activation exactly (CV = 1.0000).** That is the missing reason for using a lower $p$ near the input. **And D2L's printed $p=0.5$ example kept 11 of 16 units and runs +18.33% above the mean it preserves.**
- **⚠️ Gradient descent needs $O(\kappa)$ steps and momentum $O(\sqrt\kappa)$** — 46.01 vs 10.12 at D2L's $\kappa=20$, exactly 100× at $\kappa=10^4$. **Stability requires $\eta<2/\lambda_{\max}$, and all seven of D2L's printed traces reproduce from $\mathbf x_0=(-5,-2)$.**
- **⚠️ $\eta$ and $\beta$ are one knob, not two.** D2L's "slight reduction" of $\eta$ from 0.02 to 0.01 while raising $\beta$ from 0.5 to 0.9 was a **2.5× increase** in $\eta/(1-\beta)$ — and its own printed loss rose 0.246 → 0.254.
- **Adagrad's $\mathbf s_t$ grows without bound** ($\eta/\sqrt t$, total travel $2\eta\sqrt t$); the leaky-average fix leaves **RMSProp 225× closer after the same 20 steps at the same $\eta$.** **⚠️ But diagonal preconditioning takes $\kappa$ 20 → 1 axis-aligned and 20 → 20 rotated 45°: every adaptive method bets on axis alignment and nothing checks the bet.**
- **⚠️ Adam's uncorrected step is never too small** — 3.1623× too large at $t=1$, peaking at **6.5685× at $t=12$**, within 1% only at $t=3{,}925$. **And its corrected step is bounded by $\eta$ regardless of gradient magnitude, making Adam invariant to rescaling the loss** (spread $1.02\times10^{-6}$ over $c\in[10^{-3},10^{3}]$, where SGD diverges at one end and stalls at the other).
- **⚠️ All thirteen of D2L's printed ch. 12 runs land in a 4.96% loss band while wall-clock varies 68%** — because the benchmark is a dense, convex, five-feature regression that **cannot distinguish the algorithms it is demonstrating.**

## ⚠️ Important Notes

1. **⚠️ Never transcribe a formula from this PDF.** The cipher deletes $-$, $\leftarrow$, $\eta$, $\lambda$, $\times$ and fraction bars, turns `,`→`;`, `|`→`j`, `∈`→`2`, `∂`→`@`, `.`→`:`, `→`→`!`, and **uses `1` for both $\infty$ and literal 1 in adjacent sentences.** Every formula above was reconstructed and checked numerically. **Worked example from this chapter**: D2L's Adagrad update extracts as `wt = wt1  pst + ϵ gt` and is $\mathbf w_t=\mathbf w_{t-1}-\frac{\eta}{\sqrt{\mathbf s_t+\epsilon}}\odot\mathbf g_t$ — a deleted minus, a deleted $\eta$, a deleted fraction bar, a deleted $\odot$, and `p` for $\sqrt{\ }$.
2. **⚠️ The gradient of a shared parameter is the SUM of its paths, not the average.** Tie a layer into three positions and its gradient is three times as large — so a tied layer effectively trains at 3× the learning rate. D2L states the addition in one clause and never draws the conclusion.
3. **⚠️ "Unbiased" and "correct" are different claims, and dropout is the cleanest example.** $\mathbb E[h']=h$ exactly; the printed realization is +18.33% off; the coefficient of variation at $p=0.5$ is 1.0000. **A network is optimized on realizations, not expectations.**
4. **⚠️ Parameter count is not capacity.** §1's $3\to2\to3$ network has more parameters and less expressive power. **The relevant quantity here is rank, and in [[02 - Linear Regression|ch. 02]] it was the span of the data.** Ask what the model *can* represent, not how many numbers it holds.
5. **⚠️ Report conditioning, never rank or invertibility.** [[03 - Logistic Regression|Ch. 03]] found this twice (a $\kappa=104$ confusion matrix amplifying noise 65.9× and still returning a valid probability vector; a full-rank design with $\kappa=312$). **§17 is the third: $\kappa$ decides the step count and $\kappa=20$ vs $\kappa=10^4$ is 46 steps vs 23,026.** Full rank tells you nothing about either.
6. **⚠️ Diagonal adaptive methods assume axis alignment and never verify it.** §19: the same problem rotated 45° has the same $\kappa$ and gains **nothing** from preconditioning. **This is a property of the parametrization, not the problem** — which is also why batch normalization and residual connections (ch. 05) help: they change the parametrization.
7. **⚠️ Raising $\beta$ raises the learning rate.** The effective step is $\eta/(1-\beta)$: 0.9 → 0.99 is a **10× increase**. §18 shows the source itself getting this wrong and its own printed loss catching it.
8. **⚠️ Adam's learning rate is not comparable to SGD's.** Adam's step is $\approx\eta$ per coordinate regardless of gradient magnitude; SGD's is $\eta\|\mathbf g\|$. **Porting $\eta=0.1$ from SGD to Adam is usually catastrophic**, and the ratio depends on the loss scale, which is exactly what Adam is invariant to.
9. **⚠️ Adam without bias correction overshoots by up to 6.57×, peaking at step 12.** If you implement an optimizer from scratch, this is the bug that produces a plausible-looking early loss spike and then "recovers" — the vault's recurring **plausible wrong answer with no error.**
10. **⚠️ Adagrad's decay is $O(t^{-1/2})$ and is right for convex problems and too aggressive for deep ones.** Its total travel $2\eta\sqrt t$ still diverges, so it never *stops* — it just becomes indistinguishable from stopping. **Diagnose it by watching the step size, not the loss.**
11. **⚠️ "Half-life" of an exponential average is ambiguous.** For $\gamma=0.9$: effective sample size 10, mean lag 9, **true half-life 6.58**, cumulative weight after 10 lags 65.1%. D2L calls 10 the half-life (§20). **Declined as an erratum; recorded as a hazard.**
12. **⚠️ Classical regularization theory does not explain deep generalization.** Networks fit random labels, so VC and Rademacher bounds are vacuous; typical weight-decay strengths do not prevent interpolation. **Early stopping is the intervention with an actual mechanism** (clean data is fitted first) and it matters **only when labels are noisy.**
13. **⚠️ A benchmark that cannot separate the methods it compares is not evidence.** §23: thirteen runs, 4.96% loss spread, 68% time spread, on a problem with none of the properties the adaptive methods target. **Before believing a comparison, ask what result would have looked different.**
14. **⚠️ Newton's method walks uphill wherever the Hessian is negative** — D2L's own run ends at $x=26.83$. Second-order information is a *scaling*, not a direction, unless the curvature is positive.
15. **⚠️ Symmetry must be broken by initialization, and SGD cannot break it.** Constant initialization makes a whole layer behave as one unit forever. **Dropout can break it; minibatch noise cannot.**
16. **Activation memory scales with batch size; parameter memory does not.** A batch-size increase that fits in your head may not fit in your GPU: §5's activations are 1.275 MB at batch 256 against 0.776 MB of weights.
17. **The `float32`/`float64` distinction is not academic here.** §8's depth ceiling is 11.50 layers in single precision and 26.00 in double — and training runs in single (or lower) precision precisely because memory is the binding constraint (§5).

> [!warning] Gaps in the source material
> **All figures are images and never extract.** D2L ch. 5, 6 and 12 are figure-heavy and this chapter is the worst case so far: **Fig. 5.1.1 (the MLP schematic), Fig. 5.3.1 (the computational graph) and Fig. 5.6.1 (before/after dropout) are label-schematics whose content the prose fully states, and they are reconstructed above.** The **activation-function plots, the derivative plots, the leaky-average weight decay curves, the `show_trace_2d` optimizer trajectories, and the learning-rate schedule curves are SHAPE figures and are lost** — *but every one of the optimizer trajectories was recovered numerically from the printed endpoint, which is stronger than the figure.* **This is the figure rule in its settled form** (both classes inside one book; the test is what the figure's content *is*).
>
> **Code listings lose their indentation** and must be re-derived from the logic, never copied. **Printed code *outputs* extract intact**, which is what made §13, §16, §19 and §23 possible.
>
> **Mathematics is reconstructed, never transcribed.** No new cipher entries were needed in this chapter; the table in this subject's `CLAUDE.md` covered every formula.
>
> **Added beyond D2L, and labelled as mine throughout:**
> - **The rank argument and the parameter count** in §1 and exercise 1 — D2L's exercise 5.1.1 asks for a case where depth reduces expressive power and gives no answer.
> - **The whole of §8** — the $0.25^L$ bound, the float32/float64 depth ceilings, the $\mathbb E[\sigma'(z)]=0.206643$ simulation, and the $4^L$ argument. D2L says only that the sigmoid's gradient "vanishes".
> - **The Lyapunov exponent $\tfrac12[\ln2+\psi(n/2)]$** in §9 (Cohen & Newman 1984; Newman 1986) with its 400-replication Monte Carlo and the critical scale $\sigma^*=0.572372$. **D2L prints one run and generalizes from it.**
> - **The mean-versus-median simulation of Xavier** in §10, and the observation that the compromise is exact only at $n_{\text{in}}=n_{\text{out}}$ (with the $1.2279\times$/$0.7016\times$ figures).
> - **$\operatorname{Var}[h']=h^2p/(1-p)$ and the CV table** in §12, and **the audit of the printed dropout realization** in §13 — D2L's exercise 5.6.3 asks for the variance and never answers it.
> - **The entire memory accounting of §5**, answering D2L's exercise 5.3.3, including the 1-billion-parameter scaling *(mixed precision, 8-bit optimizer states and ZeRO sharding are modern practice the book predates)*.
> - **The closed form $x_t=(1-\eta\lambda)^tx_0$, the recovery of $\mathbf x_0=(-5,-2)$, and the reproduction of all seven printed traces** (§16, §17, §19). D2L prints the endpoints and writes none of the algebra.
> - **The $\kappa$ vs $\sqrt\kappa$ table and the optimal $\eta^*,\beta^*$ formulas** in §17 — standard accelerated-gradient theory that D2L gestures at ("$0<\eta<2+2\beta$") and does not state.
> - **The effective-step audit of §18**, which is the source contradicting itself two paragraphs apart.
> - **The rotated-problem preconditioning result and the Gerschgorin bound** in §19 — D2L's exercises 12.7.2–12.7.4, all unanswered.
> - **The bias-correction ratio $\frac{1-\beta_1^t}{\sqrt{1-\beta_2^t}}$, its 6.5685 peak at $t=12$, and the $t=3{,}925$ figure** in §21.
> - **Adam's bounded step and scale invariance** in §22, with the $c\in[10^{-3},10^3]$ verification. **D2L lists Adam's ingredients and never states its defining property.**
> - **The thirteen-run table of §23**, including the from-scratch/framework overhead of 1.286× and the caveat about what the benchmark can and cannot show.
>
> **One discrepancy investigated and DECLINED** (§20, logged in [[00-Index]] as **D7**): D2L calls $\frac{1}{1-\rho}=10$ a "half-life" when the true half-life at $\rho=0.9$ is 6.5788. **Ruled out**: own extraction (the sentence extracts cleanly, no deleted glyphs), own arithmetic (verified three ways), and alternative convention — *"half-life" is used loosely for a time constant in several literatures, and the computed quantity itself is correct*. **Filing a false erratum against a correct source is the worse failure.**
>
> **Deliberately deferred, not omitted:** D2L §5.2 (the from-scratch and concise MLP implementations) and §5.7 (the Kaggle house-price competition) are **implementation walk-throughs**, used here only where they carry a result — the $784\to256\to10$ architecture that §5 costs out. **D2L ch. 6's File I/O and GPU sections (§6.6–6.7) are engineering** and belong with [[MLOps/contents/00-Index|MLOps]]. **D2L §12.2 (convexity) and §12.3–12.5 (gradient descent, SGD, minibatch SGD) are held by [[Optimization/contents/02 - Convex Sets and Convex Functions|Optimization ch. 02]], [[Optimization/contents/05 - Gradient Methods|ch. 05]] and [[02 - Linear Regression|this subject's ch. 02]]** — only §12.1's landscape, §12.3.3's Newton discussion and the accelerated/adaptive methods from §12.6 on are developed here. **§12.11's schedule *implementations* are summarized rather than reproduced;** the four design aspects are in §24.
>
> **Left as the source states it:** all citations (Cybenko 1989, Micchelli 1984, Glorot & Bengio 2010, Nair & Hinton 2010, Srivastava et al. 2014, Bishop 1995, Duchi et al. 2011, Tieleman & Hinton 2012, Zeiler 2012, Kingma & Ba 2014, Reddi et al. 2019, Zaheer et al. 2018, Zhang et al. 2021, Nakkiran et al. 2021, Jacot et al. 2018, Rolnick et al. 2017, Garg et al. 2021, Xiao et al. 2018, Polyak 1964, Nesterov 2018); the claim that Xiao et al. trained 10,000-layer networks; the double-descent phenomenon, which is asserted and not demonstrated here; and the neural-tangent-kernel result, which is quoted without derivation.

**Previous:** [[03 - Logistic Regression]] · **Next:** [[05 - Convolutional Neural Network]]
