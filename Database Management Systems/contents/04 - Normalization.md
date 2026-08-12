---
subject: Database Management Systems
chapter: 4
tags: [ds, dbms, normalization, functional-dependency, 1nf, 2nf, 3nf, bcnf, denormalization, lossless-join]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 6"
---

# Normalization

[[01 - Databases and Data Models|Chapter 01]] diagnosed the disease — update, insertion and deletion anomalies, all caused by storing one fact in several places. **This chapter is the cure, and it is a procedure rather than an art.**

Normalisation takes a table and a set of **functional dependencies** ([[02 - The Relational Model and Relational Algebra|ch. 02]] §2's determination) and decomposes it until no dependency can cause an anomaly. **Each normal form removes one specific kind of bad dependency:**

| form | forbids | removes |
|---|---|---|
| **1NF** | non-atomic values, repeating groups | lists in cells ([[03 - Entity-Relationship Modelling\|ch. 03]] §1.3) |
| **2NF** | **partial** dependencies — on *part* of a composite key | redundancy per key-part |
| **3NF** | **transitive** dependencies — nonprime → nonprime | redundancy per non-key attribute |
| **BCNF** | **any** determinant that is not a candidate key | the residue 3NF misses |

**Two properties make a decomposition legitimate**, and §5 shows what happens without the first:

- **Lossless join** — rejoining the fragments reproduces the original *exactly*, with no rows lost and none invented.
- **Dependency preservation** — every dependency can still be enforced within a single table.

**3NF always achieves both. BCNF always achieves the first and sometimes sacrifices the second** — which is why 3NF, not BCNF, is the usual target (§7).

## 📘 Main Knowledge

### 1. Detecting dependencies rather than asserting them

**A functional dependency $X \to Y$ can be tested against data directly:**

```sql
SELECT COUNT(*) FROM (
    SELECT X FROM t GROUP BY X HAVING COUNT(DISTINCT Y) > 1
);   -- zero violations => X -> Y holds in this data
```

*(Applied to the classic project-assignment table:)*

| dependency | result |
|---|---|
| `proj_num → proj_name` | **HOLDS** |
| `emp_num → emp_name` | **HOLDS** |
| `emp_num → job_class` | **HOLDS** |
| `job_class → chg_hour` | **HOLDS** |
| `(proj_num, emp_num) → hours` | **HOLDS** |
| `proj_num → hours` | fails |
| `emp_num → hours` | fails |

> [!warning] ⚠️ A dependency found in data is evidence, not proof
> The same scan reported two dependencies that are **artefacts of this eight-row sample**:
> - **`chg_hour → job_class` "HOLDS"** — only because no two job classes happen to share a charge rate. Set one class to another's rate and it fails.
> - **`hours` was reported as a candidate key** — the eight `hours` values happen to be distinct. It is obviously not a key.
>
> **This is [[01 - Databases and Data Models|ch. 01]] §7's warning in a new setting: data shows what *has* happened, not what is *permitted*.** A `GROUP BY … HAVING` scan can **refute** a dependency conclusively — one violation and it is dead — but it can only *fail to refute* the rest.
>
> **So use the scan to disprove and to generate hypotheses; use business rules to confirm.** A normalisation driven purely by profiling a sample will decompose on accidents.

**Reading the surviving dependencies against the intended key `(proj_num, emp_num)`:**

```
proj_num  -> proj_name            PARTIAL    (depends on part of the key)  -> breaks 2NF
emp_num   -> emp_name, job_class  PARTIAL    (depends on part of the key)  -> breaks 2NF
job_class -> chg_hour             TRANSITIVE (nonprime -> nonprime)        -> breaks 3NF
(proj_num, emp_num) -> hours      FULL       (on the whole key)            -> fine
```

**A *prime* attribute is one appearing in some candidate key; everything else is nonprime.** That definition is what separates 3NF from BCNF in §7, so it is worth fixing now.

### 2. What the bad dependencies cost

**The unnormalised table stores "Database Designer costs 105.00" four times** *(verified)*. All three anomalies follow.

**Update anomaly** — a partial change leaves contradictions:
```
job_class         | chg_hour | rows
------------------+----------+-----
Database Designer | 105.0    | 2
Database Designer | 110.0    | 2
```
*(Verified: one `UPDATE` touching only project 15 produced two rates for one job class.)*

**Deletion anomaly** — *(verified)* six of the seven employees appear on exactly one project, so deleting that project erases everything known about them: their name, their job class, and the fact that they exist.

**Insertion anomaly** — a new job class with no assignment cannot be recorded at all, because the primary key `(proj_num, emp_num)` would have to be null.

> [!note] The anomalies are not three problems
> They are three symptoms of one cause: **an attribute is stored somewhere other than with the thing it describes.** `chg_hour` describes a *job class*, not an assignment, so storing it on the assignment row makes it repeat, makes it losable, and makes it unstorable on its own.
>
> **Normalisation is just: put each attribute in the table whose key determines it.**

### 3. First normal form

> [!note] 1NF
> **All values atomic, no repeating groups, and a primary key defined.**

Covered by [[03 - Entity-Relationship Modelling|ch. 03]] §1.3 — the multivalued attribute where an exact search returned **0 rows on data that was present**. **1NF is the formal name for "no lists in cells".**

### 4. Second normal form — remove partial dependencies

> [!note] 2NF
> **1NF, and no nonprime attribute depends on only *part* of a composite key.**
>
> *(A table whose primary key is a single attribute is automatically in 2NF — there is no "part" of it to depend on.)*

`proj_name` depends on `proj_num` alone, so it is repeated for every employee on that project. Decompose by moving each partially-dependent attribute to a table keyed by its actual determinant:

```sql
CREATE TABLE project  AS SELECT DISTINCT proj_num, proj_name FROM assign_raw;
CREATE TABLE employee AS SELECT DISTINCT emp_num, emp_name, job_class, chg_hour FROM assign_raw;
CREATE TABLE assign   AS SELECT proj_num, emp_num, hours FROM assign_raw;
```

**Is it lossless? Join it back and compare:**
```
original rows: 8 | rejoined rows: 8 | identical: True
```
*(Verified.)* **The decomposition removed redundancy, not information.**

### 5. Lossless join — and a decomposition that fails it

> [!note] The lossless-join test
> A decomposition of $R$ into $R_1$ and $R_2$ is **lossless** if their common attributes form a **superkey of at least one fragment**:
> $$(R_1 \cap R_2) \to R_1 \quad\text{or}\quad (R_1 \cap R_2) \to R_2$$
>
> **§4's decomposition passes** because `proj_num` is the key of `PROJECT` and `emp_num` the key of `EMPLOYEE`.

**Now split on a *non-key* attribute instead** — `job_class`, which is a key of neither fragment:

```sql
CREATE TABLE lossy_a AS SELECT DISTINCT emp_num,  job_class FROM assign_raw;
CREATE TABLE lossy_b AS SELECT DISTINCT job_class, proj_num FROM assign_raw;
```

```
original (emp, job, proj) triples : 8
after rejoining                   : 13
```

**Five rows were invented.** *(Verified — the spurious tuples, listed:)*
```
emp_num | job_class         | proj_num
--------+-------------------+---------
101     | Database Designer | 22
105     | Database Designer | 22
105     | Database Designer | 25
113     | Database Designer | 15
113     | Database Designer | 25
```

> [!warning] "Lossy" means it *gains* rows, not that it loses them
> The name is misleading. **Nothing was deleted — the join *fabricated* facts**, asserting that employee 105 works on projects 22 and 25 when they work on neither.
>
> **What was lost is information**: after the split, the database no longer records which employee is on which project, only which *job classes* are on which projects. **Rejoining cannot recover it, so it guesses — and guesses by cross product**, pairing every Database Designer with every project that has one.
>
> **This is [[03 - Entity-Relationship Modelling|ch. 03]] §7's fan trap, formalised.** There, joining two tables through a shared *parent* invented rows; here, joining two fragments through a shared *non-key* invents rows. **Same mechanism, same signature — inflation on the join — and the lossless-join condition is the precise statement of when it cannot happen.**
>
> **Practical rule: decompose only on a determinant.** Splitting a table on an attribute that is not a key of one of the resulting fragments destroys information silently, and the damage appears later as inflated counts.

### 6. Third normal form — remove transitive dependencies

> [!note] 3NF
> **2NF, and no nonprime attribute depends on another nonprime attribute.**

In the 2NF `EMPLOYEE` table the key is `emp_num`, and *(verified)*:
```
emp_num   -> job_class   HOLDS
job_class -> chg_hour    HOLDS      <- nonprime determines nonprime
```
So `emp_num → chg_hour` only **transitively**, through `job_class`. Decompose:

```sql
CREATE TABLE job      AS SELECT DISTINCT job_class, chg_hour FROM employee;   -- job_class is the key
CREATE TABLE employee AS SELECT emp_num, emp_name, job_class FROM employee;
```
*(Verified lossless: 7 rows in, 7 rejoined, identical.)*

**And now the anomalies are gone** *(all verified)*:

| | before | after |
|---|---|---|
| "Database Designer" rate stored | **4 times** | **once** |
| rows changed by a rate rise | 4 | **1** |
| contradiction possible? | yes | **no — `job_class` is the primary key of `JOB`** |
| new job class with no employees | impossible | **ordinary insert** |

**The last row is the insertion anomaly disappearing:** `INSERT INTO job VALUES ('Data Scientist', 125.00)` now simply works.

### 7. Boyce–Codd normal form — when 3NF is not enough

> [!note] BCNF
> **3NF, and *every* determinant is a candidate key.**
>
> **BCNF can only be violated when a table has more than one candidate key**, which is why the earlier examples — all with a single candidate key — reached BCNF automatically at 3NF.

**Coronel & Morris's Figure 6.8**, with dependencies $A{+}B \to C,D$; $A{+}C \to B,D$; $C \to B$:

```
a  | b  | c  | d
---+----+----+---
a1 | b1 | c1 | d1
a1 | b2 | c2 | d2
a2 | b1 | c1 | d3
a2 | b2 | c2 | d4
a3 | b1 | c1 | d5
a3 | b3 | c3 | d6
```

*(Verified: `c → b` holds, and the candidate keys found are `(a+b)` and `(a+c)`.)*

> [!note] Why this is in 3NF but not BCNF
> **`b` and `c` are both *prime*** — each appears in a candidate key.
>
> **3NF forbids nonprime → nonprime.** Here `c → b` is **prime → prime**, so **3NF is satisfied**.
>
> **BCNF forbids any determinant that is not a candidate key.** `c` determines `b`, and `c` alone is not a candidate key — so **BCNF is violated.**

**And the violation permits real redundancy** *(verified)*:
```
c  | b  | times_repeated
---+----+---------------
c1 | b1 | 3
c2 | b2 | 2
```
**The pair `(c1,b1)` is stored three times**, so updating one copy and not the others silently breaks `c → b`.

**The fix** — pull the offending dependency into its own table where its determinant *is* the key:
```sql
CREATE TABLE r1 AS SELECT DISTINCT c, b FROM t;      -- c is now the key
CREATE TABLE r2 AS SELECT DISTINCT a, c, d FROM t;
```
*(Verified lossless: 6 rows in, 6 rejoined, identical — because `c` is a key of `R1`.)*

> [!warning] BCNF costs dependency preservation
> **The dependency $A{+}B \to C,D$ can no longer be checked within a single table** — `a`, `b`, `c` and `d` no longer sit together anywhere. Enforcing it now requires a join, or a trigger, or nothing.
>
> **The formal statement:**
>
> | | lossless join | dependency preserving |
> |---|---|---|
> | **3NF** | **always** | **always** |
> | **BCNF** | **always** | **not always** |
>
> **This is why 3NF is the practical target.** BCNF removes slightly more redundancy but can leave a constraint unenforceable — and an unenforceable constraint is how the data becomes inconsistent, which is what normalisation was for. **Going to BCNF is right when the residual redundancy is costly and the lost dependency can be enforced another way; otherwise stop at 3NF.**
>
> *(In practice C&M is right that most tables reach BCNF automatically once in 3NF — the gap requires overlapping composite candidate keys, which is uncommon.)*

### 8. Denormalisation — measuring the trade

**Normalisation costs joins. Here is how much**, on 200 000 assignments, 20 000 employees and 50 job classes:

```sql
-- normalised: two joins
SELECT e.job_class, SUM(a.hours * j.chg_hour) AS billed
FROM big_assign a JOIN big_emp e USING (emp_num) JOIN big_job j USING (job_class)
GROUP BY e.job_class;
```

| | time |
|---|---|
| normalised (2 joins) | 0.1698 s |
| **denormalised (1 table)** | **0.1075 s — 1.6× faster** |

*(Verified, best of 5, and both return the identical answer.)*

**And the cost of that speed:**

| | normalised | denormalised |
|---|---|---|
| rows stored | 220 050 across 3 tables | 200 000 in 1 |
| `chg_hour` for one job class stored | **once** | **4 104 times** |

> [!note] Reading this honestly
> **1.6× is a real but modest gain**, and it is the whole case for denormalisation. **The cost is the update anomaly of §2 at scale**: one rate change now rewrites 4 104 rows instead of 1, and any partial failure leaves contradictions across thousands of rows rather than four.
>
> **The trade is asymmetric in *when* you pay.** Normalised: cheap writes, costly reads. Denormalised: cheap reads, costly and dangerous writes.
>
> **So denormalise when writes are few, batched and controlled** — a warehouse loaded nightly by one ETL process ([[10 - Data Warehouses and OLAP|ch. 10]]), where the anomaly is prevented by *process* rather than by structure. **Never denormalise a transactional table for a 1.6× read gain**; add an index instead ([[09 - Query Optimization and Indexing|ch. 09]]), which speeds reads without duplicating facts.

## ✏️ Exercises

**1. (Dependencies.)** (a) How do you test an FD against data, and what can the test establish? (b) Two dependencies in the verified output were artefacts — identify and explain them. (c) Define prime, partial and transitive. (d) What is normalisation, in one sentence?

> [!example]- Solution
> **(a)** `SELECT X FROM t GROUP BY X HAVING COUNT(DISTINCT Y) > 1` — **any row returned is a counterexample.**
>
> **The test is asymmetric, and this is the important part.** A single violation **refutes** $X \to Y$ conclusively — you have two rows agreeing on $X$ and differing on $Y$, and no business rule can make that legal. **Zero violations proves nothing**; it establishes only that the sample contains no counterexample.
>
> **So the scan is a refutation tool and a hypothesis generator, never a confirmation.**
>
> **(b) Two artefacts of an eight-row sample:**
>
> **`chg_hour → job_class` "HOLDS"** — reported because no two job classes in this data share a charge rate. **It is obviously false as a rule**: two different jobs could easily bill at the same rate, and one such row would refute it. Acting on it would produce a table keyed by charge rate, which is absurd.
>
> **`hours` reported as a candidate key** — the eight `hours` values happen to be distinct. **With a ninth assignment of 23.8 hours it collapses immediately.** *(The same accident appeared in §7, where `(d)` was reported as a candidate key.)*
>
> **The general failure: uniqueness in a sample is weak evidence, and it gets weaker as the sample gets smaller relative to the domain.** Continuous or high-cardinality attributes are almost always "unique" in small samples, so they always look like keys.
>
> **This is [[01 - Databases and Data Models|ch. 01]] §7's point exactly** — data shows what *has* happened, not what is *permitted* — and it has direct force here, because **normalising on a spurious dependency produces a schema that rejects legitimate future data.**
>
> **The practical procedure:** run the scan to *eliminate* candidate dependencies, then confirm the survivors against business rules before decomposing on any of them.
>
> **(c)** A **prime** attribute appears in *some* candidate key; all others are **nonprime**.
>
> A **partial** dependency: a nonprime attribute depends on *part* of a composite key — e.g. `proj_num → proj_name` where the key is `(proj_num, emp_num)`. **The consequence is repetition once per other key-part**: `proj_name` repeats for every employee on the project.
>
> A **transitive** dependency: a nonprime attribute depends on another nonprime attribute — e.g. `job_class → chg_hour`, so `emp_num → chg_hour` only via `job_class`. **The consequence is repetition once per row sharing the intermediate value.**
>
> **Both are the same defect at different scales:** an attribute stored somewhere other than with the thing whose key determines it.
>
> **(d) Put every attribute in the table whose key determines it.**
>
> The normal forms are the systematic enumeration of the ways that can fail: 1NF (values not atomic), 2NF (determined by part of the key), 3NF (determined by a nonprime attribute), BCNF (determined by a non-candidate-key).

**2. (2NF, 3NF and the anomalies.)** (a) Why does 2NF only bite on composite keys? (b) Walk the 3NF decomposition and say which anomaly each step removed. (c) Interpret the verified before/after table. (d) Why is the insertion anomaly the clearest evidence of a design fault?

> [!example]- Solution
> **(a) Because a single-attribute key has no proper part to depend on.**
>
> A partial dependency is on *part* of the key. If the key is one attribute, its only subsets are the empty set and itself, so **any table with a single-attribute primary key is automatically in 2NF.**
>
> **A useful corollary: introducing a surrogate key does not normalise anything.** It makes 2NF vacuous by construction, but the underlying redundancy — `proj_name` repeating across rows — is untouched, and now shows up as a 3NF violation instead. **Surrogate keys hide 2NF violations rather than fixing them**, which is worth knowing since surrogate keys are the modern default.
>
> **(b)** **Step 1 (→ 2NF): remove partial dependencies.** `proj_name` moved to `PROJECT` (keyed by `proj_num`); `emp_name`, `job_class`, `chg_hour` moved to `EMPLOYEE` (keyed by `emp_num`); `hours` stayed with `(proj_num, emp_num)`, where it genuinely belongs.
>
> **This removed the deletion anomaly.** Previously six of seven employees appeared on exactly one project *(verified)*, so deleting that project erased them. **Now employee data lives in `EMPLOYEE` and survives any project's deletion.** It also removed the corresponding insertion anomaly for projects and employees.
>
> **Step 2 (→ 3NF): remove the transitive dependency** `job_class → chg_hour`, splitting `EMPLOYEE` into `EMPLOYEE(emp_num, emp_name, job_class)` and `JOB(job_class, chg_hour)`.
>
> **This removed the update anomaly on charge rates and the insertion anomaly for job classes.**
>
> **Both steps were verified lossless** — 8 rows rejoining to 8, and 7 to 7, identical in each case.
>
> **(c)**
>
> | | before | after |
> |---|---|---|
> | rate stored | 4 times | **once** |
> | rows changed by a rate rise | 4 | **1** |
> | contradiction possible | yes *(demonstrated: 105.0 and 110.0 coexisting)* | **no** |
> | new job class with no employees | impossible | **ordinary insert** |
>
> **The third row is the important one, and it is qualitative rather than quantitative.** Before, nothing *prevented* two rates — the demonstration produced them with one `UPDATE`. After, `job_class` is the **primary key** of `JOB`, so there is exactly one row per class and **a second rate is not representable.**
>
> **That is the distinction [[01 - Databases and Data Models|ch. 01]] §4 drew: normalisation restricts the representable *states*, not the answerable *questions*.** The join still answers everything the flat table did; it just cannot express a contradiction.
>
> **(d) Because it proves the schema cannot represent a fact that is true.**
>
> Update and deletion anomalies are about *risk* — they permit corruption that may not have happened yet, so a defender can always say "our process prevents it". **The insertion anomaly is a present, demonstrable inability**: a new job class with no assignment cannot be recorded, because `(proj_num, emp_num)` would have to be null.
>
> **There is no process fix.** No discipline lets you store a fact the schema has nowhere to put. **The only remedy is to change the schema** — which is why it is the argument that ends the discussion.
>
> **It also identifies the missing entity precisely.** *"I cannot record a job class without an assignment"* means job classes are an entity in their own right and need their own table. **The insertion anomaly does not merely reveal a fault; it names the fix** *(verified: after decomposition, `INSERT INTO job VALUES ('Data Scientist', 125.00)` simply works)*.

**3. (Hard — lossless join.)** (a) State the condition. (b) Explain the five spurious tuples. (c) Why is "lossy" a misleading name? (d) How does this relate to the fan trap, and what is the practical rule?

> [!example]- Solution
> **(a) A decomposition of $R$ into $R_1, R_2$ is lossless if the common attributes form a superkey of at least one fragment:**
> $$(R_1 \cap R_2) \to R_1 \quad\text{or}\quad (R_1 \cap R_2) \to R_2$$
>
> **The intuition: the shared attribute must uniquely identify rows on at least one side**, so each row of the other side has exactly one partner and the join reconstructs original rows rather than combining fragments arbitrarily.
>
> *(Verified in §4: `proj_num` is the key of `PROJECT` and `emp_num` of `EMPLOYEE`, so both joins are lossless — 8 rows in, 8 out, identical.)*
>
> **(b)** Splitting on `job_class`, which is a key of **neither** fragment:
> ```
> lossy_a(emp_num, job_class)     lossy_b(job_class, proj_num)
> ```
> **8 original triples became 13.** *(Verified.)*
>
> **The mechanism:** `Database Designer` appears in `lossy_a` for employees 101, 105, 113 and in `lossy_b` for projects 15, 22, 25. Joining on `job_class` produces **all $3\times3 = 9$ combinations**, of which only 4 were real — hence 5 fabrications, including "employee 105 works on project 25".
>
> **The information that was destroyed is precisely the pairing.** After the split, the database records which employees hold which job class, and which job classes appear on which projects — **but not which employee is on which project.** That fact existed in the original and exists in neither fragment.
>
> **(c) Because nothing is deleted — the join *gains* rows.**
>
> Every original row is still derivable; the problem is that **13 rows come back where 8 went in**, and the extra 5 are false. **A more accurate name would be "spurious-tuple-generating".**
>
> **What is lost is *information*, not *data*** — the ability to distinguish which triples are real. And **the damage is undetectable from the fragments alone**: both look perfectly sensible, every value in them is true, and only comparison with the original reveals the loss. **In production there is no original to compare against.**
>
> **This makes lossy decomposition worse than the anomalies of §2**, which at least corrupt data visibly.
>
> **(d) They are the same phenomenon, and the lossless-join condition is its formal statement.**
>
> **[[03 - Entity-Relationship Modelling|Ch. 03]] §7's fan trap:** joining `TEAM` and `PLAYER` through their shared parent `DIVISION` reported 3, 3, 1 players in a 4-player league — a cross product within each division, because `div_id` identifies neither a team nor a player.
>
> **Here:** joining two fragments through `job_class` fabricated 5 triples, because `job_class` is a key of neither fragment.
>
> **Identical mechanism.** In both cases the join key is **not a key of either side**, so matching on it pairs every row of one group with every row of the other. **The fan trap is a modelling error; a lossy decomposition is a normalisation error; the underlying fault is joining on a non-key.**
>
> **The unification is worth holding onto: a join is only meaningful when its key identifies rows in at least one of the tables.** That single sentence covers the fan trap, lossy decomposition, and the everyday inflated-`SUM` bug.
>
> **The practical rule: decompose only on a determinant.** When splitting $R$ into $R_1$ and $R_2$, the shared attributes must be a key of one of them. **Following the normal forms guarantees this automatically** — each step moves an attribute to a table keyed by its own determinant, which is exactly the lossless condition. **Ad-hoc splitting "to tidy things up" does not.**
>
> **And the detection is the same as before: `COUNT(*)` before and after.** A join that increases the row count on a supposedly many-to-one path is fabricating.

**4. (Hard — BCNF and denormalisation.)** (a) Why is the verified table in 3NF but not BCNF? (b) What does the BCNF decomposition cost? (c) Interpret the denormalisation measurement. (d) When is denormalising right?

> [!example]- Solution
> **(a) Because the offending dependency is prime → prime.**
>
> *(Verified: the candidate keys are `(a+b)` and `(a+c)`, and `c → b` holds.)*
>
> Since `b` appears in `(a+b)` and `c` in `(a+c)`, **both are prime attributes**.
>
> **3NF forbids nonprime → nonprime.** `c → b` is prime → prime, **so 3NF is not violated.** **BCNF forbids any determinant that is not a candidate key.** `c` determines `b` but `c` alone is not a candidate key, **so BCNF is violated.**
>
> **The violation is not academic** *(verified)*: the pair `(c1,b1)` is stored **3 times** and `(c2,b2)` twice. **Update one copy and not the others and `c → b` silently ceases to hold** — the update anomaly, in a table that passed 3NF.
>
> **BCNF can only be violated with overlapping composite candidate keys**, which is why every earlier example reached BCNF automatically. C&M is right that most tables do.
>
> **(b) Dependency preservation.**
>
> Decomposing into `R1(c,b)` — where `c` is now the key — and `R2(a,c,d)` is **lossless** *(verified: 6 rows in, 6 rejoined, identical)*, because `c` is a key of `R1`.
>
> **But $A{+}B \to C,D$ is no longer checkable in any single table**: `a`, `b`, `c`, `d` never sit together again. Enforcing it now needs a join in a trigger, or a periodic check, or — realistically — nothing.
>
> | | lossless | dependency preserving |
> |---|---|---|
> | **3NF** | always | **always** |
> | **BCNF** | always | **not always** |
>
> **So BCNF removes a redundancy and may create an unenforceable constraint** — and an unenforceable constraint is precisely how data becomes inconsistent, which is what normalisation existed to prevent. **You can trade one route to inconsistency for another.**
>
> **Hence 3NF is the practical target.** Go further only when the residual redundancy is genuinely costly *and* the lost dependency can be enforced another way.
>
> **(c)**
>
> | | |
> |---|---|
> | normalised (2 joins) | 0.1698 s |
> | denormalised (1 table) | **0.1075 s — 1.6×** |
> | `chg_hour` per job class | once → **4 104 times** |
>
> **1.6× is modest, and reporting it honestly matters.** Denormalisation is often argued for as though it were transformative; on this workload it removed 37% of the runtime. **Against that, one rate change now rewrites 4 104 rows instead of 1.**
>
> **Two caveats on the measurement.** These tables have primary-key indexes, so the joins are already efficient — **on unindexed tables the gap would be far larger, which is really an argument for indexing** ([[09 - Query Optimization and Indexing|ch. 09]]), not for denormalising. And everything is in memory, so no I/O is involved; on disk the denormalised table's better locality would widen the gap ([[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] §7).
>
> **The asymmetry is in *when* you pay:** normalised is cheap to write and costly to read; denormalised is cheap to read and costly — and *risky* — to write.
>
> **(d) When writes are few, batched and controlled, so process prevents the anomaly that structure no longer prevents.**
>
> **The canonical case is a data warehouse** ([[10 - Data Warehouses and OLAP|ch. 10]]): loaded by one ETL job on a schedule, read constantly by analysts, never updated in place. **The update anomaly cannot occur because nothing updates** — the table is rebuilt. **Under those conditions denormalisation is not a compromise, it is correct design**, which is why star schemas are deliberately denormalised.
>
> **The dangerous case is a transactional table** with many concurrent writers ([[08 - Transactions and Concurrency Control|ch. 08]]). There the 4 104-row update is both slow and a correctness hazard: interrupt it halfway and you have contradictions, exactly as §2 demonstrated with four rows.
>
> **Before denormalising, exhaust the alternatives:**
> 1. **Add an index** — speeds reads with no duplication of facts.
> 2. **A materialised view** — the denormalised data is maintained *by the DBMS*, so it cannot drift.
> 3. **Cache in the application**, where staleness is visible and bounded.
> 4. **Only then denormalise**, and write down what now guarantees consistency.
>
> **The general principle: denormalisation moves a guarantee from the schema into a process.** That is acceptable when the process is real, automated and monitored — and it is how most production data corruption begins when it is not.

## 📝 Summary

- **Normalisation in one sentence: put every attribute in the table whose key determines it.** The normal forms enumerate the ways that can fail.
- **A functional dependency can be tested** with `GROUP BY X HAVING COUNT(DISTINCT Y) > 1` — **but the test can only refute.** *(Verified: the scan reported `chg_hour → job_class` and `hours` as a candidate key, both artefacts of an 8-row sample.)* **Confirm dependencies against business rules, not data.**
- **A *prime* attribute appears in some candidate key.** That definition is what separates 3NF from BCNF.
- **All three anomalies were demonstrated on the unnormalised table:** a partial update left **two charge rates for one job class**; six of seven employees existed on only one project; a job class with no assignment was unstorable.
- **1NF: atomic values, no repeating groups** — the formal name for [[03 - Entity-Relationship Modelling|ch. 03]]'s "no lists in cells".
- **2NF: no nonprime attribute depends on part of a composite key.** *(A single-attribute key makes 2NF vacuous — so **surrogate keys hide 2NF violations rather than fixing them**.)*
- **3NF: no nonprime attribute depends on another nonprime attribute.** *(Verified after decomposition: the charge rate went from stored **4 times to once**, a rate rise from 4 rows to **1**, contradiction became **unrepresentable**, and a new job class became an ordinary insert.)*
- **A decomposition is lossless iff the shared attributes are a superkey of one fragment.** *(Both normalisation steps verified lossless — 8→8 and 7→7, identical.)*
- **⚠️ "Lossy" means the join *invents* rows.** *(Verified: splitting on the non-key `job_class` turned 8 triples into 13, fabricating 5 — including "employee 105 works on project 25".)*
- **Lossy decomposition and [[03 - Entity-Relationship Modelling|ch. 03]]'s fan trap are the same fault**: joining on a key that identifies rows in neither table. **A join is only meaningful when its key identifies rows in at least one side.**
- **BCNF: every determinant is a candidate key** — violable only with overlapping composite candidate keys. *(Verified: with keys `(a+b)` and `(a+c)`, `c → b` is prime→prime, so 3NF holds while BCNF fails, and the pair `(c1,b1)` is stored 3 times.)*
- **3NF is always lossless *and* dependency-preserving; BCNF is always lossless but not always dependency-preserving.** *(Verified: the BCNF split left $A{+}B \to C,D$ unenforceable in any one table.)* **Hence 3NF is the usual target.**
- **Denormalisation measured: 1.6× faster reads** (0.1698 s → 0.1075 s), at the cost of storing one charge rate **4 104 times instead of once**.
- **Denormalise only when writes are batched and controlled** — a warehouse, not a transactional table. **Try an index or a materialised view first.**

## ⚠️ Important Notes

1. **Never infer a functional dependency from data alone.** A scan refutes; only a business rule confirms. Normalising on a sample artefact produces a schema that rejects valid future data.
2. **High-cardinality attributes always look like keys in small samples.** `hours` was reported as a candidate key over 8 rows.
3. **A surrogate key does not normalise anything.** It makes 2NF vacuous and relabels the redundancy as a 3NF violation.
4. **Decompose only on a determinant.** Splitting on a non-key silently fabricates rows on rejoin.
5. **⚠️ Verify every decomposition is lossless** by rejoining and comparing to the original — row count *and* content. Following the normal forms guarantees it; ad-hoc splitting does not.
6. **A join that increases the row count on a many-to-one path is fabricating.** `COUNT(*)` before and after, every time.
7. **The insertion anomaly is the argument that ends the discussion** — it proves the schema cannot store a true fact, and no process discipline fixes it.
8. **Normalisation restricts representable states, not answerable questions.** The join still answers everything; it just cannot express a contradiction.
9. **Stop at 3NF by default.** BCNF removes slightly more redundancy but can leave a constraint unenforceable, which is a different route to the same inconsistency.
10. **BCNF violations require overlapping composite candidate keys.** If your table has one candidate key, 3NF already gives you BCNF.
11. **Do not denormalise a transactional table for a modest read gain.** Add an index first — it speeds reads without duplicating facts.
12. **Prefer a materialised view to hand-maintained denormalisation** — the DBMS keeps it correct, so it cannot drift.
13. **Denormalisation moves a guarantee from the schema into a process.** Write down what that process is, or the guarantee does not exist.
14. **Measure before denormalising.** The gain here was 1.6×, not the order of magnitude usually assumed — and part of even that would have been recovered by indexing.
15. **Higher normal forms exist (4NF for multivalued dependencies, 5NF for join dependencies) but are rarely reached deliberately.** A correct ER model ([[03 - Entity-Relationship Modelling|ch. 03]]) usually lands in 3NF or better without a formal pass.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 6 extracts cleanly as prose** — the need for normalisation, the definitions of 1NF/2NF/3NF/BCNF/4NF, the conversion procedure, the surrogate-key discussion, denormalisation, and the data-modelling checklist all came through readably. **Book page $n$ = PDF page $n+28$; ch. 6 is PDF pages 220–266.**
>
> **All figures are images and are lost**, including the dependency diagrams that are this chapter's principal teaching device — C&M draws each functional dependency as an arrow beneath the table, and the 1NF→2NF→3NF conversion is presented as a sequence of such diagrams. **Figure 6.7 and Figure 6.8 (the multiple-candidate-key and 3NF-not-BCNF cases) are both lost**, though **Figure 6.8's dependencies survive in the prose** ($A{+}B \to C,D$; $A{+}C \to B,D$; $C \to B$), which is enough to reconstruct it exactly.
>
> **Reconstructed content, flagged.** The **project-assignment example** (`proj_num, proj_name, emp_num, emp_name, job_class, chg_hour, hours`) is C&M's running example and its *structure and dependencies* are the book's; **the specific rows are partly reconstructed** — the employee names, project names and charge rates appear in surviving prose fragments, but **the hours and the exact set of assignments are mine**, chosen so that each anomaly is visible in eight rows. **The `bcnf_demo` data is entirely mine**, constructed to satisfy C&M's stated dependencies while making the redundancy countable. **The 200 000-row denormalisation dataset is generated.**
>
> **No error was found in Coronel & Morris ch. 6.**
>
> **Additions beyond the source.** **§1's programmatic dependency detection is mine** — C&M asserts which dependencies hold (they are given in the figures); **testing them turned up two false positives in the book's own example structure**, which produced the "evidence, not proof" warning that is the most transferable idea in the chapter and appears nowhere in the source.
>
> **§5, the lossless-join treatment, is entirely mine.** **C&M does not cover lossless join or dependency preservation at all** — a significant omission, since without them "decompose the table" has no correctness criterion. **Executing a lossy decomposition and listing the five fabricated tuples**, then identifying it as [[03 - Entity-Relationship Modelling|ch. 03]]'s fan trap in formal dress, is my own and unifies three separate failures under one rule (*a join is only meaningful when its key identifies rows in at least one table*).
>
> **The 3NF-versus-BCNF trade table** (lossless always; dependency-preserving only for 3NF) is an addition — C&M presents BCNF as strictly better and does not mention what it costs, which is why it cannot explain why 3NF is the standard target. **§8's denormalisation measurement is mine**; C&M discusses denormalisation qualitatively, and **the honest 1.6× figure — with the caveats that indexing and in-memory data both flatter the normalised side — is more useful than the usual unquantified claim.** The observation in Exercise 2(a) that **surrogate keys hide rather than fix 2NF violations**, and the ordering of alternatives before denormalising in Exercise 4(d), are additions.
>
> **Deliberately compressed.** **4NF and multivalued dependencies** (C&M §6-6b) are noted in Important Note 15 but not developed — they require a specific pathology (two independent multivalued facts in one table) that a sound ER model does not produce. **5NF/join dependencies** (§6-6c) are mentioned only. **§6-4's "improving the design" walkthrough** and **§6-9's data-modelling checklist** are process material already covered by [[03 - Entity-Relationship Modelling|ch. 03]] and [[07 - Database Design|ch. 07]]. **§6-5 on surrogate keys** was largely covered in [[02 - The Relational Model and Relational Algebra|ch. 02]] §2 and appears here only where it bears on 2NF. **§6-7's normalisation-and-design integration** is deferred to [[07 - Database Design|ch. 07]].

**Previous:** [[03 - Entity-Relationship Modelling]] · **Next:** [[05 - SQL Fundamentals]]
