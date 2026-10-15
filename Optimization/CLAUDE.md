# Optimization

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata (full table): `contents/00-Index.md`.

## Sources (`documents/`)

| Short name | File | Role |
|---|---|---|
| **C&Ż** | `An Introduction to Optimization, 4th Edition Edwin K. P. Chong, Stanislaw H. Zak-An.pdf` | **Primary spine**: unconstrained + LP + constrained |
| **L&Y** | `2016_Book_LinearAndNonlinearProgramming.pdf` (Luenberger & Ye) | deeper theory, better proofs, sensitivity/duality economics |
| **B&T** | `Dimitris Bertsimas, John N. Tsitsiklis - Introduction to Linear Optimization (1997)` | LP only, authoritative |
| **Léonard & Long** | `Optimal_Control_Theory_and_Static_Optimization_in_Economics` | **unusable: 367 pages, zero extractable text** |

No lecture slides. Source conflicts worth knowing: **"polytope" and "polyhedron" mean opposite things** in C&Ż §4.5 and B&T §2.1 (notes use the modern convention); C&Ż Thm 8.4 and L&Y Thm 2 give different steepest-descent rates, and only L&Y's is attained.

## Extraction

Re-extract each book whole to a scratchpad file and split by line range; grep the TOC line numbers to find a chapter.

**C&Ż OCR substitution table** (the book is scanned; this is OCR damage, not a font cipher; chapters 10–12 cite this table):

| Reads as | Means | | Reads as | Means |
|---|---|---|---|---|
| `G`, `£` | ∈ | | `V/`, `V /` | ∇f |
| `—►`, `->` | → | | `£>/` | *Df* |
| `φ` | ≠ *or* φ (context) | | `F(x)` | Hessian |
| `\\x\\` | ‖x‖ | | `/` alone | *f* |
| `#i` | xᵢ | | `fc` | *k* |
| `7fc` | γₖ | | `p` | ρ |
| `e`, `£` | ε | | `0fk(afc)` | φₖ(αₖ) |
| `1Z(A)`, `11(A)` | ℝ(A) (range) | | `λί(Α)` | 𝒩(A) (nullspace) |

**All transpose superscripts are lost everywhere.** **All matrices lose their brackets and row structure**: reconstruct by hand and verify by reproducing the example's printed answer. Simplex tableaus extract as a bare column of numbers.

**B&T fails silently**: some boxed definitions and theorems have no text layer while the prose around them reads fine. Don't assume a missing definition isn't there.

**L&Y extracts well** (born-digital): `/enc-118` marks the end-of-proof box, page numbers split digits (`8 3` for 83), inline references break across lines.

## Open items

Scope (12 chapters from four books) is my decision. If the syllabus arrives, likely mismatches: (1) **optimal control**: absent because the PDF has no text layer, so ask for a readable copy; (2) integer/combinatorial optimization (C&Ż 18–19, B&T 10–11); (3) network flows and max-flow/min-cut (`Discrete Mathematics/` ch. 10 has the duality); (4) interior-point methods in depth (summarised in ch. 12 §8). Each needs a **new chapter file plus an index update**.

Ch. 11's gaps callout defers C&Ż §20.6's equality-constrained QP closed form; ch. 12 is the natural place to mention it as the subproblem inside every SQP method.
