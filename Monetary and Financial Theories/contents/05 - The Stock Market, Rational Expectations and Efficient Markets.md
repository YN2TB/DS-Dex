---
subject: Monetary and Financial Theories
chapter: 5
tags: [ds, economics, stock-market, gordon-growth-model, rational-expectations, efficient-markets, behavioral-finance]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 7"
---

# The Stock Market, Rational Expectations and Efficient Markets

**Nothing new is needed to value equity — it is [[02 - The Meaning of Interest Rates|ch. 02]]'s present value applied to dividends.** **The chapter's real content is what happens when you *use* that formula, and what "the market has already priced it in" actually means.**

**Four results.**

**§3 — the Gordon model is a sensitivity amplifier, not a valuation tool.** *(Computed: Mishkin's three investors agree on **every cash flow** and differ only in required return, 15% vs 10% — and their valuations differ by **71.4%**. A **one-point** change in either input moves the price 10–12.5%, and the sensitivity **explodes** as $k_e\to g$: at $k_e=5\%$ a one-point cut **doubles** the price.)*

**§4 — what a 53% crash implies.** *(Computed: the DJIA's fall from 14,066 to 6,547 is **−53.46%** ✓, which requires the denominator $k_e-g$ to have **more than doubled** — a **4-to-9-point** move in a spread nobody can observe.)* **⚠️ The model has one equation and two unknowns, which is *why* the efficient-markets debate is unresolved.**

**§5 — why adaptive expectations are irrational, computed.** *(Every forecast error after a level shift has **the same sign for years**.)* **They fail not by being inaccurate but by being inaccurate *in a predictable direction*.**

**§7 — the football tipster, which Mishkin tells without arithmetic.** *(Computed: **1,024 marks manufacture exactly one perfect 10-for-10 record**; and in a population of **10,000 fund managers with no skill whatever, ~10 beat the market ten years running**.)*

## 📘 Main Knowledge

### 1. Valuing a stock — one principle, three models

$$\textbf{the value of any investment}=\text{the present value of the cash flows it generates}$$

**For equity the cash flows are dividends plus a final sale price** — **and equity is a *residual* claim ([[01 - The Financial System and What Money Is|ch. 01]]), so those flows are whatever is left after everyone else is paid.**

**(a) One-period model.**
$$P_0=\frac{D_1}{1+k_e}+\frac{P_1}{1+k_e}$$
*(Verified — Intel at \$50, $D_1=\$0.16$, forecast $P_1=\$60$, $k_e=12\%$: $P_0=\$0.1429+\$53.5714=\mathbf{\$53.7143}$; the book gives \$0.14 + \$53.57 = \$53.71.)*

> [!warning] ⚠️ \$53.71 is not a fact about Intel
> **The discount rate is the *required return on equity*, not an interest rate** — it is **your** compensation for **your** perceived risk. **Mishkin's own caveat: the market may price the stock at \$50 because other investors forecast lower cash flows *or apply a higher $k_e$*.** **So a valuation is a statement about the valuer as much as about the firm** — §3 shows just how much.

**(b) Generalised model — the final sale price drops out.**
$$P_0=\sum_{t=1}^{\infty}\frac{D_t}{(1+k_e)^t}$$
*(Mishkin's justification, verified: \$50 seventy-five years out at 12% is worth **\$0.0102** — "just one cent".)*

> [!note] But the "it doesn't matter" argument is rate-dependent
> *(Computed: \$50 in 75 years is worth **\$0.0102 at 12%** but **\$1.2876 at 5%** — a factor of 126.)* **The terminal value becomes negligible only if the discount rate is high enough.** **At today's low required returns, terminal values carry far more weight than the textbook demonstration suggests.**

> [!note] "But many stocks pay no dividends"
> **Mishkin: buyers expect the firm to pay them *someday* — usually once the rapid-growth phase ends.** **The model is not falsified by a zero *current* dividend, only by a zero *expected* one** *(in which case the stock is genuinely worthless under this theory, and whatever is supporting its price is not in the model)*.

**(c) Gordon growth model.** **Assume dividends grow at a constant $g$:**
$$\boxed{\ P_0=\frac{D_0(1+g)}{k_e-g}=\frac{D_1}{k_e-g}\ }$$

| assumption | |
|---|---|
| 1 | dividends grow at a constant rate **forever** — or long enough that the error is discounted away |
| **2** | **$g<k_e$** — otherwise the firm would grow impossibly large |

### 2. How the market sets prices

> [!note] The auto-auction lesson, in three parts
> 1. **The price is set by the buyer willing to pay the most — but lands only *incrementally above the second-highest bid*.** *(The Miata sells for \$5,100, not the winner's \$7,000 valuation.)* **The market price reveals the runner-up's valuation, not the winner's.**
> 2. **The asset goes to whoever can put it to best use.**
> 3. **⚠️ Superior information raises value by *reducing risk*** — the better-informed buyer discounts the *same* cash flows at a *lower* rate.

*(Mishkin's three investors, all verified — $D_1=\$2$, $g=3\%$:)*

| investor | $k_e$ | price |
|---|---|---|
| **You** (uncertain) | 15% | **\$16.67** ✓ |
| **Jennifer** (spoke to insiders) | 12% | **\$22.22** ✓ |
| **Bud** (dating the CEO) | 10% | **\$28.57** ✓ |

**The market price lands between \$22.22 and \$28.57, and if you hold the stock you sell it to Bud.**

> [!warning] ⚠️ What Mishkin does not say about his own example
> **The three investors agree on *every cash flow*. Same $D_1$, same $g$.** **They differ only in the risk they perceive — 15% against 10% — and their valuations differ by 71.4%.**
>
> **That is not a quirk of the chosen numbers. It is what the formula does, and §3 makes it general.**

### 3. ⚠️ The Gordon model is a sensitivity amplifier

$$P=\frac{D_1}{k_e-g}\qquad\Rightarrow\qquad \frac{\partial P}{\partial(k_e-g)}=-\frac{P}{k_e-g}$$

**$k_e$ and $g$ enter *only as a difference*, so a one-point error in one is exactly a one-point error in the other.** **⚠️ And the denominator is a difference of two largish numbers: it inherits both their errors and keeps none of their size.**

*(Computed, $D_1=\$2$:)*

| $k_e\backslash g$ | 0% | 2% | 4% | 6% | 8% | 10% |
|---|---|---|---|---|---|---|
| **8%** | 25.00 | 33.33 | 50.00 | **100.00** | — | — |
| **10%** | 20.00 | 25.00 | 33.33 | 50.00 | **100.00** | — |
| **12%** | 16.67 | 20.00 | 25.00 | 33.33 | 50.00 | **100.00** |
| **15%** | 13.33 | 15.38 | 18.18 | 22.22 | 28.57 | 40.00 |
| **20%** | 10.00 | 11.11 | 12.50 | 14.29 | 16.67 | 20.00 |

> [!warning] ⚠️ Read along any row
> **At $k_e=10\%$, raising $g$ from 0 to 8% takes the price from \$20.00 to \$100.00 — fivefold, from a forecast nobody can make with confidence.**
>
> **The dashes are where $g\ge k_e$. There the formula returns a *negative* price — not a low valuation but a broken one.** **⚠️ Assumption 2 is not a technicality; it is the boundary at which the model stops existing.**

*(Sensitivity computed exactly, from $k_e=12\%$, $g=3\%$, $P=\$22.22$:)*

| change | new price | change |
|---|---|---|
| $k_e$ **+1 point** | \$20.00 | **−10.0%** |
| $k_e$ **−1 point** | \$25.00 | **+12.5%** |
| $g$ +1 point | \$25.00 | +12.5% |
| $k_e$ −1 **and** $g$ +1 | \$28.57 | **+28.6%** |

> [!warning] ⚠️ And it gets worse as $k_e$ approaches $g$
> *(Computed — effect of a one-point cut in $k_e$, with $g=3\%$:)*
>
> | $k_e$ | price | after −1 pt | change |
> |---|---|---|---|
> | 20% | \$11.76 | \$12.50 | +6.2% |
> | 12% | \$22.22 | \$25.00 | +12.5% |
> | 10% | \$28.57 | \$33.33 | +16.7% |
> | 8% | \$40.00 | \$50.00 | **+25.0%** |
> | **5%** | **\$100.00** | **\$200.00** | **+100.0%** |
>
> **⚠️ So the Gordon model is not really a valuation tool — it is an instrument for converting small disagreements about risk and growth into enormous disagreements about price.**
>
> **Which is exactly what a stock market looks like**, and it explains how the same firm can be "obviously cheap" and "obviously expensive" to two honest analysts who differ by a percentage point. *(It also warns that **low-rate environments are structurally more volatile**: the same one-point shock that moves prices 6% at $k_e=20\%$ moves them 100% at $k_e=5\%$.)*

### 4. Applications — monetary policy, and the crash

**Monetary policy: the Fed cuts rates. Two effects, same direction.**

| | effect |
|---|---|
| **1** | bonds (the alternative asset) yield less ⇒ investors accept a lower $k_e$ ⇒ denominator shrinks ⇒ **$P$ up** |
| **2** | lower rates stimulate the economy ⇒ **$g$ rises** ⇒ denominator shrinks ⇒ **$P$ up** |

> [!note] ⚠️ Unambiguous — like the Fisher effect, unlike the business cycle
> **Both effects push the same way, so no parameter choice reverses the sign.** *(Compare [[03 - The Behavior of Interest Rates|ch. 03]] §4, where the two effects opposed and the model could not deliver a sign.)*
>
> *(Quantified from $k_e=12\%$, $g=3\%$: a **half-point** easing that also lifts $g$ by a quarter-point gives **+9.1%**; a one-point easing gives **+20.0%**; two points gives **+50.0%**.)* **A half-point rate cut, if it moves both inputs, is a double-digit move in equities — which is why analysts hang on every word the Fed chair says.** *(And [[12 - Monetary Policy Theory, Expectations and Transmission|ch. 12]] makes this a *transmission channel*, not just a market curiosity.)*

**The global financial crisis.** *(Verified: DJIA peak **14,066** (Oct 2007) to trough **6,547** (Mar 2009) = **−53.46%**; Mishkin says the market "lost 53% of its value".)*

**His account is entirely qualitative:** **$g$ fell** *(growth prospects cut)* **and $k_e$ rose** *(uncertainty and widening credit spreads — [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s +360 bp)*. **Both raise the denominator, so $P$ falls.** **He never asks how much.**

> [!warning] ⚠️ A 53% crash is a 4-to-9 point move in a spread nobody can observe
> **Holding $D_1$ fixed, $(k_e-g)_{\text{new}}/(k_e-g)_{\text{old}}=P_{\text{old}}/P_{\text{new}}=\mathbf{2.1485}$** — **the denominator more than doubled.**
>
> | if $k_e-g$ was | it became | move |
> |---|---|---|
> | 4.0% | 8.59% | **+4.59 pts** |
> | 5.0% | 10.74% | +5.74 pts |
> | 8.0% | 17.19% | **+9.19 pts** |
>
> **Split it any way you like between "$k_e$ rose" and "$g$ fell" — the model cannot tell you, because it has one equation and two unknowns.**
>
> **⚠️ And *that* is why §6's question is unresolved.** **Is a four-point repricing of risk-and-growth a rational response to genuinely terrible news, or a panic?** **Nothing in the model distinguishes them** — which is a fact about what is observable, not a defect of the formula.

*(The other crashes: **Black Monday, 19 October 1987 — the DJIA fell more than 20% in one day, the largest one-day decline in US history**; and the NASDAQ from ~5,000 in March 2000 to ~1,500 in 2001–02, **−70.0%**, which is Mishkin's "well over 60%".)*

### 5. ⚠️ Rational expectations — and why adaptive expectations are not

$$\boxed{\ X^e=X^{of}\ }\qquad\text{the expectation equals the optimal forecast using ALL available information}$$

> [!note] "Rational" does not mean "always right"
> **Joe Commuter: 30 minutes off-peak, +10 in rush hour ⇒ optimal forecast 40.** *(Verified: on two days he takes 45 and 35 minutes — **errors +5 and −5, mean exactly 0**. **Wrong both days, and still rational**, because it is unbiased.)*
>
> **An expectation fails to be rational for exactly two reasons:**
> 1. **the information is available but using it is too much effort;**
> 2. **the information is not available at all.**
>
> **⚠️ And the asymmetry between them matters.** **If a traffic report existed and Joe ignored it, 40 minutes is *irrational*.** **If no report existed, 40 minutes is *rational* even though the true answer was 2 hours 40.** **Rationality is judged against the information set, never against the outcome.**

**Two implications.**

**1. Change how a variable *moves* and you change how expectations of it are *formed*.** *(Mishkin's case: if rates are mean-reverting, "high today" forecasts a fall; if rates are persistent, "high today" forecasts more high. **The same observation, opposite forecast** — and nothing about the observation tells you which regime you are in.)*

**2. Forecast errors average zero and cannot be predicted ahead of time.**

> [!warning] ⚠️ Why adaptive expectations fail implication 2 — computed
> **Adaptive expectations are a weighted average of past values of one variable: $\pi^e_t=(1-\lambda)\sum_{j\ge0}\lambda^j\pi_{t-j}$.** *(Simulated — inflation jumps permanently from 5% to 10%:)*
>
> | adjustment speed | path | years to get within 1 point |
> |---|---|---|
> | **0.20** | 5.00, 6.00, 6.80, 7.44, 7.95, 8.36, 8.69, 8.95, 9.16, 9.33 | **8** |
> | 0.35 | 5.00, 6.75, 7.89, 8.63, 9.11, 9.42, … | 4 |
> | 0.50 | 5.00, 7.50, 8.75, 9.38, 9.69, … | 3 |
>
> **⚠️ Every forecast error has the same sign, for years** *(at speed 0.20: +5.00, +4.00, +3.20, +2.56, +2.05, +1.64, +1.31, +1.05, +0.84, +0.67)*.
>
> **So the error is trivially predictable — "I am under-forecasting; add something" — and any forecaster who noticed would fix it.** **That is why adaptive expectations are not rational: not because they are inaccurate, but because they are inaccurate *in a predictable direction*.** *(Mishkin's own sketch, 5% → 6% → 7%, is linear; the actual geometric path is above and is **slower** than his sketch suggests.)*
>
> **And his deeper objection: adaptive expectations use past values of *one variable only*.** **Anyone forecasting inflation would obviously also use announced monetary policy** — **so adaptive expectations commit failure mode 1, ignoring free and relevant information.**

> [!note] Why people bother
> **It is costly not to.** **Joe underpredicts and is late; overpredicts and loses sleep.** **General Electric misforecasts interest rates and builds too many or too few appliances.** **⚠️ The incentives are strongest of all in financial markets, where people with better forecasts *get rich*** — which is exactly why the theory transfers there.

### 6. ⚠️ The efficient market hypothesis

**Take [[02 - The Meaning of Interest Rates|ch. 02]]'s return, apply rational expectations, and impose equilibrium:**

$$R^e=R^{of}\quad\text{(rational expectations)}\qquad R^e=R^*\quad\text{(equilibrium)}\qquad\Longrightarrow\qquad\boxed{\ R^{of}=R^*\ }$$

$$\textbf{a security's price fully reflects all available information}$$

**The mechanism is arbitrage, and it is a *disequilibrium* argument:**

$$R^{of}>R^*\ \Rightarrow\ \text{buy}\ \Rightarrow\ P_t\uparrow\ \Rightarrow\ R^{of}\downarrow$$
$$R^{of}<R^*\ \Rightarrow\ \text{sell}\ \Rightarrow\ P_t\downarrow\ \Rightarrow\ R^{of}\uparrow\qquad\text{until }R^{of}=R^*$$

> [!warning] ⚠️ The crucial rider — EMH is not a claim about investors' intelligence
> **Not everyone need be informed or rational.** **A few "smart money" participants suffice, because eliminating an unexploited profit opportunity is *how they profit*.** **⚠️ This is what makes the hypothesis plausible at all** — it survives any amount of documented investor foolishness, so long as *someone* is watching.

**Random walk.** *(Verified: if HFC's price were predictably +1% next week, that is **52%** simply annualised or **67.8%** compounded — both far above any equilibrium return, so it is bought away instantly.)*

> [!note] The random walk is a *consequence*, not an assumption
> **Prices are unpredictable *because* anything predictable has already been traded on.** *(The same argument applies to exchange rates — [[10 - Foreign Exchange and the International Financial System|ch. 10]].)* **And this is what "the random-walk theory of stock prices" in the press actually refers to.**

### 7. ⚠️ The football tipster — the chapter's best story, computed

**The con: split a mailing list in two; tell half "team A wins" and half "team B wins". Next week write only to the half you were right for. Repeat.** **After ten games one group has received ten correct predictions in a row — and you have made no forecast at all.**

*(Mishkin tells this and never does the arithmetic. Computed:)*

| week | letters sent | still perfect |
|---|---|---|
| 1 | **1,024** | 512 |
| 5 | 64 | 32 |
| 10 | 2 | **1** |

**⚠️ $2^{10}=1{,}024$ marks manufacture exactly one perfect 10-for-10 record, guaranteed.**

> [!warning] ⚠️ And the generalisation is the part that matters
> **With $N$ genuinely skill-less forecasters, the expected number with a perfect $k$-year record is $N/2^k$:**
>
> | forecasters | perfect 5-yr | perfect 10-yr | perfect 15-yr |
> |---|---|---|---|
> | 1,000 | 31.25 | 0.98 | 0.03 |
> | **10,000** | **312.50** | **9.77** | 0.31 |
> | 100,000 | 3,125 | 97.66 | 3.05 |
>
> **⚠️ In a population of 10,000 fund managers with no skill whatever, about 312 beat the market five years running and about 10 do it for ten.** **They will be interviewed. The other 9,990 will not be.**
>
> **Mishkin's own summing-up is the diagnosis:** *"there will also be a group of persistent losers, but you rarely hear about them because no one brags about a poor forecasting record."* **That is survivorship bias, and the con man differs from the fund industry only in knowing what he was doing.**
>
> *(The San Francisco Chronicle ran it as an experiment instead: **the orangutan Jolyn "beat the investment advisers as often as they beat her."**)*

### 8. What EMH prescribes — and what it does not claim

| prescription | why |
|---|---|
| **published advice and hot tips are worthless** | they use *public* information, already in the price |
| **a hot tip helps only if you are among the first to have it** | you profit by *eliminating* the opportunity |
| **do not trade actively** | it enriches brokers and triggers capital-gains tax |
| **buy and hold** | same average return, higher net profit |
| **⚠️ small investors: a no-load, low-fee fund** | since no fund reliably beats the market, **fees are the only thing you control** |

> [!note] The rare directly actionable economics result
> **The last row is the whole practical content of the chapter**, and it follows from $R^{of}=R^*$ with no further assumptions. *(Mishkin notes some documented **anomalies** suggest an extremely clever investor might beat buy-and-hold — **and sends them to an off-book appendix**, the fourth such in five chapters.)*

**Good news and falling prices — the test that convinces people.** **Prices respond only to *surprises*.**

| earnings | expected | surprise | price |
|---|---|---|---|
| +15% | +20% | **−5%** | **FALLS** |
| +15% | +15% | 0 | unchanged |
| +15% | +10% | +5% | RISES |

> [!warning] ⚠️ "Earnings rose 15%" is not information; "15% when 20% was expected" is
> **If a stock moved on expected news, the move would have been predictable — which an efficient market rules out.** **The running theme once more: the number alone does not carry its meaning — here it needs the expectation.**

> [!warning] ⚠️ The distinction Mishkin is most careful about — and the hypothesis is misnamed
> | | claim |
> |---|---|
> | **EMH** *(weak)* | **prices are unpredictable**; no unexploited profit opportunities survive |
> | **"financial markets are efficient"** *(strong)* | **prices equal true fundamental value** |
>
> **The first does not imply the second.**
>
> **Crashes and bubbles are evidence against the *strong* version** — economists are "hard pressed to find fundamental changes in the economy" that moved prices 20% on 19 October 1987 — **while leaving the weak version intact, *so long as the crashes themselves were unpredictable*.**
>
> **⚠️ So the honest position is: prices may be wrong and still unbeatable.** *(Some economists disagree, holding that bubbles imply unexploited opportunities did exist. **Mishkin says plainly that the controversy continues** — and §4 showed why it cannot be settled by looking at prices: one equation, two unknowns.)*

### 9. Behavioural finance — and why the arbitrage is one-sided

| finding | consequence |
|---|---|
| **loss aversion** | short sales have *unlimited* downside ⇒ **very little short selling happens** (and rules restrict it further) |
| **overconfidence** | investors trade on beliefs ⇒ explains the **huge trading volume EMH does not predict** |
| **overconfidence + social contagion** | positive feedback loop ⇒ **speculative bubbles** |

> [!warning] ⚠️ The structural point is sharper than the psychology
> **The arbitrage mechanism is not symmetric.**
>
> - **To correct an *undervalued* stock you BUY it** — anyone with cash can.
> - **To correct an *overvalued* stock you must SHORT it** — which requires borrowing the stock, bearing unlimited loss, and is often restricted outright.
>
> **⚠️ So the corrective force is strong on the downside and weak on the upside, and overvaluation is therefore easier to sustain than undervaluation.**
>
> **That is a prediction about the *shape* of market errors, not merely an assertion that errors exist** — and it explains why the anomalies people point to are *bubbles* rather than "anti-bubbles".
>
> **Note this does not overturn §6.** **Smart money still eliminates every opportunity it can reach; the claim is that it cannot reach all of them, and that *which* ones it cannot reach is systematic.**

## ✏️ Exercises

**1. (Valuation.)** (a) Value Intel with the one-period model. (b) Why does the final sale price drop out, and when does that argument fail? (c) State the Gordon model and its two assumptions.

> [!example]- Solution
> **(a) \$53.71 — so buy at \$50.**
>
> $$P_0=\frac{0.16}{1.12}+\frac{60}{1.12}=\$0.1429+\$53.5714=\mathbf{\$53.7143}$$
>
> ✓ against the book's \$0.14 + \$53.57 = \$53.71. **Note the dividend contributes 0.27% of the value and the terminal price 99.73%** — over one year, the sale price is essentially the whole story.
>
> **⚠️ But \$53.71 is not a fact about Intel.** **The discount rate is *your* required return on equity**, so the number is a joint statement about the firm and about you. **Mishkin's own caveat is the important one: the market may price it at \$50 because other investors forecast lower cash flows *or apply a higher $k_e$.** **Exercise 3 shows how far apart honest people can land.**
>
> **(b) Because distant amounts discount to nothing — but only if the rate is high.**
>
> *(Verified: \$50 seventy-five years out at 12% is **\$0.0102**, the book's "just one cent".)* **So $P_n$ can be dropped and $P_0=\sum D_t/(1+k_e)^t$ — the price of a stock is the present value of its dividends and nothing else.**
>
> **⚠️ The argument is rate-dependent, and Mishkin does not say so.** *(Computed: the same \$50 at 75 years is worth **\$1.2876 at 5%** — **126 times more**.)* **At low required returns the terminal value carries real weight**, which matters because §3 shows low-$k_e$ valuations are exactly the fragile ones.
>
> *(And the natural objection — many stocks pay no dividend — is answered by expectations: **buyers expect dividends someday**, usually once rapid growth ends. **A zero *current* dividend is fine; a zero *expected* one means the model values the stock at zero**, and whatever is holding its price up is outside the theory.)*
>
> **(c) $P_0=D_1/(k_e-g)$, assuming constant growth forever and $g<k_e$.**
>
> **Assumption 1 is forgiving** — errors about distant dividends are discounted away, so constant growth "for an extended period" suffices.
>
> **⚠️ Assumption 2 is not.** **If $g\ge k_e$ the formula returns a negative or infinite price** — not a low valuation but a broken one. **Gordon's own justification is economic, not mathematical: a firm growing faster than its cost of equity forever would eventually become larger than the economy.**

**2. (Hard — sensitivity.)** (a) Mishkin's three investors agree on every cash flow. How far apart are their valuations, and why? (b) Quantify the sensitivity in general. (c) What does this say about what the Gordon model is *for*?

> [!example]- Solution
> **(a) 71.4% apart, from a five-point disagreement about risk.**
>
> | investor | $k_e$ | price |
> |---|---|---|
> | You | 15% | **\$16.67** ✓ |
> | Jennifer | 12% | **\$22.22** ✓ |
> | Bud | 10% | **\$28.57** ✓ |
>
> *(All three verified against the book.)* **They agree on $D_1=\$2$ and on $g=3\%$ — every cash flow is identical.** **The only difference is perceived risk, and Bud's valuation is 71.4% above yours.**
>
> **The mechanism is the auction lesson: superior information raises value by *reducing risk*.** **Bud discounts the same cash flows at a lower rate because he is more certain of them** — and so he wins the auction, at a price just above Jennifer's \$22.22 rather than at his own \$28.57.
>
> **(b) A one-point move in either input is 10–12.5%, and it explodes as $k_e\to g$.**
>
> **$k_e$ and $g$ enter only as a difference, so a one-point error in one is exactly a one-point error in the other.** From $P=D_1/(k_e-g)$:
> $$\frac{\partial P}{\partial(k_e-g)}=-\frac{P}{k_e-g}$$
>
> *(Computed from $k_e=12\%$, $g=3\%$, $P=\$22.22$: $k_e$ +1 pt ⇒ **−10.0%**; $k_e$ −1 pt ⇒ **+12.5%**; $k_e$ −1 **and** $g$ +1 ⇒ **+28.6%**.)*
>
> **⚠️ And the sensitivity is not constant — it grows as the denominator shrinks.** *(Computed, effect of a one-point cut in $k_e$ with $g=3\%$: **+6.2% at $k_e=20\%$**, +12.5% at 12%, +25.0% at 8%, **+100.0% at 5%**.)*
>
> **The reason: the denominator is a difference of two largish numbers, so it inherits both their errors and keeps none of their size.** **A 12% and a 3% that are each accurate to a point give a 9% spread accurate to two points — a 22% relative error before you start.**
>
> **(c) It is an instrument for amplifying disagreement, not for settling it.**
>
> **⚠️ The Gordon model converts small, honest differences about risk and growth into enormous differences about price** — which is exactly what a stock market looks like, and it explains how the same firm can be obviously cheap and obviously expensive to two competent analysts one percentage point apart.
>
> **Two consequences worth carrying.**
> - **Low-rate environments are structurally more volatile.** The same one-point shock that moves prices 6% at $k_e=20\%$ moves them 100% at $k_e=5\%$. **This is a property of the arithmetic, not of investor psychology.**
> - **⚠️ A Gordon valuation should never be quoted as a number.** **It should be quoted as a range over the plausible inputs**, because the point estimate carries no information the inputs did not already contain — and the inputs are forecasts.
>
> *(Compare [[02 - The Meaning of Interest Rates|ch. 02]]'s duration, which is exactly right in the limit and silently wrong outside it. **This is the opposite failure**: the Gordon model is algebraically exact everywhere and *useless* wherever its inputs are uncertain — which is everywhere.)*

**3. (Hard — the crash.)** (a) Verify the crisis figures. (b) Back out what the fall implies for $k_e-g$. (c) Why can't this settle whether the crash was rational?

> [!example]- Solution
> **(a) −53.46%.**
>
> **DJIA peak 14,066 (Oct 2007) to trough 6,547 (Mar 2009) ⇒ $6547/14066-1=\mathbf{-53.46\%}$** ✓ against "lost 53% of its value".
>
> *(And the others: **Black Monday, 19 Oct 1987, DJIA −20% in a single day**, the largest one-day fall in US history; **NASDAQ ~5,000 → ~1,500, −70.0%**, Mishkin's "well over 60%".)*
>
> **Mishkin's account is entirely qualitative: $g$ fell (growth prospects cut) and $k_e$ rose (uncertainty, and the widening credit spreads [[04 - The Risk and Term Structure of Interest Rates|ch. 04]] measured at +360 bp).** **Both raise the denominator ⇒ $P$ falls. He never asks how much.**
>
> **(b) The denominator more than doubled — a 4-to-9 point move.**
>
> **Holding $D_1$ fixed, $P=D_1/(k_e-g)$ gives $(k_e-g)_{\text{new}}/(k_e-g)_{\text{old}}=P_{\text{old}}/P_{\text{new}}=14{,}066/6{,}547=\mathbf{2.1485}$.**
>
> | if $k_e-g$ was | it became | move |
> |---|---|---|
> | 4.0% | 8.59% | **+4.59 pts** |
> | 5.0% | 10.74% | +5.74 pts |
> | 8.0% | 17.19% | **+9.19 pts** |
>
> **A 53% crash is a few percentage points on a spread that is not directly observable.** *(This is §2's amplification running in reverse, and it is worth noticing that the "enormous" crash and the "modest" repricing are the same event described in two units.)*
>
> **(c) Because there is one equation and two unknowns.**
>
> **The 2.1485 can be split any way at all between "$k_e$ rose" and "$g$ fell", and those two stories have opposite interpretations:**
> - **$g$ fell** ⇒ **the market received genuinely terrible news about future dividends** ⇒ the crash was a *rational repricing*;
> - **$k_e$ rose** ⇒ **the same cash flows are now discounted more harshly** ⇒ which may be rational (real uncertainty rose) *or* may be panic.
>
> **⚠️ Nothing observable in the price separates them.** **That is not a defect in the Gordon model — it is why the efficient-markets debate is unresolved after forty years.**
>
> **And the debate's actual structure is exactly this.** **One camp says economists "are hard pressed to find fundamental changes in the economy" to justify a 20% single-day move, so the *strong* version — prices equal fundamental value — is wrong.** **The other says nothing in EMH rules out large price changes, and the *weak* version survives so long as the crash was unpredictable.**
>
> **⚠️ Both can be right simultaneously, and Mishkin's careful position is that they are: prices may be wrong and still unbeatable.** *(Which is the practically important conclusion, because it is the second property, not the first, that determines whether you should try to trade.)*

**4. (Expectations.)** (a) Define rational expectations and show a wrong forecast can be rational. (b) Prove adaptive expectations are not. (c) State the two implications.

> [!example]- Solution
> **(a) $X^e=X^{of}$ — the optimal forecast given available information.**
>
> **Joe Commuter: 30 minutes off-peak, +10 in rush hour ⇒ 40 minutes.** *(Verified: on two days he takes 45 and 35 — **errors +5 and −5, mean exactly 0**.)* **Wrong on both days, and rational, because the forecast is unbiased.** **"An optimal forecast will never be completely accurate" — there is irreducible randomness.**
>
> **Two failure modes:** **(i) the information is available but using it is too much effort; (ii) the information is not available.**
>
> **⚠️ And the asymmetry between them is the definition's whole content.** **A two-hour traffic jam Joe could not have known about leaves 40 minutes rational.** **The same jam, announced on a radio report he ignored, makes 40 minutes irrational — the optimal forecast was 2 h 40.** **Rationality is judged against the information set, never against the outcome**, which is why "the forecast was wrong" is never by itself a criticism.
>
> **(b) Because their errors are one-signed for years — hence predictable.**
>
> *(Simulated — inflation jumps permanently 5% → 10%, $\pi^e_t=\pi^e_{t-1}+(1-\lambda)(\pi_{t-1}-\pi^e_{t-1})$:)*
>
> | speed | path | errors | within 1 pt |
> |---|---|---|---|
> | **0.20** | 5.00, 6.00, 6.80, 7.44, 7.95, 8.36, 8.69, 8.95, 9.16, 9.33 | **+5.00, +4.00, +3.20, +2.56, +2.05, +1.64, …** | **8 years** |
> | 0.35 | 5.00, 6.75, 7.89, 8.63, 9.11, … | all positive | 4 years |
> | 0.50 | 5.00, 7.50, 8.75, 9.38, … | all positive | 3 years |
>
> **⚠️ Every error has the same sign, for years.** **So the error is trivially predictable — "I keep under-forecasting; add something" — and implication 2 says a rational forecaster would do exactly that.**
>
> **The failure is not inaccuracy. It is inaccuracy *in a predictable direction*** — and that is a free lunch left on the table, which is precisely what rationality rules out.
>
> *(Mishkin's own sketch, 5→6→7%, is **linear**; the true geometric path is above and is **slower** than his sketch suggests. And his deeper objection is failure mode 1: **adaptive expectations use past values of one variable only**, ignoring announced monetary policy, which is free and obviously relevant.)*
>
> **(c) Regime changes change expectation formation; and errors are unpredictable.**
>
> **1.** **If rates are mean-reverting, "high today" forecasts a fall; if rates become persistent, "high today" forecasts more high.** **The same observation yields opposite forecasts, and nothing in the observation tells you which regime you are in.** **⚠️ So a forecasting rule estimated under one regime is worthless under another** — which is the Lucas critique in embryo, and it is why [[12 - Monetary Policy Theory, Expectations and Transmission|ch. 12]] is a separate chapter.
>
> **2.** **Errors average zero and cannot be predicted.** **If Joe were late by 5 minutes on average he would notice and add 5 minutes.**
>
> *(And the reason people bother is incentives: Joe is fired or loses sleep; GE builds too many or too few appliances. **⚠️ The incentives are strongest in financial markets, where people with better forecasts get rich** — which is exactly why the theory transfers there under the name EMH.)*

**5. (Hard — EMH.)** (a) Derive it and state the crucial rider. (b) Do the tipster arithmetic and generalise. (c) What does EMH prescribe, and what does it *not* claim?

> [!example]- Solution
> **(a) $R^{of}=R^*$, and not everyone need be rational.**
>
> **Rational expectations give $P^e_{t+1}=P^{of}_{t+1}$, hence $R^e=R^{of}$. Equilibrium gives $R^e=R^*$. Together: $R^{of}=R^*$** — **a security's price fully reflects all available information.**
>
> **The mechanism is arbitrage and it is a disequilibrium argument.** If ExxonMobil's optimal forecast return is 50% against an equilibrium 10%, **that is an unexploited profit opportunity; buying it drives $P_t$ up and $R^{of}$ down until they equalise.**
>
> **⚠️ The crucial rider: not everyone in the market need be well informed or rational.** **A few "smart money" participants suffice, because eliminating the opportunity is *how they profit*.** **This is what makes EMH plausible at all** — **it survives any amount of documented investor foolishness**, and so cannot be refuted by pointing at foolish investors.
>
> *(Random walk follows: a predictable +1% week is **52% simply annualised or 67.8% compounded** — verified — far above equilibrium, so it is arbitraged away. **The random walk is a consequence of profit-seeking, not an assumption about prices.**)*
>
> **(b) 1,024 marks buy exactly one perfect record — and 10,000 skill-less managers produce ~10 ten-year winners.**
>
> **The con halves the mailing list each week, writing only to those it was right for.** *(Computed: **$2^{10}=1{,}024$ initial marks manufacture exactly one recipient who has received ten correct predictions in a row**, guaranteed, from a forecaster who forecast nothing.)*
>
> **Generalising: with $N$ skill-less forecasters the expected number with a perfect $k$-year record is $N/2^k$.**
>
> | forecasters | perfect 5-yr | perfect 10-yr |
> |---|---|---|
> | 1,000 | 31.25 | 0.98 |
> | **10,000** | **312.50** | **9.77** |
> | 100,000 | 3,125 | 97.66 |
>
> **⚠️ So a perfect ten-year record is not evidence of skill in a large population — it is what pure chance predicts.** **Those ~10 will be interviewed; the 9,990 will not**, and **Mishkin names the mechanism exactly: "you rarely hear about them because no one brags about a poor forecasting record."** **That is survivorship bias, and the con man differs from the fund industry only in knowing what he was doing.**
>
> *(The Chronicle ran it as an experiment: **the orangutan Jolyn beat the eight analysts as often as they beat her.**)*
>
> **(c) Buy and hold cheap index funds; and it does NOT claim prices are right.**
>
> **Prescriptions:** hot tips and published advice are worthless *(they use public information)*; a tip helps only if you are among the first; **do not trade actively — it enriches brokers and triggers capital-gains tax**; buy and hold; **⚠️ and for small investors, a no-load low-fee fund, because if no fund can reliably beat the market then *fees are the only thing you control*.**
>
> **The surprise test that convinces people: prices respond only to surprises.** **Earnings up 15% when 20% was expected is *bad* news and the price falls.** **"Earnings rose 15%" is not information; "15% when 20% was expected" is.**
>
> **⚠️ And the distinction Mishkin is most careful about — the hypothesis is misnamed.**
>
> | | claim |
> |---|---|
> | **EMH** | prices are **unpredictable** |
> | **"markets are efficient"** | prices equal **true fundamental value** |
>
> **The first does not imply the second.** **Crashes and bubbles are evidence against the strong version and leave the weak version intact, provided the crashes were unpredictable.** **So prices may be wrong and still unbeatable.**
>
> **⚠️ Behavioural finance sharpens this into a prediction about the *shape* of the errors.** **To correct an undervalued stock you buy — anyone can. To correct an overvalued one you must short — which needs borrowed stock, carries unlimited loss, and is often restricted.** **So the corrective force is strong on the downside and weak on the upside ⇒ overvaluation is easier to sustain than undervaluation ⇒ the anomalies are bubbles, not anti-bubbles.**
>
> **This does not overturn (a).** **Smart money still eliminates every opportunity it can reach; the claim is that it cannot reach all of them and that *which* ones are unreachable is systematic.**

## 📝 Summary

- **Equity valuation is [[02 - The Meaning of Interest Rates|ch. 02]]'s present value applied to dividends** — **nothing new is needed.** The discount rate is the **required return on equity**, not an interest rate.
- **One-period model verified** — Intel at $D_1=\$0.16$, $P_1=\$60$, $k_e=12\%$ gives **\$53.7143** ✓.
- **The terminal price drops out** *(verified: \$50 in 75 years at 12% is **\$0.0102**)* — **but ⚠️ the argument is rate-dependent: at 5% the same \$50 is worth \$1.2876, 126× more.**
- **Gordon: $P_0=D_1/(k_e-g)$, assuming constant growth and $g<k_e$.** **Assumption 2 is the boundary where the model stops existing, not a technicality.**
- **⚠️ Mishkin's three investors agree on every cash flow and value the stock 71.4% apart** *(verified: \$16.67 / \$22.22 / \$28.57)* — **the difference is purely perceived risk.**
- **⚠️ The Gordon model is a sensitivity amplifier** *(computed: a one-point move in either input is **10–12.5%**, rising to **+100.0% at $k_e=5\%$**)*. **Small honest disagreements become enormous price disagreements** — ⇒ **quote a range, never a point estimate**, and note that **low-rate environments are structurally more volatile.**
- **Monetary policy is unambiguous** — lower rates cut $k_e$ *and* raise $g$, both raising prices *(computed: a half-point easing gives **+9.1%**, two points gives **+50.0%**)*. **Unlike [[03 - The Behavior of Interest Rates|ch. 03]]'s business cycle.**
- **⚠️ The 2007–09 crash verified at −53.46%** *(14,066 → 6,547)* **and implies $k_e-g$ more than doubled — a 4-to-9 point move in an unobservable spread.**
- **⚠️ One equation, two unknowns — so the model cannot say whether a crash was rational**, and that is why the efficient-markets debate is unresolved.
- **Rational expectations: $X^e=X^{of}$ — right *on average*, not always right.** **Rationality is judged against the information set, never against the outcome.**
- **⚠️ Adaptive expectations are irrational because their errors are one-signed for years** *(computed: +5.00, +4.00, +3.20, … taking **8 years** to close to within a point at speed 0.20)* — **inaccurate in a *predictable direction*, which is a free lunch left on the table.**
- **Change how a variable moves and you change how expectations of it form** — **the same observation yields opposite forecasts under different regimes.**
- **EMH = rational expectations plus equilibrium: $R^{of}=R^*$.** **⚠️ The crucial rider is that a few "smart money" participants suffice** — so EMH cannot be refuted by pointing at foolish investors.
- **The random walk is a *consequence* of profit-seeking** *(verified: a predictable +1% week is **52%** simple / **67.8%** compounded annualised)*.
- **⚠️ The tipster: 1,024 marks manufacture exactly one perfect 10-for-10 record** — and **10,000 skill-less managers produce ~312 five-year and ~10 ten-year perfect records by chance alone.** **Survivorship bias.**
- **Prescription: buy and hold a no-load, low-fee fund — fees are the only thing you control.**
- **Prices respond only to surprises** — **+15% earnings against a +20% expectation is bad news.**
- **⚠️ EMH ≠ "markets are efficient".** **Prices may be wrong and still unbeatable**, and **behavioural finance predicts the *shape* of the errors: arbitrage is one-sided, so overvaluation outlasts undervaluation.**

## ⚠️ Important Notes

1. **$k_e$ is the *required return on equity*, not an interest rate.** It embeds the investor's own risk perception.
2. **⚠️ A valuation is a statement about the valuer as much as about the firm.**
3. **The terminal value drops out only at high discount rates.** At 5% it does not.
4. **A zero *current* dividend is fine; a zero *expected* dividend values the stock at zero.**
5. **⚠️ $g<k_e$ is a boundary, not a technicality.** Outside it the formula returns nonsense, not a low number.
6. **$k_e$ and $g$ enter only as a difference** — a one-point error in one is exactly a one-point error in the other.
7. **⚠️ Gordon sensitivity explodes as $k_e\to g$.** Quote a range over plausible inputs, never a point estimate.
8. **⚠️ Low-rate environments are arithmetically more volatile** — a property of the formula, not of psychology.
9. **The auction price sits just above the *second*-highest valuation**, not at the winner's.
10. **Superior information raises value by lowering the discount rate**, not by changing the forecast cash flows.
11. **⚠️ A large price change is not by itself evidence against EMH** — only an unexploited, *predictable* opportunity is.
12. **Rationality is judged against the information set, not the outcome.** A wrong forecast can be rational; an ignored radio report cannot.
13. **⚠️ Adaptive expectations fail because their errors are one-signed**, not because they are inaccurate.
14. **A rule estimated under one regime is worthless under another** — the Lucas critique in embryo.
15. **⚠️ EMH survives foolish investors.** Only a few smart participants are needed.
16. **The random walk is derived, not assumed.**
17. **⚠️ A perfect ten-year record is what chance predicts in a large population.** Ask how many started.
18. **Prices move on surprises only** — good news can lower a price.
19. **⚠️ EMH does not say prices are right.** "Unpredictable" and "correct" are different claims, and the name conflates them.
20. **⚠️ Arbitrage is one-sided** — buying is unconstrained, shorting is not — **so market errors are systematically upward.**

> [!warning] Gaps in the source material
> **This chapter extracts unusually well** — it is almost entirely prose and worked arithmetic, with **only one substantive figure**, and **every one of Mishkin's numbers reproduces**.
>
> **⚠️ The parenthesis fault appears but is easily handled** — the footnote deriving the Gordon model from the infinite sum extracts with parentheses intact in places and mangled in others, and **the derivation was reconstructed from the prose and checked against the book's own three worked prices (\$16.67 / \$22.22 / \$28.57), all of which reproduce.**
>
> **Figure 1 (stock price indexes 1950–2017) is an image and is lost.** **Its qualitative content survives in the prose** — the October 1987 and 2000–02 crashes, and the 2007–09 fall — **and the three quantitative claims attached to it (DJIA 14,066 → 6,547; DJIA −20% on 19 October 1987; NASDAQ ~5,000 → ~1,500) are stated in the text and are verified here.** **The series themselves are not recoverable and are not reconstructed.**
>
> **No table in this chapter** other than Mishkin's three-investor list, **which survived complete** and all three of whose entries reproduce.
>
> **No erratum found.** **Everything checks: \$53.71, \$0.01 at 75 years, all three Gordon prices, the 53% DJIA decline, the NASDAQ decline, and the >50% annualised weekly return.**
>
> **⚠️ TWO MORE OFF-BOOK APPENDICES** *(the pattern is now systematic — see [[00-Index]])*: **the models of asset pricing** referenced in [[03 - The Behavior of Interest Rates|ch. 03]] is invoked again here, and **the EMH *anomalies*** — the documented deviations that "an extremely clever investor may be able to" exploit — **are sent entirely to the publisher's website.** **This is a real loss**: the anomalies are the empirical case against the hypothesis the chapter spends most of its length building, **and the note therefore presents the EMH evidence as Mishkin does, which is favourably.** **Flagged rather than filled**, since inventing anomalies would be fabrication.
>
> **Additions beyond the source.**
>
> - **⚠️ §3 is the chapter's principal addition and it is a genuine result, not an elaboration.** **Mishkin computes his three investors' prices and moves on.** Observing that **they agree on every cash flow and differ by 71.4%**, then computing the sensitivity table and the $k_e\to g$ explosion *(+6.2% at 20%, +100.0% at 5%)*, **turns a worked example into a statement about what the model is for** — and yields two consequences he never states: **quote a range, not a point**, and **low-rate environments are arithmetically more volatile.**
> - **⚠️ §4's back-out of the crash is mine.** **Mishkin's crisis application is entirely qualitative** — "$g$ fell, $k_e$ rose, so $P$ fell". Computing **$(k_e-g)$ must have risen by a factor of 2.1485**, i.e. **4 to 9 percentage points**, quantifies it; **and the observation that one equation with two unknowns is *why* the rational-versus-panic question is unanswerable is my synthesis of his own two-sided discussion.**
> - **⚠️ §5's simulation of adaptive expectations is mine.** **Mishkin asserts they adjust "slowly" and sketches 5→6→7% linearly.** Simulating the actual geometric path shows **it is slower than his sketch** and — the decisive point — that **every error carries the same sign for years**, which is *why* they violate his own implication 2. **He states the two facts separately and does not connect them.**
> - **⚠️ §7's arithmetic is mine and it is the chapter's best addition per line.** **Mishkin tells the tipster story with no numbers at all.** **$2^{10}=1{,}024$**, and the generalisation to **$N/2^k$ skill-less forecasters** *(≈10 perfect ten-year records among 10,000 managers)*, **converts an anecdote into a quantitative warning** — and it is directly usable whenever a track record is offered as evidence.
> - **§9's observation that arbitrage is *one-sided* is mine.** **Mishkin gives the loss-aversion explanation for why little short selling occurs and notes it can leave stocks overvalued**; **stating it as a structural asymmetry — buying is unconstrained, shorting is not, therefore market errors are systematically upward — makes it a prediction about the *shape* of anomalies** rather than an assertion that anomalies exist.
> - **§1's rate-dependence of the terminal-value argument is mine** *(\$0.0102 at 12% versus \$1.2876 at 5%)*.
> - **§4's quantification of the monetary-policy channel, and §8's surprise table, are mine.**
> - **The identification of §8's "earnings +15% against +20% expected" as another instance of the running theme — a number does not carry its own meaning — is my synthesis.**

**Previous:** [[04 - The Risk and Term Structure of Interest Rates]] · **Next:** [[06 - Asymmetric Information and Financial Structure]]
