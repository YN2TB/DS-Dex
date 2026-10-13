---
subject: Big Data Analytics
chapter: 7
tags: [ds, spark, data-sources, parquet, orc, csv, json, jdbc, partitioning, bucketing, compression]
source: "Chambers & Zaharia, Spark: The Definitive Guide, ch. 9; Karau et al., Learning Spark, ch. 5"
---

# Data Sources and File Formats

## 📘 Main Knowledge

### 1. Reader and writer API

```python
# read
df = spark.read.format("csv") \
    .option("mode", "FAILFAST").option("inferSchema", "true").option("header", "true") \
    .schema(mySchema).load("/data/flight-data/csv/2010-summary.csv")
# write
df.write.format("parquet").mode("overwrite") \
    .partitionBy("DEST_COUNTRY_NAME").save("/tmp/out.parquet")
```

Reading: `DataFrameReader.format(...).option(...).schema(...).load(path)`. The default format is **Parquet**.

Writing: `DataFrameWriter.format(...).option(...).partitionBy(...).bucketBy(...).sortBy(...).save(path)`. `partitionBy`, `bucketBy` and `sortBy` work only for file sources (bucketing only with `saveAsTable`).

**Read modes** (for malformed records):

| Mode | Behaviour |
|---|---|
| `permissive` (default) | sets the bad record's fields to null and puts the raw text in `_corrupt_record` |
| `dropMalformed` | drops malformed rows |
| `failFast` | fails immediately |

**Save modes**:

| Mode | If data exists at the path |
|---|---|
| `errorIfExists` (default) | fail |
| `append` | add new files |
| `overwrite` | replace everything there |
| `ignore` | do nothing |

### 2. Formats

| Format | Type | Schema | Notes |
|---|---|---|---|
| CSV | row, text | none (header optional) | many options; tricky in practice (quotes, separators, nulls); no complex types |
| JSON | row, text | self-describing per record | Spark expects **line-delimited** JSON (one object per line); `multiLine` for whole-file JSON |
| Parquet | columnar, binary | stored in the file | Spark's default; column pruning, compression, predicate pushdown, complex types; recommended for long-term storage |
| ORC | columnar, binary | stored in the file | similar to Parquet; DG: Parquet is more optimized for Spark, ORC for Hive |
| Text | lines | single `value` column | for logs; `write.text` needs one string column |
| JDBC | database tables | from the database | needs the driver JAR |
| Avro, SequenceFiles, protobuf | row, binary | | Hadoop formats (LS ch. 5) |

**CSV options** (DG Table 9-3): `sep` (`,`), `header` (false), `escape` (`\`), `inferSchema` (false), `ignoreLeadingWhiteSpace`, `nullValue` (""), `nanValue`, `dateFormat` (`yyyy-MM-dd`), `timestampFormat`, `maxColumns`, `multiLine`, `compression`, `quote`. **JSON options** add `allowComments`, `allowSingleQuotes`, `primitiveAsString` etc.

**Why columnar formats are faster for analytics**: values of one column are stored together, so a query that needs 3 of 50 columns reads only those columns; similar values compress well; files store min/max statistics per row group, so filters can skip blocks (predicate pushdown). Row formats (CSV, JSON, Avro) suit writing whole records and record-at-a-time processing.

### 3. SQL databases (JDBC)

```python
df = spark.read.format("jdbc").option("url", url).option("dbtable", "flight_info") \
    .option("driver", driver).option("numPartitions", 10).load()
```

- **Query pushdown**: Spark pushes column selection and supported filters into the database (`PushedFilters` in `explain()`). For things Spark cannot translate, pass a subquery as `dbtable`: `"(SELECT DISTINCT(DEST_COUNTRY_NAME) FROM flight_info) AS flight_info"`.
- **Parallel reads**: by default one connection reads everything into one partition. Give `partitionColumn`, `lowerBound`, `upperBound`, `numPartitions` (Spark splits the range into strides, one query per partition), or a list of `predicates`, one per partition.
- `numPartitions` also limits concurrent connections, to avoid overloading the database.
- Writing: `df.write.jdbc(url, table, mode="overwrite", properties=props)`.

### 4. Splittability and compression

A format is **splittable** if several tasks can read different parts of one file (they can find where records start). Not all compression is splittable (LS Table 5-3):

| Codec | Splittable | Speed | Compression on text |
|---|---|---|---|
| gzip | no | fast | high |
| LZO | yes (with an index) | very fast | medium |
| bzip2 | yes | slow | very high |
| zlib (deflate) | no | slow | medium |
| Snappy | no (as a raw stream) | very fast | low |

A single large gzip file is read by **one** task. Inside Parquet and ORC, compression applies to individual pages/chunks, so the files remain splittable by row group whatever the codec. DG recommends Parquet with gzip; Spark's default Parquet codec since 2.0 is Snappy (faster, less compression).

### 5. Parallelism and file layout

- **Reading**: each file (or each split of a splittable file, ~128 MB) becomes a partition; files are read in parallel.
- **Writing**: one file per partition. `csvFile.repartition(5).write.format("csv").save("/tmp/multiple.csv")` creates a folder with five `part-0000x-...csv` files. "A file" in Spark is usually a directory of part files.
- **Partitioning on write** (`partitionBy("DEST_COUNTRY_NAME")`) encodes a column as folders: `DEST_COUNTRY_NAME=Senegal/part-...parquet`. Queries filtering on that column read only the matching folders (**partition pruning**). DG calls it "probably the lowest-hanging optimization". Use columns with moderate cardinality that are often filtered (date, country); a high-cardinality column creates a huge number of tiny folders.
- **Bucketing** (`bucketBy(10, "count").saveAsTable("bucketedFiles")`) hashes rows into a fixed number of files by column value. Data with the same bucket ID is already grouped, so later joins and aggregations on that column can avoid a shuffle. Only for Spark-managed tables.
- **File size**: many small files cost metadata and scheduling overhead (the **small file problem**, bad for HDFS NameNode too); huge files waste reads. `option("maxRecordsPerFile", 5000)` caps records per file (Spark 2.2+). Aim for files of roughly hundreds of MB.
- Complex types (arrays, maps, structs) work in Parquet/ORC/JSON but not CSV.

### 6. Other storage (LS ch. 5)

Spark reads from local file systems (the file must exist at the same path on every node), HDFS (`hdfs://namenode:port/path`), Amazon S3 (`s3a://bucket/path`), Hive tables, Cassandra, HBase, Elasticsearch and others via connectors. Spark does not require Hadoop, but uses Hadoop's input/output format APIs.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Pick a format*
> Choose a format: (a) a nightly export a finance team opens in Excel; (b) a 5 TB table queried by analysts on a few columns at a time; (c) web server logs; (d) API responses with nested fields, kept raw for later parsing.
>
> ---
> (a) CSV. (b) Parquet (or ORC): columnar, compressed, column pruning and predicate pushdown. (c) Text (or compressed text), parsed with regex later; convert to Parquet for analysis. (d) Line-delimited JSON in the raw zone; then flatten into Parquet.

> [!example]- **2.** *(Easy–medium) Read modes and save modes*
> A CSV has 1,000 rows, 3 of them malformed. How many rows do you get with `permissive`, `dropMalformed`, `failFast`? Then you write to a path that already holds data without setting a mode. What happens?
>
> ---
> permissive: 1,000 rows, with the 3 bad rows' fields null (and their raw text in `_corrupt_record` if that column is in the schema). dropMalformed: 997. failFast: the read fails at the first bad row (when an action runs). Writing without a mode uses `errorIfExists`, so the write fails.

> [!example]- **3.** *(Medium) How much data is read?*
> A table has one year of data partitioned by `date` (365 equal partitions) stored as Parquet with 50 equally sized columns. A query selects 3 columns for one week. What fraction is read compared with scanning everything? What if the data were CSV without partitioning?
>
> ---
> Partition pruning: $7/365=1.92\%$. Column pruning: $3/50=6\%$. Combined: $0.0192\times0.06\approx0.115\%$, about 870× less. With unpartitioned CSV Spark must read and parse every row and every column: 100%. (Row-group statistics in Parquet can skip even more.)

> [!example]- **4.** *(Medium–hard) Count the files*
> A DataFrame with 200 partitions, each containing rows from all 50 countries, is written with `partitionBy("country")`. (a) Up to how many files? (b) How do you get one file per country? (c) A country has 1.2 million rows and you set `maxRecordsPerFile=5000`; how many files for that country?
>
> ---
> (a) Each task writes one file into each country folder it has data for: up to $200\times50=10{,}000$ small files.
>
> (b) `df.repartition("country").write.partitionBy("country")...`: all rows of a country land in one partition, so one file per country (50 files).
>
> (c) $1{,}200{,}000/5{,}000=240$ files.

> [!example]- **5.** *(Hard) Why is my job slow?*
> A job reads one 10 GB `events.csv.gz` file and runs on a 64-core cluster, but the first stage has one task that takes 40 minutes. Explain and propose two fixes.
>
> ---
> gzip is not splittable, so the whole file is read and decompressed by a single task; 63 cores sit idle. An uncompressed file would split into about $10{,}240/128=80$ partitions.
>
> Fixes: (1) repartition right after reading (`.repartition(128)`) so later stages are parallel; the read itself stays single-threaded. (2) Better: ask for the data as many smaller files or in a splittable form (bzip2, uncompressed, or ideally Parquet), or convert it once to Parquet so every later job reads in parallel.

## 📝 Summary

- Reader: `format/option/schema/load`; writer: `format/option/mode/partitionBy/bucketBy/save`; default format Parquet.
- Read modes: permissive (default), dropMalformed, failFast. Save modes: errorIfExists (default), append, overwrite, ignore.
- CSV and JSON are row-based text; Parquet and ORC are columnar, compressed, schema-carrying, and support pushdown and complex types.
- JDBC: pushdown, parallel reads via partition column bounds or predicates, `numPartitions` to protect the database.
- Splittable formats/codecs allow parallel reads; gzip and Snappy streams are not splittable, but Parquet/ORC stay splittable.
- One output file per partition; `partitionBy` creates folders for partition pruning; `bucketBy` pre-groups data to avoid shuffles; control file size with `repartition` and `maxRecordsPerFile`.

## ⚠️ Important Notes

1. `save("/tmp/x.csv")` creates a directory of part files, not one file.
2. Default save mode `errorIfExists` fails on existing data; `overwrite` deletes what is there.
3. Spark's JSON reader expects one JSON object per line unless `multiLine` is set.
4. A single gzip file means a single read task.
5. Partitioning on a high-cardinality column (user ID) creates millions of tiny files.
6. `partitionBy` on write is about folders on disk; `repartition` is about in-memory partitions. They are different things.
7. Bucketing only works with `saveAsTable` (managed tables).
8. JDBC reads use one partition and one connection unless you configure parallelism.
9. Without an explicit schema, `inferSchema` on CSV costs an extra pass and may guess wrong types.
10. In permissive mode, bad records silently become nulls; count them.

> [!warning] Gaps in the source material
> - **Added by me:** the row vs columnar explanation, row-group statistics, Snappy as Spark's default Parquet codec, `s3a://`, the pruning arithmetic and all exercises.
> - LS Table 5-3 footnotes (e.g. LZO splittability depends on the library) are summarized.
> - DG's recommendation "Parquet with gzip" refers to compression inside Parquet, which remains splittable.

**Previous:** [[06 - Aggregations and Joins]] · **Next:** [[08 - Running, Monitoring and Tuning Spark]]
