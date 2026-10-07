---
subject: Computer Vision
chapter: 3
tags: [ds, computer-vision, classification, knn, linear-classifier, hinge, softmax, cross-entropy, regularization, sgd]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 03: Image Classification & Linear Models (61 slides); Stanford CS231n notes; Szeliski 2nd ed. §5.1–5.2"
---

# Image Classification and Linear Models

Week 3. The first lecture about *learning*. Instead of designing filters and features by hand (week 2), we let data set the parameters. The lecture builds the complete pipeline every later model reuses: a score function, a loss function, and an optimiser.

## 📘 Main Knowledge

### 1. The task and the data-driven approach (slides 3–7)

**Image classification:** the input is a fixed-size array of numbers (an image); the output is one label from a fixed set of $C$ categories. Detection, segmentation and captioning are all built on top of it.

There's no obvious algorithm: you can't write `if` statements over all the pixels to recognise a cat. Instead, *write a program that writes the classifier*: collect labelled examples and fit a model to them.

**The three components every learning system needs (slide 7):**
1. A **score function** $f(x; W)$ mapping pixels to class scores.
2. A **loss function** measuring how wrong the scores are.
3. An **optimisation** procedure that finds the $W$ minimising the loss.

### 2. Data and evaluation (slides 8–12)

**Benchmark datasets:**

| Dataset | Classes | Training images | Image size | Note |
|---|---|---|---|---|
| MNIST | 10 | 60,000 | 28×28 grey | solved; only useful for debugging |
| CIFAR-10 | 10 | 50,000 | 32×32 RGB | the teaching standard |
| CIFAR-100 | 100 | 50,000 | 32×32 RGB | same images, finer labels |
| ImageNet-1k | 1,000 | 1.28 million | ~256×256 | the benchmark that started deep learning |

Benchmark accuracy isn't the same as working in practice: all of these have known label noise and collection bias.

**Splitting the data (slide 10):**
- **Train**: the model fits these.
- **Validation**: choose hyperparameters (settings you pick rather than learn, e.g. $k$ in k-NN, $\lambda$, learning rate) on these.
- **Test**: used **once**, at the very end.

A typical split is 70/15/15, or the fixed test set that comes with a benchmark. Looking at test results and then changing something leaks test information into the model, and the test score stops being an honest estimate.

**Cross-validation (slide 11).** Split the training data into $k$ folds. Train on $k-1$ folds, validate on the remaining one, rotate through all $k$, and average.
- Uses all the data for both training and validation.
- Gives an **error bar** (spread across folds), so you can tell a real improvement from noise.
- Costs $k$ training runs. Standard for small datasets and classical methods, rare in deep learning (too expensive). Useful for small projects.

**Measuring performance (slide 12):**
- **Accuracy** = correct / total. Easy to read, easy to abuse. Under class imbalance it's useless: if 99% of scans are healthy, a model that always says "healthy" scores 99%. And it doesn't say which classes fail.
- **Confusion matrix** $M_{ij}$ = number of examples of true class $i$ predicted as class $j$. The off-diagonal entries show what the model actually confuses. Usually the first thing to plot when a model underperforms.
- **Top-5 accuracy**: correct if the true label is among the 5 highest scores (used for ImageNet, where many classes are similar).

### 3. Nearest neighbour (slides 13–19)

**The simplest possible classifier.**
- *Train:* memorise every training image and its label.
- *Predict:* find the most similar training image and copy its label.

Cost: training is $O(1)$ (just store), prediction is $O(N)$ (compare with all $N$ training images). That's backwards from what we want: training can take hours, but prediction should be fast. For CIFAR-10, one prediction compares against 50,000 images of 3,072 numbers each: about 154 million operations.

**Distance between images** (treated as vectors in $\mathbb R^D$, summing over pixels $p$):

$$d_1(I_1, I_2) = \sum_p |I_1^p - I_2^p| \quad (\text{L1, Manhattan}), \qquad d_2(I_1, I_2) = \sqrt{\sum_p (I_1^p - I_2^p)^2} \quad (\text{L2, Euclidean})$$

**k-nearest neighbours (slide 16):** take a majority vote among the $k$ closest training points.
- $k = 1$: jagged decision boundary, islands of noise, zero training error.
- Larger $k$: smoother boundary, more robust, but small classes get outvoted.
- $k$ and the distance metric are **hyperparameters**, chosen on validation data.
- Regions with no clear majority are genuinely ambiguous.

**Why k-NN fails on images (slides 17–18):**
- Pixel distance measures *photometric* difference, not *semantic* difference. Very different corruptions of an image (shifted, masked, darkened) can all have nearly the same L2 distance to the original. This is the semantic gap from week 1 with a number attached.
- **Curse of dimensionality:** to cover $[0,1]^D$ at resolution $r$ you need about $(1/r)^D$ points. With $r = 0.1$: 10 points for $D = 1$, 1,000 for $D = 3$, and for $D = 3072$ (CIFAR-10) more points than atoms in the universe. In high dimensions the nearest and farthest neighbours end up at nearly the same distance, so "nearest" stops meaning anything: $(d_{max} - d_{min})/d_{min}$ collapses as $D$ grows.

**Verdict (slide 19):** never use k-NN on raw pixels. But k-NN on **learned features** is everywhere: face recognition (nearest neighbour in an embedding space), image retrieval and deduplication, retrieval-augmented generation (RAG), few-shot learning. *"The space matters more than the classifier."*

### 4. Linear classification (slides 20–27)

**The score function:**

$$f(x_i; W, b) = W x_i + b$$

With $C$ classes and $D$-dimensional inputs:
- $x_i \in \mathbb R^{D}$: one image, flattened into a column vector;
- $W \in \mathbb R^{C \times D}$: the weights;
- $b \in \mathbb R^{C}$: the bias;
- output $s \in \mathbb R^{C}$: one score per class.

For CIFAR-10, $W$ is $10 \times 3072$ and $b$ is $10 \times 1$: **30,730 parameters**. Each row of $W$ is a separate classifier for one class, all run in parallel. Prediction = the class with the highest score.

**The bias trick (slide 23).** Append a 1 to $x$ and the column $b$ to $W$: $Wx + b = \tilde W \tilde x$. One matrix, one gradient. In code, frameworks keep weight and bias separate anyway, because they're regularised differently (weight decay applies to $W$ but usually not to $b$).

**Three ways to read a linear classifier:**

1. **Algebra:** a matrix multiply plus a bias.
2. **Template matching (slide 24).** Row $k$ of $W$, $w_k$, has the same shape as an image. The score $s_k = w_k^\top x$ is an inner product: how well the image lines up with template $w_k$. Reshape $w_k$ back into an image to see what the classifier learned. The limitation: **one template per class**. A cat facing left and a cat facing right must share a single template, so the template ends up a blurry average (e.g. the "horse" template often looks like a two-headed horse).
3. **Geometry (slide 25).** Each image is a point in $\mathbb R^D$. For class $k$, $w_k^\top x + b_k = 0$ is a **hyperplane**: scores are positive on one side, negative on the other. $w_k$ sets the orientation, $b_k$ shifts it away from the origin. Scaling $w_k$ makes the scores steeper without moving the boundary.

**What a linear classifier can't do (slide 26).** A single hyperplane only separates **linearly separable** data.
- XOR-like patterns: impossible for any $W$.
- Two concentric rings: impossible.
- Multimodal classes (a horse seen from two viewpoints): one template has to cover both, so it covers neither well.

Two ways out:
1. Transform the features first, then use a linear model. That's HOG + SVM ([[02 - Classical Image Processing|ch. 02]]).
2. **Learn** the transformation. That's a neural network ([[04 - From Neural Networks to CNNs|ch. 04]]).

**Preprocessing (slide 27):**
- **Mean subtraction** centres the data: $x \leftarrow x - \mu$, with $\mu = \frac1N \sum_i x_i$.
- **Normalisation** puts features on comparable scales: $x \leftarrow (x - \mu)/\sigma$.
- Uncentred data makes the loss surface a long, narrow valley, and gradient descent zig-zags across it.
- **Compute $\mu$ and $\sigma$ on the training set only**, then apply those same numbers to validation and test data.

### 5. Loss functions (slides 28–38)

A loss turns "these scores are bad" into a number to minimise:

$$L = \underbrace{\frac{1}{N} \sum_{i=1}^{N} L_i\big(f(x_i; W),\, y_i\big)}_{\text{data loss}} + \underbrace{\lambda R(W)}_{\text{regularisation}}$$

- $L_i \ge 0$, and $L_i = 0$ exactly when the prediction is as good as we ask.
- It must be differentiable (almost everywhere) for gradient descent.
- **We don't optimise accuracy directly.** Accuracy is piecewise constant (it only changes when a prediction flips), so its gradient is zero almost everywhere. We optimise a differentiable stand-in (a *surrogate*) and hope accuracy follows.

#### Multiclass SVM (hinge) loss (slides 30–31)

$$L_i = \sum_{j \ne y_i} \max\big(0,\ s_j - s_{y_i} + \Delta\big), \qquad \Delta = 1$$

It wants the correct class's score $s_{y_i}$ to beat every other score by at least the margin $\Delta$.
- If $s_{y_i} \ge s_j + \Delta$, that term is zero (good enough).
- Otherwise it grows linearly with how far short we fell.
- Called "hinge" because of the kink at zero.

Slide 31's examples (correct class first, $\Delta = 1$):
- $s = [13, -7, 11]$: $\max(0, -7 - 13 + 1) + \max(0, 11 - 13 + 1) = 0 + 0 = 0$. Correct and past the margin.
- $s = [13, -7, 12.5]$: $0 + \max(0, 12.5 - 13 + 1) = 0.5$. Still correctly classified, but too close, so the loss is nonzero and training continues.

*"Loss and accuracy are not the same thing"*: zero loss is possible while the model could still improve, and nonzero loss is possible at 100% accuracy.

#### Binary classification: sigmoid and binary cross-entropy (slide 32)

With two classes, one score is enough:

$$p = \sigma(s) = \frac{1}{1 + e^{-s}} = P(y = 1 \mid x), \qquad P(y = 0 \mid x) = 1 - p$$

Maximising the likelihood of the observed label gives the **binary cross-entropy (BCE)**:

$$L = -\big[y \log p + (1 - y) \log(1 - p)\big], \qquad y \in \{0, 1\}$$

Only one term survives: $-\log p$ if $y = 1$, $-\log(1-p)$ if $y = 0$. With a linear score $s = w^\top x + b$ this is exactly **logistic regression** ([[Deep Learning/contents/03 - Logistic Regression|DL ch. 03]]). One output unit, not two.

#### Multiclass: softmax and cross-entropy (slide 33)

$C$ classes, exactly one correct. Treat the scores as unnormalised log-probabilities and apply **softmax**:

$$p_k = P(Y = k \mid x_i) = \frac{e^{s_k}}{\sum_j e^{s_j}}$$

Minimise the negative log-probability of the correct class:

$$L_i = -\log p_{y_i} = -s_{y_i} + \log \sum_j e^{s_j}$$

- $p_k \in (0, 1)$ and $\sum_k p_k = 1$.
- This is the cross-entropy $H(q, p) = -\sum_k q_k \log p_k$ between the one-hot true distribution $q$ and the prediction $p$.
- With $C = 2$ it reduces exactly to binary cross-entropy, and in both cases $\partial L / \partial s_k = p_k - y_k$.

#### Multi-label: independent sigmoids (slides 34–36)

Sometimes several classes are true at once (a photo containing a person *and* a rocket). Softmax forces the probabilities to sum to 1, so it must split them (e.g. 0.55 and 0.35). For multi-label problems, drop that constraint and ask $C$ separate yes/no questions:

$$p_k = \sigma(s_k), \qquad L = -\sum_{k=1}^{C} \big[y_k \log p_k + (1 - y_k) \log(1 - p_k)\big]$$

- The label is a binary vector $y \in \{0,1\}^C$, not a single integer.
- Scores don't compete with each other. In PyTorch: `nn.BCEWithLogitsLoss`.
- Predict by thresholding each $p_k$ (usually at 0.5). There's no argmax.
- Used for VOC/COCO image-level classification, scene tagging, medical findings. Detection and segmentation avoid the issue by classifying each box or pixel, which is single-label again (weeks 7–9).

**Slide 36's worked example**, classes [person, rocket, cat, bus]:

| | Scores | Probabilities | Loss |
|---|---|---|---|
| Binary ("is there a person?") | $s = 2.2$ | $\sigma(2.2) = 0.900$ | $-\ln 0.900 = 0.105$ if truth is 1; $-\ln 0.100 = 2.305$ if truth is 0 |
| Multiclass (softmax), truth = person | $[2.40, 1.95, 0.18, -0.22]$ | $[0.55, 0.35, 0.06, 0.04]$ (sum 1) | $-\ln 0.55 = 0.598$ |
| Multi-label (sigmoids), truth = $[1,1,0,0]$ | $[2.9, 2.0, -3.5, -3.9]$ | $[0.95, 0.88, 0.03, 0.02]$ (sum 1.88) | per class $[0.054, 0.127, 0.030, 0.020]$, total 0.230 |

The multi-label probabilities summing to 1.88 is correct, not a bug: each one is a separate question.

**Numerical stability (slide 37).** $e^{s}$ overflows quickly (e.g. $e^{1000}$). Subtracting the maximum score doesn't change the result:

$$p_k = \frac{e^{s_k - \max_j s_j}}{\sum_j e^{s_j - \max_j s_j}}$$

Now the largest exponent is $e^0 = 1$, so nothing overflows, and small terms underflowing to zero is harmless. `torch.nn.CrossEntropyLoss` takes **raw scores (logits)**, not probabilities, so it can do this internally. Applying softmax yourself before it is a common, silent bug.

**Hinge vs softmax (slide 38):**

| | Hinge | Softmax (cross-entropy) |
|---|---|---|
| Output | scores | probabilities |
| Zero loss | reachable | never exactly |
| Once correct | stops caring (gradient exactly 0 past the margin) | keeps pushing $p_{y_i}$ towards 1 |
| Outliers | robust | sensitive |

Cross-entropy dominates modern work because it gives probabilities and combines easily with everything downstream.

### 6. Regularisation (slides 39–42)

**$W$ is not unique (slide 40).** If $W$ achieves zero hinge loss, so do $2W$, $10W$, $100W$: scaling all scores up keeps every margin satisfied. The data loss alone can't choose between them, so we add a term:

$$L = \frac1N \sum_i L_i + \lambda R(W), \qquad R(W) = \sum_k \sum_d W_{k,d}^2 \quad (\text{L2})$$

L2 penalises large weights and prefers **small, spread-out** weights over large, concentrated ones. Slide 40's example: $x = [1,1,1,1]$, $w_a = [1,0,0,0]$, $w_b = [0.25, 0.25, 0.25, 0.25]$. Both give $w^\top x = 1$, but $R(w_a) = 1$ and $R(w_b) = 0.25$. L2 prefers $w_b$, which uses all four pixels instead of betting everything on one.

**Forms of regularisation (slide 41):**

$$R_{L2}(W) = \sum W^2, \qquad R_{L1}(W) = \sum |W|, \qquad R_{elastic}(W) = \sum \big(\beta W^2 + |W|\big)$$

- **L2** ("weight decay"): shrinks all weights smoothly. The default.
- **L1**: drives weights exactly to **zero**, giving sparse models that use only a few inputs. Geometrically, the L1 constraint region is a diamond with corners on the axes, and the loss contours usually touch it at a corner (where some weights are 0). The L2 region is round and has no corners.
- **Elastic net**: a mix of both.
- Later in the course: dropout, batch norm, data augmentation, early stopping. These are all regularisers, but none is a penalty term.

**Choosing $\lambda$ (slide 42):**
- $\lambda$ too small: the model fits training noise, so there's a large gap between training and validation accuracy (**overfitting**).
- $\lambda$ too large: the model can't even fit the real pattern, so both scores are poor (**underfitting**).
- Pick $\lambda$ at the best *validation* score, not the best training score.
- Search on a **log scale**: $10^{-6}, 10^{-5}, \dots, 10^{2}$. A linear grid wastes almost all its samples.
- Bayesian reading: L2 is a Gaussian prior on $W$, L1 is a Laplace prior. Minimising loss + penalty is MAP (maximum a posteriori) estimation, and $\lambda$ says how strongly we believe the prior.

### 7. Optimisation (slides 43–52)

$L(W)$ is a function of 30,730 variables (for CIFAR-10). We want its minimum.
- **Random search** (try random $W$, keep the best): a terrible idea.
- **Random local search** (take a random step, keep it if the loss drops): better, still hopeless in 30,000 dimensions.
- **Follow the gradient**: the steepest-descent direction can be computed exactly for the cost of one pass over the data.

**Gradient descent (slide 45).** The gradient $\nabla_W L$ is the vector of partial derivatives; it points towards steepest increase, so step the other way:

$$W \leftarrow W - \eta\, \nabla_W L, \qquad \eta = \text{learning rate}$$

**Deriving the softmax gradient (slides 46–47).** With $L = -s_y + \log \sum_j e^{s_j}$:
- The first term contributes $-1$ only when $k = y$.
- The second term: $\frac{\partial}{\partial s_k} \log \sum_j e^{s_j} = \frac{e^{s_k}}{\sum_j e^{s_j}} = p_k$.

$$\boxed{\frac{\partial L}{\partial s_k} = p_k - \mathbb 1[k = y]}$$

i.e. predicted probability minus the one-hot truth. Since $s = Wx$, $\partial s_k / \partial W_{k,d} = x_d$, so by the chain rule

$$\frac{\partial L}{\partial W_{k,d}} = \big(p_k - \mathbb 1[k = y]\big)\, x_d$$

In matrix form, averaged over a batch of $N$ examples with L2 regularisation:

$$\nabla_W L = \frac1N (P - Y)^\top X + 2\lambda W$$

where $X \in \mathbb R^{N\times D}$ is the batch, $P \in \mathbb R^{N\times C}$ the predicted probabilities, and $Y$ the one-hot labels. **Check the shapes:** $(C\times N)(N\times D) = C\times D$, the shape of $W$. Shape-checking catches most gradient bugs.

**The hinge gradient (slide 48).** Let $m_j = \mathbb 1[s_j - s_{y_i} + \Delta > 0]$ mark the classes that violate the margin. Then

$$\nabla_{w_j} L_i = m_j\, x_i \quad (j \ne y_i), \qquad \nabla_{w_{y_i}} L_i = -\Big(\sum_{j \ne y_i} m_j\Big) x_i$$

- Only violating classes contribute.
- The correct-class row gets pushed up once for every violator.
- Examples already past the margin give no gradient at all.
- At exactly $s_j - s_{y_i} + \Delta = 0$ the derivative doesn't exist; pick a **subgradient** (say 0) and move on. Hitting the kink exactly almost never happens in floating point.

**The learning rate (slide 49)** is the single most important hyperparameter.
- Too small: correct but very slow.
- Slightly too large: the loss plateaus at a poor value.
- Far too large: the loss blows up to `nan` within a few iterations.

In practice: sweep on a log scale, watch the first few hundred iterations, pick the largest rate that still decreases smoothly, then decay it during training. Momentum, RMSProp and Adam refine this ([[05 - CNN Architectures|ch. 05]]).

**Stochastic gradient descent (slide 50).** Computing the gradient over all $N$ examples for one update is wasteful. The extreme alternative: update after every single example,

$$W \leftarrow W - \eta\, \nabla_W L_i, \qquad i \text{ chosen at random}$$

- The estimate is **unbiased**: $\mathbb E_i[\nabla_W L_i] = \nabla_W L$. Right on average, wrong on any single step.
- Cost per update drops from $O(N)$ to $O(1)$, so one epoch gives $N$ updates instead of one.
- Robbins & Monro, 1951.
- Convergence needs a **decaying** $\eta$, because the noise never dies out by itself.
- Nobody actually does this: one example can't fill a GPU, and the path is so noisy that $\eta$ must be small.

**Mini-batch gradient descent (slide 51)**, which is what everyone today calls "SGD":

$$\nabla_W L \approx \frac{1}{|B|} \sum_{i \in B} \nabla_W L_i, \qquad B \subset \{1,\dots,N\},\ |B| \ll N$$

- Still unbiased; the variance falls as $1/|B|$.
- Batch size is typically 32–256 (powers of two suit the hardware).
- **Iteration** = one parameter update. **Epoch** = one full pass over the data = $N/|B|$ iterations.
- Reshuffle every epoch, or the model learns the ordering.
- A batch is one matrix multiply, which is exactly what a GPU is built for.
- The noise helps: it can escape shallow minima and saddle points that trap full-batch descent, and small batches tend to generalise better (not fully understood).
- `torch.optim.SGD` + a `DataLoader` batch = mini-batch gradient descent.

**Comparison (slide 52):**

| | Full batch | Mini-batch | SGD (single example) |
|---|---|---|---|
| $\lvert B\rvert$ | $N$ | 32–256 | 1 |
| Gradient | exact | noisy | very noisy |
| Cost per update | $O(N)$ | $O(\lvert B\rvert)$ | $O(1)$ |
| Updates per epoch | 1 | $N/\lvert B\rvert$ | $N$ |
| GPU use | poor | ideal | poor |

In the lecture's demo, mini-batch's path was only 11% longer than full batch's, while pure SGD travelled 3.8× further to reach the same point. At the same $\eta$, batch size 1 was visibly unstable: **batch size and learning rate must be tuned together.**

### 8. The training loop (slides 53–57)

The whole method in a few lines (slide 54):

```python
W = 0.001 * np.random.randn(C, D)
for it in range(num_iters):
    idx = np.random.choice(N, batch)
    X_b, y_b = X[idx], y[idx]
    scores = X_b @ W.T
    loss, dS = softmax_loss(scores, y_b)      # dS = P - Y
    dW = dS.T @ X_b / batch + 2 * reg * W
    W -= lr * dW
```

Every training loop in the rest of the course (ResNet, ViT, diffusion models) has exactly this shape. What changes: `scores` comes from a deep network, `dW` comes from autograd instead of hand derivation, and `W -= lr * dW` becomes `optimizer.step()`.

**Sanity checks (slide 56).**

Before training:
1. **Check the initial loss.** With small random weights all scores are near 0. Softmax then gives every class $p = 1/C$, so $L \approx \log C$ (2.30 for $C = 10$). Hinge gives $\approx C - 1$ (each of the $C-1$ wrong classes contributes $\Delta = 1$).
2. **Turn regularisation up**: the loss should go up.
3. **Gradient check**: compare the analytic gradient with a numerical one $(f(x+h) - f(x-h))/2h$ on a few random coordinates.

During training:

4. **Overfit about 20 examples** to ~100% accuracy with regularisation off. If you can't, the model or the gradient is broken. *"Step 4 costs two minutes and finds most bugs. Skipping it costs a weekend."*
5. Watch the **train–validation gap**, not just the loss.
6. Plot the loss curve; its shape diagnoses the learning rate (§7).

**The bridge to next week (slide 57).**
- Today: $s = Wx$. One template per class; can't represent XOR or a horse from two viewpoints; trained on raw pixels, a poor representation. Last week's fix was hand-designed features (HOG) plus a linear model.
- Next week: $s = W_2 \max(0, W_1 x)$. One nonlinearity and the model can represent XOR. $W_1$ **learns** the features; $W_2$ is still today's linear classifier. The loss, gradient and training loop don't change. Then $W_1$ becomes a convolution, and we're back to week 2's filters, now learned.

**Hands-on (slide 61):** vectorised k-NN (the loop version is ~100× slower); tune $k$ by cross-validation; softmax loss with loops then vectorised; analytic gradient + gradient check; SGD with a learning-rate sweep; visualise learned templates; overfit 20 examples; reproduce it with `nn.Linear`.

## ✏️ Exercises

> [!example]- Exercise 1 — Hinge vs softmax on one example
> Three classes [cat, car, frog]. An image of a **cat** gets scores $s = [3.2,\ 5.1,\ -1.7]$.
> **(a)** Compute the hinge loss ($\Delta = 1$).
> **(b)** Compute the softmax probabilities and the cross-entropy loss.
> **(c)** Compute $\partial L / \partial s$ for the cross-entropy loss. Which way does gradient descent push each score?
> **(d)** Now suppose the scores are $[8.0, 5.1, -1.7]$. What are the hinge loss and the hinge gradient? Does cross-entropy still produce a gradient?
>
> ---
> **(a)** $\max(0, 5.1 - 3.2 + 1) + \max(0, -1.7 - 3.2 + 1) = 2.9 + 0 = 2.9$. Only "car" violates the margin.
>
> **(b)** Subtract the max (5.1) for stability: exponents of $[-1.9, 0, -6.8]$ = $[0.150, 1, 0.0011]$. Normalising: $p \approx [0.130, 0.869, 0.001]$. Loss $= -\ln 0.130 = 2.04$.
>
> **(c)** $p - y = [0.130 - 1,\ 0.869,\ 0.001] = [-0.870,\ 0.869,\ 0.001]$. Gradient descent subtracts the gradient, so it **raises** the cat score and **lowers** the car score strongly; frog barely moves (it's already very low).
>
> **(d)** Cat now beats car by $8.0 - 5.1 = 2.9 > 1$ and frog by more, so the hinge loss is **0** and its gradient is exactly **0**: the example no longer affects training. Cross-entropy still gives $p_{cat} < 1$, so it still produces a (small) gradient and keeps pushing the margin wider. That's the "satisfied vs never satisfied" difference from slide 38.

> [!example]- Exercise 2 — Read the training log
> You train a softmax linear classifier on CIFAR-10 ($C = 10$). What does each observation suggest?
> **(a)** The loss at iteration 0 is 2.31.
> **(b)** The loss at iteration 0 is 47.6.
> **(c)** After 2,000 iterations the loss is still 2.30 and accuracy is ~10%.
> **(d)** The loss goes to `nan` after 15 iterations.
> **(e)** Your code applies `torch.softmax` to the scores and passes the result to `nn.CrossEntropyLoss`. Training "works" but is slow and ends worse than expected. Why?
>
> ---
> **(a)** Expected. $\ln 10 = 2.30$: with small random weights every class gets about $1/10$.
>
> **(b)** Something is wrong before training starts. Typical causes: weights initialised too large (scores are big, so one wrong class dominates), unnormalised inputs (0–255 instead of standardised), or a bug in the loss.
>
> **(c)** The model has learned nothing: it still predicts uniform probabilities, i.e. chance accuracy. Likely causes: learning rate far too small, gradient not applied (e.g. a bug in the update), or gradients that are zero. Overfitting 20 examples would quickly tell you which.
>
> **(d)** Learning rate far too large: the updates overshoot and the scores explode. Lower it by about 10× and sweep on a log scale.
>
> **(e)** `CrossEntropyLoss` applies its own (log-)softmax internally and expects raw scores. Applying softmax twice squashes the inputs into $[0,1]$, so the second softmax sees nearly equal values and produces small, weak gradients. Pass raw logits.

> [!example]- Exercise 3 — One label or several?
> A chest X-ray model has three outputs: [pneumonia, effusion, nodule]. For one image the scores are $s = [1.5,\ -0.5,\ 0.8]$. The radiologist's report lists pneumonia **and** a nodule.
> **(a)** Compute softmax probabilities. What does a softmax model "predict"?
> **(b)** Compute independent sigmoid probabilities, and the prediction with a 0.5 threshold.
> **(c)** Which output layer and loss should this model use, and why?
>
> ---
> **(a)** Softmax: $p \approx [0.613,\ 0.083,\ 0.304]$. Argmax says pneumonia only. The nodule gets 0.30 because softmax forces the three probabilities to share a total of 1, so pneumonia and nodule compete.
>
> **(b)** Sigmoids: $\sigma(1.5) = 0.818$, $\sigma(-0.5) = 0.378$, $\sigma(0.8) = 0.690$. Thresholding at 0.5 predicts **pneumonia and nodule**, matching the report.
>
> **(c)** Multi-label: one sigmoid per finding with binary cross-entropy per class (`nn.BCEWithLogitsLoss`), labels as a binary vector $[1, 0, 1]$. Findings can occur together, so they shouldn't compete for probability. Softmax is only right when exactly one class is true.

> [!example]- Exercise 4 — Regularisation decisions
> **(a)** Two weight vectors both give score 1 on $x = [1,1,1,1]$: $w_a = [1, 0, 0, 0]$ and $w_b = [0.25, 0.25, 0.25, 0.25]$. Which does L2 prefer? Which does L1 prefer?
> **(b)** Training accuracy 99%, validation 61%. Raise or lower $\lambda$?
> **(c)** Training 52%, validation 51%. Raise or lower $\lambda$? Could $\lambda$ alone fix it?
> **(d)** Why search $\lambda$ over $\{10^{-6}, 10^{-5}, \dots, 10^{2}\}$ instead of $\{0, 0.5, 1, 1.5, \dots\}$?
>
> ---
> **(a)** L2: $R(w_a) = 1$, $R(w_b) = 4 \times 0.0625 = 0.25$, so L2 prefers $w_b$ (spread-out weights). L1: $R(w_a) = 1$, $R(w_b) = 4 \times 0.25 = 1$, a tie. L1 doesn't penalise concentration the way L2 does; with other loss terms in play it tends to push weights to exactly zero (sparse solutions like $w_a$).
>
> **(b)** Large train–validation gap = overfitting. **Raise** $\lambda$ (or add other regularisation such as augmentation).
>
> **(c)** Both low and close together = underfitting. **Lower** $\lambda$. But if it's already small, the real problem is that a linear model on raw pixels can't represent the classes (one template per class, linear boundaries only). You need better features or a more expressive model (week 4).
>
> **(d)** The useful values span many orders of magnitude, and the effect of $\lambda$ depends on its order of magnitude, not on small additive changes. A linear grid would spend almost all its points on values that all over-regularise and never test the small values where the optimum often is.

> [!example]- Exercise 5 — Batches, epochs, shapes
> CIFAR-10 has $N = 50{,}000$ training images, $D = 3072$, $C = 10$. You use mini-batches of 128.
> **(a)** How many iterations in one epoch? In 20 epochs?
> **(b)** You increase the batch to 512. By what factor does the standard deviation of the gradient estimate change? What should you consider doing to the learning rate?
> **(c)** Give the shapes of $X_b$, $P - Y$ and $\nabla_W L$ for one batch, and confirm they multiply correctly.
> **(d)** How many multiply-adds does k-NN need to classify one test image (L2 distance, no tricks), and why does that make it impractical?
>
> ---
> **(a)** $50{,}000/128 = 390.6$, so 391 iterations per epoch (the last batch is partial; 390 if you drop it). 20 epochs ≈ 7,820 updates.
>
> **(b)** Variance falls as $1/|B|$, so 4× the batch gives $1/4$ the variance and **half** the standard deviation. With a less noisy gradient you can usually afford a **larger** learning rate; batch size and learning rate need to be tuned together (slide 52).
>
> **(c)** $X_b$: $128 \times 3072$. $P - Y$: $128 \times 10$. $\nabla_W L = \frac{1}{128}(P - Y)^\top X_b$: $(10 \times 128)(128 \times 3072) = 10 \times 3072$, matching $W$.
>
> **(d)** $50{,}000 \times 3072 \approx 1.5 \times 10^8$ per test image, versus $10 \times 3072 = 30{,}720$ for the linear classifier. And it must keep the whole training set in memory. Training is free, but every prediction is expensive: the opposite of what deployment needs.

## 📝 Summary

- **Data-driven classification** = score function + loss + optimiser. Split into train/validation/test; touch the test set once. Cross-validation gives error bars but costs $k$ runs.
- **Accuracy misleads under imbalance**; look at the confusion matrix. ImageNet often uses top-5.
- **k-NN** memorises the data: $O(1)$ training, $O(N)$ prediction. Pixel distance isn't semantic distance, and in high dimensions all distances look alike (curse of dimensionality). Never use it on raw pixels; use it on learned features.
- **Linear classifier** $s = Wx + b$ (CIFAR-10: 30,730 parameters). Three views: algebra, one template per class, hyperplanes. Can't do XOR, rings or multimodal classes.
- **Losses:** hinge $\sum_{j\ne y}\max(0, s_j - s_y + \Delta)$ stops at zero; softmax cross-entropy $-\log p_y$ never does. Binary: sigmoid + BCE. Multi-label: one sigmoid per class + BCE, threshold instead of argmax. Subtract the max before exponentiating; pass logits to `CrossEntropyLoss`.
- **Regularisation:** $W$ isn't unique, so add $\lambda R(W)$. L2 = small, spread-out weights; L1 = sparse. Tune $\lambda$ on validation, on a log scale.
- **Optimisation:** $W \leftarrow W - \eta \nabla_W L$. Softmax gradient $= p - y$, so $\nabla_W L = \frac1N (P-Y)^\top X + 2\lambda W$. Mini-batch gradient descent (32–256) is the practical default; tune batch size and learning rate together.
- **Sanity checks:** initial loss ≈ $\log C$ (softmax) or $C-1$ (hinge); gradient check; overfit 20 examples.

## ⚠️ Important Notes

1. **Never tune on the test set.** Each look-and-adjust leaks information and makes the test score optimistic.
2. **Compute normalisation statistics ($\mu$, $\sigma$) on the training set only**, then apply them unchanged to validation and test.
3. **Loss ≠ accuracy.** Zero hinge loss doesn't mean the model is perfect, and nonzero loss is possible at 100% accuracy.
4. **Softmax probabilities sum to 1; independent sigmoids don't.** Use softmax when exactly one class is true, sigmoids when several can be.
5. **`nn.CrossEntropyLoss` wants raw logits.** Applying softmax first is a silent bug. Same for `BCEWithLogitsLoss`: don't apply a sigmoid first.
6. **Initial loss is a free bug detector**: $\ln C$ for softmax (2.30 at $C = 10$, 6.91 at $C = 1000$), about $C - 1$ for hinge.
7. **The hinge loss gives zero gradient for examples past the margin.** Cross-entropy never fully stops, so regularisation is needed to keep weights from growing forever.
8. **Scaling $W$ changes confidence, not predictions.** Multiplying all scores by 10 makes softmax much more confident without changing the argmax. A softmax output is not automatically a calibrated probability.
9. **L1 gives exact zeros, L2 doesn't.** That's a geometric fact (corners of the L1 diamond), useful for a "which regulariser" question.
10. **Learning rate symptoms:** too small → loss barely moves; slightly too large → plateau at a poor value; far too large → `nan`.
11. **Batch size and learning rate interact.** Changing one usually means re-tuning the other.
12. **"SGD" in PyTorch means mini-batch gradient descent**, not single-example updates.
13. **Shape-check every gradient.** $\nabla_W L$ must have the same shape as $W$.
14. **A linear classifier on raw pixels has one template per class.** It can't handle a class that looks very different from different viewpoints, which is the motivation for neural networks.

> [!warning] Gaps in the source material
> - **Figures lost in extraction:** slide 6 (data-driven pipeline), 12 (MNIST confusion matrix), 16 (k-NN boundaries for $k = 1, 3, 5$), 17 (images with equal L2 distance), 18 (distance-ratio plot), 22/24/25 (score geometry and learned templates), 30 (SVM decision regions), 38 (loss vs margin plot), 41 (L1/L2 constraint regions), 42 (accuracy vs $\lambda$), 44–45 (loss landscape), 52 (optimisation paths), 55 (training loop figure). Each is described from its caption.
> - **All numbers from slide 36 were recomputed** and match (e.g. $\sigma(2.2) = 0.9002$, softmax sum $= 20.05$, multi-label total 0.230).
> - **Added beyond the slides:** the "two-headed horse" description of templates (from CS231n); why initial loss is $\log C$ and $C-1$; the numerical gradient formula; the k-NN operation count; all five exercises and the Important Notes.
> - The 11% / 3.8× path-length figures (slide 52) are from the lecturer's demo and can't be reproduced without its data.

**Previous:** [[02 - Classical Image Processing]] · **Next:** [[04 - From Neural Networks to CNNs]]
