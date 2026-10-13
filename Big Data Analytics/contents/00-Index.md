---
subject: Big Data Analytics
chapter: 00
tags: [ds, moc, big-data, spark]
source: "Chambers & Zaharia, Spark: The Definitive Guide (2018); Karau et al., Learning Spark (2015); user's course notes"
---

# Big Data Analytics — Map of Content

Notes for the Big Data Analytics course (Data Science, NEU). The course plan in `note/Overview.md` is: mid-term on the big data platform (Airflow, Kafka, message bus), final on PySpark. The user's notes also cover big data concepts, Hadoop, data warehouses, lakes, lakehouses, data mesh and governance.

## Scope

> [!note] Scope is my choice
> The two books in `documents/` are both about Spark. The order and topics below follow the user's notes and Overview; the platform chapters (02, 10) have no textbook in the folder and are built from the user's notes plus standard material. Please confirm against the real syllabus.

| # | Note | Covers | Main source | Status |
|---|---|---|---|---|
| 01 | [[01 - Big Data and Distributed Computing]] | 5 Vs, why clusters, Hadoop (HDFS, MapReduce, YARN), MapReduce's limits, history of Spark | user notes; DG 1; LS 1 | ✅ |
| 02 | [[02 - Data Architectures]] | data warehouse tiers, OLAP, data lake, ETL vs ELT, lakehouse, data mesh, governance, ACID | user notes | ✅ |
| 03 | [[03 - Spark Architecture and Execution]] | driver, executors, cluster manager, SparkSession, partitions, transformations/actions, lazy evaluation, jobs/stages/tasks | DG 2, 15; LS 2, 7 | ✅ |
| 04 | [[04 - RDDs, Key-Value Pairs and Shared Variables]] | RDD API, pair RDDs, reduceByKey vs groupByKey, partitioners, caching, broadcast variables, accumulators | LS 3, 4, 6; DG 12–14 | ✅ |
| 05 | [[05 - DataFrames and Spark SQL]] | schemas, columns, expressions, transformations, data types, nulls, UDFs, Catalyst, SQL tables and views | DG 4–6, 10 | ✅ |
| 06 | [[06 - Aggregations and Joins]] | groupBy, window functions, rollup/cube, join types, shuffle vs broadcast joins | DG 7–8 | ✅ |
| 07 | [[07 - Data Sources and File Formats]] | CSV, JSON, Parquet, ORC, JDBC, partitioning and bucketing, compression and splittability | DG 9; LS 5 | ✅ |
| 08 | [[08 - Running, Monitoring and Tuning Spark]] | spark-submit, cluster managers, configuration, Spark UI, memory, serialization, skew, tuning | DG 16–19; LS 7–8 | ✅ |
| 09 | [[09 - Stream Processing and Kafka]] | stream processing concepts, message buses, Kafka, Structured Streaming, event time, watermarks, checkpointing | DG 20–23; LS 10 | ✅ |
| 10 | [[10 - Workflow Orchestration with Airflow]] | DAGs, operators, scheduling, idempotency, backfills, retries | no source in folder | ✅ |
| 11 | [[11 - MLlib Pipelines and Feature Engineering]] | transformers, estimators, pipelines, scaling, encoding, text features, PCA | DG 24–25; LS 11 | ✅ |
| 12 | [[12 - MLlib Models, Evaluation and Tuning]] | linear and generalized linear regression, ElasticNet, classification, trees, evaluation, cross-validation, ALS, k-means | DG 26–29 | ✅ |

### Not covered

| Source part | Reason |
|---|---|
| DG 11 Datasets | Scala/Java only; the course uses PySpark |
| DG 30–33 (GraphX/GraphFrames, deep learning, language bindings, ecosystem) | not in the user's course plan |
| LS 2 installation, LS 7 Maven/sbt packaging | setup, not examinable |
| Old Spark Streaming DStreams (LS 10) | replaced by Structured Streaming; only the key ideas are kept in ch. 09 |

## Source notes

- DG (2018) targets Spark 2.2; LS (2015) targets Spark 1.1. Where they differ, DG is followed. Some details have changed in Spark 3 (e.g. adaptive query execution); these are noted as additions.
- Figures in both books are images and do not extract.

## Cross-subject links

| Subject | Relationship |
|---|---|
| [[Database Management Systems/contents/00-Index\|Database Management Systems]] | SQL, joins, ACID, transactions |
| [[MLOps/contents/00-Index\|MLOps]] | pipelines, orchestration, deployment |
| [[Machine Learning/contents/00-Index\|Machine Learning]] and [[Econometrics/contents/00-Index\|Econometrics]] | models behind MLlib (regression, GLMs) |
| [[Data Structures and Algorithms/contents/00-Index\|Data Structures and Algorithms]] | hashing, sorting, complexity |
| [[Data Preparation and Visualization/contents/00-Index\|Data Preparation and Visualization]] | cleaning, scaling, encoding |

## Errata

| # | Where | Printed | Correct | Note |
|---|---|---|---|---|
| E1 | LS Table 4-2 (p. 50) | rightOuterJoin: "key must be present in the first RDD"; leftOuterJoin: "…in the other RDD" | descriptions swapped: left outer keeps all keys of the first RDD, right outer of the other | the table's example results are correct |
| E2 | LS Example 4-12 (p. 54) | `sumCount.map(lambda key, xy: (key, xy[0]/xy[1]))` | `map` passes one tuple: `lambda kv: (kv[0], kv[1][0]/kv[1][1])` or `mapValues(lambda xy: xy[0]/xy[1])` | raises TypeError as printed |
| E3 | LS Example 4-16 (p. 57) | Scala "custom parallelism" line identical to the default one | should pass `10` as in the Python version | |
| E4 | DG ch. 5, "Sorting Rows" (p. 85) | `df.orderBy(expr("count desc"))` as a descending sort | `expr("count desc")` parses as `count AS desc`, so the sort is ascending; use `desc("count")` | |
| E6 | DG ch. 25, Polynomial Expansion (p. 447) | degree 2 on 2 features gives "four output features (2x2)"; degree 3 on 3 features gives "27 (3x3x3)" | $\binom{n+d}{d}-1$: 5 and 19 (3 features at degree 2 is 9, which DG gets right by coincidence) | |
| E5 | DG ch. 6, nulls (p. 109) | `nullif` "returns null if the two values are equal or else returns the second" | returns the **first** value when they differ (standard SQL) | the printed example only shows the equal case |
