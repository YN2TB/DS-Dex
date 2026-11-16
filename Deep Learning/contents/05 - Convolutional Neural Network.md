---
subject: Deep Learning
chapter: 5
tags: [ds, deep-learning, cnn, convolution, pooling, receptive-field, batch-normalization, resnet, densenet, architecture]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 7 (Convolutional Neural Networks) and ch. 8 (Modern Convolutional Neural Networks)"
---

# Convolutional Neural Network

D2L ch. 7 builds the convolution from first principles and implements it; ch. 8 goes through LeNet → AlexNet → VGG → NiN → GoogLeNet → batch norm → ResNet → ResNeXt → DenseNet → design spaces (RegNet). Each section below gives the idea, D2L's PyTorch code and the printed shapes. All printed shapes and worked examples were recomputed and match the book.

## 📘 Main Knowledge

### 1. From an MLP to a convolution (§7.1)

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

### 2. Cross-correlation (§7.2)

True convolution flips the kernel: $(f*g)(i,j)=\sum_a\sum_b f(a,b)\,g(i-a,j-b)$. Deep learning layers compute cross-correlation ($i+a$, $j+b$). Since the kernel is learned, the network just learns the flipped kernel, so the difference is invisible inside a trained model. It matters only when importing kernels from signal processing.

Example:

| $\mathsf X$ | $\mathsf K$ | output |
|---|---|---|
| $\begin{pmatrix}0&1&2\\3&4&5\\6&7&8\end{pmatrix}$ | $\begin{pmatrix}0&1\\2&3\end{pmatrix}$ | $\begin{pmatrix}19&25\\37&43\end{pmatrix}$ |

e.g. $0\cdot0+1\cdot1+3\cdot2+4\cdot3=19$.

**Edge detection.** Kernel $[1,-1]$ on a $6\times8$ image with a black middle stripe gives $+1$ at white→black edges and $-1$ at black→white, 0 elsewhere (row: $[0,1,0,0,0,-1,0]$). It is a finite difference, $x_{i,j}-x_{i,j+1}$, so it finds vertical edges only: on the transposed image its output is all zero. One kernel detects one direction, which is why layers have many channels. D2L then learns a kernel from the input/output pair: after 10 steps it is $[0.9797, -0.9816]$, close to $[1,-1]$.

**Code (§7.2).** Cross-correlation by sliding the kernel, and a layer built on it (kernel and scalar bias are the two parameters, initialized randomly):

```python
def corr2d(X, K):
    h, w = K.shape
    Y = torch.zeros((X.shape[0] - h + 1, X.shape[1] - w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i:i + h, j:j + w] * K).sum()
    return Y

class Conv2D(nn.Module):
    def __init__(self, kernel_size):
        super().__init__()
        self.weight = nn.Parameter(torch.rand(kernel_size))
        self.bias = nn.Parameter(torch.zeros(1))
    def forward(self, x):
        return corr2d(x, self.weight) + self.bias
```

Learning the edge kernel from the pair (X, Y): a $1\times2$ `nn.LazyConv2d(1, kernel_size=(1, 2), bias=False)`, inputs reshaped to (batch, channel, height, width) = (1, 1, 6, 8), squared error, learning rate 0.03, 10 steps:

```python
for i in range(10):
    Y_hat = conv2d(X)
    l = (Y_hat - Y) ** 2
    conv2d.zero_grad()
    l.sum().backward()
    conv2d.weight.data[:] -= lr * conv2d.weight.grad
```

Printed loss: 13.904 (step 2), 2.333, 0.392, 0.066, 0.011 (step 10). (My rerun from another random start: $[1.0063,-0.9662]$, loss 0.043. Any start converges toward $[1,-1]$.)

**Feature map.** The output of a convolutional layer is called a feature map: a learned representation in the spatial dimensions passed to the next layer.

### 3. Padding, stride and output size (§7.3)

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

**Code (§7.3).** A helper adds and strips the batch and channel axes:

```python
def comp_conv2d(conv2d, X):
    X = X.reshape((1, 1) + X.shape)
    Y = conv2d(X)
    return Y.reshape(Y.shape[2:])

conv2d = nn.LazyConv2d(1, kernel_size=3, padding=1)                    # 8x8 -> 8x8
conv2d = nn.LazyConv2d(1, kernel_size=(5, 3), padding=(2, 1))          # 8x8 -> 8x8
conv2d = nn.LazyConv2d(1, kernel_size=3, padding=1, stride=2)          # 8x8 -> 4x4
conv2d = nn.LazyConv2d(1, kernel_size=(3, 5), padding=(0, 1), stride=(3, 4))  # -> 2x2
```

In PyTorch `padding=p` means $p$ rows/columns **per side**, i.e. total padding $2p$ in the formula. Stride example (Fig. 7.3.3, strides 3 and 2): the first output column is $0\cdot0+0\cdot1+1\cdot2+2\cdot3=8$ and $0\cdot0+6\cdot1+0\cdot2+0\cdot3=6$. With total padding $k-1$ the output is $\lfloor(n+s-1)/s\rfloor$, and $n/s$ when $s$ divides $n$.

### 4. Channels (§7.4)

With $c_i$ input channels the kernel is $c_i\times k_h\times k_w$: cross-correlate each channel and sum. With $c_o$ outputs the kernel is $c_o\times c_i\times k_h\times k_w$. D2L's examples reproduce: $\begin{pmatrix}56&72\\104&120\end{pmatrix}$ for two input channels, plus $\begin{pmatrix}76&100\\148&172\end{pmatrix}$ and $\begin{pmatrix}96&128\\192&224\end{pmatrix}$ for the extra output channels.

D2L warns against reading channel $k$ as "the edge detector": channels are learned jointly, and an edge detector may be a direction in channel space.

Cost: $h\cdot w\cdot k^2\cdot c_i\cdot c_o$ multiply-adds. For $256\times256$, $k=5$, $c_i=c_o=128$ that is $53{,}687{,}091{,}200$ operations counting multiplies and adds separately ("over 53 billion"). Doubling both channel counts quadruples the cost.

**Code (§7.4).**

```python
def corr2d_multi_in(X, K):               # sum over input channels
    return sum(d2l.corr2d(x, k) for x, k in zip(X, K))

def corr2d_multi_in_out(X, K):           # stack over output channels
    return torch.stack([corr2d_multi_in(X, k) for k in K], 0)

K = torch.stack((K, K + 1, K + 2), 0)    # shape [3, 2, 2, 2]: c_o, c_i, k_h, k_w
```

D2L's view of channels: they combine MLP-style nonlinear mixing with localized convolution, letting a CNN reason about several features (edges, shapes) at once.

### 5. $1\times1$ convolution

It sees no neighbours, so it only mixes channels: a fully connected $c_i\to c_o$ layer applied at every pixel with shared weights. Uses:
- change the channel count cheaply (Inception, ResNeXt, DenseNet transitions);
- add nonlinearity across channels (NiN).

With a nonlinearity between them, consecutive convolutions do not collapse into one ([[04 - Neural Network|ch. 04]] §1).

**Code.** A $1\times1$ convolution is a matrix product after flattening space:

```python
def corr2d_multi_in_out_1x1(X, K):
    c_i, h, w = X.shape
    c_o = K.shape[0]
    X = X.reshape((c_i, h * w))
    K = K.reshape((c_o, c_i))
    Y = torch.matmul(K, X)
    return Y.reshape((c_o, h, w))
```

On random $3\times3\times3$ input with a $2\times3\times1\times1$ kernel it agrees with `corr2d_multi_in_out` to within $10^{-6}$. It needs $c_oc_i$ weights plus biases.

### 6. Pooling (§7.5)

A fixed window computing max or mean; no parameters. On $\mathsf X=0..8$ with a $2\times2$ window: max $\begin{pmatrix}4&5\\7&8\end{pmatrix}$, average $\begin{pmatrix}2&3\\5&6\end{pmatrix}$.

Purposes: downsampling ($2\times2$, stride 2 quarters the resolution) and local translation invariance (after the edge detector, $2\times2$ max-pooling still reports an edge shifted by one pixel). Pooling works per channel and does not change the channel count.

In PyTorch, pooling's stride defaults to the window size (`nn.MaxPool2d(3)` has stride 3), while convolution's defaults to 1.

**Code (§7.5).**

```python
def pool2d(X, pool_size, mode='max'):
    p_h, p_w = pool_size
    Y = torch.zeros((X.shape[0] - p_h + 1, X.shape[1] - p_w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            if mode == 'max':
                Y[i, j] = X[i: i + p_h, j: j + p_w].max()
            elif mode == 'avg':
                Y[i, j] = X[i: i + p_h, j: j + p_w].mean()
    return Y
```

On `X = arange(16).reshape(1, 1, 4, 4)`:

| layer | output |
|---|---|
| `nn.MaxPool2d(3)` (stride defaults to 3) | `[[10]]` |
| `nn.MaxPool2d(3, padding=1, stride=2)` | `[[5, 7], [13, 15]]` |
| `nn.MaxPool2d((2, 3), stride=(2, 3), padding=(0, 1))` | `[[5, 7], [13, 15]]` |

On two channels `cat((X, X + 1), 1)` the second output channel is `[[6, 8], [14, 16]]`: one result per input channel. Pooling has no parameters, so it needs no initialization.

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

### 8. LeNet (§7.6)

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

**Code (§7.6).** D2L replaces LeNet's final Gaussian (RBF) layer with a softmax output; otherwise it is LeNet-5. Weights get Xavier initialization:

```python
def init_cnn(module):
    if type(module) == nn.Linear or type(module) == nn.Conv2d:
        nn.init.xavier_uniform_(module.weight)

class LeNet(d2l.Classifier):
    def __init__(self, lr=0.1, num_classes=10):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.Sequential(
            nn.LazyConv2d(6, kernel_size=5, padding=2), nn.Sigmoid(),
            nn.AvgPool2d(kernel_size=2, stride=2),
            nn.LazyConv2d(16, kernel_size=5), nn.Sigmoid(),
            nn.AvgPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.LazyLinear(120), nn.Sigmoid(),
            nn.LazyLinear(84), nn.Sigmoid(),
            nn.LazyLinear(num_classes))

def layer_summary(self, X_shape):
    X = torch.randn(*X_shape)
    for layer in self.net:
        X = layer(X)
        print(layer.__class__.__name__, 'output shape:\t', X.shape)

model = LeNet()
model.layer_summary((1, 1, 28, 28))     # shapes as in the table above

trainer = d2l.Trainer(max_epochs=10, num_gpus=1)
data = d2l.FashionMNIST(batch_size=128)
model = LeNet(lr=0.1)
model.apply_init([next(iter(data.get_dataloader(True)))[0]], init_cnn)
trainer.fit(model, data)
```

Padding 2 in the first conv compensates for the $5\times5$ kernel; the second conv has none and loses 4 pixels. Trimming MNIST's scans from $32\times32$ to $28\times28$ saved about 30% of storage ($784/1024=76.6\%$ kept) when megabytes mattered. CNNs have fewer parameters than comparable MLPs but can cost more compute, because each parameter is used in many multiplications (§18). D2L: LeNet is far closer to ResNet than to an MLP; what used to take months of C++ and assembly (and the Lisp-based SN) now takes minutes.

### 9. AlexNet (2012, §8.1)

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

D2L says the two 4096-unit layers need "nearly 1GB". They have 54,534,144 parameters = 208.0 MB. With gradients and two Adam moments (4×) it is 832.1 MB, so the claim fits the training footprint, not the weights (declined discrepancy D8). D2L's own §8.1.4 gives the weights of these layers as 164 MB, so the book is inconsistent with itself.

**Representation learning (§8.1.1).** Until 2012 the decisive part of a vision pipeline was the hand-engineered representation, and papers were about new feature functions. LeCun, Hinton, Bengio, Ng, Amari, Schmidhuber and others argued that features should be **learned** and composed hierarchically: low layers detect edges, colours and textures, higher layers eyes, noses, blades of grass, and higher still whole objects. AlexNet's first layer indeed learned filters resembling classical ones (Fig. 8.1.1, image lost).

Why did it take from LeNet (1995) to AlexNet (2012)? Two missing ingredients:

- **Data.** 1990s research used tiny UCI datasets with low-resolution images on clean backgrounds. **ImageNet** (2009): 1 million images, 1000 per class for 1000 WordNet nouns, prefiltered by Google Image Search and verified on Amazon Mechanical Turk, at $224\times224$ (TinyImages had 80 million $32\times32$ thumbnails; CIFAR-100 60,000 images). Today's LAION-5B has billions.
- **Hardware.** CPU cores are powerful but expensive in chip area (branch prediction, deep pipelines, caches); servers rarely exceed 64 cores per socket. GPUs have thousands of simple cores (NVIDIA Ampere: up to 6912 CUDA cores) at about 1 GHz. A100: over 300 TFLOPs in BF16 matrix multiplication, up to 20 TFLOPs FP32; CPUs rarely exceed 1 TFLOP. Reasons: power grows roughly quadratically with clock frequency, so one core at 4× speed costs the power of 16 cores at ¼ speed, which give $16\times\tfrac14=4$× the throughput; GPU cores are simpler; GPU memory buses are at least 10× wider. GPUs were built for $4\times4$ matrix–vector products in graphics, the same maths as convolutions. Krizhevsky and Sutskever used two GTX 580s (3 GB each, 1.5 TFLOPs each) and wrote cuda-convnet.

**Code.** D2L's AlexNet for 1-channel Fashion-MNIST upsampled to $224\times224$ (not smart in general: more compute, no more information; done to keep the architecture):

```python
class AlexNet(d2l.Classifier):
    def __init__(self, lr=0.1, num_classes=10):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.Sequential(
            nn.LazyConv2d(96, kernel_size=11, stride=4, padding=1),
            nn.ReLU(), nn.MaxPool2d(kernel_size=3, stride=2),
            nn.LazyConv2d(256, kernel_size=5, padding=2), nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.LazyConv2d(384, kernel_size=3, padding=1), nn.ReLU(),
            nn.LazyConv2d(384, kernel_size=3, padding=1), nn.ReLU(),
            nn.LazyConv2d(256, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2), nn.Flatten(),
            nn.LazyLinear(4096), nn.ReLU(), nn.Dropout(p=0.5),
            nn.LazyLinear(4096), nn.ReLU(), nn.Dropout(p=0.5),
            nn.LazyLinear(num_classes))
        self.net.apply(d2l.init_cnn)
```

Shapes on $1\times224\times224$: conv1 $96\times54\times54$ → pool $26\times26$ → conv2 $256\times26\times26$ → pool $12\times12$ → three convs at $12\times12$ (384, 384, 256) → pool $256\times5\times5$ → flatten 6400 → 4096 → 4096 → 10. Trained with `lr=0.01`, batch 128, 10 epochs.

**Discussion (§8.1.4).** The two hidden dense layers are $6400\times4096$ and $4096\times4096$: D2L says 164 MB and 81 MFLOPs. (Check: 42,991,616 parameters = 164.0 MiB in float32; 43.0 M multiply-adds = 86.0 MFLOPs, or 82.0 in binary mega-units.) Despite over 40 million parameters on 60,000 images, training and validation loss stay almost identical: dropout and the other regularizers work. Adoption still took years, partly because tools (DistBelief, Caffe) did not exist yet and Theano lacked features; TensorFlow changed that.

### 10. VGG (2014, §8.2)

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

**Code (§8.2).**

```python
def vgg_block(num_convs, out_channels):
    layers = []
    for _ in range(num_convs):
        layers.append(nn.LazyConv2d(out_channels, kernel_size=3, padding=1))
        layers.append(nn.ReLU())
    layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
    return nn.Sequential(*layers)

class VGG(d2l.Classifier):
    def __init__(self, arch, lr=0.1, num_classes=10):
        super().__init__()
        self.save_hyperparameters()
        conv_blks = []
        for (num_convs, out_channels) in arch:
            conv_blks.append(vgg_block(num_convs, out_channels))
        self.net = nn.Sequential(
            *conv_blks, nn.Flatten(),
            nn.LazyLinear(4096), nn.ReLU(), nn.Dropout(0.5),
            nn.LazyLinear(4096), nn.ReLU(), nn.Dropout(0.5),
            nn.LazyLinear(num_classes))
        self.net.apply(d2l.init_cnn)

VGG(arch=((1, 64), (1, 128), (2, 256), (2, 512), (2, 512))).layer_summary((1, 1, 224, 224))
# blocks: 64x112x112, 128x56x56, 256x28x28, 512x14x14, 512x7x7; flatten 25088
```

`arch` makes VGG a **family** of networks. For Fashion-MNIST D2L trains a slimmer VGG-11 with channels (16, 32, 64, 128, 128), `lr=0.01`, $224\times224$ inputs; training and validation loss stay close (little overfitting).

### 11. NiN (2013, §8.3)

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

**Code (§8.3).** A NiN block is one $k\times k$ convolution followed by two $1\times1$ convolutions, each with ReLU. Kernel sizes and channels follow AlexNet (11, 5, 3; 96, 256, 384), each block followed by $3\times3$ max-pooling with stride 2:

```python
def nin_block(out_channels, kernel_size, strides, padding):
    return nn.Sequential(
        nn.LazyConv2d(out_channels, kernel_size, strides, padding), nn.ReLU(),
        nn.LazyConv2d(out_channels, kernel_size=1), nn.ReLU(),
        nn.LazyConv2d(out_channels, kernel_size=1), nn.ReLU())

self.net = nn.Sequential(
    nin_block(96, kernel_size=11, strides=4, padding=0), nn.MaxPool2d(3, stride=2),
    nin_block(256, kernel_size=5, strides=1, padding=2), nn.MaxPool2d(3, stride=2),
    nin_block(384, kernel_size=3, strides=1, padding=1), nn.MaxPool2d(3, stride=2),
    nn.Dropout(0.5),
    nin_block(num_classes, kernel_size=3, strides=1, padding=1),
    nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten())
```

Shapes: $96\times54\times54$ → $26$ → $256\times26\times26$ → $12$ → $384\times12\times12$ → $5$ → $10\times5\times5$ → $10\times1\times1$ → 10 logits. D2L notes the parameter saving may cost longer training. `lr=0.05`.

### 12. GoogLeNet (2014, §8.4)

The Inception block runs four branches in parallel ($1\times1$; $1\times1$→$3\times3$; $1\times1$→$5\times5$; $3\times3$ max-pool→$1\times1$) and concatenates them along channels. Instead of choosing a kernel size, it uses several and lets training allocate channels. The $1\times1$ convolutions reduce channels before the expensive $3\times3$ and $5\times5$.

GoogLeNet also introduced the **stem / body / head** structure used since. Replacing only the head is the basis of fine-tuning in [[06 - Object Detection|ch. 06]].

**Code (§8.4).**

```python
class Inception(nn.Module):
    # c1--c4: output channels of each branch
    def __init__(self, c1, c2, c3, c4, **kwargs):
        super(Inception, self).__init__(**kwargs)
        self.b1_1 = nn.LazyConv2d(c1, kernel_size=1)
        self.b2_1 = nn.LazyConv2d(c2[0], kernel_size=1)
        self.b2_2 = nn.LazyConv2d(c2[1], kernel_size=3, padding=1)
        self.b3_1 = nn.LazyConv2d(c3[0], kernel_size=1)
        self.b3_2 = nn.LazyConv2d(c3[1], kernel_size=5, padding=2)
        self.b4_1 = nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        self.b4_2 = nn.LazyConv2d(c4, kernel_size=1)
    def forward(self, x):
        b1 = F.relu(self.b1_1(x))
        b2 = F.relu(self.b2_2(F.relu(self.b2_1(x))))
        b3 = F.relu(self.b3_2(F.relu(self.b3_1(x))))
        b4 = F.relu(self.b4_2(self.b4_1(x)))
        return torch.cat((b1, b2, b3, b4), dim=1)
```

All branches keep height and width (padding), so they can be concatenated. The tuned hyperparameters are the channel counts per branch, i.e. how to allocate capacity among kernel sizes.

The full network stacks 9 Inception blocks in three groups with max-pooling between them:

| module | content | output on $96\times96$ |
|---|---|---|
| b1 (stem) | $7\times7$ conv 64, stride 2; $3\times3$ max-pool s2 | $64\times24\times24$ |
| b2 | $1\times1$ conv 64; $3\times3$ conv 192; pool | $192\times12\times12$ |
| b3 | Inception(64, (96,128), (16,32), 32) → 256 ch; Inception(128, (128,192), (32,96), 64) → 480 ch; pool | $480\times6\times6$ |
| b4 | five Inceptions → 512, 512, 512, 528, 832 ch; pool | $832\times3\times3$ |
| b5 | Inceptions → 832, 1024 ch; global average pool | 1024 |
| head | dense 10 | 10 |

Channel ratios in b3: $64:128:32:32=2:4:1:1$, with the $3\times3$ and $5\times5$ branches first reduced to $192/2=96$ and $192/12=16$ channels; the second block uses $128:192:96:64=4:6:3:2$. D2L trains it at $96\times96$, `lr=0.01`. The many fairly arbitrary hyperparameters reflect 2014, when shapes had to be specified by hand and design exploration was brute force. (Mine: this version has 5,977,530 parameters.)

### 13. Batch normalization (2015, §8.5)

$$\mathrm{BN}(\mathbf x)=\boldsymbol\gamma\odot\frac{\mathbf x-\hat{\boldsymbol\mu}_{\mathcal B}}{\hat{\boldsymbol\sigma}_{\mathcal B}}+\boldsymbol\beta,\qquad \hat{\boldsymbol\mu}_{\mathcal B}=\frac{1}{|\mathcal B|}\sum_{\mathbf x\in\mathcal B}\mathbf x,\quad \hat{\boldsymbol\sigma}^2_{\mathcal B}=\frac{1}{|\mathcal B|}\sum_{\mathbf x\in\mathcal B}(\mathbf x-\hat{\boldsymbol\mu}_{\mathcal B})^2+\epsilon$$

Normalize with the minibatch's statistics, then rescale and shift with learned $\boldsymbol\gamma,\boldsymbol\beta$. In conv layers it is per channel over all positions. Usually placed after the affine/conv layer and before the activation.

Benefits: input standardization inside the network, more stable activations, and regularization through batch noise.

- With batch size 1 the output is exactly 0: the signal is gone.
- Batch statistics have relative noise about $1/\sqrt{|\mathcal B|}$: 14.1% at 50, 10.0% at 100 (D2L's recommended range), 4.4% at 512. Larger batches regularize less, so increasing the batch size to speed up training also weakens regularization (64 → 512 cuts the noise 2.83×).
- Training uses batch statistics; prediction uses running averages over the dataset, so an image's prediction does not depend on its batch.
- Cost: 2 parameters per channel.

**Where it goes (§8.5.2).** Fully connected: $\mathbf h=\phi(\mathrm{BN}(\mathbf W\mathbf x+\mathbf b))$, after the affine map and before the activation (the original paper; later work also tried after the activation). Convolutional: per output channel, over all $m\cdot p\cdot q$ values (examples × height × width), with one scalar scale and shift per channel. Same mean and variance at every location, consistent with translation invariance.

**Layer normalization** (Ba et al. 2016) normalizes one example at a time over its $n$ coordinates:
$$\mathrm{LN}(\mathbf x)=\frac{\mathbf x-\hat\mu}{\hat\sigma},\qquad \hat\mu=\frac1n\sum_{i=1}^nx_i,\quad \hat\sigma^2=\frac1n\sum_{i=1}^n(x_i-\hat\mu)^2+\epsilon$$
(with learned per-coordinate scale and offset). It is scale independent, $\mathrm{LN}(\alpha\mathbf x)\approx\mathrm{LN}(\mathbf x)$ for $\alpha\ne0$, which prevents divergence; it does not depend on batch size and behaves the same in training and testing. Transformers use it ([[08 - Sequence to Sequence|ch. 08]]). For convolutions even a batch of one gives a well-defined per-channel mean over locations.

**From scratch.**

```python
def batch_norm(X, gamma, beta, moving_mean, moving_var, eps, momentum):
    if not torch.is_grad_enabled():            # prediction mode
        X_hat = (X - moving_mean) / torch.sqrt(moving_var + eps)
    else:
        assert len(X.shape) in (2, 4)
        if len(X.shape) == 2:                  # fully connected: per feature
            mean = X.mean(dim=0)
            var = ((X - mean) ** 2).mean(dim=0)
        else:                                  # conv: per channel, keep shape
            mean = X.mean(dim=(0, 2, 3), keepdim=True)
            var = ((X - mean) ** 2).mean(dim=(0, 2, 3), keepdim=True)
        X_hat = (X - mean) / torch.sqrt(var + eps)
        moving_mean = (1.0 - momentum) * moving_mean + momentum * mean
        moving_var = (1.0 - momentum) * moving_var + momentum * var
    Y = gamma * X_hat + beta
    return Y, moving_mean.data, moving_var.data

class BatchNorm(nn.Module):
    def __init__(self, num_features, num_dims):
        super().__init__()
        shape = (1, num_features) if num_dims == 2 else (1, num_features, 1, 1)
        self.gamma = nn.Parameter(torch.ones(shape))    # scale, learned
        self.beta = nn.Parameter(torch.zeros(shape))    # shift, learned
        self.moving_mean = torch.zeros(shape)           # not parameters
        self.moving_var = torch.ones(shape)
    def forward(self, X):
        if self.moving_mean.device != X.device:
            self.moving_mean = self.moving_mean.to(X.device)
            self.moving_var = self.moving_var.to(X.device)
        Y, self.moving_mean, self.moving_var = batch_norm(
            X, self.gamma, self.beta, self.moving_mean,
            self.moving_var, eps=1e-5, momentum=0.1)
        return Y
```

Design pattern: maths in a function, bookkeeping (devices, buffers, moving averages) in the layer. The `momentum` here is a misnomer: it is the weight of the new batch in an exponential moving average, unrelated to optimizer momentum. With 0.1, the running estimate averages over roughly the last $1/0.1=10$ batches. (D2L's from-scratch version decides the mode with `torch.is_grad_enabled()`, so evaluating under `no_grad` uses the moving averages, as the `Trainer` does.)

**BN-LeNet.** Insert `BatchNorm(6, num_dims=4)` after each convolution and `BatchNorm(120, num_dims=2)`, `BatchNorm(84, num_dims=2)` after the dense layers, each before its sigmoid; same training (`lr=0.1`, batch 128, 10 epochs). Learned values in the first BN layer: $\gamma=(2.24,1.88,2.07,1.13,1.96,1.68)$, $\beta=(0.31,-1.02,1.48,-0.21,-1.91,0.62)$: the network chose scales far from the standardized 1. Concise: `nn.LazyBatchNorm2d()` and `nn.LazyBatchNorm1d()`, much faster because compiled.

**Discussion (§8.5.6).** The original paper explained BN by reducing **internal covariate shift**. D2L's objections: the drift it describes is not covariate shift (it is closer to concept drift), and the explanation does not say why the technique works. Ali Rahimi's 2017 NeurIPS "alchemy" talk and Lipton & Steinhardt (2018) used it as an example of vague claims; Santurkar et al. (2018) argue BN works despite behaving opposite to the original claim. D2L's practical summary: BN stabilizes intermediate outputs; it differs slightly for dense and conv layers (layer norm is an alternative for conv); like dropout it behaves differently in training and prediction; it helps regularization and convergence; for robustness to input perturbations, consider removing it (Wang et al. 2022). A bias right before BN is redundant (D2L ex. 8.5.1): the mean subtraction cancels it and $\boldsymbol\beta$ replaces it.

### 14. ResNet (2015, §8.6)

A bigger function class $\mathcal F'$ is only guaranteed to fit at least as well as $\mathcal F$ if $\mathcal F\subseteq\mathcal F'$. A residual block computes
$$\mathbf y=\mathbf x+g(\mathbf x)$$
With $g\equiv0$ it is the identity, so adding blocks cannot shrink the function class. D2L's argument is about nested function classes; the familiar "gradients flow through the skip" explanation is also true. Learning $g=f-\mathbf x$ is easy when $f$ is close to the identity: push weights toward zero.

ResNet-18: stem ($7\times7$ s2, 64 channels, BN, ReLU, $3\times3$ max-pool s2), four modules of two residual blocks each (each module doubles channels and halves resolution), global average pooling, one dense layer. On a $96\times96$ input the shapes are $64\times24\times24\to64\times24\times24\to128\times12\times12\to256\times6\times6\to512\times3\times3\to10$.

ResNet combines VGG's $3\times3$ convolutions, GoogLeNet's stem and pooled head, and NiN's lack of a dense body.

**Code (§8.6).** The block: $3\times3$ conv → BN → ReLU → $3\times3$ conv → BN, add the input, ReLU. When channels or resolution change, a $1\times1$ convolution (with the same stride) reshapes the input:

```python
class Residual(nn.Module):
    def __init__(self, num_channels, use_1x1conv=False, strides=1):
        super().__init__()
        self.conv1 = nn.LazyConv2d(num_channels, kernel_size=3, padding=1, stride=strides)
        self.conv2 = nn.LazyConv2d(num_channels, kernel_size=3, padding=1)
        self.conv3 = nn.LazyConv2d(num_channels, kernel_size=1, stride=strides) \
                     if use_1x1conv else None
        self.bn1 = nn.LazyBatchNorm2d()
        self.bn2 = nn.LazyBatchNorm2d()
    def forward(self, X):
        Y = F.relu(self.bn1(self.conv1(X)))
        Y = self.bn2(self.conv2(Y))
        if self.conv3:
            X = self.conv3(X)
        Y += X
        return F.relu(Y)

Residual(3)(torch.randn(4, 3, 6, 6)).shape                        # [4, 3, 6, 6]
Residual(6, use_1x1conv=True, strides=2)(torch.randn(4, 3, 6, 6)).shape  # [4, 6, 3, 3]

def block(self, num_residuals, num_channels, first_block=False):
    blk = []
    for i in range(num_residuals):
        if i == 0 and not first_block:      # halve resolution, change channels
            blk.append(Residual(num_channels, use_1x1conv=True, strides=2))
        else:
            blk.append(Residual(num_channels))
    return nn.Sequential(*blk)

class ResNet18(ResNet):
    def __init__(self, lr=0.1, num_classes=10):
        super().__init__(((2, 64), (2, 128), (2, 256), (2, 512)), lr, num_classes)
```

The stem is GoogLeNet's with BN added ($7\times7$ conv 64 s2, BN, ReLU, $3\times3$ max-pool s2). The first module keeps resolution because the stem already pooled. Counting layers: $1$ stem conv + $4\times2\times2$ block convs + 1 dense $=18$, hence ResNet-18; more blocks and channels give ResNet-152. (Mine: the Fashion-MNIST ResNet-18 has 11,178,378 parameters.) Training at $96\times96$, `lr=0.01`, shows a large gap between training and validation loss: such a flexible network would benefit from more data.

**Discussion (§8.6.6).** Residual connections change the inductive bias from "simple means $f(\mathbf x)=0$" to "simple means $f(\mathbf x)=\mathbf x$". Inputs propagate faster through the shortcuts, so much deeper networks train (152 layers in the paper), and new layers can be added during training initialized as the identity. Highway networks (2015) had gated shortcuts first; the Transformer uses residual connections throughout.

### 15. ResNeXt: grouped convolution (§8.6.5)

Splitting channels into $g$ groups and convolving within each group cuts parameters and FLOPs by $g$:
$$c_ic_o\ \to\ \frac{c_ic_o}{g}$$
At $c_i=c_o=256$: 65,536 → 16,384 ($g=4$) → 2,048 ($g=32$). No information crosses groups, so the grouped $3\times3$ sits between two $1\times1$ convolutions that mix channels. AlexNet split channels across two GPUs for memory reasons; ResNeXt made it a design choice.

**Code.** The block: $1\times1$ conv to $b$ bottleneck channels → grouped $3\times3$ conv → $1\times1$ conv back to $c$, each with BN, plus the (possibly $1\times1$-projected) shortcut. Cost $O(cb)$ for the $1\times1$ kernels and $O(b^2/g)$ for the grouped $3\times3$. It is a **bottleneck** block when $b<c$.

```python
class ResNeXtBlock(nn.Module):
    def __init__(self, num_channels, groups, bot_mul, use_1x1conv=False, strides=1):
        super().__init__()
        bot_channels = int(round(num_channels * bot_mul))
        self.conv1 = nn.LazyConv2d(bot_channels, kernel_size=1, stride=1)
        self.conv2 = nn.LazyConv2d(bot_channels, kernel_size=3, stride=strides,
                                   padding=1, groups=bot_channels//groups)
        self.conv3 = nn.LazyConv2d(num_channels, kernel_size=1, stride=1)
        self.bn1, self.bn2, self.bn3 = (nn.LazyBatchNorm2d() for _ in range(3))
        if use_1x1conv:
            self.conv4 = nn.LazyConv2d(num_channels, kernel_size=1, stride=strides)
            self.bn4 = nn.LazyBatchNorm2d()
        else:
            self.conv4 = None
    def forward(self, X):
        Y = F.relu(self.bn1(self.conv1(X)))
        Y = F.relu(self.bn2(self.conv2(Y)))
        Y = self.bn3(self.conv3(Y))
        if self.conv4:
            X = self.bn4(self.conv4(X))
        return F.relu(Y + X)

ResNeXtBlock(32, 16, 1)(torch.randn(4, 32, 96, 96)).shape     # [4, 32, 96, 96]
```

> [!note] What `groups` means (discrepancy D11)
> The §8.6.5 prose calls the argument `groups` the number of groups $g$. The code passes `groups=bot_channels//groups` to the convolution, so the argument is really the **group width** (channels per group). `ResNeXtBlock(32, 16, 1)` builds 2 groups of 16 channels, not 16 groups (checked: `conv2.groups == 2`). §8.8 and RegNet use "group width", which matches the code.

Other views: a grouped convolution is a block-diagonal weight matrix. ShiftNet mimics a $3\times3$ convolution at no compute cost by adding shifted activations to channels.

### 16. DenseNet (§8.7)

Instead of adding, concatenate every previous output:
$$\mathbf x\to[\mathbf x,\ f_1(\mathbf x),\ f_2([\mathbf x,f_1(\mathbf x)]),\ \dots]$$
A dense block of $n$ convolutions with growth rate $k$ takes $c_0$ channels to $c_0+nk$ (D2L: $3+10+10=23$, matching `torch.Size([4, 23, 8, 8])`).

Channels grow linearly but parameters grow quadratically, since layer $i$ reads $c_0+(i-1)k$ channels:
$$\text{total}=9k\left[nc_0+\frac{kn(n-1)}{2}\right]$$
At $c_0=64$, $k=32$: 129,024 ($n=4$), 405,504 ($n=8$), 1,400,832 ($n=16$). **Transition layers** ($1\times1$ conv halving channels + average pool s2) control this. ResNet needs none because addition keeps the channel count fixed.

**Code (§8.7).** DenseNet uses ResNet's later "BN → ReLU → conv" order:

```python
def conv_block(num_channels):
    return nn.Sequential(
        nn.LazyBatchNorm2d(), nn.ReLU(),
        nn.LazyConv2d(num_channels, kernel_size=3, padding=1))

class DenseBlock(nn.Module):
    def __init__(self, num_convs, num_channels):
        super(DenseBlock, self).__init__()
        layer = []
        for i in range(num_convs):
            layer.append(conv_block(num_channels))
        self.net = nn.Sequential(*layer)
    def forward(self, X):
        for blk in self.net:
            Y = blk(X)
            X = torch.cat((X, Y), dim=1)    # concatenate along channels
        return X

def transition_block(num_channels):
    return nn.Sequential(
        nn.LazyBatchNorm2d(), nn.ReLU(),
        nn.LazyConv2d(num_channels, kernel_size=1),
        nn.AvgPool2d(kernel_size=2, stride=2))

transition_block(10)(DenseBlock(2, 10)(torch.randn(4, 3, 8, 8))).shape   # [4, 10, 4, 4]
```

The model: ResNet's stem, four dense blocks of 4 convs with growth rate 32 (each adds 128 channels), a transition halving channels and resolution between blocks, then BN, ReLU, global average pooling and a dense layer. Channel trace on $96\times96$ (mine, matches the code): $64\to192\to96\to224\to112\to240\to120\to248$; 758,226 parameters, 14.7× fewer than ResNet-18. Concatenation reuses features but uses a lot of GPU memory (Pleiss et al. 2017 give memory-efficient versions).

### 17. Designing convolutional architectures (§8.8)

**Before: hand design.** VGG popularized $3\times3$ convs, NiN $1\times1$ convs and global pooling, GoogLeNet multi-branch blocks, ResNet the identity bias, ResNeXt grouped convs; **SENet** added per-channel global attention, a precursor to vision Transformers. **Neural architecture search** (NAS) finds one network by brute force, genetic algorithms or RL at enormous cost (EfficientNet came from it). Radosavovic et al. (2020) instead optimize **distributions of networks**, design spaces, which is cheaper and gives design principles.

**AnyNet.** Stem ($3\times3$ conv, stride 2, BN, ReLU: $r\times r\to r/2\times r/2$, $c_0$ channels) → body of 4 stages, each starting with a stride-2 ResNeXt block then more ResNeXt blocks at the same resolution ($224/2^{1+4}=7$) → head (global average pool + dense). Per stage $i$: width $c_i$, depth $d_i$, bottleneck ratio $k_i$, group width $g_i$; with $c_0$ that is 17 parameters. Even two choices each gives $2^{17}=131{,}072$ networks.

```python
class AnyNet(d2l.Classifier):
    def stem(self, num_channels):
        return nn.Sequential(
            nn.LazyConv2d(num_channels, kernel_size=3, stride=2, padding=1),
            nn.LazyBatchNorm2d(), nn.ReLU())
    def stage(self, depth, num_channels, groups, bot_mul):
        blk = []
        for i in range(depth):
            if i == 0:
                blk.append(d2l.ResNeXtBlock(num_channels, groups, bot_mul,
                                            use_1x1conv=True, strides=2))
            else:
                blk.append(d2l.ResNeXtBlock(num_channels, groups, bot_mul))
        return nn.Sequential(*blk)
    def __init__(self, arch, stem_channels, lr=0.1, num_classes=10):
        super(AnyNet, self).__init__()
        self.save_hyperparameters()
        self.net = nn.Sequential(self.stem(stem_channels))
        for i, s in enumerate(arch):
            self.net.add_module(f'stage{i+1}', self.stage(*s))
        self.net.add_module('head', nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten(), nn.LazyLinear(num_classes)))
        self.net.apply(d2l.init_cnn)
```

**Assumptions** that make search cheap: (1) good design principles exist, so many networks in a good space perform well; (2) accuracy after a few epochs predicts final accuracy (multi-fidelity optimization); (3) results on small networks transfer to large ones; (4) design aspects roughly factorize.

**Comparing design spaces.** Sample networks uniformly from a space, train briefly, and compare the **empirical CDF of errors**
$$\hat F(e,\mathcal Z)=\frac1n\sum_{i=1}^n\mathbf 1(e_i\le e).$$
A space whose CDF lies above another's (more networks below each error level) is better. Findings: tying the bottleneck ratio across stages ($k_i=k$) and tying the group width ($g_i=g$) cost nothing (6 fewer parameters); widths and depths should increase across stages, $c_i\le c_{i+1}$, $d_i\le d_{i+1}$ (AnyNetX$_E$). Among the best networks, width grows roughly linearly with block index, $c_j\approx c_0+c_aj$ (approximated piecewise constant per stage), and $k=1$ (no bottleneck) is best.

**RegNetX-32** ($k=1$, group width $g=16$, $c_1=32$, $c_2=80$, $d_1=4$, $d_2=6$):

```python
class RegNetX32(AnyNet):
    def __init__(self, lr=0.1, num_classes=10):
        stem_channels, groups, bot_mul = 32, 16, 1
        depths, channels = (4, 6), (32, 80)
        super().__init__(
            ((depths[0], channels[0], groups, bot_mul),
             (depths[1], channels[1], groups, bot_mul)),
            stem_channels, lr, num_classes)
```

On $96\times96$: stem $32\times48\times48$ → stage 1 $32\times24\times24$ → stage 2 $80\times12\times12$ → 10. (Mine: stem conv + $10\times3$ block convs + dense = 32 layers; 179,290 parameters; stage-2 convs have $80/16=5$ groups.) The principles also hold for SE networks (RegNetY).

**Discussion.** CNNs' inductive biases (locality, translation invariance) made them dominant from LeNet until vision Transformers overtook them in accuracy. Transformers have much weaker biases; they win thanks to huge datasets (LAION-400m, LAION-5B) and hardware that favours them (NVIDIA Ampere, Hopper). Even MLPs (MLP-Mixer) do surprisingly well. D2L's conclusion: at large scale, **scalability trumps inductive biases** ([[08 - Sequence to Sequence|ch. 08]]).

### 18. Where parameters and computation live

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
- Code patterns: `nn.LazyConv2d(c, kernel_size, stride, padding)` (padding per side), `nn.MaxPool2d(k)` (stride = k), blocks as functions returning `nn.Sequential`, `nn.AdaptiveAvgPool2d((1, 1))` for global pooling, `init_cnn` = Xavier.
- BN from scratch: batch statistics in training, moving averages (`momentum=0.1` = weight of the new batch) in prediction; layer norm normalizes per example. The internal-covariate-shift explanation is disputed.
- Design spaces (RegNet): compare error CDFs of sampled networks; share bottleneck ratio and group width, grow width and depth across stages, no bottleneck. At large scale vision Transformers win: scalability beats inductive bias.

## ⚠️ Important Notes

1. `(39c2)` in the PDF means $3\times9c^2$. Reconstruct formulas, do not transcribe them.
2. Pooling's default stride equals its window size; convolution's is 1.
3. If the receptive field is smaller than the object, the network cannot recognize it.
4. Shrinking a model and speeding it up act on different layers (§18).
5. Translation invariance is an assumption; it fails when absolute position matters.
6. Batch norm output depends on the rest of the batch; changing batch size changes regularization.
7. Do not read one channel as one interpretable feature.
8. Kernels imported from signal processing need flipping.
9. Max pooling is not a convolution (it is nonlinear), but $\max(a,b)=a+\mathrm{ReLU}(b-a)$. Average pooling is a convolution with a constant kernel.
10. Global average pooling discards position: fine for classification, not for localization ([[06 - Object Detection|ch. 06]]).
11. Check whether a memory figure means weights only, or weights + gradients + optimizer state (AlexNet's "1 GB").
12. LeNet and AlexNet differ mainly in data, hardware, ReLU, dropout and initialization, not in architecture.
13. Residual, Inception and Dense blocks are variants of one idea: combine an identity/shortcut path with learned branches.
14. Inception branches must keep height and width (padding) so they can be concatenated; residual branches must match the input shape or use a $1\times1$ projection.
15. In D2L's `ResNeXtBlock`, `groups` is the group width; the conv gets `bot_channels // groups` groups (D11).
16. BN `momentum` is not optimizer momentum. A bias directly before BN is wasted.
17. Upsampling $28\times28$ images to $224\times224$ adds compute, not information; D2L does it only to keep the original architectures.
18. DenseNet's concatenations are memory-hungry even though the parameter count is small.

> [!warning] Gaps in the source material
> - **Figures:** diagrams of cross-correlation, padding, channels, pooling, LeNet, Inception, residual and dense blocks are reconstructed from the prose and printed shapes. Lost: Waldo images, biological filters, AlexNet's learned filters, pixel-usage heat maps, the nested function-class diagram, and all training curves (so no accuracies are reported).
> - **Cipher:** `(39c2)` = $3\times9c^2$ (the multiplication sign is deleted, like `1 1` = $1\times1$).
> - **Added by me:** the cascade ratios; all parameter counts and the §17 table; weight-sharing ratios; the receptive-field trace; the stacking table beyond $5\times5$; the AlexNet "1 GB" resolution (D8); the batch-norm noise table; the DenseNet formula; answers to D2L ex. 7.3.1, the odd-kernel question and ex. 7.5.3; the exercise-4 experiment.
> - **Also added by me:** the parameter counts and channel traces of D2L's GoogLeNet, ResNet-18, DenseNet and RegNetX-32 (recomputed in PyTorch, shapes match the printouts); the kernel-learning rerun; the AlexNet 164 MB / 81 MFLOPs check; discrepancy D11 (ResNeXt `groups`).
> - **Lost:** Fashion-MNIST training curves are images, so no accuracies are reported; the design-space CDF plots (Fig. 8.8.2) are lost but their conclusions are stated in the text.
> - **Skipped:** download helpers and plotting code. Augmentation and fine-tuning are in [[06 - Object Detection|ch. 06]].
> - Hardware figures and historical claims are quoted from D2L.

**Previous:** [[04 - Neural Network]] · **Next:** [[06 - Object Detection]]
