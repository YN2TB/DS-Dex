# Linear Algebra

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata (full table): `contents/00-Index.md`.

## Source

**Nicholson, *Linear Algebra with Applications* 7e** — the only file in `documents/`. **No lecture slides.** No *computational* error found in ch. 1–8; all 10+ defects are typographical. The worst: Definition 2.5 (the matrix–vector product) is printed with every coefficient as $x_1$.

**The book has no singular value decomposition anywhere** (not in the contents, index or text). §8.10 derives PCA by eigendecomposing the covariance matrix: correct, but the numerically inferior route. Flagged at every point where the SVD would appear (ch. 05 rank, ch. 05 least squares, ch. 08 §2 and §5), each pointing to Strang ch. 7.

**Nicholson defers two load-bearing proofs out of ch. 5** (the Fundamental Theorem and basis extension) into §§6.3–6.4. A reader who stops at ch. 5, as he suggests, never sees them. Noted in both chapters.

## Extraction: every matrix is destroyed

Brackets, row structure, **and the position of minus signs** are all lost — e.g. `34 1 1 / 23 0 0 / 43 1 2−−`. Rebuild every matrix by hand and verify it by recomputing the example's printed answer.

| Reads as | Means |
|---|---|
| `S`…`T` | large brackets (a matrix) |
| `U`…`V` | set braces |
| `Q`…`R` | large parentheses |
| `e` / `u` / `U` at the start of a display | large brace grouping a system |
| `/bbR` | ℝ |
| `/uni25ba.001` | marks the start of a solution |

Image-only objects: §5.6 Example 3's data table was **recovered** as (1,1), (3,2), (4,3), (6,4), (7,5) (reproduces all four printed sums, det 114, and the answer 9/38, 25/38). §3.1 Example 10's 4×4 matrix was **not** recoverable; its printed arithmetic is verified instead.

## Boundaries

Ch. 05 and 08 are prerequisites for `Optimization/contents/08 - Least Squares and Linear Equations.md`, `Econometrics/contents/03`, and `Data Preparation and Visualization` (PCA).

## Open items

- Scope (Nicholson ch. 1–8; ch. 9–11 excluded, reasons in the index) is my decision and needs syllabus confirmation. Ch. 8 is non-negotiable for Data Science (spectral theorem, PCA).
