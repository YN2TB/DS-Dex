---
subject: Computer Vision
chapter: 4
tags: [ds, computer-vision, neural-network, activation, backpropagation, convolution, pooling, receptive-field]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 04: From Neural Networks to CNNs (43 slides); Stanford CS231n notes (Neural Networks 1–3, Backpropagation, ConvNets)"
---

# From Neural Networks to CNNs

Week 4. Last week's linear classifier had two problems: one template per class (it can't separate rings or XOR) and it works on raw pixels. This lecture fixes both: first with **one nonlinearity** (neural networks), then with **one structural idea** (convolution). In between it covers activation functions and backpropagation.

For a longer treatment of the same material see [[Deep Learning/contents/04 - Neural Network|DL ch. 04]] (MLPs, backprop, initialisation) and [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]] (convolution and CNN architectures).

## 📘 Main Knowledge

### 1. Recap: what the linear model could and couldn't do (slide 4)

$$s = Wx, \qquad L = \frac1N \sum_i -\log p_{y_i} + \lambda \|W\|^2, \qquad W \leftarrow W - \eta \nabla_W L$$

| Worked | Didn't |
|---|---|
| fast at test time, no stored training set | one template per class (a left-facing and a right-facing cat must share it) |
| clean, cheap, checkable gradient | can't separate concentric rings or XOR |
| the training loop is reused all semester | operates on raw pixels |

### 2. Neural networks (slides 5–11)

**Adding a layer (slide 6):**

$$s = Wx \quad \longrightarrow \quad s = W_2\, \sigma(W_1 x)$$

- $W_1 \in \mathbb R^{H \times D}$, $W_2 \in \mathbb R^{C \times H}$.
- $H$ is the **hidden size**, typically 100–4096.
- $\sigma$ is a nonlinear function applied **elementwise** (to each number separately).
- The second layer is last week's linear classifier; the first layer transforms the input into new features.
- Three layers: $s = W_3\, \sigma(W_2\, \sigma(W_1 x))$, and so on.

**Without the nonlinearity, depth does nothing (slide 7).** Two stacked linear layers are *exactly* one linear layer: $W_2 (W_1 x) = (W_2 W_1) x = W' x$. *"$\sigma$ is not a detail bolted on for convenience — it is the only reason depth exists."*

**What the hidden layer buys (slide 8).** A two-layer net does what we did by hand last week (transform, then classify), except the transform is **learned**. A linear model gets one template per class; a two-layer net gets $H$ templates in its first layer and can **combine** them (e.g. "left-facing cat template OR right-facing cat template").

**Universal approximation (slide 9).** Cybenko (1989) and Hornik (1991): a network with **one hidden layer** and a suitable nonlinearity can approximate any continuous function on a bounded, closed domain to any accuracy, given enough hidden units.

What people take from it: "neural networks can represent anything." What it leaves open:
- **how many** hidden units are needed (possibly exponentially many);
- whether SGD can actually **find** that solution;
- whether it would **generalise** to new data if found.

*"Representation was never the bottleneck."* The hard part is finding a good function from finite data, which is why architecture (week 5) matters more than width.

**The neuron analogy, handle with care (slides 10–11).** A unit computes $h_j = \sigma\big(\sum_d W_{jd} x_d + b_j\big)$, loosely like a biological neuron: dendrites collect signals ($x_d$), synapses weight them ($W_{jd}$), the cell body sums them, the axon fires if the sum is large enough ($\sigma$). It's useful for intuition and naming, but it breaks down quickly: real neurons spike over time, have nonlinear dendrites and dozens of neurotransmitters, and aren't trained by gradient descent (there's no known biological mechanism for backpropagation). Don't use it to argue that a network will behave like a brain. (The first artificial neuron model was McCulloch–Pitts, 1943.)

### 3. Activation functions (slides 12–15)

**Sigmoid:**
$$\sigma(x) = \frac{1}{1 + e^{-x}}, \qquad \sigma'(x) = \sigma(x)\big(1 - \sigma(x)\big) \le \frac14$$
- Squashes to $(0, 1)$; historically read as a neuron's firing rate.
- **Saturates**: for $|x| > 5$ the gradient is essentially zero.
- **Not zero-centred**: outputs are always positive, so all gradients flowing into a unit's weights share the same sign, which makes updates zig-zag.

**Tanh:**
$$\tanh(x) = 2\sigma(2x) - 1, \qquad \tanh'(x) = 1 - \tanh^2(x) \le 1$$
- Zero-centred, so strictly better than sigmoid, but still saturates at both ends.

**ReLU (Rectified Linear Unit):**
$$\text{ReLU}(x) = \max(0, x), \qquad \text{ReLU}'(x) = \begin{cases} 1 & x > 0 \\ 0 & x < 0 \end{cases}$$
- **No saturation for $x > 0$**: the gradient is exactly 1.
- Cheap to compute, and converged several times faster than tanh in AlexNet (2012).
- Failure mode, **dying ReLU**: a unit whose input is negative for *every* example outputs 0 and gets zero gradient forever, so it can never recover. Usually caused by a large learning rate or a badly initialised, very negative bias.
- Fixes: **Leaky ReLU** ($\max(0.01x, x)$) keeps a small slope for $x < 0$ so the unit can recover; **ELU** and **GELU** smooth the corner. None of them saturate for $x > 0$.

**Why saturation kills deep networks (slide 15).** Backpropagation multiplies one factor per layer:

$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial h_n}\, \underbrace{\sigma'(\cdot) W_n \cdots \sigma'(\cdot) W_1}_{n \text{ factors}}$$

With sigmoid, every factor carries $\sigma' \le 1/4$. After $n$ layers the gradient is scaled by at most $4^{-n}$ (ignoring the weights):

| Layers $n$ | $4^{-n}$ |
|---|---|
| 5 | ≈ $10^{-3}$ |
| 10 | ≈ $10^{-6}$ |
| 20 | ≈ $10^{-12}$, numerically zero |

The early layers stop learning entirely. This is the **vanishing gradient** problem. ReLU's derivative of exactly 1 (for active units) is the main reason deep networks became trainable.

### 4. Backpropagation (slides 16–24)

**The problem (slide 17).** We need $\nabla_{W_1} L$ and $\nabla_{W_2} L$ for $L(W_2\, \sigma(W_1 x))$. Deriving by hand is tedious for two layers, impossible for fifty, and must be redone every time the architecture changes.

**The idea:** write the computation as a **graph of simple operations**. Each node only needs to know how to differentiate itself; the chain rule assembles the rest. One backward pass gives *every* partial derivative, at roughly the cost of one forward pass, however many parameters there are.

Note: the loss is a function of the **weights**. The input $x$ and label $y$ are constants. We differentiate with respect to $W$, not the data.

**The chain rule as a local rule (slide 18).** For a node with input $a$ and output $u$:

$$\underbrace{\frac{\partial L}{\partial a}}_{\text{downstream (sent back)}} = \underbrace{\frac{\partial L}{\partial u}}_{\text{upstream (received)}} \cdot \underbrace{\frac{\partial u}{\partial a}}_{\text{local (known)}}$$

Every node does the same two steps: receive the gradient from above, multiply by its own local derivative, pass it down. The node doesn't care whether $a$ is an image, an activation or a weight, which is why one backward pass produces all gradients at once.

**Example (slide 19):** $f(a,b,c) = (a+b)\cdot c$ with $a = -2$, $b = 5$, $c = -4$.
- Forward: $q = a + b = 3$, $f = q\,c = -12$.
- Local gradients: $\partial q/\partial a = \partial q/\partial b = 1$; $\partial f/\partial q = c$; $\partial f/\partial c = q$.
- Backward (start from $\partial f/\partial f = 1$): $\partial f/\partial c = q = 3$; $\partial f/\partial q = c = -4$; $\partial f/\partial a = \partial f/\partial b = -4 \times 1 = -4$.

**On an actual weight (slide 20).** One neuron with squared error, $L = (\sigma(wx + b) - y)^2$, with $w = 0.5$, $x = 2$, $b = -0.3$, $y = 1$:
- Forward: $z = 0.5 \cdot 2 - 0.3 = 0.7$, $\hat y = \sigma(0.7) = 0.668$.
- $\partial L/\partial \hat y = 2(\hat y - y) = -0.664$.
- $\partial L/\partial z = -0.664 \times \sigma(1-\sigma) = -0.664 \times 0.222 = -0.147$.
- $\partial L/\partial w = \partial L/\partial z \cdot x = -0.294$; $\partial L/\partial b = -0.147$.
- $\partial L/\partial x$ exists too, but we don't use it ($x$ is data).

Both gradients are negative, so gradient descent *increases* $w$ and $b$, pushing $\hat y$ up towards 1.

**Gate patterns (slide 21):**

| Gate | Local rule | Behaviour in the backward pass |
|---|---|---|
| Add, $u = a + b$ | $\partial u/\partial a = \partial u/\partial b = 1$ | **distributor**: passes the upstream gradient to both inputs unchanged |
| Multiply, $u = a \cdot b$ | $\partial u/\partial a = b$ | **swapper**: each input gets the upstream gradient times the *other* input |
| Max, $u = \max(a,b)$ | 1 for the larger input, 0 for the other | **router**: the whole gradient goes to the larger input |

Consequence of the multiply gate: a very large input sends a very large gradient to the *other* branch. That's why unnormalised data destabilises training, and one reason week 3 insisted on preprocessing.

**When a value is used twice, gradients add (slide 22):**

$$\frac{\partial L}{\partial a} = \sum_k \frac{\partial L}{\partial u_k} \frac{\partial u_k}{\partial a}$$

This is the multivariable chain rule. Frameworks therefore **accumulate** into `.grad` instead of overwriting it, so you must call `optimizer.zero_grad()` every iteration. Forget it and gradients silently pile up across iterations: training doesn't crash, it just does the wrong thing.

**Vector and matrix form (slide 23).** With vectors, the local derivative is a Jacobian matrix $\partial u / \partial a \in \mathbb R^{m\times n}$, but we almost never build it.
- For an **elementwise** operation $H = \sigma(Z)$ the Jacobian is diagonal, so the backward pass is an elementwise product: $\frac{\partial L}{\partial Z} = \frac{\partial L}{\partial H} \odot \sigma'(Z)$.
- For a **matrix product** $Z = XW^\top$ with $X \in \mathbb R^{N\times D}$, $W \in \mathbb R^{H\times D}$: $\frac{\partial L}{\partial W} = \left(\frac{\partial L}{\partial Z}\right)^\top X$ and $\frac{\partial L}{\partial X} = \frac{\partial L}{\partial Z} W$.
- **The shape trick:** a gradient has the same shape as the quantity it's for, and there's usually only one way to multiply the available matrices to get that shape. Check shapes first.
- A 4096×4096 Jacobian would be 67 MB per example; frameworks compute the vector–Jacobian product directly instead.

**The two-layer network end to end (slide 24):**

Forward:
$$Z_1 = X W_1^\top + b_1, \quad H = \max(0, Z_1), \quad S = H W_2^\top + b_2, \quad L = \text{softmax\_loss}(S, y)$$

Backward:
$$\frac{\partial L}{\partial S} = \frac{P - Y}{N}$$
$$\frac{\partial L}{\partial W_2} = \left(\frac{\partial L}{\partial S}\right)^\top H, \qquad \frac{\partial L}{\partial b_2} = \sum_{\text{rows}} \frac{\partial L}{\partial S}$$
$$\frac{\partial L}{\partial H} = \frac{\partial L}{\partial S} W_2, \qquad \frac{\partial L}{\partial Z_1} = \frac{\partial L}{\partial H} \odot \mathbb 1[Z_1 > 0]$$
$$\frac{\partial L}{\partial W_1} = \left(\frac{\partial L}{\partial Z_1}\right)^\top X, \qquad \frac{\partial L}{\partial b_1} = \sum_{\text{rows}} \frac{\partial L}{\partial Z_1}$$

(The slide labels the last bias gradient $\partial L/\partial b_2$; it should be $b_1$.)

The ReLU's backward pass is just a mask: gradient passes where $Z_1 > 0$, is blocked elsewhere. Every deep network repeats this pattern, which is why autograd can automate it.

### 5. Convolution as a layer (slides 25–39)

**Why fully connected layers fail on images (slide 26).** A modest 224×224×3 image into a hidden layer of 1,000 units needs $150{,}528 \times 1{,}000 \approx 1.5 \times 10^8$ weights in the first layer alone.
- Far more parameters than training images.
- **Flattening destroys spatial structure**: neighbouring pixels become unrelated coordinates.
- **No translation equivariance**: a cat learned in the top-left teaches nothing about a cat in the bottom-right.

**Inspiration from the visual cortex (slide 27).** Hubel and Wiesel (1959–62) recorded single cells in cat visual cortex (V1):
- each cell watches a small **receptive field**, not the whole retina;
- **simple cells** fire for an oriented edge at a specific place;
- **complex cells** keep firing as that edge moves a little;
- the same cell types repeat across the visual field.

As an architecture: local window ⇒ small kernel; same cell everywhere ⇒ weight sharing; simple → complex ⇒ conv → pool; stacking the pair ⇒ a hierarchy. Fukushima's **Neocognitron** (1980) copied this directly; its layers are called S and C after simple and complex cells.

**Two priors (slide 28):**
- **Locality:** a pixel is related to its neighbours, not to a pixel 200 rows away. So each unit looks at a small local window.
- **Translation equivariance:** an edge detector is useful everywhere in the image, so the **same weights** are applied at every position (**parameter sharing**). Shift the input and the output shifts the same way.

A layer that is local, shift-equivariant and linear *is* a convolution (week 2). The only new ingredient is that the kernel is learned.

**The convolution layer (slide 29).** Input $C_{in} \times H \times W$, weights $C_{out} \times C_{in} \times k \times k$:

$$Z_{c,i,j} = \sum_{c'=1}^{C_{in}} \sum_{u=1}^{k} \sum_{v=1}^{k} W_{c,c',u,v}\, X_{c',\, i+u,\, j+v} + b_c$$

- Each filter spans **all input channels**: it's a small 3D block ($C_{in} \times k \times k$), not a 2D square.
- Each filter produces one 2D **activation map**; $C_{out}$ filters stack into the output.
- **Parameters:** $C_{out} \cdot C_{in} \cdot k^2 + C_{out}$, **independent of $H$ and $W$**.
- Strictly it's cross-correlation (no kernel flip), as `Conv2d` implements.

**Convolution as a constrained fully connected layer (slide 30).** Written as a matrix multiplication, a convolution's weight matrix is:
- **sparse**: each output touches only $k$ inputs (in 1D), so almost every entry is zero;
- **tied**: the non-zero entries repeat down the diagonals, the same $k$ numbers over and over.

So a conv layer is a fully connected layer with most weights forced to zero and the rest forced to be equal. It's **strictly less expressive**, and that's the point: *"constraints that match the problem are how to win with limited data."*

**Output size (slide 31):**

$$H_{out} = \left\lfloor \frac{H + 2p - k}{s} \right\rfloor + 1$$

- **Padding $p$:** "same" padding $p = (k-1)/2$ (odd $k$) keeps the spatial size.
- **Stride $s$:** $s = 2$ halves the resolution, a cheaper alternative to pooling.
- **Dilation $d$:** insert $d - 1$ gaps between kernel elements. Effective kernel size $k' = d(k-1) + 1$. Grows the receptive field with no extra parameters.
- Example, ResNet's first layer: $224\times224$, $k = 7$, $s = 2$, $p = 3$: $\lfloor (224 + 6 - 7)/2 \rfloor + 1 = 112$.

**Receptive fields (slide 32).** The **receptive field** of a unit is the region of the *input image* that can affect it. Stacking 3×3 convolutions (stride 1) grows it linearly: 1 layer → 3×3, 2 layers → 5×5, 3 layers → 7×7.

Three 3×3 layers see the same region as one 7×7 layer but use $3 \times 9C^2 = 27C^2$ parameters instead of $49C^2$ (with $C$ channels in and out), and add two extra nonlinearities. *"That argument is the whole of VGG."* Pooling and stride grow the field much faster (multiplicatively).

A general rule for computing it layer by layer: $r_l = r_{l-1} + (k_l - 1)\, j_{l-1}$, where $j$ is the product of all strides so far (the "jump" between neighbouring units in input pixels), starting from $r_0 = 1$, $j_0 = 1$.

**Pooling (slide 33).** Downsample each activation map independently, typically 2×2 with stride 2:

$$\text{maxpool}(X)_{i,j} = \max_{u,v \in \{0,1\}} X_{2i+u,\, 2j+v}$$

- **No parameters.**
- Cuts compute in later layers by 4×.
- Grows the receptive field multiplicatively.
- Gives a little **local** translation invariance (a feature can move within the 2×2 window without changing the output).
- Backward pass: route the gradient to the position that was the max, zero elsewhere (the max gate).
- Average pooling takes the mean instead. Modern networks often replace pooling with strided convolution, and use **global average pooling** (average each whole channel to one number) before the classifier.

**Backward through a convolution (slide 34).** A conv layer is linear, so the same rules apply, and both gradients turn out to be convolutions:
- **Weights:** $\frac{\partial L}{\partial W} = X \star \frac{\partial L}{\partial Z}$ (correlate the input with the upstream gradient). Every position where the filter was applied contributes, which is "gradients add when a value is reused", applied $H' \times W'$ times. Parameter sharing is why the weight gradient sums over all positions.
- **Input:** $\frac{\partial L}{\partial X} = \frac{\partial L}{\partial Z} * \tilde W$, a full convolution with the kernel flipped in both axes. This is the **transposed convolution**, which returns in segmentation and generative models.

**The 1×1 convolution (slide 35).** A 1×1 kernel looks at one spatial position but **all channels**: $Z_{c,i,j} = \sum_{c'} W_{c,c'} X_{c',i,j}$.
- It's a fully connected layer applied independently at every pixel.
- Its job is **channel mixing** and **dimensionality reduction**: going from 256 to 64 channels costs $256 \times 64 = 16{,}384$ weights and no spatial extent.
- A cheap way to add another nonlinearity.

**Why deep rather than wide? (slide 36).** Universal approximation says one hidden layer is enough; practice says otherwise. The reason is **composition**:
- A shallow, wide network must represent every pattern independently. A deep network **reuses** earlier features: one edge detector serves every object class above it.
- Some functions need exponentially many units at depth 2 but only polynomially many at greater depth.
- Each layer adds a nonlinearity, so the number of linear regions the network can carve out grows multiplicatively with depth.

The record: AlexNet (2012), 8 layers, 16.4% top-5 error; VGG (2014), 19 layers, 7.3%; ResNet (2015), 152 layers, 3.6%. Depth won every time, but only once people worked out how to *train* it (week 5).

**What the filters learn (slides 37–38).** Trained first-layer kernels are oriented edges at several scales and orientations, and colour-opponent blobs: **Gabor filters**, the operators designed by hand in week 2, and the receptive fields Hubel and Wiesel measured. Deeper layers build a hierarchy:
- **early layers:** edges, colours, simple textures (small receptive field, generic);
- **middle layers:** corners, motifs, textures, object parts;
- **late layers:** whole objects and scene structure (large receptive field, task-specific).

This is why **transfer learning** works: the early layers of an ImageNet-trained network are useful for nearly any vision task. Almost every project in the course will start from pretrained weights ([[05 - CNN Architectures|ch. 05]]).

**A first CNN (slide 39)**, for 28×28 grayscale digits:

| Layer | Output | Parameters |
|---|---|---|
| input | 1×28×28 | 0 |
| conv 3×3, 16 filters, pad 1 | 16×28×28 | $16 \cdot 1 \cdot 9 + 16 = 160$ |
| ReLU + maxpool 2 | 16×14×14 | 0 |
| conv 3×3, 32 filters, pad 1 | 32×14×14 | $32 \cdot 16 \cdot 9 + 32 = 4{,}640$ |
| ReLU + maxpool 2 | 32×7×7 | 0 |
| flatten | 1,568 | 0 |
| fully connected → 10 | 10 | $1568 \cdot 10 + 10 = 15{,}690$ |
| **total** | | **20,490** |

The convolutions do the real work with 4,800 parameters; the single fully connected layer at the end uses over three times as many. That imbalance is why modern architectures replace the final FC layers with global average pooling. The pattern $[\text{conv} \to \text{ReLU} \to \text{pool}] \times N \to \text{FC}$ is **LeNet-5** (1998), the skeleton of everything in week 5.

**Hands-on (slide 43):** backprop by hand through $(a+b)c$ and check numerically; a two-layer net failing on `make_circles` without its nonlinearity; full NumPy forward/backward with gradient checks; vanishing gradients, sigmoid vs ReLU, gradient norm by layer; compare autograd with your algebra; a conv layer by hand vs `F.conv2d`; train a small CNN on digits and look at first-layer kernels.

## ✏️ Exercises

> [!example]- Exercise 1 — Backprop through max and a reused value
> $f = \max(a \cdot w,\ c) \cdot c$.
> **(a)** With $a = 3$, $w = 2$, $c = 4$: compute $f$ and the gradients $\partial f/\partial a$, $\partial f/\partial w$, $\partial f/\partial c$.
> **(b)** Repeat with $c = 7$ (same $a$, $w$). What happens to $\partial f/\partial w$, and why?
>
> ---
> Let $p = a w$ and $m = \max(p, c)$, so $f = m \cdot c$. Note $c$ is used **twice** (inside the max and as a multiplier), so its gradients add.
>
> **(a)** Forward: $p = 6$, $m = \max(6, 4) = 6$, $f = 24$.
> - Multiply gate $f = m c$: $\partial f/\partial m = c = 4$; direct $\partial f/\partial c = m = 6$.
> - Max gate: $p = 6 > c = 4$, so the full gradient 4 goes to $p$, and 0 to $c$.
> - Multiply gate $p = a w$: $\partial f/\partial w = 4 \cdot a = 12$; $\partial f/\partial a = 4 \cdot w = 8$.
> - Total for $c$: $6$ (direct) $+ 0$ (via max) $= 6$.
>
> **(b)** Forward: $p = 6$, $m = \max(6, 7) = 7$, $f = 49$.
> - $\partial f/\partial m = c = 7$, routed entirely to $c$ (the larger input). $p$ gets 0, so $\partial f/\partial w = \partial f/\partial a = 0$.
> - Total for $c$: $7$ (direct) $+ 7$ (via max) $= 14$. Check: here $f = c^2$, so $\partial f/\partial c = 2c = 14$. ✓
>
> When the max picks the other branch, $w$ gets **zero** gradient: it doesn't affect the output at all for this input. That's how max-pooling behaves too: only the winning position learns.

> [!example]- Exercise 2 — The deep linear network
> A student builds $3072 \to 100 \to 10$ with **no activation** between the layers and trains it on CIFAR-10. It reaches the same accuracy as the plain linear classifier from week 3.
> **(a)** Explain why.
> **(b)** Compare the number of parameters with the linear classifier.
> **(c)** The student adds three more hidden layers, still with no activation. What changes?
> **(d)** What one change would let the network beat the linear classifier?
>
> ---
> **(a)** $W_2(W_1 x + b_1) + b_2 = (W_2 W_1) x + (W_2 b_1 + b_2)$: exactly one linear layer with $W' = W_2 W_1$ ($10 \times 3072$). The set of functions it can represent is the same as the linear classifier's (slide 7).
>
> **(b)** $3072 \cdot 100 + 100 + 100 \cdot 10 + 10 = 308{,}310$ parameters vs 30,730: 10× more parameters, no extra expressive power.
>
> **(c)** Nothing in what it can represent. A product of any number of matrices is still one matrix. It does make optimisation harder and slower.
>
> **(d)** Put a nonlinearity (e.g. ReLU) after each hidden layer. Then the first layer's 100 units act as 100 learned templates/features that the last layer can combine, so the network can represent non-linear boundaries (rings, XOR, multimodal classes).

> [!example]- Exercise 3 — Diagnose the gradients
> **(a)** A 10-layer network uses sigmoid activations. Give an upper bound on how much the activation derivatives alone shrink the gradient reaching layer 1. What will you observe during training?
> **(b)** You switch to ReLU and the network trains. But after a few epochs with a high learning rate, 40% of the units in one layer output exactly 0 for every training image. What happened, and will they recover?
> **(c)** Suggest two fixes for (b).
>
> ---
> **(a)** Each sigmoid derivative is at most $1/4$, so $4^{-10} \approx 10^{-6}$. The last layers learn while the first layers barely change (their weight updates are about a million times smaller): the vanishing gradient problem. Loss decreases slowly and plateaus.
>
> **(b)** **Dying ReLU.** A large update pushed those units' weights/biases so their input is negative for every example. ReLU's derivative is 0 for negative input, so they receive zero gradient and **never recover**.
>
> **(c)** Lower the learning rate; use Leaky ReLU (small negative slope keeps a gradient alive) or ELU/GELU; better initialisation (He init, [[05 - CNN Architectures|ch. 05]]); batch normalisation before the activation keeps inputs centred around 0.

> [!example]- Exercise 4 — Shapes and parameters of a small CNN
> Input: 3×64×64 RGB image.
> 1. conv 5×5, 32 filters, stride 1, padding 2, then ReLU
> 2. maxpool 2×2, stride 2
> 3. conv 3×3, 64 filters, stride 2, padding 1, then ReLU
> 4. flatten, fully connected → 10 classes
>
> **(a)** Output shape and parameter count of each layer.
> **(b)** Which layer holds most of the parameters? What would you replace it with?
> **(c)** How many weights would a fully connected layer from the raw input to 1,000 hidden units need?
>
> ---
> **(a)**
> 1. $\lfloor(64 + 4 - 5)/1\rfloor + 1 = 64$ → **32×64×64**. Params $32 \cdot 3 \cdot 25 + 32 = 2{,}432$.
> 2. → **32×32×32**. 0 params.
> 3. $\lfloor(32 + 2 - 3)/2\rfloor + 1 = 16$ → **64×16×16**. Params $64 \cdot 32 \cdot 9 + 64 = 18{,}496$.
> 4. Flatten: $64 \cdot 16 \cdot 16 = 16{,}384$. FC: $16{,}384 \cdot 10 + 10 = 163{,}850$.
>
> **(b)** The FC layer: 163,850 of 184,778 parameters (~89%), while the convolutions do most of the computation. Replace flatten + FC with **global average pooling** (64×16×16 → 64) + FC to 10: $64 \cdot 10 + 10 = 650$ parameters.
>
> **(c)** $3 \cdot 64 \cdot 64 \cdot 1{,}000 = 12{,}288{,}000$ weights, about 5,000× layer 1's 2,432, and it would lose translation equivariance.

> [!example]- Exercise 5 — Receptive fields and cheap layers
> **(a)** With $C = 64$ input and output channels, compare the weights of three stacked 3×3 conv layers with one 7×7 layer (ignore biases). Which has the larger receptive field? Which is more expressive?
> **(b)** A 3×3 kernel with dilation 2: effective size, and number of weights per input–output channel pair?
> **(c)** Network: conv 3×3 (stride 1) → maxpool 2×2 (stride 2) → conv 3×3 (stride 1). What's the receptive field of one output unit?
> **(d)** A layer has 256 channels and the next 3×3 conv expects 64. What's the cheapest way to reduce the channels, and what does it cost?
>
> ---
> **(a)** Three 3×3: $3 \times 9 \times 64^2 = 110{,}592$. One 7×7: $49 \times 64^2 = 200{,}704$. **Same 7×7 receptive field**, but the stack uses 55% of the parameters and has three nonlinearities instead of one, so it can represent more complex functions.
>
> **(b)** $k' = d(k-1) + 1 = 2 \cdot 2 + 1 = 5$: covers a 5×5 area with only **9** weights.
>
> **(c)** Using $r_l = r_{l-1} + (k_l - 1) j_{l-1}$: conv: $r = 1 + 2 \cdot 1 = 3$, $j = 1$. Pool: $r = 3 + 1 \cdot 1 = 4$, $j = 2$. Conv: $r = 4 + 2 \cdot 2 = 8$. **8×8 pixels.** The conv after the pool counts double because each step in its input is 2 pixels in the image.
>
> **(d)** A **1×1 convolution** 256 → 64: $256 \cdot 64 + 64 = 16{,}448$ parameters. It mixes channels at each pixel without any spatial cost (the "bottleneck" idea used in GoogLeNet and ResNet).

## 📝 Summary

- **Neural network:** $s = W_2\, \sigma(W_1 x)$. The nonlinearity $\sigma$ is the only reason depth helps; without it, stacked layers collapse to one linear map. The hidden layer learns $H$ features the last layer combines.
- **Universal approximation** says one hidden layer can represent anything, but not how many units, whether SGD finds it, or whether it generalises.
- **Activations:** sigmoid ($\sigma' \le 1/4$, saturates, not zero-centred), tanh (zero-centred, saturates), **ReLU** (gradient 1 for $x > 0$, cheap; can "die"), Leaky ReLU/ELU/GELU. Sigmoid shrinks gradients by up to $4^{-n}$ over $n$ layers (vanishing gradient).
- **Backpropagation** = chain rule applied locally on a computation graph: downstream gradient = upstream × local. Add distributes, multiply swaps, max routes. Gradients **add** where a value is reused, so call `zero_grad()` each iteration.
- **Matrix form:** $\partial L/\partial W = (\partial L/\partial Z)^\top X$, $\partial L/\partial X = (\partial L/\partial Z) W$; elementwise ops multiply elementwise. Check shapes.
- **Convolution layer** = locality + weight sharing (from Hubel & Wiesel's cells). Params $C_{out} C_{in} k^2 + C_{out}$, independent of image size. A conv layer is a sparse, tied FC layer: less expressive, but much more data-efficient.
- **Output size** $\lfloor (H + 2p - k)/s \rfloor + 1$; dilation gives effective size $d(k-1)+1$. Stacked 3×3 convs grow the receptive field linearly; pooling/stride multiplicatively. Three 3×3 = one 7×7 receptive field with fewer parameters.
- **Pooling** has no parameters and gives local translation invariance; **1×1 conv** mixes channels; **depth** beats width by reusing features. First-layer filters become Gabor-like edge detectors; early layers transfer to almost any task.

## ⚠️ Important Notes

1. **No nonlinearity, no depth.** Any stack of linear layers equals one linear layer, however many parameters it has.
2. **Sigmoid and tanh saturate.** Large inputs (|x| > 5) give near-zero gradients; in deep nets the factors multiply. Use ReLU-family activations in hidden layers.
3. **Dead ReLUs don't come back.** A unit with negative input for every example gets zero gradient forever. Watch for high learning rates.
4. **Gradients accumulate in PyTorch.** Forgetting `optimizer.zero_grad()` doesn't crash; it silently adds old gradients to new ones.
5. **Multiply gates swap magnitudes.** A huge input sends a huge gradient to the other branch, which is why unnormalised inputs make training unstable.
6. **The max gate gives zero gradient to the losing input.** Only the selected position in max-pooling learns from that example.
7. **Conv parameters don't depend on image size**; FC parameters do. Doubling the image size doesn't change a conv layer's parameter count, but it quadruples the flattened size feeding an FC layer.
8. **Each filter spans all input channels.** A 3×3 conv on a 64-channel input has $64 \times 9$ weights per filter, not 9.
9. **Get the output-size formula right.** Mismatched shapes usually surface several layers later with a confusing error. Remember the floor.
10. **"Same" padding $p = (k-1)/2$ only works cleanly for odd $k$.**
11. **Receptive field ≠ kernel size.** It's the input region a unit can see after all layers so far; strides and pooling multiply its growth.
12. **Pooling gives only local invariance**, not invariance to large shifts, rotations or scale.
13. **Universal approximation is not a reason to use one wide layer.** Depth gives feature reuse and is what actually works.
14. **Most CNN parameters are often in the final FC layer, not the convolutions.** Global average pooling removes most of them.

> [!warning] Gaps in the source material
> - **Figures lost in extraction:** slide 8 (linear vs hidden-layer decision boundaries), 11 (McCulloch–Pitts diagram), 13–14 (activation plots), 15 (gradient-by-layer plot from a 12-layer net), 18 (graph diagram), 26 (parameters vs input size plot), 29–30 (conv sweep and banded matrix), 32 (receptive field growth), 33 (max vs average pooling), 37 (learned filters). Described from captions.
> - **Possible typo on slide 24:** the last bias gradient is written $\partial L/\partial b_2$ again; from the forward pass it must be $\partial L/\partial b_1$. Corrected in §4.
> - **All worked numbers were recomputed** (slide 20's neuron, slide 23's 67 MB, slide 31's 112, slide 39's parameter table) and match.
> - **Added beyond the slides:** the forward values on slide 20 ($z = 0.7$, $\hat y = 0.668$); typical causes of dying ReLU; the receptive-field recurrence $r_l = r_{l-1} + (k_l - 1) j_{l-1}$; global average pooling's definition; all exercises and Important Notes.

**Previous:** [[03 - Image Classification and Linear Models]] · **Next:** [[05 - CNN Architectures]]
