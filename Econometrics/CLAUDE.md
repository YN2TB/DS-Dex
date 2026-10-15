# Econometrics

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Source

**Wooldridge, *Introductory Econometrics: A Modern Approach*, 7e** — `documents/Wooldridge-Introductory-Econometrics_-A-Modern-Approach.pdf`. **No lecture slides.**

This subject's `00-Index.md` is **the template for every textbook-only subject**: scope stated up front, then "what is not covered, and why".

## No data files exist in the vault

`WAGE1`, `PHILLIPS`, `BARIUM`, `NYSE`, `EARNS` and the rest are **all absent**, so **no regression can be re-estimated.** Every regression in the notes is quoted as printed. Every derived statistic (t, F, LM, p-values, turning points, intervals, the Newey–West SE) was recomputed with scipy and agrees with the text.

## Extraction quirks

Two-column layout mangles maths: `b^ j` for $\hat\beta_j$, `E1u0x2` for $E(u\mid x)$, `g` for $\Sigma$, `R2 j` for $R^2_j$. **Every equation must be transcribed and checked by hand.**

**The minus sign renders as the digit `2` throughout**: sign-check every negative coefficient against the surrounding prose.

All figures and all statistical tables are images and do not extract.

**Table 9.1's turning point does not reconcile:** the printed coefficients give **0.379**, the text says **0.365**. Recorded in the notes as an unresolved discrepancy.

## Boundaries

`Time-series Analysis/contents/` covers stationarity, unit roots and serial correlation from the ARMA side; ch. 10–12 cross-link to it. Ch. 03–05 lean on `Linear Algebra/contents/08 - Orthogonality.md` and `Optimization/contents/08 - Least Squares and Linear Equations.md`.

## Open items

- Scope (Wooldridge ch. 1–12) is my decision and needs syllabus confirmation. **Ch. 15 (IV) is the omission most likely to matter** if the course emphasises endogeneity.
- New material from ch. 13–19 needs a **new chapter file and an index update**, not an edit to an existing note.
