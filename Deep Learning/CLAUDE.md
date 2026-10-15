# Deep Learning

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata (none; 9 discrepancies declined): `contents/00-Index.md`.

## Source

- *Dive into Deep Learning* (Zhang, Lipton, Li, Smola), Cambridge UP, PyTorch edition: `documents/Dive into Deep Learning.pdf`, 1185 pages. PDF page = book page + 40.
- The eight topics come from the user's syllabus in `note/Index.md` (read it, never edit `note/`). D2L sections used per note:

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

My two scope calls: optimizers go in 04; attention/Transformer go in 08.

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

## Boundaries

`Computer Vision/` links here for extra depth only; its own notes cover every lecture topic (see `Computer Vision/CLAUDE.md`).
