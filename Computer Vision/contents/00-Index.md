---
subject: Computer Vision
chapter: 00
tags: [ds, moc, computer-vision]
source: "Nguyen Manh Toan (Swinburne Vietnam), Computer Vision lecture slides; Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed."
---

# Computer Vision — Map of Content

Course notes for **Computer Vision**, Data Science major, NEU. Lecturer: **Nguyen Manh Toan (Swinburne Vietnam)**.

## 🎯 Scope — set by the lecturer's own course outline

> [!note] This subject's scope is **not** an editorial guess
> **Slide 7 of Lecture 01:** *"Modern, **deep-learning-focused** computer vision: from image formation and linear classifiers to CNNs, transformers, detection, segmentation, generative models, and 3D vision."*
>
> **Slide 8 lists fourteen teaching topics; week 15 is project presentations.** The fourteen notes below are built to that list exactly.
>
> ⚠️ **This overturned a guess.** Before the slides were read, this subject's scope had been recorded as "lean to the geometry half of Szeliski." **The lecturer says the opposite.** Szeliski is one of *three* stated references — alongside **Stanford CS231n** and "selected papers per lecture" — not the spine.

| # | Note | Covers | Status |
|---|---|---|---|
| 01 | [[01 - Introduction and Image Formation]] | Why vision is hard; the semantic gap; pinhole and lens cameras; perspective projection; sensors, sampling, quantization; colour spaces; the image as a tensor | ✅ |
| 02 | [[02 - Classical Image Processing]] | Point operations, histograms, linear filtering and convolution, edges, corners, pyramids, morphology | ✅ |
| 03 | [[03 - Image Classification and Linear Models]] | Nearest neighbour, linear classifiers, loss functions, the train/val/test protocol | ✅ |
| 04 | [[04 - From Neural Networks to CNNs]] | MLPs on pixels and why they fail; convolution as a constrained layer | ✅ |
| 05 | [[05 - CNN Architectures]] | LeNet → ResNet → EfficientNet, and how to read an architecture table | ✅ |
| 06 | [[06 - Vision Transformers]] | Patch embedding, ViT, inductive bias vs. data, Swin, hybrid designs | ✅ |
| 07 | [[07 - Object Detection I]] | The detection problem, anchors, IoU, NMS, two-stage detectors | ✅ |
| 08 | [[08 - Object Detection II]] | One-stage detectors, YOLO, FPN, focal loss, DETR, evaluation by mAP | ✅ |
| 09 | [[09 - Segmentation]] | Semantic, instance and panoptic; FCN, U-Net, transposed convolution, Mask R-CNN, SAM | ✅ |
| 10 | [[10 - Pose Estimation and Faces]] | Keypoints, heatmaps, top-down vs bottom-up, face detection, recognition and embeddings | ✅ |
| 11 | [[11 - Video and Motion]] | Optical flow, temporal models, 3D convolutions, two-stream networks, tracking | ✅ |
| 12 | [[12 - Self-Supervised Learning]] | Pretext tasks, contrastive learning, SimCLR/MoCo, BYOL, masked image modelling, CLIP | ✅ |
| 13 | [[13 - Generative Models]] | Autoencoders, VAEs, GANs, diffusion models, text-to-image | ✅ |
| 14 | [[14 - 3D Vision and Emerging Topics]] | Stereo and depth, structure from motion, point clouds, NeRF, Gaussian splatting | ✅ |

*(Week 15 is project presentations — no note.)*

## ⚠️ The boundary with Deep Learning, and it is the big scope decision here

**[[Deep Learning/contents/00-Index|Deep Learning]] is already complete in this vault (8 chapters), and it owns a large part of this course's middle.**

| this course's week | already in the vault |
|---|---|
| 04 From neural networks to CNNs | **[[Deep Learning/contents/04 - Neural Network\|DL ch. 04]] + [[Deep Learning/contents/05 - Convolutional Neural Network\|DL ch. 05]]** |
| 05 CNN architectures | **[[Deep Learning/contents/05 - Convolutional Neural Network\|DL ch. 05]]** — LeNet → AlexNet → VGG → NiN → GoogLeNet → BN → ResNet → ResNeXt → DenseNet |
| 06 Vision transformers | [[Deep Learning/contents/08 - Sequence to Sequence\|DL ch. 08]] has the Transformer — **but not ViT** |
| 07 Object detection I | **[[Deep Learning/contents/06 - Object Detection\|DL ch. 06]]** — anchors, IoU, NMS, SSD, R-CNN family |
| 08 Object detection II | DL ch. 06 partially — **no YOLO, FPN, focal loss or DETR** |

> [!warning] ⚠️ THE RULE: cross-reference, do not duplicate
> **Notes 04, 05, 07 and half of 06 state the *vision-specific* framing, link to the Deep Learning note, and add only what is genuinely new.** Rewriting them would waste effort and — worse — create two copies of the same material that can drift apart.
>
> **The depth goes where Deep Learning has nothing:** image formation (01), classical processing (02), ViT (06), segmentation (09, which DL explicitly deferred), pose and faces (10), video and motion (11), self-supervised learning (12), generative models (13, DL put GANs out of scope), and 3D vision (14).
>
> *This is the same kind of boundary as the [[Commercial Banking/contents/00-Index|Commercial Banking]] / [[Monetary and Financial Theories/contents/00-Index|Monetary Theories]] split, and like that one it is recorded on both sides.*

## ⚠️ Source coverage — read this before trusting a chapter

**Only weeks 1–2 have slides.**

| | |
|---|---|
| **ch. 01** | `Lecture01_Introduction.pdf`, **68 slides** — the lecturer's own material |
| **ch. 02** | `Lecture02_Image_Processing.pdf`, **67 slides** — the lecturer's own material |
| **ch. 03–14** | ⚠️ **no slides.** Built from Szeliski (2nd ed.), the lecturer's stated second reference **Stanford CS231n**, and standard practice |

**Every chapter from 03 on says so in its gaps callout.** Where this course's emphasis is likely to differ from a generic treatment, that is flagged rather than guessed.

## 📊 Assessment (Lecture 01, slide 10)

| component | weight | |
|---|---|---|
| **Mid-term exam** | **40%** | Week 9, **"inference-style questions: given a model, an architecture, or an output, reason about what happens and why — not memorization"** |
| **Final project** | **50%** | teams of ~6, topics released week 3, presented week 15 |
| Participation | 10% | attendance and in-class exercises |

> [!warning] ⚠️ The exam format should shape how these notes are read
> **"Not memorization"** — the mid-term asks you to *reason from* an architecture or an output. ⇒ **the ⚠️ Important Notes sections matter more than the definitions**, and the exercises are written to be inference-style for the same reason.
>
> *(The 17 project topics are in `note/project_topics.md`, which is the lecturer's own file and lives outside `contents/`.)*

## 📋 Errata

**None filed.** Any discrepancy between a stated number and a recomputation is logged here **only after** ruling out extraction damage, my own arithmetic, and an alternative convention.

| # | Location | Stated | Recomputed | Verdict |
|---|---|---|---|---|
| — | — | — | — | — |

## 📐 Conventions in these notes

- Every numeric claim is recomputed (`numpy`/`sympy`) before it is written down, including every exercise answer.
- **Formulas are reconstructed from the slides, never transcribed** — beamer extraction deletes spaces and flattens fractions (`x=f X Z` is $x=f\frac{X}{Z}$).
- **All slide figures are images and never extract**; captions often state a figure's whole content and are used where they do.
- Cross-subject links are encouraged, and the Deep Learning boundary above is honoured strictly.

## 🔗 Related subjects in this vault

- **[[Deep Learning/contents/00-Index|Deep Learning]]** — the boundary partner; see the rule above
- [[Machine Learning/contents/00-Index|Machine Learning]] — reinforcement learning
- [[Linear Algebra/contents/00-Index|Linear Algebra]] — projection, eigendecomposition, SVD
- [[Probability Theory/contents/00-Index|Probability Theory]] and [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]]
- [[MLOps/contents/00-Index|MLOps]] — deployment, monitoring, drift
