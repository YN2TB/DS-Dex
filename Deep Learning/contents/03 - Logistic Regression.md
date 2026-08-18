---
subject: Deep Learning
chapter: 3
tags: [ds, deep-learning, classification, softmax, cross-entropy, distribution-shift]
source: "Zhang, Lipton, Li & Smola — Dive into Deep Learning, §4.1–4.7 (book pp. 127–169)"
---

# Logistic Regression

> [!info] Naming — read this first
> The syllabus topic is *Logistic Regression*; D2L's chapter is *Softmax Regression*. **They are the same model.** Softmax regression over $q$ classes reduces **exactly** to binary logistic regression when $q=2$ (proved in §7 and exercise 2). This note treats the general case and derives the binary one as the special case, because everything interesting — cross-entropy, the gradient, the information theory — is identical.
>
> D2L's own framing: *"most of the plumbing remains the same"* as [[02 - Linear Regression]] — load data, forward pass, compute loss, take gradients, update. **What changes is exactly three things: the form of the targets, the parametrization of the output layer, and the loss function.**

## 📘 Main Knowledge

### 1. Why regression is the wrong hammer

Regression answers *how much?* and *how many?*. But D2L is careful that even genuinely numerical targets often break its assumptions:

- **House prices are never negative**, and changes are typically *relative* to a baseline ⇒ regress on $\log(\text{price})$.
- **Days in hospital** is a **discrete non-negative** random variable ⇒ least squares is not ideal; this is *time-to-event* modelling, handled by the subfield of **survival modelling**.

*(These are D2L §3.1.6 exercise 7–8 made explicit; both are recorded in the gaps callout of [[02 - Linear Regression]].)*

Classification answers **which category?** — spam or inbox; sign up or not; donkey, dog, cat or rooster.

> [!note] "Classification" is overloaded, and D2L flags it
> Practitioners use one word for two subtly different problems: **(i) hard assignments** of examples to categories, and **(ii) soft assignments** — the probability that each category applies. The distinction blurs because **even when we only care about hard assignments we still use models that make soft ones.** ([[01 - Introduction to Deep Learning]] §4.1 explains why: the decision needs probabilities *and* a loss matrix.)
>
> And more than one label may be true — a news article can be about entertainment, business *and* spaceflight. That is **multi-label classification**, not multi-class.

### 2. Representing the labels: one-hot encoding

Running example: a $2\times2$ grayscale image, so four features $x_1,x_2,x_3,x_4$, belonging to one of *cat*, *chicken*, *dog*.

The tempting choice is $y\in\{1,2,3\}$. It is a fine way to *store* the information and a bad way to *model* it, because **it invents an ordering that does not exist** — it asserts that chicken is between cat and dog, and that $\text{dog}-\text{cat}=2\times(\text{chicken}-\text{cat})$.

> [!important] When the ordering is real, use it
> If the categories were $\{\text{baby},\text{toddler},\text{adolescent},\text{young adult},\text{adult},\text{geriatric}\}$ **there is a natural ordering**, and it may be right to keep integer labels and treat the task as **ordinal regression**. Throwing away a real ordering is as much an error as inventing a false one.

For unordered categories, statisticians long ago settled on the **one-hot encoding**: a vector with one component per category, 1 in the component for this instance's class and 0 elsewhere.
$$\mathbf{y}\in\{(1,0,0),\,(0,1,0),\,(0,0,1)\}$$

**Why it is the right representation:** it is *permutation-symmetric* — no class is closer to any other — and, as §4 shows, it makes the loss pick out exactly one term.

### 3. The linear model: one affine function per class

To estimate a conditional probability for every class we need **as many outputs as classes**, hence as many affine functions. With 4 features and 3 categories that is $4\times3=12$ weights and 3 biases:
$$\begin{aligned}
o_1 &= x_1w_{11}+x_2w_{12}+x_3w_{13}+x_4w_{14}+b_1\\
o_2 &= x_1w_{21}+x_2w_{22}+x_3w_{23}+x_4w_{24}+b_2\\
o_3 &= x_1w_{31}+x_2w_{32}+x_3w_{33}+x_4w_{34}+b_3
\end{aligned}$$
or compactly $\mathbf{o}=\mathbf{W}\mathbf{x}+\mathbf{b}$ with $\mathbf{W}\in\mathbb{R}^{3\times4}$, $\mathbf{b}\in\mathbb{R}^3$.

**This is again a single-layer network** — and because every output depends on every input, the output layer is **fully connected**.

> [!warning] The parametrization is deliberately redundant, by exactly one degree of freedom
> D2L: *"Strictly speaking, we only need one fewer, since the final category has to be the difference between 1 and the sum of the other categories, but **for reasons of symmetry we use a slightly redundant parametrization**."*
>
> This is not a footnote. It is why **softmax is translation-invariant** (§8), why the binary case collapses to a *single* sigmoid of a *difference* (§7), and why the weights of a softmax layer are never unique — you can add any constant to a whole row of $\mathbf{W}$ and $\mathbf{b}$ without changing a single prediction. **Never interpret an individual softmax logit; only differences are meaningful.**

**Minibatched:** with $\mathbf{X}\in\mathbb{R}^{n\times d}$, $\mathbf{W}\in\mathbb{R}^{d\times q}$, $\mathbf{b}\in\mathbb{R}^{1\times q}$,
$$\mathbf{O}=\mathbf{X}\mathbf{W}+\mathbf{b},\qquad \hat{\mathbf{Y}}=\operatorname{softmax}(\mathbf{O})$$
which turns the dominant operation into a **matrix–matrix product** and lets softmax be applied **rowwise**. (Recall [[02 - Linear Regression]] §6: the whole point is deleting Python from the inner loop.)

### 4. The softmax

Why not just regress the one-hot vector directly with squared loss? It "works surprisingly well" and is unsatisfactory:

- nothing forces the outputs $o_i$ to **sum to 1**;
- nothing forces them to be **non-negative**, or $\le 1$.

D2L's illustration: if there is a positive linear dependence between bedrooms and the likelihood of buying, **the probability exceeds 1 when it comes to a mansion.** Both defects make the estimation problem hard and the solution **brittle to outliers**. We need to "squish" the outputs.

**One alternative D2L names and rejects:** assume $\mathbf{y}=\mathbf{o}+\boldsymbol{\epsilon}$ with Gaussian $\epsilon_i$ — the **probit** model of Fechner (1860). Appealing, but it does not work as well nor lead to as nice an optimization problem.

**The softmax.** Take $P(y=i)\propto\exp o_i$: this is monotone in $o_i$, guarantees non-negativity, and normalizes by dividing by the sum:
$$\boxed{\hat{\mathbf{y}}=\operatorname{softmax}(\mathbf{o}),\qquad \hat y_i=\frac{\exp(o_i)}{\sum_j\exp(o_j)}}$$

**Softmax preserves order.** The largest coordinate of $\mathbf{o}$ is the most likely class, so
$$\operatorname*{argmax}_j \hat y_j=\operatorname*{argmax}_j o_j$$
⇒ **at prediction time you never need to compute the softmax at all** — take the argmax of the logits. (The softmax is needed for the *loss*, not the *decision*.)

> [!note] Where softmax comes from: statistical physics
> The idea dates to **Gibbs (1902)**, adapting **Boltzmann**, who found that the prevalence of an energy state in a thermodynamic ensemble is proportional to $\exp(-E/kT)$ — $E$ the energy, $T$ the temperature, $k$ Boltzmann's constant. Statisticians "raising or lowering the temperature" are changing $T$ to favour higher or lower energy states.
>
> **Following Gibbs' idea, energy equates to error.** This is the whole basis of **energy-based models** (Ranzato et al., 2007). Temperature is worked out quantitatively in exercise 4's companion note below and in §Important Notes 9.

### 5. Cross-entropy, derived the same way as squared loss

We use the *same* tool as [[02 - Linear Regression]] §4: **maximum likelihood**. Softmax gives $\hat y_1=P(y=\text{cat}\mid\mathbf{x})$, so the likelihood of the dataset factorizes over independent examples:
$$P(\mathbf{Y}\mid\mathbf{X})=\prod_{i=1}^n P\!\left(\mathbf{y}^{(i)}\mid\mathbf{x}^{(i)}\right)$$
Take $-\log$ to turn the product into a sum and maximization into minimization:
$$-\log P(\mathbf{Y}\mid\mathbf{X})=\sum_{i=1}^n -\log P\!\left(\mathbf{y}^{(i)}\mid\mathbf{x}^{(i)}\right)=\sum_{i=1}^n \ell\!\left(\mathbf{y}^{(i)},\hat{\mathbf{y}}^{(i)}\right)$$
with the per-example **cross-entropy loss**
$$\boxed{\ell(\mathbf{y},\hat{\mathbf{y}})=-\sum_{j=1}^{q}y_j\log\hat y_j}$$

**Because $\mathbf{y}$ is one-hot, every term vanishes but one** — the loss is just $-\log$ of the probability the model assigned to the true class.

**Bounds.** $\ell\ge0$ whenever $\hat{\mathbf{y}}$ is a probability vector (no entry exceeds 1, so no negative log is below 0), and $\ell=0$ **only** on predicting the true label with certainty. That can never happen for finite weights: driving a softmax output to 1 requires sending $o_i\to+\infty$ (or all others to $-\infty$).

> [!warning] And this is the danger
> *"Even if our model could assign an output probability of 0, any error made when assigning such high confidence would incur infinite loss"* — $-\log 0=\infty$. **Cross-entropy punishes confident mistakes without bound.** It is why overconfident models blow up training, and why label smoothing and gradient clipping exist.

**Substituting the softmax into the loss** gives the form actually used in code:
$$\ell(\mathbf{y},\hat{\mathbf{y}})=\log\sum_{k=1}^q\exp(o_k)-\sum_{j=1}^q y_jo_j$$
— note it is written **entirely in logits**, with no division and no explicit exponential ratio. That is not cosmetic; it is the numerically stable form (§8).

### 6. The gradient — and why it looks exactly like regression

Differentiate with respect to any logit $o_j$:
$$\boxed{\partial_{o_j}\,\ell(\mathbf{y},\hat{\mathbf{y}})=\frac{\exp(o_j)}{\sum_k\exp(o_k)}-y_j=\operatorname{softmax}(\mathbf{o})_j-y_j}$$

**The gradient is the difference between what the model believed and what actually happened.** Compare [[02 - Linear Regression]]: there the gradient was $\hat y - y$ too.

> [!important] This is not a coincidence
> D2L: *"In any **exponential family** model, the gradients of the log-likelihood are given by precisely this term."* Predicted-minus-observed is a structural fact about exponential families, not a lucky cancellation — and it is why gradients are cheap for this entire class of models.

**Second derivative.** The Hessian of the loss in the logits is
$$\nabla^2_{\mathbf{o}}\,\ell=\operatorname{diag}(\hat{\mathbf{y}})-\hat{\mathbf{y}}\hat{\mathbf{y}}^\top$$
which is exactly the **covariance matrix of the distribution $\hat{\mathbf{y}}$**. *(Verified symbolically; this answers D2L's exercise 1, which asks for both and for the proof that they match.)* Two consequences: the log-partition function $g(\mathbf{x})=\log\sum_i\exp x_i$ is **convex** (a covariance is positive semi-definite), and **the curvature is largest when the model is most uncertain** and vanishes as it becomes confident — so a confidently wrong model has a large gradient and almost no curvature.

**Soft labels work unchanged.** Replace the one-hot $(0,0,1)$ with a generic probability vector like $(0.1,0.2,0.7)$ and the same formula still applies; it is then the **expected loss under a distribution over labels**. This is exactly what label smoothing and knowledge distillation exploit.

### 7. The binary case: this is logistic regression

Set $q=2$:
$$\hat y_1=\frac{e^{o_1}}{e^{o_1}+e^{o_2}}=\frac{1}{1+e^{-(o_1-o_2)}}=\sigma(o_1-o_2)$$

> **Softmax over two classes is the logistic sigmoid applied to the difference of the logits.** Only $o_1-o_2$ matters — the redundant degree of freedom of §3, made visible.

So binary logistic regression is the $q=2$ instance of everything above: same cross-entropy, same gradient $\hat y - y$, same information-theoretic reading. In the binary case the cross-entropy is usually written
$$\ell=-\big[y\log\hat y+(1-y)\log(1-\hat y)\big]$$
which is just the two-term expansion of $-\sum_j y_j\log\hat y_j$.

D2L uses this fact concretely in §10.2: **covariate-shift correction needs a density ratio, and logistic regression is exactly the tool that produces one.**

### 8. Information theory — the survival guide

D2L calls this section a survival guide, because deep learning papers use the vocabulary constantly.

**Entropy.** For a distribution $P$,
$$H[P]=\sum_j -P(j)\log P(j)$$
Shannon (1948): to encode data drawn from $P$ you need **at least $H[P]$ nats**. A **nat** is the base-$e$ analogue of a bit:
$$1\text{ nat}=\frac{1}{\log 2}\approx \mathbf{1.4427}\text{ bit}$$

**Surprisal.** What has compression to do with prediction? If the next token is always easy to predict, the stream is easy to compress — in the extreme, a constant stream needs no transmission at all. **Easy to predict, easy to compress.** Shannon quantified the surprise of seeing event $j$ to which you assigned probability $P(j)$ as
$$\log\frac{1}{P(j)}=-\log P(j)$$
and **entropy is the expected surprisal of someone who assigned the true probabilities.**

**Cross-entropy.** $H(P,Q)$ is the **expected surprisal of an observer with subjective probabilities $Q$ seeing data actually generated by $P$**:
$$H(P,Q)\stackrel{\text{def}}{=}\sum_j -P(j)\log Q(j)$$
**The lowest possible cross-entropy is achieved at $Q=P$, where $H(P,P)=H(P)$.**

*(Mine, and the one line D2L leaves out.)* The gap is the **Kullback–Leibler divergence**:
$$H(P,Q)=H(P)+D_{\mathrm{KL}}(P\,\|\,Q)$$
Verified numerically on $P=(0.7,0.2,0.1)$, $Q=(0.5,0.3,0.2)$: $H(P)=0.801819$, $D_{\mathrm{KL}}=0.085123$, $H(P,Q)=0.886941$ nats — and $0.801819+0.085123=0.886941$ exactly. **$H(P)$ is fixed by the data and cannot be optimized away**, so *minimizing cross-entropy is minimizing KL divergence*, and the irreducible floor is the data's own entropy.

> **Two readings of the same objective:** (i) **maximize the likelihood** of the observed data; (ii) **minimize the surprisal — the number of bits — needed to communicate the labels.**

### 9. Numerical stability, and why frameworks fuse softmax with the loss

Care must be taken not to exponentiate or take logarithms of large numbers. Concretely, for logits $\mathbf{o}=(1000,1001,1002)$:

| Method | Result |
|---|---|
| naive $\exp(o_i)/\sum_k\exp(o_k)$ | `[nan, nan, nan]` — $e^{1000}$ overflows `float64` |
| subtract the max first | `[0.090031, 0.244728, 0.665241]` |

The fix rests on **translation invariance**: $\operatorname{softmax}(\mathbf{o}+c)=\operatorname{softmax}(\mathbf{o})$ for any scalar $c$, so choosing $c=-\max_i o_i$ makes the largest exponent exactly $e^0=1$ and everything else smaller. This is the **log-sum-exp trick**, and it is D2L's exercise 6.4. Frameworks apply it automatically — *which is why you pass **logits**, not probabilities, to `CrossEntropyLoss`.* Computing softmax yourself and then taking a log re-introduces the very underflow the fused version avoids.

**Cost.** A fully connected layer with $d$ inputs and $q$ outputs costs $O(dq)$ in both parameters and compute, which can be prohibitive. Reductions exist: **Deep Fried Convnets** (Yang et al., 2015) use permutations, Fourier transforms and scaling to get from quadratic to **log-linear**; quaternion-like decompositions reach $O(dq/n)$ for a compression factor $n$. D2L notes the real difficulty: *we do not strive for the fewest FLOPs but for what executes most efficiently on modern GPUs.*

### 10. Generalization in classification

[[02 - Linear Regression]] §8 asked *when* training error is close to population error. This section asks the sharper, practical question: **how big must a test set be?**

#### 10.1 The test set is a mean estimation problem

For a **fixed** classifier $f$, the test error $\epsilon_D(f)$ is the sample average of the indicator $\mathbf{1}(f(X)\ne Y)$, and the population error $\epsilon(f)$ is its expectation. By the **central limit theorem** the sample average tends to a normal centred at the true mean with standard deviation $\sigma/\sqrt n$. So
$$\epsilon_D(f)\to\epsilon(f)\ \text{ at rate }\ O(1/\sqrt n)$$
> **To estimate the test error twice as precisely you need four times the data; a hundred times more precisely needs ten thousand times the data.** And $O(1/\sqrt n)$ is generally the best statistics has to offer.

**Now sharpen it.** The indicator is **Bernoulli**, so its variance is $\epsilon(f)(1-\epsilon(f))$, which is **maximized at $\epsilon=0.5$** where it equals $0.25$, and is far smaller near 0 or 1. Hence the standard deviation is at most $\sqrt{0.25/n}$, and:

| Requirement | Algebra | $n$ |
|---|---|---|
| one sd $=0.01$ | $0.25/n=0.01^2$ | **2,500** |
| two sd $=0.01$ (≈95% confidence) | $0.25/n=0.005^2$ | **10,000** |

**All three of D2L's figures check out exactly.** And it explains something you have seen: *this is the size of the test set for many popular ML benchmarks.*

> [!warning] The observation D2L makes and most readers skate past
> **"You might be surprised to find out that thousands of applied deep learning papers get published every year making a big deal out of error rate improvements of 0.01 or less."** With a 10,000-example test set, an improvement of 0.01 is *exactly the width of the 95% interval* — i.e. indistinguishable from noise. The caveat D2L adds is real, though: **when error rates are close to 0 the Bernoulli variance collapses**, and a 0.01 improvement genuinely is a big deal.

**Finite-sample version.** The asymptotics assume $n\to\infty$. Because the variable is bounded we can get a valid finite-sample bound from **Hoeffding (1963)**:
$$P\big(\epsilon_D(f)-\epsilon(f)\ge t\big)<\exp(-2nt^2)$$
Solving at $t=0.01$ and $\delta=0.05$ gives $n=-\ln(0.05)/(2\times0.01^2)=\mathbf{14{,}979}$ — D2L's "roughly 15,000" against the asymptotic 10,000. The general lesson holds: **finite-sample guarantees are typically slightly more conservative**, and asymptotics still give useful ballpark figures.

> [!note] A caveat on that comparison — mine, not D2L's
> The 15,000 comes from the **one-sided** bound as printed (a single tail at $\delta=0.05$), while "two standard deviations ⇒ 95% confident" is a **two-sided** interval. The like-for-like finite-sample number is $n=\ln(2/0.05)/(2t^2)=\mathbf{18{,}444}$. So the honest comparison is **18,444 vs 10,000 (1.84×)**, not 15,000 vs 10,000 (1.50×). D2L's equation and its arithmetic are mutually consistent; only the *comparison* mixes conventions. **Recorded as a discrepancy investigated and declined**, since the conclusion ("slightly more conservative", "not so far apart") survives either way.

#### 10.2 Test set reuse — how you destroy a test set without noticing

You do everything right: size the test set properly, keep it sacred, tune all hyperparameters and select among architectures on the **validation** set, evaluate $f_1$ once, report an unbiased estimate with a confidence interval.

Then at 3am you have a better idea. You build $f_2$, tune it on validation, and it beats $f_1$. **You do not have a test set.** Two separate failures:

1. **False discovery / multiple hypothesis testing.** Your precision analysis assumed a *single* classifier. With $k$ classifiers, guaranteeing that *none* got a misleading score is much harder — D2L: *"With 20 classifiers under consideration, you might have no power at all to rule out the possibility that at least one among them received a misleading score."*
2. **Adaptive overfitting** (Dwork et al., 2015). The analysis assumed the classifier was chosen **without any contact with the test set**. But $f_2$ was chosen *after* you saw $f_1$'s test performance. **Once information from the test set has leaked to the modeller, it can never be a true test set again in the strictest sense.**

**D2L's practical advice, worth memorising:** create real test sets; consult them **as infrequently as possible**; account for multiple hypothesis testing in confidence intervals; **raise vigilance when stakes are high and datasets small**; and when running benchmark challenges, **maintain several test sets so that after each round the old one is demoted to a validation set.**

#### 10.3 Statistical learning theory, and its failure on deep networks

*"Test sets are all that we really have"* — and that is unsatisfying: we seldom possess a **true** test set (someone has usually already evaluated on it), and even a true one tells us only **post hoc** whether a classifier generalized, never **a priori** whether it should.

The distinction that matters:

> **Any *fixed* classifier does generalize** — its error on unseen data is an unbiased estimate of population error. The hard question is what happens when a classifier is **trained and evaluated on the same dataset**, chosen from a set $\mathcal{F}$ that is typically **infinite** ($|\mathcal{F}|=\infty$ even for linear models, since parameters are continuous).

The ambitious fix is **uniform convergence**: with probability $\ge1-\delta$, *every* classifier in $\mathcal{F}$ has empirical error within $\alpha$ of its true error simultaneously. **This cannot hold for all classes** — recall the memorization machines with empirical error 0 that never beat random guessing. Too flexible, no uniform convergence; but a *fixed* classifier is useless, fitting neither training nor test data. Hence the classical framing: **flexible (high variance) classes fit better and risk overfitting, rigid (high bias) classes generalize but risk underfitting.**

**Vapnik and Chervonenkis** gave the canonical answer via the **VC dimension** — the largest number of points to which you can assign *any* arbitrary binary labelling and still find a member of the class that agrees:
$$P\big(R[p,f]-R_{\text{emp}}[\mathbf{X},\mathbf{Y},f]<\alpha\big)\ge1-\delta \quad\text{for}\quad \alpha\ge c\sqrt{(\text{VC}-\log\delta)/n}$$
**Linear models on $d$-dimensional inputs have VC dimension $d+1$** — a line can realise any labelling of three points in the plane, but not four.

> [!warning] The punchline, and it frames the rest of the course
> These complexity measures *"turn out to be **powerless** (as straightforwardly applied) for explaining why deep neural networks generalize."* Deep networks have millions of parameters, **can easily assign random labels to large collections of points**, and nevertheless generalize well — and, surprisingly, **often generalize *better* when they are larger and deeper, despite incurring higher VC dimensions.** Classical theory predicts the opposite. Revisited in [[04 - Neural Network]].

### 11. Environment and distribution shift

*"We never stopped to contemplate either where data came from in the first place or what we ultimately plan to do with the outputs."* **Many failed deployments trace back to exactly this.**

D2L's loan example is the sharpest statement of the problem in the book. Suppose a model finds that footwear predicts default — Oxfords repay, sneakers default — and you start granting loans on that basis. **Customers catch on. Soon every applicant wears Oxfords, with no coincident improvement in creditworthiness.**

> **By introducing our model-based decisions to the environment, we might break the model.**

#### 11.1 Three kinds of shift

Train from $p_S(\mathbf{x},y)$, test on $p_T(\mathbf{x},y)$. First, a sobering fact: **absent any assumption relating $p_S$ and $p_T$, learning a robust classifier is impossible.** The pathological case: inputs unchanged, $p_S(\mathbf{x})=p_T(\mathbf{x})$, but every label flipped, $p_S(y\mid\mathbf{x})=1-p_T(y\mid\mathbf{x})$. **If God decides all cats are now dogs, no amount of data can distinguish that from no change at all.**

| Shift | What changes | What is fixed | Natural when | Example |
|---|---|---|---|---|
| **Covariate** | $P(\mathbf{x})$ | $P(y\mid\mathbf{x})$ | **$\mathbf{x}$ causes $y$** | trained on photos of cats/dogs, tested on cartoons |
| **Label** | $P(y)$ | $P(\mathbf{x}\mid y)$ | **$y$ causes $\mathbf{x}$** | predicting diagnoses from symptoms as disease prevalence changes — *diseases cause symptoms* |
| **Concept** | the *definition* of the labels | — | usage drifts over time or space | diagnostic criteria for mental illness; job titles; **what Americans call a soft drink, by region** |

**The causal direction is the thing to remember.** It is what tells you which correction applies. *(D2L notes a degenerate overlap: when the label is deterministic, covariate shift holds even when $y$ causes $\mathbf{x}$ — and there it is often better to use label-shift methods anyway, because they manipulate **low-dimensional label-like objects** instead of high-dimensional inputs.)*

#### 11.2 Four cautionary tales, all real

- **Medical diagnostics.** A startup building a blood test for a disease affecting older men found healthy samples hard to get, so used **university students** as controls. Distinguishing the cohorts was trivially easy — and on **age, hormone levels, physical activity, diet, alcohol consumption**, none of which relate to the disease. Extreme covariate shift, **not correctable by conventional methods**. They wasted a significant sum of money.
- **Self-driving cars.** Synthetic training data from a game engine worked beautifully on rendered test data and was a disaster in a real car: **all the roadside had been rendered with the same simplistic texture**, and the detector learned that "feature" immediately.
- **Tanks in the forest.** The US Army photographed a forest without tanks, then drove tanks in and photographed again. The classifier *appeared to work perfectly*. It had learned to **distinguish trees with shadows from trees without** — the first set was shot in early morning, the second at noon.
- **Nonstationary distributions.** An ad model that never learns the iPad launched; a spam filter versus spammers who wise up; a recommender that pushes Santa hats **long after Christmas**.

> [!important] What links all four
> **Every one produced excellent test-set numbers.** The model did exactly what it was told; the *data* encoded a shortcut. This is the vault's standing finding — *the expensive failures are the ones that produce a plausible wrong answer with no error* — in its purest form. **A held-out test set drawn from the same flawed sample cannot detect any of these.**

#### 11.3 Correcting covariate shift

Empirical risk minimization minimizes $\frac1n\sum_i \ell(f(\mathbf{x}_i),y_i)$ as a stand-in for the true **risk** $\mathbb{E}_{p}[\ell(f(\mathbf{x}),y)]$. If the $\mathbf{x}_i$ came from a **source** $q(\mathbf{x})$ but we care about a **target** $p(\mathbf{x})$, and $p(y\mid\mathbf{x})=q(y\mid\mathbf{x})$, then the identity
$$\iint \ell\,p(y\mid\mathbf{x})p(\mathbf{x})\,d\mathbf{x}\,dy=\iint \ell\,q(y\mid\mathbf{x})q(\mathbf{x})\frac{p(\mathbf{x})}{q(\mathbf{x})}\,d\mathbf{x}\,dy$$
says: **reweight each example by how much more likely it was under the right distribution than the wrong one.**
$$\beta_i\stackrel{\text{def}}{=}\frac{p(\mathbf{x}_i)}{q(\mathbf{x}_i)},\qquad \min_f\ \frac1n\sum_{i=1}^n\beta_i\,\ell(f(\mathbf{x}_i),y_i)$$

**We do not know the ratio — so estimate it, and logistic regression is exactly the right tool.** Label data from $p$ with $z=1$ and data from $q$ with $z=-1$. With equal numbers from each,
$$P(z=1\mid\mathbf{x})=\frac{p(\mathbf{x})}{p(\mathbf{x})+q(\mathbf{x})}\quad\Longrightarrow\quad \frac{P(z=1\mid\mathbf{x})}{P(z=-1\mid\mathbf{x})}=\frac{p(\mathbf{x})}{q(\mathbf{x})}$$
and if the classifier is logistic, $P(z=1\mid\mathbf{x})=\frac{1}{1+\exp(-h(\mathbf{x}))}$, then
$$\beta_i=\frac{1/(1+e^{-h(\mathbf{x}_i)})}{e^{-h(\mathbf{x}_i)}/(1+e^{-h(\mathbf{x}_i)})}=\boxed{\exp(h(\mathbf{x}_i))}$$
*(Verified symbolically. Read it as: a point the discriminator finds twice as likely to be target-data gets $\beta=2$, i.e. $h=\ln 2=0.693$.)*

**The algorithm:**
1. Build a binary set $\{(\mathbf{x}_1,-1),\dots,(\mathbf{x}_n,-1),(\mathbf{u}_1,1),\dots,(\mathbf{u}_m,1)\}$ from labelled training inputs and **unlabelled** test inputs.
2. Train a logistic classifier to get $h$.
3. Weight by $\beta_i=\exp(h(\mathbf{x}_i))$, **or better $\beta_i=\min(\exp(h(\mathbf{x}_i)),c)$** for a constant $c$.
4. Train on the original labelled data with those weights.

> [!warning] The assumption that makes or breaks it
> **Every point in the target distribution must have had non-zero probability at training time.** If $p(\mathbf{x})>0$ where $q(\mathbf{x})=0$, the importance weight is **infinite** and no reweighting can help. This is why step 3 clips at $c$ — and why the blood-test startup could not be rescued: their healthy controls had *zero* probability of being an older man.
>
> Note also what you **do** need: samples of **features** from both distributions. You do **not** need target labels.

#### 11.4 Correcting label shift — with the worked example D2L omits

If $q(y)\ne p(y)$ but $q(\mathbf{x}\mid y)=p(\mathbf{x}\mid y)$, the same identity gives $\beta_i=p(y_i)/q(y_i)$. The advantage: **you never touch the ambient dimension** — inputs are high-dimensional images, labels are just categories.

Take a decent classifier, compute its **confusion matrix** $\mathbf{C}$ on a validation set from the source distribution, and average all test-time predictions into $\mu(\hat{\mathbf{y}})$. Then
$$\mathbf{C}\,p(\mathbf{y})=\mu(\hat{\mathbf{y}})\qquad\Longrightarrow\qquad p(\mathbf{y})=\mathbf{C}^{-1}\mu(\hat{\mathbf{y}})$$

> [!note] A definition that must be read carefully — mine
> D2L describes $c_{ij}$ as *"the fraction of total predictions on the validation set where the true label was $j$ and our model predicted $i$."* Taken literally that is a **joint** frequency, and the linear system would be dimensionally wrong. For $\mathbf{C}p(\mathbf{y})=\mu(\hat{\mathbf{y}})$ to hold, $\mathbf{C}$ must be **column-conditional**: $c_{ij}=P(\hat y=i\mid y=j)$, so that **each column sums to 1**. Check your columns before inverting.

**A worked instance (mine — D2L gives none).** Three classes, source labels $q=(0.5,0.3,0.2)$, and a classifier with
$$\mathbf{C}=\begin{pmatrix}0.85&0.10&0.05\\0.10&0.80&0.15\\0.05&0.10&0.80\end{pmatrix}\quad(\text{columns sum to }1;\ \text{source accuracy }82.5\%)$$
Suppose the true test distribution has shifted to $p=(0.2,0.3,0.5)$. Then
$$\mu(\hat{\mathbf{y}})=\mathbf{C}p=(0.225,\ 0.335,\ 0.440)$$
and $\mathbf{C}^{-1}\mu$ recovers $(0.2,0.3,0.5)$ **exactly**. The weights are
$$\beta=\left(\tfrac{0.2}{0.5},\tfrac{0.3}{0.3},\tfrac{0.5}{0.2}\right)=(0.4,\ 1.0,\ \mathbf{2.5})$$

**Why the inversion is not optional:** using the raw model outputs $\mu$ as the label distribution would give $(0.225,0.335,0.440)$ against the truth $(0.2,0.3,0.5)$ — errors of **+12.5%, +11.7%, −12.0%**. The confusion matrix is what separates *"what the model said"* from *"what is actually there"*.

> [!important] "Sufficiently accurate ⇒ invertible" is the wrong criterion — and this is chapter 2's lesson again
> D2L says that if the classifier is accurate enough, $\mathbf{C}$ will be invertible. **Invertibility is a yes/no test; conditioning is what decides the answer.** Above, $\kappa(\mathbf{C})=1.50$. Take a near-useless classifier with $\kappa(\mathbf{C})=104$: the exact solve still returns $(0.2,0.3,0.5)$, but perturb $\mu$ by a realistic **0.005 of sampling noise** and it returns
> $$\hat p=(0.100,\ 0.800,\ 0.100)$$
> — an error of **0.648**, against **0.0098** for the well-conditioned classifier: a **65.9× amplification**. And note what makes it dangerous: **$\hat p$ is still a perfectly valid probability vector.** Nothing raises an error; the answer is simply wrong.
>
> This is **exactly** the finding of [[02 - Linear Regression]] exercise 4, where a *full-rank* design with $\kappa=312$ let a 0.1 nudge move the parameters by 0.20 and flipped a coefficient's sign. **Two chapters, two settings, one rule: never report rank or invertibility where conditioning is what matters.**

#### 11.5 Concept shift, and the taxonomy of learning problems

**Concept shift is much harder to fix in a principled way.** If the problem suddenly changes from cats-vs-dogs to white-vs-black animals, nothing beats collecting new labels and retraining. Fortunately extreme shifts are rare and tasks usually change **slowly** — ads gain and lose popularity, **traffic camera lenses degrade with environmental wear**, news accumulates gradually. There, the fix is simply to **keep the existing weights and run a few update steps on new data** rather than retrain from scratch.

**The taxonomy**, which also sharpens [[01 - Introduction to Deep Learning]] §4:

| Setting | Description |
|---|---|
| **Batch learning** | train once on $\{(\mathbf{x}_i,y_i)\}$, deploy, never update — *the default assumption everywhere in this course*. The smart cat door installed in a customer's home and never touched again. |
| **Online learning** | observe $\mathbf{x}_t$ → predict $f_t(\mathbf{x}_t)$ → observe $y_t$ → incur loss → update to $f_{t+1}$. Tomorrow's stock price. |
| **Bandits** | online learning with a **finite** set of arms rather than a continuously parametrized $f$ — simpler, so **stronger optimality guarantees** are available |
| **Control** | the environment **remembers** what you did (a coffee boiler's temperature depends on whether it was heating before). PID controllers; now also used to tune hyperparameters |
| **Reinforcement learning** | environment with memory that may **cooperate or compete** — chess, Go, StarCraft; other drivers reacting to an autonomous car |

> **A strategy that works in a stationary environment may not work in one that adapts.** D2L's example: *an arbitrage opportunity discovered by a trader is likely to disappear once it is exploited.* **The speed and manner in which the environment changes determines which algorithms you may bring to bear** — if things change only slowly, force your estimates to change slowly too.

#### 11.6 Fairness, accountability, transparency

> **When you deploy a machine learning system you are not merely optimizing a predictive model — you are providing a tool that will be used to automate decisions**, and those decisions affect people.

If you deploy a medical diagnostic, **you need to know for which populations it works and for which it does not.** Overlooking foreseeable risk to a subpopulation *"could cause us to administer inferior care."* This is the same thread as [[01 - Introduction to Deep Learning]] §2 (the skin-cancer model that never saw black skin) — and §11.2 above shows the **mechanism**: a training sample that differs systematically from the deployment population produces high test accuracy and unsafe behaviour, and no amount of held-out data drawn from the same flawed sample will reveal it.

## ✏️ Exercises

> [!example]- **1.** *(Easy — softmax mechanics)*
> Logits $\mathbf{o}=(2,\ 1,\ 0.1)$ for classes (cat, chicken, dog); the true label is **cat**.
> **(a)** Compute $\hat{\mathbf{y}}$ and the cross-entropy loss.
> **(b)** Compute the gradient $\partial_{\mathbf{o}}\ell$.
> **(c)** Recompute $\hat{\mathbf{y}}$ for $\mathbf{o}+5=(7,6,5.1)$. Explain.
> **(d)** Which class does the model predict, and did you need the softmax to answer?
>
> ---
> **(a)** $e^2=7.3891$, $e^1=2.7183$, $e^{0.1}=1.1052$; sum $=11.2125$.
> $$\hat{\mathbf{y}}=(\mathbf{0.659001},\ 0.242433,\ 0.098566),\qquad \textstyle\sum_j\hat y_j=1$$
> With $\mathbf{y}=(1,0,0)$, only one term survives: $\ell=-\log(0.659001)=\boxed{0.41703\text{ nats}}$ $=0.6016$ bits.
>
> **(b)** $\partial_{\mathbf{o}}\ell=\hat{\mathbf{y}}-\mathbf{y}=\boxed{(-0.341,\ +0.2424,\ +0.0986)}$ — sums to 0, as it must (softmax outputs and one-hot labels both sum to 1). Gradient descent **raises** the cat logit and **lowers** the other two, each in proportion to the probability wrongly assigned to it.
>
> **(c)** **Identical** — $(0.659001, 0.242433, 0.098566)$. Softmax is **translation invariant**: adding $c$ multiplies every numerator and the denominator by $e^c$. This is the redundant degree of freedom of §3, and the basis of the log-sum-exp trick (§9).
>
> **(d)** **Cat**, and **no** — softmax preserves order, so $\operatorname{argmax}_j\hat y_j=\operatorname{argmax}_j o_j$, and $o_1=2$ is already the largest. The softmax is needed to compute the *loss*, never to make the *decision*.

> [!example]- **2.** *(Easy–medium — softmax with two classes is logistic regression)*
> **(a)** Show that for $q=2$, $\hat y_1=\sigma(o_1-o_2)$ where $\sigma(z)=1/(1+e^{-z})$.
> **(b)** Show that $-\sum_j y_j\log\hat y_j$ becomes the familiar binary cross-entropy.
> **(c)** A colleague trains a 3-class softmax layer and reports "the weight on feature 7 for class 2 is 0.8, so feature 7 pushes towards class 2." Respond.
> **(d)** How many parameters could you delete from a $q$-class softmax layer with $d$ inputs without changing any prediction?
>
> ---
> **(a)** $$\hat y_1=\frac{e^{o_1}}{e^{o_1}+e^{o_2}}=\frac{1}{1+e^{o_2-o_1}}=\frac{1}{1+e^{-(o_1-o_2)}}=\sigma(o_1-o_2)$$ dividing numerator and denominator by $e^{o_1}$. **Only the difference of logits matters.**
>
> **(b)** With $\mathbf{y}=(y,1-y)$ and $\hat{\mathbf{y}}=(\hat y,1-\hat y)$: $-\sum_j y_j\log\hat y_j=\boxed{-\big[y\log\hat y+(1-y)\log(1-\hat y)\big]}$ — the binary cross-entropy is not a different loss, just the two-term expansion.
>
> **(c)** **Not valid as stated.** Softmax logits are defined only up to a common additive constant, so an individual weight $w_{2,7}$ has no meaning on its own — you may add any constant to the whole column of $\mathbf{W}$ for feature 7 across all classes and every prediction is unchanged. The meaningful quantity is a **difference**, e.g. $w_{2,7}-w_{1,7}$: "feature 7 pushes towards class 2 *relative to class 1*." **Never interpret a single softmax logit or weight.**
>
> **(d)** Exactly $\boxed{d+1}$ — one whole row of $\mathbf{W}$ ($d$ weights) plus its bias can be fixed at zero, since only differences from it matter. That is why binary classification needs **one** sigmoid output rather than two softmax outputs, and it is precisely the "one fewer" D2L mentions and then declines to use for symmetry.

> [!example]- **3.** *(Medium — how big must a test set be?)*
> **(a)** Why is the test error's variance at most $0.25/n$?
> **(b)** Derive the 2,500 and 10,000 figures.
> **(c)** D2L's exercise 4.6.5 #1: estimate a fixed model's error to within $0.0001$ with probability $>99.9\%$. How many samples?
> **(d)** A paper reports 94.3% vs. a baseline's 93.4% on a 10,000-example test set. What can you conclude?
>
> ---
> **(a)** The per-example error is the indicator $\mathbf{1}(f(X)\ne Y)$, a **Bernoulli** variable with parameter $\epsilon(f)$, so its variance is $\epsilon(1-\epsilon)$. That is a downward parabola **maximized at $\epsilon=0.5$**, where it equals $0.25$. The sample mean of $n$ such variables has variance $\epsilon(1-\epsilon)/n\le 0.25/n$. **Crucially the bound is worst-case**: a model with 2% error has variance $0.02\times0.98=0.0196$, nearly **13× smaller** than 0.25.
>
> **(b)** One sd $=0.01$: $\sqrt{0.25/n}=0.01\Rightarrow n=0.25/10^{-4}=\boxed{2{,}500}$. Two sd (≈95%): $\sqrt{0.25/n}=0.005\Rightarrow n=0.25/(2.5\times10^{-5})=\boxed{10{,}000}$.
>
> **(c)** Hoeffding with $t=10^{-4}$, $\delta=0.001$: $n=-\ln(0.001)/(2t^2)=6.9078/(2\times10^{-8})=\boxed{345{,}387{,}764}$ one-sided, or $\ln(2000)/(2t^2)=\boxed{380{,}045{,}123}$ two-sided. **Roughly 350–380 million examples** — three to four orders of magnitude larger than any standard benchmark. The $O(1/\sqrt n)$ rate is brutal: cutting $t$ by 100× costs $10^4\times$ the data.
>
> **(d)** **Very little from the numbers alone.** The gap is 0.009, and the 95% interval half-width at $n=10{,}000$ is up to 0.01 *per model* — so the difference sits inside the noise of either estimate. Two mitigating points: at ~6% error the Bernoulli sd is $\sqrt{0.06\times0.94/10^4}=0.0024$, so two sd is 0.0047 and the gap is about **1.9 sd of a single estimate** — suggestive, not conclusive, and a proper paired test on the same test set (which shares examples and so has lower variance) would be the right analysis. And if the test set has been used before, §10.2 says the estimate is not unbiased anyway. **This is exactly what D2L is warning about.**

> [!example]- **4.** *(Medium–hard — entropy, and why joint coding wins)*
> D2L's exercise 4.1.5 #2: three classes with probability $(\tfrac13,\tfrac13,\tfrac13)$.
> **(a)** What is the entropy, in bits? What is the problem with a binary code for single symbols?
> **(b)** Does encoding two observations jointly help? Three? Compute bits/symbol for $n=1,2,3,5,100,1000$.
> **(c)** D2L's #3: how many **ternary** units are needed to transmit an integer in $\{0,\dots,7\}$, and why might engineers prefer that?
> **(d)** Relate (b) to the training objective of this chapter.
>
> ---
> **(a)** $H=\log_2 3=\mathbf{1.584963}$ bits/symbol. The problem: **a whole number of bits cannot equal $\log_2 3$.** A single symbol needs $\lceil 1.585\rceil=2$ bits, which is $\mathbf{26.19\%}$ above the floor — a quarter of every transmission wasted.
>
> **(b)** Encoding $n$ jointly needs $\lceil n\log_2 3\rceil$ bits for $3^n$ equally likely messages:
>
> | $n$ | bits | bits/symbol | above floor |
> |---|---|---|---|
> | 1 | 2 | 2.0000 | 26.19% |
> | 2 | 4 | 2.0000 | 26.19% |
> | 3 | 5 | 1.6667 | 5.15% |
> | 5 | 8 | 1.6000 | 0.95% |
> | 100 | 159 | 1.5900 | 0.32% |
> | 1000 | 1585 | 1.5850 | 0.00% |
>
> **$n=2$ does not help at all** ($3^2=9$ still needs 4 bits) — the first real gain is at $n=3$, where $3^3=27\le32=2^5$. The overhead is the rounding waste $\lceil nH\rceil-nH$ **amortized over $n$ symbols**, so it vanishes as $O(1/n)$. This is Shannon's source coding theorem in miniature: **the entropy bound is achievable only in the limit of long blocks.**
>
> **(c)** $3^k\ge8$ needs $\boxed{k=2}$ (since $3^2=9\ge8$), against $2^k\ge8\Rightarrow k=3$ binary digits. **Two ternary units instead of three binary ones**, because each carries $\log_2 3=1.585$ bits rather than 1. Electronically: fewer symbol periods for the same information means **fewer transitions per bit and lower bandwidth on the wire** — you trade signal-to-noise margin (three levels to distinguish instead of two) for spectral efficiency, which is exactly the trade PAM-3 makes.
>
> **(d)** They are the same quantity. Cross-entropy $H(P,Q)$ is the **expected bits an observer believing $Q$ needs for data generated by $P$**, and $H(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q)$. Training minimizes cross-entropy, which minimizes $D_{\mathrm{KL}}$, since $H(P)$ is fixed by the data. **The 26.19% overhead above is the coding analogue of a model's excess loss over the irreducible floor** — and just as no code beats $H(P)$, no classifier drives cross-entropy below the data's own entropy.

> [!example]- **5.** *(Hard — label shift, and when the correction destroys your answer)*
> Three classes; source labels $q=(0.5,0.3,0.2)$; confusion matrix (columns = truth)
> $$\mathbf{C}=\begin{pmatrix}0.85&0.10&0.05\\0.10&0.80&0.15\\0.05&0.10&0.80\end{pmatrix}$$
> At test time the mean model output is $\mu(\hat{\mathbf{y}})=(0.225,0.335,0.440)$.
> **(a)** Check $\mathbf{C}$ is a valid confusion matrix and give the classifier's source accuracy.
> **(b)** Recover $p(\mathbf{y})$ and the importance weights $\beta$.
> **(c)** What error would you make by using $\mu$ directly as the label distribution?
> **(d)** Repeat with a near-useless classifier, $\kappa(\mathbf{C})=104$, when $\mu$ carries $0.005$ of sampling noise. What is the lesson, and where have you met it before?
>
> ---
> **(a)** Columns sum to $1.00,1.00,1.00$ ✓ — each column is $P(\hat y=i\mid y=j)$. Source accuracy $=\sum_j c_{jj}q_j=0.85(0.5)+0.80(0.3)+0.80(0.2)=\boxed{82.5\%}$.
>
> **(b)** Solving $\mathbf{C}p=\mu$:
> $$p(\mathbf{y})=\mathbf{C}^{-1}\mu=\boxed{(0.2,\ 0.3,\ 0.5)}\quad\text{exactly}$$
> Weights $\beta_j=p_j/q_j=\boxed{(0.4,\ 1.0,\ 2.5)}$ — class 3 is upweighted **2.5×**, class 1 down to **40%**, class 2 untouched. Plug these into weighted ERM.
>
> **(c)** You would report $(0.225,0.335,0.440)$ against the truth $(0.2,0.3,0.5)$ — errors of **+12.5%, +11.7%, −12.0%**. The model's average output is **not** the label distribution; it is the label distribution *smeared by the confusion matrix*, and the whole point of $\mathbf{C}^{-1}$ is to undo the smearing. Note the direction: the rare-in-training class 3 is **understated**, so the naive estimate *underweights exactly the class the shift made important.*
>
> **(d)** With $\kappa=104$ the exact solve still returns $(0.2,0.3,0.5)$ — but adding $0.005$ of noise to $\mu$ returns
> $$\hat p=(0.100,\ 0.800,\ 0.100),\qquad \|\hat p-p\|=0.648$$
> against $0.0098$ for the well-conditioned $\mathbf{C}$ — a **65.9× amplification**. And $\hat p$ is still a **valid probability vector**: non-negative, sums to 1, nothing raises an error.
> **The lesson:** D2L says "if our classifier is sufficiently accurate, $\mathbf{C}$ will be invertible", but **invertibility is a yes/no test and conditioning is what decides whether the answer means anything.** The correction amplifies estimation noise by $\kappa(\mathbf{C})$, so a weak classifier makes label-shift correction *worse than useless* — it converts small sampling error into a confident, well-formed, wrong answer.
> **Where you met it:** [[02 - Linear Regression]] exercise 4, where a design matrix that *was* full rank ($\det=4$) had $\kappa=312$, a 0.1 nudge in one label moved the parameters by 0.20, and ridge flipped a coefficient's sign. **Same rule, two chapters apart, in unrelated settings.**

## 📝 Summary

- **Classification changes exactly three things** from [[02 - Linear Regression]]: the target's form (**one-hot**, which refuses to invent an ordering), the output layer (**one affine function per class**, deliberately redundant by one degree of freedom), and the loss (**cross-entropy**). Everything else — data loading, forward pass, gradients, SGD — is unchanged.
- **Softmax squishes logits into a probability vector** via $\hat y_i=e^{o_i}/\sum_j e^{o_j}$: non-negative, sums to 1, order-preserving. Because it preserves order, **you never compute it to make a prediction** — only to compute the loss. It comes from Boltzmann and Gibbs, where **energy equates to error**.
- **Cross-entropy is maximum likelihood again.** Same derivation as squared loss, different noise model: categorical instead of Gaussian. $\ell=-\sum_j y_j\log\hat y_j$, which for a one-hot label is just $-\log$ of the probability assigned to the truth — **and $-\log 0=\infty$, so confident mistakes are punished without bound.**
- **The gradient is $\hat{\mathbf{y}}-\mathbf{y}$** — predicted minus observed, exactly as in regression. This is a structural property of **exponential families**, not a coincidence. The **Hessian is the covariance of $\hat{\mathbf{y}}$**, so the log-partition function is convex and curvature vanishes as the model grows confident.
- **Softmax over two classes *is* the logistic sigmoid of $o_1-o_2$.** Only differences of logits are meaningful, so an individual softmax weight cannot be interpreted, and $d+1$ parameters are always redundant.
- **Entropy is expected surprisal; cross-entropy is the surprisal of an observer believing $Q$ when reality is $P$**; and $H(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q)$, so minimizing cross-entropy minimizes KL against an **irreducible floor $H(P)$**. One nat $=1.4427$ bits.
- **Test-set size follows from Bernoulli variance.** $\sigma^2=\epsilon(1-\epsilon)\le0.25$, giving **2,500** examples for one sd of 0.01 and **10,000** for two — which is why benchmarks are that size, and why *"thousands of papers make a big deal out of improvements of 0.01 or less."* Hoeffding's finite-sample version needs ~15,000.
- **A test set is destroyed by use, not by misuse.** Multiple hypothesis testing plus **adaptive overfitting**: once test information reaches the modeller, it is never a true test set again. Curate several and demote them in rotation.
- **Classical complexity theory (VC dimension) is powerless on deep networks** — they can fit random labels, yet generalize, and often generalize *better* when larger and deeper. The theory predicts the opposite.
- **Distribution shift comes in three kinds, told apart by causality**: covariate ($\mathbf{x}$ causes $y$; reweight by $\beta_i=\exp(h(\mathbf{x}_i))$ from a logistic discriminator), label ($y$ causes $\mathbf{x}$; solve $\mathbf{C}p=\mu$), and concept (definitions drift; retrain incrementally). **Absent any assumption linking train and test, robust learning is impossible.**
- **Deploying a model changes the world it predicts.** Grant loans on footwear and everyone buys Oxfords. Every cautionary tale in §11.2 produced excellent test numbers — a held-out set drawn from the same flawed sample **cannot detect any of them.**

## ⚠️ Important Notes

1. **One-hot is a modelling decision, not a storage format.** Integer labels assert an ordering and a metric. Use them **only** when the ordering is real (ordinal regression) — and then do not throw it away.
2. **A softmax layer's parameters are not identifiable.** Add any constant to a whole row of $(\mathbf{W},\mathbf{b})$ and every prediction is unchanged. **Never interpret an individual logit or weight; only differences.** This alone invalidates a lot of casual "feature importance" talk about classifiers.
3. **Do not compute softmax to make a prediction.** $\operatorname{argmax}\hat y=\operatorname{argmax}\mathbf{o}$. Computing it anyway wastes time and invites underflow.
4. **Pass logits to the loss, never probabilities.** Frameworks fuse softmax with cross-entropy specifically to apply the log-sum-exp trick. Applying `softmax` then `log` yourself re-creates the overflow: on $(1000,1001,1002)$ the naive route returns `nan`, the shifted one returns $(0.0900,0.2447,0.6652)$.
5. **Cross-entropy is unbounded above.** A single confidently-wrong prediction can dominate a whole minibatch. This is the mechanism behind exploding losses, and why label smoothing and clipping exist.
6. **The gradient $\hat{\mathbf{y}}-\mathbf{y}$ always sums to zero** across classes — both vectors are distributions. Useful as a check, but it is a *self*-consistency check and therefore weak evidence.
7. **Curvature is largest where the model is most uncertain.** Since the Hessian is $\operatorname{diag}(\hat{\mathbf{y}})-\hat{\mathbf{y}}\hat{\mathbf{y}}^\top$, a saturated softmax has near-zero curvature *and* near-zero gradient in the correct direction — one route to the vanishing-gradient problem of [[04 - Neural Network]].
8. **Squared loss on one-hot targets "works surprisingly well"** — D2L's words. It is not absurd, just unprincipled and brittle. Know why it is rejected (no normalization, no non-negativity, outlier-brittle) rather than reciting that it is wrong.
9. **Temperature is a real dial, and it is $\lambda$ in $Q(i)\propto P(i)^\lambda$.** Since $P\propto e^{-E/kT}$, raising to $\lambda$ gives $e^{-E/k(T/\lambda)}$, so **$T_{\text{eff}}=T/\lambda$: doubling temperature means $\lambda=\tfrac12$, halving means $\lambda=2$.** As $T\to0$ ($\lambda\to\infty$) the distribution collapses onto the argmax; as $T\to\infty$ ($\lambda\to0$) it goes uniform. Verified on $(0.6,0.3,0.1)$: entropy runs $0.898\to0.594$ nats at $\lambda=2$ and $\to\ln 3=1.0986$ as $\lambda\to0$.
10. **The Bernoulli variance bound is worst-case.** $0.25$ applies at $\epsilon=0.5$; a model at 2% error has variance 13× smaller and needs far fewer test examples for the same absolute precision. Do not quote 10,000 as a universal requirement.
11. **$O(1/\sqrt n)$ is unforgiving.** Twice the precision costs 4× the data; 100× costs 10,000×. D2L's exercise 1 works out to **~350 million examples** for a precision of $10^{-4}$ — which is why nobody makes that claim.
12. **Improvements of 0.01 on a 10,000-example test set are inside the noise** unless the error rate is already small (where Bernoulli variance collapses) or a paired test is used. This is one of the most useful things in the chapter for reading papers.
13. **A test set dies from being consulted, not from being cheated on.** Adaptive overfitting needs no dishonesty — merely that you saw a number and had another idea. Rotate test sets; demote old ones to validation.
14. **"Any fixed classifier generalizes."** The difficulty is entirely in choosing $f$ using the data. If you can hold a model genuinely fixed with respect to a dataset, evaluation on it is unbiased — that single sentence explains the whole train/validation/test architecture.
15. **VC dimension does not explain deep learning.** Do not present it in an exam as the reason networks generalize; present it as the classical theory that **fails** on them, since larger and deeper often generalizes *better*.
16. **Identify the causal direction before choosing a shift correction.** $\mathbf{x}$ causes $y$ ⇒ covariate shift; $y$ causes $\mathbf{x}$ ⇒ label shift. Applying the wrong correction is worse than none.
17. **Importance weights must be clipped.** $\beta_i=\min(\exp(h(\mathbf{x}_i)),c)$ — and if any target point had **zero** probability at training time, the true weight is infinite and no reweighting can save you. That is precisely why the blood-test startup was unrescuable.
18. **Confusion matrices for label shift must be column-conditional** ($c_{ij}=P(\hat y=i\mid y=j)$, columns summing to 1). D2L's prose describes a joint frequency; taken literally the linear system does not hold.
19. **Conditioning, not invertibility — again.** Label-shift correction amplifies noise in $\mu$ by $\kappa(\mathbf{C})$: at $\kappa=104$, sampling noise of 0.005 turned $(0.2,0.3,0.5)$ into $(0.1,0.8,0.1)$, **still a valid probability vector**. Same lesson as [[02 - Linear Regression]] exercise 4's full-rank-but-ill-conditioned design.
20. **Concept shift usually cannot be corrected, only tracked.** If the labels' *meaning* changed, there is no reweighting; fine-tune continuously and accept that the model is always slightly stale.
21. **Deployment is an intervention.** The loan/footwear example is not a curiosity — a model whose outputs influence behaviour invalidates its own training distribution. Any model driving decisions needs monitoring for exactly this, which is where [[MLOps/contents/00-Index|MLOps]] takes over.
22. **Every failure in §11.2 had excellent test-set numbers.** Shadows, textures, and student blood donors are all *real* signal in the data collected. The system did exactly what it was told — the vault's recurring finding, and the reason test accuracy is necessary and never sufficient.

> [!warning] Gaps in the source material
> **Figures — all lost, and one class of them matters.** Fig. 4.1.1 (softmax regression as a single-layer network) is a **label-schematic whose content is its labels**, and the prose names all of them ($x_1..x_4$ fully connected to $o_1..o_3$) — **reconstructed above**. Fig. 4.7.1 and 4.7.2 (photo cats/dogs vs. cartoon cats/dogs) and Fig. 4.7.3 (the US soft-drink-name map) are **photographs and a data map; their content is genuinely lost**, but each is an *illustration of a claim the prose states in full*, so nothing conceptual is missing. The Fashion-MNIST sample grids in §4.2 are lost and immaterial.
>
> **Mathematics is reconstructed, never transcribed**, and this chapter added **two new cipher entries** now recorded in this subject's `CLAUDE.md`: **`!` is `→`** and **`λ` is deleted**, on top of the known deletions. D2L's exercise 5.4 extracts as `Showthatfor !1 wehave 1RealSoftMax(a; b)! max(a; b)`, which is $\text{for }\lambda\to\infty\text{ we have }\lambda^{-1}\mathrm{RealSoftMax}(\lambda a,\lambda b)\to\max(a,b)$ — **three deletions and two substitutions in one line.** The `1`-means-`∞` hazard recurs in exercise 7.3 ("what happens if we let the temperature approach `1`" = $\infty$).
>
> **Added beyond D2L, and labelled as mine throughout:**
> - **$H(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q)$** (§8), verified numerically. D2L defines entropy and cross-entropy and never names KL divergence or states the decomposition — which is the sentence that explains *why* minimizing cross-entropy is the right objective.
> - **The full solution to D2L's exercise 1** (§6): that the Hessian is $\operatorname{diag}(\hat{\mathbf{y}})-\hat{\mathbf{y}}\hat{\mathbf{y}}^\top$ and equals the covariance of the softmax distribution, verified symbolically.
> - **The binary reduction** (§7 and exercise 2), including the count of $d+1$ redundant parameters. D2L mentions the redundancy in one clause and never uses it.
> - **The one-sided/two-sided caveat** on the 15,000-vs-10,000 comparison (§10.1) — like-for-like is **18,444 vs 10,000**. Logged as a declined discrepancy.
> - **The whole of exercise 4's table** — bits/symbol at $n=1,2,3,5,100,1000$ and the finding that **$n=2$ buys nothing** while $n=3$ is the first real gain. D2L poses the question and gives no answer.
> - **The entire label-shift worked example** (§11.4, exercise 5): the confusion matrix, the recovery of $p=(0.2,0.3,0.5)$, the weights $(0.4,1.0,2.5)$, the +12.5%/+11.7%/−12.0% naive errors, and **the $\kappa=104$ failure with its 65.9× noise amplification**. D2L gives the linear system and not a single number.
> - **The observation that $\mathbf{C}$ must be column-conditional**, since D2L's wording describes a joint frequency under which the linear system is dimensionally wrong.
> - **The temperature computation** in Important Note 9 (D2L's exercise 7, unanswered), and the **numerical-overflow demonstration** in §9.
> - **The MNIST/hardware cross-check** below.
>
> **A cross-chapter check on [[01 - Introduction to Deep Learning]]'s Table 1.5.1, and it half fails.** §4.2 states that in 1995 a Sun SPARCStation 5 with **64 MB of RAM and 5 MFLOPS** was state of the art for ML at AT&T Bell Labs. Against the table's 1990 row (10 MB, 10 MF): memory is $6.4\times$ larger, sitting sensibly between the 1990 and 2000 rows — **but compute is $0.5\times$**, i.e. the 1995 machine was *slower* than the table's 1990 figure. **The table's compute column is optimistic for the era.** Separately, MNIST's 60,000 $28\times28$ images are 47.04 MB at one byte per pixel — **73.5% of that machine's entire RAM**, and $2.94\times$ the whole machine as `float32`. That is a quantitative reason why MNIST "posed a formidable challenge", and it extends the parameter-count argument of [[01 - Introduction to Deep Learning]] exercise 5 with a second, independent data point.
>
> **Left as the source states it:** all citations (Fechner 1860, Gibbs 1902, Shannon 1948, Vapnik–Chervonenkis, Hoeffding 1963, Dwork et al. 2015, and the rest); the four cautionary tales in §11.2, which are anecdotes and unverifiable; the claimed complexity reductions of Deep Fried Convnets and quaternion decompositions.
>
> **Deliberately deferred, not omitted:** D2L §4.2 (the Fashion-MNIST data pipeline), §4.3 (the base `Classifier` class and accuracy), §4.4 and §4.5 (softmax implementations from scratch and concise) are **framework scaffolding**, used here only where they carry a result — the dataset's 60,000/10,000 split and the numerical-stability discussion. §4.7.4's taxonomy is summarized rather than expanded because **[[Machine Learning/contents/00-Index|Machine Learning]] owns reinforcement learning** in this vault. The **statistical learning theory of §4.6.3 is stated, not derived**; a proper treatment belongs to [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].

**Previous:** [[02 - Linear Regression]] · **Next:** [[04 - Neural Network]]
