---
subject: Big Data Analytics
chapter: 1
tags: [ds, big-data, hadoop, hdfs, mapreduce, spark]
source: "User's course notes (note/1.md, 2.md, 3.md); Chambers & Zaharia, Spark: The Definitive Guide, ch. 1; Karau et al., Learning Spark, ch. 1"
---

# Big Data and Distributed Computing

## 📘 Main Knowledge

### 1. What makes data "big"

Big data is data that one machine cannot store or process in reasonable time. The course describes it with the **V's**:

| V | Meaning | Example |
|---|---|---|
| Volume | terabytes to exabytes, more than one machine's disk or memory | years of clickstream logs |
| Velocity | data arrives fast and must be processed quickly | payments, IoT sensors, e-commerce events |
| Variety | structured (SQL tables), semi-structured (JSON, XML), unstructured (images, video, text) | product catalogue + reviews + photos |
| Veracity | data may be incomplete, inconsistent or wrong | faulty sensors, inconsistent customer records |
| Value | data is only worth something if it leads to decisions | churn prediction that changes retention policy |

The user's notes add two engineering requirements: **fault tolerance** (machines fail, so data and computation must survive failures) and **scalability with cost efficiency** (use many cheap commodity machines instead of one expensive server).

### 2. Why clusters became necessary

DG ch. 1 explains the economics:

- Until about 2005 processors got faster every year, so software sped up for free. Then heat limits stopped clock speeds rising; manufacturers added cores instead. Programs now have to be parallel to get faster.
- Storage kept getting cheaper: the cost of storing 1 TB halves roughly every 14 months. That is about $2^{120/14}\approx380$× cheaper per decade (my arithmetic).
- Sensors and cameras became cheap (a 12-megapixel webcam for \$3–4), so organizations collect far more data.

Result: collecting data is cheap, but processing it needs parallel computation on clusters.

**Scale up vs. scale out.** Scaling up means buying a bigger machine; scaling out means adding more machines. Scaling out is cheaper and has no hard ceiling, but the software must split work across machines and handle failures.

A simple illustration (my numbers): reading 1 TB from one disk at 100 MB/s takes $10^{12}/10^8=10{,}000$ s ≈ 2.8 hours. Spread over 100 disks reading in parallel it takes about 1.7 minutes. Parallel I/O, not just parallel CPU, is the point of a cluster.

**Data locality**: moving data over the network is expensive, so distributed systems try to run computation on the machines that already hold the data.

### 3. Hadoop

Hadoop (open-source, inspired by Google's GFS and MapReduce papers) has two core parts, plus a resource manager added in Hadoop 2.

#### HDFS (Hadoop Distributed File System)

The storage layer. Master–worker architecture:

| Component | Role |
|---|---|
| Client | reads and writes files |
| NameNode (master) | keeps metadata: file names, which blocks make up each file, where each block is stored |
| DataNodes (workers) | store the actual blocks and serve reads/writes; send heartbeats to the NameNode |

- Files are split into large **blocks** (128 MB by default in Hadoop 2+; often 256 MB).
- Each block is **replicated** (default 3 copies) on different DataNodes, so losing a machine does not lose data. When a DataNode dies, the NameNode re-replicates its blocks.
- Designed for **write once, read many**: large sequential reads, appends, no in-place updates. HDFS is not ACID (see [[02 - Data Architectures]]).
- Large blocks keep NameNode metadata small and make reads mostly sequential.

#### MapReduce

The original processing engine: divide and conquer.

1. **Map**: each mapper processes one input split (usually one block, on the node that stores it) and emits key–value pairs.
2. **Shuffle and sort**: pairs are grouped by key and sent over the network so that all values for a key reach the same reducer.
3. **Reduce**: each reducer combines the values for its keys and writes output to HDFS.

Word count: map emits `(word, 1)` for each word; reduce sums the 1s for each word.

#### YARN

YARN (Yet Another Resource Negotiator, Hadoop 2) separates resource management from MapReduce: a ResourceManager allocates CPU and memory on the cluster to applications, so other engines (including Spark) can run on the same Hadoop cluster. (Standard Hadoop material, added beyond the notes.)

### 4. The limits of MapReduce

From the user's notes and DG/LS:

- **Disk between steps.** Each job writes its output to HDFS and the next job reads it back. High latency.
- **Iterative algorithms are slow.** A typical ML algorithm makes 10–20 passes over the data (DG). In MapReduce each pass is a separate job, launched separately, reading the data from scratch.
- **No streaming.** MapReduce is batch-only.
- **Hard to program.** Multi-step logic has to be chained as many map/reduce jobs.
- **Storage and compute tied together.** Hadoop bundled HDFS and MapReduce, so it was hard to use one without the other or to read data stored elsewhere (DG).

### 5. Spark

DG defines Spark as "a unified computing engine and a set of libraries for parallel data processing on computer clusters."

- **Unified**: one engine and consistent APIs for SQL, batch, streaming, machine learning and graphs, so one application can combine them and the engine can optimize across them (e.g. one scan for a SQL query followed by an ML model).
- **Computing engine only**: Spark does not store data long term. It reads from HDFS, S3, Azure Storage, Cassandra, Kafka and others. This decoupling suits the cloud, where storage and compute are bought separately.
- **Libraries**: Spark SQL, MLlib, Spark Streaming / Structured Streaming, GraphX, plus external packages.
- **In-memory data sharing** between steps, so iterative and interactive work avoids repeated disk reads. LS: Spark was already 10–20× faster than MapReduce for certain jobs soon after 2009.

Spark's stack (LS): Spark Core (scheduling, memory, fault recovery, RDDs) at the bottom; Spark SQL, Streaming, MLlib, GraphX on top; cluster managers (Standalone, YARN, Mesos; later Kubernetes) underneath.

### 6. Timeline

| Year | Event | Source |
|---|---|---|
| 2003–2004 | Google publishes GFS and MapReduce papers | standard |
| 2006–2008 | Hadoop; Yahoo! runs it on a 10,000-node cluster (2007); Apache top-level project (2008) | user notes |
| 2009 | Spark started at UC Berkeley (RAD Lab → AMPLab), Matei Zaharia et al. | DG, LS |
| 2010 | paper "Spark: Cluster Computing with Working Sets"; open-sourced March 2010 | DG, LS |
| 2011 | Shark (SQL on Spark), Spark Streaming started | DG, LS |
| 2013 | donated to Apache (June); Databricks founded | DG, LS |
| 2014 | Spark 1.0 (May); Apache top-level; Spark SQL added | DG, LS |
| 2016 | Spark 2.0: structured APIs (DataFrames, Datasets), Structured Streaming | DG |
| 2020s | data lakes, lakehouses (Delta Lake, Iceberg), managed platforms (Databricks, Snowflake) | user notes |

The user's notes date Spark's open-sourcing to 2012; LS says March 2010. In 2014 Spark sorted 100 TB about 3× faster than the previous Hadoop record using about 10× fewer machines (23 min on 206 machines vs 72 min on 2,100; Daytona GraySort; external figure, added). The commonly quoted "100× faster than MapReduce" is a best case for in-memory iterative jobs, not a typical speedup.

## ✏️ Exercises

> [!example]- **1.** *(Easy) HDFS blocks*
> A 1 TB file is stored in HDFS with 128 MB blocks and replication factor 3. How many blocks, how many block replicas, and how much raw disk space?
>
> ---
> $1\text{ TB}=1{,}048{,}576$ MB, so $1{,}048{,}576/128=8{,}192$ blocks. With 3 replicas: 24,576 block replicas and 3 TB of raw storage. The NameNode keeps metadata for 8,192 blocks; with 4 KB blocks (a typical local file system) it would need 268 million entries, which is why HDFS blocks are large.

> [!example]- **2.** *(Easy) Which V?*
> Name the main V for each: (a) a bank must flag fraudulent card payments within 200 ms; (b) a retailer combines sales tables, product JSON and customer photos; (c) 30% of IoT readings are missing or duplicated; (d) a company stores 5 PB of logs but no one uses them.
>
> ---
> (a) Velocity. (b) Variety. (c) Veracity. (d) Value (also Volume, but the problem is that the data creates no value).

> [!example]- **3.** *(Medium) Word count by hand*
> Input split into three lines handled by three mappers: `big data big`, `data spark`, `spark big`. Show the map output, the shuffle groups and the reduce output. How many pairs cross the network if there is no combiner?
>
> ---
> Map: `(big,1),(data,1),(big,1)`; `(data,1),(spark,1)`; `(spark,1),(big,1)`: 7 pairs.
>
> Shuffle: `big → [1,1,1]`, `data → [1,1]`, `spark → [1,1]`.
>
> Reduce: `big 3`, `data 2`, `spark 2`.
>
> Without a combiner all 7 pairs are shuffled (in general, one per word occurrence). A **combiner** sums locally on each mapper first: mapper 1 would send `(big,2),(data,1)`, giving 6 pairs here and far fewer on real text, where common words repeat many times within a split.

> [!example]- **4.** *(Medium–hard) Why iterative jobs hurt MapReduce*
> An algorithm makes 10 passes over a 500 GB dataset. Assume the cluster reads from disk at 10 GB/s and from memory at 100 GB/s (assumed figures). Compare (a) MapReduce reading from disk every pass, (b) Spark reading once from disk and caching in memory. Ignore compute and writes.
>
> ---
> (a) $10\times500/10=500$ s.
>
> (b) First pass from disk 50 s, then $9\times500/100=45$ s: 95 s. About 5.3× faster.
>
> If MapReduce also writes each pass's 500 GB output back to disk, its time doubles to 1,000 s (10.5×). The gain grows with the number of passes, which is why iterative ML and interactive queries were Spark's first use cases. If the data does not fit in memory the advantage shrinks.

> [!example]- **5.** *(Hard) Why replicate three times?*
> A file has 8,192 blocks. Each node independently fails during a given day with probability 0.01, and assume (simplistically) that blocks on failed nodes are not re-replicated in time and replicas sit on different nodes. Find the probability of losing at least one block for replication factor 1, 2 and 3.
>
> ---
> A block is lost if all its replicas fail: probability $0.01^r$. With $n=8{,}192$ blocks, $P(\ge1\text{ lost})=1-(1-0.01^r)^n$:
>
> | $r$ | per block | expected blocks lost | $P(\ge1)$ |
> |---|---|---|---|
> | 1 | 0.01 | 81.9 | ≈ 1 |
> | 2 | $10^{-4}$ | 0.82 | 0.559 |
> | 3 | $10^{-6}$ | 0.0082 | 0.0082 |
>
> A 1% per-block risk sounds small, but across 8,192 blocks losing something is almost certain. Each extra replica cuts the risk 100×. Real HDFS also re-replicates quickly and places replicas across racks, which makes losses rarer still; correlated failures (a whole rack) are the main remaining risk.

## 📝 Summary

- Big data: Volume, Velocity, Variety, Veracity, Value; systems also need fault tolerance and cheap scaling.
- Clock speeds stalled around 2005 while storage cost kept halving every ~14 months, so processing moved to clusters of commodity machines (scale out).
- HDFS: NameNode holds metadata, DataNodes hold 128 MB blocks replicated 3×; write once, read many.
- MapReduce: map → shuffle/sort → reduce, with results written to disk between jobs; YARN manages cluster resources.
- MapReduce is slow for iterative and interactive work, has no streaming, and is verbose.
- Spark: unified engine plus libraries, compute only (storage elsewhere), in-memory data sharing; started 2009 at Berkeley, Apache 2013, 1.0 in 2014, 2.0 in 2016.

## ⚠️ Important Notes

1. Spark does not replace HDFS; it replaces MapReduce. Spark has no storage layer of its own.
2. "100× faster" applies to in-memory iterative workloads. For a single pass over disk data the gap is much smaller.
3. HDFS block size (128 MB) is not the same as a local file-system block (4 KB).
4. Replication protects against node failure, not against bad data or accidental deletion.
5. The NameNode is a single point of failure in classic HDFS (later versions add a standby NameNode).
6. The shuffle is the expensive step in MapReduce and in Spark: data crosses the network.
7. Combiners only work for operations that can be applied partially (sum, max), not for things like median.
8. Scaling out adds coordination and failure handling; for data that fits on one machine, a single-machine tool is often faster.
9. Velocity is about latency requirements, not data size.
10. Know the timeline in order: Google papers → Hadoop → Spark (2009) → Apache (2013) → 1.0 (2014) → 2.0 (2016).

> [!warning] Gaps in the source material
> - The V's, Hadoop details and the 2007–2020 timeline come from the user's notes; DG and LS cover Spark's history and motivation.
> - **Added by me:** the 380×-per-decade and disk-read arithmetic, YARN, combiners, Google's GFS/MapReduce papers, the 2014 sort benchmark figures, and all exercise scenarios (assumed numbers are labelled).
> - The user's notes date Spark's open-sourcing to 2012; LS says March 2010.
> - Figures (Spark stack, Spark toolkit) are images; their content is described in the text.

**Previous:** [[00-Index]] · **Next:** [[02 - Data Architectures]]
