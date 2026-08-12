---
subject: Database Management Systems
chapter: 1
tags: [ds, dbms, data-models, anomalies, data-redundancy, abstraction, metadata, relational]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 1–2"
---

# Databases and Data Models

Every other subject in this degree starts *after* this one finishes. [[Data Preparation and Visualization/contents/00-Index|Data Preparation]] begins with a dataframe, [[Machine Learning/contents/00-Index|Machine Learning]] with a feature matrix, [[Econometrics/contents/00-Index|Econometrics]] with a sample. **This chapter is about where those come from, and why they are shaped as they are.**

The chapter's argument is a single one, and §3 demonstrates it by running it:

> **Storing the same fact in more than one place is not untidy — it is a structural defect that makes contradiction possible.** Everything else — normalisation, keys, the entire relational model — follows from taking that seriously.

**This is the practical link to data cleaning.** A large share of "dirty data" is not noise or measurement error; **it is somebody's schema permitting two versions of one fact.** §3 shows exactly how that happens, in a real database, in four lines of SQL.

## 📘 Main Knowledge

### 1. Data, information, and what a database actually stores

> [!note] The distinction the book leads with
> **Data** are raw, unprocessed facts. **Information** is data processed to reveal meaning. **Knowledge** is the body of information understood in a context.
>
> The chain is: *data → information → knowledge → decisions.* **Information is produced by processing data, so the quality of every decision is bounded by the quality of the data underneath it** — "garbage in, garbage out", which is the same point [[Data Preparation and Visualization/contents/00-Index|Data Preparation]] makes from the other end.

> [!note] Definitions
> A **database** is a shared, integrated computer structure that stores **end-user data** *and* **metadata** — data about the data.
>
> A **DBMS** (database management system) is the software layer between the user and the physical database. Applications never touch the files; they ask the DBMS.

**The metadata is the part that is easy to overlook and is what makes a database more than a pile of files.** It records each field's name, type, length, whether it may be empty, and how tables relate — held in the **data dictionary**. **Because the DBMS knows the structure, it can enforce it** — which is §5's point and the whole difference from a folder of CSVs.

### 2. What a file system cannot do

Databases evolved out of file systems, and the specific failures are worth naming because **they recur every time someone manages data in spreadsheets or loose CSVs.**

> [!note] Structural and data dependence
> **Structural dependence:** access to a file depends on its structure, so **changing the structure breaks every program that reads it.** Adding one column means editing every consumer.
>
> **Data dependence:** programs must know how the data is *physically stored* — its format and layout — so a change in physical storage breaks logical access.
>
> **A database provides structural and data *independence*:** you say *what* you want, and the DBMS decides *how* to get it. **This is why `SELECT` is declarative** — and why the engine is free to change its mind about indexes and join order ([[09 - Query Optimization and Indexing|ch. 09]]) without any query changing.

**Data redundancy** — the same fact stored in several files — produces what Coronel & Morris call **islands of information**: scattered stores that drift apart because nothing keeps them in step.

**Redundancy causes three specific failures**, and they are the heart of the chapter.

### 3. The three anomalies — demonstrated, not described

Here is a customer table in the file-system style, with each customer's agent details repeated inline. *(This is the actual output of a real SQLite database; every result below was executed.)*

```
    cust_id | cust_name       | agent_name   | agent_phone  | agent_area
    --------+-----------------+--------------+--------------+-----------
    1       | Amy B. O'Brian  | Leah F. Hahn | 615-882-2144 | 615
    2       | George Williams | Leah F. Hahn | 615-882-2144 | 615
    3       | Olette K. Smith | Leah F. Hahn | 615-882-2144 | 615
    4       | John T. Okon    | John T. Okon | 713-223-7745 | 713
    5       | Paul F. Olowski | Leah F. Hahn | 615-882-2144 | 615
```

**Leah Hahn's phone number is stored 4 times. It is one fact about one person.**

#### 3.1 The update anomaly

Change the number, but miss two rows — as any partial update, interrupted script or concurrent edit would:

```sql
UPDATE customer_flat SET agent_phone='615-999-0000'
WHERE agent_name='Leah F. Hahn' AND cust_id <= 2;
```

```
    agent_name   | agent_phone  | rows
    -------------+--------------+-----
    John T. Okon | 713-223-7745 | 1
    Leah F. Hahn | 615-882-2144 | 2
    Leah F. Hahn | 615-999-0000 | 2
```

**The database now asserts two different phone numbers for one person, and nothing in the schema forbids it.** *(Verified: 1 agent holding contradictory values.)* **Neither number is marked as wrong. There is no way to tell which is current.**

#### 3.2 The insertion anomaly

Record a new agent who has no customers yet:

```
INSERT INTO customer_flat (cust_id, cust_name) VALUES (99, NULL);
-> rejected: NOT NULL constraint failed: customer_flat.cust_name
```

**The agent cannot be recorded at all.** *(Verified.)* Agent data has no home of its own — it exists only as a passenger on a customer row. **To store the agent you must invent a fake customer**, and if the schema forbids that (as here), the fact is simply unstorable.

> [!note] This came out sharper than the book's version
> Coronel & Morris describe the insertion anomaly as *having to add a dummy customer entry*. **In a schema with a `NOT NULL` constraint on the customer's name, the insert is refused outright** — so the anomaly presents as an outright inability to record the fact rather than as a phantom row.
>
> **Both are the same defect**: the table conflates two independent things, so one cannot exist without the other. The stricter schema surfaces it earlier, which is an argument for constraints.

#### 3.3 The deletion anomaly

```
distinct agents before: 2   [John T. Okon, Leah F. Hahn]
DELETE FROM customer_flat WHERE cust_name='John T. Okon';
distinct agents after:  1   [Leah F. Hahn]
```

**Deleting one customer destroyed an agent's contact details.** *(Verified.)* **No error, no warning** — the operation succeeded exactly as asked, and unrelated information was silently lost.

> [!warning] Why the deletion anomaly is the most dangerous
> The update anomaly leaves contradictory data, which an audit can at least *detect*. **The deletion anomaly leaves no trace at all** — the data is gone, and nothing records that it ever existed.
>
> **All three come from one cause: the table stores facts about two different things.** Customers and agents are independent entities, and forcing them into one table means their lifecycles become entangled.

### 4. The fix, and what it costs

**Split the table so each fact lives in exactly one place**, joined by a **foreign key**:

```sql
CREATE TABLE agent (
    agent_id    INTEGER PRIMARY KEY,
    agent_name  TEXT NOT NULL,
    agent_phone TEXT NOT NULL,
    agent_area  TEXT
);
CREATE TABLE customer (
    cust_id   INTEGER PRIMARY KEY,
    cust_name TEXT NOT NULL,
    agent_id  INTEGER REFERENCES agent(agent_id)
);
```

**All three anomalies disappear** *(all verified):*

| | flat table | split tables |
|---|---|---|
| **update** the phone number | 4 rows to change; contradiction possible | **1 row**; contradiction **impossible** |
| **insert** an agent with no customers | rejected outright | **ordinary insert** |
| **delete** a customer | **agent data destroyed** | agents before 3, after 3 — **survives** |

> [!note] It costs nothing in what you can see
> ```
>     cust_name       | agent_name   | agent_phone
>     ----------------+--------------+-------------
>     Amy B. O'Brian  | Leah F. Hahn | 615-999-0000
>     George Williams | Leah F. Hahn | 615-999-0000
>     ...
> ```
> **A join reconstructs the original flat view on demand** *(verified)*. **Normalisation does not remove any question you could ask — it only removes the ability to be inconsistent.**
>
> **What it does cost is join work at query time**, which is why [[10 - Data Warehouses and OLAP|ch. 10]]'s star schemas deliberately denormalise for analytics. **That is a considered trade, not a relapse** — and it is only safe once you know precisely what you are giving up.

### 5. The DBMS *enforces* the structure

Splitting the tables is not merely tidier — **the schema now actively rejects invalid data:**

```
INSERT INTO customer VALUES (6,'Ghost Customer', 999);   -- no agent 999 exists
-> FOREIGN KEY constraint failed
```

*(Verified.)* **In the flat table nothing could have prevented the equivalent nonsense.** This is the real argument for a database over a folder of files: **correctness is guaranteed by the structure rather than by every program that touches it remembering to check.**

> [!warning] SQLite gotcha, verified
> **SQLite parses `REFERENCES` but ignores it unless foreign keys are switched on — and they are OFF by default, per connection.**
> ```
> PRAGMA foreign_keys        -> (0,)      <- default: NOT enforced
> PRAGMA foreign_keys = ON   -> (1,)
> ```
> *(Verified on SQLite 3.50.4.)* **So a schema full of foreign keys can silently enforce nothing.** PostgreSQL and MySQL/InnoDB enforce them by default. **Check the pragma before trusting an SQLite schema** — this is a genuine source of corrupt data in Python projects, where each new `sqlite3.connect()` starts fresh with enforcement off.

### 6. What a DBMS provides

Beyond storage, the DBMS supplies:

- **Data dictionary management** — the metadata, so structure is known and enforceable.
- **Data storage management**, including performance structures like indexes ([[09 - Query Optimization and Indexing|ch. 09]]).
- **Transformation and presentation** — the logical/physical separation of §2.
- **Security management** — who may see and change what.
- **Multi-user access control** — concurrency without corruption ([[08 - Transactions and Concurrency Control|ch. 08]]).
- **Backup and recovery**, **integrity management** (§5), **a query language** (SQL), and **communication interfaces**.

**The database system as a whole is five components: hardware, software, people, procedures, and data** — Coronel & Morris's framing, and worth remembering because **most database failures in practice are procedural, not technical.**

### 7. Data models and their building blocks

> [!note] Definition
> A **data model** is a relatively simple abstraction of a complex real-world structure — a representation of *what* the data means, used to communicate between designers, programmers and end users.

**Four building blocks:**

| | |
|---|---|
| **Entity** | a thing about which data is collected (a customer, an agent) — a *table* |
| **Attribute** | a characteristic of an entity (a phone number) — a *column* |
| **Relationship** | an association among entities: **1:1, 1:M, M:N** |
| **Constraint** | a restriction on the data (a GPA must lie in $[0,4]$; a phone number must exist) |

**Relationships and constraints come from *business rules*** — brief, precise descriptions of a policy or procedure in the organisation. *"An agent serves many customers; each customer has one agent"* is a business rule, and it is what determines the 1:M relationship implemented by §4's foreign key.

> [!note] Business rules are where design actually starts
> **The schema is a formalisation of the rules, so getting the rules wrong makes every downstream decision wrong**, however elegant the SQL. Nouns tend to become entities, verbs tend to become relationships.
>
> **And the rules are not derivable from the data** — only people who know the organisation can supply them. This is why [[07 - Database Design|ch. 07]] treats requirements-gathering as the first real step.

### 8. The evolution of data models

| era | model | contribution / limitation |
|---|---|---|
| 1960s | **Hierarchical** | Data as a tree, parent-to-child. **Fast for 1:M, but cannot represent M:N** and navigation is manual. |
| 1970s | **Network** | Allowed a record many owners, so M:N worked. **Still navigational** — the programmer traverses pointers by hand. |
| **1970 →** | **Relational** (Codd) | **Data as tables of rows and columns, related by *values* rather than pointers.** Structural and data independence at last, plus a declarative query language. |
| 1976 → | **Entity Relationship** | Not a storage model but a *design* notation — graphical, and it maps directly to relational tables ([[03 - Entity-Relationship Modelling|ch. 03]]). |
| 1980s–90s | **Object-oriented**, then **object/relational**, **XML** | Richer types, inheritance, semi-structured data. Mostly absorbed into relational systems as extensions. |
| **2000s →** | **NoSQL / Big Data** | Key–value, document, column-family, graph. **Trade the relational guarantees for scale and schema flexibility** ([[11 - Big Data and NoSQL|ch. 11]]). |

> [!note] The one that mattered
> **Codd's insight in 1970 was that relationships should be expressed by matching *values*, not by following stored pointers.** The hierarchical and network models made the programmer navigate the structure by hand — so the program encoded the physical layout, and §2's dependence problems were unavoidable.
>
> **Matching on values means the *system* can find the connection**, which is what makes a query declarative and what makes [[09 - Query Optimization and Indexing|optimisation]] possible: the engine may choose any strategy that yields the right values. **That single change is why the relational model won and why it has survived every successor.**
>
> **It also gives the model a mathematical foundation** — relations in the [[Discrete Mathematics/contents/03 - Functions, Sequences and Relations|Discrete Maths]] sense — which is what [[02 - The Relational Model and Relational Algebra|ch. 02]] develops.

### 9. Degrees of data abstraction

The ANSI/SPARC framework, and the reason a schema change need not break everything:

| level | what it describes | who sees it |
|---|---|---|
| **External** | one user group's view of the data — several per database | end users, applications |
| **Conceptual** | the whole database, logically — the **ER model** lives here | designers; DBMS-independent |
| **Internal** | the conceptual model mapped to a *specific* DBMS | the DBA |
| **Physical** | how bytes are actually stored and accessed | the storage engine |

> [!note] Why the layering earns its keep
> **Each level is insulated from changes below it.** Re-index a table, move it to a different disk, or switch storage engines — **the physical level changes and no query needs rewriting.** That is §2's data independence, made structural.
>
> **The conceptual level is the one to care about as a designer**, because it is DBMS-independent: an ER model is not committed to PostgreSQL or Oracle. **The external level is the one to care about as an analyst** — a view exposing exactly the columns you need, which is [[06 - Advanced SQL|ch. 06]]'s `CREATE VIEW`.

## ✏️ Exercises

**1. (Foundations.)** (a) Distinguish data, information and knowledge. (b) What is metadata and why does it matter? (c) Define structural and data dependence. (d) Why is `SELECT` declarative, and what does that buy?

> [!example]- Solution
> **(a) Data are raw facts; information is processed data that reveals meaning; knowledge is information understood in context.**
>
> A list of exam marks is data. *"The mean is 6.2 and 40% failed"* is information. *"This cohort is weaker than last year's, so the syllabus needs changing"* is knowledge.
>
> **The practical consequence is the direction of dependence: information cannot be better than the data beneath it.** No analysis recovers a fact that was never recorded, or corrects one that was recorded two contradictory ways (§3.1).
>
> **(b) Metadata is data about the data** — field names, types, lengths, nullability, keys, and how tables relate — held in the **data dictionary**.
>
> **It matters because it is what lets the DBMS enforce anything.** A folder of CSVs has no idea that `agent_id` in one file refers to a row in another, so it cannot object when the reference is invalid. **A database knows, and refuses** *(verified in §5: `FOREIGN KEY constraint failed`)*.
>
> **It is also what makes a database self-describing** — you can ask a database what it contains, which is how tooling, migrations and ORMs work at all.
>
> **(c) Structural dependence: access to a file depends on its structure**, so changing the structure breaks every program that reads it. **Data dependence: programs must know the physical storage format**, so a storage change breaks logical access.
>
> **Both mean a change in one place forces changes everywhere else**, and both make a system progressively harder to modify — the practical reason file-based data management collapses as an organisation grows.
>
> **A database gives independence at both levels** (§9): add a column, add an index, or move the file, and existing queries keep working.
>
> **(d) Because you state *what* you want, not *how* to get it.** `SELECT name FROM customer WHERE agent_id = 3` names a result, never a procedure — no loops, no file handles, no index choices.
>
> **What it buys is threefold.** **Independence:** the engine can change its strategy freely, so adding an index speeds queries up without editing them ([[09 - Query Optimization and Indexing|ch. 09]]). **Optimisation:** the engine knows table sizes and index availability and can pick a better plan than a hand-written loop. **Brevity:** a join is one clause instead of a nested loop.
>
> **This is the direct descendant of Codd's value-matching insight** (§8): if relationships are found by matching values rather than by following pointers, the *system* can do the finding — and then it can choose *how*.

**2. (Hard — the anomalies.)** (a) Name the common cause. (b) Explain each, using the verified output. (c) Why is the deletion anomaly the most dangerous? (d) The book says insertion needs a dummy row, but my test was rejected outright — reconcile.

> [!example]- Solution
> **(a) One table storing facts about two independent entities.**
>
> The flat table mixes customer facts (`cust_name`) with agent facts (`agent_name`, `agent_phone`, `agent_area`). **Since agents serve many customers, agent facts are repeated once per customer** — Leah Hahn's number stored 4 times *(verified)* — and **their lifecycle becomes tied to customers'**, which is exactly what should not be true of independent things.
>
> **Redundancy is the mechanism; entangled lifecycles are the cause.**
>
> **(b)**
>
> **Update anomaly** — changing a repeated fact requires changing every copy, and any partial update leaves contradictions:
> ```
> Leah F. Hahn | 615-882-2144 | 2 rows
> Leah F. Hahn | 615-999-0000 | 2 rows
> ```
> *(Verified: 1 agent with contradictory values.)* **The database asserts two incompatible facts, and neither is marked wrong.** Partial updates are not hypothetical — an interrupted script, a `WHERE` clause that is subtly too narrow, or two concurrent sessions ([[08 - Transactions and Concurrency Control|ch. 08]]) all produce them.
>
> **Insertion anomaly** — an agent with no customers cannot be recorded, because agent data has no home of its own *(verified: rejected by `NOT NULL`)*. **You cannot record a real fact about the world**, which is a failure of the model, not of the data.
>
> **Deletion anomaly** — deleting a customer destroyed an agent: `distinct agents before: 2 → after: 1` *(verified)*. **Information about one entity was lost by an operation on a different one.**
>
> **(c) Because it is silent and irreversible, while the other two leave evidence.**
>
> The **update** anomaly leaves contradictory rows, and a query like `GROUP BY agent_name HAVING COUNT(DISTINCT agent_phone) > 1` finds them — the corruption is *detectable*, which is how data-quality checks work. The **insertion** anomaly announces itself immediately: the insert fails or you notice the phantom row.
>
> **The deletion anomaly leaves nothing.** The `DELETE` succeeded exactly as written, no error was raised, and afterwards **nothing records that the agent ever existed.** You cannot detect it by inspecting the database, because a database that never held the fact looks identical to one that lost it.
>
> **You would only discover it later, when the fact is needed and cannot be found** — and by then the backup window has probably closed. **A failure you can detect is a much smaller problem than one you cannot.**
>
> **(d) Both are the same defect; the constraint changes how it surfaces.**
>
> Coronel & Morris assume a permissive schema, so you *can* insert a row with a real agent and a blank customer — giving a phantom row that pollutes every count and every join.
>
> **My schema declared `cust_name TEXT NOT NULL`, so the insert was refused: `NOT NULL constraint failed`.** The fact simply cannot be stored.
>
> **The underlying defect is identical** — agent data has no independent existence — but the observable symptom differs: **silent pollution in the permissive schema, an outright error in the strict one.**
>
> **Two conclusions.** **The stricter schema is better**, because it converts a silent data-quality problem into a loud failure at the moment of the mistake — the general principle that **constraints turn corruption into errors**, and errors are cheaper. **And a textbook's description of a symptom is contingent on its assumed schema**, which is a good reason to reproduce these things rather than read them.

**3. (Normalisation's cost, and models.)** (a) What did splitting the tables cost in expressiveness? (b) So why does anyone denormalise? (c) Why did the relational model displace hierarchical and network? (d) What are business rules and why can't they be inferred from data?

> [!example]- Solution
> **(a) Nothing.** *(Verified — a join reproduces the original flat view exactly:)*
> ```
>     cust_name       | agent_name   | agent_phone
>     ----------------+--------------+-------------
>     Amy B. O'Brian  | Leah F. Hahn | 615-999-0000
> ```
> **Every question answerable against the flat table is answerable against the split ones.** What was removed is not information but **the *ability to be inconsistent*** — the split schema cannot represent two phone numbers for one agent, because there is only one row in which to put one.
>
> **This is the key insight about normalisation: it restricts the set of representable *states*, not the set of answerable questions.** The states it forbids are exactly the contradictory ones.
>
> **(b) Because the join is not free.** Reconstructing the flat view costs work at query time, and on large tables joins are the dominant cost.
>
> **The trade is: normalised schemas optimise for *writing* correctly; denormalised schemas optimise for *reading* quickly.**
>
> **This is why [[10 - Data Warehouses and OLAP|ch. 10]]'s star schemas are deliberately denormalised.** A warehouse is written once by a controlled ETL process and read constantly by analysts — **so the update anomaly is largely prevented by process rather than by structure, and the join cost is paid on every query.** Under those conditions denormalisation is correct.
>
> **The conditions matter.** It is safe when writes are few, controlled and batched; it is dangerous in a transactional system where many users update concurrently. **Denormalising an OLTP schema for speed is one of the standard ways to create the anomalies of §3** — and note the distinction only makes sense if you know what normalisation was protecting, which is why [[04 - Normalization|ch. 04]] comes before ch. 10.
>
> **(c) Because relationships are expressed by matching *values* rather than by following stored pointers.**
>
> Hierarchical and network models were **navigational**: the programmer traversed pointers by hand, so **the program encoded the physical structure** and §2's dependence problems were unavoidable — change the structure, rewrite the programs.
>
> **Matching on values means the system can find the connection**, with three consequences:
> 1. **Declarative queries** — state the result, not the route (Exercise 1(d)).
> 2. **Optimisation becomes possible** — any strategy producing the right values is legal, so the engine may choose ([[09 - Query Optimization and Indexing|ch. 09]]).
> 3. **A mathematical foundation** — tables are relations in the [[Discrete Mathematics/contents/03 - Functions, Sequences and Relations|Discrete Maths]] sense, which gives relational algebra ([[02 - The Relational Model and Relational Algebra|ch. 02]]) and lets correctness be *proved*.
>
> **The hierarchical model also could not represent M:N relationships at all** — a genuine expressive limitation, not just an inconvenience.
>
> **(d) A business rule is a brief, precise description of a policy, procedure or principle in the organisation** — *"an agent serves many customers; each customer has exactly one agent"*. **Rules determine the relationships and constraints**, and hence the schema: that rule is what makes §4's foreign key correct.
>
> **They cannot be inferred from data because data shows what *has* happened, not what is *permitted*.**
>
> Suppose every customer in the current data has exactly one agent. **Does that mean a customer *may not* have two, or merely that none does yet?** The data cannot distinguish these, and they imply different schemas — one foreign key versus a junction table. **Choosing wrongly means either rejecting valid future data or permitting invalid data.**
>
> **Only people who know the organisation can settle it**, which is why [[07 - Database Design|ch. 07]] treats requirements-gathering as the first real design step, and why a database designed by inspecting a sample of data is unreliable. *(This is also a warning for data science: a pattern that holds in every row you have may be a rule, or may be an accident of the sample.)*

**4. (Hard — abstraction and enforcement.)** (a) Give the four levels and what each insulates. (b) Which matters to a designer, which to an analyst? (c) Explain the SQLite foreign-key finding and why it is dangerous. (d) What is the general principle about constraints?

> [!example]- Solution
> **(a)**
>
> | level | describes | insulates against |
> |---|---|---|
> | **External** | one user group's view | **schema changes elsewhere** — your view keeps working when unrelated tables change |
> | **Conceptual** | the whole database, logically; DBMS-independent | **choice of DBMS** — the design outlives the product |
> | **Internal** | the conceptual model in a specific DBMS | **physical storage decisions** |
> | **Physical** | actual bytes, files, access methods | — |
>
> **The point is that each level is written against the one below without depending on its details.** Re-index a table, move it to another disk, switch storage engines: **the physical level changes and not one query is rewritten.** That is data independence made structural rather than promised.
>
> **(b) A designer works at the conceptual level; an analyst lives at the external level.**
>
> **Conceptual, for the designer**, because it is DBMS-independent — an ER model ([[03 - Entity-Relationship Modelling|ch. 03]]) commits to no product, so the design survives a migration and can be discussed with people who do not write SQL. **Design decisions made at the internal level are decisions made too early.**
>
> **External, for the analyst**, because it is where a **view** exposes exactly the columns needed, with joins and filters already applied ([[06 - Advanced SQL|ch. 06]]). This gives a stable interface even when the underlying tables are restructured, hides columns the analyst should not see, and encodes the correct join logic once instead of in every query.
>
> **The layering is what makes it possible for a DBA to reorganise storage on Monday without any analyst noticing.**
>
> **(c) SQLite parses `REFERENCES` but does not enforce it unless `PRAGMA foreign_keys = ON`, and the default is OFF, per connection.**
> ```
> PRAGMA foreign_keys        -> (0,)
> PRAGMA foreign_keys = ON   -> (1,)
> ```
> *(Verified on SQLite 3.50.4. With it on, `INSERT INTO customer VALUES (6,'Ghost Customer',999)` was correctly rejected.)*
>
> **It is dangerous for three compounding reasons:**
> 1. **The schema *looks* correct.** `REFERENCES agent(agent_id)` is present, reviewed and approved — and enforces nothing.
> 2. **The failure is silent and cumulative.** Orphaned rows accumulate with no error, and are discovered much later as rows vanishing from inner joins.
> 3. **It is per connection, so it must be set every time.** **Every new `sqlite3.connect()` in a Python script starts with enforcement off** — so a codebase can be correct in the module that sets the pragma and unprotected everywhere else.
>
> **PostgreSQL and MySQL/InnoDB enforce foreign keys by default**, so the habit transfers badly in either direction — and the assumption "my schema declares it, therefore it holds" is false exactly where testing is most casual.
>
> **The general lesson: verify that a constraint is enforced, do not assume it from the DDL.** *(Which is this subject's run-the-SQL rule doing real work — reading the schema would have given the wrong answer.)*
>
> **(d) Constraints convert silent data corruption into loud, immediate errors — and errors are far cheaper than corruption.**
>
> Every example in this chapter fits the pattern:
>
> | without the constraint | with it |
> |---|---|
> | orphaned customer rows accumulate silently | `FOREIGN KEY constraint failed`, at the offending statement |
> | a phantom customer row pollutes counts and joins | `NOT NULL constraint failed`, immediately (§3.2) |
> | contradictory phone numbers persist undetected | the split schema **cannot represent** the contradiction |
>
> **Three reasons the error is better.** It arrives **at the moment of the mistake**, when the cause is obvious, instead of months later during analysis. It is **loud** — an exception, not a subtly wrong number. And it is **central**: the rule sits in the schema once, rather than in every application that touches the data, so it cannot be forgotten by one of them.
>
> **The deeper point is that this is what a database is *for*.** A file system stores bytes; **a DBMS stores facts and refuses to store non-facts.** §5's rejected insert is the whole argument for the subject in one line — and the strongest form of the principle is the last row of the table, where a good schema does not *detect* the contradiction but makes it **unrepresentable**.

## 📝 Summary

- **Data → information → knowledge → decisions.** Information cannot be better than the data beneath it, which is why schema quality is a data-science concern and not just an engineering one.
- **A database stores end-user data *and* metadata.** The metadata — the data dictionary — is what lets the DBMS *enforce* structure, and is the real difference from a folder of CSVs.
- **File systems suffer structural dependence** (changing structure breaks programs) **and data dependence** (physical format leaks into logical access). A database provides independence at both levels.
- **Redundancy — the same fact in several places — creates islands of information that drift apart.**
- **Three anomalies, all reproduced in a live database.** **Update:** a partial change left one agent with two contradictory phone numbers, with nothing in the schema forbidding it. **Insertion:** an agent with no customers could not be recorded at all. **Deletion:** removing one customer silently destroyed an agent (2 distinct agents → 1).
- **All three have one cause:** a table storing facts about two independent entities, which entangles their lifecycles.
- **The deletion anomaly is the most dangerous** because it is silent and leaves no evidence — the other two are at least detectable.
- **Splitting into two tables with a foreign key removed all three** *(verified: 1 row updated instead of 4; the new agent inserted normally; agents survived the delete)*.
- **Normalisation costs nothing in expressiveness** — a join reconstructs the flat view *(verified)*. **It restricts the representable states, not the answerable questions**, and the states it forbids are the contradictory ones.
- **It does cost join work at read time**, which is why [[10 - Data Warehouses and OLAP|ch. 10]]'s star schemas denormalise deliberately — safe when writes are few and controlled.
- **The DBMS enforces integrity:** a customer pointing at a non-existent agent was rejected with `FOREIGN KEY constraint failed`. **The flat table could not have prevented it.**
- **⚠️ SQLite ignores foreign keys unless `PRAGMA foreign_keys = ON`, and the default is OFF, per connection** *(verified)* — so a correct-looking schema can enforce nothing.
- **Data-model building blocks: entity, attribute, relationship (1:1, 1:M, M:N), constraint** — with relationships and constraints determined by **business rules**, which cannot be inferred from data because data shows what *has* happened, not what is *permitted*.
- **Codd's 1970 insight was to relate data by matching *values* rather than following pointers**, which gave declarative queries, made optimisation possible, and grounded the model in [[Discrete Mathematics/contents/03 - Functions, Sequences and Relations|relations]]. **That is why relational displaced hierarchical and network.**
- **Four levels of abstraction — external, conceptual, internal, physical** — each insulated from changes below. **Designers work conceptually; analysts live in the external level, i.e. views.**

## ⚠️ Important Notes

1. **Never store the same fact in two places** unless you have deliberately chosen denormalisation and can say what prevents the anomalies.
2. **Redundancy is not a tidiness issue — it makes contradiction *representable*.** A good schema makes invalid states impossible, not merely unlikely.
3. **The deletion anomaly leaves no evidence.** Update anomalies can be found with `GROUP BY … HAVING COUNT(DISTINCT …) > 1`; lost rows cannot be found at all.
4. **Anomalies are properties of a schema, not of data.** They will eventually occur if the schema permits them, however careful the current process is.
5. **Denormalise only for read-heavy, write-controlled workloads** — warehouses, caches, reporting tables. **Denormalising a transactional schema for speed reintroduces every anomaly in §3.**
6. **⚠️ In SQLite, run `PRAGMA foreign_keys = ON` on every connection.** It is off by default and per connection; `REFERENCES` in the DDL is otherwise decorative.
7. **Verify that a constraint is enforced, don't infer it from the DDL.** Insert a deliberately invalid row and check it is rejected.
8. **Constraints turn corruption into errors.** `NOT NULL`, `CHECK`, `UNIQUE` and foreign keys move failures to the moment of the mistake, where they are cheap.
9. **A strict schema surfaces problems earlier**, as §3.2 showed — the same defect appeared as a phantom row in a permissive schema and an immediate error in a strict one.
10. **Business rules cannot be inferred from data.** "Every customer currently has one agent" does not mean a customer *may not* have two. Ask; do not infer.
11. **Design at the conceptual level.** An ER model is DBMS-independent and survives migration; decisions made at the internal level are made too early.
12. **Use views as the analyst-facing interface** — they give a stable contract when underlying tables are restructured.
13. **Do not confuse a data *model* with a *schema*.** The model is the abstraction (relational, document, graph); the schema is one design expressed in it.
14. **`SELECT` is declarative on purpose.** Never work around the optimiser by hand-writing procedural loops before checking the query plan ([[09 - Query Optimization and Indexing|ch. 09]]).
15. **Much of "data cleaning" is upstream denormalisation.** When a source file has one customer's address spelled three ways, the fix belongs in the schema, not the notebook.

> [!warning] Gaps in the source material
> **Coronel & Morris chapters 1–2 extract cleanly** — real prose, no glyph substitution, no mangled identifiers. **The easiest source in the vault so far.** *(Verified. **Book page $n$ = PDF page $n+28$**; ch. 1–2 are PDF pages 31–92.)*
>
> **All figures are images and are lost**, including **Figure 1.7 (the redundant `CUSTOMER` file that the anomaly discussion refers to throughout)**, Figure 1.9 (the database system environment), the file-system-versus-database comparisons, and every diagram in ch. 2's model-evolution and abstraction sections.
>
> **Figure 1.7 was reconstructed as a real table**, using the agent and customer names the surrounding prose names explicitly — *Leah F. Hahn*, *John T. Okon*, *Amy B. O'Brian*, *George Williams*, *Olette K. Smith*, *Paul F. Olowski* — with the structure the text fully determines (agent name, phone and area repeated on each customer row). **The phone numbers and the `agent_area` values are my own inventions**, since the prose does not state them; nothing in the argument depends on their values. **This is the only reconstruction in the chapter**, and it is flagged rather than presented as the book's figure.
>
> **No error was found in Coronel & Morris ch. 1–2.**
>
> **Additions beyond the source. §3 in its entirety is mine** — the book *describes* the three anomalies in prose; **here each one is executed against a real SQLite database and the actual output printed.** That converts three definitions into three demonstrations, and it produced a finding the book does not contain: **the insertion anomaly presents differently under a `NOT NULL` constraint** (outright rejection rather than a dummy row), which is the basis of Exercise 2(d) and of the general principle that constraints convert corruption into errors. **§4's before/after comparison, §5's foreign-key enforcement test, and §7's join-reconstruction demonstration are all mine.**
>
> **The SQLite `PRAGMA foreign_keys` finding (§5) is entirely mine and is not in the book** — that foreign keys are **off by default and per connection** is a genuine trap for anyone prototyping in Python, and it was found by testing rather than by reading.
>
> **The framing of normalisation as "restricting representable states, not answerable questions"** (§4, Exercise 3(a)) is my own and is not how the book puts it. **The forward link from denormalisation to [[10 - Data Warehouses and OLAP|ch. 10]]'s star schemas**, the observation in Exercise 3(d) that business rules cannot be inferred from data (with its warning for data science), and the emphasis on **Codd's value-matching** as the single decisive idea (§8) are additions.
>
> **Deliberately compressed.** **Coronel & Morris §1-7a's full five-component database-system environment** (hardware, software, people, procedures, data) is reduced to one line in §6 — it is organisational framing rather than technical content. **The DBMS-functions list (§1-7b)** is given as a list without the book's extended discussion of each. **§1-3's taxonomy of database types** (single- vs multi-user, centralised vs distributed, workgroup vs enterprise, general-purpose vs discipline-specific, OLTP vs analytical, structured vs unstructured, XML) is omitted; the one distinction that matters later — **OLTP versus analytical** — is developed properly in [[10 - Data Warehouses and OLAP|ch. 10]] where it belongs. **§2-4a–c on discovering and naming business rules** is summarised in §7 rather than reproduced. **§2-5d–e (object-oriented, object/relational and XML models)** are given one table row each: they are historically important but largely absorbed, and this vault's scope has no chapter depending on them.

**Previous:** [[00-Index]] · **Next:** [[02 - The Relational Model and Relational Algebra]]
