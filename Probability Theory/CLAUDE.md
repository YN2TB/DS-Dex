# Probability Theory — subject context

**Status: ✅ complete** (2026-07-29). `contents/00-Index.md` plus chapters 01–10.

## Source

**Ross, *A First Course in Probability* 10e (Global Edition)** — the only file in `documents/`. **No lecture slides.**

## Scope — my editorial decision, needs syllabus confirmation

**All ten chapters of Ross.** Ch. 1–8 are the standard one-semester core; **ch. 9–10 (Poisson processes, Markov chains, entropy/coding, simulation) were included because a Data Science degree needs them.** If the real course stops at ch. 8, chapters 09–10 are bonus material — say so rather than assuming they're examinable.

## Chapters

01 Combinatorial Analysis · 02 Axioms of Probability · 03 Conditional Probability and Independence · 04 Random Variables · 05 Continuous Random Variables · 06 Jointly Distributed Random Variables · 07 Properties of Expectation · 08 Limit Theorems · 09 Additional Topics in Probability · 10 Simulation

## ⚠️ Five genuine errors in Ross — errata table is in `contents/00-Index.md`

The two that matter:

- **ch. 06 birthday-triple value.** Ross prints $.504$ at $n=88$; the correct value is **$.4889$** (confirmed by simulation).
- **ch. 08 Example 5e prints $\ge$ where $\le$ is required**, which invalidates the Chernoff derivation exactly as printed.

Also: ch. 09 applies the ergodicity theorem to the **periodic** Ehrenfest chain; the ch. 07 summary misstates the variance-of-a-sum formula.

## `log` means $\log_2$ throughout ch. 09

Stated in a footnote that is easy to miss. **Getting it wrong changes every entropy figure by a factor of 1.4427.**

## Extraction quirks

**Ross's PDF extracts unusually well** — notably `<` and `>` survive intact. But:

| Reads as | Means | | Reads as | Means |
|---|---|---|---|---|
| `…` | ≤ | | `Ú` | ≥ |
| `q` | ∞ | | `Z` | ≠ |
| `L` | ≈ | | `K` | ≡ |
| `3` | ⟺ | | `%` | → |
| `5` | = | | `2` | − (in figures) |

Binomial coefficients extract across four lines. The same Greek capital gets three different encodings (`/Phi1`, `/H9278` for Φ). All figures are images.

## Verification standard

**Every numeric claim in all ten chapters was recomputed** (scipy / mpmath / simulation) before being written, and every exercise's arithmetic verified before the exercise was written down. That is why no arithmetic error reached the notes — keep the practice.

Cross-subject: `Mathematical Statistics/contents/` builds directly on ch. 04–08; `Machine Learning/contents/02 - Markov Decision Processes.md` builds on ch. 09's Markov chains.
