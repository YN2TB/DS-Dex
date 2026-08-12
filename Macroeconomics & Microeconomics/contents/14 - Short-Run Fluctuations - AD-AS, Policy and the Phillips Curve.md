---
subject: Macroeconomics & Microeconomics
chapter: 14
tags: [ds, economics, macroeconomics, ad-as, multiplier, phillips-curve, sacrifice-ratio, expectations]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 20–22"
---

# Short-Run Fluctuations: AD–AS, Policy and the Phillips Curve

**[[12 - The Monetary System and Inflation|Chapter 12]] called monetary neutrality "the hinge between the two halves of macro". This is the other side of it.** In the short run prices are sticky, so nominal changes move real output — **and everything in this chapter follows from that one failure.**

**Three results.**

**§4 — the multiplier and crowding out, *netted*.** Mankiw gives both effects and never combines them. *(Computed: the net multiplier ranges from **0.80 to 10.00** depending on the MPC and the degree of offset — at MPC 0.5 with 60% crowding out, \$20bn of spending raises demand by only \$16bn, **less than it cost**.)*

**§5 — the Phillips curve is the short-run AS curve with different axes**, and *(computed)* **once expectations adjust, unemployment sits at 5.00% whether inflation is 2%, 4% or 6%.** **The long-run trade-off vanishes** — which is [[12 - The Monetary System and Inflation|ch. 12]]'s neutrality in Phillips coordinates.

**§6 — the sacrifice ratio puts a number on credibility.** *(Verified: Mankiw's estimate of 5, so Volcker's 6-point disinflation cost **30% of annual output**.)*

**And §4 is the fourth appearance of one shape**: two identified forces oppose and the theory does not sign the net.

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]].

## 📘 Main Knowledge

### 1. Why the short run is different

**[[12 - The Monetary System and Inflation|Ch. 12]] established monetary neutrality — money moves nominal variables and leaves real ones alone. That is a *long-run* claim, and this is where it fails.**

**The reason is sticky prices and wages.** Firms do not reprice instantly: **menu costs, contracts, and coordination all delay adjustment**, so in the short run a change in nominal demand moves **real** output.

> [!note] AD–AS does not replace the long-run model — it describes the path toward it
> **[[09 - Production and Growth|Ch. 09]]'s growth theory and [[12 - The Monetary System and Inflation|ch. 12]]'s quantity theory still describe the long run.** This chapter describes the **adjustment**, and how policy can smooth it.
>
> **Three facts about fluctuations** frame the chapter: they are **irregular and unpredictable**; **most macroeconomic quantities move together**; and **as output falls, unemployment rises.**

### 2. Aggregate demand and aggregate supply

**AD slopes down for three reasons — all different from the microeconomic reason:**

| effect | mechanism |
|---|---|
| **wealth** | lower $P$ raises real money balances → **consume more** |
| **interest-rate** | lower $P$ cuts money demand → lower $r$ → **more investment** |
| **exchange-rate** | lower $r$ → currency depreciates → **more net exports** ([[13 - Open-Economy Macroeconomics|ch. 13]]) |

> [!note] AD's slope comes from $C$, $I$ and $NX$ in turn
> **Not from substitution toward other goods** — there is no "other good" when the price level itself moves. **The three effects are the components of [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s identity, one at a time.**

**Long-run AS is vertical.** Output is determined by labour, capital, resources and technology — **[[09 - Production and Growth|ch. 09]]'s production function — not by the price level.** Doubling all prices and wages changes nothing real.

> [!note] The long-run AS curve sits at the natural rate of output
> **And [[11 - Unemployment|ch. 11]]'s natural rate of unemployment is its labour-market twin** — the same idea measured on the other side of the production function.

**Short-run AS slopes up**, for three reasons: **sticky wages**, **sticky prices**, and **misperceptions** about relative prices.

> [!warning] All three short-run AS explanations share one structure
> **Something nominal fails to adjust, so a nominal change has a real effect.** *(That is worth noticing because it means the three theories are not rivals — they are three mechanisms for the same failure, and any one of them is enough to give the result.)*

**Two sources of fluctuation:** shifts in **AD** (output and prices move together) and shifts in **AS** (**stagflation** — output falls while prices rise, which is the diagnostic signature).

### 3. The spending multiplier

*(Verified — Mankiw's example: \$20bn of government purchases with $MPC = 0.75$:)*

| round | spending | cumulative |
|---|---|---|
| initial | 20.000 | 20.000 |
| 2 | 15.000 | 35.000 |
| 3 | 11.250 | 46.250 |
| 4 | 8.438 | 54.688 |
| … | | |
| **limit** | | **80.0** |

$$\text{multiplier}=\frac{1}{1-MPC}=\mathbf{4.0}$$

| MPC | multiplier |
|---|---|
| 0.50 | 2.00 |
| 0.75 | **4.00** |
| 0.90 | **10.00** |

**Each round of spending becomes someone's income, and they spend $MPC$ of it** — a geometric series. *(Mankiw also notes the **investment accelerator**, which strengthens it.)*

### 4. ⚠️ Netting the multiplier against crowding out

**Mankiw gives both effects and never combines them. They oppose:**

- **multiplier** — extra spending raises income, raising consumption;
- **crowding out** — extra spending raises money demand, raising $r$, which **cuts investment** *([[10 - Saving, Investment and the Financial System|ch. 10]]'s mechanism, now working through the money market)*.

*(Computed — net multiplier $=\frac{1}{1-MPC}\times(1-\text{offset})$:)*

| MPC | gross | offset | **net multiplier** | net effect of \$20bn |
|---|---|---|---|---|
| 0.50 | 2.00 | 0% | 2.00 | 40.0 |
| **0.50** | 2.00 | **60%** | **0.80** | **16.0** |
| 0.75 | 4.00 | 30% | **2.80** | 56.0 |
| 0.75 | 4.00 | 60% | 1.60 | 32.0 |
| **0.90** | 10.00 | 30% | **7.00** | 140.0 |

> [!warning] The net multiplier ranges from 0.80 to 10.00
> **At MPC 0.5 with 60% crowding out, \$20bn of government spending raises demand by \$16bn — less than it cost.**
>
> **So the fiscal-policy debate is not about whether the multiplier exists.** Both effects are agreed. **The question is their relative size, which is empirical.**
>
> **⚠️ And this is the fourth appearance of one shape:**
>
> | chapter | question | opposing forces |
> |---|---|---|
> | [[07 - Factor Markets and the Theory of Consumer Choice\|07]] | higher wages → hours worked? | substitution vs income |
> | [[10 - Saving, Investment and the Financial System\|10]] | crowding out of a deficit? | the saving-curve slope |
> | [[11 - Unemployment\|11]] | minimum-wage job losses? | the demand elasticity |
> | **14** | **the fiscal multiplier?** | **multiplier vs crowding out** |
>
> **In every case two identified forces oppose and the theory does not sign the net.** *(Quoting a point estimate as though it did is the error, and it is made in both political directions.)*
>
> **⚠️ Note when the offset is small**: if $r$ cannot fall further (a **liquidity trap**) or the economy is far below capacity, **crowding out is weak and the net multiplier is large.** **That is why the debate is most intense in deep recessions — the parameter genuinely changes**, so both sides can be right about different circumstances.

**Monetary policy works through the same channel in reverse**: the central bank changes the money supply, which moves $r$, which moves investment and $NX$. **Automatic stabilisers** — taxes and transfers that move with income — do some of this without anyone deciding.

> [!note] The case against active stabilisation is about lags, not mechanism
> **Policy acts with long and variable lags**, so a stimulus can arrive after the recovery. **That is an argument for rules over discretion, and it does not dispute that the mechanism works.**

### 5. ⚠️ The Phillips curve is AD–AS rearranged

**The short-run Phillips curve plots inflation against unemployment and slopes down. It is not a separate theory** — it is the short-run AS curve with different axes:

**AD shifts right → output up and prices up → unemployment down** *(Okun's law)* **→ inflation up with unemployment down.**

**But the trade-off depends on expectations:**

$$u = u_n - a(\pi - \pi^{\text{expected}})$$

*(Computed with $u_n = 5.0\%$ and $a = 0.5$:)*

| expected $\pi$ | actual $\pi$ | surprise | **unemployment** |
|---|---|---|---|
| 2.0% | 2.0% | 0.0% | **5.00%** |
| 2.0% | 4.0% | +2.0% | **4.00%** |
| 2.0% | 6.0% | +4.0% | **3.00%** |
| **4.0%** | **4.0%** | **0.0%** | **5.00%** |
| **6.0%** | **6.0%** | **0.0%** | **5.00%** |
| 6.0% | 4.0% | −2.0% | **6.00%** |

> [!warning] With no surprise, unemployment is 5.00% whether inflation is 2%, 4% or 6%
> **So the long-run Phillips curve is vertical.** Once expectations catch up, **any inflation rate is compatible with the natural rate** — **which is [[12 - The Monetary System and Inflation|ch. 12]]'s monetary neutrality in Phillips-curve coordinates.**
>
> **That is the natural-rate hypothesis (Friedman and Phelps), and it was a *prediction*** — made before the 1970s produced the stagflation that confirmed it. **Mankiw makes this point and it is worth dwelling on: a macroeconomic theory predicted an unprecedented phenomenon in advance**, which is as good as the subject gets.
>
> **The policy consequence is sharp: a government can buy lower unemployment only by inflating *faster than expected*, and only until expectations adjust.** **Doing it repeatedly just raises inflation with no lasting gain** — which is the analytical case for central-bank independence.

**Supply shocks** shift the short-run Phillips curve **outward**, giving higher inflation *and* higher unemployment together — **the 1970s oil shocks**, and the reason stagflation cannot be explained by demand alone.

### 6. ⚠️ The sacrifice ratio

> **The number of percentage points of annual output lost in the process of reducing inflation by 1 percentage point. A typical estimate of the sacrifice ratio is 5.** — Mankiw

*(Verified — the Volcker disinflation as Mankiw sets it up: inflation near 10%, target about 4%, so a **6-point** reduction:)*

$$6\times5=\mathbf{30\%\text{ of annual output}}$$

*(Spread over five years, **6% of output per year**.)*

| sacrifice ratio | 6-point disinflation costs | over 5 years |
|---|---|---|
| 1.0 | 6% | 1.2%/yr |
| 2.0 | 12% | 2.4%/yr |
| **5.0** | **30%** | **6.0%/yr** |
| 8.0 | 48% | 9.6%/yr |

> [!warning] This is the number attached to credibility
> **The cost depends on the slope of the Phillips curve and on how fast expectations adjust** — Mankiw says exactly this.
>
> **So if a central bank announces a disinflation and is *believed*, expected inflation falls immediately, the short-run Phillips curve shifts down, and the economy reaches lower inflation without the recession.**
>
> **[[12 - The Monetary System and Inflation|Ch. 12]] ended by saying credibility is a central bank's main asset. This is the price tag.** **With full credibility and rational expectations the sacrifice ratio could approach zero** — and **in practice Volcker's disinflation caused a severe recession**, which suggests **credibility had to be earned rather than announced.**
>
> *(That asymmetry — cheap to lose, expensive to rebuild — is the strongest argument in the chapter for rules, inflation targets and independence.)*

### 7. What the macro half adds up to

| | determined by |
|---|---|
| **long run** ([[09 - Production and Growth\|09]]–[[13 - Open-Economy Macroeconomics\|13]]) | output by productive capacity; $r$ by saving and investment; unemployment by the natural rate; the price level by money; the trade balance by $S-I$. **Money is neutral.** |
| **short run** (14) | prices are sticky, so **aggregate demand moves real output**. Policy can stabilise — imperfectly, with lags, against parameters nobody knows precisely. |

> [!note] Not rival theories
> **The long-run model says where the economy is *headed*; the short-run model describes the *path* and how policy can smooth it.**
>
> **And the honest summary of every policy chapter is the one this subject reached four times: the theory identifies the forces and does not sign the net.** **That is a real contribution and it is not a forecast** — knowing *which parameter decides the answer* is most of what a model is for.

## ✏️ Exercises

**1. (AD–AS.)** (a) Why does AD slope down? (b) Why is long-run AS vertical and short-run AS upward-sloping? (c) How do you tell a demand shock from a supply shock?

> [!example]- Solution
> **(a) Three effects, none of them the microeconomic reason.**
>
> **A microeconomic demand curve slopes down because buyers substitute toward other goods. There is no "other good" when the whole price level moves**, so AD needs a different explanation:
>
> | effect | mechanism | component |
> |---|---|---|
> | **wealth** | lower $P$ → higher real balances → more consumption | $C$ |
> | **interest-rate** | lower $P$ → less money demand → lower $r$ → more investment | $I$ |
> | **exchange-rate** | lower $r$ → depreciation → more net exports | $NX$ |
>
> **The three are [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s identity taken one component at a time**, and the interest-rate effect is quantitatively the most important in most treatments.
>
> **(b) Because in the long run output is set by capacity and in the short run something nominal is stuck.**
>
> **Long-run AS is vertical** because output depends on labour, capital, resources and technology — **[[09 - Production and Growth|ch. 09]]'s production function** — and **not on the price level.** Doubling every price and wage changes nothing real. *(It sits at the natural rate of output, whose labour-market twin is [[11 - Unemployment|ch. 11]]'s natural rate of unemployment.)*
>
> **Short-run AS slopes up** for three reasons: **sticky wages**, **sticky prices**, and **misperceptions**.
>
> **⚠️ All three share one structure: something nominal fails to adjust, so a nominal change has a real effect.** **They are not rival theories — they are three mechanisms for one failure, and any single one delivers the result.**
>
> **(c) By what happens to prices and output together.**
>
> | shock | output | prices |
> |---|---|---|
> | **AD** | falls | **falls** |
> | **AS** | falls | **rises** — *stagflation* |
>
> **That is the diagnostic signature**, and it is why the 1970s could not be explained by demand alone: **output and inflation moved in the same unfavourable direction**, which an AD shift cannot produce.
>
> **The policy consequence matters too**: an adverse AD shock can be offset by expansionary policy with no tension. **An adverse AS shock forces a choice** — accommodating it worsens inflation, resisting it worsens the recession. **There is no policy that fixes both**, which is why supply shocks are the hard case.

**2. (Hard — policy.)** (a) Derive the multiplier. (b) Net it against crowding out. (c) When is the offset small, and what does the pattern say?

> [!example]- Solution
> **(a) A geometric series in the marginal propensity to consume.**
>
> *(Verified: \$20bn at $MPC = 0.75$ gives 20 → 15 → 11.25 → 8.44 → … summing to **\$80bn**, so the multiplier is $1/(1-MPC) = \mathbf{4.0}$.)*
>
> **Each round of spending becomes someone's income and they spend $MPC$ of it.** *(Computed across MPCs: **2.00** at 0.5, **4.00** at 0.75, **10.00** at 0.9 — the multiplier rises steeply because the series converges more slowly.)*
>
> **Mankiw's investment accelerator strengthens it further**: higher demand induces firms to invest, adding another round.
>
> **(b) The two effects oppose, and the net can be less than one.**
>
> *(Computed:)*
>
> | MPC | offset | **net multiplier** |
> |---|---|---|
> | 0.50 | 60% | **0.80** |
> | 0.75 | 30% | **2.80** |
> | 0.90 | 30% | **7.00** |
>
> **At MPC 0.5 with 60% crowding out, \$20bn of spending raises demand by \$16bn — less than the government spent.**
>
> **The crowding-out mechanism here works through the *money* market**: higher income raises money demand, which raises $r$, which cuts investment. *(That is [[10 - Saving, Investment and the Financial System|ch. 10]]'s result reached by a different route — there the deficit competed for loanable funds directly.)*
>
> **⚠️ So the fiscal-policy debate is not about whether the multiplier exists.** Both forces are agreed by everyone. **It is about their relative size**, and that is empirical.
>
> **(c) When the interest rate cannot rise — and the pattern is the subject's signature.**
>
> **Crowding out is weak when $r$ is already at zero (a liquidity trap), or when the economy is far below capacity so that extra demand does not bid up rates.** **In those conditions the net multiplier is large.**
>
> **⚠️ That is why the fiscal debate is most intense in deep recessions: the parameter genuinely changes**, so both sides can be right about different circumstances — and arguing about "the" multiplier as though it were a constant is the mistake.
>
> **And this is the fourth appearance of one shape**: [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]] (substitution vs income), [[10 - Saving, Investment and the Financial System|ch. 10]] (the saving slope), [[11 - Unemployment|ch. 11]] (the demand elasticity), and now multiplier vs crowding out.
>
> **In every case the theory identifies two opposing forces and refuses to sign the net.** **That is not a weakness — it tells you exactly which quantity to go and measure**, which is a great deal more useful than a confident wrong answer.

**3. (The Phillips curve.)** (a) Where does it come from? (b) Why is the long-run curve vertical? (c) What does the sacrifice ratio cost, and what does that imply?

> [!example]- Solution
> **(a) It is the short-run AS curve with different axes.**
>
> **AD shifts right → output rises and prices rise → unemployment falls (Okun's law) → so inflation is up and unemployment down.** **A downward-sloping curve, and not a separate theory.**
>
> **Recognising this matters** because it means the Phillips curve inherits every limitation of short-run AS: **it holds only while prices are sticky, and it shifts when anything shifts AS.**
>
> **(b) Because only *surprises* move unemployment away from the natural rate.**
>
> $$u=u_n-a(\pi-\pi^{\text{expected}})$$
>
> *(Computed with $u_n = 5\%$: when expected and actual inflation are equal — at **2%, 4% or 6%** — unemployment is **5.00% in every case**. Only a surprise moves it: +2 points of surprise gives 4.00%, and −2 points gives 6.00%.)*
>
> **So the long-run Phillips curve is vertical: any inflation rate is compatible with the natural rate once expectations have caught up.** **That is [[12 - The Monetary System and Inflation|ch. 12]]'s monetary neutrality, in different coordinates** — and it is the same statement that money is neutral in the long run.
>
> **⚠️ This was the natural-rate hypothesis of Friedman and Phelps, and it was a *prediction*.** They argued the apparent 1960s trade-off would break down as expectations adjusted; **the 1970s then produced stagflation, which the prevailing view could not explain and this one had anticipated.** **A macroeconomic theory predicting an unprecedented phenomenon in advance is rare enough to be worth remembering.**
>
> **Policy consequence: lower unemployment can be bought only by inflating faster than expected, and only until expectations adjust.** **Repeating it just raises inflation with no lasting gain** — the analytical case for central-bank independence.
>
> **(c) About 30% of annual output for Volcker's disinflation — and it is the price of credibility.**
>
> *(Verified: Mankiw's typical sacrifice ratio of **5**, and a 6-point reduction from ~10% to 4% costs $6\times5 = \mathbf{30\%}$ of annual output, or **6% per year over five years**.)*
>
> **The cost depends on the Phillips curve's slope and on how fast expectations adjust.**
>
> **⚠️ So if a disinflation is *believed*, expected inflation falls immediately, the short-run curve shifts down, and lower inflation arrives without the recession.** *(Computed: at a sacrifice ratio of 1 rather than 5, the same disinflation costs **6%** instead of 30%.)*
>
> **[[12 - The Monetary System and Inflation|Ch. 12]] said credibility is a central bank's main asset; this is the number attached to it.**
>
> **And the historical evidence is instructive rather than clean: Volcker's disinflation *did* cause a severe recession**, which suggests **credibility must be earned rather than announced** — expectations did not adjust simply because a policy was declared.
>
> **That asymmetry — credibility is cheap to lose and expensive to rebuild — is the strongest argument in the chapter for rules, inflation targets and independence**, and it is why modern central banks guard their communications so carefully.

## 📝 Summary

- **Sticky prices break [[12 - The Monetary System and Inflation|ch. 12]]'s monetary neutrality in the short run** — that is the hinge, and everything here follows from it. **AD–AS describes the *path*; the long-run models describe the *destination*.**
- **AD slopes down through wealth, interest-rate and exchange-rate effects** — [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s components one at a time, **not** microeconomic substitution.
- **Long-run AS is vertical at the natural rate of output** ([[09 - Production and Growth|ch. 09]]'s production function), whose labour-market twin is [[11 - Unemployment|ch. 11]]'s natural rate of unemployment.
- **Short-run AS slopes up via sticky wages, sticky prices and misperceptions** — **three mechanisms for one failure**, not rival theories.
- **AD shocks move output and prices together; AS shocks move them oppositely — stagflation**, which is the diagnostic signature and the hard policy case.
- **The spending multiplier is $1/(1-MPC)$** *(verified: **4.0** at MPC 0.75, giving \$80bn from \$20bn)*.
- **⚠️ Netted against crowding out, the multiplier ranges from 0.80 to 10.00** *(computed)*. **At MPC 0.5 with 60% offset, \$20bn of spending raises demand by \$16bn — less than it cost.**
- **The debate is about relative size, not existence.** **⚠️ Crowding out is weak in a liquidity trap or far below capacity — so the parameter genuinely changes, and both sides can be right about different circumstances.**
- **⚠️ Fourth appearance of one shape**: [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]], [[10 - Saving, Investment and the Financial System|ch. 10]], [[11 - Unemployment|ch. 11]], ch. 14. **Two forces oppose and the theory does not sign the net** — which tells you *which parameter to measure.*
- **The case against active stabilisation is about lags, not mechanism.**
- **⚠️ The Phillips curve is short-run AS with different axes**, so it inherits every limitation of short-run AS.
- **⚠️ Expectations-augmented: $u = u_n - a(\pi-\pi^e)$.** *(Computed: with no surprise, unemployment is **5.00%** at inflation of 2%, 4% **or** 6%.)* **The long-run Phillips curve is vertical — [[12 - The Monetary System and Inflation|ch. 12]]'s neutrality in different coordinates.**
- **The natural-rate hypothesis was a *prediction*** that the 1960s trade-off would break down; **the 1970s confirmed it.**
- **Lower unemployment can be bought only by inflating faster than expected, and only until expectations adjust.**
- **⚠️ The sacrifice ratio is ~5, so Volcker's 6-point disinflation cost ~30% of annual output** *(verified)* — **6% a year over five years.**
- **Credibility is the lever: a believed disinflation shifts the short-run curve down and avoids the recession.** **But Volcker's *did* cause one — so credibility is earned, not announced.**

## ⚠️ Important Notes

1. **⚠️ Neutrality is long-run only.** Sticky prices are why the short run exists.
2. **AD slopes down for three macro reasons**, none of them substitution.
3. **Long-run AS is vertical** — output depends on capacity, not the price level.
4. **The three short-run AS theories are one mechanism**: something nominal fails to adjust.
5. **⚠️ Stagflation identifies a supply shock.** Demand shocks move output and prices the same way.
6. **An adverse supply shock forces a choice** — no policy fixes inflation and unemployment together.
7. **Multiplier $=1/(1-MPC)$**, and it rises steeply with the MPC.
8. **⚠️ Always net the multiplier against crowding out.** The net can be below 1.
9. **⚠️ The offset depends on circumstances** — weak in a liquidity trap or with large slack.
10. **The fiscal debate is about a parameter, not a mechanism.**
11. **Lags are the real case against discretion**, not a dispute about how policy works.
12. **⚠️ The Phillips curve is not an independent theory.** It is AD–AS rearranged.
13. **⚠️ Only inflation *surprises* move unemployment from the natural rate.**
14. **The long-run Phillips curve is vertical** — the same statement as monetary neutrality.
15. **⚠️ The natural-rate hypothesis predicted stagflation before it happened.**
16. **Sacrifice ratio ≈ 5**: disinflation is expensive, and the cost falls with credibility.
17. **⚠️ Credibility is earned, not announced** — Volcker's disinflation still caused a recession.
18. **Four times in this subject: the theory identifies the forces and does not sign the net.** Report a range and name the parameter.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located all three chapters** *(Macro 2017, PDF pp. 448–533)*.
>
> **⚠️ THE OPERATOR CIPHER applies** — see [[00-Index]]. **Nothing was transcribed**, and Mankiw's two verifiable figures (the multiplier formula applied to \$20bn at MPC ¾, and the sacrifice ratio of 5 applied to a 6-point disinflation) both reproduce.
>
> **⚠️ Every figure is lost, and this is the most diagram-dependent chapter in the book.** **The AD–AS diagram itself, all the shift panels, the money-market diagram, the short-run and long-run Phillips curves, the shifting-expectations sequence, and the Volcker disinflation path are all images.** **AD–AS is taught almost entirely through shifting curves**, so the whole chapter had to be rebuilt from the prose.
>
> **This is why §§4–6 state the relationships algebraically** — $\frac{1}{1-MPC}(1-\text{offset})$ and $u = u_n - a(\pi-\pi^e)$ — **rather than describing pictures. The algebra is checkable and the diagrams are gone.**
>
> **No erratum.** Every figure Mankiw states reproduces.
>
> **Additions beyond the source.**
>
> - **⚠️ §4's netting of the multiplier against crowding out is the chapter's main addition.** **Mankiw presents the multiplier formula, then presents the crowding-out effect, and never combines them.** Computing the net across MPCs and offsets shows the range **0.80 to 10.00** — **and that at plausible parameters the net can be below 1**, which is the entire content of the fiscal-policy dispute. **The observation that the offset is weak in a liquidity trap or with large slack — so the parameter changes with circumstances and both sides can be right — is mine.**
> - **⚠️ The identification of this as the *fourth* "two forces oppose, theory does not sign the net" result** — after [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]], [[10 - Saving, Investment and the Financial System|ch. 10]] and [[11 - Unemployment|ch. 11]] — **is my running synthesis across the subject**, and it is the most transferable thing in the macro half.
> - **§5's expectations table is mine.** Mankiw explains the expectations-augmented curve verbally and in a lost figure; **tabulating it shows unemployment sitting at exactly 5.00% at three different inflation rates**, which makes "the long-run curve is vertical" a computed result rather than an assertion — and makes its identity with [[12 - The Monetary System and Inflation|ch. 12]]'s neutrality visible.
> - **§6's sensitivity table** (the same disinflation at sacrifice ratios of 1 to 8) is an addition; Mankiw gives the single estimate of 5. **The framing that this is "the number attached to credibility"**, discharging [[12 - The Monetary System and Inflation|ch. 12]]'s closing claim, is mine — as is the observation that **Volcker's disinflation still caused a recession, so credibility is earned rather than announced.**
> - **§2's note that the three short-run AS theories are three mechanisms for one failure** rather than competing explanations is mine.
> - **The point that an adverse supply shock forces a genuine policy choice while a demand shock does not** is an addition.
> - **§7's summary of how the long-run and short-run models relate** — destination versus path — is my framing of the subject's structure.
>
> **Deliberately compressed.** **Mankiw ch. 20's historical account of the Great Depression and the 2008–09 recession** is represented by the analytical content; the narratives are long and the accompanying figures are lost. **The theory of liquidity preference and the money-market diagram** (ch. 21) are stated as the mechanism linking money to $r$ rather than developed — **the diagram is lost and [[Monetary and Financial Theories/contents/00-Index|Mishkin]] owns monetary transmission by the boundary recorded in [[00-Index]]**. **The extended debate over active versus passive policy, and over zero inflation versus moderate inflation**, is compressed to §4's lag argument and §6's credibility point; both are represented in [[00-Index]]'s omission of Macro ch. 23 (*Six Debates*), whose content is these arguments restated. **The tax-multiplier variant and the balanced-budget multiplier** are noted implicitly in §3's formula rather than derived separately. **Okun's law** is used to connect output and unemployment and is not developed as a topic of its own.

**Previous:** [[13 - Open-Economy Macroeconomics]] · **Next:** *(end of subject — return to [[00-Index]])*
