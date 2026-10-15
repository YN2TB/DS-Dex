# Calculus

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Sources

**Stewart, Clegg, Watson & Redlin, *Calculus: Early Transcendentals* 9e**, plus the same authors' ***Multivariable Calculus* (2020)**. Both in `documents/`. **No lecture slides.**

Verification found **no mathematical error anywhere in Stewart**; every failure in this subject is extraction, not authorship. Don't go looking for errata.

## Extraction: Stewart's maths is a glyph cipher

The worst extraction problem in the vault. **Stewart's maths font maps glyphs to the wrong codepoints, so every formula extracts as a substitution cipher.** The full key is in `contents/00-Index.md`. The core of it:

| Reads as | Means | | Reads as | Means |
|---|---|---|---|---|
| `s` … `d` | ( … ) | | `S` … `D` | large ( … ) |
| `f` … `g` | [ … ] | | `−` | **=** |
| isolated ` 1 ` | **+** | | isolated ` 2 ` | **−** |
| `l` | → | | `y` | fraction bar |
| `<` | ≤ | | `t` | Stewart's *second* function name (genuinely `t`) |
| `/H9266` | π | | | |

Worked example: `f sxd − x2 2 s2xy1000d` is $f(x)=x^2-\frac{2^x}{1000}$.

**`1` and `2` are ambiguous between digits and `+`/`−`**: spacing disambiguates, an isolated ` 2 ` is a minus. In ch. 15 the integral signs, limits and differentials also detach, and stacked limits sometimes invert. **Nothing from this book can be quoted without recomputation in `sympy`.**

**Every figure is an image and lost.** §15.3 (regions of integration) and §15.9 (the Jacobian) are sections whose figures *were* the argument. Two exercise sets are unattemptable (§15.1's Colorado contour maps, the swimming-pool table).

## Boundaries

- Vectors belong to `Linear Algebra/contents/04 - Vector Geometry.md`, which is why Stewart 12–13 are excluded.
- Ch. 06–08 are prerequisites for all of `Optimization/contents/`; ch. 09 for `Probability Theory/contents/06` (joint densities).
- Deliberate departures, recorded in the notes: ch. 08 expanded well beyond Stewart's 21 pages on multivariable optimization; the Gaussian integral $\sqrt\pi$ (Ex. 15.3.50) and the hyperspheres Discovery Project promoted into ch. 09.

## Open items

- Scope (Stewart 1–2, 3, 4, 5, 7, 11, 14.1–14.8, 15; the rest excluded, reasons in the index) is my decision and needs syllabus confirmation.
