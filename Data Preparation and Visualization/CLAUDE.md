# Data Preparation and Visualization — subject context

**Status: ✅ complete** (2026-07-27). `contents/00-Index.md` plus chapters 01–11. This was the **first subject written in the vault** — it set the conventions now recorded in the root `../CLAUDE.md`.

## Sources

**12 lecture decks in `documents/slides/`** (PDF + PPTX), extracted with `pypdf` / `python-pptx`. No textbook. Lecturer: **Dr. Nguyen Tuan Long**, ntlong@neu.edu.vn.

Structure follows the lecturer's three parts: Part 1 Pandas (ch. 01–03), Part 2 data preparation (ch. 04–09), Part 3 visualization (ch. 10–11).

## Chapters

01 Getting Started with Pandas · 02 Loading, Diagnosing, Missing Data and Combining Datasets · 03 Data Aggregation and Group Operations · 04 Foundations of Data Preparation for ML · 05 String Manipulation and Time Series Data · 06 Data Cleaning · 07 Data Transformation · 08 Feature Selection · 09 Building Pipelines · 10 Visualization with Matplotlib and Seaborn · 11 Chart Design and Data Storytelling

## Gaps in the source material — raise these with the lecturer

- **Lesson 4 is missing entirely.** The decks run 0, 1, 2, 3, 5, 6, 7, 8, 9. Nothing fills the jump from Data Aggregation to String Manipulation.
- **Chapter 04 is my editorial placement, not a recovered Lesson 4.** `Foundation of Data preparation for ML.pdf` is unnumbered in the source.
- **Dimensionality reduction (PCA / SVD / t-SNE) has no recoverable content anywhere**, though it is named as one of the five task groups. (Cross-link: `Linear Algebra/contents/08 - Orthogonality.md` covers PCA properly.)
- The **Seaborn half** of the Matplotlib/Seaborn `.pptx` is almost entirely images; reconstructed code in ch. 10 is marked as such.
- **Lesson 7 poses eight "Question:" prompts it never answers** — answered in ch. 07's exercises as reconstructions.
- `OnlineRetail.xlsx` / `.csv` and the Pokémon dataset are referenced but **absent from `documents/`**, so nothing can be re-run.

## If new material arrives

If the user supplies the missing Lesson 4 or the dimensionality-reduction material, add it and update the gap warning in `contents/00-Index.md`. A recovered Lesson 4 would renumber nothing — chapter 04 stays where it is; slot the new content beside it and say so.
