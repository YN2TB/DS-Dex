# Monetary and Financial Theories

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata (1 filed; 6 discrepancies investigated, not filed): `contents/00-Index.md`.

## Source

**Mishkin, *The Economics of Money, Banking, and Financial Markets* (Global Edition)** — the only file in `documents/`. **No lecture slides.** 746 pages, 26 chapters. **Book page $n$ = PDF page $n+1$.** The outline is excellent: locate by outline, extract the range. Unusually rich in worked numerical examples, so most chapters verify against the source directly.

## Extraction

**No operator cipher** (unlike Mankiw): prose arithmetic is reliable (`$1 million/(1 + 0.10) = $909,090` comes through intact). **But displayed equations lose their parentheses to digits:**

| extracts as | means |
|---|---|
| `11 + i2` | $(1+i)$ |
| `11 + i22` | $(1+i)^2$ |
| `11 + i2n` | $(1+i)^n$ |

`(` → `1`, `)` → `2`, exponent appended right after. The YTM formula `LV = FP/11 + i2 + FP/11 + i22 + ... + FP/11 + i2n` is $LV=\sum FP/(1+i)^t$. **In inline maths the parentheses survive but superscripts flatten**: `(1 + 0.10)2` is $(1.10)^2$. The fault is inconsistent within a chapter, so **reconstruct every displayed formula and check it against a worked number**.

**Figures split three ways:** data series are always lost; shift diagrams' content is the direction, which the prose states; schematics whose content is their labels survive (ch. 10's trilemma triangle, ch. 12's transmission figure). Check whether the prose names a figure's points before recording it lost. Figure axis labels are unreliable (`(i 5 33.0%)` where the prose says 33.3%).

**Numeric tables set as text survive whole** (nine confirmed). Verify subtotals before trusting.

**Mishkin sends topics to off-book appendices**: check the footnotes before assuming a topic is absent. Duration (ch. 4), CAPM/diversification/loanable funds (ch. 5), **the EMH anomalies** (ch. 7, the significant loss), money-demand empirics (ch. 20).

## Boundaries: the three-way split, stated in all three indexes

- **`Commercial Banking/` owns the bank's balance sheet** (spread, gap/duration, capital, credit risk, liquidity, lending).
- **`Macroeconomics & Microeconomics/` owns the macro model** (AD–AS, Phillips curve, quantity theory as identity, growth, fiscal multiplier).
- **This subject owns the monetary system** (rate determination, term-structure theory, central-bank operations and transmission, asymmetric information, crises). Ch. 04 discharges CB ch. 07's term-structure reference; ch. 08 discharges Macro/Micro ch. 12's money-multiplier reference.
- Computed elsewhere, link rather than re-derive: present value and diversification (Macro/Micro ch. 10), securitisation correlation (CB ch. 06), credit rationing $r^*=18\%$ (CB ch. 11, explained theoretically in ch. 06 here), the solvent bank failing at 48.5% withdrawals (CB ch. 08).

## Open items

- Scope (12 chapters from 26; reasons per omission in the index) is my decision. The exclusion most worth arguing about is Mishkin 9 (bank management), owned by Commercial Banking ch. 03–08.
