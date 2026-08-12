---
subject: Basic Programming (C++)
chapter: 1
tags: [ds, cpp, types, overflow, undefined-behaviour, floating-point, casting, const]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 1–2"
---

# Fundamentals: Types, Variables and Expressions

**Everything in this chapter follows from one fact: a C++ `int` is 32 bits and that is all it is.**

Python's integers are arbitrary precision, so `2**100` just works. **C++ gives you a fixed-width box, and when the number does not fit, you do not get an error — you get a different number.** §2 shows a factorial that is correct through 12 and false from 13 onward, with nothing to mark the transition.

That is the theme of the whole subject, stated in `00-Index.md`: **C++ produces plausible wrong answers where Python raises exceptions.** This chapter is where it starts.

**Every program below was compiled and run** with MSVC 14.50, `/EHsc /std:c++17 /Zc:__cplusplus /W3`.

## 📘 Main Knowledge

### 1. Compiled, not interpreted

**Python reads your source at run time. C++ does not — the source no longer exists when the program runs.**

The pipeline is: **preprocess** (`#include`, macros) → **compile** (source → object code) → **link** (objects + libraries → executable).

*(Verified — these were substituted at compile time:)*
```
__cplusplus  = 201703
compiled on  = Jul 31 2026 23:20:02
```

> [!note] What you buy and what you pay
> **You buy speed and early error detection.** A type error is caught at compile time — the cheapest place a bug can be found, which is exactly the argument [[Database Management Systems/contents/07 - Database Design|DBMS ch. 07]] made for constraints.
>
> **You pay in flexibility and in a build step.** And you pay in something less obvious: **the compiler only checks what it can check.** Types are verified; array bounds and arithmetic overflow are not.
>
> **⚠️ MSVC quirk, verified:** without `/Zc:__cplusplus`, the `__cplusplus` macro reports **199711 (C++98) even under `/std:c++17`** — a legacy default. Code branching on `__cplusplus` silently takes the wrong path.

### 2. Types have fixed sizes

*(Verified on this machine, MSVC x64:)*

| type | bytes | min | max |
|---|---|---|---|
| `char` | 1 | −128 | 127 |
| `short` | 2 | −32 768 | 32 767 |
| **`int`** | **4** | **−2 147 483 648** | **2 147 483 647** |
| `long long` | 8 | −9.22×10¹⁸ | 9.22×10¹⁸ |
| `unsigned int` | 4 | 0 | 4 294 967 295 |
| `float` | 4 | ~**6** significant digits | |
| `double` | 8 | ~**15** significant digits | |
| `bool` | 1 | | |

> [!warning] These sizes are not guaranteed by the standard
> The standard fixes only **minimum** sizes and relative ordering. **`int` is 4 bytes here; `long` is 4 on Windows and 8 on Linux** — a classic portability bug.
>
> **Use `<cstdint>`'s `int32_t`, `int64_t` when the width matters**, and never assume `sizeof(int) == sizeof(void*)`.

### 3. ⚠️ Integer overflow — the number simply stops being right

```
INT_MAX      = 2147483647
INT_MAX + 1  = -2147483648      <- NEGATIVE
UINT_MAX     = 4294967295
UINT_MAX + 1 = 0                <- wraps to 0
```

**And here it is doing real damage** — a factorial that looks entirely reasonable:

```cpp
int f = 1;
for (int i = 1; i <= 15; ++i) f *= i;
```

| $i$ | `int` result | true value | |
|---|---|---|---|
| 5 | 120 | 120 | ok |
| 12 | 479 001 600 | 479 001 600 | ok |
| **13** | **1 932 053 504** | **6 227 020 800** | **✗ WRONG** |
| 14 | 1 278 945 280 | 87 178 291 200 | ✗ |
| 15 | 2 004 310 016 | 1 307 674 368 000 | ✗ |

*(All verified.)*

> [!warning] There is no error, no warning, no exception
> **12! is right and 13! is wrong, and nothing marks the boundary.** The program runs to completion and reports a positive-looking number. **In Python the answer would simply have been correct.**
>
> **Unsigned overflow is *defined*** — it wraps modulo $2^n$, which is occasionally useful (hashing, checksums).
>
> **⚠️ Signed overflow is *undefined behaviour*.** The compiler is entitled to assume it never happens and to optimise accordingly — so `if (x + 1 < x)` may be compiled to `false`. **The −2 147 483 648 above is what this compiler did on this run; it is not a guarantee.**
>
> **Defences:** use `long long` or `int64_t` when values may be large; check before multiplying rather than after; and compile with `-fsanitize=signed-integer-overflow` (Clang/GCC) during testing.

### 4. ⚠️ Signed/unsigned comparison — a false statement that compiles

```cpp
int s = -1;
unsigned int u = 1;
std::cout << (s < u);        // prints: false
```

**−1 is not less than 1.** *(Verified.)*

**Why:** in a mixed comparison the **signed operand is converted to unsigned**, and `-1` becomes **4 294 967 295** *(verified)*.

> [!note] This is the `.size()` trap
> ```cpp
> for (int i = 0; i < v.size(); ++i)     // warning C4018: signed/unsigned mismatch
> ```
> **`std::vector::size()` returns an unsigned type**, so this comparison mixes them. It usually works — until the loop needs to run backwards or a subtraction goes negative, and then `i` becomes a huge positive number and the loop runs four billion times.
>
> **The compiler did warn** *(verified: `warning C4018: '<': signed/unsigned mismatch`)*, **which is the whole argument for compiling with warnings enabled and treating them as errors.** In C++ a warning is frequently the only notice you get before undefined behaviour.
>
> **Modern fix:** `for (std::size_t i = 0; i < v.size(); ++i)`, or better, a range-based `for` ([[04 - Repetition|ch. 04]]).

### 5. Integer division truncates

*(Verified — Malik's own example:)*
```
15 / 2                        = 7
15.0 / 2                      = 7.5
static_cast<double>(15) / 2   = 7.5
static_cast<double>(15 / 2)   = 7      <- cast applied TOO LATE
```

**`static_cast<double>(15 / 2)` is 7 because the division happened first**, in `int`, and casting afterwards cannot recover the lost remainder.

**And the version that bites in real code:**
```
100 * correct / total    = 70     (right)
correct / total * 100    = 0      *** WRONG -- 7/10 is 0 in integer arithmetic
```
*(Verified, with `correct = 7`, `total = 10`.)*

> [!note] Two operands, one rule
> **If both operands are integers, the result is an integer.** Promote *before* dividing — `100.0 * correct / total`, or `static_cast<double>(correct) / total`.
>
> **This is a plausible-wrong-answer bug**: `0` is a perfectly valid percentage, and nothing complains.

### 6. Floating point is not the real numbers

*(Verified, printed to 20 significant digits:)*
```
0.1 stored as   0.10000000000000000555
0.2 stored as   0.2000000000000000111
0.1 + 0.2   =   0.30000000000000004441
0.3 stored as   0.2999999999999999889

(0.1 + 0.2 == 0.3)?  false
difference:          5.551115e-17
```

**Neither 0.1, 0.2 nor 0.3 is representable in binary** — they are stored as the nearest `double`, and the errors do not cancel.

> [!warning] Never compare floating-point values with `==`
> ```cpp
> if (std::abs(a - b) < 1e-9)     // compare against a tolerance
> ```
> **And never accumulate money in `double`.** Use integer cents, or a decimal type. *(This is the same issue [[Mathematical Statistics/contents/00-Index|numerical work]] deals with as catastrophic cancellation.)*
>
> **`float` has only ~6 significant digits** *(verified: `digits10 = 6`)*. Widening `0.1f` to `double` gives **0.10000000149011611938** — the error was baked in at the narrower precision and cannot be recovered. **Use `double` unless you have a measured reason not to.**

### 7. `const` moves errors to compile time

```cpp
const double PI = 3.14159265358979;
PI = 3.0;     // does not compile: 'expression must be a modifiable lvalue'
```

**A whole class of bug becomes impossible rather than merely unlikely** — and it is caught at compile time, the cheapest place. **This is [[Database Management Systems/contents/01 - Databases and Data Models|DBMS ch. 01]]'s principle in a different language: constraints convert corruption into errors.**

**Declare everything `const` that does not need to change.** It documents intent, prevents accidental modification, and enables optimisation.

## ✏️ Exercises

**1. (Types and overflow.)** (a) Why does everything follow from fixed width? (b) Explain the factorial table. (c) Signed vs unsigned overflow? (d) What defends against it?

> [!example]- Solution
> **(a) Because a fixed-width type has a largest representable value, and exceeding it cannot be reported without a check that C++ does not make.**
>
> **Python's `int` grows as needed**, so arithmetic is always exact. **A C++ `int` is 32 bits** *(verified)*, giving a maximum of 2 147 483 647 — and when a result exceeds it, the extra bits are simply not there.
>
> **The design choice is deliberate: C++ chooses speed.** A machine addition is one instruction; checking for overflow on every operation would cost a branch every time. **C++ assumes you know your ranges.**
>
> **(b)** *(Verified:)* 12! = 479 001 600 is correct and fits. **13! = 6 227 020 800 exceeds `INT_MAX`, so the stored value is 1 932 053 504** — the true value modulo $2^{32}$, reinterpreted as signed.
>
> **What makes it dangerous is that the result stays plausible.** It is positive, it is large, it is the right order of magnitude. **A test checking "is the factorial positive and increasing" passes for 13! and 14!.** *(14! actually decreased — 1 278 945 280 against 13!'s 1 932 053 504 — so a monotonicity check would catch it, but only by luck.)*
>
> **And nothing at all is reported.** No exception, no warning, no flag.
>
> **(c) Unsigned overflow is defined; signed overflow is undefined behaviour.**
>
> **Unsigned wraps modulo $2^n$** *(verified: `UINT_MAX + 1 == 0`)*. That is guaranteed by the standard and is occasionally used deliberately — hashing ([[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists|DSA ch. 09]]), checksums, ring buffers.
>
> **Signed overflow is UB**, which is much worse than "an unpredictable value". **The compiler may assume it never occurs and optimise on that basis** — so `if (x + 1 < x)` can legally be compiled to `false`, deleting an overflow check you wrote. **The −2 147 483 648 printed above is what this compiler did on this run**, not a rule.
>
> **This distinction is the first appearance of the subject's central idea: UB is not "undefined value", it is "no constraints whatsoever on program behaviour".**
>
> **(d)**
> 1. **Use a wider type** — `long long` / `int64_t` holds 9.2×10¹⁸, enough for 20!.
> 2. **Check before, not after.** `if (a > INT_MAX / b) …` before multiplying — checking after is checking a value that is already wrong (and, for signed types, checking a value UB says need not exist).
> 3. **Sanitizers in testing** — `-fsanitize=signed-integer-overflow` traps it at run time. *(Clang/GCC; MSVC has `/RTC` and ASan but not this specific check.)*
> 4. **Compile with warnings on** — some cases are caught statically.
> 5. **Know your ranges.** Ninety percent of overflow bugs come from not asking "how big can this get?"

**2. (Hard — conversions.)** (a) Why is `-1 < 1u` false? (b) Why is this worse than it looks? (c) Explain `static_cast<double>(15 / 2)`. (d) What is the general rule?

> [!example]- Solution
> **(a) Because the signed operand is converted to unsigned before the comparison.**
>
> C++'s **usual arithmetic conversions** bring both operands to a common type. When one is `unsigned int` and the other `int` of the same rank, **the signed one converts to unsigned** — and `-1` in two's complement is all-bits-set, which as unsigned is **4 294 967 295** *(verified)*.
>
> **So the comparison actually performed is `4294967295 < 1`, which is correctly false.** The machine did exactly what the language specifies; the language specifies something surprising.
>
> **(b) Because it is silent, common, and produces a plausible answer.**
>
> **It compiles**, it runs, and it prints `false` — a valid-looking boolean. **Nothing indicates that a conversion changed the value's meaning.**
>
> **And the canonical form is extremely common:**
> ```cpp
> for (int i = 0; i < v.size(); ++i)
> ```
> `size()` returns unsigned, so every iteration performs this conversion. **It usually works** — until you write `v.size() - 1` on an empty vector, which is not −1 but **4 294 967 295**, and the loop runs four billion times reading past the end.
>
> **The mitigation exists and was seen working:** *(verified — the compiler emitted `warning C4018: '<': signed/unsigned mismatch`)*. **This is the argument for `/W4` or `-Wall -Wextra`, and for treating warnings as errors.** In C++ a warning is frequently the only notice before UB.
>
> **Modern fixes:** use `std::size_t` for indices; prefer a range-based `for` ([[04 - Repetition|ch. 04]]) which has no index at all; use `std::ssize()` (C++20) for a signed size.
>
> **(c) Because the division happens before the cast, and truncation is not reversible.**
>
> `static_cast<double>(15 / 2)`: the parenthesised `15 / 2` is evaluated first, both operands are `int`, so **integer division gives 7**. Casting 7 to `double` gives **7.0** *(verified)*. **The remainder was discarded before the cast could act.**
>
> `static_cast<double>(15) / 2` casts *first*, so the division is `double`-by-`int` → both promoted to `double` → **7.5** *(verified)*.
>
> **The realistic version is worse:**
> ```
> 100 * correct / total   = 70     (right)
> correct / total * 100   = 0      *** WRONG
> ```
> *(Verified with 7 and 10.)* **Mathematically these are the same expression.** In integer arithmetic the second computes `7/10 = 0` first. **And `0` is a perfectly plausible percentage** — nothing looks wrong.
>
> **(d) If both operands are integers, the result is an integer — so promote *before* the operation, never after.**
>
> Practically: **write `100.0 * correct / total`**, making one operand a `double` literal, or `static_cast<double>(correct) / total`.
>
> **The wider rule is that C++ converts silently and often**, and each conversion can lose information: integer division loses the remainder; signed→unsigned reinterprets negatives; `double`→`float` loses precision *(verified: `0.1f` widened back to `double` is **0.10000000149011611938**)*; narrowing `int`→`char` truncates.
>
> **None of these is reported at run time.** Some are caught by warnings; brace initialisation (`int x{3.7};`) makes narrowing a compile error, which is one reason to prefer it.

**3. (Floating point and `const`.)** (a) Why is `0.1 + 0.2 != 0.3`? (b) How should you compare? (c) `float` or `double`? (d) Why does `const` matter?

> [!example]- Solution
> **(a) Because none of the three is representable in binary.**
>
> *(Verified:)*
> ```
> 0.1 stored as 0.10000000000000000555
> 0.2 stored as 0.2000000000000000111
> sum         = 0.30000000000000004441
> 0.3 stored as 0.2999999999999999889
> ```
>
> **A `double` stores a binary fraction.** One-tenth in binary is the recurring `0.0001100110011…`, so it must be truncated — exactly as $1/3$ must be truncated in decimal. **Each of 0.1 and 0.2 is stored as the nearest representable value, and their rounding errors do not happen to cancel.**
>
> **The sum lands 5.55×10⁻¹⁷ above the stored 0.3** *(verified)*. Both are "0.3" to any sane precision, and they are different bit patterns, so `==` is false.
>
> **This is not a C++ defect** — it is IEEE 754, and Python, Java and JavaScript all do the same. **It is more visible in C++ because you control the precision.**
>
> **(b) Compare the magnitude of the difference against a tolerance:**
> ```cpp
> if (std::abs(a - b) < 1e-9)
> ```
> **Choosing the tolerance is the real work**, and there is no universal value. An absolute tolerance fails for very large numbers (where 10⁻⁹ is below the representable gap) and for very small ones (where it is enormous). **A relative tolerance — `std::abs(a-b) <= eps * std::max(std::abs(a), std::abs(b))` — is usually better**, with a small absolute floor for values near zero.
>
> **The better move is often to avoid the comparison entirely.** For money, use integer cents. For loop counts, use integers. **`for (double x = 0; x != 1.0; x += 0.1)` never terminates**, and that is the same bug wearing a different hat.
>
> **(c) `double`, unless you have measured a reason for `float`.**
>
> *(Verified: `float` gives ~**6** significant digits, `double` ~**15**.)* And the loss is permanent — **`0.1f` widened back to `double` is 0.10000000149011611938** *(verified)*: the precision was destroyed at the narrower type and widening cannot restore it.
>
> **`float` is worth it only when memory bandwidth dominates** — large arrays, GPU work, machine-learning weights where reduced precision is a deliberate and tested trade. **For scalar arithmetic there is usually no speed advantage at all**, since x86 computes in wide registers regardless.
>
> **The general rule: narrow at the end if you must, never in the middle.** Each narrowing compounds.
>
> **(d) Because it converts a runtime bug into a compile error.**
>
> *(Verified: assigning to a `const double` fails to compile — "expression must be a modifiable lvalue".)*
>
> **The value is not that you *would* have modified `PI`** — it is that the compiler now guarantees nobody does, including code written later by someone else.
>
> **This is exactly [[Database Management Systems/contents/01 - Databases and Data Models|DBMS ch. 01]]'s argument for constraints**, one level down: **a rule enforced by the system holds always; a rule enforced by convention holds until someone forgets.** [[Database Management Systems/contents/07 - Database Design|DBMS ch. 07]] audited a schema and found 6 of 10 rules enforced, with the rest relying on discipline — and `const` is how you move a rule into the enforced column here.
>
> **`const` also does real work beyond safety:** it documents intent at a glance, allows the compiler to optimise more aggressively, and — most importantly — **`const` references let you pass large objects without copying while guaranteeing they are not modified** ([[05 - Functions and Scope|ch. 05]]).
>
> **Practice: make everything `const` that does not need to change**, and let the compiler tell you when you were wrong.

## 📝 Summary

- **C++ is compiled: the source does not exist at run time.** *(Verified — `__cplusplus` and `__DATE__` were substituted at compile time.)* You buy speed and early type checking; **the compiler checks types but not bounds or overflow.**
- **⚠️ Without `/Zc:__cplusplus`, MSVC reports C++98 even under `/std:c++17`** *(verified)*.
- **Types have fixed sizes** *(verified: `int` = 4 bytes, max 2 147 483 647)*. **The standard fixes only minimums** — `long` is 4 bytes on Windows and 8 on Linux, so use `int32_t`/`int64_t` when width matters.
- **⚠️ Integer overflow gives a wrong number, not an error.** *(Verified: `12!` correct, **`13!` = 1 932 053 504 against a true 6 227 020 800**, with no exception and no warning.)*
- **Unsigned overflow is defined (wraps mod $2^n$); signed overflow is undefined behaviour** — the compiler may assume it cannot happen and delete your overflow check.
- **⚠️ `-1 < 1u` is false** *(verified)*, because the signed operand converts to unsigned: `-1` becomes **4 294 967 295**. This is the `v.size()` loop trap.
- **The compiler warned** (`C4018`) — **which is the argument for enabling warnings and treating them as errors.** In C++ a warning is often the only notice before UB.
- **Integer division truncates** *(verified: `static_cast<double>(15 / 2)` is **7**, because the cast came too late)*. **`correct / total * 100` gave 0 where `100 * correct / total` gave 70.**
- **Floating point is not the reals** *(verified: `0.1 + 0.2` is 0.30000000000000004441 and `0.3` is 0.2999999999999999889 — `==` is false, difference 5.55×10⁻¹⁷)*. **Compare against a tolerance, preferably relative.**
- **`float` has ~6 significant digits, `double` ~15** *(verified)*, and narrowing is irreversible — **`0.1f` widened back is 0.10000000149011611938.** Use `double` by default.
- **`const` converts a runtime bug into a compile error** — [[Database Management Systems/contents/01 - Databases and Data Models|DBMS ch. 01]]'s constraint principle in another language.

## ⚠️ Important Notes

1. **Ask "how big can this get?" before choosing a type.** Most overflow bugs are ranges nobody considered.
2. **⚠️ Use `long long` / `int64_t` for anything that accumulates** — factorials, running totals, counters, milliseconds since epoch.
3. **Never rely on signed overflow behaviour.** It is UB, so the compiler may optimise as though it cannot occur.
4. **Check for overflow *before* the operation, not after.** Afterwards the value is already wrong.
5. **⚠️ Never mix signed and unsigned in a comparison.** Use `std::size_t` for indices, or avoid indices entirely with a range-based `for`.
6. **Compile with `/W4` (MSVC) or `-Wall -Wextra` (GCC/Clang), and treat warnings as errors.** A warning is frequently the only notice before UB.
7. **Promote to floating point *before* dividing, not after.** `100.0 * a / b`, never `static_cast<double>(a / b)`.
8. **⚠️ Never compare floating-point values with `==`.** Use a relative tolerance, and never write `for (double x = 0; x != 1.0; x += 0.1)`.
9. **Never store money in `double`.** Use integer cents or a decimal type.
10. **Prefer `double` to `float`.** Narrowing is irreversible and rarely buys speed for scalar arithmetic.
11. **Narrow at the end if you must, never in the middle** — each narrowing compounds.
12. **Declare everything `const` that does not change**, and prefer brace initialisation (`int x{…}`), which makes narrowing conversions a compile error.
13. **Use `int32_t`/`int64_t` from `<cstdint>` when the exact width matters**, and never assume `sizeof(int) == sizeof(void*)`.
14. **Remember what UB actually means**: not "an unpredictable value" but **"no constraints on program behaviour at all"** — including the compiler removing code that assumed it.

> [!warning] Gaps in the source material
> **Malik chapters 1–2 extract well** — much better than [[Data Structures and Algorithms/contents/00-Index|Goodrich's Python]] did. **Braces, semicolons, `#include` directives and operators all survive**, and indentation is partially preserved. **Book page $n$ = PDF page $n+50$; ch. 1–2 are PDF pages 51–172.**
>
> **⚠️ The one extraction quirk: `C++` in *prose* renders as `C11`** — *"The following C11 program…"* — **238 times across pages 81–400.** The prose sets `C++` in a different font from the code. **Crucially, `+` survives inside code listings** *(verified: 728 literal `+` characters in those pages, and `for (i = 10; i <= 9; i++)` came through exactly)*, so arithmetic and increment operators are safe. **Read `C11` as `C++` in prose.**
>
> **All figures are images and are lost.** For this chapter that is minor — the figures are mostly the compilation-pipeline diagram and memory-layout sketches, and §1's verified compile-time constants make the same point.
>
> **No error was found in Malik ch. 1–2.**
>
> **Additions beyond the source.** **Malik is a first-course text and presents types, conversions and expressions as syntax to learn. Every failure demonstrated here is an addition:**
>
> - **§3's overflowing factorial is mine.** Malik covers data-type ranges and mentions overflow; **showing a natural-looking program that is correct through 12! and false from 13! — with the true values beside it — turns a range table into a demonstration.**
> - **The distinction between defined unsigned wrap and undefined signed overflow is an addition**, along with the point that **UB means "no constraints on behaviour", not "unpredictable value"** — which is the concept the rest of this subject depends on.
> - **§4's `-1 < 1u` is mine**, including the connection to the `v.size()` loop trap and **the observation that the compiler emitted `warning C4018`** — making the case for warnings-as-errors concrete rather than exhortative.
> - **§5's `correct / total * 100 = 0` is my extension** of Malik's `static_cast` example from a textbook expression to a bug someone would actually write.
> - **§6's floating-point demonstration is entirely mine** — Malik notes that floating-point comparison is unreliable without showing why; **printing the stored values to 20 digits, and the 5.55×10⁻¹⁷ residual, makes it concrete**, as does the irreversibility of `0.1f`.
> - **§7's framing of `const` as [[Database Management Systems/contents/01 - Databases and Data Models|DBMS ch. 01]]'s constraint principle** is my cross-subject link.
> - **The modern-practice notes** — `int32_t`, brace initialisation catching narrowing, `std::size_t`, sanitizers, `std::ssize` — are additions, per the subject file's instruction to give the modern form where Malik predates it.
>
> **Deliberately compressed.** **Malik ch. 1 is almost entirely history and background** — the evolution of programming languages, the parts of a computer, and a problem-analysis methodology. **Reduced to §1's compilation pipeline**, which is the only part with consequences for the code. **The full operator-precedence table** is omitted: it is reference material, and the practical advice — parenthesise anything non-obvious — does not require memorising it. **Malik's extensive coverage of `char` arithmetic and ASCII** is deferred to [[06 - Arrays, C-Strings and std vector|ch. 06]], where C-strings make it relevant. **Named constants via `#define`** are mentioned only to say `const` is preferred — macros are not type-checked and do not respect scope.

**Previous:** [[00-Index]] · **Next:** [[02 - Input and Output]]
