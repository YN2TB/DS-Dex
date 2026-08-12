---
subject: Principle of Accounting
chapter: 07
tags: [ds, accounting, inventory, fifo, lifo, average-cost, lcnrv, inventory-errors]
source: "documents/slides/ch06.pptx (Doan Thuy Duong, SAA); Weygandt, Kimmel & Kieso, *Accounting Principles*, 13th ed., Ch. 6"
---

# Inventories

> [!abstract] Where this sits in the course
> [[06 - Accounting for Merchandising Operations]] left one figure undefined. The cost-of-goods-sold formula depends on **ending inventory** — but if you bought identical goods at three different prices, **which cost belongs to the units sold and which to the units left?**
>
> That single question is this entire chapter. The answer changes reported profit, reported assets, and the tax bill, without any difference in what physically happened. It is the clearest illustration in the whole course that **accounting numbers depend on assumptions, not just facts.**

---

## 📘 Main Knowledge

### 1. Classifying and determining inventory

#### Classification

| Company type | Classification |
|---|---|
| **Merchandising** | **One:** Inventory |
| **Manufacturing** | **Three:** Raw Materials, Work in Process, Finished Goods |

**Regardless of the classification, companies report all inventories under Current Assets on the balance sheet.**

#### Taking a physical inventory

**Involves counting, weighing, or measuring each kind of inventory on hand.** Companies often "take inventory" **when the business is closed or business is slow**, and **at the end of the accounting period.**

**A physical inventory is taken for two reasons:**

| System | Reasons |
|---|---|
| **Perpetual** | **Check accuracy of inventory records**; **determine amount of inventory lost** due to wasted raw materials, shoplifting, or employee theft |
| **Periodic** | **Determine the inventory on hand**; **determine the cost of goods sold** for the period |

> [!important] Both systems count — but for different reasons
> Under a **periodic** system the count is the *only* source of the inventory figure: without it there is no way to compute COGS. Under a **perpetual** system the records already give a figure, so the count is a **verification** — and the difference between record and count is the shrinkage entry from [[06 - Accounting for Merchandising Operations]] §5.
>
> **A perpetual system does not remove the need to count.** It changes what the count is *for*.

---

### 2. Determining ownership of goods

The count tells you what is physically on the premises. **That is not the same as what you own.**

#### Goods in transit

Two situations: **purchased goods not yet received**, and **sold goods not yet delivered**.

> **Goods in transit should be included in the inventory of the company that has legal title to the goods. Legal title is determined by the terms of sale.**

| Terms | Ownership |
|---|---|
| **FOB shipping point** | **Ownership passes to the buyer when the public carrier accepts the goods from the seller** |
| **FOB destination** | **Ownership remains with the seller until the goods reach the buyer** |

> [!important] The count and the ownership test disagree, and ownership wins
> Goods on a lorry are on nobody's premises, so **no physical count will find them.** Yet somebody owns them and must include them.
>
> - **You bought, FOB shipping point** → yours the moment it left the supplier → **add to your inventory** even though you have not seen it.
> - **You sold, FOB destination** → still yours until the customer receives it → **add to your inventory** even though it has left your building.
>
> **This is the same FOB rule as [[06 - Accounting for Merchandising Operations]] §3**, applied to a different question. There it determined who pays freight; here it determines whose balance sheet the goods sit on.

#### Consigned goods

> **To hold the goods of other parties and try to sell the goods for them for a fee, but without taking ownership of the goods.**

**Many car, boat, and antique dealers sell goods on consignment.** Why? Because these are **high-value, slow-moving items**. A dealer who bought a fleet of used boats outright would tie up enormous capital and bear the entire risk of not selling them. **Consignment lets the dealer display and sell the goods while the owner keeps both the title and the risk** — the dealer earns a fee and invests nothing.

> [!warning] Consigned goods are on your premises but are **not** your inventory
> If you hold goods on consignment **for** someone else, exclude them from your count — you do not own them. If you have sent goods out on consignment **to** someone else, **include** them — you still own them, even though they are in another company's showroom.
>
> **This is the reverse of the physical-presence instinct**, and it is exactly what the lecture's DO IT! tests (Exercise 1).

---

### 3. Cost flow assumptions

> **Inventory is accounted for at cost. Cost includes all expenditures necessary to acquire goods and place them in a condition ready for sale.**

That includes the purchase price plus freight-in, import duties and handling — the "Inventory" account of [[06 - Accounting for Merchandising Operations]] §3.

**Unit costs are applied to quantities to compute the total cost of the inventory and the cost of goods sold, using one of four costing methods:**

1. **Specific identification**
2. **First-in, first-out (FIFO)**
3. **Last-in, first-out (LIFO)**
4. **Average-cost**

#### Specific identification

> **An actual physical flow costing method in which items still in inventory are specifically costed to arrive at the total cost of the ending inventory.**

> **Illustration:** Crivitz TV Company purchases three identical 50-inch TVs on different dates at costs of **$700, $750, and $800**. During the year Crivitz sold **two** sets at $1,200 each.
>
> **If Crivitz sold the TVs it purchased on February 3 and May 22**, then its cost of goods sold is $\mathbf{\$1{,}500}$ $(\$700 + \$800)$, and its ending inventory is $\mathbf{\$750}$.

**Practice is relatively rare. Most companies make assumptions (cost flow assumptions) about which units were sold.**

> [!warning] Specific identification invites manipulation
> The three TVs are **identical**. Crivitz can choose which two to "sell" and thereby choose its own profit:
>
> | Units chosen as sold | COGS | Gross profit on $2,400 sales |
> |---|---|---|
> | $700 + $750 | 1,450 | **950** |
> | $700 + $800 | 1,500 | **900** |
> | $750 + $800 | 1,550 | **850** |
>
> **A $100 swing in reported profit, with no difference in what happened.** This is precisely why specific identification is restricted to genuinely distinguishable items — cars with VINs, works of art, custom machinery — where the choice is not free.

#### The key principle

> [!important] **Cost flow assumptions do NOT need to be consistent with the physical movement of the goods.**
> A supermarket rotates stock so the oldest milk sells first — but it may account for it using LIFO. **The cost flow assumption is about which *dollars* attach to the sold units, not which *units* physically left.**
>
> This surprises everyone at first, and it is stated explicitly on the slides. It is what makes the choice of method a policy decision rather than a description of the warehouse.

---

### 4. The three cost flow methods

Throughout, the identity from [[06 - Accounting for Merchandising Operations]] holds:

$$
(\text{Beginning inventory} + \text{Purchases}) - \text{Ending inventory} = \text{Cost of goods sold}
$$

So **the three methods differ only in how they split goods available for sale between ending inventory and COGS.** The total is always the same.

> [!warning] The lecture's worked data is lost
> The Houston Electronics "Astro condensers" example (Illustrations 6-5, 6-6, 6-8, 6-11) that the deck uses to demonstrate all three methods is **entirely image-based** — the purchase schedule and every computation are lost. The example below is my own construction, built to the same pattern.

> [!example] Worked example — all three methods
> **Sunrise Traders, unit purchase record for the year:**
>
> | Date | | Units | Unit cost | Total cost |
> |---|---|---|---|---|
> | Jan 1 | Beginning inventory | 200 | $8 | 1,600 |
> | Mar 12 | Purchase | 300 | $9 | 2,700 |
> | Jul 8 | Purchase | 400 | $11 | 4,400 |
> | Oct 20 | Purchase | 300 | $12 | 3,600 |
> | | **Goods available for sale** | **1,200** | | **12,300** |
>
> **700 units were sold**, so **500 units remain**.
>
> ---
> **FIFO — first-in, first-out**
>
> > **Costs of the earliest goods purchased are the first to be recognised in determining cost of goods sold.** Often parallels actual physical flow of merchandise. **Companies determine the cost of the ending inventory by taking the unit cost of the most recent purchase and working backward** until all units of inventory have been costed.
>
> Ending inventory = the **newest** 500 units:
> $$300 \times \$12 = 3{,}600 \qquad 200 \times \$11 = 2{,}200 \qquad \Rightarrow\ \textbf{EI} = \mathbf{\$5{,}800}$$
> $$\text{COGS} = 12{,}300 - 5{,}800 = \mathbf{\$6{,}500}$$
>
> > [!tip] **LISH — "last in, still here."** The helpful hint on the slides. Under FIFO, the units *still here* are the ones bought *last*.
>
> ---
> **LIFO — last-in, first-out**
>
> > **Costs of the latest goods purchased are the first to be recognised in determining cost of goods sold.** **Seldom coincides with actual physical flow** — exceptions include goods stored in piles, such as **coal or hay**.
>
> Ending inventory = the **oldest** 500 units:
> $$200 \times \$8 = 1{,}600 \qquad 300 \times \$9 = 2{,}700 \qquad \Rightarrow\ \textbf{EI} = \mathbf{\$4{,}300}$$
> $$\text{COGS} = 12{,}300 - 4{,}300 = \mathbf{\$8{,}000}$$
>
> > [!tip] **FISH — "first in, still here."** Under LIFO, the units *still here* are the ones bought *first*.
>
> ---
> **Average-cost**
>
> > **Allocates cost of goods available for sale on the basis of weighted-average unit cost incurred**, then **applies weighted-average unit cost to the units on hand** to determine the cost of the ending inventory.
>
> $$\text{Weighted-average unit cost} = \frac{\$12{,}300}{1{,}200 \text{ units}} = \$10.25$$
> $$\textbf{EI} = 500 \times 10.25 = \mathbf{\$5{,}125} \qquad \text{COGS} = 700 \times 10.25 = \mathbf{\$7{,}175}$$
>
> > [!warning] Weight by **total cost ÷ total units**, not by averaging the unit prices
> > $(8+9+11+12)/4 = \$10.00$ is **wrong** — it ignores that 400 units were bought at $11 and only 200 at $8. **Always divide total cost by total units.**
>
> ---
> **Comparison (prices rising):**
>
> | | FIFO | Average | LIFO |
> |---|---|---|---|
> | Ending inventory | **5,800** | 5,125 | **4,300** |
> | Cost of goods sold | **6,500** | 7,175 | **8,000** |
> | EI + COGS | 12,300 ✓ | 12,300 ✓ | 12,300 ✓ |
>
> **Every column totals $12,300.** The methods only redistribute the same pool between the balance sheet and the income statement.

---

### 5. Financial statement and tax effects

**Each of the three cost flow methods is acceptable for use.** In practice:

- **Reebok International Ltd.** and **Wendy's International** use **FIFO**.
- **Campbell Soup Company**, **Krogers** and **Walgreen Drugs** use **LIFO** for part or all of their inventory.
- **Bristol-Myers Squibb**, **Starbucks** and **Motorola** use the **average-cost** method.
- **Stanley Black & Decker** uses **LIFO for domestic inventories and FIFO for foreign inventories.**

#### Balance sheet effects

> **A major advantage of the FIFO method is that in a period of inflation, the costs allocated to ending inventory will approximate their current cost.**
>
> **A major shortcoming of the LIFO method is that in a period of inflation, the costs allocated to ending inventory may be significantly understated in terms of current cost.**

#### Income statement and tax effects

> **Both inventory and net income are higher when companies use FIFO in a period of inflation.**
>
> **LIFO results in the lowest income taxes** (because of lower net income) **during times of rising prices.**

> [!important] The whole story in one table (**rising prices**)
> | | FIFO | LIFO |
> |---|---|---|
> | COGS uses | **Old, low** costs | **New, high** costs |
> | Cost of goods sold | **Lower** | **Higher** |
> | **Net income** | **Higher** | **Lower** |
> | Ending inventory uses | **New, high** costs | **Old, low** costs |
> | **Balance sheet inventory** | **Higher** — near current cost ✅ | **Lower** — badly outdated ❌ |
> | **Income taxes** | **Higher** | **Lower** ✅ |
>
> **Neither method is better on both statements.** FIFO gives a realistic balance sheet and an arguably overstated profit (it matches old costs against current revenues). LIFO gives a realistic income statement — current costs against current revenues — and a balance sheet whose inventory figure may be decades out of date.
>
> **Reverse every row if prices are falling.** The exam nearly always specifies "in a period of inflation"; if it does not, say so in your answer.

> [!note] The **LIFO conformity rule**
> A tax rule requiring that **if companies use LIFO for tax purposes they must also use it for financial reporting purposes.** This is why LIFO is used at all: a company cannot take the tax saving while reporting the higher FIFO profit to shareholders. **It must choose one story and tell it to everyone.**

#### Consistency

> **The method should be used consistently — this enhances comparability.** Although consistency is preferred, **a company may change its inventory costing method**, provided the change is **disclosed**.

This is the consistency concept from [[01 - Introduction to Accounting]]: changing method is permitted, but the change and its effect must be visible, so that a profit rise caused by a switch is not mistaken for improved trading.

---

### 6. Inventory errors

**Common causes:**
- **Failure to count or price inventory correctly.**
- **Not properly recognising the transfer of legal title to goods in transit.**

**Errors affect both the income statement and the balance sheet.**

#### Income statement effects

> **Inventory errors affect the computation of cost of goods sold and net income in TWO periods.**
>
> **An error in ending inventory of the current period will have a reverse effect on net income of the next accounting period.**
>
> **Over the two years, the total net income is correct because the errors offset each other.**

> [!important] Why the error reverses — the mechanism
> $$\text{COGS} = \text{Beginning inventory} + \text{Purchases} - \text{Ending inventory}$$
>
> **Ending inventory of year 1 *is* beginning inventory of year 2.** So a single mistake enters the formula twice, with opposite signs:
>
> | | Year 1 | Year 2 |
> |---|---|---|
> | The error sits in | **Ending** inventory (subtracted) | **Beginning** inventory (added) |
> | Effect on COGS | Opposite sign to the error | Same sign as the error |
> | Effect on net income | Same sign as the error | **Opposite sign** |
>
> **Overstate ending inventory by $3,000** → year 1 COGS understated $3,000 → **net income overstated $3,000**. In year 2, beginning inventory is overstated $3,000 → COGS overstated → **net income understated $3,000**.
>
> **Combined income for the 2-year period is correct.** The error is self-correcting — but each individual year is wrong, and that is what users see.

#### Balance sheet effects

The effect is determined using the basic accounting equation, $\text{Assets} = \text{Liabilities} + \text{Equity}$:

| Ending inventory error | **Assets** | **Liabilities** | **Equity** |
|---|---|---|---|
| **Overstated** | Overstated | No effect | Overstated |
| **Understated** | Understated | No effect | Understated |

**Inventory is an asset, and the profit error flows into equity — so both move the same way, and liabilities are untouched.**

> [!warning] The most common exam question, and its answer
> *"Understating ending inventory will overstate: (a) assets, (b) cost of goods sold, (c) net income, (d) stockholders' equity."*
>
> **Answer: (b) cost of goods sold.** Since ending inventory is **subtracted** in the COGS formula, understating it makes COGS **larger**. Assets, net income and equity are all **understated**, not overstated.
>
> **The trick is that only one item moves in the opposite direction to the error**, and it is COGS. Everything else follows the error's own direction.

---

### 7. Presentation and analysis

#### Presentation

- **Balance sheet:** inventory is classified as a **current asset**.
- **Income statement:** cost of goods sold is subtracted from sales.

**There should also be disclosure of:**
- the **major inventory classifications**,
- the **basis of accounting** (cost or LCM), and
- the **costing method** (FIFO, LIFO, or average-cost).

#### Lower-of-cost-or-net realisable value

> **When the value of inventory is lower than its cost, companies must "write down" the inventory to its net realisable value.**
>
> **Net realisable value: the amount that a company expects to realise (receive from the sale of inventory).**
>
> **This is an example of conservatism.**

> [!important] LCNRV is applied **item by item**, and it only ever writes *down*
> Two rules that questions test together:
> 1. **Compare cost against NRV for each category separately** and take the lower of the two. You may **not** offset a category where NRV exceeds cost against one where it falls short.
> 2. **There is no write-*up*.** If NRV exceeds cost, inventory stays at cost. Unrealised gains are not recognised — that is what "conservatism" means here.
>
> Exercise 4 works this through.

#### Analysis

> **Inventory management is a double-edged sword.**
> - **High inventory levels** may incur **high carrying costs** — investment, storage, insurance, obsolescence, and damage.
> - **Low inventory levels** may lead to **stock-outs and lost sales.**

$$
\boxed{\;\text{Inventory turnover} = \frac{\text{Cost of Goods Sold}}{\text{Average Inventory}}\;}
$$

**Measures the number of times on average the inventory is sold during the period.**

$$
\boxed{\;\text{Days in inventory} = \frac{365}{\text{Inventory turnover}}\;}
$$

**Measures the average number of days inventory is held.**

> **Illustration:** Wal-Mart reported in its 2014 annual report a beginning inventory of **$43,803 million**, an ending inventory of **$44,858 million**, and cost of goods sold for the year ended January 31, 2014 of **$358,069 million**.
> $$\text{Average inventory} = \frac{43{,}803+44{,}858}{2} = \$44{,}330.5\text{m}$$
> $$\text{Inventory turnover} = \frac{358{,}069}{44{,}330.5} = \mathbf{8.1 \text{ times}}$$
> $$\text{Days in inventory} = \frac{365}{8.1} \approx \mathbf{45.1 \text{ days}}$$
>
> **This is the approximate time that it takes a company to sell the inventory.**

> [!tip] Use **cost** of goods sold, not sales, in the numerator
> Inventory is carried at **cost**, so the numerator must also be at cost. Using sales revenue inflates the ratio by the gross margin and makes the figure meaningless for comparison.
>
> **Reading the result:** 45 days is fast for a general retailer — Wal-Mart's scale and logistics let it turn stock eight times a year. A luxury jeweller might turn once or twice; a supermarket's fresh-food category, dozens of times. **Compare only within an industry.**

---

### 8. Appendix 6A — cost flow methods under a **perpetual** system

The §4 calculations assumed a **periodic** system: all purchases pooled, then split at the year end. Under a **perpetual** system, cost of goods sold is computed **at each sale** using the costs available *at that moment*.

| Method | Perpetual behaviour |
|---|---|
| **FIFO** | **Same answer as periodic.** The oldest costs are used first either way, and the order of sales does not change which costs those are. |
| **LIFO** | **Can differ from periodic.** Perpetual LIFO uses the newest costs *available at the date of each sale*; periodic LIFO uses the newest costs of the *whole year*, including purchases made after the sale. |
| **Average-cost** | Becomes the **moving-average** method: a **new weighted average is computed after every purchase**, and that average is used for the next sale. |

> [!important] Only FIFO is system-independent
> This is worth remembering as a one-line fact. **FIFO gives identical results under perpetual and periodic**; LIFO and average-cost do not. If an exam gives you a perpetual system and asks for average cost, it wants the **moving average** — recomputed after each purchase — not a single year-end figure.

---

### 9. Appendix 6B — estimating inventories

Sometimes inventory must be valued without a count — for interim statements, or after a fire destroys the stock.

#### The gross profit method

> **A method of estimating the cost of ending inventory by applying a gross profit rate to net sales.** A company needs to know its **net sales**, **cost of goods available for sale**, and **gross profit rate**.

$$
\text{Estimated gross profit} = \text{Net sales} \times \text{Gross profit rate}
$$
$$
\text{Estimated COGS} = \text{Net sales} - \text{Estimated gross profit}
$$
$$
\boxed{\;\text{Estimated ending inventory} = \text{Cost of goods available for sale} - \text{Estimated COGS}\;}
$$

> **Illustration:** Kishwaukee Company records show net sales of **$200,000**, beginning inventory **$40,000**, and cost of goods purchased **$120,000**. In the preceding year the company realised a **30%** gross profit rate and expects the same this year.
>
> | | $ |
> |---|---|
> | Net sales | 200,000 |
> | Less: estimated gross profit ($200{,}000 \times 30\%$) | (60,000) |
> | **Estimated cost of goods sold** | **140,000** |
> | Beginning inventory | 40,000 |
> | Add: cost of goods purchased | 120,000 |
> | **Cost of goods available for sale** | **160,000** |
> | Less: estimated cost of goods sold | (140,000) |
> | **Estimated cost of ending inventory** | **$20,000** |

#### The retail inventory method

> **Retail companies establish a relationship between cost and sales price.** The company **applies the cost-to-retail percentage to ending inventory at retail prices to determine inventory at cost.**

$$
\text{Cost-to-retail ratio} = \frac{\text{Goods available for sale at cost}}{\text{Goods available for sale at retail}}
$$
$$
\text{Estimated cost of ending inventory} = \text{Ending inventory at retail} \times \text{Cost-to-retail ratio}
$$

**It is not necessary to take a physical inventory to determine the estimated cost of goods on hand at any given time.**

> **The major disadvantage of the retail method is that it is an averaging technique. It may produce an incorrect inventory valuation if the mix of the ending inventory is not representative of the mix in the goods available for sale.**

> [!note] Both methods are estimates — and their weakness is the same
> **Gross profit method** assumes this year's margin equals last year's. **Retail method** assumes the ending mix matches the overall mix. Both fail when the assumption fails — a sales promotion, a change in product mix, or a shift to higher-margin lines will distort either.
>
> **Neither replaces a physical count for annual accounts.** They are for interim reporting and insurance claims.

---

### 10. A look at IFRS

**Similarities:**
- **IFRS and GAAP account for inventory acquisitions at historical cost and value inventory at the lower-of-cost-or-net-realisable-value** subsequent to acquisition.
- **Who owns the goods** — goods in transit or consigned goods — **as well as the costs to include in inventory, are essentially accounted for the same** under both.

**Differences:**
- The requirements are **more principles-based under IFRS**; **GAAP provides more detailed guidelines.**
- **A major difference relates to LIFO. GAAP permits the use of LIFO for inventory valuation. IFRS PROHIBITS its use.** **FIFO and average-cost are the only two acceptable cost flow assumptions permitted under IFRS.** Both sets of standards permit **specific identification** where appropriate.

**Looking to the future:** convergence on LIFO **will be difficult to resolve.** IFRS specifically prohibits it; **the LIFO cost flow assumption is widely used in the United States because of its favourable tax advantages.** In addition, many argue that LIFO **provides a better matching of current costs against revenue** and therefore enables companies to compute a **more realistic income**.

> [!important] What this means for a Vietnamese student
> **Vietnam follows IFRS-based standards, so LIFO is not permitted.** In practice you will use **FIFO or weighted average**.
>
> **But LIFO remains examinable**, because the textbook is American and because the FIFO-vs-LIFO comparison is the clearest way to see how a cost flow assumption drives reported profit. **Learn LIFO as an analytical tool, not as something you will ever apply.**

---

## ✏️ Exercises

### Exercise 1 — Rules of ownership (lecture DO IT!)

Hasbeen Company completed its inventory count, arriving at a total inventory value of **$200,000**. Discuss how the following affects the reported cost of inventory:

1. Hasbeen **included** in the inventory goods held **on consignment for Falls Co.**, costing $15,000.
2. The company **did not include** in the count **purchased** goods of $10,000 which were in transit (terms: **FOB shipping point**).
3. The company **did not include** in the count inventory that had been **sold** with a cost of $12,000, which was in transit (terms: **FOB shipping point**).

> [!example]- Solution
> | Item | Treatment | Adjustment |
> |---|---|---|
> | 1. Consigned goods held for Falls Co. | Hasbeen **does not own** them — Falls Co. does | **Deduct $15,000** |
> | 2. Purchased, in transit, FOB shipping point | Title passed **when the carrier accepted them** → Hasbeen owns them | **Add $10,000** |
> | 3. Sold, in transit, FOB shipping point | Title passed to the **buyer** on shipment → Hasbeen no longer owns them | **Treated correctly** — no adjustment |
>
> $$\text{Correct inventory} = 200{,}000 - 15{,}000 + 10{,}000 = \mathbf{\$195{,}000}$$
>
> ---
> **Items 2 and 3 look symmetric but are not.** Both are FOB shipping point and both are in transit — yet one is added and one is excluded. **The difference is direction of travel:**
> - **Goods coming to you** under FOB shipping point are **already yours** (title passed at the supplier's dock), even though you cannot count them.
> - **Goods leaving you** under FOB shipping point are **already the customer's**, so correctly excluded.
>
> **Had item 3 been FOB *destination*, the answer would change** — Hasbeen would still own them and $12,000 would be added, giving $207,000. **Always check the direction *and* the terms; either alone is not enough.**
>
> **Item 1 is the physical-presence trap.** The goods are sitting in Hasbeen's warehouse and were counted — but possession is not ownership.

---

### Exercise 2 — Cost flow method concepts

**(a)** Goods in transit should be included in the inventory of the buyer when the:
1. public carrier accepts the goods from the seller 2. goods reach the buyer 3. terms of sale are FOB destination 4. terms of sale are FOB shipping point

**(b)** The cost flow method that often parallels the actual physical flow of merchandise is the:
1. FIFO method 2. LIFO method 3. average cost method 4. gross profit method

**(c)** In a period of inflation, the cost flow method that results in the lowest income taxes is the:
1. FIFO method 2. LIFO method 3. average cost method 4. gross profit method

> [!example]- Solution
> **(a) Answers 1 and 4 are both correct** — they are two ways of saying the same thing. Under **FOB shipping point**, title passes **when the public carrier accepts the goods from the seller**, so the buyer includes them from that moment.
>
> Option 2 describes FOB destination timing, and option 3 names the terms under which the buyer does **not** yet own the goods.
>
> **A defective question**, since two options are equivalent. Weygandt's intended answer is **4** (it names the terms rather than the mechanism). If both appear, choose the one that names the *terms of sale*, since that is what the ownership rule is stated in terms of.
>
> **(b) Answer: 1 — FIFO.**
>
> Most businesses genuinely sell their **oldest** stock first, particularly with perishable or fashion goods. So FIFO's cost flow usually matches the physical flow.
>
> **But remember §3: it does not have to.** LIFO's *seldom* coinciding with physical flow is not an objection to LIFO — the exceptions the slides give (**coal or hay**, stored in piles and taken from the top) are the rare cases where LIFO's cost flow *does* match reality.
>
> Option 4 is a distractor: the **gross profit method is an estimation technique**, not a cost flow assumption at all — it appears in both (b) and (c) for that reason.
>
> **(c) Answer: 2 — LIFO.**
>
> Rising prices → LIFO charges the **newest, highest** costs to COGS → **highest COGS** → **lowest net income** → **lowest tax**.
>
> **Two conditions the answer depends on**, both worth stating explicitly in a written answer:
> 1. **Prices must be rising.** If prices fall, FIFO gives the lowest tax.
> 2. **The LIFO conformity rule applies:** the company must also report the lower profit to shareholders. The tax saving is not free.

---

### Exercise 3 — Inventory errors (lecture DO IT!, extended)

Visual Company **overstated its 2016 ending inventory by $22,000**. Determine the impact on ending inventory, cost of goods sold, and stockholders' equity in **2016** and **2017**. Then compute the effect on each year's net income and on the two-year total.

> [!example]- Solution
> | | **2016** | **2017** |
> |---|---|---|
> | **Ending inventory** | $22,000 **overstated** | **No effect** |
> | **Cost of goods sold** | $22,000 **understated** | $22,000 **overstated** |
> | **Stockholders' equity** | $22,000 **overstated** | **No effect** |
>
> **Net income effects:**
>
> | | 2016 | 2017 | Two-year total |
> |---|---|---|---|
> | Net income | **Overstated $22,000** | **Understated $22,000** | **Correct** |
>
> ---
> **Working through the mechanism.**
>
> **2016.** Ending inventory is overstated by $22,000. In $\text{COGS} = \text{BI}+\text{P}-\text{EI}$, a larger EI is subtracted, so **COGS is understated by $22,000** → **net income overstated by $22,000** → **retained earnings, hence equity, overstated by $22,000.** The balance sheet is wrong on both sides in the same direction: assets up $22,000 and equity up $22,000, so **the equation still balances** — which is exactly why the error is not caught by the trial balance.
>
> **2017.** The overstated 2016 ending inventory becomes the **overstated 2017 beginning inventory**. Now it is **added** in the formula, so **COGS is overstated by $22,000** → **net income understated by $22,000.**
>
> **Why 2017's ending inventory and equity show "no effect".** The 2017 count is assumed correct, so ending inventory is right. And equity — cumulative — was $22,000 too high at the end of 2016 and is brought back down by 2017's $22,000 understated income. **The two errors cancel exactly.**
>
> **The self-correcting property, and why it does not excuse the error.** Over two years the total is right. But **each individual year is wrong by $22,000**, and users make decisions on annual figures. A company reporting 2016 growth followed by a 2017 collapse — when in truth both years were flat — has seriously misled its readers, even though the two-year total is unimpeachable.
>
> **A useful check for any inventory-error question:** the only item that moves in the *opposite* direction to the error is **cost of goods sold** (in the year of the error). Everything else — inventory, assets, net income, equity — moves in the **same** direction.

---

### Exercise 4 — Lower-of-cost-or-NRV (lecture DO IT!)

Tracy Company sells three different types of home heating stove:

| | Cost | Net realisable value |
|---|---|---|
| Gas | $84,000 | $79,000 |
| Wood | 250,000 | 280,000 |
| Pellet | 112,000 | 101,000 |

Determine the value of the company's inventory under the lower-of-cost-or-net-realisable-value approach, and record any necessary write-down.

> [!example]- Solution
> **Apply LCNRV to each category separately:**
>
| | Cost | NRV | **Lower** |
|---|---|---|---|
| Gas | 84,000 | 79,000 | **79,000** ← NRV |
| Wood | 250,000 | 280,000 | **250,000** ← cost |
| Pellet | 112,000 | 101,000 | **101,000** ← NRV |
| **Total** | 446,000 | 460,000 | **$430,000** |
>
> **Inventory is reported at $430,000.**
>
> **The write-down entry:**
> $$\text{Total cost } 446{,}000 - \text{LCNRV } 430{,}000 = \$16{,}000$$
> $$\text{Dr Cost of Goods Sold } 16{,}000 \;/\; \text{Cr Inventory } 16{,}000$$
> *(Some texts debit a "Loss on inventory write-down" account; both are acceptable, and the effect on profit is identical.)*
>
> ---
> **Two things this exercise is designed to catch.**
>
> **1. You may NOT offset wood's $30,000 gain against the losses.** Applying LCNRV to the **total** would give $\min(446{,}000,\;460{,}000) = \$446{,}000$ — no write-down at all, and inventory overstated by $16,000. **The comparison is item by item**, which is deliberately more conservative.
>
> **2. Wood stays at cost, not at NRV.** Its NRV of $280,000 exceeds cost, but **there is no write-up.** Recognising that $30,000 would be booking an unrealised gain on unsold goods — precisely what conservatism forbids.
>
> **The asymmetry is the point.** Losses are recognised as soon as they are anticipated; gains only when realised through sale. This is the same conservatism that underlies historical cost in [[01 - Introduction to Accounting]], and it means **inventory can be written down but essentially never up** (IFRS permits reversal of a previous write-down if NRV recovers, but never above original cost).

---

### Exercise 5 — Full cost flow computation and analysis

Delta Supplies had beginning inventory of 150 units at $20. Purchases: 250 units at $22 (March), 300 units at $25 (July), 200 units at $28 (November). It sold 640 units for $45 each.

(a) Compute ending inventory and COGS under FIFO, LIFO and average-cost (periodic). (b) Compute gross profit under each. (c) Compute inventory turnover under FIFO. (d) If the tax rate is 20%, how much tax does the choice of method save or cost?

> [!example]- Solution
> **Goods available for sale:**
>
> | | Units | Unit cost | Total |
> |---|---|---|---|
> | Beginning | 150 | 20 | 3,000 |
> | March | 250 | 22 | 5,500 |
> | July | 300 | 25 | 7,500 |
> | November | 200 | 28 | 5,600 |
> | **Total** | **900** | | **21,600** |
>
> Sold 640, so **ending inventory = 260 units**. Sales revenue $= 640 \times 45 = \$28{,}800$.
>
> **(a) The three methods.**
>
> **FIFO** — ending inventory is the newest 260 units:
> $$200 \times 28 = 5{,}600 \qquad 60 \times 25 = 1{,}500 \qquad \textbf{EI} = \mathbf{\$7{,}100}$$
> $$\text{COGS} = 21{,}600 - 7{,}100 = \mathbf{\$14{,}500}$$
>
> **LIFO** — ending inventory is the oldest 260 units:
> $$150 \times 20 = 3{,}000 \qquad 110 \times 22 = 2{,}420 \qquad \textbf{EI} = \mathbf{\$5{,}420}$$
> $$\text{COGS} = 21{,}600 - 5{,}420 = \mathbf{\$16{,}180}$$
>
> **Average-cost:**
> $$\frac{21{,}600}{900} = \$24.00 \text{ per unit}$$
> $$\textbf{EI} = 260 \times 24 = \mathbf{\$6{,}240} \qquad \text{COGS} = 640 \times 24 = \mathbf{\$15{,}360}$$
>
> Check each: $7{,}100+14{,}500 = 21{,}600$ ✓; $5{,}420+16{,}180 = 21{,}600$ ✓; $6{,}240+15{,}360 = 21{,}600$ ✓
>
> **(b) Gross profit** (sales $28,800):
>
> | | FIFO | Average | LIFO |
> |---|---|---|---|
> | Sales | 28,800 | 28,800 | 28,800 |
> | COGS | (14,500) | (15,360) | (16,180) |
> | **Gross profit** | **14,300** | **13,440** | **12,620** |
> | Gross profit rate | 49.7% | 46.7% | 43.8% |
> | Ending inventory | **7,100** | 6,240 | **5,420** |
>
> **Prices rose from $20 to $28, so FIFO gives the highest profit and the highest inventory — exactly as §5 predicts.**
>
> **(c) Inventory turnover under FIFO:**
> $$\text{Average inventory} = \frac{3{,}000 + 7{,}100}{2} = \$5{,}050$$
> $$\text{Turnover} = \frac{14{,}500}{5{,}050} = \mathbf{2.87 \text{ times}}
> \qquad
> \text{Days} = \frac{365}{2.87} = \mathbf{127 \text{ days}}$$
> Slow — over four months of stock. Compare Wal-Mart's 45 days in §7. Plausible for a specialist supplier; alarming for a grocer.
>
> **(d) Tax effect.** Gross profit differs by $14{,}300 - 12{,}620 = \$1{,}680$ between FIFO and LIFO:
> $$\text{Tax difference} = 1{,}680 \times 20\% = \mathbf{\$336}$$
> **LIFO saves $336 in tax this year** — real cash, permanently deferred while inventory levels hold up.
>
> ---
> **Three points to close on:**
>
> **1. Nothing physical differs between the three columns.** Same units bought, same units sold, same cash paid and received. **Only the assumption about which dollars attached to which units changes** — and profit moves by $1,680, or 13% of the FIFO figure.
>
> **2. The trade-off is genuine.** LIFO's $336 tax saving comes at the cost of reporting $1,680 less profit to shareholders (the **LIFO conformity rule**) and carrying inventory on the balance sheet at $5,420 when its current cost is nearer $7,100.
>
> **3. Under IFRS this choice does not exist** — LIFO is prohibited, so the realistic comparison for a Vietnamese company is **FIFO ($14,300) versus average-cost ($13,440)**, a smaller but still material $860 difference.

---

## 📝 Summary

- **Merchandisers have one inventory classification; manufacturers have three** (raw materials, work in process, finished goods). **All are current assets.**
- **A physical count is required under both systems** — under periodic it *determines* inventory and COGS; under perpetual it *verifies* the records and reveals shrinkage.
- **Ownership, not possession, decides inclusion.** Goods in transit belong to whoever holds legal title: **FOB shipping point** → buyer owns from the moment the carrier accepts them; **FOB destination** → seller owns until delivery. **Consigned goods held for others are excluded; goods sent out on consignment are included.**
- **Inventory is recorded at cost** — all expenditures necessary to acquire the goods and make them ready for sale. Four methods: **specific identification, FIFO, LIFO, average-cost.**
- **Cost flow assumptions need not match physical flow.** FIFO: oldest costs to COGS, newest to inventory (**LISH**). LIFO: newest costs to COGS, oldest to inventory (**FISH**). Average: total cost ÷ total units, applied to both.
- **In a period of inflation:** FIFO gives **higher** net income and a balance-sheet inventory close to current cost; LIFO gives **lower** net income, **lowest income taxes**, and a badly understated inventory figure. The **LIFO conformity rule** forces a company using LIFO for tax to use it for reporting too.
- **Inventory errors affect two periods and are self-correcting.** An ending-inventory error reverses in the following year, so the **two-year total net income is correct** while each individual year is wrong. **Only COGS moves opposite to the error;** inventory, assets, net income and equity all move with it.
- **LCNRV** writes inventory down to net realisable value when NRV is below cost — **applied item by item, with no write-ups.** An example of conservatism.
- $\text{Inventory turnover} = \dfrac{\text{COGS}}{\text{Average inventory}}$ and $\text{Days in inventory} = \dfrac{365}{\text{turnover}}$. High inventory means carrying costs; low inventory means stock-outs.
- **Under a perpetual system, FIFO gives the same answer as periodic; LIFO and average-cost do not** (average becomes moving-average). **IFRS prohibits LIFO entirely.**
- **Estimation methods:** the **gross profit method** applies a historic margin to net sales; the **retail method** applies a cost-to-retail ratio to ending inventory at retail.

---

## ⚠️ Important Notes

> [!warning] Possession is not ownership
> The three traps, in order of how often they appear:
> 1. **Consigned goods on your premises** → exclude (not yours).
> 2. **Goods you bought, in transit FOB shipping point** → include (already yours).
> 3. **Goods you sold, in transit FOB destination** → include (still yours).
>
> **Read the terms *and* the direction of travel.** Either alone gives the wrong answer half the time.

> [!warning] Weighted average means total cost ÷ total units
> **Not** the arithmetic mean of the unit prices. Averaging $\$20,\$22,\$25,\$28$ to get $\$23.75$ ignores the quantities and gives a different — wrong — answer from the correct $\$24.00$.

> [!tip] LISH and FISH
> **FIFO → LISH:** *last in, still here.* **LIFO → FISH:** *first in, still here.*
>
> These tell you what is in **ending inventory**, which is the harder half to remember. Once you have ending inventory, COGS follows from $\text{COGS} = \text{Goods available} - \text{EI}$.

> [!warning] "In a period of inflation" is a load-bearing phrase
> Every FIFO-vs-LIFO conclusion **reverses** if prices fall. If a question omits the phrase, state your assumption explicitly in the answer.

> [!note] LCNRV: item by item, and never up
> Comparing totals instead of items understates the write-down. And inventory whose NRV exceeds cost stays **at cost** — no gain is recognised until sale. Both rules follow from conservatism, and both are tested in the same question.

> [!tip] Turnover uses COGS, not sales
> Inventory is carried at cost, so the numerator must be at cost too. And **compare turnover only within an industry** — 45 days is excellent for a supermarket and terrible for a fresh-fish stall.

> [!important] For Vietnamese practice, LIFO is prohibited
> IFRS permits only **FIFO, average-cost and specific identification**. LIFO remains examinable because the textbook is American, and because the FIFO/LIFO contrast is the clearest demonstration of how a cost flow assumption drives reported profit — but you will not apply it.

> [!warning] Gaps in the source slides
> This deck is Weygandt's Chapter 6 set. The text survives well, but **every numerical demonstration is an image.**
> - **The entire Houston Electronics "Astro condensers" example is lost.** Illustrations 6-5 (the purchase data), 6-6 (FIFO), 6-8 (LIFO) and 6-11 (average-cost) are all images. **The deck therefore contains no visible computation of any cost flow method.** The worked example in §4 and Exercise 5 are my own constructions.
> - **Also image-only:** Illustration 6-3 and 6-4 (Crivitz specific identification — only the narrative survives), 6-12 (cost flow methods in US companies), 6-13 (comparative effects), 6-14 (disclosure of a change in method), 6-15, 6-16, 6-17 (inventory-error effects), 6-18 (balance-sheet effects), 6-20 (LCNRV computation), 6-21 (Wal-Mart turnover), 6A-1 to 6A-4 (**the whole perpetual-system appendix**), and 6B-1 to 6B-4 (**the whole estimation appendix**).
> - **Appendix 6A is entirely image-based.** Four slides, each a single illustration, covering perpetual FIFO, perpetual LIFO and moving-average — with **no text at all** beyond the headings. §8 is reconstructed from standard material; **the moving-average computation is never demonstrated anywhere.**
> - **Appendix 6B's formulas (Illustrations 6B-1 and 6B-3) are images.** The gross-profit-method formulas in §9 are reconstructed; the Kishwaukee narrative data survives in text and I have verified the $20,000 answer from it. **The retail method has no worked example at all.**
> - **The cost flow methods DO IT! (slide 36) is entirely image-based** — question and answer both lost.
> - **The comparative-effects table (Illustration 6-13)** — the single most examinable summary in the chapter — is an image. The table in §5 is reconstructed from the surrounding text statements, which do survive.

---

**Previous:** [[06 - Accounting for Merchandising Operations]] · **Next:** [[08 - Accounting for Receivables]] · **Index:** [[00-Index]]

#accounting #inventory #fifo #lifo #average-cost #lcnrv #inventory-errors #turnover
