---
subject: Big Data Analytics
chapter: 4
tags: [ds, spark, rdd, pair-rdd, partitioning, caching, broadcast, accumulator]
source: "Karau et al., Learning Spark, ch. 3, 4, 6; Chambers & Zaharia, Spark: The Definitive Guide, ch. 12–14"
---

# RDDs, Key-Value Pairs and Shared Variables

RDDs are Spark's low-level API. DataFrames ([[05 - DataFrames and Spark SQL]]) compile down to RDDs and are usually faster, but RDDs explain how Spark works and are still used for unstructured data, custom partitioning and some MLlib internals (e.g. `computeSVD` on a `RowMatrix`).

## 📘 Main Knowledge

### 1. What an RDD is

A **Resilient Distributed Dataset** is an immutable, partitioned collection of objects that can be processed in parallel.

- **Partitioned**: split across the cluster.
- **Immutable**: transformations create new RDDs.
- **Resilient**: Spark records the **lineage graph** (how each RDD was derived) and recomputes lost partitions from it. LS: "the ability to always recompute an RDD is actually why RDDs are called 'resilient'."
- **Lazy**: like DataFrames, transformations only record what to do; actions trigger computation.

Unlike DataFrames, RDD elements are arbitrary Python/Java objects, so Spark cannot see inside them and cannot optimize the way Catalyst does for DataFrames. In Python, RDD functions also run in Python worker processes, which is slower.

Creating RDDs:
```python
lines = sc.textFile("README.md")          # from storage
nums  = sc.parallelize([1, 2, 3, 3])     # from a local collection
rdd   = df.rdd                            # from a DataFrame
```

### 2. Transformations and actions

On `{1, 2, 3, 3}` (LS tables 3-2 and 3-4):

| Transformation | Example | Result |
|---|---|---|
| `map` | `x + 1` | {2, 3, 4, 4} |
| `flatMap` | `x.to(3)` (range from x to 3) | {1, 2, 3, 2, 3, 3, 3} |
| `filter` | `x != 1` | {2, 3, 3} |
| `distinct` | | {1, 2, 3} (needs a shuffle) |
| `sample` | `sample(False, 0.5)` | random |

Two-RDD transformations on {1, 2, 3} and {3, 4, 5}: `union` → {1, 2, 3, 3, 4, 5} (keeps duplicates, no shuffle); `intersection` → {3}; `subtract` → {1, 2}; `cartesian` → all 9 pairs (very expensive).

| Action | Result on {1, 2, 3, 3} |
|---|---|
| `collect()` | all elements |
| `count()` | 4 |
| `countByValue()` | {1: 1, 2: 1, 3: 2} |
| `take(2)` / `top(2)` | {1, 2} / {3, 3} |
| `reduce(lambda x, y: x + y)` | 9 |
| `fold(0, add)` | 9 (zero value used once per partition, so it must be the identity) |
| `aggregate((0,0), seqOp, combOp)` | (9, 4), i.e. sum and count, so mean 2.25 |
| `foreach(f)` | runs `f` on executors, returns nothing |

`reduce` and `fold` need a function that is **associative and commutative**, because Spark combines partial results in any order. `aggregate` can return a different type from the elements: `seqOp` adds an element to a partition's accumulator, `combOp` merges accumulators.

**Passing functions.** Functions are serialized and shipped to executors. If you pass a method of an object, or refer to a field like `self.query`, Spark ships the whole object; copy the field into a local variable first.

### 3. Pair RDDs

RDDs of `(key, value)` tuples get key-based operations. Create them with `map`:
```python
pairs = lines.map(lambda x: (x.split(" ")[0], x))
```

On `{(1, 2), (3, 4), (3, 6)}` (LS tables 4-1, 4-3):

| Operation | Result |
|---|---|
| `reduceByKey(lambda x, y: x + y)` | {(1, 2), (3, 10)} |
| `groupByKey()` | {(1, [2]), (3, [4, 6])} |
| `mapValues(lambda x: x + 1)` | {(1, 3), (3, 5), (3, 7)} |
| `flatMapValues(lambda x: range(x, 6))` | {(1, 2), (1, 3), (1, 4), (1, 5), (3, 4), (3, 5)} |
| `keys()` / `values()` | {1, 3, 3} / {2, 4, 6} |
| `sortByKey()` | sorted by key |
| `countByKey()` (action) | {1: 1, 3: 2} |
| `collectAsMap()` (action) | {1: 2, 3: 6} in Python (one value per key kept) |
| `lookup(3)` (action) | [4, 6] |

With `other = {(3, 9)}`:

| Operation | Result |
|---|---|
| `join` | {(3, (4, 9)), (3, (6, 9))} |
| `leftOuterJoin` (keep all keys of `rdd`) | {(1, (2, None)), (3, (4, 9)), (3, (6, 9))} |
| `rightOuterJoin` (keep all keys of `other`) | {(3, (4, 9)), (3, (6, 9))} |
| `subtractByKey` | {(1, 2)} |
| `cogroup` | {(1, ([2], [])), (3, ([4, 6], [9]))} |

(LS's descriptions of left and right outer join are swapped; its example results are correct. See errata.)

### 4. Aggregating by key

- **`reduceByKey(f)`** combines values per key **within each partition first** (map-side combine), then shuffles only the partial results.
- **`groupByKey()`** shuffles **every** value and builds a full list per key in memory. `groupByKey().mapValues(sum)` gives the same answer as `reduceByKey(add)` but moves much more data and can run out of memory on a large key.
- **`combineByKey(createCombiner, mergeValue, mergeCombiners)`** is the general form; the result type can differ from the value type. Per-key average:

```python
sumCount = nums.combineByKey(
    lambda v: (v, 1),                                  # first value of a key in a partition
    lambda acc, v: (acc[0] + v, acc[1] + 1),           # add a value
    lambda a, b: (a[0] + b[0], a[1] + b[1]))           # merge partitions
avg = sumCount.mapValues(lambda sc: sc[0] / sc[1]).collectAsMap()
```

(LS writes `sumCount.map(lambda key, xy: ...)`, which fails because `map` passes one tuple; see errata.)

- `aggregateByKey(zero, seqOp, combOp)` and `foldByKey` are similar with a zero value.

Most per-key operations take an optional number of partitions: `reduceByKey(f, 10)`.

### 5. Partitioning

Communication is the expensive part of distributed programs. For pair RDDs you can control how keys are placed:

- `partitionBy(HashPartitioner(100))` hash-partitions by key (or `RangePartitioner` for sorted ranges); then **`persist()`** the result, otherwise the partitioning is redone each time.
- If a large RDD is partitioned and persisted, joining it with a small RDD shuffles **only the small one**. LS's example: a large `userData` table joined every five minutes with a small `events` log; without `partitionBy`, `userData` is re-hashed and shuffled on every join.
- Operations that set a partitioner on their output: `cogroup`, `join` and outer joins, `groupByKey`, `reduceByKey`, `combineByKey`, `partitionBy`, `sort`; `mapValues`, `flatMapValues` and `filter` keep the parent's partitioner.
- `map` **loses** the partitioner because it might change keys; use `mapValues` when keys stay the same.
- Partitioning helps only for data reused in key-based operations; for data scanned once it is wasted work.

**PageRank** (LS's example): each page starts at rank 1.0; each iteration a page sends `rank / number_of_links` to each page it links to, and each page's new rank is `0.15 + 0.85 × contributions received`. About 10 iterations are typical.

```scala
val links = sc.objectFile[(String, Seq[String])]("links")
              .partitionBy(new HashPartitioner(100)).persist()
var ranks = links.mapValues(v => 1.0)
for (i <- 0 until 10) {
  val contributions = links.join(ranks).flatMap {
    case (pageId, (links, rank)) => links.map(dest => (dest, rank / links.size)) }
  ranks = contributions.reduceByKey((x, y) => x + y).mapValues(v => 0.15 + 0.85*v)
}
```

`links` is large and static, so it is partitioned and persisted once; `mapValues` keeps `ranks` on the same partitioner, so each `join` needs no shuffle of `links`.

`repartition(n)` reshuffles everything; `coalesce(n)` only reduces partitions and avoids moving most data. Check the count with `rdd.getNumPartitions()`.

### 6. Persistence (caching)

Each action recomputes an RDD from its lineage unless it is persisted. `cache()` = `persist()` with the default level (`MEMORY_ONLY` for RDDs).

| Level | Space | CPU | In memory | On disk | Note |
|---|---|---|---|---|---|
| `MEMORY_ONLY` | high | low | yes | no | partitions that don't fit are recomputed |
| `MEMORY_ONLY_SER` | low | high | yes | no | serialized |
| `MEMORY_AND_DISK` | high | medium | some | some | spills to disk |
| `MEMORY_AND_DISK_SER` | low | high | some | some | serialized, spills |
| `DISK_ONLY` | low | high | no | yes | |

Add `_2` to replicate on two nodes. `persist` is lazy (data is stored at the first action). When memory fills, Spark evicts partitions using LRU; `unpersist()` removes data manually. (DataFrame `cache()` defaults to `MEMORY_AND_DISK`.)

**Checkpointing** (DG ch. 12) saves an RDD to reliable storage and cuts its lineage; useful when lineage gets very long, e.g. many iterations.

### 7. Shared variables

Normally each task gets its own copy of any variable it uses, and changes on executors never reach the driver.

**Broadcast variables**: a read-only value sent to each executor **once**, instead of with every task (e.g. a lookup table of country codes).
```python
lookup = sc.broadcast({"US": "United States", "VN": "Vietnam"})
rdd.map(lambda c: lookup.value.get(c, "unknown"))
```
Large broadcasts should use a fast serializer (Kryo). Broadcast joins in DataFrames use the same idea ([[06 - Aggregations and Joins]]).

**Accumulators**: write-only (from tasks) counters that the driver can read, e.g. counting blank or malformed lines.
```python
blank = sc.accumulator(0)
def extract(line):
    if line == "": blank.add(1)
    return line.split(" ")
words = lines.flatMap(extract)
words.count()            # an action must run before blank.value is meaningful
print(blank.value)
```

Fault tolerance caveat (LS): tasks can be re-run (failures, speculative execution, recomputing evicted cache). Spark applies each task's update **only once for accumulators used in actions** (e.g. `foreach`). Updates inside **transformations** can be counted more than once, so use them only for debugging there.

### 8. Per-partition operations

`mapPartitions(f)` calls `f` once per partition with an iterator, so expensive setup (a database connection, a parser, a random generator) happens once per partition instead of once per element. `foreachPartition` is the action version. `mapPartitionsWithIndex` also gives the partition number.

Numeric RDDs have `stats()`, `mean()`, `variance()`, `stdev()`, computed in one pass.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Predict the output*
> `rdd = sc.parallelize([1, 2, 3, 3])`. Give: (a) `rdd.map(lambda x: x * 2).collect()`; (b) `rdd.distinct().count()`; (c) `rdd.reduce(lambda a, b: a + b)`; (d) `rdd.aggregate((0, 0), lambda acc, x: (acc[0] + x, acc[1] + 1), lambda a, b: (a[0] + b[0], a[1] + b[1]))` and the mean.
>
> ---
> (a) [2, 4, 6, 6]. (b) 3. (c) 9. (d) (9, 4); mean $9/4=2.25$.

> [!example]- **2.** *(Easy–medium) Pair operations*
> `rdd = [(1, 2), (3, 4), (3, 6)]`, `other = [(3, 9)]`. Give `reduceByKey(add)`, `groupByKey().mapValues(list)`, `join`, `leftOuterJoin`, `rightOuterJoin`.
>
> ---
> `reduceByKey`: [(1, 2), (3, 10)]. `groupByKey`: [(1, [2]), (3, [4, 6])]. `join`: [(3, (4, 9)), (3, (6, 9))]. `leftOuterJoin`: [(1, (2, None)), (3, (4, 9)), (3, (6, 9))]. `rightOuterJoin`: [(3, (4, 9)), (3, (6, 9))] (every key of `other` is 3, which matches). Left keeps all keys of the left RDD, right keeps all keys of the right RDD.

> [!example]- **3.** *(Medium) Per-key average*
> Data `[("a", 3), ("b", 4), ("a", 1)]`. Compute the per-key average with `combineByKey`, tracing the accumulators, and explain why `reduceByKey(lambda x, y: (x + y) / 2)` is wrong.
>
> ---
> With all data in one partition: "a" → createCombiner(3) = (3, 1), then mergeValue((3, 1), 1) = (4, 2); "b" → (4, 1). Averages: a = 2.0, b = 4.0. Across partitions, mergeCombiners adds sums and counts.
>
> Averaging pairwise is not associative: for values 3, 1, 5 it gives $((3+1)/2+5)/2=3.5$ in one order and $(3+(1+5)/2)/2=3$ in another, while the true mean is 3. Carry (sum, count) and divide at the end.

> [!example]- **4.** *(Medium–hard) reduceByKey vs groupByKey*
> A word count over $10^9$ (word, 1) pairs has $10^5$ distinct words and 100 input partitions (assume each partition contains every word). How many records cross the network with each method?
>
> ---
> `groupByKey` shuffles every pair: $10^9$ records, and must hold each word's full list (the most common word may have hundreds of millions of 1s) in memory.
>
> `reduceByKey` first sums within each partition, so each partition sends at most one record per distinct word: at most $100\times10^5=10^7$ records, at least 100× fewer. Same result, far less network and memory.

> [!example]- **5.** *(Hard) PageRank by hand*
> Links: A → B, A → C, B → C, C → A. Using LS's update (start 1.0; new rank = 0.15 + 0.85 × received), compute two iterations. Then explain what happens in LS's code to a page with no incoming links.
>
> ---
> Iteration 1: A sends 0.5 to B and 0.5 to C; B sends 1 to C; C sends 1 to A. Received: A 1, B 0.5, C 1.5. Ranks: A $=0.15+0.85=1.0$, B $=0.15+0.425=0.575$, C $=0.15+1.275=1.425$.
>
> Iteration 2: A sends 0.5 to B and C; B sends 0.575 to C; C sends 1.425 to A. Ranks: A $=0.15+0.85\times1.425=1.36125$, B $=0.15+0.85\times0.5=0.575$, C $=0.15+0.85\times1.075=1.06375$.
>
> After many iterations: A ≈ 1.1634, B ≈ 0.6444, C ≈ 1.1922 (sum 3). C ranks highest because it receives links from two pages.
>
> A page with no incoming links receives no contribution, so after `reduceByKey` it has no row in `ranks`; on the next `join` it drops out and stops sending contributions. A full implementation adds such pages back with rank 0.15 (e.g. by outer-joining with all page IDs).

## 📝 Summary

- RDD: immutable, partitioned, lazily evaluated collection of objects; lineage makes it resilient.
- Transformations (`map`, `flatMap`, `filter`, `distinct`, `union`…) vs actions (`collect`, `count`, `reduce`, `aggregate`, `take`…). Reduce functions must be associative and commutative.
- Pair RDDs: `reduceByKey`, `groupByKey`, `combineByKey`, `mapValues`, joins, `cogroup`, `countByKey`, `lookup`.
- Prefer `reduceByKey`/`combineByKey` over `groupByKey` + reduce: map-side combining shuffles far less.
- `partitionBy` + `persist` on a large, reused pair RDD avoids reshuffling it in repeated joins; `mapValues` keeps the partitioner, `map` loses it.
- Persistence levels trade memory, CPU and disk; `cache()` is lazy; LRU eviction; checkpointing cuts lineage.
- Broadcast variables send read-only data once per executor; accumulators count from tasks, reliably only inside actions.
- `mapPartitions` does setup once per partition.

## ⚠️ Important Notes

1. Prefer DataFrames: RDD code (especially in Python) skips the Catalyst optimizer and is slower.
2. `groupByKey` on a skewed key can run an executor out of memory.
3. `map` on a partitioned pair RDD drops the partitioner; use `mapValues`.
4. `partitionBy` without `persist` repeats the shuffle every time the RDD is used.
5. `cache()` does nothing until an action runs.
6. Accumulator values are only reliable after an action, and only for updates made inside actions.
7. Changing a normal Python variable inside `map` does not change it on the driver.
8. `fold`'s zero value is applied once per partition, so a non-identity zero (e.g. 1 for a sum) gives wrong results.
9. `collectAsMap` keeps one value per key; duplicate keys are lost.
10. `cartesian` on large RDDs explodes in size ($n\times m$).
11. Referencing `self.field` in a function ships the whole object to executors.

> [!warning] Gaps in the source material
> - LS was written for Spark 1.x; examples are mostly Scala/Java. Python versions here are rewritten and checked for correctness.
> - **Errata in LS** (logged in [[00-Index]]): E1 left/right outer join descriptions swapped in Table 4-2; E2 Example 4-12's `lambda key, xy` fails; E3 Example 4-16's "custom parallelism" Scala line omits the `10`.
> - **Added by me:** the reduceByKey/groupByKey record counts, the PageRank hand calculation and the missing-page issue, the non-associative average counterexample, DataFrame `cache()`'s default level, and the remark about MLlib's `computeSVD`.
> - Figures (lineage graph, partitioned joins) are images; described in the text.

**Previous:** [[03 - Spark Architecture and Execution]] · **Next:** [[05 - DataFrames and Spark SQL]]
