---
subject: Database Management Systems
chapter: 6
tags: [ds, dbms, sql, subqueries, cte, recursive-cte, window-functions, views, ranking, frames]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 8"
---

# Advanced SQL

**This is the chapter that matters most for data science.** [[05 - SQL Fundamentals|Chapter 05]] covered the SQL that every developer knows; this one covers the SQL that turns the database into an analytical tool — **window functions, CTEs and recursive queries** — and that lets you push work down to the engine instead of pulling everything into pandas.

**Coronel & Morris is thin here**, as its subject file anticipated: it covers subqueries thoroughly and views adequately, but window functions get a fraction of the space their usefulness warrants. **This chapter is correspondingly enriched.**

Two results are worth flagging up front:

- **§8: the default window frame is `RANGE`, not `ROWS`** — so the obvious way to write a running total is **wrong whenever the ordering column has duplicates**, which for dates is almost always.
- **§10: rewriting a correlated subquery as a window function was 3 068× faster** — after a first measurement that said the opposite, for an instructive reason.

## 📘 Main Knowledge

### 1. Subqueries

| kind | returns | used |
|---|---|---|
| **scalar** | one value | anywhere a constant can go |
| **`IN` / `NOT IN`** | one column | set membership *(⚠️ [[05 - SQL Fundamentals\|ch. 05]] §3)* |
| **`EXISTS`** | boolean | existence tests — **null-safe** |
| **correlated** | re-evaluated per outer row | comparisons against a row's own group |
| **derived table** | a table | in `FROM`, by [[02 - The Relational Model and Relational Algebra\|ch. 02]]'s closure |

**The distinction that matters is scalar versus correlated:**

```sql
-- SCALAR: one global average, computed once
WHERE salary > (SELECT AVG(salary) FROM emp)

-- CORRELATED: each employee against their OWN department's average
WHERE salary > (SELECT AVG(salary) FROM emp x WHERE x.dept_id = e.dept_id)
```

*(Verified: they select different employees. `Vo F` at 55 000 beats the global average, but the correlated version judges him against IT's higher average.)*

**The correlated subquery references the outer row (`e.dept_id`), so it is conceptually re-executed for every row** — which is where §10's performance problem comes from.

**`EXISTS` stops at the first match** and returns a boolean, so it never compares values — **which is why it is null-safe and why [[05 - SQL Fundamentals|ch. 05]] recommended `NOT EXISTS` over `NOT IN`.**

### 2. Common table expressions

**A CTE names an intermediate result.** It is exactly a derived table with a name in front:

```sql
WITH agg AS (
    SELECT dept_id, COUNT(*) AS n, ROUND(AVG(salary)) AS avg_sal
    FROM emp GROUP BY dept_id
)
SELECT dept_name, n, avg_sal FROM dept JOIN agg USING (dept_id) ORDER BY avg_sal DESC;
```

*(Verified identical to the derived-table version.)*

> [!note] The benefit is readability, and it is not a small one
> **A derived table reads inside-out**; a CTE reads **top to bottom, in the order the work happens.** With three or four stages the difference between a comprehensible query and an unmaintainable one is entirely this.
>
> **Multiple CTEs can be chained**, each referring to the previous, which turns a nested monster into a sequence of named steps. **Same plan, same speed** — most engines inline CTEs. *(PostgreSQL before v12 materialised them, which could be slower; `MATERIALIZED` / `NOT MATERIALIZED` now control it explicitly.)*

### 3. Recursive CTEs — the thing plain SQL cannot do

```sql
WITH RECURSIVE tree(cat_id, name, depth, path) AS (
    SELECT cat_id, name, 0, name FROM category WHERE parent IS NULL   -- anchor
    UNION ALL
    SELECT c.cat_id, c.name, t.depth+1, t.path || ' > ' || c.name     -- recursive step
    FROM category c JOIN tree t ON c.parent = t.cat_id
)
SELECT depth, path FROM tree ORDER BY path;
```

*(Verified:)*
```
depth | path
------+--------------------------------------
0     | All
1     | All > Clothing
2     | All > Clothing > Shoes
1     | All > Electronics
2     | All > Electronics > Computers
3     | All > Electronics > Computers > Laptops
3     | All > Electronics > Computers > Desktops
```

> [!note] Why this is genuinely different
> **A plain join can only traverse a fixed number of levels.** Three joins gives you three levels; a hierarchy of unknown depth cannot be walked at all without recursion.
>
> **The structure is always the same:** an **anchor** (the starting rows) `UNION ALL` a **recursive step** referring to the CTE itself. **This is [[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]]'s graph traversal in SQL** — and it inherits the same hazard: **a cycle in the data makes it loop forever.** Guard with a depth limit or by accumulating a visited path.

### 4. Window functions — aggregate without collapsing

> [!note] The defining difference
> **`GROUP BY` collapses rows; a window function does not.**

*(Verified — the same data both ways:)*
```
GROUP BY: 8 rows in, 3 out          window: 8 rows in, 8 out
dept_id | n | avg_sal                emp_name | dept_id | salary | dept_avg | vs_dept_avg
--------+---+--------                ---------+---------+--------+----------+------------
10      | 3 | 47333                  Nguyen A | 10      | 50000  | 47333    | 2667
20      | 3 | 51667                  Le C     | 10      | 50000  | 47333    | 2667
30      | 2 | 47000                  Tran B   | 10      | 42000  | 47333    | -5333
```

```sql
AVG(salary) OVER (PARTITION BY dept_id)
```

**`GROUP BY` answers *"what is the average per department?"*. The window function answers *"how does each employee compare with their department's average?"* — a question `GROUP BY` cannot express**, because the individual rows are gone by the time the average exists.

**`PARTITION BY` is the window's `GROUP BY`; `ORDER BY` inside `OVER` defines an ordering within each partition (needed for running totals and ranking).**

### 5. `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`

**They differ only on ties** *(verified — Sales has a 50 000 tie, Research a 47 000 tie)*:

| emp | salary | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|---|---|---|---|---|
| Nguyen A | 50 000 | **1** | 1 | 1 |
| Le C | 50 000 | **2** | 1 | 1 |
| Tran B | 42 000 | 3 | **3** | **2** |

- **`ROW_NUMBER`** — always 1, 2, 3. **Ties are broken arbitrarily.**
- **`RANK`** — ties share a rank, then it **skips** (1, 1, 3).
- **`DENSE_RANK`** — ties share a rank, **no gap** (1, 1, 2).

> [!warning] `ROW_NUMBER` is nondeterministic without a tiebreaker
> With `ORDER BY salary DESC` alone, which of the two 50 000 employees gets row 1 is **undefined** — it may change between runs, releases or query plans.
>
> **Always add a unique tiebreaker**: `ORDER BY salary DESC, emp_name`. Otherwise a "top 1 per group" query can silently return a different person tomorrow, and a report that is supposed to be reproducible is not.

### 6. Top-N per group — the proper fix for [[05 - SQL Fundamentals|ch. 05]]'s bare-column trap

```sql
WITH ranked AS (
    SELECT emp_name, dept_id, salary,
           ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_name) AS rn
    FROM emp
)
SELECT dept_id, emp_name, salary FROM ranked WHERE rn = 1 ORDER BY dept_id;
```
*(Verified.)*

**[[05 - SQL Fundamentals|Ch. 05]] §7 showed that `SELECT dept_id, emp_name, MAX(salary) … GROUP BY dept_id` works in SQLite by a documented accident and is meaningless in PostgreSQL. This is the portable, deterministic answer** — and changing `rn = 1` to `rn <= 3` gives top-3 per group, which the `MAX` trick cannot do at all.

### 7. `LAG` and `LEAD` — comparing with neighbouring rows

```sql
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_month,
       revenue - LAG(revenue) OVER (ORDER BY month) AS change
FROM sales;
```

```
month   | revenue | prev_month | change | pct_change
--------+---------+------------+--------+-----------
2025-01 | 1000    | None       | None   | None
2025-02 | 1200    | 1000       | 200    | 20.0
2025-03 | 1100    | 1200       | -100   | -8.3
```

*(Verified.)* **This is period-over-period analysis without a self-join** — the first row's `LAG` is correctly `NULL`, and [[05 - SQL Fundamentals|ch. 05]]'s null rules then apply: **that row will vanish from any subsequent filter unless you handle it.**

### 8. ⚠️ The frame trap — the default is `RANGE`, not `ROWS`

**A running total is usually written like this:**
```sql
SUM(revenue) OVER (ORDER BY revenue)
```

**With a tie in the ordering column, that is wrong.** *(Verified — ordering by `revenue`, which has two rows at 1500:)*

| month | revenue | default frame | explicit `ROWS` | explicit `RANGE` |
|---|---|---|---|---|
| 2025-01 | 1000 | 1000 | 1000 | 1000 |
| 2025-03 | 1100 | 2100 | 2100 | 2100 |
| 2025-02 | 1200 | 3300 | 3300 | 3300 |
| **2025-04** | **1500** | **6300** | **4800** | **6300** |
| **2025-05** | **1500** | **6300** | **6300** | **6300** |
| 2025-06 | 1800 | 8100 | 8100 | 8100 |

> [!warning] Look at the first 1500 row: 6300 versus 4800
> **The default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`**, and the default matches `RANGE`, not `ROWS`.
>
> - **`RANGE` is *value*-based.** "Current row" means **every row with the same `ORDER BY` value**, so both 1500 rows get an identical total — each already includes the other.
> - **`ROWS` is *position*-based.** Each row includes only rows up to its own position, giving the running total you intended.
>
> **So `SUM(x) OVER (ORDER BY date)` is wrong whenever two rows share a date** — and duplicate dates are the normal case: multiple transactions per day, multiple readings per timestamp, anything at daily granularity.
>
> **The failure is silent and plausible.** Tied rows share an inflated value, the final total is still correct, and only the intermediate rows are wrong — so a spot-check of the last row passes.
>
> **Always write the frame explicitly:**
> ```sql
> SUM(x)  OVER (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)  -- running total
> AVG(x)  OVER (ORDER BY d ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)          -- 3-period moving average
> ```
> *(Both verified: running total 1000 → 2200 → 3300 → 4800 → 6300 → 8100; moving average 1000 → 1100 → 1100 → 1266.7 → 1366.7 → 1600.)*

### 9. Views

**A view stores the *query*, not the result.**

```sql
CREATE VIEW v_dept_summary AS
    SELECT d.dept_id, d.dept_name, COUNT(e.emp_id) AS headcount,
           ROUND(AVG(e.salary)) AS avg_salary
    FROM dept d LEFT JOIN emp e USING (dept_id)
    GROUP BY d.dept_id, d.dept_name;
```

*(Verified: after inserting an employee into Research, the view's headcount went 2 → 3 and its average changed, with no refresh.)*

**So a view is always current and costs exactly what its query costs.** It is the **external level** of [[01 - Databases and Data Models|ch. 01]] §9 made real: a stable interface that hides joins, restricts columns, and survives restructuring of the tables beneath.

> [!note] Two engine facts, verified
> **SQLite views are read-only** — `UPDATE v_dept_summary …` gives *"cannot modify v_dept_summary because it is a view"*. Other engines permit updates through simple views, and offer `INSTEAD OF` triggers for complex ones.
>
> **SQLite has no materialised views.** PostgreSQL's `CREATE MATERIALIZED VIEW … REFRESH` caches the *result* — fast to read, but **stale until refreshed.**
>
> **A materialised view is exactly [[04 - Normalization|ch. 04]] §8's denormalisation trade, managed by the DBMS instead of by hand** — which is why [[04 - Normalization|ch. 04]] recommended trying one before denormalising manually. The redundancy still exists; the difference is that the engine owns keeping it correct.

### 10. Correlated subquery versus window function — 3 068×

**The same question two ways** — "each row against its group's average", on 40 000 rows in 200 groups:

```sql
-- correlated subquery: re-scans the group for every row
SELECT id, (SELECT AVG(v2.val) FROM big v2 WHERE v2.grp = b.grp) FROM big b;

-- window function: partitions once
SELECT id, AVG(val) OVER (PARTITION BY grp) FROM big;
```

| | time |
|---|---|
| correlated subquery | **51.13 s** |
| **window function** | **0.0167 s — 3 068× faster** |

*(Verified; identical results.)*

**The correlated form is quadratic**: for each of 40 000 rows it scans the table to find that row's group. The window function sorts once and sweeps.

> [!warning] My first measurement said the opposite, and the reason is worth knowing
> I initially timed both with `ORDER BY id LIMIT 5`, and got:
> ```
> correlated + LIMIT 5 : 0.0060 s
> window     + LIMIT 5 : 0.0220 s   -> window 3.6x SLOWER
> ```
> **The `LIMIT` invalidated the comparison.** `id` is the primary key, so SQLite could produce the first five rows in order and stop — **evaluating the correlated subquery only five times.** The window function, by contrast, **must partition all 40 000 rows before it can emit anything.**
>
> **So the first test measured "cost to produce five rows", not "cost to answer the question".** Removing the `LIMIT` reversed the result by four orders of magnitude.
>
> *(A second attempt also failed: wrapping in `SELECT COUNT(*)` let the optimiser discard the subquery entirely, giving 0.0000 s. Forcing the value to be used — `SUM(grp_avg)` — produced the real figure.)*
>
> **This is the vault's recurring lesson in a new subject: when a measurement contradicts a sound argument, suspect the measurement.** A `LIMIT`, a lazily-evaluated column, or an optimiser shortcut can each make a benchmark answer a different question from the one asked.

## ✏️ Exercises

**1. (Subqueries and CTEs.)** (a) Distinguish scalar, correlated and derived-table subqueries. (b) Why is `EXISTS` null-safe? (c) What does a CTE add? (d) What can a recursive CTE do that nothing else can?

> [!example]- Solution
> **(a)** A **scalar** subquery returns a single value and is evaluated **once**, usable anywhere a constant is. A **correlated** subquery references a column of the outer query, so it is **conceptually re-evaluated for every outer row**. A **derived table** appears in `FROM` and returns a table.
>
> *(Verified: the scalar version compares every employee to one global average; the correlated version compares each to their own department's — selecting different people.)*
>
> **The performance consequence is severe and is §10's subject**: the correlated form is quadratic, and rewriting it as a window function was **3 068× faster**.
>
> **Derived tables exist because of [[02 - The Relational Model and Relational Algebra|ch. 02]] §5's closure** — a query returns a relation, so it can appear wherever a relation can.
>
> **(b) Because it never compares values — it asks whether a row exists.**
>
> `NOT IN (10, 20, NULL)` expands to a chain of `<>` comparisons, one of which is unknown, poisoning the whole result ([[05 - SQL Fundamentals|ch. 05]] §3 — verified there to return **zero rows for any data**).
>
> **`NOT EXISTS` asks a different question**: *"is there a row in `emp` with this `dept_id`?"* For a department with no employees, the correlated condition `e.dept_id = d.dept_id` is false-or-unknown for every row, so **no matching row exists** — and "no match exists" is a definite answer even when values are unknown.
>
> **The general principle: existence tests are three-valued-logic-safe; value comparisons are not.**
>
> **(c) Readability, and it is the difference between maintainable and not.**
>
> A derived table reads **inside-out** — you must find the innermost parenthesis and work outward. A CTE reads **top to bottom, in the order the work happens**, and each stage has a name saying what it is.
>
> *(Verified identical output to the derived-table version — this is purely a rewriting.)*
>
> **CTEs also compose**: a second CTE can refer to the first, turning a deeply nested query into a linear sequence of steps. **And a CTE can be referenced twice** in the same query, which a derived table cannot without repeating it.
>
> **Performance is normally unchanged** — most engines inline CTEs into the surrounding query. *(The exception worth knowing: PostgreSQL before v12 always materialised them, creating an optimisation fence that could be much slower. Since v12 it inlines by default, with `MATERIALIZED` / `NOT MATERIALIZED` to override.)*
>
> **(d) Traverse a structure of unknown depth.**
>
> **A plain join goes a fixed number of levels** — three joins, three levels. A hierarchy whose depth is not known when the query is written cannot be traversed at all.
>
> *(Verified: the category tree was walked to depth 3, building a full path string, with one query that would work at depth 30.)*
>
> **The structure is always anchor `UNION ALL` recursive-step.** The anchor supplies the starting rows; the step refers to the CTE itself and is repeated until it produces nothing.
>
> **This is [[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]]'s traversal in SQL, and it inherits the same hazard: a cycle makes it run forever.** [[03 - Entity-Relationship Modelling|Ch. 03]] noted that nothing prevents a cycle in a recursive foreign key. **Defend with a depth counter (`WHERE depth < 50`) or by accumulating the visited path and excluding revisits** — the `path` column here would support exactly that.

**2. (Window functions.)** (a) What is the defining difference from `GROUP BY`? (b) Explain the three ranking functions on ties. (c) Why is `ROW_NUMBER` dangerous without a tiebreaker? (d) How does this fix ch. 05's bare-column trap?

> [!example]- Solution
> **(a) `GROUP BY` collapses rows; a window function keeps them.**
>
> *(Verified: `GROUP BY` turned 8 rows into 3; `AVG(salary) OVER (PARTITION BY dept_id)` returned all 8 with the departmental average attached to each.)*
>
> **This changes what questions are askable.** `GROUP BY` answers *"what is the average per department?"*. **A window function answers *"how does each employee compare to their department's average?"* — and `GROUP BY` cannot express that at all**, because by the time the average exists the individual rows are gone.
>
> **The usual workaround before window functions was a self-join to an aggregated derived table**, which is verbose and, as §10 shows, can be catastrophically slow when written as a correlated subquery instead.
>
> **`PARTITION BY` is the window's `GROUP BY`**; omitting it makes the whole result one partition. **`ORDER BY` inside `OVER` orders rows within each partition**, which ranking, `LAG`/`LEAD` and running totals all require.
>
> **(b)**
>
> | | ties | after a 2-way tie |
> |---|---|---|
> | `ROW_NUMBER` | **broken arbitrarily** — 1, 2 | 3 |
> | `RANK` | share a rank — 1, 1 | **3** (skips) |
> | `DENSE_RANK` | share a rank — 1, 1 | **2** (no gap) |
>
> *(Verified on a 50 000 tie in Sales.)*
>
> **Which to use depends on the question.** `DENSE_RANK` for "how many distinct salary levels are above this one" — grades, bands, medal-style rankings. `RANK` for competition ranking where two firsts mean no second. **`ROW_NUMBER` when you need exactly one row per position** — deduplication, pagination, top-N.
>
> **(c) Because which tied row gets which number is undefined.**
>
> With `ORDER BY salary DESC` alone and two employees at 50 000, **the engine may return either order**, and the choice can change between runs, between releases, or when the query plan changes because an index was added.
>
> **The consequences are worse than they look.** A "top earner per department" report becomes **non-reproducible** — it may name a different person tomorrow with no data change. A deduplication keeping `rn = 1` deletes an **arbitrary** one of the duplicates. **And the bug is invisible in testing**, since any single run looks consistent.
>
> **The fix is one clause: add a unique tiebreaker.** `ORDER BY salary DESC, emp_name` *(verified)* — or better, the primary key, which is guaranteed unique.
>
> **The general rule: any `ORDER BY` whose result you depend on should be total.** The same applies to `ORDER BY … LIMIT` in ordinary queries.
>
> **(d)** [[05 - SQL Fundamentals|Ch. 05]] §7 showed `SELECT dept_id, emp_name, MAX(salary) … GROUP BY dept_id` is accepted by SQLite (which documents that bare columns come from the `MAX` row) and **rejected by PostgreSQL** — so it is non-portable, and with any other aggregate the bare column is arbitrary.
>
> **The window-function version is portable and deterministic** *(verified)*:
> ```sql
> WITH ranked AS (SELECT …, ROW_NUMBER() OVER (PARTITION BY dept_id
>                                              ORDER BY salary DESC, emp_name) AS rn FROM emp)
> SELECT dept_id, emp_name, salary FROM ranked WHERE rn = 1;
> ```
>
> **And it generalises in ways the `MAX` trick cannot.** `rn <= 3` gives top-3 per group. `RANK()` instead of `ROW_NUMBER()` keeps all tied leaders rather than picking one. Additional columns come along automatically. **The `MAX` trick can do none of these** — it is a special case that happens to work for exactly one problem, in one engine.

**3. (Hard — the frame trap.)** (a) What is the default frame? (b) Explain 6300 versus 4800. (c) Why is this dangerous in real data? (d) State the rule.

> [!example]- Solution
> **(a) `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`** — the SQL standard default whenever `ORDER BY` appears inside `OVER` without an explicit frame.
>
> *(Verified: the default column matched `explicit_range` exactly and differed from `explicit_rows`.)*
>
> **(b) Because `RANGE` defines "current row" by *value*, not by position.**
>
> Two rows share `revenue = 1500`. Under **`RANGE`**, the frame for either of them is *"all rows whose ordering value is ≤ 1500"* — **which includes both tied rows.** So both get 1000 + 1100 + 1200 + 1500 + 1500 = **6300**.
>
> Under **`ROWS`**, the frame is *"all rows up to my position"*. The first 1500 row includes only itself and its predecessors: 1000 + 1100 + 1200 + 1500 = **4800**. The second includes both: **6300**.
>
> **`RANGE` treats tied rows as a single indivisible point in the ordering; `ROWS` treats them as distinct positions.** With no ties the two are identical, which is exactly why the trap survives — **it is invisible until duplicates appear.**
>
> **(c) Because duplicate ordering values are the normal case, and the failure is silent and partial.**
>
> **Where duplicates arise:** multiple transactions on the same date, several readings at the same timestamp, any daily aggregation, ties in a score or amount. **A running total over a date column is the single commonest window function**, and if more than one row shares a date the intermediate values are wrong.
>
> **The failure is unusually well camouflaged:**
> - **The final total is still correct** — the last row's frame includes everything either way. **A spot-check of the total passes.**
> - **Only the tied rows are wrong**, so most rows agree and the error looks like noise.
> - **The values are plausible** — monotonically increasing, right order of magnitude.
> - **It is data-dependent**: correct until the day two rows share a date, then silently wrong, with no code change to blame.
>
> **That last property puts it in the same class as [[05 - SQL Fundamentals|ch. 05]]'s `NOT IN` trap, [[03 - Entity-Relationship Modelling|ch. 03]]'s fan trap and [[02 - The Relational Model and Relational Algebra|ch. 02]]'s inner-join row loss** — correct-looking SQL, no error, wrong answer, and it starts failing only when the data changes.
>
> **A related surprise worth knowing:** `ROW_NUMBER`, `RANK` and `LAG`/`LEAD` are unaffected, because they do not use the frame. **Only frame-sensitive aggregates (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX` over a window) are hit** — so a query mixing them can have some columns right and others wrong.
>
> **(d) Always write the frame explicitly.**
> ```sql
> SUM(x) OVER (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)  -- running total
> AVG(x) OVER (ORDER BY d ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)          -- 3-period moving avg
> ```
> *(Both verified.)*
>
> **Supporting habits:**
> 1. **Treat an `OVER (ORDER BY …)` with no frame as a bug** in review, even when it currently gives the right answer.
> 2. **Check whether the ordering column has duplicates** — `GROUP BY d HAVING COUNT(*) > 1`. If it does, `RANGE` and `ROWS` differ.
> 3. **Use `RANGE` deliberately when you want value-based semantics** — "total of everything up to and including this amount" is a real question, and then `RANGE` is right. The problem is never `RANGE` itself; it is `RANGE` **by default, unnoticed**.
> 4. **Add a tiebreaker to the `ORDER BY`** so the ordering is total, which also fixes §5's `ROW_NUMBER` nondeterminism.

**4. (Views and performance.)** (a) What does a view store? (b) Compare views and materialised views. (c) Explain the 3 068× result. (d) What went wrong with the first measurement, and what is the general lesson?

> [!example]- Solution
> **(a) The query, not the result.**
>
> *(Verified: inserting an employee into Research changed the view's headcount from 2 to 3 and its average salary, with no refresh — the view re-ran.)*
>
> **Consequences:** it is **always current**; it **costs what its query costs** every time (a view over a slow join is a slow view); and it **stores no data**, so it takes no space and cannot become inconsistent.
>
> **Its real value is as an interface** — the **external level** of [[01 - Databases and Data Models|ch. 01]] §9. It hides join logic so it is written once instead of in every query, restricts which columns are visible (a security boundary), and **gives analysts a stable contract when the underlying tables are restructured.**
>
> *(Verified engine fact: SQLite views are read-only — `UPDATE` on one gives "cannot modify … because it is a view". Other engines allow updates through simple views and offer `INSTEAD OF` triggers for complex ones.)*
>
> **(b)**
>
> | | view | materialised view |
> |---|---|---|
> | stores | the query | **the result** |
> | freshness | **always current** | **stale until refreshed** |
> | read cost | the full query | **a table scan** |
> | space | none | a full copy |
>
> **A materialised view is [[04 - Normalization|ch. 04]] §8's denormalisation, managed by the DBMS.** The redundancy is real — the data is genuinely duplicated — but **the engine owns keeping it correct**, which removes the failure mode where hand-maintained denormalised data silently drifts.
>
> **The remaining risk is staleness, and it is visible and bounded**: you know when the last refresh was, unlike hand-rolled duplication where you do not know whether the copy is right. **This is why [[04 - Normalization|ch. 04]] put "materialised view" above "denormalise by hand" in its list of options.**
>
> *(SQLite has none — verified. PostgreSQL: `CREATE MATERIALIZED VIEW … / REFRESH MATERIALIZED VIEW`, optionally `CONCURRENTLY`.)*
>
> **(c) The correlated subquery is quadratic; the window function is one sort and one sweep.**
>
> | | |
> |---|---|
> | correlated subquery | **51.13 s** |
> | window function | **0.0167 s** |
>
> **For each of 40 000 rows, the correlated subquery scans to find that row's group** — work proportional to $n^2$, roughly 1.6 billion row-touches. **The window function sorts by `grp` once and computes each partition's average in a single pass** — $O(n\log n)$.
>
> **Identical results** *(verified)*.
>
> **The practical lesson: a correlated subquery in the `SELECT` list is a red flag.** It is the SQL equivalent of a nested loop, and a window function is usually the same query without the loop. *(An index on `grp` would help the correlated form considerably — [[09 - Query Optimization and Indexing|ch. 09]] — but it cannot make it linear.)*
>
> **(d) The first measurement used `LIMIT 5` and therefore answered a different question.**
> ```
> correlated + LIMIT 5 : 0.0060 s
> window     + LIMIT 5 : 0.0220 s     -> window 3.6x SLOWER
> ```
> **`id` is the primary key, so SQLite could walk it in order, produce five rows and stop — evaluating the correlated subquery only five times.** The window function **cannot emit anything until it has partitioned all 40 000 rows**, so it paid the full cost to return five.
>
> **The benchmark measured "cost to produce the first five rows", not "cost to answer the question".** Removing the `LIMIT` reversed the result by four orders of magnitude.
>
> **A second attempt failed differently:** wrapping each in `SELECT COUNT(*)` gave 0.0000 s, because the optimiser saw the computed column was unused and **discarded the subquery entirely.** Forcing it to be consumed — `SUM(grp_avg)` — produced the real number.
>
> **Both failures share a shape: the benchmark did less work than the question required**, once by early termination and once by dead-code elimination.
>
> **The general lesson — and this vault has now hit it in two subjects — is that when a measurement contradicts a sound argument, the measurement is the thing to doubt.** [[Data Structures and Algorithms/contents/00-Index|DSA]] recorded five such cases. **The specific hazards for SQL benchmarking:**
> 1. **`LIMIT` lets some plans stop early** and others not — it changes what is being compared.
> 2. **Unused expressions may be optimised away.** Consume the result.
> 3. **Caching** — run several times and take the minimum.
> 4. **Check the plan (`EXPLAIN QUERY PLAN`)** when a result surprises you; it says what the engine actually did ([[09 - Query Optimization and Indexing|ch. 09]]).

## 📝 Summary

- **Subqueries:** scalar (one value, evaluated once), correlated (references the outer row, re-evaluated per row), `EXISTS` (boolean, **null-safe**), derived table (in `FROM`, by closure). *(Verified: scalar and correlated versions select different employees.)*
- **A CTE is a named derived table** — same plan, same speed, **read top-to-bottom instead of inside-out**, and referenceable more than once.
- **Recursive CTEs traverse structures of unknown depth** — anchor `UNION ALL` recursive step. *(Verified on a category tree.)* **A cycle in the data loops forever**; guard with a depth limit.
- **Window functions aggregate without collapsing rows** *(verified: 8 rows in, 8 out, with the group average attached)*. **`GROUP BY` cannot express "each row versus its group".**
- **`ROW_NUMBER` (1,2,3), `RANK` (1,1,3), `DENSE_RANK` (1,1,2)** differ only on ties *(verified)*.
- **⚠️ `ROW_NUMBER` is nondeterministic without a unique tiebreaker** — a "top earner" report can name a different person tomorrow with no data change.
- **Top-N per group via `ROW_NUMBER` in a CTE** is the portable fix for [[05 - SQL Fundamentals|ch. 05]]'s bare-column trap, and generalises to top-3 as the `MAX` trick cannot.
- **`LAG`/`LEAD` give period-over-period comparison without a self-join**; the first row's `LAG` is correctly null.
- **⚠️ The default window frame is `RANGE`, not `ROWS`.** *(Verified: with a tie in the ordering column, a running total gave **6300** where `ROWS` gives **4800**.)* `RANGE` is value-based and treats tied rows as one point; `ROWS` is position-based.
- **So `SUM(x) OVER (ORDER BY date)` is wrong whenever two rows share a date** — and the failure is silent, partial, and leaves the final total correct. **Always write the frame explicitly.**
- **Ranking and `LAG`/`LEAD` are unaffected by the frame**, so one query can have some columns right and others wrong.
- **A view stores the query, not the result** *(verified: it updated itself after an insert)*. **SQLite views are read-only and it has no materialised views.**
- **A materialised view is [[04 - Normalization|ch. 04]]'s denormalisation with the DBMS owning correctness** — stale but *visibly* stale, which beats hand-maintained duplication.
- **A correlated subquery rewritten as a window function ran 3 068× faster** (51.13 s → 0.0167 s) — the correlated form is quadratic.
- **⚠️ The first benchmark said the opposite**, because `LIMIT 5` let the correlated form stop early while the window function had to partition everything. **A second attempt was optimised away entirely.** *When a measurement contradicts a sound argument, doubt the measurement.*

## ⚠️ Important Notes

1. **Prefer `NOT EXISTS` to `NOT IN`** on nullable columns — existence tests are null-safe, value comparisons are not ([[05 - SQL Fundamentals|ch. 05]] §3).
2. **A correlated subquery in the `SELECT` list is a red flag.** It is a nested loop; a window function is usually the same query without it.
3. **Use CTEs for anything with more than two stages.** Inside-out nesting is where SQL becomes unmaintainable.
4. **Guard recursive CTEs against cycles** with a depth limit or a visited-path check. Nothing in the data prevents one.
5. **Reach for a window function whenever the question is "each row compared with its group".** `GROUP BY` cannot answer it.
6. **⚠️ Always give `ROW_NUMBER` a unique tiebreaker.** Otherwise the result is nondeterministic and the report is not reproducible.
7. **Pick the right ranking function**: `DENSE_RANK` for bands, `RANK` for competition ranking, `ROW_NUMBER` for exactly-one-per-position.
8. **Use `ROW_NUMBER` in a CTE for top-N per group**, not the `MAX` + bare-column trick, which is non-portable and does not generalise.
9. **⚠️ Never write `OVER (ORDER BY …)` without an explicit frame.** The default is `RANGE`, which silently mis-computes running totals when the ordering column has duplicates.
10. **Check whether your ordering column has ties** — `GROUP BY d HAVING COUNT(*) > 1`. If so, `RANGE` and `ROWS` differ.
11. **Use `RANGE` deliberately when value-based semantics are what you want.** The problem is `RANGE` unnoticed, not `RANGE`.
12. **Remember `LAG`'s first row is null**, and that [[05 - SQL Fundamentals|ch. 05]]'s null rules then apply — it will vanish from any filter.
13. **Use views as the analyst-facing interface.** They hide joins, restrict columns, and survive restructuring below.
14. **A view costs what its query costs, every time.** A view over a slow join is a slow view.
15. **Prefer a materialised view to hand-maintained denormalisation** — the staleness is visible and bounded, unlike silent drift.
16. **⚠️ When benchmarking SQL: avoid `LIMIT`** (it lets some plans stop early), **consume the result** (or it may be optimised away), **take the minimum of several runs**, and **check `EXPLAIN QUERY PLAN`** when the answer surprises you.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 8 extracts cleanly** — the subquery taxonomy, set operators, views, and the SQL function catalogue came through readably. **Book page $n$ = PDF page $n+28$; ch. 8 is PDF pages 379–458.**
>
> **All figures are images and are lost**, but as in [[05 - SQL Fundamentals|ch. 05]] this matters less than elsewhere, because C&M's figures here are screenshots of query results — **and every result in this note is live output from a real database instead.**
>
> **The entire dataset is my own.** C&M's examples run against downloadable sample databases not present in `documents/`, so the `dept`/`emp`, `category`, `sales` and `big` schemas and all their data were written for this note — **deliberately seeded with ties** (two employees at 50 000, two at 47 000, two months at 1 500 revenue), because ties are what make §5's ranking differences and §8's frame trap visible at all.
>
> **No error was found in Coronel & Morris ch. 8.**
>
> **Additions beyond the source — this is the most heavily enriched chapter in the subject so far**, as the subject file predicted for the analytics material.
>
> - **§§4–8, the entire window-function treatment, is essentially mine.** C&M's coverage of window functions is brief relative to their importance for data analysis, and **the frame clause — the subject of §8 — is not covered in the depth needed to avoid the trap.**
> - **§8's `RANGE`-versus-`ROWS` demonstration is my own and is the chapter's most valuable finding.** That the *default* frame silently mis-computes running totals over duplicated ordering values is a real, common, silent bug; showing 6300 against 4800 on the same data makes it concrete. **I have not seen it stated in an introductory database text.**
> - **§5's point that `ROW_NUMBER` is nondeterministic without a tiebreaker**, and its consequence for report reproducibility, is an addition.
> - **§6's framing of top-N-per-group as the *fix* for [[05 - SQL Fundamentals|ch. 05]] §7's bare-column trap** is my own cross-chapter link.
> - **§10's benchmark is mine**, along with the account of its two failed attempts — the `LIMIT` that let the correlated form stop early, and the `COUNT(*)` that let the optimiser discard the work. **The four SQL-benchmarking hazards in Important Note 16 are drawn from those failures.**
> - **The materialised-view discussion** connecting back to [[04 - Normalization|ch. 04]]'s denormalisation options, and **the recursive-CTE cycle hazard** connecting to [[03 - Entity-Relationship Modelling|ch. 03]] and [[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]], are additions.
>
> **Deliberately compressed.** **Set operators (`UNION`, `INTERSECT`, `EXCEPT`) are not re-covered** — they were executed and explained in [[02 - The Relational Model and Relational Algebra|ch. 02]] §4 as the relational-algebra operators they are, including the union-compatibility requirement. **C&M's SQL function catalogue (§8-6, string/numeric/date/conversion functions)** is reference material that differs per engine and dates quickly; [[05 - SQL Fundamentals|ch. 05]] §9 covered the ones whose *semantics* surprise people. **Sequences and triggers (§8-4, §8-5)** are omitted: triggers are procedural rather than declarative and belong with the transactional material of [[08 - Transactions and Concurrency Control|ch. 08]], and sequences are largely superseded by identity columns. **Embedded SQL and dynamic SQL (§8-8)** are application-integration topics excluded with C&M ch. 15 by the scope decision in `00-Index.md`. **`INSTEAD OF` triggers on views are mentioned but not demonstrated**, since SQLite's read-only views make it untestable here — flagged rather than described as if verified.

**Previous:** [[05 - SQL Fundamentals]] · **Next:** [[07 - Database Design]]
