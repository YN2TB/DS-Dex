# Calculus — subject context

**Status: ✅ complete** (2026-07-29). `contents/00-Index.md` plus chapters 01–09.

## Sources

**Stewart, Clegg, Watson & Redlin, *Calculus: Early Transcendentals* 9e**, plus the same authors' ***Multivariable Calculus* (2020)**. Both in `documents/`. **No lecture slides.**

## Scope — my editorial decision, chosen by downstream necessity; needs syllabus confirmation

Nine notes map to **Stewart ch. 1–2, 3, 4, 5, 7, 11, 14.1–14.6, 14.7–14.8, 15.**

**Excluded: Stewart 6, 8, 9, 10, 12, 13, 16, 17** — mostly because `Linear Algebra/contents/04 - Vector Geometry.md` already covers vectors, and vector calculus is used nowhere in a DS curriculum. The index states the exclusions and why.

**Ch. 08 was deliberately expanded well beyond Stewart's 21 pages** on multivariable optimization, which is a serious under-weighting for a DS reader.

## Chapters

01 Functions, Limits and Continuity · 02 Derivatives · 03 Applications of Differentiation · 04 Integrals · 05 Techniques of Integration · 06 Sequences, Series and Taylor Approximation · 07 Partial Derivatives and the Gradient · 08 Multivariable Optimization · 09 Multiple Integrals and Change of Variables

## ⚠️ The worst extraction problem in the vault: Stewart's maths is a glyph cipher

**Stewart's maths font maps glyphs to the wrong codepoints, so every formula extracts as a substitution cipher.** The full key is in `contents/00-Index.md`. The core of it:

| Reads as | Means | | Reads as | Means |
|---|---|---|---|---|
| `s` … `d` | ( … ) | | `S` … `D` | large ( … ) |
| `f` … `g` | [ … ] | | `−` | **=** |
| isolated ` 1 ` | **+** | | isolated ` 2 ` | **−** |
| `l` | → | | `y` | fraction bar |
| `<` | ≤ | | `t` | Stewart's *second* function name (genuinely `t`) |
| `/H9266` | π | | | |

Worked example: `f sxd − x2 2 s2xy1000d` is $f(x)=x^2-\frac{2^x}{1000}$.

**The dangerous part is that `1` and `2` are ambiguous between digits and the `+`/`−` signs** — spacing disambiguates, an isolated ` 2 ` is a minus. In ch. 15 the integral signs, limits and differentials also detach from each other, and stacked limits sometimes invert.

**Nothing from this book can be quoted without recomputation.** Every worked example, limit, derivative, integral, series, critical point and iterated integral in these notes was independently evaluated with `sympy` before being written down.

## Do not go looking for errata here

**That verification found no mathematical error anywhere in Stewart** — across all nine chapters. Contrast `Linear Algebra` (Nicholson, 10+ defects) and `Probability Theory` (Ross, 5 real errors). **Every failure in this subject is extraction, not authorship.**

## Every figure in the book is an image and all are lost

For a subject taught through pictures this is structural, not cosmetic. §15.3 (drawing regions of integration) and §15.9 (the Jacobian derivation) are sections whose figures *were* the argument. **Two exercise sets are unattemptable** because their data lives only in images — §15.1's Colorado contour maps and the swimming-pool table.

## Two deliberate departures from the book's emphasis

Both recorded in the notes:
- the **Gaussian integral $\sqrt\pi$** was promoted out of Exercise 15.3.50 into ch. 09's body
- the **hyperspheres Discovery Project** (curse of dimensionality) into ch. 09 §9

Cross-subject: ch. 06–08 are prerequisites for all of `Optimization/contents/`; ch. 09 for `Probability Theory/contents/06` (joint densities).
