---
subject: Deep Learning
chapter: 2
tags: [ds, deep-learning, regression, sgd, regularization]
source: "Zhang, Lipton, Li & Smola, Dive into Deep Learning, ch. 3 Linear Neural Networks for Regression, §3.1–3.7 (book pp. 82–126)"
---

# Linear Regression

Linear regression is a one-layer network with no nonlinearity. It is worth a full chapter because every part of training (model, loss, optimizer, data pipeline, evaluation) appears here without an architecture to distract from it. Everything in [[04 - Neural Network]] is this chapter plus nonlinearity. The note follows D2L's order: theory (§3.1), the code framework (§3.2), synthetic data (§3.3), implementation from scratch (§3.4) and with PyTorch (§3.5), generalization (§3.6) and weight decay (§3.7).

## 📘 Main Knowledge

### 1. The model (§3.1.1)

Running example: predict house price from area and age. Two assumptions:

1. **Linearity**: the conditional mean $\mathbb{E}[Y \mid X = \mathbf{x}]$ is a weighted sum of the features. Individual targets can deviate because of noise.
2. **Gaussian noise**: the deviation is normally distributed. §4 shows this assumption produces the squared loss.

$$\hat y = w_1x_1 + \cdots + w_dx_d + b = \mathbf{w}^\top\mathbf{x} + b$$

Notation: $n$ examples, $d$ features. Superscripts index examples, subscripts index coordinates: $x^{(i)}_j$ is feature $j$ of example $i$. Stacking examples as rows gives the design matrix $\mathbf{X}\in\mathbb{R}^{n\times d}$ and all predictions at once, $\hat{\mathbf{y}} = \mathbf{X}\mathbf{w} + b$, with $b$ broadcast.

Strictly, $\mathbf{w}^\top\mathbf{x}+b$ is affine. Without $b$ the fit is forced through the origin. The usual trick is to append a column of 1s to $\mathbf{X}$ and absorb $b$ into $\mathbf{w}$.

### 2. The loss

$$\ell^{(i)}(\mathbf{w},b) = \tfrac{1}{2}\left(\hat y^{(i)} - y^{(i)}\right)^2, \qquad L(\mathbf{w},b) = \frac{1}{n}\sum_{i=1}^{n}\ell^{(i)}(\mathbf{w},b)$$

The $\tfrac12$ only cancels the 2 from differentiation; it does not change the minimizer. With the data fixed, $L$ is a function of the parameters only.

Squaring makes large errors count heavily. That pushes the model away from big mistakes and also makes it sensitive to outliers: one point at distance 10 costs as much as 100 points at distance 1.

### 3. The analytic solution

Absorb $b$ and minimize $\|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2$. Setting the gradient $2\mathbf{X}^\top(\mathbf{X}\mathbf{w}-\mathbf{y})$ to zero gives the normal equations:
$$\mathbf{X}^\top\mathbf{X}\mathbf{w} = \mathbf{X}^\top\mathbf{y} \quad\Longrightarrow\quad \mathbf{w}^* = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$$

This requires full column rank. The loss is convex, so the single critical point is the global minimum (see [[Optimization/contents/00-Index|Optimization]]). If columns are dependent, $\mathbf{X}^\top\mathbf{X}$ is singular and there is a whole subspace of minimizers. Near-dependence is also a problem: the solution becomes very sensitive to the data (exercise 4).

D2L's warning: "you should not get used to such good fortune." Linear regression is the last model in the course with a closed-form solution; everything later is solved by iteration.

### 4. Squared loss is maximum likelihood under Gaussian noise (§3.1.3)

Assume $y = \mathbf{w}^\top\mathbf{x} + b + \epsilon$ with $\epsilon \sim \mathcal{N}(0,\sigma^2)$. Then
$$P(y\mid\mathbf{x}) = \frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{1}{2\sigma^2}\left(y - \mathbf{w}^\top\mathbf{x} - b\right)^2\right)$$

Examples are independent, so the likelihood is a product. Take $-\log$:
$$-\log P(\mathbf{y}\mid\mathbf{X}) = \sum_{i=1}^{n}\left[\tfrac{1}{2}\log(2\pi\sigma^2) + \frac{1}{2\sigma^2}\left(y^{(i)}-\mathbf{w}^\top\mathbf{x}^{(i)}-b\right)^2\right]$$

The first term has no $\mathbf{w}$ or $b$, and $\sigma$ only scales the second. So minimizing MSE is maximum likelihood for a linear model with Gaussian noise.

This is the recipe for every loss in the course: pick a noise model, take the negative log-likelihood. Laplace noise gives the $\ell_1$ loss (exercise 2); Bernoulli noise gives cross-entropy in [[03 - Logistic Regression]]. For the estimator's properties see [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].

D2L's §3.1 exercises push the recipe to targets where Gaussian noise is wrong:

- **Prices** cannot be negative and fluctuate in relative terms, so regress $y=\log(\text{price})$: additive noise on the log is multiplicative noise on the price. Penny stocks add a discreteness problem: prices move in fixed ticks, a large relative step for a cheap stock.
- **Counts** (apples sold) are non-negative integers. The Poisson model $p(k\mid\lambda)=\lambda^ke^{-\lambda}/k!$ has mean $\lambda$. Its negative log-likelihood is $\lambda-k\log\lambda+\log k!$; with $\lambda=e^\theta$ the loss $e^\theta-k\theta$ is minimized at $\theta=\log k$, and $\lambda$ stays positive automatically.

### 5. Minibatch stochastic gradient descent (§3.1.1)

| Strategy | Examples per update | Problem |
|---|---|---|
| Full batch | all $n$ | one update per pass over the data; wasteful when the data is redundant |
| Pure SGD | 1 | hardware is much faster at matrix–vector work than at many vector–vector operations; some layers (batch norm) need more than one example |

The compromise: at step $t$ sample a minibatch $\mathcal{B}_t$ and update
$$(\mathbf{w},b) \leftarrow (\mathbf{w},b) - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}_t}\partial_{(\mathbf{w},b)}\,\ell^{(i)}(\mathbf{w},b)$$

For squared loss this is
$$\mathbf{w} \leftarrow \mathbf{w} - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}_t}\mathbf{x}^{(i)}\left(\mathbf{w}^\top\mathbf{x}^{(i)}+b-y^{(i)}\right),\qquad b \leftarrow b - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}_t}\left(\mathbf{w}^\top\mathbf{x}^{(i)}+b-y^{(i)}\right)$$

Each example moves $\mathbf{w}$ along its own feature vector, scaled by its residual, so well-predicted examples contribute almost nothing.

- Batch size 32–256 (preferably a power of 2) is a reasonable start.
- Batch size and learning rate are hyperparameters: anything not updated inside the training loop. Tune them on validation data.
- SGD does not reach the exact minimizer in finitely many steps, and runs differ because minibatches are random. This rarely matters: minimizing training loss is easy in practice; generalization is the hard part (§12).
- Linear regression has one global minimum. Deep networks have many minima and saddle points.

D2L uses "prediction" rather than "inference" because in statistics *inference* means estimating parameters.

### 6. Vectorization (§3.1.2)

D2L adds two 10,000-dimensional vectors two ways:

| Method | Printed time |
|---|---|
| Python `for` loop | `0.16781 sec` |
| one call to `+` | `0.00180 sec` |

The ratio is 93.23×. Per element that is 16.781 µs against 0.180 µs. At roughly $10^9$ additions per second, one addition takes about 1 ns, i.e. 0.0060% of the loop's per-element cost. Almost all of the loop's time is interpreter overhead, so vectorizing removes Python from the inner loop rather than speeding up arithmetic. (Compare [[Basic Programming (C++)/contents/00-Index|Basic Programming (C++)]].)

### 7. Linear regression as a neural network (§3.1.4)

Inputs $x_1,\dots,x_d$ form the input layer; there is one output $o_1$. Linear regression is a single-layer fully connected network: D2L counts only layers that compute something.

The biological analogy: dendrites receive inputs $x_i$, synaptic weights $w_i$ scale them, the nucleus sums $\sum_i x_iw_i + b$, an optional nonlinearity is applied, and the axon carries the result onward. D2L adds that airplanes were inspired by birds but aeronautics does not run on ornithology; modern deep learning draws more on mathematics, statistics and computer science than on neuroscience.

Stacking two linear layers does not help (D2L exercise 3.1.6): $\mathbf W_2(\mathbf W_1\mathbf x+\mathbf b_1)+\mathbf b_2=(\mathbf W_2\mathbf W_1)\mathbf x+(\mathbf W_2\mathbf b_1+\mathbf b_2)$ is again one affine map. Depth needs a nonlinearity between layers ([[04 - Neural Network]]). Quadratic features $x_ix_j$ can be added as extra inputs, which keeps the model linear in its parameters.

### 8. Object-oriented design for implementation (§3.2)

Every model in the book is trained with the same three classes, modelled on PyTorch Lightning:

| Class | Role | Key methods |
|---|---|---|
| `d2l.Module` (subclass of `nn.Module`) | model, loss, optimizer | `__init__` (parameters), `forward`, `loss`, `training_step`, `validation_step`, `configure_optimizers` |
| `d2l.DataModule` | data | `train_dataloader`, `val_dataloader` (both call `get_dataloader(train)`) |
| `d2l.Trainer` | joins the two | `fit(model, data)` loops `max_epochs` times over `fit_epoch` |

Three utilities make notebook-style code possible:

- `add_to_class(Class)`: a decorator that registers a function as a method of an existing class, even after instances exist. It lets D2L split one class over several code cells.
- `HyperParameters.save_hyperparameters(ignore=[])`: stores every `__init__` argument as an attribute (`B(a=1, b=2, c=3)` with `ignore=['c']` gives `self.a = 1`, `self.b = 2`, and no `self.c`).
- `ProgressBoard`: plots training curves live; `draw(x, y, label, every_n)` averages `n` neighbouring points.

`Module.training_step(batch)` computes `self.loss(self(*batch[:-1]), batch[-1])`: all but the last element of the batch are inputs, the last is the label. Calling `model(X)` runs `forward` because `nn.Module.__call__` calls it.

### 9. Synthetic regression data (§3.3)

Synthetic data with known parameters lets you check that a model recovers them. D2L draws 1000 training and 1000 validation examples:
$$\mathbf y=\mathbf X\mathbf w+b+\boldsymbol\epsilon,\qquad X_{ij}\sim\mathcal N(0,1),\quad \epsilon\sim\mathcal N(0,0.01^2),\quad \mathbf w=[2,-3.4]^\top,\; b=4.2.$$

```python
class SyntheticRegressionData(d2l.DataModule):
    def __init__(self, w, b, noise=0.01, num_train=1000, num_val=1000, batch_size=32):
        super().__init__()
        self.save_hyperparameters()
        n = num_train + num_val
        self.X = torch.randn(n, len(w))
        noise = torch.randn(n, 1) * noise
        self.y = torch.matmul(self.X, w.reshape((-1, 1))) + b + noise
```

The first example prints features $[2.2793,-0.2246]$, label 9.5014. Check: $2(2.2793)-3.4(-0.2246)+4.2=9.5222$, so that example's noise was $-0.0208$, about $2\sigma$.

**Reading the data.** A hand-written loader shuffles the training indices (validation stays in order, for reproducible debugging) and yields slices of `batch_size`:

```python
def get_dataloader(self, train):
    if train:
        indices = list(range(0, self.num_train))
        random.shuffle(indices)        # random order for training
    else:
        indices = list(range(self.num_train, self.num_train + self.num_val))
    for i in range(0, len(indices), self.batch_size):
        batch_indices = torch.tensor(indices[i: i + self.batch_size])
        yield self.X[batch_indices], self.y[batch_indices]
```

The first batch has `X` of shape `[32, 2]` and `y` of shape `[32, 1]`. This version keeps all data in memory and does random memory access, so D2L replaces it with the framework loader, which also handles files and streams:

```python
def get_tensorloader(self, tensors, train, indices=slice(0, None)):
    tensors = tuple(a[indices] for a in tensors)
    dataset = torch.utils.data.TensorDataset(*tensors)
    return torch.utils.data.DataLoader(dataset, self.batch_size, shuffle=train)
```

`len(data.train_dataloader())` is 32: $\lceil1000/32\rceil=32$ batches, the last holding only $1000-31\cdot32=8$ examples (pass `drop_last=True` to discard it). Loaders compose, so a whole preprocessing pipeline (load, crop, augment) can be one loader.

### 10. Implementation from scratch (§3.4)

Only tensors and autograd are used.

**Model.** Weights from $\mathcal N(0,0.01^2)$, bias 0:

```python
class LinearRegressionScratch(d2l.Module):
    def __init__(self, num_inputs, lr, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.w = torch.normal(0, sigma, (num_inputs, 1), requires_grad=True)
        self.b = torch.zeros(1, requires_grad=True)

def forward(self, X):
    return torch.matmul(X, self.w) + self.b     # b is broadcast to every row
```

**Loss.** Squared loss with the $\tfrac12$, averaged over the minibatch:

```python
def loss(self, y_hat, y):
    l = (y_hat - y) ** 2 / 2
    return l.mean()
```

**Optimizer.** Because the loss is already a minibatch *mean*, the learning rate need not be divided by the batch size:

```python
class SGD(d2l.HyperParameters):
    def __init__(self, params, lr):
        self.save_hyperparameters()
    def step(self):
        for param in self.params:
            param -= self.lr * param.grad
    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()

def configure_optimizers(self):
    return SGD([self.w, self.b], self.lr)
```

**Training loop.** One **epoch** passes once over the training data. Per minibatch: compute the loss, zero the gradients, backpropagate, step. Then evaluate on the validation loader without gradients:

```python
def fit_epoch(self):
    self.model.train()
    for batch in self.train_dataloader:
        loss = self.model.training_step(self.prepare_batch(batch))
        self.optim.zero_grad()
        with torch.no_grad():
            loss.backward()
            if self.gradient_clip_val > 0:      # see ch. 07
                self.clip_gradients(self.gradient_clip_val, self.model)
            self.optim.step()
        self.train_batch_idx += 1
    if self.val_dataloader is None:
        return
    self.model.eval()
    for batch in self.val_dataloader:
        with torch.no_grad():
            self.model.validation_step(self.prepare_batch(batch))
        self.val_batch_idx += 1
```

In symbols: initialize $(\mathbf w,b)$; repeat $\mathbf g\leftarrow\partial_{(\mathbf w,b)}\frac1{|\mathcal B|}\sum_{i\in\mathcal B}\ell(\mathbf x^{(i)},y^{(i)},\mathbf w,b)$, then $(\mathbf w,b)\leftarrow(\mathbf w,b)-\eta\mathbf g$.

Run with `lr=0.03`, `max_epochs=3`. D2L prints errors $\mathbf w-\hat{\mathbf w}=[0.1163,-0.2020]$ and $b-\hat b=0.2383$. Exact recovery is not guaranteed in general: deep models have no unique solution, and even linear models need linearly independent features. What we care about is accurate prediction, and SGD often finds it because many parameter settings predict well.

### 11. Concise implementation (§3.5)

The framework supplies layers, losses and optimizers. First-generation frameworks were Theano, DistBelief and Caffe; earlier, SN2 (1988) had a Lisp-like interface.

```python
class LinearRegression(d2l.Module):
    def __init__(self, lr):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.LazyLinear(1)              # input size inferred on first call
        self.net.weight.data.normal_(0, 0.01)    # methods ending in _ act in place
        self.net.bias.data.fill_(0)
    def forward(self, X):
        return self.net(X)
    def loss(self, y_hat, y):
        fn = nn.MSELoss()                        # mean squared error, no 1/2
        return fn(y_hat, y)
    def configure_optimizers(self):
        return torch.optim.SGD(self.parameters(), self.lr)
    def get_w_b(self):
        return (self.net.weight.data, self.net.bias.data)
```

A layer is **fully connected** when every input connects to every output through a matrix–vector product. `nn.Linear(in, out)` needs the input size; `nn.LazyLinear(out)` infers it, which helps later when input sizes after convolutions are tedious to compute.

Same data, same `lr=0.03`, 3 epochs. D2L prints errors $[0.0031,-0.0099]$ and $0.0127$, about **20× smaller** than from scratch.

**Why the concise run is so much better** (my analysis). The only real difference is the missing $\tfrac12$ in `nn.MSELoss`: its gradient is twice as large, so it behaves like the scratch code at $\eta=0.06$. With standardized features ($\mathbb E[\mathbf x\mathbf x^\top]=\mathbf I$), each step shrinks the parameter error by about $(1-\eta)$ for scratch and $(1-2\eta)$ for concise. Three epochs of 32 batches are 96 steps, and the initial error is about $|\mathbf w|$, $|b|$ because the init is near 0:

| | factor after 96 steps | predicted error $w_1, w_2, b$ | D2L prints | my 20-seed rerun |
|---|---|---|---|---|
| scratch | $0.97^{96}=0.0537$ | 0.107, 0.183, 0.226 | 0.116, 0.202, 0.238 | 0.109, 0.180, 0.219 |
| concise | $0.94^{96}=0.00263$ | 0.0053, 0.0089, 0.0111 | 0.0031, 0.0099, 0.0127 | 0.0058, 0.0090, 0.0104 |

Neither run has converged; both are still in the phase where the error decays geometrically from its starting value. The scratch run is not worse code, it took smaller steps.

D2L's §3.5 advice: use framework components when they exist (they are optimized and tested), but know how to write them, because researchers build components no library has yet. In PyTorch, `data` handles data loading and `nn` provides layers and losses.

**Huber loss** (D2L exercise 3.5.2), robust like $\ell_1$ for large residuals and smooth like $\ell_2$ near 0:
$$l(y,y')=\begin{cases}|y-y'|-\frac\sigma2 & |y-y'|>\sigma\\ \frac1{2\sigma}(y-y')^2 & \text{otherwise}\end{cases}$$
Both pieces equal $\sigma/2$ at $|y-y'|=\sigma$, so the loss is continuous with a continuous slope. With $\sigma=1$: residual 0.5 costs 0.125, residual 1 costs 0.5, 2 costs 1.5, 10 costs 9.5 (squared loss: 50). Its gradient is capped at $\pm1$, so one outlier (D2L suggests setting $y_5=10000$) cannot dominate a step. In PyTorch this form is `nn.SmoothL1Loss(beta=σ)`; `nn.HuberLoss(delta=δ)` is the same curve multiplied by $\delta$, so the two agree at 1.

### 12. Generalization (§3.6)

D2L's example: one student memorizes every past exam answer (100% on repeated questions, lost on new ones); another learns patterns (90% on old and new exams alike). We want the second, and need a way to tell them apart before the real exam.

#### 12.1 Training error vs. generalization error

$$R_{\text{emp}}[\mathbf{X},\mathbf{y},f] = \frac1n\sum_{i=1}^n \ell\!\left(\mathbf{x}^{(i)},y^{(i)},f(\mathbf{x}^{(i)})\right) \qquad\text{(a statistic)}$$
$$R[p,f] = \mathbb{E}_{(\mathbf{x},y)\sim P}\left[\ell(\mathbf{x},y,f(\mathbf{x}))\right] \qquad\text{(an expectation)}$$

$R$ cannot be computed because $p(\mathbf{x},y)$ is unknown. We estimate it on a held-out test set. On the test set the model is fixed, so the estimate is ordinary mean estimation and is unbiased. On the training set the model was chosen using that same sample, so training error is biased downward.

All of this assumes IID data: training and test examples drawn independently from the same distribution. Without that assumption (or another one linking the two distributions) nothing can be said about generalization. Distribution shift is covered in [[03 - Logistic Regression]].

#### 12.2 Model complexity

If a model class can fit any labels, even random ones, then fitting the training data says nothing about generalization. If it could not fit arbitrary labels, a good fit means it found a pattern. D2L links this to Popper's falsifiability: a theory that explains every possible observation tells us nothing.

Complexity is not just parameter count. Kernel methods have infinitely many parameters and controlled complexity. A useful second measure is the range of values the parameters may take, which is what weight decay restricts (§13).

Low training error from a very flexible model does not imply high generalization error either. It only means training error alone certifies nothing, so we check on held-out validation data.

#### 12.3 Underfitting and overfitting

| Symptom | Diagnosis | Action |
|---|---|---|
| training and validation error both high, small gap | underfitting | more expressive model |
| training error much lower than validation error | overfitting | regularize or get more data |

A gap is not automatically bad. The best deep models often do much better on training data than validation data. What matters is validation error. If training error is zero, the gap equals the generalization error.

Polynomial regression $\hat y = \sum_{i=0}^{d} x^i w_i$ is still linear regression (features are powers of $x$). Raising the degree never increases training error, and with $n$ distinct $x$ values a degree $n-1$ polynomial fits the training set exactly.

With a fixed model, less data means more overfitting. Model complexity should not grow faster than the amount of data; deep networks typically beat linear models only with many thousands of examples.

#### 12.4 Model selection

Never use the test set to choose a model: if you overfit the test set, nothing will tell you. Use a three-way split (train / validation / test). D2L admits its own reported accuracies are validation accuracies, since the book has no true test sets.

$K$-fold cross-validation, for small datasets: split the training data into $K$ parts, train $K$ times each holding out one part, average the $K$ validation errors. Cost: $K$ trainings.

D2L's rules of thumb: select on validation data; more complex models need more data; complexity means both parameter count and parameter range; more data almost always helps; everything rests on IID.

### 13. Weight decay (§3.7)

Restricting features is a coarse tool. With $k$ variables the number of monomials of degree $d$ is $\binom{k-1+d}{k-1}$. For $k=200$:

| Degree $d$ | Monomials |
|---|---|
| 1 | 200 |
| 2 | 20,100 |
| 3 | 1,353,400 |
| 4 | 68,685,050 |

Going from degree 2 to 3 multiplies the feature count by 67.33×. Weight decay gives a continuous control instead, by penalizing the size of the weights:
$$L(\mathbf{w},b) + \frac{\lambda}{2}\|\mathbf{w}\|^2$$

$\lambda \ge 0$ is tuned on validation data; $\lambda=0$ is the plain loss. The SGD update becomes
$$\mathbf{w} \leftarrow (1-\eta\lambda)\,\mathbf{w} - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}}\mathbf{x}^{(i)}\left(\mathbf{w}^\top\mathbf{x}^{(i)}+b-y^{(i)}\right)$$

The factor $(1-\eta\lambda)$ shrinks the weights toward zero every step, hence the name.

| | $\ell_2$ (ridge, weight decay) | $\ell_1$ (lasso) |
|---|---|---|
| Penalty | $\|\mathbf{w}\|^2$ | $\sum_j|w_j|$ |
| Effect | penalizes large weights most; spreads weight over many features | sets many weights exactly to zero |
| Use | robustness to noise in any single feature | feature selection |

The bias is usually not penalized. PyTorch's optimizer `weight_decay` decays every parameter it is given, so D2L puts only `net.weight` in the decayed group. For SGD, $\ell_2$ regularization and weight decay are the same thing; for Adam they are not (see [[04 - Neural Network]]).

### 14. D2L's weight-decay experiment

Setup: $y = 0.05 + \sum_{i=1}^{200} 0.01\,x_i + \epsilon$, $\epsilon\sim\mathcal{N}(0, 0.01^2)$; 20 training examples, 100 validation; 10 epochs at batch size 5, so 40 updates in total. D2L prints:

| Run | Printed `l2_penalty(w)` |
|---|---|
| scratch, $\lambda = 0$ | `0.009889112785458565` |
| scratch, $\lambda = 3$ | `0.0014726519584655762` |
| concise, `wd=3` | `0.01231398992240429` |

Three things to notice (my analysis, not D2L's):

1. **The caption is wrong.** It says `'L2 norm of w: '` but `l2_penalty` returns $\tfrac12\|\mathbf{w}\|^2$. The actual norms are 0.1406 and 0.0543 (ratio 2.59×, not 6.72×).
2. **A correct norm does not mean a correct vector.** The true value of the printed quantity is $\tfrac12 \times 200 \times 0.01^2 = 0.0100$, so the overfitting run is within 1.11% of it. A NumPy reproduction over 200 seeds shows what that hides:

| | $\tfrac12\|\mathbf{w}\|^2$ | $\|\hat{\mathbf{w}}-\mathbf{w}_{\text{true}}\|$ | $\cos(\hat{\mathbf{w}},\mathbf{w}_{\text{true}})$ | train loss | val loss |
|---|---|---|---|---|---|
| $\lambda=0$ | 0.01007 | 0.1907 | 0.092 | 0.0000118 | 0.01924 |
| $\lambda=3$ | 0.00144 | 0.1410 | 0.195 | 0.000463 | 0.01096 |

$\|\mathbf{w}_{\text{true}}\| = 0.1414$. The unregularized estimate has the right length but its error (0.1907) is larger than the true vector itself and it points about 84.7° away. With 20 examples in 200 dimensions, the data only constrains a 20-dimensional subspace; the other 180 directions are filled by noise. The regularized estimate is too short but closer, better aligned, and has 1.76× lower validation loss.

3. **The concise run is not comparable.** It prints 0.012314 at the same nominal $\lambda=3$, 8.4× the scratch value. `nn.MSELoss` lacks the $\tfrac12$ (halving the effective $\lambda$), and PyTorch's default init $\mathcal{U}(-1/\sqrt d, 1/\sqrt d)$ starts at $\tfrac12\|\mathbf{w}\|^2 = 0.1667$ instead of 0.0100. Forty updates cannot forget that start: pure decay predicts $0.1667\times(1-\eta\lambda)^{80} = 0.0146$, and a simulation gives 0.0140.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Normal equations by hand*
> Four houses, features (area, age) and an intercept column:
> $$\mathbf{X}=\begin{pmatrix}1&1&1\\2&1&1\\3&2&1\\4&2&1\end{pmatrix},\qquad \mathbf{y}=\begin{pmatrix}4\\7\\9\\13\end{pmatrix}$$
> **(a)** Solve the normal equations. **(b)** Give fitted values, residuals and SSE. Why do the residuals sum to zero? **(c)** What changes if you drop the $\tfrac12$ from the loss?
>
> ---
> **(a)** $\mathbf{X}^\top\mathbf{X}=\begin{pmatrix}30&17&10\\17&10&6\\10&6&4\end{pmatrix}$, $\mathbf{X}^\top\mathbf{y}=(97,55,33)^\top$, $\det=4$. Solution: $w_{\text{area}}=3.5$, $w_{\text{age}}=-1.5$, $b=1.75$.
>
> **(b)** Fitted $(3.75, 7.25, 9.25, 12.75)$; residuals $(-\tfrac14,+\tfrac14,+\tfrac14,-\tfrac14)$; SSE $=\tfrac14$. The normal-equation row for the column of 1s says $\sum_i r_i = 0$, so any fit with an intercept has residuals summing to zero.
>
> **(c)** The minimizer is unchanged. The gradient doubles, so at a fixed learning rate SGD takes steps twice as large. This is one cause of the concise/scratch mismatches in §11 and §14.

> [!example]- **2.** *(Easy–medium) Change the noise model, change the loss*
> **(a)** Find the constant $b$ minimizing $\sum_i(x_i-b)^2$. **(b)** Minimize $\sum_i|x_i-b|$ instead; which noise model does it correspond to? **(c)** Try both on $\{2,4,4,5,10\}$. **(d)** For noise $p(\epsilon)=\tfrac12 e^{-|\epsilon|}$, write the negative log-likelihood and say what goes wrong for SGD near the optimum.
>
> ---
> **(a)** Derivative $-2\sum_i(x_i-b)=0$ gives $b=\bar x$, the mean: the MLE of a Gaussian's location.
>
> **(b)** The derivative is $-\sum_i\operatorname{sign}(x_i-b)$, zero when half the points lie on each side: $b$ = median. This is the MLE under Laplace noise.
>
> **(c)** Mean 5, median 4. $\sum|x_i-4|=9$, $\sum|x_i-5|=10$, so the median wins under $\ell_1$. The single value 10 pulls the mean up and does not move the median.
>
> **(d)** $-\log P = n\log 2 + \sum_i|y^{(i)}-\mathbf{w}^\top\mathbf{x}^{(i)}-b|$, the $\ell_1$ loss. Its gradient is $\pm1$ however small the residual, so with a fixed $\eta$ SGD keeps oscillating around the minimum. Fix: decay the learning rate, or use the smooth Huber loss.

> [!example]- **3.** *(Medium) One SGD step, then 96*
> **(a)** Start at $\mathbf w=(0,0)$, $b=0$. Take a minibatch of two examples, $\mathbf x=(1,1), y=4$ and $\mathbf x=(2,1), y=7$, with the averaged loss $\tfrac12(\hat y-y)^2$ and $\eta=0.1$. Compute the gradient, the new parameters and the minibatch loss before and after.
> **(b)** In D2L's synthetic problem ($\mathbf w=[2,-3.4]$, $b=4.2$, standard normal features) each step shrinks the error by about $(1-\eta)$. Predict the errors after 3 epochs of 32 batches at $\eta=0.03$.
> **(c)** The concise version uses `nn.MSELoss` at the same $\eta$. Predict its errors and explain the difference.
>
> ---
> **(a)** Residuals $\hat y-y=(-4,-7)$. $\partial_{\mathbf w}=\tfrac12[(1,1)(-4)+(2,1)(-7)]=(-9,-5.5)$, $\partial_b=\tfrac12(-11)=-5.5$. New $\mathbf w=(0.9,0.55)$, $b=0.55$. Loss $\tfrac14(16+49)=16.25$ before; residuals become $(-2,-4.1)$ and the loss $\tfrac14(4+16.81)=5.2025$ after.
>
> **(b)** 96 steps: $0.97^{96}=0.0537$. Errors $\approx 0.107, 0.183, 0.226$; D2L prints 0.116, 0.202, 0.238.
>
> **(c)** No $\tfrac12$ means a doubled gradient, so the factor is $(1-0.06)^{96}=0.00263$ and the errors $\approx0.005, 0.009, 0.011$; D2L prints 0.003, 0.010, 0.013. Same model and data, but twice the effective learning rate: after only 96 steps that is a 20× difference.

> [!example]- **4.** *(Medium–hard) Full rank is not enough*
> Use $\mathbf{X}$ from exercise 1. **(a)** Compute corr(area, age) and the condition number of $\mathbf{X}^\top\mathbf{X}$. **(b)** Change $y_2$ from 7 to 7.1. How far does $\mathbf{w}$ move? **(c)** Repeat with ridge, $\lambda=1$, and report $\mathbf{w}_{\text{ridge}}$. **(d)** Using the SVD, give ridge's shrinkage factor per direction.
>
> ---
> **(a)** corr $=0.8944$. Singular values of $\mathbf{X}$: $(6.572, 0.8185, 0.3718)$, so $\kappa(\mathbf{X}^\top\mathbf{X}) = 312.46$. The matrix is full rank ($\det=4$) and still badly conditioned.
>
> **(b)** $\Delta\mathbf{w} = (0.05,-0.15,0.125)$, $\|\Delta\mathbf{w}\| = 0.2016$: a 0.1 change in one label moves the parameters by twice that, mostly in the collinear age coefficient.
>
> **(c)** $\|\Delta\mathbf{w}\| = 0.0278$, 7.25× less sensitive. $\mathbf{w}_{\text{ridge}} = (\tfrac{17}{7},\tfrac{6}{7},\tfrac{5}{7}) \approx (2.429, 0.857, 0.714)$. The age coefficient changes sign (−1.5 → +0.857); SSE rises from 0.25 to 1.571. Under collinearity a coefficient's sign is not reliable.
>
> **(d)** With $\mathbf{X}=\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$:
> $$\mathbf{w}_{\text{OLS}} = \sum_j \frac{1}{\sigma_j}(\mathbf{u}_j^\top\mathbf{y})\mathbf{v}_j, \qquad \mathbf{w}_{\text{ridge}} = \sum_j \frac{\sigma_j}{\sigma_j^2+\lambda}(\mathbf{u}_j^\top\mathbf{y})\mathbf{v}_j$$
> Ridge scales direction $j$ by $\sigma_j^2/(\sigma_j^2+\lambda)$: here 0.977, 0.401, 0.121. Well-determined directions pass almost unchanged; poorly determined ones (small $\sigma_j$, where OLS's $1/\sigma_j$ blows up) are shrunk hard.

> [!example]- **5.** *(Hard) Audit the weight-decay experiment*
> $d=200$, $n_{\text{train}}=20$, true $w_i=0.01$, noise sd 0.01, 10 epochs, batch 5, $\eta=0.01$. Printed `l2_penalty(w)`: 0.009889 ($\lambda=0$), 0.001473 ($\lambda=3$).
> **(a)** What is printed? Convert to $\|\mathbf{w}\|$. **(b)** What is the true value of the printed quantity? **(c)** Did the $\lambda=0$ run recover the truth? **(d)** How many updates were made, and why does that explain the concise run's 0.012314?
>
> ---
> **(a)** $\tfrac12\|\mathbf{w}\|^2$. Norms: 0.1406 and 0.0543.
>
> **(b)** $\tfrac12\cdot200\cdot0.01^2 = 0.0100$. The $\lambda=0$ run is 1.11% below it, the $\lambda=3$ run 85.3% below.
>
> **(c)** No. A norm says nothing about direction. Over 200 seeds the $\lambda=0$ error $\|\hat{\mathbf{w}}-\mathbf{w}_{\text{true}}\| = 0.1907$ exceeds $\|\mathbf{w}_{\text{true}}\| = 0.1414$, with cosine 0.092 (about 84.7°); predicting $\mathbf{0}$ would be closer. The $\lambda=3$ run has error 0.1410, cosine 0.195 and validation loss 0.01096 vs 0.01924. The 20 examples only pin down a 20-dimensional subspace.
>
> **(d)** $10 \times 20/5 = 40$ updates for 200 parameters, far from convergence. The concise model's default init gives $\tfrac12\|\mathbf{w}\|^2 \approx 0.1667$ at the start; decay alone predicts $0.1667\times(1-\eta\lambda)^{80} = 0.0146$, and simulation gives 0.0140. The printed value mostly reflects initialization, so it cannot be compared with the scratch run.

## 📝 Summary

- The model is affine, $\hat{\mathbf{y}}=\mathbf{X}\mathbf{w}+b$; absorb $b$ with a column of 1s.
- Minimizing squared loss is maximum likelihood under Gaussian noise. Laplace noise gives $\ell_1$ and the median.
- The normal equations $\mathbf{X}^\top\mathbf{X}\mathbf{w}=\mathbf{X}^\top\mathbf{y}$ need full rank, but conditioning is what decides how stable the solution is.
- Minibatch SGD: average the gradient over a random batch and step by $\eta$. Batches of 32–256 are typical. Results are approximate and vary between runs.
- Vectorize: the loop in D2L's benchmark is 93× slower, almost all of it interpreter overhead.
- Code pattern used for the whole book: `Module` (model, loss, optimizer), `DataModule` (loaders), `Trainer.fit` (epochs of zero_grad → backward → step, then validation under `no_grad`).
- The scratch and concise runs differ 20× only because `nn.MSELoss` has no $\tfrac12$: twice the effective learning rate over 96 unconverged steps.
- Training error is biased because the model was fitted on it; test error on a fixed model is unbiased. Everything assumes IID.
- Complexity = parameter count and parameter range. Weight decay adds $\tfrac{\lambda}{2}\|\mathbf{w}\|^2$, giving the update factor $(1-\eta\lambda)$, and in SVD terms shrinks direction $j$ by $\sigma_j^2/(\sigma_j^2+\lambda)$.
- A norm can be right while the vector is wrong: in D2L's experiment the overfitting model's norm is 1.1% from the truth while it points 85° away.

## ⚠️ Important Notes

1. Without the bias you can only fit hyperplanes through the origin.
2. $x^{(i)}_j$: superscript = example, subscript = feature.
3. The $\tfrac12$ factors do not change the minimizer but do double/halve the gradient, which matters at a fixed learning rate and step count.
4. Full rank guarantees a unique solution, not a stable one. Check the condition number.
5. Squared loss is sensitive to outliers. The principled fix is a different noise model (Laplace, Huber), not deleting data.
6. SGD is random; report averages over seeds, not one run.
7. Hyperparameters (η, batch size, λ, architecture) are tuned on validation data, never on the test set.
8. Training error is biased because the model depends on the training sample, not because training data is easier.
9. A model that can fit arbitrary labels can have low training error and still generalize well or badly; training error alone proves nothing.
10. Parameter count is only a proxy for complexity. Large networks often generalize better than small ones.
11. Read the code that produces a printed number, not just its caption (`l2_penalty` prints $\tfrac12\|\mathbf{w}\|^2$).
12. Compare runs only when everything except the variable of interest is the same. Few updates on many parameters leave a model close to its initialization.
13. Weight decay and $\ell_2$ regularization coincide for SGD only (AdamW exists because they differ for Adam).
14. PyTorch's `weight_decay` also decays biases unless you use parameter groups.
15. A working regularizer raises training loss: in §14 training loss rose 39× while validation loss fell 1.76×.
16. Order inside the loop: `zero_grad()` → `backward()` → `step()`. Evaluation goes under `torch.no_grad()` and `model.eval()`.
17. If $n$ is not divisible by the batch size, the last batch is smaller (8 of 1000 at size 32); `drop_last=True` drops it.
18. Shuffle the training set every epoch; keep validation order fixed. A dataset sorted by label can make SGD drift one way for many steps.
19. Huber / smooth-$\ell_1$ caps the gradient at $\pm1$; it is the cheap compromise between squared and absolute loss.

> [!warning] Gaps in the source material
> - **Figures:** all are images. The single-layer network diagram and the neuron diagram are fully described by the prose and reconstructed above. The 1-D fit, the complexity curve and the training curves are lost.
> - **Formulas** extract with arrows, minus signs, $\eta$ and fraction bars deleted; every formula here was rebuilt from the prose and checked numerically.
> - **Added by me:** the ratio of D2L's two timings and the per-element breakdown (§6); the monomial table at $k=200$; the whole audit of the weight-decay experiment, including the 200-seed NumPy reproduction (within 1.8% and 2.3% of the printed values); exercise 4 (condition number, sensitivity, sign flip, SVD shrinkage); the Laplace/median derivation in exercise 2. D2L asks exercises 2 and 4 without answers.
> - **Taken from the source unverified:** historical citations, the 32–256 batch-size advice, the hardware-efficiency claim, the timing printouts.
> - **Also added by me:** the first-example noise check; the $(1-\eta)^{96}$ explanation of the scratch vs concise errors with a 20-seed PyTorch rerun (§11); the Huber values.
- **Skipped:** `ProgressBoard` internals and plotting code; D2L defers `save_hyperparameters` and `draw` to its appendix B.7. $K$-fold CV is described, not implemented.

**Previous:** [[01 - Introduction to Deep Learning]] · **Next:** [[03 - Logistic Regression]]
