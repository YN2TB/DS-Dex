---
subject: Deep Learning
chapter: 3
tags: [ds, deep-learning, classification, softmax, cross-entropy, distribution-shift]
source: "Zhang, Lipton, Li & Smola, Dive into Deep Learning, ch. 4 Linear Neural Networks for Classification, §4.1–4.7 (book pp. 127–169)"
---

# Logistic Regression

> [!info] Naming The lectures (3.1, 3.2) derive binary logistic regression from maximum likelihood and the softmax gradient in matrix form: §15–16.
> The syllabus says *Logistic Regression*; D2L calls the chapter *Softmax Regression*. Softmax regression with $q=2$ classes is exactly binary logistic regression (§7), so this note covers the general case. Compared with [[02 - Linear Regression]], three things change: the targets (one-hot), the output layer (one affine function per class) and the loss (cross-entropy). The note follows D2L's order: theory (§4.1), the Fashion-MNIST data (§4.2), the `Classifier` base class (§4.3), implementations from scratch and with PyTorch (§4.4–4.5), generalization (§4.6) and distribution shift (§4.7).

## 📘 Main Knowledge

### 1. Regression vs. classification (§4.1)

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

The parametrization has one redundant degree of freedom: since probabilities sum to 1, $q-1$ outputs would be enough. D2L keeps all $q$ for symmetry. Consequences: adding a constant to every logit changes nothing (§12), the binary case depends only on $o_1-o_2$ (§7), and individual logits or weights cannot be interpreted, only differences.

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

Logistic regression reappears in §14.3 as a tool for estimating density ratios.

### 8. Information theory (§4.1.3)

**Entropy** $H[P]=-\sum_j P(j)\log P(j)$ is the minimum average code length for data from $P$ (Shannon, 1948). In nats with natural log; $1\text{ nat}=1/\ln 2\approx1.4427$ bits.

**Surprisal** of an event with probability $P(j)$ is $-\log P(j)$. Predictable data is compressible. Entropy is the expected surprisal of an observer who knows the true probabilities.

**Cross-entropy** $H(P,Q)=-\sum_j P(j)\log Q(j)$ is the expected surprisal of an observer who believes $Q$ while the data comes from $P$. It is minimized at $Q=P$.

The gap is the KL divergence (D2L does not state this):
$$H(P,Q)=H(P)+D_{\mathrm{KL}}(P\,\|\,Q)$$
Check with $P=(0.7,0.2,0.1)$, $Q=(0.5,0.3,0.2)$: $H(P)=0.801819$, $D_{\mathrm{KL}}=0.085123$, sum $0.886941=H(P,Q)$. $H(P)$ is fixed by the data, so minimizing cross-entropy minimizes KL divergence, and $H(P)$ is the floor.

So training with cross-entropy can be read two ways: maximize the likelihood of the labels, or minimize the bits needed to transmit them.

**Cost.** A fully connected output layer with $d$ inputs and $q$ outputs costs $O(dq)$. Structured alternatives (Deep Fried Convnets, quaternion-style decompositions) reduce this, though what matters in practice is speed on GPUs, not FLOP counts.

### 9. The image classification dataset (§4.2)

**MNIST** (LeCun et al., 1998): 60,000 training and 10,000 test images of handwritten digits, $28\times28$. In 1995 a Sun SPARCStation 5 with 64 MB RAM and 5 MFLOPS was state of the art at AT&T Bell Labs; LeNet-5, SVMs with invariances and tangent-distance classifiers all reached under 1% error, which helped automate USPS letter sorting. Today even simple models exceed 95%, so MNIST is a sanity check, not a benchmark. ImageNet is the relevant challenge but too slow for the book's examples.

D2L uses **Fashion-MNIST** (Xiao et al., 2017): 10 clothing classes, $28\times28$ grayscale, 6,000 training and 1,000 test images per class (60,000 / 10,000).

```python
class FashionMNIST(d2l.DataModule):
    def __init__(self, batch_size=64, resize=(28, 28)):
        super().__init__()
        self.save_hyperparameters()
        trans = transforms.Compose([transforms.Resize(resize),
                                    transforms.ToTensor()])
        self.train = torchvision.datasets.FashionMNIST(
            root=self.root, train=True, transform=trans, download=True)
        self.val = torchvision.datasets.FashionMNIST(
            root=self.root, train=False, transform=trans, download=True)

    def text_labels(self, indices):
        labels = ['t-shirt', 'trouser', 'pullover', 'dress', 'coat',
                  'sandal', 'shirt', 'sneaker', 'bag', 'ankle boot']
        return [labels[int(i)] for i in indices]

    def get_dataloader(self, train):
        data = self.train if train else self.val
        return torch.utils.data.DataLoader(data, self.batch_size, shuffle=train,
                                           num_workers=self.num_workers)
```

- Images are stored as **$c\times h\times w$** tensors (channels, height, width). `data.train[0][0].shape` is `[1, 32, 32]` after resizing to 32. RGB images have 3 channels; hyperspectral images can have over 100 (HyMap: 126).
- A minibatch is `X: [64, 1, 32, 32]` (float32) and `y: [64]` (int64): labels are class indices, not one-hot vectors.
- One pass over the training loader took 5.41 s in D2L's run. That is slow, but a deep network's compute takes longer, so training is not I/O bound.
- Always look at your data (`visualize` shows images with their text labels): humans spot oddities quickly.

### 10. The base classification model (§4.3)

`Classifier` extends `Module` so that validation reports both loss and **accuracy**:

```python
class Classifier(d2l.Module):
    def validation_step(self, batch):
        Y_hat = self(*batch[:-1])
        self.plot('loss', self.loss(Y_hat, batch[-1]), train=False)
        self.plot('acc', self.accuracy(Y_hat, batch[-1]), train=False)

def accuracy(self, Y_hat, Y, averaged=True):
    Y_hat = Y_hat.reshape((-1, Y_hat.shape[-1]))
    preds = Y_hat.argmax(axis=1).type(Y.dtype)       # predicted class per row
    compare = (preds == Y.reshape(-1)).type(torch.float32)
    return compare.mean() if averaged else compare
```

Accuracy is the fraction of correct hard predictions. It is not differentiable, so we train on cross-entropy, but it is usually the number we report. The `.type(Y.dtype)` cast is needed because `==` is sensitive to data types.

**Averaging over batches.** The validation curve is the mean of per-batch means. That is exact only when all batches are equal in size. Fashion-MNIST's 10,000 validation images at batch size 256 give 39 full batches and one of 16. If $L^q_v$ is the mean of the 40 batch losses and $l^b_v$ the last batch's loss, the true validation loss is
$$L_v=\frac{256\,(40L^q_v-l^b_v)+16\,l^b_v}{10{,}000}.$$
The quick estimate is still unbiased in expectation over random batches (D2L ex. 4.3.2), but it gives the 16 examples of the last batch 16× the weight of the others.

### 11. Softmax regression from scratch (§4.4)

**Softmax.** Exponentiate, sum each row (`keepdims=True` keeps a column for broadcasting), divide. The denominator is the **partition function**, a name from statistical physics.

```python
X = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
X.sum(0, keepdims=True), X.sum(1, keepdims=True)   # [[5., 7., 9.]], [[6.], [15.]]

def softmax(X):
    X_exp = torch.exp(X)
    partition = X_exp.sum(1, keepdims=True)
    return X_exp / partition        # broadcasting
```

On random input each row sums to 1. D2L warns this code is not robust to very large or very small arguments (§12).

**Model.** Flatten each $28\times28$ image to a vector of 784; 10 outputs; $\mathbf W\in\mathbb R^{784\times10}$ from $\mathcal N(0,0.01^2)$, $\mathbf b\in\mathbb R^{10}$ zeros: $784\cdot10+10=7{,}850$ parameters.

```python
class SoftmaxRegressionScratch(d2l.Classifier):
    def __init__(self, num_inputs, num_outputs, lr, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.W = torch.normal(0, sigma, size=(num_inputs, num_outputs),
                              requires_grad=True)
        self.b = torch.zeros(num_outputs, requires_grad=True)
    def parameters(self):
        return [self.W, self.b]
    def forward(self, X):
        X = X.reshape((-1, self.W.shape[0]))
        return softmax(torch.matmul(X, self.W) + self.b)
```

**Cross-entropy by indexing.** With integer labels, `y_hat[range(n), y]` picks the probability of each true class, so no one-hot matrix or loop is needed:

```python
y = torch.tensor([0, 2])
y_hat = torch.tensor([[0.1, 0.3, 0.6], [0.3, 0.2, 0.5]])
y_hat[[0, 1], y]                    # tensor([0.1000, 0.5000])

def cross_entropy(y_hat, y):
    return -torch.log(y_hat[list(range(len(y_hat))), y]).mean()
cross_entropy(y_hat, y)             # tensor(1.4979)
```

Check: $\tfrac12(-\ln0.1-\ln0.5)=\tfrac12(2.302585+0.693147)=1.497866$. (Accuracy on this toy batch is 0.5: both rows predict class 2.)

**Training.** `FashionMNIST(batch_size=256)`, `lr=0.1`, 10 epochs, reusing `Trainer.fit` from [[02 - Linear Regression]]. That is $\lceil60{,}000/256\rceil=235$ updates per epoch. D2L treats the Fashion-MNIST test split as the validation set.

**Prediction.** `model(X).argmax(axis=1)` on a validation batch gives 256 predictions; D2L shows the misclassified images with true and predicted labels. With linear and softmax regression we have reached "the state of the art of 1960–1970s statistical modeling".

### 12. Concise implementation and numerical stability (§4.5)

```python
class SoftmaxRegression(d2l.Classifier):
    def __init__(self, num_outputs, lr):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.Sequential(nn.Flatten(),             # [n,1,28,28] -> [n,784]
                                 nn.LazyLinear(num_outputs))
    def forward(self, X):
        return self.net(X)                                 # logits, no softmax

def loss(self, Y_hat, Y, averaged=True):
    Y_hat = Y_hat.reshape((-1, Y_hat.shape[-1]))
    Y = Y.reshape((-1,))
    return F.cross_entropy(Y_hat, Y, reduction='mean' if averaged else 'none')
```

**Why the loss takes logits.** Float32 covers roughly $10^{-38}$ to $10^{38}$, so $\exp(o)$ is only safe for $o$ in about $[-90,90]$. (Exactly: overflow above $\ln(3.4\times10^{38})=88.72$; below $-87.34$ results are subnormal and lose precision; below $-103.28$ they become 0.)

Subtract $\bar o=\max_k o_k$ (softmax is translation invariant):
$$\hat y_j=\frac{\exp(o_j-\bar o)}{\sum_k\exp(o_k-\bar o)}.$$
Every exponent is now $\le0$, the numerator is $\le1$ and the denominator lies in $[1,q]$, so nothing overflows. Underflow can still make a numerator 0, and then $\log\hat y_j=\log0$ gives `NaN`s in backprop. Since we want $\log\hat y$ anyway, combine the two steps (the **LogSumExp trick**):
$$\log\hat y_j=o_j-\bar o-\log\sum_k\exp(o_k-\bar o).$$
This is what `F.cross_entropy` does, which is why it takes logits. Keep the plain softmax for when you want to read probabilities.

Checks in float32 (mine):

| logits | naive softmax | stable softmax |
|---|---|---|
| $(1000,1001,1002)$ | `[nan, nan, nan]` | `[0.090031, 0.244728, 0.665241]` |
| $(100,1,0)$ | `[nan, 0, 0]` ($e^{100}$ overflows) | `[1.0, 1.0e-43, 3.8e-44]` |
| $(-100,-101,-102)$ | `[0.6585, 0.2439, 0.0976]` (1% off: subnormals) | `[0.6652, 0.2447, 0.0900]` |
| $(-110,-111,-112)$ | `[nan, nan, nan]` (0/0) | `[0.6652, 0.2447, 0.0900]` |

The safe exponent range per number format (D2L ex. 4.5.1): FP16 about $[-9.7, 11.1]$, BF16 and FP32 about $[-87.3, 88.7]$, FP64 about $[-708.4, 709.8]$. FP16's range is why mixed-precision training keeps the loss in FP32.

Training the concise model with the same settings converges to a similarly accurate solution in fewer lines. D2L's caution: high-level APIs hide the sharp edges, which makes it harder to fix things when the framework's protection fails. Learn both versions.

### 13. Generalization in classification (§4.6)

#### 13.1 How big must a test set be?

For a fixed classifier, test error is the mean of the Bernoulli variable $\mathbf{1}(f(X)\ne Y)$. By the CLT it converges to the true error at rate $O(1/\sqrt n)$: twice the precision needs 4× the data.

Bernoulli variance $\epsilon(1-\epsilon)$ is at most 0.25 (at $\epsilon=0.5$), so:

| Requirement | Algebra | $n$ |
|---|---|---|
| one sd $=0.01$ | $0.25/n=0.01^2$ | 2,500 |
| two sd $=0.01$ (≈95%) | $0.25/n=0.005^2$ | 10,000 |

Many benchmarks have test sets of this size. D2L remarks that thousands of papers claim improvements of 0.01 or less, which on 10,000 examples is within the noise. Near zero error the variance is much smaller and 0.01 can be meaningful.

Hoeffding's finite-sample bound $P(\epsilon_D(f)-\epsilon(f)\ge t)\lt \exp(-2nt^2)$ at $t=0.01$, $\delta=0.05$ gives $n=14{,}979$ (D2L: "roughly 15,000"). Note this is one-sided while the 10,000 is two-sided; the like-for-like two-sided figure is 18,444. The conclusion (finite-sample bounds are somewhat more conservative) holds either way.

#### 13.2 Reusing the test set

Suppose you evaluate $f_1$ once on a clean test set, then build $f_2$ after seeing the result. Two problems:

1. **Multiple testing**: with many classifiers, at least one may get a misleadingly good score.
2. **Adaptive overfitting** (Dwork et al., 2015): $f_2$ was chosen with knowledge of the test set, so the test set is no longer independent of the model.

D2L's advice: use real test sets as rarely as possible, account for multiple comparisons, be extra careful with small data and high stakes, and in competitions keep several test sets, demoting each old one to validation.

#### 13.3 Statistical learning theory

Any fixed classifier's test error is an unbiased estimate. The hard case is a classifier chosen from an (infinite) class $\mathcal{F}$ using the same data. Uniform convergence asks that every $f\in\mathcal{F}$ have empirical error close to true error simultaneously; that fails for very flexible classes.

Vapnik and Chervonenkis: the **VC dimension** is the largest number of points the class can label in every possible way. With probability $\ge1-\delta$,
$$R[p,f]-R_{\text{emp}}[\mathbf{X},\mathbf{Y},f]\lt \alpha \quad\text{for}\quad \alpha\ge c\sqrt{(\text{VC}-\log\delta)/n}$$
Linear models in $d$ dimensions have VC dimension $d+1$.

These bounds do not explain deep learning. Deep networks can fit random labels yet generalize well, and larger, deeper networks often generalize better despite higher VC dimension. See [[04 - Neural Network]].

### 14. Distribution shift (§4.7)

D2L's loan example: a model finds that people wearing Oxfords repay and people in sneakers default. Once loans are granted on that basis, everyone wears Oxfords and creditworthiness does not change. Deploying a model can break it.

#### 14.1 Types of shift

Train on $p_S(\mathbf{x},y)$, test on $p_T(\mathbf{x},y)$. Without some assumption linking them, robust learning is impossible: if all labels flip while inputs stay the same, no data can detect it.

| Shift | Changes | Fixed | Typical when | Example |
|---|---|---|---|---|
| Covariate | $P(\mathbf{x})$ | $P(y\mid\mathbf{x})$ | $\mathbf{x}$ causes $y$ | train on photos, test on cartoons |
| Label | $P(y)$ | $P(\mathbf{x}\mid y)$ | $y$ causes $\mathbf{x}$ | disease prevalence changes; diseases cause symptoms |
| Concept | meaning of labels | | definitions drift | diagnostic criteria; regional names for soft drinks |

The causal direction tells you which correction to use. When labels are deterministic, label-shift methods can still be easier because they work with low-dimensional labels.

#### 14.2 Examples from D2L

- **Medical test**: healthy controls were university students; the disease affects older men. The classifier separated the groups by age, hormones, diet and so on. Not correctable.
- **Self-driving**: trained on game-engine images where all roadsides had the same texture; failed on real roads.
- **Tanks**: photos without tanks were taken in the morning, with tanks at noon; the classifier learned shadows.
- **Nonstationarity**: ad models unaware of new products, spammers adapting, recommending Santa hats after Christmas.

- **More anecdotes**: a face detector that fails on close-ups where the face fills the image; a US search engine deployed in the UK; a classifier trained on 1000 classes × 1000 images deployed where real label frequencies are far from uniform (label shift).

All of these looked excellent on a test set drawn from the same flawed data.

**Empirical risk and risk.** Training minimizes the **empirical risk** $\frac1n\sum_{i=1}^n l(f(\mathbf x_i),y_i)$, an average over the training data that approximates the **risk** $\mathbb E_{p(\mathbf x,y)}[l(f(\mathbf x),y)]=\iint l(f(\mathbf x),y)\,p(\mathbf x,y)\,d\mathbf x\,dy$. Minimizing the former in the hope of minimizing the latter is **empirical risk minimization**. Every correction below rewrites the risk under the target distribution as a weighted risk under the source.

#### 14.3 Correcting covariate shift

If inputs come from source $q(\mathbf{x})$, we care about target $p(\mathbf{x})$, and $p(y\mid\mathbf{x})=q(y\mid\mathbf{x})$, then
$$\iint l(f(\mathbf x),y)\,p(y\mid\mathbf x)p(\mathbf x)\,d\mathbf x\,dy=\iint l(f(\mathbf x),y)\,q(y\mid\mathbf x)q(\mathbf x)\frac{p(\mathbf x)}{q(\mathbf x)}\,d\mathbf x\,dy,$$
so reweight each example:
$$\beta_i=\frac{p(\mathbf{x}_i)}{q(\mathbf{x}_i)},\qquad \min_f\ \frac1n\sum_{i=1}^n\beta_i\,\ell(f(\mathbf{x}_i),y_i)$$

Estimate the ratio with logistic regression. Label target samples $z=1$ and source samples $z=-1$ (equal numbers). Then $P(z=1\mid\mathbf{x})/P(z=-1\mid\mathbf{x})=p(\mathbf{x})/q(\mathbf{x})$, and with $P(z=1\mid\mathbf{x})=\sigma(h(\mathbf{x}))$:
$$\beta_i=\exp(h(\mathbf{x}_i))$$

Algorithm:
1. Combine labelled training inputs (label −1) and unlabelled test inputs (label +1).
2. Train a logistic classifier to get $h$.
3. Set $\beta_i=\min(\exp(h(\mathbf{x}_i)),c)$.
4. Train on the labelled data with weights $\beta_i$.

Requirement: every region with $p(\mathbf{x})>0$ must have $q(\mathbf{x})>0$, otherwise the weight is infinite. The medical startup's controls had zero chance of being older men, so no reweighting could help. You need features from both distributions, but no target labels.

#### 14.4 Correcting label shift

If $q(y)\ne p(y)$ but $q(\mathbf{x}\mid y)=p(\mathbf{x}\mid y)$, then $\beta_i=p(y_i)/q(y_i)$. Estimate $p(y)$ from a confusion matrix $\mathbf{C}$ (computed on source validation data) and the average test prediction $\mu(\hat{\mathbf{y}})$:
$$\mathbf{C}\,p(\mathbf{y})=\mu(\hat{\mathbf{y}})\quad\Longrightarrow\quad p(\mathbf{y})=\mathbf{C}^{-1}\mu(\hat{\mathbf{y}})$$

$\mathbf{C}$ must be column-conditional, $c_{ij}=P(\hat y=i\mid y=j)$, with columns summing to 1. D2L's wording describes a joint frequency, under which the equation would not hold.

Worked example (mine). Source labels $q=(0.5,0.3,0.2)$,
$$\mathbf{C}=\begin{pmatrix}0.85&0.10&0.05\\0.10&0.80&0.15\\0.05&0.10&0.80\end{pmatrix}$$
(source accuracy 82.5%). If the true test distribution is $p=(0.2,0.3,0.5)$, then $\mu=\mathbf{C}p=(0.225,0.335,0.440)$, and $\mathbf{C}^{-1}\mu$ recovers $p$ exactly. Weights $\beta=(0.4,1.0,2.5)$. Using $\mu$ directly would be off by +12.5%, +11.7%, −12.0%.

D2L says a sufficiently accurate classifier makes $\mathbf{C}$ invertible. What matters is the condition number. Here $\kappa(\mathbf{C})=1.50$. With a weak classifier, $\kappa=104$, adding 0.005 of sampling noise to $\mu$ gives $\hat p=(0.100,0.800,0.100)$: error 0.648 vs 0.0098, 65.9× worse, and still a valid-looking probability vector. Same lesson as [[02 - Linear Regression]] exercise 4.

#### 14.5 Concept shift and learning settings

Concept shift has no principled fix beyond new labels. Usually it is gradual (camera lenses wearing, ads changing popularity), and continuing to train the existing model on new data is enough.

| Setting | Description |
|---|---|
| Batch learning | train once, deploy, never update (the default in this course) |
| Online learning | predict $f_t(\mathbf{x}_t)$, see $y_t$, update to $f_{t+1}$ |
| Bandits | online learning with a finite set of actions; stronger guarantees |
| Control | the environment remembers past actions (PID controllers) |
| Reinforcement learning | environment with memory that may cooperate or compete |

A strategy that works in a stationary environment may fail once the environment adapts (an arbitrage disappears once exploited). If the environment changes slowly, make estimates change slowly too.

#### 14.6 Fairness

A deployed model automates decisions about people. For a medical model you must know which populations it works for. A training sample that differs from the deployment population can give high test accuracy and unsafe behaviour.

## From the lecture slides (3.1 Logistic Regression, 3.2 Softmax Regression)

D2L derives softmax first and treats two classes as a special case (§7). The lectures go the other way. They derive binary logistic regression from maximum likelihood, then generalize it to softmax with an explicit matrix gradient. Numbers below were recomputed.

### 15. Lecture 3.1: binary logistic regression

**One form, three models.** All three compute $y=f(\mathbf w^\top\mathbf x)$ and differ only in $f$:

| model | $f$ | output |
|---|---|---|
| linear regression | $f(s)=s$ | any real number |
| perceptron (PLA) | $f(s)=\operatorname{sgn}(s)$ | $\pm1$ |
| logistic regression | $f(s)=\sigma(s)=\dfrac{1}{1+e^{-s}}$ | $(0,1)$, read as a probability |

The slide's candidate curves:
- the hard threshold;
- $\sigma(s)$;
- $e^s/(e^s+e^{-s})$, which is just $\sigma(2s)=(1+\tanh s)/2$;
- a linear function.

**Why the sigmoid is chosen:**
- it is bounded in $(0,1)$, with $\lim_{s\to-\infty}\sigma=0$ and $\lim_{s\to\infty}\sigma=1$;
- it is smooth;
- its derivative is $\sigma'(s)=\sigma(s)(1-\sigma(s))$ (checked with sympy).

**Likelihood.** Let $z_i=\sigma(\mathbf w^\top\mathbf x_i)$ be the model's probability of class 1. Then $P(y_i=1\mid\mathbf x_i;\mathbf w)=z_i$ and $P(y_i=0\mid\mathbf x_i;\mathbf w)=1-z_i$, or in one line
$$P(y_i\mid\mathbf x_i;\mathbf w)=z_i^{y_i}(1-z_i)^{1-y_i}$$
With independent samples the likelihood is the product $\prod_i z_i^{y_i}(1-z_i)^{1-y_i}$ (MLE). Taking $-\log$ turns the product into a sum, avoids underflow, and gives the binary cross-entropy of §7:
$$J(\mathbf w)=-\sum_{i=1}^N\big(y_i\log z_i+(1-y_i)\log(1-z_i)\big)$$

**Gradient.** The factor $\sigma'=\sigma(1-\sigma)$ cancels the denominators, leaving
$$\frac{\partial J_i}{\partial\mathbf w}=(z_i-y_i)\,\mathbf x_i\qquad\Longrightarrow\qquad \mathbf w\leftarrow\mathbf w+\eta\,(y_i-z_i)\,\mathbf x_i\ \ \text{(slide's SGD step)}$$
This is the same form as linear regression's SGD step (§16 of [[02 - Linear Regression|ch. 02]]) with $\mathbf x_i^\top\mathbf w$ replaced by $z_i$. I checked it with sympy.

**Prediction.** $\hat y=1$ if $\sigma(\mathbf w^\top\mathbf x)\ge0.5$, i.e. if $\mathbf w^\top\mathbf x\ge0$, so the decision boundary is linear.

**The lecture's dataset and exercise.** Twenty students studied 0.5–5.5 hours; 10 passed:

| hours | .5 | .75 | 1 | 1.25 | 1.5 | 1.75 | 1.75 | 2 | 2.25 | 2.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| pass | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |

| hours | 2.75 | 3 | 3.25 | 3.5 | 4 | 4.25 | 4.5 | 4.75 | 5 | 5.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| pass | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |

The exercise asks for the model. The maximum-likelihood fit (Newton's method run to convergence) is
$$P(\text{pass}\mid h)=\sigma(-4.0777+1.5046\,h)$$
- **Decision boundary:** $h=4.0777/1.5046=2.71$ hours.
- **Training accuracy** at the 0.5 threshold is 0.80. The minimum negative log-likelihood is 8.030.
- **Plain SGD.** The slide's update with a fixed $\eta=0.05$ for 20,000 epochs ends near $(-4.09, 1.61)$. A constant step keeps SGD bouncing around the optimum; it settles only if the step decays ([[04 - Neural Network|ch. 04 §24]]).

Probability of passing:

| hours | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $P(\text{pass})$ | 0.071 | 0.256 | 0.607 | 0.874 | 0.969 |

### 16. Lecture 3.2: softmax regression in matrix form

**One-vs-rest first.** For $C$ classes, the slide first trains $C$ binary logistic models, each one "class $i$ vs not $i$". Their outputs $a_i=\sigma(z_i)$ each lie in $(0,1)$ but do not sum to 1. Softmax fixes that.

**Notation (slide).** $\mathbf x\in\mathbb R^{d+1}$ with $x_0=1$; $\mathbf W\in\mathbb R^{(d+1)\times C}$ with one column $\mathbf w_i$ per class; the logits are $\mathbf z=\mathbf W^\top\mathbf x$ and the probabilities are
$$a_i=\frac{\exp(z_i)}{\sum_{j=1}^C\exp(z_j)},\qquad P(y=i\mid\mathbf x;\mathbf W)=a_i$$

**The slide's four examples:**

| $\mathbf z$ | softmax | slide |
|---|---|---|
| (2, 2, 2) | (0.333, 0.333, 0.333) | same |
| (2, 1.8, 0) | (0.512, 0.419, 0.069) | same |
| (−1, −1.5, −2) | (0.506, 0.307, 0.186) | 0.507 for the first |
| (3, 3, 0.1) | (0.487, 0.487, 0.027) | 0.486 for the first two |

The last-digit differences are rounding. Together the rows show three properties:
- equal logits give equal probabilities;
- order is preserved;
- negative logits are fine, since only differences matter.

**Loss.** The cross-entropy of distributions $\mathbf p$, $\mathbf q$ is $H(\mathbf p,\mathbf q)=-\sum_i p_i\log q_i$. With a one-hot label $\mathbf y_i$ (as a column of $\mathbf Y\in\{0,1\}^{C\times N}$):
$$J_i(\mathbf W)=-\sum_{j=1}^C y_{ji}\log a_{ji}=-\log a_{y_i,i},\qquad J(\mathbf W)=-\frac1N\sum_{i=1}^N\log a_{y_i,i}$$
Since $\sum_jy_{ji}=1$, this expands to $J_i=-\sum_jy_{ji}\mathbf w_j^\top\mathbf x_i+\log\sum_k\exp(\mathbf w_k^\top\mathbf x_i)$, the LogSumExp form of §12.

**Gradient.** Per column,
$$\nabla_{\mathbf w_j}J_i=-y_{ji}\mathbf x_i+\frac{\exp(\mathbf w_j^\top\mathbf x_i)}{\sum_k\exp(\mathbf w_k^\top\mathbf x_i)}\mathbf x_i=(a_{ji}-y_{ji})\,\mathbf x_i=e_{ji}\,\mathbf x_i$$
Stack the error $\mathbf e_i=\mathbf a_i-\mathbf y_i$ and $\mathbf E=\mathbf A-\mathbf Y\in\mathbb R^{C\times N}$:
$$\nabla_{\mathbf W}J_i=\mathbf x_i\mathbf e_i^\top,\qquad \nabla_{\mathbf W}J=\frac1N\sum_i\mathbf x_i\mathbf e_i^\top=\frac1N\mathbf X\mathbf E^\top\quad(\mathbf X\in\mathbb R^{d\times N})$$
Against finite differences on a random 4×3 problem the maximum error is $4\times10^{-10}$. This is §6's "softmax minus one-hot", written for the whole batch.

**Minibatch update.** With $\mathbf X_b\in\mathbb R^{d\times N_b}$ and $\mathbf E_b\in\mathbb R^{C\times N_b}$:
$$\mathbf W\leftarrow\mathbf W-\frac{\eta}{N_b}\mathbf X_b\mathbf E_b^\top$$

**Weight decay, and a sign slip on the slide.** The slide writes $\bar J=-\frac1N\big(\sum_i\log a_{y_i,i}+\frac\lambda2\Vert\mathbf W\Vert_F^2\big)$. As written, the leading minus also flips the penalty, so the loss would *reward* large weights. The intended loss is
$$\bar J(\mathbf W)=-\frac1N\sum_{i=1}^N\log a_{y_i,i}+\frac\lambda2\Vert\mathbf W\Vert_F^2,\qquad \nabla\bar J=\frac1N\mathbf X\mathbf E^\top+\lambda\mathbf W$$
which is weight decay as in [[02 - Linear Regression|ch. 02 §13]].

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

> [!example]- **2.** *(Easy–medium) Implementation pitfalls (D2L ex. 4.4.1, 4.3.1)*
> **(a)** Run the from-scratch `softmax` in float32 on $(100,1,0)$ and on $(-110,-111,-112)$. What happens and why? **(b)** What does it give for $(-100,-101,-102)$? **(c)** Fix it. **(d)** With $\hat{\mathbf Y}=\begin{pmatrix}0.1&0.3&0.6\\0.3&0.2&0.5\end{pmatrix}$ and labels $(0,2)$, compute the cross-entropy and accuracy. **(e)** A validation set of 10,000 images is read in batches of 256. Write the true mean loss in terms of the mean of batch means $L^q$ and the last batch's loss $l^b$.
>
> ---
> **(a)** $e^{100}\approx2.7\times10^{43}$ exceeds float32's max $3.4\times10^{38}$: `inf/inf = nan` for the first entry. For $-110$ every $e^{o}$ underflows to 0 (below $e^{-103.3}$): `0/0 = nan` everywhere.
>
> **(b)** `[0.6585, 0.2439, 0.0976]` instead of `[0.6652, 0.2447, 0.0900]`: no crash, but about 1% wrong, because values near $e^{-100}$ are subnormal and have few significant bits.
>
> **(c)** Subtract the row max before exponentiating: `X_exp = torch.exp(X - X.max(1, keepdim=True).values)`. Better still, never compute $\log(\text{softmax})$ yourself; pass logits to `F.cross_entropy`, which uses LogSumExp.
>
> **(d)** Picked probabilities 0.1 and 0.5; loss $\tfrac12(2.302585+0.693147)=1.4979$. Both rows predict class 2, so accuracy $=0.5$.
>
> **(e)** 39 full batches and one of 16: $L_v=\big(256(40L^q-l^b)+16\,l^b\big)/10{,}000$. The quick $L^q$ over-weights the 16 last examples.

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
> Source labels $q=(0.5,0.3,0.2)$, $\mathbf{C}$ as in §14.4, test mean output $\mu=(0.225,0.335,0.440)$.
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
- Code: `nn.Sequential(nn.Flatten(), nn.LazyLinear(10))` outputs logits; `F.cross_entropy` takes logits and integer labels and applies LogSumExp. From scratch, cross-entropy is `-log(y_hat[range(n), y]).mean()`.
- Float32 `exp` is safe only for arguments in about $[-87, 89]$; subtract the max.
- $H(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q)$: minimizing cross-entropy minimizes KL, with floor $H(P)$.
- Bernoulli variance gives 2,500 test examples for one sd of 0.01 and 10,000 for two. Reusing a test set biases it.
- VC theory does not explain why large networks generalize.
- Shift types: covariate (reweight with $\exp(h(\mathbf{x}))$ from a logistic discriminator), label (solve $\mathbf{C}p=\mu$, watch conditioning), concept (retrain). Deploying a model can change the data it sees.

## ⚠️ Important Notes

1. Integer labels imply an order; use them only for genuinely ordinal classes.
2. Softmax parameters are not identifiable: do not interpret single logits or weights.
3. Pass logits to the loss. Doing softmax then log yourself can overflow (`nan` on $(1000,1001,1002)$) or underflow to `log 0`.
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
17. PyTorch classification labels are integer class indices (`int64`, shape `[n]`), not one-hot vectors.
18. Images are `[batch, channels, height, width]`; `nn.Flatten()` keeps the batch axis and flattens the rest.
19. Averaging batch means is exact only with equal batch sizes; the small last batch gets extra weight.
20. D2L's reported "test" accuracies on Fashion-MNIST are really validation accuracies.
21. Logistic regression's SGD step $\mathbf w\leftarrow\mathbf w+\eta(y_i-z_i)\mathbf x_i$ has the same shape as linear regression's; only $z_i=\sigma(\mathbf w^\top\mathbf x_i)$ differs. Softmax's batch gradient is $\frac1N\mathbf X\mathbf E^\top$ with $\mathbf E=\mathbf A-\mathbf Y$ (samples as columns).
22. A penalty is added to the loss, never subtracted. The lecture's regularized softmax loss puts $\frac\lambda2\Vert\mathbf W\Vert_F^2$ inside $-\frac1N(\cdot)$; take it out.

> [!warning] Gaps in the source material
> - **Figures:** the softmax-as-network diagram is reconstructed from the prose. The photo/cartoon images and the soft-drink map are lost but only illustrate claims stated in the text.
> - **Formulas:** this chapter showed that `!` means `→` and that `λ` is deleted. Exercise 5.4 extracts as `Showthatfor !1 wehave 1RealSoftMax(a; b)! max(a; b)`, i.e. for $\lambda\to\infty$, $\lambda^{-1}\mathrm{RealSoftMax}(\lambda a,\lambda b)\to\max(a,b)$.
> - **Added by me:** the KL decomposition; the Hessian solution (D2L ex. 1); the binary reduction and $d+1$ count; the one-/two-sided caveat (18,444 vs 10,000, logged as a declined discrepancy); the block-coding table; the full label-shift example including the $\kappa=104$ failure; the column-conditional remark; the temperature calculation; the overflow demo.
> - **Cross-check with ch. 01:** D2L says a 1995 Sun SPARCStation 5 had 64 MB and 5 MFLOPS. Against Table 1.5.1's 1990 row (10 MB, 10 MF) the memory fits but compute is half, so the table's compute column looks optimistic. MNIST (47.04 MB at one byte per pixel) was 73.5% of that machine's RAM.
> - **Also added by me:** the float32 range table and the subnormal example; the per-format exp ranges; the exact batch-averaging formula; the toy accuracy.
> - **Skipped:** `show_images` plotting code and the training curves (images). VC theory is stated, not derived.
> - **Lecture slides (3.1, 3.2), added 2026-11-17:** §15–16. I fitted the study-hours MLE and probabilities myself (the slide only poses the exercise); checked the softmax examples (last-digit rounding differences); checked the gradient $\frac1N\mathbf X\mathbf E^\top$ against finite differences; flagged the slide's regularized-loss sign.

**Previous:** [[02 - Linear Regression]] · **Next:** [[04 - Neural Network]]
