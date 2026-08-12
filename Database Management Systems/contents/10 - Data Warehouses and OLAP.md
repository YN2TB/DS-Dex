---
subject: Database Management Systems
chapter: 10
tags: [ds, dbms, data-warehouse, olap, star-schema, snowflake, scd, grain, etl, business-intelligence]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 13"
---

# Data Warehouses and OLAP

**This is where the subject meets the rest of the degree.** [[Data Preparation and Visualization/contents/00-Index|Data Preparation]], [[Machine Learning/contents/00-Index|Machine Learning]] and every BI tool assume data arrives in a particular shape — **and this chapter is where that shape is made.**

The organising idea is a reversal. **[[04 - Normalization|Chapter 04]] spent its length removing redundancy; this chapter puts it back on purpose.** A star schema is a *deliberately denormalised* design, and it is correct — but only because of a specific precondition that §9 makes explicit.

**Two results carry the chapter:**

- **§5: an SCD Type 1 update retroactively changed 2023 and 2024 revenue figures** — last year's published report can no longer be reproduced. This is the strongest available argument for Type 2.
- **§6: joining a fact table on the *business* key instead of the *surrogate* key inflated total revenue**, silently. The surrogate key is what makes Type 2 safe.

## 📘 Main Knowledge

### 1. OLTP versus OLAP

| | **OLTP** (ch. 01–09) | **OLAP** (this chapter) |
|---|---|---|
| workload | many short transactions | few long analytical queries |
| access | read **and** write, concurrent | **read-mostly**, batch-loaded |
| data | current state | **historical, time-variant** |
| schema | **normalised** ([[04 - Normalization\|ch. 04]]) | **deliberately denormalised** |
| optimised for | correct **writes** | fast **reads** |
| typical question | *"what is this customer's balance now?"* | *"how did revenue by region trend over 3 years?"* |

**These are different jobs, and no single schema is optimal for both** — which is §9's argument for separating them.

### 2. The star schema

> [!note] Two kinds of table
> A **fact table** holds **measures** (numeric, additive: quantity, revenue) plus **foreign keys** to dimensions. It is huge and grows constantly.
>
> **Dimension tables** hold the **descriptive attributes you group and filter by** (year, category, region). They are small and **denormalised on purpose**.

```sql
CREATE TABLE dim_product (
    prod_key INTEGER PRIMARY KEY, prod_name TEXT,
    category TEXT, subcategory TEXT, brand TEXT);       -- flattened, not normalised

CREATE TABLE fact_sales (
    date_key INTEGER, prod_key INTEGER, cust_key INTEGER, store_key INTEGER,
    quantity INTEGER, unit_price REAL, revenue REAL);   -- keys + measures only
```

*(Built with 300 000 fact rows, 144 dates, 200 products, 3 000 customers, 50 stores.)*

**Every analytical query has the same shape: filter dimensions, join to the fact table, aggregate measures.**

```sql
SELECT d.year, p.category, SUM(f.revenue) AS revenue, SUM(f.quantity) AS units
FROM fact_sales f
JOIN dim_date d    ON f.date_key = d.date_key
JOIN dim_product p ON f.prod_key = p.prod_key
WHERE d.year >= 2024
GROUP BY d.year, p.category;
```
*(Verified.)*

**One join per dimension, always fact-to-dimension, never dimension-to-dimension** — which is exactly why the diagram looks like a star, and why [[03 - Entity-Relationship Modelling|ch. 03]] §7's fan trap cannot arise: dimensions are never joined to each other.

### 3. Star versus snowflake

**A snowflake schema normalises the dimensions** — `dim_product → dim_subcategory → dim_category`.

*(Verified, same question both ways:)*

| | joins | time |
|---|---|---|
| **star** | 1 | **0.1475 s** |
| snowflake | 3 | 0.1679 s |

**Star is 1.14× faster, identical answer.**

> [!note] Report the modest number honestly
> **1.14× is a small gain**, and quoting it plainly matters more than inflating it. **The case for the star is not primarily speed** — dimension tables are tiny, so the extra joins are cheap.
>
> **The real arguments are simplicity and comprehensibility.** A star query is one join per dimension; a snowflake query needs a chain per hierarchy, and BI tools generate worse SQL against it. **The space saved by normalising a 200-row dimension is irrelevant** next to a 300 000-row fact table.
>
> **This is [[04 - Normalization|ch. 04]]'s trade made deliberately, in the direction that is safe here** — and §9 says why it is safe.

### 4. Grain — the most consequential decision

> [!note] Definition
> **The grain is the answer to: "what does exactly one row of the fact table mean?"**
>
> Here: *one product, on one order line, on one date, at one store.*

**Declare the grain before choosing dimensions or measures.** Every dimension must apply at that grain, and every measure must be additive at it. **Mixing grains in one fact table is how double-counting begins.**

### 5. ⚠️ Slowly changing dimensions — Type 1 falsifies history

**Customer 1 lives in the *Central* region and buys throughout 2023–2024. On 2025-01-01 they move to *South*.** What should the reports say?

*(Customer 1's revenue by year, verified: 2023 → 22 019, 2024 → 34 461, 2025 → 22 022.)*

#### Type 1 — overwrite in place

```sql
UPDATE dim_customer SET region = 'South' WHERE cust_key = 1;
```

*(Verified — Central region's revenue, before and after that single update:)*

| year | before | after | **change** |
|---|---|---|---|
| 2023 | 25 181 662 | 25 159 643 | **−22 019** |
| 2024 | 25 260 123 | 25 225 663 | **−34 460** |
| 2025 | 25 438 193 | 25 416 171 | −22 022 |

> [!warning] The 2023 and 2024 figures changed — and they are now wrong
> **Those sales genuinely happened in Central, while the customer lived there.** A Type 1 update has retroactively reassigned them to South.
>
> **The changes are exactly customer 1's revenue for each year** (−22 019 and −34 460 against 22 019 and 34 461), which confirms the mechanism precisely.
>
> **Last year's published report can no longer be reproduced.** Anyone re-running it gets different numbers, with no record that anything changed — and no way to tell whether the old report or the new one is right. **For anything audited, regulated or externally published, this is disqualifying.**

#### Type 2 — add a new row, close the old one

*(Verified — `dim_customer` now holds both versions:)*
```
cust_key | cust_id | region  | valid_from | valid_to   | is_current
---------+---------+---------+------------+------------+-----------
1        | 1       | Central | 2000-01-01 | 2024-12-31 | 0
90001    | 1       | South   | 2025-01-01 | NULL       | 1
```

**The existing fact rows still point at `cust_key = 1`** — the Central version — **because that is who the customer *was* at the time of sale.** New sales will point at `cust_key = 90001`.

**And now both questions are answerable** *(both verified, same 78 502 of revenue):*

| question | answer |
|---|---|
| **"as it was"** — attributed to where they lived at the time | **Central: 78 502** |
| **"as it is now"** — attributed to their current region | **South: 78 502** |

> [!note] This is why Type 2 is the warehousing default
> **Type 1 can answer only "as it is now" and destroys "as it was". Type 2 answers both.**
>
> **This is [[03 - Entity-Relationship Modelling|ch. 03]] §9's time-variant data, now with its standard name** — and the same asymmetry applies: **you can always stop keeping history; you can never reconstruct history you did not keep.**
>
> *(Type 3 keeps a "previous value" column — one step of history only, rarely enough. Type 1 remains right for genuine **corrections**: if the region was simply recorded wrongly, you *want* history rewritten.)*

### 6. ⚠️ The surrogate key is what makes Type 2 safe

**Customer 1 now has two dimension rows. Does anything double-count?**

*(Verified:)*

| join | total revenue |
|---|---|
| no dimension join | 226 809 647 |
| **joining on `cust_key`** (surrogate) | **226 809 647** — no inflation |
| **joining on `cust_id`** (business key) | **226 888 149** — **inflated by 78 502** |

> [!warning] Never join a fact table to a dimension on the natural key
> **Each fact row points at exactly one `cust_key`, so it matches exactly one dimension row** — no inflation.
>
> **But `cust_id = 1` matches *both* versions**, so every one of customer 1's fact rows is counted twice. **The inflation is exactly customer 1's revenue, 78 502** — confirming the mechanism.
>
> **This is [[03 - Entity-Relationship Modelling|ch. 03]] §7's fan trap and [[04 - Normalization|ch. 04]] §5's lossy join, a third time**, and the same rule explains all three: **a join is only meaningful when its key identifies rows in at least one table.** `cust_id` no longer identifies a dimension row once Type 2 is in use.
>
> **So the surrogate key is not bureaucratic overhead — it is the mechanism that makes historical tracking possible without corrupting every aggregate.** It is also why fact tables use meaningless integer keys throughout.

### 7. OLAP operations are `GROUP BY` in disguise

*(All verified:)*

| operation | what it is |
|---|---|
| **roll-up** | aggregate to a coarser level — `GROUP BY year` |
| **drill-down** | the reverse — `GROUP BY year, quarter` |
| **slice** | fix one dimension — `WHERE year = 2025` |
| **dice** | fix several — `WHERE year = 2025 AND category = 'Electronics'` |
| **pivot** | rotate rows/columns — a presentation choice |

```
roll-up:      2023 | 75,543,145      drill-down:  2025 Q1 | 19,322,935
              2024 | 75,320,663                   2025 Q2 | 18,857,668
              2025 | 75,945,838                   2025 Q3 | 18,982,834
```

> [!note] There is nothing new here, and that is the point
> **Roll-up, drill-down, slice, dice and pivot are `GROUP BY` with different columns and different `WHERE` clauses.** The OLAP vocabulary describes *what an analyst is doing*, not new database operations.
>
> **What makes them fast is the schema, not the syntax** — dimensions pre-joined and flattened, so every level of every hierarchy is one column away.

### 8. Subtotals — and a SQLite gap

**Standard SQL provides `ROLLUP`, `CUBE` and `GROUPING SETS` for subtotals in one query.**

> [!warning] SQLite supports none of them — verified
> ```
> GROUP BY ROLLUP(...)        -> no such function: ROLLUP
> GROUP BY CUBE(...)          -> no such function: CUBE
> GROUP BY GROUPING SETS(...) -> syntax error
> ```
> **PostgreSQL, SQL Server and Oracle all support them.** In SQLite, subtotals must be assembled with `UNION ALL` *(verified)*:
> ```sql
> SELECT d.year, p.category, SUM(f.revenue) FROM … GROUP BY d.year, p.category
> UNION ALL
> SELECT d.year, '(all categories)', SUM(f.revenue) FROM … GROUP BY d.year
> ```
> ```
> 2025 | (all categories) | 75,945,838
> 2025 | Clothing         | 30,567,073
> 2025 | Electronics      | 30,218,853
> 2025 | Grocery          | 15,159,913
> ```
> **This is the second SQLite *limitation* in the subject** (after [[08 - Transactions and Concurrency Control|ch. 08]]'s whole-database lock), as distinct from the four *permissivenesses* of ch. 01–05.

### 9. Why the warehouse is a separate database

1. **Workload.** An analytical scan of 300 000 rows would block the OLTP system's short transactions ([[08 - Transactions and Concurrency Control|ch. 08]]). Separation isolates them.
2. **Shape.** OLTP is normalised for correct writes; OLAP is denormalised for fast reads. **One schema cannot be optimal for both.**
3. **History.** OLTP holds current state and routinely overwrites; the warehouse holds every version (§5).
4. **Integration.** A warehouse merges several source systems — which is where the **ETL** (extract, transform, load) work actually goes.

> [!note] The precondition that makes the denormalisation safe
> **[[04 - Normalization|Ch. 04]] warned that denormalisation reintroduces the update anomaly.** Here it cannot occur, **because nothing updates in place**: the warehouse is loaded in controlled batches by one ETL process, and dimensions are versioned rather than modified (§5).
>
> **The anomaly is prevented by *process* rather than by *structure*** — which is exactly the condition [[04 - Normalization|ch. 04]] §8 stated. **Denormalising an OLTP table for speed does not meet it**, which is why the same technique is right here and wrong there.

## ✏️ Exercises

**1. (Star schemas.)** (a) Distinguish facts and dimensions. (b) Why is star preferred to snowflake, given only 1.14×? (c) What is grain? (d) Why can't the fan trap arise?

> [!example]- Solution
> **(a) A fact table holds numeric measures and foreign keys; dimension tables hold the descriptive attributes you group and filter by.**
>
> **The practical test: if you `SUM` it, it is a measure; if you `GROUP BY` or `WHERE` it, it is a dimension attribute.**
>
> **The asymmetry in size is the design's whole basis.** Here: 300 000 fact rows against dimensions of 144, 200, 3 000 and 50 rows. **Dimensions are small enough that denormalising them costs almost nothing** — which is what makes the star affordable.
>
> **(b) Because the case is simplicity, not speed.**
>
> *(Verified: 0.1475 s vs 0.1679 s — 1.14×.)* **That is a small gain, and reporting it plainly is the honest thing to do**; the star is not defended by this number.
>
> **The real arguments:**
> - **Query simplicity** — one join per dimension. A snowflake needs a chain per hierarchy, and every query must know the hierarchy's depth.
> - **BI tools generate better SQL against a star**, because the pattern is uniform.
> - **The space saved is negligible** — normalising a 200-row dimension against a 300 000-row fact table.
> - **Comprehensibility.** Analysts read the schema; a star is legible at a glance.
>
> **The gain would grow with more hierarchy levels or larger dimensions**, but it will never be the main reason.
>
> **(c) The grain is what exactly one fact row means** — here, one product on one order line, on one date, at one store.
>
> **It must be declared before choosing dimensions or measures**, because every dimension must apply at that grain and every measure must be additive at it.
>
> **Getting it wrong is expensive and hard to reverse.** **Too coarse** (one row per order rather than per line) and product-level analysis is impossible for ever — the detail was never stored. **Too fine** is merely costly, and can be aggregated later. **So err fine**: the asymmetry is the same as [[03 - Entity-Relationship Modelling|ch. 03]]'s history decision — you can always aggregate up, never disaggregate down.
>
> **Mixing grains in one fact table causes double-counting**, because a measure at one grain gets summed across rows at another.
>
> **(d) Because dimensions are never joined to one another.**
>
> [[03 - Entity-Relationship Modelling|Ch. 03]] §7's fan trap arises when two tables are joined *through a shared parent* — `TEAM` to `PLAYER` via `DIVISION` — producing a cross product.
>
> **In a star, every join is fact-to-dimension.** The fact table is the hub; dimensions are leaves. **Joining `dim_product` to `dim_customer` is never necessary and never done**, so the structure that creates a fan trap does not exist.
>
> **This is an underrated virtue of the star** — the shape makes a whole class of error unavailable. *(§6 shows the star's own analogous trap, which is joining on the wrong key rather than through the wrong table.)*

**2. (Hard — slowly changing dimensions.)** (a) What did the Type 1 update do? (b) Why is that disqualifying? (c) How does Type 2 work and what does it enable? (d) When is Type 1 correct?

> [!example]- Solution
> **(a) It retroactively changed historical revenue figures.**
>
> *(Verified — one `UPDATE` moving customer 1 from Central to South:)*
>
> | year | before | after | change |
> |---|---|---|---|
> | 2023 | 25 181 662 | 25 159 643 | **−22 019** |
> | 2024 | 25 260 123 | 25 225 663 | **−34 460** |
>
> **The changes are exactly customer 1's revenue in those years** (22 019 and 34 461), confirming the mechanism: their entire purchase history moved region.
>
> **The mechanism is that fact rows carry no region.** They point at a dimension row, and the region is read from *whatever that row currently says*. **Overwrite it and every historical fact is silently reinterpreted.**
>
> **(b) Because published figures stop being reproducible, silently.**
>
> **Re-running last year's report gives different numbers, and nothing records that anything changed.** There is no version, no timestamp, no audit trail — the old value is simply gone.
>
> **Three consequences:**
> - **Reconciliation becomes impossible.** Two reports disagree and neither can be shown correct.
> - **Audited or regulated reporting is disqualified.** A financial statement that changes retroactively is not acceptable, and this would be a control failure.
> - **Model training data becomes non-reproducible.** A model trained on last month's extract cannot be retrained on the same data, which breaks the reproducibility [[MLOps/contents/00-Index|MLOps]] depends on. *(This is the point-in-time correctness problem of [[03 - Entity-Relationship Modelling|ch. 03]] §9, in production.)*
>
> **And it is not detectable after the fact.** The database looks entirely consistent; it is just describing a past that did not happen.
>
> **(c) Type 2 closes the old row and inserts a new one with a new surrogate key.**
>
> *(Verified: `cust_key 1` gets `valid_to = '2024-12-31'`, `is_current = 0`; a new `cust_key 90001` carries the South region from 2025-01-01 with `is_current = 1`.)*
>
> **Existing fact rows keep pointing at `cust_key 1`** — unchanged, because they record who the customer *was*. **New facts point at 90001.**
>
> **Both questions become answerable** *(both verified at 78 502)*:
> - **"as it was"** — join fact to dimension on `cust_key`, giving **Central**.
> - **"as it is now"** — join through to the `is_current = 1` row for the same `cust_id`, giving **South**.
>
> **That second query is the one people forget Type 2 supports.** Type 1 gives only the "as it is now" view; **Type 2 gives both, and the choice is made per query rather than baked into the data.** That is the whole argument.
>
> **The costs are real:** the dimension grows with every change, every fact load must look up the *currently valid* row, and every analyst must know to use `is_current = 1` when they want the present view.
>
> **(d) When the change is a *correction* rather than a *change*.**
>
> **If the region was recorded wrongly — a typo, a bad import — you *want* history rewritten**, because the old value was never true. Keeping it as a "previous version" would preserve a fiction.
>
> **The distinction is whether the old value was ever correct:**
>
> | | example | treatment |
> |---|---|---|
> | **correction** | region was mistyped | **Type 1** — overwrite, no history |
> | **genuine change** | the customer moved | **Type 2** — new version |
>
> **Type 1 is also acceptable for attributes nobody analyses historically** — a contact phone number, say — where the storage and complexity of Type 2 buy nothing.
>
> **The decision is per attribute, not per table**, and it is a business decision: *"do we ever need to report this as it was?"* **Getting it wrong is asymmetric in the usual direction** — Type 2 data can always be collapsed to a current-only view; Type 1 data cannot be un-overwritten.

**3. (Hard — the surrogate key.)** (a) Explain the inflation. (b) How does this relate to earlier chapters? (c) Why does the surrogate key fix it? (d) How would you detect it?

> [!example]- Solution
> **(a) Joining on the business key matched two dimension rows per fact row.**
>
> *(Verified:)*
>
> | join | total |
> |---|---|
> | on `cust_key` (surrogate) | 226 809 647 — correct |
> | **on `cust_id` (business key)** | **226 888 149 — inflated by 78 502** |
>
> **After the Type 2 split, `cust_id = 1` identifies *two* dimension rows** (the Central version and the South version). **So every one of customer 1's fact rows joins to both and is counted twice.**
>
> **The inflation is exactly 78 502 — customer 1's total revenue** — which confirms the mechanism precisely rather than merely suggesting it.
>
> **(b) It is the same fault as two earlier chapters, for the same reason.**
>
> | | joined on | consequence |
> |---|---|---|
> | [[03 - Entity-Relationship Modelling\|ch. 03]] §7 fan trap | `div_id`, a key of neither team nor player | 3, 3, 1 players in a 4-player league |
> | [[04 - Normalization\|ch. 04]] §5 lossy decomposition | `job_class`, a key of neither fragment | 8 triples became 13 |
> | **here** | **`cust_id`, no longer a key of the dimension** | **revenue inflated by 78 502** |
>
> **The unifying rule, stated in [[04 - Normalization|ch. 04]] and confirmed again: a join is only meaningful when its key identifies rows in at least one of the tables.**
>
> **What makes this instance especially instructive is that `cust_id` *used* to be a key.** Before the Type 2 split it identified exactly one dimension row, and the join was correct. **Implementing Type 2 silently invalidated every query that joined on it** — a schema change that breaks queries without breaking them syntactically.
>
> **(c) Because the surrogate key identifies a *version*, while the business key identifies an *entity*.**
>
> **`cust_key` is unique in the dimension by construction** — one row per version — so a fact-to-dimension join on it always matches exactly one row. **`cust_id` identifies the customer across all their versions**, which is a one-to-many relationship, and joining a fact table into a one-to-many relationship multiplies rows.
>
> **So the surrogate key is not bureaucratic overhead — it is the mechanism that makes historical tracking possible without corrupting every aggregate.** Type 2 is only usable *because* facts reference versions rather than entities.
>
> **This also explains why fact tables use meaningless integer keys throughout**, even where a natural key exists: the natural key cannot survive versioning, and it is wider and slower ([[09 - Query Optimization and Indexing|ch. 09]]).
>
> **`cust_id` still belongs in the dimension** — it is how you find all versions of a customer, and how the "as it is now" query works. **It just must never be the fact-to-dimension join key.**
>
> **(d) Reconcile totals against the fact table alone.**
>
> ```sql
> SELECT SUM(revenue) FROM fact_sales;                       -- the truth
> SELECT SUM(f.revenue) FROM fact_sales f JOIN dim … ;       -- must match
> ```
> **A dimension join must never change a fact-table total.** Any difference means row multiplication. *(Verified: the `cust_key` join preserved the total exactly; the `cust_id` join did not.)*
>
> **Other detections, in order of practicality:**
> 1. **`COUNT(*)` before and after the join** — the habit from [[02 - The Relational Model and Relational Algebra|ch. 02]] §4.7, and it catches this immediately.
> 2. **Check the dimension key is unique**: `GROUP BY join_key HAVING COUNT(*) > 1`. If it returns rows, the column is not a key and the join will multiply.
> 3. **Sanity-check against an independently known figure** — last month's total, the source system's own report.
>
> **The first is the cheapest and should be automatic.** In a warehouse, the fact-table total is a fixed quantity that no dimension join may alter, so it is an ideal invariant to assert in a test.

**4. (OLAP and separation.)** (a) What are roll-up, drill-down, slice and dice really? (b) What did the subtotal test show? (c) Why separate the warehouse? (d) Why is denormalising safe here but not in OLTP?

> [!example]- Solution
> **(a) `GROUP BY` with different columns, and `WHERE` with different filters.**
>
> *(All verified.)* **Roll-up** — aggregate to a coarser level (`GROUP BY year`). **Drill-down** — the reverse (`GROUP BY year, quarter`). **Slice** — fix one dimension (`WHERE year = 2025`). **Dice** — fix several. **Pivot** — rotate rows and columns, a presentation choice made in the client.
>
> **The vocabulary describes what an *analyst* is doing, not what the *database* is doing.** It comes from the cube metaphor — slicing a three-dimensional block — and is worth knowing because BI tools use it in their interfaces.
>
> **What makes these fast is the schema, not the syntax.** Because dimensions are flattened, every level of every hierarchy is one column away: rolling up from month to quarter to year is just changing which `dim_date` column you group by, with no extra joins. **In a normalised OLTP schema each level would be another join.**
>
> **(b) That SQLite supports none of `ROLLUP`, `CUBE` or `GROUPING SETS`** *(verified: `no such function: ROLLUP`, `no such function: CUBE`, and a syntax error for `GROUPING SETS`)*.
>
> **These compute subtotals at several levels in one pass.** `GROUP BY ROLLUP(year, category)` returns per-category rows *and* a per-year subtotal *and* a grand total — the shape every management report wants.
>
> **In SQLite they must be assembled with `UNION ALL`** *(verified)*, which is correct but scans the fact table once per level — so an $n$-level rollup costs $n$ passes instead of one.
>
> **This is the second SQLite *limitation*, as opposed to permissiveness.** [[01 - Databases and Data Models|Ch. 01]]–[[05 - SQL Fundamentals|05]] found four cases where SQLite **accepts what stricter engines reject**; [[08 - Transactions and Concurrency Control|ch. 08]] found it *stricter* (whole-database locking); **this is a straightforward missing feature.** The pattern to carry: **SQLite is an excellent teaching database and a poor model of any production engine, in both directions.**
>
> **(c) Four reasons, of which the first two are decisive.**
> 1. **Workload isolation.** A scan of the whole fact table would hold locks and block the OLTP system's short transactions ([[08 - Transactions and Concurrency Control|ch. 08]] measured how badly contention degrades throughput). **Analysts must not be able to slow the checkout.**
> 2. **Incompatible shapes.** Normalised for correct writes versus denormalised for fast reads — **no single schema is optimal for both**, and any compromise is bad at both.
> 3. **History.** OLTP holds current state and overwrites (§5); the warehouse keeps every version.
> 4. **Integration.** A warehouse merges several source systems, each with its own keys, formats and definitions — **and that reconciliation is where most ETL effort actually goes**, not in the loading.
>
> **(d) Because the update anomaly requires updates, and a warehouse does not do them.**
>
> **[[04 - Normalization|Ch. 04]] §8 showed denormalisation buying a 1.6× read gain at the price of storing one value 4 104 times** — so one change means rewriting 4 104 rows, with contradictions if it fails partway.
>
> **In a warehouse that cannot happen**, because:
> - **Loading is batch, by one controlled ETL process** — not many concurrent users.
> - **Nothing updates in place.** Facts are inserted and never modified; dimensions are **versioned** (§5) rather than overwritten.
> - **The load is repeatable.** If it fails, you re-run it; the warehouse is derived data, not the system of record.
>
> **So the anomaly is prevented by *process* rather than by *structure*** — which is precisely the condition [[04 - Normalization|ch. 04]] stated for denormalisation being acceptable.
>
> **And that is why the same technique is right here and wrong in OLTP.** Denormalising a transactional table does not meet the condition: it has many concurrent writers, updates in place, and is the system of record. **The technique is identical; only the precondition differs — and the precondition is what makes it correct.**

## 📝 Summary

- **OLTP and OLAP are different jobs**: short concurrent transactions on normalised current data, versus long read-mostly queries on denormalised historical data. **No single schema is optimal for both.**
- **A star schema is a fact table (measures + foreign keys) surrounded by denormalised dimension tables.** Every query is: filter dimensions → join to fact → aggregate measures, **one join per dimension**.
- **Star beat snowflake by only 1.14×** *(verified, 0.1475 s vs 0.1679 s)*. **The case for the star is simplicity, not speed** — the space saved by normalising a 200-row dimension is irrelevant beside a 300 000-row fact table.
- **[[03 - Entity-Relationship Modelling|Ch. 03]]'s fan trap cannot arise in a star**, because dimensions are never joined to each other.
- **Declare the grain first** — what exactly one fact row means. **Too coarse is unrecoverable; too fine is merely costly**, so err fine.
- **⚠️ SCD Type 1 falsifies history.** *(Verified: one `UPDATE` changed 2023 revenue by −22 019 and 2024 by −34 460 — exactly the moved customer's totals.)* **Last year's report can no longer be reproduced, and nothing records that it changed.**
- **SCD Type 2 closes the old dimension row and inserts a new version** with a new surrogate key. Facts keep pointing at the version current *at the time*. *(Verified: both "as it was" → Central and "as it is now" → South, same 78 502.)*
- **Type 1 answers only "as it is now"; Type 2 answers both.** Type 1 remains right for **corrections** — where the old value was never true.
- **⚠️ Never join a fact table to a dimension on the business key.** *(Verified: joining on `cust_id` instead of `cust_key` inflated revenue by exactly 78 502 — the double-counted customer.)*
- **The surrogate key identifies a *version*; the business key identifies an *entity*.** That distinction is what makes Type 2 possible without corrupting aggregates.
- **This is the third appearance of one rule:** the fan trap ([[03 - Entity-Relationship Modelling|ch. 03]]), lossy decomposition ([[04 - Normalization|ch. 04]]), and this. **A join is only meaningful when its key identifies rows in at least one table.**
- **Roll-up, drill-down, slice, dice and pivot are `GROUP BY` and `WHERE` in disguise.** What makes them fast is the flattened schema, not the syntax.
- **⚠️ SQLite supports none of `ROLLUP`, `CUBE` or `GROUPING SETS`** *(verified)* — subtotals need `UNION ALL`, costing one pass per level.
- **The warehouse is separate for workload isolation, incompatible shapes, history, and integration** — and **ETL's real cost is the integration, not the loading.**
- **Denormalising is safe here because nothing updates in place**: batch loads, insert-only facts, versioned dimensions. **The anomaly is prevented by process, which is exactly the condition [[04 - Normalization|ch. 04]] required.**

## ⚠️ Important Notes

1. **Declare the grain before anything else**, and write it down. Every dimension must apply at it and every measure be additive at it.
2. **Err on the side of a finer grain.** You can always aggregate up; you can never recover detail you did not store.
3. **Never mix grains in one fact table.** It is the direct route to double-counting.
4. **Prefer star to snowflake** for simplicity and tool compatibility — not for the modest speed gain.
5. **⚠️ Use SCD Type 2 for any attribute you might report on historically.** Type 1 silently rewrites published figures.
6. **Decide Type 1 vs Type 2 per attribute, not per table**, and by one question: *was the old value ever correct?* Corrections take Type 1; genuine changes take Type 2.
7. **⚠️ Always join facts to dimensions on the surrogate key.** The business key matches every version and multiplies rows.
8. **A dimension join must never change a fact-table total.** Assert it: `SUM` before and after must match.
9. **`COUNT(*)` before and after every join** — the habit from [[02 - The Relational Model and Relational Algebra|ch. 02]], and it catches this class of fault immediately.
10. **Check a join key is actually a key**: `GROUP BY key HAVING COUNT(*) > 1`. Implementing Type 2 turns a former key into a non-key and silently breaks existing queries.
11. **Remember `is_current = 1` when you want the present view** of a Type 2 dimension — omitting it silently sums across versions.
12. **⚠️ In SQLite, subtotals need `UNION ALL`** — no `ROLLUP`, `CUBE` or `GROUPING SETS`.
13. **Keep the warehouse physically separate** from the OLTP system. Analysts must not be able to block transactions.
14. **Denormalise only where nothing updates in place.** That precondition — not the schema shape — is what makes it correct.
15. **Budget ETL effort for integration, not loading.** Reconciling keys, formats and conflicting definitions across source systems is where the work is.
16. **A warehouse is derived data, not the system of record.** If a load fails, re-run it — which is also why batch loading is safe.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 13 extracts cleanly** — the OLTP/OLAP contrast, data-warehouse characteristics, star and snowflake schemas, facts and dimensions, the OLAP operations, and the data-mart discussion all came through readably. **Book page $n$ = PDF page $n+28$; ch. 13 is PDF pages 601–667.**
>
> **All figures are images and are lost**, and here that is **severe** — second only to [[03 - Entity-Relationship Modelling|ch. 03]]. **A star schema is conventionally taught by its diagram** (the fact table at the centre, dimensions radiating), and C&M's chapter is built around such figures, plus multidimensional-cube illustrations and screenshot-heavy BI-tool walkthroughs. **The response was to give the schema as executable `CREATE TABLE` statements and to run every OLAP operation**, so the structure is shown by what it does rather than by how it is drawn. **The reader should sketch the star** — it is the one diagram in this chapter genuinely worth drawing.
>
> **The entire warehouse is my own** — the schema, the 300 000 generated fact rows, and every query. C&M's examples use downloadable sample databases not present in `documents/`.
>
> **No error was found in Coronel & Morris ch. 13.**
>
> **Additions beyond the source.** **§5's demonstration that Type 1 falsifies history is mine and is the chapter's centrepiece.** C&M defines the SCD types; **executing a Type 1 update and showing 2023 and 2024 revenue *change by exactly the moved customer's totals* converts a definition into an argument.** The consequences drawn — non-reproducible published reports, audit failure, and broken point-in-time correctness for [[MLOps/contents/00-Index|model training]] — are additions, as is the "was the old value ever correct?" test for choosing between Type 1 and Type 2.
>
> **§6, the surrogate-key inflation, is entirely mine**, and is the more surprising result: **joining on the business key inflated revenue by exactly the double-counted customer's total.** Identifying it as the **third instance** of one rule — with [[03 - Entity-Relationship Modelling|ch. 03]]'s fan trap and [[04 - Normalization|ch. 04]]'s lossy decomposition — is my own cross-chapter synthesis, and the observation that **implementing Type 2 retroactively invalidates queries joining on the business key** does not appear in the source.
>
> **§3's star-versus-snowflake measurement is mine**, including the decision to report **1.14×** plainly and argue the star on other grounds rather than inflate the number. **§8's SQLite feature test is mine.** **§9's identification of the precondition that makes warehouse denormalisation safe** — batch loading, insert-only facts, versioned dimensions, and hence *process* rather than *structure* preventing the anomaly — completes the argument [[04 - Normalization|ch. 04]] §8 opened, and is my framing rather than C&M's.
>
> **One error of my own, caught and fixed before writing.** The first Type 1 demonstration hardcoded the customer's region as `North` when the generated data had placed them in `Central`, so **the measured change was 0, 0, 0 while the narrative asserted that history had changed** — the claim contradicted its own output. Fixed by reading the customer's actual region from the data. *(This is the same failure the [[Data Structures and Algorithms/contents/00-Index|DSA]] notes recorded five times: **when a measurement contradicts the claim, the claim is usually the thing that is wrong.**)*
>
> **Deliberately compressed.** **C&M §13-2's twelve rules of data-warehousing (Inmon) and the full characteristic list** are reduced to §1's table and §9's four reasons — the substance is the OLTP/OLAP contrast, and the rest is enumeration. **§13-5's BI architecture and tool survey** (dashboards, reporting styles, vendor comparisons) is omitted: it is business-school framing that dates quickly, and the [[Data Preparation and Visualization/contents/00-Index|Data Preparation]] notes cover visualisation properly. **§13-8's SQL extensions for OLAP** are covered in §8 through the window functions of [[06 - Advanced SQL|ch. 06]] and the `ROLLUP` discussion, rather than as a syntax catalogue. **Data marts** are mentioned but not developed — the structural content is identical to a warehouse at smaller scope. **ETL is discussed as an argument for separation (§9) rather than as a methodology**; the tooling is outside this vault's scope and belongs with [[MLOps/contents/00-Index|MLOps]].

**Previous:** [[09 - Query Optimization and Indexing]] · **Next:** [[11 - Big Data and NoSQL]]
