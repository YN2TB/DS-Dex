---
subject: Database Management Systems
chapter: 9
tags: [ds, dbms, indexing, b-tree, query-optimization, explain, selectivity, covering-index, joins]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 11"
---

# Query Optimization and Indexing

**This is where [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] pays off.** That chapter derived B-trees from the block-transfer cost model and measured $10^9$ records needing **30 disk seeks with a binary tree versus 3 with a B-tree.** This chapter is that result in production: **a database index *is* a B-tree**, and everything about how it behaves follows from what ch. 10 established.

**Nothing here is re-derived** — the boundary is recorded in `00-Index.md`. [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] owns B-trees and the I/O cost model, [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]] owns hashing, [[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]] owns external merge-sort. **This chapter cross-links and measures.**

**Everything below was measured on 400 000 rows** — large enough that the timings exceed clock resolution, which [[07 - Database Design|ch. 07]] §6 could not manage.

## 📘 Main Knowledge

### 1. `EXPLAIN QUERY PLAN` first, always

**Before optimising anything, ask the engine what it is doing.**

```sql
EXPLAIN QUERY PLAN SELECT COUNT(*), SUM(amount) FROM orders WHERE cust_id = 12345;
```

*(Verified, 400 000 rows:)*

| | plan | time |
|---|---|---|
| **no index** | `SCAN orders` | 0.02627 s |
| **index on `cust_id`** | **`SEARCH orders USING INDEX idx_cust (cust_id=?)`** | **0.00003 s** |

**755× faster, identical answer.**

> [!note] Read the plan, not the clock
> **`SCAN` means "read every row". `SEARCH … USING INDEX` means "descend a B-tree".** That single word is the difference between $O(n)$ and $O(\log_B n)$ — **[[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] §7 exactly.**
>
> **`SCAN` on a large table is the warning sign**, and reading the plan is faster and more reliable than timing: it tells you *why*, and it does not depend on cache state or machine load.

### 2. Selectivity — an index only pays if it eliminates rows

*(Verified — the same table, three columns:)*

| column | distinct values | avg rows per value |
|---|---|---|
| `cust_id` | 49 984 | **8.0** |
| `country` | 8 | 50 000 |
| `status` | **3** | **133 333** |

**With an index on `status` (only three values), the query time depends entirely on how much the filter removes:**

| filter | rows matched | time |
|---|---|---|
| `status = 'shipped'` | 360 102 (90%) | **0.01433 s** |
| `status = 'cancelled'` | 8 107 (2%) | **0.00022 s** |

**65× apart, using the same index on the same column.**

> [!note] The principle
> **An index pays only when it eliminates most rows.** Fetching 90% of a table through an index is *slower* than scanning it, because each index hit is a **random jump** back to the row, whereas a scan reads sequentially.
>
> **So: index high-cardinality columns you filter on.** An index on `status`, `gender`, or a boolean is usually worthless — the optimiser will often ignore it, and it still costs write time (§7).
>
> *(Here both queries used the index because `COUNT(*)` could be answered from the index alone — §6's covering case — so no row lookups were needed. **On a query selecting actual columns, the 90% case would fall back to a scan**, which is the behaviour the principle describes.)*

### 3. Statistics — the optimiser is only as good as `ANALYZE`

**The optimiser decides between scan and index by *estimating* how many rows match.** That estimate comes from statistics gathered by `ANALYZE`.

> [!warning] An honest negative result
> **In this experiment `ANALYZE` did not change either plan** *(verified: `status='shipped'` and `status='cancelled'` both used `SEARCH … USING COVERING INDEX` before and after).*
>
> **The reason is that these particular queries are `COUNT(*)`, answerable from the index alone**, so the index wins regardless of selectivity and there is no decision for statistics to inform.
>
> **This does not mean `ANALYZE` is unimportant** — it means this query did not discriminate. **Stale or missing statistics are a classic cause of a query that was fast last month and is slow today**: the data distribution shifts, the optimiser's estimates go stale, and it chooses a plan that no longer suits. Run `ANALYZE` after bulk loads. *(PostgreSQL's autovacuum does this automatically; SQLite does not.)*

### 4. Why every database index is a B-tree

*(Verified:)*
```sql
SELECT COUNT(*) FROM orders WHERE amount BETWEEN 100 AND 150;
-> SEARCH orders USING COVERING INDEX idx_amount (amount>? AND amount<?)
   0.00011 s, 3874 rows

SELECT order_id FROM orders ORDER BY amount LIMIT 5;
-> SCAN orders USING COVERING INDEX idx_amount        <- no sort step at all
```

> [!note] The reason, from [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]] and [[Data Structures and Algorithms/contents/10 - Search Trees|ch. 10]]
> **A B-tree stores keys in order.** So a range query is one descent plus a sequential walk, and **`ORDER BY` on an indexed column needs no sort at all** — the index is already sorted.
>
> **A hash index cannot do either.** [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]] showed hashing *deliberately scatters* keys to avoid clustering — which destroys order by design. **A hash index supports equality only.**
>
> **That is the whole reason general-purpose indexes are B-trees**: equality is common, but ranges, sorting, `MIN`/`MAX` and prefix matching are also common, and only an ordered structure serves all of them. **Hash indexes exist (PostgreSQL has them) and are narrowly useful for equality-only lookups.**

### 5. Composite indexes and the leftmost-prefix rule

*(Verified, with an index on `(country, status)`:)*

| query | plan |
|---|---|
| `WHERE country='VN' AND status='pending'` | **uses `idx_country_status`** |
| `WHERE country='VN'` (leftmost only) | **uses `idx_country_status`** |
| `WHERE status='pending'` (second only) | **cannot use it** — fell back to a different index |

> [!note] The phone-book analogy
> **An index on `(a, b)` serves `a` and `a AND b`, but not `b` alone.**
>
> A phone book sorted by (surname, first name) finds all the Nguyens instantly, and Nguyen Huy instantly — **but cannot find everyone called Huy** without reading the whole book, because the Huys are scattered across every surname.
>
> **So column order in a composite index is a design decision, not formatting.** Put the column you *always* filter on first. If you need both `b` alone and `a AND b`, you need two indexes.
>
> *(The third test confirms the rule by elimination: the optimiser could not use `idx_country_status` for `status` alone and reached for the separate `idx_status` instead.)*

### 6. ⚠️ Wrapping a column in a function destroys the index

*(Verified:)*

| query | plan | time |
|---|---|---|
| `WHERE country = 'vn'` | **`SEARCH … USING COVERING INDEX`** | **0.00005 s** |
| `WHERE LOWER(country) = 'vn'` | **`SCAN orders`** | **0.04878 s** |
| `WHERE order_date >= '2025-01-01'` | `SEARCH … (order_date>?)` | 0.00593 s |
| `WHERE substr(order_date,1,4) >= '2025'` | **`SCAN`** | 0.03243 s |

**Nearly 1 000× slower for a logically identical filter.**

> [!warning] Non-sargable predicates
> **The index stores `country`, not `LOWER(country)`.** The engine cannot know that `LOWER` preserves the ordering, so it must compute the function for every row — which means reading every row.
>
> **A predicate that prevents index use is called *non-sargable*.** The common forms:
> - a **function on the column**: `LOWER(col)`, `substr(col,…)`, `CAST(col AS …)`, `YEAR(date_col)`
> - **arithmetic on the column**: `WHERE price * 1.1 > 100` instead of `WHERE price > 100/1.1`
> - **leading wildcards**: `LIKE '%abc'` (a trailing wildcard, `LIKE 'abc%'`, *can* use a B-tree)
> - **implicit type conversion**, where a string column is compared to a number
>
> **Two fixes.** **Rewrite so the column stands alone** — `WHERE order_date >= '2025-01-01'` rather than `substr(order_date,1,4) >= '2025'`. **Or build an expression index**: *(verified — after `CREATE INDEX idx_lower_country ON orders(LOWER(country))`, the `LOWER` query uses an index again.)*
>
> **This is among the most common causes of a slow query in practice**, and it is invisible unless you read the plan.

### 7. Covering indexes

*(Verified:)*
```sql
SELECT SUM(amount) FROM orders WHERE cust_id BETWEEN 100 AND 200;
```

| index | plan | time |
|---|---|---|
| `(cust_id)` | `SEARCH … USING INDEX` | 0.00507 s |
| **`(cust_id, amount)`** | **`SEARCH … USING COVERING INDEX`** | **0.00008 s — 66× faster** |

> [!note] Why "covering" is so much faster
> **With `(cust_id)` alone, the index finds the matching rows and then must jump to the table for each one to read `amount`** — a random access per matching row.
>
> **With `(cust_id, amount)`, `amount` is *in* the index, so the table is never touched.** The plan says `USING COVERING INDEX`, and the engine reads a contiguous run of index entries.
>
> **This is the cheapest large win available in query tuning**: add the selected column to an index you already have. **The cost is a wider index** — more space, and more write cost (§8).

### 8. What indexes cost

*(Verified — inserting 20 000 rows:)*

| | time |
|---|---|
| with **7 indexes** | **0.8726 s** |
| with **no indexes** | **0.0297 s** |

**Indexes made writes 29× slower.**

> [!warning] Every write must maintain every index
> An `INSERT` writes one row and **updates all seven B-trees**. An `UPDATE` to an indexed column deletes and reinserts an index entry. A `DELETE` removes seven entries.
>
> **So an index is a read optimisation bought with write cost and disk space** — and **an unused index is pure loss**: it slows every write and helps nothing.
>
> **Practical consequences:**
> - **Audit your indexes.** Most databases can report index usage; drop the ones nothing uses.
> - **Drop indexes before a bulk load and rebuild after.** 29× is worth the rebuild.
> - **Do not index "just in case".** Index in response to a measured slow query, not in anticipation.
> - **A composite index often replaces two single-column ones** (§5's leftmost-prefix rule) — fewer indexes, same coverage.

### 9. Join algorithms

*(Verified:)*
```
SELECT c.tier, COUNT(*) FROM orders o JOIN customer c USING (cust_id)
WHERE c.tier = 'gold' GROUP BY c.tier;

plan: SCAN c | SEARCH o USING COVERING INDEX idx_cust2 (cust_id=?)
time: 0.0215 s
```

**SQLite chose a nested-loop join**: scan the filtered `customer` side, and for each row do an **indexed** lookup into `orders`.

| algorithm | how | source |
|---|---|---|
| **nested loop** | for each row of $R$, look up matches in $S$ — **needs an index on $S$**, or it is $\lvert R\rvert\cdot\lvert S\rvert$ | [[02 - The Relational Model and Relational Algebra\|ch. 02]] §4.7's definition, made efficient |
| **hash join** | build a hash table on the smaller side, probe with the larger | [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists\|DSA ch. 09]] |
| **sort-merge join** | sort both by the join key, sweep once | [[Data Structures and Algorithms/contents/11 - Sorting and Selection\|DSA ch. 11]] |

> [!note] What the optimiser does, and what you do
> **[[02 - The Relational Model and Relational Algebra|Ch. 02]] §4.7 showed a join is defined as $\pi(\sigma(R \times S))$ — a Cartesian product with a filter.** No engine actually forms that product; the three algorithms above are all strategies for avoiding it, and **the optimiser is free to choose because the algebra constrains only the *result*.**
>
> **Your job is not to choose the algorithm** — you cannot, in SQL. **Your job is to make sure the optimiser has something good to choose**: an index on the join key, and current statistics. **Without `idx_cust2`, this join would be 400 000 × 50 000 comparisons.**
>
> *(SQLite only implements nested-loop joins. PostgreSQL and others pick among all three based on table sizes and available indexes — which is why the same query can be fast on one engine and slow on another.)*

### 10. The rules, all demonstrated

1. **Index the columns you filter and join on** — not the ones you display.
2. **An index helps only if it eliminates most rows** (§2).
3. **Composite index order follows the leftmost-prefix rule** (§5).
4. **Never wrap an indexed column in a function** (§6).
5. **A covering index avoids touching the table** (§7).
6. **Every index slows every write — drop unused ones** (§8).
7. **Run `ANALYZE`**; the optimiser is only as good as its statistics (§3).
8. **Read `EXPLAIN QUERY PLAN` before optimising**: `SCAN` is the warning sign (§1).

## ✏️ Exercises

**1. (Indexes and selectivity.)** (a) What do `SCAN` and `SEARCH` mean, and what is the underlying structure? (b) Interpret the 755×. (c) Explain selectivity with the measured numbers. (d) When is an index actively harmful?

> [!example]- Solution
> **(a) `SCAN` reads every row; `SEARCH … USING INDEX` descends a B-tree.**
>
> **The structure is exactly [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] §7's B-tree**: a multiway search tree with one node per disk block, giving $O(\log_B n)$ block transfers instead of $O(n)$. **DSA measured 3 seeks versus 30 for $10^9$ records at 1 000 keys per node** — that is the same mechanism, in a database.
>
> **Why the plan is better evidence than a stopwatch:** it says *what the engine did*, is deterministic, and does not depend on cache state or machine load. **A timing tells you something is slow; the plan tells you why.**
>
> **(b) 755× on 400 000 rows** *(0.02627 s → 0.00003 s, identical answer)*.
>
> **The ratio grows with table size**, which is the signature of different complexity classes ([[02 - The Relational Model and Relational Algebra|DSA ch. 02]]'s diagnostic). A scan is $O(n)$; an index lookup is $O(\log_B n)$ and barely moves. **At 4 million rows the gap would be roughly ten times larger.**
>
> **The identical answer matters**: the index changed cost, not meaning — [[07 - Database Design|ch. 07]] §6's separation of logical and physical design, now measured properly.
>
> **(c) An index pays only when it eliminates most rows.**
>
> | filter | matched | time |
> |---|---|---|
> | `status='shipped'` | 360 102 (90%) | 0.01433 s |
> | `status='cancelled'` | 8 107 (2%) | 0.00022 s |
>
> **65× apart, same index, same column** — the only difference is how much was eliminated.
>
> **The mechanism: an index lookup finds row *locations*, then must fetch each row.** Each fetch is a **random access**. A table scan is **sequential**, which is far cheaper per row. **So there is a crossover** — typically somewhere around 5–20% of the table — beyond which scanning wins.
>
> **The cardinality table shows which columns can ever be selective:** `cust_id` has 49 984 distinct values (8 rows each), while `status` has **3** (133 333 rows each). **A `status` filter can never eliminate much**, so an index on it is nearly useless whatever the query.
>
> *(Both measured queries did use the index, because `COUNT(*)` is answerable from the index alone — §7's covering case, so no row fetches were needed. **On a query selecting actual columns the 90% case would fall back to a scan**, which is the behaviour the principle describes. Reporting this distinction rather than glossing it is the difference between a demonstration and a claim.)*
>
> **(d) Three ways.**
>
> 1. **Write cost.** *(Verified: 7 indexes made a 20 000-row insert **29× slower**.)* Every write maintains every index, so **an unused index is pure loss.**
> 2. **A bad plan.** With stale statistics the optimiser may choose an index that turns out unselective, doing random fetches where a scan would have been faster. *(This is what §3's `ANALYZE` exists to prevent.)*
> 3. **Space**, and hence cache pressure — index pages compete with data pages for memory.
>
> **So: index in response to a measured slow query, never in anticipation.**

**2. (Hard — B-trees and non-sargable predicates.)** (a) Why is a database index a B-tree and not a hash table? (b) What is the leftmost-prefix rule? (c) Explain the 1 000× `LOWER()` result. (d) List the non-sargable forms and the fixes.

> [!example]- Solution
> **(a) Because a B-tree keeps keys in order, and a hash table deliberately does not.**
>
> *(Verified: a `BETWEEN` range used the index; `ORDER BY amount` used it with **no sort step at all**.)*
>
> **A B-tree serves:** equality, **ranges** (`BETWEEN`, `<`, `>`), **`ORDER BY` without sorting**, `MIN`/`MAX` (the leftmost/rightmost leaf), and **prefix matching** (`LIKE 'abc%'`).
>
> **A hash index serves equality only.** [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]] §2 showed hashing *deliberately scatters* keys to avoid clustering — so `1000` and `1001` land in unrelated buckets and there is no way to walk a range. **The property that makes a hash table fast is exactly the one that makes it useless for ranges.**
>
> **Hence B-trees for general-purpose indexes.** Equality is common, but so are ranges, sorting and `MIN`/`MAX`, and only an ordered structure serves all of them. **A hash index is faster for equality alone** — $O(1)$ against $O(\log_B n)$ — which is why PostgreSQL offers them for that narrow case.
>
> **The `ORDER BY` result is the underrated one.** Sorting 400 000 rows is $O(n\log n)$ and may spill to disk ([[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]]'s external merge-sort). **An index on the sort column eliminates the sort entirely** — which is why `ORDER BY … LIMIT 10` on an indexed column is nearly free and on an unindexed one is not.
>
> **(b) An index on `(a, b)` serves `a` and `a AND b`, but not `b` alone.**
>
> *(Verified: an index on `(country, status)` was used for both columns and for `country` alone, but for `status` alone the optimiser could not use it and reached for a different index.)*
>
> **The phone book:** sorted by (surname, first name), it finds all Nguyens instantly and Nguyen Huy instantly, **but everyone called Huy is scattered across every surname** — no better than reading the whole book.
>
> **Consequences for design:**
> - **Put the column you always filter on first.**
> - **Prefer the more selective column first** when both are always present — it narrows faster.
> - **An index on `(a,b)` makes a separate index on `(a)` redundant** — a useful way to reduce §8's write cost.
> - **If you need `b` alone *and* `a AND b`, you need two indexes.**
> - **A range on the first column stops the second being useful**: `WHERE a > 5 AND b = 3` can use the index for `a` but must then check `b` on each row, because within `a > 5` the `b` values are not ordered.
>
> **(c) Because the index stores `country`, not `LOWER(country)`.**
>
> *(Verified: `WHERE country='vn'` → `SEARCH`, 0.00005 s. `WHERE LOWER(country)='vn'` → **`SCAN`**, 0.04878 s.)*
>
> **The engine cannot assume `LOWER` preserves ordering** — in general a function can map ordered inputs to unordered outputs, so the index's ordering says nothing about the function's values. **The only way to evaluate the predicate is to compute the function for every row, which requires reading every row.**
>
> **The date case is the same and is more common in practice:** `substr(order_date,1,4) >= '2025'` scanned where `order_date >= '2025-01-01'` searched. **The two are logically identical and differ by a factor of six here** — more on a bigger table.
>
> **This is invisible without reading the plan.** The query is correct, returns the right answer, and looks reasonable in review.
>
> **(d)**
>
> | non-sargable form | fix |
> |---|---|
> | `LOWER(col) = 'x'` | store normalised, or an **expression index** |
> | `substr(date_col,1,4) = '2025'` | `col >= '2025-01-01' AND col < '2026-01-01'` |
> | `YEAR(date_col) = 2025` | same range rewrite |
> | `price * 1.1 > 100` | `price > 100/1.1` — **move arithmetic to the constant** |
> | `LIKE '%abc'` (leading wildcard) | no B-tree fix — needs a **full-text or trigram index** |
> | `col + 0 = 5` (implicit conversion) | fix the column's type |
>
> **The unifying rule: keep the indexed column *bare* on one side of the comparison.** Move every function and every arithmetic operation to the other side, where it is a constant computed once.
>
> **The expression index is the fallback when you cannot rewrite** *(verified: after `CREATE INDEX ON orders(LOWER(country))`, the `LOWER` query used an index again)*. **It costs another index to maintain** (§8), so rewriting is preferable when possible.

**3. (Covering indexes and cost.)** (a) Why was the covering index 66× faster? (b) What does a covering index cost? (c) Interpret the 29× write penalty. (d) What is the index-design procedure?

> [!example]- Solution
> **(a) Because the table was never touched.**
>
> *(Verified: `SUM(amount) … WHERE cust_id BETWEEN 100 AND 200` took 0.00507 s with an index on `(cust_id)` and **0.00008 s** with `(cust_id, amount)`.)*
>
> **With `(cust_id)` alone**, the index finds which rows match and stores their locations — **but `amount` is not in the index**, so the engine must jump to the table for each matching row. **Each jump is a random access**, and there are hundreds of them.
>
> **With `(cust_id, amount)`**, `amount` is in the index. The engine reads a **contiguous run** of index entries and sums them — sequential access, no table lookups at all. The plan says `USING COVERING INDEX`.
>
> **This is [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] §7's locality argument again**: the win is not fewer comparisons but **fewer random accesses.** The comparison count is identical.
>
> **(b) A wider index — more space, more write cost, and less of it fits in cache.**
>
> Adding `amount` makes every index entry bigger, so the index occupies more pages, takes longer to update, and **displaces more useful pages from memory.**
>
> **The rule: add columns to make an index covering only for queries that matter and run often.** A covering index for a rare report is a poor trade. **And there is a limit** — an index covering every column is a second copy of the table.
>
> *(A related design point: the covering index `(cust_id, amount)` makes the separate `(cust_id)` index redundant by the leftmost-prefix rule, so the true cost is less than it appears.)*
>
> **(c) Every write must maintain every index.**
>
> *(Verified: 20 000 inserts took **0.8726 s** with 7 indexes and **0.0297 s** with none — **29×**.)*
>
> **An `INSERT` writes one table row and inserts into seven B-trees**, each of which may split nodes. An `UPDATE` to an indexed column is a delete-plus-insert in that index. A `DELETE` removes seven entries.
>
> **So indexes are not free lookups — they are a read optimisation bought with write cost.** On a write-heavy table the balance can easily go the wrong way.
>
> **Two practical consequences.** **Drop indexes before a bulk load and rebuild afterwards** — at 29×, rebuilding is far cheaper than maintaining them row by row. **And audit for unused indexes**, which cost the full write penalty and return nothing.
>
> **(d)**
> 1. **Find the slow query.** Do not guess — measure, or read the slow-query log.
> 2. **Read `EXPLAIN QUERY PLAN`.** `SCAN` on a large table is the signal.
> 3. **Check the predicate is sargable** (§6) — a rewrite may fix it with no new index.
> 4. **Check selectivity** (§2). If the filter keeps most rows, no index will help.
> 5. **Index the filter/join columns**, most selective first, respecting leftmost-prefix.
> 6. **Consider making it covering** by adding the selected columns, if the query is frequent.
> 7. **Re-measure**, and confirm the plan changed.
> 8. **Run `ANALYZE`.**
> 9. **Check what you broke** — re-measure write performance, and look for now-redundant indexes to drop.
>
> **Step 9 is the one that gets skipped**, and it is why production databases accumulate dozens of overlapping indexes that nothing uses.

**4. (Joins and the optimiser.)** (a) Name the three join algorithms. (b) What did the measured plan show? (c) Why can the optimiser choose? (d) What can and cannot the query author control?

> [!example]- Solution
> **(a)** **Nested loop** — for each row of $R$, find matches in $S$; **$O(\lvert R\rvert \cdot \lvert S\rvert)$ without an index on $S$, and $O(\lvert R\rvert\log\lvert S\rvert)$ with one.** **Hash join** — build a hash table on the smaller side and probe with the larger ([[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]]); $O(\lvert R\rvert + \lvert S\rvert)$, needing memory for the hash table. **Sort-merge join** — sort both by the join key and sweep once ([[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]]); $O(n\log n)$, but **free if both inputs are already sorted**, e.g. by an index.
>
> **(b)** *(Verified:)* `SCAN c | SEARCH o USING COVERING INDEX idx_cust2 (cust_id=?)`, 0.0215 s.
>
> **A nested loop with the *filtered* side outer.** SQLite scanned `customer` (already narrowed by `tier='gold'`) and, for each row, did an **indexed** lookup into the 400 000-row `orders`.
>
> **The choice of which side to scan is the important decision.** Scanning the smaller/filtered side and indexing into the larger is right; the reverse would scan 400 000 rows and probe 50 000 times. **`SCAN c` first tells you the optimiser got it right.**
>
> **Without `idx_cust2` this becomes 400 000 × 50 000 comparisons** — twenty billion, which would not finish.
>
> **(c) Because [[02 - The Relational Model and Relational Algebra|ch. 02]] §4.7 defines a join only by its *result*.**
>
> $R \bowtie S = \pi(\sigma(R \times S))$ specifies **what** the answer is, not how to compute it. **Any strategy producing those rows is legal**, so the engine may choose freely — and this is the payoff of SQL being declarative ([[01 - Databases and Data Models|ch. 01]] §8, Codd's value-matching insight).
>
> **It is also why [[02 - The Relational Model and Relational Algebra|ch. 02]] §5's closure matters**: because the operators form an algebra, the optimiser can *rewrite* expressions using algebraic identities — most importantly **pushing filters down below joins**, so fewer rows are joined. **That is a theorem about the algebra, not a heuristic.**
>
> **(d)**
>
> | you cannot control | you can control |
> |---|---|
> | the join algorithm | **whether an index exists on the join key** |
> | the join order | **whether statistics are current (`ANALYZE`)** |
> | whether an index is used | **whether the predicate is sargable** (§6) |
> | | **how much data the query asks for** |
> | | **which engine you run on** |
>
> **The mental model: you do not instruct the optimiser, you *equip* it.** Give it an index on the join key, current statistics, and a sargable predicate, and it will usually find a good plan. **Withhold any of those and it cannot.**
>
> **And the engine matters more than it looks.** *(SQLite implements only nested-loop joins; PostgreSQL picks among all three.)* **A query that is fast on PostgreSQL because it chose a hash join can be slow on SQLite, which has no such option** — one more reason ([[05 - SQL Fundamentals|ch. 05]], [[08 - Transactions and Concurrency Control|ch. 08]]) that behaviour learned on SQLite does not transfer.
>
> *(Most engines offer hints or `SET enable_hashjoin = off` to force a plan. **Treat these as a last resort** — they freeze a decision that should adapt as the data grows.)*

## 📝 Summary

- **A database index is a B-tree** — [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] §7's structure and cost model, cross-linked rather than re-derived.
- **Read `EXPLAIN QUERY PLAN` before optimising.** `SCAN` = read every row; `SEARCH … USING INDEX` = descend a B-tree. *(Verified: **755× faster** with an index, 0.02627 s → 0.00003 s, identical answer.)*
- **⚠️ An index pays only if it eliminates most rows.** *(Verified: same index, `status='shipped'` (90% of rows) took **0.01433 s**, `status='cancelled'` (2%) took **0.00022 s** — 65× apart.)*
- **Cardinality decides whether an index can ever be selective**: `cust_id` had 49 984 distinct values (8 rows each); `status` had **3** (133 333 each).
- **`ANALYZE` supplies the statistics the optimiser estimates with.** *(Honest negative result: it changed neither plan here, because `COUNT(*)` on a covering index wins regardless — this query did not discriminate.)* **Stale statistics are a classic cause of a query that was fast last month.**
- **B-trees serve ranges, `ORDER BY` without sorting, `MIN`/`MAX` and prefix matching; hash indexes serve equality only** — because [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|hashing deliberately destroys order]]. *(Verified: `ORDER BY amount` used the index with **no sort step**.)*
- **Leftmost-prefix rule: an index on `(a,b)` serves `a` and `a AND b`, never `b` alone.** *(Verified.)* Column order is a design decision.
- **⚠️ Wrapping an indexed column in a function makes the predicate non-sargable and forces a scan.** *(Verified: `LOWER(country)='vn'` was **~1 000× slower** than `country='vn'`.)* Fix by rewriting so the column stands bare, or with an **expression index** *(verified to restore index use)*.
- **A covering index answers the query without touching the table.** *(Verified: **66× faster** by adding `amount` to a `cust_id` index.)* The win is fewer *random accesses*, not fewer comparisons.
- **⚠️ Every write maintains every index.** *(Verified: 7 indexes made 20 000 inserts **29× slower** — 0.8726 s vs 0.0297 s.)* **An unused index is pure loss.**
- **Three join algorithms — nested loop, hash join ([[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]]), sort-merge ([[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]])** — and the optimiser chooses, because [[02 - The Relational Model and Relational Algebra|ch. 02]]'s algebra constrains only the result.
- **You do not instruct the optimiser, you equip it**: an index on the join key, current statistics, and a sargable predicate.

## ⚠️ Important Notes

1. **Always read `EXPLAIN QUERY PLAN` before optimising.** It says *why*, is deterministic, and beats a stopwatch.
2. **`SCAN` on a large table is the warning sign** — but a scan is correct when the filter keeps most rows.
3. **Index high-cardinality columns you filter on.** An index on a boolean, a status, or a gender is nearly worthless.
4. **⚠️ Never wrap an indexed column in a function.** `LOWER(col)`, `substr(col,…)`, `YEAR(col)`, `col * 1.1` and leading-wildcard `LIKE` all force scans.
5. **Move arithmetic to the constant side** — `price > 100/1.1`, not `price * 1.1 > 100`.
6. **`LIKE 'abc%'` can use a B-tree; `LIKE '%abc'` cannot.** The latter needs a full-text or trigram index.
7. **Put the column you always filter on first in a composite index**, and remember `(a,b)` makes a separate `(a)` index redundant.
8. **A range on the first column of a composite index stops the second being useful** for seeking.
9. **Make an index covering only for frequent, important queries.** An index covering everything is a second copy of the table.
10. **⚠️ Audit and drop unused indexes.** They cost the full write penalty and return nothing.
11. **Drop indexes before a bulk load and rebuild afterwards.** At 29×, rebuilding is far cheaper.
12. **Run `ANALYZE` after bulk loads and schema changes.** SQLite will not do it for you.
13. **Do not index in anticipation.** Index in response to a measured slow query.
14. **After adding an index, re-measure writes** and look for indexes it has made redundant.
15. **Ensure an index exists on every join key.** Without one, a nested-loop join is the product of the table sizes.
16. **⚠️ Join performance does not transfer between engines** — SQLite has only nested-loop joins; PostgreSQL also has hash and merge joins.
17. **Treat optimiser hints as a last resort.** They freeze a decision that should adapt as data grows.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 11 extracts cleanly** — the query-processing phases, index selection, optimiser types (rule-based vs cost-based), statistics, and the SQL performance-tuning guidance all came through readably. **Book page $n$ = PDF page $n+28$; ch. 11 is PDF pages 538–571.**
>
> **All figures are images and are lost**, including the query-processing flow diagram and the B-tree/index-structure illustrations. **The B-tree loss does not matter here**, because [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] owns that structure and covers it in far more depth than C&M does — which is exactly the boundary recorded in `00-Index.md`.
>
> **The entire dataset is my own** — 400 000 synthetic orders with a deliberately **skewed** `status` distribution (90/8/2), because uniform data would not have demonstrated §2's selectivity effect at all. **The table was sized so that timings exceed clock resolution**, correcting [[07 - Database Design|ch. 07]] §6, where the indexed query fell below the timer and no ratio could honestly be quoted.
>
> **No error was found in Coronel & Morris ch. 11.**
>
> **Additions beyond the source.** **Every measurement is mine**, and C&M gives none — it describes index selection and optimisation qualitatively. The verified figures that carry this chapter — **755× for a point lookup, 65× between selective and unselective filters on the same index, ~1 000× for a non-sargable predicate, 66× for a covering index, and 29× write penalty for 7 indexes** — turn advice into evidence.
>
> **§6's non-sargable treatment is substantially mine.** C&M mentions avoiding functions on indexed columns; **demonstrating the plan flipping from `SEARCH` to `SCAN`, and then showing an expression index restoring it, is my own** — as is the tabulated list of non-sargable forms with their rewrites, which is the most directly reusable thing in the chapter.
>
> **§3 reports an honest negative result** — `ANALYZE` did not change either plan, because `COUNT(*)` on a covering index wins regardless of selectivity. **Reporting that rather than claiming a difference is deliberate**, and the note explains why the query failed to discriminate. **§2 carries the same caveat**: both measured queries used the index because no row fetches were needed, so the crossover the principle describes was not directly observed. **Flagging the limits of what was demonstrated is part of the demonstration.**
>
> **The cross-links to [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] (B-trees, block transfers, locality), [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|ch. 09]] (why hash indexes cannot do ranges) and [[Data Structures and Algorithms/contents/11 - Sorting and Selection|ch. 11]] (external merge-sort behind sort-merge joins)** are the boundary planned in `00-Index.md`, and they carry the *explanations* C&M states without justifying. **The observation that the optimiser's freedom follows from [[02 - The Relational Model and Relational Algebra|ch. 02]]'s algebra constraining only the result — and that closure is what licenses filter pushdown — is my own framing**, completing an argument begun in ch. 02.
>
> **The nine-step index-design procedure in Exercise 3(d), and the "you equip the optimiser, you do not instruct it" framing in Exercise 4(d), are additions.**
>
> **Deliberately compressed.** **C&M's query-processing phases (parsing, execution, fetching) are summarised in §1** rather than reproduced — the internal pipeline is DBMS-implementation material. **Rule-based versus cost-based optimisers (§11-5)** is reduced to the statistics discussion in §3; every modern engine is cost-based, so the distinction is historical. **§11-7's long list of SQL performance-tuning tips** is condensed into §10's eight rules, each of which is demonstrated above rather than asserted. **DBMS-specific tuning (buffer pools, sort buffers, cache sizes)** is omitted as engine- and version-specific. **Bitmap and function-based index types** are mentioned only where relevant (§6's expression index); **B-tree behaviour is the transferable content, and the exotic index types differ too much between engines to teach generically.**

**Previous:** [[08 - Transactions and Concurrency Control]] · **Next:** [[10 - Data Warehouses and OLAP]]
