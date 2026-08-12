---
subject: Database Management Systems
chapter: 3
tags: [ds, dbms, er-model, eer, entities, relationships, cardinality, weak-entity, fan-trap, specialisation]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 4–5"
---

# Entity-Relationship Modelling

[[02 - The Relational Model and Relational Algebra|Chapter 02]] described what a relational database *is*. This chapter is about deciding **what tables to have in the first place** — the step where most database failures actually happen.

**An ER model is a design notation, not a storage model.** It sits at the conceptual level of [[01 - Databases and Data Models|ch. 01]] §9: DBMS-independent, discussable with people who do not write SQL, and mapping mechanically onto tables.

**Everything in this chapter is presented as executable `CREATE TABLE` rather than as a diagram** — partly because every ER diagram in the source is a lost image, but mainly because it is more precise. A diagram can be ambiguous about whether participation is optional; `NOT NULL` cannot.

**The centrepiece is §7, the fan trap** — a modelling error that does not raise an error or lose rows but **returns confidently wrong numbers**. It is the sharpest available argument that modelling is an analyst's concern and not just an architect's.

## 📘 Main Knowledge

### 1. Entities and attributes

> [!note] Definitions
> An **entity** is a thing about which data is stored — becomes a **table**; an **entity instance** is one row.
> An **attribute** is a characteristic of an entity — becomes a **column**.

**Attributes come in kinds, and two of them cannot be stored as a single column:**

| kind | example | treatment |
|---|---|---|
| **simple / atomic** | `city` | one column |
| **composite** | `address`, `name` | **decompose into components** |
| single-valued | `date_of_birth` | one column |
| **multivalued** | several phone numbers | **must become its own table** |
| **derived** | `age` | **compute it; do not store it** |

#### 1.1 Composite attributes — decompose them

```sql
    first_name TEXT NOT NULL,      -- 'name' decomposed
    last_name  TEXT NOT NULL,
    street     TEXT,               -- 'address' decomposed
    city       TEXT,
    postcode   TEXT
```

*(Verified: filtering on `city` works.)* **Storing `address` as one blob makes "customers in Hanoi" impossible** — you cannot filter, group, or index on part of a text field reliably. **Decompose to the finest granularity you will ever query at.**

#### 1.2 Derived attributes — compute, don't store

*(Verified:)*
```sql
SELECT cust_id, dob,
       CAST((julianday('2026-07-31') - julianday(dob))/365.25 AS INT) AS age_derived
FROM customer;
--  1 | 1998-03-14 | 28
--  2 | 2001-11-02 | 24
```

**A stored age is wrong the next day.** Store what does not change (`dob`); derive what does. **Storing both invites them to disagree** — §8's redundancy problem in miniature.

#### 1.3 Multivalued attributes — the list-in-a-cell trap

**Wrong:**
```
cust_id | phones
--------+----------------------
1       | 0912345678,0987654321
```

*(Verified, and the failure is worse than it looks:)*
```
exact search for '0987654321'  -> 0 rows      <- the number IS there
LIKE '%0912%'                  -> 1 row       <- but cannot use an index
```

> [!warning] Why a list in a cell is a genuine defect, not a shortcut
> **The exact search returns zero rows for a value that is present.** The only way to find it is `LIKE`, which **cannot use an index** (so it is a full scan) and **matches substrings** — searching for `1234` would match `0912345678`, and searching for `123` would match a different customer's number entirely.
>
> **You also cannot** attach attributes to individual values (which phone is the mobile?), constrain them, count them reliably, or add and remove one without parsing and rewriting the whole string.
>
> **Correct: promote it to its own table** — a 1:M relationship:
> ```sql
> CREATE TABLE cust_phone (
>     cust_id INTEGER NOT NULL REFERENCES customer(cust_id),
>     phone   TEXT NOT NULL,
>     kind    TEXT,                        -- now each phone can have attributes
>     PRIMARY KEY (cust_id, phone)
> );
> ```
> *(Verified: exact, indexable search now works.)* **This is exactly [[02 - The Relational Model and Relational Algebra|ch. 02]]'s atomicity property, and it is what 1NF will formalise ([[04 - Normalization|ch. 04]]).**

### 2. Relationships: connectivity, participation, degree

**Three independent properties, and they are frequently confused.**

#### 2.1 Connectivity (cardinality) — 1:1, 1:M, M:N
Covered in [[02 - The Relational Model and Relational Algebra|ch. 02]] §6: a foreign key on the "many" side for 1:M, a junction table for M:N.

#### 2.2 Participation — optional or mandatory

> [!note] The mechanism is one keyword
> **Mandatory participation = `NOT NULL` on the foreign key.** That is the entire implementation.

*(Verified:)*
```
INSERT INTO employee VALUES (6,'No Dept',NULL,NULL);
-> rejected: NOT NULL constraint failed: employee.dept_id
```

**But the other side cannot be enforced this way at all:**
```
departments with NO employees:
    30 | Research
```
*(Verified.)*

> [!warning] Optional participation on the "one" side is unenforceable by constraint
> *"Every department must have at least one employee"* **cannot be expressed as a column constraint**, because the constraint would have to be checked on the `DEPARTMENT` row when an `EMPLOYEE` row changes.
>
> **It requires a trigger, a deferred constraint, or enforcement in process** — and in practice it is usually left unenforced, which is why empty parent rows accumulate in real databases. **An ER diagram will happily show mandatory participation on both sides; the schema can only deliver one of them.** That gap between the model and what is enforceable is worth knowing before you promise it.

#### 2.3 Degree — unary, binary, ternary
**Binary is the overwhelming norm.** Unary (recursive) is §3. **Ternary relationships should almost always be decomposed** into an associative entity (§5), because a genuine three-way constraint is rare and hard to enforce.

### 3. Recursive relationships

An entity related to itself — an employee manages employees:

```sql
    mgr_id INTEGER REFERENCES employee(emp_id)     -- points at its own table
```

*(Verified — the table joined to itself:)*
```
employee | manager
---------+---------
Nguyen A | (none)
Tran B   | Nguyen A
Le C     | Nguyen A
Pham D   | (none)
Hoang E  | Pham D
```

> [!note] The recursive foreign key must be nullable
> **Somebody has no manager.** A `NOT NULL` recursive foreign key is **unsatisfiable** — the very first row could never be inserted, because there is no existing row for it to point at. *(This is why `mgr_id` is nullable while `dept_id` is not.)*

**And the hierarchy is walked with a recursive CTE** ([[06 - Advanced SQL|ch. 06]]):
```sql
WITH RECURSIVE chain(emp_id, emp_name, lvl) AS (
    SELECT emp_id, emp_name, 0 FROM employee WHERE mgr_id IS NULL
    UNION ALL
    SELECT e.emp_id, e.emp_name, c.lvl+1
    FROM employee e JOIN chain c ON e.mgr_id = c.emp_id)
SELECT lvl, emp_name FROM chain ORDER BY lvl;
```
*(Verified: level 0 = Nguyen A, Pham D; level 1 = Tran B, Le C, Hoang E.)* **This is a [[Data Structures and Algorithms/contents/13 - Graph Algorithms|graph traversal]] — specifically BFS — expressed in SQL.**

### 4. Weak entities and relationship strength

> [!note] Definitions
> A **weak entity** is **existence-dependent** on another and **inherits part of its key** from the parent. The relationship is called **identifying**.
>
> **The test is where the parent's key goes: into the child's primary key (identifying, weak) or merely into a foreign key column (non-identifying, strong).**

```sql
CREATE TABLE dependent (
    emp_id   INTEGER NOT NULL REFERENCES employee(emp_id) ON DELETE CASCADE,
    dep_num  INTEGER NOT NULL,
    dep_name TEXT NOT NULL,
    PRIMARY KEY (emp_id, dep_num)      -- parent's key is PART of the child's key
);
```

```
emp_id | dep_num | dep_name
-------+---------+---------
1      | 1       | Child A
1      | 2       | Child B
2      | 1       | Child C
```

**`dep_num` restarts at 1 for each employee**, which only works because the key is the *pair*. **"Child A" has no identity of its own** — it is *dependent 1 of employee 1*.

*(Verified: deleting employee 2 cascaded, removing Child C — dependents 3 → 2. Existence dependence made real.)*

> [!warning] Each foreign key needs its own referential action — an instructive failure
> Deleting employee **1** was **rejected**, and not because of the dependents:
> ```
> rejected -> FOREIGN KEY constraint failed
> employees still managed by 1:  Tran B, Le C
> ```
> *(Verified.)* **`ON DELETE CASCADE` was declared on `DEPENDENT` but not on `mgr_id`**, so the recursive key blocked the delete.
>
> **This is correct behaviour and the right default.** Cascading on `mgr_id` would mean **deleting a manager deletes their entire reporting tree** — a catastrophic action from a single `DELETE`. **Cascade is appropriate for genuine existence dependence (a dependent cannot outlive the employee) and dangerous everywhere else.** `ON DELETE SET NULL` is usually what a recursive key wants.

### 5. Associative entities: M:N with attributes

**When an M:N relationship has attributes of its own, the junction table is a full entity.**

```sql
CREATE TABLE enrolment (
    stu_id   INTEGER NOT NULL REFERENCES student(stu_id),
    crs_id   TEXT    NOT NULL REFERENCES course(crs_id),
    semester TEXT    NOT NULL,
    grade    REAL,                                -- attribute OF THE RELATIONSHIP
    PRIMARY KEY (stu_id, crs_id, semester)
);
```

**A grade belongs to neither the student nor the course — it belongs to the enrolment.**

> [!note] The key had to grow, and noticing that is the design work
> The obvious key is `(stu_id, crs_id)`. **But students retake courses** — the verified data has Vo K taking `DS101` in both `2025A` and `2025B` — so a two-attribute key **would have rejected a legitimate fact.**
>
> *(Verified: with `semester` in the key, the retake is accepted and a true duplicate is still rejected — `UNIQUE constraint failed: enrolment.stu_id, enrolment.crs_id, enrolment.semester`.)*
>
> **The general lesson: the composite key must include everything that distinguishes two genuine occurrences of the relationship.** Getting this wrong does not corrupt data — it makes valid data *unstorable*, which surfaces months later as "the system won't let me record this".

### 6. Specialisation hierarchies (EER)

**A supertype holds shared attributes; subtypes hold the specific ones.**

```sql
CREATE TABLE person (
    person_id INTEGER PRIMARY KEY NOT NULL,
    name      TEXT NOT NULL,
    p_type    TEXT NOT NULL CHECK (p_type IN ('STUDENT','STAFF'))   -- discriminator
);
CREATE TABLE person_student (
    person_id INTEGER PRIMARY KEY NOT NULL REFERENCES person(person_id),
    programme TEXT NOT NULL
);
CREATE TABLE person_staff (
    person_id INTEGER PRIMARY KEY NOT NULL REFERENCES person(person_id),
    salary    REAL NOT NULL
);
```

*(Verified, including that `p_type='ALIEN'` is rejected by the `CHECK`.)*

**Three ideas:**

- **The subtype discriminator** (`p_type`) says which subtype table to look in.
- **Disjoint vs overlapping:** may an instance belong to more than one subtype? *(Here the `CHECK` makes it disjoint. Overlapping — a person who is both student and staff — would need a different discriminator design, e.g. separate boolean flags or no discriminator at all.)*
- **Completeness:** must every supertype instance belong to some subtype (**total**) or may it belong to none (**partial**)?

**A subtype's primary key being simultaneously a foreign key to the supertype gives exactly 1:1** — the key trick that makes this work.

### 7. The fan trap — a design error that returns wrong numbers

> [!note] Definition
> A **fan trap** occurs when one entity is in **two 1:M relationships** with two other entities, creating an apparent association between those two that the model does not actually record.

**The flawed model:** `DIVISION` 1:M `TEAM`, and `DIVISION` 1:M `PLAYER`. Both relationships are individually correct. **Nothing records which player is on which team.**

```
TEAM                          PLAYER
team_id | team_name | div_id  play_id | play_name | div_id
--------+-----------+------   --------+-----------+------
10      | Hawks     | 1       100     | Player A  | 1
11      | Eagles    | 1       101     | Player B  | 1
12      | Sharks    | 2       102     | Player C  | 1
                              103     | Player D  | 2
```

**Now ask: how many players are on each team?** The only available join path is `TEAM → DIVISION → PLAYER`:

```sql
SELECT t.team_name, COUNT(p.play_id) AS players
FROM team_bad t JOIN player_bad p ON t.div_id = p.div_id
GROUP BY t.team_id;
```

```
team_name | players
----------+--------
Hawks     | 3
Eagles    | 3
Sharks    | 1
```

> [!warning] These numbers are fiction, and nothing says so
> **There are 4 players in total. This result reports 7.** *(Verified: the join produced 7 rows for 4 players.)*
>
> **North division has 2 teams and 3 players, so the join pairs every team with every player in the division** — a $2\times3$ cross product, and each team claims all three players.
>
> **The query is not wrong. The model is.** The information "which player is on which team" was never recorded, so no query can recover it — **but instead of failing, the database returns a plausible, well-formatted, entirely false answer.**

**The fix is to chain the relationships:** `DIVISION` 1:M `TEAM` 1:M `PLAYER`, with `player.team_id` pointing at `TEAM` rather than at `DIVISION`.

```
team_name | players        players per division:
----------+--------        div_name | players
Hawks     | 2              ---------+--------
Eagles    | 1              North    | 3
Sharks    | 1              South    | 1
```
*(Verified: 4 join rows for 4 players — no inflation. And the division is still reachable **transitively** through `TEAM`.)*

> [!note] The general principle, worth carrying beyond databases
> **If B and C are both children of A, that does not relate B to C.** Joining them through A fabricates a cross product within each group of A.
>
> **The division did not need its own link to players** — it is reachable through the team, and storing it directly is precisely what creates the trap. **A relationship that is derivable by composition should be derived, not stored.**
>
> **For an analyst this is the important paragraph of the chapter.** The symptom is inflated counts and sums after a join, and it is easy to mistake for a data-quality problem when it is a modelling problem. **`COUNT(*)` before and after a join** ([[02 - The Relational Model and Relational Algebra|ch. 02]] §4.7) catches both.

### 8. Redundant relationships — the same error from the other side

**What if we kept `player.div_id` *as well as* `player.team_id`?** Both foreign keys are valid, so referential integrity is satisfied — and the two paths to the division can disagree:

```
play_id | stored_div | div_via_team
--------+------------+-------------
103     | 1          | 2
```

*(Verified: player 103 is on the Sharks, which are in the South division (2), but is recorded as division 1.)*

> [!warning] Referential integrity does not detect this
> **Both `team_id` and `div_id` point at rows that exist**, so every constraint passes. **The contradiction is invisible to the DBMS**, and the two paths silently give different answers to the same question depending on which join you write.
>
> **`div_id` is derivable from `team_id`, so storing it is redundancy** — and this is [[01 - Databases and Data Models|ch. 01]] §3.1's update anomaly wearing a different hat. **Derivable data should be derived** (§1.2's rule about `age`, applied to relationships).

### 9. Time-variant data

**Overwriting an attribute destroys the past.** If salary history matters, the attribute becomes a 1:M relationship:

```sql
CREATE TABLE emp_salary (
    emp_id     INTEGER NOT NULL,
    salary     REAL NOT NULL,
    valid_from TEXT NOT NULL,
    valid_to   TEXT,                  -- NULL = current
    PRIMARY KEY (emp_id, valid_from)
);
```

*(Verified:)*
```
current salary          -> WHERE valid_to IS NULL              -> 39000
salary as at 2024-06-15 -> BETWEEN valid_from AND valid_to     -> 34000
```

**This is the **slowly changing dimension** of [[10 - Data Warehouses and OLAP|ch. 10]], met early** — and the decision "do we need history?" is a business rule, not a technical preference. **Getting it wrong is unrecoverable in one direction only:** you can always stop keeping history, but you cannot reconstruct history you never kept.

## ✏️ Exercises

**1. (Attributes.)** (a) Name the attribute kinds. (b) Why decompose composite attributes? (c) Why is a list in a cell a defect — use the verified searches. (d) Why not store derived attributes?

> [!example]- Solution
> **(a) Simple/atomic, composite, single-valued, multivalued, derived.** **Two need structural work: multivalued (→ its own table) and derived (→ computed, not stored).**
>
> **(b) Because you can only query at the granularity you stored.** *(Verified: with `city` as its own column, "customers in Hanoi" is a simple indexed filter.)* With `address` as one blob it becomes a `LIKE '%Hanoi%'` — a full scan that also matches an address on "Hanoi Street" in another city.
>
> **The rule: decompose to the finest granularity you will ever query, group, sort or index at.** Recomposition is trivial (concatenate); decomposition after the fact requires parsing free text, which is unreliable.
>
> **(c) Because the value becomes unfindable and unconstrained.** *(Verified:)*
> ```
> exact search for '0987654321' -> 0 rows    <- the value IS stored
> LIKE '%0912%'                 -> 1 row
> ```
> **The exact search fails on data that is present** — the cell contains `'0912345678,0987654321'`, which is not equal to either number.
>
> **`LIKE` is not a fix.** It cannot use an index, so it is always a full table scan; and it matches substrings, so searching `1234` matches `0912345678` and returns a false positive. **You get both false negatives (exact) and false positives (`LIKE`).**
>
> **Beyond searching, you cannot** attach attributes to individual values (which is the mobile?), apply constraints or foreign keys, count reliably, or add/remove one value without parsing and rewriting the string — with every concurrent writer racing on the same cell.
>
> **The fix is a 1:M table**, and *(verified)* exact search then works and each phone carries its own `kind`. **This is [[02 - The Relational Model and Relational Algebra|ch. 02]]'s atomicity and [[04 - Normalization|ch. 04]]'s 1NF.**
>
> *(The trap is seductive because JSON columns make it feel modern. They are appropriate for genuinely schema-less payloads — not for a field you filter and join on.)*
>
> **(d) Because a stored derivation can disagree with what it was derived from.** *(Verified: age computed from `dob` gives 28 and 24.)* **A stored `age` is wrong the next day**, and then the database asserts both a birth date and an inconsistent age.
>
> **Store what does not change; derive what does.** The same principle rules out §8's stored `div_id` — and note it is the update anomaly again ([[01 - Databases and Data Models|ch. 01]]), which is why one principle keeps reappearing.
>
> **The counter-consideration is cost.** Deriving on every read is work, so if the computation is expensive and read constantly you may store it — **but then you own the job of keeping it correct** (a trigger, a materialised view, a scheduled refresh). **That is a deliberate trade, exactly like [[10 - Data Warehouses and OLAP|ch. 10]]'s denormalisation, and it is only safe when named as one.**

**2. (Relationships.)** (a) Distinguish connectivity, participation and degree. (b) How is mandatory participation implemented, and what cannot be? (c) Why must a recursive foreign key be nullable? (d) What distinguishes a weak entity?

> [!example]- Solution
> **(a) Three independent properties.**
>
> **Connectivity (cardinality)** — how many of each side: 1:1, 1:M, M:N. **Participation** — whether an instance *must* take part: optional or mandatory. **Degree** — how many entities the relationship involves: unary, binary, ternary.
>
> **They are independent**, which is why they are confused: a 1:M relationship may be optional or mandatory on either side, giving four combinations for one connectivity.
>
> **(b) Mandatory participation is `NOT NULL` on the foreign key** — the whole mechanism. *(Verified: an employee with `dept_id NULL` was rejected.)* A nullable foreign key means optional participation.
>
> **What cannot be implemented that way is a minimum on the "one" side.** *"Every department must have at least one employee"* is a constraint on `DEPARTMENT` that is violated by changes to `EMPLOYEE` — no column constraint can express it. *(Verified: `Research` exists with no employees.)*
>
> **It requires a trigger, a deferred constraint checked at commit, or process discipline** — and there is a chicken-and-egg problem too: you cannot insert the department before its first employee or the employee before their department, so any strict enforcement needs deferred checking within a transaction ([[08 - Transactions and Concurrency Control|ch. 08]]).
>
> **The practical point: an ER diagram can show mandatory participation on both sides, and the schema can only deliver one.** Know which half of your diagram is documentation rather than enforcement.
>
> **(c) Because the first row would have nothing to point at.**
>
> A `NOT NULL` recursive foreign key is **unsatisfiable**: the first employee's `mgr_id` must reference an existing employee, and there are none. **The table could never be populated.** *(Verified: two employees have `mgr_id IS NULL`, correctly shown as `(none)`.)*
>
> **The general form: any recursive hierarchy needs a root, and the root is marked by a null.** The alternative — a self-referencing row where the CEO manages themselves — makes traversal loop forever unless every query special-cases it, so the null is much cleaner.
>
> **Two consequences.** **Traversal needs a recursive CTE**, anchored on `WHERE mgr_id IS NULL` *(verified: levels 0 and 1 correctly identified)* — a BFS ([[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]]) in SQL. **And nothing prevents a cycle** — A manages B manages A — which a recursive CTE will follow forever. Cycle prevention needs a trigger or application logic.
>
> **(d) A weak entity is existence-dependent and inherits part of its key from its parent.**
>
> **The test is where the parent's key lands: inside the child's primary key (identifying → weak) or in an ordinary foreign key column (non-identifying → strong).**
>
> *(Verified: `PRIMARY KEY (emp_id, dep_num)`, so `dep_num` restarts at 1 for each employee — possible only because the key is the pair. "Child A" is not an independent thing; it is *dependent 1 of employee 1*.)*
>
> **Existence dependence was made real by `ON DELETE CASCADE`**: deleting employee 2 removed Child C, dependents 3 → 2 *(verified)*.
>
> **But the attempt to delete employee 1 was rejected** *(verified)* — by the **recursive `mgr_id` key**, not the dependents. **Each foreign key carries its own referential action**, and cascading on `mgr_id` would mean one `DELETE` silently removing a manager's entire reporting tree. **Cascade only where existence dependence is genuine; `ON DELETE SET NULL` or `RESTRICT` elsewhere.**

**3. (Hard — the fan trap.)** (a) What is it and why is the flawed model individually correct? (b) Explain the wrong numbers exactly. (c) Why is it dangerous? (d) State the general principle and how to detect it.

> [!example]- Solution
> **(a) One entity in two 1:M relationships with two others, implying an association between those two that is never recorded.**
>
> `DIVISION` 1:M `TEAM` and `DIVISION` 1:M `PLAYER`. **Each relationship is true**: a division does have many teams, and does have many players. **What is missing is the relationship that actually matters** — which player plays for which team.
>
> **That is what makes it a trap rather than an obvious error.** Every business rule stated is faithfully represented; the fault is a rule that was never stated. **The diagram looks complete**, and the fan-out from `DIVISION` to two children is where the name comes from.
>
> **(b)** *(Verified:)*
> ```
> Hawks  | 3        <- actually 2
> Eagles | 3        <- actually 1
> Sharks | 1        <- correct by luck (one team, one player in that division)
> ```
> **The only join path is `TEAM → DIVISION → PLAYER`.** North division contains 2 teams and 3 players, so matching on `div_id` pairs **every team with every player in that division** — a $2\times3=6$-row cross product, plus South's $1\times1$, giving **7 rows for 4 players** *(verified)*.
>
> **Each North team therefore claims all 3 North players, and the reported total is 7 players in a league of 4.**
>
> **Sharks is right by accident** — South has one team and one player, so the cross product is $1\times1$. **That is what makes the bug hard to spot: it is not uniformly wrong.** Small or singleton groups look correct, and only larger groups inflate — so a spot-check on a small division would pass.
>
> **(c) Because it fails silently, plausibly, and in the one way that survives review.**
>
> **No error is raised.** The SQL is valid, the foreign keys are valid, the join runs. **The output is well-formed and plausible** — small positive integers where you expect small positive integers.
>
> **The information was never recorded, so no query could recover it** — but instead of being unable to answer, the database answers wrongly. **A missing table would have caused an error; a missing *relationship* causes a wrong number.**
>
> **Compare the failure modes in this vault so far:** [[01 - Databases and Data Models|ch. 01]]'s deletion anomaly destroys data silently; [[02 - The Relational Model and Relational Algebra|ch. 02]]'s inner join drops rows silently; **the fan trap invents rows silently.** All three share the property that makes them expensive — **nothing in the system objects** — and it is why "the query ran" is never evidence that the answer is right.
>
> **It is also an *analyst's* problem, not only a designer's.** You typically inherit the schema; the fan trap arrives as an inflated total that looks like double-counting or a data-quality issue, when the real cause is that the join you wrote was the only one available and it was meaningless.
>
> **(d) Principle: if B and C are both children of A, that does not relate B to C.** Joining them through A produces a cross product within each group of A.
>
> **The fix is to chain the relationships:** `DIVISION` 1:M `TEAM` 1:M `PLAYER`, with `player.team_id` pointing at the team. *(Verified: 4 join rows for 4 players; per-team counts 2, 1, 1; and the per-division counts 3 and 1 remain available **transitively** through `TEAM`.)*
>
> **Note the division link is not lost — it was never needed.** Storing it directly is what created the trap, and §8 shows that keeping *both* paths lets them contradict each other *(verified: player 103 on a South team recorded as division 1, with every constraint satisfied)*. **A relationship derivable by composition should be derived.**
>
> **Detection, in order of usefulness:**
> 1. **`COUNT(*)` before and after every join.** Rows should not increase when joining on what you believe is a many-to-one path. Inflation means either a fan trap or an unexpected duplicate key.
> 2. **Sanity-check totals against an independent count.** 7 reported players against `SELECT COUNT(*) FROM player` = 4 is immediate.
> 3. **Ask what the join key *means*.** Joining two tables on a key that is a *parent* of both, rather than a key of one of them, is the structural signature.
> 4. **Beware `SUM` more than `COUNT`.** An inflated `COUNT` may look odd; an inflated `SUM` of revenue just looks like a good quarter.
>
> **The deeper lesson: a join is only meaningful when the join key identifies rows in at least one of the tables.** `div_id` identifies neither a team nor a player, so `ON t.div_id = p.div_id` was never a meaningful pairing — it was a grouping dressed up as a join.

**4. (EER and history.)** (a) Explain supertype/subtype with the discriminator. (b) What are disjoint/overlapping and completeness? (c) Why did the enrolment key need `semester`? (d) Why model time-variant data as 1:M?

> [!example]- Solution
> **(a) The supertype holds attributes shared by all instances; each subtype holds those specific to it.**
>
> `PERSON` holds `name`; `PERSON_STUDENT` holds `programme`; `PERSON_STAFF` holds `salary`. **The subtype's primary key is simultaneously a foreign key to the supertype**, which is what enforces exactly 1:1 — one subtype row per supertype row at most.
>
> **The discriminator (`p_type`) records which subtype applies**, so you know which table to look in without probing all of them. *(Verified: a `CHECK` constraint rejected `p_type='ALIEN'`, so the discriminator cannot take a meaningless value.)*
>
> **Why bother, rather than one wide table?** A single `PERSON` table with both `programme` and `salary` would leave one of them null on every row — nulls that mean "not applicable" rather than "unknown", which is a different thing and cannot be constrained. **With subtypes, `salary` can be `NOT NULL` where it applies**, which is impossible in the wide design.
>
> **The cost is joins**, so the wide-table alternative is legitimate when subtypes have few distinct attributes. **This is the same normalisation-versus-read-cost trade as everywhere else.**
>
> **(b) Disjointness: may an instance belong to more than one subtype?**
> - **Disjoint** — student *or* staff, never both. *(Verified: the `CHECK` on a single `p_type` column enforces this, because one column holds one value.)*
> - **Overlapping** — a person may be both, e.g. a PhD student who teaches. **A single discriminator column cannot express this**; you need boolean flags per subtype, or no discriminator and a probe of the subtype tables.
>
> **Completeness: must every supertype instance be in some subtype?**
> - **Total** — every person is a student or staff. **Also not enforceable by a column constraint**, for the same reason as §2.2's minimum participation: it constrains `PERSON` but is violated by what is absent from the subtype tables.
> - **Partial** — a person may be neither.
>
> **So of the four EER constraints, the schema enforces disjointness cleanly and completeness not at all.** Another instance of the diagram promising more than the schema delivers.
>
> **(c) Because students retake courses, and `(stu_id, crs_id)` would make a true fact unstorable.**
>
> *(Verified: Vo K took `DS101` in both `2025A` and `2025B`.)* With a two-attribute key the second enrolment would be rejected as a duplicate — **and it is not a duplicate, it is a different event with a different grade.**
>
> **With `semester` in the key both retakes are stored and a genuine duplicate is still rejected** *(verified: `UNIQUE constraint failed` on re-inserting the same triple)*.
>
> **The general rule: the composite key must contain everything that distinguishes two genuine occurrences of the relationship.**
>
> **This failure mode is worth contrasting with the others in this chapter.** The fan trap and redundant relationships let you *store wrong things*; an over-narrow key stops you *storing right things*. **The second is less dangerous — it fails loudly** — but it surfaces late, as "the system won't let me enter this", long after the schema is in production and hard to change.
>
> **The diagnostic question is temporal:** *can this relationship happen more than once between the same two entities?* Enrolments, orders, visits, payments — usually yes, and then a date or sequence number belongs in the key. *(A surrogate key plus a `UNIQUE` constraint on the natural triple is often cleaner in practice.)*
>
> **(d) Because an attribute that changes over time is not one value but a series, and a column holds one value.**
>
> Overwriting a salary **destroys the past irrecoverably**. Modelling it as a 1:M history table with `valid_from`/`valid_to` keeps every version:
> ```
> current salary          -> WHERE valid_to IS NULL           -> 39000
> salary as at 2024-06-15 -> BETWEEN valid_from AND valid_to   -> 34000
> ```
> *(Both verified.)*
>
> **The `valid_to IS NULL` convention marks the current row**, which makes "current" a cheap indexed lookup rather than a `MAX(valid_from)` subquery.
>
> **Why the decision is high-stakes: it is asymmetric.** **You can always stop keeping history; you can never reconstruct history you did not keep.** So when it is genuinely unclear, keeping it is the recoverable choice — and it is a business rule ([[01 - Databases and Data Models|ch. 01]] §7), not a technical preference: *"must we be able to answer what this employee earned in 2024?"*
>
> **This is the slowly changing dimension of [[10 - Data Warehouses and OLAP|ch. 10]]** — specifically Type 2 — and the same structure supports audit trails and regulatory reporting. **For a data scientist it is also what makes point-in-time correctness possible**: training a model on today's salary to predict a 2024 outcome leaks the future, and only a history table lets you reconstruct what was actually known then.

## 📝 Summary

- **An ER model is a design notation at the conceptual level** — DBMS-independent and mapping mechanically onto tables. Here it is given as executable `CREATE TABLE`, which is more precise than a diagram.
- **Composite attributes must be decomposed** to the finest granularity you will ever query at; recomposition is easy, decomposition after the fact is not.
- **Derived attributes should be computed, not stored** *(verified: age from `dob`)* — a stored age is wrong the next day.
- **Multivalued attributes must become their own table.** *(Verified: an exact search for a phone number stored in a comma-separated cell returned **0 rows** despite the value being present; `LIKE` finds it but cannot use an index and matches substrings.)*
- **Connectivity, participation and degree are three independent properties** of a relationship.
- **Mandatory participation = `NOT NULL` on the foreign key** *(verified)*. **A minimum on the "one" side cannot be enforced by any column constraint** *(verified: an employee-less department)* — it needs a trigger or process.
- **A recursive foreign key must be nullable**, or the first row could never be inserted. Hierarchies are then walked with a recursive CTE — a [[Data Structures and Algorithms/contents/13 - Graph Algorithms|BFS]] in SQL *(verified)*.
- **A weak entity is existence-dependent and inherits part of its key**; the test is whether the parent's key sits *inside* the child's primary key. *(Verified: `dep_num` restarts per employee; `ON DELETE CASCADE` removed the dependent with its parent.)*
- **Each foreign key needs its own referential action** *(verified: deleting a manager was blocked by the recursive key, not the dependents)*. **Cascade only where existence dependence is genuine.**
- **An M:N junction becomes an entity once the relationship has attributes** — a grade belongs to the enrolment, not to the student or the course.
- **The composite key must include everything distinguishing two genuine occurrences.** *(Verified: without `semester`, a legitimate retake would have been rejected.)*
- **EER: supertype holds shared attributes, subtypes the specific ones**, with a discriminator saying which applies and the subtype PK doubling as a FK to give 1:1. **Disjointness is enforceable by a `CHECK`; completeness is not.**
- **⚠️ The fan trap:** one entity in two 1:M relationships implies an association it never records. *(Verified: per-team player counts of **3, 3, 1** in a league with **4 players** — the join produced 7 rows. Correct answers are 2, 1, 1.)*
- **The trap is not uniformly wrong** — singleton groups come out right, so spot-checks pass. **Fix by chaining the relationships**; the division stays reachable transitively.
- **Redundant relationships let two join paths disagree** *(verified: a player on a South team recorded as North)* **while every foreign key remains valid, so the DBMS cannot detect it.**
- **Time-variant attributes become a 1:M history table** with `valid_from`/`valid_to` *(verified: current and as-at-date queries)*. **The decision is asymmetric — you can stop keeping history, but never reconstruct it.**

## ⚠️ Important Notes

1. **Decompose composite attributes** to the finest granularity you will ever filter, group or index on.
2. **Never store a list in a cell.** Exact search fails on data that is present, `LIKE` cannot use an index and gives false positives, and you cannot constrain or attach attributes to the individual values.
3. **A JSON column is not an exemption.** It is right for genuinely schema-less payloads, wrong for anything you filter or join on.
4. **Do not store derived values** unless the computation is expensive and read constantly — and then own the job of keeping them correct.
5. **Mandatory participation is `NOT NULL` on the foreign key.** If your diagram shows a minimum on the "one" side, know that the schema is not enforcing it.
6. **A recursive foreign key must be nullable**, and nothing prevents cycles in it — a recursive CTE will loop forever on one.
7. **Weak entity ⇔ the parent's key is inside the child's primary key.** If it is merely a foreign key column, the entity is strong.
8. **⚠️ `ON DELETE CASCADE` belongs only where existence dependence is genuine.** On a recursive key it means deleting a manager deletes their whole reporting tree.
9. **Expect junction tables to acquire attributes** — and check whether the two-column key is still sufficient once they do.
10. **Ask whether a relationship can recur between the same two entities.** If it can, a date or sequence number belongs in the key, or the schema will reject valid data.
11. **⚠️ Never join two tables on a key that is a parent of both.** That is the fan trap's structural signature — the key identifies rows in neither table.
12. **`COUNT(*)` before and after every join.** Rows increasing on a supposedly many-to-one path means a fan trap or an unexpected duplicate key.
13. **An inflated `SUM` is more dangerous than an inflated `COUNT`** — it just looks like a good quarter.
14. **The fan trap is not uniformly wrong.** Singleton groups give correct answers, so small-sample checks will not catch it.
15. **Do not store a relationship that is derivable by composition.** Two paths to the same fact will eventually disagree, and referential integrity will not notice.
16. **Decide about history before you need it.** You can stop keeping it; you cannot reconstruct it — and without it, point-in-time correctness for modelling is impossible.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 4–5 extract cleanly as prose** — entity and attribute types, connectivity/participation/degree, relationship strength and weak entities, the EER constructs (supertype/subtype, discriminator, disjoint/overlapping, completeness), primary-key guidance, and all four design cases came through readably. **Book page $n$ = PDF page $n+28$; ch. 4–5 are PDF pages 136–219.**
>
> **This is the worst-hit chapter in the subject for lost figures, and it is not close.** **Every ER diagram is an image**, and in these two chapters the diagrams *are* the content: Chen and Crow's Foot notation side by side, the entity-instance illustrations, the full ERD walkthrough of §4-2, **Figure 5.12 (the fan trap) and Figure 5.13 (its correction)**, and every specialisation hierarchy. **The prose refers to them continuously** ("as you can see in Figure 5.12"), so the argument is repeatedly incomplete on its own.
>
> **The response was to rebuild every construct as an executable schema** rather than attempt to redraw diagrams — which is more precise, since a diagram cannot show whether a constraint is actually enforced, and §2.2, §4 and §6 all turn on exactly that distinction.
>
> **Reconstructed content, flagged:** the JCB-league fan-trap example names `DIVISION`, `TEAM` and `PLAYER` and states the relationships, so the *structure* is the book's — **but all the data (Hawks, Eagles, Sharks, Players A–D and their assignments) is mine**, chosen so that North division has 2 teams and 3 players, which is what makes the inflation visible. **Every other schema and dataset in this chapter — customers, employees, dependents, students, enrolments, persons, salaries — is entirely my own.** *(Crow's Foot notation itself is not reproduced; it cannot be conveyed in text, and the reader should consult any ER-diagram reference alongside this note.)*
>
> **No error was found in Coronel & Morris ch. 4–5.**
>
> **Additions beyond the source.** **The fan-trap demonstration (§7) is mine and is the chapter's centrepiece.** C&M explains the trap in prose and two figures but **never shows the wrong answer it produces** — executing it turns "the relationships are not properly identified" into *"this query reports 7 players in a 4-player league, and 3 of the 3 numbers are wrong in a way that passes a spot-check."* **The observation that singleton groups come out correct — so the bug survives small-sample testing — is my own and is the practically important part.**
>
> **§8's redundant-relationship demonstration is mine**: C&M discusses redundant relationships abstractly, and showing two valid foreign keys yielding contradictory answers *while referential integrity is fully satisfied* is what makes the point land. **§1.3's multivalued-attribute searches are mine** — the exact-match returning 0 rows on present data is more convincing than the assertion that lists are bad. **The `ON DELETE CASCADE` failure in §4 was not planned**: the delete was blocked by the recursive `mgr_id` key, which is a better lesson than the one intended, so it is reported as it happened. **The recursive-CTE hierarchy walk, the cross-links to [[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]] (BFS) and to [[10 - Data Warehouses and OLAP|ch. 10]] (slowly changing dimensions), and the point in Exercise 4(d) about point-in-time correctness for model training** are all additions.
>
> **The repeated theme — that a diagram promises more than a schema can enforce** (minimum participation, completeness constraints) — is my framing, not the book's, and is drawn from testing each construct rather than describing it.
>
> **Deliberately compressed.** **Chen versus Crow's Foot notation** (C&M §4-1) is not reproduced — it is irreducibly graphical, and this vault's schemas carry the same information unambiguously. **§4-2's full step-by-step Tiny College ERD development** (some 25 pages, almost entirely figures) is not reproduced; its constructs are covered individually here. **§4-3 on conflicting design goals** is folded into the trade-off remarks in §6 and Exercise 1(d). **§5-2 entity clustering** is omitted — it is a diagram-simplification device with no schema consequence. **§5-3's primary-key guidance** was largely covered in [[02 - The Relational Model and Relational Algebra|ch. 02]] §2 and is not repeated. **§5-4a (implementing 1:1 relationships)** appears only as the subtype mechanism in §6. **Ternary relationships** are mentioned in §2.3 but not implemented, since the recommended treatment is to decompose them into associative entities, which §5 covers.

**Previous:** [[02 - The Relational Model and Relational Algebra]] · **Next:** [[04 - Normalization]]
