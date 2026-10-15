# Probability Theory

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Source

**Ross, *A First Course in Probability* 10e (Global Edition)** — the only file in `documents/`. **No lecture slides.** Ross has five genuine errors; the table is in `contents/00-Index.md`.

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

**`log` means $\log_2$ throughout ch. 09**, stated in an easy-to-miss footnote. Getting it wrong changes every entropy figure by a factor of 1.4427.

## Boundaries

`Mathematical Statistics/contents/` builds directly on ch. 04–08; `Machine Learning/contents/02 - Markov Decision Processes.md` builds on ch. 09's Markov chains.

## Open items

- Scope (all ten chapters of Ross) is my decision. Ch. 1–8 are the standard core; ch. 9–10 were added because a Data Science degree needs them. If the course stops at ch. 8, say 09–10 are bonus material rather than assuming they're examinable.
