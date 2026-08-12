---
subject: Database Management Systems
chapter: 7
tags: [ds, dbms, database-design, dblc, sdlc, conceptual-design, logical-design, physical-design, constraints]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 9"
---

# Database Design

**This is the chapter that ties [[03 - Entity-Relationship Modelling|ch. 03]] and [[04 - Normalization|ch. 04]] together into a procedure.** ER modelling gives you entities; normalisation removes anomalies; **this chapter says in what order to do them, and what else has to happen around them.**

It is also the most *methodological* chapter in the book, and honesty requires saying so: **Coronel & Morris is a business-school text, and ch. 9 is process** — life cycles, phases, deliverables. Much of it is not verifiable by running anything.

**So this note does one thing the source does not.** §3 takes a complete design, states its business rules explicitly, and then **tests every rule by trying to violate it** — establishing which rules the schema actually enforces and which are merely documentation. **The answer is 6 of 10**, and the three failures fall into three named classes that no `CHECK` constraint can express.

That audit is the practical content of database design: **a design is not "the diagram", it is the set of guarantees you can actually make.**

## 📘 Main Knowledge

### 1. The Database Life Cycle

C&M nests the **DBLC** inside the broader **SDLC** (planning → analysis → detailed design → implementation → maintenance). The database-specific phases:

| phase | produces |
|---|---|
| **1. Initial study** | scope, objectives, and the problems the database must solve |
| **2. Design** | **conceptual → DBMS selection → logical → physical** (§2) |
| **3. Implementation and loading** | the created database, populated |
| **4. Testing and evaluation** | verification, performance tuning, backup/recovery plans |
| **5. Operation** | the system in use |
| **6. Maintenance and evolution** | schema changes, new requirements |

> [!note] What is worth taking from this
> **The phases are not the insight — the ordering constraint is.** Conceptual design must precede DBMS selection, because **a conceptual model that assumes a product cannot be evaluated against alternatives.** And physical design must come last, because it optimises a logical model that must first be *correct*.
>
> **Phase 6 is where most real time goes, and it is the one the diagram never shows.** Requirements change, so the schema must too — which is the real argument for normalisation ([[04 - Normalization|ch. 04]]) and for views as a stable interface ([[06 - Advanced SQL|ch. 06]] §9): both make later change survivable.

### 2. The three design levels

**These are [[01 - Databases and Data Models|ch. 01]] §9's abstraction levels used as a *sequence*:**

| level | question | output | depends on the DBMS? |
|---|---|---|---|
| **Conceptual** | *what does the business mean?* | ER model, business rules | **no** |
| **Logical** | *how does that become tables?* | schema, normalised | somewhat |
| **Physical** | *how is it stored and accessed?* | indexes, storage, partitioning | **entirely** |

> [!note] The discipline is to not skip ahead
> **Conceptual design is DBMS-independent on purpose** — it can be discussed with people who do not write SQL, and it survives a change of product. **Deciding at the conceptual stage that something will be "a `VARCHAR(50)` with an index" is deciding too early.**
>
> **Logical design is where [[04 - Normalization|ch. 04]] applies**: map entities to tables, then validate by normalising, then validate the constraints, then validate against the original requirements — which is §3.
>
> **Physical design changes cost, never meaning** — and §6 demonstrates exactly that.

### 3. Auditing a design — which rules does the schema actually enforce?

**Ten business rules for a small student-records database:**

| | rule |
|---|---|
| R1 | A course has a unique code and a title. |
| R2 | A student has a unique id and a name. |
| R3 | A student enrols in many courses; a course has many students. |
| R4 | An enrolment records a grade, **which may not yet be known**. |
| R5 | A grade, once recorded, is between 0 and 10. |
| R6 | A student **may retake** a course in a later semester. |
| R7 | A course belongs to **exactly one** department. |
| R8 | A department has **at least one** course. |
| R9 | A student may not enrol in **more than 5** courses in one semester. |
| R10 | A course's credit value **never changes** once students have enrolled. |

**The schema:**

```sql
CREATE TABLE course (                                    -- R1, R7
    crs_code  TEXT PRIMARY KEY NOT NULL,
    title     TEXT NOT NULL,
    credits   INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 10),
    dept_code TEXT NOT NULL REFERENCES dept(dept_code)   -- NOT NULL = exactly one
);
CREATE TABLE enrolment (                                 -- R3, R4, R5, R6
    stu_id   INTEGER NOT NULL REFERENCES student(stu_id),
    crs_code TEXT    NOT NULL REFERENCES course(crs_code),
    semester TEXT    NOT NULL,
    grade    REAL    CHECK (grade IS NULL OR grade BETWEEN 0 AND 10),
    PRIMARY KEY (stu_id, crs_code, semester)             -- semester in the key: R6
);
```

**Now test each rule by attempting to violate it** *(all results verified)*:

| rule | result |
|---|---|
| **R1** unique course code | **ENFORCED** — `UNIQUE constraint failed: course.crs_code` |
| **R2** unique student id | **ENFORCED** — `UNIQUE constraint failed: student.stu_id` |
| **R4** grade may be null | **ENFORCED** — the null insert was accepted, as intended |
| **R5** grade in 0–10 | **ENFORCED** — `CHECK constraint failed` on 11.0 |
| **R6** retakes allowed | **ENFORCED** — the second semester was accepted |
| **R7** exactly one department | **ENFORCED** — `NOT NULL constraint failed: course.dept_code` |
| **R8** department has ≥1 course | **❌ NOT ENFORCED** |
| **R9** at most 5 per semester | **❌ NOT ENFORCED** |
| **R10** credits cannot change | **❌ NOT ENFORCED** |

*(R3 is structural — the junction table **is** the M:N relationship, so it is realised rather than constrained, and cannot be "violated".)*

**Scorecard: 6 of 10 rules live in the schema.**

### 4. The three constraint classes `CHECK` cannot express

**Each failure has a specific, nameable cause** — this is the transferable part.

#### R8 — minimum cardinality on the "one" side
```
departments with no courses: Physics, Empty Department
```
*(Verified.)* **The constraint belongs to `DEPT` but is violated by what is absent from `COURSE`.** No column constraint can see that. *(This is [[03 - Entity-Relationship Modelling|ch. 03]] §2.2's finding, now confirmed on a real design — and note the chicken-and-egg problem: you cannot insert the department before its first course, nor the course before its department, so even a trigger needs deferred checking inside a transaction.)*

#### R9 — aggregate constraints
```
student 1 now has 6 enrolments in 2026A (limit was 5)
```
*(Verified.)* **`CHECK` evaluates against a single row.** R9 depends on a `COUNT` over *other* rows, which is outside its visibility.

#### R10 — transition constraints
```
credits 3 -> 6 while 4 students are enrolled
```
*(Verified.)* **`CHECK` sees only the new value, never the old one.** R10 restricts how a value may *change*, which is a statement about a pair of states, not about a state.

> [!warning] All three need a trigger, application logic — or they hold nowhere
> **And "nowhere" is the default.** If nobody writes the rule down, the schema silently does not enforce it and no one discovers this until the data is already wrong.
>
> **This is what a design document is actually for.** Not to describe the tables — the DDL does that better — but to record **which guarantees are enforced where**: this rule by a constraint, that one by a trigger, this other one by application code, and this one not at all (accepted risk).
>
> **The general principle, and the strongest form of a theme running through this whole subject:** [[03 - Entity-Relationship Modelling|ch. 03]] found that a diagram promises more than a schema delivers; [[01 - Databases and Data Models|ch. 01]], [[02 - The Relational Model and Relational Algebra|ch. 02]] and [[05 - SQL Fundamentals|ch. 05]] found that SQLite delivers less than its DDL claims. **Here: a requirements list promises more than any schema can deliver.** In every case the remedy is the same — **test the constraint by trying to violate it.**

### 5. Validating the logical model

C&M's four validation steps, which §3 is an instance of:

1. **Map the conceptual model to tables** — entities to tables, relationships to foreign keys, M:N to junction tables ([[03 - Entity-Relationship Modelling|ch. 03]]).
2. **Validate by normalising** — [[04 - Normalization|ch. 04]]; if normalisation forces a change, the ER model was wrong.
3. **Validate the integrity constraints** — §3's audit.
4. **Validate against user requirements** — write the queries the users actually asked for and check they run.

> [!note] Step 4 is the one that gets skipped, and it catches a specific failure
> **A schema can be perfectly normalised and still unable to answer the question the business asked.** [[03 - Entity-Relationship Modelling|Ch. 03]] §7's fan trap is exactly this — every relationship correct, every table in 3NF, and *"how many players on each team"* unanswerable.
>
> **The test is cheap: write the actual queries against sample data before building anything.** A relationship you cannot traverse is a relationship you did not model.

### 6. Physical design changes cost, not meaning

*(Verified — 300 000 enrolment rows, "all enrolments for one student":)*

| | time | query plan |
|---|---|---|
| no index | 0.0081 s | `SCAN big_enrol` |
| **with index** | **below timer resolution** | **`SEARCH big_enrol USING INDEX idx_enrol_stu (stu_id=?)`** |

**Same answer both times** *(verified: `(11, 5.509)`)*.

> [!note] The point is what did *not* change
> **Identical logical model, identical data, identical query, identical answer.** Only the physical design changed.
>
> **Physical design cannot alter what the database means — only what it costs.** That is precisely why it comes last: there is no point optimising a model that is wrong, and a correct model can always be optimised afterwards without changing any query.
>
> **The timing ratio here is not worth quoting** — the indexed time is at the edge of the timer's resolution, so any figure would be noise. **The query plan is the solid evidence**: `SCAN` (read every row) became `SEARCH … USING INDEX`. **[[09 - Query Optimization and Indexing|Ch. 09]] measures this properly**; here it only illustrates the separation of levels.

### 7. Design strategies

| | |
|---|---|
| **Top-down** | identify entities first, then their attributes. Suits a new system designed from requirements. |
| **Bottom-up** | identify attributes first, then group them into entities. Suits an existing system with known data. |
| **Centralised** | one designer/team, one model. Fine for small or medium scope. |
| **Decentralised** | separate models per subsystem, then **integrated** — needed for large systems, and the integration step is where conflicts surface. |

**In practice designs are built both ways at once**: top-down for structure, bottom-up when working from existing files or reports. **The decentralised case is the one with a real hazard** — two teams modelling "customer" differently, discovered only at integration.

## ✏️ Exercises

**1. (The process.)** (a) Why must conceptual design precede DBMS selection? (b) Why does physical design come last? (c) What are C&M's four logical-validation steps? (d) Which is skipped, and what does it catch?

> [!example]- Solution
> **(a) Because a model that assumes a product cannot be used to evaluate products.**
>
> The conceptual model states *what the business means* — entities, relationships, rules. **If it is expressed in one DBMS's features, you have already chosen**, and the selection step becomes a formality.
>
> **Two further reasons.** It must be **discussable with non-technical stakeholders**, who are the only source of business rules ([[01 - Databases and Data Models|ch. 01]] §7) and who cannot review a model expressed in vendor syntax. **And it outlives the product** — databases are migrated, and a DBMS-independent conceptual model survives migration while a product-specific one must be re-derived.
>
> **(b) Because it optimises a model that must first be correct, and because it changes nothing semantic.**
>
> *(Verified in §6: adding an index changed the plan from `SCAN` to `SEARCH … USING INDEX` and left the answer identical.)*
>
> **Optimising a wrong model wastes the work twice** — once doing it, once redoing it after the model changes. **And since physical design does not alter meaning, nothing is lost by deferring it**: a correct logical model can always be tuned later without rewriting a single query. **The reverse is not true** — physical decisions made early (denormalising "for speed", choosing types to save bytes) constrain the logical model and are expensive to undo.
>
> **The asymmetry is the argument.** Late physical design costs nothing; early physical design costs correctness.
>
> **(c)** **1.** Map the conceptual model to tables. **2.** Validate by normalising ([[04 - Normalization|ch. 04]]). **3.** Validate the integrity constraints (§3's audit). **4.** Validate against user requirements.
>
> **Step 2 is a check on step 1**: if normalisation forces a decomposition, the ER model had missed an entity. **The two are not independent activities** — normalisation is how you find the entities you overlooked.
>
> **(d) Step 4 — validating against user requirements — and it catches a schema that is technically perfect and practically useless.**
>
> **A schema can be fully normalised, fully constrained, and unable to answer the question the business asked.** [[03 - Entity-Relationship Modelling|Ch. 03]] §7's fan trap is exactly this: `DIVISION` 1:M `TEAM` and `DIVISION` 1:M `PLAYER` — every relationship correct, every table in 3NF, and *"how many players are on each team"* not merely hard but **unanswerable**, because the fact was never modelled.
>
> **Steps 1–3 cannot catch it.** Normalisation checks for redundancy, not for missing relationships. Constraint validation checks that stated rules hold, not that the model captures everything needed. **Only writing the actual queries reveals a relationship that was never recorded.**
>
> **The test is cheap and almost always skipped:** populate the tables with a handful of rows and write the queries the users described. **If a query cannot be written, or returns an inflated count, the model is wrong** — and finding that out on ten rows is much better than on ten million.

**2. (Hard — the audit.)** (a) What did the audit establish and why does testing beat reading? (b) Name the three classes of unenforceable constraint. (c) Why is R8's chicken-and-egg problem awkward? (d) What is a design document actually for?

> [!example]- Solution
> **(a) That 6 of 10 stated business rules are enforced by the schema and 3 are not.**
>
> **Testing beats reading because a constraint's presence in the DDL is not evidence that it binds.** This subject has now found four separate cases where it does not: **foreign keys off by default** ([[01 - Databases and Data Models|ch. 01]]), **`PRIMARY KEY` accepting nulls** ([[02 - The Relational Model and Relational Algebra|ch. 02]]), **an alias accepted in `WHERE`**, and **a bare column accepted beside an aggregate** ([[05 - SQL Fundamentals|ch. 05]]).
>
> **In this chapter the gap is different in kind** — the schema is not misbehaving. **R8, R9 and R10 are simply not expressible as column constraints**, so the DDL never claimed them. **Reading it would tell you nothing was there; you would still not know a rule had gone missing** unless you had the rule list beside you.
>
> **That is why the audit is done against the *rules*, not against the schema.** Start from what the business said, and check each statement individually. **A rule you cannot test is a rule you are not enforcing.**
>
> **(b)**
>
> | class | example | why `CHECK` fails |
> |---|---|---|
> | **minimum cardinality on the "one" side** | R8: a department must have a course | the constraint is on `DEPT` but violated by what is **absent** from `COURSE` |
> | **aggregate constraints** | R9: at most 5 enrolments per semester | depends on a `COUNT` over **other rows**; `CHECK` sees one row |
> | **transition constraints** | R10: credits may not change once enrolled | restricts **old → new**; `CHECK` sees only new |
>
> *(All three verified as unenforced: two departments with no courses; a student with 6 enrolments; credits changed 3 → 6 with 4 students enrolled.)*
>
> **The unifying reason: `CHECK` is a predicate over a single row's new values.** Anything requiring another table, other rows, or the previous state is outside its reach. **All three need a trigger, a deferred constraint, or application logic.**
>
> **Recognising the class matters because it tells you the remedy.** Aggregate constraints are usually enforced by a trigger on the child table; transition constraints by an `UPDATE` trigger comparing `OLD` and `NEW`; minimum cardinality by deferred checking at commit — or, commonly and legitimately, by accepting the risk.
>
> **(c) Because the two rows must be created together, and neither can come first.**
>
> R8 says a department must have at least one course; R7 says a course must have a department. **So you cannot insert the department (it would momentarily have no courses) nor the course (it would reference a non-existent department).**
>
> **The resolution is deferred constraint checking**: the rule is evaluated at `COMMIT` rather than at each statement, so both rows can be inserted inside one transaction and the intermediate state is never observed. **PostgreSQL supports `DEFERRABLE INITIALLY DEFERRED`; SQLite does not for `CHECK`-style rules.**
>
> **This is why minimum-cardinality rules are so often left unenforced in practice** — the enforcement mechanism is more complex than the rule, and the cost of a rare empty department is low. **That is a legitimate decision. What is not legitimate is making it by accident**, which is the default when nobody audits.
>
> **(d) To record which guarantees are enforced where — not to describe the tables.**
>
> **The DDL describes the tables better than any document can**, and it cannot go stale. **What the DDL cannot tell you is what is missing**: which of the business's rules are enforced by a constraint, which by a trigger, which by application code, and **which by nothing at all**.
>
> **A useful design document is essentially §3's scorecard**: every business rule, and against each one the mechanism that enforces it or an explicit note that none does.
>
> **Why it matters practically:**
> - **A rule enforced only in application code holds only for the paths that remember it.** A bulk load, a migration script or a second application bypasses it.
> - **An unenforced rule that nobody recorded becomes an assumption** — analysts will write queries assuming at most 5 enrolments per semester, and be wrong.
> - **When the data turns out inconsistent, the document says whether it was a bug or a known gap.**
>
> **The connecting theme of this whole subject:** [[03 - Entity-Relationship Modelling|ch. 03]] — a diagram promises more than a schema delivers; [[05 - SQL Fundamentals|ch. 05]] — an engine may deliver less than its DDL claims; **here — a requirements list promises more than any schema can deliver.** **The remedy is always the same: try to violate the constraint and see what happens.**

**3. (Levels and strategies.)** (a) Distinguish the three design levels. (b) What did §6 demonstrate? (c) Top-down vs bottom-up? (d) What is the hazard in decentralised design?

> [!example]- Solution
> **(a)** **Conceptual** — what the business means; an ER model plus business rules; **DBMS-independent.** **Logical** — how that becomes tables; a normalised schema with keys and constraints; somewhat DBMS-dependent (data types, available constraint kinds). **Physical** — how it is stored and accessed; indexes, storage organisation, partitioning; **entirely DBMS-dependent.**
>
> **These are [[01 - Databases and Data Models|ch. 01]] §9's abstraction levels used as a *sequence* rather than as a description**, and the ordering carries the discipline: **each level should be fully settled before the next constrains it.**
>
> **(b) That physical design changes cost and not meaning.**
>
> *(Verified: adding an index to 300 000 rows changed the plan from `SCAN big_enrol` to `SEARCH big_enrol USING INDEX idx_enrol_stu (stu_id=?)`, with the identical answer `(11, 5.509)`.)*
>
> **Nothing else changed** — same tables, same data, same query text, same result. **This is the justification for deferring physical design**: it can be added later without touching anything, and it can be changed later without breaking anything. **[[01 - Databases and Data Models|Ch. 01]] §2's data independence, in practice.**
>
> **I have deliberately not quoted a speed-up factor.** The unindexed query took 0.0081 s and the indexed one fell below the timer's resolution, so any ratio would be an artefact of the clock rather than a measurement. **The plan change is the reliable evidence**, and [[09 - Query Optimization and Indexing|ch. 09]] measures the effect properly on data large enough for the timing to mean something.
>
> **(c)** **Top-down** identifies entities first, then their attributes — natural when designing from stated requirements, because that is the order people describe a business in. **Bottom-up** identifies attributes first and groups them into entities — natural when working from existing files, reports or spreadsheets, where the attributes are what you actually have.
>
> **In practice both are used at once.** Top-down for the overall structure, bottom-up whenever there is an existing system, and the two are reconciled where they meet. **Bottom-up is also what [[04 - Normalization|ch. 04]] formalises**: given a wide table of attributes, normalisation *derives* the entities — which is why a normalisation pass so often uncovers an entity the ER model missed.
>
> **(d) That two teams model the same real-world thing differently, and it is discovered only at integration.**
>
> Decentralised design splits a large system into subsystems modelled separately. **The classic failure is that "customer" means different things in two of them** — different keys, different attributes, different granularity (one row per person vs one per account) — and the conflict surfaces at the integration step, when both models are already built.
>
> **The specific conflicts to expect: synonyms** (`CLIENT` and `CUSTOMER` are the same entity), **homonyms** (two different `ACCOUNT`s), **different keys for the same entity**, and **different granularity**.
>
> **The mitigation is a shared vocabulary agreed before modelling starts** — a data dictionary of entity names and definitions — plus integration checkpoints rather than one integration at the end. **The cost of getting it wrong is high**, because reconciling two live schemas means migrating data, not just editing a diagram.

## 📝 Summary

- **The DBLC nests inside the SDLC**: initial study → **design** → implementation and loading → testing → operation → **maintenance and evolution**, which is where most real time goes.
- **The ordering is the insight, not the phases.** Conceptual design precedes DBMS selection (a model assuming a product cannot evaluate products); physical design comes last (it optimises a model that must first be correct).
- **Three levels: conceptual (what the business means, DBMS-independent) → logical (tables, normalised) → physical (indexes, storage).**
- **⚠️ An audit of 10 business rules found the schema enforces 6.** *(All verified by attempting violations.)* R1, R2, R4, R5, R6, R7 enforced; **R8, R9, R10 not**; R3 structural.
- **Three classes of constraint `CHECK` cannot express**, each verified as unenforced:
  - **minimum cardinality on the "one" side** — the constraint is on one table, violated by absence from another *(two departments with no courses)*;
  - **aggregate constraints** — depend on a `COUNT` over other rows *(a student with 6 enrolments against a limit of 5)*;
  - **transition constraints** — restrict old → new, and `CHECK` sees only new *(credits changed 3 → 6 with students enrolled)*.
- **All three need a trigger, deferred checking, or application logic — or they hold nowhere**, and *nowhere is the default* if no one writes the rule down.
- **R8's chicken-and-egg problem** (department needs a course, course needs a department) **requires deferred constraint checking**, which SQLite lacks — a legitimate reason such rules go unenforced, provided the decision is made deliberately.
- **C&M's four logical-validation steps**: map to tables → validate by normalising → validate constraints → **validate against user requirements**.
- **The fourth is the one that gets skipped**, and it catches a schema that is fully normalised and still cannot answer the question asked — [[03 - Entity-Relationship Modelling|ch. 03]]'s fan trap exactly. **Write the users' queries against sample data before building.**
- **Physical design changes cost, not meaning** *(verified: an index changed the plan from `SCAN` to `SEARCH … USING INDEX` with an identical answer)*. This is why it can safely come last.
- **Strategies: top-down** (entities first, from requirements) **vs bottom-up** (attributes first, from existing data — what normalisation formalises); **centralised vs decentralised**, where integration is the hazard.
- **The connecting theme:** a diagram promises more than a schema delivers ([[03 - Entity-Relationship Modelling|ch. 03]]); an engine may deliver less than its DDL claims ([[05 - SQL Fundamentals|ch. 05]]); **a requirements list promises more than any schema can deliver.** **Always test a constraint by trying to violate it.**

## ⚠️ Important Notes

1. **Do the conceptual model before choosing a DBMS.** A model expressed in vendor features has already made the choice.
2. **Do not make physical decisions during logical design.** "It'll be a `VARCHAR(50)` with an index" is a decision made too early.
3. **⚠️ Audit every business rule by trying to violate it.** A constraint in the DDL is not evidence it binds, and a rule *missing* from the DDL is invisible unless you have the rule list beside you.
4. **Keep the business rules as an explicit written list.** They are the only thing you can audit the schema against.
5. **Know the three unenforceable classes** — minimum cardinality on the "one" side, aggregate constraints, transition constraints — so that when a rule falls into one you reach for a trigger rather than assuming a `CHECK` covers it.
6. **A rule enforced only in application code holds only for the paths that remember it.** Bulk loads, migrations and second applications bypass it.
7. **Record where each rule is enforced** — constraint, trigger, application, or nowhere. **"Nowhere" is an acceptable answer; an unrecorded "nowhere" is not.**
8. **Mutually-mandatory relationships need deferred constraint checking.** Without it the rule cannot be enforced at all, since no valid insertion order exists.
9. **Validate against user requirements by writing the actual queries** on sample data. Normalisation and constraint checks cannot detect a relationship you never modelled.
10. **Expect normalisation to reveal missing entities.** If it forces a decomposition, the ER model was incomplete — that is the check working, not a nuisance.
11. **Physical design cannot fix a wrong logical model**, and a correct one can always be tuned later. Optimise last.
12. **Use `EXPLAIN QUERY PLAN` rather than a stopwatch** when the timing is near the clock's resolution. The plan is evidence; a ratio computed from noise is not.
13. **In decentralised design, agree entity names and definitions before modelling.** Synonyms, homonyms, mismatched keys and mismatched granularity all surface at integration, when both schemas already exist.
14. **Plan for maintenance from the start.** Normalisation and views are what make later schema change survivable.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 9 extracts cleanly** — the SDLC and DBLC phases, the conceptual/logical/physical progression, the DBMS-selection discussion, the four logical-validation steps, and the design strategies all came through readably. **Book page $n$ = PDF page $n+28$; ch. 9 is PDF pages 459–500.**
>
> **All figures are images and are lost.** Here the loss is **moderate**: the chapter's figures are mostly process diagrams (the SDLC/DBLC phase charts, the design-flow diagram), which prose conveys adequately — unlike [[03 - Entity-Relationship Modelling|ch. 03]], where the diagrams carried irreplaceable content. **The one real loss is the worked Tiny College conceptual-design walkthrough**, which is largely figures.
>
> **This is the least verifiable chapter in the subject, and the note says so.** C&M ch. 9 is methodology — phases, deliverables, checklists — and **most of it cannot be tested by running anything.** Rather than pad the note with invented demonstrations, §§1–2, 5 and 7 are deliberately compact summaries, and the effort went into §3, which *is* testable.
>
> **The entire worked design is my own** — the ten business rules, the schema, and the audit. C&M's design examples run against sample databases not present in `documents/`.
>
> **No error was found in Coronel & Morris ch. 9.**
>
> **Additions beyond the source.** **§3–§4, the constraint audit, is entirely mine and is this chapter's reason for existing.** C&M lists "validate the logical model integrity constraints" as a step and **does not say how, nor what the outcome typically is.** Stating ten rules, testing each by attempting a violation, and reporting **6 of 10 enforced** turns a checklist item into a result — and produces the three-class taxonomy (**minimum cardinality on the "one" side, aggregate constraints, transition constraints**) that names *why* each failure happens and therefore what to do about it. **I have not seen that taxonomy set out this way in an introductory text**, and it is the most reusable thing here.
>
> **The observation that R8 is unenforceable without deferred checking** — because no valid insertion order exists for mutually-mandatory relationships — is mine, extending [[03 - Entity-Relationship Modelling|ch. 03]] §2.2's finding. **§6's physical-design demonstration is mine**, as is the decision **not** to quote a speed-up ratio, since the indexed time fell below timer resolution and the query plan is the honest evidence. **The framing of a design document as "a record of which guarantees hold where"** rather than a description of tables (Exercise 2(d)) is my own, and **the three-way connecting theme** — diagram > schema, DDL > engine, requirements > any schema — is drawn from findings across [[01 - Databases and Data Models|ch. 01]], [[03 - Entity-Relationship Modelling|ch. 03]] and [[05 - SQL Fundamentals|ch. 05]].
>
> **Deliberately compressed.** **The SDLC phases (§9-2) are given as one table** — they are general systems-analysis material, not database-specific, and are covered properly in any software-engineering course. **The DBLC phase descriptions (§9-3a–f) are summarised rather than reproduced**; the deliverable lists are checklist material. **§9-5 DBMS software selection** is reduced to the ordering argument in §1, since the specific selection criteria (cost, licensing, vendor support) date quickly and are not data-science content. **§9-4d distributed database design** is excluded with C&M ch. 12 by the scope decision in `00-Index.md`. **§9-7's physical-design specifics** (storage organisation, RAID, file placement) are omitted as hardware-dependent and largely obsolete for cloud-hosted databases; **the part that matters — indexing — is [[09 - Query Optimization and Indexing|ch. 09]]**, where the [[Data Structures and Algorithms/contents/10 - Search Trees|B-tree]] machinery makes it explicable. **§9-4c's data-model verification** is folded into §5.

**Previous:** [[06 - Advanced SQL]] · **Next:** [[08 - Transactions and Concurrency Control]]
