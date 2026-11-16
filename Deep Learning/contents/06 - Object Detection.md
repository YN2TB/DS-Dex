---
subject: Deep Learning
chapter: 6
tags: [ds, deep-learning, object-detection, anchor-boxes, iou, nms, ssd, r-cnn, transfer-learning, augmentation]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, §14.1–14.8 (Image Augmentation, Fine-Tuning, Bounding Boxes, Anchor Boxes, Multiscale Detection, the Detection Dataset, SSD, R-CNNs)"
---

# Object Detection

Classification says what is in an image; detection says what and where, for every object. D2L §14.1–14.8 covers augmentation and fine-tuning, then bounding boxes, anchor boxes, IoU, anchor labelling, non-maximum suppression, multiscale detection, SSD and the R-CNN family. Every printed tensor in this range was recomputed and matches; no discrepancies were found. The note follows D2L's order and includes its code for each step, from augmentation to TinySSD.

## 📘 Main Knowledge

### 1. Image augmentation (§14.1)

Large datasets are a prerequisite for deep networks ([[05 - Convolutional Neural Network|ch. 05]] §9). **Image augmentation** applies random changes to training images, producing similar but distinct examples. It enlarges the training set and, more importantly, makes the model rely less on attributes such as an object's position or colour. D2L thinks augmentation was probably essential to AlexNet's success.

Each augmentation assumes the label does not change under that transformation. A horizontal flip is fine for cats but wrong for digits, text or anything with handedness. Choose augmentations from the task's actual symmetries.

**Common methods** (`torchvision.transforms`, shown on a $400\times500$ cat photo):

| transform | what it does |
|---|---|
| `RandomHorizontalFlip()` | flip left–right with probability 0.5; the oldest and most common |
| `RandomVerticalFlip()` | flip up–down with probability 0.5; less common |
| `RandomResizedCrop((200, 200), scale=(0.1, 1), ratio=(0.5, 2))` | crop 10%–100% of the area with width/height ratio in $[0.5,2]$, resize to $200\times200$: objects appear at different positions and scales |
| `ColorJitter(brightness=0.5, contrast=0, saturation=0, hue=0)` | brightness randomly 50%–150% of the original |
| `ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5)` | all four colour aspects at once |
| `Compose([RandomHorizontalFlip(), color_aug, shape_aug])` | chain several augmentations |

Random values in this section are drawn uniformly from the stated interval. Cropping complements pooling ([[05 - Convolutional Neural Network|ch. 05]] §6) in reducing sensitivity to position.

**Training with augmentation.** CIFAR-10 instead of Fashion-MNIST, because Fashion-MNIST objects are already normalized in position and size while CIFAR-10's vary in colour and size. Augment only the training set; at prediction time use no random operations so results are deterministic. `ToTensor()` converts images to float32 in $[0,1]$ with shape (batch, channels, height, width).

```python
train_augs = torchvision.transforms.Compose([
    torchvision.transforms.RandomHorizontalFlip(),
    torchvision.transforms.ToTensor()])
test_augs = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor()])

def load_cifar10(is_train, augs, batch_size):
    dataset = torchvision.datasets.CIFAR10(root="../data", train=is_train,
                                           transform=augs, download=True)
    return torch.utils.data.DataLoader(dataset, batch_size=batch_size,
        shuffle=is_train, num_workers=d2l.get_dataloader_workers())
```

`train_ch13` trains with `nn.DataParallel` over all GPUs, using `CrossEntropyLoss(reduction="none")` summed per batch. `train_with_data_aug` trains ResNet-18 (10 classes, 3 input channels) with Adam, `lr=0.001`, batch 256, 10 epochs. With random flips only: train loss 0.226, train acc 0.920, **test acc 0.840** (3322 examples/s on two GPUs). D2L's exercise asks you to rerun with `train_with_data_aug(test_augs, test_augs)` to see whether the train–test gap (0.920 vs 0.840) grows without augmentation; note that one such comparison supports, but cannot prove, that augmentation reduces overfitting.

### 2. Fine-tuning (§14.2)

Typical datasets sit between Fashion-MNIST (60,000 images) and ImageNet (over 10 million images, 1000 classes). D2L's example: recognizing 100 kinds of chair from 1000 photos each, a tenth of ImageNet's size, so ImageNet-scale models would overfit. Collecting more data is expensive (ImageNet cost millions of dollars). **Transfer learning** moves knowledge from a **source dataset** to a **target dataset**: features learned on ImageNet (edges, textures, shapes, object parts) help with chairs too.

**Fine-tuning** steps:

1. Pretrain a **source model** on the source dataset (ImageNet).
2. Create a **target model** copying all layers and parameters except the output layer (the output layer is tied to the source labels).
3. Add a new output layer with as many outputs as target classes, randomly initialized.
4. Train on the target data: the new layer from scratch, the others fine-tuned from their pretrained values.

**Hot dog recognition.** 1400 hot-dog images and 1400 other-food images; 1000 of each class for training, the rest for testing (`ImageFolder` over `hotdog/train` and `hotdog/test`). Images vary in size and aspect ratio.

```python
normalize = torchvision.transforms.Normalize(
    [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])      # ImageNet channel stats
train_augs = torchvision.transforms.Compose([
    torchvision.transforms.RandomResizedCrop(224),
    torchvision.transforms.RandomHorizontalFlip(),
    torchvision.transforms.ToTensor(), normalize])
test_augs = torchvision.transforms.Compose([
    torchvision.transforms.Resize([256, 256]),
    torchvision.transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(), normalize])

pretrained_net = torchvision.models.resnet18(pretrained=True)
pretrained_net.fc          # Linear(in_features=512, out_features=1000, bias=True)

finetune_net = torchvision.models.resnet18(pretrained=True)
finetune_net.fc = nn.Linear(finetune_net.fc.in_features, 2)
nn.init.xavier_uniform_(finetune_net.fc.weight)

def train_fine_tuning(net, learning_rate, batch_size=128, num_epochs=5,
                      param_group=True):
    ...
    if param_group:
        params_1x = [param for name, param in net.named_parameters()
                     if name not in ["fc.weight", "fc.bias"]]
        trainer = torch.optim.SGD([{'params': params_1x},
                                   {'params': net.fc.parameters(),
                                    'lr': learning_rate * 10}],
                                  lr=learning_rate, weight_decay=0.001)
    else:
        trainer = torch.optim.SGD(net.parameters(), lr=learning_rate,
                                  weight_decay=0.001)
    d2l.train_ch13(net, train_iter, test_iter, loss, trainer, num_epochs, devices)
```

Each RGB channel is standardized with ImageNet's per-channel mean and standard deviation, because the pretrained network expects inputs scaled that way.

| run | lr | train loss | train acc | test acc |
|---|---|---|---|---|
| fine-tuned (head at 10× = $5\times10^{-4}$) | $5\times10^{-5}$ | 0.204 | 0.918 | **0.926** |
| same ResNet-18 from random init | $5\times10^{-4}$ | 0.459 | 0.819 | 0.871 |

Pretrained weights are already close to right, so they get a small rate; the random head needs a larger one. A single large learning rate for everything can wreck the pretrained backbone. The fine-tuned model is better at the same epoch count because its starting point is better. This relies on the stem/body/head split of [[05 - Convolutional Neural Network|ch. 05]]: early layers learn general features.

Variants in D2L's exercises: freeze the backbone (`param.requires_grad = False` for all but the head) and train only the new layer; or reuse ImageNet's own "hotdog" class, whose output weights are row 934 of `pretrained_net.fc.weight` (shape `[1, 512]`), to initialize the new head.

### 3. Bounding boxes and IoU (§14.3, §14.4.2)

A box is $(x_1,y_1,x_2,y_2)$ (corners) or $(c_x,c_y,w,h)$ (centre and size).

**Intersection over union** (Jaccard index):
$$J(\mathcal A,\mathcal B)=\frac{|\mathcal A\cap\mathcal B|}{|\mathcal A\cup\mathcal B|}\in[0,1]$$

For two unit squares shifted horizontally by $d$:
$$\mathrm{IoU}=\frac{1-d}{1+d}$$

| $d$ | IoU |
|---|---|
| 0 | 1.0000 |
| 1/3 | 0.5000 |
| 0.5 | 0.3333 |
| 1 | 0 |

IoU 0.5 needs the boxes to share two-thirds of their width, since the union grows as the intersection shrinks. IoU 0.5 is also reached by a box with half the area nested inside another (side $\sqrt2$ inside side 2). So IoU cannot tell "wrong place" from "wrong size", and every pair of disjoint boxes scores 0, which gives no gradient. (GIoU/DIoU losses address this; beyond D2L.)

**Code (§14.3, §14.4.2).** Image coordinates start at the upper-left corner; $x$ grows to the right and $y$ downward. D2L's dog and cat boxes are `[60, 45, 378, 516]` and `[400, 112, 655, 493]`; converting corner → centre → corner returns them exactly.

```python
def box_corner_to_center(boxes):
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w, h = x2 - x1, y2 - y1
    return torch.stack((cx, cy, w, h), axis=-1)

def box_center_to_corner(boxes):
    cx, cy, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    x1, y1 = cx - 0.5 * w, cy - 0.5 * h
    x2, y2 = cx + 0.5 * w, cy + 0.5 * h
    return torch.stack((x1, y1, x2, y2), axis=-1)

def box_iou(boxes1, boxes2):
    box_area = lambda boxes: ((boxes[:, 2] - boxes[:, 0]) *
                              (boxes[:, 3] - boxes[:, 1]))
    areas1, areas2 = box_area(boxes1), box_area(boxes2)
    inter_upperlefts = torch.max(boxes1[:, None, :2], boxes2[:, :2])
    inter_lowerrights = torch.min(boxes1[:, None, 2:], boxes2[:, 2:])
    inters = (inter_lowerrights - inter_upperlefts).clamp(min=0)
    inter_areas = inters[:, :, 0] * inters[:, :, 1]
    union_areas = areas1[:, None] + areas2 - inter_areas
    return inter_areas / union_areas      # shape (n1, n2)
```

`boxes1[:, None, :2]` broadcasts every box of the first list against every box of the second; `clamp(min=0)` makes disjoint boxes have zero intersection. Labelling a box takes longer than labelling a class, which is one reason detection datasets are small.

### 4. Anchor boxes (§14.4.1)

At each pixel, generate boxes with scale $s\in(0,1]$ and aspect ratio $r$: width $ws\sqrt r$, height $hs/\sqrt r$. With $n$ scales and $m$ ratios, D2L keeps only combinations containing $s_1$ or $r_1$:
$$(s_1,r_1),\dots,(s_1,r_m),(s_2,r_1),\dots,(s_n,r_1)\quad\Rightarrow\quad n+m-1 \text{ per pixel}$$
(44.4% fewer than all $nm$ pairs at $3\times3$.)

On a $561\times728$ image with 5 anchors per pixel: $561\times728\times5=2{,}042{,}040$ anchors, matching D2L's `torch.Size([1, 2042040, 4])`. With one class and four offsets each, that is 38.9 MB of labels for one image. Placing anchors at every pixel is the real cost; §7 fixes it.

**Code.** `multibox_prior` returns all anchors as normalized corner coordinates, shape (1, number of anchors, 4):

```python
def multibox_prior(data, sizes, ratios):
    in_height, in_width = data.shape[-2:]
    device, num_sizes, num_ratios = data.device, len(sizes), len(ratios)
    boxes_per_pixel = (num_sizes + num_ratios - 1)
    size_tensor = torch.tensor(sizes, device=device)
    ratio_tensor = torch.tensor(ratios, device=device)
    offset_h, offset_w = 0.5, 0.5              # centre of each pixel
    steps_h, steps_w = 1.0 / in_height, 1.0 / in_width
    center_h = (torch.arange(in_height, device=device) + offset_h) * steps_h
    center_w = (torch.arange(in_width, device=device) + offset_w) * steps_w
    shift_y, shift_x = torch.meshgrid(center_h, center_w, indexing='ij')
    shift_y, shift_x = shift_y.reshape(-1), shift_x.reshape(-1)
    w = torch.cat((size_tensor * torch.sqrt(ratio_tensor[0]),
                   sizes[0] * torch.sqrt(ratio_tensor[1:]))) \
        * in_height / in_width                 # handle rectangular inputs
    h = torch.cat((size_tensor / torch.sqrt(ratio_tensor[0]),
                   sizes[0] / torch.sqrt(ratio_tensor[1:])))
    anchor_manipulations = torch.stack((-w, -h, w, h)).T.repeat(
        in_height * in_width, 1) / 2
    out_grid = torch.stack([shift_x, shift_y, shift_x, shift_y],
                           dim=1).repeat_interleave(boxes_per_pixel, dim=0)
    output = out_grid + anchor_manipulations
    return output.unsqueeze(0)
```

With `sizes=[0.75, 0.5, 0.25]`, `ratios=[1, 2, 0.5]` on the $561\times728$ image, `Y.reshape(h, w, 5, 4)[250, 250, 0, :]` is `[0.06, 0.07, 0.63, 0.82]`. Check: centre $(250.5/728,\ 250.5/561)=(0.344,0.447)$; width $0.75\cdot561/728=0.578$ in $x$-units, height $0.75$: corners $(0.055, 0.072, 0.633, 0.822)$. The factor `in_height / in_width` makes a ratio-1 anchor square in pixels on a non-square image. Multiply by `(w, h, w, h)` to get pixels for plotting.

### 5. Labelling anchors (§14.4.3)

Each anchor needs a class and four offsets. Given the IoU matrix $\mathbf X$ (anchors × ground-truth boxes):

1. Take the largest $x_{ij}$, assign box $B_j$ to anchor $A_i$, and remove row $i$ and column $j$.
2. Repeat until every ground-truth box is assigned.
3. Every other anchor gets its best box only if that IoU exceeds a threshold (0.5); otherwise it is background.

D2L's example (IoU matrix computed here):

| | dog | cat |
|---|---|---|
| $A_0$ | 0.053648 | 0 |
| $A_1$ | 0.141723 | 0 |
| $A_2$ | 0 | 0.565724 |
| $A_3$ | 0 | 0.205882 |
| $A_4$ | 0 | 0.745908 |

$A_4$ → cat (0.7459); then $A_1$ → dog (0.1417). Threshold pass: $A_0$ background, $A_2$ cat (0.5657), $A_3$ background. Result `[0, 1, 2, 0, 2]`, as printed.

Step 2 guarantees every object at least one anchor, which is why $A_1$ is labelled dog despite IoU 0.14. Without it, small or oddly shaped objects could have no positive anchors.

**Offsets** encode the box relative to the anchor, standardized:
$$\left(\frac{(x_b-x_a)/w_a}{0.1},\ \frac{(y_b-y_a)/h_a}{0.1},\ \frac{\log(w_b/w_a)}{0.2},\ \frac{\log(h_b/h_a)}{0.2}\right)$$
i.e. centre offsets ×10, log size ratios ×5, so one $\ell_1$ loss weights all four similarly. Decoding must undo the scaling. All 20 printed offsets and the mask reproduce from the five anchors and two boxes. (Offset 18 prints `4.17e-06`; the two widths are equal, so the exact value is $5\log1=0$.)

**Code.** D2L's implementation does the threshold pass first and then the greedy pass, which overrides; the result is the same as the order described above.

```python
def assign_anchor_to_bbox(ground_truth, anchors, device, iou_threshold=0.5):
    num_anchors, num_gt_boxes = anchors.shape[0], ground_truth.shape[0]
    jaccard = box_iou(anchors, ground_truth)
    anchors_bbox_map = torch.full((num_anchors,), -1, dtype=torch.long,
                                  device=device)
    max_ious, indices = torch.max(jaccard, dim=1)
    anc_i = torch.nonzero(max_ious >= iou_threshold).reshape(-1)
    box_j = indices[max_ious >= iou_threshold]
    anchors_bbox_map[anc_i] = box_j
    col_discard = torch.full((num_anchors,), -1)
    row_discard = torch.full((num_gt_boxes,), -1)
    for _ in range(num_gt_boxes):
        max_idx = torch.argmax(jaccard)               # largest remaining IoU
        box_idx = (max_idx % num_gt_boxes).long()
        anc_idx = (max_idx / num_gt_boxes).long()
        anchors_bbox_map[anc_idx] = box_idx
        jaccard[:, box_idx] = col_discard
        jaccard[anc_idx, :] = row_discard
    return anchors_bbox_map

def offset_boxes(anchors, assigned_bb, eps=1e-6):
    c_anc = d2l.box_corner_to_center(anchors)
    c_assigned_bb = d2l.box_corner_to_center(assigned_bb)
    offset_xy = 10 * (c_assigned_bb[:, :2] - c_anc[:, :2]) / c_anc[:, 2:]
    offset_wh = 5 * torch.log(eps + c_assigned_bb[:, 2:] / c_anc[:, 2:])
    return torch.cat([offset_xy, offset_wh], axis=1)
```

(The `eps` inside the log is why offset 18 prints `4.17e-06` instead of 0: $5\log(1+10^{-6})=5.0\times10^{-6}$, minus float rounding.) The general form of the offsets has means $\mu_x=\mu_y=\mu_w=\mu_h=0$ and standard deviations $\sigma_x=\sigma_y=0.1$, $\sigma_w=\sigma_h=0.2$:
$$\left(\frac{\frac{x_b-x_a}{w_a}-\mu_x}{\sigma_x},\ \frac{\frac{y_b-y_a}{h_a}-\mu_y}{\sigma_y},\ \frac{\log\frac{w_b}{w_a}-\mu_w}{\sigma_w},\ \frac{\log\frac{h_b}{h_a}-\mu_h}{\sigma_h}\right).$$

`multibox_target(anchors, labels)` loops over the batch, calls `assign_anchor_to_bbox` on `label[:, 1:]`, sets each positive anchor's class to the box's class **+ 1** (0 is background), fills a mask of four 1s per positive anchor, and multiplies the offsets by the mask. It returns `(bbox_offset, bbox_mask, class_labels)`. In D2L's example the dog box is `[0.1, 0.08, 0.52, 0.92]` and the cat box `[0.55, 0.2, 0.9, 0.88]` (normalized), with anchors $A_0,\dots,A_4$ = `[0, 0.1, 0.2, 0.3]`, `[0.15, 0.2, 0.4, 0.4]`, `[0.63, 0.05, 0.88, 0.98]`, `[0.66, 0.45, 0.8, 0.8]`, `[0.57, 0.3, 0.92, 0.9]`; it prints classes `[0, 1, 2, 0, 2]`.

### 6. Non-maximum suppression (§14.4.4)

Many anchors cover the same object. NMS sorts predictions by confidence, keeps the top one, deletes all boxes with IoU above $\epsilon$ with it, and repeats.

D2L's example (confidences 0.90, 0.80, 0.70, 0.90; $\epsilon=0.5$):

| | $B_0$ | $B_1$ | $B_2$ | $B_3$ |
|---|---|---|---|---|
| $B_0$ | 1 | 0.7368 | 0.5454 | 0 |
| $B_1$ | 0.7368 | 1 | 0.6306 | 0.0115 |
| $B_2$ | 0.5454 | 0.6306 | 1 | 0.0839 |
| $B_3$ | 0 | 0.0115 | 0.0839 | 1 |

Keep $B_0$, delete $B_1$ and $B_2$; keep $B_3$. Matches D2L.

NMS only uses geometry. Two real objects that overlap above $\epsilon$ (people side by side, cars in a queue) lose the lower-scoring one permanently. The threshold trades duplicate detections for missed objects (D2L ex. 14.4.4). Soft-NMS lowers scores instead of deleting.

**Code.** Decoding inverts the offset transform; `nms` is the greedy loop; `multibox_detection` puts them together:

```python
def offset_inverse(anchors, offset_preds):
    anc = d2l.box_corner_to_center(anchors)
    pred_bbox_xy = (offset_preds[:, :2] * anc[:, 2:] / 10) + anc[:, :2]
    pred_bbox_wh = torch.exp(offset_preds[:, 2:] / 5) * anc[:, 2:]
    pred_bbox = torch.cat((pred_bbox_xy, pred_bbox_wh), axis=1)
    return d2l.box_center_to_corner(pred_bbox)

def nms(boxes, scores, iou_threshold):
    B = torch.argsort(scores, dim=-1, descending=True)
    keep = []
    while B.numel() > 0:
        i = B[0]
        keep.append(i)
        if B.numel() == 1: break
        iou = box_iou(boxes[i, :].reshape(-1, 4),
                      boxes[B[1:], :].reshape(-1, 4)).reshape(-1)
        inds = torch.nonzero(iou <= iou_threshold).reshape(-1)
        B = B[inds + 1]
    return torch.tensor(keep, device=boxes.device)
```

`multibox_detection(cls_probs, offset_preds, anchors, nms_threshold=0.5, pos_threshold=0.009999999)`, per image: take each anchor's best non-background class and its probability as confidence, decode boxes, run `nms` on **all** boxes regardless of class, mark suppressed boxes as class −1, and also mark boxes whose confidence is below `pos_threshold` as −1 (storing $1-\text{conf}$). Output rows are `[class, confidence, x1, y1, x2, y2]`, kept boxes first.

D2L's example uses zero offsets (predicted boxes = anchors) and class probabilities dog $(0.9, 0.8, 0.7, 0.1)$, cat $(0.1, 0.2, 0.3, 0.9)$, background 0:

```
[[ 0.00, 0.90, 0.10, 0.08, 0.52, 0.92],    # dog, kept
 [ 1.00, 0.90, 0.55, 0.20, 0.90, 0.88],    # cat, kept
 [-1.00, 0.80, 0.08, 0.20, 0.56, 0.95],    # suppressed
 [-1.00, 0.70, 0.15, 0.30, 0.62, 0.91]]    # suppressed
```

In practice, drop low-confidence boxes before NMS to save work, and keep only high-confidence results afterwards.

### 7. Multiscale detection (§14.5)

Put anchors on feature maps instead of pixels. Each feature-map cell has a receptive field covering a patch of the image ([[05 - Convolutional Neural Network|ch. 05]] §7).

TinySSD uses five levels with 4 anchors per cell:
$$(32^2+16^2+8^2+4^2+1)\times4=5{,}444$$

| map | cells | anchors | stride | anchor scales | object size (px) |
|---|---|---|---|---|---|
| 32×32 | 1,024 | 4,096 | 8 | 0.20–0.272 | 51–70 |
| 16×16 | 256 | 1,024 | 16 | 0.37–0.447 | 95–114 |
| 8×8 | 64 | 256 | 32 | 0.54–0.619 | 138–158 |
| 4×4 | 16 | 64 | 64 | 0.71–0.790 | 182–202 |
| 1×1 | 1 | 4 | 256 | 0.88–0.961 | 225–246 |

Against per-pixel anchors on the same $256\times256$ image this is 48× fewer, whatever the number of anchors per position (it cancels). Each level covers a different object size. Scales split $[0.2,1.05]$ evenly, and each level's second scale is the geometric mean with the next ($\sqrt{0.2\times0.37}=0.272$, …), all matching D2L.

D2L's intuition: on a $2\times2$ image, $1\times1$, $1\times2$ and $2\times2$ objects fit in 4, 2 and 1 positions, so small objects need more samples.

**Code (§14.5).** Anchors are centred on the cells of a feature map, so their centres are spread uniformly over any input image:

```python
def display_anchors(fmap_w, fmap_h, s):
    fmap = torch.zeros((1, 10, fmap_h, fmap_w))   # only the last two dims matter
    anchors = d2l.multibox_prior(fmap, sizes=s, ratios=[1, 2, 0.5])
    bbox_scale = torch.tensor((w, h, w, h))
    d2l.show_bboxes(d2l.plt.imshow(img).axes, anchors[0] * bbox_scale)

display_anchors(fmap_w=4, fmap_h=4, s=[0.15])   # 16 centres, small boxes
display_anchors(fmap_w=2, fmap_h=2, s=[0.4])    # 4 centres, boxes overlap
display_anchors(fmap_w=1, fmap_h=1, s=[0.8])    # 1 centre: the image centre
```

**Why it works.** At one scale there are $c$ feature maps of size $h\times w$, giving $hw$ sets of $a$ anchors. The $c$ units at one spatial position share a receptive field on the input, so they can predict the classes and offsets of the $a$ anchors centred there. Layers closer to the output have larger receptive fields and detect larger objects.

### 8. The object detection dataset (§14.6)

There is no small detection dataset like MNIST, so D2L made one: photos of a banana (in different rotations, sizes and positions) pasted onto backgrounds, $256\times256$ pixels, 1000 training and 100 validation images, one banana per image. Labels come from a CSV file with class and box corners.

```python
def read_data_bananas(is_train=True):
    data_dir = d2l.download_extract('banana-detection')
    csv_fname = os.path.join(data_dir, 'bananas_train' if is_train
                             else 'bananas_val', 'label.csv')
    csv_data = pd.read_csv(csv_fname).set_index('img_name')
    images, targets = [], []
    for img_name, target in csv_data.iterrows():
        images.append(torchvision.io.read_image(os.path.join(
            data_dir, 'bananas_train' if is_train else 'bananas_val',
            'images', f'{img_name}')))
        targets.append(list(target))       # (class, x1, y1, x2, y2), class 0
    return images, torch.tensor(targets).unsqueeze(1) / 256

class BananasDataset(torch.utils.data.Dataset):
    def __init__(self, is_train):
        self.features, self.labels = read_data_bananas(is_train)
    def __getitem__(self, idx):
        return (self.features[idx].float(), self.labels[idx])
    def __len__(self):
        return len(self.features)
```

A minibatch is images `[32, 3, 256, 256]` and labels `[32, 1, 5]`: (batch, $m$, 5), where $m$ is the largest number of boxes in any image. Images with fewer boxes are padded with illegal boxes of class −1, so every image in a batch has $m$ label rows. Here $m=1$. Dividing by 256 normalizes coordinates to $[0,1]$.

### 9. SSD (§14.7)

Single Shot Multibox Detection (Liu et al. 2016): a base network followed by downsampling blocks; each block's feature map generates anchors and predicts their classes and offsets.

The heads are $3\times3$ convolutions: $a(q+1)$ output channels for classes and $4a$ for offsets. Checked: $5\times11=55$ and $3\times11=33$ channels, concatenated length $20^2\cdot55+10^2\cdot33=25{,}300$; TinySSD's 5,444 anchors give 21,776 offsets.

A dense class head on one 64-channel $32\times32$ map ($a=4$, $q=1$) would need 536,879,104 parameters; the $3\times3$ conv needs 4,616. All five TinySSD heads total 124,536 parameters.

Each downsampling block (two $3\times3$ convs + $2\times2$ pool) has a $6\times6$ receptive field on its input.

Loss: cross-entropy on anchor classes + $\ell_1$ on offsets of positive anchors only (masked). D2L uses $\ell_1$ so that a few large offsets do not dominate.

**Code (§14.7).**

```python
def cls_predictor(num_inputs, num_anchors, num_classes):
    return nn.Conv2d(num_inputs, num_anchors * (num_classes + 1),
                     kernel_size=3, padding=1)

def bbox_predictor(num_inputs, num_anchors):
    return nn.Conv2d(num_inputs, num_anchors * 4, kernel_size=3, padding=1)
```

Output channel $i(q+1)+j$ at a position is the score of class $j$ for anchor $i$ centred there. Different scales give different shapes, so predictions are flattened with channels last, then concatenated:

```python
def flatten_pred(pred):
    return torch.flatten(pred.permute(0, 2, 3, 1), start_dim=1)
def concat_preds(preds):
    return torch.cat([flatten_pred(p) for p in preds], dim=1)

def down_sample_blk(in_channels, out_channels):      # VGG-style: halves h, w
    blk = []
    for _ in range(2):
        blk.append(nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1))
        blk.append(nn.BatchNorm2d(out_channels))
        blk.append(nn.ReLU())
        in_channels = out_channels
    blk.append(nn.MaxPool2d(2))
    return nn.Sequential(*blk)

def base_net():                                      # 3 -> 16 -> 32 -> 64 channels
    blk = []
    num_filters = [3, 16, 32, 64]
    for i in range(len(num_filters) - 1):
        blk.append(down_sample_blk(num_filters[i], num_filters[i + 1]))
    return nn.Sequential(*blk)                       # 256x256 -> 64x32x32

def get_blk(i):
    if i == 0:   blk = base_net()
    elif i == 1: blk = down_sample_blk(64, 128)
    elif i == 4: blk = nn.AdaptiveMaxPool2d((1, 1))
    else:        blk = down_sample_blk(128, 128)
    return blk

def blk_forward(X, blk, size, ratio, cls_predictor, bbox_predictor):
    Y = blk(X)
    anchors = d2l.multibox_prior(Y, sizes=size, ratios=ratio)
    return (Y, anchors, cls_predictor(Y), bbox_predictor(Y))

sizes = [[0.2, 0.272], [0.37, 0.447], [0.54, 0.619], [0.71, 0.79], [0.88, 0.961]]
ratios = [[1, 2, 0.5]] * 5
num_anchors = len(sizes[0]) + len(ratios[0]) - 1     # 4

class TinySSD(nn.Module):
    def __init__(self, num_classes, **kwargs):
        super(TinySSD, self).__init__(**kwargs)
        self.num_classes = num_classes
        idx_to_in_channels = [64, 128, 128, 128, 128]
        for i in range(5):
            setattr(self, f'blk_{i}', get_blk(i))
            setattr(self, f'cls_{i}', cls_predictor(idx_to_in_channels[i],
                                                    num_anchors, num_classes))
            setattr(self, f'bbox_{i}', bbox_predictor(idx_to_in_channels[i],
                                                      num_anchors))
    def forward(self, X):
        anchors, cls_preds, bbox_preds = [None] * 5, [None] * 5, [None] * 5
        for i in range(5):
            X, anchors[i], cls_preds[i], bbox_preds[i] = blk_forward(
                X, getattr(self, f'blk_{i}'), sizes[i], ratios[i],
                getattr(self, f'cls_{i}'), getattr(self, f'bbox_{i}'))
        anchors = torch.cat(anchors, dim=1)
        cls_preds = concat_preds(cls_preds)
        cls_preds = cls_preds.reshape(cls_preds.shape[0], -1, self.num_classes + 1)
        bbox_preds = concat_preds(bbox_preds)
        return anchors, cls_preds, bbox_preds
```

On a batch of 32 images of $256\times256$: anchors `[1, 5444, 4]`, class predictions `[32, 5444, 2]`, offset predictions `[32, 21776]`. The fifth block uses global max pooling to reach $1\times1$. The original SSD used a truncated VGG as base network; ResNet is also common.

**Training.** Banana data, batch 32, SGD `lr=0.2`, `weight_decay=5e-4`, 20 epochs. Loss = cross-entropy over anchor classes + $\ell_1$ over masked offsets, each averaged per image:

```python
cls_loss = nn.CrossEntropyLoss(reduction='none')
bbox_loss = nn.L1Loss(reduction='none')

def calc_loss(cls_preds, cls_labels, bbox_preds, bbox_labels, bbox_masks):
    batch_size, num_classes = cls_preds.shape[0], cls_preds.shape[2]
    cls = cls_loss(cls_preds.reshape(-1, num_classes),
                   cls_labels.reshape(-1)).reshape(batch_size, -1).mean(dim=1)
    bbox = bbox_loss(bbox_preds * bbox_masks,
                     bbox_labels * bbox_masks).mean(dim=1)
    return cls + bbox
```

Each step: forward → `multibox_target(anchors, Y)` labels the freshly generated anchors → loss → backward. Metrics: class error over all anchors and mean absolute error of masked offsets. D2L prints **class err 3.31e-03, bbox mae 3.11e-03** (3535.8 examples/s); no validation evaluation is done.

**Prediction.** `net.eval()`, softmax over classes, `multibox_detection` (NMS), keep rows whose class is not −1, and display boxes with confidence ≥ 0.9.

**Better losses** (D2L ex. 14.7.5). **Smooth $\ell_1$** with parameter $\sigma$:
$$f(x)=\begin{cases}(\sigma x)^2/2 & |x|<1/\sigma^2\\ |x|-0.5/\sigma^2 & \text{otherwise}\end{cases}$$
Both pieces equal $1/(2\sigma^2)$ at the switch, with slope 1. Large $\sigma$ approaches $\ell_1$; small $\sigma$ is smoother. **Focal loss** (Lin et al. 2017): $-\alpha(1-p_j)^\gamma\log p_j$ for the true-class probability $p_j$. Larger $\gamma$ shrinks the loss of well-classified examples so training focuses on hard ones:

| $p_j$ | $\gamma=0$ (cross-entropy) | $\gamma=1$ | $\gamma=5$ |
|---|---|---|---|
| 0.1 | 2.3026 | 2.0723 | 1.3597 |
| 0.5 | 0.6931 | 0.3466 | 0.0217 |
| 0.9 | 0.1054 | 0.0105 | 0.000001 |

D2L also suggests upscaling the input for small objects, **downsampling negative anchors** to balance classes, weighting the class and offset losses differently, and evaluating with the SSD paper's metrics.

### 10. Class imbalance

TinySSD's 5,444 anchors labelled against one object (IoU ≥ 0.5; computed here):

| object | positives | background | ratio |
|---|---|---|---|
| small, 10% of width | 1 | 5,443 | 5,443:1 |
| medium, 25% | 44 | 5,400 | 123:1 |
| large, 50% | 32 | 5,412 | 169:1 |
| D2L's dog box | 12 | 5,432 | 453:1 |
| D2L's cat box | 36 | 5,408 | 150:1 |

D2L's mask removes negatives from the offset loss, but the class loss sums over all anchors. Predicting "background" everywhere is 99.8% correct. Standard fixes: **Focal Loss** (Lin et al. 2017), which multiplies cross-entropy by $(1-p_t)^\gamma$, and downsampling negative anchors, both suggested in D2L's exercises (§9); and hard-negative mining (original SSD: at most 3 negatives per positive) and fixed sampling ratios, beyond D2L.

The IoU threshold sets how many positives there are (50%-wide box):

| threshold | positives | ratio |
|---|---|---|
| 0.3 | 203 | 26:1 |
| 0.4 | 96 | 56:1 |
| 0.5 | 32 | 169:1 |
| 0.6 | 12 | 453:1 |
| 0.7 | 4 | 1,360:1 |

(The best anchor reaches IoU 0.7693, so at 0.8 only step 2 would provide a positive.)

**What D2L's training metric hides** (mine). D2L's printed class error, 3.31e-03, is computed over all 5,444 anchors of each image. A model that answers "background" for every anchor has class error equal to the positive fraction: 12–44 positives out of 5,444 (the table above) gives 0.22%–0.81%. So 0.33% class error by itself says little about whether bananas are found; the masked offset MAE and the displayed predictions are the informative outputs. Report detection with per-object metrics (precision/recall at an IoU threshold, mAP), not per-anchor accuracy.

### 11. The R-CNN family (§14.8)

- **R-CNN** (Girshick et al. 2014): selective search proposes ~2,000 regions; each is resized and run through a CNN; SVMs classify and linear regression refines boxes.
- **Fast R-CNN** (2015): run the CNN once on the whole image and use **RoI pooling** to extract a fixed-size feature for each proposal. That is 2,000 CNN passes reduced to 1.
- **Faster R-CNN** (Ren et al. 2015): a **region proposal network** replaces selective search, making the detector trainable end to end.
- **Mask R-CNN** (He et al. 2017): adds a per-pixel mask branch and uses **RoI align** (bilinear interpolation) instead of rounding.

**RoI pooling** splits any region into an $h_2\times w_2$ grid and takes each cell's max, so different region shapes give the same output size. On $\mathsf X=0..15$ ($4\times4$) with `spatial_scale=0.1`:

| region | maps to | $2\times2$ output |
|---|---|---|
| (0,0)–(20,20) | `X[0:3, 0:3]` | $\begin{pmatrix}5&6\\9&10\end{pmatrix}$ |
| (0,10)–(30,30) | `X[1:4, 0:4]` | $\begin{pmatrix}9&11\\13&15\end{pmatrix}$ |

| model | CNN passes | proposals | end to end |
|---|---|---|---|
| R-CNN | ~2,000 | selective search | no |
| Fast R-CNN | 1 | selective search | no |
| Faster R-CNN | 1 | RPN | yes |
| Mask R-CNN | 1 | RPN | yes (+ masks) |

Each step replaces a hand-designed stage with a learned one, as in [[05 - Convolutional Neural Network|ch. 05]] (hand features → learned kernels; dense head → global pooling). DETR (2020, beyond D2L) later removed anchors and NMS too.

**Details (§14.8).**

- **R-CNN**, four steps: (1) selective search proposes about 2,000 regions at several scales, each labelled with a class and a ground-truth box; (2) a pretrained CNN truncated before its output layer extracts features from each resized proposal; (3) one SVM per class decides whether the region contains that class; (4) linear regression predicts the box. Thousands of forward passes per image make it impractical.
- **Fast R-CNN**: the CNN (now trainable) runs once on the whole image, giving a $1\times c\times h_1\times w_1$ map. The $n$ proposals mark regions on it; **RoI pooling** turns each into $c\times h_2\times w_2$, giving $n\times c\times h_2\times w_2$; a dense layer maps this to $n\times d$, then softmax regression gives $n\times q$ class scores and a regressor $n\times4$ boxes. Unlike ordinary pooling (shape set indirectly by window, padding and stride), RoI pooling sets the output shape directly: an $h\times w$ region is split into $h_2\times w_2$ sub-windows of about $(h/h_2)\times(w/w_2)$, rounded up, and each outputs its maximum. In D2L's $4\times4$ example with a $3\times3$ region the sub-windows hold $\{0,1,4,5\}$, $\{2,6\}$, $\{8,9\}$ and $\{10\}$, giving 5, 6, 9, 10. Code: `torchvision.ops.roi_pool(X, rois, output_size=(2, 2), spatial_scale=0.1)` with `rois = [[0, 0, 0, 20, 20], [0, 0, 10, 30, 30]]` (first entry is the image index in the batch; D2L calls it the class) on a 40×40 image whose feature map is 1/10 the size.
- **Faster R-CNN** keeps Fast R-CNN and replaces selective search with a **region proposal network**: (1) a $3\times3$ conv (padding 1) gives each feature-map position a length-$c$ vector; (2) anchors of several scales and ratios are generated at each position and labelled; (3) from that vector, predict object-vs-background and a box for each anchor; (4) NMS on the predicted object boxes gives the proposals for RoI pooling. The RPN is trained jointly with the detector: the loss includes the detector's class and box terms and the RPN's binary class and box terms, so it learns to propose fewer, better regions.
- **Mask R-CNN** builds on Faster R-CNN when pixel-level labels exist: **RoI alignment** (bilinear interpolation, no rounding) replaces RoI pooling to keep spatial precision, and an extra fully convolutional network predicts each object's pixel mask (FCNs are §14.11, beyond this note).

### 12. One-stage vs two-stage

| | one-stage (SSD, YOLO) | two-stage (R-CNN family) |
|---|---|---|
| structure | classify and regress all anchors at once | propose, then classify and regress |
| speed | faster | slower |
| small objects | weaker | stronger |
| class imbalance | severe: every anchor is an example | reduced: proposals filter out most background |

The imbalance in §10 is why Focal Loss was designed for one-stage detectors.

## ✏️ Exercises

> [!example]- **1.** *(Easy) IoU*
> **(a)** IoU of $[0,0,4,4]$ with $[2,2,6,6]$, and with $[1,1,3,3]$. **(b)** Build two boxes with IoU 0.5 in two different ways. **(c)** What does (b) show?
>
> ---
> **(a)** Intersection 4, union 28: 0.142857. Nested: 4/16 = 0.25.
>
> **(b)** Shift two unit squares by $d=1/3$; or nest a box of half the area (side $\sqrt2$ inside side 2). Both give 0.500000.
>
> **(c)** IoU cannot separate position errors from size errors, and all disjoint pairs score 0 (no gradient).

> [!example]- **2.** *(Easy–medium) Anchor budget*
> **(a)** $600\times800$ image, 4 scales, 3 ratios: anchors with all pairs vs $n+m-1$? **(b)** Label memory? **(c)** A 5-level pyramid on $256\times256$ with $a$ anchors per cell vs per-pixel.
>
> ---
> **(a)** All pairs 5,760,000; subset (6 per pixel) 2,880,000.
>
> **(b)** $2{,}880{,}000\times5$ floats = 54.9 MB per image (1.76 GB for a batch of 32).
>
> **(c)** $1361a$ vs $65{,}536a$: 48× fewer for any $a$ ($a=4$: 5,444 vs 262,144).

> [!example]- **3.** *(Medium) Run the assignment*
> Use the IoU matrix in §5. Give the classes and explain each anchor.
>
> ---
> Step 2: $A_4$ → cat (0.7459), then $A_1$ → dog (0.1417); both boxes assigned. Step 3: $A_0$ (0.0536) background, $A_2$ (0.5657) cat, $A_3$ (0.2059) background. Classes `[0, 1, 2, 0, 2]`, mask `[0,0,0,0, 1,1,1,1, 1,1,1,1, 0,0,0,0, 1,1,1,1]`. $A_1$ is positive only because step 2 runs first.

> [!example]- **4.** *(Medium–hard) NMS*
> **(a)** Run NMS on §6's boxes at $\epsilon=0.5$. **(b)** At $\epsilon=0.8$? **(c)** Construct a case where NMS deletes a correct detection.
>
> ---
> **(a)** Keep $B_0$, suppress $B_1$ (0.7368), $B_2$ (0.5454); keep $B_3$.
>
> **(b)** Nothing exceeds 0.8 against $B_0$, so $B_1$ and $B_2$ survive: three boxes on one dog.
>
> **(c)** Two real objects $[0,0,1,1]$ and $[0.3,0,1.3,1]$ have IoU $0.7/1.3=0.5385>0.5$, so the weaker one is deleted. NMS cannot tell two objects from two boxes on one object.

> [!example]- **5.** *(Hard) Imbalance and conv heads*
> **(a)** TinySSD, one object 25% wide: positives at IoU ≥ 0.5 and the ratio? **(b)** What does D2L's loss do about it? **(c)** Dense vs conv class head on a 64-channel $32\times32$ map, $a=4$, $q=1$.
>
> ---
> **(a)** 44 positives, 5,400 background (123:1). A small object gives 5,443:1.
>
> **(b)** Nothing for the class loss: the mask only affects offsets. Fixes: hard-negative mining, sampling ratios, Focal Loss.
>
> **(c)** 8,192 scores. Dense from 65,536 inputs: 536,879,104 parameters. $3\times3$ conv with 8 channels: 4,616 (116,308× fewer).

## 📝 Summary

- Augmentation and fine-tuning both assume an invariance; check it holds. Augment only training data (flips, `RandomResizedCrop`, `ColorJitter`, `Compose`). Fine-tune with a small rate on pretrained layers and 10× on the new head, and standardize inputs with ImageNet's channel statistics. Hot dogs: fine-tuned 0.926 vs from scratch 0.871 test accuracy.
- IoU 0.5 means two-thirds shared width for equal boxes; IoU mixes position and size errors and is 0 for all disjoint boxes.
- Per-pixel anchors explode (2,042,040 for one image); feature-map anchors cut this ~48× and assign object sizes to levels.
- Anchor labelling first guarantees each object an anchor, then thresholds the rest. Offsets are standardized (×10 centre, ×5 log size).
- NMS removes duplicates greedily and can delete real neighbouring objects.
- SSD predicts classes and offsets with conv heads on several feature maps (TinySSD: 5,444 anchors, outputs `[32, 5444, 2]` and `[32, 21776]`); its class loss suffers 123:1 to 5,443:1 background imbalance, which Focal Loss or negative downsampling fix. Per-anchor class error near 0.3% is close to the all-background baseline.
- Detection labels are padded to (batch, $m$, 5) with class −1 for missing boxes.
- The IoU threshold controls how many positives there are (0.6 → 0.3: 16.9× more).
- R-CNN → Fast R-CNN (one CNN pass + RoI pooling) → Faster R-CNN (learned proposals) → Mask R-CNN (RoI align, masks).
- One-stage detectors are faster; two-stage detectors filter background first and handle small objects better.

## ⚠️ Important Notes

1. Anchor labels can cost more memory than you expect (38.9 MB per image at 2M anchors).
2. IoU thresholds are stricter than they sound: 0.5 → 0.7 cut positives 8× in the measured case.
3. Check the positive:negative ratio before trusting a detection loss; an unweighted loss can train a detector that finds nothing.
4. D2L's `multibox_detection` runs NMS over all boxes regardless of class (class-agnostic). Many libraries run it per class, so a dog box cannot suppress an overlapping cat box; know which one you use.
5. Labelling and NMS both use IoU thresholds but for different purposes; they need not be equal.
6. Apply the offset standardization when labelling and invert it when decoding, or boxes come out the wrong size.
7. Objects smaller than a level's stride are invisible to that level; missing small objects often means you need a higher-resolution map.
8. RoI pooling rounds coordinates; masks need RoI align.
9. Freeze the backbone or use parameter groups when fine-tuning.
10. D2L trains with `RandomResizedCrop(224)` and tests with `Resize(256)` + `CenterCrop(224)`. The difference is deliberate; copy both correctly.
11. A detector containing a CNN is not necessarily end-to-end trainable (R-CNN, Fast R-CNN).
12. D2L's banana dataset has one object per image, so it cannot reveal NMS problems with crowded scenes.
13. Pretrained models expect their own input normalization (ImageNet mean/std per channel).
14. Anchor classes are shifted by +1 so that 0 means background; decoded predictions use −1 for background or suppressed.
15. `multibox_prior` scales widths by `in_height / in_width` so ratio-1 anchors are square in pixels.
16. Per-anchor accuracy is a poor detection metric under heavy imbalance; use per-object precision/recall or mAP.

> [!warning] Gaps in the source material
> - **Figures:** IoU, assignment, SSD, R-CNN and RoI pooling diagrams are reconstructed from the prose. Lost: the cat/dog photo with anchors, augmentation grids, hot-dog samples, multiscale anchor plots, and all training curves (so no accuracies are quoted).
> - **Added by me:** the all-background baseline for D2L's class error (§10); the `4.17e-06` explanation (eps and float32); the anchor-corner check at pixel (250, 250); the focal-loss table; the IoU formula $(1-d)/(1+d)$ and the nested case (D2L ex. 14.4.2); the IoU matrix in §5; the imbalance and threshold tables (§10); the 48× pyramid saving; the head parameter comparison; the R-CNN 2,000× figure and comparison tables; the NMS failure case; label-memory arithmetic. Hard-negative mining, Soft-NMS, GIoU, mAP and DETR are named beyond D2L (Focal Loss and smooth $\ell_1$ are in D2L's exercises).
> - **No discrepancies** in this range.
> - **Skipped:** plotting helpers (`show_bboxes`, `bbox_to_rect`); segmentation, transposed convolution, FCN, style transfer and the Kaggle sections (§14.9–14.14), which are outside the syllabus topic.

**Previous:** [[05 - Convolutional Neural Network]] · **Next:** [[07 - Recurrent Neural Network]]
