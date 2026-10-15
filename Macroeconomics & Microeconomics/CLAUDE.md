# Macroeconomics & Microeconomics

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`. One folder, two courses: one sequence, micro 01–07 then macro 08–14.

## Sources: four overlapping books, no slides

| File | Use |
|---|---|
| `1-Mankiw - Principles of Macroeconomics 2017.pdf` | **Macro spine**, and the source for the shared ch. 1–9 |
| `Principles of Microeconomics( 6th Edition)_N. Gregory Mankiw.pdf` | **Micro spine** (micro ch. 10–22) |
| `mankiw_principles_of_economic 8th (1).pdf` | combined 8e, a superset: gap-filling only, **disclosed in the note when used** |
| `1-Michael Parkin, Robin Bade - Macroeconomics _ Chapter25-BoP and ex rate.pdf` | one chapter (BoP, exchange rates): **co-equal source for ch. 13** |

The three Mankiw books overlap on exactly ch. 1–9; the dedup mapping is in `contents/00-Index.md`. **All three have excellent outlines** (24 / 29 / 34 entries): locate by outline, then extract the range.

## Extraction: the operator cipher

**Mankiw's PDFs render every arithmetic operator as a digit**, so equations extract as lists of numbers and are **silently wrong**:

| extracts as | actually means |
|---|---|
| `5` | **=** |
| `1` | **+** |
| `2` | **−** |
| `3` | **×** |

`Y 5 C 1 I 1 G 1 NX` is $Y = C + I + G + NX$.

**It is not a fixed substitution.** `Price elasticity of demand 5 (Q2 2 Q1) / [(Q2 1 Q1) / 2]` is $\frac{Q_2-Q_1}{(Q_2+Q_1)/2}$: six digits, four meanings. In `(6 2 4) / 5 3 100 5 40`, `5` is both a literal and an equals sign. **There is no mechanical decoder: reconstruct each formula from the prose and verify it against the book's worked figures.**

Other faults: possessive apostrophes mangle (`today's`→`todayrs`), short phrases duplicate, running heads interleave. **Parkin & Bade extracts cleanly**, equations included.

**Every figure is an image and lost**, the worst case in the vault since Mankiw teaches through shifting curves. Captions and stray axis labels survive and **look like data**. Numerical tables are images too: recompute, never transcribe.

## Boundaries

- **Mankiw owns the macro model; `Monetary and Financial Theories/` (Mishkin) owns the financial plumbing** (money multiplier operations, central-bank operations). Recorded in both indexes.
- **Micro 22 (asymmetric information) is omitted only because `Commercial Banking/` ch. 11 owns it** (its credit-rationing curve is Stiglitz–Weiss). If the syllabus requires it, add it rather than substituting.
- Mankiw is calculus-free: cross-link `Calculus/contents/07` and `Optimization/contents/11` for consumer choice and cost minimisation (labelled additions). `Econometrics/contents/10–12` estimates these relationships.

## Open items

Scope (14 chapters from 36; excluded Micro 12, 19, 20, 22 and Macro 23, reasons in the index) is my decision and needs syllabus confirmation.
