---
subject: Deep Learning
chapter: 5
tags: [ds, deep-learning, cnn, convolution, pooling, receptive-field, batch-normalization, resnet, densenet, architecture]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 7 (Convolutional Neural Networks) and ch. 8 (Modern Convolutional Neural Networks)"
---

# Convolutional Neural Network

D2L ch. 7 builds the convolution from first principles; ch. 8 goes through LeNet → AlexNet → VGG → NiN → GoogLeNet → batch norm → ResNet → ResNeXt → DenseNet. All printed shapes and worked examples below were recomputed and match the book.

## 📘 Main Knowledge

### 1. From an MLP to a convolution

A one-megapixel image into a dense layer of 1,000 units needs $10^9$ parameters (3.7 GB in float32) for one layer. Treat input and hidden layer as $1000\times1000$ grids, so the weights form a fourth-order tensor:
$$[\mathsf H]_{i,j}=[\mathsf U]_{i,j}+\sum_a\sum_b[\mathsf V]_{i,j,a,b}[\mathsf X]_{i+a,\,j+b}$$
(writing input positions as offsets $a,b$ from the output position).

1. **Translation invariance**: a shifted input gives a shifted output, so $\mathsf V$ and $\mathsf U$ cannot depend on $(i,j)$.
2. **Locality**: only offsets with $|a|,|b|\le\Delta$ matter.

$$[\mathsf H]_{i,j}=u+\sum_{a=-\Delta}^{\Delta}\sum_{b=-\Delta}^{\Delta}[\mathsf V]_{a,b}[\mathsf X]_{i+a,\,j+b}$$

This is a convolutional layer; $\mathsf V$ is the kernel (filter).

| | parameters | reduction |
|---|---|---|
| full tensor | $10^{12}$ | |
| + translation invariance | $4\times10^6$ | 250,000× |
| + locality ($\Delta=5$, $11\times11$ kernel) | 100 | 40,000× |

In total, two assumptions reduce the parameter count by $10^{10}$. D2L stresses that this is an inductive bias: if images were not translation invariant, the model could fail even to fit the training data. Position matters in tasks like face alignment, document layout or board games, which is why later architectures add position encodings ([[08 - Sequence to Sequence|ch. 08]]).

D2L's intuition: what Waldo looks like does not depend on where Waldo is, so sweep one detector over every patch.

### 2. Cross-correlation

True convolution flips the kernel: $(f*g)(i,j)=\sum_a\sum_b f(a,b)\,g(i-a,j-b)$. Deep learning layers compute cross-correlation ($i+a$, $j+b$). Since the kernel is learned, the network just learns the flipped kernel, so the difference is invisible inside a trained model. It matters only when importing kernels from signal processing.

Example:

| $\mathsf X$ | $\mathsf K$ | output |
|---|---|---|
| $\begin{pmatrix}0&1&2\\3&4&5\\6&7&8\end{pmatrix}$ | $\begin{pmatrix}0&1\\2&3\end{pmatrix}$ | $\begin{pmatrix}19&25\\37&43\end{pmatrix}$ |

e.g. $0\cdot0+1\cdot1+3\cdot2+4\cdot3=19$.

**Edge detection.** Kernel $[1,-1]$ on a $6\times8$ image with a black middle stripe gives $+1$ at white→black edges and $-1$ at black→white, 0 elsewhere (row: $[0,1,0,0,0,-1,0]$). It is a finite difference, $x_{i,j}-x_{i,j+1}$, so it finds vertical edges only: on the transposed image its output is all zero. One kernel detects one direction, which is why layers have many channels. D2L then learns a kernel from the input/output pair: after 10 steps it is $[0.9797, -0.9816]$, close to $[1,-1]$.

### 3. Padding, stride and output size

Without padding, each layer shrinks the image by $k-1$ (ten $5\times5$ layers take $240\times240$ to $200\times200$). With total padding $p$ and stride $s$:
$$\left\lfloor\frac{n-k+p+s}{s}\right\rfloor\quad\text{per dimension}$$

| configuration | computed | D2L prints |
|---|---|---|
| $k=3$, $p=2$, $s=1$, $n=8$ | 8 | `torch.Size([8, 8])` |
| $k=(5,3)$, $p=(4,2)$, $s=1$, $n=8$ | 8 | `torch.Size([8, 8])` |
| $k=3$, $p=2$, $s=2$, $n=8$ | 4 | `torch.Size([4, 4])` |
| $k=(3,5)$, $p=(0,2)$, $s=(3,4)$, $n=8$ | $\lfloor8/3\rfloor\times\lfloor9/4\rfloor=2\times2$ | `torch.Size([2, 2])` |

(The last row is D2L ex. 7.3.1.)

To keep the size you need $p=k-1$, i.e. $(k-1)/2$ per side, which is an integer only for odd $k$. That is why kernels are usually 1, 3, 5, 7: even kernels work but need asymmetric padding.

Corner pixels are covered by fewer windows than central ones; padding evens this out. Zero padding also lets a CNN pick up some absolute position information from where the borders are.

### 4. Channels

With $c_i$ input channels the kernel is $c_i\times k_h\times k_w$: cross-correlate each channel and sum. With $c_o$ outputs the kernel is $c_o\times c_i\times k_h\times k_w$. D2L's examples reproduce: $\begin{pmatrix}56&72\\104&120\end{pmatrix}$ for two input channels, plus $\begin{pmatrix}76&100\\148&172\end{pmatrix}$ and $\begin{pmatrix}96&128\\192&224\end{pmatrix}$ for the extra output channels.

D2L warns against reading channel $k$ as "the edge detector": channels are learned jointly, and an edge detector may be a direction in channel space.

Cost: $h\cdot w\cdot k^2\cdot c_i\cdot c_o$ multiply-adds. For $256\times256$, $k=5$, $c_i=c_o=128$ that is $53{,}687{,}091{,}200$ operations counting multiplies and adds separately ("over 53 billion"). Doubling both channel counts quadruples the cost.

### 5. $1\times1$ convolution

It sees no neighbours, so it only mixes channels: a fully connected $c_i\to c_o$ layer applied at every pixel with shared weights. Uses:
- change the channel count cheaply (Inception, ResNeXt, DenseNet transitions);
- add nonlinearity across channels (NiN).

With a nonlinearity between them, consecutive convolutions do not collapse into one ([[04 - Neural Network|ch. 04]] §1).

### 6. Pooling

A fixed window computing max or mean; no parameters. On $\mathsf X=0..8$ with a $2\times2$ window: max $\begin{pmatrix}4&5\\7&8\end{pmatrix}$, average $\begin{pmatrix}2&3\\5&6\end{pmatrix}$.

Purposes: downsampling ($2\times2$, stride 2 quarters the resolution) and local translation invariance (after the edge detector, $2\times2$ max-pooling still reports an edge shifted by one pixel). Pooling works per channel and does not change the channel count.

In PyTorch, pooling's stride defaults to the window size (`nn.MaxPool2d(3)` has stride 3), while convolution's defaults to 1.

### 7. Receptive field

The receptive field of a unit is the set of input pixels that can affect it:
$$\mathrm{RF}_{\text{out}}=\mathrm{RF}_{\text{in}}+(k-1)\cdot j,\qquad j_{\text{out}}=j_{\text{in}}\cdot s$$
where the jump $j$ is the input distance between neighbouring outputs.

VGG-11's body on $224\times224$:

| after | RF | jump |
|---|---|---|
| conv 3×3 | 3 | 1 |
| pool s2 | 4 | 2 |
| conv | 8 | 2 |
| pool | 10 | 4 |
| conv, conv | 18, 26 | 4 |
| pool | 30 | 8 |
| conv, conv | 46, 62 | 8 |
| pool | 70 | 16 |
| conv, conv | 102, 134 | 16 |
| pool | 150 | 32 |

One $3\times3$ sees 9 pixels; the whole body sees $150\times150$, 67% of the image. Without the poolings, eight $3\times3$ layers reach only 17. Receptive field grows geometrically with downsampling steps and linearly with plain depth. Depth plus striding is how local operations answer global questions. LeNet's receptive field (32) exceeds its 28×28 input.

### 8. LeNet

LeNet-5 (LeCun et al. 1998): two blocks of conv → sigmoid → average pool, then three dense layers. Under 1% error on digits; used in ATMs.

| layer | output | parameters |
|---|---|---|
| conv1 $1\to6$, $5\times5$, pad 2 | $6\times28\times28$ | 156 |
| avg-pool 2×2 s2 | $6\times14\times14$ | 0 |
| conv2 $6\to16$, $5\times5$ | $16\times10\times10$ | 2,416 |
| avg-pool 2×2 s2 | $16\times5\times5$ | 0 |
| fc1 $400\to120$ | 120 | 48,120 |
| fc2 $120\to84$ | 84 | 10,164 |
| fc3 $84\to10$ | 10 | 850 |

Total 61,706 parameters; the convolutions are only 4.17%. A dense layer from 784 inputs to conv1's 4,704 outputs would need 3,692,640 parameters, 23,671× more than conv1's 156: that ratio is the saving from weight sharing.

LeNet used sigmoid and average pooling because ReLU and max pooling had not yet been adopted. MNIST's $28\times28$ is a trimmed $32\times32$.

### 9. AlexNet (2012)

Five conv layers, two dense hidden layers, one output layer: close to LeNet in structure. What changed:

| | LeNet | AlexNet |
|---|---|---|
| activation | sigmoid | ReLU |
| pooling | average | max |
| regularization | weight decay | dropout, heavy augmentation |
| first kernel | $5\times5$ | $11\times11$ |
| channels | 6, 16 | 96, 256, 384, 384, 256 |
| data | 60,000 $28\times28$ | 1.2M $224\times224$, 1000 classes |
| hardware | CPU | two GTX 580s |

Before 2012 the pipeline was hand-crafted features (SIFT, SURF, HOG, bags of visual words) plus a linear or kernel model. AlexNet learned the features.

| | D2L's 1-channel, 10-class version | original 3-channel, 1000-class |
|---|---|---|
| conv layers | 3,723,968 (8.0%) | 3,747,200 (6.0%) |
| fc layers | 43,040,778 (92.0%) | 58,631,144 (94.0%) |
| total | 46,764,746 (178.4 MB) | 62,378,344 (238.0 MB) |

D2L says the two 4096-unit layers need "nearly 1GB". They have 54,534,144 parameters = 208.0 MB. With gradients and two Adam moments (4×) it is 832.1 MB, so the claim fits the training footprint, not the weights (declined discrepancy D8).

### 10. VGG (2014)

A VGG block is several $3\times3$ convolutions (padding 1) with ReLU, then a $2\times2$ max-pool, stride 2. VGG-11 has five blocks (1, 1, 2, 2, 2 convs; 64, 128, 256, 512, 512 channels) plus AlexNet's dense head.

Blocks separate depth from downsampling: if every conv were followed by pooling, a $224\times224$ input would allow only about $\log_2 224=7.8$ layers.

D2L: two $3\times3$ convs cover the same pixels as one $5\times5$, and one $5\times5$ ($25c^2$ parameters) costs about as much as three $3\times3$s. The PDF prints "(39c2)", which means $3\times9c^2=27c^2$ (the multiplication sign is lost; $27/25=1.08$ fits "approximately as many", $39/25$ would not).

$L$ stacked $3\times3$ layers have receptive field $1+2L$:

| receptive field | $L$ | stacked params | single kernel | saving | nonlinearities |
|---|---|---|---|---|---|
| $5\times5$ | 2 | $18c^2$ | $25c^2$ | 28.0% | 2 |
| $7\times7$ | 3 | $27c^2$ | $49c^2$ | 44.9% | 3 |
| $11\times11$ | 5 | $45c^2$ | $121c^2$ | 62.8% | 5 |

Stacks of small kernels have fewer parameters and more nonlinearities; only latency and activation memory favour one large kernel. (Liu et al. 2022 revisited large kernels.)

| VGG-11 | parameters | share |
|---|---|---|
| 8 conv layers | 9,219,328 | 7.2% |
| 3 fc layers | 119,586,826 | 92.8% |
| total | 128,806,154 | 491.4 MB |

The first dense layer, $25{,}088\times4096=102{,}764{,}544$ parameters = 392.0 MB, is 79.8% of the network, matching D2L's "almost 400MB". It is 11.1× larger than all conv layers together.

### 11. NiN (2013)

Two ideas:
1. $1\times1$ convolutions after each $k\times k$ convolution add per-pixel nonlinearity across channels.
2. **Global average pooling** replaces the dense head: the last block outputs one channel per class, and each channel is averaged over space to give the logits.

| network | parameters | MB | dense-layer share |
|---|---|---|---|
| LeNet | 61,706 | 0.2 | 95.8% |
| AlexNet (original) | 62,378,344 | 238.0 | 94.0% |
| VGG-11 | 128,806,154 | 491.4 | 92.8% |
| NiN | 1,992,166 | 7.6 | 0% |

NiN is 64.7× smaller than VGG-11 and 31.3× smaller than AlexNet. D2L notes that the averaging did not hurt accuracy. The dense head mainly learned where in the image evidence appeared, which classification does not need.

### 12. GoogLeNet (2014)

The Inception block runs four branches in parallel ($1\times1$; $1\times1$→$3\times3$; $1\times1$→$5\times5$; $3\times3$ max-pool→$1\times1$) and concatenates them along channels. Instead of choosing a kernel size, it uses several and lets training allocate channels. The $1\times1$ convolutions reduce channels before the expensive $3\times3$ and $5\times5$.

GoogLeNet also introduced the **stem / body / head** structure used since. Replacing only the head is the basis of fine-tuning in [[06 - Object Detection|ch. 06]].

### 13. Batch normalization (2015)

$$\mathrm{BN}(\mathbf x)=\boldsymbol\gamma\odot\frac{\mathbf x-\hat{\boldsymbol\mu}_{\mathcal B}}{\hat{\boldsymbol\sigma}_{\mathcal B}}+\boldsymbol\beta,\qquad \hat{\boldsymbol\mu}_{\mathcal B}=\frac{1}{|\mathcal B|}\sum_{\mathbf x\in\mathcal B}\mathbf x,\quad \hat{\boldsymbol\sigma}^2_{\mathcal B}=\frac{1}{|\mathcal B|}\sum_{\mathbf x\in\mathcal B}(\mathbf x-\hat{\boldsymbol\mu}_{\mathcal B})^2+\epsilon$$

Normalize with the minibatch's statistics, then rescale and shift with learned $\boldsymbol\gamma,\boldsymbol\beta$. In conv layers it is per channel over all positions. Usually placed after the affine/conv layer and before the activation.

Benefits: input standardization inside the network, more stable activations, and regularization through batch noise.

- With batch size 1 the output is exactly 0: the signal is gone.
- Batch statistics have relative noise about $1/\sqrt{|\mathcal B|}$: 14.1% at 50, 10.0% at 100 (D2L's recommended range), 4.4% at 512. Larger batches regularize less, so increasing the batch size to speed up training also weakens regularization (64 → 512 cuts the noise 2.83×).
- Training uses batch statistics; prediction uses running averages over the dataset, so an image's prediction does not depend on its batch.
- Cost: 2 parameters per channel.

### 14. ResNet (2015)

A bigger function class $\mathcal F'$ is only guaranteed to fit at least as well as $\mathcal F$ if $\mathcal F\subseteq\mathcal F'$. A residual block computes
$$\mathbf y=\mathbf x+g(\mathbf x)$$
With $g\equiv0$ it is the identity, so adding blocks cannot shrink the function class. D2L's argument is about nested function classes; the familiar "gradients flow through the skip" explanation is also true. Learning $g=f-\mathbf x$ is easy when $f$ is close to the identity: push weights toward zero.

ResNet-18: stem ($7\times7$ s2, 64 channels, BN, ReLU, $3\times3$ max-pool s2), four modules of two residual blocks each (each module doubles channels and halves resolution), global average pooling, one dense layer. On a $96\times96$ input the shapes are $64\times24\times24\to64\times24\times24\to128\times12\times12\to256\times6\times6\to512\times3\times3\to10$.

ResNet combines VGG's $3\times3$ convolutions, GoogLeNet's stem and pooled head, and NiN's lack of a dense body.

### 15. ResNeXt: grouped convolution

Splitting channels into $g$ groups and convolving within each group cuts parameters and FLOPs by $g$:
$$c_ic_o\ \to\ \frac{c_ic_o}{g}$$
At $c_i=c_o=256$: 65,536 → 16,384 ($g=4$) → 2,048 ($g=32$). No information crosses groups, so the grouped $3\times3$ sits between two $1\times1$ convolutions that mix channels. AlexNet split channels across two GPUs for memory reasons; ResNeXt made it a design choice.

### 16. DenseNet

Instead of adding, concatenate every previous output:
$$\mathbf x\to[\mathbf x,\ f_1(\mathbf x),\ f_2([\mathbf x,f_1(\mathbf x)]),\ \dots]$$
A dense block of $n$ convolutions with growth rate $k$ takes $c_0$ channels to $c_0+nk$ (D2L: $3+10+10=23$, matching `torch.Size([4, 23, 8, 8])`).

Channels grow linearly but parameters grow quadratically, since layer $i$ reads $c_0+(i-1)k$ channels:
$$\text{total}=9k\left[nc_0+\frac{kn(n-1)}{2}\right]$$
At $c_0=64$, $k=32$: 129,024 ($n=4$), 405,504 ($n=8$), 1,400,832 ($n=16$). **Transition layers** ($1\times1$ conv halving channels + average pool s2) control this. ResNet needs none because addition keeps the channel count fixed.

### 17. Where parameters and computation live

| network | parameters | conv share of params | multiply-adds | conv share of FLOPs |
|---|---|---|---|---|
| LeNet | 61,706 | 4.2% | 416,520 | 85.9% |
| AlexNet | 46,764,746 | 8.0% | 938,146,176 | 95.4% |
| VGG-11 | 128,806,154 | 7.2% | 7,547,232,256 | 98.4% |

Convolutions hold under 8% of the parameters and over 85% of the computation; dense layers the reverse. A conv weight is reused at all $h\times w$ positions, while a dense weight is used once:

| layer | params | mult-adds | per parameter |
|---|---|---|---|
| VGG conv1 | 640 | 28,901,376 | 45,158 |
| VGG conv4 | 590,080 | 1,849,688,064 | 3,135 |
| VGG conv8 | 2,359,808 | 462,422,016 | 196 |
| VGG fc1 | 102,764,544 | 102,760,448 | 1.0 |
| LeNet conv1 | 156 | 117,600 | 754 |
| LeNet fc1 | 48,120 | 48,000 | 1.0 |

To make a network smaller, shrink the head (NiN, global average pooling); to make it faster, shrink the convolutions (grouped convolutions, $1\times1$ bottlenecks). (This table is my compilation; D2L gives no parameter counts.)

## ✏️ Exercises

> [!example]- **1.** *(Easy) Shapes and odd kernels*
> **(a)** Trace $1\times1\times32\times32$ through conv $5\times5$ (no pad) → max-pool 2×2 s2 → conv $3\times3$ pad 1 → max-pool 2×2 s2. **(b)** Padding that preserves size, and why $k$ is odd. **(c)** D2L ex. 7.3.1: kernel (3,5), padding (0,1) per side, stride (3,4) on $8\times8$.
>
> ---
> **(a)** 32 → 28 → 14 → 14 → 7.
>
> **(b)** Total $p=k-1$, i.e. $(k-1)/2$ per side, an integer only for odd $k$. Even $k$ needs uneven padding, so outputs are no longer centred on inputs.
>
> **(c)** Height $\lfloor(8-3+0+3)/3\rfloor=2$, width $\lfloor(8-5+2+4)/4\rfloor=2$: $2\times2$, as printed.

> [!example]- **2.** *(Easy–medium) Weight sharing*
> Compare each conv layer's parameters with a dense layer producing the same output from the same input. **(a)** LeNet conv1. **(b)** VGG conv1 ($1\to64$, $3\times3$, output $64\times224\times224$). **(c)** What does the ratio roughly equal?
>
> ---
> | layer | conv params | dense equivalent | ratio |
> |---|---|---|---|
> | LeNet conv1 | 156 | 3,692,640 | 23,671× |
> | VGG conv1 | 640 | 161,131,593,728 | 251,768,115× |
> | AlexNet conv2 | 614,656 | 11,230,815,232 | 18,272× |
>
> **(c)** Roughly the number of positions $h\cdot w$ where each weight is reused, adjusted for the conv reading only $c_ik^2$ inputs per output. VGG conv1 as a dense layer would need 644 GB.

> [!example]- **3.** *(Medium) Big kernels vs stacks*
> **(a)** How many $3\times3$ layers match one $k\times k$? **(b)** Parameters at $c=64$ for $k=5,7,11$. **(c)** Gains and losses.
>
> ---
> **(a)** $L=(k-1)/2$.
>
> **(b)**
>
> | RF | $L$ | stacked | single | saving |
> |---|---|---|---|---|
> | 5 | 2 | 73,728 | 102,400 | 28.0% |
> | 7 | 3 | 110,592 | 200,704 | 44.9% |
> | 11 | 5 | 184,320 | 495,616 | 62.8% |
>
> **(c)** Gain: more nonlinearities, fewer parameters. Lose: more stored activations and more sequential layers (latency).

> [!example]- **4.** *(Medium–hard) Find the inversion, then fix the head*
> Input $3\times64\times64$: conv $3\to32$ 3×3 p1 → pool s2 → conv $32\to64$ 3×3 p1 → pool s2 → flatten → fc $16384\to256$ → fc $256\to10$.
> **(a)** Parameters and multiply-adds per layer. **(b)** Where are the parameters and the computation? **(c)** Replace the head with global average pooling + $64\to10$.
>
> ---
> **(a)**
>
> | layer | params | mult-adds |
> |---|---|---|
> | conv1 | 896 | 3,538,944 |
> | conv2 | 18,496 | 18,874,368 |
> | fc1 | 4,194,560 | 4,194,304 |
> | fc2 | 2,570 | 2,560 |
>
> **(b)** Conv: 19,392 params (0.5%), 22,413,312 mult-adds (84.2%). Dense: 4,197,130 params (99.5%), 4,196,864 mult-adds (15.8%).
>
> **(c)** Parameters 4,216,522 → 20,042 (210.4× smaller); computation 26,610,176 → 22,413,952 (−15.8%).

> [!example]- **5.** *(Hard) DenseNet growth*
> Growth rate $k=32$, $c_0=64$, $3\times3$ convs. **(a)** Channels and parameters after $n$ layers. **(b)** Closed form; why quadratic? **(c)** Add a transition halving channels after $n=8$.
>
> ---
> **(a)**
>
> | $n$ | channels | layer $n$ params | cumulative |
> |---|---|---|---|
> | 1 | 96 | 18,432 | 18,432 |
> | 4 | 192 | 46,080 | 129,024 |
> | 8 | 320 | 82,944 | 405,504 |
>
> **(b)** Layer $n$ costs $9k(c_0+(n-1)k)$, linear in $n$, so the sum is quadratic: $9k[nc_0+kn(n-1)/2]$. $n=16$ gives 1,400,832, 3.45× the $n=8$ cost.
>
> **(c)** $1\times1$ conv $320\to160$: 51,360 parameters. The next block's first conv costs 46,080 instead of 92,160.

## 📝 Summary

- Translation invariance + locality turn a $10^{12}$-parameter layer into a 100-parameter kernel ($10^{10}$×), at the cost of assuming position does not matter.
- "Convolution" in DL is cross-correlation; the difference does not matter for learned kernels. $[1,-1]$ is a finite-difference edge detector.
- Output size $\lfloor(n-k+p+s)/s\rfloor$; odd kernels allow symmetric padding.
- Cost $h\,w\,k^2c_ic_o$; $1\times1$ convs mix channels; pooling is parameter-free and per channel.
- Receptive field grows geometrically with strides: VGG-11's body sees 150×150 pixels.
- LeNet, AlexNet and VGG are over 92% dense-layer parameters; VGG's first dense layer alone is 392 MB. NiN removes the head with global average pooling and is 64.7× smaller.
- Stacking $3\times3$ kernels beats large kernels on parameters and nonlinearity.
- Batch norm: normalize per batch, then scale/shift; useless at batch size 1; its regularization weakens as batch size grows.
- ResNet: $\mathbf y=\mathbf x+g(\mathbf x)$ nests smaller models inside larger ones. ResNeXt: grouped convs divide cost by $g$. DenseNet: concatenation, quadratic parameter growth, transition layers.
- Parameters sit in the dense head, computation in the convolutions.

## ⚠️ Important Notes

1. `(39c2)` in the PDF means $3\times9c^2$. Reconstruct formulas, do not transcribe them.
2. Pooling's default stride equals its window size; convolution's is 1.
3. If the receptive field is smaller than the object, the network cannot recognize it.
4. Shrinking a model and speeding it up act on different layers (§17).
5. Translation invariance is an assumption; it fails when absolute position matters.
6. Batch norm output depends on the rest of the batch; changing batch size changes regularization.
7. Do not read one channel as one interpretable feature.
8. Kernels imported from signal processing need flipping.
9. Max pooling is not a convolution (it is nonlinear), but $\max(a,b)=a+\mathrm{ReLU}(b-a)$. Average pooling is a convolution with a constant kernel.
10. Global average pooling discards position: fine for classification, not for localization ([[06 - Object Detection|ch. 06]]).
11. Check whether a memory figure means weights only, or weights + gradients + optimizer state (AlexNet's "1 GB").
12. LeNet and AlexNet differ mainly in data, hardware, ReLU, dropout and initialization, not in architecture.
13. Residual, Inception and Dense blocks are variants of one idea: combine an identity/shortcut path with learned branches.

> [!warning] Gaps in the source material
> - **Figures:** diagrams of cross-correlation, padding, channels, pooling, LeNet, Inception, residual and dense blocks are reconstructed from the prose and printed shapes. Lost: Waldo images, biological filters, AlexNet's learned filters, pixel-usage heat maps, the nested function-class diagram, and all training curves (so no accuracies are reported).
> - **Cipher:** `(39c2)` = $3\times9c^2$ (the multiplication sign is deleted, like `1 1` = $1\times1$).
> - **Added by me:** the cascade ratios; all parameter counts and the §17 table; weight-sharing ratios; the receptive-field trace; the stacking table beyond $5\times5$; the AlexNet "1 GB" resolution (D8); the batch-norm noise table; the DenseNet formula; answers to D2L ex. 7.3.1, the odd-kernel question and ex. 7.5.3; the exercise-4 experiment.
> - **Skipped:** Fashion-MNIST training runs (their results are only in lost plots); §8.8 AnyNet/RegNet (architecture search, out of scope). Augmentation and fine-tuning are in [[06 - Object Detection|ch. 06]].
> - Hardware figures and historical claims are quoted from D2L.

**Previous:** [[04 - Neural Network]] · **Next:** [[06 - Object Detection]]
