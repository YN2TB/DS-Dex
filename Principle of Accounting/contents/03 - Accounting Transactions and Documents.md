---
subject: Principle of Accounting
chapter: 03
tags: [ds, accounting, source-documents, petty-cash, payroll, imprest, audit-trail]
source: "documents/slides/ch03. Accounting transactions and documents.pptx (Doan Thuy Duong, SAA)"
---

# Accounting Transactions and Documents

> [!abstract] Where this sits in the course
> [[02 - The Accounting Equation]] established *what* accounting records and *why* it balances. This chapter covers the **paperwork** — the four transaction types a business meets, the **source documents** that evidence them, and how computerised systems process them. It is the least conceptual chapter in the course and the most practical: it is what an actual bookkeeper spends the day doing.
>
> The four transaction types introduced here map **one-to-one** onto the four double-entry patterns in [[04 - Ledger Accounting and Double Entry]], so this chapter is best read as its preparation.

---

## 📘 Main Knowledge

### 1. The four types of transaction

| Type | Description |
|---|---|
| **Credit transactions** | Credit Sale / Credit Purchase — goods change hands now, cash later |
| **Cash transactions** | Cash Sale / Cash Purchase — goods and cash change hands together |
| **Petty cash transactions** | Small day-to-day payments from a float held on the premises |
| **Payroll transactions** | Paying employees, and the deductions that go with it |

> [!important] Why the credit/cash split is the fundamental one
> A **cash** transaction is settled immediately: one event, one entry. A **credit** transaction splits into **two separate events** — the sale or purchase, and the later payment — and creates a **receivable** or **payable** in between.
>
> This is the **accruals concept** ([[01 - Introduction to Accounting]]) made operational. Revenue is recognised when goods are delivered, not when cash arrives, and the receivable is the bookkeeping device that holds the gap open. **Nearly every complication in the rest of this course comes from that gap.**
>
> Petty cash and payroll are really special cases of cash transactions, separated out because each has its own control system and its own paperwork.

---

### 2. Source documents

> [!note] What "source document" means and why it matters
> A **source document** is the original evidence that a transaction occurred — the piece of paper (or electronic record) that authorises and substantiates an accounting entry. It is the start of the **audit trail**: a chain from the entry in the ledger back to the document proving it happened.
>
> **No source document, no entry.** This is the basic internal control against fraud and error, and it is why the distinction between documents that *are* sources and those that are not (see the debit note below) matters.

#### Credit transaction documents

| Document | Description | Source document? |
|---|---|---|
| **Invoice** | May relate to a sales or purchase order | ✅ **Yes** |
| **Credit note** | A "negative invoice" — issued to a customer relating to **returned goods**, or refunds when a customer has been **overcharged** for whatever reason | ✅ **Yes** |
| **Debit note** | A document **requesting a credit note from a supplier** | ❌ **NOT a source document** |

> [!important] Why a debit note is *not* a source document
> A debit note is a **request**, not a record of anything that has happened. The buyer sends it saying "we believe you have overcharged us — please issue a credit note." **Nothing is entered in the books until the supplier agrees and issues the credit note**, which *is* the source document.
>
> **This is a standard exam question.** The logic generalises: purchase orders, quotations and delivery notes are also not source documents for the same reason — they precede or accompany the transaction rather than evidencing its financial effect.

#### Cash at bank documents

**Source documents:** transaction report downloaded from electronic banking, cheque, bank transfer, and similar.

Two processing regimes:

| Regime | How it works |
|---|---|
| **Manual** | Bank transactions are recorded manually in the **cash book**, then **reconciled to the bank statement at the end of the month** |
| **Computerised** | Transactions are reconciled to the bank statement (transaction report) **daily**. Any unknown transaction is recorded in a temporary **suspense account** and reported on an **exception report** |

> [!important] Two ideas here are worth more than they look
> **The suspense account.** When a transaction cannot be identified, the system does not simply drop it — that would unbalance the books. It parks the amount in a **suspense account** so that debits still equal credits, and flags it for investigation. **A suspense account should always be cleared to zero before financial statements are prepared**; a suspense balance in published accounts means something is genuinely unresolved.
>
> **The exception report.** Rather than reviewing every transaction, the system lists only those needing human attention. This is **management by exception**, and it is the principle that makes high-volume computerised accounting feasible at all.
>
> Note also the frequency difference: **monthly** reconciliation under a manual system, **daily** under a computerised one. Faster reconciliation means errors and fraud are caught sooner — one of the concrete benefits of computerisation.

#### Petty cash documents

**Source document:** the **petty cash book** — records all payments out of and receipts into petty cash (manual first, then computerised).

**The imprest system.** Keep an agreed sum of petty cash (a small amount) for staff refreshments, postage, taxi fares. It **must be topped up from time to time**, and the controlling identity is:

$$
\boxed{\;\text{Cash still held in petty cash} \;+\; \text{Vouchers for payments} \;=\; \text{Imprest amount}\;}
$$

> [!important] The imprest system is a control, not just an accounting method
> The identity above can be **checked at any moment without notice**. If the float is £200 and you count £120 of cash, there must be £80 of vouchers. **Anything missing is immediately visible.**
>
> Two further control features fall out of it:
> 1. **Topping up restores the float to the fixed imprest amount** — so the reimbursement is always exactly equal to the total of the vouchers submitted, which forces the vouchers to be produced and examined.
> 2. **The maximum possible loss is capped at the imprest amount.** Holding a small fixed float limits exposure in a way that an open cash drawer does not.
>
> This is why the imprest system is preferred over simply handing out cash as needed, and it is the standard exam answer to "what are the advantages of the imprest system?"

#### Payroll documents

**Source document:** the **payroll** — records employee wages and salaries (manual first, then computerised).

**Employee side:**

| Item | Meaning |
|---|---|
| **Gross pay** | Total pay to employees before deductions |
| **Net pay** | Cash actually paid to employees |
| **Employee pension contribution** | A deduction |
| **Employee NI contribution** | A deduction (National Insurance) |
| **PAYE income tax** | A deduction (Pay As You Earn) |

$$
\text{Net pay} = \text{Gross pay} - \text{PAYE} - \text{Employee NI} - \text{Employee pension}
$$

**Employer side — additional cost:**

- **Employer NI contribution**
- **Employer pension contribution**

$$
\boxed{\;\text{Gross pay} + \text{Additional cost} = \text{Total payroll cost}\;}
$$

> [!important] The employer's cost exceeds gross pay, which exceeds net pay
> Three different numbers that students routinely confuse:
>
> | Figure | Whose perspective | Where it appears |
> |---|---|---|
> | **Net pay** | What the employee receives | Cash leaving the bank to employees |
> | **Gross pay** | What the employee earns | Part of the wages expense |
> | **Total payroll cost** | What the business bears | **The full wages expense in profit or loss** |
>
> **The expense in the statement of profit or loss is the total payroll cost, not gross pay and certainly not net pay.** The deductions do not disappear — they become **liabilities** owed to the tax authority (HMRC) and the pension trustee until paid over.
>
> This is exactly the double entry shown in [[04 - Ledger Accounting and Double Entry]] §3.5: one debit to wages expense, three credits (cash, HMRC, pension trustee).

> [!note] UK terminology
> **PAYE** and **NI** are UK-specific (Pay As You Earn income tax; National Insurance, the UK social-security contribution). Vietnam's equivalents are personal income tax (thuế TNCN) and compulsory social/health/unemployment insurance, which work the same way structurally: deducted at source from the employee, plus a separate employer contribution on top. **The accounting is identical; only the names change.**

---

### 3. Computerised accounting systems

| Concept | Definition |
|---|---|
| **Standing data** | Data that does not regularly change: name, address, payment terms |
| **Real-time processing** | Processing at the point at which the transaction takes place |
| **Batch processing** | Processing a number of transactions together in a group or batch |

> [!important] Real-time vs batch — the trade-off
> | | Real-time | Batch |
> |---|---|---|
> | **Records updated** | Immediately | Periodically (nightly, weekly) |
> | **Information currency** | Always up to date | Out of date between runs |
> | **Error detection** | At the point of entry | Only when the batch runs |
> | **Processing cost** | Higher — the system must be always available | Lower — one efficient run |
> | **Typical use** | Retail point of sale, online banking, stock levels | Payroll, monthly invoicing, interest calculation |
>
> **Payroll is the canonical batch process:** it happens once a month for everyone at once, and there is no benefit to processing each employee the instant their hours are recorded. **Stock levels are the canonical real-time process:** a shop needs to know *now* whether an item is in stock.
>
> The concepts are the accounting instance of a general computing distinction — compare stream processing versus batch pipelines in [[MLOps/contents/03 - Data in MLOps|data engineering]].

> [!note] Why standing data is separated
> A customer's name, address and payment terms are entered **once** and referenced by every transaction thereafter, rather than being retyped on each invoice. Three benefits: **less data entry**, **fewer errors**, and **consistency** — change the address once and every future document is correct.
>
> The control implication is that **standing data changes need strong authorisation.** Altering a supplier's bank account details in standing data is one of the most common routes to payment fraud, precisely because the change is made once and then quietly applied to every subsequent payment.

---

## ✏️ Exercises

> [!warning] The lecture's own questions are lost
> Slides 11 and 12 are headed "Question 1" and "Question 2" with **no extractable content** — they are images. All exercises below are my own construction.

### Exercise 1 — Source document or not?

For each document, state whether it is a source document, and identify the accounting entry (if any) it supports.

(a) A sales invoice issued to a customer · (b) A purchase order sent to a supplier · (c) A credit note received from a supplier · (d) A debit note sent to a supplier · (e) A goods received note · (f) A cheque stub · (g) The petty cash book · (h) A quotation received from a potential supplier

> [!example]- Solution
> | | Document | Source doc? | Supports |
> |---|---|---|---|
> | (a) | Sales invoice issued | ✅ **Yes** | Dr Trade receivable / Cr Revenue |
> | (b) | Purchase order sent | ❌ No | Nothing — an *intention* to buy |
> | (c) | Credit note **received** from supplier | ✅ **Yes** | Dr Trade payable / Cr Purchases (or purchase returns) |
> | (d) | Debit note **sent** to supplier | ❌ **No** | Nothing — a *request* for a credit note |
> | (e) | Goods received note | ❌ No (but see below) | Nothing directly |
> | (f) | Cheque stub | ✅ **Yes** | Dr Trade payable / Cr Cash |
> | (g) | Petty cash book | ✅ **Yes** | Dr expenses / Cr Petty cash |
> | (h) | Quotation received | ❌ No | Nothing — a *proposal* |
>
> **The organising principle: has a financial obligation actually arisen?**
>
> - **(b), (d), (h)** all fail the test — an order, a request and a quotation are all about what *might* or *should* happen. None creates a liability. **(d) is the one the exam asks about**, because it looks official and is easy to mistake for evidence.
> - **(e) is the interesting case.** A goods received note does not itself trigger an entry, but it is essential to the **three-way match**: purchase order (what we asked for) + goods received note (what arrived) + supplier invoice (what we are being charged for). **Only when all three agree should the invoice be posted and paid.** So the GRN is a critical control document even though it is not a source document.
> - **(c)** is a source document because the supplier has *agreed* — the obligation genuinely changes. Contrast with (d), where nothing has been agreed yet.

---

### Exercise 2 — The imprest system

A business operates petty cash on an imprest system with a float of £250. At the end of March the tin contains £68.40 in cash and the following vouchers: postage £42.15, taxi fares £61.30, staff refreshments £48.75, stationery £29.40.

(a) Does the float reconcile? (b) How much is needed to top it up? (c) What if the cash counted had been £58.40 instead?

> [!example]- Solution
> **(a) Check the imprest identity.**
> $$\text{Cash held} + \text{Vouchers} = \text{Imprest amount}$$
> Vouchers total: $42.15+61.30+48.75+29.40 = \mathbf{£181.60}$
> $$68.40 + 181.60 = \mathbf{£250.00} \;\;✓$$
> **The float reconciles exactly.**
>
> **(b) The top-up is £181.60** — exactly the total of the vouchers, which restores the tin to £250.00.
>
> **This is the defining feature of the imprest system:** the reimbursement always equals the expenditure, so the float returns to the same fixed amount each period. The person authorising the top-up must see £181.60 of vouchers to justify handing over £181.60, which forces the documentation to be produced and examined.
>
> **The double entry on top-up** (see [[04 - Ledger Accounting and Double Entry]] §3.4) is two steps:
> $$\text{Dr Postage } 42.15,\;\text{Dr Travel } 61.30,\;\text{Dr Refreshments } 48.75,\;\text{Dr Stationery } 29.40 \;/\; \text{Cr Petty cash } 181.60$$
> $$\text{Dr Petty cash } 181.60 \;/\; \text{Cr Cash at bank } 181.60$$
> Note that **the expenses are recognised when the vouchers are processed, not when the float was originally created.** Creating the float is merely moving cash between two asset accounts.
>
> **(c) £58.40 would leave a £10.00 shortfall:**
> $$58.40 + 181.60 = 240.00 \neq 250.00$$
> **£10 is missing** — and the imprest system has done its job by making that immediately visible.
>
> Possible causes, in the order you would check them: a voucher lost or not yet submitted; a payment made without a voucher; an arithmetic error in the petty cash book; or theft. The shortfall must be **investigated, then written off to an expense account** (`Cash shortage` or similar) so that the float still restores to £250. **It must never be quietly absorbed by topping up £191.60** — that would conceal the discrepancy and defeat the entire control.

---

### Exercise 3 — Payroll figures

For March, a business has: gross pay £48,000; PAYE income tax deducted £7,200; employee NI £3,840; employee pension contributions £2,400; employer NI £5,520; employer pension contributions £1,920.

(a) Compute net pay. (b) Compute total payroll cost. (c) What amount leaves the bank account, and to whom? (d) Which figure appears as the wages expense?

> [!example]- Solution
> **(a) Net pay** — gross less all *employee* deductions:
> $$48{,}000 - 7{,}200 - 3{,}840 - 2{,}400 = \mathbf{£34{,}560}$$
>
> **(b) Total payroll cost** — gross pay plus *employer* costs:
> $$48{,}000 + 5{,}520 + 1{,}920 = \mathbf{£55{,}440}$$
>
> **(c) Money leaving the bank, in total £55,440**, in three directions:
>
> | Recipient | Amount | Made up of |
> |---|---|---|
> | **Employees** | £34,560 | Net pay |
> | **HMRC** (tax authority) | £16,560 | PAYE 7,200 + employee NI 3,840 + employer NI 5,520 |
> | **Pension trustee** | £4,320 | Employee 2,400 + employer 1,920 |
> | **Total** | **£55,440** | ✓ |
>
> Note the **timing**: employees are paid on payday, but HMRC and the pension trustee are usually paid later in the following month. So on payday the entry credits **liabilities** to HMRC and the pension trustee, which are settled subsequently. Between payday and settlement, those amounts sit on the balance sheet as current liabilities.
>
> **(d) The wages expense is £55,440 — the total payroll cost.**
>
> **This is the point of the exercise.** Three plausible-looking figures are available, and only one is the expense:
> - £34,560 (net pay) — **wrong**; it ignores the deductions, which the business still bears
> - £48,000 (gross pay) — **wrong**; it ignores the employer's own contributions
> - **£55,440 (total payroll cost) — correct**
>
> A useful sanity check: **the employee costs the business 60% more than they take home** ($55{,}440/34{,}560 = 1.60$). That gap — between what a worker receives and what an employer pays — is a real and frequently misunderstood economic quantity, and it is exactly the "tax wedge" discussed in labour economics.

---

### Exercise 4 — Real-time or batch?

For each process, state whether real-time or batch processing is more appropriate and why.

(a) Recording supermarket checkout sales · (b) Running the monthly payroll · (c) Updating a customer's credit limit · (d) Calculating interest on 200,000 savings accounts · (e) Recording an online order · (f) Producing month-end management accounts

> [!example]- Solution
> | | Process | Choice | Why |
> |---|---|---|---|
> | (a) | Supermarket checkout | **Real-time** | Stock levels and cash position must be current; the till cannot wait for a nightly run to know whether an item exists |
> | (b) | Monthly payroll | **Batch** | Happens once for everyone at once; no benefit to instant processing; large volume, identical calculation — ideal for one efficient run |
> | (c) | Customer credit limit | **Real-time** | It is **standing data** used to authorise sales. A stale limit means either refusing a good order or accepting a bad one |
> | (d) | Interest on 200,000 accounts | **Batch** | Identical calculation applied en masse at a defined date; overnight processing is cheaper and there is no user waiting |
> | (e) | Online order | **Real-time** | The customer needs immediate confirmation, and stock must be reserved before someone else buys it |
> | (f) | Month-end management accounts | **Batch** | By definition a periodic summary of a completed period |
>
> **The pattern.** Ask two questions:
> 1. **Is someone waiting for the answer?** (Customer at a till, buyer online → real-time.)
> 2. **Does the work naturally occur at a point in time, in volume?** (Payroll, interest, period-end → batch.)
>
> **A note on (c).** Credit limits are standing data, and the real risk is not processing speed but **authorisation**. A real-time system that lets any user raise a credit limit instantly is worse than a batch system with proper approval. **Processing mode and control are separate questions**, and the exam sometimes conflates them.
>
> **Modern practice blurs the line.** Most systems now capture transactions in real time and run periodic batch jobs for reconciliation, reporting and interest. The distinction survives as a way of thinking about *when* information becomes available, not as a hard architectural split.

---

### Exercise 5 — Trace the audit trail

An auditor selects a £4,800 entry in the purchases account. Describe the chain of documents she would follow to verify it, and state what each proves. What would make her suspicious at each stage?

> [!example]- Solution
> **The chain, working backwards from the ledger:**
>
> | Step | Document | Proves | Red flag |
> |---|---|---|---|
> | 1 | **Ledger entry** — Dr Purchases £4,800 / Cr Trade payable £4,800 | The entry exists and is balanced | Posted to an unusual account; posted out of sequence; round-sum amount |
> | 2 | **Purchase invoice** from the supplier | A supplier has charged £4,800 | Supplier not on the approved list; address is a PO box or a residential address; invoice number is sequential across many months (suggesting we are the only "customer") |
> | 3 | **Goods received note** | The goods physically arrived | No GRN at all; GRN quantity differs from the invoice; GRN signed by the person who raised the order |
> | 4 | **Purchase order** | The purchase was authorised in advance | No PO; PO dated *after* the invoice; PO value below an approval threshold while the invoice exceeds it |
> | 5 | **Authorisation** on the PO | An appropriate person approved it | Approver lacks authority for that amount; approver is the same person who receives the goods |
> | 6 | **Payment record** — cheque stub or bank transfer | The money went to the right place | Payment to a bank account different from the supplier's standing data; payment made before goods arrived |
> | 7 | **Bank statement** | The payment cleared | No corresponding entry |
>
> **The three-way match** at the heart of this — **purchase order + goods received note + invoice** — is the standard control over purchases. All three must agree on quantity, price and description before the invoice is posted and paid.
>
> **What each break in the chain would mean:**
> - **No invoice** → the liability may be fictitious.
> - **No GRN** → we may be paying for goods never received (the classic supplier fraud).
> - **No PO or no authorisation** → the purchase may not have been sanctioned; a route for employees to buy things for themselves.
> - **PO dated after the invoice** → the paperwork was fabricated after the fact to legitimise an unauthorised purchase.
> - **Payment to a different bank account** → **standing data has been altered** — see §3. This is one of the most common and most costly frauds, because it needs only one change to divert every subsequent payment to a genuine supplier.
>
> **Segregation of duties** is the underlying principle: the person who *orders*, the person who *receives*, the person who *records* and the person who *pays* should be four different people. Where the same person controls two or more of these steps, the audit trail can be constructed to conceal a fraud rather than reveal it.
>
> **Why this exercise matters conceptually.** [[02 - The Accounting Equation]] showed that the books always balance — but **a fraudulent entry balances just as neatly as a genuine one.** Double entry catches *errors*, not *lies*. The audit trail and segregation of duties are what catch lies, and that is the real reason source documents are treated so strictly.

---

## 📝 Summary

- **Four transaction types:** credit (sale/purchase), cash (sale/purchase), petty cash, and payroll. The **credit/cash split is fundamental** — a credit transaction is two events with a receivable or payable in between, which is the accruals concept made operational.
- **A source document is the original evidence** that a transaction occurred, and the start of the audit trail. **No source document, no entry.**
- **Credit documents:** the **invoice** and the **credit note** (a negative invoice, for returns or overcharges) are source documents. The **debit note** — a *request* to a supplier for a credit note — is **not**, because nothing has yet been agreed.
- **Bank documents:** transaction reports, cheques, transfers. Manual systems record in a **cash book** and reconcile **monthly**; computerised systems reconcile **daily**, parking unidentified items in a **suspense account** and flagging them on an **exception report**.
- **Petty cash** runs on the **imprest system**: a fixed float for small expenses, with
  $$\text{Cash held} + \text{Vouchers} = \text{Imprest amount}$$
  This can be verified at any time, caps the maximum loss, and forces vouchers to be produced before reimbursement.
- **Payroll** distinguishes three figures: **net pay** (what the employee receives), **gross pay** (what the employee earns), and **total payroll cost** = gross pay + employer NI + employer pension (**what the business bears — and the figure that is the wages expense**). Deductions become liabilities to the tax authority and the pension trustee.
- **Computerised systems** hold **standing data** (name, address, payment terms — entered once, referenced often, and requiring strong authorisation to change) and process either in **real time** (at the point of transaction) or in **batches** (a group processed together).

---

## ⚠️ Important Notes

> [!warning] A debit note is not a source document
> The most-tested point in this chapter. A debit note **requests** a credit note; it records nothing. **Only the supplier's credit note, once issued, is the source document.** The same reasoning excludes purchase orders, quotations and delivery notes.

> [!warning] Three payroll figures, one expense
> **Net pay < Gross pay < Total payroll cost.** The **wages expense is the total payroll cost**. Deductions do not vanish — they become liabilities until paid to HMRC and the pension trustee. Questions frequently supply all three figures and ask for "the charge to profit or loss"; the answer is always the largest one.

> [!tip] The imprest identity is checkable at any moment
> $$\text{Cash} + \text{Vouchers} = \text{Imprest amount}$$
> A discrepancy must be **investigated and written off**, never absorbed by topping up a larger amount. Topping up to hide a shortfall destroys the control.

> [!note] Double entry catches errors; the audit trail catches fraud
> [[02 - The Accounting Equation]]'s balancing property proves nothing about honesty — a fictitious transaction balances perfectly. **Source documents, the three-way match, and segregation of duties are what make fraud detectable**, which is why this apparently dull chapter is where internal control actually lives.

> [!tip] Vietnamese equivalents of the UK terms
> The slides use UK payroll vocabulary. The structure is identical elsewhere:
> - **PAYE** ↔ personal income tax withheld at source (thuế TNCN)
> - **NI** ↔ compulsory social, health and unemployment insurance, split between employee and employer
> - **HMRC** ↔ the General Department of Taxation / social insurance agency
>
> **Learn the structure, not the acronyms** — the accounting is the same in any jurisdiction.

> [!warning] Gaps in the source slides
> This is the **thinnest deck in the course** — 12 slides for three topics.
> - **Slide 4 ("2. Accounting Documents") is a bare section heading** with no content.
> - **Slides 11 and 12 ("Question 1", "Question 2") are image-only** — the lecture's own practice questions and any answers are **lost**. All five exercises above are my own construction.
> - **No double entries appear anywhere in this chapter**, despite it introducing the four transaction types whose entries are the whole of [[04 - Ledger Accounting and Double Entry]]. The two chapters must be read together.
> - **The three-way match, segregation of duties and internal control are never mentioned**, although source documents exist precisely to support them. §2 and Exercise 5 supply this from standard material.
> - **No worked petty cash or payroll figures.** The imprest identity and the payroll cost formula are stated abstractly with no numbers; Exercises 2 and 3 fill the gap.
> - **"Registered traders — Taxable / Exempt"** appears in the VAT note of the *next* deck without explanation; VAT registration status is never covered here despite being a documentation issue.
> - **Computerised systems get three bullet points** — standing data, real-time, batch — with no discussion of controls, backups, access rights or the risks that computerisation introduces.

---

**Previous:** [[02 - The Accounting Equation]] · **Next:** [[04 - Ledger Accounting and Double Entry]] · **Index:** [[00-Index]]

#accounting #source-documents #petty-cash #imprest #payroll #internal-control #audit-trail
