---
subject: Macroeconomics & Microeconomics
chapter: 7
tags: [ds, economics, microeconomics, labour, marginal-product, consumer-choice, indifference-curves, giffen]
source: "Mankiw, *Principles of Microeconomics* 6e, ch. 18 and 21"
---

# Factor Markets and the Theory of Consumer Choice

**This chapter closes the micro half by going underneath both curves.** [[05 - Production Costs and Competitive Markets|Ch. 05]] derived supply from costs; **§1–2 derive where those costs come from — the labour market.** [[02 - Supply, Demand and Elasticity|Ch. 02]] took demand as given; **§3–6 derive it from the consumer's choice problem.**

**Four results.**

**§2 — "hire until $VMPL = W$" and "produce until $P = MC$" are the *same equation*.** Mankiw calls them "two sides of the same coin" and stops. *(Two lines of algebra plus a numerical check on his own table: the firm stops at 3 workers, where implied $MC = \$8.33 < \$10$, and refuses a fourth at $MC = \$12.50$. **Same answer, same reason.**)*

**§4 — the tangency condition is a Lagrange first-order condition.** *(Solved: with $U=\sqrt{xy}$ the optimum is **50 pizzas and 250 pints** — exactly Mankiw's "point C", which he describes as "the middle of the line" without ever saying what preferences put a consumer there.)*

**§5 — the income and substitution effects, decomposed numerically.** *(Computed: a Pepsi price fall moves pizza **−14.6447 then +14.6447 — exactly cancelling** — while Pepsi rises **+103.55 then +146.45 = +250**.)*

**§6 — a Giffen good, constructed rather than described.** *(Computed: the potato price rises \$1.00 → \$1.50 and potato consumption rises **4.0000 → 5.7143**. A genuinely upward-sloping demand curve from entirely standard behaviour.)*

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]] for the operator cipher.

## 📘 Main Knowledge

### 1. The firm's demand for labour

*(Verified — Mankiw's Table 1: apples at \$10/bushel, wage \$500/week:)*

| $L$ | $Q$ | $MPL$ | **$VMPL = P\times MPL$** | $W$ | $\Delta$profit | hire? |
|---|---|---|---|---|---|---|
| 1 | 100 | 100 | **1 000** | 500 | +500 | **yes** |
| 2 | 180 | 80 | **800** | 500 | +300 | **yes** |
| **3** | 240 | 60 | **600** | 500 | **+100** | **yes** |
| 4 | 280 | 40 | 400 | 500 | −100 | no |
| 5 | 300 | 20 | 200 | 500 | −300 | no |

**The firm hires 3 workers** — the third adds \$600 of revenue for \$500 of wage; a fourth would add \$400 for \$500.

$$\textbf{hire until } VMPL = W$$

> [!note] The VMPL curve *is* the labour demand curve
> **$MPL$ falls (100, 80, 60, 40, 20) — diminishing marginal product, [[05 - Production Costs and Competitive Markets|ch. 05]]'s assumption seen from the input side.** So $VMPL$ falls too, and **at any wage you read off the labour demanded where $VMPL = W$.** That downward slope is the entire content of "labour demand."
>
> **Shifts come from anything that raises $VMPL$**: a higher output price, better technology, or more capital per worker.

### 2. ⚠️ Factor demand and output supply are one rule

**Mankiw says the two decisions are "two sides of the same coin" and leaves it. The algebra is two lines:**

$$\text{hire until } P\cdot MPL = W \;\Longrightarrow\; P=\frac{W}{MPL}$$

**And $W/MPL$ *is* marginal cost** — one more unit of output requires $1/MPL$ extra workers, each costing $W$. So:

$$\boxed{P = MC}$$

**[[05 - Production Costs and Competitive Markets|Ch. 05]]'s rule, unchanged.** *(Verified numerically on Mankiw's own table:)*

| $L$ | $MPL$ | implied $MC = W/MPL$ | $P$ | |
|---|---|---|---|---|
| 1 | 100 | \$5.00 | \$10 | produce more |
| 2 | 80 | \$6.25 | \$10 | produce more |
| **3** | 60 | **\$8.33** | \$10 | **produce more — stop here** |
| 4 | 40 | **\$12.50** | \$10 | **no** |

**The firm stops at $L=3$ either way. Same answer, same reason.**

> [!warning] There is no separate "theory of factor demand"
> **Labour demand is *derived* demand** — the firm wants workers only for the output they produce. **So the labour market is the output market seen from the input side**, and the two rules cannot disagree because they are one rule written twice.
>
> **Two consequences fall straight out:**
> - **Anything that raises the output price raises labour demand** — which is why wages in a booming industry rise without any change in workers' skills.
> - **Anything that raises productivity raises labour demand.** **That is why wages track productivity** — [[09 - Production and Growth|ch. 09]]'s central macro fact, arriving here first and for a microeconomic reason.
>
> **The same logic applies to every factor**: land and capital are also paid their marginal products, so **factor prices are determined by marginal productivity, and the distribution of income is a by-product of production technology.** *(Which is a genuine claim about how the world works, not a normative one — and Mankiw is careful to say the theory explains what wages *are*, not what they *should* be.)*

### 3. The budget constraint

*(Verified — Mankiw's Figure 1 table, income \$1 000, pizza \$10, Pepsi \$2/pint: **all 11 bundles cost exactly \$1 000**.)*

| pizzas | pints | on pizza | on Pepsi | total |
|---|---|---|---|---|
| 100 | 0 | 1 000 | 0 | **1 000** |
| 50 | 250 | 500 | 500 | **1 000** |
| 0 | 500 | 0 | 1 000 | **1 000** |

$$\text{slope}=-\frac{500}{100}=-5=-\frac{P_{\text{pizza}}}{P_{\text{Pepsi}}}=-\frac{10}{2}$$

> [!note] The slope is the relative price — and the opportunity cost
> **The budget line's slope is the rate at which the *market* lets you trade one good for the other**: give up one pizza, get 5 pints.
>
> **That is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s opportunity cost in consumption space** — and the exact analogue of the production possibilities frontier's slope. **Same object, different setting.**

### 4. ⚠️ The optimum is a constrained optimisation

**Indifference curves** connect bundles giving equal satisfaction. They slope down, never cross, and are **bowed inward** — because people prefer balanced bundles, so the **marginal rate of substitution** (how much Pepsi you would trade for one pizza) falls as you get more pizza.

**The consumer picks the highest curve the budget allows — the tangency point:**

$$MRS=\frac{P_x}{P_y}$$

> [!note] Mankiw states this geometrically. It is a Lagrange condition. *(Addition.)*
> $$\max U(x,y)\quad\text{s.t.}\quad P_x x+P_y y=M$$
> $$\mathcal{L}=U(x,y)-\lambda(P_x x+P_y y-M)$$
> $$\frac{\partial\mathcal{L}}{\partial x}=U_x-\lambda P_x=0,\qquad \frac{\partial\mathcal{L}}{\partial y}=U_y-\lambda P_y=0$$
> $$\Longrightarrow\;\frac{U_x}{U_y}=\frac{P_x}{P_y}\qquad\text{and }\frac{U_x}{U_y}\text{ *is* the MRS}$$
>
> **Equivalently $\dfrac{U_x}{P_x}=\dfrac{U_y}{P_y}=\lambda$ — "the marginal utility per dollar is equal across goods."** If it were not, you could shift a dollar toward the higher one and gain.
>
> **This is [[Optimization/contents/00-Index|Optimization]] ch. 11's constrained optimisation, exactly**, and $\lambda$ is the marginal utility of income. **Mankiw is deliberately calculus-free, so recognising the tangency picture as a first-order condition is genuine enrichment for this reader** — it makes the result computable rather than merely visual.

*(Solved concretely with $U=\sqrt{xy}$: $MRS = y/x$, so tangency gives $y = 5x$; the budget then gives $x=\mathbf{50}$, $y=\mathbf{250}$ — **\$500 on each good.**)*

> [!note] That is exactly Mankiw's point C
> **He marks (50 pizzas, 250 pints) as "the middle of the line" where spending is equal, and never says what preferences would put a consumer there.** Equal-weight Cobb-Douglas does — **and it is worth knowing that "spend a constant share of income on each good" is a *property of a particular utility function*, not a general law.**

### 5. ⚠️ Income and substitution effects, decomposed

**A price change does two things at once**, and separating them is the chapter's main analytical tool.

*(Computed — the Pepsi price falls from \$2 to \$1:)*

| | pizza | Pepsi |
|---|---|---|
| start | 50.000 | 250.000 |
| **compensated** *(same utility, new prices)* | **35.355** | **353.553** |
| final | 50.000 | 500.000 |

| effect | pizza | Pepsi |
|---|---|---|
| **substitution** | **−14.6447** | **+103.5534** |
| **income** | **+14.6447** | **+146.4466** |
| **total** | **0.0000** | **+250.0000** |

> [!warning] The two effects can reinforce or cancel
> **Pepsi:** both push the same way. It is relatively cheaper (substitute toward it) *and* you are effectively richer (buy more of a normal good). **+250 in total.**
>
> **Pizza:** they **exactly cancel**. You substitute away from pizza — now relatively dearer — but the price fall made you richer, so you buy more. *(With this utility function the two are precisely equal; that is a property of Cobb-Douglas, not a general result.)*
>
> **⚠️ The asymmetry that matters: the substitution effect *always* points toward the good that got cheaper. The income effect can go either way** — it depends on whether the good is normal or inferior.
>
> **That asymmetry is the entire content of §6**, and it is also why demand curves slope down *almost* always rather than always.

### 6. ⚠️ A Giffen good, constructed

**Mankiw describes Giffen goods and calls them "a theoretical curiosity". Here is one built explicitly.**

**A consumer must reach 1 000 calories on \$20.** Potatoes give 100 calories at price $p$ (cheap calories); meat gives 150 at \$4 (preferred, but dear). **They buy as much meat as they can afford while still hitting 1 000 calories.**

*(Computed — every row hits exactly 1 000 calories and spends exactly \$20:)*

| potato price | **potatoes** | meat | |
|---|---|---|---|
| \$1.00 | **4.0000** | 4.0000 | |
| \$1.10 | **4.2553** | 3.8298 | ↑ |
| \$1.20 | **4.5455** | 3.6364 | ↑ |
| \$1.35 | **5.0633** | 3.2911 | ↑ |
| \$1.50 | **5.7143** | 2.8571 | ↑ |

> [!warning] The price rose and consumption rose with it
> **An upward-sloping demand curve, produced by entirely standard, rational behaviour.**
>
> **The mechanism:** potatoes are **inferior** (more income ⇒ fewer potatoes) *and* they take a **large share of the budget**. When their price rises, the consumer is effectively poorer, can no longer afford meat, and **must fall back on the cheap calorie source — buying more potatoes.**
>
> **The negative income effect outweighs the always-positive substitution effect.**
>
> **Both conditions are necessary**, which is why Giffen goods are *rare* rather than impossible: **an inferior good that is a small share of spending cannot manage it, however inferior it is.** The income effect simply has too little to work with.

### 7. Two applications the apparatus settles — by declining to

> [!note] Does a higher wage increase hours worked?
> **The choice is between consumption and leisure, and the wage is the *price of leisure*.**
>
> - **substitution effect** — leisure is dearer ⇒ **work more**
> - **income effect** — you are richer ⇒ buy more leisure ⇒ **work less**
>
> **They oppose, so the answer is genuinely ambiguous, and a *backward-bending* labour supply curve is possible.** **Mankiw notes that over the last century hours worked *fell* as wages rose — the income effect won.**

> [!note] Do higher interest rates increase saving?
> **The choice is between consumption now and later, and the interest rate is the price of consuming now.**
>
> - **substitution effect** — future consumption is cheaper ⇒ **save more**
> - **income effect** — a saver is richer ⇒ consume more now ⇒ **save less**
>
> **Ambiguous again — and this one matters for [[10 - Saving, Investment and the Financial System|ch. 10]], whose loanable-funds model usually *assumes* an upward-sloping saving curve.** The assumption is a convenience, not a theorem.

> [!warning] Notice how often the two effects oppose
> **In both applications the theory's honest answer is "it depends which effect dominates", and that is an empirical question.**
>
> **This is worth carrying beyond the chapter**: a great many policy debates cannot be settled from theory alone, **not because the theory is weak but because it correctly identifies two forces pointing opposite ways.** Demanding a sign from a model that does not determine one is how confident wrong answers get made.

## ✏️ Exercises

**1. (Factor markets.)** (a) How does a firm decide how much labour to hire? (b) Show this is the same as $P = MC$. (c) What shifts labour demand, and what does the theory claim about wages?

> [!example]- Solution
> **(a) Hire until the value of the marginal product equals the wage.**
>
> $$VMPL = P\times MPL,\qquad \text{hire until } VMPL = W$$
>
> *(Verified on Mankiw's Table 1: the firm hires **3 workers** — the third adds \$600 for a \$500 wage; a fourth would add \$400.)*
>
> **$MPL$ falls (100, 80, 60, 40, 20) by diminishing marginal product, so $VMPL$ falls, so labour demand slopes down.** **The $VMPL$ curve *is* the labour demand curve.**
>
> **(b) Divide the hiring rule by $MPL$.**
>
> $$P\cdot MPL=W\;\Longrightarrow\;P=\frac{W}{MPL}=MC$$
>
> **because producing one more unit needs $1/MPL$ extra workers at $W$ each.**
>
> *(Verified numerically: implied $MC$ runs \$5.00, \$6.25, **\$8.33**, \$12.50, \$25.00 against a price of \$10 — the firm stops at $L=3$ exactly where the hiring rule said.)*
>
> **So there is no separate theory of factor demand.** Labour demand is **derived** demand — the firm wants workers only for their output — **and the labour market is the output market viewed from the other side.**
>
> **This is why the two rules can never conflict**: they are one equation written twice, and Mankiw's "two sides of the same coin" is literally true rather than a figure of speech.
>
> **(c) Anything raising $VMPL$ — and the theory explains wages without justifying them.**
>
> **Labour demand shifts with:**
> - **the output price** — a booming industry pays more without any change in workers' skills;
> - **technology** — better methods raise $MPL$;
> - **the quantity of other factors** — more capital per worker raises $MPL$.
>
> **⚠️ And the same argument applies to every factor.** Land and capital are also paid their marginal products, so **factor prices are determined by marginal productivity and the distribution of income is a by-product of production technology.**
>
> **The strongest consequence: wages track productivity.** *(This is [[09 - Production and Growth|ch. 09]]'s central macro fact, and it arrives here for a purely microeconomic reason — a firm will not pay more than a worker adds, and competition will not let it pay less.)*
>
> **Mankiw is careful about the normative limit, and it is worth repeating: the theory explains what wages *are*, not what they *ought to be*.** A worker's marginal product depends on the capital they work with, the technology available and the price of the output — **none of which is their doing.** *(This is exactly [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s positive/normative distinction, and the place where it is easiest to slip.)*

**2. (Hard — consumer choice.)** (a) What is the budget constraint's slope? (b) State the optimum and solve it. (c) Decompose a price change. (d) What determines whether both effects agree?

> [!example]- Solution
> **(a) The relative price — and it is an opportunity cost.**
>
> *(Verified: all 11 of Mankiw's bundles cost exactly \$1 000, and the slope is $-500/100 = -5 = -P_{\text{pizza}}/P_{\text{Pepsi}}$.)*
>
> **Give up one pizza and the market gives you 5 pints.** That is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s opportunity cost, now in consumption space — **the exact analogue of the PPF's slope in production space.**
>
> **(b) Tangency: $MRS = P_x/P_y$, which is a Lagrange condition.**
>
> **The consumer reaches the highest indifference curve the budget allows, and that is where the curve just touches the line.** If the slopes differed, the consumer could move along the budget line onto a higher curve.
>
> $$\mathcal{L}=U(x,y)-\lambda(P_x x+P_y y-M)\;\Longrightarrow\;\frac{U_x}{U_y}=\frac{P_x}{P_y}\;\Longleftrightarrow\;\frac{U_x}{P_x}=\frac{U_y}{P_y}$$
>
> **The second form is the memorable one: equalise the marginal utility per dollar across goods.** If a dollar spent on pizza yielded more utility than a dollar on Pepsi, you would move a dollar.
>
> *(Solved with $U=\sqrt{xy}$: $MRS = y/x = 5$, so $y = 5x$, and the budget gives **$x=50$, $y=250$** — \$500 on each.)*
>
> **That is precisely Mankiw's point C**, which he marks as "the middle of the line" **without saying what preferences put a consumer there.** Equal-weight Cobb-Douglas does — **and it is worth knowing that "constant expenditure shares" is a property of one utility function, not a general law.**
>
> **This connects the chapter to [[Optimization/contents/00-Index|Optimization]] ch. 11 directly**, with $\lambda$ interpretable as the marginal utility of income. **Mankiw's geometry is correct and cannot compute; the Lagrange version can.**
>
> **(c) Substitution first, then income.**
>
> *(Computed — Pepsi falls \$2 → \$1:)*
>
> | | pizza | Pepsi |
> |---|---|---|
> | substitution | **−14.6447** | +103.5534 |
> | income | **+14.6447** | +146.4466 |
> | **total** | **0.0000** | **+250.0000** |
>
> **The substitution effect is found by asking what the consumer would buy at the *new relative prices* while held at the *old utility level*** — the compensated bundle (35.355, 353.553), which costs only \$707.11 at the new prices. **The income effect is the rest of the move**, reflecting the \$292.89 of purchasing power the price fall released.
>
> **Pizza's two effects exactly cancel here** — a Cobb-Douglas property, not a general one.
>
> **(d) Whether the good is normal or inferior.**
>
> **⚠️ The substitution effect always points toward the good that became cheaper.** It is a pure relative-price response and its sign is fixed by the shape of indifference curves.
>
> **The income effect has no fixed sign.** A price fall raises real income; whether that raises or lowers consumption of the good depends on whether it is **normal** (+) or **inferior** (−).
>
> | good | substitution | income | total |
> |---|---|---|---|
> | **normal** | + | + | **+ always** |
> | **inferior**, small budget share | + | − (small) | **+** |
> | **inferior**, large budget share | + | **− (large)** | **can be −** ⇒ **Giffen** |
>
> **So the law of demand is *almost* a theorem** — it can only fail through a large negative income effect, which is §6.

**3. (Giffen goods and applications.)** (a) Construct a Giffen good. (b) Why are they rare? (c) Why can't the theory say whether higher wages raise hours worked?

> [!example]- Solution
> **(a) An inferior good with a large budget share.**
>
> *(Computed — 1 000 calories required on \$20; potatoes 100 cal at price $p$, meat 150 cal at \$4:)*
>
> | potato price | **potatoes bought** |
> |---|---|
> | \$1.00 | **4.0000** |
> | \$1.20 | **4.5455** |
> | \$1.50 | **5.7143** |
>
> **The price rose 50% and consumption rose 43%.** *(Every row hits exactly 1 000 calories and spends exactly \$20 — verified.)*
>
> **The mechanism: when potatoes get dearer, the consumer can no longer afford meat, and must meet the calorie requirement from the cheap source.** They give up meat and buy **more** potatoes.
>
> **Nothing irrational happens.** The consumer is optimising throughout; **the demand curve slopes up because the income effect is negative and large.**
>
> **(b) Because two demanding conditions must hold at once.**
>
> 1. **The good must be inferior** — real income up ⇒ consumption down. Rules out most goods.
> 2. **It must absorb a large share of spending** — otherwise the income effect is too small to overturn the substitution effect, **however inferior the good is.**
>
> **The second condition is the binding one**, and it explains the historical examples: staple foods for very poor households, where a single cheap calorie source dominates the budget.
>
> **⚠️ And it is why "Giffen good" is not a loophole in the law of demand so much as a boundary case that proves the law's structure**: demand slopes down unless a large negative income effect overwhelms the substitution effect, and that requires poverty plus concentration of spending.
>
> **(c) Because the two effects oppose, and the theory does not say which wins.**
>
> **Leisure is a good, and the wage is its price.** A wage rise makes leisure dearer (**substitution: work more**) and makes you richer (**income: buy more leisure, work less**).
>
> **The supply curve of labour can therefore bend backwards**, and **Mankiw notes that hours worked fell over the last century as wages rose — so historically the income effect won.**
>
> **The same structure governs saving** (§7): a higher interest rate makes future consumption cheaper (**save more**) and makes savers richer (**save less**). **This one matters for [[10 - Saving, Investment and the Financial System|ch. 10]], which assumes an upward-sloping saving curve** — a convenience rather than a result.
>
> **⚠️ The general lesson is the one to keep.** The honest answer is "it depends which effect dominates", and that is empirical. **A model that identifies two opposing forces has done its job; demanding a sign from it anyway is how confident wrong answers get made** — and it is a good reason to be suspicious of any policy argument that claims theory settles a question of this shape.

## 📝 Summary

- **Factor markets and consumer choice are what lie underneath the supply and demand curves** used since [[02 - Supply, Demand and Elasticity|ch. 02]].
- **A firm hires until $VMPL = P\times MPL = W$** *(verified on Mankiw's Table 1: it hires **3 workers** — the third adds \$600 for a \$500 wage)*. **The $VMPL$ curve is the labour demand curve.**
- **⚠️ "$VMPL = W$" and "$P = MC$" are the same equation** — divide by $MPL$ and $W/MPL$ *is* marginal cost. *(Verified: implied $MC$ = \$5.00, \$6.25, **\$8.33**, \$12.50 against $P=\$10$ — the firm stops at $L=3$ either way.)*
- **So factor demand is *derived* demand** — the labour market is the output market seen from the input side, and the two rules cannot disagree.
- **⚠️ Wages track productivity** because anything raising $MPL$ raises labour demand — **[[09 - Production and Growth|ch. 09]]'s central macro fact, arriving here for a microeconomic reason.**
- **Every factor is paid its marginal product**, so the distribution of income is a by-product of production technology. **The theory explains what wages *are*, not what they ought to be.**
- **The budget constraint's slope is the relative price** *(verified: all 11 bundles cost exactly \$1 000; slope $-5 = -P_x/P_y$)* — **[[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s opportunity cost in consumption space.**
- **⚠️ The optimum is where $MRS = P_x/P_y$ — a Lagrange first-order condition**, equivalently $U_x/P_x = U_y/P_y$: **equalise marginal utility per dollar.** *(This is [[Optimization/contents/00-Index|Optimization]] ch. 11; Mankiw is calculus-free.)*
- *(Solved: $U=\sqrt{xy}$ gives **50 pizzas and 250 pints** — **exactly Mankiw's point C**, which he never explains in terms of preferences. "Constant expenditure shares" is a Cobb-Douglas property, not a law.)*
- **⚠️ A price change decomposes into substitution and income effects** *(computed for a Pepsi price fall: pizza **−14.6447 then +14.6447**, exactly cancelling; Pepsi **+103.55 then +146.45 = +250**)*.
- **⚠️ The substitution effect always points toward the cheaper good; the income effect can go either way.** That asymmetry is the whole reason demand curves slope down *almost* always.
- **⚠️ A Giffen good, constructed** *(computed: potato price \$1.00 → \$1.50, consumption **4.0000 → 5.7143**, with every row hitting 1 000 calories on \$20)*. **The price rose and consumption rose — from entirely rational behaviour.**
- **It needs an inferior good *and* a large budget share.** The second condition is the binding one, which is why Giffen goods are rare rather than impossible.
- **Higher wages have an ambiguous effect on hours worked** — substitution says work more, income says less. **Backward-bending supply is possible, and Mankiw notes hours *fell* as wages rose over the last century.**
- **Higher interest rates have an ambiguous effect on saving** — which matters because [[10 - Saving, Investment and the Financial System|ch. 10]] *assumes* an upward-sloping saving curve.
- **⚠️ Notice how often the two effects oppose.** "It depends which dominates" is an honest answer and an empirical question — **demanding a sign from a model that does not determine one is how confident wrong answers get made.**

## ⚠️ Important Notes

1. **$VMPL = P \times MPL$** — convert the marginal product into money before comparing it to the wage.
2. **⚠️ The $VMPL$ curve is the labour demand curve.** Its downward slope comes from diminishing marginal product.
3. **⚠️ "$VMPL = W$" and "$P = MC$" are one rule.** Never treat factor demand as a separate theory.
4. **Factor demand is derived demand** — it shifts with the output price and with productivity.
5. **⚠️ Wages track productivity, and this is a microeconomic result** before it is a macro one.
6. **Marginal-productivity theory is positive, not normative.** A worker's marginal product depends on capital and technology they did not choose.
7. **The budget line's slope is the relative price** — and the opportunity cost of one good in units of the other.
8. **⚠️ The tangency $MRS = P_x/P_y$ is a Lagrange condition**; the useful form is $U_x/P_x = U_y/P_y$.
9. **Constant expenditure shares is a Cobb-Douglas property**, not a general law.
10. **⚠️ Always decompose a price change into substitution and income effects** before predicting the direction.
11. **⚠️ The substitution effect has a fixed sign; the income effect does not.**
12. **Normal goods: both effects agree. Inferior goods: they oppose.**
13. **⚠️ Giffen requires inferiority *and* a large budget share.** Inferiority alone is not enough.
14. **The law of demand is almost a theorem** — it fails only through a large negative income effect.
15. **⚠️ Labour supply can bend backwards**, and historically the income effect has dominated.
16. **[[10 - Saving, Investment and the Financial System|Ch. 10]]'s upward-sloping saving curve is an assumption**, not a result of this theory.
17. **⚠️ When two effects oppose, say so.** The model's refusal to give a sign is information, not a failure.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located both chapters** *(Micro 6e, PDF pp. 401–422 for ch. 18 and pp. 465–492 for ch. 21)*. **Per the deduplication rule in [[00-Index]], micro chapters 10–22 come from the Micro 6e volume.**
>
> **⚠️ BOTH TABLES SURVIVED EXTRACTION COMPLETELY** — ch. 18's Table 1 (labour, output, $MPL$, $VMPL$, wage, marginal profit) and ch. 21's Figure 1 budget-constraint schedule (all 11 bundles). **This is now the third and fourth Mankiw table to come through whole** *(after [[05 - Production Costs and Competitive Markets|ch. 05]]'s costs and [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]'s revenue)*, and it confirms the rule settled in [[Commercial Banking/contents/00-Index|Commercial Banking]]: **graphical exhibits are lost; numeric tables set as text survive.**
>
> **⚠️ THE OPERATOR CIPHER applies** — see [[00-Index]]. Table 1's header shows it plainly: `MPL =∆Q/∆L` and `VMPL = P × MPL` came through, but **nothing was transcribed** — every relationship was reconstructed and verified against the tabulated values.
>
> **⚠️ Every figure is lost, and ch. 21 is the most figure-dependent chapter in the micro half.** **The indifference-curve diagrams, the tangency picture, the income/substitution decomposition (which is *only* ever shown as a shifted budget line), the Giffen-good panel, and the labour-supply and saving diagrams are all images.** What survives is captions and axis labels.
>
> **This is precisely why §§4–6 solve the problems algebraically rather than describing pictures** — and the algebra reproduces Mankiw's own point C exactly, which is what makes the reconstruction verified rather than assumed.
>
> **No erratum.** Every value Mankiw tabulates or states reproduces exactly.
>
> **Additions beyond the source.**
>
> - **⚠️ §2's demonstration that $VMPL = W$ and $P = MC$ are one equation is mine.** **Mankiw calls them "two sides of the same coin" and does not show it.** The algebra plus the numerical check on his own table (implied $MC$ = \$8.33 at $L=3$, \$12.50 at $L=4$) makes the claim verifiable, and the consequence — **wages track productivity, for a microeconomic reason, before [[09 - Production and Growth|ch. 09]] makes it a macro fact** — is an addition.
> - **⚠️ §4's Lagrange formulation is mine and is the strongest [[Optimization/contents/00-Index|Optimization]] cross-link in the subject.** **Mankiw presents tangency purely geometrically.** Solving $U=\sqrt{xy}$ and recovering **exactly his point C** shows what preferences his unexplained "middle of the line" corresponds to — and that constant expenditure shares is a property of one utility function rather than a general law.
> - **⚠️ §5's numerical decomposition is mine.** Mankiw shows the decomposition only as a shifted budget line in a lost figure. **Computing the compensated bundle (35.355, 353.553) and its \$707.11 cost turns a picture into arithmetic**, and exposes that pizza's two effects cancel *exactly* — a Cobb-Douglas artefact worth flagging as such.
> - **⚠️ §6's constructed Giffen good is mine.** **Mankiw describes the concept and calls it "a theoretical curiosity" without producing one.** The calorie-constrained model yields a genuinely upward-sloping demand curve from rational behaviour, and makes clear that **the large-budget-share condition is the binding one.**
> - **The observation in §7 that [[10 - Saving, Investment and the Financial System|ch. 10]]'s upward-sloping saving curve is an assumption this chapter cannot justify** is mine, as is the closing note that **a model identifying two opposing forces has done its job.**
>
> **Deliberately compressed.** **Mankiw ch. 18's treatment of land and capital markets** is compressed to §2's note that every factor is paid its marginal product — the analysis is identical to labour's with the names changed. **The equilibrium in the labour market and the linkage among factors** are summarised rather than worked. **Ch. 18's "Monopsony" appendix** is noted only in passing; it is the mirror of [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]'s monopoly with the same structure. **Ch. 21's four applications** are represented by the two in §7 that have the clearest analytical content; the demand-curve derivation and the Giffen discussion are absorbed into §§5–6. **⚠️ Micro ch. 19 (Earnings and Discrimination) and ch. 20 (Income Inequality) are excluded from this subject's scope** — see [[00-Index]]'s omissions table, which notes that ch. 19's measurement problem is properly an [[Econometrics/contents/00-Index|econometrics]] topic.

**Previous:** [[06 - Monopoly, Oligopoly and Monopolistic Competition]] · **Next:** [[08 - Measuring the Macroeconomy - GDP and the Cost of Living]] *(macro begins)*
