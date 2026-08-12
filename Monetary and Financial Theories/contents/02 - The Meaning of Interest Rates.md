---
subject: Monetary and Financial Theories
chapter: 2
tags: [ds, economics, interest-rates, present-value, yield-to-maturity, bonds, duration, fisher-equation]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 4"
---

# The Meaning of Interest Rates

**There are four different numbers called "the interest rate", and confusing them is expensive.** Mishkin's chapter is nominally about definitions; **its actual content is that the *yield to maturity* tells you nothing about how well you will do.**

**Three results.**

**§5 — Mishkin's Table 2, reproduced exactly.** *(Every figure verified.)* **A 10% bond can lose you 39.7% in a year.** Irving the Investor knew his bond's interest rate precisely and still lost his shirt.

**§6 — the chapter's main addition: maturity is the wrong metric, and duration is the right one.** *(Computed: the 30-year and 20-year bonds lose **49.75% and 48.43%** — nearly identical despite ten years' difference in maturity — **because their durations are 10.37 and 9.36 years, barely one year apart**. Mishkin's table shows this and cannot explain it; **he relegates duration to an appendix that is not in the book.**)*

**§6 also — and this is the vault's rule #1 again: duration predicts a 94.27% loss where the exact repricing gives 49.79%.** **A first-order measure reports success precisely when the risk it omits is the one that matters.**

**⚠️ One erratum filed** *(§7 — a $1,555 that should be $1,155)*, **and one discrepancy deliberately not filed.**

## 📘 Main Knowledge

### 1. Present value — the whole chapter rests on one equation

$$PV=\frac{CF}{(1+i)^n}\qquad\text{(Mishkin's Equation 1)}$$

> [!note] Why: a dollar today can be invested
> **\$100 at 10% becomes \$110, \$121, \$133 over three years** *(verified — exactly \$133.10; **the book rounds to \$133**, which is why discounting it back gives \$99.92 rather than \$100)*. **Discounting is that operation run backwards.**

> [!warning] ⚠️ The lottery jackpot — the chapter's best application
> **"You have won \$20 million"** — \$1 million a year for twenty years. *(Verified against Mishkin's own figures: the year-1 payment is worth **\$909,090**, the year-2 payment **\$826,446**, and the whole stream is worth **\$9.36 million** — the book says \$9.4 million.)*
>
> **The advertised figure is 213% of the truth.** *(Computed: the PV is **46.8%** of the headline.)*
>
> **⚠️ And the general principle is bigger than the example: adding cash flows across time is not an operation you are allowed to perform.** The "\$20 million" sums quantities that are not commensurable — **exactly as [[Macroeconomics & Microeconomics/contents/08 - Measuring the Macroeconomy - GDP and the Cost of Living|Macro/Micro ch. 08]] found you may not add 1990 and 2020 dollars.** **Discounting is what makes them addable.**
>
> **And the overstatement grows with the interest rate:**
>
> | $i$ | PV | % of headline |
> |---|---|---|
> | 2% | \$16.68m | 83.4% |
> | 5% | \$13.09m | 65.4% |
> | **10%** | **\$9.36m** | **46.8%** |
> | 15% | \$7.20m | 36.0% |

### 2. Yield to maturity — and the four instruments

$$\textbf{YTM}=\text{the rate equating the PV of an instrument's cash flows with its price today}$$

**This is what economists *mean* by "the interest rate".** *(Mishkin's footnote: in other contexts it is called the **internal rate of return** — the same apparatus as [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s NPV.)*

| instrument | cash flows | YTM |
|---|---|---|
| **simple loan** | principal + interest at maturity | $PV=CF/(1+i)^n$ |
| **fixed-payment loan** | equal payment every period | $LV=\sum_{t=1}^{n} FP/(1+i)^t$ |
| **coupon bond** | $C$ each year, then $F$ | $P=\sum_{t=1}^{n} C/(1+i)^t+F/(1+i)^n$ |
| **discount bond** | $F$ at maturity only | $i=(F-P)/P$ *(one year)* |
| **perpetuity / consol** | $C$ forever | $P_c=C/i_c$ |

> [!note] All of Mishkin's worked figures verified
> - **Simple loan** — borrow \$100, repay \$110: $i=10\%$. ✓ **For a simple loan the simple interest rate *equals* the YTM — and this is the only instrument for which that is true.**
> - **Fixed-payment loan** — \$1,000 over 25 years at 7% ⇒ **\$85.81** ✓; and inverting, \$85.81 recovers **7.0000%** ✓.
> - **Mortgage** — \$100,000, 20 years, 7% ⇒ **\$9,439.29** ✓. *(Computed: the borrower pays **\$188,785.85** in total — **89% of the principal again in interest**.)*
> - **Coupon bond** — 10% coupon, \$1,000 face, 8 years, 12.25% YTM ⇒ **\$889.20** ✓.
> - **Discount bond** — \$1,000 bill at \$900 ⇒ **11.1%** ✓; at \$950 ⇒ **5.3%** ✓.
> - **Perpetuity** — \$100 a year at price \$2,000 ⇒ **5%** ✓; \$100 forever at 10% prices at \$1,000, at 20% at \$500.
>
> *(One trap: Mishkin's **\$126 a year on \$1,000 for 25 years** illustrates the *instrument*, not the 7% rate — **it implies 11.83%**. Do not conflate the two examples.)*

### 3. Table 1 and the three facts

*(Verified — a 10%-coupon, \$1,000-face, ten-year bond:)*

| price | YTM computed | Mishkin |
|---|---|---|
| \$1,200 | **7.1347%** | 7.13% ✓ |
| \$1,100 | **8.4775%** | 8.48% ✓ |
| **\$1,000** | **10.0000%** | 10.00% ✓ |
| \$900 | **11.7519%** | 11.75% ✓ |
| \$800 | **13.8052%** | 13.81% ✓ |

1. **At par, YTM = coupon rate** — *exactly*, not approximately.
2. **Price and YTM move oppositely.**
3. **Below par ⇒ YTM > coupon rate; above par ⇒ YTM < coupon rate.**

> [!warning] Fact 2 is not an empirical regularity — it is algebra
> **$i$ appears only in denominators of the pricing equation.** Raising it lowers every term. **There is no configuration of cash flows in which price and yield move together**, so this is not a tendency that might one day reverse.

### 4. ⚠️ How good is the current-yield approximation?

**Mishkin claims $i_c=C/P$ approximates the YTM well "when a coupon bond has a long term to maturity (say, 20 years or more)".** He asserts it and moves on. *(Tested — the error $|i_c-\text{YTM}|$ in percentage points, 10% coupon bond:)*

| price | $i_c$ | $n=1$ | $n=5$ | $n=10$ | $n=20$ | $n=50$ |
|---|---|---|---|---|---|---|
| \$1,200 | 8.33% | **16.667** | 2.996 | 1.199 | 0.366 | 0.026 |
| \$1,100 | 9.09% | 9.091 | 1.564 | 0.613 | 0.179 | 0.011 |
| \$900 | 11.11% | 11.111 | 1.720 | 0.641 | 0.168 | 0.006 |
| \$800 | 12.50% | **25.000** | 3.626 | 1.305 | 0.316 | 0.009 |

> [!warning] The claim is correct, and the arithmetic sharpens it into a rule
> **The error falls monotonically with maturity** — under 0.4 points at 20 years, hundredths of a point at 50. **Mishkin's "20 years or more" is well chosen.**
>
> **⚠️ But at short maturities it is not an approximation, it is a mistake.** At $n=1$ and a price of \$800 the current yield says **12.50%** while the true yield is **37.50%** — an error of **25 percentage points**, larger than the number itself.
>
> **And the error is worse the further the price is from par ⇒ the approximation works best exactly when it is least needed.** *(A deeply discounted short bond is where you most want a quick yield and least may take one.)*

### 5. ⚠️ Interest rate versus return — Irving the Investor

$$R=\frac{C+P_{t+1}-P_t}{P_t}=\underbrace{\frac{C}{P_t}}_{i_c\ \text{current yield}}+\underbrace{\frac{P_{t+1}-P_t}{P_t}}_{g\ \text{rate of capital gain}}$$

*(Worked case verified: buy at \$1,000, 10% coupon, sell at \$1,200 ⇒ $R=(100+200)/1000=\mathbf{30\%}$ — **while the YTM was 10%.**)*

**⚠️ Table 2 — one-year returns when rates rise 10% → 20%.** *(All figures verified against Mishkin. Every bond is a 10%-coupon bond bought at par; **next year's price is that of a bond with one fewer year to run, discounted at the new 20%**.)*

| yrs to maturity | price next year | Mishkin | capital gain $g$ | **return $R=i_c+g$** | Mishkin |
|---|---|---|---|---|---|
| **30** | \$502.53 | \$503 ✓ | **−49.75%** | **−39.75%** | −39.7 ✓ |
| **20** | \$515.65 | \$516 ✓ | −48.43% | −38.43% | −38.4 ✓ |
| 10 | \$596.90 | \$597 ✓ | −40.31% | −30.31% | −30.3 ✓ |
| 5 | \$741.13 | \$741 ✓ | −25.89% | −15.89% | −15.9 ✓ |
| 2 | \$916.67 | \$917 ✓ | −8.33% | **+1.67%** | +1.7 ✓ |
| **1** | \$1,000.00 | \$1,000 ✓ | 0.00% | **+10.00%** | +10.0 ✓ |

- **The only bond whose return equals its YTM is the one whose maturity equals the holding period.** *(The one-year bond: its price at the horizon is fixed at face value, so no rate change can touch it.)*
- **Every longer bond takes a capital loss**, and **the loss grows with maturity**.
- **⚠️ A 10% bond returned −39.75%.** The coupon does not come close to covering the capital loss.

> [!note] The same table with rates *falling* — Mishkin does not run it
> *(Computed, 10% → 5%:)*
>
> | yrs | price next year | $g$ | $R$ |
> |---|---|---|---|
> | **30** | \$1,757.05 | **+75.71%** | **+85.71%** |
> | 20 | \$1,604.27 | +60.43% | +70.43% |
> | 10 | \$1,355.39 | +35.54% | +45.54% |
> | 5 | \$1,177.30 | +17.73% | +27.73% |
> | 1 | \$1,000.00 | 0.00% | +10.00% |
>
> **The one-year bond returns 10% whatever happens.** **The thirty-year bond ranges from −39.75% to +85.71%.** **⚠️ A long bond is a leveraged bet on interest rates, and calling it a "safe fixed-income asset" is a category error** — the *coupon* is fixed, the *return* is not.

### 6. ⚠️ Maturity is the wrong metric — duration, and the appendix that is not in the book

> [!warning] Mishkin's footnote 4 sends duration off-book
> **"Interest-rate risk can be quantitatively measured using the concept of duration… discussed in an appendix to this chapter, which can be found at [the publisher's website]."** **So the quantitative treatment is not in the book at all.** *(This vault already has it — [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|Commercial Banking ch. 05]] built duration and ch. 07 used it. What follows is that machinery applied to Mishkin's own table.)*

**Two things fall out, and the first is a genuine gap in Mishkin's explanation.**

**(a) Duration explains the *shape* of Table 2, which maturity cannot.**

*(Computed — Macaulay duration of a 10%-coupon par bond at 10%:)*

| maturity $n$ | **Macaulay $D$** | modified $D$ | Table 2's loss |
|---|---|---|---|
| **30** | **10.3696** | 9.4269 | −49.75% |
| **20** | **9.3649** | 8.5136 | −48.43% |
| 10 | 6.7590 | 6.1446 | −40.31% |
| 5 | 4.1699 | 3.7908 | −25.89% |
| 2 | 1.9091 | 1.7355 | −8.33% |

> [!warning] ⚠️ Why 30 years and 20 years lose almost the same amount
> **Mishkin's table shows the 30-year and 20-year bonds losing 49.75% and 48.43% — nearly identical, despite ten years' difference in maturity — while 5 years and 2 years differ by seventeen points.** **His prose says only "the more distant the maturity, the greater the change", which is true and does not explain the spacing.**
>
> **Duration does. The 30-year bond's duration is 10.37 years and the 20-year bond's is 9.36 — barely one year apart**, because at a 10% coupon almost all the present value sits in the near coupons and the distant face value is discounted to nearly nothing. *(At 10%, \$1,000 thirty years out is worth \$57.31.)*
>
> **⚠️ So maturity is the wrong metric. Duration is the right one, and it is the reason the table's rows bunch at the top and spread at the bottom.** **This is also why [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|CB ch. 05]] manages a bank's rate risk with duration rather than maturity** — the two orderings agree, the two *spacings* do not.

**(b) ⚠️ And duration fails at this shock — which is the vault's verification rule #1, again.**

*(Computed — instantaneous repricing when rates jump 10% → 20%:)*

| $n$ | duration predicts | **exact repricing** | error |
|---|---|---|---|
| **30** | **−94.27%** | **−49.79%** | **−44.48 pts** |
| 20 | −85.14% | −48.70% | −36.44 pts |
| 10 | −61.45% | −41.92% | −19.52 pts |
| 5 | −37.91% | −29.91% | −8.00 pts |
| 1 | −9.09% | −8.33% | −0.76 pts |

> [!warning] The error as a function of shock size — 30-year bond
> | shock | duration says | exact | error | error as % of true |
> |---|---|---|---|---|
> | +1 bp | −0.0943% | −0.0942% | 0.0001 | **0.08%** |
> | +10 bp | −0.9427% | −0.9349% | 0.0078 | 0.84% |
> | +100 bp | −9.4269% | −8.6938% | 0.7331 | 8.43% |
> | +200 bp | −18.8538% | −16.1104% | 2.7435 | 17.03% |
> | +500 bp | −47.1346% | −32.8299% | 14.3047 | 43.57% |
> | **+1000 bp** | **−94.2691%** | **−49.7894%** | **44.4798** | **89.34%** |
>
> **⚠️ At Mishkin's own 10-point shock, duration says the 30-year bond is very nearly wiped out; it in fact halves.**
>
> **Why: duration is the *first* derivative, and price is convex in the yield**, so the true loss is always *smaller* than the linear prediction. **At one basis point the error is invisible (0.08%); at a thousand it is 89% of the answer.**
>
> **⚠️ This is [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|Commercial Banking ch. 05]]'s finding (error 0.0000% at 1 bp → 2.5823% at a 5-point shock) pushed to a 10-point shock, and it lands in the same place: a first-order measure reports success precisely when the risk it leaves out is the one that matters.** **The vault's rule — *verify against something independent of the model that produced the number* — is what makes Table 2 valuable here: it is an exact repricing, so it can referee duration.**

### 7. Reinvestment risk — the exposure that runs the other way

**Interest-rate risk is for a bond *longer* than your horizon. Reinvestment risk is for one *shorter*.** *(Mishkin's footnote 6: Irving has a two-year horizon and buys one-year bonds. \$1,000 at 10% ⇒ \$1,100 after a year, then reinvested at the new rate.)*

| reinvestment rate | value at year 2 | two-year return |
|---|---|---|
| **20%** (rates rise) | \$1,320 | **+32.0%** ✓ |
| **5%** (rates fall) | \$1,155 | **+15.5%** ✓ |

> [!warning] ⚠️ So the sign of your exposure depends on your horizon, not on the bond
> **Bond longer than horizon ⇒ you lose when rates rise.** **Bond shorter than horizon ⇒ you *gain* when rates rise.** **⚠️ "Long bonds are risky" is therefore not a property of long bonds** — it is a statement about an investor whose horizon is short, and it reverses for a pension fund with thirty-year liabilities. *(This is precisely why [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|CB ch. 05]] matches the duration of assets to that of **liabilities** rather than minimising duration.)*

> [!warning] ⚠️ ERRATUM — Mishkin footnote 6, p. 129
> The book writes the 5% case as **"($1,555 − \$1,000)/1,000 = 0.155 = 15.5%"**. **But \$1,555 − \$1,000 = \$555, which is 55.5%, not 15.5%.** **The line immediately before it correctly computes \$1,100 × 1.05 = \$1,155**, so **\$1,555 is a slip for \$1,155 and the stated answer 15.5% is correct.**
>
> *(Ruled out per the vault's rule 4: my extraction — **both figures appear one line apart**; my arithmetic — verified; an abridged table — not a table; an alternative convention — **none produces \$1,555.**)* **Filed. The conclusion is unharmed.**

> [!note] A second discrepancy in the same footnote — investigated and NOT filed
> **The two annualisations use different conventions.** *(Computed: 32% over two years is **14.89% geometric** / 13.88% continuous — the book says **14.9%**. But 15.5% over two years is **7.47% geometric** / **7.21% continuous** — the book says **7.2%**.)*
>
> **So 14.9% is the geometric annualisation and 7.2% is the continuous one.** **Each is defensible alone; using both in one footnote is not** — but **neither number is *wrong* under its own convention**, and rule 4 says rule out alternative conventions before filing. **Not filed.**
>
> **⚠️ The lesson survives the non-filing: "at an annual rate" is not a well-defined instruction until you say *which* annualisation.**

### 8. Real versus nominal — the Fisher equation

$$i=r+\pi^e\qquad\Longleftrightarrow\qquad r=i-\pi^e$$

| | |
|---|---|
| **nominal rate** | what the contract says |
| **ex ante real rate** | adjusted for **expected** inflation — **what drives decisions** |
| **ex post real rate** | adjusted for **actual** inflation — how the lender *did* |

*(Verified: $i=5\%,\pi^e=3\%\Rightarrow r=2\%$; $i=8\%,\pi^e=10\%\Rightarrow r=-2\%$.)*

> [!warning] A negative real rate is not a curiosity
> **The lender loses purchasing power and the borrower gains it, and nothing in the contract has to change.** **When the real rate is low there are greater incentives to borrow and fewer to lend** — which is why the *real* rate, not the nominal one, indicates whether credit conditions are tight. *(Mishkin's Figure 1: **US nominal rates were high in the 1970s while real rates were often negative.** Judging by nominal rates you would have called credit tight; you would have been wrong.)*

> [!note] ⚠️ How small is "small"? — the exact Fisher equation
> **Exactly, $(1+i)=(1+r)(1+\pi^e)$, so $i=r+\pi^e+r\pi^e$.** Mishkin drops the cross term. *(Computed, solving for $r$:)*
>
> | $i$ | $\pi^e$ | approx $r$ | **exact $r$** | error |
> |---|---|---|---|---|
> | 5% | 3% | 2.00% | 1.94% | +0.06 |
> | 10% | 5% | 5.00% | 4.76% | +0.24 |
> | 30% | 25% | 5.00% | 4.00% | +1.00 |
> | 80% | 75% | 5.00% | 2.86% | +2.14 |
> | **200%** | **190%** | **10.00%** | **3.45%** | **+6.55** |
>
> **The approximation is excellent at ordinary rates and breaks under high inflation** — **and high inflation is exactly when people reach for the Fisher equation.** *([[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s hyperinflation cases are precisely where $i-\pi^e$ stops being usable.)*

> [!warning] ⚠️ After-tax real rates — Mishkin's footnote 8, and the sharpest result in it
> $$r_{\text{after tax}}=i(1-t)-\pi^e$$
>
> | $i$ | $t$ | after-tax nominal | $\pi^e$ | **after-tax real** | Fisher real |
> |---|---|---|---|---|---|
> | 10% | 30% | 7.0% | 5% | **2.00%** | 5.00% |
> | **10%** | **30%** | **7.0%** | **8%** | **−1.00%** | **2.00%** |
> | 15% | 40% | 9.0% | 10% | −1.00% | 5.00% |
>
> **The gap is $i\cdot t$ — it *grows with the nominal rate*.** **⚠️ So inflation raises the tax burden on saving even at an unchanged tax rate**, because the tax is levied on the *nominal* return, **part of which is not income at all but compensation for the erosion of the principal.**
>
> **Row 2 is the killer: a 10% bond, a 30% taxpayer, 8% inflation ⇒ the saver is running at −1.00% while the headline says 10%.**

### 9. ⚠️ Four numbers, four questions

| measure | formula | what it answers | known |
|---|---|---|---|
| **yield to maturity** $i$ | PV of cash flows = price | *what rate does this instrument embed?* | **at purchase** |
| **current yield** $i_c$ | $C/P$ | an approximation to the YTM — **long maturities only** | at purchase |
| **rate of capital gain** $g$ | $(P_{t+1}-P_t)/P_t$ | *what did the price do?* | afterwards |
| **rate of return** $R$ | $i_c+g$ | ***how did I actually do?*** | **afterwards** |

> [!warning] ⚠️ $R=i$ only when maturity equals the holding period
> **In every other case they differ, and Table 2 shows the gap reaching fifty percentage points.**
>
> **⚠️ This is [[01 - The Financial System and What Money Is|ch. 01]]'s lesson in a second setting.** There the question was *which M?*; **here it is *which interest rate?*** **Both times: a number's name does not tell you which question it answers, and the damage is done by people who assume it does.** **Irving the Investor knew his bond's interest rate exactly and lost 39.7%.**

## ✏️ Exercises

**1. (Present value.)** (a) A lottery advertises \$20 million as \$1 million a year for twenty years, first payment today. At 10%, what is it worth? (b) Why is the advertised figure not merely optimistic but *ill-formed*? (c) What happens as the interest rate rises?

> [!example]- Solution
> **(a) \$9.36 million — under half.**
>
> $$PV=\sum_{t=0}^{19}\frac{1}{(1.10)^t}=\mathbf{\$9.36\text{ million}}$$
>
> **The first payment is worth its full \$1 million** *(it arrives today)*; **the second is worth \$909,090 and the third \$826,446** *(both verified against Mishkin's own figures)*, and the twentieth is worth \$163,508. **Mishkin gives \$9.4 million; the exact figure is \$9.3649 million.**
>
> *(Note the annuity is **due**, not ordinary — the first payment is immediate. Treating it as an ordinary annuity gives \$8.51m and does not match the book, which is how you know the convention.)*
>
> **(b) Because adding cash flows across time is not a permitted operation.**
>
> **The "\$20 million" is a sum of twenty quantities that are not commensurable** — a dollar in year 19 and a dollar today are different goods, exactly as **a 1990 dollar and a 2020 dollar are different goods ([[Macroeconomics & Microeconomics/contents/08 - Measuring the Macroeconomy - GDP and the Cost of Living|Macro/Micro ch. 08]])**.
>
> **So the error is not that the advertiser was too cheerful; it is that the arithmetic was invalid before any judgement entered.** **Discounting is precisely the operation that converts the twenty amounts into a common unit so that they *may* be added.** *(This is the same discipline as deflating a nominal series before comparing years — and it is the single most transferable idea in the chapter.)*
>
> **(c) The overstatement grows.**
>
> | $i$ | PV | % of headline |
> |---|---|---|
> | 2% | \$16.68m | 83.4% |
> | 5% | \$13.09m | 65.4% |
> | 10% | \$9.36m | 46.8% |
> | 15% | \$7.20m | **36.0%** |
>
> **The headline is a valid number only at a zero interest rate.** **The higher the rate, the more of the "prize" is fiction** — which is worth knowing in the direction it runs: **advertising undiscounted totals is most misleading exactly when money is most expensive.**

**2. (Yield to maturity.)** (a) Verify Mishkin's Table 1 and state the three facts. (b) Show fact 2 is algebra, not observation. (c) A \$100,000 mortgage at 7% over 20 years — what is the payment and what is the total interest?

> [!example]- Solution
> **(a) All five verify.**
>
> | price | YTM | Mishkin |
> |---|---|---|
> | \$1,200 | 7.1347% | 7.13% ✓ |
> | \$1,100 | 8.4775% | 8.48% ✓ |
> | \$1,000 | **10.0000%** | 10.00% ✓ |
> | \$900 | 11.7519% | 11.75% ✓ |
> | \$800 | 13.8052% | 13.81% ✓ |
>
> 1. **At par the YTM equals the coupon rate — exactly.** *(Intuition: buying a \$1,000 bond with a \$100 coupon is the same transaction as putting \$1,000 in an account paying 10% and withdrawing \$100 a year.)*
> 2. **Price and yield move oppositely.**
> 3. **Below par ⇒ YTM above the coupon rate; above par ⇒ below it.** *(Fact 3 follows from 1 and 2 together; it is not independent.)*
>
> **(b) Because $i$ appears only in denominators.**
>
> $$P=\frac{C}{1+i}+\frac{C}{(1+i)^2}+\cdots+\frac{C+F}{(1+i)^n}$$
>
> **Every term is strictly decreasing in $i$, so $P$ is strictly decreasing in $i$.** *(Formally $dP/di<0$ term by term, with no cancellation possible since all cash flows are positive.)*
>
> **⚠️ Why this matters: it means the relationship cannot break.** **An empirical regularity might reverse under new conditions; this one is a property of the definition of price.** **Any observation of price and yield rising together is a measurement error, a change in the cash flows, or a different bond** — never a counterexample. *(This is the same class of certainty as an accounting identity, and it should be reasoned about the same way: identities constrain, they do not explain.)*
>
> **(c) \$9,439.29 a year; \$88,785.85 of interest.**
>
> $$FP=\frac{LV\cdot i}{1-(1+i)^{-n}}=\frac{100{,}000\times0.07}{1-(1.07)^{-20}}=\mathbf{\$9{,}439.29}$$
>
> ✓ against Mishkin. **Total paid = 20 × \$9,439.29 = \$188,785.85, so interest = \$88,785.85 — 89% of the principal paid again.**
>
> **⚠️ And note what that figure is *not*: it is not a measure of how bad the deal is.** **The \$88,785.85 is spread over twenty years and is not discounted** — **so quoting it is the lottery error in reverse**, adding non-commensurable amounts to produce an alarming total. **By construction the PV of the twenty payments is exactly \$100,000**, which is what "a 7% loan" means. *(Both errors come from the same place: treating dated money as dateless.)*

**3. (Hard — interest-rate risk.)** (a) Reproduce Mishkin's Table 2. (b) Which bond is riskless here, and why? (c) Run the same table for rates *falling* to 5% and say what the pair shows.

> [!example]- Solution
> **(a) Every figure reproduces.** *(10% coupon bonds bought at par; next year's price is that of a bond with one fewer year to run, discounted at the new 20%.)*
>
> | yrs | price next year | Mishkin | $g$ | $R=i_c+g$ | Mishkin |
> |---|---|---|---|---|---|
> | 30 | \$502.53 | 503 ✓ | −49.75% | **−39.75%** | −39.7 ✓ |
> | 20 | \$515.65 | 516 ✓ | −48.43% | −38.43% | −38.4 ✓ |
> | 10 | \$596.90 | 597 ✓ | −40.31% | −30.31% | −30.3 ✓ |
> | 5 | \$741.13 | 741 ✓ | −25.89% | −15.89% | −15.9 ✓ |
> | 2 | \$916.67 | 917 ✓ | −8.33% | +1.67% | +1.7 ✓ |
> | 1 | \$1,000.00 | 1,000 ✓ | 0.00% | +10.00% | +10.0 ✓ |
>
> **A 10% bond returned −39.75% in a year.**
>
> **(b) The one-year bond — and the reason is structural, not statistical.**
>
> **Its price at the end of the holding period is already fixed at face value.** **A change in interest rates cannot touch a payment that is contractually \$1,000 on that date**, so the return equals the YTM, **and the YTM was known at purchase.**
>
> **⚠️ The condition is *maturity = holding period*, not "short bond".** **A one-year bond is riskless to a one-year investor and risky to a two-year one** *(§7's reinvestment risk)*. *(Mishkin's footnote 5 adds the honest qualification: strictly this holds for **zero-coupon** bonds, since a coupon bond's intermediate payments must be reinvested at an unknown rate — the effect is small but it is not zero.)*
>
> **(c) The pair shows a long bond is a leveraged bet, not a safe asset.**
>
> | yrs | rates → 20% | rates → 5% |
> |---|---|---|
> | **30** | **−39.75%** | **+85.71%** |
> | 10 | −30.31% | +45.54% |
> | 5 | −15.89% | +27.73% |
> | **1** | **+10.00%** | **+10.00%** |
>
> **The one-year bond returns 10% either way. The thirty-year bond spans 125 percentage points.**
>
> **⚠️ So "fixed income" names the *coupon*, not the return**, and calling long bonds safe is a category error. **A 30-year Treasury has no default risk and enormous price risk**, and the two are entirely different questions — **which is exactly why [[04 - The Risk and Term Structure of Interest Rates|ch. 04]] separates the *risk structure* from the *term structure*.**
>
> *(This also explains a fact about institutions: [[Commercial Banking/contents/07 - The Investment Portfolio|CB ch. 07]] found banks holding short securities and giving up 3.75 points of yield. **This table is the price of that yield** — the give-up buys the bottom row of the left column instead of the top.)*

**4. (Hard — duration.)** (a) Mishkin's Table 2 shows 30-year and 20-year bonds losing almost the same amount while 5-year and 2-year bonds differ sharply. His prose cannot explain this. Can you? (b) Does duration predict the table's numbers? (c) What rule does (b) confirm?

> [!example]- Solution
> **(a) Yes — duration, which Mishkin sends to an appendix that is not in the book.**
>
> *(Computed, 10%-coupon par bonds at 10%:)*
>
> | maturity | **Macaulay $D$** | Table 2's loss |
> |---|---|---|
> | 30 | **10.3696** | −49.75% |
> | 20 | **9.3649** | −48.43% |
> | 10 | 6.7590 | −40.31% |
> | 5 | 4.1699 | −25.89% |
> | 2 | 1.9091 | −8.33% |
>
> **Maturities 30 and 20 differ by ten years; their durations differ by one.** **That is why their losses differ by 1.3 points.** **Maturities 5 and 2 differ by three years and their durations by 2.26 — so their losses differ by 17.6 points.**
>
> **Why: duration is the PV-weighted average time to a cash flow.** At a 10% coupon, **the face value thirty years out is worth only \$57.31 today**, so extending maturity from 20 to 30 adds ten years of small, heavily-discounted coupons and barely moves the centre of mass. **⚠️ Maturity counts the last payment; duration weights all of them.**
>
> **Mishkin's statement "the more distant the maturity, the greater the change" is true and gives the *ordering* only.** **Duration gives the *spacing*, and the spacing is what a risk manager needs** — which is why [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|CB ch. 05]] runs on duration and not maturity.
>
> **(b) It predicts the ordering and gets the magnitudes badly wrong.**
>
> | $n$ | duration says | **exact** | error |
> |---|---|---|---|
> | 30 | **−94.27%** | **−49.79%** | −44.48 pts |
> | 20 | −85.14% | −48.70% | −36.44 pts |
> | 10 | −61.45% | −41.92% | −19.52 pts |
> | 5 | −37.91% | −29.91% | −8.00 pts |
> | 1 | −9.09% | −8.33% | −0.76 pts |
>
> **Duration says the 30-year bond is nearly wiped out. It halves.**
>
> **Because duration is the *first* derivative and price is *convex* in the yield**, the linear prediction always overstates a loss and understates a gain. **The error scales with the square of the shock:**
>
> | shock | error as % of the true loss |
> |---|---|
> | +1 bp | **0.08%** |
> | +100 bp | 8.43% |
> | +500 bp | 43.57% |
> | **+1000 bp** | **89.34%** |
>
> **(c) The vault's first verification rule: a self-consistent calculation is not a verified one.**
>
> **Duration checked against duration is always perfect.** **The only reason we can see it failing here is that Mishkin's Table 2 is an *exact repricing* — a number produced by different machinery.** *(This is the same structure as [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|CB ch. 05]]'s duration hedge, which showed a ±1 residual under its own formula and lost 1.46% of equity at +2% and 7.81% at +5% under exact repricing.)*
>
> **⚠️ And the general form is worth stating carefully: a first-order measure reports success precisely when the exposure it omits is second-order.** **It is not that duration is unreliable — it is *exactly* right in the limit and its error is 0.08% at a basis point.** **The failure mode is using it where its assumption has quietly stopped holding**, and **nothing in the output announces that**, which is the same shape as the vault's technical finding that the expensive bugs produce plausible wrong answers with no error.

**5. (Real rates.)** (a) State the Fisher equation and compute two cases. (b) When does the approximation break? (c) Add taxes — what does inflation do to a saver at an unchanged tax rate?

> [!example]- Solution
> **(a) $r=i-\pi^e$; and negative real rates are ordinary.**
>
> - $i=5\%$, $\pi^e=3\%$ ⇒ $r=2\%$ ✓ — **you expect 2% more in real goods.**
> - $i=8\%$, $\pi^e=10\%$ ⇒ $r=-2\%$ ✓ — **you receive 8% more dollars and pay 10% more for goods, so you can buy 2% *less*.**
>
> **The lender loses purchasing power and the borrower gains it, with nothing in the contract changing.** **⚠️ And the ex ante / ex post distinction matters: decisions are made on *expected* inflation, outcomes are settled by *actual* inflation, and unexpected inflation is a pure transfer from lender to borrower.**
>
> *(Mishkin's Figure 1 is the payoff: **US nominal rates were high in the 1970s while real rates were often negative.** Judging tightness by nominal rates would have had you calling credit expensive during the cheapest borrowing conditions of the post-war period.)*
>
> **(b) At high inflation — which is exactly when it gets used.**
>
> **Exactly, $(1+i)=(1+r)(1+\pi^e)$, so $i=r+\pi^e+r\pi^e$; Mishkin drops the cross term.**
>
> | $i$ | $\pi^e$ | approx | **exact** | error |
> |---|---|---|---|---|
> | 5% | 3% | 2.00% | 1.94% | 0.06 |
> | 10% | 5% | 5.00% | 4.76% | 0.24 |
> | 30% | 25% | 5.00% | 4.00% | 1.00 |
> | **200%** | **190%** | **10.00%** | **3.45%** | **6.55** |
>
> **At ordinary rates the error is hundredths of a point and the approximation is entirely safe.** **At 190% expected inflation the subtraction overstates the real rate by 6.55 points — nearly three times the truth.**
>
> **⚠️ Same shape as exercise 4: an approximation that is excellent in its domain, silently wrong outside it, and reached for most eagerly at the moment it stops working.** *([[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s hyperinflations are exactly that region.)*
>
> **(c) Inflation raises the tax burden on saving even with the tax rate held fixed.**
>
> $$r_{\text{after tax}}=i(1-t)-\pi^e$$
>
> | $i$ | $t$ | $\pi^e$ | **after-tax real** | Fisher real | gap |
> |---|---|---|---|---|---|
> | 10% | 30% | 5% | 2.00% | 5.00% | 3.00 |
> | **10%** | **30%** | **8%** | **−1.00%** | 2.00% | 3.00 |
> | 15% | 40% | 10% | −1.00% | 5.00% | 6.00 |
>
> **The gap is $i\cdot t$, so it grows with the nominal rate.** **⚠️ And the nominal rate rises with expected inflation (that is the Fisher equation) — so inflation mechanically widens the wedge without any legislature acting.**
>
> **The reason is that tax is levied on the *nominal* return, part of which is not income at all but compensation for the erosion of the principal.** **The saver is taxed on maintaining their position.**
>
> **Row 2 is the case worth remembering: a 10% bond, a 30% taxpayer, 8% inflation ⇒ the saver runs at −1.00% while the headline says 10%.** *(And symmetrically, deductible interest makes the effective cost of borrowing $i(1-t)-\pi^e$ too — so the same distortion **subsidises** debt. That asymmetry is a standing argument for indexing the tax base, and it is why [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] lists inflation-induced tax distortions among the costs of inflation.)*

## 📝 Summary

- **Present value, $PV=CF/(1+i)^n$, is the whole chapter.** Everything else is this equation applied to different cash-flow patterns.
- **⚠️ Adding cash flows across time is not a permitted operation** — the lottery's "\$20 million" is worth **\$9.36m** *(verified)*, **46.8% of the headline**, and less still at higher rates.
- **Yield to maturity is what economists mean by "the interest rate"**: the rate equating the PV of cash flows to the price. **Four instruments, one idea.**
- **All of Mishkin's worked figures verify** — \$189.04, \$909,090, \$826,446, \$85.81, \$9,439.29, \$889.20, 11.1%, 5%, and **all five rows of Table 1**.
- **Three facts: at par YTM = coupon rate exactly; price and yield move oppositely; below par YTM exceeds the coupon rate.** **⚠️ Fact 2 is algebra, not observation** — $i$ appears only in denominators.
- **The current-yield approximation is good only at long maturity** *(computed: error **0.366 pts at n=20** but **25 pts at n=1** for a bond at \$800)* — **and it is worst furthest from par, so it works best when least needed.**
- **⚠️ $R=i_c+g$, and $R=i$ only when maturity equals the holding period.** Table 2 verified in full: **a 10% bond returned −39.75%.**
- **⚠️ Run the table the other way and the 30-year bond returns +85.71%** — **a long bond is a leveraged bet on rates; "fixed income" names the coupon, not the return.**
- **⚠️ Maturity is the wrong metric — duration is the right one** *(computed: 30-year and 20-year bonds have durations **10.37 and 9.36**, one year apart, which is why their losses are 49.75% and 48.43%)*. **Mishkin's prose gives the ordering; only duration gives the spacing.**
- **⚠️ And duration itself fails at this shock** *(computed: predicts **−94.27%** where exact repricing gives **−49.79%**)*. **Error 0.08% at 1 bp → 89.34% at 1000 bp.** **A first-order measure reports success precisely when the omitted risk is the one that matters.**
- **Reinvestment risk runs the opposite way** — a bond *shorter* than your horizon **gains** when rates rise. **⚠️ The sign of your exposure is set by your horizon, not by the bond.**
- **⚠️ Erratum filed:** footnote 6's **\$1,555 should be \$1,155** *(the answer 15.5% is correct)*. **A second discrepancy — two different annualisation conventions in one footnote — investigated and not filed.**
- **Fisher: $r=i-\pi^e$.** **Negative real rates are ordinary**, and the **real** rate, not the nominal one, indicates whether credit is tight — **US nominal rates were high in the 1970s while real rates were negative.**
- **⚠️ The approximation breaks under high inflation** *(computed: **6.55 points** of error at $\pi^e=190\%$)* — **exactly the regime in which it gets used.**
- **⚠️ After tax, $r=i(1-t)-\pi^e$ and the wedge $i\cdot t$ grows with inflation** — **a 10% bond, a 30% taxpayer and 8% inflation leave the saver at −1.00%.**
- **Four numbers, four questions.** **A number's name does not tell you which question it answers** — [[01 - The Financial System and What Money Is|ch. 01]]'s "which M?" in a second setting.

## ⚠️ Important Notes

1. **Never add undiscounted cash flows from different dates.** The lottery headline and "total interest paid on a mortgage" are the same error in opposite directions.
2. **For a simple loan only, the simple interest rate equals the YTM.** For every other instrument they differ.
3. **⚠️ At par — and only at par — the YTM equals the coupon rate.** This is the anchor for all three of Table 1's facts.
4. **Price and yield move oppositely as a matter of algebra.** An apparent counterexample is a measurement error or a different bond.
5. **The current yield is a long-maturity approximation.** At $n=1$ it can be off by 25 points; do not use it on short paper.
6. **⚠️ The approximation is worst furthest from par** — worst precisely where a quick estimate is most tempting.
7. **⚠️ Return ≠ interest rate.** The YTM is known at purchase and describes the *instrument*; the return is known afterwards and describes *you*.
8. **The only riskless case is maturity = holding period**, and strictly only for zero-coupon bonds *(Mishkin's own footnote 5)*.
9. **⚠️ "Long bonds are risky" is a statement about the investor, not the bond.** For a 30-year liability, a 30-year bond is the *safe* asset and cash is risky.
10. **⚠️ Maturity orders interest-rate risk; duration measures it.** Thirty years and twenty years are nearly the same bond in risk terms.
11. **⚠️ Duration is first-order.** Its error is 0.08% at one basis point and 89% at ten percentage points — **the failure is silent**.
12. **Convexity always favours the bondholder** — the true loss is smaller than the linear estimate and the true gain is larger.
13. **⚠️ Verify a model against machinery that did not produce it.** Table 2 can referee duration precisely because it is an exact repricing.
14. **Reinvestment risk is the mirror of interest-rate risk.** Both are horizon-relative.
15. **⚠️ Real ≠ nominal, and ex ante ≠ ex post.** Decisions run on expected inflation; unexpected inflation is a pure transfer to borrowers.
16. **The Fisher approximation drops $r\pi^e$** — safe at ordinary rates, unusable in hyperinflation.
17. **⚠️ Taxes are levied on nominal returns**, so inflation raises the effective tax on saving with no change in law.
18. **"At an annual rate" is undefined until you name the annualisation** — geometric and continuous differ, as Mishkin's own footnote demonstrates.

> [!warning] Gaps in the source material
> **Extraction was good.** The outline located ch. 4 at PDF pp. 115–136 exactly. **⚠️ The parenthesis fault recorded in [[00-Index]] appears throughout the displayed equations** — `$100 * 11 + 0.102 = $110` is $\$100\times(1+0.10)=\$110$, and `LV = FP/11 + i2 + ...` is $LV=\sum FP/(1+i)^t$. **Every formula in this note was reconstructed from the prose and then checked against one of Mishkin's own worked numbers**; **all of them reproduce**, which is what makes the reconstruction verified rather than assumed. *(Interestingly the fault is **inconsistent within this chapter** — some inline expressions such as `$250/(1 + 0.15)2 = $189.04` keep their parentheses and lose only the superscript. **So there is no mechanical decoder here either; the check against a worked number is the only reliable route.**)*
>
> **⚠️ Both tables survived extraction complete** — Table 1's five rows and Table 2's six rows with all six columns, **and every figure in both reproduces.** *(The vault's extraction rule holds for a third subject: **graphical exhibits are lost; numeric tables set as text survive whole**.)*
>
> **Figure 1 is lost** — the 1953–2017 series of real and nominal three-month Treasury bill rates. **This is a real loss**, since it is the chapter's only empirical evidence and it carries the claim that the two series diverge. **The claim is stated in §8 on Mishkin's authority and the accompanying prose, not reconstructed** — no data file exists in the vault, and **inventing a plausible-looking chart would be exactly the fabrication the vault's rules forbid.** *(The specific facts retained: nominal rates were high in the 1970s while estimated real rates were often negative; Mishkin's real-rate series is model-based, estimating expected inflation from past rates, inflation and time trends, so it is an **estimate and not an observation** — worth remembering before treating "the real interest rate" as data.)*
>
> **⚠️ Mishkin's duration appendix is not in the book** — footnote 4 sends the reader to the publisher's website. **§6 is therefore built on [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|Commercial Banking ch. 05]]'s duration machinery, which this vault already has**, applied to Mishkin's own bonds. **Flagged as an addition, not as recovered source material.**
>
> **⚠️ ERRATUM FILED — footnote 6, p. 129.** **"($1,555 − \$1,000)/1,000 = 0.155 = 15.5%"**: **\$1,555 − \$1,000 = \$555**, and the line immediately above correctly gives **\$1,100 × 1.05 = \$1,155**. **The \$1,555 is a slip for \$1,155; the stated 15.5% is correct.** *(Rule 4 applied: extraction ruled out — both figures appear one line apart; arithmetic verified; not an abridged table; no convention produces \$1,555.)*
>
> **⚠️ DISCREPANCY INVESTIGATED AND NOT FILED — same footnote.** *(Computed: 32% over two years annualises to **14.89% geometrically** and 13.88% continuously — the book says 14.9%. But 15.5% annualises to **7.47% geometrically** and **7.21% continuously** — the book says 7.2%.)* **So the footnote uses the geometric convention for one figure and the continuous convention for the other.** **Neither figure is wrong under its own convention**, and the vault's rule 4 requires ruling out alternative conventions before filing. **Not filed** — recorded because **the coexistence is itself the lesson.**
>
> **Additions beyond the source.**
>
> - **⚠️ §6 is the chapter's principal addition and its best result.** **Mishkin's Table 2 exhibits a pattern his prose cannot account for** — 30-year and 20-year bonds losing almost identically while 5-year and 2-year bonds differ by 17.6 points — **and the explanation is duration, which he removed from the book.** Computing it *(10.3696 vs 9.3649 years)* **turns his table from a list of numbers into an explained one**, and independently supplies the reason [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|CB ch. 05]] manages rate risk by duration rather than maturity.
> - **§6(b), the duration-versus-exact-repricing test, is mine**, and it uses Mishkin's Table 2 as the independent oracle. **The result (−94.27% predicted against −49.79% actual) confirms the vault's first verification rule in a fourth setting.**
> - **§4's quantification of the current-yield approximation is mine.** Mishkin asserts "20 years or more" without evidence; **the error table shows the claim is well judged and adds the two facts he omits — the error is catastrophic at short maturity and grows with distance from par.**
> - **§5's falling-rate table is mine** — Mishkin runs only the rate *rise*. **Running both is what shows the long bond is a leveraged bet rather than merely a risky one**, and it makes the "fixed income" misnomer visible.
> - **§8's exact-versus-approximate Fisher table and the after-tax table are mine**; Mishkin gives both formulas in footnotes without ever computing an error. **The finding that the tax wedge $i\cdot t$ grows with inflation at an unchanged statutory rate is the sharpest thing in the section and he does not state it.**
> - **§1's interest-rate sensitivity of the jackpot, and the connection to [[Macroeconomics & Microeconomics/contents/08 - Measuring the Macroeconomy - GDP and the Cost of Living|Macro/Micro ch. 08]]'s prohibition on adding dollars from different years, are mine.**
> - **§9's four-measures table and the identification of this chapter as [[01 - The Financial System and What Money Is|ch. 01]]'s "which M?" in a second setting is my synthesis.** **Mishkin distinguishes the measures carefully and never names the general hazard.**

**Previous:** [[01 - The Financial System and What Money Is]] · **Next:** [[03 - The Behavior of Interest Rates]]
