---
subject: Database Management Systems
chapter: 8
tags: [ds, dbms, transactions, acid, concurrency, locking, isolation-levels, lost-update, deadlock, wal]
source: "Coronel & Morris, *Database Systems: Design, Implementation, & Management*, ch. 10"
---

# Transactions and Concurrency Control

Every chapter so far has assumed **one user at a time**. This one removes that assumption, and the consequences are severe: **operations that are individually correct produce wrong results when they interleave.**

The centrepiece is §4, where five concurrent threads make 100 bookings against 100 seats and **only 20 seats are consumed — 80 are sold twice.** Every booking committed successfully. No error was raised. The database was in a perfectly valid state throughout.

**And the crucial point, which is the one most often got wrong: no isolation level prevents that bug.** It happens *between* transactions, in the application. §§5–6 give the two fixes that do work.

## 📘 Main Knowledge

### 1. What a transaction is

> [!note] Definition
> A **transaction** is a logical unit of work that takes the database from one consistent state to another. **It succeeds entirely or not at all.**

The canonical example is a transfer: debit one account, credit another. **Either both happen or neither does** — a debit without its credit destroys money.

### 2. ACID, verified

**Atomicity — all or nothing.** *(Verified:)*
```
before:               {Alice: 1000, Bob: 500}
mid-transaction:      {Alice: 800,  Bob: 500}     <- debit applied
second statement failed -> CHECK constraint failed: balance >= 0
after ROLLBACK:       {Alice: 1000, Bob: 500}     <- debit undone
```
**The partial work vanished.** Without atomicity, Alice would be 200 poorer and nobody richer.

**Consistency — constraints hold at commit.** *(Verified: setting a balance to −1 was rejected.)* The database moves between *valid* states only; the constraints of [[07 - Database Design|ch. 07]] define what valid means.

**Isolation — concurrent transactions do not see each other's partial work.** §7.

**Durability — a committed change survives.** *(Verified: a committed balance of 1234 was still there after closing and reopening the database file.)*

> [!note] Where each property comes from
> **Atomicity and durability come from the write-ahead log or rollback journal** — the DBMS records what it is about to do, so it can undo (atomicity) or redo (durability) after a crash. **Consistency comes from your constraints** — it is the property the *designer* supplies, which is why [[07 - Database Design|ch. 07]]'s audit matters. **Isolation comes from concurrency control**, and it is the one with a tunable cost.

### 3. The three concurrency problems

| problem | what happens |
|---|---|
| **Lost update** | two transactions read the same value, both modify it, **one overwrites the other** |
| **Uncommitted data (dirty read)** | one transaction reads data another has written but **not committed** — and which may be rolled back |
| **Inconsistent retrieval** | a transaction reads data **while another is changing it**, so the values are internally inconsistent |

### 4. ⚠️ The lost update, produced for real

**The realistic pattern** — read in one request, write in a later one, which is how every web application works:

```python
seats = SELECT available FROM seats        # request 1
# ... the user thinks, the request returns ...
UPDATE seats SET available = seats - 1     # request 2, a separate transaction
```

**Five threads, 20 bookings each, against 100 seats** *(verified)*:

```
bookings attempted     : 100
bookings that errored  : 0
bookings that COMMITTED: 100
seats consumed         : 20
final available        : 80

*** 100 bookings committed but only 20 seats were taken.
    80 seats were sold twice. ***
```

> [!warning] Every booking succeeded, and four out of five were fictitious
> **No error. No warning. No constraint violated.** The database was in a valid state before, during and after — `available` never went negative, and every transaction was individually correct.
>
> **The mechanism:** many threads read `available = 100`, each computes 99, each writes 99. **The last writer wins and the others are silently discarded.** The seats were sold; the count was not decremented.
>
> **This is the airline-overbooking bug, the double-spend bug, and the inventory-oversell bug** — the same defect each time.
>
> **The critical misconception to kill: this is *not* an isolation-level problem.** The read and the write are in **different transactions**, with an unbounded gap between them. **No isolation level covers a gap it cannot see** — there is no transaction spanning the read and the write for the DBMS to protect. Setting `SERIALIZABLE` changes nothing.

**An earlier version of this experiment produced a different, also instructive, result.** With the read *inside* the writing transaction, SQLite prevented every lost update — **by rejecting 51 of the 100 bookings with `database is locked`.** *(Verified.)* **Correctness was preserved by refusing half the work**, which is the isolation/throughput trade in its rawest form.

### 5. Fix 1 — make the read-modify-write atomic

```sql
UPDATE seats SET available = available - 1 WHERE flight = 'VN123' AND available > 0;
```

*(Verified: 100 bookings committed, **100 seats consumed, 0 lost**, final `available` = 0.)*

> [!note] Why this works completely
> **The value is never held in the application.** The database reads and writes it inside one statement, under one lock — **there is no window for another transaction to slip into.**
>
> **This is the right fix whenever the new value is a function of the old one**: counters, balances, stock levels, vote tallies. **Prefer `SET x = x - 1` to `SET x = <value I computed>` always** — the second form is a lost update waiting to happen.
>
> **The `AND available > 0` guard matters too**: it makes the statement refuse to oversell rather than relying on the `CHECK` to raise an error.

### 6. Fix 2 — optimistic locking with a version column

**When the update is not a simple arithmetic function of the old value**, carry a version:

```sql
SELECT qty, version FROM inventory WHERE item = 'widget';   -- read version 7
-- ... arbitrary application logic ...
UPDATE inventory SET qty = ?, version = version + 1
WHERE item = 'widget' AND version = 7;                      -- only if still 7
```

**If another transaction has changed the row, `version` is no longer 7, `rowcount` is 0, and the write is refused — so you re-read and retry.**

*(Verified: 100 successful decrements, **14 retries**, 0 lost updates, final `qty` = 0 and `version` = 101.)*

> [!note] Optimistic versus pessimistic
> **Optimistic locking assumes conflicts are rare**: proceed, and detect the collision at write time. **The 14 retries out of 100 are the collisions being caught** — each one is a lost update that did *not* happen.
>
> **Pessimistic locking** (`SELECT … FOR UPDATE`) takes the lock at read time and holds it. **It prevents the conflict rather than detecting it**, at the cost of holding a lock across the whole think-time — which is exactly what §4's 51 `database is locked` errors cost.
>
> **Optimistic suits low contention and long think-times (web applications); pessimistic suits high contention and short transactions.** *(SQLite has no `SELECT … FOR UPDATE`; `BEGIN IMMEDIATE` takes a write lock immediately, which is the closest equivalent.)*

### 7. Isolation — what SQLite actually provides

*(Verified:)*
```
Connection A: BEGIN; UPDATE account SET balance = 9999 ...   (uncommitted)
Connection B: SELECT balance ...  ->  1000.0                 <- the OLD value
```
**No dirty read** — B cannot see A's uncommitted work.

```
Connection B: BEGIN IMMEDIATE; UPDATE account ...  ->  database is locked
```

> [!warning] SQLite's isolation is strong and its concurrency is poor
> **SQLite gives `SERIALIZABLE` by default**, implemented with a **whole-database write lock**: many readers *or* one writer, never both.
>
> **That is genuinely strong isolation** — none of §3's problems can occur within transactions. **But the granularity is the entire database**, so any two concurrent writers conflict even on unrelated tables. **This is the first SQLite behaviour in this subject that is *stricter* than PostgreSQL's**, rather than more permissive.
>
> **PostgreSQL and MySQL use row-level locking and MVCC**, so writers conflict only on the same rows.

### 8. The isolation levels

| level | dirty read | non-repeatable read | phantom |
|---|---|---|---|
| **READ UNCOMMITTED** | **yes** | yes | yes |
| **READ COMMITTED** | no | **yes** | yes |
| **REPEATABLE READ** | no | no | **yes** |
| **SERIALIZABLE** | no | no | no |

- **Dirty read** — reading another transaction's **uncommitted** data, which may be rolled back.
- **Non-repeatable read** — re-reading a **row** and getting a different value.
- **Phantom read** — re-running a **query** and getting different **rows** (someone inserted).

**Defaults differ and matter:** **PostgreSQL → `READ COMMITTED`**, **MySQL/InnoDB → `REPEATABLE READ`**, **SQLite → `SERIALIZABLE` only**.

> [!warning] The table does not include "lost update", and that is the point
> **§4's bug appears nowhere in it**, because the levels describe what a transaction may *observe*, not what happens *between* transactions.
>
> **Choosing a stricter isolation level does not fix a lost update caused by an application-level read-modify-write.** Only §5's atomic statement or §6's version check does.
>
> **This is the single most useful thing to take from the chapter**, because the instinct on discovering a concurrency bug is to raise the isolation level — and here that is wasted effort with a real throughput cost.

### 9. Deadlock, and WAL mode

**Deadlock:** T1 holds A and wants B; T2 holds B and wants A. Neither can proceed. **DBMSs detect it with a wait-for graph** — a cycle means deadlock ([[Data Structures and Algorithms/contents/13 - Graph Algorithms|DSA ch. 13]]'s cycle detection) — and **abort one transaction as the victim.**

**Prevention: acquire locks in a consistent order** (always the lower account id first), and **keep transactions short.**

*(SQLite avoids deadlock structurally by taking a single database-wide lock — hence the `database is locked` errors instead. Application code must be prepared to retry.)*

**WAL mode** changes the concurrency picture *(verified)*:
```
PRAGMA journal_mode = WAL;   ->  wal
A: BEGIN IMMEDIATE; UPDATE ...  (uncommitted 777)
B: SELECT ...  ->  500.0        <- NOT blocked, sees the old value
```
**Readers no longer block the writer, nor the writer readers** — the writer appends to a log while readers continue against the previous state. **This is MVCC in miniature**, and it is why WAL is the right default for any SQLite database with concurrent access.

## ✏️ Exercises

**1. (ACID.)** (a) Define the four properties and say where each comes from. (b) What did the atomicity demonstration show? (c) Why is consistency the designer's property? (d) How are atomicity and durability implemented together?

> [!example]- Solution
> **(a)** **Atomicity** — all or nothing. **Consistency** — the database moves between valid states only. **Isolation** — concurrent transactions do not see each other's partial work. **Durability** — a committed change survives failure.
>
> **Their sources differ, which is the useful observation.** **Atomicity and durability come from the log** (§(d)). **Consistency comes from *your constraints*** — the DBMS enforces what you declared and nothing more. **Isolation comes from concurrency control** and is the only one with a tunable cost (§8).
>
> **(b) That partial work is genuinely undone.** *(Verified:)* the debit took Alice from 1000 to 800, the credit failed on a `CHECK`, and after `ROLLBACK` both balances were back to 1000 and 500.
>
> **The mid-transaction reading is the important line.** The database really was in the inconsistent state — 200 had left Alice and arrived nowhere. **Atomicity does not prevent the inconsistent intermediate state; it guarantees the state is never *committed* and never visible to others** (which is isolation's half of the job).
>
> **(c) Because the DBMS can only enforce constraints that were declared.**
>
> Atomicity, isolation and durability are properties the engine provides whatever you do. **Consistency is different: "valid" is defined entirely by your `CHECK`s, keys and foreign keys.** A schema declaring nothing has a trivially satisfied consistency property and permits any garbage.
>
> **[[07 - Database Design|Ch. 07]]'s audit is exactly the measurement of how much consistency you actually get** — 6 of 10 rules there. **The other four are not enforced by the "C" in ACID**, because they were never expressed in a form the engine could check.
>
> **So ACID's consistency guarantee is conditional**: *if* your constraints capture what validity means, the DBMS will maintain it. That is a much weaker promise than it sounds.
>
> **(d) Both come from writing intentions down before acting.**
>
> The DBMS records each change in a **log** (a write-ahead log or rollback journal) **before** applying it to the data pages.
>
> - **Atomicity (undo):** if the transaction aborts or the system crashes mid-transaction, the log holds the previous values and the changes are rolled back. *(This is what restored Alice's 1000.)*
> - **Durability (redo):** at `COMMIT` the log record is forced to disk. If the machine dies before the data pages are written, recovery **replays** the log. *(Verified: the committed 1234 survived closing the file.)*
>
> **The commit point is when the log record reaches durable storage** — not when the data is written, which may happen much later. **That is why commits are fast and why durability survives a crash between commit and data write.**
>
> **The design insight is that undo and redo are the same mechanism read in two directions**, which is why one log delivers two of the four properties.

**2. (Hard — the lost update.)** (a) Explain the mechanism and the numbers. (b) Why did no error occur? (c) Why does no isolation level fix it? (d) What did the earlier version, with 51 rejected bookings, show?

> [!example]- Solution
> **(a) Many threads read the same value, each computes a decrement from it, and the last write wins.**
>
> Five threads execute `SELECT available` → compute `available - 1` → `UPDATE … SET available = <computed>`. **Because the read is not inside the writing transaction, several threads read 100, all compute 99, and all write 99.**
>
> *(Verified: **100 bookings committed, 20 seats consumed, 80 sold twice.**)*
>
> **The ratio is roughly the thread count**, which makes sense: with five threads interleaving, about four in five writes are overwriting a value another thread had already decremented. **Each such write silently discards the other's work.**
>
> **(b) Because nothing invalid happened.**
>
> Every statement was legal. Every transaction committed. **`available` never went negative**, so no `CHECK` fired. Every individual transaction was internally consistent — it read a value and wrote that value minus one.
>
> **The error is not in any transaction but in the *relationship between* them**, and no per-transaction check can see that. **The database's job is to keep the data valid, and the data *was* valid — just wrong.**
>
> **This is the recurring shape of the worst bugs in this subject** — [[03 - Entity-Relationship Modelling|ch. 03]]'s fan trap, [[05 - SQL Fundamentals|ch. 05]]'s `NOT IN`, [[06 - Advanced SQL|ch. 06]]'s frame default. **Valid-looking operations, no error, wrong answer.** Here the consequence is 80 passengers with tickets for seats that do not exist.
>
> **(c) Because the read and the write are in different transactions, with an unbounded gap.**
>
> **Isolation levels govern what a transaction may *observe* while it runs.** §4's writing transaction observes nothing problematic — it opens, writes a number, and commits. **The damage was done before it began**, when a stale value was read in an earlier transaction.
>
> **There is no transaction spanning the read and the write for any isolation level to protect.** Setting `SERIALIZABLE` changes nothing, and the level table in §8 does not list "lost update" precisely because it is not an observation anomaly.
>
> **This matters because the instinct is exactly wrong.** On seeing a concurrency bug, the natural move is to raise the isolation level — **which here costs throughput and fixes nothing.** *(Some engines do detect a related case: PostgreSQL's `REPEATABLE READ` aborts a transaction that writes a row changed since its snapshot. But that only helps when the read *is* inside the transaction — it cannot help the read-in-request-1, write-in-request-2 pattern, which is the common one.)*
>
> **The fix must be at the application/statement level: §5's atomic update or §6's version check.**
>
> **(d) That preventing the anomaly and preserving throughput are in direct tension.**
>
> With the read placed *inside* the writing transaction, **SQLite prevented every lost update — by rejecting 51 of 100 bookings with `database is locked`.** *(Verified.)*
>
> **Correctness was bought by refusing half the work.** That is the isolation/concurrency trade in its rawest form, and it explains why serialisable isolation is not simply the default everywhere: **the cost is not latency, it is failed transactions that the application must retry.**
>
> **Two lessons.** **Retry logic is not optional** in any application using a database under contention — `database is locked` and serialisation failures are normal operating conditions, not bugs. **And the fix in §5 is strictly better than stronger isolation**, because it achieves correctness *without* the rejections: 100 committed, 100 consumed, 0 lost.

**3. (The fixes.)** (a) Why does the atomic statement work completely? (b) Explain optimistic locking and the 14 retries. (c) Optimistic vs pessimistic? (d) Which fix when?

> [!example]- Solution
> **(a) Because the value is never held outside the database.**
>
> ```sql
> UPDATE seats SET available = available - 1 WHERE flight='VN123' AND available > 0;
> ```
> **The engine reads and writes within one statement, under one lock.** There is no interval in which another transaction can read a value this one is about to invalidate — **the window that §4 exploited does not exist.**
>
> *(Verified: 100 committed, 100 consumed, 0 lost, and no rejections.)*
>
> **The general rule: prefer `SET x = x - 1` over `SET x = <a value I computed>`.** The second form always contains a lost-update window; the first cannot.
>
> **The `AND available > 0` guard is worth noting separately.** It makes the statement *decline* to oversell — updating zero rows, which the application can detect — rather than relying on a `CHECK` to raise an error. **A refused update is easier to handle than an exception.**
>
> **(b) Read a version, and make the write conditional on the version not having changed.**
>
> ```sql
> UPDATE inventory SET qty = ?, version = version + 1
> WHERE item = 'widget' AND version = <the version I read>;
> ```
> **If someone else has written, `version` has advanced, the `WHERE` matches nothing, and `rowcount` is 0 — the write is refused rather than silently overwriting.** The application re-reads and retries.
>
> *(Verified: 100 successful decrements, **14 retries**, 0 lost updates, final `version` = 101 — one increment per successful write, confirming none was lost.)*
>
> **The 14 retries are the collisions being caught.** Each is a lost update that would have occurred under §4's code and did not. **The retry count is a direct measure of contention**, which makes it worth logging in production.
>
> **The final version of 101 is the strongest evidence**: starting at 1 with exactly 100 successful increments, any lost update would have left it lower.
>
> **(c)**
>
> | | optimistic | pessimistic |
> |---|---|---|
> | assumes | conflicts are **rare** | conflicts are **likely** |
> | mechanism | version check at write | lock at read (`SELECT … FOR UPDATE`) |
> | conflict is | **detected**, then retried | **prevented** by waiting |
> | cost | wasted work on retry | **lock held across think-time** |
> | suits | web apps, long think-times | short transactions, high contention |
>
> **The deciding factor is how long the gap between read and write is.** In a web application it spans a user's thinking — seconds or minutes — and holding a lock that long is unacceptable: it is precisely what produced §4's 51 rejections. **Optimistic locking holds no lock at all during that gap.**
>
> **Where contention is high, optimistic degrades badly** — retries pile up and the same work is repeated. **Then pessimistic wins**, provided transactions are short enough for the lock to be brief.
>
> **(d)**
> - **New value is an arithmetic function of the old** (counter, balance, stock) → **§5's atomic statement.** Simplest, no retries, no extra column.
> - **New value depends on application logic** the database cannot express, or on multiple rows → **§6's version column.**
> - **Short transaction, high contention, and you can hold a lock** → pessimistic `SELECT … FOR UPDATE`.
> - **Genuinely need the whole read-compute-write inside one transaction** → serialisable isolation *and* retry logic, accepting the rejections.
>
> **Try them in that order.** §5 is free and total when it applies; §6 costs a column and some retry code; locking costs throughput. **Raising the isolation level is not on this list, because §2(c) showed it does not solve the problem.**

**4. (Isolation and engines.)** (a) Define the three read anomalies. (b) Why does the level table omit "lost update"? (c) What is SQLite's isolation, and how is it unusual here? (d) What does WAL change?

> [!example]- Solution
> **(a)** **Dirty read** — reading data another transaction has written but **not committed**; if that transaction rolls back, you acted on a value that never existed. **Non-repeatable read** — re-reading the **same row** within one transaction and getting a **different value**, because another transaction committed an update in between. **Phantom read** — re-running the **same query** and getting **different rows**, because another transaction inserted or deleted.
>
> **The progression is by scope**: dirty reads concern *uncommitted* data, non-repeatable reads concern *a row's value*, phantoms concern *which rows exist*. **Each level blocks one more**, and each costs more concurrency.
>
> *(Verified that SQLite blocks dirty reads: connection B read 1000.0 while A held an uncommitted 9999.)*
>
> **(b) Because the levels describe what a transaction may *observe*, and a lost update is not an observation.**
>
> All three anomalies are about a transaction **reading** something it should not. **A lost update is about a *write* destroying another write** — and in §4 the two are in different transactions with a gap between, so no transaction observed anything wrong.
>
> **The omission is not an oversight in the standard; it is a statement about scope.** Isolation levels cannot address anomalies that occur between transactions rather than within one.
>
> **The practical consequence is the chapter's most useful takeaway:** on finding a concurrency bug, **determine first whether the read and write are in the same transaction.** If not, the isolation level is irrelevant and only §5 or §6 will help. **Raising it is a costly no-op** — and, worse, it can appear to help by slowing everything down enough that collisions become rare, which hides the bug rather than fixing it.
>
> **(c) SQLite provides `SERIALIZABLE` only, via a whole-database write lock.**
>
> *(Verified: no dirty read; and connection B's concurrent write attempt gave `database is locked`.)*
>
> **It is unusual in this subject because it is *stricter* than the alternatives.** [[01 - Databases and Data Models|Ch. 01]], [[02 - The Relational Model and Relational Algebra|ch. 02]] and [[05 - SQL Fundamentals|ch. 05]] found four cases where SQLite is **more permissive** than PostgreSQL — foreign keys off by default, nulls in primary keys, aliases in `WHERE`, bare columns with aggregates. **Here it is the opposite.**
>
> **But strictness is not free: the lock granularity is the entire database file**, so two writers conflict even on unrelated tables. **PostgreSQL and MySQL use row-level locking with MVCC**, so writers conflict only on the same rows — much better concurrency, at the cost of a weaker default level (`READ COMMITTED` / `REPEATABLE READ`).
>
> **The trade is explicit: SQLite chooses the strongest isolation and the worst concurrency**, which suits its intended use — embedded, mostly single-writer. **It also means concurrency behaviour learned in SQLite does not transfer**, in either direction: code that works there may hit anomalies on PostgreSQL's `READ COMMITTED`, and code that works on PostgreSQL may hit `database is locked` on SQLite.
>
> **(d) WAL lets readers and a writer proceed simultaneously.**
>
> *(Verified: with `journal_mode = WAL`, connection B read successfully — returning the old value, 500.0 — while A held an uncommitted write. Without WAL, B would have blocked or errored.)*
>
> **The mechanism:** the writer appends changes to a separate write-ahead log rather than modifying the database file in place, so readers continue against the last committed state undisturbed. **Readers no longer block the writer, and the writer no longer blocks readers** — though there is still **only one writer at a time.**
>
> **This is MVCC in miniature** — the same idea PostgreSQL uses generally: keep old versions available so readers never need to wait.
>
> **Practically: enable WAL for any SQLite database with concurrent access.** It converts the commonest source of `database is locked` (a reader colliding with a writer) into no contention at all. **The remaining writer-writer contention still requires retry logic.** *(The costs: extra `-wal` and `-shm` files, and it does not work well on network filesystems.)*

## 📝 Summary

- **A transaction is a logical unit of work that succeeds entirely or not at all.**
- **ACID, all verified:** **atomicity** *(a failed transfer's debit was undone)*, **consistency** *(a negative balance was rejected)*, **isolation** *(§7)*, **durability** *(a commit survived reopening the file)*.
- **The properties have different sources:** atomicity and durability from the log (undo and redo are one mechanism read two ways); **consistency from *your* constraints** — so [[07 - Database Design|ch. 07]]'s 6-of-10 audit is the real measure of it; isolation from concurrency control.
- **⚠️ The lost update, produced for real: 100 bookings committed, 20 seats consumed, 80 sold twice** *(verified, 5 threads)*. **No error, no warning, no constraint violated** — the data stayed valid and was wrong.
- **⚠️ No isolation level prevents it**, because the read and write are in **different transactions** with a gap. The level table describes what a transaction may *observe*; this is a write destroying a write. **Raising the isolation level is a costly no-op.**
- **An earlier variant with the read inside the transaction had zero lost updates — and rejected 51 of 100 bookings** with `database is locked`. **Correctness bought by refusing half the work**: the isolation/throughput trade, exactly.
- **Fix 1 — the atomic statement:** `SET available = available - 1`. *(Verified: 100 committed, 100 consumed, 0 lost, no rejections.)* **The value is never held in the application, so no window exists.** Always prefer this to `SET x = <computed value>`.
- **Fix 2 — optimistic locking:** `UPDATE … WHERE version = <version I read>`. *(Verified: 100 successes, **14 retries**, 0 lost, final version 101 — one increment per success proves none was lost.)* **The retries are the collisions being caught.**
- **Optimistic suits long think-times and low contention; pessimistic (`SELECT … FOR UPDATE`) suits short, high-contention transactions.**
- **The three read anomalies** — dirty read (uncommitted data), non-repeatable read (a row's value changes), phantom (which rows exist changes) — **are blocked progressively by READ UNCOMMITTED → READ COMMITTED → REPEATABLE READ → SERIALIZABLE.**
- **Defaults differ: PostgreSQL `READ COMMITTED`, MySQL `REPEATABLE READ`, SQLite `SERIALIZABLE` only.**
- **⚠️ SQLite is *stricter* here than PostgreSQL** — the first such case in this subject, after four permissivenesses — **but its lock is the whole database**, so unrelated writers conflict.
- **Deadlock is a cycle in the wait-for graph**; engines detect it and abort a victim. Prevent by locking in a consistent order and keeping transactions short.
- **WAL mode lets readers and a writer run concurrently** *(verified: B read while A held an uncommitted write)* — MVCC in miniature, and the right default for concurrent SQLite.

## ⚠️ Important Notes

1. **Wrap multi-statement changes in a transaction.** A transfer that debits without crediting is what atomicity exists to prevent.
2. **ACID's "consistency" only enforces what you declared.** It is as strong as [[07 - Database Design|ch. 07]]'s audit says it is, and no stronger.
3. **⚠️ Never write `SET x = <value I read earlier>`.** That is a lost update waiting to happen. Use `SET x = x - 1`.
4. **⚠️ On a concurrency bug, first ask whether the read and write are in the same transaction.** If not, the isolation level is irrelevant — no level can fix it.
5. **Raising the isolation level can *hide* a lost update** by slowing things enough that collisions become rare. That is worse than not fixing it.
6. **Guard decrements with `AND qty > 0`** so the statement declines rather than raising an error. A zero row count is easier to handle than an exception.
7. **Use a version column when the new value is not a simple function of the old.** Check `rowcount` — 0 means someone else won, so re-read and retry.
8. **Log the retry count.** It is a direct, free measure of contention.
9. **Retry logic is not optional.** `database is locked` and serialisation failures are normal operating conditions under contention.
10. **Keep transactions short.** Long transactions hold locks, cause deadlocks and multiply rejections. **Never hold a transaction open across user think-time.**
11. **Acquire locks in a consistent order** (always the lower id first) to prevent deadlock cycles.
12. **Enable `PRAGMA journal_mode = WAL`** for any SQLite database with concurrent access — it removes reader/writer contention entirely.
13. **⚠️ Concurrency behaviour does not transfer between engines.** SQLite's whole-database lock and PostgreSQL's row-level MVCC produce different failures in both directions. Test on the target engine.
14. **Beware autocommit.** Many clients commit each statement, so a "transaction" spanning several statements never existed ([[05 - SQL Fundamentals|ch. 05]] §8).
15. **A committed change is durable at the moment the *log record* reaches disk**, not when the data pages are written — which is why commits are fast and survive a crash immediately after.

> [!warning] Gaps in the source material
> **Coronel & Morris ch. 10 extracts cleanly** — the transaction definition, ACID, the three concurrency problems, locking granularity, two-phase locking, deadlock handling, time-stamping and optimistic methods, and the isolation levels all came through readably. **Book page $n$ = PDF page $n+28$; ch. 10 is PDF pages 501–537.**
>
> **All figures are images and are lost**, including the interleaved-schedule tables that are this chapter's principal teaching device — C&M shows each concurrency problem as a two-column trace of T1 and T2 operations over time. **That loss is largely compensated here by *running* the concurrency instead of tabulating it**, which is stronger evidence than a hand-drawn schedule: §4's 80 double-sold seats were produced by real threads, not by a diagram.
>
> **The entire worked scenario is my own** — the `account`, `seats` and `inventory` schemas, the threading harness, and all three concurrency experiments.
>
> **No error was found in Coronel & Morris ch. 10.**
>
> **Additions beyond the source.** **§4 — actually producing a lost update — is mine, and is the chapter's reason for existing.** C&M *describes* the lost update with a schedule table; **executing it with five threads and reporting "100 bookings committed, 20 seats consumed, 80 sold twice" makes it concrete in a way a table cannot.**
>
> **The most important addition is the insistence that no isolation level fixes it** (§4, §8, Exercise 2(c), Exercise 4(b)). **C&M presents the isolation-level table and the lost-update problem in the same chapter without stating that the table does not address it** — which is precisely the misconception that leads engineers to raise the isolation level and change nothing. Stating why (the anomaly is between transactions, not within one) is my own framing.
>
> **§§5–6, the two fixes, are additions** — C&M covers locking and optimistic methods at the level of DBMS internals, not as application patterns. **The verified results (0 lost updates in both, with 14 retries under optimistic locking, and a final version of 101 proving no write was lost) are mine.** **The earlier experimental variant that rejected 51 of 100 bookings is reported rather than discarded**, because it demonstrates the isolation/throughput trade better than any description.
>
> **§9's WAL demonstration is mine and is not in C&M** (which predates none of it, but treats concurrency generically rather than per-engine). **The observation that SQLite is *stricter* here than PostgreSQL — the first such case after four permissivenesses in earlier chapters — is my own running finding.**
>
> **Deliberately compressed.** **Two-phase locking's growing/shrinking phases and the lock-compatibility matrix (C&M §10-3)** are summarised rather than reproduced — they are DBMS-internal mechanisms, and this note's audience uses the guarantees rather than implementing them. **Time-stamping and the wait/die and wound/wait schemes (§10-4)** are omitted for the same reason; optimistic concurrency is covered instead, as §6, because it is the one an application programmer actually writes. **Database recovery management (§10-6)** — checkpoints, deferred and immediate write, the recovery procedure — is reduced to the log discussion in §2 and Exercise 1(d); the full recovery algorithm is operating-systems material. **`SELECT … FOR UPDATE` is described but not demonstrated**, since SQLite does not support it — flagged rather than presented as if verified.

**Previous:** [[07 - Database Design]] · **Next:** [[09 - Query Optimization and Indexing]]
