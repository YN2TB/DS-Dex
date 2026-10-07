# CLAUDE.md — Computer Vision

Subject-specific context. Read this plus the root `CLAUDE.md`. Everything about the chapters themselves is in the chapter notes, so it is not repeated here.

*Rewritten 2026-10-07. The previous version (60 KB, mostly a copy of the chapter findings) is in git history at commit `5af6a3c`.*

## Status

The course is **still running**. Lecture slides arrive weekly, and as of 2026-10-07 slides exist for **lectures 1–8**. The mid-term (week 9, 40%) covers weeks 1–8.

**Notes 01–08 were rewritten from their slides on 2026-10-07.** Every lecture topic is covered in the CV note itself; Deep Learning is linked for extra depth only (see "The Deep Learning boundary rule" below). Formatting is deliberately plain: section headings, bold only for key terms, callouts sparingly. Exercises are written in the mid-term's "given X, what happens and why" style.

| # | Note | Slides | State of the note |
|---|---|---|---|
| 01 | Introduction and Image Formation | `Lecture01_Introduction.pdf` (68 p.) | ✅ rewritten 2026-10-07 |
| 02 | Classical Image Processing | `Lecture02_Image_Processing.pdf` (67 p.) | ✅ rewritten 2026-10-07 |
| 03 | Image Classification and Linear Models | `Lecture03_…` (61 p.) | ✅ rewritten 2026-10-07 |
| 04 | From Neural Networks to CNNs | `Lecture04_From_NNs_to_CNNs.pdf` (43 p.) | ✅ rewritten 2026-10-07 |
| 05 | CNN Architectures (titled "Training Deep Networks and CNN Architectures"; filename kept so links don't break) | `Lecture05_CNN_Architectures.pdf` (48 p.) | ✅ rewritten 2026-10-07 |
| 06 | Vision Transformers | `Lecture06_Vision_Transformers.pdf` (48 p.) | ✅ rewritten 2026-10-07 |
| 07 | Object Detection I | `Lecture07_Object_Detection1.pdf` (53 p.) | ✅ rewritten 2026-10-07 (now holds mAP and FPN, as the lecture does) |
| 08 | Object Detection II | `Lecture08_Object_Detection2.pdf` (52 p.) | ✅ rewritten 2026-10-07 |
| 09–14 | Segmentation … 3D Vision | none yet | ⏳ old-style notes written ahead of the lectures; check each one when its slides arrive |

Week 15 is project presentations, so it gets no note.

**Next:** when `Lecture09_*.pdf` appears in `slides/`, rewrite note 09 from it the same way, and so on. Slide discrepancies found so far are in `contents/00-Index.md` (errata table). The gap table below records what the *old* notes 03–08 were missing; it's kept as a record of why they were rewritten.

## Sources

| | |
|---|---|
| **Slides (the spine)** | `slides/Lecture01…08_*.pdf`. Lecturer: **Nguyen Manh Toan (Swinburne Vietnam)** |
| **Textbook (reference)** | `documents/Szeliski_CVAABook_2ndEd.pdf`, 1,232 PDF pages, text layer extracts fine. PDF page 301 = book page 275 (offset +26) |
| **Other stated reference** | Stanford CS231n notes (named on each lecture's "Reading & Reference" slide) |
| `note/project_topics.md` | Lecturer's 17 final-project topics: 50% of the grade, ~6 per team, released week 3, presented week 15. All scoped to fine-tuning on one consumer GPU |
| `note/1 - Image Formation.md` | A three-line stub by the user. Leave it alone |

Every lecture from 3 on ends with a **"Hands-On"** slide naming a notebook (`lectureNN_handson.ipynb`) that is *not* in the folder. Lectures 6–8 also have a **"For Final Project"** slide (which model to reach for in which situation). Both are worth a short mention in the matching note.

## Scope

Set by Lecture 01, slide 8 (course outline): 14 teaching weeks in four parts.

- **Foundations:** 1 Intro & image formation · 2 Classical image processing · 3 Image classification & linear models · 4 From NNs to CNNs
- **Core architectures:** 5 CNN architectures · 6 Vision transformers · 7 Object detection I · 8 Object detection II
- **Dense prediction:** 9 Segmentation · 10 Pose estimation & faces · 11 Video & motion
- **Modern topics:** 12 Self-supervised learning · 13 Generative models · 14 3D vision & emerging topics

One note per week. **The lecture slides decide what a note covers.** Szeliski and papers only fill in detail.

## Why notes 03–08 were rewritten (gaps in the old versions)

Found on 2026-10-07 by listing every slide title and searching the old notes for each topic. All of these are now covered.

| Lecture | Topics in the slides but missing or thin in the note |
|---|---|
| 03 | bias trick; template-matching and geometric interpretations of $W$; preprocessing; sigmoid + binary CE; **multi-label with independent sigmoids** (slides 34–36); softmax numerical stability; **softmax and hinge gradient derivations**; learning rate; SGD vs mini-batch vs full batch; the training loop; sanity checks |
| 04 | adding a hidden layer; why depth without a nonlinearity collapses; universal approximation; neuron analogy and its limits; **activation functions** (sigmoid/tanh/ReLU family, saturation); **backpropagation** (computational graphs, gate patterns, gradients adding at forks, matrix form, two-layer net end to end); Hubel & Wiesel; conv as a constrained FC layer; receptive fields; **pooling**; backward pass through a conv; **1×1 convolution**; deep vs wide; what filters learn; a first CNN's parameter table |
| 05 | **initialisation** (variance argument, He init); **BatchNorm** (train vs test behaviour, the normalisation family); **optimisers** (momentum, RMSProp, Adam, LR schedules); **data augmentation** and regularisation; the LeNet → AlexNet → VGG → GoogLeNet → ResNet timeline with each one's distinctive features; the degradation problem; **transfer learning** (feature extraction vs fine-tuning, domain shift, the data-size × domain-similarity decision table, a torchvision recipe). The current note's MobileNet/EfficientNet content is *not* in the lecture |
| 06 | attention from scratch (soft dictionary lookup, scaled dot-product, why $\sqrt{d_k}$, self-attention, multi-head, permutation equivariance); [class] token; position embeddings; ViT model variants; the lecturer's own ViT-vs-CNN experiment (slide 25); **DeiT** (training recipe, knowledge distillation, dark knowledge, distillation token); Swin's relative position bias and patch merging; the "what should you use" scoreboard |
| 07 | box encodings; **Viola–Jones, HOG + linear SVM, Deformable Part Models**; IoU thresholds; **AP computation and VOC vs COCO protocols**; NMS and where it fails; selective search; **R-CNN → Fast R-CNN → Faster R-CNN** (RoI pooling, multi-task loss, anchors, RPN, label assignment, the measured comparison table); **FPN and the four ways to handle scale** (the note currently puts FPN in ch. 08) |
| 08 | where the two-stage budget goes; why the naive one-stage detector fails; YOLO architecture and loss in detail; **SSD**; **RetinaNet**; focal loss's α = 0.25 detail; **anchor-free detectors (FCOS, CenterNet)**; DETR's measured costs (small-object AP collapse, slow convergence); the current frontier; the "nine years, one component at a time" summary |

mAP and its conventions are in the note for ch. 08 but in Lecture **07**. Move them when 07/08 are reworked.

## The Deep Learning boundary rule

The 2026-08 notes followed *"cross-reference Deep Learning, do not duplicate it"*, so old notes 04, 05 and 07 mostly linked to DL ch. 04–06. That was the main reason they didn't match the lectures.

**Current rule (applied in the 2026-10-07 rewrite):** each CV note covers everything its lecture teaches, with the lecturer's formulas and examples, so it can be revised on its own for the exam. Deep Learning notes are linked for longer derivations and code-level detail only. The user didn't explicitly choose this; if they ask for shorter notes, the alternative is to keep definitions and formulas and move derivations out to the DL links.

## Extraction quirks

**Slides (Beamer):**
- Prose and bullets extract cleanly and in order.
- Spaces next to italic or math runs are often deleted: `Whyk-NN` = "Why k-NN", `intokfolds` = "into k folds". Read carefully, don't transcribe.
- Fractions flatten and superscripts drop: `x=f X Z` is $x = fX/Z$, `R H×W×3` is $\mathbb R^{H\times W\times 3}$. Rebuild formulas and check them numerically (root rule).
- Every slide ends with a footer `Nguyen Manh Toan (Swinburne Vietnam) Computer Vision Week N k / M`. Filter it out.
- Figures are images and never extract. Captions and table cells do, and tables (e.g. the R-CNN family comparison, model-variant tables) come through as text. Check their numbers before quoting.

**Szeliski:** has a text layer and extracts normally. Figures are lost as usual.

## Errata

Four slide discrepancies (one certain typo, one inconsistent pairing, one possible error, one missing slide) are tabled in `contents/00-Index.md`. Also there: the old notes' 11-point AP of 0.7045 was a floating-point comparison bug (`0.6000000000000001 > 0.6`); correct value 0.712. **Use a tolerance when comparing recall levels.**

## Open items

- When slides 09–14 arrive, rewrite each note from its slides the same way.
- Gaps already flagged in the notes: **RANSAC** (ch. 14) and **camera calibration** (ch. 01 assumes it, ch. 14 doesn't derive it). Add them if a later lecture covers them.
