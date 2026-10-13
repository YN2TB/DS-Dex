---
subject: Big Data Analytics
chapter: 9
tags: [ds, streaming, kafka, message-bus, structured-streaming, event-time, watermark, checkpointing]
source: "Chambers & Zaharia, Spark: The Definitive Guide, ch. 20–23; Karau et al., Learning Spark, ch. 10; standard Kafka material"
---

# Stream Processing and Kafka

The mid-term part of the course (`note/Overview.md`) covers Kafka and message buses; this note combines DG's streaming chapters with the core Kafka concepts.

## 📘 Main Knowledge

### 1. Stream processing

**Stream processing** continuously incorporates new data to compute a result. The input is **unbounded**: events such as card transactions, clicks or sensor readings keep arriving. **Batch processing** computes once over a fixed dataset. In practice the two are combined (streams joined with batch-produced tables; the same logic run in both).

Use cases (DG): notifications and alerting, real-time reporting/dashboards, incremental ETL into a warehouse, updating data served in real time, real-time decision making (e.g. fraud checks), online machine learning.

Why stream (DG):
1. **Lower latency** (minutes down to milliseconds), keeping state in memory.
2. **Incremental computation**: updating a 24-hour statistic every hour, a batch job rescans 24 hours each time; a streaming job processes only the new hour.

Batch is simpler and usually has higher throughput, so stream only when you need these.

Challenges: out-of-order and late data, keeping large state, high throughput, exactly-once processing despite failures, combining streams with batch data, updating running applications, writing to external systems transactionally.

### 2. Design choices

| Choice | Options |
|---|---|
| API style | **record-at-a-time** (e.g. Apache Storm: full control, but you manage state, cleanup and duplicates yourself) vs **declarative** (say what to compute; the engine handles state and recovery) |
| Time | **event time** (timestamp set at the source, e.g. on the phone) vs **processing time** (when the record reaches the system). Remote sources (mobile, IoT) need event time because data arrives late and out of order |
| Execution | **continuous** (each record processed immediately; lowest latency at low rates, but per-record overhead and fixed topology) vs **micro-batch** (collect e.g. 500 ms of data, process it as a small batch job; higher throughput, latency ~100 ms–1 s) |

Spark has two streaming APIs:
- **Spark Streaming (DStreams)**, 2012: micro-batches of RDDs, processing time only, Java/Python objects (no Catalyst). Covered in LS ch. 10; now legacy.
- **Structured Streaming**, 2016: built on DataFrames/SQL, event-time support, the same code as batch; micro-batch, with an experimental continuous mode from Spark 2.3.

### 3. Message buses and Kafka

A **message bus** (message broker) decouples **producers** (systems that emit events) from **consumers** (systems that process them). Producers do not need to know who reads the data, consumers can read at their own pace, and the bus buffers bursts. Two classic patterns: a **queue** (each message handled by one consumer) and **publish/subscribe** (each subscriber gets every message). Examples: Apache Kafka, RabbitMQ, AWS Kinesis, Google Pub/Sub.

**Apache Kafka** (originally LinkedIn) is a distributed, persistent, append-only log used as a pub/sub bus. Core concepts (standard Kafka material, added beyond DG):

| Concept | Meaning |
|---|---|
| broker | a Kafka server; a cluster has several |
| topic | a named stream of records, e.g. `payments` |
| partition | a topic is split into partitions, each an ordered, append-only log; partitions are spread over brokers and are the unit of parallelism |
| offset | the position of a record within a partition |
| record | key, value (bytes), timestamp, headers; records with the same key go to the same partition |
| producer | writes records to a topic |
| consumer / consumer group | consumers in one group share the partitions (each partition read by one consumer in the group); different groups each read the full topic |
| replication | each partition has a leader and follower replicas on other brokers (replication factor, e.g. 3) |
| retention | records are kept for a configured time or size, whether or not they were read, so consumers can **replay** from an old offset |

Properties: ordering is guaranteed **within a partition**, not across a topic; throughput scales with the number of partitions; consumers track their own offsets.

**Delivery semantics**: at-most-once (may lose messages), at-least-once (may duplicate; the usual default), exactly-once (each message affects the result once; needs replayable sources, offset tracking and idempotent or transactional sinks).

### 4. Structured Streaming model

A stream is treated as a **table that keeps growing**; your query is a normal DataFrame query, and Spark runs it **incrementally** as new data arrives, updating a **result table**.

```python
static = spark.read.json("/data/activity-data")
streaming = spark.readStream.schema(static.schema) \
    .option("maxFilesPerTrigger", 1).json("/data/activity-data")
activityCounts = streaming.groupBy("gt").count()
query = activityCounts.writeStream.queryName("activity_counts") \
    .format("memory").outputMode("complete").start()
query.awaitTermination()   # in a script
```

- Transformations are (almost) the same as batch; some cannot be incrementalized (e.g. sorting a non-aggregated stream, some multi-aggregations in Spark 2.2).
- There is one action: `start()`, which runs the query continuously.
- Streaming reads need an explicit schema (no inference by default).

**Sources** (Spark 2.2): Kafka, files in a directory (new files are picked up), socket (testing). **Sinks**: Kafka, files, `foreach` (custom code per row), console and memory (testing).

**Output modes**:

| Mode | Writes | Allowed for |
|---|---|---|
| append | only new rows that will not change | queries without aggregation; event-time aggregations **with a watermark** (a window is emitted once it is final) |
| update | rows that changed since the last trigger | most queries |
| complete | the whole result table each time | aggregations only (keeping all raw rows would be impossible) |

**Triggers** control when to process: by default as soon as the previous micro-batch finishes; `trigger(processingTime="1 minute")` for fixed intervals (fewer, larger output files); `trigger(once=True)` to process available data and stop (batch-like runs on a schedule).

Stream–static joins work (join a stream with a reference table); stream–stream joins came in Spark 2.3.

### 5. Event time, windows and watermarks

Event time is just a column: `withEventTime = streaming.selectExpr("*", "cast(cast(Creation_Time as double)/1000000000 as timestamp) as event_time")`.

```python
from pyspark.sql.functions import window, col
withEventTime.groupBy(window(col("event_time"), "10 minutes")).count()               # tumbling
withEventTime.groupBy(window(col("event_time"), "10 minutes", "5 minutes")).count()  # sliding
```

- **Tumbling windows**: fixed, non-overlapping; each event in exactly one window.
- **Sliding windows**: length L, starting every S; each event is in L/S windows (10 min every 5 min → 2).
- A late event updates the window it belongs to, even after newer windows have started.

Without limits Spark must keep every window's state forever. A **watermark** says how late data may be:

```python
withEventTime.withWatermark("event_time", "30 minutes") \
    .groupBy(window(col("event_time"), "10 minutes", "5 minutes")).count()
```

Watermark = (maximum event time seen) − (allowed delay). Windows that end before the watermark are finalized: their state is dropped, append mode emits them, and later data for them can be ignored. Larger delay = more complete results but more state and later output.

**Deduplication**: `dropDuplicates(["User", "event_time"])` with a watermark turns an at-least-once source into exactly-once results (DG). **Arbitrary stateful processing**: `mapGroupsWithState` / `flatMapGroupsWithState` (Scala/Java) for sessionization and custom state with timeouts.

### 6. Kafka with Structured Streaming

```python
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "host1:port1,host2:port2") \
    .option("subscribe", "topic1") \
    .option("startingOffsets", "earliest").load()
parsed = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
```

- Choose exactly one of `assign` (specific topic partitions, JSON `{"topicA":[0,1]}`), `subscribe` (list of topics) or `subscribePattern`.
- `startingOffsets` / `endingOffsets`: `earliest`, `latest`, or per-partition JSON (−2 = earliest, −1 = latest). Only applies when a new query starts; a restarted query resumes from its checkpoint.
- Other options: `failOnDataLoss`, `maxOffsetsPerTrigger`.
- Each row has `key` (binary), `value` (binary), `topic`, `partition`, `offset`, `timestamp`; parse `value` (JSON with `from_json`, or Avro).
- Writing: provide `key`/`value` columns (and `topic` as a column or option), plus a checkpoint location:

```python
out.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
   .writeStream.format("kafka") \
   .option("kafka.bootstrap.servers", "host1:port1") \
   .option("checkpointLocation", "/to/HDFS-compatible/dir") \
   .option("topic", "topic1").start()
```

### 7. Fault tolerance and production

- **Checkpointing**: set `checkpointLocation` on reliable storage (HDFS, S3). Spark saves the source offsets processed in each trigger (write-ahead log) and the state. After a failure or restart with the same checkpoint, the query resumes where it stopped.
- **End-to-end exactly-once** requires a replayable source (Kafka, files), checkpointed offsets/state, and an idempotent or transactional sink (the file sink is; the Kafka sink is at-least-once).
- **Updating an application**: code changes that keep the same input/output schema can reuse the checkpoint; changing aggregation keys or state structure needs a new checkpoint.
- **Monitoring**: `query.status`, `query.recentProgress` (input rate vs processing rate, batch duration), the Spark UI, and `StreamingQueryListener` for alerts. If processing rate stays below input rate, the stream falls further behind.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Which output mode?*
> (a) Filter and select clicks from a stream and write them to Parquet. (b) Count clicks per country since the stream started. (c) Count clicks per 10-minute event-time window with a 15-minute watermark, written as final results to files.
>
> ---
> (a) Append (no aggregation; rows never change). Complete is not allowed.
> (b) Complete or update; append is not allowed because counts keep changing and there is no watermark.
> (c) Append: each window is written once, after the watermark passes its end. The file sink supports append only.

> [!example]- **2.** *(Easy–medium) Windows*
> An event has event time 12:07. Which windows contain it for (a) 10-minute tumbling windows; (b) 10-minute windows sliding every 5 minutes; (c) 1-hour windows sliding every 10 minutes (how many)?
>
> ---
> (a) [12:00, 12:10). (b) [12:00, 12:10) and [12:05, 12:15). (c) $60/10=6$ windows: those starting at 11:10, 11:20, 11:30, 11:40, 11:50, 12:00.

> [!example]- **3.** *(Medium) Watermarks*
> 10-minute tumbling windows, watermark delay 10 minutes. The largest event time seen so far is 12:30. (a) What is the watermark? (b) Which windows are finalized? (c) An event with time 12:15 arrives now; is it counted? (d) One with 12:22?
>
> ---
> (a) 12:30 − 10 min = 12:20.
> (b) Windows ending at or before 12:20: [12:00, 12:10) and [12:10, 12:20) (and earlier).
> (c) Its window [12:10, 12:20) is already finalized, so it is too late and may be dropped (Spark guarantees to keep data newer than the watermark, not to drop all older data).
> (d) Yes: [12:20, 12:30) is still open.

> [!example]- **4.** *(Medium–hard) Kafka partitions and parallelism*
> A topic has 12 partitions. (a) A consumer group has 4 consumers; how are partitions assigned? With 15 consumers? (b) A Spark job reads the topic; how many tasks per micro-batch by default? (c) Events for one user must be processed in order; how should producers set keys?
>
> ---
> (a) 3 partitions per consumer; with 15 consumers, 12 get one partition each and 3 sit idle (a partition is read by one consumer per group).
> (b) One task per Kafka partition: 12 (repartition after reading for more parallelism downstream).
> (c) Use the user ID as the record key, so all of a user's events go to the same partition, where order is preserved. Kafka does not order across partitions.

> [!example]- **5.** *(Hard) Design an exactly-once pipeline*
> Payment events go to Kafka (duplicates possible after producer retries). You need per-merchant 5-minute totals in event time, tolerating events up to 20 minutes late, written to files and safe across restarts. Write the pipeline outline and explain each choice.
>
> ---
> ```python
> raw = spark.readStream.format("kafka").option("kafka.bootstrap.servers", servers) \
>     .option("subscribe", "payments").option("startingOffsets", "earliest").load()
> pay = raw.select(from_json(col("value").cast("string"), schema).alias("p")).select("p.*")
> totals = (pay.withWatermark("event_time", "20 minutes")
>              .dropDuplicates(["payment_id", "event_time"])
>              .groupBy(window("event_time", "5 minutes"), "merchant_id")
>              .agg(sum("amount").alias("total")))
> totals.writeStream.format("parquet").outputMode("append") \
>     .option("path", out).option("checkpointLocation", ckpt) \
>     .trigger(processingTime="1 minute").start()
> ```
> - Kafka is replayable; offsets are stored in the checkpoint, so a restart resumes exactly where it stopped.
> - The watermark bounds state and lets append mode emit each window once it is final (≥ 20 minutes after its end).
> - `dropDuplicates` on the payment ID (with the event time, so the watermark can expire old keys) removes producer retries.
> - The file sink is idempotent with the checkpoint, giving end-to-end exactly-once.
> - The 1-minute trigger avoids many tiny files.

## 📝 Summary

- Streaming = incremental processing of unbounded data; use it for low latency or incremental updates; batch is simpler.
- Design choices: record-at-a-time vs declarative, event time vs processing time, continuous vs micro-batch.
- Message bus decouples producers and consumers. Kafka: brokers, topics, partitions (ordered logs, unit of parallelism), offsets, consumer groups, replication, retention and replay.
- Structured Streaming: a stream is an unbounded table; same DataFrame code; `readStream` / `writeStream.start()`.
- Output modes: append, update, complete; triggers: default, processing time, once.
- Event-time windows (tumbling, sliding) and watermarks (max event time − delay) bound state and finalize windows; `dropDuplicates` with a watermark gives exactly-once results.
- Kafka source rows: key, value, topic, partition, offset, timestamp; options `subscribe`, `startingOffsets`.
- Checkpoints + replayable sources + idempotent sinks give exactly-once and restartability.

## ⚠️ Important Notes

1. Without a watermark, stateful aggregations keep state forever and memory grows without bound.
2. Complete mode is only for aggregations; append mode with aggregation needs a watermark.
3. Kafka orders records only within a partition.
4. More consumers than partitions leaves consumers idle.
5. `startingOffsets` is ignored when restarting from a checkpoint.
6. Changing the checkpoint location restarts processing from scratch (or from `startingOffsets`).
7. The Kafka sink is at-least-once; downstream consumers should handle duplicates.
8. Processing time is not event time; late mobile data is assigned to the wrong window if you use arrival time.
9. Streaming reads need a schema.
10. Watch input rate vs processing rate; if processing is slower, latency grows forever.

> [!warning] Gaps in the source material
> - DG describes Kafka only as a Spark source/sink. **Added by me** (standard material): message bus patterns, Kafka architecture (brokers, partitions, offsets, consumer groups, replication, retention), delivery semantics, and the Kafka sink's at-least-once guarantee.
> - LS ch. 10 covers DStreams (Spark 1.x); only the key ideas (micro-batches, checkpointing, receivers) are reflected here.
> - **Added by me:** all exercises; Spark 2.3 features (continuous mode, stream–stream joins) are mentioned as DG announces them.
> - Figures (micro-batch vs continuous, windows, watermark timeline) are images.

**Previous:** [[08 - Running, Monitoring and Tuning Spark]] · **Next:** [[10 - Workflow Orchestration with Airflow]]
