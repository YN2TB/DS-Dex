---
subject: Database Management Systems
chapter: 5
tags: [ds, dbms, sql, null, three-valued-logic, group-by, having, aggregates, ddl, dml, constraints]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 7"
---

# SQL Fundamentals

[[02 - The Relational Model and Relational Algebra|Chapter 02]] showed that SQL is the eight relational operators wearing keywords. This chapter is the keywords — but **the syntax is the least interesting part**, and it is not what this note spends its length on.

**What actually causes wrong answers in SQL is `NULL`.** Not joins, not syntax: `NULL`, because it makes SQL's logic **three-valued** rather than Boolean, and almost every intuition carried over from Python or mathematics is wrong there. §3 shows a correct-looking query that **cannot return a row, whatever the data.**

So this chapter is organised around the things that fail silently:

- **§2–4** — three-valued logic, the `NOT IN` trap, and how aggregates treat nulls.
- **§5–6** — the clause evaluation order, which explains `WHERE` versus `HAVING` rather than requiring it to be memorised.
- **§7** — a construct SQLite accepts and PostgreSQL rejects, which produces meaningless output rather than an error.

## 📘 Main Knowledge

### 1. DDL — the constraints are the point

```sql
CREATE TABLE emp (
    emp_id    INTEGER PRIMARY KEY NOT NULL,
    emp_name  TEXT    NOT NULL,
    dept_id   INTEGER REFERENCES dept(dept_id),
    salary    REAL    CHECK (salary > 0),
    bonus     REAL,                                 -- deliberately nullable
    hired     TEXT    NOT NULL DEFAULT '2020-01-01',
    grade     TEXT    CHECK (grade IN ('A','B','C'))
);
```

*(Every constraint verified as actually enforcing:)*

| attempted | result |
|---|---|
| `salary = -100` | **rejected** — `CHECK constraint failed: salary > 0` |
| `grade = 'Z'` | **rejected** — `CHECK constraint failed: grade IN ('A','B','C')` |
| duplicate `dept_name` | **rejected** — `UNIQUE constraint failed` |
| `dept_id = 99` (no such dept) | **rejected** — `FOREIGN KEY constraint failed` |
| omitting `hired` | **`DEFAULT` supplied `2020-01-01`** |

**`CHECK` is the underused one.** It encodes a business rule in the schema where it cannot be bypassed — a grade outside `A/B/C` is not merely discouraged, it is unstorable. **This is [[01 - Databases and Data Models|ch. 01]]'s principle: constraints convert corruption into errors.**

### 2. `NULL` is not a value — it is *unknown*

> [!note] The single most important fact about SQL
> **`NULL` means "unknown", not "empty" or "zero".** Every comparison involving it returns **unknown**, not true or false.

*(Verified:)*
```
NULL = NULL   ->  None        NULL <> NULL  ->  None
NULL = 1      ->  None        NULL IS NULL  ->  1  (true)
```

**Even `NULL = NULL` is unknown** — two unknown values might or might not be equal. **This is why `IS NULL` exists**: it is a test of *nullity*, not a comparison.

**So SQL's logic has three values, and the truth tables are not Boolean:**

| expression | result |
|---|---|
| `true AND unknown` | **unknown** |
| `false AND unknown` | **false** |
| `true OR unknown` | **true** |
| `false OR unknown` | **unknown** |
| `NOT unknown` | **unknown** |

*(All verified.)* **The pattern: when the other operand already settles the answer, the unknown does not matter** — `false AND anything` is false. Otherwise the result is unknown.

#### 2.1 The consequence: a condition and its negation do not partition the table

```
WHERE bonus > 1000   ->  3 rows
WHERE bonus <= 1000  ->  0 rows
total rows           ->  6
```
*(Verified: 3 + 0 = 3, not 6.)*

> [!warning] The three rows with a null bonus are in **neither** result
> **`WHERE` keeps rows where the condition is TRUE.** Unknown is discarded just like false — so a row with `bonus IS NULL` fails `bonus > 1000` *and* fails `bonus <= 1000`.
>
> **This is the commonest `NULL` bug in analysis**, and it is silent: you filter a population into two groups, they do not add up, and nothing warns you. **Every null-valued row vanishes from both.**
>
> **The fix is to say what unknown should do, explicitly:**
> ```sql
> WHERE bonus > 1000 OR bonus IS NULL      -- verified: returns all 6 rows
> ```
> **Whenever you filter on a nullable column, decide where the nulls go.**

### 3. The `NOT IN` trap — a query that cannot return a row

**The setup** *(verified)*: four departments (Sales, IT, Research, **Legal**); employees use dept 10, 20, 30 and one has a **null** `dept_id`. **The true answer to "which departments have no employees?" is Legal (40).**

```sql
SELECT dept_id, dept_name FROM dept
WHERE dept_id NOT IN (SELECT dept_id FROM emp);
```
```
(0 rows)
```

**Wrong — and not just wrong, incapable of being right.**

> [!warning] Why it returns nothing, whatever the data
> `NOT IN (10, 20, 30, NULL)` expands to
> ```
> dept_id <> 10 AND dept_id <> 20 AND dept_id <> 30 AND dept_id <> NULL
> ```
> **The last conjunct is *unknown* for every row.** By §2's truth table, `true AND unknown` is unknown — so the chain can be **false** (if some other conjunct fails) or **unknown**, but **never true.**
>
> **A single `NULL` anywhere in the `NOT IN` list makes the query return the empty set, permanently.** It does not lose *some* rows — it loses *all* of them.
>
> **`IN` is not affected.** A null in the list can never turn a genuine match into a non-match, so only `NOT IN` is poisoned. That asymmetry is what makes the bug so easy to miss.

**Three fixes, all verified to return Legal (40):**

```sql
-- 1. exclude nulls from the subquery
WHERE dept_id NOT IN (SELECT dept_id FROM emp WHERE dept_id IS NOT NULL)

-- 2. NOT EXISTS -- null-safe by construction     <- PREFERRED
WHERE NOT EXISTS (SELECT 1 FROM emp e WHERE e.dept_id = d.dept_id)

-- 3. the anti-join
FROM dept d LEFT JOIN emp e USING (dept_id) WHERE e.emp_id IS NULL
```

**Prefer `NOT EXISTS`.** Fix 1 works but relies on you remembering the danger every time; **`NOT EXISTS` is correct whether or not nulls are present**, because it asks about the *existence of a matching row* rather than comparing against a list of values.

### 4. Aggregates ignore nulls — except `COUNT(*)`

*(Verified on 6 rows, 3 with a null bonus:)*

| | |
|---|---|
| `COUNT(*)` | **6** |
| `COUNT(bonus)` | **3** |
| `SUM(bonus)` | 16 000 |
| **`AVG(bonus)`** | **5 333.33** |
| `SUM(bonus)/COUNT(*)` | **2 666.67** |

> [!warning] `AVG` divides by the count of non-nulls, not by the number of rows
> **These are two different questions and the difference is a factor of two here:**
> - **5 333.33** — the average bonus *among employees who received one*.
> - **2 666.67** — the average bonus *per employee*, counting no-bonus as zero.
>
> **`AVG(bonus)` silently answers the first.** If you meant the second, you must say so:
> ```sql
> AVG(COALESCE(bonus, 0))     -- verified: 2666.67
> ```
> **`COALESCE` makes the decision explicit; silence makes it implicitly the first one.** Neither is wrong — reporting the wrong one is.
>
> **`COUNT(*)` versus `COUNT(col)` is the same trap** *(verified: 6 rows, but `COUNT(dept_id)` = 5)*. **`COUNT(*)` counts rows; `COUNT(col)` counts non-null values.**

### 5. Clause evaluation order

**The written order is not the evaluation order**, and knowing the real one removes the need to memorise most SQL rules:

```
written:    SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT
evaluated:  FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

**This is testable.** An aggregate cannot appear in `WHERE`, because `WHERE` runs before grouping and no aggregate exists yet:

```
SELECT dept_id FROM emp WHERE COUNT(*) > 1 GROUP BY dept_id
-> ERROR: misuse of aggregate: COUNT()
```
*(Verified.)* **`HAVING` exists precisely to provide a filter that runs *after* grouping.**

**Aliases follow the same logic**: an alias is created in `SELECT`, so `ORDER BY` (later) can use it *(verified)*.

> [!warning] SQLite accepts an alias in `WHERE`; PostgreSQL does not
> ```
> SELECT salary*12 AS annual FROM emp WHERE annual > 500000
> -> SQLite ACCEPTED it (5 rows)
> ```
> *(Verified.)* **This is a SQLite extension.** PostgreSQL and SQL Server reject it — `column "annual" does not exist` — **exactly because `WHERE` is evaluated before `SELECT`.**
>
> **So a query that works in SQLite can fail in production.** Repeat the expression in `WHERE`, or wrap the query in a subquery, if it must be portable. *(This is the third SQLite permissiveness in this subject, after [[01 - Databases and Data Models|ch. 01]]'s foreign keys and [[02 - The Relational Model and Relational Algebra|ch. 02]]'s null primary keys.)*

### 6. `WHERE` versus `HAVING`

**`WHERE` filters rows before grouping; `HAVING` filters groups after aggregating.** They answer different questions and give different answers:

*(All verified on the same table:)*

| | Sales (10) | IT (20) |
|---|---|---|
| **no filter** | n=2, avg 46 000 | n=2, avg 50 000 |
| **`WHERE salary > 45000`** | **n=1**, avg 50 000 | **n=1**, avg 61 000 |
| **`HAVING AVG(salary) > 45000`** | n=2, avg 46 000 | n=2, avg 50 000 |

**`WHERE` changed the group contents; `HAVING` changed which groups appear.** *(Here `HAVING` dropped none, since every department's average exceeds 45 000 — which is itself the point: `WHERE` removed low-paid individuals, `HAVING` would remove low-paying departments.)*

> [!note] Use each for its own job
> **Put row conditions in `WHERE` and aggregate conditions in `HAVING`.** A row condition in `HAVING` gives the same answer but is slower — the rows are grouped first and discarded afterwards, so the grouping work is wasted.

**And a null-handling inconsistency worth noting** *(verified)*: `GROUP BY dept_id` put the null-department employee in **its own group**.

> [!warning] `GROUP BY` treats nulls as equal; `=` does not
> **Two nulls group together, but `NULL = NULL` is unknown.** SQL is deliberately inconsistent here — `GROUP BY`, `DISTINCT` ([[02 - The Relational Model and Relational Algebra|ch. 02]] §4.2), `ORDER BY` and the set operators all treat nulls as equal to one another, while comparison operators do not.
>
> **The practical consequence: a `GROUP BY` result can contain a null group you did not expect**, and it is easy to mistake for a data error when it is the "unknown" category.

### 7. The bare-column trap

```sql
SELECT dept_id, emp_name, SUM(salary) FROM emp GROUP BY dept_id;
```

**SQLite accepts this. PostgreSQL and SQL Server reject it** with *"column must appear in the GROUP BY clause or be used in an aggregate function"*.

*(Verified — SQLite returned:)*
```
dept_id | emp_name | SUM(salary)
--------+----------+------------
10      | Nguyen A | 92000.0
20      | Le C     | 100000.0
```

> [!warning] `emp_name` here is meaningless
> **The group has two employees and one `emp_name` column, so SQLite picks one arbitrarily.** `Nguyen A` is not "the" employee of department 10 in any sense — the value is undefined and could change between releases or query plans.
>
> *(With `MAX`/`MIN` specifically, SQLite documents that bare columns come from the row that produced the extreme value — genuinely useful, and genuinely non-portable. **With `SUM`, `AVG` or `COUNT` there is no such guarantee.**)*
>
> **Never select a bare column alongside an aggregate.** Either group by it, aggregate it, or use a window function ([[06 - Advanced SQL|ch. 06]]). The query is portable nonsense: it runs in SQLite and MySQL, fails in PostgreSQL, and its output means nothing in either case.

### 8. DML — and the habit that prevents disasters

```sql
BEGIN;
UPDATE emp SET salary = salary * 1.10 WHERE dept_id = 20;   -- 2 rows changed
-- inspect...
ROLLBACK;                                                   -- verified: undone
```

*(Verified: the salaries rose, then `ROLLBACK` restored them exactly.)*

> [!warning] `UPDATE` and `DELETE` without a `WHERE` affect every row
> **There is no confirmation prompt.** `DELETE FROM emp` deletes all six rows and reports success.
>
> **Two habits that prevent it:**
> 1. **Write the `SELECT` first.** `SELECT * FROM emp WHERE …`, check the rows are the ones you mean, *then* replace `SELECT *` with `DELETE` or `UPDATE … SET …`.
> 2. **Wrap it in a transaction and check `rowcount` before committing** ([[08 - Transactions and Concurrency Control|ch. 08]]). If the count is not what you expected, `ROLLBACK`.

### 9. Operators worth knowing exactly

| | behaviour |
|---|---|
| **`BETWEEN a AND b`** | **inclusive at both ends** *(verified)* — equivalent to `>= a AND <= b` |
| `IN (…)` | set membership; safe with nulls, unlike `NOT IN` (§3) |
| **`LIKE`** | `%` = any string, `_` = any single character |
| `CASE WHEN … THEN … ELSE … END` | conditional logic inside a query |
| `COALESCE(a, b)` | first non-null argument — the explicit null decision of §4 |

> [!warning] `LIKE` case-sensitivity is engine-dependent
> *(Verified: SQLite's `LIKE` matched `'N%'` against `Nguyen A` **and** is case-insensitive for ASCII by default.)* **PostgreSQL's `LIKE` is case-sensitive** and offers `ILIKE` for the insensitive version; MySQL depends on the column's collation.
>
> **Never assume. Test on your engine** — a search that works in development can silently miss rows in production.

**Date handling is also engine-specific.** SQLite has no date type at all — dates are text, and arithmetic goes through `julianday()` *(verified: years of service computed from `hired`)*. PostgreSQL has real `date`/`interval` types.

## ✏️ Exercises

**1. (Null semantics.)** (a) What does `NULL` mean and why is `NULL = NULL` unknown? (b) Give the three-valued truth tables and the pattern behind them. (c) Why did 3 + 0 ≠ 6? (d) What is the general rule?

> [!example]- Solution
> **(a) `NULL` means *unknown*, not empty, zero or blank.**
>
> **`NULL = NULL` is unknown because two unknown quantities might or might not be equal.** If one row's bonus is unknown and another's is unknown, are they the same? **You cannot know** — that is what unknown means. Returning `true` would assert they are equal; returning `false` would assert they differ; both claim knowledge you do not have.
>
> **Hence `IS NULL`**, which is not a comparison but a test of whether the value is absent — a question that always has a definite answer.
>
> *(Verified: `NULL = NULL`, `NULL <> NULL` and `NULL = 1` all return `None`; `NULL IS NULL` returns 1.)*
>
> **(b)**
>
> | | AND | OR |
> |---|---|---|
> | **true, unknown** | **unknown** | **true** |
> | **false, unknown** | **false** | **unknown** |
>
> and `NOT unknown` = **unknown**. *(All verified.)*
>
> **The pattern: if the known operand already determines the answer, the unknown is irrelevant.** `false AND x` is false for every possible `x`, so it is false even when `x` is unknown. `true OR x` is true regardless, so it is true. **Otherwise the result depends on the unknown value and is therefore itself unknown.**
>
> **This is not arbitrary — it is what you get by treating unknown as "some value I cannot see" and asking whether the answer is the same for every possible substitution.** Knowing that derivation means you never have to memorise the tables.
>
> **(c) Because `WHERE` keeps rows where the condition is TRUE, and unknown is discarded exactly like false.**
>
> The three rows with `bonus IS NULL` evaluate `bonus > 1000` to unknown → dropped, and `bonus <= 1000` to unknown → dropped. **They appear in neither result.** *(Verified: 3 rows and 0 rows out of 6.)*
>
> **This breaks an intuition carried from everywhere else: `P` and `NOT P` do not partition a set.** In ordinary logic every element satisfies one or the other; in SQL, rows with nulls satisfy neither.
>
> **The danger is that it is silent and plausible.** Splitting customers into `spend > 100` and `spend <= 100` gives two groups that look complete, and every customer with unknown spend has vanished from the analysis. **Nothing errors, and the totals are simply wrong.**
>
> **(d) Whenever you filter on a nullable column, decide explicitly where the nulls go.**
>
> ```sql
> WHERE bonus > 1000 OR bonus IS NULL     -- verified: 6 rows
> ```
>
> **Practically:**
> 1. **Know which columns are nullable** — read the DDL, do not guess from the data.
> 2. **Add `OR col IS NULL` when nulls belong in the group**, or `AND col IS NOT NULL` to exclude them deliberately and visibly.
> 3. **Check that your partitions sum to the total.** If the parts do not add to `COUNT(*)`, nulls are the usual reason.
> 4. **Prefer `COALESCE` at the point of use** when there is a sensible default — but only when the default is genuinely right (§4).

**2. (Hard — the `NOT IN` trap.)** (a) Why does it return nothing? (b) Why is it worse than an ordinary bug? (c) Why is `IN` unaffected? (d) Compare the three fixes.

> [!example]- Solution
> **(a) Because one unknown conjunct poisons the whole chain.**
>
> `NOT IN (10, 20, 30, NULL)` is defined as
> ```
> dept_id <> 10 AND dept_id <> 20 AND dept_id <> 30 AND dept_id <> NULL
> ```
> **The final conjunct is unknown for every row** — comparing anything to `NULL` yields unknown.
>
> By §2's table, `true AND unknown` = unknown. So for a row that passes the first three tests, the result is **unknown, not true** — and `WHERE` discards it. For a row that fails one, the result is false — also discarded.
>
> **Every row is therefore discarded. The query returns the empty set for any data whatsoever.** *(Verified: 0 rows where the true answer is Legal (40).)*
>
> **(b) Because it fails completely, silently, and only when the data changes.**
>
> **The failure is total, not partial.** A bug returning slightly wrong numbers might be caught by a sanity check; **this returns nothing at all**, which is easy to read as "there are no such departments" — a perfectly plausible business answer.
>
> **The query is syntactically valid and reads correctly.** `WHERE dept_id NOT IN (SELECT dept_id FROM emp)` is exactly how you would say it in English. **Code review will not catch it.**
>
> **And it is data-dependent.** With no nulls in `emp.dept_id` the query is correct. **It starts failing the day one employee is inserted without a department** — long after deployment, with no code change to blame. **This is the worst property a bug can have**, and it is shared with [[03 - Entity-Relationship Modelling|ch. 03]]'s fan trap and [[02 - The Relational Model and Relational Algebra|ch. 02]]'s inner-join row loss: correct-looking SQL, no error, wrong answer.
>
> **(c) Because a null can never turn a real match into a non-match.**
>
> `IN` is a chain of `OR`s: `dept_id = 10 OR dept_id = 20 OR dept_id = NULL`. **If the row genuinely matches 10, the first disjunct is true, and `true OR unknown` is true** (§2) — the row is correctly returned.
>
> **The asymmetry:** `IN` can only fail to *reject* — a non-matching row returns unknown rather than false and is discarded either way, so the result is unchanged. **`NOT IN` fails to *accept*, and the accept case is the whole answer.**
>
> **So `IN` is safe and `NOT IN` is not**, which is exactly why the bug survives: people generalise their experience with `IN`.
>
> **(d)**
>
> | fix | correct? | robust? |
> |---|---|---|
> | `NOT IN (… WHERE col IS NOT NULL)` | ✓ | **relies on you remembering, every time** |
> | **`NOT EXISTS`** | ✓ | **✓ null-safe by construction** |
> | `LEFT JOIN … WHERE key IS NULL` | ✓ | ✓ |
>
> *(All three verified to return Legal (40).)*
>
> **Fix 1 is a patch on a landmine.** It works, but the query remains one forgotten `IS NOT NULL` away from silently returning nothing, and the next person to edit it will not know why the clause is there.
>
> **Fix 2, `NOT EXISTS`, is the right default.** It never compares values against a list — it asks *"does a matching row exist?"*, which is a definite question even when values are unknown. **The correlated `e.dept_id = d.dept_id` is false-or-unknown for null rows, so no match exists, which is the right conclusion.** It is correct whether or not nulls are present, so it cannot rot when the data changes.
>
> **Fix 3, the anti-join, is equally correct** and sometimes faster on large tables, since the optimiser can use a hash or merge join ([[09 - Query Optimization and Indexing|ch. 09]]). **It reads less clearly** — `WHERE e.emp_id IS NULL` after a `LEFT JOIN` is idiomatic but opaque to newcomers, and you must test a `NOT NULL` column of the right table or it breaks.
>
> **Rule: use `NOT EXISTS` for "not related to any"; reserve `NOT IN` for literal lists you wrote yourself.**

**3. (Aggregates and evaluation order.)** (a) Explain 5 333.33 versus 2 666.67. (b) `COUNT(*)` versus `COUNT(col)`? (c) State the evaluation order and how it was verified. (d) When `WHERE`, when `HAVING`?

> [!example]- Solution
> **(a) `AVG` ignores nulls, so it divides by the number of non-null values, not the number of rows.**
>
> Three employees have bonuses totalling 16 000; three have `NULL`.
> - **`AVG(bonus)` = 16 000 / 3 = 5 333.33** — the average *among those who received a bonus*.
> - **`AVG(COALESCE(bonus,0))` = 16 000 / 6 = 2 666.67** — the average *per employee*.
>
> *(Both verified.)*
>
> **Neither is wrong; they answer different questions, and `AVG(bonus)` answers the first without saying so.** The gap is a factor of two here and can be far larger.
>
> **Which is right depends on what `NULL` means in that column** — and this is where §2's "unknown" matters:
> - **If null means "received no bonus"**, the second is right, and `COALESCE(bonus,0)` is correct because zero is the true value.
> - **If null means "we don't know their bonus"**, the first is right and the second is *fabrication* — you would be asserting a bonus of zero for people whose bonus you have not recorded.
>
> **So you must know why the nulls are there.** `COALESCE` makes the decision explicit and reviewable; silence hides it.
>
> **(b) `COUNT(*)` counts rows; `COUNT(col)` counts non-null values of `col`.** *(Verified: 6 rows, `COUNT(dept_id)` = 5.)*
>
> **`COUNT(*)` is the only aggregate that does not ignore nulls**, because it never looks at a column.
>
> **This makes `COUNT(col)` genuinely useful** — `COUNT(dept_id)` is "how many employees have a department", so `COUNT(*) - COUNT(dept_id)` counts the missing ones. **But `COUNT(some_column)` written when `COUNT(*)` was meant undercounts silently**, and the shortfall is exactly the null count.
>
> *(A related trap: `COUNT(DISTINCT col)` also ignores nulls, so "how many distinct departments" excludes the unknown one — even though `GROUP BY` would give it a group. §6's inconsistency again.)*
>
> **(c)**
> ```
> FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
> ```
>
> **Verified by a test that fails on every engine:**
> ```
> SELECT dept_id FROM emp WHERE COUNT(*) > 1 GROUP BY dept_id
> -> ERROR: misuse of aggregate: COUNT()
> ```
> **`WHERE` runs before `GROUP BY`, so at that moment no groups and no aggregates exist.** The error is not a restriction someone chose; it is a consequence of the order.
>
> **The alias behaviour is the same logic** — aliases are created in `SELECT`, so `ORDER BY` (later) can use them *(verified)*.
>
> **But the alias-in-`WHERE` test did not behave portably**: *(verified)* **SQLite accepted `WHERE annual > 500000`, returning 5 rows.** This is a SQLite extension; **PostgreSQL and SQL Server reject it**, precisely because `WHERE` precedes `SELECT`. **So a query developed against SQLite can fail in production** — the fourth such permissiveness this subject has found, after foreign keys, null primary keys and the bare-column rule.
>
> **Knowing the order explains, rather than requires memorising: why aggregates cannot appear in `WHERE`, why `HAVING` exists, why aliases work in `ORDER BY` but not portably in `WHERE`, and why `LIMIT` applies after sorting.**
>
> **(d) `WHERE` for conditions on rows; `HAVING` for conditions on aggregates.**
>
> *(Verified, same table:)*
>
> | | Sales (10) | IT (20) |
> |---|---|---|
> | no filter | n=2, avg 46 000 | n=2, avg 50 000 |
> | `WHERE salary > 45000` | **n=1**, avg 50 000 | **n=1**, avg 61 000 |
> | `HAVING AVG(salary) > 45000` | n=2, avg 46 000 | n=2, avg 50 000 |
>
> **`WHERE` changed what is *in* each group; `HAVING` changed *which groups* appear.** Different questions: *"the average of high salaries per department"* versus *"departments whose average is high"*.
>
> **A row condition put in `HAVING` gives the same answer but is slower** — the rows are grouped and then thrown away, so the grouping work is wasted. **On a large table with a selective condition this is a substantial difference**, because `WHERE` can also use an index ([[09 - Query Optimization and Indexing|ch. 09]]) while `HAVING` cannot.
>
> **The exception: `HAVING` may reference a row condition when it must be applied after grouping** — but that is rare and usually signals a subquery is wanted instead.

**4. (Portability and safety.)** (a) What is the bare-column trap? (b) Why is `emp_name` meaningless there? (c) How do you avoid `UPDATE`/`DELETE` disasters? (d) What has this subject found about trusting SQLite?

> [!example]- Solution
> **(a) Selecting a column that is neither grouped nor aggregated.**
>
> ```sql
> SELECT dept_id, emp_name, SUM(salary) FROM emp GROUP BY dept_id;
> ```
> **SQLite and MySQL accept it; PostgreSQL and SQL Server reject it** — *"column must appear in the GROUP BY clause or be used in an aggregate function"*.
>
> **The rejection is correct.** The group has two employees and one `emp_name` slot, so the query asks an incoherent question.
>
> **(b) Because the group contains several values and the query names no rule for choosing.**
>
> *(Verified: department 10 has two employees; SQLite returned `Nguyen A`.)* **`Nguyen A` is not "the" employee of department 10 in any sense** — the value is arbitrary and may change with the query plan, the row order, or the SQLite version.
>
> **The special case worth knowing:** with `MAX`/`MIN` *only*, SQLite documents that bare columns come from the row producing the extreme value — so `SELECT dept_id, emp_name, MAX(salary) … GROUP BY dept_id` genuinely gives the highest-paid employee's name *(verified)*. **That is useful and completely non-portable.** With `SUM`, `AVG` or `COUNT` there is no guarantee at all.
>
> **The portable equivalents:** a window function (`ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC)`, [[06 - Advanced SQL|ch. 06]]), or a correlated subquery, or a join back to the aggregate.
>
> **What makes this dangerous is that it is *silently* meaningless.** It does not error and does not look odd — it produces a plausible name next to a correct total, and the name is noise.
>
> **(c) Write the `SELECT` first; wrap the change in a transaction.**
>
> **`UPDATE` and `DELETE` without a `WHERE` affect every row, with no confirmation.** `DELETE FROM emp` removes all six rows and reports success.
>
> **The habits:**
> 1. **Write `SELECT * FROM emp WHERE …` first, inspect the rows, then replace `SELECT *` with `DELETE` or `UPDATE … SET …`** — keeping the `WHERE` clause untouched.
> 2. **Wrap it in a transaction and check the row count before committing.** *(Verified: an `UPDATE` raised two salaries and `ROLLBACK` restored them exactly.)* If the count is not what you expected, roll back.
> 3. **Beware autocommit.** Many clients commit each statement immediately, so there is nothing to roll back — you must open the transaction explicitly. *(This is [[08 - Transactions and Concurrency Control|ch. 08]]'s territory.)*
>
> **The row count is the check that matters**, because it is the one number that reveals a `WHERE` clause matching more than intended.
>
> **(d) That its permissiveness is systematic, and the pattern is: SQLite accepts what stricter engines reject, silently.**
>
> **Four findings so far, all verified by testing rather than reading:**
>
> | | SQLite | PostgreSQL |
> |---|---|---|
> | foreign keys ([[01 - Databases and Data Models\|ch. 01]]) | **off by default**, per connection | enforced |
> | `PRIMARY KEY` and null ([[02 - The Relational Model and Relational Algebra\|ch. 02]]) | **accepts nulls**; `INTEGER PRIMARY KEY` **auto-assigns** | rejected |
> | alias in `WHERE` (§5) | **accepted** | rejected |
> | bare column with aggregate (§7) | **accepted**, value arbitrary | rejected |
>
> **In every case SQLite produces a result where a stricter engine produces an error** — and an error is much cheaper than a wrong answer.
>
> **The practical conclusions:**
> - **SQLite is excellent for learning** — zero setup, and every idea in this subject is demonstrable in it. **This vault's run-the-SQL rule depends on that.**
> - **It is a poor oracle for correctness.** Working in SQLite is not evidence a query is right, or portable.
> - **Enable what can be enabled** (`PRAGMA foreign_keys = ON`, `STRICT` tables) and **know the remaining gaps**.
> - **Test against the target engine before deploying.**
>
> **The transferable habit is the one this subject keeps demonstrating: verify behaviour, do not infer it from documentation or DDL.** Every one of the four rows above would have been got wrong by reading the schema and assuming the standard applied.

## 📝 Summary

- **Constraints are the point of DDL** *(all verified as enforcing)*: `CHECK`, `UNIQUE`, `NOT NULL`, `DEFAULT` and foreign keys turn corruption into errors. **`CHECK` is the underused one** — it puts a business rule where it cannot be bypassed.
- **`NULL` means *unknown*.** Every comparison with it yields **unknown** *(verified: even `NULL = NULL` returns `None`)* — hence `IS NULL`.
- **SQL logic is three-valued.** `false AND unknown` = false; `true OR unknown` = true; everything else involving unknown is unknown. **The pattern: if the known operand settles it, the unknown does not matter.**
- **⚠️ A condition and its negation do not partition a table.** *(Verified: `bonus > 1000` gave 3 rows, `bonus <= 1000` gave 0, out of 6 — the three null rows appear in neither.)* **Decide explicitly where nulls go.**
- **⚠️ The `NOT IN` trap: one null in the list makes the query return the empty set for any data.** *(Verified: 0 rows where the answer was Legal.)* `NOT IN (…, NULL)` expands to an `AND` chain containing an unknown, which can never be true.
- **`IN` is unaffected** — a null cannot turn a genuine match into a non-match. **Only `NOT IN` is poisoned**, which is why the bug survives.
- **Prefer `NOT EXISTS`** — null-safe by construction, unlike the `IS NOT NULL` patch, which relies on remembering. The `LEFT JOIN … IS NULL` anti-join also works. *(All three verified.)*
- **Aggregates ignore nulls; `COUNT(*)` does not.** *(Verified: `AVG(bonus)` = **5 333.33** but `AVG(COALESCE(bonus,0))` = **2 666.67** — a factor of two.)* **Which is right depends on whether null means "none" or "unknown".**
- **Evaluation order is `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`**, which explains rather than requires memorising most SQL rules. *(Verified: an aggregate in `WHERE` errors on every engine.)*
- **⚠️ SQLite accepts a `SELECT` alias in `WHERE`; PostgreSQL rejects it** *(verified)* — so a query that works in development can fail in production.
- **`WHERE` filters rows before grouping, `HAVING` filters groups after** *(verified: different answers on the same table)*. A row condition in `HAVING` is slower and cannot use an index.
- **`GROUP BY` treats nulls as equal (one group) while `=` does not** *(verified)* — the same inconsistency as `DISTINCT`.
- **⚠️ Never select a bare column with an aggregate.** *(Verified: SQLite returned an arbitrary `emp_name` beside a `SUM`.)* Portable nonsense — accepted by SQLite and MySQL, rejected by PostgreSQL, meaningless in both.
- **`UPDATE`/`DELETE` without `WHERE` hit every row.** **Write the `SELECT` first; wrap the change in a transaction and check the row count before committing** *(verified: `ROLLBACK` restored the salaries exactly)*.
- **`BETWEEN` is inclusive; `LIKE` case-sensitivity and date handling are engine-specific.** Test, do not assume.

## ⚠️ Important Notes

1. **`NULL` is unknown, not zero or empty.** Never compare with `=`; use `IS NULL` / `IS NOT NULL`.
2. **⚠️ Whenever you filter a nullable column, say where the nulls go.** A condition and its negation leave them in neither group.
3. **Check that your partitions sum to `COUNT(*)`.** If they do not, nulls are almost always why.
4. **⚠️ Never use `NOT IN` with a subquery on a nullable column.** One null makes the result empty, permanently, and the query reads perfectly.
5. **Use `NOT EXISTS` for "not related to any".** Reserve `NOT IN` for literal lists you wrote yourself.
6. **`AVG` divides by the non-null count.** Decide whether null means "none" (use `COALESCE(col,0)`) or "unknown" (leave it out) — and never let the choice be implicit.
7. **`COUNT(*)` counts rows; `COUNT(col)` and `COUNT(DISTINCT col)` skip nulls.** Their difference is the null count, which is sometimes exactly what you want.
8. **Learn the evaluation order.** It explains why aggregates cannot go in `WHERE`, why `HAVING` exists, and why aliases behave as they do.
9. **⚠️ Do not rely on a `SELECT` alias in `WHERE`.** SQLite allows it; PostgreSQL does not. Repeat the expression or use a subquery.
10. **Row conditions in `WHERE`, aggregate conditions in `HAVING`.** `HAVING` cannot use an index and groups rows before discarding them.
11. **Expect a `NULL` group from `GROUP BY`.** It is the "unknown" category, not a data error.
12. **⚠️ Never select a bare column alongside an aggregate.** Use a window function or a subquery instead. SQLite's `MAX`/`MIN` behaviour is real but non-portable.
13. **Always write `UPDATE`/`DELETE` as a `SELECT` first**, then swap the verb, leaving the `WHERE` untouched.
14. **Wrap risky DML in a transaction and check the row count before committing.** Beware autocommit clients, where there is nothing to roll back.
15. **`BETWEEN` is inclusive at both ends** — a frequent off-by-one with dates, where `BETWEEN '2025-01-01' AND '2025-01-31'` excludes anything timestamped later on the 31st.
16. **`LIKE` case-sensitivity, string comparison and date handling are engine-specific.** SQLite has no date type at all. Test on the engine you will deploy to.
17. **SQLite accepts what stricter engines reject — four times so far in this subject.** It is an excellent teaching database and a poor oracle for correctness.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 7 extracts cleanly** — the data types, `SELECT` options, column aliases and computed columns, `WHERE` operators, the join syntaxes, aggregate functions, `GROUP BY` and `HAVING`, and the subquery introduction all came through readably. **Book page $n$ = PDF page $n+28$; ch. 7 is PDF pages 267–378** — at 112 pages the longest chapter in the book.
>
> **All figures are images and are lost.** For this chapter that is **less damaging than elsewhere**, because C&M's figures are mostly screenshots of query results — and every result in this note is real output from a live database instead, which is strictly better. **The lost items that would have helped are the schema diagram of the `Ch07_SaleCo` sample database** used throughout the chapter, and the syntax-summary boxes.
>
> **The entire worked dataset here is my own.** C&M's examples run against downloadable `Ch07_SaleCo` / `Ch07_ConstructCo` databases that are not in `documents/`, so **the `dept`/`emp` schema, its rows, and every query were written for this note** — deliberately including three null bonuses, one null `dept_id`, and an employee-less `Legal` department, because those are what make §§2–4's failures visible.
>
> **No error was found in Coronel & Morris ch. 7.**
>
> **Additions beyond the source — this chapter is substantially reframed.** C&M ch. 7 is organised as a syntax tour: one section per clause, each with examples. **That is reference material, and it is the part of SQL least worth a long note.** This chapter instead centres on the constructs that fail silently, which C&M covers thinly or not at all:
>
> - **§§2–3, three-valued logic and the `NOT IN` trap, are mine.** C&M introduces `IS NULL` as syntax and notes that aggregates ignore nulls, but **does not present the three-valued truth tables, does not show that a condition and its negation fail to partition a table, and does not mention the `NOT IN` trap at all.** The last is arguably the single most damaging SQL bug in practice, and demonstrating a query that *cannot return a row whatever the data* is the strongest form of the point.
> - **§4's `AVG` comparison** (5 333.33 vs 2 666.67, a factor of two) **and the analysis of when each is correct** — turning on whether null means "none" or "unknown" — are additions.
> - **§5's evaluation order is not in C&M at all.** It is the single most useful organising fact about SQL, and it converts several apparently arbitrary rules into consequences.
> - **§7's bare-column trap is mine**, including the finding that SQLite's `MAX`/`MIN` behaviour is a documented special case while `SUM` gives an arbitrary value.
> - **The four-row SQLite-versus-PostgreSQL permissiveness table** in Exercise 4(d), accumulated across [[01 - Databases and Data Models|ch. 01]], [[02 - The Relational Model and Relational Algebra|ch. 02]] and this chapter, is my own running finding and is not something a textbook would report.
> - **§8's `SELECT`-first habit and the transaction/row-count check** are practice, not syntax, and are additions.
>
> **Two corrections to my own work, made before writing.** The `NOT IN` demonstration initially used a department that *did* have an employee, so the "correct" answer was also zero rows and **the trap proved nothing** — fixed by adding the employee-less `Legal` department. And the evaluation-order demonstration originally relied on an alias in `WHERE` being rejected; **SQLite accepted it**, so the demonstration was replaced with an aggregate in `WHERE` (which fails everywhere) and the SQLite deviation was reported as a finding in its own right.
>
> **Deliberately compressed.** **Joins (C&M §7-7, eleven subsections) are not repeated here** — they were covered in [[02 - The Relational Model and Relational Algebra|ch. 02]] §4 with the algebra that explains them, and the outer-join row-loss trap is documented there. **Subqueries (§7-9) are deferred to [[06 - Advanced SQL|ch. 06]]**, where they belong with CTEs and window functions. **The catalogue of string, numeric and date functions (§7-6)** is reference material that dates quickly and differs per engine; §9 covers the operators whose *semantics* surprise people (`BETWEEN`, `LIKE`, `COALESCE`, `CASE`) and omits the rest. **§7-1a's data-type table** is engine-specific and omitted — SQLite's dynamic typing makes it actively misleading as a guide to other systems. **`COMMIT`/`ROLLBACK` are used in §8 but their semantics are deferred to [[08 - Transactions and Concurrency Control|ch. 08]].**

**Previous:** [[04 - Normalization]] · **Next:** [[06 - Advanced SQL]]
