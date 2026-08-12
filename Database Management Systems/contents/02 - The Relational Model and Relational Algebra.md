---
subject: Database Management Systems
chapter: 2
tags: [ds, dbms, relational-model, relational-algebra, keys, integrity, join, divide, sql]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 3"
---

# The Relational Model and Relational Algebra

[[01 - Databases and Data Models|Chapter 01]] ended on Codd's decisive idea: **relate data by matching *values* rather than by following pointers.** This chapter makes that precise.

The payoff is that **SQL stops being a list of keywords to memorise and becomes eight operators and their combinations.** Every query you will ever write is a composition of the operators in §4 — and once you can see which ones a query is using, both the query and its cost ([[09 - Query Optimization and Indexing|ch. 09]]) become predictable.

**Coronel & Morris is thin here** — it is a business-school text and treats relational algebra as vocabulary. **This chapter develops it properly and executes every operator**, because it is the one piece of theory that pays for itself immediately.

## 📘 Main Knowledge

### 1. A relation is a set

> [!note] Definition
> A **relation** (table) is a set of **tuples** (rows) over a fixed set of **attributes** (columns), each drawing values from a **domain** — the set of values that attribute may take.

**Five properties follow from "set of tuples", and each has a practical consequence:**

| property | consequence |
|---|---|
| every row is unique | enforced by the primary key |
| **row order carries no meaning** | never rely on "the order rows come back in" |
| column order carries no meaning | never rely on `SELECT *` column positions |
| **every value is atomic** | no lists in a cell — this is what 1NF will demand ([[04 - Normalization\|ch. 04]]) |
| a column's values share a domain | the column's type, and why comparisons make sense |

*(Verified — the same relation printed two ways:)*
```
ordered by code : ['311452','312452','313452','314452','315452','316452','317452']
ordered by price: ['311452','316452','313452','312452','315452','317452','314452']
same set? True
```
**`ORDER BY` is a presentation choice, not a change of relation.** A query without `ORDER BY` may return rows in any order at all, and that order may change between runs as the optimiser changes its plan.

### 2. Determination and the hierarchy of keys

> [!note] Determination
> **$A \to B$ ("$A$ determines $B$") means: knowing the value of $A$ lets you look up exactly one value of $B$.** This is a **functional dependency** — a function from $A$'s values to $B$'s, in the [[Discrete Mathematics/contents/03 - Functions, Sequences and Relations|Discrete Maths]] sense.
>
> **A key is an attribute set that determines all the others.** Everything below is a refinement of that one idea, and [[04 - Normalization|ch. 04]] is built entirely on it.

*(Verified by testing the definition directly rather than asserting it:)*
```
p_code -> p_descript, price ?   violations found: 0   -> p_code determines both
vend_code -> p_code ?           violations found: 2   -> vend_code does NOT
```
**A vendor supplies many products, so `vend_code` fails to determine `p_code`** — which is exactly why it cannot be a key of `PRODUCT`, and the test is a `GROUP BY … HAVING COUNT(DISTINCT …) > 1`.

| key | definition |
|---|---|
| **superkey** | any attribute set that uniquely identifies a row |
| **candidate key** | a **minimal** superkey — remove any attribute and uniqueness is lost |
| **primary key** | the candidate key chosen as *the* identifier |
| **foreign key** | an attribute whose values must match a primary key elsewhere (or be null) |
| **secondary key** | used for retrieval convenience; **need not be unique** |

*(Verified on `VENDOR`, testing both uniqueness and minimality:)*

| attribute set | unique? | verdict |
|---|---|---|
| `{vend_code}` | ✓ | **candidate key** (minimal) |
| `{vend_name}` | ✓ | **candidate key** (minimal) |
| `{vend_area}` | ✗ | not a superkey |
| `{vend_code, vend_name}` | ✓ | **superkey, not minimal** |
| `{vend_name, vend_area}` | ✓ | **superkey, not minimal** |

> [!note] Two things worth noticing
> **There can be several candidate keys.** Both `vend_code` and `vend_name` identify a vendor here; choosing one as primary is a design decision. **Prefer a short, stable, meaningless key** — names change, and `vend_name` as a primary key would propagate every rename into every referencing table.
>
> **Uniqueness in the current data does not prove a key.** `vend_name` is unique in these four rows; that is not a guarantee two vendors cannot share a name. **Only a business rule settles it** ([[01 - Databases and Data Models|ch. 01]] §7) — the same warning as before: data shows what *has* happened, not what is *permitted*.

### 3. The two integrity rules

> [!note] The rules
> **Entity integrity:** every primary key value is **unique and not null**. Without it a row has no identity and cannot be referred to.
>
> **Referential integrity:** every foreign key value either **matches an existing primary key** or **is null**. Without it references dangle.

*(Verified — the enforcement, not just the statement:)*

| attempted | result |
|---|---|
| duplicate primary key | **rejected** — `UNIQUE constraint failed: vendor.vend_code` |
| foreign key `vend_code=777` (no such vendor) | **rejected** — `FOREIGN KEY constraint failed` |
| foreign key `vend_code=NULL` | **accepted** — legal, means "unknown/none" |
| deleting vendor 231, which has 3 products | **rejected** — `FOREIGN KEY constraint failed` |

**Note the asymmetry: a foreign key may be null, a primary key may not.** A product with no vendor is a meaningful state (the vendor is not yet chosen); a product with no identity is not.

**And referential integrity protects both ends** — it blocks orphan creation by `INSERT` *and* orphan creation by `DELETE`. That second half is easy to forget and is what `ON DELETE CASCADE` / `ON DELETE SET NULL` exist to customise.

> [!warning] ⚠️ SQLite does not enforce entity integrity by default — verified
> **`PRIMARY KEY` does not imply `NOT NULL` in SQLite.** Worse, the nulls are not even unique:
> ```
> CREATE TABLE t (id TEXT PRIMARY KEY, v TEXT);
> INSERT INTO t VALUES (NULL,'a');
> INSERT INTO t VALUES (NULL,'b');
> SELECT * FROM t;  ->  [(None,'a'), (None,'b')]
> ```
> **Two rows, both with no identity, in a table whose primary key is supposed to forbid exactly that.** *(Verified on SQLite 3.50.4.)*
>
> **`INTEGER PRIMARY KEY` misbehaves differently**: it is an alias for the internal `ROWID` and **silently auto-assigns a value** instead of rejecting the null — even when you write `NOT NULL`:
> ```
> CREATE TABLE t3 (id INTEGER PRIMARY KEY NOT NULL, v TEXT);
> INSERT INTO t3 VALUES (NULL,'a');   ->  [(1,'a')]      -- invented an id
> ```
> **In this chapter's own demonstration that quirk inserted a phantom "Null PK Co" vendor**, which then appears in §4's `UNION` output — an accidental but honest illustration of the consequence.
>
> **Two fixes, both verified:** declare `id TEXT PRIMARY KEY NOT NULL` (→ `NOT NULL constraint failed`), or use a **`STRICT` table**, which enforces it properly (→ `NOT NULL constraint failed`).
>
> **Taken with [[01 - Databases and Data Models|ch. 01]]'s finding that `PRAGMA foreign_keys` is off by default, the pattern is clear: SQLite enforces neither integrity rule unless you ask.** It is an excellent teaching database and a trap for anyone who assumes the declarations mean what they say. **PostgreSQL rejects all of these outright.**

### 4. The eight operators

**Every one below was executed; the outputs are real.**

#### (1) SELECT (σ) — choose rows
Also called RESTRICT. Unary: takes one relation, returns rows matching a condition.

$$\sigma_{\text{price} < 10.00}(\text{PRODUCT})$$
```sql
SELECT * FROM product WHERE price < 10.00;   -- 4 rows
```

#### (2) PROJECT (π) — choose columns
Unary: returns the named attributes, **with duplicates removed.**

$$\pi_{\text{vend\_code}}(\text{PRODUCT})$$
```sql
SELECT DISTINCT vend_code FROM product;
```

> [!warning] SQL is not relational algebra: tables are bags, relations are sets
> **Relational PROJECT removes duplicates by definition. Plain SQL `SELECT` does not.**
> ```
> SELECT vend_code          -> 7 rows
> SELECT DISTINCT vend_code -> 4 rows
> ```
> *(Verified.)* **SQL tables are *multisets* (bags); relations are *sets*.** `DISTINCT` bridges the gap, and forgetting it is why aggregates come out inflated — a `COUNT(*)` after a join counts duplicated rows, not distinct entities.
>
> *(Note `DISTINCT` treats all nulls as one value: the 4 above includes `NULL` as a single entry.)*

#### (3)(4)(5) UNION, INTERSECT, DIFFERENCE — set operators

**All three require the relations to be *union-compatible*: the same number of attributes, drawn from the same domains.**

```sql
SELECT vend_name, vend_area FROM vendor UNION     SELECT name, area FROM supplier;
SELECT vend_name, vend_area FROM vendor INTERSECT SELECT name, area FROM supplier;
SELECT vend_name, vend_area FROM vendor EXCEPT    SELECT name, area FROM supplier;  -- DIFFERENCE
```

*(Verified, including the failure:)*
```
1 column UNION 2 columns -> rejected:
    SELECTs to the left and right of UNION do not have the same number of result columns
```
**`UNION` removes duplicates** (`UNION ALL` keeps them, and is faster because it need not sort). **SQL's keyword for DIFFERENCE is `EXCEPT`** — worth remembering, since the algebra name never appears.

#### (6) PRODUCT (×) — every pairing

$$|\text{VENDOR} \times \text{PRODUCT}| = |\text{VENDOR}|\cdot|\text{PRODUCT}|$$

*(Verified: $5 \times 7 = 35$.)*

**On its own it is almost always meaningless.** It matters because of what it builds:

#### (7) JOIN — and what it really is

> [!note] JOIN is not primitive
> $$\text{PRODUCT} \bowtie \text{VENDOR} \;=\; \pi\big(\sigma_{\text{p.vend\_code}=\text{v.vend\_code}}(\text{PRODUCT} \times \text{VENDOR})\big)$$
>
> **Take every pairing, keep the ones where the keys match, project the columns you want.** *(Verified: the natural join and the explicit product-select-project both returned 6 rows, and the results were **identical**.)*
>
> **This is worth knowing for two reasons.** It explains why a forgotten join condition returns a huge result — you get the raw Cartesian product. And it explains why joins are the expensive operation ([[09 - Query Optimization and Indexing|ch. 09]]): the naive cost is $|R|\cdot|S|$, and everything the optimiser does is an attempt to avoid actually forming that product.

**The join variants:**

| | keeps |
|---|---|
| **INNER JOIN** | only rows matching on both sides |
| **LEFT OUTER** | all left rows; nulls where the right has no match |
| **RIGHT / FULL OUTER** | mirror image / both |
| **NATURAL JOIN** | joins on all same-named columns automatically — **avoid it**, it breaks when a column is added |

> [!warning] The inner join silently discards non-matching rows
> *(Verified — a `LEFT JOIN` reveals exactly what the inner join lost:)*
> ```
> p_descript     | vend_name
> ---------------+----------
> PVC pipe 3.5in | None
> ```
> **`PVC pipe` has no vendor, so the inner join dropped it — with no error and no warning.** 7 products in, 6 out.
>
> **This is the single commonest cause of silently missing rows in analysis.** Your row count falls, nothing complains, and the loss is invisible unless you look for it. **Check `COUNT(*)` before and after every join**, and use a `LEFT JOIN … WHERE right.key IS NULL` to see what would be dropped.

#### (8) DIVIDE (÷) — "related to *all* of them"

**The hard one, and the one with no SQL keyword.** *"Which vendors supply **every** part?"*

```
SUPPLIES:  231 -> bolt, nut, washer      PART:  bolt
           232 -> bolt, nut                     nut
           235 -> bolt, nut, washer             washer
           240 -> washer
```

```sql
SELECT DISTINCT s.vend_code FROM supplies s
WHERE NOT EXISTS (
    SELECT 1 FROM part p
    WHERE NOT EXISTS (
        SELECT 1 FROM supplies s2
        WHERE s2.vend_code = s.vend_code AND s2.part = p.part));
```
*(Verified: returns **231 and 235** — correctly excluding 232, which lacks `washer`, and 240, which has only `washer`.)*

> [!note] Why it needs a double negative
> **SQL has `EXISTS` but no "for all".** So $\forall$ is expressed by the logical equivalence
> $$\forall x\, P(x) \;\equiv\; \neg\,\exists x\, \neg P(x)$$
> — *"there is no part that this vendor does **not** supply"* ([[Discrete Mathematics/contents/01 - Sets and Logic|DM ch. 01]]'s quantifier negation, doing real work).
>
> **The counting alternative** is easier to read and often faster:
> ```sql
> SELECT vend_code FROM supplies GROUP BY vend_code
> HAVING COUNT(DISTINCT part) = (SELECT COUNT(*) FROM part);
> ```
> *(Verified: same answer, 231 and 235.)* **But it is only correct if the divisor has no duplicates and the pairings are unique** — hence `COUNT(DISTINCT part)`, not `COUNT(part)`. The double-`NOT EXISTS` form is always correct.
>
> **Divide answers a common shape of question**: students who passed every core module, customers who bought every product in a range, users with every required permission.

### 5. Closure — why any of this composes

> [!note] The closure property
> **Every relational operator takes relations and returns a relation.** So results can be fed straight back in.

*(Verified — select, join, project and aggregate in one expression, whose result is itself a table:)*
```sql
SELECT v.vend_area, COUNT(*) AS n, ROUND(AVG(p.price),2) AS avg_price
FROM product p JOIN vendor v ON p.vend_code = v.vend_code
WHERE p.price < 100
GROUP BY v.vend_area HAVING COUNT(*) > 1
ORDER BY avg_price DESC;
```
```
vend_area | n | avg_price
----------+---+----------
904       | 3 | 14.9
615       | 2 | 7.47
```

**Closure is why subqueries, CTEs and views exist at all** ([[06 - Advanced SQL|ch. 06]]). It is a small formal property with a very large practical consequence: **the language needs no separate constructs for intermediate results.**

### 6. Relationships, and why M:N needs a third table

| | implementation |
|---|---|
| **1:1** | foreign key in either table, with a uniqueness constraint |
| **1:M** | **foreign key on the "many" side** — the common case |
| **M:N** | **cannot be stored directly — requires a junction (bridge) table** |

**Why M:N is impossible directly:** to put many vendors in a part's row you would need a *list* in one cell, violating **atomicity** (§1). The solution is a table of the pairings, whose primary key is the pair:

```sql
CREATE TABLE supplies (
    vend_code INTEGER, part TEXT,
    PRIMARY KEY (vend_code, part)      -- composite key: each pairing recorded once
);
```
*(Verified: re-inserting `(231,'bolt')` was rejected — `UNIQUE constraint failed: supplies.vend_code, supplies.part`.)*

**An M:N relationship becomes two 1:M relationships pointing into the junction table**, and the junction table is often an entity in its own right — an `ENROLMENT` carries a grade, an `ORDER_LINE` carries a quantity. **Recognising that is most of [[03 - Entity-Relationship Modelling|ch. 03]].**

## ✏️ Exercises

**1. (Relations and keys.)** (a) List the five properties of a relation and give a consequence of each. (b) Define superkey, candidate key and primary key, using the verified table. (c) Why is `vend_code` not a key of `PRODUCT`? (d) Why prefer a meaningless primary key?

> [!example]- Solution
> **(a)**
>
> | property | consequence |
> |---|---|
> | rows are unique | the primary key exists to guarantee it; duplicates are not merely untidy but not *representable* |
> | **row order is meaningless** | **never rely on returned order without `ORDER BY`** — the optimiser may change its plan and the order with it |
> | column order is meaningless | avoid `SELECT *` in code that reads by position; a new column silently shifts everything |
> | **values are atomic** | no comma-separated lists in a cell — this *is* first normal form ([[04 - Normalization\|ch. 04]]) |
> | a column shares one domain | gives the column its type, and makes comparison and indexing meaningful |
>
> *(The order property was verified: the same rows sorted by code and by price form the same set.)*
>
> **(b)** A **superkey** uniquely identifies a row. A **candidate key** is a *minimal* superkey — drop any attribute and uniqueness fails. The **primary key** is the candidate key chosen as the identifier.
>
> *(Verified on `VENDOR`:)* `{vend_code}` and `{vend_name}` are each unique and single-attribute, so both are **candidate keys**. `{vend_code, vend_name}` is unique but **not minimal** — `vend_code` alone suffices — so it is a superkey only. `{vend_area}` is not unique at all.
>
> **Minimality is the whole distinction**, and it matters because a non-minimal key wastes space in every referencing table and makes joins more expensive.
>
> **(c) Because a vendor supplies many products, so `vend_code` determines no unique `p_code`.**
>
> *(Verified: `GROUP BY vend_code HAVING COUNT(DISTINCT p_code) > 1` returned **2** violating groups.)* Two vendors each supply several products, so knowing the vendor does not tell you which product.
>
> **This is the definitional test for a key** — a key must determine *every* other attribute — and it is worth running rather than assuming, because it is the same test [[04 - Normalization|ch. 04]] uses for functional dependencies throughout.
>
> **(d) Because a meaningful key changes, and a primary key must not.**
>
> `vend_name` is a candidate key here, but names change — a merger, a rebrand, a typo correction. **The primary key is copied into every referencing table as a foreign key**, so changing it means updating every one of them, in step, without error. That is the update anomaly of [[01 - Databases and Data Models|ch. 01]] §3.1 arriving through the front door.
>
> **A surrogate key** (an arbitrary integer with no business meaning) is stable precisely because nothing in the world can force it to change. Choose primary keys that are **short** (copied everywhere, and used in every index — [[09 - Query Optimization and Indexing|ch. 09]]), **stable**, and **never null**.
>
> **The counter-consideration:** surrogate keys make it possible to insert genuine duplicates that differ only by their invented id. **So keep a `UNIQUE` constraint on the natural key as well** — the surrogate is for referencing, the natural key for correctness.

**2. (Integrity — and SQLite's failure to provide it.)** (a) State both rules and why each is needed. (b) Why may a foreign key be null when a primary key may not? (c) What did the SQLite tests show? (d) What is the general lesson?

> [!example]- Solution
> **(a) Entity integrity: the primary key is unique and not null.** Without uniqueness a "key" identifies several rows; without non-nullity a row has **no identity**, so it cannot be referenced, updated by key, or reliably deleted.
>
> **Referential integrity: a foreign key matches an existing primary key, or is null.** Without it references dangle — a product pointing at vendor 777 when no such vendor exists, so the join silently returns nothing and the product vanishes from every report.
>
> **Together they guarantee that the value-matching of [[01 - Databases and Data Models|ch. 01]] §8 actually works.** The relational model connects data by matching values; these two rules are what make the matched values trustworthy.
>
> **(b) Because "not yet known" is a meaningful state for a relationship and a meaningless one for identity.**
>
> A product whose vendor has not been chosen is a real thing — *(verified: `PVC pipe 3.5in` has `vend_code = NULL` and is accepted)*. **A null foreign key says "this row participates in no relationship", which is often true.**
>
> **A row with no identity is incoherent.** You could not refer to it, update it by key, or distinguish it from another such row. *(Verified in the SQLite test: two rows with null keys were genuinely indistinguishable.)* And since nulls do not compare equal to each other, a null primary key could not even be checked for uniqueness — which is exactly why the SQLite table accepted **two** of them.
>
> **The asymmetry also shows in `DELETE`:** removing a vendor that still has products was **rejected** *(verified)*, because it would create dangling references. Referential integrity protects both ends — insertion *and* deletion — which is what `ON DELETE CASCADE` and `ON DELETE SET NULL` let you customise.
>
> **(c) That SQLite enforces neither rule by default.**
>
> | test | result |
> |---|---|
> | `TEXT PRIMARY KEY`, insert `NULL` twice | **both accepted** — two rows, no identity, not unique |
> | `INTEGER PRIMARY KEY`, insert `NULL` | **auto-assigns a value** — no rejection |
> | `INTEGER PRIMARY KEY NOT NULL`, insert `NULL` | **still auto-assigns** — the `NOT NULL` is overridden |
> | `TEXT PRIMARY KEY NOT NULL`, insert `NULL` | rejected ✓ |
> | **`STRICT` table**, insert `NULL` | rejected ✓ |
>
> *(All verified on SQLite 3.50.4.)*
>
> **The first row is the serious one**: a declared primary key permitting two identity-less rows is entity integrity failing completely, silently, with a schema that looks correct on review.
>
> **The `INTEGER PRIMARY KEY` case is subtler and arguably worse** — it does not fail, it *invents* data. In this chapter's own demonstration it created a phantom `"Null PK Co"` vendor that then turned up in the `UNION` results. **A schema bug produced a fabricated business record.**
>
> **Combined with [[01 - Databases and Data Models|ch. 01]]'s finding that `PRAGMA foreign_keys` defaults to off, SQLite provides neither integrity rule unless explicitly asked.** PostgreSQL and MySQL/InnoDB reject all of these.
>
> **(d) A declaration is not an enforcement. Test the constraint; do not read it.**
>
> Every one of these schemas passes review — `PRIMARY KEY` and `REFERENCES` are right there in the DDL. **The only way to know whether they bind is to insert a row that should be refused and check that it is.**
>
> **The generalisation beyond SQLite:** the same gap appears as MySQL's MyISAM engine ignoring foreign keys, as `CHECK` constraints parsed but unenforced in older versions, and as ORM-level validation that vanishes the moment anything writes directly to the database. **Constraints enforced by application code are not constraints** — they hold only for the paths that remember them.
>
> **This is also the vault's verify-every-number rule doing real work in a new domain.** Reading the schema would have given the wrong answer; running it gave the right one — and it is why this subject's rule is *run the SQL*.

**3. (Hard — the operators.)** (a) Why is PROJECT not plain `SELECT`? (b) Show that JOIN is not primitive, and give two consequences. (c) Why does the inner join lose rows silently? (d) What is closure and why does it matter?

> [!example]- Solution
> **(a) Because PROJECT is defined to remove duplicates and `SELECT` is not.**
>
> *(Verified: `SELECT vend_code` gave **7** rows, `SELECT DISTINCT vend_code` gave **4**.)*
>
> **The underlying reason is that SQL tables are *multisets* (bags) while relations are *sets*.** SQL departed from the model deliberately: deduplication requires sorting or hashing, so making it automatic would impose a cost on every query whether or not it was wanted.
>
> **The practical consequence is inflated aggregates.** After a join that duplicates rows, `COUNT(*)` counts row-copies rather than distinct entities — the classic wrong answer where "customers who ordered" is really "orders". **`COUNT(DISTINCT customer_id)` is the fix**, and knowing that SQL is bag-based is what makes the bug predictable rather than surprising.
>
> *(A related subtlety, verified: `DISTINCT` treats all nulls as a single value, so the 4 above includes `NULL` as one entry — even though `NULL = NULL` is not true in a `WHERE` clause. The set operators and `GROUP BY` treat nulls as equal; comparison operators do not.)*
>
> **(b)** $$R \bowtie_{\theta} S \;=\; \pi_{\text{cols}}\big(\sigma_{\theta}(R \times S)\big)$$
>
> **Form every pairing, keep those satisfying the join condition, project the columns wanted.** *(Verified: the natural join and the explicit product-select-project produced 6 rows each and were **identical**.)*
>
> **Consequence 1 — a missing join condition gives you the Cartesian product.** Omit the `ON` clause and you get $|R|\cdot|S|$ rows *(verified: $5\times 7=35$)*. On two million-row tables that is $10^{12}$ rows — the runaway query that hangs a database, and now its cause is obvious rather than mysterious.
>
> **Consequence 2 — the join is the expensive operator, and optimisation is the art of not doing this.** The definition's cost is $O(|R|\cdot|S|)$. **No engine actually forms the product**: it uses a nested-loop join with an index (turning the inner scan into a [[Data Structures and Algorithms/contents/10 - Search Trees|B-tree]] lookup), a **hash join** ([[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]]), or a **sort-merge join** ([[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]]). **The algebra says what the answer is; the optimiser chooses how** ([[09 - Query Optimization and Indexing|ch. 09]]) — and it may, precisely because the definition constrains only the result.
>
> **(c) Because a row with no match satisfies no pairing, so the σ step removes it — which is correct behaviour, not a bug.**
>
> *(Verified: 7 products in, 6 out. A `LEFT JOIN … WHERE vend_name IS NULL` identified the casualty as `PVC pipe 3.5in`, which has a null vendor.)*
>
> **It is dangerous because nothing signals it.** No error, no warning; the query succeeds and returns a smaller answer. **Every downstream number is then computed on a silently reduced population** — a total, a mean, a model's training set. The parallel with [[01 - Databases and Data Models|ch. 01]] §3.3's deletion anomaly is exact: **the failure modes that leave no evidence are the expensive ones.**
>
> **Three defences.** **Count before and after** every join and reconcile the difference. **Use `LEFT JOIN … WHERE right.key IS NULL`** to enumerate what would be dropped, before dropping it. **Prefer a `LEFT JOIN` when the left table is the population you are reporting on** — you want the nulls to show up as nulls, visibly, rather than as absent rows.
>
> **Nulls in the join column are the usual cause**, and they arise legitimately (§3): a null foreign key means "no relationship", and an inner join is entitled to conclude there is nothing to join to.
>
> **(d) Closure: every operator takes relations and returns a relation, so results can be reused as inputs.**
>
> *(Verified: select → join → project → aggregate composed in a single expression, itself yielding a table.)*
>
> **Why it matters practically:**
> 1. **Subqueries work at all** — a query's result is a table, so it can appear wherever a table can.
> 2. **Views are possible** — name a query and use it as a table ([[06 - Advanced SQL|ch. 06]]), which is what makes the external level of [[01 - Databases and Data Models|ch. 01]] §9 implementable.
> 3. **CTEs and recursive queries** chain relations by name.
> 4. **The language stays small** — no separate constructs for intermediate results.
>
> **Why it matters theoretically:** closure makes the operators an *algebra* in the mathematical sense — a set closed under its operations, like the integers under addition. **That is what allows algebraic *rewriting*, and rewriting is what an optimiser does.** Because $\sigma_\theta(R \bowtie S) = \sigma_\theta(R) \bowtie S$ when $\theta$ mentions only $R$, the engine can push the filter down and join far fewer rows — **the single most valuable transformation in query optimisation** ([[09 - Query Optimization and Indexing|ch. 09]]), and it is a theorem about the algebra, not a heuristic.

**4. (DIVIDE and M:N.)** (a) What does DIVIDE compute and why the double negative? (b) Compare it with the counting version. (c) Why can M:N not be stored directly? (d) When is a junction table an entity?

> [!example]- Solution
> **(a) DIVIDE finds the $X$ related to *every* $Y$** — *"which vendors supply all parts?"*
>
> *(Verified: 231 and 235, correctly excluding 232 — which lacks `washer` — and 240, which supplies only `washer`.)*
>
> **The double negative is needed because SQL has `EXISTS` but no universal quantifier.** So you use the logical equivalence from [[Discrete Mathematics/contents/01 - Sets and Logic|DM ch. 01]]:
> $$\forall x\, P(x) \;\equiv\; \neg\,\exists x\, \neg P(x)$$
>
> Read the query inside out: *there is **no** part $p$ such that there is **no** `supplies` row pairing this vendor with $p$* — i.e. **no part this vendor fails to supply**, i.e. the vendor supplies all of them.
>
> **The inner `NOT EXISTS` is correlated to both** the outer vendor and the middle part, which is why the query is hard to read and easy to get wrong. **It is worth memorising as a template** rather than re-deriving each time.
>
> **(b)**
> ```sql
> SELECT vend_code FROM supplies GROUP BY vend_code
> HAVING COUNT(DISTINCT part) = (SELECT COUNT(*) FROM part);
> ```
> *(Verified: same answer.)*
>
> | | double `NOT EXISTS` | counting |
> |---|---|---|
> | readability | poor | **good** |
> | correctness | **always** | needs care |
> | speed | can be slow | usually faster (one aggregation) |
>
> **The counting version's trap is `COUNT(part)` versus `COUNT(DISTINCT part)`.** If `supplies` can hold the same pair twice, `COUNT(part)` counts duplicates and a vendor supplying `bolt` three times would appear to cover three parts. *(Here the composite primary key prevents duplicates — verified by the rejected re-insert — so both forms are safe. **In general the composite key is what makes the shortcut valid**, which is a good reason to always declare it.)*
>
> **A second trap: it must count only parts that are in the divisor.** If `supplies` contained a part absent from `PART`, the counts could match for the wrong reason. The robust form joins to `part` first.
>
> **Use counting when the keys are properly constrained; keep the `NOT EXISTS` template for when they are not.**
>
> **(c) Because storing many vendors in one part's row would require a list in a cell, violating atomicity (§1).**
>
> A 1:M relationship needs only one foreign key, on the "many" side. **M:N has a "many" on *both* sides**, so neither table has a single value to store — `part.vendors` would have to be `'231,232,235'`.
>
> **Why that is fatal rather than merely inelegant:** you cannot index it, join on it, or constrain it with a foreign key; `WHERE vendors = '231'` fails and `LIKE '%231%'` matches `1231`; adding or removing one vendor means parsing and rewriting a string. **This is exactly what 1NF forbids** ([[04 - Normalization|ch. 04]]).
>
> **The junction table solves it** by making each *pairing* a row, with the pair as the composite primary key *(verified: re-inserting `(231,'bolt')` was rejected)*. **An M:N relationship becomes two 1:M relationships pointing into the junction table** — and note the junction table is what DIVIDE operates on, which is not a coincidence: "all of them" questions are inherently about M:N relationships.
>
> **(d) Whenever the *relationship itself* has attributes — which is most of the time.**
>
> A pure junction table holds only the two foreign keys. But ask what else is true *of the pairing*:
>
> | junction | attributes of the relationship |
> |---|---|
> | `SUPPLIES` (vendor–part) | unit price, lead time, contract date |
> | `ENROLMENT` (student–course) | **grade**, semester, attendance |
> | `ORDER_LINE` (order–product) | **quantity**, price at time of sale |
>
> **A grade belongs to neither the student nor the course — it belongs to the *enrolment*.** Once the table carries such attributes it is a full entity, usually with its own name and sometimes its own surrogate key.
>
> **Two design consequences.** **The composite key may stop being sufficient**: if a student can retake a course, `(student, course)` no longer identifies a row and the key must include the semester. **And the junction table often acquires its own relationships** — an `ORDER_LINE` might reference a shipment.
>
> **Recognising this early is most of [[03 - Entity-Relationship Modelling|ch. 03]]**, because a designer who treats junctions as plumbing rather than entities has nowhere to put the attributes that inevitably appear, and ends up storing the grade on the student.

## 📝 Summary

- **A relation is a *set* of tuples**, so rows are unique, **row and column order carry no meaning**, values are **atomic**, and each column draws from one domain. *(Verified: the same relation sorted two ways is the same set — `ORDER BY` is presentation, not content.)*
- **$A \to B$ means knowing $A$ determines exactly one $B$** — a functional dependency, and the foundation of both keys and [[04 - Normalization|ch. 04]].
- **Superkey ⊃ candidate key (minimal) ⊃ primary key.** *(Verified on `VENDOR`: `{vend_code}` and `{vend_name}` are candidate keys; `{vend_code, vend_name}` is a superkey but not minimal; `{vend_area}` is neither.)*
- **`vend_code` is not a key of `PRODUCT`** *(verified: 2 violating groups)* — a vendor supplies many products.
- **Prefer short, stable, meaningless primary keys.** A meaningful key propagates every change into every referencing table.
- **Entity integrity:** primary keys unique and not null. **Referential integrity:** foreign keys match an existing key or are null. *(Both verified as enforced — including that deleting a referenced vendor was rejected.)*
- **A foreign key may be null; a primary key may not** — "no relationship" is meaningful, "no identity" is not.
- **⚠️ SQLite enforces neither rule by default** *(verified)*: `TEXT PRIMARY KEY` accepted **two null keys**, and `INTEGER PRIMARY KEY` **auto-assigns** rather than rejecting — even with `NOT NULL`. Fix with an explicit `NOT NULL` on a non-integer key, or a **`STRICT` table**.
- **The eight operators:** SELECT (rows), PROJECT (columns, deduplicated), UNION / INTERSECT / DIFFERENCE (`EXCEPT` in SQL, requiring union compatibility), PRODUCT, JOIN, DIVIDE.
- **SQL tables are bags; relations are sets.** *(Verified: 7 rows vs 4 with `DISTINCT`.)* This is why aggregates after a join come out inflated.
- **JOIN is not primitive: $R \bowtie S = \pi(\sigma(R \times S))$** *(verified identical)*. Hence a missing join condition yields the full product ($5\times7=35$), and **the join is the operator optimisation exists to speed up.**
- **⚠️ An inner join silently drops non-matching rows** *(verified: 7 products in, 6 out — `PVC pipe` lost to a null vendor)*. **Count before and after every join.**
- **DIVIDE answers "related to all"** via double `NOT EXISTS`, because $\forall x\,P(x) \equiv \neg\exists x\,\neg P(x)$. *(Verified: 231 and 235.)* The counting form is clearer but needs `COUNT(DISTINCT …)` and a properly constrained junction.
- **Closure — every operator returns a relation — is why subqueries, views and CTEs exist**, and why the optimiser may rewrite queries algebraically.
- **M:N cannot be stored directly** (it would need a list in a cell) and requires a **junction table with a composite key** *(verified: duplicate pairing rejected)*. **It becomes an entity as soon as the relationship has attributes** — a grade, a quantity, a price.

## ⚠️ Important Notes

1. **Never rely on row order without `ORDER BY`.** There is no default order, and the one you observe can change when the data or the query plan changes.
2. **Avoid `SELECT *` in stored code.** Column order is meaningless and a new column silently shifts positional reads.
3. **A key must determine every other attribute — test it** with `GROUP BY key HAVING COUNT(DISTINCT other) > 1` rather than assuming.
4. **Uniqueness in current data does not prove a candidate key.** Only a business rule does.
5. **Choose primary keys that are short, stable and never null**, and keep a `UNIQUE` constraint on the natural key alongside a surrogate.
6. **⚠️ In SQLite, `PRIMARY KEY` does not imply `NOT NULL`.** Write it explicitly or use a `STRICT` table. With `INTEGER PRIMARY KEY` a null is *auto-assigned*, fabricating data.
7. **⚠️ Also set `PRAGMA foreign_keys = ON` per connection** ([[01 - Databases and Data Models|ch. 01]]). **SQLite gives you neither integrity rule unless asked.**
8. **Test constraints by inserting rows that should fail.** A declaration in the DDL is not evidence of enforcement.
9. **`DISTINCT` is not optional when you mean PROJECT.** Aggregates after joins need `COUNT(DISTINCT …)` or they count row-copies.
10. **Nulls behave inconsistently by design**: `DISTINCT`, `GROUP BY` and the set operators treat all nulls as equal; `=` does not. Use `IS NULL`.
11. **`EXCEPT` is SQL's DIFFERENCE**, and set operators need union compatibility — same column count, same domains.
12. **A forgotten join condition produces the Cartesian product.** On large tables it will not finish.
13. **⚠️ Check `COUNT(*)` before and after every join.** Inner joins drop non-matching rows with no warning — the commonest source of quietly wrong analysis.
14. **Use `LEFT JOIN … WHERE right.key IS NULL` to see what an inner join would discard**, before discarding it.
15. **Avoid `NATURAL JOIN`.** It joins on all same-named columns, so adding a column later changes the query's meaning without touching the query.
16. **Memorise the double-`NOT EXISTS` template for "for all" questions**; use the counting form only when the junction's composite key guarantees no duplicate pairings.
17. **Always declare the composite primary key on a junction table.** It prevents duplicate pairings and is what makes counting-based division correct.
18. **Expect junction tables to become entities.** If the relationship has any attribute of its own, it already is one.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 3 extracts cleanly** — the relation properties, determination and the key hierarchy, both integrity rules, and the definitions of all eight operators came through readably. **Book page $n$ = PDF page $n+28$; ch. 3 is PDF pages 93–135.**
>
> **All figures are images and are lost**, including **Figure 3.1 (the `STUDENT` table used for the determination discussion)** and the tabulated before/after illustrations of every relational-algebra operator — which in this chapter is a substantial loss, since the book teaches the operators almost entirely through those figures. **The response was to rebuild them as a real database and print genuine output**, so every operator in §4 is shown by execution rather than by illustration.
>
> **The `VENDOR`/`PRODUCT` data is reconstructed.** The product codes, descriptions and prices (`311452 Power drill 109.99`, `312452 Claw hammer 9.95`, …) and the vendor names (`Bryson Inc.`, `SuperLoo Inc.`, `Rubicon Systems`, `Fullerton Supply`) are named in the surviving prose; **the vendor area codes, the `SUPPLIER` table, and the entire `SUPPLIES`/`PART` data used for DIVIDE are my own**, since the prose does not determine them. Nothing in the argument depends on the particular values.
>
> **No error was found in Coronel & Morris ch. 3.**
>
> **Additions beyond the source — this chapter is heavily enriched, as the subject file anticipated.** **Coronel & Morris treats relational algebra as vocabulary**: it names the operators and shows a figure for each, but does not develop the algebra as a system. Mine adds:
>
> - **Every operator executed in SQL** (§4), with the algebra-to-SQL correspondence made explicit — including that **DIFFERENCE is `EXCEPT`**, which the book never says.
> - **The identity $R \bowtie S = \pi(\sigma(R \times S))$, verified by computing both sides and checking they are identical** — and the two consequences drawn from it (runaway Cartesian products; why the join is what optimisation targets). **The book states the definition but never exploits it.**
> - **The bag-versus-set distinction** (§4.2). **The book does not mention that SQL departs from the relational model here**, yet it is the source of the commonest aggregate bug.
> - **The inner-join row-loss demonstration** (§4.7) and the practice of counting before and after — mine, and the most immediately useful thing in the chapter.
> - **DIVIDE explained through quantifier negation** $\forall x P(x) \equiv \neg\exists x \neg P(x)$, linked to [[Discrete Mathematics/contents/01 - Sets and Logic|DM ch. 01]], **with both the `NOT EXISTS` and counting implementations executed and compared**, and the conditions under which the counting shortcut is valid. The book gives DIVIDE a figure and no SQL at all.
> - **The closure discussion** (§5) and the point that closure is what licenses algebraic rewriting by the optimiser — an addition, and the bridge to [[09 - Query Optimization and Indexing|ch. 09]].
> - **The key-hierarchy test** (§2), which checks minimality programmatically rather than asserting which sets are candidate keys.
> - **The SQLite entity-integrity findings** (§3) are entirely my own and are not in any textbook: that `TEXT PRIMARY KEY` accepts **multiple nulls**, that `INTEGER PRIMARY KEY` **auto-assigns** even under `NOT NULL`, and that `STRICT` tables fix it. Found by testing, not by reading — and it produced a phantom vendor row inside this chapter's own demonstration.
> - **Cross-links to [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]] and [[Data Structures and Algorithms/contents/11 - Sorting and Selection|ch. 11]]** for the actual join algorithms (hash join, sort-merge join), per the boundary recorded in `00-Index.md`.
>
> **Deliberately compressed.** **Codd's 12 rules** (C&M §3-8) are omitted — they are of historical interest and no chapter here depends on them. **The data dictionary and system catalog** (§3-5) are mentioned only via [[01 - Databases and Data Models|ch. 01]]'s metadata discussion. **§3-7 on indexes** is deferred entirely to [[09 - Query Optimization and Indexing|ch. 09]], where the [[Data Structures and Algorithms/contents/10 - Search Trees|B-tree]] machinery makes it explicable rather than assertable. **§3-6's relationship-in-the-relational-database walkthrough** is condensed into §6. **Outer-join variants** are tabulated rather than each demonstrated; only the `LEFT JOIN` case is executed, because it is the one that matters for detecting lost rows.

**Previous:** [[01 - Databases and Data Models]] · **Next:** [[03 - Entity-Relationship Modelling]]
