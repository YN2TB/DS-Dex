---
subject: Computer Vision
chapter: 5
tags: [ds, computer-vision, initialization, batchnorm, optimizers, augmentation, regularization, alexnet, vgg, googlenet, resnet, transfer-learning]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision Lecture 05: Training Deep Networks & CNN Architectures (48 slides); the original papers listed on slide 47"
---

# Training Deep Networks and CNN Architectures

Week 5. After week 4 we can build and differentiate a small CNN, but we can't yet train anything *deep* (gradients vanish, losses plateau, runs diverge), and we don't know which of the infinitely many ways to stack layers to use. This lecture covers the techniques that make depth trainable (initialisation, normalisation, optimisers, augmentation and regularisation), then the architectures they enabled (LeNet → AlexNet → VGG → GoogLeNet → ResNet and after), then transfer learning.

More detail on the same architectures: [[Deep Learning/contents/05 - Convolutional Neural Network|DL ch. 05]]. On optimisers and initialisation: [[Deep Learning/contents/04 - Neural Network|DL ch. 04]].

## 📘 Main Knowledge

### 1. Initialisation (slides 4–7)

**Why not just small random numbers? (slide 5)**
- **All zeros:** fatal. Every unit in a layer computes the same thing, gets the same gradient, and stays identical forever. The *symmetry never breaks*.
- **Small Gaussian**, $W \sim 0.01\,\mathcal N(0,1)$: fine for a few layers, fatal for many. Activations shrink at every layer until they're numerically zero, and so do the gradients.
- **Large Gaussian**, $W \sim \mathcal N(0,1)$: activations explode, or saturate the nonlinearity.

**The variance argument (slide 6).** For one unit $z = \sum_{i=1}^{n_{in}} w_i x_i$, with $w$ and $x$ independent and zero-mean:

$$\operatorname{Var}(z) = n_{in}\, \operatorname{Var}(w)\, \operatorname{Var}(x)$$

To keep the variance the same from layer to layer we need $n_{in} \operatorname{Var}(w) = 1$, i.e. $\operatorname{Var}(w) = 1/n_{in}$. If it's smaller, the variance shrinks by a constant factor each layer (geometric decay with depth); if larger, it grows geometrically.

**Xavier / Glorot (2010)** balances the forward and backward passes:
$$\operatorname{Var}(w) = \frac{2}{n_{in} + n_{out}}$$
derived for tanh (symmetric around zero).

**He initialisation (2015), the ReLU correction (slide 7).** ReLU sets half its inputs to zero, which halves the variance of what passes through. Compensate with a factor of 2:
$$\operatorname{Var}(w) = \frac{2}{n_{in}}, \qquad w \sim \mathcal N\!\left(0,\ \sqrt{2/n_{in}}\right) \text{ (std)}$$
- Without it a 30-layer ReLU network barely trains; with it, depth is routine.
- It's PyTorch's default for `Conv2d` and `Linear`: `nn.init.kaiming_normal_(w, mode='fan_in', nonlinearity='relu')`. Biases start at zero.
- For a conv layer, $n_{in} = C_{in} \cdot k^2$ (the number of inputs each output unit sums over).

### 2. Normalisation (slides 8–12)

**Batch normalisation (BatchNorm, BN) (slide 9).** Good initialisation sets the scale at step 0, but nothing keeps it there during training. So normalise explicitly, as a layer, over the batch:

$$\hat x^{(k)} = \frac{x^{(k)} - \mu_B^{(k)}}{\sqrt{\big(\sigma_B^{(k)}\big)^2 + \epsilon}}, \qquad z^{(k)} = \gamma^{(k)} \hat x^{(k)} + \beta^{(k)}$$

- $\mu_B$, $\sigma_B$ are computed **per channel**, across the batch (and across all spatial positions, for conv layers).
- $\gamma$ and $\beta$ are **learned** scale and shift. They let the network undo the normalisation if it wants. Forcing zero mean and unit variance would be a constraint: a sigmoid would be pinned to its linear middle region.
- Placed between the convolution and the nonlinearity (conv → BN → ReLU).
- Differentiable, so it trains like any other layer. $\epsilon$ is a small constant to avoid division by zero.

**Pros and cons (slide 10).**

| Pros | Cons |
|---|---|
| much higher learning rates become stable | behaves differently at train and test time (a genuine source of bugs) |
| far less sensitive to initialisation | breaks down at very small batch sizes (the batch statistics become noisy) |
| faster convergence, often several times fewer epochs | |
| mild regularisation: each example is normalised using whichever others share its batch | |

**Train time vs test time (slide 11).**
- **Training:** normalise with the current batch's statistics, and keep a running average of $\mu$ and $\sigma^2$.
- **Inference:** use the stored running averages. A prediction must not depend on which other images happen to be in the batch.

> [!warning] The bug you'll write at least once
> Forget `model.eval()` before validating, and BatchNorm keeps using batch statistics: validation accuracy then depends on batch composition, and a batch of size 1 produces nonsense. Use `model.train()` to switch back. Dropout has the same train/test split.

**The normalisation family (slide 12).** All compute $\hat x = (x - \mu)/\sigma$; they differ in which axes of an $(N, C, H, W)$ tensor $\mu$ and $\sigma$ are computed over.

| Method | Normalises over | Notes |
|---|---|---|
| BatchNorm | $(N, H, W)$, per channel | depends on batch size |
| LayerNorm | $(C, H, W)$, per example | batch-independent; standard in transformers |
| InstanceNorm | $(H, W)$, per example per channel | style transfer |
| GroupNorm | groups of channels, per example | works at batch size 2; used in detection |

**Why BatchNorm works is unsettled.** The original paper said it reduces "internal covariate shift" (the distribution of each layer's inputs changing as earlier layers train). Santurkar et al. (2018) showed the benefit remains even when covariate shift is deliberately added back, and argued it instead smooths the loss landscape. *A rare case of a technique whose usefulness is settled and whose explanation is not.*

### 3. Optimisers (slides 13–17)

**The trouble with plain SGD (slide 14):**
- **Ravines:** when the loss curves much more steeply in one direction than another, SGD zig-zags across the valley and crawls along it.
- **Saddle points:** gradients near zero in every direction. In high dimensions these are far more common than true local minima.
- **One learning rate for every parameter**, however differently they scale.

**Momentum (slide 15):**
$$v \leftarrow \mu v - \eta \nabla_W L, \qquad W \leftarrow W + v, \qquad \mu \approx 0.9$$
- $v$ is a **velocity**: gradients accumulate rather than being applied once.
- Consistent directions build up speed; oscillating ones cancel. So the zig-zag is damped and movement along the valley floor speeds up.
- The effective step size approaches $\eta/(1 - \mu)$, so $\mu = 0.9$ is roughly a 10× amplification.
- Carries the optimiser through small saddles and plateaus.
- **Nesterov momentum** evaluates the gradient *after* the momentum step (a look-ahead correction). Slightly better in theory and usually in practice: `nesterov=True`.
- SGD + momentum 0.9 still trains most vision models today.

**RMSProp (slide 16).** Parameters with consistently large gradients should take smaller steps, and vice versa. Track a running average of the squared gradient:
$$s \leftarrow \beta_2 s + (1 - \beta_2)(\nabla L)^2, \qquad W \leftarrow W - \frac{\eta}{\sqrt{s} + \epsilon} \nabla L$$
(all operations elementwise). This gives each parameter its own effective learning rate.

**Adam** = momentum + RMSProp, with bias correction:
$$m \leftarrow \beta_1 m + (1 - \beta_1)\nabla L, \qquad s \leftarrow \beta_2 s + (1 - \beta_2)(\nabla L)^2$$
$$\hat m = \frac{m}{1 - \beta_1^t}, \qquad \hat s = \frac{s}{1 - \beta_2^t}, \qquad W \leftarrow W - \eta \frac{\hat m}{\sqrt{\hat s} + \epsilon}$$

$m$ and $s$ start at zero, so early on they're biased towards zero; dividing by $1 - \beta^t$ (with $t$ the step number) corrects that. Defaults $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\eta = 10^{-3}$ work surprisingly often.

**Which one?** Adam to get something working fast, and for transformers and generative models. SGD + momentum often generalises slightly better on vision benchmarks if you're willing to tune. *Start with Adam; switch only if you have a reason.*

**Learning rate schedules (slide 17).** A fixed $\eta$ is a compromise: large enough to make progress early is too large to settle later.
- **Step:** multiply by 0.1 at fixed epochs (the classic ResNet recipe).
- **Cosine:** smooth decay to zero; now the default.
- **Exponential:** $\eta_t = \eta_0 \gamma^t$.
- **Warm-up:** start small for a few hundred iterations, then rise. Essential for large batches and transformers.

### 4. Augmentation and regularisation (slides 18–21)

**Data augmentation (slide 19).** Apply label-preserving transformations at training time, so the model sees a different version of every image every epoch.
- **Geometric:** random crop, horizontal flip, small rotation, scaling.
- **Photometric:** brightness, contrast, saturation, hue jitter.
- **Erasing:** Cutout / random erasing (blank out a random patch).
- **Mixing:** MixUp, CutMix (blend two images *and* their labels).

AlexNet's augmentation (random 224×224 crops from 256×256 images, plus flips: $32^2 \times 2 = 2{,}048$ variants of each image) cut its error by over 1%, effectively 2,048× more training data for free.

**Choose augmentations that preserve the label (slide 20).**
- Horizontal flip: fine for cats, **wrong** for digits and text.
- Vertical flip: wrong for almost every natural photo.
- Heavy colour jitter: wrong when colour *is* the class (traffic lights, ripe fruit, medical stains).

The question to ask: *"Could this transformed image plausibly appear in my test set, with the same label?"* Augmentation encodes the invariances you believe the task has: domain knowledge written as code.

**Test-time augmentation (TTA):** average predictions over several crops or flips of the test image. Costs inference time, usually buys 0.5–1%.

**Regularisation in deep networks (slide 21):**

| Method | Where | What it does |
|---|---|---|
| Weight decay (L2) | optimiser | shrinks weights; $10^{-4}$ is the usual starting point |
| Dropout | FC layers | zeroes each unit with probability $p$ at training time, forcing redundancy; largely displaced by BN in conv nets |
| Data augmentation | input | the most effective regulariser in vision |
| Early stopping | training loop | keep the checkpoint with the best validation score |
| Label smoothing | loss | target $1 - \epsilon$ instead of 1 for the true class; discourages over-confidence |

If the train–validation gap is large: reach for **augmentation first, weight decay second, and a smaller model last**.

### 5. CNN architectures (slides 22–36)

**Timeline (slide 23):** LeNet-5 (1998) → AlexNet (2012) → VGG, GoogLeNet (2014) → ResNet (2015) → DenseNet, MobileNet, SENet (2017) → EfficientNet (2019) → ConvNeXt (2022).
- Fourteen years pass between LeNet and AlexNet: the idea wasn't the bottleneck.
- 2012–2015 is when the whole design language was settled.
- After ResNet the goal changes from "deeper" to "cheaper and better-scaled".
- Every later model still uses convolution, BatchNorm, ReLU and residual connections.

**ImageNet results (slide 25).** ILSVRC (the ImageNet Large Scale Visual Recognition Challenge): 1.28M training images, 1,000 classes, scored on top-5 error.

| Year | Winner | Top-5 error |
|---|---|---|
| 2011 | best classical pipeline | 25.8% |
| 2012 | AlexNet | 15.3% (a 10-point jump, "the end of the argument") |
| 2014 | GoogLeNet (VGG 7.3%) | 6.7% |
| 2015 | ResNet | 3.57% |

Human top-5 error on this task is about 5%, crossed in 2015.

**LeNet-5 (1998) (slide 24).** LeCun, Bottou, Bengio and Haffner; built for handwritten and printed character recognition. 5×5 conv layers (stride 1), 2×2 average pooling (stride 2), tanh activations. The $[\text{conv} \to \text{activation} \to \text{pool}] \times N \to \text{FC}$ pattern from [[04 - From Neural Networks to CNNs|ch. 04]].

**AlexNet (2012) (slides 26–27).** Similar to LeNet but deeper and bigger, with conv layers stacked directly on each other.
- 8 weight layers, **60M parameters**, trained on two GTX 580 GPUs for six days.
- First large-scale use of **ReLU** instead of tanh/sigmoid (several times faster to converge).
- **Dropout** in the FC layers; aggressive data augmentation.
- 11×11 first-layer filters with stride 4, huge by modern standards.

*Nothing in it was conceptually new.* What was new: ImageNet (enough data) and GPUs (enough compute). The field's lesson: scale the data and compute, not just the idea.

**VGG (2014): depth through uniformity (slides 28–29).**
- **Only 3×3 convolutions** (stride 1, pad 1) and 2×2 max-pooling. Double the channels after every pool.
- VGG-16 and VGG-19 (16 and 19 weight layers). Showed that depth is essential for good performance.
- Three stacked 3×3 layers have the same 7×7 receptive field as one 7×7 layer, with $27C^2$ parameters instead of $49C^2$ and two extra nonlinearities.
- **Limitation:** 138M parameters, most of them in the first FC layer ($7 \cdot 7 \cdot 512 \cdot 4096 \approx 103$M, about 74% of the total). About 15.5 GFLOPs per image.
- Legacy: *"small filters, uniform blocks, double the channels when you halve the resolution"* still underpins almost every backbone.

**GoogLeNet (2014): efficiency (slides 30–31).** 22 layers but only **5M parameters**, 12× fewer than AlexNet, while winning.
- **Inception module:** run 1×1, 3×3, 5×5 convolutions and pooling **in parallel** on the same input and concatenate the outputs, so the network can choose the scale.
- **1×1 bottlenecks** before the expensive 3×3 and 5×5 branches reduce the channel count first. That's what makes it affordable.
- **No large FC layers**: global average pooling instead.
- **Auxiliary classifiers** partway through, to push gradient into the early layers.

**The degradation problem (slide 32).** Take a working 20-layer network and make it 56 layers: it gets **worse, on the training set**.
- Not overfitting: training error is higher too.
- Not vanishing gradients: BatchNorm already fixed that.
- The deeper network *contains* the shallower one (copy the 20 layers, make the other 36 the identity), so in principle it can never be worse.

So it's an **optimisation** problem: SGD can't find that solution. Learning an identity mapping through a stack of conv layers is apparently hard.

**ResNet (2015): learn the residual (slides 33–34).** He et al. If the identity is hard to learn, build it in and learn only the difference:

$$y = F(x, \{W_i\}) + x$$

- The block only has to produce the **residual** $F$.
- To recover the identity, drive the weights to zero, which weight decay already pushes towards.
- The addition has no parameters.
- Gradients reach earlier layers through the skip path unchanged:
$$\frac{\partial y}{\partial x} = \frac{\partial F}{\partial x} + 1$$
  With the $+1$, the block can never fully kill the gradient.

In practice:
- **ResNet-18/34:** basic blocks of two 3×3 convs.
- **ResNet-50/101/152:** **bottleneck** blocks: 1×1 to reduce channels, 3×3 conv, 1×1 to restore. Cheaper per block, so the network can be deeper. (For 256 channels: $256\cdot64 + 9\cdot64\cdot64 + 64\cdot256 = 69{,}632$ weights, vs $2 \times 9 \cdot 256 \cdot 256 = 1{,}179{,}648$ for two 3×3 convs at full width, about 17× fewer.)
- Every conv is followed by BatchNorm; no FC layers except the classifier, with global average pooling before it.
- When the shape changes (fewer pixels, more channels), the skip path uses a 1×1 stride-2 convolution so $x$ and $F(x)$ can be added.
- ResNet-152: 3.57% top-5, with fewer parameters than VGG-16.

Residual connections turned out to be the general answer to depth: they're in every transformer block, every diffusion U-Net, every large language model.

**After ResNet: four directions (slide 35).**
- **Better connectivity: DenseNet (2017).** Every layer takes *all* previous layers' outputs as input, **concatenated** rather than added. Maximum feature reuse; DenseNet-121 matches ResNet-50 with ~8M parameters instead of 25M, but uses a lot of memory.
- **More paths: ResNeXt (2017).** Replace one wide convolution with $G$ parallel **grouped** convolutions. A third axis besides depth and width, called **cardinality**, which buys more accuracy per parameter than either.
- **Recalibration: SENet (2017).** Squeeze-and-excitation: pool each channel to one number, pass through a small learned gate, and rescale the channels. The network decides which feature maps matter *for this image*. Won the final ILSVRC (2017) at 2.25%.
- **Efficiency: MobileNet (2017).** Built for phones with **depthwise separable convolutions**, ~4M parameters. A depthwise separable convolution splits a standard $k\times k$ conv into a depthwise $k \times k$ conv (one filter per input channel, no channel mixing) followed by a 1×1 conv that mixes channels. Weights drop from $k^2 C_{in} C_{out}$ to $k^2 C_{in} + C_{in} C_{out}$; for $k = 3$ and 256 channels in and out that's 589,824 → 67,840, about 8.7× fewer.

**Side by side (slide 36):**

| Model | Year | Layers | Params | Top-5 | Key idea |
|---|---|---|---|---|---|
| AlexNet | 2012 | 8 | 60M | 15.3% | ReLU, dropout, GPUs |
| VGG-16 | 2014 | 16 | 138M | 7.3% | only 3×3, uniform blocks |
| GoogLeNet | 2014 | 22 | 5M | 6.7% | Inception, 1×1 bottlenecks |
| ResNet-50 | 2015 | 50 | 25M | ~5% | residual connections |
| ResNet-152 | 2015 | 152 | 60M | 3.57% | residual connections |

Error fell by a factor of about four while parameters didn't grow: *depth and structure beat raw size.* **For your project: ResNet-50 unless you have a reason.** It's the default baseline in almost every vision paper and every framework ships pretrained weights.

### 6. Transfer learning (slides 37–44)

**Why not train from scratch? (slide 39).** ImageNet training takes days on many GPUs and 1.28M labelled images; a project has one GPU and perhaps a few thousand images. But the early layers of any trained CNN learn edges, colours and textures, which aren't specific to ImageNet's classes and which your task needs too. Using a pretrained network isn't a shortcut; it's the standard method, and it usually **beats** training from scratch on small data.

**Two modes:**
- **Feature extraction:** freeze the backbone (pretrained layers), replace and train only the final classifier. Fast, few parameters, little risk of overfitting.
- **Fine-tuning:** also update some or all of the backbone, with a much smaller learning rate (10× to 100× smaller) so the pretrained features aren't destroyed.

**Domain (slide 42).** Two domains differ if they have different feature spaces or different input distributions (e.g. natural photos vs X-rays, or daylight vs night images).

**Which strategy? (slide 43)** depends on data size × domain similarity:

| | Similar domain | Different domain |
|---|---|---|
| **Small data** | freeze everything, train the classifier only (fine-tuning would overfit immediately) | the hard case: freeze early layers, train from an intermediate layer; expect to work for your accuracy |
| **Large data** | fine-tune the whole network (safest, best-performing case) | fine-tune everything, or consider training from scratch |

**A practical recipe (slide 44):**

```python
from torchvision import models
m = models.resnet50(weights="DEFAULT")
for p in m.parameters():            # 1. freeze the backbone
    p.requires_grad = False
m.fc = nn.Linear(2048, num_classes) # 2. new head for your classes
opt = torch.optim.Adam(m.fc.parameters(), lr=1e-3)  # 3. train the head only
```

Then, if you have the data: unfreeze the last block or two, drop the learning rate to $10^{-4}$ or below, and continue training.

Two details that bite:
- Use the **same normalisation** the pretrained model was trained with (ImageNet mean and std).
- Keep **BatchNorm layers in eval mode** while the backbone is frozen, or their running statistics will drift towards your data even though the weights are frozen.

**Hands-on (slide 48):** activation collapse at four initialisation scales; verify the $2/n_{in}$ rule and break it; train with and without BatchNorm at a learning rate only one survives; reproduce the `model.eval()` bug; compare SGD, momentum, RMSProp and Adam; inspect an augmentation pipeline; fine-tune a pretrained ResNet-18, frozen vs unfrozen.

## ✏️ Exercises

> [!example]- Exercise 1 — Initialisation scales
> A 10-layer ReLU MLP has 512 units per layer and normalised inputs.
> **(a)** What standard deviation does He initialisation use? Xavier (with $n_{out} = 512$)?
> **(b)** Someone uses $W \sim 0.01\,\mathcal N(0,1)$. By what factor does the activation variance change per layer? After 10 layers? What happens to training?
> **(c)** And with $W \sim \mathcal N(0,1)$?
> **(d)** A colleague initialises all weights to 0 "to be safe". What happens?
>
> ---
> **(a)** He: $\sqrt{2/512} = 0.0625$. Xavier: $\sqrt{2/1024} \approx 0.0442$.
>
> **(b)** Per layer: $n_{in} \operatorname{Var}(w) \times \tfrac12$ (ReLU halves it) $= 512 \times 10^{-4} \times 0.5 = 0.0256$. After 10 layers: $0.0256^{10} \approx 1.2 \times 10^{-16}$ in variance, i.e. the standard deviation shrinks by about $10^{-8}$. The activations, and with them the gradients, are essentially zero in the last layers; the network barely learns.
>
> **(c)** Factor $512 \times 1 \times 0.5 = 256$ per layer: activations explode ($256^{10} \approx 10^{24}$ in variance), giving `inf`/`nan` or saturated units.
>
> **(d)** Every unit in a layer computes the same output and receives the same gradient, so they stay identical forever. Symmetry never breaks, and each layer behaves like a single unit.

> [!example]- Exercise 2 — BatchNorm puzzles
> **(a)** Validation accuracy is 91% with validation batch size 256 but 74% with batch size 16, using the same trained model. What's wrong?
> **(b)** At deployment, single images are classified one at a time and the outputs look random. Same cause?
> **(c)** A detection model only fits batch size 2 on the GPU, and training with BatchNorm is unstable. What would you use instead and why?
> **(d)** You freeze a pretrained ResNet's weights (`requires_grad = False`) and train a new head, but leave the model in `train()` mode. Are the backbone's BN layers really frozen?
>
> ---
> **(a)** The model is in training mode during validation, so BN normalises with each batch's own statistics. Predictions depend on which images share the batch; smaller batches give noisier statistics. Call `model.eval()` before validating.
>
> **(b)** Yes. With batch size 1 in training mode, each channel is normalised using the statistics of a single image, which wipes out the information the network relies on. In eval mode it uses the stored running averages.
>
> **(c)** **GroupNorm** (or LayerNorm). They normalise within each example, so they don't depend on batch size. BN's batch statistics from 2 images are too noisy.
>
> **(d)** No. In `train()` mode BN still updates its running mean and variance from your batches (those aren't parameters, so `requires_grad` doesn't affect them). The statistics drift away from what the frozen weights expect. Put the BN layers (or the whole backbone) in `eval()` mode.

> [!example]- Exercise 3 — Optimiser arithmetic
> **(a)** SGD with momentum, $\eta = 0.01$. What's the effective step size along a direction where the gradient is constant, for $\mu = 0.9$ and $\mu = 0.99$? What does this mean if you raise $\mu$ without touching $\eta$?
> **(b)** Adam at its very first step ($t = 1$) with defaults, and gradient $g$ for some parameter. Compute $m$, $s$, $\hat m$, $\hat s$ and the update. What would the update be *without* bias correction?
> **(c)** Your loss drops quickly, then bounces around a value without improving further. Which schedule change would help?
>
> ---
> **(a)** $\eta/(1-\mu)$: $0.01/0.1 = 0.1$ for $\mu = 0.9$; $0.01/0.01 = 1.0$ for $\mu = 0.99$. Raising $\mu$ from 0.9 to 0.99 is effectively a **10× larger learning rate**, which can make training unstable. Momentum and learning rate must be tuned together.
>
> **(b)** $m = 0.1g$, $s = 0.001g^2$. Bias correction: $\hat m = 0.1g/(1 - 0.9) = g$, $\hat s = 0.001g^2/(1 - 0.999) = g^2$. Update $= \eta\, g/|g| = \eta \cdot \operatorname{sign}(g)$ (ignoring $\epsilon$): a step of size $\eta$. Without correction: $\eta \cdot 0.1g / \sqrt{0.001 g^2} = \eta \cdot 0.1/0.0316 \approx 3.16\eta$, a first step over 3× too large.
>
> **(c)** The learning rate is too large to settle into the minimum. Decay it: a step drop (×0.1) at that point, or a cosine schedule from the start.

> [!example]- Exercise 4 — Read the curves, choose the fix
> **(a)** A plain (no skip connections) 56-layer CNN with BatchNorm has *higher training error* than a 20-layer version. Is this overfitting? Vanishing gradients? What's the fix?
> **(b)** Train accuracy 98%, validation 70%. In what order would you try fixes?
> **(c)** Which augmentations are wrong for each task: (i) handwritten digit recognition, (ii) traffic-light state (red/amber/green), (iii) satellite images of farmland, (iv) street scenes for a self-driving car?
>
> ---
> **(a)** Neither. Overfitting would show low training error; BN handles vanishing gradients. This is the **degradation problem**: the optimiser can't find the solution where the extra layers act as the identity. Add residual connections (ResNet), so each block only learns $F(x)$ and the identity is the default ($F = 0$).
>
> **(b)** Large gap = overfitting. Slide 21's order: (1) data augmentation, (2) weight decay, (3) a smaller model. Early stopping and label smoothing also help, and if you're training from scratch, start from pretrained weights instead.
>
> **(c)**
> - (i) No horizontal flip and no large rotations: a flipped 2 or a rotated 6 changes or destroys the label.
> - (ii) No hue/colour jitter: colour *is* the label. Vertical flip also changes which lamp is on top.
> - (iii) Vertical flips and 90° rotations are fine (there's no "up" from above); strong colour jitter may hide crop types.
> - (iv) Horizontal flip is usually fine; vertical flip is wrong (sky below road never appears at test time). Be careful if the task involves text or driving side.

> [!example]- Exercise 5 — Transfer-learning decisions
> You start from an ImageNet-pretrained ResNet-50 (25.6M parameters, final layer `fc: 2048 → 1000`).
> **(a)** You have 800 photos of 5 kinds of local street food. Which strategy? How many parameters are trained?
> **(b)** You have 200,000 labelled photos of the same 5 kinds. What changes?
> **(c)** You have 600 grayscale chest X-rays labelled normal/abnormal. Why is this the hard case, and what would you do?
> **(d)** In (b), why use a learning rate of $10^{-4}$ for the backbone instead of $10^{-2}$?
>
> ---
> **(a)** Small data, similar domain (natural photos). **Feature extraction**: freeze the backbone, replace `fc` with `Linear(2048, 5)` and train only that: $2048 \cdot 5 + 5 = 10{,}245$ parameters. Fine-tuning 25M parameters on 800 images would overfit.
>
> **(b)** Large data, similar domain: **fine-tune the whole network** (after first training the new head), the safest and best-performing case.
>
> **(c)** Small data **and** a different domain: X-rays look nothing like ImageNet photos, so late-layer features (dog faces, car wheels) don't transfer well; early features (edges, textures) still might. Freeze early layers, fine-tune from an intermediate layer with a small learning rate, use strong but label-preserving augmentation, and expect lower accuracy. Remember to replicate the grayscale channel to 3 channels and apply ImageNet normalisation to match the backbone. (Note: horizontal flips can be questionable for chest X-rays because the heart is on one side.)
>
> **(d)** The pretrained weights are already good. A large learning rate would change them a lot in the first steps (especially while the new head is still random and sending large gradients) and destroy what was learned. A 10–100× smaller rate adjusts them gently.

## 📝 Summary

- **Initialisation:** keep activation variance constant across layers. $\operatorname{Var}(w) = 1/n_{in}$ in general, Xavier $2/(n_{in} + n_{out})$ for tanh, **He $2/n_{in}$ for ReLU** (PyTorch default). All-zero init never breaks symmetry.
- **BatchNorm:** normalise per channel over the batch, then learned $\gamma, \beta$. Allows higher learning rates, less init sensitivity, faster training. Uses batch statistics in training and running averages at test time: call `model.eval()`. LayerNorm (transformers), InstanceNorm (style transfer), GroupNorm (small batches).
- **Optimisers:** momentum ($v \leftarrow \mu v - \eta \nabla L$, effective step $\eta/(1-\mu)$); RMSProp (per-parameter rate from squared gradients); **Adam** = both + bias correction ($\beta_1 = 0.9$, $\beta_2 = 0.999$, $\eta = 10^{-3}$). Schedules: step, cosine, exponential, warm-up.
- **Augmentation** = label-preserving transformations (crop, flip, colour jitter, erasing, MixUp/CutMix); the strongest regulariser in vision, but only if it preserves the label. Other regularisers: weight decay, dropout, early stopping, label smoothing.
- **Architectures:** LeNet (conv-pool pattern) → **AlexNet** (ReLU, dropout, GPUs, 60M) → **VGG** (only 3×3, 138M, mostly in FC) → **GoogLeNet** (Inception, 1×1 bottlenecks, 5M) → **ResNet** ($y = F(x) + x$, solves degradation, $\partial y/\partial x = \partial F/\partial x + 1$) → DenseNet, ResNeXt, SENet, MobileNet.
- **Transfer learning:** feature extraction (freeze, train head) vs fine-tuning (small learning rate). Choose by data size × domain similarity. Default project baseline: pretrained ResNet-50.

## ⚠️ Important Notes

1. **Never initialise all weights to the same value.** Symmetric units stay symmetric forever.
2. **He init is for ReLU, Xavier for tanh.** Using Xavier with ReLU loses half the variance per layer.
3. **`model.eval()` before validation and inference; `model.train()` before training.** Both BatchNorm and Dropout change behaviour.
4. **BatchNorm needs reasonable batch sizes.** At batch size 1–2, use GroupNorm or LayerNorm.
5. **Frozen weights ≠ frozen BatchNorm statistics.** Running averages still update in training mode.
6. **Momentum multiplies the effective learning rate by $1/(1-\mu)$.** Changing $\mu$ changes the step size.
7. **Adam's bias correction matters most in the first steps**; without it the first update is about 3× too large with default settings.
8. **Start with Adam, but SGD + momentum often generalises slightly better on vision benchmarks** if tuned.
9. **Augmentations must preserve the label.** Flip, rotation and colour jitter are task-dependent, not universal.
10. **The degradation problem is not overfitting** (training error is worse too) and not vanishing gradients (BN is present). It's an optimisation problem that residual connections fix.
11. **The ResNet skip path needs matching shapes.** When resolution or channel count changes, use a 1×1 (stride-2) convolution on the skip path.
12. **Most of VGG's parameters are in its first FC layer**, not its convolutions. Parameter count and computation live in different parts of a CNN.
13. **Fine-tune with a learning rate 10–100× smaller** than for training from scratch, and use the pretrained model's input normalisation.
14. **Top-5 numbers depend on the setting** (single model vs ensemble, extra data). AlexNet is quoted as 16.4% in Lecture 04 and 15.3% here; both are published figures for different configurations.

> [!warning] Gaps in the source material
> - **Figures lost in extraction:** activation std through 10 layers (slide 5), with/without BN curves (10), four optimisers on a ravine (14), four schedules (17), eight augmented views (19), LeNet/AlexNet/VGG/GoogLeNet/ResNet diagrams (24, 26, 28, 30, 33), top-5 by year (25), degradation curves (32), feature extraction vs fine-tuning diagrams (38, 40–42). Described from captions and text.
> - **Missing slide:** slide 35 says "The next slide is how it works" for MobileNet's depthwise separable convolutions, but the next slide in the deck is the comparison table. The explanation and the 8.7× example in §5 are added from Howard et al. (2017).
> - **Possible inaccuracy, slide 29:** "VGG-16 needs about 15.5 GFLOPs per image — roughly 4× GoogLeNet". GoogLeNet's paper gives about 1.5 billion multiply-adds, which makes VGG-16 roughly **10×**, not 4×. Not counted as a certain error, since FLOP-counting conventions vary; worth checking with the lecturer.
> - **Added beyond the slides:** Adam's bias-correction formulas ($\hat m$, $\hat s$ are named but not written on the slide); $n_{in} = C_{in}k^2$ for conv layers; the AlexNet 2,048 derivation; the VGG first-FC parameter count; the ResNet bottleneck parameter comparison; the depthwise separable explanation; all exercises and Important Notes.
> - **Removed from the previous version of this note:** EfficientNet's compound scaling (not in the lecture; only named on the timeline).

**Previous:** [[04 - From Neural Networks to CNNs]] · **Next:** [[06 - Vision Transformers]]
