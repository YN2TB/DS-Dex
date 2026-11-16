---
subject: Deep Learning
chapter: 4
tags: [ds, deep-learning, mlp, backpropagation, activation-functions, initialization, dropout, optimizers, adam, momentum, conditioning]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 5 (Multilayer Perceptrons), ch. 6 (Builders' Guide), ch. 12 (Optimization Algorithms)"
---

# Neural Network

This note merges three D2L chapters and follows each in order: ch. 5 (MLPs, implementation, backpropagation, numerical stability, generalization, dropout, the Kaggle house-price workflow), ch. 6 (the Builders' Guide: modules, parameters, initialization, custom layers, file I/O, GPUs) and ch. 12 (gradient descent, SGD, minibatches, momentum through Adam, learning-rate schedules). The syllabus has no separate optimizer topic, so ch. 12 lives here (scope call recorded in [[00-Index]]).

## 📘 Main Knowledge

## Multilayer perceptrons (D2L ch. 5)

### 1. A hidden layer needs a nonlinearity (§5.1)

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

ReLU's main advantage is its derivative: 0 or 1, never a damping factor in between (§9).

### 3. Universal approximation

One hidden layer with enough units can approximate any continuous function (Cybenko 1989, Micchelli 1984). D2L's caveats: being able to represent a function is different from learning it; kernel methods are also universal; and deep networks often represent functions far more compactly than wide shallow ones.

### 4. Implementing an MLP (§5.2)

Fashion-MNIST again: 784 inputs, 10 classes, one hidden layer of 256 units. Width and depth are hyperparameters; widths are usually multiples of large powers of 2 because of how hardware allocates and addresses memory.

**From scratch.** `nn.Parameter` registers a tensor as a parameter that autograd tracks and `model.parameters()` returns:

```python
class MLPScratch(d2l.Classifier):
    def __init__(self, num_inputs, num_outputs, num_hiddens, lr, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.W1 = nn.Parameter(torch.randn(num_inputs, num_hiddens) * sigma)
        self.b1 = nn.Parameter(torch.zeros(num_hiddens))
        self.W2 = nn.Parameter(torch.randn(num_hiddens, num_outputs) * sigma)
        self.b2 = nn.Parameter(torch.zeros(num_outputs))

def relu(X):
    a = torch.zeros_like(X)
    return torch.max(X, a)

def forward(self, X):
    X = X.reshape((-1, self.num_inputs))
    H = relu(torch.matmul(X, self.W1) + self.b1)
    return torch.matmul(H, self.W2) + self.b2      # logits

model = MLPScratch(num_inputs=784, num_outputs=10, num_hiddens=256, lr=0.1)
data = d2l.FashionMNIST(batch_size=256)
trainer = d2l.Trainer(max_epochs=10)
trainer.fit(model, data)
```

The training loop is the one from softmax regression; only the model changed.

**Concise.** Two fully connected layers instead of one; no `forward` is needed because `Module.forward` calls `self.net(X)`:

```python
class MLP(d2l.Classifier):
    def __init__(self, num_outputs, num_hiddens, lr):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.Sequential(nn.Flatten(), nn.LazyLinear(num_hiddens),
                                 nn.ReLU(), nn.LazyLinear(num_outputs))
```

Hand-named parameters (`W1`, `b1`, …) do not scale: inserting a layer between layers 42 and 43 means renaming, and the framework cannot optimize code it cannot see. D2L: with an MLP you have reached "the state of the art of the late 1980s". A one-unit hidden layer is a bad idea (D2L ex. 5.2.3): it is a rank-1 bottleneck, and if that ReLU unit dies (input always negative) no gradient reaches the layers below.

### 5. Forward and backward propagation (§5.3)

One example, no hidden bias, $\ell_2$ penalty:
$$\mathbf z=\mathbf W^{(1)}\mathbf x,\quad \mathbf h=\phi(\mathbf z),\quad \mathbf o=\mathbf W^{(2)}\mathbf h,\quad L=l(\mathbf o,y),\quad s=\tfrac{\lambda}{2}\left(\|\mathbf W^{(1)}\|_F^2+\|\mathbf W^{(2)}\|_F^2\right),\quad J=L+s$$

Backpropagation applies the chain rule in reverse order:
$$\frac{\partial J}{\partial \mathbf W^{(2)}}=\frac{\partial J}{\partial\mathbf o}\mathbf h^\top+\lambda\mathbf W^{(2)},\qquad \frac{\partial J}{\partial\mathbf h}=\mathbf W^{(2)\top}\frac{\partial J}{\partial\mathbf o}$$
$$\frac{\partial J}{\partial\mathbf z}=\frac{\partial J}{\partial\mathbf h}\odot\phi'(\mathbf z),\qquad \frac{\partial J}{\partial \mathbf W^{(1)}}=\frac{\partial J}{\partial\mathbf z}\mathbf x^\top+\lambda\mathbf W^{(1)}$$

- Each weight gradient is an outer product of a backward vector and a forward activation, so activations must be stored until the backward pass uses them.
- The activation enters the backward pass only through the factor $\phi'(\mathbf z)$, once per layer (§9).
- Weight decay adds $\lambda\mathbf W$ directly, even when the data gradient is zero.

Forward and backward passes alternate: the forward pass uses the current weights, and the backward pass needs the stored forward values.

### 6. Memory cost of training

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

### 7. Vanishing and exploding gradients (§5.4)

For $L$ layers the gradient at layer $l$ is a product of Jacobians:
$$\partial_{\mathbf W^{(l)}}\mathbf o=\mathbf M^{(L)}\cdots\mathbf M^{(l+1)}\,\mathbf v^{(l)},\qquad \mathbf M^{(k)}=\partial_{\mathbf h^{(k-1)}}\mathbf h^{(k)}$$

A long product of matrices whose eigenvalues are not near 1 shrinks or grows geometrically. Exploding gradients wreck the model; vanishing gradients stop learning.

### 8. Symmetry

If all hidden weights start equal, every hidden unit gets the same input and the same gradient, and they stay identical: the layer acts like one unit. Random initialization is therefore required. Dropout breaks the symmetry because it drops different units each step; plain SGD does not. (Equivalently, any minimum of a $d$-unit layer has $d!$ permutation copies.)

### 9. The sigmoid limits depth

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

### 10. Products of random matrices

D2L multiplies 100 random $4\times4$ $\mathcal N(0,1)$ matrices and prints an entry of $1.2044\times10^{25}$. The growth rate has a closed form (Cohen & Newman 1984; added beyond D2L), the top Lyapunov exponent:
$$\lambda_1=\tfrac12\left[\ln(2\sigma^2)+\psi(n/2)\right]$$
At $n=4$, $\sigma=1$: $\lambda_1=0.557966$, predicting $10^{24.23}$ after 100 products. D2L's run ($10^{25.08}$) is ordinary: $z=+0.28$ against 400 simulated replications, which ranged from $10^{19.72}$ to $10^{29.67}$. "The product explodes" describes a distribution, and one printed run is one draw.

Neutral growth needs $\sigma^*=e^{-\lambda_1}=0.572372$ at $n=4$. Xavier gives $\sqrt{2/8}=0.5$, contracting the top direction by 12.64% per layer. The gap shrinks like $O(1/n)$ (simulated over 20,000 layers: $n=4$: −0.135181 theory vs −0.137873; $n=64$: −0.007853 vs −0.007866).

### 11. Initialization

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

### 12. Generalization in deep networks (§5.5)

- Deep networks are over-parametrized and usually fit every training label, even random ones (Zhang et al. 2021), so VC and Rademacher bounds say nothing useful.
- Making models larger often reduces test error: **double descent** (Nakkiran et al. 2021).
- Nonparametric views fit better: 1-nearest-neighbour has zero training error and is consistent; infinitely wide MLPs behave like kernel methods (neural tangent kernel, Jacot et al. 2018).
- **Early stopping**: networks fit clean labels first and noisy labels later. Stop when validation error has not improved by $\epsilon$ for a set number of epochs (patience). It matters when labels are noisy and little when classes are cleanly separable.
- Typical weight-decay strengths do not prevent interpolation; D2L suggests its benefit may come together with early stopping.

### 13. Dropout (§5.6)

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

D2L's printed example at $p=0.5$ on $\mathbf X=0,\dots,15$ kept 10 or 11 of 16 units (the first entry is 0 whether kept or not; $P(\ge10)=0.227$, $P(\ge11)=0.105$ under $\mathrm{Bin}(16,0.5)$), and its mean is 8.875 against 7.5 (+18.33%). Unbiased on average does not mean close on any single draw, and the network trains on single draws.

**Dropout from scratch.** Keep a unit when a uniform draw exceeds $p$, rescale survivors by $1/(1-p)$:

```python
def dropout_layer(X, dropout):
    assert 0 <= dropout <= 1
    if dropout == 1: return torch.zeros_like(X)
    mask = (torch.rand(X.shape) > dropout).float()
    return mask * X / (1.0 - dropout)
```

On `X = arange(16).reshape(2, 8)`: $p=0$ returns `X`, $p=1$ returns zeros, $p=0.5$ printed `[[0, 2, 4, 0, 8, 10, 12, 0], [16, 18, 20, 22, 0, 0, 0, 30]]`: survivors doubled.

D2L's model applies dropout after each hidden activation, only when `self.training` is true (set by `model.train()`, cleared by `model.eval()`):

```python
class DropoutMLPScratch(d2l.Classifier):
    def __init__(self, num_outputs, num_hiddens_1, num_hiddens_2,
                 dropout_1, dropout_2, lr):
        super().__init__()
        self.save_hyperparameters()
        self.lin1 = nn.LazyLinear(num_hiddens_1)
        self.lin2 = nn.LazyLinear(num_hiddens_2)
        self.lin3 = nn.LazyLinear(num_outputs)
        self.relu = nn.ReLU()
    def forward(self, X):
        H1 = self.relu(self.lin1(X.reshape((X.shape[0], -1))))
        if self.training:
            H1 = dropout_layer(H1, self.dropout_1)
        H2 = self.relu(self.lin2(H1))
        if self.training:
            H2 = dropout_layer(H2, self.dropout_2)
        return self.lin3(H2)

hparams = {'num_outputs': 10, 'num_hiddens_1': 256, 'num_hiddens_2': 256,
           'dropout_1': 0.5, 'dropout_2': 0.5, 'lr': 0.1}
```

Concise: put `nn.Dropout(p)` after each hidden `nn.ReLU()` in an `nn.Sequential`; it is the identity in eval mode.

### 14. Predicting house prices on Kaggle (§5.7)

A full workflow on real data: the Ames, Iowa housing data (De Cock, 2011; sales 2006–2010), larger than the Boston data. Training: 1460 rows × 80 features + `SalePrice`; test: 1459 rows × 80 features, no labels (scored by Kaggle). Features mix integers (year built), categories (roof type) and floats, with missing values marked "NA". Data files are cached and checked by SHA-1.

**Preprocessing.**

1. Drop `Id` (it identifies rows but carries no information).
2. Standardize every numeric column, $x\leftarrow(x-\mu)/\sigma$. Check: $\mathbb E[(x-\mu)/\sigma]=0$ and $\mathbb E[(x-\mu)^2]=(\mu^2+\sigma^2)-2\mu^2+\mu^2=\sigma^2$. Two reasons: easier optimization, and no feature is penalized more than another by weight decay just because of its units.
3. Fill missing numeric values with 0, which after standardization is the mean.
4. One-hot encode categorical columns (`pd.get_dummies(..., dummy_na=True)`, so "missing" becomes its own category). `MSZoning` ∈ {RL, RM} becomes `MSZoning_RL` and `MSZoning_RM`.

```python
def preprocess(self):
    label = 'SalePrice'
    features = pd.concat((self.raw_train.drop(columns=['Id', label]),
                          self.raw_val.drop(columns=['Id'])))
    numeric_features = features.dtypes[features.dtypes != 'object'].index
    features[numeric_features] = features[numeric_features].apply(
        lambda x: (x - x.mean()) / (x.std()))
    features[numeric_features] = features[numeric_features].fillna(0)
    features = pd.get_dummies(features, dummy_na=True)
    self.train = features[:self.raw_train.shape[0]].copy()
    self.train[label] = self.raw_train[label]
    self.val = features[self.raw_train.shape[0]:].copy()
```

79 feature columns become 331. Note that the means and standard deviations are computed on training and test features together. That is allowed here (test features are given, labels are not), but in a real deployment you would fit the scaler on training data only ([[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]]).

**Error measure.** For prices the relative error $(y-\hat y)/y$ matters: \$100,000 off is terrible for a \$125,000 house in rural Ohio and excellent in Los Altos Hills (median over \$4 million). A small $|\log y-\log\hat y|\le\delta$ means $e^{-\delta}\le\hat y/y\le e^{\delta}$. Kaggle scores
$$\sqrt{\frac1n\sum_{i=1}^n(\log y_i-\log\hat y_i)^2},$$
so D2L trains on $\log(\text{price})$ (the loader returns `torch.log(SalePrice)`).

**K-fold cross-validation.** `k_fold_data` cuts the training set into $K$ slices of `1460 // K` rows; each fold trains on $K-1$ slices and validates on the remaining one. With $K=5$, `lr=0.01`, 10 epochs, a linear model gives average validation log-MSE 0.1861. (Mine: that is a log-RMSE of 0.431, a typical error factor of $e^{0.431}=1.54$; a baseline, not a good model.) A training error far below the K-fold error signals overfitting; with many hyperparameter trials, K-fold estimates can themselves become optimistic (multiple testing).

**Submission.** Average the $K$ models' predictions after exponentiating back to prices (an ensemble), write `submission.csv` with `Id` and `SalePrice`, upload.

D2L's summary: standardize real-valued features, fill missing values with the mean, one-hot encode categories, use log error when relative error matters, select models with K-fold CV. Mean imputation assumes values are missing at random (D2L ex. 5.7.2); if, say, "no basement" is what makes the basement area missing, the missingness itself is informative.

## Builders' Guide (D2L ch. 6)

Libraries moved from single neurons to whole layers to **blocks** of layers, as chip design moved from transistors to circuits to code. This chapter shows the PyTorch machinery the later architectures rely on.

### 15. Layers and modules (§6.1)

A **module** (`nn.Module`) can be one layer, a group of layers or the whole model, and modules nest. ResNet-152 has hundreds of layers built from repeating groups, which would be tedious to write one layer at a time. A module must:

1. take input data in its `forward` method;
2. return an output (possibly of a different shape);
3. compute gradients of output with respect to input (autograd does this);
4. store and expose its parameters;
5. initialize them.

```python
net = nn.Sequential(nn.LazyLinear(256), nn.ReLU(), nn.LazyLinear(10))
X = torch.rand(2, 20)
net(X).shape                      # torch.Size([2, 10]); net(X) is net.__call__(X)
```

**A custom module.** Define the layers in `__init__` (after `super().__init__()`) and the computation in `forward`; backprop and parameter registration come for free:

```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.LazyLinear(256)
        self.out = nn.LazyLinear(10)
    def forward(self, X):
        return self.out(F.relu(self.hidden(X)))
```

Layers are instance attributes, so two `MLP()` objects are two independent models.

**What `Sequential` does.** Register each module with `add_module` and run them in order:

```python
class MySequential(nn.Module):
    def __init__(self, *args):
        super().__init__()
        for idx, module in enumerate(args):
            self.add_module(str(idx), module)
    def forward(self, X):
        for module in self.children():
            X = module(X)
        return X
```

Storing the modules in a plain Python list instead (D2L ex. 6.1.1) breaks this: PyTorch does not see them, so `parameters()` is empty, the optimizer updates nothing, and `.to(device)` and `state_dict()` skip them. (`nn.ModuleList` exists for this.)

**Arbitrary code in `forward`.** D2L's `FixedHiddenMLP` uses a constant random matrix (a plain tensor, not a `Parameter`, so never updated), reuses the same `Linear` layer twice (shared parameters), and runs a `while` loop:

```python
class FixedHiddenMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.rand_weight = torch.rand((20, 20))   # constant, no gradient
        self.linear = nn.LazyLinear(20)
    def forward(self, X):
        X = self.linear(X)
        X = F.relu(X @ self.rand_weight + 1)
        X = self.linear(X)                        # same layer again: shared weights
        while X.abs().sum() > 1:                  # control flow
            X /= 2
        return X.sum()
```

Modules can be nested freely: `nn.Sequential(NestMLP(), nn.LazyLinear(20), FixedHiddenMLP())`.

### 16. Parameter management (§6.2)

```python
net = nn.Sequential(nn.LazyLinear(8), nn.ReLU(), nn.LazyLinear(1))
net(torch.rand(size=(2, 4)))
net[2].state_dict()          # OrderedDict with 'weight' [1, 8] and 'bias' [1]
type(net[2].bias)            # torch.nn.parameter.Parameter
net[2].bias.data             # the values
net[2].weight.grad == None   # True: no backward pass yet
[(name, p.shape) for name, p in net.named_parameters()]
# [('0.weight', [8, 4]), ('0.bias', [8]), ('2.weight', [1, 8]), ('2.bias', [1])]
```

Index `Sequential` like a list; the ReLU at index 1 has no parameters, which is why names jump from `0.` to `2.`. A `Parameter` holds values, gradient and metadata, so ask for `.data` explicitly.

**Tied parameters.** Use the same layer object twice:

```python
shared = nn.LazyLinear(8)
net = nn.Sequential(nn.LazyLinear(8), nn.ReLU(),
                    shared, nn.ReLU(),
                    shared, nn.ReLU(),
                    nn.LazyLinear(1))
net(X)
net[2].weight.data[0, 0] = 100
net[2].weight.data[0] == net[4].weight.data[0]    # still all True: same tensor
```

Layers 2 and 4 are one object, not two equal copies. In backprop the gradients from both uses are **added** (weight tying in language models, the shared kernel of a convolution in [[05 - Convolutional Neural Network|ch. 05]], the shared cell of an RNN in [[07 - Recurrent Neural Network|ch. 07]]).

### 17. Parameter initialization (§6.3)

PyTorch's default for `Linear` draws uniformly from a range computed from the layer's input and output sizes. `net.apply(fn)` calls `fn` on every submodule:

```python
def init_normal(module):
    if type(module) == nn.Linear:
        nn.init.normal_(module.weight, mean=0, std=0.01)
        nn.init.zeros_(module.bias)
net.apply(init_normal)

def init_constant(module):          # all weights 1: a bad idea (symmetry, §8)
    if type(module) == nn.Linear:
        nn.init.constant_(module.weight, 1)
        nn.init.zeros_(module.bias)

def init_xavier(module):
    if type(module) == nn.Linear:
        nn.init.xavier_uniform_(module.weight)
net[0].apply(init_xavier)           # different initializers per block
net[2].apply(init_42)               # e.g. a constant 42
```

**Custom initializer.** D2L's toy distribution: $w\sim U(5,10)$ with probability $\tfrac14$, $0$ with probability $\tfrac12$, $U(-10,-5)$ with probability $\tfrac14$. Implementation: draw $U(-10,10)$, then zero every entry with $|w|<5$:

```python
def my_init(module):
    if type(module) == nn.Linear:
        nn.init.uniform_(module.weight, -10, 10)
        module.weight.data *= module.weight.data.abs() >= 5
```

($P(|w|<5)=10/20=\tfrac12$, and each tail has $\tfrac14$, as required.) Parameters can always be set directly: `net[0].weight.data[:] += 1`, `net[0].weight.data[0, 0] = 42`.

### 18. Lazy initialization (§6.4)

`nn.LazyLinear(256)` does not know its input size, so before the first forward pass `net[0].weight` is an `<UninitializedParameter>`. After `net(torch.rand(2, 20))`, `net[0].weight.shape` is `[256, 20]`: the framework infers shapes layer by layer and only then initializes. This is especially handy for CNNs, where the size after convolutions depends on the image resolution. PyTorch's default initializer for `Linear` is also why the concise weight-decay run in [[02 - Linear Regression|ch. 02]] started from a different norm than the scratch run. D2L's helper runs a dummy batch and then applies a custom initializer:

```python
def apply_init(self, inputs, init=None):
    self.forward(*inputs)
    if init is not None:
        self.net.apply(init)
```

### 19. Custom layers (§6.5)

**Without parameters:**

```python
class CenteredLayer(nn.Module):
    def forward(self, X):
        return X - X.mean()

CenteredLayer()(torch.tensor([1.0, 2, 3, 4, 5]))   # tensor([-2., -1., 0., 1., 2.])
net = nn.Sequential(nn.LazyLinear(128), CenteredLayer())
net(torch.rand(4, 8)).mean()                        # ~2.3e-09: zero up to rounding
```

**With parameters.** Wrap tensors in `nn.Parameter` so they are registered, saved, loaded and shared like built-in ones:

```python
class MyLinear(nn.Module):
    def __init__(self, in_units, units):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(in_units, units))
        self.bias = nn.Parameter(torch.randn(units,))
    def forward(self, X):
        linear = torch.matmul(X, self.weight) + self.bias   # D2L writes .data here
        return F.relu(linear)
```

> [!warning] Erratum E1 (D2L §6.5.2)
> D2L's `forward` uses `self.weight.data` and `self.bias.data`. `.data` bypasses autograd, so the layer computes the right forward values (its printed outputs are fine) but **cannot be trained**: with D2L's code, `net(X).requires_grad` is `False` and `backward()` raises "element 0 of tensors does not require grad" (checked in PyTorch 2.11). Use the parameters themselves, as above.

### 20. File I/O (§6.6)

Save checkpoints during long runs so a crash does not lose days of compute.

```python
x = torch.arange(4)
torch.save(x, 'x-file');        x2 = torch.load('x-file')
torch.save([x, y], 'x-files');  x2, y2 = torch.load('x-files')
torch.save({'x': x, 'y': y}, 'mydict')

net = MLP()
torch.save(net.state_dict(), 'mlp.params')    # parameters only
clone = MLP()                                  # rebuild the architecture in code
clone.load_state_dict(torch.load('mlp.params'))
clone.eval()
clone(X) == net(X)                             # all True
```

Only **parameters** are saved, not the architecture, because a model's `forward` can contain arbitrary code that does not serialize naturally. To reload, recreate the class in code, then load the state dict. To reuse the first layers of a trained network in a new one, load only the matching entries of its `state_dict` (the basis of fine-tuning, [[06 - Object Detection|ch. 06]]).

### 21. GPUs (§6.7)

GPU performance has grown about 1000× per decade since 2000. `nvidia-smi` shows the cards. Every tensor has a **device**:

```python
torch.device('cpu')        # all CPU cores and main memory
torch.device('cuda')       # = cuda:0, one GPU and its memory
torch.device(f'cuda:{i}')  # the i-th GPU
torch.cuda.device_count()

def try_gpu(i=0):
    if torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')

X = torch.ones(2, 3, device=try_gpu())        # created on GPU 0
Y = torch.rand(2, 3, device=try_gpu(1))       # on GPU 1
Z = X.cuda(1)                                 # explicit copy to GPU 1
Y + Z                                         # fine; Y + X raises an error
Z.cuda(1) is Z                                # True: no copy if already there
net = net.to(device=try_gpu())                # move the parameters
```

All operands of an operation must be on the same device; PyTorch refuses rather than silently copying, because transfers are much slower than computation. Rules of thumb: few large operations beat many small ones; printing a tensor or converting it to NumPy copies it to main memory and waits on Python's global interpreter lock; logging the loss to the CPU every minibatch can stall the GPU, so accumulate logs on the GPU. D2L's `Trainer` gains `num_gpus`, and `prepare_batch`/`prepare_model` move data and model to `gpus[0]`.

## Optimization algorithms (D2L ch. 12)

### 22. The landscape (§12.1)

Optimization minimizes training error; generalization is a separate goal. In high dimensions, zero-gradient points are mostly **saddle points**: a minimum needs all Hessian eigenvalues positive, which becomes unlikely as dimension grows ([[Optimization/contents/03 - Unconstrained Optimality Conditions|Optimization ch. 03]]).

D2L also lists **local minima** (a stationary point that is lowest only nearby) and **vanishing gradients** (e.g. $\tanh$ saturating) as obstacles. Adaptive optimizers can be seen as cheap approximations to the diagonal of $\mathbf H^{-1}$ ([[Optimization/contents/06 - Newton and Quasi-Newton Methods|Optimization ch. 06]]). Convexity (§12.2) is covered in [[Optimization/contents/02 - Convex Sets and Convex Functions|Optimization ch. 02]].

### 23. Gradient descent (§12.3)

Rarely used directly in deep learning, but divergence from a large learning rate and preconditioning already show up here.

**One dimension.** Taylor: $f(x+\epsilon)=f(x)+\epsilon f'(x)+O(\epsilon^2)$. Choose $\epsilon=-\eta f'(x)$:
$$f(x-\eta f'(x))=f(x)-\eta f'^2(x)+O(\eta^2f'^2(x)).$$
If $f'(x)\ne0$ and $\eta$ is small enough, $f$ decreases. Iterate $x\leftarrow x-\eta f'(x)$ until $|f'(x)|$ is small or a step budget runs out.

D2L minimizes $f(x)=x^2$ from $x=10$ for 10 steps. Each step multiplies $x$ by $1-2\eta$:

| $\eta$ | factor | $x_{10}=10(1-2\eta)^{10}$ | D2L prints | behaviour |
|---|---|---|---|---|
| 0.2 | 0.6 | 0.060466 | 0.060466 | converges |
| 0.05 | 0.9 | 3.486784 | 3.486784 | too slow |
| 1.1 | −1.2 | 61.917364 | 61.917364 | overshoots, diverges |

**Local minima.** $f(x)=x\cos(cx)$ with $c=0.15\pi$ has infinitely many local minima. With an unrealistically high $\eta=2$, 10 steps from 10 end at $x=-1.528166$, a poor local minimum.

**Multivariate.** $f(\mathbf x+\boldsymbol\epsilon)=f(\mathbf x)+\boldsymbol\epsilon^\top\nabla f(\mathbf x)+O(\|\boldsymbol\epsilon\|^2)$, so $-\nabla f$ is the steepest-descent direction and $\mathbf x\leftarrow\mathbf x-\eta\nabla f(\mathbf x)$. On $f=x_1^2+2x_2^2$ from $(-5,-2)$ with $\eta=0.1$, 20 steps give $(-5\cdot0.8^{20},\,-2\cdot0.6^{20})=(-0.057646,-0.000073)$, as D2L prints. D2L's helper `train_2d(trainer, steps=20)` starts every 2-D experiment of the chapter at $(-5,-2)$ and passes two state variables `s1, s2` for momentum-type methods.

**Newton's method.** Keep the second-order term: $f(\mathbf x+\boldsymbol\epsilon)=f(\mathbf x)+\boldsymbol\epsilon^\top\nabla f+\tfrac12\boldsymbol\epsilon^\top\mathbf H\boldsymbol\epsilon+O(\|\boldsymbol\epsilon\|^3)$. Setting the derivative in $\boldsymbol\epsilon$ to 0 gives $\boldsymbol\epsilon=-\mathbf H^{-1}\nabla f(\mathbf x)$. Storing $\mathbf H$ costs $O(d^2)$, too much for deep networks.

| problem | result |
|---|---|
| $f=\tfrac12x^2$ | one step reaches 0 (the Taylor expansion is exact) |
| $f=\cosh(0.5x)$ from 10 | 0 after 10 steps (convex) |
| $f=x\cos(0.15\pi x)$ from 10, $\eta=1$ | $x=26.8341$: walks **uphill** where $f''<0$ |
| same, $\eta=0.5$ | $x=7.2699$ |

Fixes for the nonconvex case: use $|f''|$, or bring back a learning rate. Second-order information still helps: cautious where curvature is large, bold where the function is flat.

**Convergence of Newton.** Let $e^{(k)}=x^{(k)}-x^*$ for convex, three-times differentiable $f$ with $f''>0$. Expanding $f'(x^*)=0$ around $x^{(k)}$ gives
$$|e^{(k+1)}|=\tfrac12(e^{(k)})^2\frac{|f'''(\xi^{(k)})|}{f''(x^{(k)})}\le c\,(e^{(k)})^2$$
in a region where that ratio is bounded by $c$: the error is squared each step. On $\cosh(0.5x)$ from $x=1$: 0.0758, $3.6\times10^{-5}$, $4.0\times10^{-15}$, then 0 (mine). Caveats: no guarantee when you reach that region, and $f$ must be well behaved up to third derivatives.

> [!note] Terminology (discrepancy D10)
> D2L says optimization researchers call $|e^{(k+1)}|\le c(e^{(k)})^2$ "linear convergence" and $|e^{(k+1)}|\le\alpha|e^{(k)}|$ a "constant rate". Standard usage (e.g. Nocedal & Wright) calls the first **quadratic** convergence and the second **linear** convergence. The mathematics in D2L is right; the names are swapped. See [[Optimization/contents/00-Index|Optimization]].

**Preconditioning.** Use only the Hessian's diagonal: $\mathbf x\leftarrow\mathbf x-\eta\,\mathrm{diag}(\mathbf H)^{-1}\nabla f(\mathbf x)$. This fixes units mismatches (one variable in millimetres, another in kilometres) and amounts to a separate learning rate per coordinate, the idea behind Adagrad, RMSProp and Adam (§28–30).

**Line search.** Take the direction $-\nabla f$ and binary-search the $\eta$ minimizing $f(\mathbf x-\eta\nabla f)$. Fast to converge, but each probe evaluates the loss on the whole dataset, so it is impractical in deep learning.

### 24. Stochastic gradient descent (§12.4)

The objective is an average over examples, $f(\mathbf x)=\frac1n\sum_if_i(\mathbf x)$, so a full gradient costs $O(n)$. SGD samples one index $i$ uniformly and steps $\mathbf x\leftarrow\mathbf x-\eta\nabla f_i(\mathbf x)$ at cost $O(1)$. The stochastic gradient is **unbiased**: $\mathbb E_i\nabla f_i(\mathbf x)=\frac1n\sum_i\nabla f_i(\mathbf x)=\nabla f(\mathbf x)$.

D2L simulates SGD by adding $\mathcal N(0,1)$ noise to the gradient of $x_1^2+2x_2^2$. With constant $\eta=0.1$, after 50 steps $\mathbf x=(-0.299,-0.024)$: the noise keeps the iterate bouncing near the minimum, and more steps do not help. The only remedy is to **decrease $\eta$ over time**:

| schedule | formula | D2L's run |
|---|---|---|
| piecewise constant | $\eta_i$ for $t_i\le t<t_{i+1}$ | common for deep nets: drop when progress stalls |
| exponential | $\eta_0e^{-\lambda t}$ | $e^{-0.1t}$: after 1000 steps still at $(-0.896,0.012)$; the rate dies before convergence |
| polynomial | $\eta_0(\beta t+1)^{-\alpha}$ | $(1+0.1t)^{-1/2}$: $(0.054,0.059)$ after only 50 steps |

$\alpha=0.5$ is the popular, well-analysed choice for convex problems.

**Convergence for convex objectives** (Nesterov & Vial). With stochastic gradients bounded by $L$, $r=\|\mathbf x_1-\mathbf x^*\|$ and the weighted average iterate $\bar{\mathbf x}=\sum_t\eta_t\mathbf x_t/\sum_t\eta_t$:
$$\mathbb E[R(\bar{\mathbf x})]-R^*\le\frac{r^2+L^2\sum_{t=1}^T\eta_t^2}{2\sum_{t=1}^T\eta_t}.$$
The per-step inequality $\|\mathbf x_t-\mathbf x^*\|^2-\|\mathbf x_{t+1}-\mathbf x^*\|^2\ge2\eta_t(f(\xi_t,\mathbf x_t)-f(\xi_t,\mathbf x^*))-\eta_t^2L^2$ shows we make progress only while the loss gap exceeds $\eta_tL^2/2$, so $\eta_t$ must go to zero. With $\eta=r/(L\sqrt T)$ the bound is $rL/\sqrt T$: rate $O(1/\sqrt T)$. For nonconvex problems no such guarantee exists (minimizing them is NP-hard in general).

**With or without replacement.** Drawing $n$ samples with replacement, a given example is picked at least once with probability $1-(1-1/n)^n\to1-e^{-1}\approx0.63$, and exactly once with probability $\approx e^{-1}\approx0.37$. Sampling with replacement wastes data and adds variance, so practice (and this book) passes over a reshuffled dataset each epoch.

### 25. Minibatch SGD (§12.5)

Full-batch GD is not **data-efficient** when examples are similar; single-example SGD is not **computationally efficient** because hardware cannot vectorize. Minibatches sit in between.

**Hardware.** A 2 GHz CPU with 16 cores and AVX-512 can process up to $2\times10^9\cdot16\cdot32=10^{12}$ bytes/s; GPUs 100× more. Memory bandwidth of a midrange server is about 100 GB/s, under a tenth of what keeps the processor fed. Memory is read in wide chunks (64 bits and up, 384 on some GPUs) and first access is costly while sequential (burst) reads are cheap. Caches (registers, L1, L2, L3) bridge the gap, and that is what batching exploits.

D2L computes $\mathbf A=\mathbf B\mathbf C$ for $256\times256$ matrices ($2mnp=2\cdot256^3=3.36\times10^7\approx0.03$ GFLOP) four ways:

| method | GFLOP/s (D2L's run) |
|---|---|
| element by element, `A[i,j] = dot(B[i,:], C[:,j])` | 0.013 |
| column by column, `A[:,j] = mv(B, C[:,j])` | 0.159 |
| blocks of 64 columns | 1.258 |
| one `torch.mm(B, C)` | 3.200 |

A block of 64 columns is nearly as efficient as the whole product, which is why moderate minibatches cost little more per example than full batches. Python and framework overhead per command adds to this.

**Statistics.** The minibatch gradient $\mathbf g_t=\partial_{\mathbf w}\frac1{|\mathcal B_t|}\sum_{i\in\mathcal B_t}f(\mathbf x_i,\mathbf w)$ has the same expectation as one example's gradient, and its standard deviation falls by $b^{-1/2}$ for batch size $b$. Beyond some size the extra variance reduction is small compared to the linear growth in compute; pick a batch that is efficient and fits GPU memory. With larger batches the noise that batch norm relies on also shrinks ([[05 - Convolutional Neural Network|ch. 05]]).

**Experiment.** NASA airfoil self-noise data, first 1500 examples, whitened (zero mean, unit variance per coordinate); linear regression; loss = squared loss averaged over the minibatch.

```python
def sgd(params, states, hyperparams):
    for p in params:
        p.data.sub_(hyperparams['lr'] * p.grad)
        p.grad.data.zero_()
```

| run | batch | lr | epochs | loss | sec/epoch |
|---|---|---|---|---|---|
| GD | 1500 | 1 | 10 | 0.253 | 0.028 |
| SGD | 1 | 0.005 | 2 | 0.243 | 0.954 |
| minibatch | 100 | 0.4 | 2 | 0.246 | 0.035 |
| minibatch | 10 | 0.05 | 2 | 0.252 | 0.109 |
| concise (`torch.optim.SGD`) | 10 | 0.01 | 4 | 0.242 | 0.128 |

GD updates once per epoch and stalls after about 6 steps. SGD makes 1500 updates per epoch and wins per example processed but is 34× slower per epoch. Batch 100 is the best trade-off in wall-clock time, even beating GD. The concise version uses `nn.MSELoss(reduction='none')` and halves it when reporting, to match the $\tfrac12$ convention.

### 26. Gradient descent on an ill-conditioned quadratic (§12.6)

D2L's example $f(\mathbf x)=0.1x_1^2+2x_2^2$ has Hessian eigenvalues 0.2 and 4, so $\kappa=20$. Per eigendirection, gradient descent is exactly
$$x_t=(1-\eta\lambda)^t\,x_0$$

| $\eta$ | closed form after 20 steps from $(-5,-2)$ | D2L prints |
|---|---|---|
| 0.4 | $(0.92)^{20}(-5)=-0.943467$, $(-0.6)^{20}(-2)=-0.000073$ | `x1: -0.943467, x2: -0.000073` |
| 0.6 | $(0.88)^{20}(-5)=-0.387814$, $(-1.4)^{20}(-2)=-1673.365109$ | `x1: -0.387814, x2: -1673.365109` |

The start point $(-5,-2)$ is not given in the text; it was recovered by matching the printout, and all of D2L's printed traces in this section then match to six decimals.

Stability: $|1-\eta\lambda_{\max}|<1\iff\eta<2/\lambda_{\max}=0.5$. So $\eta=0.4$ is stable and $\eta=0.6$ diverges at rate 1.4 per step. The underlying tension: $x_2$ needs a small step, $x_1$ a large one, and both share $\eta$.

### 27. Momentum (§12.6)

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

### 28. Adagrad and preconditioning (§12.7)

$$\mathbf s_t=\mathbf s_{t-1}+\mathbf g_t^2,\qquad \mathbf w_t=\mathbf w_{t-1}-\frac{\eta}{\sqrt{\mathbf s_t+\epsilon}}\odot\mathbf g_t$$

Motivation: sparse features (rare features get larger steps), and more generally diagonal preconditioning, using gradient magnitudes as a cheap proxy for the Hessian diagonal.

| $\eta$ | simulated | D2L prints |
|---|---|---|
| 0.4 | $(-2.382563, -0.158591)$ | `x1: -2.382563, x2: -0.158591` |
| 2.0 | $(-0.002295, -0.000000)$ | `x1: -0.002295, x2: -0.000000` |

With roughly constant gradients $s_t\approx tg^2$, so the step decays like $\eta/\sqrt t$. Total travel $2\eta\sqrt t$ still grows, so Adagrad slows down rather than stopping. At $\eta=0.4$, Adagrad has covered 52.35% of the distance in $x_1$ after 20 steps; RMSProp (§29) at the same $\eta$ has covered 99.79% ($x_1=-0.010599$).

**Rotated problems** (D2L ex. 12.7.2–4, unanswered). Rotate the same quadratic by 45°: $f=0.1(x_1+x_2)^2+2(x_1-x_2)^2$, $\mathbf Q=\begin{pmatrix}4.2&-3.8\\-3.8&4.2\end{pmatrix}$.

| | eigenvalues | $\kappa$ | after diagonal preconditioning | $\kappa$ |
|---|---|---|---|---|
| axis-aligned | (0.2, 4.0) | 20 | (1.0, 1.0) | 1 |
| rotated 45° | (0.4, 8.0) | 20 | (0.095238, 1.904762) | 20 |

Diagonal preconditioning fixes the axis-aligned case completely and does nothing for the rotated one. All diagonal adaptive methods (Adagrad, RMSProp, Adadelta, Adam) assume curvature is roughly aligned with the coordinates. Gerschgorin's theorem gives $\kappa\le(1+R)/(1-R)$ after preconditioning, where $R$ is the largest off-diagonal row sum; here $R=0.904762$ and the bound equals the true $\kappa=20$.

### 29. RMSProp and Adadelta (§12.8–12.9)

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

### 30. Adam (§12.10)

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

### 31. D2L's optimizer runs side by side

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

### 32. Learning-rate scheduling (§12.11)

The rate at which weights change matters as much as the update rule. D2L's checklist:

1. **Magnitude**: too large diverges, too small is slow; the condition number sets the usable range (§26).
2. **Decay**: needed to stop bouncing around the minimum, but probably slower than the $O(t^{-1/2})$ suited to convex problems.
3. **Warmup**: initial parameters are random, so early update directions may be meaningless; start small.
4. **Cyclic schedules** and averaging over the parameter path (Izmailov et al. 2018): out of scope.

**Toy problem.** A modernized LeNet (ReLU, max pooling; see [[05 - Convolutional Neural Network|ch. 05]]) on Fashion-MNIST, batch 256, SGD, 30 epochs. The training loop sets `param_group['lr'] = scheduler(epoch)` after each epoch for a custom scheduler, or calls `scheduler.step()` for a PyTorch one. The learning rate can always be set by hand: `trainer.param_groups[0]["lr"] = 0.1`.

| schedule | formula | train loss | train acc | test acc |
|---|---|---|---|---|
| constant 0.3 | $\eta=0.3$ | 0.191 | 0.926 | 0.895 |
| square root, $\eta_0=0.1$ | $\eta_0(t+1)^{-1/2}$ | 0.272 | 0.901 | 0.883 |
| multi-step, 0.5 halved at epochs 15, 30 | see erratum E2 | 0.196 | 0.926 | 0.889 |
| cosine 0.3 → 0.01 over 20 epochs | below | 0.186 | 0.932 | 0.901 |
| cosine with 5 warmup epochs | below | 0.200 | 0.925 | 0.897 |

With a constant rate, training accuracy keeps rising while test accuracy stalls: overfitting. The square-root schedule gives smoother curves and a smaller train–test gap. D2L notes it is not well understood why decaying the rate reduces overfitting; "smaller steps keep parameters near zero" does not fully explain it.

**Factor scheduler.** $\eta_{t+1}\leftarrow\max(\eta_{\min},\eta_t\alpha)$. With $\alpha=0.9$, $\eta_0=2$ and floor 0.01 it decays geometrically; after 50 updates it is $2\cdot0.9^{50}=0.0103$, just above the floor.

```python
class FactorScheduler:
    def __init__(self, factor=1, stop_factor_lr=1e-7, base_lr=0.1):
        self.factor = factor
        self.stop_factor_lr = stop_factor_lr
        self.base_lr = base_lr
    def __call__(self, num_update):
        self.base_lr = max(self.stop_factor_lr, self.base_lr * self.factor)
        return self.base_lr
```

**Multi-factor (piecewise constant).** Keep $\eta$ constant and multiply it by $\alpha$ at chosen times $s=\{5,10,20\}$: let optimization reach a stationary distribution of weights, then reduce the rate to settle into a better local minimum. PyTorch: `lr_scheduler.MultiStepLR(trainer, milestones=[15, 30], gamma=0.5)`.

> [!warning] Erratum E2 (D2L §12.11.3, multi-factor run)
> To plot the schedule, D2L calls `trainer.step(); scheduler.step()` 30 times on the *same* optimizer and scheduler, then trains with them. The plotting loop has already passed both milestones, so the learning rate is 0.125 when training starts and stays 0.125 for all 30 epochs (checked in PyTorch). The printed result (test acc 0.889) is therefore a constant-0.125 run, not the 0.5 → 0.25 → 0.125 schedule described. To reproduce the intended run, create a fresh optimizer and scheduler after plotting.

**Cosine** (Loshchilov & Hutter 2016): do not cut the rate drastically at first, and finish with a very small rate:
$$\eta_t=\eta_T+\frac{\eta_0-\eta_T}2\Big(1+\cos\frac{\pi t}{T}\Big),\qquad t\in[0,T],$$
then hold $\eta_T$. With $\eta_0=0.3$, $\eta_T=0.01$, $T=20$: 0.3 at $t=0$, 0.2575 at 5, 0.155 at 10, 0.0525 at 15, 0.01 from 20 on. It helped here (best test accuracy) but improvements are not guaranteed.

**Warmup.** Some architectures are unstable early; a small rate avoids divergence but is slow, a large one diverges. Increase the rate linearly to its maximum, then cool down. With 5 warmup steps the cosine schedule above becomes 0, 0.06, …, 0.24, 0.3 at $t=5$, then decays from there over the remaining 15 steps (0.2275 at $t=10$, 0.01 at 20). Warmup can precede any schedule. Gotmare et al. (2018) find it limits parameter divergence in very deep networks.

```python
class CosineScheduler:
    def __init__(self, max_update, base_lr=0.01, final_lr=0,
                 warmup_steps=0, warmup_begin_lr=0):
        self.base_lr_orig = base_lr
        self.max_update = max_update
        self.final_lr = final_lr
        self.warmup_steps = warmup_steps
        self.warmup_begin_lr = warmup_begin_lr
        self.max_steps = self.max_update - self.warmup_steps
    def get_warmup_lr(self, epoch):
        increase = (self.base_lr_orig - self.warmup_begin_lr) \
                   * float(epoch) / float(self.warmup_steps)
        return self.warmup_begin_lr + increase
    def __call__(self, epoch):
        if epoch < self.warmup_steps:
            return self.get_warmup_lr(epoch)
        if epoch <= self.max_update:
            self.base_lr = self.final_lr + (
                self.base_lr_orig - self.final_lr) * (1 + math.cos(
                math.pi * (epoch - self.warmup_steps) / self.max_steps)) / 2
        return self.base_lr
```

D2L's closing point: optimizer and schedule choices change not only the training loss but also how much the model overfits, for the same training error.

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

> [!example]- **2.** *(Easy–medium) PyTorch mechanics (D2L ch. 6)*
> `shared = nn.LazyLinear(8)`; `net = nn.Sequential(nn.LazyLinear(8), nn.ReLU(), shared, nn.ReLU(), shared, nn.ReLU(), nn.LazyLinear(1))`, run once on a $2\times4$ input.
> **(a)** How many parameters does `net.parameters()` count, and which names does `named_parameters()` list? **(b)** How does `shared.weight.grad` relate to the gradients of an untied copy? **(c)** A custom module stores its layers in a Python list. What breaks? **(d)** What is wrong with `torch.matmul(X, self.weight.data)` in a layer's `forward`? **(e)** You trained on `cuda:0` and want predictions on a CPU-only machine. What do you save and how do you reload?
>
> ---
> **(a)** $4\cdot8+8=40$, shared $8\cdot8+8=72$ (counted once), last $8+1=9$: 121. Names `0.weight, 0.bias, 2.weight, 2.bias, 6.weight, 6.bias`; index 4 is the same object as 2 and is not listed again.
>
> **(b)** It is the **sum** of the gradients the two uses would have as separate copies with equal values (checked: `allclose` is True).
>
> **(c)** The layers are not registered: `parameters()` is empty (0 tensors in a test), so the optimizer trains nothing, and `.to(device)` and `state_dict()` skip them. Use `nn.ModuleList` or `add_module`.
>
> **(d)** `.data` detaches from autograd, so no gradient reaches the weight; `backward()` fails (erratum E1). Use `self.weight`.
>
> **(e)** Save `net.state_dict()`; on the CPU machine rebuild the class in code, `load_state_dict(torch.load('mlp.params', map_location='cpu'))`, then `eval()`.

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
- Code: `nn.Sequential(nn.Flatten(), nn.LazyLinear(256), nn.ReLU(), nn.LazyLinear(10))`; dropout via `nn.Dropout(p)`, active only in `train()` mode.
- Real data (Kaggle): standardize numerics, fill NAs with the mean (0 after standardizing), one-hot categories, train on log price, select with K-fold CV.
- PyTorch: modules nest; `Sequential` registers children; shared layers sum gradients; `apply` initializes; lazy layers infer shapes on the first batch; save `state_dict()` and rebuild the class to load; keep all operands on one device.
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
- GD on $x^2$ multiplies $x$ by $1-2\eta$ per step; Newton squares the error near a convex minimum but walks uphill where $f''<0$. SGD is unbiased but needs a decaying rate; convex rate $O(1/\sqrt T)$. Minibatch std falls as $b^{-1/2}$; blocks of 64 columns already run near full-matrix speed.
- Schedules: piecewise constant, factor, square root, cosine, warmup. They change overfitting as well as training loss.

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
17. Using `.data` inside `forward` silently disables learning for that parameter (erratum E1).
18. Layers kept in a plain Python list are invisible to `parameters()`, `.to()` and `state_dict()`.
19. `state_dict()` saves parameters, not code; you need the class to reload.
20. A scheduler object carries state: stepping it for a plot changes the run that follows (erratum E2).
21. Exponential decay often stops learning before convergence; $t^{-1/2}$ or piecewise drops are safer.
22. SGD with a constant learning rate does not converge to the minimum; it hovers at a noise floor.
23. Fit standardization on training data only in real deployments; D2L pools train and test features for the competition.
24. Moving tensors to the CPU each step (printing the loss, `.numpy()`) stalls the GPU.

> [!warning] Gaps in the source material
> - **Figures:** the MLP diagram, computational graph and dropout diagram are reconstructed from the prose. Activation plots, optimizer trajectory plots and schedule curves are lost, but the trajectories were recovered numerically from the printed endpoints.
> - **Code** loses its indentation; printed outputs extract intact.
> - **Added by me:** the rank example (D2L ex. 5.1.1); §8's depth bounds; the Lyapunov exponent and 400-run simulation; the Xavier mean/median table; the dropout variance (ex. 5.6.3) and audit of the printed example; the memory accounting (ex. 5.3.3); the closed form for GD, the recovered start point and the reproduced traces; the $\kappa$ vs $\sqrt\kappa$ table; the effective-step check; the rotated preconditioning result and Gerschgorin bound (ex. 12.7.2–4); the Adam bias ratio and scale invariance; the 13-run table.
> - **Declined discrepancy D7:** "half-life of 10" for $\rho=0.9$ (true half-life 6.58); loose wording for a correctly computed quantity.
> - **Errata found by running D2L's code (PyTorch 2.11):** E1, `MyLinear` uses `.data` in `forward` and cannot be trained (§19); E2, the multi-factor schedule run trains at a constant 0.125 because the plotting loop already stepped the scheduler past both milestones (§32). **Discrepancy D10:** Newton's quadratic convergence is called "linear" (§23).
> - **Also added by me:** the closed forms for D2L's GD, Newton and schedule printouts; the Newton error sequence on cosh; the $2mnp$ count; the Kaggle log-RMSE conversion; the plain-list and tied-gradient checks (exercise 2); the corrected dropout keep count (10 or 11).
> - **Skipped:** convexity proofs (§12.2, see [[Optimization/contents/02 - Convex Sets and Convex Functions|Optimization]]); download helpers; the `Animator`/plotting code; multi-GPU training (ch. 13, see [[MLOps/contents/00-Index|MLOps]]).
> - Literature results (double descent, NTK, 10,000-layer training) are quoted, not derived.

**Previous:** [[03 - Logistic Regression]] · **Next:** [[05 - Convolutional Neural Network]]
