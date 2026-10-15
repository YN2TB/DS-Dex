# Computer Vision

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters with per-note state, errata: `contents/00-Index.md`.

The course is **still running**; slides arrive weekly.

## Sources

| | |
|---|---|
| **Slides (the spine)** | `slides/Lecture01…08_*.pdf`. Lecturer: **Nguyen Manh Toan (Swinburne Vietnam)** |
| **Textbook (reference)** | `documents/Szeliski_CVAABook_2ndEd.pdf`, 1,232 PDF pages, text layer fine. PDF page 301 = book page 275 (offset +26) |
| **Other stated reference** | Stanford CS231n notes (named on each lecture's "Reading & Reference" slide) |
| `note/project_topics.md` | Lecturer's 17 final-project topics: 50% of the grade, ~6 per team, presented week 15 |

**The lecture slides decide what a note covers**; Szeliski and papers fill in detail. Lectures 3+ end with a "Hands-On" slide naming a notebook not in the folder; lectures 6–8 have a "For Final Project" slide. Mention both in the matching note.

## Extraction quirks

**Slides (Beamer):**
- Prose and bullets extract cleanly and in order.
- Spaces next to italic or math runs are often deleted: `Whyk-NN` = "Why k-NN", `intokfolds` = "into k folds".
- Fractions flatten and superscripts drop: `x=f X Z` is $x = fX/Z$, `R H×W×3` is $\mathbb R^{H\times W\times 3}$. Rebuild formulas and check them numerically.
- Every slide ends with a footer `Nguyen Manh Toan (Swinburne Vietnam) Computer Vision Week N k / M`. Filter it out.
- Figures never extract. Captions and table cells do (e.g. the R-CNN family comparison). Check their numbers before quoting.

**Szeliski** extracts normally; figures lost.

The old notes' 11-point AP of 0.7045 was a float comparison bug (`0.6000000000000001 > 0.6`); correct value 0.712. **Use a tolerance when comparing recall levels.**

## Boundaries

**Each CV note covers everything its lecture teaches**, with the lecturer's formulas and examples, so it can be revised alone for the exam. `Deep Learning/` notes are linked for longer derivations and code-level detail only. (Not an explicit choice by the user; if they want shorter notes, keep definitions and formulas and move derivations to the DL links.)

## Open items

- **When `Lecture09_*.pdf` (and later) appears in `slides/`:** rewrite that note from its slides the same way, mark it in `00-Index.md`, and update the Progress row. Week 15 is project presentations: no note.
- Gaps flagged in the notes: **RANSAC** (ch. 14) and **camera calibration** (ch. 01 assumes it, ch. 14 doesn't derive it). Add them if a later lecture covers them.
