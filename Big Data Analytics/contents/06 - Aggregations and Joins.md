---
subject: Big Data Analytics
chapter: 6
tags: [ds, spark, aggregation, window-functions, rollup, cube, joins, broadcast-join]
source: "Chambers & Zaharia, Spark: The Definitive Guide, ch. 7–8"
---

# Aggregations and Joins

## 📘 Main Knowledge

### 1. Aggregation functions

An aggregation groups rows by a key and applies a function that returns one value per group. DG's retail dataset (541,909 rows) is used for the examples.

| Function | DG result | Note |
|---|---|---|
| `count("StockCode")` | 541,909 | `count("*")`/`count(1)` counts all rows including nulls; `count(col)` skips nulls |
| `countDistinct("StockCode")` | 4,070 | exact; needs a shuffle of distinct values |
| `approx_count_distinct("StockCode", 0.1)` | 3,364 | HyperLogLog sketch; much cheaper on big data |
| `first`, `last` | 85123A, 22138 | by row order, which is not guaranteed after shuffles |
| `min`, `max` of Quantity | −80,995, 80,995 | |
| `sum`, `sumDistinct`, `avg`/`mean` | | |
| `var_samp`/`variance`, `stddev_samp`/`stddev` | | **sample** versions are the default |
| `var_pop`, `stddev_pop` | | population versions |
| `skewness`, `kurtosis`, `corr`, `covar_samp`, `covar_pop` | | |
| `collect_list`, `collect_set` | | aggregate into arrays (watch memory) |

The second argument of `approx_count_distinct` is the maximum **relative standard deviation** (rsd), not a hard error bound: DG's own result is $(4070-3364)/4070=17.3\%$ off with rsd 0.1.

Aggregating over the whole DataFrame: `df.select(sum("Quantity"))` or `df.agg(...)`.

### 2. groupBy

```python
from pyspark.sql.functions import count, expr
df.groupBy("InvoiceNo", "CustomerId").count()
df.groupBy("InvoiceNo").agg(count("Quantity").alias("quan"), expr("count(Quantity)"))
df.groupBy("InvoiceNo").agg({"Quantity": "avg", "UnitPrice": "stddev_pop"})
```

`groupBy` returns a `RelationalGroupedDataset`; you must call an aggregation to get a DataFrame. Spark aggregates in two phases: a partial aggregate per partition, a shuffle by key, then the final aggregate (as in [[03 - Spark Architecture and Execution]]).

### 3. Window functions

A group-by puts each row in exactly one group and returns one row per group. A **window function** returns a value for **every** row, computed over a **frame** of related rows; one row can belong to many frames (a 7-day rolling average puts each day in 7 frames).

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import desc, max, dense_rank, rank
windowSpec = Window.partitionBy("CustomerId", "date") \
    .orderBy(desc("Quantity")) \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
maxPurchaseQuantity = max(col("Quantity")).over(windowSpec)
purchaseDenseRank = dense_rank().over(windowSpec)
purchaseRank = rank().over(windowSpec)
```

A window spec has three parts: **partitionBy** (which rows belong together), **orderBy** (order inside a partition), and the **frame** (`rowsBetween` by row offsets, or `rangeBetween` by value range).

Kinds of window functions:
- **ranking**: `row_number`, `rank` (gaps after ties), `dense_rank` (no gaps), `percent_rank`, `ntile`;
- **analytic**: `lag`, `lead`, `cume_dist`, `first`, `last`;
- **aggregate**: `sum`, `avg`, `max`, … `.over(window)` for running totals and moving averages.

In SQL: `rank() OVER (PARTITION BY CustomerId, date ORDER BY Quantity DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.

### 4. Grouping sets, rollup, cube, pivot

- **Grouping sets** (SQL only): `GROUP BY customerId, stockCode GROUPING SETS((customerId, stockCode), ())` computes several groupings in one query. Remove nulls first, because null also marks the subtotal rows.
- **Rollup**: hierarchical subtotals. `rollup("Date", "Country")` gives (Date, Country), (Date) and the grand total (null, null) = 5,176,450 in DG's data.
- **Cube**: subtotals for every combination of the dimensions: (Date, Country), (Date), (Country) and the grand total.
- **`grouping_id()`** tells which level a row belongs to (0 = most detailed, larger = more aggregated), so you can separate real nulls from subtotal rows.
- **Pivot** turns values of a column into columns: `groupBy("date").pivot("Country").sum()` creates columns like `USA_sum(Quantity)`. Useful only for low-cardinality columns; pass the list of values (`pivot("Country", ["USA", "France"])`) to avoid an extra job that finds them.

User-defined aggregation functions (UDAFs) exist in Scala/Java.

### 5. Join types

DG's example data:

| person (id, name, graduate_program) | graduateProgram (id, degree, department) |
|---|---|
| 0, Bill Chambers, 0 | 0, Masters, School of Information |
| 1, Matei Zaharia, 1 | 2, Masters, EECS |
| 2, Michael Armbrust, 1 | 1, Ph.D., EECS |

```python
joinExpression = person["graduate_program"] == graduateProgram["id"]
person.join(graduateProgram, joinExpression, "inner")
```

| Type (`joinType`) | Keeps |
|---|---|
| `inner` (default) | rows whose keys match on both sides |
| `outer` / `full_outer` | all rows from both sides, nulls where no match |
| `left_outer` | all rows from the left |
| `right_outer` | all rows from the right |
| `left_semi` | left rows that have a match on the right; only left columns, no duplication (a filter, like `EXISTS`) |
| `left_anti` | left rows with **no** match on the right (like `NOT EXISTS`) |
| natural | joins on same-named columns implicitly (risky) |
| `cross` | every left row with every right row ($n\times m$) |

Join expressions can be any Boolean expression, including on complex types: `expr("array_contains(spark_status, id)")`.

**Duplicate column names.** If both sides have a column with the same name, selecting it raises `Reference 'graduate_program' is ambiguous`. Fixes: join on a column-name string or list (`df1.join(df2, "graduate_program")`, which keeps one copy), drop the duplicate after the join, or rename before joining.

### 6. How Spark executes joins

Two decisions: how data moves between nodes, and how each node computes the join.

| Situation | Strategy |
|---|---|
| big ⨝ big | **shuffle join**: both sides are repartitioned by the join key so matching keys meet; all-to-all network traffic |
| big ⨝ small (small fits in an executor's memory) | **broadcast join**: the small table is copied to every executor once; the big table is joined in place with no shuffle |
| small ⨝ small | let Spark decide |

Per node, Spark uses a **sort-merge join** (sort both sides by key, then merge) for big tables, or a **broadcast hash join** (build a hash table of the small side) when broadcasting.

- Spark broadcasts automatically when a table's estimated size is below `spark.sql.autoBroadcastJoinThreshold` (10 MB by default; a standard default, not printed in DG). Force it with a hint: `big.join(broadcast(small), "key")` or `/*+ BROADCAST(t) */` in SQL.
- Too large a broadcast can run the driver or executors out of memory.
- If both sides are already partitioned the same way on the join key (e.g. bucketed tables, [[07 - Data Sources and File Formats]]), the shuffle can be skipped.
- Joins that filter (inner, semi) placed early reduce the data moved by later steps.
- **Skew**: if one key holds a large share of the rows, the task for that key is much slower than the others (see [[08 - Running, Monitoring and Tuning Spark]]).

## ✏️ Exercises

> [!example]- **1.** *(Easy) Join results*
> Using DG's `person` and `graduateProgram` with key `graduate_program = id`, how many rows (and which) does each return? (a) person inner graduateProgram; (b) graduateProgram left_outer person; (c) graduateProgram left_semi person; (d) graduateProgram left_anti person; (e) cross join.
>
> ---
> (a) 3: Bill–Masters/School of Information, Matei–Ph.D., Michael–Ph.D.
>
> (b) 4: program 0 with Bill, program 1 with Matei and with Michael, program 2 with nulls.
>
> (c) 2: programs 0 and 1, graduateProgram columns only; program 1 appears once even though two people match.
>
> (d) 1: program 2 (Masters, EECS), which nobody attended.
>
> (e) $3\times3=9$.

> [!example]- **2.** *(Easy–medium) Ranking functions*
> One customer's quantities ordered descending: 10, 10, 8, 5. Give `row_number`, `rank`, `dense_rank`, and a running `max` with frame (unboundedPreceding, currentRow).
>
> ---
> row_number 1, 2, 3, 4; rank 1, 1, 3, 4; dense_rank 1, 1, 2, 3; running max 10, 10, 10, 10. Use `dense_rank` when ties should not leave gaps (DG uses it for this reason). `row_number` breaks ties arbitrarily unless the ordering is unique.

> [!example]- **3.** *(Medium) Rollup vs cube size*
> Data has 2 dates and 3 countries, and every (date, country) pair occurs. How many rows do `rollup("Date", "Country").sum()` and `cube("Date", "Country").sum()` return? How do you tell subtotal rows from real null values?
>
> ---
> Rollup: 6 (date, country) + 2 (date) + 1 grand total = 9 rows. Cube adds 3 (country) rows: 12. Real nulls in Date or Country would look like subtotals; drop them first or use `grouping_id()` (0 for detail rows, higher for aggregated levels).

> [!example]- **4.** *(Medium–hard) Shuffle or broadcast?*
> A 1 TB fact table joins a 50 MB dimension table on 100 executors. Estimate data moved over the network for a shuffle join and for a broadcast join. When would broadcasting be a bad idea?
>
> ---
> Shuffle join: both sides are repartitioned by key, so roughly all 1 TB plus 50 MB cross the network (minus the fraction that happens to stay local).
>
> Broadcast: the 50 MB table is sent to each executor: $50\times100=5{,}000$ MB ≈ 4.9 GB, and the fact table does not move. About 200× less traffic, and no shuffle stage.
>
> Bad idea when the "small" table does not fit comfortably in executor (and driver) memory, or when it is not actually small after filtering estimates are wrong. Spark auto-broadcasts only under `spark.sql.autoBroadcastJoinThreshold` (10 MB default), so a 50 MB table needs a `broadcast()` hint or a higher threshold.

> [!example]- **5.** *(Hard) Write the query*
> From an `orders(customer_id, order_date, amount)` DataFrame, produce for each order: the customer's previous order amount, the running total of the customer's spending, and the order's rank within the customer by amount. Then keep each customer's top 2 orders.
>
> ---
> ```python
> from pyspark.sql.window import Window
> from pyspark.sql.functions import lag, sum, dense_rank, desc, col
> by_date = Window.partitionBy("customer_id").orderBy("order_date")
> running = by_date.rowsBetween(Window.unboundedPreceding, Window.currentRow)
> by_amount = Window.partitionBy("customer_id").orderBy(desc("amount"))
> result = (orders
>   .withColumn("prev_amount", lag("amount", 1).over(by_date))
>   .withColumn("running_total", sum("amount").over(running))
>   .withColumn("amount_rank", dense_rank().over(by_amount))
>   .where(col("amount_rank") <= 2))
> ```
> `lag` returns null for each customer's first order. Each distinct window spec may need its own sort; partitioning by `customer_id` shuffles once by that key. With ties, `dense_rank() <= 2` can return more than 2 rows per customer; use `row_number` for exactly 2.

## 📝 Summary

- Aggregations: `count` (column vs `*`), `countDistinct` vs `approx_count_distinct` (rsd, not a hard bound), min/max/sum/avg, sample vs population variance, `collect_list/set`.
- `groupBy(...).agg(...)`: partial aggregation per partition, shuffle, final aggregation.
- Window functions return a value per row over a frame: `partitionBy`, `orderBy`, `rowsBetween`/`rangeBetween`; ranking, analytic (`lag`, `lead`) and aggregate functions.
- Grouping sets, rollup (hierarchical), cube (all combinations), `grouping_id`, pivot.
- Join types: inner, full/left/right outer, left semi (filter), left anti (not exists), cross, natural.
- Shuffle join for big–big, broadcast join for big–small (auto below 10 MB or by hint); sort-merge vs broadcast hash join per node.
- Watch duplicate column names, skewed keys and oversized broadcasts.

## ⚠️ Important Notes

1. `count(col)` ignores nulls; `count("*")` does not.
2. `stddev`/`variance` are the sample versions.
3. `first`/`last` depend on row order, which is not deterministic after a shuffle.
4. Rollup and cube mark subtotals with null; real nulls in the data get mixed in.
5. `left_semi` never duplicates left rows; an inner join does when the right side has several matches.
6. Cross joins grow as $n\times m$; Spark refuses implicit cross joins unless enabled or written explicitly.
7. Selecting a column name present on both sides of a join is ambiguous; join on the column name to keep one copy.
8. A broadcast that is too big causes out-of-memory errors.
9. `collect_list` on a large group can exhaust executor memory.
10. A window without `partitionBy` moves all data into one partition.

> [!warning] Gaps in the source material
> - Figures (window frames, shuffle vs broadcast joins) are images; described in the text.
> - **Added by me:** the rsd interpretation and the 17.3% calculation; `autoBroadcastJoinThreshold` and its 10 MB default; `grouping_id` usage tip; pivot value list; all exercise numbers and the window-function query.
> - DG uses `drop()` for removing nulls before grouping sets; the intended call is `na.drop()` (`drop()` with no arguments drops no columns). Not filed as an erratum because the code still runs.

**Previous:** [[05 - DataFrames and Spark SQL]] · **Next:** [[07 - Data Sources and File Formats]]
