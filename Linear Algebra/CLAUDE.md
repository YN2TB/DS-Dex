# Linear Algebra — subject context

**Status: ✅ complete** (2026-07-29). `contents/00-Index.md` plus chapters 01–08.

## Source

**Nicholson, *Linear Algebra with Applications* 7e** — the only file in `documents/`. **No lecture slides.**

## Scope — my editorial decision, needs syllabus confirmation

**Chapters 1–8.** Nicholson's ch. 1–5 are his self-contained matrix course; 6–7 are the abstract theory; **ch. 8 is non-negotiable for Data Science because it holds the spectral theorem and PCA.**

**Excluded: ch. 9–11** (change of basis, inner product spaces, Jordan form), with reasons recorded in the index.

## Chapters

01 Systems of Linear Equations · 02 Matrix Algebra · 03 Determinants and Diagonalization · 04 Vector Geometry · 05 The Vector Space Rⁿ · 06 Vector Spaces · 07 Linear Transformations · 08 Orthogonality

## ⚠️ The textbook has no singular value decomposition anywhere

Not in the table of contents, not in the index, not in the text. **This is the biggest gap for a DS reader.** §8.10 derives PCA by eigendecomposing the covariance matrix — correct, but the numerically inferior route.

**Flagged at every point where the SVD would appear**: ch. 05 (rank), ch. 05 (least squares), ch. 08 §2 and §5 — each with a pointer to Strang ch. 7.

## ⚠️ PDF extraction destroys every matrix

Brackets, row structure, **and the position of minus signs** are all lost — e.g. `34 1 1 / 23 0 0 / 43 1 2−−`. **Every matrix in these notes was reconstructed by hand and then verified by recomputing the example's printed answer.**

| Reads as | Means |
|---|---|
| `S`…`T` | large brackets (a matrix) |
| `U`…`V` | set braces |
| `Q`…`R` | large parentheses |
| `e` / `u` / `U` at the start of a display | large brace grouping a system |
| `/bbR` | ℝ |
| `/uni25ba.001` | marks the start of a solution |

**Two image-only objects had to be handled:**
- §5.6 Example 3's data table was **recovered** as (1,1), (3,2), (4,3), (6,4), (7,5) — it reproduces all four printed sums, det 114, and the answer (9/38, 25/38).
- §3.1 Example 10's 4×4 matrix was **not** recoverable. The printed intermediate arithmetic is verified instead and the failure is stated in the note.

## Errata — full table in `contents/00-Index.md`

**The worst: Definition 2.5 — the definition of the matrix–vector product, the book's central definition — is printed with every coefficient as $x_1$.**

**No *computational* error was found in ch. 1–8.** All 10+ defects are typographical. (Contrast `Probability Theory` — 5 real errors — and `Calculus` — none at all.)

## A structural warning about the book

**Nicholson defers two load-bearing proofs out of ch. 5** — the Fundamental Theorem and basis extension — into §§6.3–6.4. A reader who stops at ch. 5 *as he himself suggests* never sees them. Noted in both chapters.

Cross-subject: ch. 05 and 08 are prerequisites for `Optimization/contents/08 - Least Squares and Linear Equations.md`, `Econometrics/contents/03`, and `Data Preparation and Visualization` (PCA).
