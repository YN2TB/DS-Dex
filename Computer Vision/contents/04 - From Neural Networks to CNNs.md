---
subject: Computer Vision
chapter: 4
tags: [ds, computer-vision, mlp, convolution, permutation-invariance, weight-sharing, inductive-bias]
source: "Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed. §5.3–5.4; Stanford CS231n; the lecturer's course outline (Lecture 01, slide 8)"
---

# From Neural Networks to CNNs

**Week 4 of 14. ⚠️ NO SLIDES** — see [[00-Index]].

> [!warning] ⚠️ THIS IS A CROSS-REFERENCE CHAPTER — read the Deep Learning notes for the machinery
> **[[00-Index]]'s boundary rule applies here.** [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] owns the MLP, backpropagation, initialization, dropout and the optimizer family; **[[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] owns convolution, padding, stride, channels, pooling and receptive fields** — in far more depth than a week-4 lecture can reach.
>
> **This note does one thing those do not: it states the *vision* argument for why the transition is forced, and measures it on real image sizes.** Everything else is a link.

**Three results.**

**§2 — ⚠️ AN MLP CANNOT SEE SPATIAL STRUCTURE **AT ALL**, AND THAT IS A THEOREM, NOT A WEAKNESS.** $(\mathbf W_{[:,\pi]})(\mathbf x_\pi)=\mathbf W\mathbf x$ **exactly** — verified to $1.07\times10^{-14}$ over 200 random permutations. ⇒ **shuffle every pixel of every image with one fixed permutation and an MLP learns the identical function at the identical accuracy.** The same shuffle makes a convolution's output **unrelated** ($\|\Delta\|_F=17.38$).

**§1 — ⚠️ ONE FULLY CONNECTED LAYER ON AN IMAGENET IMAGE IS 2.30 GB.** $224\times224\times3\to4096$ is **616,566,784 parameters** — and by [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5, **9.19 GB to train with Adam.** The same first layer as a convolution is **1,792 parameters — 344,066× fewer.**

**§3 — ⚠️ THE MLP'S REAL COST IS DATA, NOT MEMORY.** To be translation-invariant it must learn the same feature **49,284 separate times** on a $224\times224$ image. **A convolution learns it once and reuses it — which is why the data requirement, not the parameter count, is the binding constraint.**

## 📘 Main Knowledge

### 1. The parameter explosion, at sizes that matter

[[03 - Image Classification and Linear Models|Ch. 03]] ended with a linear model that has **one template per class and no invariances**. The obvious repair is hidden layers — an MLP has $H$ templates, and by [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §3 a single hidden layer is a universal approximator.

**It does not survive contact with an image.**

| input | numbers | $H$ | parameters | fp32 |
|---|---|---|---|---|
| CIFAR-10 $32^2\times3$ | 3,072 | 1,000 | 3,073,000 | 11.72 MB |
| CIFAR-10 $32^2\times3$ | 3,072 | 4,096 | 12,587,008 | 48.02 MB |
| **ImageNet $224^2\times3$** | 150,528 | 1,000 | 150,529,000 | 574.22 MB |
| **ImageNet $224^2\times3$** | **150,528** | **4,096** | **616,566,784** | **2.30 GB** |
| 1 megapixel | 3,000,000 | 1,000 | 3,000,001,000 | 11.18 GB |
| 4K frame | 24,883,200 | 1,000 | 24,883,201,000 | **92.70 GB** |

> [!warning] ⚠️ AND THAT IS **ONE LAYER**
> The ImageNet → 4096 layer is **2.30 GB of weights**, and [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5's accounting says training it with Adam needs **four copies — 9.19 GB** — before a single activation is stored.
>
> **The same first layer as a convolution** (64 filters, $3\times3$, 3 input channels) is $64\cdot3\cdot9+64=\mathbf{1{,}792}$ parameters.
>
> $$\textbf{344,066}\times\textbf{ fewer.}$$
>
> *(This is [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §8's weight-sharing ratio — 23,671× for LeNet's first layer — recomputed at ImageNet scale, where it is an order of magnitude larger still.)*

### 2. ⚠️ The real objection is not size — an MLP cannot see structure at all

The memory argument is the one usually given, and it is the weaker one. **The decisive objection is that an MLP has no access to the arrangement of the pixels.**

An MLP's first layer is $\mathbf h=\phi(\mathbf W\mathbf x+\mathbf b)$. Let $\pi$ be any fixed permutation of the $D$ input coordinates. Then

$$\big(\mathbf W_{[:,\pi]}\big)\big(\mathbf x_\pi\big)=\mathbf W\mathbf x$$

> [!warning] ⚠️ VERIFIED EXACTLY — worst deviation $1.07\times10^{-14}$ over 200 random $(\mathbf W,\mathbf x,\pi)$
> ⇒ **for every permutation there is a relabelled weight matrix computing precisely the same function.**
>
> **So: take CIFAR-10, shuffle all 3,072 pixels of every image with ONE fixed random permutation, and train an MLP. It reaches exactly the same accuracy as on the unshuffled data** — the permutation is absorbed into the first layer's columns.
>
> **The images become unrecognizable to a human. The MLP does not notice.**
>
> ⇒ ***an MLP treats an image as an unordered bag of 3,072 numbers.*** Every one of [[01 - Introduction and Image Formation|ch. 01]] §3's eight variations is about *spatial* structure, and the model never sees any.

**The same test on a convolution:**

| | max response | nonzero responses | |
|---|---|---|---|
| coherent image | 4.00 | 24 | **two clean vertical edges** |
| shuffled image | 4.00 | 44 | **scattered at random** |

$$\|\text{conv}(I)-\text{conv}(I_\pi)\|_F=\mathbf{17.38}$$

> [!warning] ⚠️ THE MLP'S OUTPUT IS **IDENTICAL** ($10^{-14}$); THE CONVOLUTION'S IS **UNRELATED**
> ***That difference is the entire content of this chapter.*** A convolution's output changes under a pixel shuffle **because it uses the arrangement** — locality is not an efficiency trick, it is the mechanism by which spatial structure enters the model at all.
>
> **And this is the sharpest available statement of "inductive bias":** the MLP's hypothesis class is invariant to a symmetry the *problem does not have*, and the convolution's is not. *[[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §1 puts the same point as "all learning depends on imposing inductive bias… if those biases do not agree with reality, our models might struggle even to fit our training data."*

### 3. ⚠️ What the MLP would have to learn instead — and why data is the real cost

Suppose we wanted an MLP to be translation-invariant anyway. **It would have to learn the same feature independently at every position:**

| image | pattern | positions = **copies to learn** |
|---|---|---|
| $32\times32$ | $3\times3$ | 900 |
| $32\times32$ | $5\times5$ | 784 |
| **$224\times224$** | **$3\times3$** | **49,284** |
| $224\times224$ | $5\times5$ | 48,400 |

> [!warning] ⚠️ A convolution learns **one** copy and reuses it at all 49,284 positions
> **And the cost of not doing so is data, not memory**: learning $N$ independent copies of a feature requires roughly $N$ times the examples — an edge detector at the top-left corner learns nothing from an edge at the centre.
>
> ⇒ ***the binding constraint is sample efficiency.*** Even with unlimited memory, an MLP would need on the order of $10^4$–$10^5$ times more labelled images to discover translation invariance from data — and [[01 - Introduction and Image Formation|ch. 01]] §2's argument says evolution had 540 million years and we do not.
>
> *This is [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §17's inversion from the other side: a conv weight does $h\cdot w$ times more **work** per parameter than an fc weight — the same reuse, counted in FLOPs instead of in examples.*

### 4. The two assumptions, instantiated at CIFAR-10 scale

[[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §1 derives the convolution by imposing **translation invariance** and **locality** on the fully connected layer, and measures the payoff at $10^{10}$ for a $1000\times1000$ image. **At CIFAR-10's size:**

| | parameters | reduction |
|---|---|---|
| full fourth-order tensor | 1,048,576 | — |
| + translation invariance | 4,096 | **256×** |
| + locality ($5\times5$) | **16** | **256×** |
| **total** | | **65,536×** |

> [!note] ⚠️ The reduction **grows with image size** — which is why the argument matters more for photographs than for thumbnails
> | image | full tensor | after both | ratio |
> |---|---|---|---|
> | $32\times32$ | $1.05\times10^6$ | 16 | $6.6\times10^4$ |
> | $224\times224$ | $2.52\times10^9$ | 16 | $1.6\times10^8$ |
> | $1000\times1000$ | $1.00\times10^{12}$ | 16 | $6.2\times10^{10}$ |
>
> ⇒ *CIFAR-10 understates the case by six orders of magnitude relative to a real photograph.* **Benchmarks on thumbnails systematically flatter architectures that scale badly.**

**Everything after this point — cross-correlation, padding, stride, channels, pooling, receptive fields, and the whole LeNet→DenseNet progression — is [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]], and it is not repeated here.** The one thing worth carrying forward is that **[[02 - Classical Image Processing|ch. 02]] proved the same operator from the opposite direction**: *linear + shift-invariant ⇒ the operation **is** a convolution, there is no other choice.*

> [!note] ⚠️ Three routes to one operator, and the vault has now walked all three
> | route | source | conclusion |
> |---|---|---|
> | **impose invariance on an MLP** | [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §1 | convolution, $10^{10}$ parameters saved |
> | **assume linearity + shift-invariance** | [[02 - Classical Image Processing|ch. 02]] §3 | convolution, forced by theorem |
> | **observe that an MLP is permutation-invariant** | §2 here | convolution, because nothing else uses arrangement |
>
> ***Three independent arguments converging on one operator is why the convolution is not a design choice.***

## ✏️ Exercises

> [!example]- Exercise 1 — cost the fully connected layer
> **(a)** Parameters for a first layer mapping ImageNet ($224\times224\times3$) to 4,096 units; memory in fp32; memory to train with Adam. **(b)** The same layer as 64 filters of $3\times3$. **(c)** Ratio. **(d)** Why is the ratio not the main argument?
>
> ---
> **(a)** $150{,}528\times4{,}096+4{,}096=\mathbf{616{,}566{,}784}$ parameters $=\mathbf{2.30}$ GB fp32. Adam needs weights + gradients + two moments = **4 copies = 9.19 GB** ([[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §5).
>
> **(b)** $64\times3\times3\times3+64=\mathbf{1{,}792}$.
>
> **(c)** $\mathbf{344{,}066\times}$.
>
> **(d)** ⚠️ **Because memory can be bought and structure cannot.** A 2.30 GB layer is merely expensive; §2 shows the MLP is **blind to spatial arrangement**, which no amount of memory repairs. *The parameter count is the symptom; permutation invariance is the disease.*

> [!example]- Exercise 2 — the permutation proof
> **(a)** Show that for any fixed permutation $\pi$ there is a weight matrix computing the same function on permuted inputs. **(b)** What experiment does that predict? **(c)** Run the analogous test on a convolution. **(d)** What is the general name for this?
>
> ---
> **(a)** $\big(\mathbf W_{[:,\pi]}\mathbf x_\pi\big)_j=\sum_i \mathbf W_{j,\pi(i)}x_{\pi(i)}=\sum_k \mathbf W_{jk}x_k=(\mathbf W\mathbf x)_j$ — the sum is simply re-indexed. **Verified: worst deviation $1.07\times10^{-14}$ over 200 random trials.**
>
> **(b)** ⚠️ **Shuffle all pixels of every image with one fixed permutation; an MLP's achievable accuracy is unchanged.** The permutation is absorbed into the first layer's columns during training. **The images become meaningless to a human and the model is indifferent.**
>
> **(c)** A $3\times3$ Sobel on a coherent block gives 24 nonzero responses forming **two clean vertical edges**; on the shuffled version, 44 responses **scattered at random**, with $\|\Delta\|_F=\mathbf{17.38}$. **The convolution's output is unrelated because it reads the arrangement.**
>
> **(d)** ⚠️ **Inductive bias.** The MLP's hypothesis class is invariant under a symmetry group (all $D!$ permutations) that the *problem* does not possess; the CNN's is invariant only under translations, which the problem *does* possess. **Matching the model's symmetries to the task's is what "architecture" means.**

> [!example]- Exercise 3 — the data argument
> **(a)** How many positions must a $3\times3$ feature be learned at, on $32\times32$ and $224\times224$? **(b)** What does that imply for data? **(c)** Which constraint binds first — memory or data?
>
> ---
> **(a)** $(32-3+1)^2=\mathbf{900}$ and $(224-3+1)^2=\mathbf{49{,}284}$.
>
> **(b)** Independent copies must each be learned from examples that happen to place the feature there, so **roughly $N$ times the data** — about $5\times10^4\times$ more at ImageNet resolution.
>
> **(c)** ⚠️ **Data.** 2.30 GB is affordable on a modern GPU; $5\times10^4$ times ImageNet is not affordable at all — it does not exist. ⇒ ***weight sharing is a statement about sample efficiency first and memory second***, which is the opposite of how it is usually introduced.

> [!example]- Exercise 4 — the cascade at three scales
> Impose translation invariance then locality ($5\times5$) on a fully connected image-to-image layer. **(a)** The three counts at $32\times32$. **(b)** At $224\times224$ and $1000\times1000$. **(c)** What does the trend say about benchmarks?
>
> ---
> **(a)** $1{,}048{,}576\to4{,}096\to\mathbf{16}$ — **256× then 256×, total 65,536×.**
>
> **(b)** $2.52\times10^9\to16$ ($1.6\times10^8\times$) and $1.00\times10^{12}\to16$ ($6.2\times10^{10}\times$).
>
> **(c)** ⚠️ **The advantage of convolution grows with image size**, so **CIFAR-10 understates it by roughly six orders of magnitude** relative to a real photograph. ⇒ *a benchmark on $32\times32$ thumbnails systematically flatters architectures that scale badly with resolution* — worth remembering whenever a new architecture reports CIFAR results only.

## 📝 Summary

- **An MLP is the obvious repair for [[03 - Image Classification and Linear Models|ch. 03]]'s one-template-per-class limit, and it fails on images for two reasons — one famous and one decisive.**
- **The famous one: size.** One fully connected layer from ImageNet to 4,096 units is **616,566,784 parameters = 2.30 GB**, or **9.19 GB to train with Adam**; a 4K frame to 1,000 units is **92.70 GB**. **The same first layer as a convolution is 1,792 parameters — 344,066× fewer.**
- **⚠️ The decisive one: an MLP cannot see spatial structure at all.** $\mathbf W_{[:,\pi]}\mathbf x_\pi=\mathbf W\mathbf x$ **exactly** (verified to $1.07\times10^{-14}$), so **shuffling every pixel with one fixed permutation leaves an MLP's achievable accuracy unchanged.** It treats an image as an unordered bag of numbers.
- **⚠️ The same shuffle makes a convolution's output unrelated** ($\|\Delta\|_F=17.38$; 24 responses forming clean edges become 44 scattered ones). **Locality is not an efficiency trick — it is how spatial structure enters the model.**
- **⚠️ The binding constraint is data, not memory.** Translation invariance would have to be learned **49,284 separate times** on a $224\times224$ image, needing on the order of $10^4$–$10^5$× more labelled data. **A convolution learns it once.**
- **The two assumptions buy 65,536× at CIFAR-10 size, $1.6\times10^8$ at ImageNet size and $6.2\times10^{10}$ at one megapixel** — the advantage **grows with resolution**, so thumbnail benchmarks understate it.
- **Three independent routes reach the same operator**: imposing invariance on an MLP ([[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §1), assuming linearity + shift-invariance ([[02 - Classical Image Processing|ch. 02]] §3), and observing that nothing else uses arrangement (§2 here). **The convolution is not a design choice.**

## ⚠️ Important Notes

1. **⚠️ "Too many parameters" is the weak objection.** Memory is purchasable; **permutation invariance is not repairable**. Lead with the structural argument.
2. **⚠️ The shuffled-CIFAR experiment is worth running once.** It is the fastest way to convince yourself — and anyone else — that an MLP is not doing vision. *(And it is a classic exam question of exactly the "reason about what happens and why" form [[00-Index]] records for the week-9 mid-term.)*
3. **⚠️ Inductive bias cuts both ways.** Convolution assumes translation invariance and locality; **[[01 - Introduction and Image Formation|ch. 01]] §1 lists the cases where that is false** (absolute position matters in face alignment, document layout, board games). **A wrong bias is worse than none** — which is why modern architectures re-inject position ([[06 - Vision Transformers|ch. 06]]).
4. **⚠️ Flattening destroys structure irreversibly.** Any `Flatten()` before a spatial operation throws away the arrangement for every layer after it. **In a CNN the flatten belongs at the *end*, after the convolutions have used the geometry** — and [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] §11 shows NiN deletes even that.
5. **⚠️ Benchmark resolution changes conclusions.** The convolutional advantage grows with image size, so **CIFAR-scale results do not transfer to ImageNet-scale claims** — in either direction.
6. **Universal approximation does not rescue the MLP.** It says a wide enough MLP *can* represent the right function; it says nothing about finding it from finite data. **[[Deep Learning/contents/04 - Neural Network|DL ch. 04]] §3's C-language analogy is exact: expressible is not the same as reachable.**

> [!warning] Gaps in the source material
> **⚠️ NO LECTURE SLIDES for this week** ([[00-Index]]). Built from **Szeliski §5.3–5.4**, **CS231n**, and this vault's own [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] and [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]].
>
> **⚠️ AND THIS IS DELIBERATELY A SHORT CHAPTER.** [[00-Index]]'s boundary rule says weeks 4, 5, 7 and half of 6 are already in the vault and must be **cross-referenced, not duplicated**. **Szeliski §5.3 (weights and layers, activation functions, regularization, loss functions, backpropagation, training) and §5.4 (convolution, pooling, architectures) are covered in far more depth by DL ch. 04–05**, including seven printed optimizer traces reproduced exactly and the parameters-versus-FLOPs inversion. **Reproducing them here would create two copies that can drift apart.**
>
> **What is genuinely new here, and is mine:**
> - **§1's parameter table at real image sizes** (CIFAR-10 → 4K) and the **344,066×** convolution comparison at ImageNet scale. *DL ch. 05 §8 computes 23,671× for LeNet; this is the same argument an order of magnitude further out.*
> - **§2's permutation theorem and its numerical verification** ($1.07\times10^{-14}$ over 200 trials), the shuffled-CIFAR thought experiment, and **the convolution counter-test** ($\|\Delta\|_F=17.38$, 24 clean responses → 44 scattered). **This framing — that the decisive objection is permutation invariance rather than parameter count — is not in Szeliski, CS231n or D2L in this form.**
> - **§3's positions-to-learn table and the data-versus-memory argument**, which inverts the usual order of presentation.
> - **§4's cascade at three image scales** and the observation that **thumbnail benchmarks understate the convolutional advantage by six orders of magnitude.**
> - **The three-routes table** in §4, which is a synthesis across this subject's ch. 02, DL ch. 05 and this chapter.
> - **All six Important Notes.**
>
> **No discrepancies found**; every quantitative claim here is my own computation, and every qualitative claim is either sourced to DL ch. 04–05 or stated as my synthesis. ⚠️ **One error was caught and corrected during verification**: the first implementation of §2's permutation identity indexed with `argsort(perm)` instead of `perm` and returned a deviation of $1.93\times10^2$ rather than $0$. **The claim was not written until the corrected version verified at $10^{-14}$.**
>
> **Deliberately deferred, not omitted:** **everything mechanical about convolution** — cross-correlation, padding, stride, channels, $1\times1$ convolutions, pooling, receptive fields, and the LeNet → AlexNet → VGG → NiN → GoogLeNet → BN → ResNet → ResNeXt → DenseNet progression — is [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] and is **linked, not repeated**. **Backpropagation, initialization, dropout and the optimizers** are [[Deep Learning/contents/04 - Neural Network|DL ch. 04]]. **[[05 - CNN Architectures|Ch. 05]] of this subject is the same situation and will be equally short.**
>
> **Left as the source states it:** the universal approximation results (Cybenko 1989, Micchelli 1984) via DL ch. 04 §3; Szeliski's §5.4 treatment of pooling and architectures; and the ImageNet input convention of $224\times224$, which is a preprocessing choice rather than a property of the dataset.

**Previous:** [[03 - Image Classification and Linear Models]] · **Next:** [[05 - CNN Architectures]]
