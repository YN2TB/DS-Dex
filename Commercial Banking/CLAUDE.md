# Commercial Banking

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Source

**Rose & Hudgins, *Bank Management and Financial Services* 9e** — the only file in `documents/`. **No lecture slides.**

## Extraction: five traps

**Book page $n$ = PDF page $n+18$** ("Chapter Three … 83" on PDF p101). 760 pages, **554 MB**.

1. **A watermark is interleaved with the body text** on every page: strip lines matching `Username:|reproduced|transmitted|prior written|Violators|Terms of Service|^\d{6,} \d{4}/`.
2. **Hyphens sometimes render as commas** (`Financial,Services`, `disas,ter`): read `,` as `-` inside a hyphenated word.
3. **No usable PDF outline** (bookmarks are scan-sheet numbers). The chapter list came from Brief Contents, PDF pp. 6–7. Known ranges: ch. 7 = PDF 235–272, ch. 8 = 273–310, ch. 9 = 311–338, ch. 10 starts at 339.
4. **Whole-book page scans time out** (554 MB). Extract targeted ranges only.
5. **Running headers in ch. 8–9 are OCR'd** (`Loan Sal.es`): body text is clean, but don't locate chapters by header strings.

**Graphical exhibits are lost; tabular statements set as text survive** (the BB&T Report of Condition extracted completely and its subtotals verify; the Report of *Income* did not). Test before assuming; verify subtotals before trusting a table.

## Verification

The book's own worked figures are largely unrecoverable, so **build a stated bank balance sheet + income statement and derive every ratio from it in Python**, labelling the numbers as mine and the formulas as the book's. Never reconstruct from a partial table.

## Boundaries

- **This subject owns the bank's own balance sheet** (spread, gap/duration, capital, credit risk). **`Monetary and Financial Theories/` owns the monetary system** (rate determination, term-structure theory, central-bank operations, money supply and transmission). Both indexes record the split.
- `Principle of Accounting/contents/` ch. 02 (accounting equation) and 08 (receivables: loans *are* receivables) are prerequisites. `Macroeconomics & Microeconomics/` for the money multiplier.

## Open items

- Scope is my decision: R&H 14 (fee income) and 19 (mergers) are folded in elsewhere; **R&H 20 (international banking) is the largest single omission**: flag it to the user.
