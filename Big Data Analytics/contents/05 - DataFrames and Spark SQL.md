---
subject: Big Data Analytics
chapter: 5
tags: [ds, spark, dataframe, spark-sql, catalyst, schema, udf]
source: "Chambers & Zaharia, Spark: The Definitive Guide, ch. 4, 5, 6, 10"
---

# DataFrames and Spark SQL

## 📘 Main Knowledge

### 1. The structured APIs

Spark's structured APIs are **DataFrames**, **Datasets** and **SQL tables/views**. All are immutable, lazily evaluated plans over table-like data, and all work for both batch and streaming.

- A **DataFrame** has rows and named columns; every column has a type that holds for all rows (null marks missing values).
- A **Dataset** is a typed DataFrame checked at compile time; it exists only in Scala/Java. In Scala a DataFrame is `Dataset[Row]`. In Python there are only DataFrames.
- A **table or view** is a DataFrame you query with SQL.

Spark operates on its own types and an optimized internal row format, not on Python objects. `df.select(df["number"] + 10)` does the addition inside Spark, not in Python, which is why DataFrame code performs the same in Python and Scala.

### 2. Schemas and types

A **schema** lists column names and types. It can be inferred (schema-on-read) or defined manually. DG recommends defining schemas manually for production ETL from CSV/JSON, because inference reads a sample and can guess differently on different data.

```python
from pyspark.sql.types import StructField, StructType, StringType, LongType
myManualSchema = StructType([
    StructField("DEST_COUNTRY_NAME", StringType(), True),
    StructField("ORIGIN_COUNTRY_NAME", StringType(), True),
    StructField("count", LongType(), False, metadata={"hello": "world"})])
df = spark.read.format("json").schema(myManualSchema) \
    .load("/data/flight-data/json/2015-summary.json")
```

Common Spark types and their Python values (DG Table 4-1):

| Spark type | Python value | Note |
|---|---|---|
| `ByteType`, `ShortType` | int | 1-byte (−128…127), 2-byte |
| `IntegerType` | int | too-large values are rejected; DG suggests `LongType` |
| `LongType` | int | 8-byte |
| `FloatType`, `DoubleType` | float | 4-byte / 8-byte |
| `DecimalType` | `decimal.Decimal` | exact decimals (money) |
| `StringType`, `BinaryType`, `BooleanType` | str, bytearray, bool | |
| `DateType`, `TimestampType` | `datetime.date`, `datetime.datetime` | |
| `ArrayType(elementType)` | list | `containsNull` defaults to True |
| `MapType(keyType, valueType)` | dict | |
| `StructType([StructField(...)])` | Row / tuple | nested record; field names must be unique |

`nullable=False` is **not enforced**: Spark will still let nulls in; the flag only helps the optimizer, and wrong flags can produce wrong results.

### 3. Columns, expressions and rows

A column can be referenced as `col("count")`, `df["count"]` or `"count"`. Columns are only resolved against the schema when Spark analyzes the plan.

An **expression** is a set of transformations on one or more column values. `expr("(((someCol + 5) * 200) - 6) < otherCol")` and `((col("someCol") + 5) * 200 - 6) < col("otherCol")` compile to the same logical tree. `selectExpr` is `select` with SQL expressions.

A **Row** is one record; rows have no schema of their own (only DataFrames do). `lit(5)` turns a Python constant into a Spark literal column.

### 4. Core DataFrame transformations

| Operation | Example |
|---|---|
| select columns | `df.select("DEST_COUNTRY_NAME", expr("count * 2 as double_count"))` |
| SQL expressions | `df.selectExpr("*", "(DEST_COUNTRY_NAME = ORIGIN_COUNTRY_NAME) as withinCountry")` |
| add/replace a column | `df.withColumn("numberOne", lit(1))` |
| rename | `df.withColumnRenamed("DEST_COUNTRY_NAME", "dest")` |
| drop | `df.drop("ORIGIN_COUNTRY_NAME")` |
| cast | `col("count").cast("long")` |
| filter | `df.where(col("count") < 2).where(col("ORIGIN_COUNTRY_NAME") != "Croatia")` |
| distinct | `df.select("ORIGIN_COUNTRY_NAME").distinct().count()` → 125 (of 256 rows) |
| sample | `df.sample(False, 0.5, 5).count()` → 126 |
| random split | `df.randomSplit([0.25, 0.75], seed)` (weights are normalized) |
| union | `df.union(newDF)` |
| sort | `df.orderBy(desc("count"), asc("DEST_COUNTRY_NAME"))`; `asc_nulls_first` etc. |
| sort within partitions | `df.sortWithinPartitions("count")` (no global order, no shuffle) |
| limit | `df.limit(5)` |
| repartition / coalesce | `df.repartition(5, col("DEST_COUNTRY_NAME"))`, `df.coalesce(2)` |

Notes:
- Chained `where` calls are combined by the optimizer; there is no cost to writing filters one at a time.
- **`union` matches columns by position, not by name.** Two DataFrames with the same columns in a different order are combined wrongly without error. Use `unionByName` (Spark 2.3+).
- Column names with spaces or dashes need backticks in expressions: `` selectExpr("`This Long Column-Name`") ``.
- Spark is case-insensitive about column names by default.
- Collecting: `take(n)`, `show(n, truncate)`, `collect()`, `toLocalIterator()` (one partition at a time).

### 5. Working with different data types (DG ch. 6)

Spark has hundreds of built-in functions in `pyspark.sql.functions`. Prefer them to UDFs.

- **Booleans**: combine with `&`, `|`, `~` in Python (parenthesize each condition), or write a SQL string in `where`.
- **Numbers**: `pow`, `round`, `bround`, `corr`, `describe()`, `monotonically_increasing_id()`.
- **Strings**: `initcap`, `lower`, `upper`, `trim`, `lpad`, `regexp_replace`, `regexp_extract`, `translate`, `instr`/`contains`.
- **Dates/timestamps**: `current_date`, `date_add`, `date_sub`, `datediff`, `months_between`, `to_date(col, fmt)`, `to_timestamp`. Spark returns null for strings that do not parse, rather than raising an error.
- **Complex types**: structs (`struct(...)`, access with `complex.Description` or `.*`), arrays (`split`, `size`, `array_contains`, `explode` = one row per element), maps (`create_map`, `explode` on a map gives key and value columns).
- **JSON**: `get_json_object`, `json_tuple`, `from_json`, `to_json`.

#### Nulls

DG: always represent missing data with null (not empty strings or sentinel values); Spark optimizes nulls.

| Function | Result |
|---|---|
| `coalesce(a, b, …)` | first non-null value |
| `ifnull(a, b)`, `nvl(a, b)` | b if a is null, else a |
| `nullif(a, b)` | null if a = b, else **a** |
| `nvl2(a, b, c)` | b if a is not null, else c |
| `df.na.drop("any")` / `("all")` / `subset=[...]` | drop rows with nulls |
| `df.na.fill(0)` / `fill({"col": value})` | fill nulls |
| `df.na.replace([""], ["UNKNOWN"], "Description")` | replace values |

Comparisons with null give null, and `where` keeps only rows where the condition is **true**. So `where(col("a") > 2)` and `where(~(col("a") > 2))` together can miss rows where `a` is null. Use `isNull()`/`isNotNull()` or the null-safe equality `eqNullSafe` (`<=>` in SQL).

#### User-defined functions

```python
from pyspark.sql.functions import udf
def power3(x): return x ** 3
power3udf = udf(power3)                         # returns StringType unless a type is given
udfExampleDF.select(power3udf(col("num"))).show(2)
spark.udf.register("power3py", power3, DoubleType())   # usable in SQL
```

- Scala/Java UDFs run in the JVM: small penalty (no code generation).
- **Python UDFs** start a Python process on each executor, serialize every row from the JVM to Python and back, and run row by row. The serialization is the main cost, and Python memory is outside Spark's control, so executors can fail. DG recommends writing UDFs in Scala/Java when performance matters.
- Better still: use built-in functions (`pow(col("num"), 3)`). Vectorized **pandas UDFs** (Arrow, Spark 2.3+) reduce the cost (added beyond DG).
- Give the return type; if the function returns a type that does not match, Spark returns null instead of failing.

### 6. How a query is executed (Catalyst)

1. You write DataFrame, Dataset or SQL code.
2. Spark builds an **unresolved logical plan**.
3. The **analyzer** resolves table and column names against the **catalog**; unknown names are rejected here.
4. The **Catalyst optimizer** applies rules to get an **optimized logical plan** (predicate pushdown, column pruning, constant folding, combining filters).
5. **Physical planning** generates candidate physical plans and picks one with a cost model (e.g. which join strategy, based on table sizes).
6. **Execution** runs the chosen plan as RDD operations, with runtime code generation (whole-stage codegen produces Java bytecode).

This is why Spark is sometimes called a compiler. `df.explain(True)` shows the parsed, analyzed, optimized and physical plans.

### 7. Spark SQL

Spark SQL supports ANSI SQL and HiveQL. Before Spark, **Hive** (from Facebook) was the standard SQL layer on Hadoop. DG quotes Facebook (2016): replacing hundreds of Hive jobs with one Spark job gave 4.5–6× less CPU, 3–4× less resource reservation and ~5× lower latency.

Ways to run SQL: `spark.sql("SELECT ...")` (returns a DataFrame), the `spark-sql` CLI, or the Thrift JDBC/ODBC server for BI tools. SQL and DataFrame code can be mixed freely and compile to the same plans.

**Catalog**: metadata about databases, tables, functions and views (`spark.catalog`). Spark can use a **Hive metastore** to share table definitions across sessions and tools.

**Tables**

| | Managed table | Unmanaged (external) table |
|---|---|---|
| created by | `saveAsTable`, `CREATE TABLE ... USING parquet AS SELECT ...` | `CREATE EXTERNAL TABLE ... LOCATION '...'` |
| Spark manages | metadata **and** data files | metadata only |
| `DROP TABLE` | deletes data and metadata | deletes metadata only; files stay |

Tables can be partitioned (`PARTITIONED BY (col)`), inserted into (`INSERT INTO`, optionally a specific partition), cached (`CACHE TABLE flights`) and inspected (`DESCRIBE TABLE`, `SHOW PARTITIONS`). Use `REFRESH TABLE` after files change outside Spark.

**Views** are saved query plans; no data is copied.

| View | Scope |
|---|---|
| `CREATE VIEW` | saved in a database |
| `CREATE TEMP VIEW` / `df.createOrReplaceTempView` | current session only |
| `CREATE GLOBAL TEMP VIEW` / `createGlobalTempView` | all sessions of the application, under database `global_temp` |

Dropping a view never deletes data. **Databases** group tables (`CREATE DATABASE`, `USE some_db`); after `USE`, unqualified table names resolve in the new database.

Other SQL features: `CASE WHEN`, complex types, `explode` via `LATERAL VIEW`, subqueries (correlated and uncorrelated), higher-order functions in later versions.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Define a schema*
> Write a schema for a CSV with columns `order_id` (string, never null), `customer_id` (string), `amount` (decimal with 2 places), `order_ts` (timestamp). Will Spark reject a row with a null `order_id`?
>
> ---
> ```python
> schema = StructType([
>     StructField("order_id", StringType(), False),
>     StructField("customer_id", StringType(), True),
>     StructField("amount", DecimalType(10, 2), True),
>     StructField("order_ts", TimestampType(), True)])
> df = spark.read.schema(schema).option("header", "true").csv(path)
> ```
> No: `nullable=False` is not enforced, so check with `df.where(col("order_id").isNull()).count()`. Unparseable values (e.g. a bad timestamp) become null in the default PERMISSIVE mode.

> [!example]- **2.** *(Easy–medium) Nulls and three-valued logic*
> Column `a` = [1, null, 3], column `b` = [null, 2, null]. Give: (a) `coalesce(a, b)`; (b) `count("*")`, `count("a")`, `avg("a")`; (c) rows from `where(a > 2)` and from `where(~(a > 2))`; (d) `nullif(a, lit(1))`.
>
> ---
> (a) [1, 2, 3]. (b) 3, 2, 2.0 (aggregates skip nulls). (c) `a > 2` → row with 3; `~(a > 2)` → row with 1. The null row appears in neither, because `null > 2` is null and `where` keeps only true. (d) [null, null, 3]: null where a = 1, otherwise a (and null stays null).

> [!example]- **3.** *(Medium) The union trap*
> `df1` has columns (`name`, `city`) with row ("An", "Hanoi"); `df2` has columns (`city`, `name`) with row ("Hue", "Binh"). What does `df1.union(df2)` return? How do you fix it?
>
> ---
> Union is positional: result columns (`name`, `city`) with rows ("An", "Hanoi") and ("Hue", "Binh"), so "Hue" is in `name`. No error is raised because both columns are strings. Fix: `df1.unionByName(df2)` or `df1.union(df2.select("name", "city"))`.

> [!example]- **4.** *(Medium–hard) Follow Catalyst*
> Query: `spark.table("sales").join(spark.table("stores"), "store_id").where(col("region") == "North").select("store_id", "amount")`. Describe what each planning phase does, including where the filter ends up and how the join may be executed.
>
> ---
> - Unresolved plan: join → filter → project, names not yet checked.
> - Analyzer: looks up `sales`, `stores`, `store_id`, `region`, `amount` in the catalog; fails if one is missing or ambiguous.
> - Optimizer: pushes `region = 'North'` below the join onto `stores` (it only uses `stores` columns), prunes unused columns so only `store_id`, `amount`, `region` are read, and pushes the filter into the Parquet scan if possible.
> - Physical planning: if the filtered `stores` is small, chooses a broadcast hash join (no shuffle of `sales`); otherwise a sort-merge join with shuffles on `store_id`.
> - Execution: whole-stage code generation fuses scan, filter and project into compiled code.

> [!example]- **5.** *(Hard) Replace a Python UDF*
> A pipeline uses a Python UDF `clean(s)` that trims a string, upper-cases it and replaces empty strings with null, on 2 billion rows. Explain why it is slow and rewrite it with built-in functions.
>
> ---
> Each row is serialized from the JVM to a Python worker and back, the function runs row by row in Python, and Spark cannot optimize or code-generate it; Python memory also competes with the executor JVM.
> ```python
> from pyspark.sql.functions import trim, upper, when, col
> cleaned = upper(trim(col("s")))
> df = df.withColumn("s_clean", when(cleaned == "", None).otherwise(cleaned))
> ```
> Built-ins run inside the JVM, are visible to Catalyst and use code generation. If a UDF is unavoidable, use a pandas (vectorized) UDF or write it in Scala.

## 📝 Summary

- Structured APIs: DataFrames (all languages), Datasets (Scala/Java, typed), SQL tables/views; all compile to the same optimized plans.
- Define schemas explicitly for production; `nullable` is a hint, not a constraint.
- Columns and expressions describe computations; `select`, `selectExpr`, `withColumn`, `where`, `distinct`, `orderBy`, `union`, `sample`, `randomSplit`, `repartition`.
- `union` is positional; use `unionByName`.
- Use built-in functions for strings, dates, numbers, complex types, JSON; nulls follow three-valued logic and `na.drop`/`na.fill` handle them.
- Python UDFs are slow (row-by-row serialization); prefer built-ins, pandas UDFs or Scala.
- Catalyst: unresolved plan → analyzer (catalog) → optimized logical plan → cost-based physical plan → codegen execution.
- Spark SQL: ANSI + HiveQL; managed vs external tables (drop deletes data vs only metadata); session, global temp and persistent views; databases.

## ⚠️ Important Notes

1. DataFrames are immutable; every transformation returns a new DataFrame that you must assign.
2. In Python combine conditions with `&`, `|`, `~` and parentheses, not `and`/`or`.
3. `df.orderBy(expr("count desc"))` does not sort descending: the string parses as `count` aliased to `desc`. Use `desc("count")` or `col("count").desc()`.
4. `nullif(a, b)` returns a (not b) when they differ.
5. Unparseable dates and casts produce null silently; count nulls after parsing.
6. Dropping a managed table deletes its files.
7. Temp views disappear when the session ends; global temp views live in `global_temp`.
8. `distinct` and `orderBy` shuffle; `sortWithinPartitions` and `coalesce` don't.
9. A UDF without a declared return type returns strings in PySpark.
10. Schema inference on CSV may need an extra pass over the data and can guess types differently on different samples.

> [!warning] Gaps in the source material
> - DG's Python examples are Python 2 style (e.g. `5L` literals); examples here use Python 3.
> - **Errata in DG** (logged in [[00-Index]]): E4 `orderBy(expr("count desc"))` presented as a descending sort; E5 `nullif` described as returning the second value when values differ.
> - **Added by me:** `unionByName`, `eqNullSafe`, pandas UDFs, `explain(True)`, the null-logic and union exercises, and the Catalyst walk-through example.
> - Figures (Catalyst phases, expression trees, Python UDF process) are images; described in the text.

**Previous:** [[04 - RDDs, Key-Value Pairs and Shared Variables]] · **Next:** [[06 - Aggregations and Joins]]
