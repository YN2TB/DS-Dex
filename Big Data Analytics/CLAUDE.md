# CLAUDE.md — Big Data Analytics

Subject context. Read with the root `CLAUDE.md`.

## Status

✅ Complete (2026-10-09): `00-Index.md` + ch. 01–12. 6 errata (3 LS, 3 DG), listed in `00-Index.md`.

## Sources

| Book | File | Notes |
|---|---|---|
| Chambers & Zaharia, *Spark: The Definitive Guide* (O'Reilly 2018, Spark 2.2) — "DG" | `documents/Spark-The Definitive Guide.pdf`, 601 p. | main source; outline page numbers = PDF pages |
| Karau, Konwinski, Wendell & Zaharia, *Learning Spark* (O'Reilly 2015, Spark 1.x) — "LS" | `documents/Learning Spark  Lightning-Fast Big Data Analysis .pdf`, 274 p. | RDD-era; used for RDDs, pair RDDs, cluster runtime, old Streaming |

User material in `note/`: `Overview.md` (mid-term: Big Data platform, Airflow, Kafka, message bus; final: PySpark), `1.md`–`3.md` (5V, Hadoop/HDFS/MapReduce, history, DWH tiers, OLAP, lake, ETL/ELT, lakehouse, governance, ACID, data mesh, Spark concepts), `Project explaination.md` (their Spark ML project: scaling, log transform, PCA via computeSVD, ElasticNet, Poisson GLM/IRLS). Don't edit `note/`.

## Extraction

- DG: text extracts fine but inline code splits lines; join lines when extracting (`ext.py … j` in the scratchpad: replace single newlines with spaces). Code listings come out as one flattened line with spaces around operators.
- LS: extracts cleanly; uses `‐` soft hyphens at line ends ("sup‐ port").
- Figures are images.
- Neither book covers Airflow, data warehouses/lakehouses or data mesh; those chapters are built from the user's notes plus standard knowledge and are labelled as such.

## Scope (my choice, from the user's Overview + notes; confirm with the lecturer)

| # | Note | Main source | Status |
|---|---|---|---|
| 01 | Big Data and Distributed Computing | user notes; DG ch. 1; LS ch. 1 | ✅ |
| 02 | Data Architectures | user notes (no textbook) | ✅ |
| 03 | Spark Architecture and Execution | DG ch. 2, 15; LS ch. 2, 7, 8 | ✅ |
| 04 | RDDs, Key-Value Pairs and Shared Variables | LS ch. 3, 4, 6; DG ch. 12–14 | ✅ |
| 05 | DataFrames and Spark SQL | DG ch. 4–6, 10 | ✅ |
| 06 | Aggregations and Joins | DG ch. 7–8 | ✅ |
| 07 | Data Sources and File Formats | DG ch. 9; LS ch. 5 | ✅ |
| 08 | Running, Monitoring and Tuning Spark | DG ch. 16–19; LS ch. 7–8 | ✅ |
| 09 | Stream Processing and Kafka | DG ch. 20–23; LS ch. 10 | ✅ |
| 10 | Workflow Orchestration with Airflow | no source in folder | ✅ |
| 11 | MLlib: Pipelines and Feature Engineering | DG ch. 24–25; LS ch. 11 | ✅ |
| 12 | MLlib: Models, Evaluation and Tuning | DG ch. 26–29 | ✅ |

## Errata / discrepancies

E1–E3 in LS (outer-join descriptions swapped, broken Python lambda in Ex. 4-12, missing `10` in Ex. 4-16), E4–E6 in DG (`expr("count desc")` sorts ascending, `nullif` description, PolynomialExpansion counts). Details in `contents/00-Index.md`. Note: the user's `2.md` says Spark was open-sourced in 2012; LS says March 2010 (Apache in June 2013, top-level 2014). Recorded in ch. 01, not an erratum against the books.
