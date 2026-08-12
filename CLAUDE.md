# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this is

Not a software project — an Obsidian vault used as a personal "second brain" for a Data Science major at NEU (National Economics University, Vietnam). No build, lint, or test tooling. Claude's job is **personal knowledge architect**: turning raw course material (slides, textbooks, papers) into permanent, well-structured Obsidian notes.

## Warning

- It is unnecessary to re-read the conversation, this file contains everything you need to know
- `data` folder is for agentmemory plugin, not a subject folder

## Resume state — read this, then stop reading

**Last updated: 2026-08-08.**

- **🎉 THE VAULT IS COMPLETE. Business Management — the last subject — finished today:** `00-Index` + **ch. 01–09** (nine notes from Nickels's curated nine chapters), **no erratum filed, 6 discrepancies investigated and declined.**
- **⚠️ VERIFIED AGAINST THE FILESYSTEM, NOT AGAINST THE TABLE BELOW: 215 chapter notes across 20 subjects.** The remaining four — **Big Data Analytics, Natural Language Processing, PowerBI, Programming for Data Science (Python)** — are **permanently blocked, `documents/` genuinely empty.** *(The 2026-08-08 audit that found three subjects missing from the progress table is why this check is now done directly.)*
- **⚠️ Everything worth keeping from Business Management is in `Business Management/CLAUDE.md`** — the five findings, the errata table, the piecewise-offset note. **Do NOT re-read the subject.** *(Same for every other subject: each has its own `CLAUDE.md`.)*
- **⚠️ THE SUBJECT PRODUCED A NEW KIND OF RESULT FOR THE VAULT: A FINDING CONFIRMED BY THREE INDEPENDENT SOURCES.** Marketing ch. 08 computed that the Four Seasons' retention perk breaks even at a **\$2,500** replacement cost. Nickels ch. 04's *"6–213% of salary"* cleared it only **1.2×** at the floor; ch. 07's *"75% entry-level, over 200% for a top manager"* clears it **15× and 40×**. ⇒ ***a finding confirmed by an unrelated source is qualitatively stronger than one derived twice — hunt for more of these.***
- **⚠️ AND A SECOND KIND: A STRUCTURAL FIND NEEDING NO ARITHMETIC.** **Nickels's performance-appraisal steps (his ch. 11) ARE his control process (his ch. 7) with a person as the object** — step for step, step 1 almost verbatim, printed 100 book-pages apart as unrelated topics. ⇒ **everything the vault knows about variance decomposition applies to appraising a person.** *That subject's ch. 06 had no worked example, no table, nothing checkable — and was still worth writing.*
- **⚠️ THE THIRD REUSABLE MOVE, and it worked in four chapters of one book: TAKE THE SOURCE'S ADJACENT FIGURES AND DIVIDE THEM.** Farm labour share and farm size in consecutive sentences ⇒ **output per farmer rose ≥33×, of which consolidation is only 2.87×.** Piketty's r = 5% and g = 1.5% ⇒ **capital's share doubles every 20.5 years.** Market size and export participation three pages apart ⇒ **95.61% of customers are abroad and 99% of US small businesses sell to none of them.** 20%-of-firms and 81%-of-receipts ⇒ **17.05×.**
- **⚠️ AND A RULE THAT NOW SPANS TWO SUBJECTS: THE EQUITY SHARE OF ASSETS *IS* THE WIPEOUT THRESHOLD.** Dell's LBO was **77.6% debt ⇒ a 22.4% fall in enterprise value destroys the equity**; a textbook restaurant's balance sheet has **equity at 25.79% of assets ⇒ a 25.8% fall does the same.** *Compute it on any balance sheet or debt-financed deal.*
- **Nothing is mid-chapter.** No half-written file, no pending verification, no unanswered question, no undischarged cross-subject obligation anywhere in the vault.
- **⚠️ LESSON WORTH KEEPING: THE PROGRESS TABLE WAS NOT A RELIABLE INVENTORY.** It listed 21 subjects; the filesystem has 24. **Before declaring any future milestone, list `D:\NEU` directly and check `documents/` for each folder rather than trusting this file.**
- **⚠️ Everything worth keeping from Marketing is in `Principles of Marketing/CLAUDE.md`** — the five findings, the errata table, the chapter list, and the final form of the figure rule. **Do NOT re-read the subject.** *(Same for every other subject: each has its own `CLAUDE.md`.)*
- **⚠️ THE MARKETING SUBJECT'S UNIFYING LESSON, and it generalises to the whole vault: A HEADLINE NUMBER WAS ACCURATE AND MEANT SOMETHING OTHER THAN WHAT IT APPEARED TO MEAN — in all twelve chapters.** A \$50,000 customer lifetime value that was undiscounted *revenue* (\$3,571 properly computed, **a factor of 14**); a 98% quality standard that was an **error count** compounding to 83.37% over nine stages; a launch that hit every volume target and **lost \$50,000**; a cost-plus price **33% below optimal**; a **higher** margin that earned **less**; a Super Bowl CPM **below a banner's**. ***The habit that catches all of them is one move: take the source's own scattered figures and divide them by each other.***
- **⚠️ Three templates from Marketing worth reusing on any source.** (i) **WHEN A SOURCE STATES A MULTI-PERIOD PLAN, SOLVE IT** — Kotler's illustrative marketing-strategy statement was over-determined and back-solved to **\$1,125 contribution/car with both years checking to the cent**, exposing a break-even of 63,333 against a plan of 50,000. (ii) **GENERALISE THE TOY EXAMPLE BEFORE BELIEVING ITS MAGNITUDE** — his 9-vs-6 contacts diagram generalises to **saving = (M−1)(C−1) − 1**, which is zero at 2×2 and 98.90% at 100×1,000: the theory of disintermediation in one line. (iii) **WHEN A BREAK-EVEN RETURNS AN ABSURD NUMBER, INSPECT THE DENOMINATOR** — Appendix 2's "\$3.36 billion" had a denominator of **exactly \$1.00**, 0.80% above a vertical asymptote, and at his own markup price the required volume was **exactly 1,000,000 units**, the figure that price was defined from.
- **⚠️ THE FIGURE RULE, IN ITS FINAL FORM (settled across Kotler ch. 08–12).** **Label-schematics survive intact; SHAPE figures whose content is the geometry of a curve are lost.** Ch. 08 recovered 6/6 because all six were label-schematics; ch. 09 split cleanly. ⇒ ***both classes live inside one book — the test is not "which book" but "what is this figure's content"*** — and in Kotler the prose stated every plotted point, so even the lost ones were reconstructable.
- **⚠️ The vault's single most reusable extraction finding, now confirmed across four subjects: BEFORE RECORDING A FIGURE AS LOST, CHECK WHETHER THE PROSE NAMES ITS DATA POINTS.** It worked four times in Mishkin alone. **Figures split three ways: data series are always lost; shift diagrams' content is the direction, which the prose states; and SCHEMATICS WHOSE CONTENT IS THEIR LABELS SURVIVE INTACT, because labels are text.** **⚠️ But axis labels are unreliable — usable only when the prose independently confirms them, in which case the prose was sufficient anyway.**
- **⚠️ NUMERIC TABLES SET AS TEXT SURVIVE WHOLE — now confirmed NINE times in Mishkin alone, and in every subject before it. Always test a table, and verify its internal subtotals before trusting it.**
- **⚠️ SIX DROPPED CROSS TERMS IN ONE SUBJECT** (Fisher $r\pi^e$; duration/convexity; arithmetic-vs-geometric average; debt deflation; interest parity; the quantity theory of inflation) ⇒ ***always ask what the neglected term is proportional to.*** **The sharpest case: Mishkin's debt-deflation error was 1.1% of the debt and 100% of the remaining equity** — *a term negligible against one quantity need not be negligible against the one that decides the outcome.*
- **⚠️ THE PATTERN WORTH HUNTING IN EVERY SUBJECT: two chapters of one book contradicting each other, unflagged.** Mishkin ch. 05's arbitrage makes prices informative; ch. 06's free-rider problem shows the same arbitrage destroys the incentive to produce the information (Grossman–Stiglitz). **An internal tension is worth more than either chapter alone.**
- **⚠️ FOUR TEMPLATES THAT PRODUCED THE BEST MATERIAL, worth trying everywhere:** (i) **take a table the source prints without explaining, and explain it** (Mishkin's Table 2 → duration); (ii) **take a worked example and ask how sensitive it is** (three investors agreeing on every cash flow value a stock **71.4% apart**); (iii) **back out the unobservable from the observable** (a 53% crash ⇒ $(k_e-g)$ rose ×2.1485); (iv) **score a source's own criteria using results computed in earlier chapters** (all three monetary-targeting criteria shown to have failed).
- **⚠️ Obligation ch. 07 left for the macro half: when two effects oppose, SAY SO.** Higher wages → hours worked and higher interest rates → saving are **both genuinely ambiguous** (substitution vs income), and **ch. 10's loanable-funds model ASSUMES an upward-sloping saving curve — flag it as an assumption, not a result.** *A model identifying two opposing forces has done its job; demanding a sign from it anyway is how confident wrong answers get made.*
- **⚠️ MACRO/MICRO'S BEST CROSS-CHAPTER RESULT (ch. 06): Cournot oligopoly with N firms IS ch. 04's tragedy of the commons** — identical formula $q_i=(a-c)/(N+1)$ and **identical percentages at every matching N** (100.0%, 88.9%, 33.1%, 7.7%, 0.4%). **Mankiw presents the two two chapters apart and never notices.** The chapters tell **opposite** stories about one piece of mathematics because the externality lands on different people. ⇒ ***an equilibrium is not good or bad by itself; the welfare verdict comes from outside the model — ask whose surplus the externality hits.***
- **⚠️ MACRO/MICRO'S ORGANISING RESULT, found in ch. 04 and now to be named in every remaining micro chapter: efficiency is fixed by FUNDAMENTALS, distribution by INSTITUTIONAL DETAIL, and the two are INDEPENDENT.** Three appearances: ch. 01 (comparative advantage fixes the allocation, **the price fixes only the split** — total gain constant at 10 oz across the whole feasible range), ch. 03 (the tax wedge fixes quantity and both prices, **the statute is irrelevant**, elasticities fix the split), ch. 04 (**the efficient allocation is reached whoever holds the property right** — verified across four cases). ⇒ **many policy arguments conducted in the language of efficiency are really about distribution.** *Mankiw never connects the three.*
- **⚠️ MACRO/MICRO'S DOMINANT HAZARD — Mankiw's PDFs encipher every arithmetic operator as a digit:** `5`→`=`, `1`→`+`, `2`→`−`, `3`→`×`. **`Y 5 C 1 I 1 G 1 NX` is $Y = C + I + G + NX$.** **It is NOT a fixed substitution — the same digit means different things in one line** (`(Q2 2 Q1) / [(Q2 1 Q1) / 2]` is the midpoint elasticity formula: subscript, minus, subscript, plus, subscript, literal 2). **There is no mechanical decoder — you must know the economics.** **RULE: never transcribe a formula; reconstruct it from the prose and verify numerically against the book's own worked figures.** *Verified in both spines during setup. Parkin & Bade does NOT share the cipher.* **Full table + worked decodings in the subject's `CLAUDE.md` and `00-Index.md`.**
- **⚠️ Also for Macro/Micro: every figure is lost, and this is the worst-case subject for it** — Mankiw teaches almost entirely through shifting curves and shaded surplus areas. **Method that works (ch. 01 proved it): recompute the whole worked example from the stated inputs, then check the reconstruction reproduces every figure the prose states.** That makes it verified rather than assumed. **All three Mankiw outlines are excellent — locate by outline, extract the range.**
- **⚠️ THE VAULT'S DEEPEST RESULT, now found in FOUR independent settings — the average is always fine and the joint behaviour is everything.** Commercial Banking ch. 02 (bank mergers: $\sigma_{comb}=\sigma\sqrt{(1+\rho)/2}$ — **29.3% risk reduction at ρ=0 but 2.5% at 0.9**), ch. 06 (tranching: **mean pool loss 5.00% at every ρ** while senior-tranche loss goes 0.0000% → 1.8044% — *nothing about the loans had to change for the AAA to be wrong*), ch. 11 (a loan book: **mean loss 2.00% at every ρ** while the 99th percentile goes 3.60% → **17.60%**), ch. 12 (a mortgage book: every loan is a bet on one house-price index). **Same mathematics each time ⇒ any risk measure built on EXPECTED VALUES is blind to correlation, and correlation is what turns many small independent risks into one large one.** *Hunt for a fifth setting — this generalises far beyond banking.*
- **⚠️ Four verification rules the whole vault now runs on, all earned the hard way:**
  1. **A self-consistent calculation is not a verified one.** Testing a duration hedge with the duration formula gave a perfect ±1 residual; **exact repricing showed the "fully hedged" bank losing 1.46% of equity at +2% and 7.81% at +5%, in BOTH directions.** *A first-order formula reports success precisely when the exposure it leaves is second-order — verify against something independent of the model that produced the number.*
  2. **State an approximation, then compute its error at several magnitudes.** Duration's error runs **0.0000% at 1 bp → 0.1122% at 1% → 2.5823% at 5%**, turning "it's an approximation" into an actionable rule.
  3. **Use a tolerance on every equality check against a source's number** — two correct figures were once flagged MISMATCH because `(0.12-0.11)*100e6 != 1e6` in binary floating point.
  4. **Before filing an erratum, rule out your own extraction, your own arithmetic, an abridged table, AND alternative conventions.** Commercial Banking filed 3 errata and *declined* to file 3 more on exactly these grounds. **Filing a false erratum against a correct source is the worse failure.**
- **⚠️ Three repeatable moves that produced the best chapters, worth trying in every subject:**
  1. **Take a claim an earlier chapter ASSERTED and compute the case that proves it.** CB ch. 01 asserted "solvency is a balance-sheet fact, liquidity is a timing fact"; ch. 08 ran a bank with **9.82% equity, every asset performing, zero defaults** through a withdrawal cascade and found **insolvency at 48.5% of liabilities** — *the run does not reveal insolvency, it CREATES it.* The source never computes it.
  2. **Read the footnotes — the qualitative aside is often the computable result.** R&H's footnote 6 says charging the full risk premium "may increase the chances a borrower will default"; modelling it gives a **humped** return curve peaking at $r^*=18\%$, so past it the lender earns less by charging more.
  3. **Hold the first-order term fixed to isolate the second.** Three portfolios at duration **exactly 5.0000** have convexities 26.70/32.63/40.94, and the barbell beats the bullet at every shock in both directions. *Sources routinely vary two things at once and cannot separate them.*
- **⚠️ When an invented illustration contradicts the finding it illustrates, DELETE it — do not tune its parameters until it agrees.** A fabricated chart that matches the claim looks like evidence and is none. **Label assumed figures as mine and the formulas as the source's.**
- **⚠️ EXTRACTION RULE SETTLED (two chapters of one book, ten pages apart): graphical exhibits are lost; numeric tables set as text survive whole.** One chapter's strategy diagrams were destroyed while another's four data tables came through complete with all 22 internal checks passing. **Always test a table before assuming either way, and verify its internal subtotals before trusting it.**
- **⚠️ Boundary DECIDED and recorded:** Commercial Banking owns the bank's balance sheet (spread, gap/duration, capital, credit risk); **Mishkin owns the monetary system** (why rates are what they are, term-structure theory, central-bank operations, money multiplier). **When Monetary & Financial Theories is written, its index must record the same split.**
- **⚠️ The remaining four subjects are all business/finance texts, not technical ones** — so the "run it" verification rule does not transfer directly. **The analogue is: recompute every worked number** (ratios, spreads, capital requirements, NPVs) with `sympy`/`numpy` before quoting it, exactly as Optimization and Econometrics did. **Expect the sources to be long on process and short on theory** (Coronel & Morris was, and enrichment was labelled in the gaps callout each time).
- **⚠️ The pattern worth hunting for: one subject *resolving* a question another left open.** C++ ch. 06 did it — DSA ch. 06 measured cache locality at only ~15% in Python and *conjectured* referential lists were masking it; the same traversal in C++ gave **2.5×**, confirming the diagnosis. **Two subjects measuring the same principle in different settings is worth more than either alone.**
- **If C++ is ever revisited, everything is in `Basic Programming (C++)/CLAUDE.md`** — MSVC 14.50, the `/W4` `cpprun.bat` helper, `/Zc:__cplusplus`, the six-case warning-coverage table (**coverage is uneven — never infer it from one example**), and the rule to patch `.cpp` with **Edit, never a bash heredoc**.
- **The three technical subjects converged on one finding, worth carrying everywhere:** the expensive bugs are the ones that **produce a plausible wrong answer with no error**. DSA logged five misleading measurements; DBMS logged the fan trap, `NOT IN`, the `RANGE` frame default, the lost update and the business-key join; C++ logged integer overflow, out-of-bounds reads, dangling references and object slicing. **In every case the system did exactly what it was told.**
- **Running DBMS finding worth carrying:** **SQLite enforces neither integrity rule by default** — `PRAGMA foreign_keys` is OFF per connection (ch. 01), and `PRIMARY KEY` does not imply `NOT NULL`; `TEXT PRIMARY KEY` took two NULLs and `INTEGER PRIMARY KEY` auto-assigned one, fabricating a row (ch. 02). **Test constraints by inserting rows that should fail; never trust the DDL.**
- **Nothing is mid-chapter.** No half-written file, no pending verification, no unanswered question.
- **⚠️ If any subject uses SQLite again, note the five permissivenesses + two limitations found by testing** (all recorded in `Database Management Systems/CLAUDE.md`): FKs off by default; `PRIMARY KEY` accepts NULLs; alias in `WHERE` accepted; bare column with aggregate accepted; **declared column types not enforced** (a `REAL NOT NULL CHECK` column took the string `'twenty five'`). Limitations: whole-database write lock, and no `ROLLUP`/`CUBE`/`GROUPING SETS`. **SQLite is an excellent teaching database and a poor oracle for correctness.**
- **What DSA established, worth carrying to every later subject:** derive the claim, then **measure it by doubling $n$ and reading the ratio** (2/4/8 for linear/quadratic/cubic; the constant cancels, so quote **ratios**, not seconds). **The first measurement misled five times** — ch. 08 (needed a *constructed* worst case, not random input), ch. 10 (recursive-vs-iterative → count node visits), ch. 11 (Python-vs-C → count operations), ch. 12 (twice: asserted a conclusion the printed table contradicted; used random strings whose counts weren't monotonic). **When a measurement contradicts a sound proof, suspect the measurement.**
- **Extraction facts, if either book is revisited.** **Goodrich's Python is destroyed** — indentation lost and **double underscores render as spaces** (`__init__`→`init`), so listings look plausible and are wrong; his *prose* extracts fine. Goodrich page $n$ = PDF page $n+22$. **Lambert's code extracts perfectly** but covers only ch. 01–08. **Johnsonbaugh (Discrete Maths)** extracts unusually well but **silently deletes overlines**, so complements and De Morgan arrive looking false; book page $n$ = PDF page $n+21$. **All figures and statistical tables in every book are images and never extract.**
- **Environment note:** a Bash call once failed with `claude-sonnet-5[1m] is temporarily unavailable` (tool-classifier outage, not a task problem). **Just re-run it** — it has succeeded immediately on retry both times.
- **Standing authorisation in force:** write chapter notes directly, no per-file confirmation. Work through the remaining textbook-only subjects in this order: Discrete Mathematics → Data Structures and Algorithms → Database Management Systems → Basic Programming (C++) → Commercial Banking → Macroeconomics & Microeconomics → Monetary and Financial Theories → Principles of Marketing.
- **Open question for the user, not blocking:** every textbook-only scope is an unconfirmed editorial choice. The one real gap is **optimal control** — `Optimization/documents/Léonard & Long` has no text layer at all, so that topic is absent from the vault. Worth raising with the lecturer.

**To resume: read this section + the one subject's `CLAUDE.md`, then start.** That is ~6 KB and it is sufficient. Do **not** re-read finished subjects, other subjects' files, or the previous transcript — the whole point of the per-subject split is that you don't have to.

### Keeping this current

**When the user says "checkpoint"** (or you are told the session is near its limit): rewrite the bullets above in one `Edit` call — what just finished, what is next, and anything genuinely mid-flight (a half-written chapter, an unverified number, a decision waiting on the user). Nothing else. Keep it under ~15 lines; it is a pointer, not a summary.

**Claude cannot see the session/usage limit** — it is not exposed to the model. So this section only stays fresh if it is updated at natural boundaries. Do it **after finishing each chapter**, not just at session end: one `Edit`, a few seconds, and it makes an abrupt stop costless.

**If a session does end mid-chapter**, the next one should trust this section over its own instinct to re-derive context. Re-reading a finished subject to "get oriented" is the main way tokens get wasted here.

## Read this file, then read the subject's own CLAUDE.md

**Every subject folder has its own `CLAUDE.md`** holding everything specific to that subject: source inventory, scope decision, extraction quirks, errata found, chapter list, and what remains. This root file holds only what is true of *all* subjects.

**So: check the progress table below, open `<Subject>/CLAUDE.md`, and start there.** Do not read other subjects' files — they are irrelevant and expensive.

## Vault structure

```
[Subject Name]/
  CLAUDE.md               ← subject-specific context (read this)
  contents/
    00-Index.md           ← Map of Content: links every chapter, one-line description each
    01 - [Chapter Topic].md
    ...
  documents/              ← source PDFs/textbooks
  documents/slides/       ← lecture slides, if provided (only 6 subjects have these)
```

One subject = one folder. One chapter = one file, numbered so files sort in learning order.

## Chapter note template

Every chapter file in `contents/` follows this structure exactly:

```markdown
---
subject:
chapter:
tags: [ds]
source:
---

# Chapter Title

## 📘 Main Knowledge
Core concepts, definitions, and formulas explained in plain language — not copy-pasted
from the source. $$LaTeX$$ for math. [[Wikilinks]] for related concepts, including
cross-subject links.

## ✏️ Exercises
5 practice problems, easy → hard. Solutions in collapsed callouts:
> [!example]- Solution
> ...

## 📝 Summary
5–8 bullet TL;DR — dense enough that reviewing just this section refreshes memory
before an exam.

## ⚠️ Important Notes
Common mistakes, edge cases, exam gotchas. Can be as long as needed (8–15 items).

> [!warning] Gaps in the source material
> Everything unrecoverable, reconstructed, or added beyond the source.

**Previous:** … · **Next:** …
```

## Conventions (approved by the user, 2026-07-27)

- **Depth over brevity.** Long Main Knowledge; long teaching solutions; heavily populated Important Notes. The user reviews these notes for exams.
- **`00-Index.md` is written first**, before any chapter, so the scope decision survives an early session end. It holds the Map of Content, course framing, the scope decision, an errata table, and cross-subject links.
- **Gaps are flagged, never invented.** Image-only figures, missing datasets, unanswered prompts, and anything reconstructed rather than extracted go in the closing `> [!warning]` callout.
- **Enrichment beyond the source is allowed** — standard results the source only gestures at, modern practice the book predates — but must be labelled as an addition in the gaps callout.
- **Verify every number.** No numeric claim from any source is quoted without recomputing it (`sympy`/`numpy`/`scipy`/`fractions`), and every exercise's arithmetic is verified *before* the exercise is written down. This is why no arithmetic error has reached a note; keep it.
- Forward wikilinks to unwritten chapters are fine and expected. Cross-subject links are encouraged.
- Formatting: `[[Wikilinks]]`, `#tags`, Obsidian callouts (`> [!note]`, `> [!warning]`, `> [!example]-`), LaTeX for all math.

## Workflow for a new subject

1. Read `<Subject>/CLAUDE.md`.
2. Extract the table of contents; **choose a scope** (see below) and write `00-Index.md` first.
3. Per chapter: extract → read → verify every numeric claim → design and verify 5 exercises → write → flip the `00-Index.md` status row.
4. **After each chapter, update all three of these — every time, no exceptions:**
   1. flip that chapter's status row in `<Subject>/contents/00-Index.md`;
   2. refresh the **Resume state** section above — what just finished, what is next;
   3. **update the in-progress subject's own `<Subject>/CLAUDE.md`** — its status line, its chapter-plan table, and anything newly learned about the source (a new extraction quirk, an erratum, a scope adjustment).

   **(iii) is the one that gets skipped**, and skipping it is how a subject file drifts into claiming "not started" while eight chapters already exist on disk. One `Edit` each, a few seconds total — and it is what makes an abrupt session end cost nothing.
5. On finishing a subject: mark `<Subject>/CLAUDE.md` ✅ complete with the full chapter list and the findings worth keeping, update the progress table here, and refresh the Resume state section.

**Write access:** the user has authorized writing directly to the vault without per-file confirmation ("no need for confirmation, proceed"). State paths as they are written, don't stop to ask.

## Scope decisions for textbook-only subjects

**Only 6 subjects have lecture slides** — Data Prep & Visualization, Mathematical Statistics, MLOps, Machine Learning, Time-series Analysis, Principle of Accounting. All 6 are done.

For the rest there is **a textbook and nothing else**, so nothing signals which chapters the course covers (Stewart has 17, Mankiw 36, Wooldridge 19). Writing all of them is wrong; picking arbitrarily is also wrong. **The adopted approach:** choose the standard scope for that course level, state the choice prominently at the top of `00-Index.md`, add a "**what is not covered, and why**" section with a one-line reason per omitted chapter, and tell the user it needs confirming against the real syllabus. `Econometrics/contents/00-Index.md` is the template.

## Extracting source material

`pypdf` and `python-pptx` are installed. `PYTHONIOENCODING=utf-8` is **required** — Vietnamese text raises `UnicodeEncodeError` under cp1252. The Read tool cannot render these PDFs (no poppler), so text extraction is the only route.

```bash
PYTHONIOENCODING=utf-8 python -c "
from pypdf import PdfReader
import io
r = PdfReader('file.pdf')
out = []
for i in range(START, END):
    out.append('--- p%d ---' % (i+1))
    out.append((r.pages[i].extract_text() or '').strip())
io.open('out.txt','w',encoding='utf-8').write('\n'.join(out))
"
```

Extract to a file in the scratchpad, then Read it in chunks — never print a whole book to stdout.

**Every textbook PDF mangles maths differently.** Each subject's `CLAUDE.md` records its own substitution table; Stewart's is a full glyph cipher and Nicholson destroys every matrix. **All figures and statistical tables in every book are images and never extract.**

## Progress

| Subject | Status |
|---|---|
| Data Preparation and Visualization | ✅ `00-Index` + ch. 01–11 |
| Mathematical Statistics | ✅ `00-Index` + ch. 01–09 |
| MLOps | ✅ `00-Index` + ch. 01–11 |
| Machine Learning | ✅ `00-Index` + ch. 01–10 (RL only — see subject file) |
| Time-series Analysis | ✅ `00-Index` + ch. 01–10 |
| Principle of Accounting | ✅ `00-Index` + ch. 01–09 |
| Econometrics | ✅ `00-Index` + ch. 01–12 |
| Probability Theory | ✅ `00-Index` + ch. 01–10 |
| Linear Algebra | ✅ `00-Index` + ch. 01–08 |
| Calculus | ✅ `00-Index` + ch. 01–09 |
| Optimization | ✅ `00-Index` + ch. 01–12 |
| Discrete Mathematics | ✅ `00-Index` + ch. 01–10 |
| Data Structures and Algorithms | ✅ `00-Index` + ch. 01–13 |
| Database Management Systems | ✅ `00-Index` + ch. 01–11 |
| Basic Programming (C++) | ✅ `00-Index` + ch. 01–11 |
| Commercial Banking | ✅ `00-Index` + ch. 01–12 (3 errata found) |
| Macroeconomics & Microeconomics | ✅ `00-Index` + ch. 01–14 (7 micro + 7 macro) |
| Monetary and Financial Theories | ✅ `00-Index` + ch. 01–12 (1 erratum found) |
| Principles of Marketing | ✅ `00-Index` + ch. 01–12 (no erratum; 6 discrepancies declined) |
| Business Management | ✅ `00-Index` + ch. 01–09 (no erratum; 6 discrepancies declined) |
| Big Data Analytics | 🚫 Blocked — `documents/` is empty |
| Natural Language Processing | 🚫 Blocked — `documents/` is empty |
| PowerBI | 🚫 Blocked — `documents/` is empty |
| Programming for Data Science (Python) | 🚫 Blocked — `documents/` is empty |

*(This table was incomplete until 2026-08-08 — `Big Data Analytics`, `Business Management` and `Natural Language Processing` were absent. **Verify against the filesystem, not against this table.**)*

## Available skills

- `obsidian-markdown` — wikilinks, callouts, properties, Obsidian-specific syntax
- `obsidian-cli` — read/create/search notes and manage tasks/properties from the vault
- `obsidian-bases` — database-like table/card views over notes
- `json-canvas` — visual canvases / mind maps
- `defuddle` — clean markdown from web pages when source material is a URL
