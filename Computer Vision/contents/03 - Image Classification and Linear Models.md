---
subject: Computer Vision
chapter: 3
tags: [ds, computer-vision, classification, knn, linear-classifier, hinge-loss, softmax, regularization, calibration]
source: "Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed. §5.1, §5.3.4, §6.2; Stanford CS231n; the lecturer's course outline (Lecture 01, slide 8)"
---

# Image Classification and Linear Models

**Week 3 of 14. ⚠️ THE FIRST CHAPTER WITHOUT SLIDES** — built from Szeliski, the lecturer's stated second reference (CS231n) and standard practice. See [[00-Index]].

**Five results.**

**§3 — ⚠️ THE CURSE OF DIMENSIONALITY KILLS k-NN ON PIXELS, AND THE NUMBER IS BRUTAL.** At CIFAR-10's **3,072 dimensions the farthest of 1,000 random points is only 6.6% further away than the nearest** (2,575% at $d=1$). **The relative spread falls like $1/\sqrt d$: sd/mean is 0.171 at $d=10$ and 0.0099 at $d=3072$.** ⇒ *"nearest neighbour" stops meaning anything.*

**§2 — ⚠️ k-NN'S COST PROFILE IS EXACTLY BACKWARDS.** Training $O(1)$, prediction $O(ND)$. **Predicting one CIFAR-10 image touches 153.6 million numbers where a linear classifier touches 30,720 — a ratio of $N/K=5{,}000\times$, independent of $D$.** And the whole linear model is **0.02% of the training set it replaces**.

**§5 — ⚠️ "INVERTING AN IMAGE PRESERVES THE CATEGORY" IS A *PROOF* THAT LINEAR-ON-PIXELS IS WRONG, NOT A HINT.** For any $\mathbf w$, $\text{score}(-\mathbf x)=-\text{score}(\mathbf x)$ **exactly**. ⇒ **no weight vector can score an image and its photographic negative highly at once.**

**§7 — ⚠️ THE HINGE LOSS SWITCHES OFF AND THE CROSS-ENTROPY NEVER DOES.** Hinge is **exactly 0** at margin 1 and stays there; cross-entropy decays like $e^{-\text{margin}}$ — $5.51\times10^{-1}$ at margin 1, $9.08\times10^{-5}$ at 10 — **but is never zero.**

**§8 — ⚠️ SCALING $\mathbf W$ MAKES THE MODEL MORE *CONFIDENT* WITHOUT MAKING IT MORE *ACCURATE*.** The same scores at $\times10$ move the softmax entropy from **0.975 nats to 0.0010** and the top probability from 0.576 to **0.9999** — *the prediction never changes.* **This is Szeliski's calibration warning, made numerical.**

## 📘 Main Knowledge

### 1. The task, and the data-driven answer

**Image classification**: assign one label from a fixed set to a whole image. Szeliski: *"semantic image classification, where we wish to label a complete image (or predetermined portion) with its most likely semantic category, e.g., horse, cat, or car… This is the main application for which deep networks were originally developed."*

**There is no algorithm for "cat."** [[01 - Introduction and Image Formation|Ch. 01]] §3's eight variations guarantee that any hand-written rule fails. **The data-driven approach replaces the rule with a dataset**: collect labelled examples, fit a model, predict on unseen inputs.

**Szeliski's framing of supervised learning** is worth keeping exact: pairs $\{\mathbf x_i\}$ and targets $\{t_i\}$ go into a learning algorithm that *"adjusts the model's parameters so as to maximize the agreement between the model's predictions and the target outputs."* Discrete targets → **classification**; continuous → **regression**.

> [!note] ⚠️ Szeliski's warning about the word "test"
> *"This phase is often called the **test phase**, although this sometimes fools people into focusing excessively on performance on a given test set, rather than building a system that works robustly for any plausible inputs that might arise."*
>
> ⇒ *the test set is a proxy for the world, and it is a bad one whenever the world drifts* — which is [[Deep Learning/contents/03 - Logistic Regression|DL ch. 03]] §11's distribution shift.

**What we are actually minimizing** is **expected loss (risk)**; since the true distribution is unknown, we substitute the training distribution — **empirical risk minimization**.

> [!warning] ⚠️ And Szeliski flags the asymmetry immediately
> *"In classification tasks, it is common to minimize the misclassification rate, i.e., penalizing all class prediction errors equally… However, asymmetries often exist. For example, the cost of producing a false negative diagnosis in medicine… is often greater than that of a false positive."*
>
> ⇒ **exactly [[Deep Learning/contents/01 - Introduction to Deep Learning|DL ch. 01]]'s result that `argmax` is optimal only under 0–1 loss.** *Reporting the most likely class silently asserts that every error costs the same.*

### 2. ⚠️ Nearest neighbours, and a cost profile that is backwards

**$k$-NN is non-parametric**: store every training example; at test time find the $k$ nearest and take the majority class. Szeliski: *"the training examples are all retained, and at evaluation time the 'nearest' $k$ neighbors are found and then averaged to produce the output."*

**$k$ is a hyperparameter and it controls the bias–variance trade-off directly:**
- **$k$ too small** → *"the classifier acts in a very random way, i.e., it is overfitting"* — irregular decision surfaces
- **$k$ too large** → *"the classifier underfits (over-smooths)… resulting in the shrinkage of the two smaller regions"*

*(Szeliski notes Cover and Hart (1967) proved 1-NN is **statistically optimal in the large sample limit** — which makes its practical failure below more interesting, not less.)*

**CIFAR-10, the standard testbed:** $32\times32\times3=\mathbf{3{,}072}$ numbers per image, 50,000 train, 10,000 test, 10 classes, **chance accuracy 10%**.

> [!warning] ⚠️ $k$-NN HAS THE COST PROFILE WE DO NOT WANT
> | | training | predicting **one** image |
> |---|---|---|
> | **$k$-NN** | **$O(1)$** — just store | **$O(ND)=153{,}600{,}000$** |
> | **linear classifier** | $O(\text{iters}\cdot ND)$ | **$O(KD)=30{,}720$** |
>
> **Ratio at prediction time: $5{,}000\times$ — and that is exactly $N/K=50{,}000/10$, independent of $D$.**
>
> Classifying the whole CIFAR-10 test set with $k$-NN is $10{,}000\times50{,}000=\mathbf{5\times10^8}$ distance computations, or $\mathbf{1.54\times10^{12}}$ operations.
>
> ⇒ ***we want slow training and fast prediction; $k$-NN gives instant training and unusable prediction.*** **And it must carry the entire training set as its "model": 146.5 MB as `uint8`, 585.9 MB as `float32`.**
>
> **The linear classifier is 30,730 parameters — 0.12 MB, or 0.02% of the training set it replaces.** *That compression is the point of learning.*

### 3. ⚠️ The curse of dimensionality — why $k$-NN on raw pixels cannot work

**In high dimensions every point is about the same distance from every other.** Measured with 1,000 uniform random points and a random query:

| dimension | $d_{\min}$ | $d_{\max}$ | **$(d_{\max}-d_{\min})/d_{\min}$** |
|---|---|---|---|
| 1 | 0.0004 | 0.9865 | **2,574.66** |
| 2 | 0.0168 | 1.1276 | 66.06 |
| 3 | 0.0512 | 1.4556 | 27.45 |
| 10 | 0.4613 | 2.0480 | 3.44 |
| 100 | 3.2049 | 4.7286 | 0.475 |
| 1,000 | 12.0682 | 13.7525 | 0.140 |
| **3,072** (CIFAR-10) | **21.8944** | **23.3309** | **0.0656** |

> [!warning] ⚠️ AT CIFAR-10's DIMENSION THE FARTHEST POINT IS ONLY **6.6%** FURTHER THAN THE NEAREST
> **The mechanism**: for roughly independent coordinates the mean distance grows like $\sqrt d$ while the *spread* stays $O(1)$, so the relative contrast vanishes like $1/\sqrt d$:
>
> | dimension | mean distance | sd | **sd/mean** |
> |---|---|---|---|
> | 10 | 1.4436 | 0.2475 | **0.1714** |
> | 100 | 4.1021 | 0.2277 | 0.0555 |
> | 1,000 | 13.0222 | 0.2271 | 0.0174 |
> | **3,072** | **22.5968** | **0.2238** | **0.0099** |
>
> **The standard deviation is essentially constant at 0.22 while the mean grows 15×.**
>
> ⇒ ***"nearest neighbour" stops meaning anything*** — the nearest neighbour is nearest by a margin comparable to the numerical noise, so it is chosen by accident rather than by similarity. **This is why $k$-NN on raw CIFAR-10 pixels reaches only the high thirties in accuracy despite Cover and Hart's optimality theorem: the theorem needs samples dense in the space, and no achievable $N$ is dense in $\mathbb R^{3072}$.**
>
> **The fix is not more data — it is fewer, better dimensions.** *That is what every method from [[04 - From Neural Networks to CNNs|ch. 04]] onward does: learn a representation in which distance means something.*

> [!note] ⚠️ Szeliski's preprocessing advice matters here for a related reason
> *"It is usually a good idea to **center, standardize**, and if possible, **whiten** the input data."* Centering subtracts the mean; standardizing rescales each component to unit variance; whitening decorrelates via the covariance SVD.
>
> **And his footnote is the point:** *"the reason I put 'nearest' in quotations is that standardizing and/or whitening the data will affect distances between vectors."* ⇒ ***there is no such thing as "the" distance between two images — it depends on a preprocessing choice you made.*** *(He also notes whitening is prohibitive for large image sets — see [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]] for the SVD.)*

### 4. ⚠️ L1 versus L2 — and pixels have no privileged axes

| | |
|---|---|
| **L1 (Manhattan)** | $\sum_p\lvert I_1^p-I_2^p\rvert$ |
| **L2 (Euclidean)** | $\sqrt{\sum_p(I_1^p-I_2^p)^2}$ |

> [!warning] ⚠️ L2 is rotation-invariant; L1 is not — verified over 2,000 random rotations
> Two fixed vectors in $\mathbb R^8$, distance measured after a random orthogonal $\mathbf Q$:
>
> | | min | max | **spread** |
> |---|---|---|---|
> | **L2** | 2.980753 | 2.980753 | $\mathbf{2.2\times10^{-15}}$ |
> | **L1** | 4.537625 | 8.275444 | **3.7378 — 54.0% of the mean** |
>
> **L2 is invariant to machine precision. L1 varies by more than half its own value depending on the coordinate frame.**
>
> ⇒ **L1 depends on the axes; for pixels there is no privileged frame.** Rotating the image, or changing colour space ([[01 - Introduction and Image Formation|ch. 01]] §8), **changes L1 distances and leaves L2 alone.**
>
> *This does not make L1 wrong — it makes it a statement that the coordinate axes are meaningful, which is true for tabular features and false for pixels. **Choose L1 when the axes mean something and L2 when they do not.***

### 5. ⚠️ The linear classifier, and a proof that it cannot work on pixels

$$\boxed{f(\mathbf x;\mathbf W,\mathbf b)=\mathbf W\mathbf x+\mathbf b},\qquad \mathbf W\in\mathbb R^{K\times D},\ \mathbf b\in\mathbb R^{K}$$

For CIFAR-10 that is $10\times3072+10=\mathbf{30{,}730}$ parameters. **Three readings of the same equation:**

| reading | |
|---|---|
| **algebraic** | $K$ inner products; **row $k$ of $\mathbf W$ is a template** and the score is its correlation with the image |
| **geometric** | $K$ hyperplanes in $\mathbb R^{3072}$; each row is a normal vector, each bias an offset |
| **template matching** | reshape row $k$ back to $32\times32\times3$ and **look at it** — it is a blurry average of that class |

> [!warning] ⚠️ ONE TEMPLATE PER CLASS IS A HARD LIMIT, AND THE NEGATIVE-IMAGE ARGUMENT PROVES IT
> For **any** weight vector $\mathbf w$:
> $$\text{score}(-\mathbf x)=\mathbf w^\top(-\mathbf x)=-\mathbf w^\top\mathbf x=-\text{score}(\mathbf x)$$
> **Verified: $+$ and $-$ of exactly the same magnitude, for every $\mathbf w$.**
>
> ⇒ **no linear model can give a high score to an image *and* its photographic negative.** [[01 - Introduction and Image Formation|Ch. 01]] §1's *"inverting an image preserves the category"* is therefore **a proof that linear-on-pixels is the wrong model class**, not merely a hint.
>
> **And translation breaks it just as completely.** Shifting a $2\times2$ blob across an $8\times8$ image and scoring with a fixed random $\mathbf w$:
>
> | shift (px) | score |
> |---|---|
> | 0 | $+1.0937$ |
> | 1 | $+0.9709$ |
> | 2 | $-0.1938$ |
> | 3 | $-1.0750$ |
>
> **Four shifts of the same object, four unrelated scores — including a sign flip.** ⇒ ***a linear classifier on pixels is invariant to none of [[01 - Introduction and Image Formation|ch. 01]] §3's eight variations.*** **This is precisely what convolution fixes** ([[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §1), and why [[04 - From Neural Networks to CNNs|ch. 04]] exists.

### 6. The protocol: train / validation / test

| split | used for | seen how often |
|---|---|---|
| **train** | fitting parameters | constantly |
| **validation** | choosing hyperparameters ($k$, $\lambda$, learning rate, architecture) | many times |
| **test** | **one** final estimate of generalization | **once** |

**Cross-validation** ($k$-fold) replaces a single validation split when data is scarce — average performance over $k$ rotations of which fold is held out.

> [!warning] ⚠️ Every look at the test set spends some of it
> Choosing a hyperparameter on the test set makes that set a *training* set for the hyperparameter, and its estimate optimistic. **[[Deep Learning/contents/03 - Logistic Regression|DL ch. 03]] §10 quantified the honest version: a 10,000-example test set has a two-standard-deviation interval about 1% wide**, so *"thousands of applied deep learning papers get published every year making a big deal out of error rate improvements of 0.01 or less."*
>
> ⇒ **an improvement smaller than the interval is not an improvement**, and **repeated test-set use is adaptive overfitting** even when nobody trains on it.

### 7. ⚠️ Two loss functions, and only one of them keeps learning

**Multiclass SVM (hinge)**: $L_i=\sum_{j\ne y_i}\max\big(0,\ s_j-s_{y_i}+\Delta\big)$, typically $\Delta=1$.

**Softmax (cross-entropy)**: $L_i=-\log\dfrac{e^{s_{y_i}}}{\sum_j e^{s_j}}$.

*(Szeliski writes the second as $E_n(\mathbf w)=\log Z_n - s_{nt_n}$ with $Z_n=\sum_j e^{s_{nj}}$ — the same thing, and the form that makes the numerics obvious.)*

| scores (correct class first) | hinge | cross-entropy |
|---|---|---|
| $[10,-10,-10]$ | 0.000000 | $\approx0$ |
| $[10,9,9]$ — margin 1 | **0.000000** | **0.551445** |
| $[10,-2,-2]$ — margin 12 | 0.000000 | 0.000012 |
| $[1,2,3]$ — **wrong** | 5.000000 | 2.407606 |

> [!warning] ⚠️ THE HINGE SWITCHES OFF; THE CROSS-ENTROPY NEVER DOES
> | margin | hinge | cross-entropy |
> |---|---|---|
> | 1 | **0.000000** | $5.514\times10^{-1}$ |
> | 2 | 0.000000 | $2.395\times10^{-1}$ |
> | 5 | 0.000000 | $1.339\times10^{-2}$ |
> | 10 | 0.000000 | $9.080\times10^{-5}$ |
> | 20 | 0.000000 | $4.122\times10^{-9}$ |
>
> **Once every margin exceeds $\Delta$, the hinge is *exactly* zero and those examples contribute *no gradient at all*.** The cross-entropy decays like $e^{-\text{margin}}$ and **never reaches zero**, so every example keeps pushing forever.
>
> ⇒ **with the hinge, a model that separates the data stops learning; with cross-entropy it keeps growing margins indefinitely** — which is why the softmax is the default, and why §8's regularization is not optional.
>
> ⚠️ **A "read what the code prints" catch**: at margin 50 my implementation printed `-0.000000` for the cross-entropy. **That is signed-zero underflow, not zero** — the true value is $\approx e^{-50}\approx2\times10^{-22}$. *A printed zero in a log-domain quantity usually means underflow; check before concluding the loss is satisfied.*

### 8. ⚠️ Regularization — and the confidence trap

> [!warning] ⚠️ WITHOUT REGULARIZATION THE LOSS DOES NOT DETERMINE $\mathbf W$'s MAGNITUDE
> Scores $[10,9,9]$ give hinge 0. **Scaling $\mathbf W$ by 2, 10, 100 gives $[20,18,18]$, $[100,90,90]$, $[1000,900,900]$ — hinge 0 every time.**
>
> ⇒ **the data loss alone is scale-blind once the margins are met: an entire ray of solutions $\{\alpha\mathbf W:\alpha\ge1\}$ is equally optimal.** $\lambda\|\mathbf W\|^2$ is what makes the problem well-posed and picks the smallest one — which is also the one with the widest margin.

> [!warning] ⚠️ AND FOR THE SOFTMAX THE SAME SCALING IS A TEMPERATURE — CONFIDENCE WITHOUT ACCURACY
> Same scores $[10,9,9]$, scaled:
>
> | scale | probabilities | max | **entropy (nats)** |
> |---|---|---|---|
> | 0.5 | $[0.452,0.274,0.274]$ | 0.4519 | 1.0684 |
> | **1** | $[0.576,0.212,0.212]$ | 0.5761 | **0.9753** |
> | 2 | $[0.787,0.107,0.107]$ | 0.7870 | 0.6656 |
> | **10** | $[0.9999,0,0]$ | **0.9999** | **0.0010** |
>
> **The `argmax` never changes. The accuracy never changes. The reported confidence goes from 57.6% to 99.99%.**
>
> ⇒ ***scaling $\mathbf W$ makes a model more confident without making it more accurate*** — which is exactly Szeliski's warning: *"the training losses… only encourage the network to maximize the probability-weighted correct answers, and do not, in fact, encourage the network outputs to be properly **confidence calibrated**"* (Guo, Pleiss et al. 2017). **His suggested fix — dividing the logits by a temperature — is literally undoing this scaling.**
>
> **⚠️ So a softmax output is a score, not a probability, until someone calibrates it.** *Reporting "the model was 99% sure" without calibration is reporting the norm of $\mathbf W$.*

### 9. Where this leads

Szeliski's §6.2 splits image classification into **feature-based methods** (bag of visual words over SIFT — [[02 - Classical Image Processing|ch. 02]] §10) and **deep networks**, and the whole history is the replacement of the first by the second.

**The pipeline this chapter establishes survives intact into every later chapter:** a **score function** $f(\mathbf x;\mathbf W)$, a **loss** measuring disagreement with labels, a **regularizer**, and **optimization** by gradient descent ([[Deep Learning/contents/04 - Neural Network|DL ch. 04]]). **From [[04 - From Neural Networks to CNNs|ch. 04]] on, only $f$ changes.**

## ✏️ Exercises

> [!example]- Exercise 1 — cost out $k$-NN
> CIFAR-10: 50,000 train, 10,000 test, $32\times32\times3$, 10 classes.
> **(a)** Numbers per image; training set size in MB. **(b)** Cost of predicting one image with $k$-NN vs a linear classifier. **(c)** The whole test set. **(d)** Why is this the wrong way round?
>
> ---
> **(a)** $32\cdot32\cdot3=\mathbf{3{,}072}$. Training set: $50{,}000\times3{,}072=153{,}600{,}000$ bytes $=\mathbf{146.5}$ MB as `uint8`, **585.9 MB** as `float32`.
>
> **(b)** $k$-NN: $O(ND)=50{,}000\times3{,}072=\mathbf{153{,}600{,}000}$ operations. Linear: $O(KD)=10\times3{,}072=\mathbf{30{,}720}$. **Ratio $\mathbf{5{,}000\times}$** — and note it equals $N/K$ exactly, so **it does not improve with smaller images.**
>
> **(c)** $10{,}000\times50{,}000=5\times10^8$ distances $\times\,3{,}072=\mathbf{1.54\times10^{12}}$ operations.
>
> **(d)** ⚠️ **A model is trained once and deployed millions of times.** $k$-NN puts all its cost where it is repeated and none where it is amortized — and it must ship the entire training set as its parameters. **The linear model is 30,730 numbers: 0.02% of the data it replaces.** *Learning is compression.*

> [!example]- Exercise 2 — the curse of dimensionality
> **(a)** For $n=1000$ uniform points, measure $(d_{\max}-d_{\min})/d_{\min}$ at $d=1,10,100,3072$. **(b)** What happens to the mean and spread separately? **(c)** What does this mean for $k$-NN on pixels? **(d)** Reconcile with Cover & Hart's optimality theorem.
>
> ---
> **(a)** **2,574.66 / 3.44 / 0.475 / 0.0656.** At CIFAR-10's dimension the farthest point is only **6.6%** further than the nearest.
>
> **(b)** ⚠️ **The mean grows like $\sqrt d$ (1.44 → 22.60, a 15.7× rise) while the standard deviation stays essentially constant (0.2475 → 0.2238).** So sd/mean falls **0.1714 → 0.0099**, i.e. like $1/\sqrt d$.
>
> **(c)** **The "nearest" neighbour is nearest by a margin comparable to noise**, so it is selected by accident rather than similarity. Distances stop discriminating.
>
> **(d)** ⚠️ **Cover & Hart requires the sample to become dense in the space.** Density in $\mathbb R^{3072}$ needs a number of samples exponential in $d$ — **no achievable $N$ comes close.** *The theorem is true and vacuous here: it describes a limit no dataset can approach.* **The fix is fewer, better dimensions — a learned representation — not more data.**

> [!example]- Exercise 3 — L1 versus L2
> **(a)** Are they invariant to rotation? Test empirically. **(b)** Which should you use for pixels? **(c)** Does the choice change anything else?
>
> ---
> **(a)** Over 2,000 random orthogonal $\mathbf Q$ applied to two fixed vectors: **L2 spread $2.2\times10^{-15}$ (machine precision); L1 spread 3.7378, which is 54.0% of its own mean.** **L2 invariant, L1 not.**
>
> **(b)** ⚠️ **L2 for pixels**, because the pixel axes carry no special meaning — rotating the image or changing colour space is exactly a change of frame, and L1 answers differently for each. **L1 is the right choice when the axes *do* mean something** (tabular features with individual units), where its robustness to single-coordinate outliers is an advantage.
>
> **(c)** Yes — **Szeliski's footnote**: standardizing or whitening also changes distances. ⇒ ***"the distance between two images" is not a property of the images; it is a property of your preprocessing.*** Report both.

> [!example]- Exercise 4 — why a linear classifier fails on pixels
> **(a)** Show that no $\mathbf w$ scores both $\mathbf x$ and $-\mathbf x$ highly. **(b)** What does that say about ch. 01's inversion remark? **(c)** Score a shifted object. **(d)** How many of the eight variations does a linear model handle?
>
> ---
> **(a)** $\mathbf w^\top(-\mathbf x)=-\mathbf w^\top\mathbf x$ — **the scores are exact negatives, identically in $\mathbf w$.** If one is $+s$ the other is $-s$; they cannot both be large.
>
> **(b)** ⚠️ **It upgrades the remark from an intuition to a theorem.** "Inverting an image preserves the category" plus "the linear score negates under inversion" **proves** the model class is wrong — no amount of data or training fixes it.
>
> **(c)** A $2\times2$ blob shifted 0–3 px, fixed random $\mathbf w$: $+1.0937,\ +0.9709,\ -0.1938,\ -1.0750$. **Four views of one object, four unrelated scores, including a sign flip.**
>
> **(d)** ⚠️ **None.** Viewpoint, illumination, scale, deformation, occlusion, clutter, intra-class variation and context all change the pixel vector arbitrarily, and the score is a fixed inner product. **A linear model on raw pixels has exactly one template per class and no invariance whatsoever** — which is the entire argument for [[04 - From Neural Networks to CNNs|ch. 04]].

> [!example]- Exercise 5 — losses, scale, and confidence
> **(a)** Compute hinge and cross-entropy for $[10,9,9]$ and $[1,2,3]$ (correct class 0). **(b)** What happens to each as the margin grows? **(c)** Scale $\mathbf W$ by 10 — what changes? **(d)** What does that imply about reported confidence?
>
> ---
> **(a)** $[10,9,9]$: hinge $\max(0,9-10+1)\times2=\mathbf 0$; cross-entropy $\mathbf{0.5514}$. $[1,2,3]$: hinge $(2-1+1)+(3-1+1)=\mathbf 5$; cross-entropy $\mathbf{2.4076}$.
>
> **(b)** **Hinge: exactly 0 from margin 1 onward — no gradient, the example is ignored.** Cross-entropy: $0.551\to9.08\times10^{-5}$ at margin 10 $\to4.12\times10^{-9}$ at margin 20 — **decaying like $e^{-\text{margin}}$ and never zero.** ⚠️ *A printed `-0.000000` at large margin is underflow, not zero.*
>
> **(c)** **Hinge: nothing — still 0** at every scale (verified at $\times2,\times10,\times100$). **Softmax: the top probability goes 0.5761 → 0.9999 and the entropy 0.9753 → 0.0010 nats.** The `argmax`, and therefore the accuracy, is **unchanged**.
>
> **(d)** ⚠️ ***Reported confidence is a function of $\|\mathbf W\|$, not of correctness.*** A model can be made to look certain by scaling its weights. **Szeliski's point exactly**: the losses *"do not, in fact, encourage the network outputs to be properly confidence calibrated,"* and temperature scaling is the standard repair. ⇒ **treat a softmax output as a score until someone calibrates it.**

## 📝 Summary

- **Image classification is data-driven because no rule survives [[01 - Introduction and Image Formation|ch. 01]]'s eight variations.** We minimize **empirical risk** as a proxy for true risk — and **penalizing all errors equally is an assumption**, not a default.
- **⚠️ $k$-NN's cost profile is backwards**: $O(1)$ training, $O(ND)$ prediction. **153,600,000 operations per CIFAR-10 image vs 30,720 for a linear model — $5{,}000\times$, and that ratio is $N/K$, independent of image size.** The whole test set is $1.54\times10^{12}$ operations, and the "model" is the 146.5 MB dataset.
- **⚠️ The curse of dimensionality kills it anyway**: at $d=3072$ the farthest of 1,000 points is **6.6%** further than the nearest, against 2,575% at $d=1$. **The mean distance grows like $\sqrt d$ while the spread stays constant at ≈0.22**, so sd/mean falls 0.1714 → 0.0099. **Cover & Hart's optimality needs density no achievable $N$ provides.**
- **⚠️ L2 is rotation-invariant to machine precision; L1 varies by 54% of its own mean** under rotation. **Pixels have no privileged axes, so use L2** — and remember Szeliski's footnote that **standardizing or whitening changes distances too**.
- **A linear classifier is $\mathbf W\mathbf x+\mathbf b$ — 30,730 parameters for CIFAR-10 — readable as templates, hyperplanes, or inner products.**
- **⚠️ It cannot work on pixels, and that is provable**: $\text{score}(-\mathbf x)=-\text{score}(\mathbf x)$ **identically**, so no weight vector handles an image and its negative. **Shifting one object 0–3 px gave $+1.09,+0.97,-0.19,-1.08$.** ⇒ **one template per class, zero invariances.**
- **Train / validation / test, and the test set once.** DL ch. 03's arithmetic: a 10,000-example test set has a ≈1%-wide interval, so **sub-1% improvements are noise**, and repeated use is adaptive overfitting.
- **⚠️ The hinge loss switches off at margin 1 (exactly 0, no gradient); cross-entropy decays like $e^{-\text{margin}}$ and never does** — $0.551$ at margin 1, $9.08\times10^{-5}$ at 10. **That is why softmax is the default.**
- **⚠️ Without regularization the loss does not determine $\|\mathbf W\|$**: scaling by 2, 10, 100 leaves the hinge at 0. **And for the softmax the same scaling is a temperature — top probability 0.576 → 0.9999, entropy 0.975 → 0.001 nats, with the prediction unchanged.** ⇒ **confidence is a function of $\|\mathbf W\|$, not of correctness** — Szeliski's calibration warning, made numerical.
- **The pipeline established here — score function, loss, regularizer, optimizer — survives every later chapter. From [[04 - From Neural Networks to CNNs|ch. 04]] on, only $f$ changes.**

## ⚠️ Important Notes

1. **⚠️ A softmax output is not a probability until it is calibrated.** Szeliski and Guo et al. (2017) are explicit: the training loss does not encourage calibration. **Temperature-scale on a validation set before reporting confidence, and never quote "the model was 99% sure" from raw logits.**
2. **⚠️ Distances between images depend on preprocessing.** Centering, standardizing, whitening and colour-space choice all change them — L1 more than L2. **State the preprocessing whenever you state a distance.**
3. **⚠️ The hinge loss ignores examples it already gets right.** If you use it, a separable training set produces zero gradient and training halts with an arbitrary margin. **Check whether your loss is still non-zero before concluding the model has converged.**
4. **⚠️ A printed loss of `0.000000` in the log domain is usually underflow.** Verified here at margin 50. **Check in log space, not in the printed decimal.**
5. **⚠️ Never tune on the test set.** Every hyperparameter chosen there converts it into training data. **And an improvement below ≈1% on a 10,000-example test set is inside the confidence interval** ([[Deep Learning/contents/03 - Logistic Regression|DL ch. 03]] §10).
6. **⚠️ $k$-NN's accuracy is not the reason to reject it — its cost profile and the curse of dimensionality are.** It remains genuinely useful for **large-scale matching and indexing** (Szeliski's own note) where the features are learned and low-dimensional.
7. **⚠️ Chance is 10% on CIFAR-10 and 0.1% on ImageNet-1k.** *"Beats chance" is meaningless without the class count*, and accuracy on an imbalanced set is meaningless full stop.
8. **⚠️ Equal error costs are an assumption you are making silently.** Szeliski's medical example — a false negative costs more than a false positive — generalizes: **state the cost matrix, or admit you assumed 0–1 loss** ([[Deep Learning/contents/01 - Introduction to Deep Learning|DL ch. 01]]).
9. **⚠️ $k$ too small overfits, $k$ too large oversmooths, and the optimum is data-dependent.** Choose it by cross-validation on the validation set — never on the test set, and never by eye on the decision boundary.
10. **The linear classifier is not useless — it is the last layer of nearly every network in this course.** What fails is applying it to **raw pixels**. Given good features it is fast, interpretable and hard to beat, which is exactly how [[02 - Classical Image Processing|ch. 02]]'s HOG + SVM detector worked.
11. **Learning is compression**: 146.5 MB of training data becomes 30,730 parameters (0.02%). **A model that does not compress is a lookup table** — and $k$-NN is exactly that.

> [!warning] Gaps in the source material
> **⚠️ THIS IS THE FIRST CHAPTER WITH NO LECTURE SLIDES.** Weeks 1–2 are the only ones the lecturer supplied ([[00-Index]]). This chapter is built from **Szeliski 2nd ed. §5.1 (supervised learning, nearest neighbours, preprocessing), §5.3.4 (loss functions, calibration) and §6.2 (image classification)** — all of which extract cleanly — plus **Stanford CS231n**, which the lecturer names as the course's second reference, and standard practice.
>
> **⚠️ Consequently the emphasis here is inferred, not given.** The topic title — *"Image classification & linear models"* — is the lecturer's; the choice to build it around $k$-NN, the curse of dimensionality, the linear classifier and the hinge/softmax comparison follows CS231n's canonical treatment of that title. **Where this course's week 3 differs, this chapter will be wrong about emphasis, not about content.**
>
> **Szeliski's PDF extracts unusually well** — clean prose, headers and page numbers, 1,232 pages, **book page = PDF page − 26** (verified twice). Recorded in this subject's `CLAUDE.md`. **Figures are images and never extract**: Figure 5.4 (the $k=1,9,25$ nearest-neighbour example) and Figure 5.5 (decision boundaries as $k$ varies from 1 to 50) are **lost**, though the prose states their content — *"when $k$ is too small, the classifier acts in a very random way… as $k$ gets larger, the classifier underfits"* — which is what §2 records.
>
> **Added beyond the sources, and labelled as mine throughout:**
> - **The whole of §3's curse-of-dimensionality measurement** — the $(d_{\max}-d_{\min})/d_{\min}$ table down to CIFAR-10's 3,072 dimensions, and the separation of the $\sqrt d$ mean growth from the constant spread. **Szeliski mentions neither; CS231n asserts the phenomenon without measuring it.** The reconciliation with Cover & Hart is also mine.
> - **§2's cost table**, the $5{,}000\times$ ratio and its identity with $N/K$, and the "learning is compression" figure of 0.02%.
> - **§4's rotation experiment** (2,000 random orthogonal matrices; L2 spread $2.2\times10^{-15}$ vs L1's 54%). **Szeliski's footnote observes that preprocessing changes distances; the rotation asymmetry between L1 and L2 is an addition.**
> - **§5's negative-image proof** and the shifted-blob scores. **CS231n shows learned templates; the proof that no $\mathbf w$ can handle $\mathbf x$ and $-\mathbf x$, and its identification with ch. 01's inversion remark, are mine.**
> - **§7's margin table** showing the hinge at exactly 0 and cross-entropy decaying like $e^{-\text{margin}}$, and **the underflow catch** at margin 50.
> - **§8's scaling experiment** — hinge invariant, softmax entropy 0.975 → 0.001 nats — **which turns Szeliski's qualitative calibration warning into a measurement.**
> - **All eleven Important Notes.**
>
> **No discrepancies found.** Every figure taken from Szeliski (the supervised-learning framing, the $k$-NN behaviour, the cross-entropy form $E_n=\log Z_n-s_{nt_n}$, the calibration warning) is qualitative and was reproduced faithfully; every quantitative claim in this chapter is my own computation.
>
> **Deliberately deferred, not omitted:** **Szeliski §5.1.2 (Bayesian classification), §5.1.4 (SVMs in their kernel form) and §5.1.5 (decision trees and forests)** are classical learners that the vault's [[Machine Learning/contents/00-Index|Machine Learning]] and [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] subjects own; only the **linear** SVM's hinge loss is developed here, because that is what a linear image classifier uses. **§5.2 (unsupervised learning, PCA, manifold learning)** belongs to week 12's [[12 - Self-Supervised Learning|self-supervised learning]]. **Optimization by gradient descent is stated and not developed** — [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] owns it entirely, including the optimizer family through Adam. **Bag-of-visual-words (Szeliski §6.2.1)** is treated in [[02 - Classical Image Processing|ch. 02]] §10 via SIFT and HOG.
>
> **Left as the source states it:** Cover and Hart's (1967) large-sample optimality theorem; Guo, Pleiss et al.'s (2017) calibration results; Szeliski's citations to Bishop (2006), Hastie et al. (2009), Murphy (2012) and Glassner (2018); and the claim that whitening is "prohibitively expensive for large sets of images," which is plausible and untested here.

**Previous:** [[02 - Classical Image Processing]] · **Next:** [[04 - From Neural Networks to CNNs]]
