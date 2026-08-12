---
subject: Database Management Systems
chapter: 11
tags: [ds, dbms, nosql, big-data, cap-theorem, document-store, key-value, graph-database, schemaless]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 14"
---

# Big Data and NoSQL

The last chapter of the subject, and the one that asks **when *not* to use everything the previous ten chapters taught.**

**NoSQL is not "better than SQL".** It is a set of trades, each surrendering something a relational database guarantees in exchange for scale, flexibility or availability. **The useful question is always: what am I giving up, and do I need what I get?**

The chapter's central finding is §4, and it is a correction to the marketing:

> **"Schemaless" does not mean there is no schema. It means the schema has moved into the application, where nothing enforces it and every writer may disagree.**

*(Verified: two Electronics products became invisible to the obvious query, and an aggregate came out wrong by exactly the value it could not parse.)*

**This chapter is heavily enriched.** Coronel & Morris's NoSQL chapter is largely an industry survey — the subject file flagged this at the outset — so the theory (CAP, the four families' trade-offs) and all demonstrations are added.

## 📘 Main Knowledge

### 1. Where the relational assumptions break

| the relational model assumes | it breaks when |
|---|---|
| one machine can hold the data | data exceeds one machine — you must **scale out**, not up |
| the schema is known in advance | fields vary per record, or change weekly |
| strong consistency is required | **availability matters more** (§2) |
| relationships are the point | there are none — a cache, a session store, a log |
| relationships are **shallow** | they are **deep** — a social graph, a routing network |

**Each NoSQL family attacks exactly one of these**, and gives up something to do it.

> [!note] Scale up versus scale out
> **Scaling up** — a bigger machine — is what relational databases do naturally, and it has a hard ceiling and a superlinear price.
>
> **Scaling out** — more machines — is cheap and unbounded, but **joins and transactions across machines are expensive or impossible**, which is precisely what the relational model is built on. **That tension is the origin of NoSQL.**

### 2. The CAP theorem

> [!note] Two of three
> **C**onsistency — every read sees the most recent write.
> **A**vailability — every request gets a non-error response.
> **P**artition tolerance — the system keeps working despite dropped messages.

**In a distributed system a partition *will* happen, so P is not optional.** The real choice is **C versus A during a partition**:

| | behaviour during a partition | examples |
|---|---|---|
| **CP** | **refuse to answer** rather than answer stale | HBase, MongoDB (default) |
| **AP** | **answer**, possibly with stale data | Cassandra, DynamoDB |

**A single-node database is "CA" only because it is not distributed** — there is no partition to tolerate. Everything in [[01 - Databases and Data Models|ch. 01]]–[[10 - Data Warehouses and OLAP|10]], and SQLite, is in this category.

**ACID versus BASE:**

| **ACID** ([[08 - Transactions and Concurrency Control\|ch. 08]]) | **BASE** |
|---|---|
| **A**tomic | **B**asically **A**vailable |
| **C**onsistent | **S**oft state |
| **I**solated | **E**ventually consistent |
| **D**urable | |

**BASE deliberately relaxes [[08 - Transactions and Concurrency Control|ch. 08]]'s guarantees** to buy availability and scale. **"Eventually consistent" means a read may return a stale value, and the system promises only that it will converge** — which is acceptable for a like count and unacceptable for a bank balance.

### 3. Document stores

**SQLite's JSON functions let a document store be demonstrated directly.**

```sql
CREATE TABLE products_doc (id INTEGER PRIMARY KEY, doc TEXT);
```
```
{"name":"Laptop","price":1200,"category":"Electronics","specs":{"ram":"16GB","cpu":"i7"}}
{"name":"Phone","price":600,"category":"Electronics","specs":{"ram":"8GB"},"colors":["black","blue"]}
{"name":"T-shirt","price":15,"category":"Clothing","size":"M"}
```

**Each row has its own shape**, and you query into it:
```sql
SELECT doc ->> '$.name', doc ->> '$.price', doc ->> '$.specs.ram' FROM products_doc;
```

**The promise is real:** *(verified)* inserting a product with two brand-new fields (`refresh_hz`, `panel`) needed **no `ALTER TABLE` and no downtime**. A relational table would have required a migration.

> [!note] The first cost, immediately
> **A field that does not exist returns `NULL`, with no error.** The document store **cannot distinguish "this field is missing" from "this field is genuinely null"** — [[05 - SQL Fundamentals|ch. 05]]'s null problem, now unavoidable rather than a design choice.

### 4. ⚠️ The bill — what the schema was doing for you

#### (a) No type enforcement

*(Verified — a price stored as the string `"twenty five"`:)*
```
id | name    | price       | price_type
---+---------+-------------+-----------
1  | Laptop  | 1200        | integer
6  | Mouse   | twenty five | text

SUM(price) over all 6 documents : 2123.0
the true total is                 2148.0
```

**`'twenty five'` was silently coerced to 0 and dropped from the sum.** The aggregate is wrong **by exactly the value it could not parse**, and **no error was raised at insert or at query time.**

#### (b) No required fields

*(Verified — a document with no `category`:)*
```
category      | n
--------------+--
Electronics   | 4
Grocery       | 1
Clothing      | 1
(no category) | 1        <- 7 documents, only 6 have a category
```
**A report filtering `WHERE category = 'Electronics'` silently omits it.** The relational table's `NOT NULL` made this **impossible**.

#### (c) Schema drift

*(Verified — three documents spelling the same idea as `category`, `Category` and `cat`:)*
```
WHERE category = 'Electronics'                -> 5 rows
allowing for Category / cat spellings too     -> 7 rows
```
**Two Electronics products are invisible to the obvious query.**

**And the field names actually in use** *(verified via `json_each`)*:
```
Category, cat, category, colors, name, organic, panel, price, refresh_hz, size, specs, weight_g
```

> [!warning] There *is* a schema — it is just implicit and unenforced
> **Twelve distinct field names, three of which mean the same thing.** The collection has a schema; nobody wrote it down, so nobody agrees on it.
>
> **This is [[07 - Database Design|ch. 07]]'s finding taken to its limit.** There, an audit found the schema enforced 6 of 10 business rules and the rest lived in triggers, application code, or nowhere — **and "nowhere is the default".** A document store moves *every* rule into that category at once.
>
> **The trade is real and sometimes right**: if the data genuinely has no fixed shape (user-supplied metadata, event payloads, CMS content), a schema would be a lie anyway. **But it is a trade, not a free lunch**, and the cost lands on whoever queries the data later — usually the analyst, not the developer who chose it.
>
> **Mitigation: schema validation at the application boundary** (MongoDB's `$jsonSchema`, JSON Schema, Pydantic). **This does not restore the guarantee** — it holds only for writers that go through that code — but it is much better than nothing.

### 5. What document queries cost

*(Verified, 200 000 rows, "count and total price for one category":)*

| | unindexed | indexed |
|---|---|---|
| **document** (JSON extract) | 0.1070 s | 0.04028 s |
| **relational** (columns) | **0.0161 s** | **0.01301 s** |
| ratio | **6.7×** | **3.1×** |

**Identical answers.** The document form must parse JSON per row; the relational form reads a column.

> [!note] Indexing a document field requires knowing the schema
> The document index is an **expression index** on `doc ->> '$.category'` — [[09 - Query Optimization and Indexing|ch. 09]] §6's mechanism.
>
> **Note what that requires: you must know the field's name and path in advance.** Which is to say — **you had a schema after all.** The flexibility was surrendered at exactly the point where performance mattered.
>
> **This is the honest summary of document stores: flexible where you don't query, and effectively schema'd where you do.**

### 6. Key–value stores

*(Verified — a key–value store is a two-column table:)*
```
k           | v
------------+-------------------------------
cart:42     | ["p1","p2"]
session:abc | {"user":42,"exp":"2026-08-01"}
```

**`GET` by key is $O(1)$. That is all it does.** *(Verified: "which sessions belong to user 42?" requires scanning every value — there are no secondary indexes, no joins, no queries by value.)*

> [!note] The limitation is the feature
> **Because the only access path is the key, the key alone decides which machine holds the data** — so a key–value store **partitions trivially across any number of machines**, which is what makes it scale almost without limit.
>
> **Right for caches, sessions, feature flags, rate limiters.** **Wrong for anything you must query by content** — and that is not a gap to be filled later, it is the design.

### 7. Graph data

*(Verified — a 5 000-node, 60 000-edge follower graph traversed with a recursive CTE ([[06 - Advanced SQL|ch. 06]] §3):)*

| depth | nodes reached | time |
|---|---|---|
| 1 hop | 14 | 0.0003 s |
| 2 hops | 162 | 0.0003 s |
| 3 hops | 1 603 | **0.0023 s** |
| 4 hops | 4 896 | **0.0153 s** |

**Each extra hop is another self-join, and the cost climbs steeply** — 6.7× from 3 to 4 hops.

> [!note] Index-free adjacency
> **A graph database (Neo4j) stores adjacency as *pointers* rather than as rows to be joined**, so traversing one hop is pointer-chasing at constant cost — *index-free adjacency*. Depth costs linearly rather than multiplicatively.
>
> **This is [[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]]'s adjacency list promoted from an in-memory representation to the primary storage model** — and DSA §1 measured exactly why it matters: **the adjacency map beat the matrix by 38× on neighbour iteration**, which is the operation every traversal performs.
>
> **Right for deep traversal** — social networks, recommendations, fraud rings, routing. **Wrong for bulk aggregation**, where a relational scan wins easily.

### 8. The four families

| family | model | right for | wrong for |
|---|---|---|---|
| **key–value** | key → opaque blob | caches, sessions | querying by value |
| **document** | key → JSON document | varying shapes, CMS | joins, aggregates |
| **column-family** | row key → column groups | huge sparse tables, time series | ad-hoc queries |
| **graph** | nodes + edges as pointers | deep traversal | bulk aggregation |

**And relational is right for:** a known schema, integrity that must be *enforced*, ad-hoc queries, joins, and transactions spanning entities — **which describes most business data, which is why it did not go away.**

> [!note] Polyglot persistence
> **The mature position is not to choose one.** Use PostgreSQL for orders, Redis for sessions, Elasticsearch for search, a graph store for recommendations — **each where its trade is the right one.**
>
> **The cost is operational**: several systems to run, and **no cross-store transactions or joins**, so consistency between them becomes application work.
>
> *(**NewSQL** — CockroachDB, Spanner, TiDB — attempts the other resolution: horizontal scale while keeping SQL and ACID, at the price of complexity and latency.)*

### 9. What could not be demonstrated here

> [!warning] SQLite is single-node, so distribution is theory in this note
> **Sections 3–7 are real output. Everything about *distribution* is described, not verified**, and saying so is better than faking a cluster:
> - sharding / horizontal partitioning across machines
> - replication and replica lag
> - **the CAP trade during an actual network partition**
> - eventual consistency and read-your-writes anomalies
> - column-family physical storage (HBase, Cassandra)
> - index-free adjacency in a real graph database
>
> **This matters because the distributed behaviour is where NoSQL's genuine advantages live.** A document store on one machine is mostly the *costs* of §4 with few of the benefits — which is itself a useful warning: **adopting NoSQL without needing to scale out buys the drawbacks and none of the point.**

## ✏️ Exercises

**1. (Trade-offs.)** (a) Where do the relational assumptions break? (b) State CAP precisely and the C-vs-A choice. (c) ACID vs BASE? (d) Why is "NoSQL is better" the wrong framing?

> [!example]- Solution
> **(a) Five places** — data exceeding one machine; a schema that is unknown or changing; availability mattering more than consistency; no relationships at all; relationships too deep for joins.
>
> **The most consequential is the first, because it is structural.** Relational databases **scale up** naturally, which has a hard ceiling and a superlinear price. **Scaling out is cheap and unbounded — but joins and transactions across machines are expensive or impossible**, and those are what the relational model is built on. **NoSQL exists because of that tension.**
>
> **(b) Consistency, Availability, Partition tolerance — you may guarantee two.**
>
> **The formulation matters: in a distributed system a partition *will* occur, so P is not a choice.** The real decision is **what to do during one**:
> - **CP** — refuse to answer rather than return stale data. *"I don't know" is safer than a wrong balance.*
> - **AP** — answer with possibly stale data. *A slightly old like-count beats an error page.*
>
> **A single-node database is "CA" only vacuously** — there is no partition to tolerate. Everything in this subject before now, including SQLite, is in that category.
>
> **The common misreading is that CAP is a permanent architectural choice.** It is a statement about behaviour **during a partition**; when the network is healthy, a system can be both consistent and available.
>
> **(c)**
>
> | ACID | BASE |
> |---|---|
> | Atomic, Consistent, Isolated, Durable | Basically Available, Soft state, Eventually consistent |
>
> **BASE deliberately relaxes [[08 - Transactions and Concurrency Control|ch. 08]]'s guarantees to buy availability and scale.** "Eventually consistent" means a read may return a stale value and the system promises only convergence.
>
> **The judgement is per use case, not per company.** Acceptable for a like count, a view counter, a recommendation. **Unacceptable for a balance, a seat booking, an inventory decrement** — and [[08 - Transactions and Concurrency Control|ch. 08]] §4 showed exactly what goes wrong there: **100 bookings committed against 20 seats.** Eventual consistency makes that class of problem harder, not easier.
>
> **(d) Because they solve different problems, and the question is always what you are giving up.**
>
> Every NoSQL family surrenders a relational guarantee: key–value gives up querying by value; document gives up enforced structure; column-family gives up ad-hoc queries; graph gives up efficient bulk aggregation. **In exchange each gets one thing the relational model is bad at.**
>
> **The right question is "which trade do I need?"** — and often the answer is none of them: **most business data has a known schema, integrity that must be enforced, and fits comfortably on one machine.**
>
> **§9 sharpens this: NoSQL's real advantages are in distribution**, so adopting it without needing to scale out **buys the costs of §4 and almost none of the benefit.** That is the single most common way this decision is got wrong.

**2. (Hard — schemaless.)** (a) What are the three costs demonstrated? (b) Why is §4(c) the most serious? (c) What does "schemaless" actually mean? (d) When is a document store right, and how do you mitigate?

> [!example]- Solution
> **(a) Three, all verified.**
>
> **No type enforcement** — a price stored as `"twenty five"` was accepted, then **silently coerced to 0**, so `SUM(price)` returned **2 123 where the truth is 2 148**. **The aggregate is wrong by exactly the unparseable value, and no error was raised at insert or at query time.**
>
> **No required fields** — a document with no `category` was accepted, so 7 documents yielded only 6 categorised. **A report filtering `WHERE category='Electronics'` silently omits it.**
>
> **Schema drift** — `category`, `Category` and `cat` all appeared. **`WHERE category='Electronics'` found 5 rows; allowing all three spellings found 7.** *(And `json_each` revealed **twelve** distinct field names in a five-field collection.)*
>
> **All three fail the same way: silently, at query time, long after the bad write.**
>
> **(b) Because drift is undetectable from the data and grows without limit.**
>
> The other two have signatures you could look for — a `json_type` check finds non-numeric prices; a null check finds missing categories. **But to detect drift you must already know that `Category` and `cat` exist**, and the only way to learn that is to enumerate every field name in the collection and inspect them by eye.
>
> **The query gives a plausible answer.** 5 rows is not obviously wrong; nothing suggests 2 more are hiding. **You would only notice if you independently knew the true count.**
>
> **And it compounds.** Every new writer — a new service, a new developer, a data import — can introduce another spelling, and none of them will fail. **In a long-lived collection the field-name set only ever grows.**
>
> **This is the same shape as every serious bug in this subject** — [[03 - Entity-Relationship Modelling|ch. 03]]'s fan trap, [[05 - SQL Fundamentals|ch. 05]]'s `NOT IN`, [[06 - Advanced SQL|ch. 06]]'s frame default, [[10 - Data Warehouses and OLAP|ch. 10]]'s business-key join: **valid-looking query, no error, wrong answer.**
>
> **(c) That the schema moved into the application, where nothing enforces it.**
>
> *(Verified: `json_each` listed twelve field names — `Category`, `cat`, `category`, `colors`, `name`, `organic`, `panel`, `price`, `refresh_hz`, `size`, `specs`, `weight_g`. **The collection has a schema. Nobody wrote it down, so nobody agrees on it.**)*
>
> **Every reader must know the field names, their types, which are optional, and which spellings are in use** — and that knowledge lives in whoever wrote the code, not in the database. **The database can no longer answer "what is in here?"**, which [[01 - Databases and Data Models|ch. 01]] identified as the point of metadata in the first place.
>
> **This is [[07 - Database Design|ch. 07]]'s conclusion at full strength.** There, an audit found 6 of 10 rules enforced by the schema and the rest living in triggers, application code, or nowhere — **with "nowhere" as the default.** A document store moves **every** rule into that category simultaneously.
>
> **(d) Right when the data genuinely has no fixed shape.**
>
> - **User-supplied or third-party metadata**, where fields differ per source and you do not control them.
> - **Event payloads and logs**, where each event type carries different data and the set grows.
> - **CMS or catalogue content**, where a laptop has a CPU and a shirt has a size and forcing both into one table produces mostly-null columns.
> - **Rapid prototyping**, before the shape is known.
>
> **In those cases a fixed schema would be a lie**, and the flexibility is genuine.
>
> **Mitigations, in decreasing strength:**
> 1. **Schema validation at the boundary** — MongoDB's `$jsonSchema`, JSON Schema, Pydantic. **It does not restore the guarantee** (it binds only writers who go through that code) but it catches most drift.
> 2. **Promote fields you query to real columns.** §5 showed that indexing a document field requires knowing its path anyway — **so the fields you query are already schema'd in practice.** Storing them as columns makes that explicit and faster.
> 3. **Monitor the field-name set.** A periodic `json_each` enumeration turns drift from invisible into a dashboard.
> 4. **A hybrid schema** — typed columns for the known core, one JSON column for the variable tail. **This is usually the right answer in a relational database**, and PostgreSQL's `jsonb` makes it a first-class option.

**3. (Families and cost.)** (a) Interpret the document-vs-relational timings. (b) Why is a key–value store's limitation its feature? (c) Interpret the graph timings. (d) What is polyglot persistence and what does it cost?

> [!example]- Solution
> **(a)** *(Verified, 200 000 rows:)*
>
> | | unindexed | indexed |
> |---|---|---|
> | document | 0.1070 s | 0.04028 s |
> | relational | **0.0161 s** | **0.01301 s** |
> | ratio | **6.7×** | **3.1×** |
>
> **Unindexed, the document form must parse JSON for every row** to reach a field the relational form reads directly as a column.
>
> **Indexing closes most of the gap — but look at what indexing required.** The document index is an **expression index on `doc ->> '$.category'`** ([[09 - Query Optimization and Indexing|ch. 09]] §6), which means **you had to know the field's exact name and path in advance.**
>
> **That is the honest summary: a document store is flexible where you don't query it, and effectively schema'd where you do.** The flexibility is surrendered precisely where performance matters — and the residual 3.1× is what you still pay.
>
> **(b) Because the only access path being the key is what lets it partition.**
>
> *(Verified: "which sessions belong to user 42?" required scanning every value. No secondary indexes, no joins, no queries by content.)*
>
> **Since the key alone determines where data lives, the key alone determines which machine holds it** — so a key–value store shards across any number of machines with no coordination, no distributed joins, and no cross-machine transactions.
>
> **Adding secondary indexes would destroy that**: an index on a value spans machines, requiring exactly the coordination the design avoids.
>
> **So the limitation is not a gap to be filled later — it is the source of the scalability.** Right for caches, sessions, feature flags, rate limiters. **Wrong for anything you must query by content.**
>
> **(c)**
>
> | depth | nodes | time |
> |---|---|---|
> | 1 | 14 | 0.0003 s |
> | 2 | 162 | 0.0003 s |
> | 3 | 1 603 | 0.0023 s |
> | 4 | 4 896 | **0.0153 s** |
>
> **6.7× from 3 hops to 4**, while the node count grew 3.1× — **so the cost per node reached is also rising.** Each hop is another self-join against a 60 000-edge table.
>
> **A graph database uses *index-free adjacency*: edges are stored as pointers on the node itself**, so a hop is pointer-chasing at constant cost rather than an indexed join. **Depth costs linearly instead of multiplicatively.**
>
> **This is [[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]]'s adjacency list promoted to the primary storage model** — and DSA §1 measured why: **the adjacency map beat the adjacency matrix by 38× on neighbour iteration**, the operation every traversal performs. **A relational edge table is closer to the matrix; a graph database is the adjacency list.**
>
> **The honest caveat: 4 hops in 0.015 seconds is fine.** A graph database earns its place at depth 6+, on much larger graphs, or when traversal queries are the *main* workload — not for the occasional two-hop lookup, which SQL handles well.
>
> **(d) Using several stores, each where its trade is right** — PostgreSQL for orders, Redis for sessions, Elasticsearch for search, a graph store for recommendations.
>
> **The reasoning is sound**: no single store is good at everything, and §8's table shows each family has a domain where it is clearly best.
>
> **The costs are substantial and usually underestimated:**
> 1. **No cross-store transactions.** [[08 - Transactions and Concurrency Control|Ch. 08]]'s atomicity stops at one system's boundary. Writing an order to PostgreSQL and invalidating a Redis cache is **two operations that can half-fail** — and reconciling them is application code, which is where §4's "enforced nowhere" problem reappears at the architecture level.
> 2. **No cross-store joins.** Combining data means fetching from both and joining in the application, badly.
> 3. **Operational multiplication.** Each store needs monitoring, backups, upgrades, expertise, and a failure mode you understand.
> 4. **Consistency between stores becomes your problem** — the cache is stale, the search index lags.
>
> **So the rule is: add a second store when a measured requirement demands it, not architecturally in advance.** A single PostgreSQL instance handles relational data, JSON documents (`jsonb`), full-text search and key–value patterns competently — **and one system with adequate performance usually beats four with excellent performance and no transactions between them.**
>
> *(**NewSQL** — CockroachDB, Spanner, TiDB — pursues the other resolution: horizontal scale while keeping SQL and ACID, paying in complexity and latency.)*

## 📝 Summary

- **NoSQL is a set of trades, not an improvement.** Each family surrenders a relational guarantee to fix one thing the relational model is bad at: data exceeding one machine, unknown or changing schemas, availability over consistency, no relationships, or relationships too deep to join.
- **Relational databases scale *up*; NoSQL scales *out*** — and joins and cross-machine transactions are what make scaling out hard.
- **CAP: in a distributed system partitions happen, so the real choice is C versus A *during* a partition.** **CP** refuses to answer (HBase, MongoDB); **AP** answers with possibly stale data (Cassandra, DynamoDB). **A single-node database is "CA" only vacuously.**
- **BASE relaxes [[08 - Transactions and Concurrency Control|ch. 08]]'s ACID guarantees** for availability. Fine for a like count; **not for a seat booking** — see ch. 08's 100 bookings against 20 seats.
- **Document stores deliver on flexibility** *(verified: two new fields added with no migration and no downtime)*.
- **⚠️ And the bill is three silent failures, all verified.** **No types:** `"twenty five"` was coerced to 0, so `SUM` returned **2 123 against a true 2 148** — wrong by exactly the unparseable value, with no error at insert or query. **No required fields:** 7 documents, 6 categorised, and the seventh vanishes from any category filter. **Schema drift:** `category`/`Category`/`cat` meant **5 rows found where 7 exist.**
- **`json_each` revealed twelve distinct field names** in a five-field collection. **"Schemaless" means the schema moved into the application, unenforced** — [[07 - Database Design|ch. 07]]'s "enforced nowhere holds nowhere", applied to every rule at once.
- **Drift is the most serious**, because detecting it requires already knowing the alternative spellings exist, and every new writer can add one.
- **Document queries cost 6.7× unindexed, 3.1× indexed** *(verified, 200 000 rows)* — **and indexing a document field requires knowing its exact path**, so the flexibility is surrendered precisely where performance matters.
- **A key–value store does `GET` by key and nothing else** *(verified: querying by value scans everything)*. **That limitation is what lets the key decide the shard**, and hence what makes it scale.
- **Graph traversal by recursive CTE cost 6.7× more from 3 hops to 4** *(verified)*, since each hop is another self-join. **A graph database's index-free adjacency makes a hop pointer-chasing** — [[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]]'s adjacency list as primary storage, where the map beat the matrix by 38× on exactly that operation.
- **Relational remains right for a known schema, enforced integrity, ad-hoc queries, joins and cross-entity transactions** — most business data.
- **Polyglot persistence costs cross-store transactions, cross-store joins, and operational multiplication.** Add a store when a measured need demands it.
- **⚠️ Everything about *distribution* in this chapter is theory** — SQLite is single-node, so sharding, replication, real partitions and eventual consistency were described, not verified. **And NoSQL's genuine advantages live there**, so adopting it without needing to scale out buys the costs and none of the point.

## ⚠️ Important Notes

1. **Ask what you are giving up.** Every NoSQL choice surrenders a specific relational guarantee; if you cannot name it, you have not made the decision.
2. **Do not adopt NoSQL unless you need to scale out.** On one machine you get §4's costs and almost none of the benefit.
3. **CAP is about behaviour *during a partition*, not a permanent architecture choice.** When the network is healthy a system can be both consistent and available.
4. **Choose eventual consistency per use case, not per company.** Acceptable for counters and recommendations; not for bookings, balances or inventory.
5. **⚠️ "Schemaless" means the schema is in your application, unenforced.** There is always a schema; the only question is whether anything checks it.
6. **Validate at the application boundary** (`$jsonSchema`, JSON Schema, Pydantic). It binds only writers that go through your code — but that beats nothing.
7. **Monitor the set of field names in use.** A periodic enumeration turns schema drift from invisible into visible.
8. **Promote any field you query to a real column.** You need to know its path to index it anyway, so the flexibility was already gone.
9. **Prefer a hybrid**: typed columns for the known core, one JSON column for the variable tail. PostgreSQL's `jsonb` makes this first-class.
10. **A missing field and a null field are indistinguishable in a document store** — [[05 - SQL Fundamentals|ch. 05]]'s null problem, now unavoidable.
11. **Check types explicitly when aggregating documents** (`json_type`), or a non-numeric value will be coerced to 0 and silently lower your total.
12. **Use a key–value store only for data you retrieve by key.** There are no secondary indexes, and that is by design.
13. **Reach for a graph database at depth 6+ or when traversal is the main workload** — not for occasional two-hop queries, which SQL handles well.
14. **Add a second data store only when a measured requirement demands it.** One system with adequate performance beats four with no transactions between them.
15. **Consistency *between* stores is application code** — which is exactly where rules go unenforced.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 14 extracts cleanly** — the "V"s of big data, the NoSQL family taxonomy, the Hadoop/MapReduce overview, and the NewSQL discussion all came through readably. **Book page $n$ = PDF page $n+28$; ch. 14 is PDF pages 668–702.**
>
> **All figures are images and are lost**, including the CAP-theorem triangle, the family-comparison diagrams and the Hadoop architecture illustration. **The CAP triangle is the one worth redrawing by hand**; the rest are conveyed adequately by §8's table.
>
> **This chapter is the most heavily enriched in the subject, as the subject file predicted at the outset** — it flagged that *"NoSQL gets a single late chapter that a DS reader needs more of."* **C&M ch. 14 is largely an industry survey**: it names technologies, tabulates the "V"s, and describes what each family does, but **gives no theory beyond a brief CAP mention, no measurements, and no guidance on when each trade is wrong.**
>
> **Everything demonstrated is my own** — the document collection, the drift experiment, the timing comparison, the key–value store and the graph traversal.
>
> **No error was found in Coronel & Morris ch. 14.**
>
> **Additions beyond the source.** **§4 — the three costs of schemalessness — is mine and is the chapter's centrepiece.** C&M presents schema flexibility as a straightforward benefit. **Demonstrating that a string price silently corrupts an aggregate by exactly its own value, that a missing field silently removes a row from every filtered report, and that three spellings of one field name hide 2 of 7 matching products, turns "flexible" into a measured trade.** The `json_each` enumeration of **twelve field names in a five-field collection** is the single most persuasive artefact: **the schema exists, written by nobody, agreed by no one.**
>
> **The framing "schemaless means the schema moved into the application, unenforced" is my own**, and it deliberately completes [[07 - Database Design|ch. 07]]'s finding that a rule enforced nowhere holds nowhere.
>
> **§5's measurement (6.7× unindexed, 3.1× indexed) is mine**, along with the observation that **indexing a document field requires knowing its path — so flexibility is surrendered exactly where performance matters.** **§7's graph timings are mine**, as is the connection to [[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]]'s measured 38× adjacency-map advantage, which explains *why* index-free adjacency works rather than merely naming it. **§2's CP/AP treatment, and the point that CAP describes behaviour during a partition rather than a permanent choice, are additions** — C&M mentions CAP without drawing the operative distinction.
>
> **§9 is an addition of a different kind: an explicit statement of what could not be demonstrated.** SQLite is single-node, so **sharding, replication, real partitions, eventual consistency, column-family storage and index-free adjacency are described but unverified**, and the note says so rather than implying otherwise. **The conclusion drawn from it — that NoSQL's genuine advantages live in distribution, so adopting it on one machine buys the costs and none of the point — is the most practically useful judgement in the chapter.**
>
> **A fifth SQLite permissiveness surfaced incidentally** *(§4a)*: the relational comparison table accepted `'twenty five'` into a `REAL NOT NULL CHECK (price >= 0)` column, because **SQLite's type affinity does not enforce declared types**. PostgreSQL rejects it. This joins the four found in [[01 - Databases and Data Models|ch. 01]], [[02 - The Relational Model and Relational Algebra|ch. 02]] and [[05 - SQL Fundamentals|ch. 05]].
>
> **Deliberately compressed.** **The "V"s of big data (volume, velocity, variety, veracity, value)** are absorbed into §1's table of broken assumptions — the V-list is a mnemonic, and what matters is which relational assumption each pressure breaks. **Hadoop, HDFS and MapReduce (C&M §14-3)** are omitted: MapReduce is largely superseded by Spark and by cloud warehouses, and the batch-processing model is [[MLOps/contents/00-Index|MLOps]] territory. **The vendor survey** (which product implements which family) is reduced to one example per row in §8, since it dates fastest of anything in the book. **NewSQL** is noted in §8 rather than developed. **Column-family stores are described but not demonstrated** — their advantage is a physical storage layout that SQLite cannot imitate, so imitating it would teach the wrong thing.

**Previous:** [[10 - Data Warehouses and OLAP]] · **Next:** *(end of subject — see [[00-Index]])*
