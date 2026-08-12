---
subject: Macroeconomics & Microeconomics
chapter: 9
tags: [ds, economics, macroeconomics, growth, productivity, diminishing-returns, catch-up, solow]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 12"
---

# Production and Growth

**[[08 - Measuring the Macroeconomy - GDP and the Cost of Living|Chapter 08]] built the measuring instruments. This chapter uses them on the most consequential question in economics: why are some countries rich and others poor, and what makes living standards rise?**

**The answer is productivity — and [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]] already established *why*, microeconomically: a firm will not pay a worker more than they add, and competition will not let it pay less. So wages track marginal product.** This chapter asks what determines that product.

**Three results, all asserted by Mankiw and computed here.**

**§2 — a higher saving rate raises the *level* of income, not the long-run *growth rate*.** *(Computed: at saving rates of 5% through 40% the long-run growth of output per worker is **zero in every case**, and doubling the saving rate raises output per worker by only **1.414×**, not 2× — because $y^*\propto\sqrt{s}$.)*

**§3 — the catch-up effect.** *(Computed: a country starting at $k=0.5$ grows **25× faster** than an identical one at $k=6$. Convergence is a *prediction* of the model, not an assumption.)*

**§4 — "the long run" is longer than a career.** *(Computed: after a permanent rise in saving, the transition is **half done in ~25 years and still incomplete after a century**.)*

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]].

## 📘 Main Knowledge

### 1. The production function, and the trick that makes growth theory possible

$$Y = A\,F(L,K,H,N)$$

**where $Y$ is output, $L$ labour, $K$ physical capital, $H$ human capital, $N$ natural resources, and $A$ the level of technology.** *(It extracts as `Y 5 AF(L, K, H, N )`.)*

**Constant returns to scale** means doubling every input doubles output:

$$xY=A\,F(xL,xK,xH,xN)\quad\text{for any }x>0$$

> [!note] Set $x = 1/L$ — and the whole subject becomes about *per-worker* quantities
> $$\frac{Y}{L}=A\,F\!\left(1,\frac{K}{L},\frac{H}{L},\frac{N}{L}\right)$$
>
> **Output per worker depends on capital per worker, human capital per worker, resources per worker, and technology.** **That single substitution is why growth theory studies productivity rather than output**, and Mankiw performs exactly this step.
>
> *(The working form used below is $y = A k^{\alpha}$ with $\alpha = 1/3$, and capital accumulates as $\Delta k = s\,y-\delta k$ — saving minus depreciation. A **steady state** is where investment exactly replaces depreciation.)*

### 2. ⚠️ Saving raises the level, not the growth rate

$$s\,A\,k^{\alpha}=\delta k\;\Longrightarrow\;k^*=\left(\frac{sA}{\delta}\right)^{\!1/(1-\alpha)}$$

*(Computed:)*

| saving rate | $k^*$ | $y^*$ | vs $s=10\%$ | **long-run growth of $y$** |
|---|---|---|---|---|
| 5% | 1.0000 | 1.0000 | 0.707× | **0.00%** |
| **10%** | 2.8284 | 1.4142 | 1.000× | **0.00%** |
| **20%** | 8.0000 | 2.0000 | **1.414×** | **0.00%** |
| 30% | 14.6969 | 2.4495 | 1.732× | **0.00%** |
| 40% | 22.6274 | 2.8284 | 2.000× | **0.00%** |

> [!warning] Every row grows at zero in the long run
> **Saving more does not make an economy grow forever. It makes it richer, and then it stops.**
>
> **And the level gain is heavily diminishing.** *(Computed: doubling the saving rate from 10% to 20% raises output per worker only **1.414×** — because $k^*$ rises 2.83× and the exponent $\alpha=1/3$ undoes most of it.)*
>
> $$y^*\;\propto\;s^{\alpha/(1-\alpha)}=s^{0.5}\qquad\textbf{a square root}$$
>
> **To double output per worker you must *quadruple* the saving rate** — which is why "save more" is a real policy with sharply limited returns.

> [!note] So what produces permanent growth? Only rising $A$.
> *(Computed: $y^*\propto A^{1/(1-\alpha)} = A^{1.50}$, so technology growth is **amplified by 1.5×** — a higher $A$ also pulls up the capital stock. With $A$ growing at 2%/yr, output per worker grows at **3.01%/yr, forever.**)*
>
> **Capital accumulation runs into diminishing returns; technology does not.** **The long-run growth rate is a statement about *ideas*, not about thrift** — which is why §5's R&D and education levers matter more than the saving lever, despite being harder to pull.

### 3. ⚠️ The catch-up effect, computed

**Two countries identical in every respect — same saving rate, same depreciation, same technology — differing *only* in where they start.** Both head to the same $k^*=8$.

*(Computed:)*

| starting $k$ | output $y$ | $\Delta k$ | **growth rate of $y$** |
|---|---|---|---|
| **0.50** | 0.7937 | 0.1337 | **+8.92%** |
| 1.00 | 1.0000 | 0.1500 | +5.00% |
| 2.00 | 1.2599 | 0.1520 | +2.53% |
| 4.00 | 1.5874 | 0.1175 | +0.98% |
| **6.00** | 1.8171 | 0.0634 | **+0.35%** |
| 7.90 | 1.9916 | 0.0033 | +0.01% |

> [!warning] The poorest country grows 25× faster than the richest
> **The mechanism is diminishing returns, exactly as Mankiw describes it: when a worker has almost no tools, one more tool transforms their output; when a worker already has plenty, one more adds little.**
>
> **So convergence is a *prediction* of the model, not an assumption** — and it explains post-war Japan, South Korea, and China without needing anything special about those countries beyond starting poor with the right institutions.

> [!warning] "Other things equal" does all the work
> *(Computed — countries with different $s$ or $A$ converge to **different** steady states:)*
>
> | | $s$ | $A$ | $k^*$ | $y^*$ |
> |---|---|---|---|---|
> | benchmark | 20% | 1.00 | 8.0000 | **2.0000** |
> | low saving | 5% | 1.00 | 1.0000 | **1.0000** |
> | weak institutions | 20% | 0.60 | 3.7181 | **0.9295** |
>
> **This is *conditional* convergence, and it is why the raw prediction "poor countries grow faster" fails in the data while the model survives.** Countries converge to **their own** steady state, not to ours. **A poor country with weak institutions is not far below its steady state — it is *at* a low one**, and will not catch up until $A$ or $s$ changes.
>
> **That distinction is the difference between a useful model and a refuted one**, and it is worth being precise about because the raw version is frequently quoted.

### 4. ⚠️ How long is "the long run"?

**Mankiw says reaching the new steady state "can take quite a while" and that higher saving can raise growth "for several decades". Simulate it** — an economy in steady state at $s=10\%$ permanently raises saving to 20%:

| year | $k$ | $y$ | growth of $y$ | **% of the way to the new $y^*$** |
|---|---|---|---|---|
| 0 | 2.8284 | 1.4142 | — | 0.0% |
| 5 | 3.5103 | 1.5198 | +1.250% | 18.0% |
| 10 | 4.1247 | 1.6037 | +0.943% | 32.4% |
| **25** | — | — | — | **~50%** |
| 30 | 5.9229 | 1.8093 | +0.373% | 67.4% |
| 50 | 6.9188 | 1.9055 | +0.170% | 83.9% |
| **100** | 7.7975 | 1.9830 | +0.029% | **97.1%** |

> [!warning] Half the transition takes 25 years and it is still incomplete after a century
> **So "a higher saving rate does not raise the long-run growth rate" is true *and* nearly useless as policy advice over a human lifetime.** The transitional growth lasts decades, and decades are what policy is for.
>
> **This is exactly Mankiw's point — and exactly why it needed computing rather than asserting.** The statement sounds like a case *against* promoting saving; the simulation shows it is nothing of the kind.

### 5. The determinants, and what policy can do

| determinant | |
|---|---|
| **physical capital** per worker | tools and equipment |
| **human capital** per worker | skills, education, experience |
| **natural resources** per worker | the **least** important in practice |
| **technological knowledge** ($A$) | **the only source of permanent growth** |

> [!note] Human capital and technology are different things
> **Technology is society's *knowledge* of how to produce. Human capital is the resources spent transmitting that knowledge to workers.** **A textbook is technology; a graduate is human capital.** *(The distinction matters because they need different policies — R&D subsidies versus schooling.)*

**Mankiw's policy levers, with the caveats that matter:**

- **Saving and investment** — raises the level; **§2 shows not the growth rate**.
- **Investment from abroad** — FDI raises **GDP more than GNP**, because the profits leave.
- **Education** — carries a **positive externality** ([[04 - Externalities, Public Goods and Common Resources|ch. 04]]), so the market underprovides it. *(And the **brain drain** means the returns may accrue elsewhere.)*
- **Health and nutrition** — causation runs **both ways** with income.
- **Property rights and political stability** — **the precondition for everything else.**
- **Free trade** — [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s comparative advantage as a growth policy; an inward-looking policy forgoes the gains ch. 01 computed.
- **Population growth** — dilutes capital per worker: more $L$ lowers $k$.
- **Research and development** — knowledge is a **public good** ([[04 - Externalities, Public Goods and Common Resources|ch. 04]]): non-rival and hard to exclude, so it is underprovided without patents or subsidy.

> [!warning] Four of these nine are [[04 - Externalities, Public Goods and Common Resources|ch. 04]] results reappearing
> **Education's externality, R&D as a public good, property rights, and the non-rivalry of knowledge.** **Growth policy is largely market-failure policy** — which is not obvious in advance and unifies two chapters that look unrelated.
>
> **Property rights are the sharpest case.** [[04 - Externalities, Public Goods and Common Resources|Ch. 04]] identified them as the *fix* for market failure; here they are the **precondition for growth itself**. **A country without enforceable contracts cannot accumulate capital, whatever its saving rate** — which is why $A$ in §3's table can be read as "institutions" as much as "technology."

### 6. Why growth rates matter more than they look

*(Computed:)*

| growth rate | after 10 yrs | after 35 yrs | after 70 yrs | **years to double** |
|---|---|---|---|---|
| **1.0%** | 1.10× | 1.42× | 2.01× | **69.7** |
| **2.0%** | 1.22× | 2.00× | 4.00× | **35.0** |
| 3.0% | 1.34× | 2.81× | 7.92× | 23.4 |
| **4.0%** | 1.48× | 3.95× | **15.57×** | **17.7** |

> [!note] The rule of 70
> **A variable growing at $g$% per year doubles in about $70/g$ years.** At 1% that is a lifetime; at 4% it is 18 years.
>
> *(Computed: a country growing **2 points faster overtakes one starting twice as rich in about 35 years**.)*
>
> **This is why [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]'s result matters so much.** Wages track productivity, so **productivity growth *is* the growth of living standards — and nothing else available to policy comes close in magnitude.** A percentage point of growth outweighs almost any redistribution, given enough time; the difficulty is that "enough time" is decades, which is §4's problem again.

## ✏️ Exercises

**1. (The framework.)** (a) What does constant returns to scale buy you? (b) Why does saving not raise the growth rate? (c) What does?

> [!example]- Solution
> **(a) It converts the model into per-worker terms.**
>
> $$xY=A\,F(xL,xK,xH,xN)\quad\text{so setting }x=1/L:\quad \frac{Y}{L}=A\,F\!\left(1,\frac{K}{L},\frac{H}{L},\frac{N}{L}\right)$$
>
> **Output *per worker* depends on capital *per worker* and the other inputs per worker.** That is why growth theory is about productivity rather than about total output — **a country can raise $Y$ simply by having more people, which does nothing for living standards.**
>
> **(b) Because capital runs into diminishing returns.**
>
> *(Computed: at saving rates from 5% to 40%, long-run growth of $y$ is **zero in every case**.)*
>
> **The steady state is where investment just replaces depreciation:** $sAk^\alpha=\delta k$. **Raising $s$ moves the economy to a higher $k^*$ and stops there** — because as $k$ rises, $sy$ (which grows as $k^\alpha$) rises more slowly than $\delta k$ (which grows linearly), so they must eventually meet again.
>
> **And the level gain is small:** *(computed)* $y^*\propto s^{\alpha/(1-\alpha)}=\sqrt{s}$, **so doubling the saving rate raises output per worker only 1.414×, and quadrupling it is needed to double income.**
>
> **(c) Only technology.**
>
> *(Computed: $y^*\propto A^{1.50}$, so 2%/yr technology growth gives **3.01%/yr** growth of output per worker, forever — the **1.5× amplification** arising because higher $A$ also raises the capital stock.)*
>
> **Capital accumulation faces diminishing returns; ideas do not** — a new idea can be used by everyone at once without being used up. *(That non-rivalry is exactly [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s public-good property, and it is why growth theory and market-failure theory meet in §5.)*
>
> **So the long-run growth rate is a statement about ideas rather than about thrift**, and the policies that affect it — R&D, education, openness — are slower and harder than raising the saving rate.

**2. (Hard — convergence.)** (a) Compute the catch-up effect. (b) Why does the raw prediction fail in data? (c) How long is the long run, and what does that imply?

> [!example]- Solution
> **(a) The poorest country grows 25× faster.**
>
> *(Computed — identical countries differing only in starting capital, all heading to $k^*=8$:)*
>
> | starting $k$ | growth of $y$ |
> |---|---|
> | **0.50** | **+8.92%** |
> | 2.00 | +2.53% |
> | **6.00** | **+0.35%** |
>
> **Diminishing returns is the whole mechanism.** With almost no capital, the marginal product of capital is enormous, so each unit of investment yields a large output gain. **Near the steady state, investment barely exceeds depreciation and growth approaches zero.**
>
> **Convergence is therefore a *prediction* rather than an assumption** — and it accounts for post-war Japan, South Korea and China without requiring anything exceptional about them beyond starting poor with functioning institutions.
>
> **(b) Because countries converge to *their own* steady states.**
>
> *(Computed:)*
>
> | | $s$ | $A$ | $y^*$ |
> |---|---|---|---|
> | benchmark | 20% | 1.00 | **2.0000** |
> | low saving | 5% | 1.00 | 1.0000 |
> | weak institutions | 20% | **0.60** | **0.9295** |
>
> **A poor country with weak institutions is not far below a common steady state — it is *at* a low one.** It will not catch up until $s$ or $A$ changes, and no amount of waiting will help.
>
> **This is *conditional* convergence**, and the distinction between it and the raw version is the difference between a model that fits the data and one that is refuted by it. **The raw claim "poor countries grow faster" is false in the cross-section; "poor countries grow faster *given their own determinants*" holds up.**
>
> **⚠️ And note how much $A$ is carrying.** In this model $A$ is "technology", but a country's effective $A$ includes its institutions, property rights, corruption, and contract enforcement — **which is why §5's institutional levers are not a separate topic from the production function but an input to it.**
>
> **(c) Half the transition takes ~25 years, and it is still incomplete after a century.**
>
> *(Computed after a permanent rise in saving from 10% to 20%: **18.0%** of the way after 5 years, **32.4%** after 10, **67.4%** after 30, **97.1%** after 100.)*
>
> **So the statement "higher saving does not raise the long-run growth rate" is true and close to useless as practical advice.** **The transitional growth lasts decades — and decades are the horizon policy actually operates on.**
>
> **The general lesson is worth keeping beyond this chapter: a result about the *limit* of a process can be true while being irrelevant to every horizon anyone cares about.** *(Mankiw states this correctly — "reaching this long run can take quite a while" — but a reader who takes only the headline away gets the policy conclusion backwards.)*

**3. (Policy.)** (a) List the determinants and levers. (b) What links this chapter to [[04 - Externalities, Public Goods and Common Resources|ch. 04]]? (c) Why do small growth differences matter so much?

> [!example]- Solution
> **(a) Four determinants; nine levers.**
>
> **Determinants:** physical capital, human capital, natural resources *(least important in practice — Japan and Singapore are resource-poor and rich; several resource-rich countries are poor)*, and **technological knowledge, the only source of permanent growth.**
>
> **⚠️ Technology and human capital are distinct**: technology is society's knowledge; human capital is the resources spent transmitting it. **A textbook is technology; a graduate is human capital** — and they need different policies.
>
> **Levers**: saving and investment; investment from abroad; education; health and nutrition; property rights and political stability; free trade; population growth; research and development.
>
> **Three caveats worth carrying:** FDI raises **GDP more than GNP** (profits leave); **health and income cause each other**, so the direction of policy is not obvious; and **population growth dilutes capital per worker** — more people is not more prosperity.
>
> **(b) Four of the nine levers are [[04 - Externalities, Public Goods and Common Resources|ch. 04]] results.**
>
> | lever | ch. 04 concept |
> |---|---|
> | education | **positive externality** ⇒ underprovided |
> | R&D | **public good** — non-rival, hard to exclude ⇒ underprovided |
> | property rights | the **fix for market failure** — here the *precondition for growth* |
> | knowledge's non-rivalry | why ideas escape diminishing returns |
>
> **Growth policy is largely market-failure policy**, which is not obvious in advance and unifies two chapters that look unrelated.
>
> **The property-rights case is the sharpest.** **A country without enforceable contracts cannot accumulate capital whatever its saving rate** — so institutions enter the production function through $A$, and §3 showed that a lower $A$ means a permanently lower steady state rather than a temporary shortfall.
>
> **(c) Because compounding is much stronger than intuition suggests.**
>
> *(Computed:)*
>
> | growth | after 70 yrs | years to double |
> |---|---|---|
> | 1% | 2.01× | **69.7** |
> | 2% | 4.00× | 35.0 |
> | **4%** | **15.57×** | **17.7** |
>
> **The rule of 70**: doubling takes about $70/g$ years. *(And a country growing 2 points faster **overtakes one starting twice as rich in about 35 years**.)*
>
> **This is why [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]'s result is the most consequential thing in the micro half.** Wages track marginal product, so **productivity growth *is* the growth of living standards** — and over a few decades a percentage point of growth outweighs almost any feasible redistribution.
>
> **The honest tension, though, is §4's**: the policies that raise the growth rate work over generations, while the ones that raise the level work over decades and then stop. **Neither is fast, and the political system that must choose between them operates on a much shorter clock.**

## 📝 Summary

- **Living standards are determined by productivity** — and [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]] already established why, microeconomically: **wages track marginal product.**
- **$Y = A\,F(L,K,H,N)$ with constant returns**, so setting $x=1/L$ converts everything to **per-worker** terms. **That substitution is what makes growth theory about productivity.**
- **⚠️ A higher saving rate raises the *level* of income, not the long-run *growth rate*** *(computed: growth is **zero** at every saving rate from 5% to 40%)*.
- **And the level gain diminishes sharply: $y^*\propto\sqrt{s}$** *(computed: doubling the saving rate raises output per worker only **1.414×**; quadrupling is needed to double it)*.
- **⚠️ Only technology produces permanent growth** *(computed: $y^*\propto A^{1.50}$, so 2%/yr technology growth gives **3.01%/yr** forever — amplified 1.5× because higher $A$ also raises capital)*. **Capital faces diminishing returns; ideas do not.**
- **⚠️ The catch-up effect, computed: a country at $k=0.5$ grows 25× faster than an identical one at $k=6$.** Convergence is a **prediction** of the model.
- **⚠️ But "other things equal" does all the work.** *(Computed: $y^*$ = **2.00 / 1.00 / 0.93** for the benchmark, low-saving and weak-institution cases.)* **This is *conditional* convergence — countries converge to their own steady state**, which is why the raw prediction fails in data while the model survives.
- **⚠️ The transition is half done in ~25 years and incomplete after a century** *(computed: 18.0% after 5 years, 67.4% after 30, 97.1% after 100)*. **"Saving doesn't raise the long-run growth rate" is true and nearly useless over a human lifetime.**
- **Determinants: physical capital, human capital, natural resources (least important), technology (the only permanent source).** **A textbook is technology; a graduate is human capital.**
- **⚠️ Four of Mankiw's nine policy levers are [[04 - Externalities, Public Goods and Common Resources|ch. 04]] results** — education's externality, R&D as a public good, property rights, and knowledge's non-rivalry. **Growth policy is largely market-failure policy.**
- **Property rights are the precondition for growth**, not merely a fix for market failure — institutions enter through $A$, so weak institutions mean a permanently *lower steady state*, not a temporary shortfall.
- **Caveats: FDI raises GDP more than GNP; health and income cause each other; population growth dilutes capital per worker.**
- **⚠️ The rule of 70** *(computed: doubling takes 69.7 years at 1% and 17.7 at 4%; growing 2 points faster overtakes a twice-as-rich country in **35 years**)*.
- **Productivity growth *is* the growth of living standards** — and over decades it outweighs almost any feasible redistribution.

## ⚠️ Important Notes

1. **Constant returns ⇒ divide by $L$.** Growth theory is about *per-worker* quantities.
2. **A country can raise total output by having more people.** That is not growth in the sense that matters.
3. **⚠️ Saving raises the level, not the long-run growth rate.**
4. **⚠️ $y^*\propto\sqrt{s}$** — quadruple the saving rate to double income. The returns to thrift are sharply limited.
5. **⚠️ Only technology growth is permanent**, because ideas are non-rival and escape diminishing returns.
6. **⚠️ Poor countries grow faster *given the same determinants*** — the catch-up effect is a prediction.
7. **⚠️ Convergence is *conditional*.** Countries converge to their own steady state; the unconditional claim is false in data.
8. **Institutions enter through $A$** — so weak institutions mean a permanently lower steady state, not a lag.
9. **⚠️ The transition takes decades.** A limit result can be true and irrelevant to every horizon anyone cares about.
10. **Technology ≠ human capital.** Knowledge versus the resources that transmit it.
11. **Natural resources matter least.** Resource-poor Japan and Singapore are rich.
12. **⚠️ Growth policy is largely market-failure policy** — four of nine levers are [[04 - Externalities, Public Goods and Common Resources|ch. 04]] concepts.
13. **FDI raises GDP more than GNP.** Ask which is being quoted.
14. **Population growth dilutes capital per worker.**
15. **⚠️ Rule of 70: doubling takes $70/g$ years.** Small growth differences compound enormously.
16. **Productivity growth is the growth of living standards** ([[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]) — the most consequential number in the subject.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located the chapter precisely** *(Macro 2017, PDF pp. 262–287)*.
>
> **⚠️ THE OPERATOR CIPHER applies** — the production function extracts as `Y 5 AF(L, K, H, N )` and the constant-returns condition as `xY 5 AF(xL, xK, xH, xN )`. **Nothing was transcribed.** *(This chapter also shows a second fault clearly: **word-fragment duplication**, as in "`Y denotes the quantity of Y denotes the quantity of Y`" and "`F( ) is a function that shows how the inputs are combined to F( ) is a function...`". The text is recoverable but must be read, not copied.)*
>
> **⚠️ Every figure is lost**, including the international growth-rate comparisons and the productivity time series. **This chapter is unusually prose-heavy and has no data tables**, so — unlike [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]] — **there was nothing tabular to verify against.** All figures here are from a model I state explicitly.
>
> **No erratum.** Every qualitative claim Mankiw makes is reproduced by the simulation.
>
> **Additions beyond the source.**
>
> - **⚠️ §§2–4 are the chapter's main addition and are entirely mine.** **Mankiw asserts three things and computes none of them**: that a higher saving rate raises the level but not the growth rate; that poorer countries grow faster; and that the transition "can take quite a while". **A Solow-style accumulation model ($y = Ak^{1/3}$, $\Delta k = sy - \delta k$) settles all three**, and the specific findings — **zero long-run growth at every saving rate**, **$y^*\propto\sqrt{s}$**, **a 25× growth-rate gap between the poorest and richest starting points**, and **a transition half-complete after 25 years and 97.1% complete after 100** — are not in the source.
> - **⚠️ The distinction between *unconditional* and *conditional* convergence is mine**, and it matters: **Mankiw states the catch-up effect with the qualifier "other things being equal" and does not show what happens when they are not.** Computing three different steady states (2.00 / 1.00 / 0.93) shows why the raw prediction fails in cross-country data while the model survives — **and that a weak-institution country is *at* a low steady state rather than below a common one.**
> - **The amplification result** — that $y^*\propto A^{1/(1-\alpha)}$, so technology growth is magnified 1.5× in the steady state — is a property of the specification used here and is stated as such. *(Corrected during drafting: my first pass claimed output grows at $g$, which contradicted the computed 3.01%.)*
> - **⚠️ §5's observation that four of Mankiw's nine policy levers are [[04 - Externalities, Public Goods and Common Resources|ch. 04]] results** — education's externality, R&D as a public good, property rights, and knowledge's non-rivalry — **is my cross-chapter synthesis.** Mankiw lists the levers without noting that growth policy is largely market-failure policy.
> - **The reading of $A$ as "institutions as much as technology"**, which makes §3's third row meaningful, is mine.
> - **§6's compounding table and the rule of 70** are standard, but **the link back to [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]** — that wages track marginal product, so productivity growth *is* the growth of living standards — **is the connection that makes this chapter follow from the micro half rather than starting afresh.**
> - **The closing tension in Exercise 3(c)** — that level-raising policies work over decades and growth-raising policies over generations, while politics operates on neither horizon — is mine.
>
> **Deliberately compressed.** **Mankiw's international comparison table of growth rates and living standards** is a data exhibit whose analytical content is §6's compounding point. **The extended case studies** (the productivity slowdown, "Are Natural Resources a Limit to Growth?", the Malthus and Solow–Romer boxes, and the discussion of foreign aid) are represented by their conclusions. **The "FYI: The Production Function" box** is used directly in §1. **The debate over whether population growth helps or hinders** (the dilution effect against Kremer's scale effect on ideas) is compressed to the dilution point; the second half belongs with endogenous-growth material beyond this course. **Formal Solow-model derivations** — the golden rule, the phase diagram, convergence speed — are beyond Mankiw's scope and are not introduced; only the minimum needed to compute his own claims is used.

**Previous:** [[08 - Measuring the Macroeconomy - GDP and the Cost of Living]] · **Next:** [[10 - Saving, Investment and the Financial System]]
