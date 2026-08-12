---
subject: Database Management Systems
chapter: 0
tags: [ds, dbms, index, moc, sql, relational-model, normalization, data-warehouse]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, Cengage 2023"
---

# Database Management Systems — Index

Map of Content for the subject. **Every chapter note is listed below with a one-line description and a status.**

## Course framing

**A database is the answer to a question that every other subject in this degree assumes has been answered: *where does the data come from?*** [[Data Preparation and Visualization/contents/00-Index|Data Preparation]] begins with a dataframe; [[Machine Learning/contents/00-Index|Machine Learning]] begins with features; [[Econometrics/contents/00-Index|Econometrics]] begins with a sample. **In practice all three begin with a `SELECT` statement**, and the quality of what follows is bounded by how the data was modelled and stored.

Three things make this subject worth real attention for a data scientist rather than treating SQL as a lookup table:

1. **Normalisation is applied logic, not a filing convention.** It is a formal theory of redundancy built on functional dependencies — relations in the [[Discrete Mathematics/contents/03 - Functions, Sequences and Relations|Discrete Maths]] sense. **Most "dirty data" problems are denormalisation happening upstream.**
2. **The database will out-perform your Python.** A join over millions of rows in the engine beats pulling both tables into pandas, and the reason is [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]]'s B-trees and [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|ch. 09]]'s hash tables. **Knowing *why* tells you when to push work down.**
3. **The star schema is the format analytics actually arrives in.** Warehouses, OLAP cubes and BI tools all assume it, and it is a *deliberate denormalisation* — which only makes sense once you know what normalisation was for.

> [!warning] Scope decision — needs confirming against the real syllabus
> **Coronel & Morris has 16 chapters and 17 appendices. This vault covers 11 chapters**, chosen as the standard scope for an undergraduate database course taken by a **data science** major rather than an IT-management one.
>
> **The bias is deliberate**: toward the relational model, normalisation, SQL depth, and the warehouse/OLAP material that connects to the rest of the degree — and away from administration, deployment and vendor-specific tooling. **This is my editorial judgement, not the lecturer's. Please check it against the syllabus and tell me what to add or drop.**

## Chapters

| # | Note | Source | Status | What it covers |
|---|---|---|---|---|
| 01 | [[01 - Databases and Data Models]] | C&M 1–2 | ✅ | Why databases exist: **file-system problems, data redundancy and anomalies**; the DBMS as a layer; the evolution of data models to relational |
| 02 | [[02 - The Relational Model and Relational Algebra]] | C&M 3 | ✅ | Relations, tuples, keys (super/candidate/primary/foreign); **integrity rules**; the eight relational-algebra operators — the formal basis of every SQL query |
| 03 | [[03 - Entity-Relationship Modelling]] | C&M 4–5 | ✅ | Entities, attributes, relationships; **cardinality and participation**; weak entities; EER extensions (specialisation, generalisation); mapping an ER model to tables |
| 04 | [[04 - Normalization]] | C&M 6 | ✅ | **Functional dependencies**; 1NF → 2NF → 3NF → **BCNF**; update/insert/delete anomalies; when and why to *denormalise* |
| 05 | [[05 - SQL Fundamentals]] | C&M 7 | ✅ | DDL and DML; `SELECT` and its clause order; filtering, `NULL` semantics, aggregation and `GROUP BY`; constraints |
| 06 | [[06 - Advanced SQL]] | C&M 8 | ✅ | All the **joins**; subqueries and correlated subqueries; set operators; **CTEs, recursive queries and window functions**; views |
| 07 | [[07 - Database Design]] | C&M 9 | ✅ | The design lifecycle: conceptual → logical → physical; requirements to schema; **design as a sequence of trade-offs** |
| 08 | [[08 - Transactions and Concurrency Control]] | C&M 10 | ✅ | **ACID**; the lost-update, dirty-read and phantom problems; locking, two-phase locking, deadlock; **isolation levels and what each permits** |
| 09 | [[09 - Query Optimization and Indexing]] | C&M 11 | ✅ | How a query is planned and executed; **B-tree and hash indexes**; `EXPLAIN`; why an index helps reads and costs writes |
| 10 | [[10 - Data Warehouses and OLAP]] | C&M 13 | ✅ | OLTP vs OLAP; **star and snowflake schemas**; facts and dimensions; slowly changing dimensions; roll-up, drill-down and `GROUP BY CUBE` |
| 11 | [[11 - Big Data and NoSQL]] | C&M 14 | ✅ | The relational model's limits; **CAP theorem**; key–value, document, column-family and graph stores; when *not* to use a relational database |

## What is not covered, and why

| Chapter | Why omitted |
|---|---|
| **12 — Distributed Database Management Systems** | Distributed-systems internals (fragmentation, replication protocols, two-phase commit) belong to a systems course. **The practically relevant part — the CAP theorem and eventual consistency — is folded into ch. 11.** |
| **15 — Database Connectivity and Web Technologies** | ODBC/JDBC/ADO.NET, web-to-database middleware, ColdFusion. **Vendor plumbing that dates quickly**; the data-science equivalent is a two-line `sqlalchemy` connection string. |
| **16 — Database Administration and Security** | Backup schedules, user provisioning, audit policy, disaster recovery. **A DBA's job, not an analyst's.** Worth reading if the syllabus includes it, but it teaches nothing about *data*. |
| **Appendices A–Q** (17 of them) | Vendor tutorials (MS Access, Oracle, Lucidchart, ColdFusion), superseded models (hierarchical, network, object-oriented), and UML. **Two are genuinely relevant — P (MongoDB) and Q (Neo4j) — and their ideas are absorbed into ch. 11 instead.** |

**If the syllabus differs, the likely mismatches are, in order:** (i) **ch. 16 security** — many courses require it; (ii) **ch. 12 distributed databases**, if the course is systems-flavoured; (iii) **ch. 15**, if there is a web-development component.

## Conventions for this subject

> [!note] Every query in these notes has been executed
> **This subject's analogue of the vault's verify-every-number rule is: run the SQL.** Every query shown was executed against a real SQLite database built for the purpose, and **the printed results are the actual output**, not the book's.
>
> *(Verified available: **SQLite 3.50.4**, with window functions, CTEs and recursive queries — so no query in the scope has to be presented untested.)*
>
> **Where a query relies on something SQLite lacks** — `FULL OUTER JOIN` in older versions, Oracle/SQL Server-specific syntax, materialised views — **that is stated explicitly** rather than shown as if it ran.

- **Schema diagrams are text.** Every ER diagram in the source is an image and is lost (see below), so relationships are given as tables and as `CREATE TABLE` statements with real foreign keys — which is more precise than a diagram and can be executed.
- **Cross-subject links are used heavily.** This subject sits between [[Discrete Mathematics/contents/00-Index|Discrete Maths]] (relations, functional dependency) and [[Data Structures and Algorithms/contents/00-Index|DSA]] (B-trees, hashing, sorting) on one side, and [[Data Preparation and Visualization/contents/00-Index|Data Preparation]] and [[MLOps/contents/00-Index|MLOps]] on the other.

## The Data Structures and Algorithms boundary

[[Data Structures and Algorithms/contents/00-Index|DSA]] is **complete**, and it already contains the mechanisms this subject depends on. **Cross-link rather than re-derive:**

| Topic | Proved/measured in DSA | Used here |
|---|---|---|
| **B-trees and the block-transfer cost model** | [[Data Structures and Algorithms/contents/10 - Search Trees\|ch. 10]] §7 — *why* $O(\log_B n)$ I/O beats $O(\log_2 n)$; measured 30 seeks vs 3 for $10^9$ records | **ch. 09** — this is what a database index *is* |
| **Hash tables, load factors, collisions** | [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists\|ch. 09]] | **ch. 09** — hash indexes and hash joins |
| **External merge-sort** | [[Data Structures and Algorithms/contents/11 - Sorting and Selection\|ch. 11]] | **ch. 09** — `ORDER BY` and sort-merge joins on data exceeding memory |
| **Why ordered structures beat hashing for ranges** | [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists\|ch. 09]] §8, [[Data Structures and Algorithms/contents/10 - Search Trees\|ch. 10]] | **ch. 09** — why `BETWEEN` can use a B-tree index but not a hash index |
| **Relations, functional dependency** | [[Discrete Mathematics/contents/03 - Functions, Sequences and Relations\|DM ch. 03]] | **ch. 02, 04** — the formal basis of the relational model and of normalisation |

## Errata

*(Empty so far — populated as errors are found and verified.)*

| Chapter | Location | Book says | Should be | Verified by |
|---|---|---|---|---|

## Source and its gaps

**Coronel & Morris, *Database Systems: Design, Implementation, & Management*** (Cengage 2023), 818 pages, 16 chapters. **No lecture slides.**

> [!warning] Known limitations of this source
> **It is a business-school text** — long on process, methodology and industry context, **short on theory.** Two consequences, both handled by enrichment that is labelled as such in each chapter's gaps callout:
>
> - **Relational algebra is thin.** Ch. 02 develops it properly, because it is what makes SQL comprehensible rather than memorisable.
> - **NoSQL gets one late chapter** written largely as industry survey. Ch. 11 adds the CAP theorem and the actual data models a DS reader needs.
>
> **Extraction is clean** — real prose, no glyph substitution, no mangled identifiers. *(Verified on sample pages.)* **Book page $n$ = PDF page $n+28$.**
>
> **Every ER diagram, schema diagram and table figure is an image and is lost.** This is **severe for ch. 03 and ch. 10**, where the diagram genuinely *is* the content. The response is to give schemas as executable `CREATE TABLE` statements and relationships as tables, and to **flag rather than silently reconstruct** anything the surrounding prose does not fully determine.

**Previous:** *(start of subject)* · **Next:** [[01 - Databases and Data Models]]
