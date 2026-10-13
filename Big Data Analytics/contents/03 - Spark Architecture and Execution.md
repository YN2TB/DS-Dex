---
subject: Big Data Analytics
chapter: 3
tags: [ds, spark, architecture, dag, lazy-evaluation, partitions, shuffle]
source: "Chambers & Zaharia, Spark: The Definitive Guide, ch. 2 and 15; Karau et al., Learning Spark, ch. 2 and 7"
---

# Spark Architecture and Execution

## 📘 Main Knowledge

### 1. Driver, executors, cluster manager

A **Spark application** is one driver process plus a set of executor processes.

| Component | Role |
|---|---|
| **Driver** | runs your `main()` / notebook code; keeps the application's state; turns your code into a plan and schedules tasks on executors |
| **Executors** | run the tasks the driver assigns and report status and results back; each application has its own executors |
| **Cluster manager** | owns the physical machines and grants resources to applications: Spark Standalone, YARN, Mesos (Kubernetes in later versions) |

The cluster manager has its own master/worker processes tied to machines; the driver and executors are processes of one application. Several applications can share a cluster.

**Execution modes** (DG ch. 15):

| Mode | Where the driver runs | Use |
|---|---|---|
| Cluster | on a worker node inside the cluster | production jobs via `spark-submit --deploy-mode cluster` |
| Client | on the submitting machine (a gateway/edge node) | interactive work; the client must stay alive |
| Local | everything on one machine, parallelism via threads | learning, testing |

**Life cycle of an application** (outside Spark): the client submits the application → the cluster manager starts the driver → the driver's SparkSession asks the cluster manager for executors → the driver schedules tasks, executors run them and exchange data → the driver exits and the cluster manager shuts the executors down.

### 2. SparkSession and SparkContext

- **SparkSession** (Spark 2.x) is the entry point; one per application. In `pyspark` shells it exists as `spark`; in scripts you create it:

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local").appName("Word Count") \
    .config("spark.some.config.option", "some-value").getOrCreate()
```

- **SparkContext** (`spark.sparkContext`, often `sc`) is the connection to the cluster used by the low-level APIs: RDDs, broadcast variables, accumulators. Spark 1.x used separate `SparkContext` and `SQLContext`/`HiveContext`; Spark 2 merged them into SparkSession.
- Python code runs in the driver; Spark translates DataFrame operations into JVM code on the executors. With the structured APIs all languages perform about the same.

### 3. DataFrames and partitions

A **DataFrame** is a distributed table with named, typed columns (its **schema**). Unlike pandas or R data frames it can span thousands of machines.

```python
myRange = spark.range(1000).toDF("number")
```

To work in parallel, Spark splits data into **partitions**: chunks of rows that live on one machine. Parallelism is limited by both partitions and executor cores:

- 1 partition and 1,000 executors → parallelism 1;
- 1,000 partitions and 1 executor core → parallelism 1.

With DataFrames you rarely manage partitions directly; you describe transformations and Spark decides the physical execution. When files are read, the number of partitions follows the file sizes and block size (~128 MB per partition).

### 4. Transformations and actions

Spark's core data structures are **immutable**. To "change" a DataFrame you write a **transformation**, which returns a new DataFrame:

```python
divisBy2 = myRange.where("number % 2 = 0")   # nothing runs yet
```

| | Narrow transformation | Wide transformation (shuffle) |
|---|---|---|
| dependency | each input partition feeds at most one output partition | input partitions feed many output partitions |
| examples | `select`, `filter`/`where`, `withColumn`, `map`, `union`, `coalesce` | `groupBy`, `join` (usually), `sort`/`orderBy`, `distinct`, `repartition` |
| execution | **pipelined** in memory within one stage | data is written to disk and sent across the network; starts a new stage |
| cost | cheap | expensive |

**Lazy evaluation**: transformations only build a plan (a DAG). Nothing runs until an **action**. This lets Spark optimize the whole plan, e.g. **predicate pushdown**: a filter written at the end is applied when reading the source.

**Actions** trigger computation. Three kinds (DG): view data (`show`, `take`), collect to native objects (`collect`, `count`, `first`), write to storage (`write...save`).

```python
divisBy2.count()   # 500
```

`collect()` brings every row to the driver; on large data it can crash the driver. Use `take(n)` or `show()` to inspect.

### 5. Reading a plan with `explain`

DG's flight-data example:

```python
flightData2015 = spark.read.option("inferSchema", "true") \
    .option("header", "true").csv("/data/flight-data/csv/2015-summary.csv")
flightData2015.sort("count").explain()
```
```
== Physical Plan ==
*Sort [count#195 ASC NULLS FIRST], true, 0
+- Exchange rangepartitioning(count#195 ASC NULLS FIRST, 200)
   +- *FileScan csv [...]
```

Read plans bottom to top (source at the bottom). `Exchange` is a shuffle. The default number of shuffle output partitions is **`spark.sql.shuffle.partitions` = 200**; on a laptop set it lower:

```python
spark.conf.set("spark.sql.shuffle.partitions", "5")
```

**SQL and DataFrames compile to the same plan.** After `createOrReplaceTempView("flight_data_2015")`, `spark.sql("SELECT DEST_COUNTRY_NAME, count(1) ... GROUP BY ...")` and `groupBy("DEST_COUNTRY_NAME").count()` give identical physical plans, with the aggregation done in two phases: `partial_count` per partition, an `Exchange hashpartitioning`, then the final count. There is no performance difference between the two styles.

The plan is a **lineage**: Spark can recompute any lost partition by re-running the same transformations on the same input. This is how Spark achieves fault tolerance without replicating intermediate data.

### 6. Jobs, stages, tasks

| Level | Created by | Notes |
|---|---|---|
| **Job** | one action | jobs in an application run one after another unless you launch actions from several threads |
| **Stage** | a group of tasks between shuffles | a new stage starts after each shuffle |
| **Task** | one partition + the pipelined transformations for it | runs on one executor core; #tasks in a stage = #partitions |

DG's example:

```python
df1 = spark.range(2, 10000000, 2)
df2 = spark.range(2, 10000000, 4)
step1 = df1.repartition(5)
step12 = df2.repartition(6)
step2 = step1.selectExpr("id * 5 as id")
step3 = step2.join(step12, ["id"])
step4 = step3.selectExpr("sum(id)")
step4.collect()   # 2500000000000
```

One action → one job with 6 stages:

| Stage | Tasks | Why |
|---|---|---|
| 1 | 8 | `range` creates 8 partitions (df1) |
| 2 | 8 | same for df2 |
| 3 | 6 | after `repartition(6)` |
| 4 | 5 | after `repartition(5)` (the `* 5` is pipelined here) |
| 5 | 200 | the join's shuffle uses `spark.sql.shuffle.partitions` = 200 |
| 6 | 1 | the final sum is brought to a single partition |

Rule of thumb (DG): use more partitions than executor cores, by a few times; on a local machine use fewer than 200.

### 7. Pipelining and shuffle persistence

- **Pipelining**: consecutive narrow operations (map → filter → map, or select → filter → select) run inside one task, passing each record through all steps without writing intermediates. This is a main reason Spark is faster than MapReduce.
- **Shuffle persistence**: in a shuffle, map-side tasks write **shuffle files to local disk**; reduce-side tasks fetch them. This lets the next stage run later, lets Spark retry failed reduce tasks without redoing the map side, and lets later jobs reuse the shuffle output (shown as "skipped" stages in the Spark UI). For explicit reuse, use `cache()`/`persist()` ([[04 - RDDs, Key-Value Pairs and Shared Variables]]).

### 8. Spark UI

Each application's driver serves a web UI on **port 4040** (`http://localhost:4040` locally) showing jobs, stages, tasks, storage (cached data), environment and SQL plans. Used for monitoring and tuning ([[08 - Running, Monitoring and Tuning Spark]]).

## ✏️ Exercises

> [!example]- **1.** *(Easy) Narrow or wide?*
> Classify: `filter`, `select`, `withColumn`, `groupBy().sum()`, `join`, `orderBy`, `union`, `distinct`, `repartition(10)`, `coalesce(2)`.
>
> ---
> Narrow: `filter`, `select`, `withColumn`, `union`, `coalesce(2)` (merges partitions on the same executors without a full shuffle).
>
> Wide: `groupBy().sum()`, `join` (unless one side is broadcast, see [[06 - Aggregations and Joins]]), `orderBy`, `distinct`, `repartition(10)`.

> [!example]- **2.** *(Easy–medium) Parallelism*
> A cluster has 4 executors with 4 cores each. (a) How many tasks can run at once? (b) A stage has 200 tasks of equal length; how many "waves"? (c) A stage has 10 partitions; what fraction of the cores is idle? (d) What happens with 1 partition?
>
> ---
> (a) 16. (b) $\lceil200/16\rceil=13$ waves; the last wave has only 8 tasks. (c) 6 of 16 cores (37.5%) idle. (d) One task, one core: parallelism 1 regardless of cluster size. Repartition to at least 16 (better 32–64).

> [!example]- **3.** *(Medium) Count the stages*
> For DG's `step4` job above, explain the total number of tasks and which operations cause new stages.
>
> ---
> $8+8+6+5+200+1=228$ tasks in 6 stages. New stages start at each shuffle: the two `repartition` calls, the join (exchange on `id`, 200 partitions) and the final aggregation into a single partition. The `selectExpr("id * 5")` and the partial sums are pipelined into existing stages, so they add no stages.

> [!example]- **4.** *(Medium–hard) Check the answer*
> Show that `step4.collect()` returns 2,500,000,000,000 and find how many rows survive the join.
>
> ---
> `df1` holds the even numbers 2…9,999,998; after `* 5` the values are the multiples of 10 from 10 to 49,999,990. `df2` holds 2, 6, 10, … (numbers ≡ 2 mod 4) below $10^7$. A multiple of 10, $10k$, is ≡ 2 mod 4 exactly when $k$ is odd, and it must be below $10^7$: $10, 30, \dots, 9{,}999{,}990$, i.e. $k=1,3,\dots,999{,}999$: 500,000 rows. Sum $=10\,(1+3+\dots+999{,}999)=10\times500{,}000^2=2.5\times10^{12}$. (Checked by brute force in Python.)

> [!example]- **5.** *(Hard) Laziness and reuse*
> A pipeline reads a 100 GB CSV (reading takes 10 min), filters and adds columns, then runs `count()`, `show(20)` and `write.parquet(...)`. (a) How many jobs, and how many times is the CSV read without caching? (b) What changes with `df.cache()` before the actions? (c) Why might `show(20)` be fast even without caching?
>
> ---
> (a) Three actions → (at least) three jobs. Each recomputes from the source, so the CSV is read up to three times (about 30 min of reading). Schema inference (`inferSchema`) can add another pass.
>
> (b) `cache()` is lazy: the first action computes and stores the filtered DataFrame in executor memory (spilling to disk if needed); later actions read the cached data. Reading drops to about one 10-minute pass plus fast memory scans. Cache only data you reuse, and `unpersist()` when done.
>
> (c) `show(20)` only needs 20 rows, so Spark can stop after scanning the first partitions that produce them. Laziness lets the plan stop early; `count()` and `write` must touch every row.

## 📝 Summary

- An application = a driver (plans, schedules, keeps state) + executors (run tasks); a cluster manager (Standalone, YARN, Mesos) provides resources. Modes: cluster, client, local.
- SparkSession is the entry point; SparkContext is the low-level connection used for RDDs.
- DataFrames are split into partitions; parallelism = min(partitions, cores).
- Transformations are lazy and build a DAG; actions run it. Narrow transformations are pipelined; wide ones shuffle data via disk and network.
- One action = one job; stages are separated by shuffles; tasks = partitions. Shuffles default to 200 partitions (`spark.sql.shuffle.partitions`).
- SQL and DataFrame code compile to the same plan; `explain()` shows it.
- Lineage lets Spark recompute lost partitions; shuffle files on disk let it skip finished stages.
- The Spark UI is on port 4040.

## ⚠️ Important Notes

1. Transformations do nothing until an action runs; an error in a transformation often appears only at the action.
2. `collect()` on a large DataFrame can run the driver out of memory.
3. More executors do not help if there are fewer partitions than cores.
4. 200 shuffle partitions is a cluster default; it is too many for small data on a laptop and may be too few for terabytes.
5. `repartition` always shuffles; `coalesce` only reduces partitions and avoids a full shuffle.
6. Each action recomputes the plan from the source unless data is cached.
7. In client mode, closing the client machine kills the driver and the application.
8. DataFrames are immutable: `df.where(...)` without assigning the result changes nothing.
9. Python vs Scala performance is similar for DataFrame code, but Python UDFs are slower (data must move between the JVM and Python).
10. The number of jobs is not always exactly the number of actions: some operations (schema inference, sorting with range partitioning) launch extra jobs.

> [!warning] Gaps in the source material
> - DG figures (architecture, narrow/wide dependencies, cluster modes, Spark UI) are images; their content is described in the text.
> - **Added by me:** the narrow/wide table entries for `union`, `coalesce`, `distinct`; Kubernetes as a cluster manager (added in Spark 2.3, after DG's 2.2); the ~128 MB partition size for files (DG ch. 9/19 discusses this); all exercises and the derivation of 2.5×10¹² (DG gives only the result).
> - LS ch. 7 covers the same runtime architecture in RDD-era terms; DG's version is followed.

**Previous:** [[02 - Data Architectures]] · **Next:** [[04 - RDDs, Key-Value Pairs and Shared Variables]]
