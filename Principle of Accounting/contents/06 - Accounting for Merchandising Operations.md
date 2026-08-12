---
subject: Principle of Accounting
chapter: 06
tags: [ds, accounting, merchandising, inventory, perpetual, periodic, cogs, discounts]
source: "documents/slides/ch05.pptx (Doan Thuy Duong, SAA); Weygandt, Kimmel & Kieso, *Accounting Principles*, 13th ed., Ch. 5"
---

# Accounting for Merchandising Operations

> [!abstract] Where this sits in the course
> Every example so far has been a **service** business — it performs work and bills for it. **A merchandising business buys goods and resells them**, which introduces two things a service business never has: **inventory** on the balance sheet and **cost of goods sold** in the income statement.
>
> That single addition reshapes both statements, creates a new class of adjusting entry, and introduces the perpetual-versus-periodic choice that dominates [[07 - Inventories]].

---

## 📘 Main Knowledge

### 1. Merchandising operations

**Merchandising companies buy and sell goods.** The chain runs **manufacturer → wholesaler → retailer → consumer**, and **the primary source of revenues is referred to as sales revenue or sales.**

#### Income measurement

$$
\text{Sales Revenue} - \text{Cost of Goods Sold} = \text{Gross Profit}
$$
$$
\text{Gross Profit} - \text{Operating Expenses} = \text{Net Income (Loss)}
$$

**Cost of goods sold is the total cost of merchandise sold during the period.** It is **not used in a service business** — which is precisely why a service company's income statement has no gross profit line.

> [!important] The one structural difference from a service company
> A service business has: Revenue − Expenses = Net income. **A merchandiser inserts a step**: Sales − COGS = Gross profit, *then* − Operating expenses = Net income.
>
> The extra line matters because it separates two very different questions: **is the product itself profitable** (gross profit), and **is the business profitable after running costs** (net income). A retailer with a healthy 40% gross margin and a net loss has a cost-control problem, not a pricing problem — and only the two-step format reveals which.

#### The operating cycle

**The operating cycle of a merchandising company ordinarily is longer than that of a service company.**

$$
\text{Service: } \text{Cash} \to \text{Perform service} \to \text{Receivable} \to \text{Cash}
$$
$$
\text{Merchandising: } \text{Cash} \to \textbf{Buy inventory} \to \text{Sell} \to \text{Receivable} \to \text{Cash}
$$

**The extra step is inventory**, and it is why merchandisers need more working capital: cash is tied up in goods sitting on shelves before any sale occurs.

---

### 2. Inventory systems

**Companies use either a perpetual inventory system or a periodic inventory system to account for inventory.**

#### Perpetual system

- **Maintain detailed records of the cost of each inventory purchase and sale.**
- **Records continuously show inventory that should be on hand for every item.**
- **Company determines cost of goods sold each time a sale occurs.**

#### Periodic system

- **Do not keep detailed records of the goods on hand.**
- **Cost of goods sold determined by count at the end of the accounting period.**

**Calculation of cost of goods sold:**

| | $ |
|---|---|
| Beginning inventory | 100,000 |
| Add: Purchases, net | 800,000 |
| **Goods available for sale** | **900,000** |
| Less: Ending inventory | (125,000) |
| **Cost of goods sold** | **775,000** |

$$
\boxed{\;\text{COGS} = \text{Beginning inventory} + \text{Net purchases} - \text{Ending inventory}\;}
$$

> [!important] Read the periodic formula as a residual
> The periodic system does **not measure** cost of goods sold — it **infers** it. Everything that was available and is no longer on the shelf is assumed to have been sold.
>
> **That assumption is the system's fatal weakness.** Goods stolen, broken, or lost are silently swept into cost of goods sold, and **shrinkage becomes invisible.** A perpetual system, by contrast, knows what *should* be there, so a physical count reveals any discrepancy immediately (see §5).

#### Advantages of the perpetual system

- **Traditionally used for merchandise with high unit values.**
- **Shows the quantity and cost of the inventory that should be on hand at any time.**
- **Provides better control over inventories than a periodic system.**

> [!note] Why periodic systems still existed
> Before barcode scanning, recording the cost of every item sold at the moment of sale was impossibly laborious for a shop selling thousands of low-value units. **Periodic accounting was a practical necessity, not a choice.** Point-of-sale technology removed that constraint, and perpetual systems are now standard almost everywhere — but the periodic method survives in exams because the COGS formula above is fundamental, and because [[07 - Inventories]] needs both.

---

### 3. Recording purchases (perpetual)

Purchases are **made using cash or credit (on account)**, **normally recorded when goods are received from the seller**, and **a purchase invoice should support each credit purchase**.

> **Illustration:** Sauk Stereo (the buyer) uses as a purchase invoice the sales invoice prepared by PW Audio Supply, Inc. (the seller).

$$
\text{May 4:}\qquad \text{Dr Inventory } 3{,}800 \;/\; \text{Cr Accounts Payable } 3{,}800
$$

> [!important] Under a perpetual system, purchases are debited to **Inventory**, not to "Purchases"
> This is the defining difference. **Perpetual: Dr Inventory. Periodic: Dr Purchases** (see §8). The perpetual system treats the goods as an asset from the moment they arrive and tracks them until sold; the periodic system dumps everything into a temporary "Purchases" account and sorts it out at the year end.

#### Freight costs

**Shipping terms determine who pays and who owns the goods in transit:**

| Term | Ownership passes | Freight paid by | Buyer's entry | Seller's entry |
|---|---|---|---|---|
| **FOB shipping point** | **When the public carrier accepts the goods from the seller** | Buyer | **Dr Inventory** | — |
| **FOB destination** | **Remains with the seller until the goods reach the buyer** | Seller | — | **Dr Freight-Out** |

**Freight costs incurred by the seller are an operating expense.**

> **Illustration:** Upon delivery of the goods on May 6, Sauk Stereo pays Public Freight Company $150 for freight charges:
> $$\text{Dr Inventory } 150 \;/\; \text{Cr Cash } 150$$
>
> Had the terms required PW Audio Supply to pay the freight:
> $$\text{Dr Freight-Out } 150 \;/\; \text{Cr Cash } 150$$

> [!important] Why the buyer capitalises freight and the seller expenses it
> **For the buyer, freight is part of the cost of getting the goods ready for sale**, so it is added to Inventory and only becomes an expense when the goods are sold (matching principle). Inventory cost = purchase price + freight-in.
>
> **For the seller, freight is a cost of *delivering* to a customer** — a selling expense of this period, unrelated to any future asset. It goes to **Freight-Out**, an operating expense.
>
> **Same $150, same lorry, opposite accounting**, determined entirely by who bears the cost. This is a favourite exam point.

> [!tip] Remembering FOB
> **FOB = "Free On Board."** The named point is where the seller's responsibility *ends*.
> - **FOB shipping point** → seller's job ends at the loading dock → **buyer** owns goods in transit and pays freight.
> - **FOB destination** → seller's job ends at the buyer's door → **seller** owns goods in transit and pays freight.
>
> This also determines **whose inventory the goods are in at a year end** if they are still on a lorry — which is exactly the trap in [[07 - Inventories]].

#### Purchase returns and allowances

**The purchaser may be dissatisfied because goods are damaged or defective, of inferior quality, or do not meet specifications.**

| | Definition |
|---|---|
| **Purchase return** | **Return goods for credit** if the sale was made on credit, or for a cash refund if the purchase was for cash |
| **Purchase allowance** | **May choose to keep the merchandise if the seller will grant a reduction of the purchase price** |

> **Illustration:** Sauk Stereo returned goods costing $300 to PW Audio Supply on May 8.
> $$\text{Dr Accounts Payable } 300 \;/\; \text{Cr Inventory } 300$$

> [!important] In a perpetual system the credit goes to **Inventory**
> Not to "Purchase Returns", not to "Purchases". **The goods have physically left, so the asset must fall.** This is a lecture question (Exercise 2) and the distractors are all periodic-system account names.

#### Purchase discounts

**Credit terms may permit the buyer to claim a cash discount for prompt payment.**

**Advantages:**
- **Purchaser saves money.**
- **Seller shortens the operating cycle by converting accounts receivable into cash earlier.**

**Reading credit terms:**

| Term | Meaning |
|---|---|
| **2/10, n/30** | **2% discount if paid within 10 days, otherwise net amount due within 30 days** |
| **1/10 EOM** | **1% discount if paid within the first 10 days of the next month** |
| **n/10 EOM** | **Net amount due within the first 10 days of the next month** |

> **Illustration:** Sauk Stereo pays the balance due of $3,500 (gross invoice price of $3,800 less purchase returns and allowances of $300) on May 14, the last day of the discount period.
>
> $$\text{Discount} = 3{,}500 \times 2\% = \$70$$
> $$\text{Dr Accounts Payable } 3{,}500 \;/\; \text{Cr Cash } 3{,}430,\;\; \text{Cr Inventory } 70$$
>
> If Sauk Stereo failed to take the discount and instead made full payment of $3,500 on June 3:
> $$\text{Dr Accounts Payable } 3{,}500 \;/\; \text{Cr Cash } 3{,}500$$

> [!warning] The discount is computed on the amount **after** returns
> $3,800 − $300 = $3,500, then 2% of $3,500 = $70. **Not 2% of $3,800.** You cannot claim a discount on goods you sent back.

**Should discounts be taken when offered?**

> **Example: 2% for 20 days = annual rate of 36.5%**
> $$\$3{,}500 \times 36.5\% \times \frac{20}{365} = \$70$$

> [!important] Forgoing a settlement discount is very expensive borrowing
> With terms 2/10, n/30, paying on day 30 instead of day 10 means **borrowing the money for 20 extra days at a cost of 2%**. Annualised:
> $$\frac{2\%}{20\text{ days}} \times 365 = \mathbf{36.5\%\text{ per year}}$$
>
> **Almost no business can borrow at 36.5%.** So if cash is available, **take the discount** — and if it is not, the terms are telling you the business has a working-capital problem worth fixing. This calculation is a standard exam question and a genuinely useful piece of financial management.

#### Summary of purchasing transactions

| Date | Event | Effect on Inventory |
|---|---|---|
| May 4 | Purchase | +3,800 |
| May 6 | Freight-in | +150 |
| May 8 | Return | (300) |
| May 14 | Discount | (70) |
| | **Balance** | **3,580** |

$$
3{,}800 + 150 - 300 - 70 = \$3{,}580
$$

**Under a perpetual system, all four events run through the single Inventory account** — which is why the account always shows the true cost of goods on hand.

---

### 4. Recording sales (perpetual)

Sales are **made using cash or credit (on account)**. **Sales revenue, like service revenue, is recorded when the performance obligation is satisfied** — and **the performance obligation is satisfied when the goods are transferred from the seller to the buyer.** **A sales invoice should support each credit sale.**

> [!important] Every sale requires **two** journal entries
> $$\textbf{\#1}\quad \text{Dr Cash or Accounts Receivable } XXX \;/\; \text{Cr Sales Revenue } XXX \qquad \textit{(at \textbf{selling price})}$$
> $$\textbf{\#2}\quad \text{Dr Cost of Goods Sold } XXX \;/\; \text{Cr Inventory } XXX \qquad \textit{(at \textbf{cost})}$$
>
> **Entry #1 records the revenue; entry #2 records the expense that generated it.** They must be recorded together — that is the matching principle from [[05 - Adjusting Entries]] applied at the moment of sale.
>
> **Forgetting entry #2 is the single most common error in this chapter.** It overstates profit by the full cost of the goods *and* leaves inventory on the books that no longer exists.

> **Illustration:** PW Audio Supply records the sale of $3,800 on May 4 to Sauk Stereo on account (the merchandise cost PW Audio Supply $2,400):
> $$\text{Dr Accounts Receivable } 3{,}800 \;/\; \text{Cr Sales Revenue } 3{,}800$$
> $$\text{Dr Cost of Goods Sold } 2{,}400 \;/\; \text{Cr Inventory } 2{,}400$$
>
> Gross profit on this sale: $3{,}800 - 2{,}400 = \$1{,}400$.

#### Sales returns and allowances

**The "flip side" of purchase returns and allowances.** Recorded in a **contra-revenue account to Sales Revenue (debit).**

**Sales is not reduced (debited) directly because:**
- **it would obscure the importance of sales returns and allowances as a percentage of sales**;
- **it could distort comparisons.**

> [!note] Why a contra account rather than a direct reduction
> A rising returns rate is a **warning signal** — of quality problems, misleading marketing, or a failing product. Netting returns straight against sales makes that signal invisible. **Keeping a separate contra account preserves the information** while still reducing net sales in the statement.
>
> Exactly the same reasoning as **Accumulated Depreciation** in [[05 - Adjusting Entries]]: use a contra account whenever both the gross figure and the deduction carry information.

> **Illustration:** PW Audio Supply records the credit for returned goods that had a $300 selling price (a $140 cost), the goods **not** being defective:
> $$\text{Dr Sales Returns and Allowances } 300 \;/\; \text{Cr Accounts Receivable } 300$$
> $$\text{Dr Inventory } 140 \;/\; \text{Cr Cost of Goods Sold } 140$$
>
> **If the returned goods were defective with a scrap value of $50:**
> $$\text{Dr Sales Returns and Allowances } 300 \;/\; \text{Cr Accounts Receivable } 300$$
> $$\text{Dr Inventory } 50 \;/\; \text{Cr Cost of Goods Sold } 50$$

> [!important] Returns also need two entries — and the second depends on condition
> Entry #1 (revenue reversal) is the **same** in both cases: the customer gets $300 of credit regardless.
>
> Entry #2 depends on **what came back**:
> - **Good condition** → restore inventory at its **original cost, $140**.
> - **Defective, scrap value $50** → restore inventory at only **$50**, because that is what it is now worth.
>
> The $90 difference stays in Cost of Goods Sold — **the loss on defective goods is borne by the seller**, exactly as it should be.

#### Sales discounts

**Offered to customers to promote prompt payment of the balance due.** A **contra-revenue account (debit) to Sales Revenue.**

> **Illustration:** Sauk Stereo pays the balance due of $3,500 on May 14, the last day of the discount period. PW Audio Supply records:
> $$\text{Dr Cash } 3{,}430,\;\; \text{Dr Sales Discounts } 70 \;/\; \text{Cr Accounts Receivable } 3{,}500$$
> $$\text{where } 70 = (3{,}800 - 300) \times 2\%$$

> [!tip] Buyer and seller mirror each other — but not perfectly
> | Event | **Buyer** (Sauk) | **Seller** (PW Audio) |
> |---|---|---|
> | Purchase / sale | Dr **Inventory** 3,800 / Cr AP 3,800 | Dr AR 3,800 / Cr **Sales Revenue** 3,800<br>**+ Dr COGS 2,400 / Cr Inventory 2,400** |
> | Return | Dr AP 300 / Cr **Inventory** 300 | Dr **Sales R&A** 300 / Cr AR 300<br>**+ Dr Inventory 140 / Cr COGS 140** |
> | Payment | Dr AP 3,500 / Cr Cash 3,430, **Cr Inventory 70** | Dr Cash 3,430, **Dr Sales Discounts 70** / Cr AR 3,500 |
>
> **Two asymmetries worth noting.**
> 1. **The seller always has a second entry** for cost of goods sold; the buyer never does, because the buyer is acquiring an asset, not consuming one.
> 2. **The buyer adjusts Inventory for discounts; the seller uses a contra-revenue account.** For the buyer the discount genuinely reduces the cost of the goods; for the seller it reduces revenue, and the contra account keeps that visible.

---

### 5. The accounting cycle for a merchandiser

**Generally the same as a service company**, with **one additional adjustment to make the records agree with the actual inventory on hand** — involving **Inventory and Cost of Goods Sold**.

> **Illustration:** PW Audio Supply has an unadjusted balance of $40,500 in Merchandise Inventory. A physical count determines that actual merchandise inventory at year-end is **$40,000**.
> $$\text{Dr Cost of Goods Sold } 500 \;/\; \text{Cr Inventory } 500$$

> [!important] This is the **shrinkage** entry, and it is why perpetual systems are worth having
> The perpetual records say $40,500 should be on hand; the count finds $40,000. The **$500 difference is inventory shrinkage** — theft, breakage, spoilage, or recording error.
>
> **A periodic system cannot produce this entry**, because it has no independent record of what *should* be there. The $500 loss would simply vanish into cost of goods sold, undetected and unmeasured.
>
> **A perpetual system still requires a physical count** — the count is what validates the records. What perpetual gives you is the ability to *compare* count against record and quantify the difference.

#### Closing entries

> **DO IT!:** The trial balance of Celine's Sports Wear Shop at December 31 shows Inventory $25,000, Sales Revenue $162,400, Sales Returns and Allowances $4,800, Sales Discounts $3,600, Cost of Goods Sold $110,000, Rent Revenue $6,000, Freight-Out $1,800, Rent Expense $8,800, Salaries and Wages Expense $22,000.

**Close the revenue accounts (debit balances to zero):**
$$
\text{Dr Sales Revenue } 162{,}400,\;\; \text{Dr Rent Revenue } 6{,}000 \;/\; \text{Cr Income Summary } 168{,}400
$$

**Close the expense and contra-revenue accounts:**
$$
\text{Dr Income Summary } 151{,}000 \;/\;
$$
$$
\text{Cr Cost of Goods Sold } 110{,}000,\;\; \text{Cr Sales Returns and Allowances } 4{,}800,\;\; \text{Cr Sales Discounts } 3{,}600,
$$
$$
\text{Cr Freight-Out } 1{,}800,\;\; \text{Cr Rent Expense } 8{,}800,\;\; \text{Cr Salaries and Wages Expense } 22{,}000
$$

Check: $110{,}000+4{,}800+3{,}600+1{,}800+8{,}800+22{,}000 = 151{,}000$ ✓

$$
\text{Net income} = 168{,}400 - 151{,}000 = \mathbf{\$17{,}400}
$$

> [!important] Three things to notice about the closing entries
> **1. Inventory ($25,000) is NOT closed.** It is a **balance sheet** account — a real, permanent account that carries forward. Only **temporary** accounts (revenues, expenses, contra-revenues, drawings) are closed. **Closing Inventory is a classic error** and the reason it is listed among the data.
>
> **2. Sales Returns and Allowances and Sales Discounts are closed with the *expenses*.** They have **debit** balances, so they are credited to close — exactly like expenses — even though they are contra-*revenue* accounts. **Their normal balance, not their category, determines which side they close on.**
>
> **3. Rent Revenue is closed with Sales Revenue.** Both are revenues; the fact that rent is non-operating affects where it appears in the income statement, not whether it is closed.

---

### 6. Income statement formats

#### Multiple-step income statement

**Shows several steps in determining net income. Two steps relate to principal operating activities. Distinguishes between operating and non-operating activities.**

**Key items:**

$$
\text{Net sales} \;\longrightarrow\; \text{Gross profit} \;\longrightarrow\; \text{Operating expenses} \;\longrightarrow\; \text{Non-operating activities} \;\longrightarrow\; \text{Net income}
$$

Structurally:

| | |
|---|---|
| Sales revenue | X |
| Less: Sales returns and allowances | (X) |
| Less: Sales discounts | (X) |
| **Net sales** | **X** |
| Cost of goods sold | (X) |
| **Gross profit** | **X** |
| Operating expenses (selling; administrative) | (X) |
| **Income from operations** | **X** |
| Other revenues and gains / Other expenses and losses | ±X |
| **Net income** | **X** |

> [!note] This is the same four-tier structure as [[01 - Introduction to Accounting]]
> The IAS 1 statement of profit or loss and the US multiple-step income statement are **the same thing with different labels**: gross profit → income from operations (= profit from operations) → net income. **The multiple-step format is the merchandising equivalent of what you already know.**

#### Single-step income statement

**Subtract total expenses from total revenues.** Two reasons for using it:

- **A company does not realise any profit until total revenues exceed total expenses.**
- **The format is simpler and easier to read.**

$$
\text{Total revenues} - \text{Total expenses} = \text{Net income}
$$

> [!tip] Which format, and why it matters
> **Multiple-step** is far more informative — it exposes gross margin and separates operating from non-operating results, which is what an analyst actually needs. **Single-step** is simpler but discards those distinctions.
>
> Both produce **identical net income.** The choice is purely about presentation, which is why the exam tests you on *which items appear in which format*, not on the arithmetic. A multiple-step income statement shows gross profit, cost of goods sold, and a sales revenue section — but **never an "investing activities section"**, which belongs to the [[09 - Plant Assets, Natural Resources and Intangible Assets|statement of cash flows]] (Exercise 5).

---

### 7. Appendix 5A — worksheets

**A worksheet enables companies to prepare financial statements before they journalise and post adjusting entries.** The steps in preparing a worksheet for a merchandising company are **the same as for a service company**; the unique accounts for a merchandiser using a perpetual system are Inventory, Cost of Goods Sold, Sales Returns and Allowances, Sales Discounts and Freight-Out.

---

### 8. Appendix 5B — the periodic inventory system

Under a periodic system:

- **No running account of changes in inventory.**
- **Ending inventory determined by physical count.**
- **Cost of goods sold not determined until the end of the period.**

**Recording rules:**

- **Record revenues when sales are made.**
- **Do NOT record cost of merchandise sold on the date of sale.**
- **A physical inventory count determines** the cost of merchandise on hand and the cost of merchandise sold during the period.
- **Record purchases in a Purchases account.**
- **Purchase returns and allowances, purchase discounts, and freight costs are recorded in separate accounts.**

#### The same transactions, periodic

| Event | **Perpetual** | **Periodic** |
|---|---|---|
| Purchase $3,800 on credit | Dr **Inventory** 3,800 / Cr AP 3,800 | Dr **Purchases** 3,800 / Cr AP 3,800 |
| Freight-in $150 | Dr **Inventory** 150 / Cr Cash 150 | Dr **Freight-In** 150 / Cr Cash 150 |
| Return $300 | Dr AP 300 / Cr **Inventory** 300 | Dr AP 300 / Cr **Purchase Returns and Allowances** 300 |
| Pay $3,500 less 2% | Dr AP 3,500 / Cr Cash 3,430, Cr **Inventory** 70 | Dr AP 3,500 / Cr Cash 3,430, Cr **Purchase Discounts** 70 |
| Sale $3,800 (cost $2,400) | Dr AR 3,800 / Cr Sales 3,800<br>**Dr COGS 2,400 / Cr Inventory 2,400** | Dr AR 3,800 / Cr Sales 3,800<br>**(no second entry)** |
| Sales return $300 | Dr Sales R&A 300 / Cr AR 300<br>**Dr Inventory 140 / Cr COGS 140** | Dr Sales R&A 300 / Cr AR 300<br>**(no second entry)** |
| Receive $3,430 | Dr Cash 3,430, Dr Sales Discounts 70 / Cr AR 3,500 | **Identical** |

> [!important] Two rules capture the entire difference
> **1. Perpetual routes everything through *Inventory*; periodic uses four separate temporary accounts** (Purchases, Freight-In, Purchase Returns and Allowances, Purchase Discounts).
>
> **2. Under a periodic system there is NO cost-of-goods-sold entry at the point of sale.** COGS is computed once, at the period end, from
> $$\text{COGS} = \text{Beginning inventory} + \text{Net purchases} - \text{Ending inventory}$$
> where net purchases $=$ Purchases $+$ Freight-In $-$ Returns and allowances $-$ Discounts.
>
> **Note that the *sales* side is nearly identical** in both systems — Sales Revenue, Sales Returns and Allowances and Sales Discounts work the same way. **All the difference is on the purchase and cost side.**

---

## ✏️ Exercises

### Exercise 1 — True or false (lecture DO IT!)

1. The primary source of revenue for a merchandising company results from performing services for customers.
2. The operating cycle of a service company is usually shorter than that of a merchandising company.
3. Sales revenue less cost of goods sold equals gross profit.
4. Ending inventory plus the cost of goods purchased equals cost of goods available for sale.

> [!example]- Solution
> 1. **False.** A merchandiser's primary revenue comes from **selling goods** — that is what makes it a merchandiser rather than a service company. The wording describes a service business.
> 2. **True.** A merchandiser must buy and hold inventory before selling, adding a step to the cycle and lengthening it.
> 3. **True.** This is the definition of gross profit.
> 4. **False.** It is **BEGINNING** inventory plus cost of goods purchased:
> $$\text{Goods available for sale} = \textbf{Beginning} \text{ inventory} + \text{Net purchases}$$
> $$\text{COGS} = \text{Goods available for sale} - \textbf{Ending} \text{ inventory}$$
> **Ending inventory is *subtracted*, never added.** Swapping beginning and ending is the most common error in the COGS formula, and it inverts the whole calculation.

---

### Exercise 2 — Perpetual system multiple choice

**(a)** In a perpetual inventory system, a return of defective merchandise by a purchaser is recorded by crediting:
1. Purchases 2. Purchase Returns 3. Purchase Allowance 4. Inventory

**(b)** The cost of goods sold is determined and recorded each time a sale occurs in:
1. a periodic inventory system only 2. a perpetual inventory system only 3. both 4. neither

> [!example]- Solution
> **(a) Answer: 4 — Inventory.**
>
> Under a **perpetual** system, everything runs through the Inventory account. The goods have physically gone back to the supplier, so **the asset must fall**.
>
> **Options 1, 2 and 3 are all *periodic*-system account names** — this is a pure "do you know which system you're in?" question. Under a periodic system the answer would be Purchase Returns and Allowances.
>
> **(b) Answer: 2 — a perpetual inventory system only.**
>
> This is the defining feature of the perpetual system: **every sale triggers a second entry** (Dr COGS / Cr Inventory). Under a periodic system, COGS is not known until the year-end count, so no entry can be made at the point of sale.
>
> **Both questions test the same underlying distinction** from two directions. If you can state "perpetual = Inventory account + COGS entry at each sale; periodic = separate temporary accounts + COGS computed at year end", you can answer either.

---

### Exercise 3 — Purchase transactions (lecture DO IT!)

On September 5, De La Hoya Company buys merchandise on account from Junot Diaz Company. The selling price of the goods is **$1,500**, and the cost to Diaz Company was **$800**. On September 8, De La Hoya returns defective goods with a selling price of **$200**. Record the transactions **on the books of De La Hoya Company** (the buyer).

> [!example]- Solution
> **Sept. 5 — purchase:**
> $$\text{Dr Inventory } 1{,}500 \;/\; \text{Cr Accounts Payable } 1{,}500$$
>
> **Sept. 8 — return:**
> $$\text{Dr Accounts Payable } 200 \;/\; \text{Cr Inventory } 200$$
>
> ---
> **The $800 is a deliberate distractor.**
>
> **$800 is Diaz's cost, not De La Hoya's.** De La Hoya paid $1,500 — that is *its* cost of inventory. The buyer neither knows nor cares what the seller paid; the seller's margin is not the buyer's business.
>
> The $800 becomes relevant **only in the seller's books** (Exercise 4), where it is the cost of goods sold.
>
> **The general principle:** the same transaction has **different amounts** in the two sets of books. Selling price is the seller's *revenue* and the buyer's *cost*. There is no single "value" of a transaction — it depends whose accounts you are writing.
>
> After both entries, De La Hoya's Inventory stands at $1,300 and Accounts Payable at $1,300.

---

### Exercise 4 — Sales transactions (lecture DO IT!)

Same facts, but record them **on the books of Junot Diaz Company** (the seller). On September 8, the returned defective goods have a selling price of $200 and a **fair value of $30**.

> [!example]- Solution
> **Sept. 5 — the sale, two entries:**
> $$\text{Dr Accounts Receivable } 1{,}500 \;/\; \text{Cr Sales Revenue } 1{,}500$$
> $$\text{Dr Cost of Goods Sold } 800 \;/\; \text{Cr Inventory } 800$$
>
> **Sept. 8 — the return, two entries:**
> $$\text{Dr Sales Returns and Allowances } 200 \;/\; \text{Cr Accounts Receivable } 200$$
> $$\text{Dr Inventory } 30 \;/\; \text{Cr Cost of Goods Sold } 30$$
>
> ---
> **Why the second return entry is $30, not the proportionate cost.**
>
> The goods sold for $200 and originally cost roughly $200 \times \tfrac{800}{1500} \approx \$107$. But **they came back defective, with a fair value of only $30.** You cannot put an asset back on the books at more than it is worth.
>
> So Inventory is restored at **$30**, and the remaining ~$77 of cost **stays in Cost of Goods Sold** — a real loss borne by the seller, correctly reflected in the period's profit.
>
> **Compare with the non-defective case** in §4 ($300 selling price, $140 cost, restored at $140): when goods come back saleable, the full original cost is restored and no loss arises.
>
> **Net effect on Diaz's profit:**
> $$\underbrace{1{,}500-200}_{\text{net sales } 1{,}300} - \underbrace{(800-30)}_{\text{net COGS } 770} = \mathbf{\$530 \text{ gross profit}}$$
> versus $700 had nothing been returned — the $200 return cost $170 of gross profit, of which $77 is the write-down on defective goods.

---

### Exercise 5 — Income statement format

**(a)** The multiple-step income statement for a merchandiser shows each of the following features **except**:
1. gross profit 2. cost of goods sold 3. a sales revenue section 4. investing activities section

**(b)** Using Celine's Sports Wear Shop figures from §5, prepare a multiple-step income statement and compute the gross profit rate.

> [!example]- Solution
> **(a) Answer: 4 — investing activities section.**
>
> An **investing activities section** belongs to the **statement of cash flows**, not the income statement. Options 1, 2 and 3 are all present in a multiple-step format; "non-operating activities" (other revenues/gains and other expenses/losses) is a different thing entirely from "investing activities".
>
> **The trap is the plausibility of the wording** — "investing activities" sounds like it could be the non-operating section. **Know which statement each section belongs to.**
>
> **(b) Multiple-step income statement:**
>
> | | $ | $ |
> |---|---|---|
> | Sales revenue | | 162,400 |
> | Less: Sales returns and allowances | 4,800 | |
> | Less: Sales discounts | 3,600 | (8,400) |
> | **Net sales** | | **154,000** |
> | Cost of goods sold | | (110,000) |
> | **Gross profit** | | **44,000** |
> | *Operating expenses:* | | |
> | Freight-out | 1,800 | |
> | Rent expense | 8,800 | |
> | Salaries and wages expense | 22,000 | (32,600) |
> | **Income from operations** | | **11,400** |
> | *Other revenues:* Rent revenue | | 6,000 |
> | **Net income** | | **17,400** |
>
> **Cross-check against the closing entries in §5:** $168{,}400 - 151{,}000 = \$17{,}400$ ✓
>
> **Gross profit rate:**
> $$\frac{\text{Gross profit}}{\text{Net sales}} = \frac{44{,}000}{154{,}000} = \mathbf{28.6\%}$$
>
> ---
> **Four presentation decisions worth noting:**
>
> **1. Gross profit rate uses *net* sales, not gross sales.** Using $162,400 would give 27.1% and overstate performance by ignoring returns and discounts.
>
> **2. Freight-out is an operating expense, not part of cost of goods sold.** It is a cost of *delivering to customers*, not of *acquiring goods* — see §3. Putting it in COGS would understate gross profit to $42,200.
>
> **3. Rent revenue sits below income from operations.** Celine's is a clothing shop; renting out space is incidental. **Placing it above the operating line would inflate apparent trading performance.**
>
> **4. Inventory ($25,000) does not appear at all.** It is a balance-sheet item. **Only its *change*, embedded in cost of goods sold, affects profit.**
>
> **The single-step version** would simply be: total revenues $(162{,}400+6{,}000) = 168{,}400$ less total expenses $151{,}000$ = **$17,400**. Same answer, none of the four insights above.

---

### Exercise 6 — Perpetual vs periodic, side by side

Rework the complete PW Audio / Sauk Stereo sequence under a **periodic** system, then compute cost of goods sold assuming PW Audio had beginning inventory of $18,000 and ending inventory of $21,000, with total purchases for the period of $95,000, freight-in $2,400, purchase returns $3,100 and purchase discounts $1,700.

> [!example]- Solution
> **Sauk Stereo's entries (buyer), periodic:**
>
> | Date | Entry |
> |---|---|
> | May 4 | Dr **Purchases** 3,800 / Cr Accounts Payable 3,800 |
> | May 6 | Dr **Freight-In** 150 / Cr Cash 150 |
> | May 8 | Dr Accounts Payable 300 / Cr **Purchase Returns and Allowances** 300 |
> | May 14 | Dr Accounts Payable 3,500 / Cr Cash 3,430, Cr **Purchase Discounts** 70 |
>
> **PW Audio's entries (seller), periodic:**
>
> | Date | Entry |
> |---|---|
> | May 4 | Dr Accounts Receivable 3,800 / Cr Sales Revenue 3,800 &nbsp;&nbsp;*(no COGS entry)* |
> | May 8 | Dr Sales Returns and Allowances 300 / Cr Accounts Receivable 300 &nbsp;&nbsp;*(no COGS entry)* |
> | May 14 | Dr Cash 3,430, Dr Sales Discounts 70 / Cr Accounts Receivable 3,500 |
>
> **Note the seller's entries are identical to perpetual except that the two cost entries vanish.**
>
> ---
> **Cost of goods sold for the period:**
>
> | | $ | $ |
> |---|---|---|
> | Beginning inventory | | 18,000 |
> | Purchases | 95,000 | |
> | Add: Freight-in | 2,400 | |
> | Less: Purchase returns and allowances | (3,100) | |
> | Less: Purchase discounts | (1,700) | |
> | **Net purchases** | | **92,600** |
> | **Cost of goods available for sale** | | **110,600** |
> | Less: Ending inventory | | (21,000) |
> | **Cost of goods sold** | | **89,600** |
>
> $$18{,}000 + (95{,}000+2{,}400-3{,}100-1{,}700) - 21{,}000 = \mathbf{\$89{,}600}$$
>
> ---
> **Three things this reveals:**
>
> **1. Freight-in is ADDED, returns and discounts are SUBTRACTED.** Freight increases what the goods cost you; returns and discounts reduce it. **Getting a sign wrong here is worth several marks** — and note that freight-*in* enters COGS while freight-*out* is an operating expense.
>
> **2. The four temporary accounts all feed into one number.** Under a perpetual system they would have been four adjustments to a single Inventory account, giving the same $89,600 continuously rather than once a year.
>
> **3. Shrinkage is invisible.** If $600 of goods had been stolen, the ending count would be $20,400 instead of $21,000, and COGS would come out at $90,200. **The theft is silently absorbed into cost of goods sold** — the periodic system reports it as if the goods had been sold, and management learns nothing. **This is the single strongest argument for a perpetual system**, and it is exactly what the §5 shrinkage entry makes visible.

---

## 📝 Summary

- **A merchandiser buys and sells goods.** Its income statement inserts a step: $\text{Sales} - \text{COGS} = \text{Gross profit}$, then $-\text{Operating expenses} = \text{Net income}$. **COGS is not used in a service business.** The operating cycle is longer because inventory sits between cash and sale.
- **Perpetual system:** detailed records of each purchase and sale; inventory known continuously; **COGS determined at each sale.** **Periodic system:** no detailed records; **COGS inferred at the period end** as
  $$\text{COGS} = \text{Beginning inventory} + \text{Net purchases} - \text{Ending inventory}$$
  Perpetual gives better control and reveals shrinkage; periodic hides it.
- **Perpetual purchases** all run through **Inventory**: purchase (Dr), freight-in (Dr), returns (Cr), discounts (Cr).
- **FOB shipping point** — ownership passes when the carrier accepts the goods; **buyer** pays freight and **capitalises** it into Inventory. **FOB destination** — ownership stays with the seller until delivery; **seller** pays and records **Freight-Out**, an operating expense.
- **Credit terms:** 2/10, n/30 means 2% off within 10 days, net in 30. **Forgoing a 2/10, n/30 discount costs 36.5% annualised** — almost always take it.
- **Every sale needs two entries**: revenue at selling price, and **Dr COGS / Cr Inventory at cost**. **Returns also need two**, with the second restoring inventory at original cost if saleable, or at **fair/scrap value** if defective.
- **Sales Returns and Allowances** and **Sales Discounts** are **contra-revenue** accounts, kept separate so that returns and discounts remain visible as a percentage of sales.
- **The merchandiser's extra adjusting entry** compares perpetual records against a physical count: **Dr COGS / Cr Inventory** for shrinkage. **Inventory is never closed** — it is a permanent account.
- **Multiple-step** income statements show net sales → gross profit → income from operations → net income and separate operating from non-operating activities; **single-step** simply nets total revenues against total expenses. **Both give the same net income.**

---

## ⚠️ Important Notes

> [!warning] Never forget the second entry on a sale
> $$\text{Dr COGS} \;/\; \text{Cr Inventory}$$
> Omitting it **overstates profit by the full cost of the goods** and leaves phantom inventory on the balance sheet. Under a perpetual system, **a sale is never one entry.**

> [!warning] Freight-in vs freight-out
> | | Paid by | Account | Effect |
> |---|---|---|---|
> | **Freight-in** | Buyer | **Inventory** (capitalised) | Becomes an expense only when the goods are sold |
> | **Freight-out** | Seller | **Freight-Out** (operating expense) | Expensed immediately |
>
> Putting freight-out into cost of goods sold understates gross profit; capitalising it into inventory would be worse still.

> [!warning] Discounts are computed after returns
> $(3{,}800-300)\times2\% = \$70$, **not** $3{,}800\times2\%$. You cannot claim a discount on goods you returned.

> [!warning] Inventory is not closed
> Closing entries cover **temporary** accounts only: revenues, expenses, contra-revenues, drawings. **Inventory, Accounts Receivable and Accounts Payable are permanent** and carry forward. Contra-revenue accounts *are* closed — with the expenses, because they carry debit balances.

> [!tip] Beginning vs ending inventory in the COGS formula
> $$\text{Beginning} \;\textbf{+}\; \text{Purchases} \;\textbf{−}\; \text{Ending} = \text{COGS}$$
> **Beginning is added; ending is subtracted.** A useful sanity check: if ending inventory *rises*, COGS *falls* — you bought more than you sold, so less of the cost belongs to this period.

> [!note] Which system a question is using — spot it in one line
> - Sees "Dr Inventory" on a purchase → **perpetual**.
> - Sees "Dr Purchases" → **periodic**.
> - A COGS entry at the point of sale → **perpetual**.
> - "Purchase Returns and Allowances" or "Freight-In" as account names → **periodic**.
>
> **Establish the system before writing anything**, because every purchase-side entry differs.

> [!warning] Gaps in the source slides
> This deck is Weygandt's own Chapter 5 set and is largely complete in text, but **all illustrations are images.**
> - **Fifteen slides are image-only or near-empty:** Illustrations 5-1 (income measurement diagram), 5-2 and 5-3 (operating cycles), 5-4 (flow of costs), 5-6 (the sales invoice used throughout), 5-7 (shipping terms diagram), 5-14 (the multiple-step statement, spread over **six** build slides 46–51), 5-15 (single-step), 5-16 (classified balance sheet), 5A-1 (the worksheet), 5B-2 and 5B-3.
> - **The multiple-step income statement itself never appears in text** — slides 46–51 are six successive builds of Illustration 5-14, all images, with only the "key items" bullet list extracting. **The format in §6 is reconstructed** from the key items and standard Weygandt layout.
> - **The closing-entry slides (40–42) are image-only**, so the Income Summary mechanism and the closing of Income Summary to Owner's Capital are not shown. Only the Celine's DO IT! answers survive.
> - **The financial statement classification DO IT! (slides 57–59) is entirely image-based** — the list of accounts to classify and all answers are lost.
> - **Appendix 5A (worksheets) is one paragraph plus one image.** The worksheet itself cannot be seen.
> - **The periodic cost-of-goods-sold schedule (Illustration 5B-2) is an image**; the layout in Exercise 6 is my own reconstruction from the formula given on slide 7.
> - **No inventory costing methods appear** (FIFO, LIFO, weighted average) — deferred to [[07 - Inventories]], which is correct, but it means this chapter cannot compute the "ending inventory" figure its own formula depends on.

---

**Previous:** [[05 - Adjusting Entries]] · **Next:** [[07 - Inventories]] · **Index:** [[00-Index]]

#accounting #merchandising #inventory #perpetual #periodic #cogs #discounts #fob
