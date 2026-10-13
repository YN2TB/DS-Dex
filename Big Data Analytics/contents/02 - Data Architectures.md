---
subject: Big Data Analytics
chapter: 2
tags: [ds, big-data, data-warehouse, data-lake, lakehouse, data-mesh, governance, acid]
source: "User's course notes (note/2.md, note/3.md); standard data-engineering material (no textbook in the folder)"
---

# Data Architectures

How organizations store and serve data for analytics: the data warehouse, the data lake, the lakehouse that combines them, and data mesh as an organizational alternative. Also governance and ACID.

## 📘 Main Knowledge

### 1. Data warehouse (DWH)

A centralized, structured repository optimized for BI, reporting and SQL analytics.

- **Schema-on-write**: the table structure is defined before loading; data that does not fit is rejected or cleaned first.
- Loaded by **ETL** (extract, transform, load).
- Stores cleaned, integrated, historical data; optimized for reading and aggregating (OLAP), not for many small updates (OLTP).
- Usually modelled as a **star schema**: a central fact table (e.g. sales: date_id, store_id, product_id, quantity, revenue) joined to dimension tables (date, store, product). A **snowflake schema** normalizes the dimensions further.

**OLTP vs OLAP**

| | OLTP (operational DB) | OLAP (warehouse) |
|---|---|---|
| workload | many small reads/writes | few large scans and aggregations |
| example | insert an order | revenue by region by month |
| design | normalized | denormalized (star schema) |
| data | current | historical |

#### Warehouse tiers (from the user's notes)

| Architecture | Structure | Notes |
|---|---|---|
| One-tier | users query the database directly | simple, but messy results and slow; rarely used at scale |
| Two-tier | a **data mart** layer between the warehouse and users | each department gets a smaller, subject-specific mart |
| Three-tier | bottom: warehouse database; middle: OLAP server/cubes; top: BI and reporting tools | the classic enterprise design |

#### OLAP cubes

An OLAP cube stores a measure (e.g. revenue) indexed by several dimensions (time, store, product), plus precomputed subtotals. Typical operations: **roll-up** (aggregate to a coarser level, month → year), **drill-down** (the reverse), **slice** (fix one dimension), **dice** (select a sub-cube), **pivot** (rotate the view). Spark's `rollup` and `cube` produce the same subtotals ([[06 - Aggregations and Joins]]).

### 2. Data lake

A store for raw data of any type (structured, semi-structured, unstructured) in its original format, usually on cheap object storage (HDFS, S3, ADLS).

- **Schema-on-read**: structure is applied when the data is queried.
- Cheap and flexible; good for data science and ML on raw data.
- Risk: without governance it becomes a **data swamp**: nobody knows what is there, whether it is correct, or who owns it.
- Plain files give no transactions: concurrent writers can corrupt tables, and readers can see half-written data.

### 3. ETL vs ELT

| | ETL | ELT |
|---|---|---|
| order | transform before loading | load raw, transform inside the target system |
| where transformation runs | separate ETL server/tool | the warehouse/lake engine (Spark, BigQuery, Snowflake) |
| schema | schema-on-write | often schema-on-read |
| raw data kept? | usually not | yes, can re-transform later |
| fits | classic warehouses, strict data quality, sensitive data removed before loading | cloud warehouses and lakes with cheap storage and scalable compute |

ELT became common once storage got cheap and engines like Spark could transform data at scale where it lives.

### 4. Lakehouse

A lakehouse keeps data in open file formats on cheap lake storage (e.g. Parquet) but adds warehouse features through a **table format** layer such as **Delta Lake**, **Apache Iceberg** or **Apache Hudi**:

- ACID transactions on files (via a transaction log);
- schema enforcement and schema evolution;
- time travel (query older versions);
- efficient updates, deletes and merges;
- one copy of data for BI, SQL and ML.

| | Warehouse | Lake | Lakehouse |
|---|---|---|---|
| data types | structured | any | any |
| schema | on write | on read | enforced, can evolve |
| transactions | yes | no | yes |
| cost | high | low | low |
| main users | BI analysts | data scientists | both |

### 5. Data governance

- **Data lineage**: tracking where data came from, how it was transformed and where it is used. Needed for debugging, audits and impact analysis. Tool example: Apache Atlas.
- **Data catalog / discovery**: a searchable inventory of datasets with schema, owner, freshness, quality and lineage, "Google search for your organization's data." Tools: Apache Atlas (Hadoop), AWS Glue Data Catalog. An analyst searching for "customer transactions" can find the table, read its schema (`customer_id`, `purchase_amount`), check when it was last updated and its quality score, and view its lineage.
- Also: access control (RBAC), encryption, data quality checks, retention policies.

### 6. ACID and why HDFS lacks it

| Property | Meaning |
|---|---|
| Atomicity | a transaction completes fully or not at all |
| Consistency | the database moves from one valid state to another (constraints hold) |
| Isolation | concurrent transactions do not see each other's partial work |
| Durability | committed changes survive crashes |

HDFS was built for batch analytics, not transactions (from the user's notes):

- **Atomicity**: no row-level updates; you can only append to or replace whole files.
- **Consistency**: write once, read many; no constraint checking.
- **Isolation**: readers may see incomplete files while a job is writing.
- **Durability**: data is replicated, but transactional guarantees need extra layers (Hive ACID tables, HBase, or a lakehouse table format).

See [[Database Management Systems/contents/00-Index|Database Management Systems]] for transactions in relational systems.

### 7. Data mesh

A decentralized, organizational approach: instead of one central data team owning all pipelines, each business domain owns its data and publishes it as a product. Aims: remove the central-team bottleneck and siloed ownership, deliver data faster.

Four principles:

1. **Domain-oriented ownership**: the team that produces the data (e.g. payments) owns its analytical data.
2. **Data as a product**: documented, discoverable, trustworthy, with an owner, SLAs and API access.
3. **Self-serve data infrastructure**: a platform team provides storage, pipelines, catalogs and governance tools so domains do not depend on central IT.
4. **Federated governance**: shared standards for security, compliance and interoperability, applied automatically (e.g. lineage tracking, policies as code).

Implementation steps (user's notes): identify domains and dataset owners → build documented data products with APIs → deploy self-service tools (catalog, ETL framework, query engine) → enforce federated governance (RBAC, encryption, lineage) → enable cross-domain access with **data contracts** (agreed schemas, SLAs, expectations).

Data mesh is about organization, not a specific technology; a mesh can be built on a lakehouse.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Warehouse, lake or lakehouse?*
> (a) Finance needs audited monthly revenue reports with fixed definitions. (b) Data scientists want raw clickstream JSON and product images for experiments. (c) A company wants BI dashboards and ML on the same data, with updates and deletes for GDPR requests, on cheap storage.
>
> ---
> (a) Warehouse (or the curated layer of a lakehouse): schema-on-write, consistent definitions. (b) Data lake: raw, varied data, schema-on-read. (c) Lakehouse: ACID updates/deletes plus open formats on cheap storage, one copy for BI and ML.

> [!example]- **2.** *(Easy–medium) ETL or ELT?*
> Choose and justify: (a) a hospital must remove patient identifiers before data reaches the analytics platform; (b) a startup loads app events into BigQuery and analysts keep changing their transformations.
>
> ---
> (a) ETL: sensitive fields must be removed before loading. (b) ELT: load raw events once, transform in the warehouse, and re-run transformations as requirements change.

> [!example]- **3.** *(Medium) Cube size*
> A sales cube has dimensions month (36 values), store (50) and product (1,000). (a) How many base cells? (b) If each dimension also has an "all" level for subtotals (as in a full cube), how many cells? (c) How many grouping combinations (cuboids) does a full cube over 3 dimensions have?
>
> ---
> (a) $36\times50\times1000=1{,}800{,}000$.
>
> (b) $(36+1)(50+1)(1000+1)=1{,}888{,}887$, i.e. 88,887 extra subtotal cells.
>
> (c) Each dimension is either grouped or not: $2^3=8$ cuboids (from the grand total to the full detail). `rollup` gives only the hierarchical prefixes (4 here); `cube` gives all 8.

> [!example]- **4.** *(Medium–hard) Which ACID property fails?*
> On plain HDFS/Parquet files: (a) a Spark job writing 200 files crashes after 120; (b) a dashboard reads a table while a job is overwriting it and shows mixed old and new rows; (c) you need to correct one customer's email.
>
> ---
> (a) Atomicity: a partial write is left behind. (b) Isolation: readers see uncommitted work. (c) No row-level update: you must rewrite the whole file or partition. A lakehouse table format fixes all three with a transaction log: a write is committed only when its log entry is written, and readers use the last committed version.

> [!example]- **5.** *(Hard) Design a data mesh*
> An e-commerce company has domains Orders, Payments and Marketing. Marketing needs daily order data joined with campaign data. Using the four principles, describe who owns what, what the Orders data product must provide, and what goes in the data contract.
>
> ---
> - Ownership: Orders team owns the orders data product; Marketing owns campaigns and its joined analysis.
> - The orders product: a documented, discoverable table (e.g. a Delta/Iceberg table) listed in the catalog, with owner, schema (`order_id`, `customer_id`, `order_ts`, `amount`, `campaign_code`), freshness SLA (e.g. complete by 06:00 daily), quality checks and lineage.
> - Self-serve platform: storage, scheduling (e.g. Airflow, [[10 - Workflow Orchestration with Airflow]]), catalog and access control provided centrally.
> - Federated governance: `customer_id` is pseudonymized by a shared policy; Marketing gets read access through RBAC.
> - Data contract: schema and types, meaning of each field, allowed nulls, update schedule, how breaking changes are announced (versioning), and who to contact.

## 📝 Summary

- Warehouse: structured, schema-on-write, ETL, star schemas, OLAP; one/two/three-tier designs; cubes support roll-up, drill-down, slice, dice, pivot.
- Lake: raw data of any type on cheap storage, schema-on-read; risk of a data swamp and no transactions.
- ETL transforms before loading; ELT loads raw and transforms in the engine.
- Lakehouse: lake storage + table format (Delta, Iceberg, Hudi) giving ACID, schema enforcement, time travel.
- Governance: lineage, catalogs, access control, quality.
- ACID: atomicity, consistency, isolation, durability; plain HDFS provides none of them as transactions.
- Data mesh: domain ownership, data as a product, self-serve platform, federated governance; an organizational model.

## ⚠️ Important Notes

1. Schema-on-write vs schema-on-read is the key difference between warehouse and lake.
2. A data mart is a subset of a warehouse for one department, not a separate kind of system.
3. OLAP and OLTP need different designs; running heavy analytics on the operational database slows the business.
4. Replication in HDFS gives durability of blocks, not transactional durability or atomicity.
5. Delta Lake, Iceberg and Hudi are table formats on top of files, not new storage systems.
6. ELT keeps raw data, so mistakes in transformations can be fixed by re-running them.
7. A data lake without a catalog and owners becomes a data swamp.
8. Data mesh does not remove central work; the platform and governance standards are still shared.
9. Data contracts make schema changes explicit; without them, upstream changes silently break downstream jobs.

> [!warning] Gaps in the source material
> - Neither book in `documents/` covers this chapter. Content follows the user's notes (`2.md`, `3.md`), several sections of which are unfinished (ETL vs ELT table, lakehouse, isolation).
> - **Added by me** (standard material): OLTP vs OLAP, star/snowflake schemas, cube operations, data swamp, Delta/Iceberg/Hudi features, the comparison tables and all exercises.

**Previous:** [[01 - Big Data and Distributed Computing]] · **Next:** [[03 - Spark Architecture and Execution]]
