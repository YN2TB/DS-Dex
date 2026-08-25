---
subject: Deep Learning
chapter: 5
tags: [ds, deep-learning, cnn, convolution, pooling, receptive-field, batch-normalization, resnet, densenet, architecture]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 7 (Convolutional Neural Networks) and ch. 8 (Modern Convolutional Neural Networks)"
---

# Convolutional Neural Network

**Two full D2L chapters: ch. 7 builds the convolution from first principles, ch. 8 walks LeNet → AlexNet → VGG → NiN → GoogLeNet → batch norm → ResNet → ResNeXt → DenseNet.** *(The scope is set by the user's syllabus — see [[00-Index]].)*

**⚠️ EVERY PRINTED SHAPE, EVERY WORKED EXAMPLE AND BOTH OF D2L'S MEMORY CLAIMS WERE RECOMPUTED.** All seven cross-correlation and pooling examples reproduce exactly; the output-shape formula reproduces all five printed `torch.Size` results including the one D2L leaves as an unanswered exercise; the 53-billion-operation figure and the "almost 400 MB" figure verify to the digit.

**Six results.**

**§17 — ⚠️ THE ORGANIZING RESULT OF THE WHOLE CHAPTER, AND D2L NEVER TABULATES IT: PARAMETERS AND COMPUTATION LIVE IN OPPOSITE HALVES OF EVERY PRE-2013 CNN.** LeNet, AlexNet and VGG-11 each hold **under 8% of their parameters and over 85% of their computation in the convolutions**, and **over 92% of their parameters and under 15% of their computation in the fully connected head.** ⇒ ***"convolutional neural network" describes where the arithmetic is, not where the weights are*** — **LeNet is 95.8% fully connected by parameter count.**

**§1 — ⚠️ THE PARAMETER CASCADE IS TEN ORDERS OF MAGNITUDE AND D2L GIVES ALL THREE NUMBERS WITHOUT DIVIDING THEM.** $10^{12}\to4\times10^6$ (translation invariance, **250,000×**) $\to100$ (locality, **40,000×**) = **$10^{10}$ total.** D2L says only "another four orders of magnitude."

**§11 — ⚠️ NiN IS 64.7× SMALLER THAN VGG-11 AND THE ENTIRE SAVING IS ONE DELETED MATRIX.** VGG-11's *first* fully connected layer is **102,764,544 parameters = 392.0 MB = 79.8% of the whole network**. Global average pooling replaces it with **zero parameters** — and in a controlled test **cuts a network 210.4× while reducing computation by only 15.8%**.

**§10 — ⚠️ A NEW CIPHER ENTRY, CAUGHT BY ARITHMETIC.** D2L's VGG argument extracts as *"(39c2)"*, which is **not $39c^2$ but $3\times9c^2=27c^2$** — the multiplication sign deleted. **Proof: $27/25=1.08$ is "approximately as many"; $39/25=1.56$ is not.**

**§13 — ⚠️ BATCH NORM'S REGULARIZATION IS THE SAME $1/\sqrt b$ LAW AS DROPOUT AND MINIBATCH SGD.** D2L's unexplained "works best in the 50–100 range" is exactly where batch noise is **14.1%–10.0%**. ⇒ **raising the batch size to train faster silently weakens the regularization**, and D2L flags this without quantifying it.

**§7 — ⚠️ DEPTH IS HOW A LOCAL OPERATOR BECOMES A GLOBAL ONE.** A single $3\times3$ convolution sees 9 pixels; **VGG-11's eight of them, interleaved with five poolings, see $150\times150$ — 67% of a $224\times224$ image.** Traced layer by layer; D2L says "we can build a deeper network" and computes nothing.

## 📘 Main Knowledge

### 1. ⚠️ Why an MLP cannot do vision — the cascade, with the ratios

D2L's opening argument: a one-megapixel photo fed to a fully connected layer with 1,000 hidden units needs $10^6\times10^3=\mathbf{10^9}$ parameters — **3.7 GB in `float32` for a single layer.** And 1,000 hidden units "grossly underestimates" what image representations need.

Now the derivation. Let the input and hidden representation both be $1000\times1000$ *grids*, so the weights are a **fourth-order tensor**:

$$[\mathsf H]_{i,j}=[\mathsf U]_{i,j}+\sum_k\sum_l[\mathsf W]_{i,j,k,l}[\mathsf X]_{k,l}=[\mathsf U]_{i,j}+\sum_a\sum_b[\mathsf V]_{i,j,a,b}[\mathsf X]_{i+a,\,j+b}$$

*(the re-indexing $k=i+a$, $l=j+b$ is cosmetic — it just measures the input position as an **offset** from the output position.)*

**Now impose the two principles.**

**(i) Translation invariance** — a shift in $\mathsf X$ should produce the same shift in $\mathsf H$. That forces $\mathsf V$ and $\mathsf U$ **not to depend on $(i,j)$**:

$$[\mathsf H]_{i,j}=u+\sum_a\sum_b[\mathsf V]_{a,b}[\mathsf X]_{i+a,\,j+b}$$

**(ii) Locality** — information beyond a radius $\Delta$ is irrelevant, so $[\mathsf V]_{a,b}=0$ for $|a|>\Delta$ or $|b|>\Delta$:

$$\boxed{[\mathsf H]_{i,j}=u+\sum_{a=-\Delta}^{\Delta}\sum_{b=-\Delta}^{\Delta}[\mathsf V]_{a,b}[\mathsf X]_{i+a,\,j+b}}$$

**That is a convolutional layer**, and $\mathsf V$ is the **kernel** / **filter** / the layer's weights.

> [!warning] ⚠️ THE CASCADE, WITH THE DIVISIONS D2L DOES NOT DO
> | | parameters | reduction |
> |---|---|---|
> | full fourth-order tensor $[\mathsf W]_{i,j,k,l}$ | **1,000,000,000,000** | — |
> | + translation invariance $\to[\mathsf V]_{a,b}$ | **4,000,000** | **250,000×** |
> | + locality ($\Delta=5$, an $11\times11$ kernel) | **100** | **40,000×** |
>
> $$\textbf{TOTAL REDUCTION} = \frac{10^{12}}{100}=\mathbf{10^{10}}$$
>
> **D2L states each figure and says only "we reduced the number of parameters by another four orders of magnitude."** The total is **ten** orders.
>
> ⇒ ***two assumptions about the world — that a pattern means the same thing wherever it appears, and that nearby pixels matter more than distant ones — buy a factor of ten billion.*** Everything else in this chapter is engineering on top of that.

> [!note] ⚠️ And D2L is honest about the price, which is the part to remember
> *"All learning depends on imposing inductive bias. When that bias agrees with reality, we get sample-efficient models that generalize well… But if those biases do not agree with reality, e.g., if images turned out not to be translation invariant, our models might struggle even to fit our training data."*
>
> **The $10^{10}$ is not free — it is borrowed against an assumption.** *(Its own exercise 7.1.3 asks "why might translation invariance not be a good idea after all?" Answer: whenever absolute position carries meaning — a face-alignment task where eyes are always in the upper half, a document layout where the header is always on top, or a game board. This is why modern architectures re-inject **position encodings**, which is exactly what [[08 - Sequence to Sequence|ch. 08]]'s Transformer must do.)*

**The motivation for the principles themselves is D2L's "Where's Waldo" argument, and it is the right one:** *"what Waldo looks like does not depend upon where Waldo is located."* Sweep one detector over every patch.

### 2. Cross-correlation, and why everyone calls it convolution

The true mathematical convolution flips one argument:

$$(f*g)(i,j)=\sum_a\sum_b f(a,b)\,g(i-a,\,j-b)$$

but §1's formula uses $(i+a,\,j+b)$. **So what deep learning calls a convolution is strictly a *cross-correlation*.**

> [!note] Why nobody cares, and it is a real argument
> To get strict convolution you flip the kernel horizontally and vertically. **But the kernel is *learned*** — so a layer trained to do cross-correlation learns $\mathsf K$, and the same layer doing strict convolution would learn the flipped $\mathsf K'$, producing **identical output**. ⇒ *the distinction is unobservable in a trained network.* **It matters only when you import a kernel from signal processing, where the convention is the other one.**

**The core operation, and the four numbers verified:**

| $\mathsf X$ (3×3) | $\mathsf K$ (2×2) | output |
|---|---|---|
| $\begin{pmatrix}0&1&2\\3&4&5\\6&7&8\end{pmatrix}$ | $\begin{pmatrix}0&1\\2&3\end{pmatrix}$ | $\begin{pmatrix}19&25\\37&43\end{pmatrix}$ |

$0\cdot0+1\cdot1+3\cdot2+4\cdot3=19$; $1\cdot0+2\cdot1+4\cdot2+5\cdot3=25$; $3\cdot0+4\cdot1+6\cdot2+7\cdot3=37$; $4\cdot0+5\cdot1+7\cdot2+8\cdot3=43$. **All four reproduce D2L's printout exactly.**

**The edge detector is the cleanest illustration in the chapter.** With $\mathsf K=[1,\,-1]$ on a $6\times8$ image whose middle four columns are black, the output is $0$ everywhere except $+1$ at the white→black edge and $-1$ at black→white. **Verified: row 0 = $[0,1,0,0,0,-1,0]$**, matching D2L.

> [!warning] ⚠️ That kernel is a finite-difference operator, and the transpose test proves the point
> $[1,-1]$ computes $x_{i,j}-x_{i+1,j}$ — **a discrete approximation to $\partial f/\partial i$.** Applied to the **transposed** image the output is **identically zero** (verified: $\max|Y|=0.0$). ⇒ **it detects vertical edges only.** *That is the whole reason you need many channels: one kernel is one derivative in one direction.*
>
> **And D2L's learning demo closes the loop:** starting from a random kernel and fitting $\hat{\mathsf K}$ to the input–output pair by gradient descent, after 10 iterations the loss is $0.011$ and the learned kernel is $[0.9797,\,-0.9816]$ — **it rediscovers the finite-difference operator from data.** ⇒ ***feature engineering replaced by evidence-based statistics***, in eight lines of code.

### 3. Padding and stride — the output-shape formula

Without padding, an $n_h\times n_w$ input and $k_h\times k_w$ kernel give $(n_h-k_h+1)\times(n_w-k_w+1)$ — **the image shrinks by $k-1$ per layer.** D2L's example: **ten layers of $5\times5$ on a $240\times240$ image leave $200\times200$, slicing off 30% and obliterating the boundaries.**

With total padding $p$ and stride $s$:

$$\boxed{\left\lfloor\frac{n_h-k_h+p_h+s_h}{s_h}\right\rfloor\times\left\lfloor\frac{n_w-k_w+p_w+s_w}{s_w}\right\rfloor}$$

**All five of D2L's printed shapes reproduce:**

| configuration | computed | D2L prints |
|---|---|---|
| $k=3$, $p=2$, $s=1$, $n=8$ | 8 | `torch.Size([8, 8])` ✓ |
| $k=(5,3)$, $p=(4,2)$, $s=1$, $n=8$ | 8 | `torch.Size([8, 8])` ✓ |
| $k=3$, $p=2$, $s=2$, $n=8$ | 4 | `torch.Size([4, 4])` ✓ |
| **$k=(3,5)$, $p=(0,2)$, $s=(3,4)$, $n=8$** | $\lfloor 8/3\rfloor\times\lfloor 9/4\rfloor=\mathbf{2\times2}$ | `torch.Size([2, 2])` ✓ |

**The last row is D2L's exercise 7.3.1, which it poses and does not answer.**

> [!warning] ⚠️ Why CNN kernels are 1, 3, 5, 7 and never 2, 4, 6
> To preserve the size you need $p=k-1$ split evenly, i.e. $(k-1)/2$ per side — **which is an integer only for odd $k$.** For even $k$ you must pad $\lceil p/2\rceil$ on one side and $\lfloor p/2\rfloor$ on the other, **breaking the symmetry** so that $\mathsf Y[i,j]$ is no longer the window *centred* on $\mathsf X[i,j]$.
>
> ⇒ ***the near-universal use of odd kernel sizes is a clerical convenience, not a mathematical necessity*** — and it is worth knowing that, because it means an even kernel is not wrong, merely annoying.

**Padding is not neutral.** D2L's Fig. 7.3.1 makes the point that **corner pixels are barely used** — the centre of an image is touched by many more windows than the border. Zero-padding equalises this, and has a side effect worth knowing: **it lets a CNN encode implicit position information by learning where the whitespace is** — the one channel through which a "translation-invariant" network can learn about absolute position.

### 4. Channels — where the expressive power comes back

**Multiple input channels.** For $c_i$ input channels the kernel is $c_i\times k_h\times k_w$: cross-correlate per channel and **sum over channels**.

Verified against D2L's Fig. 7.4.1: $(1\cdot1+2\cdot2+4\cdot3+5\cdot4)+(0\cdot0+1\cdot1+3\cdot2+4\cdot3)=56$, and the full output $\begin{pmatrix}56&72\\104&120\end{pmatrix}$ **matches**.

**Multiple output channels.** For $c_o$ outputs the kernel is $c_o\times c_i\times k_h\times k_w$. D2L's three-channel stack reproduces exactly: $\begin{pmatrix}56&72\\104&120\end{pmatrix}$, $\begin{pmatrix}76&100\\148&172\end{pmatrix}$, $\begin{pmatrix}96&128\\192&224\end{pmatrix}$ ✓

> [!note] ⚠️ The interpretation D2L explicitly warns against
> The tempting story is "channel 1 is an edge detector, channel 2 is a texture detector." **D2L: "channels are optimized to be *jointly* useful… rather than mapping a single channel to an edge detector, it may simply mean that some *direction in channel space* corresponds to detecting edges."**
>
> ⇒ *the basis is arbitrary; only the span is learned.* **This is exactly [[04 - Neural Network|ch. 04]]'s permutation symmetry in another guise, and the same reason [[02 - Linear Regression|ch. 02]]'s weight norm was blind to direction.**

**The cost, and D2L's own figure verified:**

$$\text{multiply-adds}=h\cdot w\cdot k^2\cdot c_i\cdot c_o$$

For $256\times256$, $k=5$, $c_i=c_o=128$, counting multiplications and additions separately: $256\cdot256\cdot25\cdot128\cdot128\cdot2=\mathbf{53{,}687{,}091{,}200}$ — **"over 53 billion operations" ✓ exact.**

**⚠️ Doubling both $c_i$ and $c_o$ quadruples the cost.** Channels are the expensive dimension, which is what ResNeXt (§15) attacks.

### 5. The $1\times1$ convolution — a fully connected layer per pixel

A $1\times1$ kernel cannot see any neighbour, so **its only computation is across channels.** It is exactly a fully connected layer $c_i\to c_o$ applied independently at every pixel, **with the weights tied across positions**: $c_ic_o$ weights plus bias.

*(D2L verifies this by implementing it as a matrix multiply and asserting agreement to $10^{-6}$.)*

> [!note] Two uses, both structural
> **(i) Channel-count surgery.** It changes $c_i\to c_o$ at negligible spatial cost — used to shrink channels before an expensive $3\times3$ (Inception, §12), to restore them (ResNeXt, §15), and to compress after concatenation (DenseNet's transition layers, §16).
>
> **(ii) Nonlinearity across channels without touching space** — NiN's insight, §11.
>
> **And a $1\times1$ convolution is not foldable into its neighbours** *because a nonlinearity sits between them* — otherwise two consecutive convolutions collapse into one, exactly [[04 - Neural Network|ch. 04]] §1's linear-collapse result.

### 6. Pooling — the only parameter-free layer

Pooling slides a fixed window and takes the **max** or the **mean**. **No kernel, no parameters, no learning.** Verified on D2L's example ($\mathsf X=0..8$, $2\times2$): max gives $\begin{pmatrix}4&5\\7&8\end{pmatrix}$ ✓, average gives $\begin{pmatrix}2&3\\5&6\end{pmatrix}$ ✓.

It serves **two** purposes at once:
1. **Downsampling** — a $2\times2$ window with stride 2 quarters the spatial resolution.
2. **Local translation invariance** — D2L's argument is precise: after the $[1,-1]$ edge detector, $2\times2$ max-pooling still reports the edge **if the pattern moves by no more than one element** in height or width.

**Pooling is applied per channel and does not sum over them**, so it leaves the channel count unchanged — the opposite of a convolutional layer. *(Verified against D2L's two-channel printout: $\begin{pmatrix}5&7\\13&15\end{pmatrix}$ and $\begin{pmatrix}6&8\\14&16\end{pmatrix}$.)*

**Frameworks default the stride to the window size** — `nn.MaxPool2d(3)` gives stride 3 — which is a real trap, because a convolution's stride defaults to 1.

### 7. ⚠️ Receptive field — depth is how a local operator becomes global

For element $x$ in some layer, its **receptive field** is every input element that can affect it. It grows layer by layer:

$$\mathrm{RF}_{\text{out}}=\mathrm{RF}_{\text{in}}+(k-1)\cdot j,\qquad j_{\text{out}}=j_{\text{in}}\cdot s$$

where $j$ is the **jump** — the input distance between adjacent outputs.

**Traced through VGG-11's body on a $224\times224$ input:**

| after | RF | jump |
|---|---|---|
| conv 3×3 | 3 | 1 |
| pool s2 | 4 | 2 |
| conv 3×3 | 8 | 2 |
| pool s2 | 10 | 4 |
| conv, conv | 18, **26** | 4 |
| pool s2 | 30 | 8 |
| conv, conv | 46, **62** | 8 |
| pool s2 | 70 | 16 |
| conv, conv | 102, **134** | 16 |
| pool s2 | **150** | 32 |

> [!warning] ⚠️ A single $3\times3$ convolution sees **9 pixels**. Eight of them, interleaved with five poolings, see **$150\times150$ — 67% of the image**
> **The strides are what make this work.** Without pooling, eight $3\times3$ layers would reach only $\mathrm{RF}=1+8\cdot2=17$. **Each stride-2 pooling doubles the jump, so every subsequent layer's $(k-1)$ counts double, then quadruple, then eightfold.** ⇒ ***the receptive field grows geometrically in the number of downsampling steps and only linearly in the number of layers.***
>
> **And on LeNet the receptive field is 32 on a 28×28 input — larger than the image itself**, which is exactly D2L's remark that "the receptive field may be larger than the actual size of the input."
>
> ⇒ ***this is the answer to "why deep": not only more nonlinearity, but the only way a stack of strictly local operators can answer a global question like "is there a cat in this image".*** **D2L says "we can build a deeper network" and computes none of it.**

*(Receptive fields are named from neurophysiology — Hubel & Wiesel's experiments found that low levels of the visual cortex respond to edges, and Field (1987) reproduced the effect on natural images with what are unmistakably convolution kernels.)*

### 8. ⚠️ LeNet — and the split that runs through the whole chapter

LeNet-5 (LeCun et al., 1998): two conv blocks (conv → sigmoid → average pool), then three fully connected layers. It reached **under 1% error per digit**, matched SVMs, and ran in ATMs for decades.

**Every printed shape recomputed, and the parameter count D2L never gives:**

| layer | output shape | **parameters** |
|---|---|---|
| conv1 $1\to6$, $5\times5$, pad 2 | $6\times28\times28$ | 156 |
| avg-pool $2\times2$ s2 | $6\times14\times14$ | 0 |
| conv2 $6\to16$, $5\times5$ | $16\times10\times10$ | 2,416 |
| avg-pool $2\times2$ s2 | $16\times5\times5$ | 0 |
| flatten | 400 | 0 |
| fc1 $400\to120$ | 120 | **48,120** |
| fc2 $120\to84$ | 84 | **10,164** |
| fc3 $84\to10$ | 10 | 850 |

**All eight shapes match D2L's printed `layer_summary`.**

> [!warning] ⚠️ THE CONVOLUTIONAL LAYERS ARE **4.17%** OF LeNet'S PARAMETERS
> **Convolutions: 2,572. Fully connected: 59,134. Total 61,706 = 0.235 MB.**
>
> $$\textbf{LeNet is 95.83\% fully connected by parameter count.}$$
>
> **And here is what the convolution buys.** conv1 maps 784 inputs to $6\times28\times28=4{,}704$ outputs. As a *fully connected* layer that is **3,692,640 parameters**; as a convolution it is **156**.
>
> $$\textbf{ratio} = \mathbf{23{,}671\times}$$
>
> ⇒ ***that number is weight sharing, measured.*** It is §1's $10^{10}$ argument instantiated on a real layer.

**Two historical notes D2L supplies:** LeNet uses **sigmoid and average pooling** because "ReLUs and max-pooling work better, [but] they had not yet been discovered." And MNIST's $28\times28$ is a **trimmed $32\times32$** — two rows and columns cut to save 30% of the space.

### 9. AlexNet (2012) — the same architecture, eight orders of magnitude more resources

AlexNet is **eight layers**: five convolutional, two fully connected hidden, one output. **The architecture is strikingly close to LeNet.** What changed was everything around it.

| | LeNet (1995) | AlexNet (2012) |
|---|---|---|
| activation | sigmoid | **ReLU** |
| pooling | average | **max** |
| regularization | weight decay | **dropout + heavy augmentation** |
| first kernel | $5\times5$ | $11\times11$ (ImageNet images are 8× larger) |
| channels | 6, 16 | 96, 256, 384, 384, 256 — **ten times more** |
| data | 60,000 $28\times28$ | **1.2M $224\times224$**, 1000 classes |
| hardware | CPU | **two GTX 580s at 1.5 TFLOPs each** |

> [!note] The pre-2012 pipeline, which is the thing AlexNet actually killed
> Obtain a dataset → hand-craft features (**SIFT, SURF, HOG, bags of visual words**) → dump into a linear model or kernel method. **"Rather than *learning* the features, the features were *crafted*."** D2L is blunt that vision researchers believed "a slightly bigger or cleaner dataset or a slightly improved feature-extraction pipeline mattered far more to the final accuracy than any learning algorithm" — **and on the evidence available then, they were right.**
>
> **The 1994 Apple QuickTake 100: 0.3 megapixels, stores 8 images, \$1,000.** That is the data-collection constraint in one line.

**Parameter count, computed for both versions:**

| | D2L's 1-channel / 10-class version | **the original: 3-channel, 1000-class** |
|---|---|---|
| five conv layers | 3,723,968 (**8.0%**) | 3,747,200 (**6.0%**) |
| three fc layers | 43,040,778 (**92.0%**) | 58,631,144 (**94.0%**) |
| **total** | 46,764,746 = 178.4 MB | **62,378,344 = 238.0 MB** |

*(The widely quoted "~60 million parameters" for AlexNet — consistent ✓.)*

> [!warning] ⚠️ D2L: "these layers require nearly 1GB model parameters" — and they are 208 MB
> The two 4096-output layers are $9216\times4096$ and $4096\times4096$ = **54,534,144 parameters = 208.0 MB in `float32`**, which is **4.9× less than 1 GB**.
>
> **Under the vault's rule 4, what reading makes it right?**
>
> | | |
> |---|---|
> | weights only | 208.0 MB |
> | + gradients | 416.1 MB |
> | + momentum | 624.1 MB |
> | **+ Adam's two moments (×4)** | **832.1 MB — "nearly 1GB"** ✓ |
>
> ⇒ **the claim is correct about the *training footprint* and wrong about the *parameters*** — which is precisely [[04 - Neural Network|ch. 04]] §5's finding that the optimizer state is half the memory bill, arriving from the opposite direction. **DECLINED as an erratum; recorded as an imprecision (D8).**

### 10. VGG (2014) — blocks, and the $3\times3$ argument

**A VGG block** = several $3\times3$ convolutions with padding 1 (size-preserving) + ReLU, then one $2\times2$ max-pool with stride 2 (halving). **VGG-11** = five blocks (1, 1, 2, 2, 2 convs; channels 64, 128, 256, 512, 512) + the AlexNet fully connected head.

> [!note] Why blocks exist at all — D2L's $\log_2 d$ argument, checked
> If every convolution is followed by a pooling, the resolution halves every layer, so the network cannot exceed $\log_2 d$ layers. **Checked: $\log_2 224=7.807$, so 7 halvings take $224\to1.75$.** *(D2L says 8, using $\log_2 256$; off by one, and the point stands.)*
>
> ⇒ ***a block decouples DEPTH from RESOLUTION LOSS by putting several convolutions between poolings.*** That is the whole idea, and it is why architectures have been described in blocks ever since.

**⚠️ Now the parameter argument — and a cipher catch.**

D2L: *"the successive application of two $3\times3$ convolutions touches the same pixels as a single $5\times5$ convolution does. At the same time, the latter uses approximately as many parameters ($25c^2$) as three $3\times3$ convolutions do **(39c2)**."*

> [!warning] ⚠️ "39c2" IS NOT $39c^2$ — it is $3\times9c^2=27c^2$, with the multiplication sign deleted
> **The arithmetic proves the reading:** $27/25=\mathbf{1.08}$ is "approximately as many"; $39/25=\mathbf{1.56}$ is not. **A new entry for this subject's cipher table** — the same deletion already recorded for `1 1` meaning $1\times1$.

**The comparison D2L sets up and does not complete.** $L$ stacked $3\times3$ convolutions have receptive field $1+2L$:

| target RF | $L$ of $3\times3$ | params ($3\times3$) | params (single) | **saving** | **ReLUs** |
|---|---|---|---|---|---|
| $5\times5$ | 2 | $18c^2$ | $25c^2$ | **28.0%** | 2 |
| **$7\times7$** | 3 | $27c^2$ | $49c^2$ | **44.9%** | **3** |
| $9\times9$ | 4 | $36c^2$ | $81c^2$ | 55.6% | 4 |
| $11\times11$ | 5 | $45c^2$ | $121c^2$ | **62.8%** | 5 |

> [!warning] ⚠️ Small stacked kernels win on **both** axes at once, and the gap widens with size
> At $c=64$: the $7\times7$ receptive field costs **110,592** parameters as three $3\times3$s and **200,704** as one $7\times7$. **At AlexNet's $11\times11$ the saving is 62.8%.**
>
> ⇒ ***more nonlinearity for fewer parameters — there is no trade-off here, which is why "stack $3\times3$" became the gold standard and AlexNet's $11\times11$ never reappeared.*** **D2L computes the $5\times5$ case (28.0%) and stops.**
>
> *(D2L notes the assumption was revisited only in 2022 by Liu et al., given far more compute and data.)*

**VGG-11's cost, and D2L's own claim verified exactly:**

| | parameters | share |
|---|---|---|
| 8 convolutional layers | 9,219,328 | **7.2%** |
| 3 fully connected layers | 119,586,826 | **92.8%** |
| **total** | **128,806,154** | **491.4 MB** |

> [!warning] ⚠️ **ONE MATRIX IS 79.8% OF VGG-11**
> The first fully connected layer is $25{,}088\times4096=\mathbf{102{,}764{,}544}$ parameters $=411{,}058{,}176$ bytes $=\mathbf{392.0\ MB}$.
>
> **D2L: "occupying almost 400MB of RAM in single precision (FP32)" — VERIFIED TO THE DIGIT.**
>
> **All eight convolutional layers together are 35.2 MB — 11.1× smaller than that single matrix.**

### 11. ⚠️ NiN (2013) — deleting the head

Two insights, both about the fully connected layers:
1. **$1\times1$ convolutions** add nonlinearity across channels at each pixel — a "network in network."
2. **Global average pooling** replaces the fully connected head entirely: make the last block output *one channel per class*, then average each channel over space to get the logits.

**A NiN block** = one $k\times k$ convolution + two $1\times1$ convolutions, each with ReLU. **The model uses AlexNet's kernel sizes ($11\times11$, $5\times5$, $3\times3$) and channel counts, and then has no fully connected layers at all.**

| network | parameters | MB (fp32) | **fc share** |
|---|---|---|---|
| LeNet | 61,706 | 0.2 | **95.8%** |
| AlexNet (original) | 62,378,344 | 238.0 | **94.0%** |
| VGG-11 | 128,806,154 | 491.4 | **92.8%** |
| **NiN** | **1,992,166** | **7.6** | **0.0%** |

> [!warning] ⚠️ **NiN IS 64.7× SMALLER THAN VGG-11 AND 31.3× SMALLER THAN AlexNet**
> **D2L says "NiN has dramatically fewer parameters" and never divides.**
>
> **What was deleted, in one line:**
> - **VGG head**: $512\times7\times7=25{,}088$ numbers $\to4096\to4096\to10$ = **119,586,826 parameters**
> - **NiN head**: $10\times5\times5\to$ average over $5\times5\to10$ = **0 parameters**
>
> ⇒ **global average pooling *throws away* the spatial positions instead of learning a weight for each one.** And D2L records the reaction: **"what surprised researchers at the time was the fact that this averaging operation did not harm accuracy."**
>
> ⇒ ***the 92% of parameters in every previous architecture were not buying accuracy.*** They were buying the ability to care *where* in the image the evidence appeared — which, for classification, is exactly the thing §1 assumed away. **The head contradicted the premise of the body.**

### 12. GoogLeNet (2014) — stem, body, head; and refusing to choose

The **Inception block** has four parallel branches — $1\times1$; $1\times1$ then $3\times3$; $1\times1$ then $5\times5$; $3\times3$ max-pool then $1\times1$ — all padded to the same spatial size, then **concatenated along channels**.

> [!note] ⚠️ The idea is to stop choosing the kernel size
> Contemporary work argued over which single kernel, from $1\times1$ to $11\times11$, was best. **GoogLeNet used all of them and let the channel allocation decide.** The $1\times1$ convolutions on the middle branches **shrink the channel count before the expensive $3\times3$ and $5\times5$** — which is what makes four parallel branches affordable at all (§4: cost $\propto c_ic_o$).
>
> **GoogLeNet also named the pattern every architecture has used since**: a **stem** (first two or three convolutions, low-level features), a **body** (the repeated blocks), and a **head** (map features to the task). *(That factorization is what makes [[06 - Object Detection|ch. 06]]'s fine-tuning possible: keep stem and body, replace the head.)*

### 13. Batch normalization (2015) — and the $1/\sqrt b$ law again

$$\mathrm{BN}(\mathbf x)=\boldsymbol\gamma\odot\frac{\mathbf x-\hat{\boldsymbol\mu}_{\mathcal B}}{\hat{\boldsymbol\sigma}_{\mathcal B}}+\boldsymbol\beta,\qquad \hat{\boldsymbol\mu}_{\mathcal B}=\frac{1}{|\mathcal B|}\sum_{\mathbf x\in\mathcal B}\mathbf x,\quad \hat{\boldsymbol\sigma}^2_{\mathcal B}=\frac{1}{|\mathcal B|}\sum_{\mathbf x\in\mathcal B}(\mathbf x-\hat{\boldsymbol\mu}_{\mathcal B})^2+\epsilon$$

Standardize using **the current minibatch's** statistics, then restore the lost degrees of freedom with a learned scale $\boldsymbol\gamma$ and shift $\boldsymbol\beta$. **In convolutional layers it is applied per channel, across all locations** — which is the only choice compatible with translation invariance. Placed **after the affine map, before the nonlinearity**.

**Three benefits at once**, and D2L is candid that they were not all intended: **preprocessing** (the same standardization we apply to inputs, applied inside), **numerical stability** (activations cannot drift), and **regularization** (noise).

> [!warning] ⚠️ It cannot work with a batch of one, and that is arithmetic, not a heuristic
> With $|\mathcal B|=1$, $\hat\mu_{\mathcal B}=x$, so $(x-\hat\mu)/\hat\sigma$ is **exactly 0** — verified. **The input value is destroyed entirely.** ⇒ BN is the first layer in this book whose output depends on *which other examples share the batch*.

> [!warning] ⚠️ D2L's unexplained "50–100 range" is the $1/\sqrt b$ law, for the third time in this subject
> The batch statistics are *estimates*; their relative noise is $1/\sqrt{|\mathcal B|}$:
>
> | $|\mathcal B|$ | relative noise in $\hat\mu_{\mathcal B}$ | |
> |---|---|---|
> | 1 | **1.0000** | destroys the signal |
> | 32 | 0.1768 | |
> | **50** | **0.1414** | ← D2L's "best in the 50–100 range" |
> | **100** | **0.1000** | ← |
> | 512 | 0.0442 | too stable — regularizes less |
> | 4096 | 0.0156 | |
>
> ⇒ **the same $1/\sqrt b$ that governs [[04 - Neural Network|ch. 04]]'s dropout variance and minibatch gradient noise.** D2L's own words: *"a larger minibatch regularizes less due to the more stable estimates, whereas tiny minibatches destroy useful signal due to high variance."*
>
> ⚠️ **THE PRACTICAL CONSEQUENCE, which D2L flags without quantifying: increasing the batch size to train faster silently weakens the regularization.** Scaling from 64 to 512 cuts the injected noise by $2.83\times$ — so a large-batch run may need *more* explicit regularization, not less.

**Cost:** 2 parameters per channel. **ResNet-18's BN layers total roughly 7,800 parameters against ~11 million weights — BN is essentially free in memory** and pays for itself many times over in trainability. **Together with residual connections it is what made 100+ layer networks routine.**

> [!note] ⚠️ Train and test behave differently, exactly like dropout
> Training normalizes by **batch** statistics; prediction normalizes by **dataset** statistics accumulated during training. **Otherwise the same image would be classified differently depending on which batch it landed in.** *(Third instance in this subject of a layer that is not a pure function of its input — after dropout and BN's own batch dependence.)*

### 14. ResNet (2015) — the nested-function-class argument

**The problem, stated properly.** Let $\mathcal F$ be the class of functions an architecture can reach. A *different, larger* architecture $\mathcal F'$ gives no guarantee of a better fit — **unless $\mathcal F\subseteq\mathcal F'$.** For non-nested classes a bigger class can move *away* from the truth.

**The fix.** A residual block computes

$$\mathbf y=\mathbf x+g(\mathbf x)$$

so **setting $g\equiv0$ recovers the identity**, and the shallower network is contained in the deeper one **by construction**.

> [!warning] ⚠️ That is the entire idea, and it is a statement about *function classes*, not about gradients
> The popular explanation — "the skip connection lets the gradient flow" — is true and is **not** D2L's argument. **The argument is that $\mathcal F_{\text{shallow}}\subseteq\mathcal F_{\text{deep}}$, so adding layers can no longer make the network strictly worse.**
>
> **And learning $g(\mathbf x)=f(\mathbf x)-\mathbf x$ is easier than learning $f$ when $f$ is near-identity**: you only need to push the weights toward zero, which is exactly what weight decay already does.
>
> ⇒ *a residual block is a special case of an Inception block in which one branch is the identity.*

**The architecture**: a GoogLeNet-style stem ($7\times7$ s2, 64 channels, BN, ReLU, $3\times3$ max-pool s2), then four modules of residual blocks, each **doubling the channels and halving the resolution**, then global average pooling and one fully connected layer. Two blocks per module gives $4\times4+1+1=\mathbf{18}$ layers — **ResNet-18**. *(Shapes verified against D2L's printout: $64\times24\times24\to64\times24\times24\to128\times12\times12\to256\times6\times6\to512\times3\times3\to10$ on a $96\times96$ input.)*

**Note what ResNet inherited: VGG's all-$3\times3$ design, GoogLeNet's stem and global-average-pool head, and NiN's refusal of a fully connected body.**

### 15. ResNeXt — grouped convolutions

The tension: more channels carry more information but cost $O(c_ic_o)$ — **quadratic**. **Grouped convolution** splits the channels into $g$ groups and convolves within each:

$$c_i\cdot c_o\ \longrightarrow\ g\cdot\frac{c_i}{g}\cdot\frac{c_o}{g}=\frac{c_ic_o}{g}$$

| $g$ | parameters ($c_i=c_o=256$) | reduction |
|---|---|---|
| 1 | 65,536 | 1× |
| 4 | 16,384 | **4×** |
| 32 | 2,048 | **32×** |

**$g$ times fewer parameters *and* $g$ times fewer FLOPs — D2L states both correctly.** The cost is that **no information crosses groups**, which is why the ResNeXt block sandwiches the grouped $3\times3$ **between two $1\times1$ convolutions** — cheap layers whose only job is to mix channels.

*(A historical footnote worth keeping: grouped convolution was **invented by accident** — AlexNet split channels across two GPUs for memory reasons "with no ill effects," and it took five years for anyone to notice this was a good idea on its own merits.)*

### 16. DenseNet — concatenate instead of add

ResNet decomposes $f(\mathbf x)=\mathbf x+g(\mathbf x)$ — a linear term plus a nonlinear correction, in the spirit of a Taylor expansion. **DenseNet asks what happens if you keep every term instead of adding them:**

$$\mathbf x\to[\mathbf x,\ f_1(\mathbf x),\ f_2([\mathbf x,f_1(\mathbf x)]),\ f_3([\mathbf x,f_1(\mathbf x),f_2([\mathbf x,f_1(\mathbf x)])]),\ \dots]$$

**Every layer receives the concatenated outputs of all preceding layers.** A **dense block** of $n$ convolutions at **growth rate** $k$ takes $c_0$ channels to $c_0+nk$. *(D2L's example: $3+10+10=23$ — **verified against the printed `torch.Size([4, 23, 8, 8])`**.)*

> [!warning] ⚠️ CHANNELS GROW LINEARLY AND PARAMETERS GROW **QUADRATICALLY** — and that is why transition layers exist
> Block $i$ must **read** $c_0+(i-1)k$ channels and writes $k$, so it costs $9k\big(c_0+(i-1)k\big)$ — linear in $i$, hence **quadratic in total**:
> $$\text{total}=9k\left[nc_0+\frac{kn(n-1)}{2}\right]$$
>
> At $c_0=64$, $k=32$: **$n=4$ → 129,024 params; $n=8$ → 405,504; $n=16$ → 1,400,832.** Doubling the depth of a dense block **more than triples** its cost.
>
> **A transition layer** ($1\times1$ conv halving the channels + average pool s2) after $n=8$ takes $320\to160$ channels for 51,360 parameters, and **makes the next block's first convolution 2.0× cheaper**.
>
> ⇒ **D2L says the expansion "can be quite high-dimensional" and never shows the quadratic.** *That quadratic is the entire reason DenseNet needs transition layers and ResNet does not — addition keeps the channel count fixed, concatenation does not.*

### 17. ⚠️ THE ORGANIZING RESULT: PARAMETERS AND COMPUTATION LIVE IN OPPOSITE HALVES

D2L presents these architectures one after another and **never puts them in one table.** Here it is, both ways:

| network | parameters | **conv share of params** | multiply-adds | **conv share of FLOPs** |
|---|---|---|---|---|
| **LeNet** | 61,706 | **4.2%** | 416,520 | **85.9%** |
| **AlexNet** | 46,764,746 | **8.0%** | 938,146,176 | **95.4%** |
| **VGG-11** | 128,806,154 | **7.2%** | 7,547,232,256 | **98.4%** |

> [!warning] ⚠️ THE INVERSION, AND ITS ONE-LINE CAUSE
> **In all three networks the convolutions hold under 8% of the parameters and over 85% of the computation; the fully connected head holds over 92% of the parameters and under 15% of the computation.**
>
> **Why:** a convolutional layer's $k^2c_ic_o$ weights are **reused at every one of the $h\times w$ positions**, so its FLOPs are $h\cdot w$ times its parameter count. A fully connected layer uses each weight **exactly once**, so its FLOPs *equal* its parameter count.
>
> **Measured, in multiply-adds per parameter:**
>
> | layer | params | mult-adds | **per parameter** |
> |---|---|---|---|
> | VGG conv1 | 640 | 28,901,376 | **45,158** |
> | VGG conv4 | 590,080 | 1,849,688,064 | **3,135** |
> | VGG conv8 | 2,359,808 | 462,422,016 | 196 |
> | **VGG fc1** | **102,764,544** | 102,760,448 | **1.0** |
> | **VGG fc2** | 16,781,312 | 16,777,216 | **1.0** |
> | LeNet conv1 | 156 | 117,600 | 754 |
> | **LeNet fc1** | 48,120 | 48,000 | **1.0** |
>
> **Exactly 1.0 for every fully connected layer, in every network. That is the signature of a weight used once.**
>
> ⇒ ***"convolutional neural network" describes where the arithmetic is, not where the weights are.*** ⇒ **and it explains the whole architectural history of §8–§16:** to make a network *smaller* you attack the head (NiN, global average pooling, §11); to make it *faster* you attack the convolutions (grouped convolutions, §15; $1\times1$ bottlenecks, §12).
>
> **They are different problems with different solutions, and confusing them is how people optimize the wrong thing.**

## ✏️ Exercises

> [!example]- Exercise 1 — shapes, and why kernels are odd
> **(a)** Trace $1\times1\times32\times32$ through: conv $5\times5$ (no padding) → max-pool $2\times2$ s2 → conv $3\times3$ pad 1 → max-pool $2\times2$ s2.
> **(b)** What padding preserves the size for kernel $k$ at stride 1? Why does that force $k$ odd?
> **(c)** Verify D2L's unanswered exercise 7.3.1: kernel $(3,5)$, padding $(0,1)$, stride $(3,4)$ on $8\times8$.
>
> ---
> **(a)** Using $\lfloor(n-k+p+s)/s\rfloor$:
>
> | layer | in → out |
> |---|---|
> | conv $5\times5$, $p=0$, $s=1$ | $32\to\mathbf{28}$ |
> | pool $2\times2$, $s=2$ | $28\to\mathbf{14}$ |
> | conv $3\times3$, $p=2$, $s=1$ | $14\to\mathbf{14}$ |
> | pool $2\times2$, $s=2$ | $14\to\mathbf{7}$ |
>
> Final: $c\times7\times7$.
>
> **(b)** $p_{\text{total}}=k-1$. Split evenly that is $(k-1)/2$ per side — **an integer only when $k$ is odd**. Verified for $k=1,3,5,7,11$: each returns $8\to8$. For even $k$ you must pad $\lceil p/2\rceil$ on one side and $\lfloor p/2\rfloor$ on the other, so the output at $[i,j]$ is **no longer the window centred on the input at $[i,j]$** — a bookkeeping nuisance forever after.
>
> **(c)** Height: $\lfloor(8-3+0+3)/3\rfloor=\lfloor8/3\rfloor=2$. Width: $\lfloor(8-5+2+4)/4\rfloor=\lfloor9/4\rfloor=2$. **$2\times2$ — which is exactly the printed `torch.Size([2, 2])`.** ✓

> [!example]- Exercise 2 — measure weight sharing
> For each layer, compute the convolutional parameter count and the parameter count of a fully connected layer producing the *same output shape from the same input*.
> **(a)** LeNet conv1: $1\to6$, $5\times5$, output $6\times28\times28$ from $784$ inputs.
> **(b)** VGG conv1: $1\to64$, $3\times3$, output $64\times224\times224$.
> **(c)** What does the ratio equal, and why?
>
> ---
> | layer | conv params | fc equivalent | **ratio** |
> |---|---|---|---|
> | LeNet conv1 | **156** | 3,692,640 | **23,671×** |
> | VGG conv1 | **640** | 161,131,593,728 | **251,768,115×** |
> | AlexNet conv2 | 614,656 | 11,230,815,232 | **18,272×** |
>
> **(c)** The ratio is essentially $h\cdot w$ — the number of positions each weight is reused at — modified by the fan-in restriction $c_ik^2/n_{\text{in}}$. **For LeNet conv1, $h\cdot w=784$ and the measured ratio is 23,671**, the extra factor being that the convolution reads only 25 inputs per output while the fully connected layer reads all 784.
>
> ⚠️ **VGG's first layer would need 161 billion parameters as a fully connected layer — 644 GB in `float32`.** It has 640. *That is §1's $10^{10}$ argument on a real network, and it is why the fully connected head (§17) is the part that got deleted first.*

> [!example]- Exercise 3 — is a big kernel ever worth it?
> **(a)** How many $3\times3$ convolutions give the receptive field of one $k\times k$?
> **(b)** Compare parameters at $c=64$ channels for $k=5,7,11$.
> **(c)** What else do you gain, and what do you lose?
>
> ---
> **(a)** Each stride-1 $3\times3$ adds 2 to the receptive field, so $L=(k-1)/2$ layers give RF $=1+2L=k$.
>
> **(b)** At $c=64$:
>
> | RF | $L$ | stacked $3\times3$ | single $k\times k$ | **saving** |
> |---|---|---|---|---|
> | $5\times5$ | 2 | 73,728 | 102,400 | **28.0%** |
> | $7\times7$ | 3 | 110,592 | 200,704 | **44.9%** |
> | $11\times11$ | 5 | 184,320 | 495,616 | **62.8%** |
>
> **(c) Gain**: $L$ nonlinearities instead of 1 — strictly more expressive. **Lose**: $L$ times the *activation* memory (each intermediate must be stored for backprop — [[04 - Neural Network|ch. 04]] §5), $L$ sequential kernel launches instead of 1, and slightly more total FLOPs per unit of receptive field at small $k$.
>
> ⇒ **the parameter and expressiveness arguments both favour stacking; only latency and activation memory favour the big kernel.** *That is why AlexNet's $11\times11$ vanished immediately and never came back — until 2022, when abundant compute made it worth re-testing.*

> [!example]- Exercise 4 — find the inversion yourself, then fix the wrong half
> A network on $3\times64\times64$: conv $3\to32$ $3\times3$ p1 → pool s2 → conv $32\to64$ $3\times3$ p1 → pool s2 → flatten → fc $16384\to256$ → fc $256\to10$.
> **(a)** Parameters and multiply-adds per layer.
> **(b)** Which half holds the parameters? Which holds the computation?
> **(c)** Replace the fully connected head with global average pooling. What happens to each?
>
> ---
> **(a)**
>
> | layer | params | mult-adds | shape |
> |---|---|---|---|
> | conv1 | 896 | 3,538,944 | $32\times64\times64$ |
> | pool | 0 | 0 | $32\times32\times32$ |
> | conv2 | 18,496 | 18,874,368 | $64\times32\times32$ |
> | pool | 0 | 0 | $64\times16\times16$ |
> | **fc1** | **4,194,560** | 4,194,304 | 256 |
> | fc2 | 2,570 | 2,560 | 10 |
>
> **(b)** conv: **19,392 params (0.5%)** and **22,413,312 mult-adds (84.2%)**. fc: **4,197,130 params (99.5%)** and **4,196,864 mult-adds (15.8%)**. **The inversion, on a network you just built.**
>
> **(c)** Global average pooling over the $64\times16\times16$ block, then $64\to10$:
> - **parameters: 4,216,522 → 20,042, a $\mathbf{210.4\times}$ reduction**
> - **computation: 26,610,176 → 22,413,952 mult-adds, a change of $\mathbf{-15.8\%}$**
>
> ⚠️ **A 210× smaller network that does 84% as much arithmetic.** ⇒ ***that is NiN's contribution in one experiment, and it is why §17's inversion is worth knowing: optimizing parameters and optimizing FLOPs are different problems and they act on different layers.***

> [!example]- Exercise 5 — DenseNet's quadratic, and what a transition layer buys
> Dense block, growth rate $k=32$, starting from $c_0=64$, $3\times3$ convolutions.
> **(a)** Channels and parameters after $n$ convolutions.
> **(b)** Closed form for the total. Why is it quadratic?
> **(c)** Insert a transition layer halving the channels after $n=8$. What does it cost and what does it save?
>
> ---
> **(a)**
>
> | $n$ | channels | params of block $n$ | cumulative |
> |---|---|---|---|
> | 1 | 96 | 18,432 | 18,432 |
> | 4 | 192 | 46,080 | 129,024 |
> | 8 | **320** | 82,944 | **405,504** |
>
> **(b)** Block $n$ reads $c_0+(n-1)k$ channels and writes $k$, costing $9k\big(c_0+(n-1)k\big)$ — **linear in $n$**. Summing a linear sequence gives
> $$\text{total}=9k\left[nc_0+\frac{kn(n-1)}{2}\right]$$
> **Verified: $n=4\to129{,}024$; $n=8\to405{,}504$; $n=16\to1{,}400{,}832$.** Channels grow **linearly** ($c_0+nk$) while parameters grow **quadratically** — doubling $n$ from 8 to 16 multiplies the cost by **3.45×**.
>
> **(c)** A $1\times1$ convolution $320\to160$ costs $\mathbf{51{,}360}$ parameters. The next dense block's first convolution then costs **46,080 instead of 92,160 — 2.0× cheaper** — and every subsequent block in it starts 160 channels lower.
>
> ⇒ ***the transition layer pays for itself within two blocks, and that is what "control the complexity of the model" means in numbers.*** **This is also the structural reason ResNet needs no such device: addition keeps the channel count fixed; concatenation does not.**

## 📝 Summary

- **Two assumptions — translation invariance and locality — take a layer from $10^{12}$ parameters to $100$, a factor of $\mathbf{10^{10}}$.** D2L gives all three numbers and never multiplies the reductions. The price is an inductive bias that fails wherever absolute position matters.
- **What deep learning calls convolution is cross-correlation**, and the distinction is unobservable because the kernel is learned. D2L's $[1,-1]$ edge kernel **is a finite-difference operator**, vanishes on the transposed image, and is **rediscovered from data in 10 gradient steps** as $[0.9797,-0.9816]$.
- **Output shape is $\lfloor(n-k+p+s)/s\rfloor$**; all five of D2L's printed shapes reproduce, including the unanswered exercise ($2\times2$). **Kernels are odd so that size-preserving padding is symmetric.**
- **Channels are where expressiveness returns** after locality removes it — at a cost of $h\cdot w\cdot k^2\cdot c_ic_o$, so **doubling both channel counts quadruples the work.** D2L's 53-billion-operation figure verifies exactly. **A $1\times1$ convolution is a fully connected layer per pixel with weights tied across positions.**
- **⚠️ Depth is how a local operator becomes global.** One $3\times3$ sees 9 pixels; VGG-11's eight, with five poolings, see **$150\times150$ — 67% of the image**. **Strides matter more than layers**: the receptive field grows geometrically in downsampling steps, only linearly in depth.
- **⚠️ LeNet is 95.8% fully connected by parameter count**, and its first convolution replaces a fully connected layer **23,671×** larger. **AlexNet 94.0%, VGG-11 92.8%.**
- **⚠️ ONE MATRIX IS 79.8% OF VGG-11** — $25{,}088\times4096=102{,}764{,}544$ parameters $=\mathbf{392.0}$ MB, verifying D2L's "almost 400MB" to the digit, and **11.1× larger than all eight convolutional layers combined.**
- **⚠️ NiN deletes exactly that matrix and is 64.7× smaller than VGG-11** with zero fully connected parameters — **and the accuracy did not fall.** In a controlled test, swapping a head for global average pooling cut a network **210.4×** while reducing computation only **15.8%**.
- **⚠️ THE ORGANIZING RESULT: parameters and computation live in opposite halves.** Convolutions hold **<8% of parameters and >85% of FLOPs**; the head holds **>92% of parameters and <15% of FLOPs**. **FLOPs per parameter is $h\cdot w$ for a convolution and exactly 1.0 for a fully connected layer** — verified across all three networks.
- **VGG's $3\times3$ stacking wins on both axes**: three of them match one $7\times7$ with **44.9% fewer parameters and three nonlinearities instead of one** (62.8% at $11\times11$). **⚠️ D2L's "(39c2)" is $3\times9c^2=27c^2$ — a deleted multiplication sign, proved by $27/25=1.08$ being "approximately" and $39/25=1.56$ not being.**
- **⚠️ Batch normalization's regularization is the $1/\sqrt{|\mathcal B|}$ law again** — its unexplained "best in the 50–100 range" is where batch noise is 14.1%–10.0%. **It cannot work at $|\mathcal B|=1$** (output exactly 0, verified). **Raising the batch size to train faster silently weakens the regularization.**
- **ResNet's argument is about function classes, not gradients**: $\mathbf y=\mathbf x+g(\mathbf x)$ with $g\equiv0$ gives the identity, so $\mathcal F_{\text{shallow}}\subseteq\mathcal F_{\text{deep}}$ **by construction** — the guarantee plain stacking lacks. **ResNeXt's grouped convolution divides both parameters and FLOPs by $g$**, at the cost of no cross-group information.
- **⚠️ DenseNet's channels grow linearly and its parameters grow quadratically** ($9k[nc_0+kn(n-1)/2]$) because block $i$ must read everything before it. **That quadratic is why transition layers exist and why ResNet needs none.**

## ⚠️ Important Notes

1. **⚠️ A new cipher entry: the multiplication sign is deleted in VGG's parameter argument.** `(39c2)` is $3\times9c^2=27c^2$, not $39c^2$. **Caught by arithmetic, not by reading** — the surrounding word "approximately" is only true for 27. Added to this subject's `CLAUDE.md`. *The standing rule holds: never transcribe a formula; reconstruct it and check it numerically.*
2. **⚠️ Padding and stride defaults differ between convolution and pooling.** Convolution defaults to stride 1; **pooling defaults its stride to the window size** (`nn.MaxPool2d(3)` has stride 3). Silently downsampling by 3× instead of 1× is the vault's recurring **plausible wrong answer with no error**.
3. **⚠️ Report the receptive field, not the depth.** Two networks with the same layer count can have wildly different receptive fields depending on where the strides are. **A network whose receptive field is smaller than the object it must recognize cannot recognize it, at any width or training budget.**
4. **⚠️ Distinguish "make it smaller" from "make it faster" — §17.** They act on opposite halves of the network. Pruning convolutions to save memory, or shrinking the classifier head to save time, is optimizing the wrong layer.
5. **⚠️ Translation invariance is an *assumption* and it is sometimes false.** Face alignment, document layout, board games and medical images with fixed anatomy all carry information in absolute position. **A CNN can only recover position from the padding artefacts** — which is why position encodings exist.
6. **⚠️ Batch normalization makes the output depend on the other examples in the batch.** Train/test behaviour differs (batch vs dataset statistics), $|\mathcal B|=1$ destroys the signal, and **changing the batch size changes the regularization strength.** Any benchmark that varies the batch size is varying two things at once.
7. **⚠️ Channels do not map one-to-one onto interpretable features.** D2L is explicit: "some *direction in channel space* corresponds to detecting edges." **Reading channel $k$ as "the edge detector" is the same error as reading a single weight in [[02 - Linear Regression|ch. 02]].**
8. **⚠️ The convolution/cross-correlation distinction only bites at the boundary with signal processing.** Inside a trained network it is unobservable; **importing a kernel from a textbook, or exporting one, requires the flip.**
9. **⚠️ Max-pooling cannot be written as a convolution** (D2L's exercise 7.5.2) — convolution is linear and max is not. It *can* be built from ReLUs, since $\max(a,b)=a+\mathrm{ReLU}(b-a)$. *Average pooling, by contrast, is exactly a convolution with a constant kernel.*
10. **⚠️ Global average pooling discards spatial position on purpose.** That is a *feature* for classification and **a bug for anything localizing** — which is precisely why [[06 - Object Detection|ch. 06]]'s detectors keep the spatial map instead.
11. **⚠️ The "1 GB" and "400 MB" claims illustrate opposite failure modes.** VGG's 392.0 MB is **exactly right**; AlexNet's "nearly 1 GB" is right only about the **training footprint** (208 MB × 4 = 832 MB), not the parameters. **Always ask whether a memory figure counts weights, weights + gradients, or the optimizer state too** — [[04 - Neural Network|ch. 04]] §5.
12. **⚠️ Depth was never blocked by ideas.** LeNet (1995) and AlexNet (2012) share almost every architectural element. **What changed was data (60,000 → 1.2M), resolution ($28^2$ → $224^2$), hardware (CPU → 3 TFLOPs), ReLU, dropout and initialization** — exactly the resource argument of [[01 - Introduction to Deep Learning|ch. 01]] and the trainability argument of [[04 - Neural Network|ch. 04]] §8.
13. **⚠️ Grouped convolution was discovered by accident.** AlexNet split channels across two GPUs for memory reasons; ResNeXt formalized it five years later. **Worth remembering when an implementation constraint looks like it is only a constraint.**
14. **A residual block is an Inception block with an identity branch, and DenseNet is a residual block that concatenates instead of adding.** The three "distinct" architectures are one design space, and D2L presents them as a chronology rather than a family.
15. **Odd kernel sizes, all-$3\times3$ bodies, stem/body/head, global average pooling, BN-then-ReLU, and doubling channels while halving resolution** are the six conventions that survived from this chapter into everything built since. **None is a theorem; all are defaults worth knowing you can break.**

> [!warning] Gaps in the source material
> **All figures are images and never extract**, and these two chapters are the most figure-dependent in the book. **Recovered because the prose states their entire content**: Fig. 7.2.1 (the $19/25/37/43$ cross-correlation), Fig. 7.3.2 and 7.3.3 (padding and stride), Fig. 7.4.1 and 7.4.2 (multi-channel and $1\times1$), Fig. 7.5.1 (max-pooling), Fig. 7.6.1–7.6.2 (LeNet's data flow — every shape is in the printed `layer_summary`), Fig. 8.4.1 (the Inception block — all four branches are named in the prose), Fig. 8.6.2 (the residual block), Fig. 8.7.1–8.7.2 (DenseNet's concatenation). **Genuinely lost**: Fig. 7.1.1–7.1.2 (Waldo), Fig. 7.2.2 (Field 1987's biological filters), Fig. 8.1.1 (AlexNet's learned first-layer filters), Fig. 7.3.1 (the pixel-utilization heat maps), and **Fig. 8.6.1 (the nested-vs-non-nested function-class diagram)**, whose content is genuinely geometric — §14 reconstructs the *argument* from the prose but not the picture. **All training curves are lost**, which is why this chapter reports no accuracies.
>
> **Code listings lose their indentation** and were re-derived from the logic; **printed code *outputs* extract intact**, which is what made every verification in §2, §3, §4, §6, §8 and §9 possible.
>
> **One new cipher entry**, recorded in this subject's `CLAUDE.md`: **the multiplication sign is deleted in `(39c2)` = $3\times9c^2$** (§10), joining the known `1 1` = $1\times1$.
>
> **Added beyond D2L, and labelled as mine throughout:**
> - **The three ratios of the parameter cascade** and the $10^{10}$ total (§1). D2L states the endpoints and only ever divides consecutive pairs.
> - **The parameter counts of LeNet, AlexNet, VGG-11 and NiN, and the whole of §17's parameter/FLOP inversion table** — including the "multiply-adds per parameter" column and the observation that it is **exactly 1.0** for every fully connected layer. **D2L gives no parameter count for any architecture in either chapter.**
> - **The weight-sharing ratios** (23,671× for LeNet conv1; 251,768,115× for VGG conv1) in §8 and exercise 2.
> - **The full receptive-field trace** of §7 with the jump recursion, and the observation that LeNet's RF (32) exceeds its input (28).
> - **The $3\times3$ stacking table** of §10 beyond D2L's single $5\times5$ case, including the ReLU column and the $c=64$ instantiation.
> - **The resolution of the "nearly 1GB" discrepancy** (§9) as $4\times$ the parameter memory, connecting it to ch. 04's optimizer-state finding.
> - **The $1/\sqrt{|\mathcal B|}$ table for batch normalization** (§13) and the identification of D2L's "50–100 range" with 14.1%–10.0% relative noise. **D2L asserts the range and computes nothing.**
> - **The DenseNet quadratic** $9k[nc_0+kn(n-1)/2]$ and the transition-layer cost/benefit (§16, exercise 5) — D2L says only "can be quite high-dimensional".
> - **The answer to exercise 7.3.1** (§3), **the odd-kernel argument** (§3, exercise 1), and the **$\max(a,b)=a+\mathrm{ReLU}(b-a)$** identity (Important Note 9) — all D2L exercises left unanswered.
> - **The $\log_2 224=7.807$ correction** to D2L's "more than 8 convolutional layers" (§10).
> - **The exercise-4 experiment** showing a 210.4× parameter reduction for a 15.8% computation reduction.
>
> **One discrepancy investigated and DECLINED** (§9, logged in [[00-Index]] as **D8**): D2L's "these layers require nearly 1GB model parameters" for AlexNet's two 4096-output layers, which are **54,534,144 parameters = 208.0 MB in fp32, 4.9× less**. **Ruled out**: own extraction (the sentence is clean prose, no deleted glyphs), own arithmetic (recomputed three ways; the total agrees with the widely quoted ~60M for AlexNet), an abridged specification (both the $9216$ and D2L's $6400$ flattening give the same order), and alternative conventions — **and the alternative convention is what resolves it: weights + gradients + two Adam moments is $4\times208.0=832.1$ MB, "nearly 1GB".** The claim is true of the training footprint and false of the parameters. **Recorded as an imprecision, not an error.**
>
> **Deliberately deferred, not omitted:** D2L §7.6.2, §8.1.3, §8.2.3, §8.3.3, §8.4.3, §8.5.4, §8.6.4 and §8.7.5 are **training runs on Fashion-MNIST whose only output is a lost figure** — no accuracies are quoted here because none survived extraction. **§8.8 (AnyNet / RegNet design spaces)** is a semi-automatic architecture-search method that belongs with hyperparameter optimization, which [[00-Index]] records as out of scope. **Image augmentation and fine-tuning (D2L §14.1–14.2) are held for [[06 - Object Detection|ch. 06]]**, where they are the first two sections.
>
> **Left as the source states it:** all citations (LeCun et al. 1995/1998, Krizhevsky et al. 2012, Simonyan & Zisserman 2014, Lin et al. 2013, Szegedy et al. 2015, Ioffe & Szegedy 2015, He et al. 2016, Xie et al. 2017, Huang et al. 2017, Fukushima 1982, Hubel & Wiesel, Field 1987, Waibel et al. 1989, Zeiler & Fergus 2013, Graham 2014, Liu et al. 2022, and the rest); the hardware figures (GeForce 256 at 480 MFLOPS, GTX 580 at 1.5 TFLOPs, A100 at 300 TFLOPs BF16), which are external and unverifiable here; the claim that ATMs still ran LeCun and Bottou's 1990s code; and the assertion that max-pooling is "in almost all cases preferable to average pooling", which is an empirical claim the chapter does not test.

**Previous:** [[04 - Neural Network]] · **Next:** [[06 - Object Detection]]
