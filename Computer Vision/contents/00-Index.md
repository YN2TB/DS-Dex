---
subject: Computer Vision
chapter: 00
tags: [ds, moc, computer-vision]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision lecture slides; Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed."
---

# Computer Vision — Map of Content

Course notes for **Computer Vision**, Data Science major, NEU. Lecturer: **Nguyen Manh Toan (Swinburne Vietnam)**.

## 🎯 Scope

Set by the lecturer's course outline (Lecture 01, slide 8): *"modern, deep-learning-focused computer vision"* in 14 teaching weeks, with week 15 for project presentations. One note per week. **The lecture slides decide what each note covers**; Szeliski, Stanford CS231n and the original papers fill in detail.

| # | Note | Covers | Built from |
|---|---|---|---|
| 01 | [[01 - Introduction and Image Formation]] | Course logistics; history of vision; the semantic gap and eight challenges; pinhole and lens cameras; sensors, sampling, quantisation; colour spaces; images as tensors; PyTorch/torchvision/OpenCV conventions | ✅ Lecture 01 |
| 02 | [[02 - Classical Image Processing]] | Point operations and histograms; convolution and padding; noise and smoothing (Gaussian, median, bilateral); gradients, Sobel, LoG/DoG, Canny; morphology; Harris, scale space, SIFT, HOG; hand-designed → learned | ✅ Lecture 02 |
| 03 | [[03 - Image Classification and Linear Models]] | Datasets, splits, cross-validation, metrics; k-NN and the curse of dimensionality; linear classifiers; hinge, sigmoid/BCE, softmax/CE, multi-label; regularisation; gradient derivations; SGD and mini-batches; the training loop and sanity checks | ✅ Lecture 03 |
| 04 | [[04 - From Neural Networks to CNNs]] | Hidden layers and nonlinearity; universal approximation; activation functions and vanishing gradients; backpropagation (gates, matrix form, two-layer net); the conv layer, output size, receptive fields, pooling, 1×1 conv; a first CNN | ✅ Lecture 04 |
| 05 | [[05 - CNN Architectures]] | Initialisation (Xavier, He); BatchNorm and its family; momentum, RMSProp, Adam, schedules; augmentation and regularisation; LeNet → AlexNet → VGG → GoogLeNet → ResNet → DenseNet/ResNeXt/SENet/MobileNet; transfer learning | ✅ Lecture 05 |
| 06 | [[06 - Vision Transformers]] | Scaled dot-product, self- and multi-head attention; ViT (patches, [class] token, position embeddings, blocks, variants); inductive bias vs data; DeiT and knowledge distillation; Swin; what to use | ✅ Lecture 06 |
| 07 | [[07 - Object Detection I]] | Detection as set prediction; sliding window, Viola–Jones, HOG+SVM, DPM; IoU, AP/mAP, VOC vs COCO, NMS; R-CNN, Fast R-CNN, Faster R-CNN (anchors, RPN); FPN | ✅ Lecture 07 |
| 08 | [[08 - Object Detection II]] | One-stage detectors (YOLO, SSD); focal loss and RetinaNet; anchor-free (FCOS, CenterNet); DETR and Hungarian matching; current detectors and licences | ✅ Lecture 08 |
| 09 | [[09 - Segmentation]] | Semantic, instance and panoptic; FCN, U-Net, transposed convolution, Mask R-CNN, SAM | ⏳ written before the lecture |
| 10 | [[10 - Pose Estimation and Faces]] | Keypoints, heatmaps, top-down vs bottom-up, face detection, recognition and embeddings | ⏳ written before the lecture |
| 11 | [[11 - Video and Motion]] | Optical flow, temporal models, 3D convolutions, two-stream networks, tracking | ⏳ written before the lecture |
| 12 | [[12 - Self-Supervised Learning]] | Pretext tasks, contrastive learning, SimCLR/MoCo, BYOL, masked image modelling, CLIP | ⏳ written before the lecture |
| 13 | [[13 - Generative Models]] | Autoencoders, VAEs, GANs, diffusion models, text-to-image | ⏳ written before the lecture |
| 14 | [[14 - 3D Vision and Emerging Topics]] | Stereo and depth, structure from motion, point clouds, NeRF, Gaussian splatting | ⏳ written before the lecture |

Notes 01–08 were rewritten from the lecture slides on 2026-10-07. Notes 09–14 were written in August 2026 from Szeliski, CS231n and the papers, before those lectures had slides; each should be checked against its slides when they arrive.

## 📊 Assessment (Lecture 01, slide 10)

| Component | Weight | Notes |
|---|---|---|
| **Mid-term exam** | **40%** | Week 9, covers weeks 1–8. *"Inference-style questions: given a model, an architecture, or an output, reason about what happens and why — not memorization."* |
| **Final project** | **50%** | Teams of ~6; topics released week 3; proposal, milestone, presentation in week 15, code |
| Participation | 10% | Attendance and in-class exercises |

The exercises in notes 01–08 are written in the mid-term's style: a setup, then "what happens and why". The 17 project topics are in `note/project_topics.md`.

## 🔗 The overlap with Deep Learning

[[Deep Learning/contents/00-Index|Deep Learning]] is also in this vault and covers some of the same ground from the D2L textbook:

| This course | Deep Learning note |
|---|---|
| 03 Linear models, softmax | [[Deep Learning/contents/03 - Logistic Regression\|DL ch. 03]] |
| 04 Neural networks, backprop | [[Deep Learning/contents/04 - Neural Network\|DL ch. 04]] |
| 04–05 Convolution, CNN architectures | [[Deep Learning/contents/05 - Convolutional Neural Network\|DL ch. 05]] |
| 06 Attention, Transformer (not ViT) | [[Deep Learning/contents/08 - Sequence to Sequence\|DL ch. 08]] |
| 07 Anchors, IoU, NMS, SSD, R-CNN family | [[Deep Learning/contents/06 - Object Detection\|DL ch. 06]] |

**Rule:** each CV note covers everything its lecture teaches, so it can be revised on its own for the exam. The Deep Learning notes are linked for longer derivations and code-level detail, not relied on to fill gaps in the lecture's content.

## 📋 Errata and discrepancies in the slides

| # | Where | Slide says | Finding | Status |
|---|---|---|---|---|
| 1 | Lecture 04, slide 24 | last bias gradient written $\partial L/\partial b_2$ | must be $\partial L/\partial b_1$ (it sums $\partial L/\partial Z_1$) | typo, corrected in [[04 - From Neural Networks to CNNs\|ch. 04]] |
| 2 | Lecture 07, slide 30 | "47 s → 0.32 s per image, ≈213× faster" | $47/0.32 \approx 147$; the paper's 213× is for 0.22 s with truncated SVD | inconsistent pairing, explained in [[07 - Object Detection I\|ch. 07]] |
| 3 | Lecture 05, slide 29 | VGG-16's 15.5 GFLOPs is "roughly 4× GoogLeNet" | GoogLeNet's paper gives ~1.5 G multiply-adds, i.e. ~10× | possible; FLOP conventions vary. Worth asking the lecturer |
| 4 | Lecture 05, slide 35 | "The next slide is how it works" (MobileNet) | the next slide is the comparison table; the explanation is missing | added from the MobileNet paper in [[05 - CNN Architectures\|ch. 05]] |
| 5 | Lecture 04 vs 05 | AlexNet top-5 16.4% (L04) and 15.3% (L05) | both are published figures, for different configurations (5-model ensemble vs 7 models with extra pretraining) | not an error |

**Correction to the previous notes:** the August 2026 version of ch. 08 gave an 11-point AP of 0.7045 for its worked example. That was a floating-point comparison error; the correct value is **0.712** (now in [[07 - Object Detection I|ch. 07]]).

## 📐 Conventions in these notes

- Every number from the slides is recomputed before it's quoted, and every exercise answer is checked numerically.
- Formulas are rebuilt from the slides, never copied from extracted text: the slide PDFs delete spaces and flatten fractions (`x=f X Z` is $x = fX/Z$).
- Slide figures don't extract; captions are used where they describe the figure, and lost figures are listed in each note's gaps callout.
- Additions beyond the slides are labelled in each note's gaps callout.

## 🔗 Related subjects in this vault

- **[[Deep Learning/contents/00-Index|Deep Learning]]** — see the overlap table above
- [[Machine Learning/contents/00-Index|Machine Learning]] — reinforcement learning
- [[Linear Algebra/contents/00-Index|Linear Algebra]] — projection, eigendecomposition, SVD
- [[Probability Theory/contents/00-Index|Probability Theory]] and [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]]
- [[MLOps/contents/00-Index|MLOps]] — deployment, monitoring, drift
