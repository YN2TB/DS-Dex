---
subject: Principle of Accounting
chapter: 08
tags: [ds, accounting, receivables, bad-debts, allowance-method, notes-receivable, factoring]
source: "documents/slides/ch07.pptx (Doan Thuy Duong, SAA); Weygandt, Kimmel & Kieso, *Accounting Principles*, 13th ed., Ch. 9"
---

# Accounting for Receivables

> [!abstract] Where this sits in the course
> Selling on credit creates a receivable — and **some customers never pay.** The accruals concept says revenue is recognised at the sale, so the loss must be recognised then too, *before you know which customers will default*.
>
> **That is the central problem of this chapter:** estimating a loss you cannot yet identify. The solution — the **allowance method** — is the clearest example in the course of an accounting estimate, and the second major use of a contra account after [[05 - Adjusting Entries|accumulated depreciation]].

---

## 📘 Main Knowledge

### 1. Types of receivables

> **Receivables are amounts due from individuals and other companies that are expected to be collected in cash.**

| Type | Definition |
|---|---|
| **Accounts receivable** | **Amounts owed by customers on account that result from the sale of goods and services** |
| **Notes receivable** | **A written promise for amounts to be received.** Normally requires the collection of **interest** |
| **Other receivables** | **Non-trade receivables** such as interest, loans to officers, advances to employees, and income taxes |

**Three accounting issues** arise for accounts receivable: **recognising**, **valuing**, and **disposing of** them.

---

### 2. Recognising accounts receivable

- A **service organisation** records a receivable **when it performs service on account.**
- A **merchandiser** records accounts receivable **at the point of sale of merchandise on account.**

Both follow the revenue recognition principle of [[05 - Adjusting Entries]]: recognise when the performance obligation is satisfied.

> **Illustration:** Jordache Co. on July 1, 2017 sells merchandise on account to Polo Company for **$1,000, terms 2/10, n/30.**
> $$\text{Jul 1:}\quad \text{Dr Accounts Receivable } 1{,}000 \;/\; \text{Cr Sales Revenue } 1{,}000$$
>
> **On July 5, Polo returns merchandise worth $100:**
> $$\text{Jul 5:}\quad \text{Dr Sales Returns and Allowances } 100 \;/\; \text{Cr Accounts Receivable } 100$$
>
> **On July 11, Jordache receives payment for the balance due:**
> $$\text{Jul 11:}\quad \text{Dr Cash } 882,\;\; \text{Dr Sales Discounts } 18 \;/\; \text{Cr Accounts Receivable } 900$$
> $$\text{where } 18 = 900 \times 2\%$$

> [!note] Nothing new here — this is [[06 - Accounting for Merchandising Operations]] §4
> The discount is computed **after** the return ($900, not $1,000), and Sales Returns and Allowances and Sales Discounts are both **contra-revenue** accounts. **July 11 is within the 10-day window**, so the discount is earned.
>
> Note also that the second entry of each sale (Dr COGS / Cr Inventory) is omitted throughout this chapter — it exists, but the focus here is the receivable.

> [!warning] Anatomy of a fraud — and the two controls that were missing
> The slides give a real case. **Tasanee** was the accounts receivable clerk for a large non-profit arts foundation. Her responsibilities included recording revenues from donations, facility rental fees, ticket revenue and bar receipts. **She was also responsible for handling all cash and cheques from receipt until deposit, as well as preparing the bank reconciliation.** She falsified bank deposits. **Total take: $1.5 million.**
>
> **The missing controls:**
> 1. **Segregation of duties.** The foundation should not have allowed a clerk whose job was to *record* receivables also to *handle* cash, *record* cash, *make deposits*, and **especially prepare the bank reconciliation**.
> 2. **Independent internal verification.** The controller was supposed to perform a thorough review of the bank reconciliation. **Because he did not, he was terminated.**
>
> This is exactly the point made in [[03 - Accounting Transactions and Documents]] Exercise 5: **double entry catches errors, not fraud.** Every one of Tasanee's entries balanced perfectly. What catches fraud is separating the person who records from the person who holds the asset — and having somebody independent check.

---

### 3. Valuing accounts receivable

Accounts receivable is a **current asset**, valued at **cash realisable value**.

> **Sales on account raise the possibility of accounts not being collected.** Companies record credit losses as debits to **Bad Debt Expense** (also called **Uncollectible Accounts Expense**).

#### Two methods

| | **Direct write-off** | **Allowance method** |
|---|---|---|
| Timing | Expense recorded **when a specific account proves bad** | Losses are **estimated** in the period of sale |
| Matching | ❌ **No matching** | ✅ **Better matching** |
| Balance sheet | ❌ **Receivable not stated at cash realisable value** | ✅ **Receivable stated at cash realisable value** |
| Acceptability | ❌ **Not acceptable for financial reporting** | ✅ **Required by GAAP** |

> **Direct write-off illustration:** Warden Co. writes off M. E. Doran's $200 balance as uncollectible on December 12.
> $$\text{Dr Bad Debt Expense } 200 \;/\; \text{Cr Accounts Receivable — M. E. Doran } 200$$

> [!important] Why the direct write-off method fails
> A sale made in **December 2024** that proves uncollectible in **September 2025** produces revenue in one year and the matching expense in another. **The expense recognition principle is violated outright**, and 2024's profit is overstated while 2025's is understated.
>
> It also leaves the balance sheet wrong: receivables are shown at their full face amount, **as if every customer will pay**, which is never true for a business of any size.
>
> **It survives only for immaterial amounts and for tax purposes in some jurisdictions.** It is not acceptable for financial reporting.

#### The allowance method

> - **Companies estimate uncollectible accounts receivable.**
> - **Debit Bad Debt Expense and credit Allowance for Doubtful Accounts** (a **contra-asset** account).
> - **Companies debit Allowance for Doubtful Accounts and credit Accounts Receivable** at the time a specific account is written off as uncollectible.

> [!important] The two-stage structure — and why it works
> **Stage 1 (estimate, at period end):**
> $$\text{Dr Bad Debt Expense} \;/\; \text{Cr Allowance for Doubtful Accounts}$$
> This is the **only** entry that touches the income statement. It records the expense **in the period of the sale**, satisfying matching, without needing to know *which* customer will default.
>
> **Stage 2 (write-off, when a specific account goes bad):**
> $$\text{Dr Allowance for Doubtful Accounts} \;/\; \text{Cr Accounts Receivable}$$
> This has **no effect on expense, on total assets, or on net income.** It merely moves a known-bad amount out of the receivable and out of the allowance that was already set aside for it. **The loss was recognised in stage 1.**
>
> **This is the same contra-account logic as accumulated depreciation** ([[05 - Adjusting Entries]]): keep the gross receivable visible, deduct the estimated shortfall separately, and preserve both pieces of information.

**Balance sheet presentation:**

$$
\text{Accounts receivable (gross)} - \text{Allowance for doubtful accounts} = \textbf{Cash realisable value}
$$

> **Illustration:** Hampson Furniture has credit sales of $1,200,000 in 2017, of which **$200,000 remains uncollected** at December 31. The credit manager estimates that **$12,000** of these sales will prove uncollectible.
> $$\text{Dec 31:}\quad \text{Dr Bad Debt Expense } 12{,}000 \;/\; \text{Cr Allowance for Doubtful Accounts } 12{,}000$$
>
> | | $ |
> |---|---|
> | Accounts receivable | 200,000 |
> | Less: Allowance for doubtful accounts | (12,000) |
> | **Cash realisable value** | **188,000** |
>
> **The $188,000 represents the expected cash realisable value of the accounts receivable at the statement date.**

#### Write-off and recovery

> **Write-off.** The vice-president of finance of Hampson Furniture on March 1, 2018 authorises a write-off of the **$500** balance owed by R. A. Ware.
> $$\text{Mar 1:}\quad \text{Dr Allowance for Doubtful Accounts } 500 \;/\; \text{Cr Accounts Receivable — R. A. Ware } 500$$

> [!note] Check what the write-off does to the balance sheet
> Before: AR $200,000 − allowance $12,000 = $188,000.
> After: AR $199,500 − allowance $11,500 = **$188,000**.
>
> **Cash realisable value is unchanged, and no expense is recorded.** Both accounts fall by the same $500. This is what "the loss was already recognised" means in practice, and it is the standard exam check.

> **Recovery.** On July 1, R. A. Ware pays the $500 that Hampson had written off on March 1. **Two entries:**
> $$\textbf{1.}\quad \text{Dr Accounts Receivable — R. A. Ware } 500 \;/\; \text{Cr Allowance for Doubtful Accounts } 500$$
> $$\textbf{2.}\quad \text{Dr Cash } 500 \;/\; \text{Cr Accounts Receivable — R. A. Ware } 500$$

> [!important] Why a recovery takes two entries rather than "Dr Cash / Cr Allowance"
> Entry 1 **reverses the write-off**, reinstating the receivable. Entry 2 then records an ordinary collection.
>
> **The reason is the customer's record.** The personal account in the receivables ledger ([[04 - Ledger Accounting and Double Entry]] §1) must show that Ware eventually paid — otherwise the credit history is permanently and unfairly damaged. Collapsing the two entries into one would leave no trace in Ware's account that the debt was settled.
>
> Note again that **no revenue and no expense arise.** The recovery adjusts the allowance, not profit.

---

### 4. Estimating the allowance

Two bases, differing in what they emphasise.

#### Percentage-of-sales

> **Management estimates what percentage of credit sales will be uncollectible**, based on **past experience and anticipated credit policy.**

> **Illustration:** Gonzalez Company concludes that **1% of net credit sales** will become uncollectible. Net credit sales for 2017 are **$800,000**:
> $$\text{Dec 31:}\quad \text{Dr Bad Debt Expense } 8{,}000 \;/\; \text{Cr Allowance for Doubtful Accounts } 8{,}000$$

> **Emphasises matching of expenses with revenues.** The adjusting entry **disregards the existing balance in Allowance for Doubtful Accounts.**

#### Percentage-of-receivables

> **Management establishes a percentage relationship between the amount of receivables and expected losses from uncollectible accounts.**

**Aging the accounts receivable** — **customer balances are classified by the length of time they have been unpaid.** Where appropriate, companies may use **only a single percentage rate.**

> **Illustration:** The unadjusted trial balance shows Allowance for Doubtful Accounts with a **credit balance of $528**. The aging schedule estimates **$2,228** of uncollectible receivables.
> $$\text{Required ending balance } 2{,}228 - \text{existing credit balance } 528 = \$1{,}700$$
> $$\text{Dec 31:}\quad \text{Dr Bad Debt Expense } 1{,}700 \;/\; \text{Cr Allowance for Doubtful Accounts } 1{,}700$$

> [!important] The single most important distinction in this chapter
> | | **Percentage-of-SALES** | **Percentage-of-RECEIVABLES** |
> |---|---|---|
> | Applies the percentage to | Net credit **sales** (income statement) | **Receivables** balance (balance sheet) |
> | Emphasises | **Matching** — getting the *expense* right | **Cash realisable value** — getting the *asset* right |
> | Existing allowance balance | **Ignored** — the computed figure *is* the entry | **Considered** — the computed figure is the required **ending balance**, and the entry is the difference |
>
> **The percentage-of-sales figure is the ENTRY. The percentage-of-receivables figure is the TARGET.**
>
> Getting this backwards is the commonest error in the chapter, and it is exactly what Exercise 3 tests. Under percentage-of-receivables you must **always look at the existing balance first** — and note its *side*, because a debit balance makes the entry *larger*, not smaller.

> [!note] Why aging is more informative
> An invoice 120 days overdue is far more likely to default than one 15 days overdue. Aging applies a **higher percentage to older brackets** — perhaps 2% on current, 5% on 31–60 days, 20% on 61–90, 50% over 90 — which uses information a single flat rate throws away.
>
> **In practice many companies use both:** percentage-of-sales for monthly interim estimates (quick, and matches well), with an aging analysis at the year end to true up the balance.

---

### 5. Disposing of accounts receivable

> **Companies sell receivables for two major reasons:**
> 1. **Receivables may be the only reasonable source of cash.**
> 2. **Billing and collection are often time-consuming and costly.**

#### Sale to a factor

> **A factor is a finance company or bank that buys receivables from businesses and then collects the payments directly from the customers.** It **typically charges a commission** to the company selling the receivables — a fee of **1–3% of the receivables purchased.**

> **Illustration:** Hendredon Furniture factors **$600,000** of receivables to Federal Factors, which assesses a service charge of **2%**.
> $$\text{Dr Cash } 588{,}000,\;\; \text{Dr Service Charge Expense } 12{,}000 \;/\; \text{Cr Accounts Receivable } 600{,}000$$
> $$\text{where } 12{,}000 = 600{,}000 \times 2\%$$

#### Credit card sales

> **Recorded the same as cash sales.** The retailer pays the card issuer a fee of **2 to 6%** for processing the transactions.

> **Illustration:** Anita Ferreri purchases $1,000 of compact discs from Karen Kerr Music Co. using her Visa First Bank Card. First Bank charges a service fee of **3%**.
> $$\text{Dr Cash } 970,\;\; \text{Dr Service Charge Expense } 30 \;/\; \text{Cr Sales Revenue } 1{,}000$$

> [!important] Note what is **not** recorded on a credit card sale
> **No accounts receivable.** The card issuer, not the retailer, bears the collection risk — which is precisely what the 3% fee buys. **Revenue is recorded gross at $1,000**; the fee is a separate expense, not a reduction of revenue.
>
> **Is 3% expensive?** Compare with the alternative: extending credit yourself means administering invoices, chasing payment, waiting weeks for cash, and absorbing bad debts. For most retailers 3% is cheap. The factoring fee of 1–3% prices the same trade-off for trade receivables.

---

### 6. Notes receivable

> **Companies may grant credit in exchange for a promissory note** — **a written promise to pay a specified amount of money on demand or at a definite time.**

**Promissory notes may be used:**
- when individuals and companies **lend or borrow money**,
- when the **amount of the transaction and the credit period exceed normal limits**, or
- **in settlement of accounts receivable.**

> **To the Payee, the promissory note is a note receivable. To the Maker, it is a note payable.**

#### Computing interest and maturity

$$
\boxed{\;\text{Interest} = \text{Face value} \times \text{Annual interest rate} \times \text{Time}\;}
$$

> **The interest rate specified is the ANNUAL rate.**

**Determining the maturity date.** A note may be expressed in **months** or in **days**:

- **Months:** a 3-month note dated 1 May matures 1 August — same day, three months on.
- **Days:** **when counting days, omit the date the note is issued, but include the due date.**

> [!warning] The 360-day convention
> Weygandt computes interest on day-based notes using a **360-day year**, so a 90-day note is exactly one quarter of the annual rate. Some texts and jurisdictions use 365. **Check which the question intends** — with a $3,400 note at 6% for 90 days, the difference is $51.00 versus $50.30.
>
> For **month-based** notes, use $\frac{\text{months}}{12}$, which is unambiguous.

> **Illustration:** Calhoun Company wrote a **$1,000, two-month, 12%** promissory note dated May 1 to settle an open account. Wilma Company records receipt of the note:
> $$\text{May 1:}\quad \text{Dr Notes Receivable } 1{,}000 \;/\; \text{Cr Accounts Receivable } 1{,}000$$

**No revenue or expense arises** — one asset simply replaces another. The lender gains a written promise and (usually) interest; the borrower gains time.

#### Valuing notes receivable

> **Report short-term notes receivable at their cash (net) realisable value.** Estimation of cash realisable value and bad debt expense are done **similarly to accounts receivable**, and **Allowance for Doubtful Accounts is used.**

#### Disposing of notes receivable

> **Notes may be held to their maturity date**; the **maker may default** and the payee must adjust the account; or the **holder may speed up conversion to cash by selling the note.**

| Outcome | Definition |
|---|---|
| **Honour** | **The maker pays it in full at its maturity date** |
| **Dishonour** | **Not paid in full at maturity. No longer negotiable.** |

##### Honour

> **Illustration:** Wolder Co. lends Higley Co. **$10,000** on June 1, accepting a **five-month, 9%** interest note. Wolder presents the note on November 1, the maturity date:
> $$\text{Interest} = 10{,}000 \times 9\% \times \tfrac{5}{12} = \$375$$
> $$\text{Nov 1:}\quad \text{Dr Cash } 10{,}375 \;/\; \text{Cr Notes Receivable } 10{,}000,\;\; \text{Cr Interest Revenue } 375$$

##### Accrual of interest at a period end

> **Illustration:** Suppose Wolder prepares financial statements as of **September 30** — four months into the note:
> $$\text{Interest} = 10{,}000 \times 9\% \times \tfrac{4}{12} = \$300$$
> $$\text{Sept 30:}\quad \text{Dr Interest Receivable } 300 \;/\; \text{Cr Interest Revenue } 300$$
>
> **Then on November 1**, when the note is honoured:
> $$\text{Dr Cash } 10{,}375 \;/\; \text{Cr Notes Receivable } 10{,}000,\;\; \text{Cr Interest Receivable } 300,\;\; \text{Cr Interest Revenue } 75$$

> [!important] The interest splits across two periods — this is [[05 - Adjusting Entries]] in action
> Total interest is $375. Four months ($300) was **earned by 30 September** and belongs to that period's profit; one month ($75) is earned in October and belongs to the next.
>
> On 1 November, **the $300 already recognised is collected by crediting Interest Receivable** — an asset being converted to cash, not new revenue. Only the extra **$75 is Interest Revenue**.
>
> **Crediting the full $375 to revenue would double-count $300**, and it is the standard trap in this question type. Always ask: *has any of this interest already been accrued?*

##### Dishonour

> **Illustration:** Higley Co. on November 1 indicates it cannot pay at present. **If Wolder Co. does expect eventual collection** (assuming no previous accrual of interest):
> $$\text{Nov 1:}\quad \text{Dr Accounts Receivable } 10{,}375 \;/\; \text{Cr Notes Receivable } 10{,}000,\;\; \text{Cr Interest Revenue } 375$$

> [!note] Why interest revenue is still recognised on a dishonoured note
> The interest **was earned** — Higley had the use of the money for five months, and owes for it. **What has changed is the form of the claim, not its existence.** The note is no longer negotiable, so the amount moves to Accounts Receivable, where it will be subject to the normal allowance process.
>
> **The condition matters: "if Wolder does expect eventual collection."** If collection were *not* expected, the whole amount would be written off against the allowance instead, and no interest revenue would be recorded.

---

### 7. Presentation and analysis

**Balance sheet:**
- **Identify each major type of receivable** in the balance sheet or in the notes.
- **Report short-term receivables as current assets.**
- **Report both the gross amount of receivables and the allowance for doubtful accounts.**

**Income statement:**
- **Report bad debt expense and service charge expense as selling expenses.**
- **Report interest revenue under "Other revenues and gains."**

> [!note] Why interest revenue sits below the operating line
> For a furniture retailer, interest is **not** part of trading — it belongs in the non-operating section, exactly as in [[06 - Accounting for Merchandising Operations]] §6. **Bad debt expense, by contrast, is a genuine cost of selling on credit** and stays in operating expenses.

#### Ratios

$$
\boxed{\;\text{Accounts receivable turnover} = \frac{\text{Net credit sales}}{\text{Average net accounts receivable}}\;}
$$

$$
\boxed{\;\text{Average collection period} = \frac{365}{\text{Accounts receivable turnover}}\;}
$$

> **Illustration:** In 2013 Cisco Systems had net sales of **$38,029 million**, a beginning accounts receivable (net) balance of **$4,369 million** and an ending balance of **$5,470 million**. Assuming all sales were on credit:
> $$\text{Average AR} = \frac{4{,}369+5{,}470}{2} = \$4{,}919.5\text{m}$$
> $$\text{Turnover} = \frac{38{,}029}{4{,}919.5} = \mathbf{7.7 \text{ times}}
> \qquad
> \text{Collection period} = \frac{365}{7.7} \approx \mathbf{47.2 \text{ days}}$$

> [!tip] How to read a collection period
> **Compare it against the credit terms offered.** If Cisco's terms are n/30 and customers take 47 days, collection is running **17 days late** — a working-capital drag worth roughly $38{,}029\text{m} \times \frac{17}{365} \approx \$1.8$ billion tied up.
>
> Rules of thumb:
> - **Collection period ≫ credit terms** → weak collection procedures, or customers in difficulty.
> - **Collection period ≪ credit terms** → possibly too strict, losing sales to competitors offering better terms.
> - **Rising trend** → the early warning of a receivables problem, usually visible before bad debts appear.
>
> Note the parallel with **inventory turnover** in [[07 - Inventories]]: same structure (flow ÷ average balance), same conversion to days, same requirement to compare within an industry.

---

### 8. A look at IFRS

**Similarities:**
- **The recording of receivables, recognition of sales returns and allowances and sales discounts, and the allowance method to record bad debts are the same** between GAAP and IFRS.
- **Both often use the term *impairment*** to indicate that a receivable, or a percentage of receivables, may not be collected.

> [!note] IFRS 9 has since moved to an "expected credit loss" model
> The slides describe both frameworks as estimating losses. Since 2018, **IFRS 9** requires a forward-looking **expected credit loss** model — recognising expected losses from day one, rather than waiting for evidence of impairment. **The mechanics in this chapter (allowance account, write-offs, recoveries) are unchanged;** only the basis of the estimate has become more forward-looking.

---

## ✏️ Exercises

### Exercise 1 — Recognising accounts receivable (lecture DO IT!)

On May 1, Wilton sold merchandise on account to Bates for **$50,000**, terms **3/15, net 45**. On May 4, Bates returns merchandise with a sales price of **$2,000**. On May 16, Wilton receives payment from Bates for the balance due. Prepare journal entries on Wilton's books.

> [!example]- Solution
> **May 1 — the sale:**
> $$\text{Dr Accounts Receivable — Bates } 50{,}000 \;/\; \text{Cr Sales Revenue } 50{,}000$$
>
> **May 4 — the return:**
> $$\text{Dr Sales Returns and Allowances } 2{,}000 \;/\; \text{Cr Accounts Receivable — Bates } 2{,}000$$
>
> **May 16 — payment:**
> $$\text{Balance due} = 50{,}000 - 2{,}000 = \$48{,}000
> \qquad
> \text{Discount} = 48{,}000 \times 3\% = \$1{,}440$$
> $$\text{Dr Cash } 46{,}560,\;\; \text{Dr Sales Discounts } 1{,}440 \;/\; \text{Cr Accounts Receivable — Bates } 48{,}000$$
>
> ---
> **Two things the question is checking.**
>
> **1. The discount period.** Terms 3/15 mean 15 days from 1 May, so the last discount day is **16 May**. Payment on the 16th **just qualifies** — one day later and the full $48,000 would be due. **Count the days deliberately;** the date is chosen to sit exactly on the boundary.
>
> **2. The discount base.** $48,000, not $50,000. 3% of $50,000 would be $1,500 — a $60 error, and a wrong cash figure. **You cannot discount goods you returned.**
>
> **Note the named account "Accounts Receivable — Bates".** This is the **personal account** in the receivables ledger from [[04 - Ledger Accounting and Double Entry]] §1, kept alongside the nominal ledger control account.

---

### Exercise 2 — Direct write-off vs allowance

Meridian Ltd made credit sales of $400,000 in 2024. At 31 December 2024 receivables stand at $85,000 and management estimates 6% will prove uncollectible. In March 2025, a customer owing $3,200 goes bankrupt. In August 2025 that customer's liquidator pays $1,100.

(a) Record all entries under the **allowance** method. (b) Record them under the **direct write-off** method. (c) Compare the profit reported in each year under the two methods.

> [!example]- Solution
> **(a) Allowance method.**
>
> *31 Dec 2024 — estimate:* $85{,}000 \times 6\% = \$5{,}100$
> $$\text{Dr Bad Debt Expense } 5{,}100 \;/\; \text{Cr Allowance for Doubtful Accounts } 5{,}100$$
> Balance sheet: AR $85,000 − allowance $5,100 = **$79,900** cash realisable value.
>
> *March 2025 — write-off:*
> $$\text{Dr Allowance for Doubtful Accounts } 3{,}200 \;/\; \text{Cr Accounts Receivable } 3{,}200$$
> **No expense.** Total assets unchanged.
>
> *August 2025 — recovery, two entries:*
> $$\text{Dr Accounts Receivable } 1{,}100 \;/\; \text{Cr Allowance for Doubtful Accounts } 1{,}100$$
> $$\text{Dr Cash } 1{,}100 \;/\; \text{Cr Accounts Receivable } 1{,}100$$
> **No revenue.**
>
> **(b) Direct write-off method.**
>
> *31 Dec 2024:* **no entry at all.**
>
> *March 2025:*
> $$\text{Dr Bad Debt Expense } 3{,}200 \;/\; \text{Cr Accounts Receivable } 3{,}200$$
>
> *August 2025:*
> $$\text{Dr Accounts Receivable } 1{,}100 \;/\; \text{Cr Bad Debt Expense } 1{,}100$$
> *(some texts credit "Uncollectible Accounts Recovered", a revenue account — either way it hits profit)*
> $$\text{Dr Cash } 1{,}100 \;/\; \text{Cr Accounts Receivable } 1{,}100$$
>
> **(c) Profit comparison:**
>
> | | Allowance | Direct write-off |
> |---|---|---|
> | **2024** bad debt expense | **5,100** | **0** |
> | **2025** bad debt expense | **0** | **3,200 − 1,100 = 2,100** |
> | 2024 receivables shown at | **79,900** (realisable) | **85,000** (face) |
>
> ---
> **The direct write-off method is wrong on both counts.**
>
> **2024 profit is overstated by $5,100.** The sales were made in 2024; the losses on them belong to 2024. Reporting zero bad debt expense in the year of sale violates the expense recognition principle outright.
>
> **2024 receivables are overstated by $5,100.** Showing $85,000 asserts that every customer will pay — which management themselves estimate is false.
>
> **And the error hits 2025 too**, where a $2,100 expense appears that has nothing to do with 2025's trading.
>
> **Under the allowance method neither year's profit is touched by the actual default** — because the loss was already recognised in the correct period. **That is the entire point of the method**, and it is why GAAP requires it.

---

### Exercise 3 — The two estimation bases (lecture DO IT!, extended)

**(a)** Brule Co. has been in business five years. The ledger at the end of the current year shows Accounts Receivable **$30,000 Dr.**, Sales Revenue **$180,000 Cr.**, Allowance for Doubtful Accounts **$2,000 Dr.** Bad debts are estimated to be **10% of receivables**. Prepare the adjusting entry.

**(b)** Rework (a) assuming instead that the Allowance had a **$2,000 credit** balance.

**(c)** Rework (a) assuming the company uses **percentage-of-sales at 1.5%** of sales revenue, with the Allowance at $2,000 Dr.

> [!example]- Solution
> **(a) Percentage-of-receivables, allowance has a DEBIT balance.**
>
> $$\text{Required ending balance (credit)} = 30{,}000 \times 10\% = \$3{,}000$$
>
> The account currently has a **$2,000 debit** balance — the wrong side. To get from $2,000 Dr to $3,000 Cr requires a credit of:
> $$3{,}000 + 2{,}000 = \$5{,}000$$
> $$\text{Dr Bad Debt Expense } 5{,}000 \;/\; \text{Cr Allowance for Doubtful Accounts } 5{,}000$$
>
> > [!important] A debit balance in the Allowance means last year's estimate was too low
> > Allowance for Doubtful Accounts is a **contra-asset** with a normal **credit** balance. A **debit** balance means **write-offs during the year exceeded the allowance that had been set aside** — the previous estimate was insufficient.
> >
> > This makes the entry **larger**, not smaller: you must both clear the $2,000 deficit *and* build the $3,000 target. **Adding when the balance is a debit, subtracting when it is a credit** is the step candidates most often get wrong, and the reason the question specifies "Dr."
>
> **(b) Same target, CREDIT balance of $2,000.**
> $$3{,}000 - 2{,}000 = \$1{,}000$$
> $$\text{Dr Bad Debt Expense } 1{,}000 \;/\; \text{Cr Allowance for Doubtful Accounts } 1{,}000$$
>
> **The same 10% estimate produces a $5,000 expense in (a) and a $1,000 expense in (b)** — a fivefold difference driven entirely by the opening balance. Both end with the allowance at exactly $3,000 credit and receivables at a realisable $27,000.
>
> **(c) Percentage-of-sales, 1.5%.**
> $$180{,}000 \times 1.5\% = \$2{,}700$$
> $$\text{Dr Bad Debt Expense } 2{,}700 \;/\; \text{Cr Allowance for Doubtful Accounts } 2{,}700$$
>
> **The existing $2,000 debit balance is IGNORED.** The computed figure *is* the entry. The allowance ends at $2{,}700 - 2{,}000 = \$700$ credit — **not** at any particular target.
>
> ---
> **The whole distinction, in one line:**
>
> | | Computed figure is… | Existing balance |
> |---|---|---|
> | **% of sales** | **the entry** | **ignored** |
> | **% of receivables** | **the required ending balance** | **must be adjusted for** |
>
> **Why the difference is principled, not arbitrary.** Percentage-of-sales asks *"how much of this year's sales will go bad?"* — a question about **this year's income statement**, unaffected by what the allowance happens to contain. Percentage-of-receivables asks *"how much of the balance outstanding now will go bad?"* — a question about **the balance sheet**, which the allowance must be adjusted to answer correctly.
>
> **Read the question wording carefully:** "bad debts are estimated to be 10% *of receivables*" versus "1.5% *of sales*" is the only clue, and it changes both the method and the answer.

---

### Exercise 4 — Notes receivable (lecture DO IT!, extended)

Gambit Stores accepts from Leonard Co. a **$3,400, 90-day, 6%** note dated **May 10** in settlement of Leonard's overdue account.

(a) What is the maturity date? (b) What is the interest payable at maturity? (c) Record the acceptance of the note and its collection at maturity. (d) Gambit prepares statements at 30 June — record the necessary adjusting entry and the revised collection entry.

> [!example]- Solution
> **(a) Maturity date.** Count 90 days, **omitting the issue date and including the due date**:
>
> | Month | Days counted | Running total |
> |---|---|---|
> | May (11th–31st) | 21 | 21 |
> | June | 30 | 51 |
> | July | 31 | 82 |
> | August | 8 | **90** |
>
> **Maturity date: 8 August.** (Verified by direct date arithmetic.)
>
> **(b) Interest**, using the 360-day convention:
> $$3{,}400 \times 6\% \times \frac{90}{360} = 3{,}400 \times 1.5\% = \mathbf{\$51.00}$$
> *(On a 365-day basis it would be $50.30. State which convention you are using.)*
>
> **(c) Entries.**
>
> *May 10 — acceptance:*
> $$\text{Dr Notes Receivable — Leonard } 3{,}400 \;/\; \text{Cr Accounts Receivable — Leonard } 3{,}400$$
> **No revenue** — one asset replaces another. Gambit has converted an overdue open account into a formal, interest-bearing, legally stronger claim.
>
> *August 8 — collection:*
> $$\text{Dr Cash } 3{,}451 \;/\; \text{Cr Notes Receivable } 3{,}400,\;\; \text{Cr Interest Revenue } 51$$
>
> **(d) With a 30 June year end.** From 10 May to 30 June is $21 + 30 = 51$ days:
> $$\text{Accrued interest} = 3{,}400 \times 6\% \times \frac{51}{360} = \$28.90$$
> $$\text{Jun 30:}\quad \text{Dr Interest Receivable } 28.90 \;/\; \text{Cr Interest Revenue } 28.90$$
>
> *August 8 — collection, revised:*
> $$\text{Dr Cash } 3{,}451 \;/\; \text{Cr Notes Receivable } 3{,}400,\;\; \text{Cr Interest Receivable } 28.90,\;\; \text{Cr Interest Revenue } 22.10$$
>
> Check: $28.90 + 22.10 = \$51.00$ ✓ — the total interest is unchanged, merely split between two accounting periods.
>
> ---
> **Three points worth extracting:**
>
> **1. The day-counting rule matters.** Omitting the issue date and including the due date gives 8 August; counting the issue date would give 7 August. **State the rule explicitly in your working** so the marker can follow it.
>
> **2. Converting an overdue account to a note is a real commercial move.** Gambit gains interest, a stronger legal instrument, and a negotiable asset it could sell. Leonard gains time. **Neither party recognises revenue or expense at that moment.**
>
> **3. Part (d) is [[05 - Adjusting Entries]] applied to interest** — exactly the accrued-revenue pattern, and the collection entry must credit Interest **Receivable** for the part already recognised. Crediting the whole $51 to revenue would double-count $28.90.

---

### Exercise 5 — Receivables analysis (lecture DO IT!, extended)

In 2017 Phil Mickelson Company had net credit sales of **$923,795**, a beginning accounts receivable (net) balance of **$38,275** and an ending balance of **$35,988**.

(a) Compute the accounts receivable turnover. (b) Compute the average collection period in days. (c) If the company's terms are n/30, what does this tell you? (d) Compare with Cisco's figures from §7 and explain the difference.

> [!example]- Solution
> **(a) Accounts receivable turnover.**
> $$\text{Average AR} = \frac{38{,}275 + 35{,}988}{2} = \$37{,}131.50$$
> $$\text{Turnover} = \frac{923{,}795}{37{,}131.50} = \mathbf{24.9 \text{ times}}$$
>
> **(b) Average collection period.**
> $$\frac{365}{24.9} = \mathbf{14.7 \text{ days}}$$
>
> **(c) Against n/30 terms.** Customers pay in **under 15 days on average — less than half the 30 days allowed.** Three readings, and the right one needs more information:
>
> - **Excellent credit control** — efficient invoicing and collection, and cash converting fast.
> - **Or the terms are not really n/30 in practice** — the company may in fact be offering a settlement discount (e.g. 2/10, n/30) that most customers take. **A 14.7-day average with a 10-day discount window strongly suggests this**, and if so the "cost" of that fast collection is the discount given up (see [[06 - Accounting for Merchandising Operations]] §3 — 2/10, n/30 costs 36.5% annualised).
> - **Or credit is being granted too restrictively**, refusing marginal customers and losing sales to competitors with easier terms.
>
> **Fast collection is not automatically good.** It must be weighed against sales foregone and discounts given.
>
> **(d) Comparison with Cisco:**
>
> | | Mickelson | Cisco |
> |---|---|---|
> | Turnover | **24.9×** | **7.7×** |
> | Collection period | **14.7 days** | **47.2 days** |
>
> **Mickelson collects more than three times as fast.** Plausible explanations, in order of likelihood:
>
> 1. **Different customer base.** Cisco sells large networking systems to enterprises and governments, which pay on long formal terms and often negotiate 60–90 days. Mickelson (a much smaller company on these figures) likely sells to smaller, faster-paying customers.
> 2. **Different bargaining power.** A large corporate buyer can dictate payment terms to a supplier; a small buyer cannot.
> 3. **Cisco's assumption is questionable.** The illustration assumes **all** Cisco's sales were on credit. If some were not, the true credit-sales figure is lower and Cisco's turnover is **overstated** — meaning its real collection period is even longer than 47 days.
>
> **The methodological caution generalises:** the ratio requires **net credit sales**, but published accounts usually disclose only total net sales. **Assuming all sales are on credit inflates the turnover** of any company with significant cash sales — which is why the comparison is only ever meaningful within an industry, and why a *trend* for one company is more reliable than a *level* compared across companies.

---

## 📝 Summary

- **Receivables** are amounts due expected to be collected in cash: **accounts receivable** (from customers on account), **notes receivable** (written promises, normally interest-bearing), and **other receivables** (non-trade).
- Receivables are recognised **when the service is performed or the goods are sold**. Returns and discounts follow [[06 - Accounting for Merchandising Operations]], with the discount computed on the balance **after** returns.
- **The direct write-off method is not acceptable** — no matching, and receivables are not stated at cash realisable value. **GAAP requires the allowance method.**
- **The allowance method has two stages.** Estimate: **Dr Bad Debt Expense / Cr Allowance for Doubtful Accounts** — the only entry affecting profit. Write-off: **Dr Allowance / Cr Accounts Receivable** — **no expense, no change in cash realisable value.** A recovery reverses the write-off and then records an ordinary collection, in **two** entries so that the customer's record shows payment.
- **Cash realisable value = gross accounts receivable − allowance for doubtful accounts.**
- **Two estimation bases.** **Percentage-of-sales** emphasises **matching**; the computed figure **is the entry** and the existing allowance balance is **ignored**. **Percentage-of-receivables** (often with an **aging schedule**) emphasises **cash realisable value**; the computed figure is the **required ending balance**, so the existing balance must be adjusted for — **added to** if it is a debit, **subtracted** if a credit.
- **Disposal:** sale to a **factor** (fee 1–3%) or **credit card sales** (fee 2–6%), both recorded with **Service Charge Expense**. Credit card sales create **no receivable** — the issuer bears the risk.
- **Notes receivable:** $\text{Interest} = \text{Face} \times \text{Annual rate} \times \text{Time}$; when counting days, **omit the issue date and include the due date**. A note **honoured** at maturity gives Dr Cash / Cr Notes Receivable + Interest Revenue; **interest accrued at a period end** must be credited to Interest **Receivable** on collection, not to revenue again. A **dishonoured** note moves to Accounts Receivable **with the interest still recognised**, if collection is expected.
- **Presentation:** short-term receivables as current assets, showing **both** gross receivables and the allowance; **bad debt and service charge expense as selling expenses**; **interest revenue under other revenues and gains**.
- $\text{AR turnover} = \dfrac{\text{Net credit sales}}{\text{Average net AR}}$ and $\text{Average collection period} = \dfrac{365}{\text{turnover}}$ — **compare against the credit terms offered.**

---

## ⚠️ Important Notes

> [!warning] The two estimation bases treat the existing allowance balance oppositely
> **% of sales → the computed figure IS the entry** (existing balance ignored).
> **% of receivables → the computed figure is the TARGET** (entry = target − existing credit balance, or target **+** existing **debit** balance).
>
> A **debit** balance in the allowance means last year's estimate was too low, and it makes this year's entry **bigger**. This is the single most-tested point in the chapter.

> [!warning] Writing off a bad debt does not create an expense
> **Dr Allowance / Cr Accounts Receivable** leaves total assets, cash realisable value and net income **unchanged**. The expense was recorded when the allowance was created. Debiting Bad Debt Expense on a write-off under the allowance method **double-counts the loss**.

> [!warning] Interest already accrued must not be recognised twice
> On collecting a note whose interest was partly accrued at a period end, credit **Interest Receivable** for the accrued portion and **Interest Revenue** only for the remainder. Crediting the full amount to revenue overstates the current period's profit.

> [!tip] The interest formula, and the day-count conventions
> $$\text{Interest} = \text{Face value} \times \text{Annual rate} \times \text{Time}$$
> - **Months** → use $\frac{\text{months}}{12}$.
> - **Days** → **omit the issue date, include the due date**; Weygandt uses a **360-day** year, so a 90-day note is exactly $\frac14$ of the annual rate. **Say which convention you are using.**

> [!note] Credit card sales create no receivable
> Record them **like cash sales**: Dr Cash (net), Dr Service Charge Expense, Cr Sales Revenue **(gross)**. The card issuer takes the collection risk, which is what the 2–6% fee buys. **Revenue is never reduced by the fee.**

> [!important] Fraud needs controls, not double entry
> The Tasanee case cost $1.5 million and every entry balanced. **Segregation of duties** — separating recording, custody of cash, and reconciliation — and **independent internal verification** are what would have caught it. This reinforces [[03 - Accounting Transactions and Documents]]: **double entry proves arithmetic, not honesty.**

> [!tip] Read the collection period against the terms offered
> A 47-day collection period on n/30 terms means 17 days of unnecessary financing. A 15-day period on n/30 may mean excellent control — or a settlement discount that is costing more than it saves. **Neither number means anything without the credit terms beside it.**

> [!warning] Gaps in the source slides
> This deck is Weygandt's Chapter 9 set (numbered 7 in the course sequence). Text survives well; illustrations do not.
> - **The T-account walkthrough (slides 11–22) is text-only fragments.** Twelve build slides trace an Accounts Receivable / Allowance pair through a credit sale, a collection, an estimate and a write-off — but only the running balances and journal entries extract. **The visual pairing that makes the sequence clear is lost.** The balances themselves are recoverable and consistent ($500 → $600 → $267 → $257 for AR; $25 → $40 → $30 for the allowance).
> - **Every numbered illustration is an image:** 9-1 (receivables as a percentage of assets), 9-3 (allowance presentation), 9-4 (ledger balances after write-off), 9-6 (**comparison of bases for estimating uncollectibles** — the single most examinable summary), 9-7 and 9-9 (bad debt accounts after posting), **9-8 (the aging schedule)**, 9-11 (promissory note), 9-14 and 9-15 (**the interest formula and day-counting**), 9-16 (interest timeline), 9-17 and 9-18 (turnover and collection period formulas).
> - **The aging schedule is never shown.** Aging is described in one sentence and Illustration 9-8 — the actual schedule with age brackets and percentages — is an image. **The $2,228 estimate in §4 is quoted with no visible working.** The bracket percentages in the note are my own illustration of typical practice.
> - **The interest and turnover formulas are images.** §6 and §7 reconstruct them from the worked examples, whose numbers I have verified independently.
> - **The Gambit Stores DO IT! (slide 48) has no answer** — only the question. Exercise 4's maturity date and interest are my own computation.
> - **The Phil Mickelson DO IT! (slide 60) shows "(a)" and "(b)" with the answers as images.** Exercise 5's figures are my own computation from the given data.
> - **The IFRS section is cut off mid-slide** — only similarities extract; the differences slide and any "looking to the future" content are missing entirely.
> - **Notes receivable disposal by sale is mentioned once** ("holder speeds up conversion to cash by selling the note receivable") and **never illustrated or journalised.**

---

**Previous:** [[07 - Inventories]] · **Next:** [[09 - Plant Assets, Natural Resources and Intangible Assets]] · **Index:** [[00-Index]]

#accounting #receivables #bad-debts #allowance-method #notes-receivable #factoring #aging
