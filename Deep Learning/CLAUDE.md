# Deep Learning

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata (E1–E2, found by running D2L's code; 14 discrepancies declined; slide errors S1–S15): `contents/00-Index.md`.

## Source

- *Dive into Deep Learning* (Zhang, Lipton, Li, Smola), Cambridge UP, PyTorch edition: `documents/Dive into Deep Learning.pdf`, 1185 pages. PDF page = book page + 40.
- `slides/`: the lecturer's full set, 16 decks (found 2026-11-17). The notes were first reworked from the book (2026-11-16), then each got a "From the lecture slides" block with what the slides add. The deck → note map and slide errors S1–S15 are in the index. Deck 10 (GAN) is not examined, so it is not written unless the user asks (memory `dl-slides-gan`).
- Slide text extracts with pypdf, but most formulas, figures and all code are images. Render pages with PyMuPDF (`fitz`, installed) and read the images. The slide code is MXNet (D2L's other edition) or Keras; TensorFlow is not installed, so Keras code is quoted, not run.
- The eight topics come from the user's syllabus in `note/Index.md` (read it; `note/` may be edited only for the user's code, see memory). D2L sections used per note:

| Note | Topic | D2L sections |
|---|---|---|
| 01 | Introduction to Deep Learning | ch. 1; 2.4–2.5 |
| 02 | Linear Regression | 3.1–3.7 |
| 03 | Logistic Regression | 4.1–4.7 |
| 04 | Neural Network | ch. 5, 6, 12 (optimizers) |
| 05 | Convolutional Neural Network | ch. 7, 8 |
| 06 | Object Detection | 14.1–14.8 |
| 07 | Recurrent Neural Network | ch. 9; 10.1–10.4 |
| 08 | Sequence to Sequence | 10.5–10.8; 11.1–11.7 (attention, Transformer) |

My two scope calls: optimizers go in 04; attention/Transformer go in 08. The slides add YOLO (06), Luong attention and BERT/GPT (08, from D2L §11.9, §15.8–15.10), none of which are D2L sections of the original plan.

## Extraction quirks

Prose and code tokens extract well; display maths is damaged silently.

| PDF text | Means |
|---|---|
| (deleted) | `←`, `−`, `η`, `λ`, `×`, fraction bars, `⊙` |
| `;` | `,` (e.g. `xi; j` = $x_{i,j}$) |
| `j` | `\|` (e.g. `jBj` = $\|\mathcal B\|$) |
| `:` | decimal point (`0:2` = 0.2) |
| `1` | `∞` **and** literal 1, sometimes in adjacent lines |
| `!` | `→` |
| `2` | `∈` |
| `@` | `∂` |
| `p` | `√` |
| `39c2` | $3\times9c^2$ (multiplication sign lost) |

Bold/blackboard typography is lost (scalar, vector, matrix look identical). Code loses indentation. Figures never extract; printed code outputs do, and they make many claims checkable.

D2L's code is not always right (E1, E2): rerun it in PyTorch (installed globally, 2.11) before trusting a printed result. D2L datasets download from `d2l-data.s3-accelerate.amazonaws.com` and can be checked against the SHA-1 in the code (done for `fra-eng.zip`).

## Boundaries

`Computer Vision/` links here for extra depth only; its own notes cover every lecture topic (see `Computer Vision/CLAUDE.md`).
