---
subject: Deep Learning
chapter: 4
tags: [ds, deep-learning, mlp, backpropagation, activation-functions, initialization, dropout, optimizers, adam, momentum, conditioning]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 5 (Multilayer Perceptrons), ch. 6 (Builders' Guide), ch. 12 (Optimization Algorithms)"
---

# Neural Network

This note merges three D2L chapters: ch. 5 (MLPs, backpropagation, numerical stability, dropout), ch. 6 (parameter management) and ch. 12 (optimizers through Adam). The syllabus has no separate optimizer topic, so ch. 12 lives here (scope call recorded in [[00-Index]]).

## 📘 Main Knowledge

### 1. A hidden layer needs a nonlinearity

One hidden layer of $h$ units, minibatch $\mathbf X\in\mathbb R^{n\times d}$:
$$\mathbf H=\mathbf X\mathbf W^{(1)}+\mathbf b^{(1)},\qquad \mathbf O=\mathbf H\mathbf W^{(2)}+\mathbf b^{(2)}$$

Without an activation this collapses to one affine layer:
$$\mathbf O=\mathbf X\,\mathbf W^{(1)}\mathbf W^{(2)}+\left(\mathbf b^{(1)}\mathbf W^{(2)}+\mathbf b^{(2)}\right)$$

It can even lose expressive power: $\operatorname{rank}(\mathbf W^{(1)}\mathbf W^{(2)})\le\min(d,h,q)$, so a narrow hidden layer caps the rank (D2L ex. 5.1.1; see [[Linear Algebra/contents/07 - Linear Transformations|Linear Algebra ch. 07]]).

| architecture | parameters | max rank |
|---|---|---|
| one $10\times10$ layer | 110 | 10 |
| $10\to10\to10$ linear | 200 | 10 |
| $10\to5\to10$ linear | 100 | 5 |
| $10\to2\to10$ linear | 40 | 2 |

Exercise 1 gives a $3\to2\to3$ example: 17 parameters, rank 2, strictly less general than a 12-parameter $3\to3$ layer. Parameter count is not capacity.

The fix is an elementwise activation: $\mathbf H=\sigma(\mathbf X\mathbf W^{(1)}+\mathbf b^{(1)})$.

D2L's motivation: linear models are monotone. Income → repayment is plausibly monotone; body temperature → health is not (risk rises on both sides of 37 °C); and inverting an image keeps its category, which no linear model can express.

### 2. Activation functions

| function | definition | derivative | range |
|---|---|---|---|
| ReLU | $\max(x,0)$ | $\mathbb 1[x>0]$ (0 at $x=0$ by convention) | $[0,\infty)$ |
| pReLU | $\max(0,x)+\alpha\min(0,x)$ | 1 if $x>0$, $\alpha$ if $x<0$ | $\mathbb R$ |
| sigmoid | $1/(1+e^{-x})$ | $\sigma(x)(1-\sigma(x))$, max 0.25 at 0 | $(0,1)$ |
| tanh | $(1-e^{-2x})/(1+e^{-2x})$ | $1-\tanh^2 x$, max 1 at 0 | $(-1,1)$ |
| GELU | $x\,\Phi(x)$ | | $\mathbb R$ |
| Swish | $x\,\sigma(x)$ | $\sigma(x)[1+x(1-\sigma(x))]$ | $\mathbb R$ |

Two facts D2L does not state:

- $\tanh(x)=2\,\mathrm{sigmoid}(2x)-1$ (D2L ex. 5.1.5, verified). A tanh unit is a sigmoid unit with rescaled weights and a shifted bias, so the two give the same function class. They differ only in how easy they are to optimize.
- Swish is not monotone: its minimum is $-0.278465$ at $x=-1.278465$ (GELU is similar). So the sign of a weight no longer fixes the direction of an effect.

ReLU's main advantage is its derivative: 0 or 1, never a damping factor in between (§8).

### 3. Universal approximation

One hidden layer with enough units can approximate any continuous function (Cybenko 1989, Micchelli 1984). D2L's caveats: being able to represent a function is different from learning it; kernel methods are also universal; and deep networks often represent functions far more compactly than wide shallow ones.

### 4. Forward and backward propagation

One example, no hidden bias, $\ell_2$ penalty:
$$\mathbf z=\mathbf W^{(1)}\mathbf x,\quad \mathbf h=\phi(\mathbf z),\quad \mathbf o=\mathbf W^{(2)}\mathbf h,\quad L=l(\mathbf o,y),\quad s=\tfrac{\lambda}{2}\left(\|\mathbf W^{(1)}\|_F^2+\|\mathbf W^{(2)}\|_F^2\right),\quad J=L+s$$

Backpropagation applies the chain rule in reverse order:
$$\frac{\partial J}{\partial \mathbf W^{(2)}}=\frac{\partial J}{\partial\mathbf o}\mathbf h^\top+\lambda\mathbf W^{(2)},\qquad \frac{\partial J}{\partial\mathbf h}=\mathbf W^{(2)\top}\frac{\partial J}{\partial\mathbf o}$$
$$\frac{\partial J}{\partial\mathbf z}=\frac{\partial J}{\partial\mathbf h}\odot\phi'(\mathbf z),\qquad \frac{\partial J}{\partial \mathbf W^{(1)}}=\frac{\partial J}{\partial\mathbf z}\mathbf x^\top+\lambda\mathbf W^{(1)}$$

- Each weight gradient is an outer product of a backward vector and a forward activation, so activations must be stored until the backward pass uses them.
- The activation enters the backward pass only through the factor $\phi'(\mathbf z)$, once per layer (§8).
- Weight decay adds $\lambda\mathbf W$ directly, even when the data gradient is zero.

Forward and backward passes alternate: the forward pass uses the current weights, and the backward pass needs the stored forward values.

### 5. Memory cost of training

D2L says training needs "significantly more memory" than prediction (ex. 5.3.3). For its MLP ($784\to256\to10$, batch 256, float32):

$$\text{parameters}=784\cdot256+256+256\cdot10+10=203{,}530$$

| item | floats | MB |
|---|---|---|
| weights | 203,530 | 0.776 |
| gradients | 203,530 | 0.776 |
| activations $\mathbf X,\mathbf Z^{(1)},\mathbf H,\mathbf O$ | 334,336 | 1.275 |

| optimizer | extra state per parameter | parameter memory | vs SGD |
|---|---|---|---|
| SGD | 0 | 1.553 MB | 1.00× |
| momentum | 1 | 2.329 MB | 1.50× |
| Adagrad / RMSProp | 1 | 2.329 MB | 1.50× |
| Adadelta | 2 | 3.106 MB | 2.00× |
| Adam | 2 | 3.106 MB | 2.00× |

Training this MLP with Adam needs 5.64× the memory of prediction. For a 1-billion-parameter float32 model: weights 3.73 GB, plus gradients 7.45 GB, plus Adam state 14.90 GB, so optimizer state is half the total. (Mixed precision, 8-bit optimizer states and ZeRO sharding address this; added beyond D2L.) Activation memory grows with batch size; parameter memory does not.

### 6. Vanishing and exploding gradients

For $L$ layers the gradient at layer $l$ is a product of Jacobians:
$$\partial_{\mathbf W^{(l)}}\mathbf o=\mathbf M^{(L)}\cdots\mathbf M^{(l+1)}\,\mathbf v^{(l)},\qquad \mathbf M^{(k)}=\partial_{\mathbf h^{(k-1)}}\mathbf h^{(k)}$$

A long product of matrices whose eigenvalues are not near 1 shrinks or grows geometrically. Exploding gradients wreck the model; vanishing gradients stop learning.

### 7. Symmetry

If all hidden weights start equal, every hidden unit gets the same input and the same gradient, and they stay identical: the layer acts like one unit. Random initialization is therefore required. Dropout breaks the symmetry because it drops different units each step; plain SGD does not. (Equivalently, any minimum of a $d$-unit layer has $d!$ permutation copies.)

### 8. The sigmoid limits depth

$\max_z\sigma'(z)=0.25$, so each sigmoid layer multiplies the backward signal by at most 0.25, even with ideal weights.

| layers $L$ | best case $0.25^L$ | realistic $\mathbb E[\sigma'(z)]^L$, $z\sim\mathcal N(0,1)$ |
|---|---|---|
| 1 | $2.500\times10^{-1}$ | $2.066\times10^{-1}$ |
| 5 | $9.766\times10^{-4}$ | $3.768\times10^{-4}$ |
| 10 | $9.537\times10^{-7}$ | $1.420\times10^{-7}$ |
| 20 | $9.095\times10^{-13}$ | $2.016\times10^{-14}$ |
| 50 | $7.889\times10^{-31}$ | $5.768\times10^{-35}$ |

($\mathbb E[\sigma'(z)]=0.206643$ by simulation.) The gradient falls below float32 epsilon ($1.192\times10^{-7}$) after 11.50 layers in the best case and 10.11 realistically. ReLU's derivative on active units is exactly 1, so surviving paths are not damped.

A bigger learning rate cannot fix this: compensating needs a factor $4^L$ ($1.049\times10^6$ at $L=10$), which would make the shallow layers diverge. There is only one $\eta$.

This is a second reason, besides memory ([[01 - Introduction to Deep Learning|ch. 01]]), why deep networks were impractical before ~2010. Both constraints eased around the same time (larger GPU memory; ReLU, Nair & Hinton 2010).

### 9. Products of random matrices

D2L multiplies 100 random $4\times4$ $\mathcal N(0,1)$ matrices and prints an entry of $1.2044\times10^{25}$. The growth rate has a closed form (Cohen & Newman 1984; added beyond D2L), the top Lyapunov exponent:
$$\lambda_1=\tfrac12\left[\ln(2\sigma^2)+\psi(n/2)\right]$$
At $n=4$, $\sigma=1$: $\lambda_1=0.557966$, predicting $10^{24.23}$ after 100 products. D2L's run ($10^{25.08}$) is ordinary: $z=+0.28$ against 400 simulated replications, which ranged from $10^{19.72}$ to $10^{29.67}$. "The product explodes" describes a distribution, and one printed run is one draw.

Neutral growth needs $\sigma^*=e^{-\lambda_1}=0.572372$ at $n=4$. Xavier gives $\sqrt{2/8}=0.5$, contracting the top direction by 12.64% per layer. The gap shrinks like $O(1/n)$ (simulated over 20,000 layers: $n=4$: −0.135181 theory vs −0.137873; $n=64$: −0.007853 vs −0.007866).

### 10. Initialization

Xavier (Glorot & Bengio 2010). For $o_i=\sum_{j=1}^{n_{\text{in}}}w_{ij}x_j$ with zero-mean independent weights (variance $\sigma^2$) and inputs (variance $\gamma^2$):
$$\operatorname{Var}[o_i]=n_{\text{in}}\sigma^2\gamma^2$$
Forward stability needs $n_{\text{in}}\sigma^2=1$, backward stability $n_{\text{out}}\sigma^2=1$. Xavier compromises:
$$\sigma=\sqrt{\frac{2}{n_{\text{in}}+n_{\text{out}}}}\qquad\text{or}\qquad \mathcal U\!\left(-\sqrt{\tfrac{6}{n_{\text{in}}+n_{\text{out}}}},\ \sqrt{\tfrac{6}{n_{\text{in}}+n_{\text{out}}}}\right)$$
(The uniform version has variance $a^2/3=2/(n_{\text{in}}+n_{\text{out}})$.) For $784\to256$: forward wants 0.035714, backward 0.062500, Xavier gives 0.043853.

Xavier preserves the mean of $\|W\mathbf x\|^2/\|\mathbf x\|^2$ exactly, but not its typical value:

| $n$ | mean | median | $\mathbb E[\ln\text{ratio}]$ |
|---|---|---|---|
| 4 | 1.00352 | 0.84195 | −0.26517 |
| 16 | 1.00109 | 0.96117 | −0.06270 |
| 64 | 1.00005 | 0.98843 | −0.01565 |
| 256 | 1.00040 | 0.99788 | −0.00349 |

A typical pass shrinks the signal, while rare large draws hold the mean at 1. Over 50 layers at $n=4$ the typical squared norm is multiplied by $1.58\times10^{-6}$ while the mean stays 1.00. Narrow layers are riskier than the variance calculation suggests.

D2L also notes Xiao et al. (2018) trained 10,000-layer networks with careful initialization alone.

### 11. Generalization in deep networks

- Deep networks are over-parametrized and usually fit every training label, even random ones (Zhang et al. 2021), so VC and Rademacher bounds say nothing useful.
- Making models larger often reduces test error: **double descent** (Nakkiran et al. 2021).
- Nonparametric views fit better: 1-nearest-neighbour has zero training error and is consistent; infinitely wide MLPs behave like kernel methods (neural tangent kernel, Jacot et al. 2018).
- **Early stopping**: networks fit clean labels first and noisy labels later. Stop when validation error has not improved by $\epsilon$ for a set number of epochs (patience). It matters when labels are noisy and little when classes are cleanly separable.
- Typical weight-decay strengths do not prevent interpolation; D2L suggests its benefit may come together with early stopping.

### 12. Dropout

Bishop (1995): training with input noise equals Tikhonov regularization. Dropout (Srivastava et al. 2014) applies noise inside the network:
$$h'=\begin{cases}0 & \text{with probability } p\\ h/(1-p) & \text{otherwise}\end{cases}$$

$\mathbb E[h']=h$. The variance (D2L ex. 5.6.3, unanswered):
$$\operatorname{Var}[h']=h^2\frac{p}{1-p},\qquad \mathrm{CV}=\sqrt{\frac{p}{1-p}}$$

| $p$ | $\operatorname{Var}/h^2$ | CV |
|---|---|---|
| 0.1 | 0.1111 | 0.3333 |
| 0.2 | 0.2500 | 0.5000 |
| 0.5 | 1.0000 | 1.0000 |
| 0.8 | 4.0000 | 2.0000 |
| 0.9 | 9.0000 | 3.0000 |

At $p=0.5$ the noise's standard deviation equals the activation. Noise added early passes through every later layer, which explains D2L's advice to use smaller $p$ near the input.

At test time dropout is turned off; no rescaling is needed because of the $1/(1-p)$ factor. Keeping it on at test time and comparing predictions gives a cheap uncertainty estimate (MC dropout).

D2L's printed example at $p=0.5$ on $\mathbf X=0,\dots,15$ kept 11 of 16 units (68.75%; $P(\ge11)=0.105$ under $\mathrm{Bin}(16,0.5)$), and its mean is 8.875 against 7.5 (+18.33%). Unbiased on average does not mean close on any single draw, and the network trains on single draws.

### 13. Parameter management (D2L ch. 6)

- **Access**: `net[2].state_dict()`, `net[2].bias.data`, `net.named_parameters()`. `.grad` is `None` until `backward()` runs.
- **Tied parameters**: using the same layer object twice makes one shared tensor. Its gradient is the sum over all uses, so a layer used three times gets three gradient contributions (weight tying in language models, shared kernels in [[05 - Convolutional Neural Network|ch. 05]]).
- **Lazy initialization**: `nn.LazyLinear` infers shapes at the first forward pass. Its default initializer is why [[02 - Linear Regression|ch. 02]]'s concise weight-decay run started from a different norm.
- **Custom layers**: subclass `nn.Module`, define `forward`, register weights with `nn.Parameter`.

## Optimizers (D2L ch. 12)

### 14. The landscape

Optimization minimizes training error; generalization is a separate goal. In high dimensions, zero-gradient points are mostly **saddle points**: a minimum needs all Hessian eigenvalues positive, which becomes unlikely as dimension grows ([[Optimization/contents/03 - Unconstrained Optimality Conditions|Optimization ch. 03]]).

**Newton's method**: $\boldsymbol\epsilon=-\mathbf H^{-1}\nabla f$. Where the Hessian is negative it steps uphill: on $f(x)=x\cos(cx)$ from $x=10$, D2L's run ends at $x=26.83$; with $\eta=0.5$ it reaches 7.27. Storing $\mathbf H$ costs $O(d^2)$. Adaptive optimizers can be seen as cheap approximations to the diagonal of $\mathbf H^{-1}$ ([[Optimization/contents/06 - Newton and Quasi-Newton Methods|Optimization ch. 06]]).

### 15. Gradient descent on an ill-conditioned quadratic

D2L's example $f(\mathbf x)=0.1x_1^2+2x_2^2$ has Hessian eigenvalues 0.2 and 4, so $\kappa=20$. Per eigendirection, gradient descent is exactly
$$x_t=(1-\eta\lambda)^t\,x_0$$

| $\eta$ | closed form after 20 steps from $(-5,-2)$ | D2L prints |
|---|---|---|
| 0.4 | $(0.92)^{20}(-5)=-0.943467$, $(-0.6)^{20}(-2)=-0.000073$ | `x1: -0.943467, x2: -0.000073` |
| 0.6 | $(0.88)^{20}(-5)=-0.387814$, $(-1.4)^{20}(-2)=-1673.365109$ | `x1: -0.387814, x2: -1673.365109` |

The start point $(-5,-2)$ is not given in the text; it was recovered by matching the printout, and all of D2L's printed traces in this section then match to six decimals.

Stability: $|1-\eta\lambda_{\max}|<1\iff\eta<2/\lambda_{\max}=0.5$. So $\eta=0.4$ is stable and $\eta=0.6$ diverges at rate 1.4 per step. The underlying tension: $x_2$ needs a small step, $x_1$ a large one, and both share $\eta$.

### 16. Momentum

$$\mathbf v_t\leftarrow\beta\mathbf v_{t-1}+\mathbf g_t,\qquad \mathbf x_t\leftarrow\mathbf x_{t-1}-\eta\mathbf v_t$$

Expanding, $\mathbf v_t=\sum_{\tau}\beta^\tau\mathbf g_{t-\tau}$: consistent directions accumulate, oscillating ones cancel.

| $\eta,\beta$ | simulated | D2L prints |
|---|---|---|
| 0.6, 0.5 | $(0.007188, 0.002553)$ | `x1: 0.007188, x2: 0.002553` |
| 0.6, 0.25 | $(-0.126340, -0.186632)$ | `x1: -0.126340, x2: -0.186632` |

At $\eta=0.6$ plain GD diverges to −1673 while momentum with $\beta=0.5$ converges.

With optimal tuning, GD contracts by $\frac{\kappa-1}{\kappa+1}$ per step and momentum (with $\beta^*=\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^2$) by $\frac{\sqrt\kappa-1}{\sqrt\kappa+1}$ (standard theory, not in D2L):

| $\kappa$ | GD steps for 100× error reduction | momentum steps | speedup |
|---|---|---|---|
| 1 | 1 | 1 | 1.00× |
| 20 | 46.0 | 10.1 | 4.55× |
| 100 | 230.3 | 22.9 | 10.03× |
| 10,000 | 23,025.9 | 230.3 | 100.00× |

GD needs $O(\kappa)$ steps, momentum $O(\sqrt\kappa)$. Momentum helps a lot on badly conditioned problems and hardly at all on well-conditioned ones.

**Effective step size.** Since $\sum_\tau\beta^\tau=1/(1-\beta)$, momentum's effective step is $\eta/(1-\beta)$ (D2L derives this). D2L then "reduces the learning rate slightly":

| $\eta$ | $\beta$ | $\eta/(1-\beta)$ | D2L's printed loss |
|---|---|---|---|
| 0.02 | 0.5 | 0.0400 | 0.246 |
| 0.01 | 0.9 | 0.1000 | 0.254 |
| 0.005 | 0.9 | 0.0500 | 0.247 |

The "reduction" is a 2.5× increase in effective step, and the loss gets worse. Treat $\eta$ and $\beta$ together: raising $\beta$ from 0.9 to 0.99 without dividing $\eta$ by 10 multiplies the effective step by 10.

### 17. Adagrad and preconditioning

$$\mathbf s_t=\mathbf s_{t-1}+\mathbf g_t^2,\qquad \mathbf w_t=\mathbf w_{t-1}-\frac{\eta}{\sqrt{\mathbf s_t+\epsilon}}\odot\mathbf g_t$$

Motivation: sparse features (rare features get larger steps), and more generally diagonal preconditioning, using gradient magnitudes as a cheap proxy for the Hessian diagonal.

| $\eta$ | simulated | D2L prints |
|---|---|---|
| 0.4 | $(-2.382563, -0.158591)$ | `x1: -2.382563, x2: -0.158591` |
| 2.0 | $(-0.002295, -0.000000)$ | `x1: -0.002295, x2: -0.000000` |

With roughly constant gradients $s_t\approx tg^2$, so the step decays like $\eta/\sqrt t$. Total travel $2\eta\sqrt t$ still grows, so Adagrad slows down rather than stopping. At $\eta=0.4$, Adagrad has covered 52.35% of the distance in $x_1$ after 20 steps; RMSProp (§18) at the same $\eta$ has covered 99.79% ($x_1=-0.010599$).

**Rotated problems** (D2L ex. 12.7.2–4, unanswered). Rotate the same quadratic by 45°: $f=0.1(x_1+x_2)^2+2(x_1-x_2)^2$, $\mathbf Q=\begin{pmatrix}4.2&-3.8\\-3.8&4.2\end{pmatrix}$.

| | eigenvalues | $\kappa$ | after diagonal preconditioning | $\kappa$ |
|---|---|---|---|---|
| axis-aligned | (0.2, 4.0) | 20 | (1.0, 1.0) | 1 |
| rotated 45° | (0.4, 8.0) | 20 | (0.095238, 1.904762) | 20 |

Diagonal preconditioning fixes the axis-aligned case completely and does nothing for the rotated one. All diagonal adaptive methods (Adagrad, RMSProp, Adadelta, Adam) assume curvature is roughly aligned with the coordinates. Gerschgorin's theorem gives $\kappa\le(1+R)/(1-R)$ after preconditioning, where $R$ is the largest off-diagonal row sum; here $R=0.904762$ and the bound equals the true $\kappa=20$.

### 18. RMSProp and Adadelta

RMSProp (Tieleman & Hinton 2012) replaces Adagrad's sum with a leaky average:
$$\mathbf s_t\leftarrow\gamma\mathbf s_{t-1}+(1-\gamma)\mathbf g_t^2,\qquad \mathbf x_t\leftarrow\mathbf x_{t-1}-\frac{\eta}{\sqrt{\mathbf s_t+\epsilon}}\odot\mathbf g_t$$

Adadelta (Zeiler 2012) has no learning rate; it scales by a leaky average of its own recent squared updates:
$$\mathbf s_t=\rho\mathbf s_{t-1}+(1-\rho)\mathbf g_t^2,\quad \mathbf g'_t=\frac{\sqrt{\Delta\mathbf x_{t-1}+\epsilon}}{\sqrt{\mathbf s_t+\epsilon}}\odot\mathbf g_t,\quad \Delta\mathbf x_t=\rho\Delta\mathbf x_{t-1}+(1-\rho)\mathbf g_t'^2$$

D2L says $\rho=0.9$ "amounts to a half-life time of 10". Three different numbers describe an exponential average:

| $\gamma$ | effective sample size $1/(1-\gamma)$ | mean lag $\gamma/(1-\gamma)$ | half-life $\ln0.5/\ln\gamma$ |
|---|---|---|---|
| 0.5 | 2.00 | 1.00 | 1.00 |
| 0.9 | 10.00 | 9.00 | 6.58 |
| 0.95 | 20.00 | 19.00 | 13.51 |
| 0.999 | 1000.00 | 999.00 | 692.80 |

At 0.9, 10 is the effective sample size; the half-life is 6.58. (Declined as an erratum: loose terminology, correct quantity.)

### 19. Adam

$$\mathbf v_t\leftarrow\beta_1\mathbf v_{t-1}+(1-\beta_1)\mathbf g_t,\qquad \mathbf s_t\leftarrow\beta_2\mathbf s_{t-1}+(1-\beta_2)\mathbf g_t^2$$
$$\hat{\mathbf v}_t=\frac{\mathbf v_t}{1-\beta_1^t},\quad \hat{\mathbf s}_t=\frac{\mathbf s_t}{1-\beta_2^t},\quad \mathbf x_t\leftarrow\mathbf x_{t-1}-\frac{\eta\,\hat{\mathbf v}_t}{\sqrt{\hat{\mathbf s}_t}+\epsilon}$$
Defaults $\beta_1=0.9$, $\beta_2=0.999$.

**Bias correction.** D2L says zero initialization biases the states "towards smaller values". Each state is biased small, but the step is their ratio, and the ratio is biased large. With a constant gradient:
$$\frac{\text{uncorrected step}}{\text{corrected step}}=\frac{1-\beta_1^t}{\sqrt{1-\beta_2^t}}$$

| step $t$ | uncorrected / corrected |
|---|---|
| 1 | 3.1623 |
| 12 | 6.5685 (peak) |
| 100 | 3.2408 |
| 1,000 | 1.2576 |
| 3,925 | within 1% |

Without correction, early steps are up to 6.6× too large for thousands of steps, because $\mathbf s$ (with $\beta_2=0.999$) is much more biased and sits under a square root.

**Bounded step and scale invariance** (not stated by D2L). With $\hat{\mathbf v}=g$ and $\hat{\mathbf s}=g^2$ the step is $\eta\,\mathrm{sign}(g)$, independent of $|g|$. Multiplying the loss by $c$ leaves Adam's updates unchanged; SGD's scale by $c$. Minimizing $cx^2$ from $x_0=1$ ($\eta=0.01$, 200 steps) for $c$ from $10^{-3}$ to $10^3$: Adam ends at 0.015572 in every case (spread $1.02\times10^{-6}$); SGD ends at 0.996 for $c=10^{-3}$ and diverges ($5.63\times10^{255}$) for $c=10^3$. This is why an Adam learning rate transfers between problems and an SGD one does not.

**Yogi** (Zaheer et al. 2018): Adam's $\mathbf s_t$ can forget too fast when $\mathbf g_t^2$ is noisy. Yogi uses $\mathbf s_t\leftarrow\mathbf s_{t-1}+(1-\beta_2)\mathbf g_t^2\odot\mathrm{sgn}(\mathbf g_t^2-\mathbf s_{t-1})$.

### 20. D2L's optimizer runs side by side

All on the same airfoil regression, batch size 10:

| section | settings | loss | sec/epoch |
|---|---|---|---|
| momentum, scratch | lr 0.02, m 0.5 | 0.246 | 0.195 |
| momentum, scratch | lr 0.01, m 0.9 | 0.254 | 0.146 |
| momentum, scratch | lr 0.005, m 0.9 | 0.247 | 0.152 |
| momentum, concise | lr 0.005, m 0.9 | 0.247 | 0.142 |
| Adagrad, scratch | lr 0.1 | 0.244 | 0.232 |
| Adagrad, concise | lr 0.1 | 0.242 | 0.155 |
| RMSProp, scratch | lr 0.01, γ 0.9 | 0.243 | 0.177 |
| RMSProp, concise | lr 0.01, α 0.9 | 0.243 | 0.138 |
| Adadelta, scratch | ρ 0.9 | 0.244 | 0.221 |
| Adadelta, concise | ρ 0.9 | 0.243 | 0.164 |
| Adam, scratch | lr 0.01 | 0.246 | 0.224 |
| Adam, concise | lr 0.01 | 0.243 | 0.182 |
| Yogi, scratch | lr 0.01 | 0.245 | 0.207 |

Losses lie within 4.96% of each other; time per epoch varies 68%. The problem is a small, dense, convex regression, so it cannot show the advantages adaptive methods are designed for (sparse features, bad conditioning). Before trusting a comparison, ask whether the benchmark could have shown a difference. The hand-written versions are on average 1.286× slower than the framework's.

### 21. Learning-rate schedules

D2L's checklist:
1. **Magnitude**: too large diverges ($\eta<2/\lambda_{\max}$ on a quadratic), too small is slow.
2. **Decay**: needed, but slower than the $O(t^{-1/2})$ suited to convex problems.
3. **Warmup**: early gradients from random weights are not informative, so start with small steps.
4. **Cyclic schedules and averaging** (Izmailov et al. 2018): not covered.

## ✏️ Exercises

> [!example]- **1.** *(Easy) The linear collapse*
> $\mathbf W^{(1)}=\begin{pmatrix}1&2\\0&1\\3&-1\end{pmatrix}$, $\mathbf b^{(1)}=(1,-1)$, $\mathbf W^{(2)}=\begin{pmatrix}2&0&1\\1&1&-1\end{pmatrix}$, $\mathbf b^{(2)}=(0.5,0.5,0.5)$, no activation.
> **(a)** Find the equivalent single layer and check it at $\mathbf x=(1,2,3)$. **(b)** Its rank? **(c)** Parameter counts.
>
> ---
> **(a)** $\mathbf W=\mathbf W^{(1)}\mathbf W^{(2)}=\begin{pmatrix}4&2&-1\\1&1&-1\\5&-1&4\end{pmatrix}$, $\mathbf b=\mathbf b^{(1)}\mathbf W^{(2)}+\mathbf b^{(2)}=(1.5,-0.5,2.5)$. Both forms give $(22.5, 0.5, 11.5)$ at $\mathbf x=(1,2,3)$.
>
> **(b)** Rank 2 (bounded by the hidden width), while a general $3\times3$ layer can have rank 3.
>
> **(c)** Two layers: $3\cdot2+2+2\cdot3+3=17$. One layer: $9+3=12$. More parameters, less expressive.

> [!example]- **2.** *(Easy–medium) How deep can a sigmoid network be?*
> **(a)** Best-case damping over $L$ layers? **(b)** Depth where it falls below float32 epsilon ($1.1921\times10^{-7}$) and float64 epsilon ($2.2204\times10^{-16}$)? **(c)** Why not raise $\eta$? **(d)** ReLU's factor?
>
> ---
> **(a)** $0.25^L$, since $\max\sigma'=0.25$. Realistically $0.206643^L$.
>
> **(b)** $L=\ln\varepsilon/\ln0.25$: 11.50 for float32, 26.00 for float64. Realistically 10.11 in float32.
>
> **(c)** You would need $\eta\times4^L$ ($1.049\times10^6$ at $L=10$), which makes shallow layers diverge.
>
> **(d)** Exactly 1 on active units, at any depth.

> [!example]- **3.** *(Medium) Dropout variance*
> **(a)** Derive $\operatorname{Var}[h']$ and CV. **(b)** Values at $p=0.2, 0.5, 0.8$. **(c)** D2L's $p=0.5$ example on $0,\dots,15$: how many kept, and how far is the mean off? **(d)** Why use smaller $p$ near the input?
>
> ---
> **(a)** $\mathbb E[h'^2]=h^2/(1-p)$, so $\operatorname{Var}=h^2p/(1-p)$ and $\mathrm{CV}=\sqrt{p/(1-p)}$.
>
> **(b)** $p=0.2$: $0.25h^2$, CV 0.5. $p=0.5$: $h^2$, CV 1. $p=0.8$: $4h^2$, CV 2.
>
> **(c)** 11 of 16 kept ($P(\ge11)=0.1051$, unremarkable). Mean 8.875 vs 7.5: +18.33%, or +0.62 sd (sd of the mean 2.2009).
>
> **(d)** Early noise propagates through all later layers.

> [!example]- **4.** *(Medium–hard) GD vs momentum on the quadratic*
> $f=0.1x_1^2+2x_2^2$ from $(-5,-2)$.
> **(a)** Closed form and $\mathbf x_{20}$ at $\eta=0.4$, 0.6. **(b)** Stability bound. **(c)** Steps for 100× error reduction with optimal GD and optimal momentum. **(d)** Scaling with $\kappa$.
>
> ---
> **(a)** $x_t=(1-\eta\lambda)^tx_0$: $\eta=0.4$ gives $(-0.943467, -0.000073)$; $\eta=0.6$ gives $(-0.387814, -1673.365109)$, matching D2L.
>
> **(b)** $\eta<2/4=0.5$.
>
> **(c)** $\kappa=20$. GD: $\eta^*=2/(0.2+4)=0.476190$, rate 0.904762, $\ln0.01/\ln0.904762=46.01$ steps. Momentum: $\beta^*=0.402605$, rate 0.634512, 10.12 steps. Speedup 4.55×.
>
> **(d)** $O(\kappa)$ vs $O(\sqrt\kappa)$: 10.03× at $\kappa=100$, 100× at $\kappa=10^4$. See [[Optimization/contents/05 - Gradient Methods|Optimization ch. 05]].

> [!example]- **5.** *(Hard) Adam's bias correction and scale invariance*
> **(a)** With a constant gradient, ratio of uncorrected to corrected step at step $t$; value at $t=1$, maximum, and when within 1%. **(b)** Is the uncorrected step too small? **(c)** Show the corrected step is bounded and scale invariant. **(d)** Check numerically on $cx^2$.
>
> ---
> **(a)** $v_t=(1-\beta_1^t)g$, $s_t=(1-\beta_2^t)g^2$, ratio $(1-\beta_1^t)/\sqrt{1-\beta_2^t}$. At $t=1$: $0.1/\sqrt{0.001}=3.1623$. Maximum 6.5685 at $t=12$. Within 1% at $t=3{,}925$.
>
> **(b)** No, it is too large at every step: $\mathbf s$ is more biased and sits under a square root.
>
> **(c)** Step $=\eta g/(|g|+\epsilon)\approx\eta\,\mathrm{sign}(g)$. Scaling the loss by $c$ scales $v$ by $c$ and $s$ by $c^2$, so $\hat v/\sqrt{\hat s}$ is unchanged.
>
> **(d)** From $x_0=1$, $\eta=0.01$, 200 steps:
>
> | $c$ | Adam | SGD |
> |---|---|---|
> | $10^{-3}$ | 0.01557351 | 0.996008 |
> | $1$ | 0.01557249 | 0.0175879 |
> | $10^{3}$ | 0.01557248 | $5.63\times10^{255}$ |
>
> Adam's spread is $1.02\times10^{-6}$; SGD diverges at $c=10^3$ since $2c\eta=20>2$. Also, 200 steps of size ≤0.01 can travel at most 2, consistent with the result.

## 📝 Summary

- Without a nonlinearity an MLP collapses to one affine layer, and a narrow hidden layer limits rank.
- tanh and sigmoid give the same function class ($\tanh x=2\,\mathrm{sigmoid}(2x)-1$); Swish and GELU are non-monotone.
- Backprop is the reverse-mode chain rule; stored activations and optimizer state make training memory-hungry (Adam: 2× SGD's parameter memory; at 1B parameters, 14.90 GB total in float32).
- Sigmoid derivatives ≤ 0.25 limit a sigmoid MLP to about 10–11 layers in float32; ReLU's factor is 1.
- Random matrix products grow at the Lyapunov rate $\tfrac12[\ln 2\sigma^2+\psi(n/2)]$; one printed run is one sample from a wide distribution.
- Xavier: $\sigma^2=2/(n_{\text{in}}+n_{\text{out}})$. It preserves the mean signal size, but the typical value shrinks at small width.
- Dropout: $\operatorname{Var}[h']=h^2p/(1-p)$; at $p=0.5$ the noise is as large as the signal.
- GD needs $\eta<2/\lambda_{\max}$ and $O(\kappa)$ steps; momentum needs $O(\sqrt\kappa)$. Effective momentum step is $\eta/(1-\beta)$.
- Adagrad's steps shrink like $1/\sqrt t$; RMSProp uses a leaky average. Diagonal methods do not help when curvature is not axis-aligned.
- Adam = momentum + RMSProp + bias correction (which shrinks early steps that would be up to 6.6× too big). Its step is about $\eta$ per coordinate and invariant to loss scale.
- D2L's 13 optimizer runs all end within 5% of each other because the benchmark is too easy to separate them.

## ⚠️ Important Notes

1. Never transcribe formulas from this PDF; e.g. the Adagrad update extracts as `wt = wt1  pst + ϵ gt` (minus, $\eta$, fraction bar and $\odot$ deleted; `p` for $\sqrt{}$).
2. A shared parameter's gradient is the sum over its uses.
3. Dropout is unbiased on average, but each training step sees one noisy draw.
4. Parameter count is not capacity; ask what the model can represent.
5. Check conditioning, not just rank: $\kappa$ sets the number of GD steps (46 at $\kappa=20$, 23,026 at $\kappa=10^4$).
6. Diagonal adaptive methods assume axis-aligned curvature. Batch norm and residual connections help partly by changing the parametrization.
7. Raising $\beta$ raises the effective learning rate $\eta/(1-\beta)$.
8. Adam and SGD learning rates are not comparable; do not port $\eta$ from one to the other.
9. A from-scratch Adam without bias correction shows an early loss spike that then recovers: easy to miss.
10. Adagrad never quite stops; watch the step size, not only the loss.
11. "Half-life" of an exponential average is ambiguous: for 0.9, effective sample size 10, mean lag 9, half-life 6.58.
12. Classical capacity bounds do not explain deep generalization. Early stopping helps mainly when labels are noisy.
13. Newton's method goes uphill where curvature is negative.
14. Constant initialization keeps units identical forever; SGD noise cannot fix it.
15. Activation memory scales with batch size; parameter memory does not.
16. The sigmoid depth limit is 11.5 layers in float32 and 26 in float64.

> [!warning] Gaps in the source material
> - **Figures:** the MLP diagram, computational graph and dropout diagram are reconstructed from the prose. Activation plots, optimizer trajectory plots and schedule curves are lost, but the trajectories were recovered numerically from the printed endpoints.
> - **Code** loses its indentation; printed outputs extract intact.
> - **Added by me:** the rank example (D2L ex. 5.1.1); §8's depth bounds; the Lyapunov exponent and 400-run simulation; the Xavier mean/median table; the dropout variance (ex. 5.6.3) and audit of the printed example; the memory accounting (ex. 5.3.3); the closed form for GD, the recovered start point and the reproduced traces; the $\kappa$ vs $\sqrt\kappa$ table; the effective-step check; the rotated preconditioning result and Gerschgorin bound (ex. 12.7.2–4); the Adam bias ratio and scale invariance; the 13-run table.
> - **Declined discrepancy D7:** "half-life of 10" for $\rho=0.9$ (true half-life 6.58); loose wording for a correctly computed quantity.
> - **Skipped:** MLP implementations and the Kaggle example (§5.2, §5.7); file I/O and GPU sections (§6.6–6.7, see [[MLOps/contents/00-Index|MLOps]]); convexity and plain GD/SGD (§12.2–12.5, see [[Optimization/contents/02 - Convex Sets and Convex Functions|Optimization]] and [[02 - Linear Regression|ch. 02]]); schedule implementations.
> - Literature results (double descent, NTK, 10,000-layer training) are quoted, not derived.

**Previous:** [[03 - Logistic Regression]] · **Next:** [[05 - Convolutional Neural Network]]
