---
subject: Basic Programming (C++)
chapter: 2
tags: [ds, cpp, streams, cin, cout, file-io, getline, manipulators, error-handling]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 3"
---

# Input and Output

**A C++ stream does not throw when a read fails. It sets a flag and carries on.**

That single design decision generates every trap in this chapter, and it is [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]'s theme applied to I/O: **the program keeps running and computes a plausible wrong answer.** §2 shows a stream that silently ignores three perfectly good numbers after one bad token, and §7 shows a missing file being indistinguishable from an empty one.

**Every program below was compiled and run.** Input is supplied via `std::istringstream` rather than the keyboard, so the demonstrations are deterministic — the stream behaviour is identical.

## 📘 Main Knowledge

### 1. What a failed read does to your variable

```cpp
std::istringstream in("abc");
int x = 999;
in >> x;
```
```
x         = 0        <- was 999
in.fail() = true
```
*(Verified.)*

> [!warning] The value came from no input, and nothing was raised
> **Since C++11 a failed extraction writes `0` into the target.** Before C++11 it left the previous value untouched — **so the same code has changed behaviour across standards**, and older textbooks describe the old rule.
>
> **Either way you now hold a number that came from nowhere**, and `0` is a perfectly plausible reading for a quantity, a count or a price.
>
> **The only reliable signal is the stream's state**, and you have to ask for it: `in.fail()`, or simply test the stream.

### 2. ⚠️ Once a stream fails, every later read does nothing

```cpp
std::istringstream in("abc 10 20 30");
int a=-1, b=-1, c=-1, d=-1;
in >> a;              // fails on "abc"
in >> b >> c >> d;    // silently no-ops
```
```
a=0  b=-1  c=-1  d=-1
a total computed from these: -3
```
*(Verified.)*

**`10`, `20` and `30` were never read.** They are still sitting in the stream. **`b`, `c` and `d` kept their initial values** because the extractions did not execute at all — the stream was already in a fail state.

> [!note] This is the failure mode that defines the subject
> **No exception. No warning. No return value anyone checks.** The program produces `-3`, which looks like an ordinary number.
>
> **And it is *sticky*: one bad token disables the stream permanently** until you clear it. In a program reading a thousand records, a single malformed field at record 3 means records 4–1000 are silently skipped and every total is wrong.
>
> **This is exactly [[Database Management Systems/contents/05 - SQL Fundamentals|DBMS ch. 05]]'s `NOT IN` trap in another language** — one bad element poisons everything downstream, and the result is well-formed and false.

### 3. Recovering: `clear()` *and* discard

```cpp
while (!(in >> v)) {
    in.clear();                        // reset the state flags
    std::string junk; in >> junk;      // *** consume the offending token ***
}
```
*(Verified: skipped `"abc"`, then read 3 numbers totalling **60** — correct.)*

> [!warning] `clear()` alone is an infinite loop
> **`clear()` resets the flags but does not consume the bad characters.** The next extraction meets the same `abc` and fails again, forever.
>
> **You must do both**: clear the state *and* remove the input that caused it — with `>>` into a `std::string`, or `in.ignore(n, '\n')` to discard a whole line.

### 4. The idiom that gets it right, and the one that does not

**Right — the extraction is the condition:**
```cpp
while (in >> v) { total += v; ++n; }
```
*(Verified: read 5 values, total 15.)* **A stream converts to `bool`: true while the last read succeeded.** The loop cannot process a value that was never read.

**⚠️ Wrong — looping on `eof()`:**
```cpp
while (!in.eof()) { in >> v; /* use v */ }
```
```
input "1 2 3\n", values seen:  1 2 3 3
-> 4 iterations for 3 values -- THE LAST VALUE WAS PROCESSED TWICE
```
*(Verified.)*

> [!warning] `eof()` is set *after* a read fails, not before
> After reading `3`, the trailing newline means end-of-file has not yet been *reached*, so `eof()` is still false and the loop body runs again. **That final `in >> v` fails, leaves `v` holding the previous value, and the body processes `3` a second time.**
>
> **The duplicate is the last element**, so totals are too high by one item and counts are off by one — **a small, plausible error**, which is why it survives testing. *(A trailing newline is what makes it fire, and every real text file has one.)*
>
> **Never loop on `eof()`. Loop on the read itself.**

### 5. `>>` versus `getline`

| | behaviour |
|---|---|
| `in >> s` | **skips leading whitespace**, reads one token, stops at whitespace |
| `std::getline(in, s)` | reads to the newline, **whitespace included**, and consumes the newline |

*(Verified: `"  Nguyen Van A  "` gives tokens `[Nguyen]` `[Van]` via `>>`, and `[Nguyen Van A]` via `getline`.)*

**⚠️ The classic bug is mixing them:**
```cpp
in >> age;                 // reads 42, LEAVES the '\n' in the stream
std::getline(in, name);    // reads the rest of that line: nothing
```
```
age = 42, name = []        <- EMPTY
```
*(Verified.)*

**The fix — discard the rest of the line first:**
```cpp
in >> age;
in.ignore(1000, '\n');
std::getline(in, name);    // name = [Nguyen Van A]     <- correct
```
*(Verified.)* *(`std::numeric_limits<std::streamsize>::max()` is the idiomatic first argument.)*

### 6. Formatting: which manipulators stick

*(Verified:)*
```
default        : 3.14159 2.71828
fixed, 3 dp    : 3.142 2.718
```

| manipulator | sticky? |
|---|---|
| `std::fixed`, `std::scientific` | **yes** — until changed |
| `std::setprecision(n)` | **yes** |
| `std::left`, `std::right` | **yes** |
| **`std::setw(n)`** | **NO — applies to the next item only** |

> [!note] `setw` not being sticky is the commonest formatting mistake
> It must be repeated for every field:
> ```cpp
> std::cout << std::left  << std::setw(10) << name
>           << std::right << std::setw(10) << value << "\n";
> ```
> *(Verified — a correctly aligned table.)*
>
> **And because `fixed`/`setprecision` *are* sticky, they leak into unrelated output later in the program.** Reset them (`std::cout.unsetf(std::ios::fixed)`) or save and restore the stream state.

### 7. File I/O — and the check everybody skips

```cpp
std::ofstream out("data.txt");
if (!out) { /* handle */ }
std::ifstream in("data.txt");
if (!in)  { /* handle */ }
while (in >> v) { total += v; ++n; }
```
*(Verified: wrote then read back 5 values totalling 150.)*

**⚠️ Now the same code against a file that does not exist:**
```
in.is_open() = false,  (bool)in = false
reading from it: got 0 values, no exception thrown
```
*(Verified.)*

> [!warning] "The file was empty" and "the file was missing" look identical
> **The loop runs zero times, the total is 0, and the program reports success.** No exception, no error code anyone looked at.
>
> **This is the same class of failure as §2** and as [[Database Management Systems/contents/02 - The Relational Model and Relational Algebra|DBMS ch. 02]]'s inner join silently dropping rows: **an empty result that is indistinguishable from a legitimately empty one.**
>
> **Always check the open**, and prefer distinguishing the cases explicitly — a missing input file is usually a fatal error, whereas an empty one may be legitimate.

## ✏️ Exercises

**1. (Stream state.)** (a) What happens to the variable on a failed read? (b) Why is the failure sticky, and why does that matter? (c) How do you recover? (d) Why is `while (in >> v)` better than `while (!in.eof())`?

> [!example]- Solution
> **(a) Since C++11, a failed extraction writes `0` into the target.** *(Verified: `x` went from 999 to 0.)* **Before C++11 it left the previous value untouched** — so the same code behaves differently across standards, and older textbooks (including Malik's era) describe the old rule.
>
> **Neither behaviour is safe.** Under the old rule an uninitialised variable keeps garbage; under the new one you get `0`, **which is a perfectly plausible value for a count, a quantity or a price.** In both cases **the number came from no input at all** and nothing was raised.
>
> **The only reliable signal is the stream's state**, which you must ask for — `in.fail()`, or just test the stream.
>
> **(b) Because a stream that has failed refuses all further extractions until cleared.**
>
> *(Verified: after `>> a` failed on `"abc"`, the subsequent `>> b >> c >> d` did nothing at all — `b`, `c`, `d` kept their initial `-1`, and `10 20 30` were never read.)*
>
> **The scaling consequence is what matters.** In a program reading a thousand records, **one malformed field at record 3 silently skips records 4–1000.** The program terminates normally and reports a total computed from two records.
>
> **And the output is plausible.** *(Verified: the total came out as `-3` — an ordinary-looking number.)* **Nothing distinguishes "the file had two records" from "the file had a thousand and we stopped reading".**
>
> **This is [[Database Management Systems/contents/05 - SQL Fundamentals|DBMS ch. 05]]'s `NOT IN` trap in another language**: one bad element poisons everything downstream, and the result is well-formed and false.
>
> **(c) `clear()` the state *and* consume the offending input.**
> ```cpp
> in.clear();
> std::string junk; in >> junk;         // or in.ignore(n, '\n')
> ```
> *(Verified: skipping `"abc"` then reading gave the correct total of 60.)*
>
> **⚠️ `clear()` alone is an infinite loop.** It resets the flags but leaves the bad characters in the buffer, so the next extraction meets the same `abc` and fails again. **Both steps are required, and forgetting the second turns a data error into a hang.**
>
> **How much to discard is a design decision.** `>> junk` removes one token — right when a single field is malformed. `ignore(n, '\n')` removes the rest of the line — right when a whole record is unusable, and usually the better default for line-oriented data.
>
> **(d) Because the extraction's success is exactly the condition you want to loop on.**
>
> `while (in >> v)` uses the stream's conversion to `bool` — true while the last read **succeeded**. **The body can never run on a value that was not read.** *(Verified: 5 values, total 15.)*
>
> **`while (!in.eof())` tests the wrong thing at the wrong time.** *(Verified with input `"1 2 3\n"`:)*
> ```
> values seen: 1 2 3 3        -> 4 iterations for 3 values
> ```
> **After reading `3` the trailing newline means EOF has not yet been *reached***, so `eof()` is false, the body runs once more, the extraction fails, `v` keeps its previous value — **and `3` is processed twice.**
>
> **Three reasons this bug survives:**
> 1. **The error is small** — one duplicate at the end. A total is high by one item; a count is off by one.
> 2. **It depends on the trailing newline**, which every real text file has but a hand-typed test string may not. *(My own first attempt used `"1 2 3"` with no newline and the bug did **not** appear — 3 iterations. Adding the newline made it fire.)*
> 3. **`eof()` sounds like the right question.** It is a perfectly reasonable thing to write.
>
> **The rule: never loop on `eof()`, `good()` or `bad()`. Loop on the operation.**

**2. (Reading text, and files.)** (a) `>>` vs `getline`? (b) Explain the mixing bug and its fix. (c) What happens when a file is missing? (d) What is the general principle?

> [!example]- Solution
> **(a) `>>` reads *tokens*; `getline` reads *lines*.**
>
> **`>>` skips leading whitespace, reads until the next whitespace, and leaves that whitespace in the stream.** **`getline` reads everything to the next newline — spaces included — and consumes the newline.**
>
> *(Verified on `"  Nguyen Van A  "`: `>>` gave `[Nguyen]` and `[Van]`; `getline` gave `[Nguyen Van A]`.)*
>
> **So `>>` cannot read a name with a space in it**, which is the usual reason to reach for `getline`.
>
> **(b) `>>` leaves the newline behind, and `getline` then reads the empty remainder of that line.**
> ```cpp
> in >> age;                 // consumes "42", leaves '\n'
> std::getline(in, name);    // reads from '\n' to '\n' -> ""
> ```
> *(Verified: `age = 42, name = []`.)*
>
> **`getline` did exactly what it promises** — it read to the end of the current line, and there was nothing left on it. **The bug is in the mixing, not in `getline`.**
>
> **The fix is to discard the rest of the line before switching:**
> ```cpp
> in >> age;
> in.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
> std::getline(in, name);      // [Nguyen Van A]
> ```
> *(Verified.)* **`ignore(n, ch)` discards up to `n` characters or until `ch`, whichever comes first** — and it consumes the delimiter, which is the point.
>
> **The wider rule: do not mix `>>` and `getline` on one stream unless you handle the boundary explicitly.** Reading whole lines with `getline` and parsing each with an `istringstream` avoids the problem entirely and is usually cleaner for record-structured input.
>
> **(c) Nothing visible. The read loop runs zero times.**
> ```
> in.is_open() = false,  (bool)in = false
> got 0 values, no exception thrown
> ```
> *(Verified.)*
>
> **The stream is created in a fail state and every extraction is a no-op** — §2's stickiness, from the very first operation. **The program computes a total of 0 and exits successfully.**
>
> **The damage is that "the file was missing" and "the file was empty" are indistinguishable** without the check. One is a deployment error worth failing loudly on; the other may be perfectly normal.
>
> **`if (!in)` is one line and catches it.** *(And note `is_open()` and the boolean conversion are not identical: `is_open()` asks whether a file is attached, while `(bool)in` asks whether the stream is in a good state — a stream can be open and failed.)*
>
> **(d) In C++ I/O, absence of error is not evidence of success — you must ask.**
>
> **Every failure in this chapter shares one shape**: the operation fails, sets a flag, returns, and **the program continues with data that is wrong or missing.** Nothing propagates. Nothing raises.
>
> **This is the deliberate design.** Streams are used in performance-sensitive and embedded contexts where exceptions may be unavailable or unwanted, so the default is to record and continue. *(You can opt in with `in.exceptions(std::ios::failbit)`, which makes failures throw — rarely used, but exactly right when any I/O failure is fatal.)*
>
> **The practical discipline:**
> 1. **Check every file open.**
> 2. **Loop on the read, never on `eof()`.**
> 3. **Check the read count against what you expected** — the reconciliation habit from [[Database Management Systems/contents/10 - Data Warehouses and OLAP|DBMS ch. 10]]: a total that must match is the cheapest invariant to assert.
> 4. **Decide what a malformed record means** — skip it, or abort — and write that decision down.
>
> **The connecting theme across this vault is now unmistakable.** [[Data Structures and Algorithms/contents/00-Index|DSA]] logged five measurements that misled; [[Database Management Systems/contents/00-Index|DBMS]] logged five silent wrong answers; [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] found a factorial that stops being right at 13. **In every case the system did what it was told and the result was plausible and false. Checking is not pedantry — it is the only defence available.**

## 📝 Summary

- **A failed stream read sets a flag and carries on.** It does not throw.
- **Since C++11 a failed extraction writes `0` to the target** *(verified: 999 → 0)*; **before C++11 it left the old value.** Either way the value came from no input, and `0` is plausible.
- **⚠️ Failure is sticky: every later read is a silent no-op.** *(Verified: after one bad token, `10 20 30` were never read and the computed total was `-3`.)* **One malformed field can silently skip the rest of a file.**
- **Recovery needs `clear()` *and* discarding the bad input.** *(Verified.)* **`clear()` alone loops forever** on the same characters.
- **Loop on the read: `while (in >> v)`** *(verified: 5 values, total 15)*.
- **⚠️ Never loop on `eof()`.** *(Verified with a trailing newline: `1 2 3 3` — **4 iterations for 3 values, the last processed twice**.)* `eof()` is set only *after* a read fails.
- **The bug depends on the trailing newline** that every real file has — my first attempt without one did not reproduce it.
- **`>>` reads tokens and skips whitespace; `getline` reads a whole line** *(verified)*.
- **⚠️ Mixing them leaves a newline behind**, so `getline` after `>>` returns empty *(verified)*. Fix with `in.ignore(max, '\n')`.
- **`fixed`, `setprecision`, `left`/`right` are sticky; `setw` applies to one item only** *(verified)* — the commonest formatting mistake, and sticky flags leak into later output.
- **⚠️ Opening a missing file throws nothing**: `is_open()` is false, the read loop runs **zero** times, and the total is 0 *(verified)*. **"Missing" and "empty" are indistinguishable without the check.**
- **Absence of error is not evidence of success.** Check the open, loop on the read, and reconcile the count.

## ⚠️ Important Notes

1. **Always check a file open**: `if (!in) { … }`. It is one line and it separates "missing" from "empty".
2. **⚠️ Always loop on the extraction, never on `eof()`.** `while (in >> v)`, not `while (!in.eof())`.
3. **A failed stream stays failed.** After handling an error you must `clear()` *and* consume the offending input, or the next read fails identically.
4. **`clear()` without discarding is an infinite loop** — a data error becomes a hang.
5. **Initialise variables you read into.** A failed read leaves them with a value you did not choose.
6. **Check how many records you read against how many you expected.** The count is the cheapest invariant available.
7. **⚠️ Do not mix `>>` and `getline` without `ignore`.** Prefer reading whole lines and parsing each with an `istringstream`.
8. **`in.ignore(std::numeric_limits<std::streamsize>::max(), '\n')`** is the idiomatic line-discard; `ignore(1000, '\n')` is a guess that can be wrong.
9. **`setw` is not sticky — repeat it for every field.** `fixed` and `setprecision` *are*, and will leak into unrelated output later.
10. **Save and restore stream flags** if you change them in a function, or the caller inherits your formatting.
11. **`is_open()` and `(bool)stream` are different questions** — a stream can be open and in a fail state.
12. **Consider `in.exceptions(std::ios::failbit)`** when any I/O failure should be fatal; it converts the silent flag into a thrown exception.
13. **Decide explicitly what a malformed record means** — skip, default, or abort — and record the decision. Doing nothing means "skip silently".

> [!warning] Gaps in the source material
> **Malik ch. 3 extracts well** — the stream-operator descriptions, manipulator tables, and file-stream mechanics all came through readably, with code listings intact. **Book page $n$ = PDF page $n+50$; ch. 3 is PDF pages 173–236.** *(The standing quirk applies: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost.** Minor here — they are mostly screenshots of console sessions, and this note prints real program output instead.
>
> **All programs are my own.** Malik's examples read from the keyboard, which cannot be demonstrated deterministically; **`std::istringstream` was used instead**, and the stream behaviour is identical — the same `std::istream` interface and the same state machine.
>
> **No error was found in Malik ch. 3**, but see the note below on a behavioural change since the book's target standard.
>
> **Additions beyond the source.** **Malik covers streams as syntax — how to read, how to format, how to open a file. Every failure mode demonstrated here is an addition:**
>
> - **§§1–2, stream state and its stickiness, are mine.** Malik mentions `cin.clear()` in passing; **showing that one bad token causes three good numbers to be silently ignored, and that the resulting total is a plausible `-3`, is what makes the point.**
> - **§4's `eof()` bug is mine**, including the finding that **it only reproduces when the input has a trailing newline** — my first attempt used `"1 2 3"` and showed 3 iterations, i.e. no bug. **Adding the newline (as every real file has) produced `1 2 3 3`.** Reporting that dependency is more useful than the bug alone, because it explains why the bug survives testing.
> - **§7's missing-file demonstration is mine**, along with the observation that **"missing" and "empty" are indistinguishable** — which is the same shape as [[Database Management Systems/contents/02 - The Relational Model and Relational Algebra|DBMS ch. 02]]'s silently-dropped join rows.
> - **The sticky-versus-non-sticky manipulator distinction** is stated explicitly here; Malik lists manipulators without grouping them by that property, which is the one thing about them that causes bugs.
> - **The `exceptions(failbit)` opt-in, and `std::numeric_limits<std::streamsize>::max()` as the correct `ignore` argument**, are modern-practice additions per the subject file.
>
> **A behavioural change worth flagging.** **Malik targets C++11 at best, and pre-C++11 a failed extraction left the target variable unmodified; since C++11 it writes `0`.** *(Verified: `999` became `0`.)* **Descriptions written for the older rule are no longer accurate**, and this note gives both.
>
> **Deliberately compressed.** **Malik's full manipulator catalogue** (`setfill`, `showpoint`, `boolalpha`, `hex`/`oct`, and the parameterised-manipulator header rules) is reduced to §6's sticky/non-sticky table plus the examples used — the rest is reference material. **The `cin.get`/`cin.putback`/`peek` family** is omitted; `getline` plus `istringstream` covers the same needs more clearly. **Malik's input-failure section (§3-6)** is the basis of §§1–3 but is substantially rewritten around demonstrations. **File I/O is introduced here rather than deferred**, because `ifstream` and `cin` are the same interface and separating them would teach the state machine twice.

**Previous:** [[01 - Fundamentals - Types, Variables and Expressions]] · **Next:** [[03 - Selection]]
