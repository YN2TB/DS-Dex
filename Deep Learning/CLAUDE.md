# CLAUDE.md — Deep Learning

Subject context. Read with the root `CLAUDE.md`; nothing else is needed.

## Status

✅ Complete: `00-Index.md` + ch. 01–08, matching the user's eight-topic syllabus in `note/Index.md`. No errata; 9 discrepancies declined (listed in `00-Index.md`).

Notes were rewritten on 2026-10-09 in a shorter, plainer style at the user's request (the earlier versions were too wordy). Content and verified numbers were kept; one arithmetic slip was fixed (ch. 08 ex. 1(b): BLEU 0.6815, not 0.6816). Earlier versions are in git history.

**Style the user wants for this subject:** short sentences, little bold, no "⚠️" on every line, no meta-commentary about the vault or the source "never dividing" its numbers. Keep the template sections, tables and verified figures.

## Source

- *Dive into Deep Learning* (Zhang, Lipton, Li, Smola), Cambridge UP, PyTorch edition: `documents/Dive into Deep Learning.pdf`, 1185 pages.
- PDF page = book page + 40.
- `note/` is the user's own folder (their notes, code, a venv). Do not edit it.

## Scope

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

My two scope calls: optimizers go in 04; attention/Transformer go in 08. Omitted chapters and reasons are in `00-Index.md`.

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

Rule: never transcribe a formula; rebuild it from the prose and check it against D2L's printed numbers.

## Main findings (details in the chapters)

- ch. 01: Table 1.5.1 shows memory per example fell 100× while compute per example stayed flat; one dense layer on raw audio first fits in RAM around 2010.
- ch. 02: in D2L's weight-decay experiment the overfit model's norm is within 1.1% of the truth while the vector points ~85° away. `l2_penalty` prints ½‖w‖², not the norm.
- ch. 03: label-shift correction is only as good as the confusion matrix's conditioning (κ=104 amplifies noise 66×).
- ch. 04: sigmoid MLPs lose gradients after ~11 layers in float32; all printed optimizer traces reproduce from start point (−5, −2); effective momentum step is η/(1−β); Adam's step is ~η and scale invariant; uncorrected Adam overshoots up to 6.57×.
- ch. 05: CNNs keep <8% of parameters but >85% of FLOPs in convolutions; NiN removes the dense head (64.7× smaller than VGG-11).
- ch. 06: every printed tensor reproduces; SSD's class imbalance is 123:1 to 5,443:1 and D2L's loss does not address it.
- ch. 07: at T=1000 the recurrent Jacobian must be within ±0.693% of 1; LSTM memory needs forget pre-activation ≈7.3 for a 1,000-step half-life.
- ch. 08: self-attention is cheaper than an RNN when n<d; path length 1 removes the Jacobian product; Transformer layers are 2/3 FFN parameters.
- Thread across ch. 04, 05, 07, 08: sigmoid MLP, ResNet, LSTM and self-attention are all ways of handling a long product of Jacobians.
