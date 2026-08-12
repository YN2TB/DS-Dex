# Optimization — subject context

**Status: ✅ complete** (2026-07-30). `contents/00-Index.md` plus chapters **01–12**, all verified.

Read the root `../CLAUDE.md` for the note template and universal conventions. Everything below is specific to Optimization.

## Sources (`documents/`)

| Short name | File | Role |
|---|---|---|
| **C&Ż** | `An Introduction to Optimization, 4th Edition Edwin K. P. Chong, Stanislaw H. Zak-An.pdf` | **Primary spine.** Right level, covers unconstrained + LP + constrained. |
| **L&Y** | `2016_Book_LinearAndNonlinearProgramming.pdf` (Luenberger & Ye) | Deeper theory, better proofs, sensitivity/duality economics. |
| **B&T** | `Dimitris Bertsimas, John N. Tsitsiklis - Introduction to Linear Optimization (1997)` | LP only, authoritative. |
| **Léonard & Long** | `Optimal_Control_Theory_and_Static_Optimization_in_Economics` | **Unusable — 367 pages, zero extractable text.** Optimal control is therefore out of scope; this is flagged in `00-Index.md`. |

No lecture slides. **Scope is an editorial decision** (12 chapters, stated at the top of `00-Index.md` with a "what is not covered, and why" section). Needs syllabus confirmation.

## Chapter plan

| # | Title | Sources | Status |
|---|---|---|---|
| 01 | The Optimization Problem | C&Ż 6; L&Y 1 | ✅ |
| 02 | Convex Sets and Convex Functions | C&Ż 4, 22; B&T 2 | ✅ |
| 03 | Unconstrained Optimality Conditions | C&Ż 6 | ✅ |
| 04 | One-Dimensional Search Methods | C&Ż 7; L&Y 8 | ✅ |
| 05 | Gradient Methods | C&Ż 8; L&Y 8 | ✅ |
| 06 | Newton and Quasi-Newton Methods | C&Ż 9, 11; L&Y 10 | ✅ |
| 07 | Conjugate Direction Methods | C&Ż 10; L&Y 9 | ✅ |
| 08 | Least Squares and Linear Equations | C&Ż 12; L&Y 8 | ✅ |
| 09 | Linear Programming and the Simplex Method | C&Ż 15–16; L&Y 2–3; B&T 1–3 | ✅ |
| 10 | Duality | C&Ż 17; L&Y 4; B&T 4 | ✅ |
| 11 | Constrained Optimization - Lagrange and KKT | C&Ż 20–21; L&Y 11 | ✅ |
| 12 | Convex Programming and Constrained Algorithms | C&Ż 22–23 (+14, 24); L&Y 12–13, §5.5 | ✅ |

**Filename note:** ch. 11 uses a **dash, not a colon** — Windows forbids `:` in filenames.

## Extraction

Both usable books are already extracted to the session scratchpad as `cz_all.txt` (all of C&Ż) and `ly_all.txt` (all of L&Y). If those are gone, re-extract whole and split by line range — grepping the TOC line numbers is the fast way to find a chapter.

**C&Ż OCR substitution table** (the book is scanned, not born-digital — this is OCR damage, not a font cipher):

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

**All transpose superscripts are lost everywhere.** **All matrices lose their brackets and row structure** — every matrix in these notes was reconstructed by hand and verified by reproducing the example's printed answer. Simplex tableaus are the worst case: they extract as a bare column of numbers.

**B&T fails silently** — some boxed definitions and theorems have no text layer at all while the surrounding prose reads fine. Do not assume a missing definition isn't there.

**L&Y extracts well** (born-digital), with minor artefacts: `/enc-118` marks the end-of-proof box, page numbers split digits (`8 3` for 83), and inline references break across lines.

## Errata and source conflicts found

The full table lives in `contents/00-Index.md`. The consequential ones:

- **C&Ż §23.5 Example 23.3(c) — genuine wrong value.** Prints $\|\mathbf x_\gamma\|^2-1=-\lambda_{\max}/(2\gamma)$ where $-\lambda_\gamma/(2\gamma)$ is correct, and for a *minimization* problem $\lambda_\gamma\to\lambda_{\min}$. The *bound* is fine, the *equality* is not — **wrong by the factor $\kappa$, hence unbounded across problems.** Verified at $\gamma=10^4$, $Q=\operatorname{tridiag}(1,3,1)$: true $-7.929\times10^{-5}$, printed $-2.207\times10^{-4}$.
- **C&Ż §7.5 Example 7.5 — genuine arithmetic error.** Prints $12-\frac{102.6}{146.65}=11.33$; it is $11.3004$. Confirmed *not* OCR: the next step's $14.73$ and $116.11$ are $g$ and $g'$ evaluated at $11.33$, so the wrong value is carried forward. The printed $x^{(2)}=11.21$ should be $11.20$. True root is exactly $11.2$.
- **C&Ż §7.6 Example 7.6 — wrong points used.** Prints $x^{(2)}=11.25$; the secant recursion on the two most recent iterates $(12,\,11.4016)$ gives $11.2272$. The printed value is exactly what pairing the *stale* $x^{(-1)}=13$ with $x^{(1)}$ produces ($11.2537$) — a violation of the method's own definition.
- **"Polytope" and "polyhedron" mean opposite things** in C&Ż §4.5 and B&T §2.1. The notes adopt the modern convention (polyhedron = intersection of half-spaces, polytope = bounded polyhedron) and flag the clash at first use.
- **C&Ż Thm 8.4 vs L&Y Thm 2** give different steepest-descent rates: $1-1/\kappa$ vs $\left(\frac{\kappa-1}{\kappa+1}\right)^2$. Both valid; **only L&Y's is attained** (verified from three starting points).
- **C&Ż's showcase Newton example (Powell) converges only linearly**, ratio exactly $(2/3)^4$, because $\nabla^2f(\mathbf 0)$ has eigenvalues $\{202,20,0,0\}$ — the book never remarks that its own example violates Theorem 9.1's invertibility hypothesis. Ch. 06 Exercise 2 makes this the point of the exercise.
- **Not errors, OCR:** C&Ż §22.2 Ex 22.5 loses a $\tfrac12$; Ex 10.2 loses a minus sign; L&Y p. 2/4 subscript artefact; L&Y §8.2 rounds $r=1.8077$ to $1.8$.

**Data recovered from the books' own arithmetic** (the tables were image-only): C&Ż Ex 12.3 — the printed $A^{\mathsf T}A=\begin{psmallmatrix}6&1\\1&6\end{psmallmatrix}$ forces $\mathbf s=(1,2,1)$ and the printed sums force $\mathbf r=(4,7,8,6,3)$, after which everything reproduces.

## Additions beyond the sources

Each is labelled as mine in that chapter's gaps callout:

- coercivity theorem + proof (ch. 01); calculus of convexity table, strict convexity ⟹ unique minimizer (ch. 02)
- why the optimality conditions are not an algorithm at scale (ch. 03); the Wolfe↔BFGS connection (ch. 04)
- **SGD, momentum, Adam, Robbins–Monro (ch. 05)** — the largest gap: *none of the four books covers stochastic optimization*, which is the only kind a DS reader will use
- L-BFGS and the per-iteration cost tables (ch. 06); CG as the standard large sparse SPD solver, Hessian-free/truncated Newton (ch. 07)
- "never form the normal equations" with the Läuchli failure (ch. 08); Klee–Minty vs practice, smoothed analysis (ch. 09)
- **Farkas' lemma and duality-as-certificates (ch. 10)** — C&Ż leaves Farkas in unproved exercises; the degeneracy analysis in ch. 10 Ex. 4 (both books state $\Delta z=\mathbf y^{\mathsf T}\Delta\mathbf b$ and never show it failing)
- **the Rayleigh quotient as PCA/LDA/CCA/spectral clustering (ch. 11 §7)** — C&Ż present it as pure algebra; also **KKT ⟹ the LP dual** in four lines (ch. 11 Ex. 5), which appears in neither book
- **§9 of ch. 12 entirely** — proximal gradient/ISTA/FISTA, soft-thresholding, projection as the prox of an indicator, ADMM, mirror descent, SQP, the projections table, SDP-as-relaxation, Slater's condition stated explicitly, and ROC curves as Pareto fronts
- **Throughout:** softmax/exponential families as maximum entropy, SVM support vectors as complementary slackness, ridge/LASSO as a Lagrangian pair, constrained deep learning (TRPO/RLHF) as primal–dual ascent. **None of the four books contains any of it.**

## Subject-wide findings worth keeping

- **The single biggest gap across all four books is stochastic optimization** — no SGD, momentum, Adam, or proximal/splitting methods anywhere. For a DS reader that is *the* relevant regime, so ch. 05 §8 and ch. 12 §9 carry it.
- **C&Ż's defects cluster in the numerical-methods chapters** (7, 23). No error was found in its theory chapters (4, 6, 15–17, 20–22), nor anywhere in L&Y or B&T.
- **Every matrix and every simplex tableau in C&Ż was reconstructed by hand** and verified by reproducing the book's printed answer. Simplex tableaus extract as bare columns of digits; ch. 10 does not reproduce Example 17.3's six-tableau run for this reason.
- **All figures in all four books are lost.** Most damaging: C&Ż Fig. 21.1 (the geometric reading of KKT), Fig. 20.12 (the four Lagrange configurations including the non-extremizer), and L&Y Figs. 11.6 / 13.2 / 4.1–4.3.
- **Léonard & Long is unreadable, so optimal control is absent from the whole subject.** This is the one thing to flag to the lecturer.

## If the syllabus arrives

The **scope decision is unconfirmed** — 12 chapters chosen from four books, stated at the top of `contents/00-Index.md` with a "what is not covered, and why" table. Most likely mismatches, in order:

1. **Optimal control** (Léonard & Long) — completely absent, and *not* an editorial choice: the PDF has no text layer. **If the course covers it, say so plainly and ask for a readable copy.**
2. **Integer / combinatorial optimization** (C&Ż 18–19, B&T 10–11) — excluded as a different subject. Ch. 12 §9 and ch. 10's Farkas material give the LP-relaxation and bounding ideas it would build on.
3. **Network flows and max-flow/min-cut** (L&Y §4.5, B&T 7) — the most attractive omission; L&Y calls max-flow/min-cut "one of the most exemplary primal–dual pairs."
4. **Interior-point methods in depth** (L&Y 5–6) — summarised in ch. 12 §8 rather than given a chapter.

Adding any of these needs a **new chapter file plus an index update**, not an edit to an existing note.

**Also worth closing the loop on:** ch. 11's gaps callout defers C&Ż §20.6's equality-constrained QP closed form to `00-Index.md`; ch. 12 is the natural place to mention it as **the subproblem solved inside every SQP method.**

After ch. 12: flip its index row, set this file's status to ✅ complete with the full chapter list, update the root `../CLAUDE.md` progress table, and note completion in the memory pointer if anything non-obvious remains.
