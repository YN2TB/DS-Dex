---
subject: Deep Learning
chapter: 2
tags: [ds, deep-learning, regression, sgd, regularization]
source: "Zhang, Lipton, Li & Smola — Dive into Deep Learning, §3.1–3.7 (book pp. 82–126)"
---

# Linear Regression

> [!info] Why a whole chapter on a model that is not deep
> D2L's framing: before making networks deep, implement a shallow one where inputs connect **directly** to outputs. Two reasons. First, you meet **every component of training** — parametrizing the output layer, handling data, specifying a loss, running the optimizer — without an architecture to distract you. Second, this class of shallow networks *is* the class of **linear models**, which subsumes much of classical statistical prediction, and you will need them as **baselines when justifying anything fancier**.
>
> Everything in [[04 - Neural Network]] and beyond is this chapter plus nonlinearity.

## 📘 Main Knowledge

### 1. The model

Running example: predict house **price** (dollars) from **area** (sq ft) and **age** (years). Linear regression dates to Gauss (1809) and Legendre (1805) and rests on two assumptions:

1. **Linearity** — the conditional mean $\mathbb{E}[Y \mid X = \mathbf{x}]$ is a weighted sum of the features. Note this is a claim about the *mean*: individual targets may deviate on account of noise.
2. **Well-behaved noise** — the deviation is **Gaussian**. (§4 shows this assumption *is* the squared loss.)

Long form, then compact form:
$$\text{price} = w_{\text{area}}\cdot\text{area} + w_{\text{age}}\cdot\text{age} + b$$
$$\hat y = w_1x_1 + \cdots + w_dx_d + b = \mathbf{w}^\top\mathbf{x} + b, \qquad \mathbf{w},\mathbf{x}\in\mathbb{R}^d$$

**Notation, and D2L is strict about it:** $n$ = number of examples, $d$ = number of features; **superscripts enumerate examples, subscripts index coordinates** — $\mathbf{x}^{(i)}$ is the $i$-th example, $x^{(i)}_j$ its $j$-th coordinate. The hat in $\hat y$ always denotes an estimate.

Stacking all $n$ examples as rows gives the **design matrix** $\mathbf{X}\in\mathbb{R}^{n\times d}$ — *one row per example, one column per feature* — and all predictions at once:
$$\hat{\mathbf{y}} = \mathbf{X}\mathbf{w} + b$$
with $b$ **broadcast** across rows.

> [!note] "Linear" is a lie, politely
> $\mathbf{w}^\top\mathbf{x}+b$ is an **affine** transformation: a linear map (the weighted sum) **plus a translation** (the bias). The bias matters — without it you are restricted to hyperplanes through the origin. We will never see a house of precisely zero area, and we still need $b$ to reach all linear functions of the features.
>
> The standard trick, used constantly: **append a column of 1s to $\mathbf{X}$ and absorb $b$ into $\mathbf{w}$.** Affine functions of $\mathbf{x}$ are exactly linear functions of $(\mathbf{x},1)$.

### 2. The loss

A **loss function** quantifies the distance between real and predicted values: non-negative, smaller is better, a perfect prediction costs 0. For regression, the **squared error**:
$$\ell^{(i)}(\mathbf{w},b) = \tfrac{1}{2}\left(\hat y^{(i)} - y^{(i)}\right)^2$$

**The $\tfrac12$ is bookkeeping, not mathematics** — it cancels against the 2 that falls out of differentiating the square. It changes the loss's value but not its minimizer.

Averaging over the dataset:
$$L(\mathbf{w},b) = \frac{1}{n}\sum_{i=1}^{n}\ell^{(i)}(\mathbf{w},b) = \frac{1}{n}\sum_{i=1}^{n}\frac12\left(\mathbf{w}^\top\mathbf{x}^{(i)} + b - y^{(i)}\right)^2$$
$$\mathbf{w}^*, b^* = \operatorname*{argmin}_{\mathbf{w},b} L(\mathbf{w},b)$$

> [!warning] The quadratic is a double-edged sword — D2L says so explicitly
> Large errors contribute *disproportionately* (quadratically). That is desirable — it pushes the model away from big mistakes — **and** it makes the fit **excessively sensitive to anomalous data**. One outlier at distance 10 contributes as much as one hundred points at distance 1. See §4 for the principled fix (change the noise model) and Important Note 6.

**The empirical error is a function of the parameters only**, because the training data is given and out of our control. Say this out loud until it is automatic — it is the mental flip on which all optimization rests.

### 3. The analytic solution — and why you should not get used to it

Absorb $b$, so the problem is to minimize $\|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2$. Differentiate and set to zero:
$$\partial_{\mathbf{w}}\|\mathbf{y}-\mathbf{X}\mathbf{w}\|^2 = 2\mathbf{X}^\top(\mathbf{X}\mathbf{w}-\mathbf{y}) = 0 \;\Longrightarrow\; \boxed{\mathbf{X}^\top\mathbf{X}\mathbf{w} = \mathbf{X}^\top\mathbf{y}}$$
These are the **normal equations**, and when $\mathbf{X}^\top\mathbf{X}$ is invertible:
$$\mathbf{w}^* = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$$

**The condition is full rank** — no feature linearly dependent on the others. Then the loss surface has exactly **one critical point**, and it is the global minimum over the whole domain. (The loss is convex; see [[Optimization/contents/00-Index|Optimization]].)

> [!important] D2L's warning, and it is the reason this book exists
> "While simple problems like linear regression may admit analytic solutions, **you should not get used to such good fortune**. Although analytic solutions allow for nice mathematical analysis, the requirement of an analytic solution is so restrictive that it would **exclude almost all exciting aspects of deep learning**."
>
> Linear regression is the *last* model in this course you can solve by algebra. Everything after it is solved by iteration.

**What goes wrong without full rank** — worked in exercise 4. If columns are linearly dependent, $\mathbf{X}^\top\mathbf{X}$ is singular, the minimizer is **not unique** (an entire affine subspace of solutions), and numerically, *near*-dependence is just as bad: the solution becomes wildly sensitive to the data. The fix is §7.

### 4. Where the squared loss actually comes from

So far the motivation was functional: squared loss returns the conditional expectation $\mathbb{E}[Y\mid X]$ when the pattern is truly linear, and penalizes outliers heavily. Here is the **principled** derivation, and it is the most important half-page in the chapter.

Assume observations are noisy measurements with **Gaussian noise**:
$$y = \mathbf{w}^\top\mathbf{x} + b + \epsilon, \qquad \epsilon \sim \mathcal{N}(0,\sigma^2)$$

Recall the normal density $p(x) = \frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{1}{2\sigma^2}(x-\mu)^2\right)$. The **likelihood** of observing a particular $y$ given $\mathbf{x}$ is therefore
$$P(y\mid\mathbf{x}) = \frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{1}{2\sigma^2}\left(y - \mathbf{w}^\top\mathbf{x} - b\right)^2\right)$$

Because examples are drawn **independently**, the likelihood of the whole dataset **factorizes**:
$$P(\mathbf{y}\mid\mathbf{X}) = \prod_{i=1}^{n} p\!\left(y^{(i)}\mid\mathbf{x}^{(i)}\right)$$

**Maximum likelihood** picks the parameters maximizing this. Products of exponentials are awkward, so take logs (monotone — the argmax is unchanged) and flip the sign (convention prefers minimization). The **negative log-likelihood**:
$$-\log P(\mathbf{y}\mid\mathbf{X}) = \sum_{i=1}^{n}\left[\underbrace{\tfrac{1}{2}\log(2\pi\sigma^2)}_{\text{no } \mathbf{w},b} + \frac{1}{2\sigma^2}\left(y^{(i)}-\mathbf{w}^\top\mathbf{x}^{(i)}-b\right)^2\right]$$

Now read off the result. The **first term does not involve $\mathbf{w}$ or $b$** — drop it. The second is the squared error up to the constant $1/\sigma^2$ — **and the minimizer does not depend on $\sigma$ either**. Therefore:

> **Minimizing mean squared error IS maximum likelihood estimation of a linear model under additive Gaussian noise.**

This is the template for every loss in the course: **choose a noise model, take the negative log-likelihood, and the loss falls out.** Change the assumption and the loss changes with it — Laplace noise gives $\ell_1$ (exercise 2), Bernoulli gives cross-entropy in [[03 - Logistic Regression]], Poisson gives a count loss.

> [!note] Cross-subject
> This is straight maximum-likelihood theory — see [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] for the estimator's properties (consistency, asymptotic normality, the Cramér–Rao bound) and [[Probability Theory/contents/00-Index|Probability Theory]] for the Gaussian itself. What deep learning adds is only that the mean is computed by a network instead of a dot product.

### 5. Minibatch stochastic gradient descent

Since almost nothing else has a closed form, we need an iterative method: **gradient descent** — repeatedly nudge the parameters in the direction that lowers the loss.

**Two extremes, both bad:**

| Strategy | Uses per update | Problem |
|---|---|---|
| **Full batch** | all $n$ examples | must pass the entire dataset for **one** update; and if the data is redundant, that expensive update buys little |
| **Pure SGD** | 1 example | **(computational)** processors are far faster at arithmetic than at moving data from main memory to cache — a matrix–vector multiply is *up to an order of magnitude* more efficient than the same count of vector–vector operations; **(statistical)** some layers, e.g. batch normalization, only work with more than one observation at a time |

**The fix is the obvious middle: the minibatch.** At iteration $t$, sample a minibatch $\mathcal{B}_t$ of fixed size $|\mathcal{B}|$, compute the gradient of the average loss on it, multiply by the **learning rate** $\eta$, subtract:

$$\boxed{(\mathbf{w},b) \leftarrow (\mathbf{w},b) - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}_t}\partial_{(\mathbf{w},b)}\,\ell^{(i)}(\mathbf{w},b)}$$

For squared loss and an affine model this expands in closed form:
$$\mathbf{w} \leftarrow \mathbf{w} - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}_t}\mathbf{x}^{(i)}\left(\mathbf{w}^\top\mathbf{x}^{(i)}+b-y^{(i)}\right)$$
$$b \leftarrow b - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}_t}\left(\mathbf{w}^\top\mathbf{x}^{(i)}+b-y^{(i)}\right)$$

Read the structure: **each example pushes the weights along its own feature vector, scaled by its residual.** An example you already predict well ($\text{residual}\approx0$) contributes nothing. That is the whole algorithm.

**Batch size guidance from D2L:** it depends on memory, number of accelerators, choice of layers and dataset size, but **32 to 256, preferably a multiple of a large power of 2, is a good start.**

**Hyperparameters.** Batch size and learning rate are **not learned** — they are set by the user, tuned on a **validation set**, and can be optimized automatically (e.g. Bayesian optimization). *Anything not updated inside the training loop is a hyperparameter.*

> [!warning] Four things D2L is careful to say about the result
> 1. **You will not reach the exact minimizer.** Even if the function is truly linear and noiseless, the algorithm converges slowly and typically **will not find the minimizers exactly in a finite number of steps**.
> 2. **The result is not even deterministic** — the minibatches are chosen at random, and that breaks determinism. Two runs give different answers.
> 3. **Linear regression has a global minimum** (whenever $\mathbf{X}$ is full rank). **Loss surfaces of deep networks contain many saddle points and minima** — this is the last chapter where "the" optimum is a meaningful phrase.
> 4. **And it does not matter.** We do not need an exact parameter set, only one that predicts accurately. In practice, practitioners **seldom struggle to minimize loss on training sets**; the formidable task is accuracy on **unseen** data — *generalization*, which is §6.

**Terminology aside.** Practitioners call the prediction phase **inference**; D2L objects, and is right: in statistics *inference* usually means **parameter** inference, so the overloading confuses conversations with statisticians. This book says **prediction**.

### 6. Vectorization — the source's own benchmark, divided

D2L benchmarks adding two 10,000-dimensional vectors of ones, a Python `for` loop against the overloaded `+`:

| Method | Printed time |
|---|---|
| Python `for`-loop, element by element | `0.16781 sec` |
| single call to `+` | `0.00180 sec` |

D2L concludes only that "vectorizing code often yields **order-of-magnitude speedups**" — and never divides its own two numbers. Doing so:

$$\frac{0.16781}{0.00180} = \mathbf{93.23\times}$$

Per element that is **16.781 µs** versus **0.180 µs**. A commodity CPU performs on the order of $10^9$ additions per second, so a single addition costs ~1 ns, which is

$$\frac{1\text{ ns}}{16.781\ \mu s} = \mathbf{0.0060\%} \text{ of the loop's per-element cost}$$

**99.994% of the loop's time is Python interpreter overhead and not arithmetic.** Even the vectorized version spends only **0.56%** of its time on the additions. This is why every inner loop in this course is pushed into the library: you are not making the arithmetic faster, you are **deleting the interpreter from the inner loop**. See [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] on counting operations rather than seconds, and [[Basic Programming (C++)/contents/00-Index|Basic Programming (C++)]] for the same gap measured from the other side.

### 7. Linear regression as a neural network

Draw the model as a graph: inputs $x_1,\dots,x_d$ in an **input layer** of dimensionality $d$; a single output $o_1$ because we predict one number.

> **Linear regression is a single-layer fully connected neural network.** The input values are all *given*; there is **just one computed neuron**.

D2L counts layers by **computed** units, which is why this is "single-layer" despite the picture having two rows of circles. *(Layer-counting conventions differ between books — state yours.)*

**The biology, and D2L's honest deflation of it.** In the cartoon neuron: **dendrites** (input terminals), **nucleus** (CPU), **axon** (output wire), **axon terminals**, connecting via **synapses**. Information $x_i$ arrives at the dendrites weighted by **synaptic weights** $w_i$ — activation or inhibition via the product $x_iw_i$ — aggregated in the nucleus as $y=\sum_i x_iw_i + b$, possibly passed through a nonlinearity $\sigma(y)$, and sent down the axon. McCulloch and Pitts began from exactly this picture.

But:

> Although **airplanes might have been inspired by birds, ornithology has not been the primary driver of aeronautics innovation for some centuries** (Russell & Norvig). Likewise, inspiration in deep learning comes in equal or greater measure from mathematics, linguistics, psychology, statistics and computer science.

Consistent with [[01 - Introduction to Deep Learning]] §5: the name is historical; the content is the alternation of linear and nonlinear layers, and the chain rule.

### 8. Generalization

**The fundamental problem of machine learning, and arguably of all of statistics.** D2L's two students:

- **Extraordinary Ellie** memorizes every past exam answer perfectly — **100% recall** on recycled questions, and freezes on a new one.
- **Inductive Irene** memorizes poorly but picks up patterns — **90%** on the old exam, losing to Ellie, and **still 90%** on an all-fresh exam.

We want Irene. The question is how to tell them apart *before* the exam.

**Scale of the problem.** Some medical tasks give you a few thousand points; rare diseases, hundreds. ImageNet has millions of labelled photographs; Flickr YFC100M has over 100 million unlabelled. **And even at that extreme, the number of data points is infinitesimally small compared to the space of all possible megapixel images.** We are always in the small-sample regime.

#### 8.1 Two errors, and only one of them is computable

$$\underbrace{R_{\text{emp}}[\mathbf{X},\mathbf{y},f] = \frac1n\sum_{i=1}^n \ell\!\left(\mathbf{x}^{(i)},y^{(i)},f(\mathbf{x}^{(i)})\right)}_{\textbf{training error — a STATISTIC, a finite sum}}$$
$$\underbrace{R[p,f] = \mathbb{E}_{(\mathbf{x},y)\sim P}\left[\ell(\mathbf{x},y,f(\mathbf{x}))\right] = \iint \ell(\mathbf{x},y,f(\mathbf{x}))\,p(\mathbf{x},y)\,d\mathbf{x}\,dy}_{\textbf{generalization error — an EXPECTATION, an integral}}$$

**We can never calculate $R$.** Nobody tells us the precise form of $p(\mathbf{x},y)$, and we cannot sample an infinite stream. So we **estimate** it on a held-out test set — the *same formula* as the training error, applied to withheld data $\mathbf{X}',\mathbf{y}'$.

> [!important] The asymmetry that makes the test set work
> On the **test set** we evaluate a **fixed** classifier — one that does not depend on that sample — so estimating its error is **just the problem of mean estimation**, and it is unbiased.
>
> On the **training set** the model we ended up with **depends explicitly on that very sample**, so the training error is a **biased** estimate of population error. This is the whole reason a held-out set exists, and it is why the bias only appears once you *fit* — see Important Note 11.

**The IID assumption.** Training and test data are drawn **independently from identical distributions**. It is a strong assumption and, absent something like it, **we are dead in the water**: why should data from $P(X,Y)$ tell us anything about predictions on data from a different $Q(X,Y)$? Relaxing it requires strong assumptions relating $P$ and $Q$ — the subject of distribution shift in [[03 - Logistic Regression]].

#### 8.2 Model complexity, and Popper

If a model class is so expressive that for **any** dataset of $n$ examples it can fit **arbitrary labels — even randomly assigned ones** — then fitting your training data perfectly tells you nothing. Generalization error might be no better than random guessing. Conversely, **if the class could *not* fit arbitrary labels, then fitting yours means it found a pattern.**

D2L traces this to **Karl Popper's falsifiability**:

> A theory that can explain any and all observations is **not a scientific theory at all** — what has it told us about the world if it has ruled out no possibility? What we want is a hypothesis that **could not explain** most conceivable observations and yet **happens to be compatible with the ones we actually made.**

**What counts as complexity is genuinely unsettled.** More parameters often means more arbitrary labels fittable — *but not necessarily*: kernel methods work in spaces with **infinitely many parameters** and control complexity by other means. A notion that often works is **the range of values the parameters may take** — a model whose parameters may be arbitrary is more complex. **That is exactly the handle weight decay grabs (§9).** And comparing complexity *across* model classes (decision trees vs. neural networks) is often not meaningful at all.

> [!warning] The sentence students get backwards
> When a model can fit arbitrary labels, **low training error does not imply low generalization error — but it does not imply *high* generalization error either.** All you may conclude is that **low training error alone does not certify low generalization error.** Deep networks are exactly such models: they generalize well in practice and are too powerful to justify that from training error, so we lean on **holdout data to certify generalization after the fact.** Error on the holdout set is the **validation error**.

#### 8.3 Underfitting vs. overfitting

| Symptom | Diagnosis | Action |
|---|---|---|
| training error **and** validation error both substantial, **small gap** | **underfitting** — model too simple to capture the pattern | use a *more* complex model |
| training error **much lower** than validation error | **overfitting** | regularize, or get more data |

> [!note] Overfitting is not automatically a failure
> "In deep learning especially, **the best predictive models often perform far better on training data than on holdout data.**" We care about driving **generalization error** down, and about the *gap* only insofar as it obstructs that. Note the corner case: **if training error is zero, the generalization gap equals the generalization error exactly**, and the only way forward is to shrink the gap.

**Polynomial curve fitting** is the classical illustration. Fitting $\hat y = \sum_{i=0}^{d} x^i w_i$ is *still a linear regression* — the features are the powers of $x$, the bias is $w_0$ since $x^0=1$. Higher degree = more parameters = wider selection range, so **higher-degree polynomials always achieve lower (at worst equal) training error**. And decisively:

> **Whenever each example has a distinct value of $x$, a polynomial of degree equal to the number of examples fits the training set perfectly.**

$n$ points, $n$ parameters, zero training error, and nothing learned. (Exercise 3.)

**Dataset size.** Fixing the model, fewer samples ⇒ more likely and more severe overfitting; more data ⇒ generalization error typically falls. **More data never hurts.** The rule of thumb: **model complexity should not increase more rapidly than the amount of data.** For many tasks deep learning only beats linear models once **many thousands** of examples are available — which is why §6 of [[01 - Introduction to Deep Learning]] matters.

#### 8.4 Model selection, and the test set you are quietly ruining

Choosing among candidates (architectures, objectives, features, preprocessing, learning rates) is **model selection**. The rule:

> **Never use the test set for model selection.** If you overfit the training data, evaluation on test data keeps you honest. **But if you overfit the test data, how would you ever know?**

Yet we cannot select on training data either, since we cannot estimate generalization error on the data we fitted. Hence the **three-way split: train / validation / test.**

D2L is unusually candid about how badly this holds up in practice:

- Real test sets are **seldom discarded after one use**; we can rarely afford a fresh one per experiment.
- **Recycling benchmark data for decades** measurably shapes algorithm development (image classification, OCR).
- The boundary between validation and test data is **"a murky business… worryingly ambiguous"**.
- **"Unless explicitly stated otherwise, in the experiments in this book we are really working with training data and validation data, with no true test sets. Therefore the accuracy reported in each experiment of the book is really the validation accuracy."**

**$K$-fold cross-validation.** When data is too scarce to hold out a proper validation set: split the training data into $K$ non-overlapping subsets; train and validate $K$ times, each time training on $K-1$ subsets and validating on the held-out one; average the $K$ results. Cost: **$K$ times the training compute** (exercise ideas in §Important Notes).

**D2L's five rules of thumb, verbatim in substance:**
1. Use validation sets (or $K$-fold CV) for model selection.
2. More complex models require more data.
3. Relevant notions of complexity include **both the number of parameters and the range of values they may take**.
4. All else equal, more data almost always generalizes better.
5. **All of this is predicated on the IID assumption.** Relax it and, absent a further assumption, **we can say nothing about generalization at all.**

### 9. Weight decay — the first regularizer

More data always helps and is often unavailable, so: given the dataset as fixed, what can we do?

**Why not just delete features?** Limiting the polynomial degree works but is "too blunt an instrument". Consider **monomials** — products of powers of variables, degree = sum of the powers ($x_1^2x_2$ and $x_3x_5^2$ are both degree 3). With $k$ variables, the number of monomials of degree $d$ is
$$\binom{k-1+d}{k-1}$$

D2L says a change "from 2 to 3 dramatically increases complexity" and stops. **Put its own $k=200$ into its own formula:**

| Degree $d$ | Monomials with $k=200$ |
|---|---|
| 1 | 200 |
| 2 | 20,100 |
| 3 | **1,353,400** |
| 4 | 68,685,050 |

Going from degree 2 to 3 multiplies the parameter count by **67.33×**. Feature count is a **discrete, violently non-uniform** dial. We want a **continuous** one.

**Weight decay** ($\ell_2$ regularization, and *ridge regression* in statistics) turns the other knob from §8.2: instead of the *number* of parameters, restrict **the values they may take.** The intuition: among all functions, $f=0$ is the simplest, and we can measure a function's complexity by **how far its parameters are from zero**.

$$\boxed{L(\mathbf{w},b) + \frac{\lambda}{2}\|\mathbf{w}\|^2}$$

- $\lambda = 0$ recovers the original loss; $\lambda > 0$ restricts $\|\mathbf{w}\|$; larger $\lambda$ constrains more.
- $\lambda$ is a **non-negative hyperparameter fitted on validation data**.
- The $\tfrac12$ is again pure convenience — it cancels on differentiation.
- We use the **squared** norm to remove the square root, leaving a sum of squares whose derivative is trivial (the derivative of a sum is the sum of derivatives).

**The update becomes:**
$$\mathbf{w} \leftarrow (1-\eta\lambda)\,\mathbf{w} - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}}\mathbf{x}^{(i)}\left(\mathbf{w}^\top\mathbf{x}^{(i)}+b-y^{(i)}\right)$$

**That leading factor $(1-\eta\lambda)$ is the name.** Given the penalty alone, the optimizer *decays* the weight toward zero at every step — multiplicatively, geometrically. The data term then pushes back.

**$\ell_2$ versus $\ell_1$:**

| | $\ell_2$ (ridge / weight decay) | $\ell_1$ (lasso) |
|---|---|---|
| Penalty | $\|\mathbf{w}\|^2$ | $\sum_j|w_j|$ |
| Effect | **outsize penalty on large components** ⇒ spreads weight **evenly** across many features | **drives weights exactly to zero** ⇒ concentrates on a few |
| Buys you | robustness to measurement error in any single variable | **feature selection** — you need not collect, store or transmit the dropped features |

**The bias is usually not penalized**, though this varies across implementations and even across layers. In PyTorch, `weight_decay` on the optimizer decays weights *and* biases by default; D2L configures separate parameter groups so only `net.weight` decays. *(And note: $\ell_2$ regularization is not equivalent to weight decay for every optimizer — the idea survives, the exact equivalence does not. This matters for Adam; see [[04 - Neural Network]].)*

### 10. The experiment — and the number D2L prints without noticing

D2L builds a deliberately brutal synthetic problem:
$$y = 0.05 + \sum_{i=1}^{d} 0.01\,x_i + \epsilon, \qquad \epsilon\sim\mathcal{N}(0, 0.01^2)$$
with $d = 200$ features, **20 training examples** and 100 validation examples. **Ten times more parameters than data points**, trained for 10 epochs at batch size 5 — that is **40 SGD updates in total**.

It prints, from `l2_penalty(w)`:

| Run | Printed |
|---|---|
| scratch, $\lambda = 0$ | `0.009889112785458565` |
| scratch, $\lambda = 3$ | `0.0014726519584655762` |
| concise, `wd=3` | `0.01231398992240429` |

> [!warning] First, the label is wrong — read the code, not the caption
> The line prints `'L2 norm of w: '`, but `l2_penalty(w)` returns `(w**2).sum()/2`. **The printed quantity is $\tfrac12\|\mathbf{w}\|^2$, not $\|\mathbf{w}\|$.** Converting: $\lambda=0$ gives $\|\mathbf{w}\| = 0.1406$; $\lambda=3$ gives $0.0543$. The *ratio* of printed values is 6.72×, but the ratio of actual norms is only **2.59×** — quoting the printed numbers as norms overstates the shrinkage by a factor of 2.6.

**Now the result D2L walks straight past.** The true weight vector has 200 entries of exactly $0.01$, so the true value of the printed quantity is
$$\tfrac12\|\mathbf{w}_{\text{true}}\|^2 = \tfrac12 \times 200 \times (0.01)^2 = \mathbf{0.0100}$$

The **unregularized** run — the one D2L labels *"a textbook case of overfitting"* — prints **0.009889**, which is **1.11% from the truth**. The **regularized** run, the one that generalizes better, prints **0.001473**, which is **85% too small**.

I reproduced the whole experiment independently in NumPy (200 random seeds), which confirms both printed figures and lets us see the quantities D2L does not print:

| | $\tfrac12\|\mathbf{w}\|^2$ | $\|\hat{\mathbf{w}}-\mathbf{w}_{\text{true}}\|$ | $\cos\angle(\hat{\mathbf{w}},\mathbf{w}_{\text{true}})$ | train loss | val loss |
|---|---|---|---|---|---|
| $\lambda=0$ | **0.01007** *(truth: 0.0100)* | **0.1907** | **0.092** | 0.0000118 | 0.01924 |
| $\lambda=3$ | 0.00144 | 0.1410 | 0.195 | 0.000463 | **0.01096** |

*(Book prints 0.009889 and 0.001473; reproduction gives 0.01007 and 0.00144 — within 1.8% and 2.3%.)* And $\|\mathbf{w}_{\text{true}}\| = 0.1414$.

**Read the second and third columns.** The unregularized estimate has **almost exactly the right length** — and its estimation error, **0.1907, is larger than the vector it is estimating (0.1414)**, with a cosine of **0.092**, i.e. it sits about **84.7° away from the truth**. It is a right-sized arrow pointing in nearly a random direction. The regularized estimate is **7× too short** and is both **closer** (0.1410) and **twice as well aligned** (0.195), and it generalizes **1.76× better**.

> [!important] The chapter's sharpest lesson, and it generalizes far beyond this experiment
> **$\|\mathbf{w}\|$ being right does not make $\mathbf{w}$ right.** With 20 examples in 200 dimensions, the fit is confined to the 20-dimensional span of the training data; the other 180 directions are unconstrained by the data and filled in by noise and initialization. A norm is **one number summarizing 200**, and it is blind to direction.
>
> This is the vault's recurring finding in a new setting: **a headline number that is accurate and means something other than what it appears to mean.** And it is the same structural point as the correlation results in [[Commercial Banking/contents/00-Index|Commercial Banking]] — *a summary statistic can be exactly right while the thing it summarizes is exactly wrong.*

**The third number, and why it is not comparable to the second.** The concise run prints **0.012314** for `wd=3` — **8.4× larger** than the scratch run at the same nominal $\lambda=3$, and D2L comments only that "the plot looks similar". Investigating (see the errata note): the concise model uses `nn.MSELoss`, which **lacks the $\tfrac12$ factor** the scratch loss has, so the data gradient doubles relative to the penalty and the *effective* $\lambda$ halves; and, decisively, PyTorch's default `nn.Linear` initialization is $\mathcal{U}(-1/\sqrt d, 1/\sqrt d)$, giving an initial $\tfrac12\|\mathbf{w}\|^2$ of $\mathbf{0.1667}$ against the scratch model's `sigma=0.01` start of $0.0100$. Pure decay over 40 steps multiplies $\|\mathbf{w}\|^2$ by $(1-\eta\lambda)^{80} = 0.0875$, predicting $0.1667\times0.0875 = 0.0146$ — and simulating the concise configuration gives **0.0140** against the book's 0.0123.

> **So the concise run's printed value is dominated by its initialization, not by anything it learned.** Forty updates is nowhere near enough to forget where it started. The two numbers are printed adjacently, invite comparison, and **cannot be compared**.

## ✏️ Exercises

> [!example]- **1.** *(Easy — solve the normal equations by hand, and see what the $\tfrac12$ does)*
> Four houses, features (area, age) and an intercept column:
> $$\mathbf{X}=\begin{pmatrix}1&1&1\\2&1&1\\3&2&1\\4&2&1\end{pmatrix},\qquad \mathbf{y}=\begin{pmatrix}4\\7\\9\\13\end{pmatrix}$$
> **(a)** Form $\mathbf{X}^\top\mathbf{X}$ and $\mathbf{X}^\top\mathbf{y}$ and solve the normal equations.
> **(b)** Compute fitted values, residuals and SSE. What do the residuals sum to, and why?
> **(c)** If you had minimized $\sum_i (\hat y^{(i)}-y^{(i)})^2$ **without** the $\tfrac12$, what would change?
>
> ---
> **(a)**
> $$\mathbf{X}^\top\mathbf{X}=\begin{pmatrix}30&17&10\\17&10&6\\10&6&4\end{pmatrix},\quad \mathbf{X}^\top\mathbf{y}=\begin{pmatrix}97\\55\\33\end{pmatrix},\quad \det = 4$$
> Solving: $$\boxed{w_{\text{area}}=\tfrac72=3.5,\quad w_{\text{age}}=-\tfrac32=-1.5,\quad b=\tfrac74=1.75}$$
>
> **(b)** Fitted $=\left(\tfrac{15}{4},\tfrac{29}{4},\tfrac{37}{4},\tfrac{51}{4}\right)=(3.75,\,7.25,\,9.25,\,12.75)$; residuals $=\left(-\tfrac14,+\tfrac14,+\tfrac14,-\tfrac14\right)$; $\mathrm{SSE}=4\times\tfrac1{16}=\boxed{\tfrac14}$.
> The residuals **sum to zero**. This is forced by the normal equations: the row of $\mathbf{X}^\top(\mathbf{X}\mathbf{w}-\mathbf{y})=0$ corresponding to the **column of 1s** reads $\sum_i r_i = 0$. *Fitting an intercept guarantees it* — so it checks your algebra but proves nothing about the model (Important Note 8 in [[01 - Introduction to Deep Learning]]).
>
> **(c)** **Nothing about the answer; everything about the numbers.** The $\tfrac12$ multiplies the loss by a constant, so the argmin is identical — $\mathbf{w}$ is unchanged. What changes is that the *gradient* doubles, so at a fixed learning rate SGD takes steps twice as large, and the reported loss value doubles. That is not academic: it is exactly the mechanism behind the concise-vs-scratch discrepancy in §10.

> [!example]- **2.** *(Easy–medium — change the noise model, change the loss)*
> **(a)** For data $x_1,\dots,x_n\in\mathbb{R}$, find the constant $b$ minimizing $\sum_i(x_i-b)^2$. Relate it to the normal distribution.
> **(b)** Now minimize $\sum_i|x_i-b|$ instead. What is the optimum, and which noise model does it correspond to?
> **(c)** Demonstrate on $\{2,4,4,5,10\}$.
> **(d)** D2L's exercise 5 assumes noise $p(\epsilon)=\tfrac12\exp(-|\epsilon|)$. Write the negative log-likelihood, and say what goes wrong with SGD near the optimum.
>
> ---
> **(a)** $\frac{d}{db}\sum_i(x_i-b)^2 = -2\sum_i(x_i-b) = 0 \Rightarrow \boxed{b=\bar x}$, the **mean**. This is exactly §4 with no features: the model is a constant, the noise is Gaussian, and **the sample mean is the MLE of a Gaussian's location parameter.** Squared loss ⟺ Gaussian ⟺ mean.
>
> **(b)** $\frac{d}{db}\sum_i|x_i-b| = \sum_i(-\operatorname{sign}(x_i-b))$, which is zero when equally many points lie above and below: $\boxed{b = \text{median}}$. The corresponding noise model is the **Laplace** distribution $p(\epsilon)\propto e^{-|\epsilon|}$ — whose negative log-likelihood *is* $\sum_i|x_i-b|$ up to constants. **Absolute loss ⟺ Laplace ⟺ median.**
>
> **(c)** Mean $=\tfrac{2+4+4+5+10}{5}=\boxed{5}$; median $=\boxed{4}$. Check the $\ell_1$ objective: $\sum|x_i-4| = 2+0+0+1+6=\mathbf{9}$; $\sum|x_i-4.5|=9.5$; $\sum|x_i-5|=3+1+1+0+5=\mathbf{10}$. The median wins, and note **the mean is dragged upward by the single point at 10** while the median ignores it — the quadratic's outlier sensitivity from §2, made concrete.
>
> **(d)** With $p(\epsilon)=\tfrac12 e^{-|\epsilon|}$,
> $$-\log P(\mathbf{y}\mid\mathbf{X}) = n\log 2 + \sum_{i=1}^n\left|y^{(i)}-\mathbf{w}^\top\mathbf{x}^{(i)}-b\right|$$
> so **Laplace noise gives $\ell_1$ regression** — no closed-form solution in general. The SGD problem: the gradient of $|r|$ is $\pm1$ **regardless of how small $|r|$ is**. It **does not vanish at the optimum**, so with a fixed learning rate the iterate oscillates around the minimum forever in a band of width $O(\eta)$ instead of settling. **Fix: decay the learning rate** ($\eta_t\to0$, e.g. $\eta_t\propto1/\sqrt t$), or smooth the kink (Huber loss). This is the first appearance of learning-rate scheduling, which returns in [[04 - Neural Network]].

> [!example]- **3.** *(Medium — why you cannot regularize by deleting features)*
> **(a)** With $k$ variables, how many monomials have degree exactly $d$? Evaluate for $k=200$ and $d=1,2,3$.
> **(b)** A polynomial of degree $d$ is fitted to $n$ points with distinct $x$ values. For which $d$ is training error exactly zero, and what is the model worth?
> **(c)** Using (a) and (b), explain in one sentence why weight decay is preferable to choosing a degree.
>
> ---
> **(a)** $\dbinom{k-1+d}{k-1}$. For $k=200$: $d=1 \Rightarrow \binom{200}{199} = \mathbf{200}$; $d=2 \Rightarrow \binom{201}{199} = \tfrac{201\cdot200}{2} = \mathbf{20{,}100}$; $d=3 \Rightarrow \binom{202}{199} = \tfrac{202\cdot201\cdot200}{6} = \mathbf{1{,}353{,}400}$. Stepping degree 2 → 3 multiplies the parameter count by $\mathbf{67.33\times}$.
>
> **(b)** $d = n-1$ already interpolates $n$ points with distinct abscissae exactly (a unique interpolating polynomial exists), and any $d\ge n-1$ gives **zero training error**. The model is worth **nothing**: it has $n$ free parameters fitting $n$ numbers, has ruled out no possible observation, and by §8.2's Popper criterion is not a scientific hypothesis at all. Note the corner case from §8.3 — with zero training error, the **generalization gap equals the generalization error**.
>
> **(c)** Because degree is a **discrete dial whose steps multiply capacity by tens or hundreds** (67× here) and jumps straight from underfitting to exact interpolation, whereas $\lambda$ is a **continuous dial** on the same underlying quantity (§8.2's "range of values the parameters may take") that can be tuned to any point in between.

> [!example]- **4.** *(Medium–hard — what full rank is actually protecting you from)*
> Use $\mathbf{X}$ from exercise 1.
> **(a)** Compute $\operatorname{corr}(\text{area},\text{age})$ and the condition number of $\mathbf{X}^\top\mathbf{X}$. Is the design "full rank"?
> **(b)** Perturb $y_2$ from 7 to 7.1 and recompute $\mathbf{w}$. How far does it move?
> **(c)** Repeat (b) with ridge, $\lambda=1$. Compare, and report $\mathbf{w}_{\text{ridge}}$ itself.
> **(d)** In terms of the SVD $\mathbf{X}=\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$, show why ridge fixes this, and give the shrinkage per singular direction.
>
> ---
> **(a)** $\operatorname{corr} = \mathbf{0.8944}$ — strongly collinear. Singular values of $\mathbf{X}$ are $(6.572,\,0.8185,\,0.3718)$, so $\kappa(\mathbf{X}) = 17.68$ and $\kappa(\mathbf{X}^\top\mathbf{X}) = \mathbf{312.46}$. Technically $\det(\mathbf{X}^\top\mathbf{X}) = 4 \ne 0$, so it **is** full rank — **and that is the point**: the theoretical condition is satisfied while the practical situation is already bad. Rank is a yes/no test; conditioning is the quantity that matters.
>
> **(b)** OLS moves from $(3.5,-1.5,1.75)$ by $\Delta\mathbf{w} = (0.05,-0.15,0.125)$, i.e. $\|\Delta\mathbf{w}\| = \mathbf{0.2016}$. **A perturbation of 0.1 in one label moved the parameters by twice that** — and note it is the *age* coefficient, the collinear one, that moves most (−0.15).
>
> **(c)** With $\lambda=1$ the same perturbation gives $\|\Delta\mathbf{w}\| = \mathbf{0.0278}$ — a **7.25× reduction in sensitivity**. The ridge solution itself is
> $$\mathbf{w}_{\text{ridge}} = \left(\tfrac{17}{7},\,\tfrac{6}{7},\,\tfrac{5}{7}\right) \approx (2.429,\,+0.857,\,0.714)$$
> **The age coefficient has flipped sign, from −1.5 to +0.857.** SSE rises from $0.25$ to $1.571$ (6.29×) while $\|\mathbf{w}\|^2$ falls from $17.56$ to $7.14$ (÷2.46). *A coefficient's sign under collinearity is not a fact about the world.*
>
> **(d)** Writing $\mathbf{X}=\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$, the two solutions are
> $$\mathbf{w}_{\text{OLS}} = \sum_j \frac{1}{\sigma_j}\left(\mathbf{u}_j^\top\mathbf{y}\right)\mathbf{v}_j, \qquad \mathbf{w}_{\text{ridge}} = \sum_j \frac{\sigma_j}{\sigma_j^2+\lambda}\left(\mathbf{u}_j^\top\mathbf{y}\right)\mathbf{v}_j$$
> so ridge multiplies each direction by
> $$\boxed{\frac{\sigma_j^2}{\sigma_j^2+\lambda}}$$
> For this design at $\lambda=1$ the three factors are $\mathbf{0.977},\ \mathbf{0.401},\ \mathbf{0.121}$. **Well-determined directions pass through essentially untouched; poorly-determined ones are crushed.** In the OLS formula the $1/\sigma_j$ **blows up** as $\sigma_j\to0$ — that is exactly the rank-deficiency failure — whereas the ridge coefficient $\sigma_j/(\sigma_j^2+\lambda)\to0$. **Ridge does not just shrink; it shrinks *selectively*, and adding $\lambda\mathbf{I}$ makes $\mathbf{X}^\top\mathbf{X}+\lambda\mathbf{I}$ invertible even when $\mathbf{X}^\top\mathbf{X}$ is not.**

> [!example]- **5.** *(Hard — audit D2L's weight-decay experiment)*
> The experiment: $d=200$, $n_{\text{train}}=20$, true $w_i=0.01$ for all $i$, $b=0.05$, noise $\sigma=0.01$; 10 epochs, batch size 5, $\eta=0.01$. D2L prints `l2_penalty(w)` $=0.009889$ for $\lambda=0$ and $0.001473$ for $\lambda=3$.
> **(a)** What quantity is actually printed? Convert both to $\|\mathbf{w}\|$.
> **(b)** Compute the **true** value of the printed quantity. Compare both runs to it.
> **(c)** (b) appears to say the unregularized model recovered the truth. Show that it did not.
> **(d)** How many SGD updates does this run perform, and why does that matter for the third printed number (`wd=3` → 0.012314)?
>
> ---
> **(a)** `l2_penalty(w)` is `(w**2).sum()/2`, i.e. $\tfrac12\|\mathbf{w}\|^2$ — **not the norm**, despite the printed caption `'L2 norm of w: '`. So $\|\mathbf{w}\| = \sqrt{2\times\text{printed}}$: $\lambda=0 \Rightarrow \boxed{0.1406}$, $\lambda=3\Rightarrow\boxed{0.0543}$. The printed values differ by 6.72× but the norms only by **2.59×**.
>
> **(b)** $\tfrac12\|\mathbf{w}_{\text{true}}\|^2 = \tfrac12\cdot200\cdot(0.01)^2 = \mathbf{0.0100}$. So $\lambda=0$ printed $0.009889$ — **1.11% below the truth**; $\lambda=3$ printed $0.001473$ — **85.3% below**. Taken at face value, the *un*regularized model looks like the accurate one.
>
> **(c)** Because a norm is one number summarizing 200 and is **blind to direction**. Reproducing the experiment (200 seeds) gives, for $\lambda=0$, an estimation error $\|\hat{\mathbf{w}}-\mathbf{w}_{\text{true}}\| = \mathbf{0.1907}$ — **larger than $\|\mathbf{w}_{\text{true}}\| = 0.1414$ itself**, at a cosine of $\mathbf{0.092}$, i.e. about **84.7° from the truth**. Predicting $\hat{\mathbf{w}}=\mathbf{0}$ would have had smaller error. For $\lambda=3$: error $0.1410$, cosine $0.195$ — **closer and twice as well aligned despite being 7× too short**, with validation loss $0.01096$ against $0.01924$, i.e. **1.76× better**.
> The mechanism: with 20 examples in 200 dimensions the fit is pinned only within the **20-dimensional span of the training data**; the remaining **180 directions are unconstrained** and get filled with noise and initialization. The unregularized estimate is a right-sized arrow pointing almost anywhere.
>
> **(d)** $10 \text{ epochs} \times \lfloor 20/5\rfloor = \mathbf{40}$ updates — **for 200 parameters**. That is far too few to converge, so *where the run started still dominates where it ends*. The concise model uses `nn.LazyLinear`, initialized $\mathcal{U}(-1/\sqrt{200},1/\sqrt{200})$, giving an **initial** $\tfrac12\|\mathbf{w}\|^2$ of $\tfrac{200}{3}\cdot\tfrac{1}{200}\cdot\tfrac12 = \mathbf{0.1667}$ — versus the scratch model's `sigma=0.01` start of $0.0100$. Pure decay multiplies $\|\mathbf{w}\|^2$ by $(1-\eta\lambda)^{2\times40} = 0.0875$, predicting $0.1667\times0.0875 = \mathbf{0.0146}$; simulating the full concise configuration gives $\mathbf{0.0140}$ against the printed $0.0123$. *(A second, smaller factor: `nn.MSELoss` omits the $\tfrac12$, doubling the data gradient and halving the effective $\lambda$.)*
> **Conclusion: the concise run's printed value is essentially its initialization, decayed — not something it learned.** D2L prints it next to the scratch value at the same nominal $\lambda$ and remarks that "the plot looks similar"; **the two numbers are not comparable at all.**

## 📝 Summary

- **The model is affine**, $\hat y=\mathbf{w}^\top\mathbf{x}+b$, and vectorizes to $\hat{\mathbf{y}}=\mathbf{X}\mathbf{w}+b$ over the design matrix (rows = examples, columns = features). Absorbing $b$ as a column of 1s makes affine functions of $\mathbf{x}$ exactly linear functions of $(\mathbf{x},1)$.
- **Squared loss is not a convention — it is a consequence.** Assume additive Gaussian noise, write the likelihood, take $-\log$: the constant term drops, $\sigma$ cancels, and what remains is MSE. **Minimizing MSE = maximum likelihood under Gaussian noise.** Change the noise model and the loss changes: Laplace ⟹ $\ell_1$ ⟹ the median.
- **The normal equations $\mathbf{X}^\top\mathbf{X}\mathbf{w}=\mathbf{X}^\top\mathbf{y}$ give the only closed-form solution you will meet in this course.** They require full rank — and full rank is a yes/no test that says nothing about conditioning, which is what actually bites.
- **Minibatch SGD is the compromise between an unaffordable full batch and a cache-hostile single example**: sample $\mathcal{B}_t$, average the gradient, step by $\eta$. Batch 32–256 is a sane default. Each example pushes the weights along its own feature vector scaled by its residual, so well-predicted examples contribute nothing.
- **You will not hit the minimizer, and the answer is not even deterministic** — minibatches are random. It does not matter: the hard problem is not minimizing training loss, it is **generalization**.
- **Vectorize.** D2L's own benchmark, divided, is **93.23×** — and per element the arithmetic is **0.0060%** of the loop's cost, so **99.994% of it is interpreter overhead**. You are not speeding up the maths; you are deleting Python from the inner loop.
- **Training error is a statistic and generalization error is an integral you can never compute.** The test set works only because the model is *fixed* with respect to it, making evaluation ordinary mean estimation; training error is biased precisely because the model was chosen using it. All of this **rests on IID** — relax it and you can say nothing.
- **Complexity is not just parameter count; it is also the range parameters may take** — which is the handle weight decay grabs. Adding $\tfrac{\lambda}{2}\|\mathbf{w}\|^2$ makes the update $\mathbf{w}\leftarrow(1-\eta\lambda)\mathbf{w}-\dots$, a geometric decay the data must push back against. In the SVD basis it shrinks direction $j$ by $\sigma_j^2/(\sigma_j^2+\lambda)$ — **crushing the ill-determined directions and leaving the well-determined ones alone.**
- **A norm is one number summarizing many, and it is blind to direction.** In D2L's own experiment the *overfitting* model's $\tfrac12\|\mathbf{w}\|^2$ lands **1.11% from the true value** while its estimation error **exceeds the size of the vector it estimates** and it sits **84.7° away** from it. The regularized model is 7× too short, better aligned, and generalizes 1.76× better.

## ⚠️ Important Notes

1. **"Linear regression" is affine regression.** The bias is not optional decoration — without it you can only fit hyperplanes through the origin. Absorb it into $\mathbf{w}$ with a column of 1s and never think about it again.
2. **Superscripts are examples, subscripts are coordinates.** $x^{(i)}_j$. Getting this backwards makes every subsequent formula unreadable, and D2L never restates it.
3. **The $\tfrac12$ in the loss and the $\tfrac12$ in the penalty are both pure convenience** — they cancel on differentiation. They do not change the minimizer. **They do change the gradient by a factor of 2**, hence the effective step size, hence what a fixed number of SGD iterations produces. That is not pedantry: it is half the explanation of §10's third number.
4. **The empirical loss is a function of the parameters, with the data held fixed.** If you find yourself differentiating with respect to $x$, you have lost the plot.
5. **Full rank is necessary for uniqueness, not for sanity.** In exercise 4 the design is full rank ($\det=4$) and already so ill-conditioned ($\kappa = 312$) that a 0.1 nudge in one label moves the parameters by 0.20 and **ridge flips the sign of a coefficient**. Report conditioning, not rank.
6. **Squared loss is outlier-sensitive by construction**, and D2L flags this itself ("a double-edged sword"). One point at distance 10 counts as much as 100 points at distance 1. The right fix is not to clip the data but to **change the noise model** — Laplace/Huber — which is a modelling decision, not a hack.
7. **A closed-form solution is a luxury of this chapter only.** Do not build intuitions that depend on it. Deep loss surfaces have many saddle points and many minima, and "the" optimum stops being a meaningful phrase from [[04 - Neural Network]] onward.
8. **SGD's output is random.** Two runs with the same hyperparameters give different parameters, and reporting a single run's number as *the* result is the most common self-deception in this subject. Average over seeds — the results in §10 use 200.
9. **A hyperparameter is anything not updated inside the training loop** — learning rate, batch size, $\lambda$, architecture. Tune them on **validation** data, never test.
10. **Never select a model on the test set.** "If we overfit our training data, there is always the evaluation on test data to keep us honest. **But if we overfit the test data, how would we ever know?**" And note D2L's own confession: the accuracies printed throughout the book are **validation** accuracies, not true test accuracies.
11. **Training error is biased *because you fitted on it*, not because it is computed differently.** The formula is identical to the test error's. The bias comes entirely from the dependence of $f$ on the sample. Students who think the training set is somehow "easier data" have the mechanism wrong.
12. **Low training error neither implies nor contradicts low generalization error** when the model class can fit arbitrary labels. The only valid conclusion is that **training error alone certifies nothing.**
13. **A degree-$(n-1)$ polynomial fits $n$ distinct points exactly and has learned nothing.** By Popper's criterion in §8.2 it is not even a hypothesis, because it ruled out no possible observation.
14. **More parameters is a *proxy* for complexity, not a definition.** Kernel methods have infinitely many parameters and controlled complexity; large networks often generalize *better* than small ones. D2L flags this as "implicit and counterintuitive", and it is an open research area — do not assert the naive version in an exam.
15. **Read what the code prints, not what the caption says.** D2L's `'L2 norm of w: '` prints $\tfrac12\|\mathbf{w}\|^2$. Quoting those figures as norms overstates the shrinkage by 2.6×. **When a source prints a number, find the line that computed it.**
16. **Comparing two runs requires that everything except the intended variable be equal.** §10's scratch and concise runs differ in loss scaling *and* initialization *and* random seed, and are 8.4× apart at the same nominal $\lambda$. **Hold the first-order thing fixed to isolate the second** — the same rule that produced the convexity result in [[Commercial Banking/contents/00-Index|Commercial Banking]].
17. **Forty updates for 200 parameters is not a converged model**, it is a lightly perturbed initialization. Before interpreting any trained quantity, ask how many steps produced it.
18. **$\ell_2$ regularization and weight decay coincide for plain SGD and *not* for every optimizer.** D2L says so in one clause and moves on; it becomes a real bug with Adam (AdamW exists for exactly this reason) — see [[04 - Neural Network]].
19. **Bias terms are usually left unpenalized**, but implementations disagree, and PyTorch's `weight_decay` decays them by default unless you build separate parameter groups. Check, do not assume.
20. **Regularization trades training fit for generalization, and the trade is visible in the numbers**: in §10, training loss *rose* 39× (0.0000118 → 0.000463) while validation loss *fell* 1.76×. **A regularizer that does not increase training error is not regularizing.**

> [!warning] Gaps in the source material
> **Figures — all lost.** Fig. 3.1.1 (a linear fit to 1-D data), Fig. 3.1.2 (linear regression as a single-layer network), Fig. 3.1.3 (the biological neuron), Fig. 3.6.1 (model complexity vs. under/overfitting), and every training curve in §3.4–3.7 are images and do not extract. **Applying the vault's figure rule:** Fig. 3.1.2 and 3.1.3 are **label-schematics whose content is their labels**, and the prose names every one (inputs $x_1..x_d$, output $o_1$; dendrites/nucleus/axon/axon terminals/synapses) — both are **fully reconstructed above**. Fig. 3.1.1 and Fig. 3.6.1 are **curve geometry and are genuinely lost**; Fig. 3.6.1's content (training error falling monotonically with complexity, validation error U-shaped) is stated in the prose and reproduced in §8.3, but *the position of the minimum is not recoverable*. **The training-curve plots in the weight-decay experiment are lost, and this matters** — D2L's claims that "we overfit badly" and "the training error increases but the validation error decreases" are supported **only** by those plots. I therefore reproduced the experiment independently (below) rather than taking them on trust.
>
> **Printed code outputs survived**, which is what made §10 checkable: `0.16781 sec`, `0.00180 sec`, and the three `l2_penalty` values.
>
> **Mathematics is reconstructed, never transcribed.** Equation (3.1.10) extracts as `(w; b) (w; b)   jBj ∑ i2B t @(w;b)l(i)(w; b)` — with the assignment arrow, the minus sign, $\eta$ and the fraction bar all **deleted**. Every formula above was rebuilt from the prose and checked numerically. See this subject's `CLAUDE.md`.
>
> **Added beyond D2L, and labelled as mine throughout:**
> - **The division of D2L's own vectorization timings** (§6): 93.23×, 16.781 µs vs 0.180 µs, and the 0.0060% / 0.56% arithmetic fractions. The book prints both times and says only "order-of-magnitude speedups".
> - **The monomial table at $k=200$** (§9): 200 / 20,100 / 1,353,400, and the **67.33×** step from degree 2 to 3. D2L gives the formula and the words "dramatically increase", and never substitutes its own $d=200$.
> - **The entire audit of the weight-decay experiment** (§10 and exercise 5) — that the printed quantity is $\tfrac12\|\mathbf{w}\|^2$ and not the norm; that its true value is exactly 0.0100; the independent 200-seed NumPy reproduction (0.01007 and 0.00144, within 1.8% and 2.3% of the printed values); the estimation errors, cosines and validation losses; and the initialization explanation of the concise run. **None of this is in the book**, which prints three numbers and comments on none of them.
> - **Exercise 4 in full** — the correlation (0.894), condition number (312.46), perturbation sensitivities (0.2016 vs 0.0278, a 7.25× reduction), the sign flip of $w_{\text{age}}$, and the **SVD shrinkage factor $\sigma_j^2/(\sigma_j^2+\lambda)$** with its three values. D2L's exercise 4 *asks* what happens without full rank and supplies no answer.
> - **The Laplace/median derivation** in exercise 2 and the SGD-oscillation diagnosis. D2L poses this as exercise 5 (parts 1–3) without solutions.
>
> **Left as the source states it:** the citations (Gauss 1809, Legendre 1805, Bottou 2010, Li et al. 2014, and the rest); the batch-size advice of 32–256; the claim that matrix–vector multiplication is "up to an order of magnitude" more efficient than the equivalent vector–vector operations, which is hardware-dependent and not verifiable here.
>
> **Deliberately deferred, not omitted:** D2L §3.2–3.5 (the object-oriented `Module`/`DataModule`/`Trainer` API, synthetic data generation, and the from-scratch and concise implementations) are **framework scaffolding rather than theory**, and are used in this note only where they carry a result — the `l2_penalty` definition and the initialization defaults in §10. §3.6.3's $K$-fold cross-validation is stated but not implemented; it returns in [[04 - Neural Network]] with the Kaggle house-price example (D2L §5.7). **Convexity and convergence rates belong to [[Optimization/contents/00-Index|Optimization]]** and are not re-derived here.

**Previous:** [[01 - Introduction to Deep Learning]] · **Next:** [[03 - Logistic Regression]]
