# Data Structures and Algorithms

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Sources

| File | Pages | Role |
|---|---|---|
| `Data Structures and Algorithms in Python ( PDFDrive ) (1) (1).pdf` | 770, 15 ch | **Goodrich, Tamassia & Goldwasser**: the spine (structure, theory, analysis) |
| `Fundamentals-of-python-data-structures-2nbsped-...pdf` | 450, 12 ch | **Lambert**: narrower, but **the only usable source of code** |

No lecture slides.

## Extraction: Goodrich's code is destroyed, Lambert's survives

**Goodrich's Python can't be transcribed.** `1 class GameEntry: / 4 def  init  (self,n a m e ,s c o r e ) :` shows all three failures: **indentation lost**, **double underscores render as spaces** (`__init__`→`init`, `_name`→`name`: plausible and wrong), identifiers space-separated and operators broken (`*=`→`=`). Line numbers survive.

**Lambert's Python extracts perfectly** (indentation, dunders, docstrings). So: Goodrich for prose/theory/analysis, Lambert for code where they overlap, my own implementations elsewhere. Lambert has no heaps, balanced trees or text processing, so heaps, AVL/splay/red–black, skip lists, hash internals, B-trees, KMP and DP are entirely mine.

- Goodrich prose and analysis maths extract well. Goodrich page $n$ ≈ PDF page $n+22$.
- Lambert's TOC is caps-mangled (`cHAP te R 1 b asic Python Programming`); strip the Cengage banner on every page.
- **All figures in both books are lost** (severe for ch. 06–10): print the actual state of the structure from running code instead.

## Verification: the unit is a program

1. **Run every listing.** It must execute.
2. **Test edge cases**: empty, single element, duplicates, sorted, reverse-sorted.
3. **Measure the complexity claim**: time a growing input and check the ratio follows the predicted curve.

## Boundaries

**`Discrete Mathematics/` owns the mathematics, this subject the implementations** (recorded in both indexes). Cross-link rather than re-prove: Big-O (DM 04), recurrences (DM 07), induction (DM 02), graph/tree theory and Dijkstra/Prim/Kruskal correctness (DM 08–09), the $\Omega(n\lg n)$ sorting bound (DM 09 §8), pigeonhole for hashing (DM 06), max-flow (DM 10). **Amortised analysis (ch. 04) is the one analytical topic DM doesn't cover**, so it is developed here. Ch. 01 is the only place in the vault that teaches core Python.

## Open items

Scope (Goodrich 1–14 plus §15.3 B-trees folded into ch. 10) is my decision. If the syllabus arrives, likely mismatches: (1) memory hierarchy (G §§15.1–15.2, excluded); (2) text-processing depth (G13: ch. 12 keeps pattern matching, tries, DP); (3) the Python primer (G1, compressed into ch. 01).
