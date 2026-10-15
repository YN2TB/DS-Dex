# Big Data Analytics

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Sources

| Book | File | Notes |
|---|---|---|
| Chambers & Zaharia, *Spark: The Definitive Guide* (O'Reilly 2018, Spark 2.2) — "DG" | `documents/Spark-The Definitive Guide.pdf`, 601 p. | main source; outline page numbers = PDF pages |
| Karau, Konwinski, Wendell & Zaharia, *Learning Spark* (O'Reilly 2015, Spark 1.x) — "LS" | `documents/Learning Spark  Lightning-Fast Big Data Analysis .pdf`, 274 p. | RDD-era; used for RDDs, pair RDDs, cluster runtime, old Streaming |

User material in `note/`: `Overview.md` (mid-term: Big Data platform, Airflow, Kafka, message bus; final: PySpark), `1.md`–`3.md` (5V, Hadoop/HDFS/MapReduce, history, DWH tiers, OLAP, lake, ETL/ELT, lakehouse, governance, ACID, data mesh, Spark concepts), `Project explaination.md` (their Spark ML project: scaling, log transform, PCA via computeSVD, ElasticNet, Poisson GLM/IRLS). Don't edit `note/`.

## Extraction

- DG: text extracts fine but inline code splits lines; join lines when extracting (replace single newlines with spaces). Code listings come out as one flattened line with spaces around operators.
- LS: extracts cleanly; uses `‐` soft hyphens at line ends ("sup‐ port").
- Figures are images.
- Neither book covers Airflow, data warehouses/lakehouses or data mesh; ch. 02 and 10 are built from the user's notes plus standard knowledge and are labelled as such.

## Errata

E1–E3 in LS, E4–E6 in DG: details in `contents/00-Index.md`. The user's `2.md` says Spark was open-sourced in 2012; LS says March 2010 (Apache in June 2013, top-level 2014). Recorded in ch. 01, not an erratum against the books.

## Open items

- Scope (12 chapters) is my choice, from the user's `Overview.md` and notes: confirm with the lecturer.
