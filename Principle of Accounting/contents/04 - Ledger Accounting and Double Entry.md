---
subject: Principle of Accounting
chapter: 04
tags: [ds, accounting, double-entry, debits-credits, ledger, discounts, vat]
source: "documents/slides/ch04. Ledger accounting and double entry.pptx (Doan Thuy Duong, SAA); Weygandt, Kimmel & Kieso, *Accounting Principles*, 13th ed., Ch. 2"
---

# Ledger Accounting and Double Entry

> [!abstract] Where this sits in the course
> This is **the mechanical heart of the whole course.** [[02 - The Accounting Equation]] showed that every transaction has at least two effects; [[03 - Accounting Transactions and Documents]] catalogued the four transaction types. **This chapter gives those two effects names — debit and credit — and a systematic place to record them.** Everything from [[05 - Adjusting Entries]] onward assumes complete fluency with what follows.
>
> If you learn one thing perfectly in this subject, make it the debit/credit rules in §2.

---

## 📘 Main Knowledge

### 1. Ledgers

**Ledger (books)** — the collection of accounts in which transactions are recorded.

| Ledger | Contents | Part of double entry? |
|---|---|---|
| **Nominal ledger** (general ledger) | Separated ledger accounts — **part of the double entry system**; used to produce the financial statements | ✅ **Yes** |
| **Receivable ledger** | Personal accounts — one per credit customer | ❌ **No** |
| **Payable ledger** | Personal accounts — one per credit supplier | ❌ **No** |

**The personal accounts are separate from the nominal ledger and are not part of the double entry system — they are used for memorandum only.**

> [!important] Why personal ledgers sit outside double entry
> The nominal ledger has **one** "Trade receivables" account holding the total owed by all customers. That total is what appears on the statement of financial position and what participates in double entry.
>
> But a business also needs to know **who** owes what — so it keeps a **receivables ledger** with one personal account per customer. These are a *breakdown* of the control account, not additional entries. Including them in the double entry would **double-count** every credit sale.
>
> **The control-account check:** the sum of all personal account balances must equal the nominal ledger's Trade receivables balance. Any difference means an error in one or the other. This is a standard exam topic and a genuinely useful reconciliation in practice.
>
> "Memorandum only" means exactly this: **useful record, not part of the arithmetic.**

#### The form of a ledger account

**An account is a record of increases and decreases in a specific asset, liability, equity, revenue, or expense item.**

$$
\textbf{Debit} = \text{“Left”}
\qquad\qquad
\textbf{Credit} = \text{“Right”}
$$

An account can be illustrated in **T-account** form:

```
              Cash at bank
   ─────────────────┬─────────────────
      DEBIT (Dr)    │    CREDIT (Cr)
        left        │       right
   ─────────────────┴─────────────────
```

> [!note] Debit and credit have **no** everyday meaning here
> They do **not** mean "good/bad", "increase/decrease", or "money in/money out". **They mean left and right — nothing more.** Whether a debit increases or decreases an account depends entirely on what type of account it is (§2).
>
> The terms come from Latin: *debere* (to owe) and *credere* (to entrust). Trying to reason from that etymology is more confusing than helpful. **Learn "debit = left, credit = right" and let the rules in §2 do the rest.**
>
> Note also that a bank calling your account "credited" means *their* books, where your deposit is a liability to them. That is why bank statements appear to use the terms backwards — they are not; you are just reading someone else's ledger.

---

### 2. Double entry bookkeeping

**Double entry bookkeeping is the method used to record transactions into accounting systems.**

**The duality effect:** each transaction has an **equal but opposite effect** (increase/decrease). Each transaction **must affect two or more accounts** to keep the basic accounting equation in balance. Recording is done by **debiting at least one account and crediting another**.

$$
\boxed{\;\textbf{DEBITS must equal CREDITS}\;}
$$

#### The rules

$$
\underbrace{\text{Assets}}_{\text{Dr}\uparrow} = \underbrace{\text{Liabilities}}_{\text{Cr}\uparrow} + \underbrace{\text{Equity}}_{\text{Cr}\uparrow} - \underbrace{\text{Expenses}}_{\text{Dr}\uparrow} + \underbrace{\text{Revenue}}_{\text{Cr}\uparrow}
$$

| Account type | Statement | Increase by | Decrease by | **Normal balance** |
|---|---|---|---|---|
| **Asset** | Financial position | **Debit** | Credit | **Debit** |
| **Expense** | Profit and loss | **Debit** | Credit | **Debit** |
| **Liability** | Financial position | **Credit** | Debit | **Credit** |
| **Equity / Capital** | Financial position | **Credit** | Debit | **Credit** |
| **Revenue** | Profit and loss | **Credit** | Debit | **Credit** |

> [!important] The one mnemonic worth memorising: **DEAD CLIC**
> **D**ebit increases: **E**xpenses, **A**ssets, **D**rawings
> **C**redit increases: **L**iabilities, **I**ncome, **C**apital
>
> Everything in this course follows from those six words. If you can recall DEAD CLIC under exam pressure, you can construct any journal entry from first principles.
>
> **Why it works.** Assets and expenses are both *uses* of funds — where the money went. Liabilities, income and capital are all *sources* — where the money came from. **Debits record uses; credits record sources.** Every transaction has a source and a use, which is why every entry has a debit and a credit.

#### Where drawings sit

**Drawings** reduce capital, and capital increases with credits — so **drawings increase with a debit**. It is kept as a separate account rather than being debited straight to capital, so that the total withdrawn over the year is visible. At the year end it is closed against capital.

> [!warning] Drawings is a debit-balance account inside equity
> This surprises people, because equity normally has a credit balance. Think of it as a **negative equity account**: it accumulates on the debit side and is subtracted from capital. **Expenses work the same way** relative to revenue — which is why both appear on the debit-increase side of DEAD CLIC despite sitting in the equity half of the equation.

#### Worked examples from the lecture

| # | Transaction | Analysis | Entry |
|---|---|---|---|
| **1** | Put more cash at bank: $1,000 | Cash at bank ↑ $1,000 (asset); Capital ↑ $1,000 | **Dr** Cash at bank 1,000 <br> &nbsp;&nbsp;&nbsp;&nbsp;**Cr** Capital 1,000 |
| **2** | Selling goods on credit: $500 | Revenue ↑ 500; Trade receivable ↑ 500 (asset) | **Dr** Trade receivable 500 <br> &nbsp;&nbsp;&nbsp;&nbsp;**Cr** Revenue 500 |
| **3** | Received cash from credit customer | Cash ↑ 500 (asset); Trade receivable ↓ 500 (asset) | **Dr** Cash 500 <br> &nbsp;&nbsp;&nbsp;&nbsp;**Cr** Trade receivable 500 |
| **4** | Issue bank loan: $2,000 | Bank loan ↑ 2,000 (liability); Cash ↑ 2,000 (asset) | **Dr** Cash 2,000 <br> &nbsp;&nbsp;&nbsp;&nbsp;**Cr** Bank loan 2,000 |

> [!tip] The three-question method for any transaction
> Work through these in order and the entry writes itself:
> 1. **Which two (or more) accounts are affected?**
> 2. **What type is each?** (Asset / liability / equity / revenue / expense)
> 3. **Is each going up or down?** Then apply DEAD CLIC.
>
> **Example 2 worked:** (1) Trade receivable and Revenue. (2) Asset and revenue. (3) Both increasing — asset up = debit, revenue up = credit. Therefore **Dr Trade receivable, Cr Revenue**. ✓
>
> **Examples 1 and 4 are worth comparing.** Both bring in cash and both credit something — but example 1 credits **Capital** (owed to the owner) and example 4 credits **Bank loan** (owed to a third party). Identical cash effect, completely different accounting. This is the **business entity concept** from [[02 - The Accounting Equation]] appearing in the mechanics.

---

### 3. Double entry for the four transaction types

**There are 4 basic transactions learnt from [[03 - Accounting Transactions and Documents|chapter 3]]:** credit transactions (credit sale, credit purchase), cash transactions (cash sale, cash purchase), petty cash transactions, and payroll transactions.

---

### 3.1 Credit purchases (the buyer)

$$
\textbf{Dr Purchases } 100 \;/\; \textbf{Cr Trade payable } 100
$$

#### Two kinds of discount

| Discount | Also called | Treatment |
|---|---|---|
| **Trade discount** | Bulk discount | **Purchases are recorded net of trade discount** — the discount never appears in the books at all |
| **Early settlement discount** | Cash discount | Depends on whether the discount is *expected to be taken* (§ below) |

> [!important] Trade discount vs settlement discount
> A **trade discount** is a reduction in the *price itself*, given for buying in volume or for being a trade customer. It is unconditional, so the invoice is simply for the lower amount. **Record the net figure and forget the discount ever existed.**
>
> An **early settlement discount** is *conditional* — you get it only if you pay within an agreed period. At the time of purchase, whether you will earn it is **uncertain**, and that uncertainty is what makes the accounting interesting.

#### Early settlement discount — buyer

The treatment depends on what you **expect** at the time of purchase. List price 100, discount 5 (so 95 if paid early).

**Case A — discount *expected* to be taken.** Record net at 95:

$$
\text{Dr Purchases } 95 \;/\; \text{Cr Trade payable } 95
$$

| Then what happens | Entry |
|---|---|
| **Paid within agreed term** (as expected) | Dr Trade payable 95 / Cr Cash 95 |
| **Paid over agreed term** (discount lost) | Dr Trade payable 95, **Dr Purchases 5** / Cr Cash 100 |

**Case B — discount *not* expected to be taken.** Record gross at 100:

$$
\text{Dr Purchases } 100 \;/\; \text{Cr Trade payable } 100
$$

| Then what happens | Entry |
|---|---|
| **Paid over agreed term** (as expected) | Dr Trade payable 100 / Cr Cash 100 |
| **Paid within agreed term** (discount earned) | Dr Trade payable 100 / Cr Cash 95, **Cr Purchases 5** |

> [!important] The principle behind all four entries
> **Record your best estimate at the time of purchase; adjust *purchases* if the estimate turns out wrong.**
>
> The correcting entry always goes to **Purchases**, not to a separate discount account. The logic: an early settlement discount is a **reduction in the cost of the goods**, so it belongs in the same place as the goods.
>
> **Check each case sums correctly.** Case A, paid late: the payable of 95 is cleared, an extra 5 of cost is recognised, and 100 leaves the bank — $95+5 = 100$ ✓. Case B, paid early: the payable of 100 is cleared, only 95 leaves the bank, and 5 of cost is removed — $95+5=100$ ✓.
>
> This is the **IFRS 15 variable-consideration** approach: estimate the amount you expect, then true it up. It replaced an older method that recorded gross and posted discounts to a separate "discounts received" income account — **you may see the old method in older textbooks; use the method above.**

---

### 3.2 Credit sales (the seller)

$$
\textbf{Dr Trade receivable } 100 \;/\; \textbf{Cr Revenue } 100
$$

**Trade discount = bulk discount ⇒ sales should be recorded net of trade discounts.** Same principle as purchases.

#### Early settlement discount — seller

**Case A — discount *expected* to be taken.** Record net at 95:

$$
\text{Dr Trade receivable } 95 \;/\; \text{Cr Revenue } 95
$$

| Then what happens | Entry |
|---|---|
| **Paid within agreed term** (as expected) | Dr Cash 95 / Cr Trade receivable 95 |
| **Paid over agreed term** (discount not taken) | Dr Cash 100 / Cr Trade receivable 95, **Cr Revenue 5** |

**Case B — discount *not* expected to be taken.** Record gross at 100:

$$
\text{Dr Trade receivable } 100 \;/\; \text{Cr Revenue } 100
$$

| Then what happens | Entry |
|---|---|
| **Paid over agreed term** (as expected) | Dr Cash 100 / Cr Trade receivable 100 |
| **Paid within agreed term** (customer took it) | Dr Cash 95, **Dr Revenue 5** / Cr Trade receivable 100 |

> [!tip] Seller and buyer are exact mirrors
> Every seller entry is the buyer entry with debits and credits swapped, and Purchases replaced by Revenue:
>
> | | Buyer | Seller |
> |---|---|---|
> | Initial | Dr **Purchases** / Cr Trade payable | Dr Trade receivable / Cr **Revenue** |
> | Adjustment | to **Purchases** | to **Revenue** |
> | Discount lost | **Dr** Purchases (cost up) | **Cr** Revenue (income up) |
> | Discount taken | **Cr** Purchases (cost down) | **Dr** Revenue (income down) |
>
> **Learn one side properly and you get the other for free.** In an exam, always ask first: *am I the buyer or the seller?*

---

### 3.3 VAT

**VAT is an indirect tax on the supply of goods and services.**

| Trader status | Treatment |
|---|---|
| **Non-registered traders** | **Neither charge VAT on their outputs nor reclaim VAT on their inputs** |
| **Registered traders** | Taxable, or Exempt |

**Sale transaction** (net 500, VAT 100, gross 600):

$$
\text{Dr Trade receivable (including VAT) } 600
$$
$$
\text{Cr Revenue (excluding VAT) } 500
$$
$$
\text{Cr VAT (output VAT) } 100
$$

**Purchase transaction** (net 500, VAT 100, gross 600):

$$
\text{Dr Purchases } 500
$$
$$
\text{Dr VAT (input VAT) } 100
$$
$$
\text{Cr Trade payable } 600
$$

> [!important] For a registered trader, VAT is neither income nor expense
> **Revenue and Purchases are recorded *excluding* VAT; receivables and payables *include* it.**
>
> The reason: the business is merely a **collector** for the tax authority. Output VAT charged to customers is owed onward; input VAT paid to suppliers is reclaimable. Both sit in the **VAT account**, and the net balance is a liability to (or receivable from) the tax authority.
>
> $$\text{Amount payable to tax authority} = \text{Output VAT} - \text{Input VAT}$$
>
> In the two entries above, output VAT 100 and input VAT 100 net to zero — nothing is owed. **VAT never touches profit for a registered trader**, which is why it is excluded from revenue and purchases.
>
> **For a non-registered trader the opposite is true:** they cannot reclaim input VAT, so the VAT they pay on purchases becomes **part of the cost** and *does* reduce profit. Same transaction, different accounting, driven entirely by registration status.

> [!warning] The classic VAT error
> Recording revenue at the **gross** amount. If you post Dr Trade receivable 600 / Cr Revenue 600, you have overstated revenue by 100 and failed to record the liability to the tax authority. **Revenue is always net; receivables are always gross.**

---

### 3.4 Cash transactions

**Cash sale:**
$$
\text{Dr Cash } 100 \;/\; \text{Cr Revenue } 100
$$

**Cash purchase:**
$$
\text{Dr Purchases } 100 \;/\; \text{Cr Cash } 100
$$

**Cash sale and cash purchase also have VAT recorded and posted the same way as credit transactions.**

**Cash transactions also include the payment and receipt of previous credit transactions** — i.e. settling a payable (Dr Trade payable / Cr Cash) or collecting a receivable (Dr Cash / Cr Trade receivable).

> [!note] A cash sale is a credit sale with the two steps collapsed
> Credit sale: Dr Receivable / Cr Revenue, then later Dr Cash / Cr Receivable. Net the two and the receivable cancels, leaving **Dr Cash / Cr Revenue**. **A cash sale is simply both steps at once**, which is why no receivable is created.

---

### 3.5 Petty cash

**At the end of the month**, post the vouchers to their expense accounts:

$$
\text{Dr Postage } 33.5,\quad \text{Dr Travel } 21 \;/\; \text{Cr Petty cash } 54.5
$$

**Top up to the imprest amount:**

$$
\text{Dr Petty cash } 54.5 \;/\; \text{Cr Cash at bank } 54.5
$$

> [!important] Note when the expense is recognised
> The expense is recorded when the **vouchers are processed**, not when the float was created and not when the top-up occurs. Creating or topping up the float is a **transfer between two asset accounts** (cash at bank → petty cash) and affects neither profit nor total assets.
>
> Note also that the top-up **exactly equals the vouchers** (54.5 both times) — that is the imprest system from [[03 - Accounting Transactions and Documents]] working: the reimbursement always restores the float to its fixed amount, so it must equal what was spent.

---

### 3.6 Payroll

**At the end of the month:**

$$
\text{Dr Wages expense } 9{,}600
$$
$$
\text{Cr Cash at bank } 5{,}640
$$
$$
\text{Cr HMRC (PAYE + Employees' NI + Employer's NI) } 3{,}005
$$
$$
\text{Cr Pension trustee (Employees' + Employer's) } 955
$$

Check: $5{,}640+3{,}005+955 = 9{,}600$ ✓

> [!important] One debit, three credits — and this is where the payroll figures land
> **The single debit of 9,600 is the total payroll cost** from [[03 - Accounting Transactions and Documents]] — gross pay *plus* the employer's NI and pension contributions. Not net pay (5,640), not gross pay.
>
> The three credits split it by **who gets the money**:
> - **Cash at bank 5,640** — net pay, leaving immediately to employees
> - **HMRC 3,005** — a **liability**, settled later
> - **Pension trustee 955** — a **liability**, settled later
>
> The two liabilities are the timing gap: the business has *incurred* the cost this month (accruals concept) but pays it over next month. **Until then they sit on the statement of financial position as current liabilities.**
>
> A transaction with more than two accounts is called a **compound entry**. Debits still equal credits; there are simply more of them.

---

## ✏️ Exercises

### Exercise 1 — Basic bookkeeping

*(The lecture's own Exercise 1.)* Record the double entry for each transaction, then compute the closing cash balance.

1. Put in cash of $20,000 as capital
2. Purchase building on credit of $100,000
3. Purchase equipment for cash of $5,000
4. Paid monthly rent of $1,000
5. Collected and paid in takings $600
6. Took out $100 for personal expense

> [!example]- Solution
> | # | Analysis | Entry |
> |---|---|---|
> | 1 | Cash ↑ (asset); Capital ↑ (equity) | **Dr** Cash 20,000 / **Cr** Capital 20,000 |
> | 2 | Building ↑ (asset); Trade payable ↑ (liability) | **Dr** Building 100,000 / **Cr** Trade payable 100,000 |
> | 3 | Equipment ↑ (asset); Cash ↓ (asset) | **Dr** Equipment 5,000 / **Cr** Cash 5,000 |
> | 4 | Rent expense ↑ (expense); Cash ↓ (asset) | **Dr** Rent expense 1,000 / **Cr** Cash 1,000 |
> | 5 | Cash ↑ (asset); Revenue ↑ (revenue) | **Dr** Cash 600 / **Cr** Revenue 600 |
> | 6 | Drawings ↑ (contra-equity); Cash ↓ (asset) | **Dr** Drawings 100 / **Cr** Cash 100 |
>
> **The cash T-account:**
>
> | Cash at bank | Dr | | Cr |
> |---|---|---|---|
> | (1) Capital | 20,000 | (3) Equipment | 5,000 |
> | (5) Takings | 600 | (4) Rent | 1,000 |
> | | | (6) Drawings | 100 |
> | | **20,600** | | **6,100** |
> | **Balance c/d** | | | **14,500** |
>
> $$\text{Closing cash} = 20{,}000 - 5{,}000 - 1{,}000 + 600 - 100 = \mathbf{\$14{,}500}$$
>
> **Full trial balance check:**
>
> | | Dr | Cr |
> |---|---|---|
> | Cash | 14,500 | |
> | Building | 100,000 | |
> | Equipment | 5,000 | |
> | Rent expense | 1,000 | |
> | Drawings | 100 | |
> | Trade payable | | 100,000 |
> | Capital | | 20,000 |
> | Revenue | | 600 |
> | | **120,600** | **120,600** ✓ |
>
> **Three points the exercise is testing:**
> - **(2) is a credit purchase of a non-current asset** — it goes to *Building*, not *Purchases*. "Purchases" is reserved for goods bought **for resale**. Buying a building creates an asset; buying inventory creates a cost of trading.
> - **(3) is an asset swap** — cash converts to equipment. **Not an expense**; profit is unaffected.
> - **(6) is drawings, not an expense.** "Personal expense" is deliberately misleading wording. Profit here is $600 - 1{,}000 = -\$400$ (a loss); had drawings been treated as an expense, the loss would show as $500 — wrong by exactly $100.

---

### Exercise 2 — Multiple choice: ledger entries

*(Lecture Question 1.)* Jones Co has the following transactions:
- Payment of $400 to J Bloggs for a **cash purchase**
- Payment of $250 to J Doe in respect of an **invoice for goods purchased last month**

What are the correct ledger entries to record these transactions?

**A.** Dr Cash 650 / Cr Purchases 650
**B.** Dr Purchases 650 / Cr Cash 650
**C.** Dr Purchases 400, Dr Trade Payables 250 / Cr Cash 650
**D.** Dr Cash 650 / Cr Trade Payables 250, Cr Purchases 400

> [!example]- Solution
> **Answer: C.**
>
> **Take the two transactions separately — that is the whole trick.**
>
> **Payment 1 — cash purchase $400.** Goods are bought *and* paid for now. No payable ever exists:
> $$\text{Dr Purchases } 400 \;/\; \text{Cr Cash } 400$$
>
> **Payment 2 — settling last month's invoice $250.** The purchase was recorded **last month** (Dr Purchases / Cr Trade payable). This month's event is only the **payment**, which clears the liability:
> $$\text{Dr Trade payable } 250 \;/\; \text{Cr Cash } 250$$
>
> **Combined:** Dr Purchases 400, Dr Trade payables 250 / Cr Cash 650 ✓
>
> **Why each wrong option is wrong:**
> - **A** has the entry **completely reversed** — crediting Purchases would *reduce* costs, and debiting Cash would *increase* cash when $650 has just left. Both directions wrong.
> - **B** correctly debits Purchases and credits Cash, but for the **whole $650**. This double-counts the second purchase: it was already expensed last month, and recording it again would overstate this month's purchases by $250.
> - **D** is A's error plus a nonsensical split.
>
> **The examinable point.** *"Goods purchased last month"* means the expense is **already in the books**. Paying for something does not create an expense — **the expense arose when the goods were received** (accruals concept, [[01 - Introduction to Accounting]]). Payment only settles a liability. **B is the trap for anyone who thinks "cash out = expense".**

---

### Exercise 3 — Early settlement discounts, both sides

Alpha sells goods to Beta with a list price of £8,000, a 10% trade discount, and a 4% settlement discount for payment within 14 days. Assume both parties **expect** the discount to be taken.

(a) Entries in Alpha's books at the date of sale. (b) Entries in Beta's books at the date of purchase. (c) Beta pays on day 20 — record it in both sets of books. (d) What if Beta had paid on day 10 instead?

> [!example]- Solution
> **First compute the amounts.**
> - Trade discount 10%: $8{,}000 \times 0.90 = \mathbf{£7{,}200}$ — this is the invoice value; the trade discount **never appears in the books**.
> - Settlement discount 4% of 7,200 $= £288$, so the early-payment amount is $7{,}200 - 288 = \mathbf{£6{,}912}$.
>
> **(a) Alpha (seller), discount expected — record net:**
> $$\text{Dr Trade receivable } 6{,}912 \;/\; \text{Cr Revenue } 6{,}912$$
>
> **(b) Beta (buyer), discount expected — record net:**
> $$\text{Dr Purchases } 6{,}912 \;/\; \text{Cr Trade payable } 6{,}912$$
>
> **(c) Paid on day 20 — outside the 14-day term, so the discount is lost.** Both parties expected 6,912 but 7,200 changes hands; the £288 difference must be recognised.
>
> **Alpha:** more revenue than expected —
> $$\text{Dr Cash } 7{,}200 \;/\; \text{Cr Trade receivable } 6{,}912,\;\; \text{Cr Revenue } 288$$
>
> **Beta:** more cost than expected —
> $$\text{Dr Trade payable } 6{,}912,\;\; \text{Dr Purchases } 288 \;/\; \text{Cr Cash } 7{,}200$$
>
> Both balance: $6{,}912+288 = 7{,}200$ ✓, and the two entries are **exact mirrors**.
>
> **(d) Paid on day 10 — within the term, as expected.** No adjustment is needed, because the original estimate was right:
>
> **Alpha:** Dr Cash 6,912 / Cr Trade receivable 6,912
> **Beta:** Dr Trade payable 6,912 / Cr Cash 6,912
>
> ---
> **Three things worth extracting:**
>
> **1. Trade discount is invisible; settlement discount is not.** The £800 trade discount never appears in any account — the invoice is simply for £7,200. The £288 settlement discount *does* appear, because whether it will be earned was uncertain when the sale was recorded.
>
> **2. Getting the estimate right means no adjustment at all.** Case (d) needs a single simple entry. The complexity in case (c) exists purely because the expectation was wrong. **Estimate well and the bookkeeping is easy.**
>
> **3. The £288 is real money.** For Beta, paying 6 days later cost £288 on a £7,200 invoice — about 4% for 6 days, which annualises to well over 200%. **Settlement discounts are an extremely expensive form of short-term credit to forgo**, and this calculation is a standard working-capital management question.

---

### Exercise 4 — VAT on both sides

A VAT-registered retailer buys goods for £2,400 (including 20% VAT) on credit and sells them for £4,200 (including VAT) for cash.

(a) Record both transactions. (b) Compute the VAT due to the tax authority. (c) Compute gross profit. (d) How would (c) differ if the retailer were **not** VAT registered?

> [!example]- Solution
> **Split gross into net and VAT.** With VAT at 20%, gross = net × 1.2, so net = gross ÷ 1.2:
>
> | | Gross | Net | VAT |
> |---|---|---|---|
> | Purchase | 2,400 | **2,000** | **400** |
> | Sale | 4,200 | **3,500** | **700** |
>
> **(a) Entries.**
>
> *Purchase on credit:*
> $$\text{Dr Purchases } 2{,}000,\;\;\text{Dr VAT (input) } 400 \;/\; \text{Cr Trade payable } 2{,}400$$
>
> *Cash sale:*
> $$\text{Dr Cash } 4{,}200 \;/\; \text{Cr Revenue } 3{,}500,\;\; \text{Cr VAT (output) } 700$$
>
> **(b) VAT due:**
> $$\text{Output VAT} - \text{Input VAT} = 700 - 400 = \mathbf{£300 \text{ payable}}$$
> The VAT account has a credit balance of 300 — a **current liability**.
>
> **(c) Gross profit:**
> $$3{,}500 - 2{,}000 = \mathbf{£1{,}500}$$
> **VAT does not appear.** Revenue and purchases are both net.
>
> **(d) If not VAT registered.** A non-registered trader **cannot reclaim input VAT**, so the £400 becomes part of the cost of the goods. They also **cannot charge output VAT**, so they would either sell at £4,200 with none of it remitted, or at a lower price.
>
> Selling at the same £4,200:
> $$\text{Gross profit} = 4{,}200 - 2{,}400 = \mathbf{£1{,}800}$$
>
> **This looks better — but it is not a real advantage.** Two reasons:
> 1. The registered trader's customers, if themselves registered, **reclaim the £700**, so the price *they* effectively pay is £3,500. The non-registered trader charging £4,200 with no reclaimable VAT is **20% more expensive to a business customer**, so the £4,200 price is not sustainable in a B2B market.
> 2. In a consumer market where no one reclaims, non-registration genuinely is an advantage — which is exactly why VAT registration thresholds exist and why small traders near the threshold pay close attention to them.
>
> **The examinable point: the same transactions produce different accounting depending on registration status**, because for a registered trader VAT is a flow-through, and for a non-registered trader it is a real cost.

---

### Exercise 5 — Compound entries and a trial balance

Record the following in journal form, then prepare a trial balance.

1. Owner invests £45,000 cash.
2. Buys inventory on credit, £12,000 (ignore VAT).
3. Pays wages: gross £8,000; PAYE £1,200; employee NI £640; employer NI £920.
4. Sells goods for £6,000 cash and £9,000 on credit.
5. Receives £5,000 from a credit customer.
6. Pays £7,000 to a supplier.
7. Owner takes £2,500 for personal use.

> [!example]- Solution
> **Journal entries.**
>
> | # | Entry | Dr | Cr |
> |---|---|---|---|
> | 1 | Dr Cash / Cr Capital | 45,000 | 45,000 |
> | 2 | Dr Purchases / Cr Trade payable | 12,000 | 12,000 |
> | 3 | **Dr Wages expense** | **8,920** | |
> | | &nbsp;&nbsp;Cr Cash (net pay) | | 6,160 |
> | | &nbsp;&nbsp;Cr HMRC (PAYE + Ee NI + Er NI) | | 2,760 |
> | 4a | Dr Cash / Cr Revenue | 6,000 | 6,000 |
> | 4b | Dr Trade receivable / Cr Revenue | 9,000 | 9,000 |
> | 5 | Dr Cash / Cr Trade receivable | 5,000 | 5,000 |
> | 6 | Dr Trade payable / Cr Cash | 7,000 | 7,000 |
> | 7 | Dr Drawings / Cr Cash | 2,500 | 2,500 |
>
> **Working for (3) — the compound entry:**
> - Net pay $= 8{,}000 - 1{,}200 - 640 = \mathbf{£6{,}160}$ (cash to employees)
> - HMRC $= 1{,}200 + 640 + 920 = \mathbf{£2{,}760}$ (liability)
> - **Wages expense = total payroll cost** $= 8{,}000 + 920 = \mathbf{£8{,}920}$
> - Check: $6{,}160 + 2{,}760 = 8{,}920$ ✓
>
> **Cash movements:** $+45{,}000 - 6{,}160 + 6{,}000 + 5{,}000 - 7{,}000 - 2{,}500 = \mathbf{£40{,}340}$
>
> **Trial balance:**
>
> | Account | Dr | Cr |
> |---|---|---|
> | Cash | 40,340 | |
> | Trade receivable | 4,000 | |
> | Purchases | 12,000 | |
> | Wages expense | 8,920 | |
> | Drawings | 2,500 | |
> | Trade payable | | 5,000 |
> | HMRC | | 2,760 |
> | Capital | | 45,000 |
> | Revenue | | 15,000 |
> | | **67,760** | **67,760** ✓ |
>
> *Trade receivable: $9{,}000-5{,}000 = 4{,}000$. Trade payable: $12{,}000-7{,}000 = 5{,}000$. Revenue: $6{,}000+9{,}000 = 15{,}000$.*
>
> ---
> **What a balanced trial balance does and does not prove.**
>
> **It proves:** total debits equal total credits, so no entry was posted one-sided and no addition error occurred.
>
> **It does NOT prove the books are correct.** Four error types pass undetected:
> 1. **Error of omission** — a transaction left out entirely. Still balances.
> 2. **Error of commission** — right amount, right side, **wrong account** (e.g. rent posted to insurance). Still balances.
> 3. **Error of principle** — e.g. a building posted to Purchases instead of Non-current assets (Exercise 1's trap). Still balances.
> 4. **Compensating errors** — two mistakes that happen to cancel.
>
> **This is the same point as [[03 - Accounting Transactions and Documents]] Exercise 5:** double entry catches arithmetic errors, not wrong judgements and not fraud. **A balanced trial balance is a necessary condition for correct books, never a sufficient one.**

---

## 📝 Summary

- **The nominal ledger** contains the accounts that form the double entry system and produce the financial statements. **Receivable and payable ledgers hold personal accounts and are memorandum only** — they break down a control account, and including them would double-count.
- **Debit = left, credit = right.** Nothing more. Whether a debit increases or decreases depends on the account type.
- **DEAD CLIC:** **D**ebit increases **E**xpenses, **A**ssets, **D**rawings; **C**redit increases **L**iabilities, **I**ncome, **C**apital. Debits record *uses* of funds; credits record *sources*.
- **Every transaction affects two or more accounts** (the duality effect) and **debits must equal credits**, which is what keeps the accounting equation in balance.
- **Credit purchase:** Dr Purchases / Cr Trade payable. **Credit sale:** Dr Trade receivable / Cr Revenue. **Seller and buyer entries are exact mirrors.**
- **Trade discount** is recorded **net** and never appears in the books. **Early settlement discount** is recorded according to whether it is *expected to be taken*, with any correction posted to **Purchases** (buyer) or **Revenue** (seller).
- **VAT:** revenue and purchases are recorded **excluding** VAT; receivables and payables **including** it. Output VAT − input VAT is payable to the tax authority. **VAT never affects profit for a registered trader**; for a non-registered trader, irrecoverable input VAT becomes part of cost.
- **Petty cash:** expenses are recognised when the vouchers are processed (Dr expenses / Cr Petty cash); the top-up (Dr Petty cash / Cr Cash at bank) is a transfer between assets and equals the vouchers exactly.
- **Payroll** is a **compound entry**: one debit to wages expense for the **total payroll cost**, credits to cash (net pay) and to liabilities for HMRC and the pension trustee.

---

## ⚠️ Important Notes

> [!warning] "Purchases" means goods bought for resale
> A building, a vehicle or equipment goes to a **non-current asset** account, not Purchases. Posting a building to Purchases is an **error of principle** — the trial balance still balances, but profit is understated by the full cost and the balance sheet omits the asset. Exercise 1 tests this deliberately.

> [!warning] Paying for something is not always an expense
> Three payments that create **no** expense:
> - Settling a trade payable (the expense arose when the goods were received)
> - Buying a non-current asset (an asset swap)
> - Drawings (a reduction of capital)
>
> **Lecture Question 1's option B is built entirely on this confusion**, and it catches a lot of candidates.

> [!warning] Revenue net, receivables gross
> With VAT in play: **Dr Trade receivable (gross) / Cr Revenue (net), Cr VAT (the difference).** Recording revenue gross overstates income *and* omits the liability to the tax authority. To split a gross figure at a 20% rate, divide by 1.2 — **not** multiply by 0.8.

> [!tip] The three-question method never fails
> 1. Which accounts are affected? 2. What type is each? 3. Up or down? → apply DEAD CLIC.
>
> Under exam pressure this beats trying to recall a memorised entry, because it works for transactions you have never seen.

> [!warning] A balanced trial balance does not mean correct books
> It catches one-sided entries and addition errors. It **cannot** catch omission, commission, principle, or compensating errors. **Double entry guarantees arithmetic consistency, not truth.**

> [!note] Settlement discounts are expensive to forgo
> A 4% discount for paying 6 days early is roughly a 200%+ annualised return on the cash. **Almost always worth taking** if the cash is available — a standard working-capital point that examiners like to attach to a discount question.

> [!warning] Gaps in the source slides
> - **Slide 10 is image-only** — placed immediately after the four worked double-entry examples, it is likely a summary diagram or a further example. Its content is lost.
> - **Slides 21 and 22 (petty cash and payroll) each show only the concluding journal entry**; the tables of vouchers and payroll figures that generate those numbers are images and did not extract. The entries in §3.5 and §3.6 are given exactly as on the slides, but **the workings behind 54.5, 9,600, 5,640, 3,005 and 955 are not visible.**
> - **Slides 25, 26 and 27 (Questions 2, 3 and 4) are image-only.** Question 2 asks for the closing balance on a trade payables T-account, but **the T-account itself did not extract**, so the question cannot be answered. Questions 3 and 4 have no visible content at all. **No answers are provided for any of the four questions.**
> - **Balancing off a ledger account is never demonstrated**, despite Question 2 requiring it. The "balance c/d / balance b/d" technique is standard and is illustrated in Exercise 1 above, but it does not appear in the deck.
> - **The trial balance is never mentioned** — a serious omission, since it is the bridge from the ledger to the financial statements and is presupposed by [[05 - Adjusting Entries]]. Exercise 5 supplies it.
> - **Control accounts and the receivables/payables ledger reconciliation are not covered**, though the deck introduces personal ledgers as "memorandum only".
> - **"Registered traders — Taxable / Exempt"** is stated with no explanation of the difference between zero-rated, exempt and standard-rated supplies, which materially affects whether input VAT is recoverable.

---

**Previous:** [[03 - Accounting Transactions and Documents]] · **Next:** [[05 - Adjusting Entries]] · **Index:** [[00-Index]]

#accounting #double-entry #debits-credits #ledger #discounts #vat #payroll
