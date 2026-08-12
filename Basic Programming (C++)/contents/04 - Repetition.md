---
subject: Basic Programming (C++)
chapter: 4
tags: [ds, cpp, loops, off-by-one, range-based-for, iterator-invalidation, undefined-behaviour]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 5"
---

# Repetition

**Loops are where an off-by-one stops being an inconvenience and becomes undefined behaviour.**

In Python, `v[len(v)]` raises `IndexError` and the program stops at the mistake. **In C++ it reads whatever bytes happen to follow the array and carries on** — §3 shows exactly that, returning a plausible-looking integer from memory the program does not own.

This chapter covers four failures that all pass compilation:

- **§2–3** — the classic `<=` off-by-one, and what it actually does.
- **§4** — a loop that never terminates because `0.1` is not representable, [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]'s floating-point problem promoted to an infinite loop.
- **§5** — a stray semicolon, which **`/W4` does not warn about** *(tested)*.
- **§8** — iterator invalidation, where growing a container while looping over it invalidates the loop itself.

**And §7 is the modern answer to most of them**: the range-based `for`, which has no index and so cannot be off by one.

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17 /W4`).

## 📘 Main Knowledge

### 1. The three loops

| | when |
|---|---|
| **`while`** | test first — **may run zero times** |
| **`do`–`while`** | body first — **always runs at least once** |
| **`for`** | init, test, update in one place — when the count is known |

*(Verified with `n = 0`: the `while` ran **0** times, the `do`–`while` ran **1**.)*

> [!note] `do`–`while` is right only when "at least once" is the requirement
> Re-prompting for input, or a menu that must display before the user can choose to quit. **Everywhere else it is a bug waiting for an empty input** — it processes one item from a container that may have none.

### 2. ⚠️ Off by one: `<` versus `<=`

*(Verified on a 5-element vector, valid indices 0–4:)*
```
for (i = 0; i <  v.size(); ++i)  ->  0 1 2 3 4      correct
for (i = 0; i <= v.size(); ++i)  ->  0 1 2 3 4 5    index 5 is OUT OF BOUNDS
```

> [!note] The half-open convention `[0, n)` is why `<` is almost always right
> With a half-open range, **the number of elements is exactly `end − begin`** — no `+1`, no `−1`. Ranges concatenate cleanly (`[0,k)` then `[k,n)`), and an empty range is `begin == end` rather than a special case.
>
> **`<=` is correct only when the upper bound is itself a valid value** — e.g. `for (int i = 1; i <= 10; ++i)` to count 1 through 10. **With sizes and indices it is a bug.**

### 3. ⚠️ What out-of-bounds actually does

*(Verified — undefined behaviour, so: this machine, this compiler, this run:)*
```
v[4]  (last valid) = 50
v[5]  (one past)   = 2015895667      <- garbage. No error. No crash.
v.at(5)            -> threw std::out_of_range: invalid vector subscript
```

> [!warning] `operator[]` does not check; `.at()` does
> **`v[5]` read whatever bytes follow the vector's buffer and the program continued.** The value looks like an ordinary integer — it could as easily have been a small plausible number that propagated into a total.
>
> **Python raises `IndexError` here.** C++ does not, and that is a deliberate trade: `operator[]` compiles to a single addressing instruction with no branch, which is why C++ container access costs what raw array access costs.
>
> **`.at()` is bounds-checked and throws** *(verified)*. **Use `.at()` while developing** and in any code path where an out-of-range index is possible; use `operator[]` in hot loops where you have already established the bound.
>
> **And note this is worse than a wrong value: it may read memory the program does not own**, which is the mechanism behind a large fraction of security vulnerabilities.

### 4. ⚠️ A loop that never terminates

```cpp
for (double x = 0.0; x != 1.0; x += 0.1)
```

*(Verified, with a guard added to stop it:)*
```
after 20 iterations x = 2.0000000000000004441
x == 1.0 ? false
```

**`x` skips straight past 1.0 without ever equalling it.** Accumulating ten inexact tenths does not land on exactly 1.0 — [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] §6, now controlling termination.

> [!note] The fix: count with an integer, derive the double
> ```cpp
> for (int i = 0; i < 10; ++i) { double t = i * 0.1; … }
> ```
> *(Verified: `i=8 → t=0.8`, `i=9 → t=0.9`.)*
>
> **The loop variable is exact and the floating-point value is computed fresh each time**, so errors do not accumulate. **Never use a floating-point loop counter**, and never test one with `!=` or `==`.

### 5. The stray semicolon

```cpp
for (int i = 0; i < 5; ++i);      // <- the ';' IS the loop body
{ ++count; }                       // an unrelated block, runs once
```
```
count = 1        <- expected 5
```
*(Verified.)*

**A lone `;` is a complete empty statement**, so it becomes the loop body. The braces that follow are just a block.

> [!warning] ⚠️ `/W4` does not warn about this — tested
> ```
> if (x == 1);            ->  warning C4390: empty controlled statement found
> for (int i…; …; …);     ->  (silent)
> while (j < 5);          ->  (silent)
> ```
> *(All three compiled at `/W4`.)*
>
> **MSVC warns for `if` and not for loops — and the loop case is the dangerous one.** `for(…);` silently does nothing; **`while (cond);` with an unchanging condition spins forever**, which is a hang rather than a wrong answer.
>
> **I originally wrote that `/W4` catches this. Testing showed it does not.** *(GCC and Clang have `-Wempty-body`, which covers `if` and `while` but is also not part of `-Wall`.)*
>
> **The defence is the same as [[03 - Selection|ch. 03]]'s: brace every loop body.** With `for (…) { }` the stray semicolon has nowhere to hide.

### 6. Modifying the loop variable inside the body

```cpp
for (int i = 0; i < 10; ++i) {
    if (i == 3) i = 1;         // resets -- the loop cannot progress
}
```
*(Verified: stopped only by an added guard, after 15 iterations.)*

> [!note] The condition still looks bounded
> **Nothing about `i < 10` suggests it may never be reached.** A reader checking the loop header sees a loop that clearly runs ten times.
>
> **Treat the loop variable as read-only inside the body.** If you need to skip or repeat, use `continue`, a nested condition, or a `while` loop where the update is deliberately explicit.

### 7. Range-based `for` — the modern default

*(Verified:)*
```cpp
for (std::string s : names)        // COPIES every element
for (const std::string& s : names) // no copy, read-only        <- default
for (std::string& s : names)       // no copy, can modify
```

> [!warning] `for (auto x : v)` copies every element
> **Silently.** For a `vector<string>` or a vector of large objects that is a real cost paid on every iteration, and nothing in the syntax suggests it.
>
> **Default to `for (const auto& x : v)`.** Use `auto&` when you need to modify *(verified: appending `"!"` to each name worked)*. Use plain `auto` only for cheap types where you *want* a copy.
>
> **And there is no index at all, so §2's off-by-one is impossible.** That is the strongest argument for it: it removes a whole bug class rather than making it less likely.

### 8. ⚠️ Iterator invalidation

```cpp
for (int x : v) v.push_back(x);      // UNDEFINED BEHAVIOUR
```

**Why:** `push_back` may **reallocate** the buffer, and the loop's iterators still point at the old memory.

*(Verified — a vector grown from capacity 3:)*
```
data() before growth: 000001E068EFA6E0
data() after  growth: 000001E068EF9F90
buffer moved? true    capacity now 28
```

> [!note] The buffer genuinely moved
> **Any pointer, reference or iterator taken before the growth now points at freed memory.** The range-based `for` holds exactly such iterators.
>
> **This is [[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis|DSA ch. 04]]'s geometric reallocation** — the same doubling that gives amortised $O(1)$ `append`, and the same one that produced the measured 5 084× latency spike. **The difference is the consequence:** in Python, appending while iterating is confusing; **in C++ it is undefined.**
>
> **Safe patterns:** index by position (`for (size_t i = 0; i < v.size(); ++i)` — `size()` is re-read each time); **`reserve()` first** so no reallocation occurs; or build a second vector and swap.

### 9. `break`, `continue`, and knowing when to stop using them

*(Verified: a linear search found 16 at index 3; summing evens with `continue` gave 70.)*

> [!note] Fine in a short loop, a problem in a long one
> **In a ten-line loop `break` and `continue` are clear.** In a fifty-line loop with three `break`s and two `continue`s, the exit conditions are scattered and no longer readable in one place.
>
> **Prefer a standard algorithm where one exists** — `std::find`, `std::count_if`, `std::any_of`. They say *what* is being computed rather than *how*, cannot be off by one, and are the C++ equivalent of [[Data Structures and Algorithms/contents/11 - Sorting and Selection|reaching for `sorted()` instead of hand-writing a sort]].

## ✏️ Exercises

**1. (Off-by-one and bounds.)** (a) Why is `<` almost always right? (b) What did `v[5]` do? (c) `operator[]` vs `.at()`? (d) Why is this worse than a wrong value?

> [!example]- Solution
> **(a) Because indices are a half-open range `[0, n)`.**
>
> *(Verified: `<` touched 0–4 on a 5-element vector; `<=` touched 0–5, and 5 is out of bounds.)*
>
> **Three properties make half-open ranges the right convention:**
> 1. **The count is exactly `end − begin`** — no `+1` or `−1` anywhere, which is where off-by-ones breed.
> 2. **Ranges concatenate**: `[0,k)` followed by `[k,n)` covers `[0,n)` with no gap and no overlap.
> 3. **Empty is `begin == end`**, not a special case — so an empty container needs no separate branch.
>
> **`<=` is correct only when the upper bound is itself a valid value**, e.g. `for (int i = 1; i <= 10; ++i)`. **With sizes and indices it is always wrong**, because `size()` is one past the last index.
>
> **(b) It read memory past the end of the buffer and the program continued.**
>
> *(Verified: `v[4]` = 50, `v[5]` = **2015895667** — no error, no crash.)*
>
> **This is undefined behaviour, so the value is meaningless** — it is whatever bytes happened to follow the allocation on this run. **It could as easily have been a small plausible number** that flowed into a total and was never noticed.
>
> **Python raises `IndexError` here**, stopping at the mistake. **C++ has no bounds information at that point at all** — `operator[]` is pointer arithmetic, and there is nothing to check against.
>
> **(c)**
>
> | | checks bounds | on failure | cost |
> |---|---|---|---|
> | `operator[]` | **no** | undefined behaviour | one addressing instruction |
> | `.at()` | **yes** | **throws `std::out_of_range`** *(verified)* | a comparison and branch |
>
> **The trade is deliberate.** `operator[]` exists so that `std::vector` costs exactly what a raw array costs — otherwise nobody would use the safe container in performance-sensitive code, which would be worse for safety overall.
>
> **Practically: use `.at()` when the index comes from outside** (user input, a file, a computation you have not bounded), and `operator[]` in loops where the bound is established by the loop itself. **Many projects use `.at()` everywhere in debug builds**, and MSVC's debug STL bounds-checks `operator[]` too.
>
> **(d) Because it may read memory the program does not own.**
>
> **A wrong value is a correctness bug. Reading out of bounds is a *memory safety* bug**, and the difference matters:
> - **It can read data from an unrelated object** — another variable, a password buffer, a pointer.
> - **Writing out of bounds can corrupt other objects or the heap's own metadata**, causing a crash arbitrarily far away, in code that is entirely correct.
> - **It is the mechanism behind a large fraction of security vulnerabilities** — buffer overflows are how attackers read secrets or hijack control flow.
>
> **And per [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]], UB means no constraints on behaviour at all** — so "it worked in testing" carries no information. The compiler is entitled to assume the access is in bounds and optimise on that basis.

**2. (Loops that do not do what they say.)** (a) Why does the floating-point loop not terminate? (b) What is the fix and why? (c) Explain the stray semicolon and the warning finding. (d) Why is modifying the loop variable dangerous?

> [!example]- Solution
> **(a) Because accumulating ten inexact tenths does not land on exactly 1.0.**
>
> *(Verified: after 20 iterations `x` = **2.0000000000000004441**, and `x == 1.0` was never true.)*
>
> **`0.1` is not representable in binary** ([[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] §6 measured it as 0.10000000000000000555). Adding it ten times accumulates ten roundings, and the result **steps over 1.0 without hitting it.**
>
> **`!=` demands exact equality**, so the loop never stops. **Without the guard it runs forever** — and note this is a *hang*, not a wrong answer: the program produces no output at all and looks like a deadlock rather than a numeric bug.
>
> **(b) Count with an integer and derive the floating-point value.**
> ```cpp
> for (int i = 0; i < 10; ++i) { double t = i * 0.1; … }
> ```
> *(Verified: `i=8 → 0.8`, `i=9 → 0.9`, terminating correctly.)*
>
> **Two reasons this is right:**
> 1. **The loop variable is exact**, so termination is exact and the iteration count is obvious from the header.
> 2. **The error does not accumulate.** `i * 0.1` is one rounding of a fresh computation; `x += 0.1` compounds a rounding every iteration. **After 1 000 steps the accumulated version has drifted a thousand times further.**
>
> **If you must use a floating-point condition, use `<` rather than `!=`** — `for (double x = 0.0; x < 1.0; x += 0.1)` terminates, though it may run 10 or 11 times depending on the accumulated error, which is its own bug.
>
> **(c) A lone `;` is a complete empty statement, so it becomes the loop body.**
>
> *(Verified: `for (int i = 0; i < 5; ++i); { ++count; }` left `count` at **1**, not 5.)* The braces are an ordinary block that runs once, and the indentation makes it look like the body — **the same "layout is not structure" problem as [[03 - Selection|ch. 03]]'s dangling `else`.**
>
> **⚠️ The finding I had to correct: `/W4` does not warn about this.** *(Tested by compiling each form:)*
>
> | | `/W4` |
> |---|---|
> | `if (x == 1);` | **C4390: empty controlled statement found** |
> | `for (…; …; …);` | **silent** |
> | `while (j < 5);` | **silent** |
>
> **I originally wrote that `/W4` flags it. It does not** — MSVC covers `if` and not loops.
>
> **And the loop case is the more dangerous one.** `for(…);` silently does nothing; **`while (cond);` with an unchanging condition spins forever.** *(GCC/Clang have `-Wempty-body`, which covers `if` and `while` but is not in `-Wall`.)*
>
> **So the tooling defence fails here, and the habit is the only one available: brace every loop body.** With `for (…) { … }` the semicolon has nowhere to hide.
>
> **This is a useful counterweight to [[03 - Selection|ch. 03]]'s conclusion.** There, raising the warning level fixed the problem. **Here it does not** — which is why "brace everything" is worth adopting as an unconditional habit rather than relying on the compiler.
>
> **(d) Because the loop header stops describing the loop.**
>
> *(Verified: `if (i == 3) i = 1;` inside a `for (int i = 0; i < 10; ++i)` prevented termination — it was stopped only by an added guard, after 15 iterations.)*
>
> **`i < 10` still reads as a bounded loop.** A reviewer scanning the header sees ten iterations; the non-termination is buried in the body, possibly dozens of lines away.
>
> **The general principle is that a `for` header is a *contract*** — it states the range and the progression in one place, and that is its entire value over a `while`. **Modifying the variable inside the body breaks the contract while leaving it on display.**
>
> **Treat the loop variable as read-only in the body.** To skip, use `continue`; to exit, use `break`; to control progression yourself, use a `while`, where the update is explicit and the reader expects to look for it.

**3. (Modern loops and containers.)** (a) What does range-based `for` fix? (b) Why does `auto` copy? (c) Explain iterator invalidation. (d) When should you not write a loop at all?

> [!example]- Solution
> **(a) It removes the index, and with it a whole bug class.**
>
> **§2's off-by-one is impossible** — there is no bound to get wrong. The signed/unsigned mismatch of [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] §4 disappears too, since there is no comparison against `size()`. **And §5's stray semicolon cannot silently produce an empty loop that appears to work**, because the body is where the work visibly is.
>
> **It also expresses intent**: "for each element" rather than "for each integer from 0 to size−1, used as an index".
>
> **It works on anything with `begin()`/`end()`** — vectors, arrays, strings, maps, and your own types.
>
> **(b) Because `for (auto x : v)` declares `x` as a value, and each iteration initialises it from the element.**
>
> *(Verified: by-value, by-const-reference and by-reference all iterate correctly; only `auto&` could modify.)*
>
> **The copy is silent and can be expensive.** For `vector<string>` it is a heap allocation and a character copy per iteration; for a large struct it is a full member-wise copy. **Nothing in the syntax hints at it** — `auto` looks like it should do the efficient thing.
>
> **The rule:**
>
> | form | use |
> |---|---|
> | **`for (const auto& x : v)`** | **default** — no copy, read-only |
> | `for (auto& x : v)` | when modifying elements |
> | `for (auto x : v)` | only for cheap types (`int`, `double`, pointers) where a copy is wanted |
>
> *(C++20 adds `for (auto&& x : v)` as a forwarding form, needed for proxy iterators like `vector<bool>`.)*
>
> **(c) Growing a container may move its buffer, leaving every existing iterator pointing at freed memory.**
>
> *(Verified: `data()` changed from `…A6E0` to `…9F90` and capacity went 3 → 28 — **the buffer genuinely moved**.)*
>
> **A range-based `for` holds iterators into the buffer for its whole duration.** If the body calls `push_back` and that triggers reallocation, **the loop's own iterators are dangling** and the next iteration is undefined behaviour.
>
> **This is [[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis|DSA ch. 04]]'s geometric growth** — the doubling that makes `append` amortised $O(1)$, and that produced the measured 5 084× single-operation spike. **Same mechanism; different consequence.** In Python, appending while iterating gives confusing but defined behaviour. **In C++ it is undefined**, so it may appear to work in testing and corrupt memory in production.
>
> **Safe patterns:**
> 1. **Index by position** — `for (size_t i = 0; i < v.size(); ++i)`, since `size()` is re-read each iteration. *(Note `v[i]` is still fine, but a saved reference is not.)*
> 2. **`reserve()` the final size first** — no reallocation, so no invalidation. **Also faster**, for the same reason DSA ch. 04's doubling analysis gives.
> 3. **Build a second container and swap** — the clearest when the output shape differs from the input.
>
> **And it is not only `push_back`.** `insert`, `erase`, `resize` and `clear` all invalidate; **`erase` invalidates even without reallocating**, which is why the erase-remove idiom exists.
>
> **(d) When a standard algorithm already says what you mean.**
>
> *(Verified: a hand-written linear search found 16 at index 3; summing evens with `continue` gave 70. Both are `std::find` and `std::accumulate` with a predicate.)*
>
> **Prefer `std::find`, `std::count_if`, `std::any_of`, `std::accumulate`, `std::sort`, `std::transform`:**
> - **They state *what*, not *how*** — `std::any_of` is self-documenting where a loop with a flag and a `break` is not.
> - **They cannot be off by one.** The range is passed as `begin, end`.
> - **They are correct.** Someone else has already made the mistakes.
> - **They are often faster**, being specialised and heavily optimised.
>
> **This is exactly [[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]]'s conclusion in another language** — there, `sorted()` beat a hand-written Python merge-sort by **14×** at the same complexity class. **The library is not just safer; it is usually faster too.**
>
> **Write a raw loop when** the logic genuinely has no algorithm counterpart, when several containers advance together in a non-uniform way, or when you are learning what the algorithm does.

## 📝 Summary

- **`while` may run zero times; `do`–`while` always runs once** *(verified with `n = 0`: 0 and 1)*. `do`–`while` is right only when "at least once" is the requirement.
- **⚠️ `<=` against `size()` is an off-by-one** *(verified: it reached index 5 on a 5-element vector)*. **The half-open range `[0, n)` is why `<` is right** — the count is exactly `end − begin`.
- **⚠️ `v[5]` returned garbage (2015895667) with no error and no crash** *(verified)*; **`.at(5)` threw `std::out_of_range`.** `operator[]` is unchecked by design so that `vector` costs what a raw array costs.
- **Out-of-bounds is a memory-safety bug, not just a wrong value** — it can read unrelated objects, and writing can corrupt the heap.
- **⚠️ `for (double x = 0; x != 1.0; x += 0.1)` never terminates** *(verified: `x` reached 2.0000000000000004441 without equalling 1.0)*. **Count with an integer and derive the double** — errors then do not accumulate.
- **A stray `;` becomes the loop body** *(verified: `count = 1`, not 5)*.
- **⚠️ And `/W4` does NOT warn about it — tested.** C4390 fires for `if (x);` but is **silent for `for(…);` and `while(…);`** — **and the loop case is the dangerous one**, since `while (cond);` hangs. **I had claimed the opposite; testing corrected it.**
- **So brace every loop body.** Unlike [[03 - Selection|ch. 03]], the compiler cannot save you here.
- **Modifying the loop variable inside the body breaks the header's contract** while leaving it looking bounded *(verified: no termination)*.
- **Range-based `for` removes the index, so off-by-one is impossible** — the strongest argument for it.
- **⚠️ `for (auto x : v)` copies every element, silently.** Default to **`for (const auto& x : v)`**; use `auto&` to modify.
- **⚠️ Growing a vector while looping is undefined behaviour** *(verified: the buffer moved and capacity went 3 → 28)*. **This is [[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis|DSA ch. 04]]'s geometric growth** — confusing in Python, **undefined here**.
- **Prefer standard algorithms to raw loops** — `std::find`, `std::count_if`, `std::accumulate`. Same lesson as [[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]]'s 14× for `sorted()`.

## ⚠️ Important Notes

1. **Use `<` with `size()`, never `<=`.** Think in half-open ranges `[0, n)`.
2. **⚠️ Use `.at()` when the index comes from outside your control** — user input, a file, an unbounded computation. It throws instead of corrupting memory.
3. **`operator[]` out of bounds is undefined behaviour, not "a wrong number".** "It worked in testing" carries no information.
4. **Never use a floating-point loop counter**, and never test one with `==` or `!=`. Count with an integer and derive the value.
5. **⚠️ Brace every loop body.** A stray semicolon is silent at `/W4` on loops — the compiler will not catch it.
6. **Treat the loop variable as read-only inside the body.** Use `continue`, `break`, or a `while` if you need to control progression.
7. **Default to `for (const auto& x : v)`.** Plain `auto` copies every element silently.
8. **Prefer range-based `for` whenever you do not need the index** — it makes off-by-one impossible.
9. **⚠️ Never modify a container while iterating it with a range-based `for`.** `push_back`, `insert`, `erase` and `resize` all invalidate.
10. **`reserve()` before a known number of `push_back`s** — it prevents invalidation and is faster.
11. **`erase` invalidates iterators even without reallocating** — hence the erase-remove idiom.
12. **Reach for `std::find` / `count_if` / `any_of` / `accumulate` before writing a loop.** They state intent, cannot be off by one, and are usually faster.
13. **Keep `break` and `continue` to short loops.** In a long one they scatter the exit conditions.

> [!warning] Gaps in the source material
> **Malik ch. 5 extracts well** — the loop forms, `break`/`continue`, nested loops and the sentinel/EOF-controlled input patterns all came through readably, with listings intact. **Book page $n$ = PDF page $n+50$; ch. 5 is PDF pages 315–396.** *(Standing quirk: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost** — flowcharts for each loop form. Minimal impact; the executed traces show the control flow directly.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 5.**
>
> **Additions beyond the source.** **Malik teaches the loop forms, their syntax, and worked counting examples. Every failure here is an addition:**
>
> - **§3's out-of-bounds read is mine** — Malik covers array bounds in [[06 - Arrays, C-Strings and std vector|his array chapter]] as a caution; **executing it to print `2015895667` and showing the program continue, then contrasting `.at()` throwing, is what makes "unchecked" concrete.** The framing as a *memory-safety* rather than *correctness* bug is mine.
> - **§4's non-terminating floating-point loop is mine**, connecting [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] §6's representation problem to a hang — and the point that **accumulating (`x += 0.1`) compounds error while deriving (`i * 0.1`) does not** is an addition.
> - **⚠️ §5's warning test is my own, and it corrected my own first claim.** I wrote that `/W4` flags the stray semicolon; **compiling three forms showed C4390 fires for `if (x);` and is silent for `for(…);` and `while(…);`.** **This is a deliberate counterweight to [[03 - Selection|ch. 03]]**, where raising the warning level *did* solve the problem — together they show tooling coverage is uneven, which is why bracing is worth adopting as an unconditional habit.
> - **§7's by-value/by-reference comparison is mine.** Malik's edition mentions range-based `for` briefly; **the silent-copy cost of `for (auto x : v)` and the `const auto&` default are modern-practice additions** per the subject file.
> - **§8's iterator invalidation is entirely mine** — Malik does not cover it — including **printing `data()` before and after growth to show the buffer physically move**, and the cross-link to [[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis|DSA ch. 04]]'s geometric reallocation, where the same mechanism was measured producing a 5 084× spike.
> - **§9's argument for standard algorithms over raw loops**, and its link to [[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]]'s 14× `sorted()` result, are additions.
>
> **Deliberately compressed.** **Malik's sentinel-controlled, counter-controlled, flag-controlled and EOF-controlled loop taxonomy** is reduced to §1's table plus [[02 - Input and Output|ch. 02]]'s `while (in >> v)` idiom, which is the EOF case done correctly. **His nested-loop pattern examples** (triangles, multiplication tables) exercise syntax without exposing behaviour and are not reproduced. **`goto`** is omitted entirely. **Loop invariants** are mentioned in [[Data Structures and Algorithms/contents/00-Index|DSA]] where they do analytical work; here they would be decoration.

**Previous:** [[03 - Selection]] · **Next:** [[05 - Functions and Scope]]
