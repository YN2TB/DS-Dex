---
subject: Big Data Analytics
chapter: 8
tags: [ds, spark, spark-submit, configuration, spark-ui, tuning, skew, memory]
source: "Chambers & Zaharia, Spark: The Definitive Guide, ch. 16–19; Karau et al., Learning Spark, ch. 7–8"
---

# Running, Monitoring and Tuning Spark

## 📘 Main Knowledge

### 1. Submitting applications

```bash
./bin/spark-submit \
  --master yarn --deploy-mode cluster \
  --num-executors 10 --executor-cores 4 --executor-memory 8g \
  --driver-memory 4g \
  --conf spark.sql.shuffle.partitions=120 \
  --py-files deps.zip \
  my_job.py arg1
```

Key options (DG Table 16-1/16-2):

| Option | Meaning |
|---|---|
| `--master` | `local[n]`, `spark://host:port` (standalone), `yarn`, `mesos://…` (later `k8s://…`) |
| `--deploy-mode` | `client` (default) or `cluster` |
| `--class` | main class (Scala/Java) |
| `--jars`, `--packages` | extra JARs / Maven coordinates (e.g. a JDBC driver, the Kafka connector) |
| `--py-files`, `--files` | Python dependencies, other files |
| `--num-executors` (YARN, default 2) | number of executors |
| `--executor-cores` | cores per executor (YARN default 1; standalone: all cores of the worker) |
| `--executor-memory`, `--driver-memory` | memory per executor / for the driver (default 1g each) |
| `--total-executor-cores` | total cores (standalone/Mesos) |

`local[*]` uses all local cores; `local[2]` two threads.

### 2. Configuration

Three places: **Spark properties** (SparkConf, `--conf`, `spark-defaults.conf`), environment variables (`conf/spark-env.sh`, per machine) and logging (`log4j.properties`). Precedence: values set in code > `spark-submit` flags > defaults file.

```python
from pyspark import SparkConf
conf = SparkConf().setMaster("local[2]").setAppName("DefinitiveGuide").set("some.conf", "to.some.value")
```

Useful properties (DG Table 16-3 and others):

| Property | Default | Note |
|---|---|---|
| `spark.driver.memory` | 1g | in client mode set it on the command line; the driver JVM has already started when your code runs |
| `spark.driver.maxResultSize` | 1g | limit on results returned to the driver (`collect`); protects it from OOM |
| `spark.executor.memory` | 1g | |
| `spark.sql.shuffle.partitions` | 200 | partitions after DataFrame shuffles |
| `spark.default.parallelism` | depends on cluster | partitions for RDD shuffles |
| `spark.serializer` | Java serializer | set to `KryoSerializer` for RDD-heavy code |
| `spark.dynamicAllocation.enabled` | false | add/remove executors with the workload |
| `spark.scheduler.mode` | FIFO | `FAIR` shares resources between concurrent jobs |
| `spark.speculation` | false | re-launch very slow tasks on other nodes |

**Scheduling.** Between applications, the cluster manager divides resources (static partitioning, or dynamic allocation). Within an application, jobs from different threads run FIFO by default; the FAIR scheduler assigns tasks round-robin so short jobs are not stuck behind long ones, with pools and weights.

**Deployment** (DG ch. 17): on-premises clusters are fixed in size and you run your own storage; cloud clusters are elastic and separate storage (S3, ADLS, GCS) from compute, which fits Spark's "compute only" design.

### 3. Monitoring

Monitor the **processes** (driver and executor CPU, memory, GC; Spark's metrics system exports to tools like Ganglia) and the **query execution** (jobs, stages, tasks).

**Spark UI** (port 4040; next applications use 4041, 4042, …):

| Tab | Shows |
|---|---|
| Jobs | each action, its stages, duration |
| Stages | tasks with duration, input/shuffle read/write sizes, GC time; summary quantiles reveal skew |
| Storage | cached DataFrames/RDDs and their size in memory/disk |
| Environment | configuration in effect |
| Executors | per-executor memory, cores, tasks, failures, logs |
| SQL | the query plan of each DataFrame/SQL query with metrics per operator |

After an application ends its UI disappears; enable event logging (`spark.eventLog.enabled`) and use the **Spark History Server** to view it later. Driver and executor **logs** are the other main source (via the cluster manager).

### 4. First aid: symptoms and treatments (DG ch. 18)

| Symptom | Likely cause | Treatment |
|---|---|---|
| job never starts; UI shows only the driver | resources requested exceed what the cluster has; network/firewall problems | request fewer/smaller executors; check ports and cluster config |
| errors before execution | bad code: missing column, wrong path | read the analysis error; check the plan |
| a few tasks run much longer than the rest (**stragglers**) | **data skew** (one key or partition much bigger) or a bad node | more partitions, repartition on another column, salt the hot key, filter early, speculation for bad nodes |
| slow `groupBy` | skewed keys, too few partitions | repartition before aggregating, filter and select first, use null (not "" or "EMPTY") for missing keys |
| slow join | shuffle of big tables, skew | broadcast the small side, join after filtering, pre-partition/bucket, check join order |
| slow reads/writes | many small files, unsplittable files, eventually consistent storage | fix file layout ([[07 - Data Sources and File Formats]]); speculation (careful: non-idempotent writes can duplicate output) |
| **driver** OutOfMemoryError | `collect()` of large data, broadcasting too much, many objects in the driver, Python–JVM conversion | avoid collecting, lower broadcast threshold, raise `spark.driver.memory` |
| **executor** OutOfMemoryError | too much data per task, skew, UDFs creating many objects | more partitions, more executor memory, fewer UDFs, check GC logs |
| nulls in unexpected places | malformed input in permissive mode, failed parsing | validate input; count nulls |
| "no space left on device" | shuffle/spill files fill local disks | more disk, more nodes, fewer data in the shuffle |
| serialization errors | function captures something that can't be serialized | don't reference non-serializable objects in UDFs/closures |

### 5. Performance tuning (DG ch. 19)

DG's priorities: (1) **read as little data as possible** (partitioning, efficient binary formats, early filters); (2) **enough parallelism and no skew**; (3) **use the structured APIs**. Use the Spark UI to find the slowest stages first.

**Indirect (design) choices**
- Use DataFrames/SQL rather than RDDs; their speed is the same across languages. Avoid Python UDFs.
- Store data as Parquet, partitioned and bucketed on common filter/join columns, with reasonable file sizes.
- Use Kryo serialization for RDDs of custom objects (register the classes).
- Size the cluster and use dynamic allocation when sharing resources.
- Keep statistics for the cost-based optimizer (`ANALYZE TABLE ... COMPUTE STATISTICS`).

**Direct choices**
- **Parallelism**: at least 2–3 tasks per CPU core for large stages (`spark.default.parallelism`, `spark.sql.shuffle.partitions`).
- **Filter early**, ideally pushed into the source.
- **Repartition vs coalesce**: `coalesce` to reduce partitions without a shuffle; `repartition` to rebalance (before joins or caching).
- **Caching** only data reused several times; caching has serialization and storage costs. Pick a storage level; `unpersist` when done. DataFrames are cached in Spark's compact columnar format, RDDs as objects.
- **Joins**: broadcast small tables, filter before joining, join on bucketed tables, avoid cartesian products.
- **Aggregations**: prefer built-in aggregations (they combine map-side) over `groupByKey`-style code.
- **Broadcast variables** for lookup tables or models used in many tasks.
- **GC tuning**: the JVM heap has a Young generation (Eden + two Survivor spaces) for short-lived objects and an Old generation for long-lived ones. Frequent full GCs mean too many objects; aim to keep only cached data in Old and give Young enough space.

**Memory inside an executor** (added; Spark 1.6+ unified memory): after a reserved ~300 MB, a fraction (`spark.memory.fraction`, 0.6) is shared between **execution** (shuffles, joins, sorts, aggregations) and **storage** (cache, broadcasts), with `spark.memory.storageFraction` (0.5) protected for storage; the rest is user memory. YARN also adds memory overhead per executor (default max(384 MB, 10%)).

**Skew and salting** (added technique): if one key dominates, append a random "salt" (0…k−1) to it, aggregate by (key, salt), then aggregate again by key. In Spark 3, adaptive query execution can split skewed join partitions automatically.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Read a submit command*
> `spark-submit --master yarn --deploy-mode cluster --num-executors 10 --executor-cores 4 --executor-memory 8g job.py`. Where does the driver run? How many tasks can run at once? What range of shuffle partitions does DG's rule suggest?
>
> ---
> Cluster mode: the driver runs inside the cluster on a node chosen by YARN. $10\times4=40$ concurrent tasks. At 2–3 tasks per core: 80–120 shuffle partitions (instead of the default 200, which is fine too for large data).

> [!example]- **2.** *(Easy–medium) Diagnose*
> Match each symptom to a cause and fix: (a) the job crashes right after `df.collect()` with an OutOfMemoryError in the driver log; (b) 199 of 200 tasks finish in 30 s, the last takes 25 min; (c) the UI shows the driver but no executors; (d) a stage writes 50,000 tiny files.
>
> ---
> (a) Too much data collected to the driver: use `take`, `show`, write to storage, or aggregate first; raise `spark.driver.maxResultSize`/memory only if the result is genuinely needed.
> (b) Skew: one partition/key has most of the data. Check the stage's task metrics; salt the key, repartition, or broadcast if it is a join.
> (c) Resources cannot be granted (requests too large, wrong queue, network); reduce executor size/count or fix the configuration.
> (d) Too many partitions at write time (often `partitionBy` without repartitioning); `repartition` by the partition column or `coalesce`, and set `maxRecordsPerFile`.

> [!example]- **3.** *(Medium) Size the executors*
> Each worker node has 16 cores and 64 GB RAM. Using the common heuristic (leave 1 core and 1 GB for the OS, 5 cores per executor, YARN overhead max(384 MB, 10%)), how many executors per node and how much `--executor-memory`?
>
> ---
> 15 usable cores / 5 = 3 executors per node. Memory per executor $=63/3=21$ GB including overhead; heap ≈ $21/1.1\approx19$ GB, so `--executor-memory 19g` (overhead ≈ 2 GB). This is a rule of thumb (added beyond DG): very large executors suffer long GC pauses, very small ones waste memory on overhead and reduce broadcast efficiency.

> [!example]- **4.** *(Medium–hard) Quantify skew*
> 100 GB is shuffled into 200 partitions, but one key holds 40% of the data. (a) How large is the hot partition compared with the others and with a balanced partition? (b) If you salt the hot key into 20 parts, how big is each piece?
>
> ---
> (a) Hot partition: 40 GB. The other 60 GB over 199 partitions ≈ 0.30 GB each. A balanced partition would be 0.5 GB, so the hot one is 80× that; the stage takes as long as that one task, and it may also run out of memory.
>
> (b) $40/20=2$ GB per salted piece, spread over 20 tasks. Aggregate by (key, salt), then combine the 20 partial results per key.

> [!example]- **5.** *(Hard) Tune a pipeline*
> A daily job reads 2 TB of CSV, joins it with a 30 MB country table and a 500 GB customer table, filters to one region, aggregates by customer, and writes the result. It runs for 3 hours. List the changes you would make, in priority order, and say what each saves.
>
> ---
> 1. **Convert input to Parquet**, partitioned by date (and maybe region): column pruning and partition pruning; no CSV parsing.
> 2. **Filter by region first**, before any join, ideally pushed into the scan: less data in every shuffle.
> 3. **Broadcast the 30 MB country table** (`broadcast()` hint; it is above the 10 MB default threshold): removes one shuffle of the large side.
> 4. **Customer join**: select only needed columns; if this join runs daily on the same key, bucket both tables by `customer_id` to avoid the shuffle; check for skewed customers.
> 5. **Set shuffle partitions** to match the cluster (2–3 per core) and the data size after filtering.
> 6. **Write** with a sensible number of files (`repartition`/`maxRecordsPerFile`).
> 7. Use the Spark UI (SQL and Stages tabs) to confirm which stage dominates before and after each change.

## 📝 Summary

- `spark-submit` sets master, deploy mode, executors, cores, memory, dependencies and configs; precedence: code > flags > defaults file.
- Key configs: driver/executor memory, `maxResultSize`, shuffle partitions, default parallelism, Kryo, dynamic allocation, FAIR scheduler, speculation.
- Spark UI (4040): Jobs, Stages, Storage, Environment, Executors, SQL; History Server for finished apps.
- Common problems: stragglers/skew, slow aggregations and joins, driver vs executor OOM, small files, unsplittable input.
- Tuning priorities: read less (formats, partitioning, early filters), enough parallelism (2–3 tasks/core) and no skew, structured APIs over RDDs/UDFs; then caching, broadcast joins, coalesce vs repartition, GC.
- Executor memory is shared between execution and storage; YARN adds overhead.

## ⚠️ Important Notes

1. In client mode, `spark.driver.memory` set in code has no effect; use `--driver-memory`.
2. Default executor memory is only 1 GB.
3. More executors do not fix skew: the slowest task sets the stage time.
4. Speculation can duplicate output with non-idempotent writes.
5. Caching data used once makes the job slower.
6. Driver OOM is usually caused by `collect`, `toPandas` or big broadcasts.
7. Use null for missing values; placeholder strings like "EMPTY" become one giant skewed key.
8. A finished application's UI is gone unless event logging and the History Server are set up.
9. The default FIFO scheduler lets one large job block small ones in a shared application.
10. Very large executors (many cores, huge heaps) can suffer long GC pauses.

> [!warning] Gaps in the source material
> - **Added by me:** the executor-sizing heuristic, unified memory fractions and YARN overhead, salting, adaptive query execution (Spark 3), `ANALYZE TABLE`, the History Server details, and all exercise numbers.
> - LS ch. 7–8 cover the same material for Spark 1.x (SparkConf, jobs/stages/tasks, web UI, level of parallelism, Kryo, memory); DG's version is followed.
> - Spark UI screenshots in DG are images.

**Previous:** [[07 - Data Sources and File Formats]] · **Next:** [[09 - Stream Processing and Kafka]]
