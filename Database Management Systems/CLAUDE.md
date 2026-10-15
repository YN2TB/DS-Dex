# Database Management Systems

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Source

**Coronel & Morris, *Database Systems: Design, Implementation, & Management*** (Cengage 2023) — the only file in `documents/`. **No lecture slides.** A business-school text: long on process, short on theory. Relational algebra and NoSQL were enriched; enrichment is labelled in the gaps callouts.

## Extraction: clean

No glyph mangling, no mangled identifiers, real prose. **Book page $n$ = PDF page $n+28$** (book p.12 = PDF p.40). 818 pages. **All ER/schema/table figures are images and lost**, severe for ch. 03 and ch. 10: reconstruct only what the prose fully determines.

## Verification: run the SQL

`sqlite3` engine **3.50.4** is available (window functions, CTEs, recursive CTEs work). Execute every query against a scratch database and print the **actual output**, never the book's. Where a query needs something SQLite lacks (old `FULL OUTER JOIN`, Oracle/T-SQL syntax, materialised views), say so rather than showing it as if it ran.

## Boundaries

- **`Data Structures and Algorithms/` owns the internals; link, don't re-derive:** B-trees and the block-transfer cost model (DSA 10 §7), hashing (DSA 09), external merge-sort (DSA 11), why ranges need an ordered index (DSA 09 §8).
- Functional dependency as a relation property: `Discrete Mathematics/contents/03`.
- Star schemas / OLAP connect to `Data Preparation and Visualization/` and to `PowerBI/` (blocked; this subject owns the modelling theory). Transactions connect to `MLOps/contents/03 - Data in MLOps.md`.
