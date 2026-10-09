---
subject: Deep Learning
chapter: 3
tags: [ds, deep-learning, classification, softmax, cross-entropy, distribution-shift]
source: "Zhang, Lipton, Li & Smola — Dive into Deep Learning, §4.1–4.7 (book pp. 127–169)"
---

# Logistic Regression

> [!info] Naming
> The syllabus says *Logistic Regression*; D2L calls the chapter *Softmax Regression*. Softmax regression with $q=2$ classes is exactly binary logistic regression (§7), so this note covers the general case. Compared with [[02 - Linear Regression]], three things change: the targets (one-hot), the output layer (one affine function per class) and the loss (cross-entropy).

## 📘 Main Knowledge

### 1. Regression vs. classification

Even numeric targets can break regression's assumptions: house prices are positive and change relatively (so regress on $\log$ price), and days in hospital is a discrete count (survival modelling).

Classification asks "which category?". The word covers two things: hard assignment to a class, and soft assignment (a probability per class). We use soft models even when we want hard answers, because decisions need probabilities and costs ([[01 - Introduction to Deep Learning]] §4.1). When several labels can be true at once, the task is multi-label, not multi-class.

### 2. One-hot labels

Running example: a $2\times2$ grayscale image (features $x_1..x_4$), class cat, chicken or dog.

Labels $y\in\{1,2,3\}$ would imply an order (chicken between cat and dog) that does not exist. For unordered classes use **one-hot** vectors:
$$\mathbf{y}\in\{(1,0,0),\,(0,1,0),\,(0,0,1)\}$$

If the classes do have an order (baby, toddler, adolescent, …), ordinal regression may be better. Dropping a real order is also a mistake.

### 3. The model: one affine function per class

With 4 features and 3 classes there are $4\times3=12$ weights and 3 biases:
$$o_i = \sum_{k=1}^4 x_k w_{ik} + b_i,\quad i=1,2,3 \qquad\text{i.e.}\qquad \mathbf{o}=\mathbf{W}\mathbf{x}+\mathbf{b}$$

This is a single fully connected layer. For a minibatch $\mathbf{X}\in\mathbb{R}^{n\times d}$, $\mathbf{O}=\mathbf{X}\mathbf{W}+\mathbf{b}$ and softmax is applied row by row.

The parametrization has one redundant degree of freedom: since probabilities sum to 1, $q-1$ outputs would be enough. D2L keeps all $q$ for symmetry. Consequences: adding a constant to every logit changes nothing (§9), the binary case depends only on $o_1-o_2$ (§7), and individual logits or weights cannot be interpreted, only differences.

### 4. Softmax

Regressing one-hot targets with squared loss "works surprisingly well" but nothing forces outputs to be non-negative or sum to 1 (a linear "probability of buying" exceeds 1 for a mansion). D2L also mentions and sets aside the probit model ($\mathbf{y}=\mathbf{o}+$ Gaussian noise).

Softmax exponentiates and normalizes:
$$\hat y_i=\frac{\exp(o_i)}{\sum_j\exp(o_j)}$$

It preserves order, so $\operatorname{argmax}_j \hat y_j=\operatorname{argmax}_j o_j$. For prediction you can skip the softmax; it is needed only for the loss.

The form comes from statistical physics: Boltzmann and Gibbs (1902) found that a state with energy $E$ occurs with probability $\propto\exp(-E/kT)$. In ML, energy plays the role of error (energy-based models).

### 5. Cross-entropy from maximum likelihood

Same method as squared loss. Independent examples give
$$-\log P(\mathbf{Y}\mid\mathbf{X})=\sum_{i=1}^n -\log P(\mathbf{y}^{(i)}\mid\mathbf{x}^{(i)}) = \sum_{i=1}^n \ell(\mathbf{y}^{(i)},\hat{\mathbf{y}}^{(i)}),\qquad \ell(\mathbf{y},\hat{\mathbf{y}})=-\sum_{j=1}^{q}y_j\log\hat y_j$$

With a one-hot $\mathbf{y}$ only one term survives: $-\log$ of the probability given to the true class.

- $\ell\ge0$, and $\ell=0$ only for a certain correct prediction, which needs infinite logits.
- $-\log 0=\infty$: a confident mistake costs without bound. This is why overconfident models destabilize training and why label smoothing exists.

Written in logits, which is how frameworks compute it:
$$\ell=\log\sum_{k=1}^q\exp(o_k)-\sum_{j=1}^q y_jo_j$$

### 6. Gradient and Hessian

$$\partial_{o_j}\,\ell=\operatorname{softmax}(\mathbf{o})_j-y_j$$

Predicted minus observed, as in linear regression. D2L notes this holds for the log-likelihood of every exponential-family model.

The Hessian in the logits is
$$\nabla^2_{\mathbf{o}}\,\ell=\operatorname{diag}(\hat{\mathbf{y}})-\hat{\mathbf{y}}\hat{\mathbf{y}}^\top,$$
the covariance matrix of the distribution $\hat{\mathbf{y}}$ (verified symbolically; D2L's exercise 1). So log-sum-exp is convex, and curvature is largest when the model is uncertain and vanishes as it becomes confident.

Soft labels such as $(0.1,0.2,0.7)$ work in the same formula, giving the expected loss under a label distribution. Label smoothing and knowledge distillation use this.

### 7. Two classes: logistic regression

$$\hat y_1=\frac{e^{o_1}}{e^{o_1}+e^{o_2}}=\frac{1}{1+e^{-(o_1-o_2)}}=\sigma(o_1-o_2)$$

Two-class softmax is the sigmoid of the logit difference. The loss becomes binary cross-entropy:
$$\ell=-\big[y\log\hat y+(1-y)\log(1-\hat y)\big]$$

Logistic regression reappears in §11.3 as a tool for estimating density ratios.

### 8. Information theory

**Entropy** $H[P]=-\sum_j P(j)\log P(j)$ is the minimum average code length for data from $P$ (Shannon, 1948). In nats with natural log; $1\text{ nat}=1/\ln 2\approx1.4427$ bits.

**Surprisal** of an event with probability $P(j)$ is $-\log P(j)$. Predictable data is compressible. Entropy is the expected surprisal of an observer who knows the true probabilities.

**Cross-entropy** $H(P,Q)=-\sum_j P(j)\log Q(j)$ is the expected surprisal of an observer who believes $Q$ while the data comes from $P$. It is minimized at $Q=P$.

The gap is the KL divergence (D2L does not state this):
$$H(P,Q)=H(P)+D_{\mathrm{KL}}(P\,\|\,Q)$$
Check with $P=(0.7,0.2,0.1)$, $Q=(0.5,0.3,0.2)$: $H(P)=0.801819$, $D_{\mathrm{KL}}=0.085123$, sum $0.886941=H(P,Q)$. $H(P)$ is fixed by the data, so minimizing cross-entropy minimizes KL divergence, and $H(P)$ is the floor.

So training with cross-entropy can be read two ways: maximize the likelihood of the labels, or minimize the bits needed to transmit them.

### 9. Numerical stability

For logits $(1000,1001,1002)$:

| Method | Result |
|---|---|
| naive $\exp(o_i)/\sum_k\exp(o_k)$ | `[nan, nan, nan]` ($e^{1000}$ overflows) |
| subtract the max first | `[0.090031, 0.244728, 0.665241]` |

Softmax is translation invariant, $\operatorname{softmax}(\mathbf{o}+c)=\operatorname{softmax}(\mathbf{o})$, so subtracting $\max_i o_i$ is safe (the log-sum-exp trick). Frameworks fuse softmax and cross-entropy to do this, which is why `CrossEntropyLoss` takes logits.

A fully connected output layer costs $O(dq)$. Structured alternatives (Deep Fried Convnets, quaternion-style decompositions) reduce this, though what matters in practice is speed on GPUs, not FLOP counts.

### 10. Generalization in classification

#### 10.1 How big must a test set be?

For a fixed classifier, test error is the mean of the Bernoulli variable $\mathbf{1}(f(X)\ne Y)$. By the CLT it converges to the true error at rate $O(1/\sqrt n)$: twice the precision needs 4× the data.

Bernoulli variance $\epsilon(1-\epsilon)$ is at most 0.25 (at $\epsilon=0.5$), so:

| Requirement | Algebra | $n$ |
|---|---|---|
| one sd $=0.01$ | $0.25/n=0.01^2$ | 2,500 |
| two sd $=0.01$ (≈95%) | $0.25/n=0.005^2$ | 10,000 |

Many benchmarks have test sets of this size. D2L remarks that thousands of papers claim improvements of 0.01 or less, which on 10,000 examples is within the noise. Near zero error the variance is much smaller and 0.01 can be meaningful.

Hoeffding's finite-sample bound $P(\epsilon_D(f)-\epsilon(f)\ge t)<\exp(-2nt^2)$ at $t=0.01$, $\delta=0.05$ gives $n=14{,}979$ (D2L: "roughly 15,000"). Note this is one-sided while the 10,000 is two-sided; the like-for-like two-sided figure is 18,444. The conclusion (finite-sample bounds are somewhat more conservative) holds either way.

#### 10.2 Reusing the test set

Suppose you evaluate $f_1$ once on a clean test set, then build $f_2$ after seeing the result. Two problems:

1. **Multiple testing**: with many classifiers, at least one may get a misleadingly good score.
2. **Adaptive overfitting** (Dwork et al., 2015): $f_2$ was chosen with knowledge of the test set, so the test set is no longer independent of the model.

D2L's advice: use real test sets as rarely as possible, account for multiple comparisons, be extra careful with small data and high stakes, and in competitions keep several test sets, demoting each old one to validation.

#### 10.3 Statistical learning theory

Any fixed classifier's test error is an unbiased estimate. The hard case is a classifier chosen from an (infinite) class $\mathcal{F}$ using the same data. Uniform convergence asks that every $f\in\mathcal{F}$ have empirical error close to true error simultaneously; that fails for very flexible classes.

Vapnik and Chervonenkis: the **VC dimension** is the largest number of points the class can label in every possible way. With probability $\ge1-\delta$,
$$R[p,f]-R_{\text{emp}}[\mathbf{X},\mathbf{Y},f]<\alpha \quad\text{for}\quad \alpha\ge c\sqrt{(\text{VC}-\log\delta)/n}$$
Linear models in $d$ dimensions have VC dimension $d+1$.

These bounds do not explain deep learning. Deep networks can fit random labels yet generalize well, and larger, deeper networks often generalize better despite higher VC dimension. See [[04 - Neural Network]].

### 11. Distribution shift

D2L's loan example: a model finds that people wearing Oxfords repay and people in sneakers default. Once loans are granted on that basis, everyone wears Oxfords and creditworthiness does not change. Deploying a model can break it.

#### 11.1 Types of shift

Train on $p_S(\mathbf{x},y)$, test on $p_T(\mathbf{x},y)$. Without some assumption linking them, robust learning is impossible: if all labels flip while inputs stay the same, no data can detect it.

| Shift | Changes | Fixed | Typical when | Example |
|---|---|---|---|---|
| Covariate | $P(\mathbf{x})$ | $P(y\mid\mathbf{x})$ | $\mathbf{x}$ causes $y$ | train on photos, test on cartoons |
| Label | $P(y)$ | $P(\mathbf{x}\mid y)$ | $y$ causes $\mathbf{x}$ | disease prevalence changes; diseases cause symptoms |
| Concept | meaning of labels | | definitions drift | diagnostic criteria; regional names for soft drinks |

The causal direction tells you which correction to use. When labels are deterministic, label-shift methods can still be easier because they work with low-dimensional labels.

#### 11.2 Examples from D2L

- **Medical test**: healthy controls were university students; the disease affects older men. The classifier separated the groups by age, hormones, diet and so on. Not correctable.
- **Self-driving**: trained on game-engine images where all roadsides had the same texture; failed on real roads.
- **Tanks**: photos without tanks were taken in the morning, with tanks at noon; the classifier learned shadows.
- **Nonstationarity**: ad models unaware of new products, spammers adapting, recommending Santa hats after Christmas.

All of these looked excellent on a test set drawn from the same flawed data.

#### 11.3 Correcting covariate shift

If inputs come from source $q(\mathbf{x})$, we care about target $p(\mathbf{x})$, and $p(y\mid\mathbf{x})=q(y\mid\mathbf{x})$, reweight each example:
$$\beta_i=\frac{p(\mathbf{x}_i)}{q(\mathbf{x}_i)},\qquad \min_f\ \frac1n\sum_{i=1}^n\beta_i\,\ell(f(\mathbf{x}_i),y_i)$$

Estimate the ratio with logistic regression. Label target samples $z=1$ and source samples $z=-1$ (equal numbers). Then $P(z=1\mid\mathbf{x})/P(z=-1\mid\mathbf{x})=p(\mathbf{x})/q(\mathbf{x})$, and with $P(z=1\mid\mathbf{x})=\sigma(h(\mathbf{x}))$:
$$\beta_i=\exp(h(\mathbf{x}_i))$$

Algorithm:
1. Combine labelled training inputs (label −1) and unlabelled test inputs (label +1).
2. Train a logistic classifier to get $h$.
3. Set $\beta_i=\min(\exp(h(\mathbf{x}_i)),c)$.
4. Train on the labelled data with weights $\beta_i$.

Requirement: every region with $p(\mathbf{x})>0$ must have $q(\mathbf{x})>0$, otherwise the weight is infinite. The medical startup's controls had zero chance of being older men, so no reweighting could help. You need features from both distributions, but no target labels.

#### 11.4 Correcting label shift

If $q(y)\ne p(y)$ but $q(\mathbf{x}\mid y)=p(\mathbf{x}\mid y)$, then $\beta_i=p(y_i)/q(y_i)$. Estimate $p(y)$ from a confusion matrix $\mathbf{C}$ (computed on source validation data) and the average test prediction $\mu(\hat{\mathbf{y}})$:
$$\mathbf{C}\,p(\mathbf{y})=\mu(\hat{\mathbf{y}})\quad\Longrightarrow\quad p(\mathbf{y})=\mathbf{C}^{-1}\mu(\hat{\mathbf{y}})$$

$\mathbf{C}$ must be column-conditional, $c_{ij}=P(\hat y=i\mid y=j)$, with columns summing to 1. D2L's wording describes a joint frequency, under which the equation would not hold.

Worked example (mine). Source labels $q=(0.5,0.3,0.2)$,
$$\mathbf{C}=\begin{pmatrix}0.85&0.10&0.05\\0.10&0.80&0.15\\0.05&0.10&0.80\end{pmatrix}$$
(source accuracy 82.5%). If the true test distribution is $p=(0.2,0.3,0.5)$, then $\mu=\mathbf{C}p=(0.225,0.335,0.440)$, and $\mathbf{C}^{-1}\mu$ recovers $p$ exactly. Weights $\beta=(0.4,1.0,2.5)$. Using $\mu$ directly would be off by +12.5%, +11.7%, −12.0%.

D2L says a sufficiently accurate classifier makes $\mathbf{C}$ invertible. What matters is the condition number. Here $\kappa(\mathbf{C})=1.50$. With a weak classifier, $\kappa=104$, adding 0.005 of sampling noise to $\mu$ gives $\hat p=(0.100,0.800,0.100)$: error 0.648 vs 0.0098, 65.9× worse, and still a valid-looking probability vector. Same lesson as [[02 - Linear Regression]] exercise 4.

#### 11.5 Concept shift and learning settings

Concept shift has no principled fix beyond new labels. Usually it is gradual (camera lenses wearing, ads changing popularity), and continuing to train the existing model on new data is enough.

| Setting | Description |
|---|---|
| Batch learning | train once, deploy, never update (the default in this course) |
| Online learning | predict $f_t(\mathbf{x}_t)$, see $y_t$, update to $f_{t+1}$ |
| Bandits | online learning with a finite set of actions; stronger guarantees |
| Control | the environment remembers past actions (PID controllers) |
| Reinforcement learning | environment with memory that may cooperate or compete |

A strategy that works in a stationary environment may fail once the environment adapts (an arbitrage disappears once exploited). If the environment changes slowly, make estimates change slowly too.

#### 11.6 Fairness

A deployed model automates decisions about people. For a medical model you must know which populations it works for. A training sample that differs from the deployment population can give high test accuracy and unsafe behaviour.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Softmax mechanics*
> Logits $\mathbf{o}=(2, 1, 0.1)$ for (cat, chicken, dog); true label cat.
> **(a)** Compute $\hat{\mathbf{y}}$ and the loss. **(b)** The gradient. **(c)** $\hat{\mathbf{y}}$ for $\mathbf{o}+5$. **(d)** The predicted class; did you need softmax?
>
> ---
> **(a)** $e^2=7.3891$, $e^1=2.7183$, $e^{0.1}=1.1052$, sum 11.2125. $\hat{\mathbf{y}}=(0.659001, 0.242433, 0.098566)$. $\ell=-\log 0.659001=0.41703$ nats (0.6016 bits).
>
> **(b)** $\hat{\mathbf{y}}-\mathbf{y}=(-0.341, +0.2424, +0.0986)$, summing to 0. Descent raises the cat logit and lowers the others.
>
> **(c)** Unchanged: softmax is translation invariant.
>
> **(d)** Cat; no, argmax of the logits is enough.

> [!example]- **2.** *(Easy–medium) Two-class softmax*
> **(a)** Show $\hat y_1=\sigma(o_1-o_2)$ for $q=2$. **(b)** Show the loss is binary cross-entropy. **(c)** A colleague says "the weight on feature 7 for class 2 is 0.8, so feature 7 pushes toward class 2." Respond. **(d)** How many parameters of a $q$-class softmax layer with $d$ inputs are redundant?
>
> ---
> **(a)** Divide numerator and denominator by $e^{o_1}$: $\hat y_1=1/(1+e^{-(o_1-o_2)})$.
>
> **(b)** With $\mathbf{y}=(y,1-y)$: $-[y\log\hat y+(1-y)\log(1-\hat y)]$.
>
> **(c)** A single weight means nothing: adding a constant to feature 7's weight in every class changes no prediction. Only differences such as $w_{2,7}-w_{1,7}$ are meaningful.
>
> **(d)** $d+1$: one row of $\mathbf{W}$ and its bias can be fixed at zero. That is why binary classification uses one sigmoid output.

> [!example]- **3.** *(Medium) Test-set size*
> **(a)** Why is the test error's variance at most $0.25/n$? **(b)** Derive 2,500 and 10,000. **(c)** D2L ex. 4.6.5 #1: error within $10^{-4}$ with probability $>99.9\%$. How many samples? **(d)** A paper reports 94.3% vs 93.4% on 10,000 test examples. Conclusion?
>
> ---
> **(a)** Each error is Bernoulli with variance $\epsilon(1-\epsilon)\le0.25$; the mean of $n$ has variance $\le0.25/n$. At 2% error the variance is $0.0196$, about 13× smaller.
>
> **(b)** $\sqrt{0.25/n}=0.01\Rightarrow n=2{,}500$; $\sqrt{0.25/n}=0.005\Rightarrow n=10{,}000$.
>
> **(c)** Hoeffding, $t=10^{-4}$, $\delta=0.001$: $n=\ln(1000)/(2\times10^{-8})=345{,}387{,}764$ one-sided, $\ln(2000)/(2\times10^{-8})=380{,}045{,}123$ two-sided. Around 350–380 million.
>
> **(d)** Weak evidence. The gap 0.009 is within the worst-case 95% half-width of 0.01. At ~6% error the sd is $\sqrt{0.06\times0.94/10^4}=0.0024$, so the gap is about 1.9 sd: suggestive at best. A paired test on the same examples would be the right analysis, and a reused test set is not unbiased anyway.

> [!example]- **4.** *(Medium–hard) Entropy and block coding*
> Three equally likely symbols.
> **(a)** Entropy in bits; what goes wrong coding one symbol at a time? **(b)** Bits per symbol when coding $n=1,2,3,5,100,1000$ symbols jointly. **(c)** How many ternary digits encode $\{0,\dots,7\}$? **(d)** Link to this chapter's loss.
>
> ---
> **(a)** $\log_2 3=1.584963$ bits. One symbol needs 2 bits, 26.19% above the floor.
>
> **(b)** $\lceil n\log_2 3\rceil$ bits for $n$ symbols:
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
> $n=2$ gains nothing ($9$ messages still need 4 bits). The rounding waste is spread over $n$ symbols, so the overhead falls like $1/n$: the entropy bound is reached only with long blocks.
>
> **(c)** 2 ternary digits ($3^2=9\ge8$) vs 3 bits. Each ternary digit carries 1.585 bits, so fewer symbols are sent, at the cost of distinguishing three signal levels (as in PAM-3).
>
> **(d)** Cross-entropy is the expected code length under a believed distribution $Q$; it equals $H(P)+D_{\mathrm{KL}}(P\|Q)$. No code beats $H(P)$, and no classifier gets cross-entropy below the data's entropy.

> [!example]- **5.** *(Hard) Label shift and conditioning*
> Source labels $q=(0.5,0.3,0.2)$, $\mathbf{C}$ as in §11.4, test mean output $\mu=(0.225,0.335,0.440)$.
> **(a)** Check $\mathbf{C}$ and give source accuracy. **(b)** Recover $p(\mathbf{y})$ and $\beta$. **(c)** Error from using $\mu$ directly? **(d)** Repeat with a classifier of $\kappa(\mathbf{C})=104$ and 0.005 noise in $\mu$.
>
> ---
> **(a)** Columns sum to 1. Accuracy $=0.85(0.5)+0.80(0.3)+0.80(0.2)=82.5\%$.
>
> **(b)** $p=\mathbf{C}^{-1}\mu=(0.2,0.3,0.5)$; $\beta=(0.4,1.0,2.5)$.
>
> **(c)** $(0.225,0.335,0.440)$ vs truth: +12.5%, +11.7%, −12.0%. The class that became common (class 3) is understated.
>
> **(d)** Exact $\mu$ still gives the right answer, but with noise $\hat p=(0.100,0.800,0.100)$, error 0.648 against 0.0098 for the good classifier (65.9×), and the result still looks like a valid distribution. Invertibility is not enough; noise is amplified by roughly $\kappa(\mathbf{C})$. Same as [[02 - Linear Regression]] exercise 4.

## 📝 Summary

- Classification changes three things from regression: one-hot targets, one affine output per class (one redundant degree of freedom), and cross-entropy loss.
- Softmax $\hat y_i=e^{o_i}/\sum_j e^{o_j}$ gives a probability vector and preserves order, so prediction can use argmax of the logits.
- Cross-entropy is the negative log-likelihood under a categorical model; for one-hot labels it is $-\log\hat y_{\text{true}}$, unbounded for confident mistakes.
- Gradient $\hat{\mathbf{y}}-\mathbf{y}$; Hessian = covariance of $\hat{\mathbf{y}}$.
- Two-class softmax = sigmoid of $o_1-o_2$. Only logit differences mean anything.
- $H(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q)$: minimizing cross-entropy minimizes KL, with floor $H(P)$.
- Bernoulli variance gives 2,500 test examples for one sd of 0.01 and 10,000 for two. Reusing a test set biases it.
- VC theory does not explain why large networks generalize.
- Shift types: covariate (reweight with $\exp(h(\mathbf{x}))$ from a logistic discriminator), label (solve $\mathbf{C}p=\mu$, watch conditioning), concept (retrain). Deploying a model can change the data it sees.

## ⚠️ Important Notes

1. Integer labels imply an order; use them only for genuinely ordinal classes.
2. Softmax parameters are not identifiable: do not interpret single logits or weights.
3. Pass logits to the loss. Doing softmax then log yourself can overflow (`nan` on $(1000,1001,1002)$).
4. One confidently wrong prediction can dominate a batch's loss.
5. The gradient $\hat{\mathbf{y}}-\mathbf{y}$ sums to zero across classes; a quick sanity check.
6. A saturated softmax has tiny gradient and tiny curvature (a route to vanishing gradients, [[04 - Neural Network]]).
7. Squared loss on one-hot targets is not absurd, just unnormalized and outlier-sensitive.
8. Temperature: $Q(i)\propto P(i)^\lambda$ gives $T_{\text{eff}}=T/\lambda$. $\lambda\to\infty$ collapses to argmax, $\lambda\to0$ gives uniform. For $(0.6,0.3,0.1)$ entropy goes from 0.898 to 0.594 nats at $\lambda=2$ and to $\ln3=1.0986$ as $\lambda\to0$.
9. The 0.25 variance bound is worst case; low-error models need fewer test examples.
10. $O(1/\sqrt n)$: 100× more precision costs 10,000× more data.
11. A test set is spoiled by repeated use, even without cheating.
12. "Any fixed classifier generalizes": the difficulty is choosing $f$ from the data.
13. Identify the causal direction before choosing a shift correction.
14. Clip importance weights; zero training density in a target region cannot be fixed.
15. The label-shift confusion matrix must be column-conditional.
16. A model that influences behaviour changes its own input distribution; monitor it ([[MLOps/contents/00-Index|MLOps]]).

> [!warning] Gaps in the source material
> - **Figures:** the softmax-as-network diagram is reconstructed from the prose. The photo/cartoon images and the soft-drink map are lost but only illustrate claims stated in the text.
> - **Formulas:** this chapter showed that `!` means `→` and that `λ` is deleted. Exercise 5.4 extracts as `Showthatfor !1 wehave 1RealSoftMax(a; b)! max(a; b)`, i.e. for $\lambda\to\infty$, $\lambda^{-1}\mathrm{RealSoftMax}(\lambda a,\lambda b)\to\max(a,b)$.
> - **Added by me:** the KL decomposition; the Hessian solution (D2L ex. 1); the binary reduction and $d+1$ count; the one-/two-sided caveat (18,444 vs 10,000, logged as a declined discrepancy); the block-coding table; the full label-shift example including the $\kappa=104$ failure; the column-conditional remark; the temperature calculation; the overflow demo.
> - **Cross-check with ch. 01:** D2L says a 1995 Sun SPARCStation 5 had 64 MB and 5 MFLOPS. Against Table 1.5.1's 1990 row (10 MB, 10 MF) the memory fits but compute is half, so the table's compute column looks optimistic. MNIST (47.04 MB at one byte per pixel) was 73.5% of that machine's RAM.
> - **Skipped:** the Fashion-MNIST pipeline and implementation sections; VC theory is stated, not derived.

**Previous:** [[02 - Linear Regression]] · **Next:** [[04 - Neural Network]]
