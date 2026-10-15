# Business Management

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata (none filed; six discrepancies declined): `contents/00-Index.md`.

## Source

**Nickels, McHugh & McHugh, *Understanding Business*, 12th ed. (McGraw-Hill, 2018)** — the only file in `documents/`. 249 pages, no lecture slides. **The scope is the source's, not an editorial guess:** the file "Chapter 1-9" holds nine curated, non-contiguous chapters (Nickels 1, 2, 3, 4, 5, 7, 11, 13, 17), one note each.

## Extraction

- Text layer is clean; prose is unmangled.
- **The page offset is piecewise** (+2 for ch. 1–5, then −27 ch. 7, −103 ch. 11, −130 ch. 13, −212 ch. 17), **but every page carries a stamp** like `nic29434_ch05_110-139.indd 118` (chapter, its book-page range, the current page). **Locate any chapter by grepping `_chNN_`; never count pages.**
- **Graph axis labels extract as glyph names**: `/one.tnum/five.tnum` = "15" (`/N.tnum` = digit N, concatenated). Decode, never transcribe. Seen only in ch. 02.
- Tables and statements survive whole (ch. 07's fifteen-act legislation table, ch. 09's balance sheet and income statement, whose subtotals verify). Every figure is a label-schematic and came through.

## Boundaries: this subject is the integration layer

Most of Nickels is owned, more deeply, by finished subjects. Where a topic is owned elsewhere, the note gives the business framing, names the owner, links there, and doesn't re-derive.

| Nickels ch. | Overlaps | Owner |
|---|---|---|
| 2 Economics | supply/demand, capitalism, market structures | `Macroeconomics & Microeconomics` |
| 3 Global markets | comparative advantage, exchange rates, protectionism | Macro/Micro ch. 01; `Monetary and Financial Theories` ch. 10 |
| 5 Mergers, LBOs | merger risk arithmetic | `Commercial Banking` ch. 02 |
| 13 Marketing | four Ps, research, segmentation | `Principles of Marketing` |
| 17 Accounting | accounting cycle, statements, ratios | `Principle of Accounting` |

New to the vault, full depth here: ethics and CSR (note 04), legal forms of business (05), management and leadership (06), human resource management (07).
