---
subject: Basic Programming (C++)
chapter: 3
tags: [ds, cpp, selection, if-else, switch, short-circuit, dangling-else, boolean]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 4"
---

# Selection

**Selection is the simplest control structure and it has the highest density of traps in the language.**

The reason is that C++ inherited from C a design where **almost anything is a valid condition**: an assignment is an expression, any non-zero value is true, and `else` binds by proximity rather than by indentation. Each of those is defensible individually; together they produce **code that compiles, runs, and means something other than it looks like.**

**This is [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]'s theme again** — and §2 is its purest form: a one-character typo that changes a comparison into an assignment, takes the branch every time, and destroys the variable, **with no warning at the default warning level.**

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17`).

## 📘 Main Knowledge

### 1. What counts as true

*(Verified:)*
```
(bool)0   = false     (bool)1   = true
(bool)-1  = true      (bool)42  = true
(bool)0.0 = false     (bool)'a' = true
```

**Any non-zero value is true — including negatives.** There is no truthiness rule to learn beyond *"is it zero?"*.

> [!note] Simpler than Python, and that is the problem
> Python has a rich notion of falsiness: `0`, `""`, `[]`, `{}`, `None` are all false. **C++ has exactly one rule**, which is easier to learn — **but it means that `if (x)` where `x` is an `int` is always legal**, and so is `if (x = 5)`. **The simplicity of the rule is what makes §2 possible.**

### 2. ⚠️ `=` versus `==` — an assignment is an expression

**In C++ an assignment *has a value*: the value assigned.** So it can appear in a condition.

*(Verified:)*
```cpp
int y = 5;
if (y = 0)  … else …       // NOT taken, and y is now 0
int z = 5;
if (z = 7)  …              // TAKEN (7 is non-zero), and z is now 7
```

> [!warning] The branch is taken for every non-zero right-hand side
> **`if (z = 7)` assigns 7, yields 7, and 7 is true.** The condition does not depend on `z` at all — **it is true unconditionally**, and the original value of `z` is destroyed.
>
> **`if (y = 0)` is the mirror image**: never taken, and `y` is silently zeroed.
>
> **Neither is a syntax error. Neither is a runtime error.** The program runs and takes the wrong path every time.

**Three defences, all verified:**

| defence | how it works |
|---|---|
| **`const`** | `if (LIMIT = z)` is a **compile error** when `LIMIT` is `const` |
| **warnings** | `/W4` gives **C4706: assignment used as a condition** |
| **constant first** | write `if (7 == z)`; the typo `if (7 = z)` **cannot compile** |

> [!warning] ⚠️ The default warning level does not catch this — verified
> ```
> /W3  ->  (silent)
> /W4  ->  warning C4706: assignment used as a condition
> ```
> **MSVC's `/W3` is the common default and says nothing.** *(GCC and Clang give `-Wparentheses` at `-Wall`.)*
>
> **This is a stronger version of [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]'s argument for warnings-as-errors**: there, the signed/unsigned warning appeared at `/W3`. **Here it does not.** Raising the warning level is not optional.
>
> *(The "constant first" style — `if (7 == z)`, called a **Yoda condition** — turns the bug into a compile error, at the cost of reading backwards. Opinions differ; the `const` and `/W4` defences are less intrusive and cover more.)*

### 3. ⚠️ The dangling `else` — indentation is not structure

```cpp
if (a == 1)
    if (b == 2)
        std::cout << "inner";
else
    std::cout << "outer else";      // looks like it belongs to the OUTER if
```

*(Verified with `a = 1`, `b = 99`: the `else` executed — meaning it bound to the **inner** `if`, not the outer one the indentation suggests.)*

> [!note] `else` binds to the nearest unmatched `if`
> **The compiler ignores whitespace entirely.** The `else` attaches to `if (b == 2)`, so it runs when `a == 1` and `b != 2` — the opposite of what the layout says.
>
> **Python cannot express this bug**, because there indentation *is* the structure. **C++ requires you to write the structure explicitly.**
>
> **The fix is unconditional: always brace the bodies of `if` and `else`**, even one-liners. *(Verified: with braces the same logic behaves as it reads.)* This also prevents the related bug where adding a second statement to an unbraced `if` silently moves it outside the branch.

### 4. Short-circuit evaluation is a guarantee

*(Verified — the right-hand side carries a visible side effect:)*
```
false && rhs   ->  rhs NOT evaluated
true  || rhs   ->  rhs NOT evaluated
true  && rhs   ->  rhs evaluated
```

**`&&` evaluates its right operand only if the left is true; `||` only if the left is false.** **This is guaranteed by the standard, not an optimisation** — so you may rely on it for correctness.

**Which is what makes guard conditions work** *(both verified)*:
```cpp
if (!v.empty() && v[0] > 0)      // v[0] never evaluated on an empty vector
if (p != nullptr && *p == 5)     // *p never dereferenced when p is null
```

> [!warning] The operand order is load-bearing
> **`v[0] > 0 && !v.empty()`** reads identically to a human and is **undefined behaviour** on an empty vector — `v[0]` is evaluated first, out of bounds.
>
> **The guard must come first**, and this is one of the few places in C++ where the order of a boolean expression changes whether the program is *correct*, not merely how fast it is.

### 5. Floating-point conditions

*(Verified:)*
```
(0.1 + 0.2 == 0.3)      ->  false
|a - b|                 ->  5.551115e-17
(fabs(a-b) < 1e-9)      ->  true
```

**This is [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] §6's problem promoted into a branch**, and that makes it worse.

> [!note] A wrong branch is worse than a wrong number
> **A wrong number is usually wrong by a small amount.** A wrong *branch* sends the program down a different path entirely — **so the error is not proportional to the input.** A rounding difference of $5\times10^{-17}$ can mean an order is rejected instead of accepted.
>
> **Compare against a tolerance**, and prefer a relative one for values of varying magnitude ([[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] Exercise 3(b)).

### 6. `switch` — fall-through is the default

*(Verified, without `break`:)*
```
grade 1  ->  one two three
grade 2  ->  two three
grade 3  ->  three
```

> [!warning] Execution *enters* at the matching label and runs on
> **A `switch` is not a set of mutually exclusive branches.** The case label is a *jump target*; execution continues until a `break` or the closing brace.
>
> **A forgotten `break` does not error — it silently runs the following cases**, which is [[02 - Input and Output|ch. 02]]'s pattern again: valid code, no diagnostic, wrong behaviour.

**But fall-through is the default because it is genuinely useful** — grouping cases:
```cpp
switch (c) {
    case 'a': case 'e': case 'i': case 'o': case 'u':
        std::cout << "a vowel"; break;
    default:
        std::cout << "a consonant";
}
```
*(Verified: `'a'` and `'e'` → vowel, `'z'` → consonant.)*

**C++17 adds `[[fallthrough]];`** to mark deliberate fall-through, so the compiler can warn about the accidental kind.

### 7. What `switch` cannot do

- **No ranges.** `case 1 ... 10` is a GNU extension, not standard C++.
- **No strings, no floating point.** The condition must be **integral or an enum**.
- **Every case label must be a compile-time constant.**

*(Verified: comparing a `std::string` requires `if` / `else if`.)*

**So `switch` is for a small set of known integral values.** For anything else, `if`/`else if` — or a lookup table, which is often clearer than either.

### 8. The conditional operator

```cpp
int mx = (a > b) ? a : b;               // 7
const int limit = (a > b) ? a : b;      // <- the real advantage
```

> [!note] Its advantage is that it is an *expression*
> **`?:` produces a value, so it can initialise a `const` or a reference. An `if`/`else` cannot** — you would have to declare the variable uninitialised first, which forfeits `const` ([[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] §7).
>
> **That is the case for using it.** Not brevity — **nesting conditional operators is unreadable, and two levels is the practical limit.**

## ✏️ Exercises

**1. (The `=` trap.)** (a) Why does `if (z = 7)` compile? (b) What does it do? (c) Compare the three defences. (d) Why is this worse than ch. 01's signed/unsigned trap?

> [!example]- Solution
> **(a) Because in C++ an assignment is an *expression*, and its value is the value assigned.**
>
> `z = 7` assigns 7 to `z` **and evaluates to 7**. A condition needs a value convertible to `bool`, and `int` converts (§1: non-zero is true). **So the code is well-formed.**
>
> **This is not gratuitous.** It is what makes idioms like `while ((c = getchar()) != EOF)` and `if (auto* p = find(...))` possible — genuinely useful chained forms. **The cost is that a one-character typo is also legal.**
>
> **(b) It takes the branch unconditionally and destroys the variable.**
>
> *(Verified: `int z = 5; if (z = 7)` → **taken**, and `z` is now **7**. And `int y = 5; if (y = 0)` → **not taken**, `y` is now **0**.)*
>
> **The condition does not depend on the variable at all** — it is true for every non-zero right-hand side and false only for zero. **So the branch is deterministic, and it is deterministically wrong.**
>
> **Two damages, not one:** the wrong branch is taken, *and* the variable's value is silently overwritten — so code *after* the `if` is also wrong.
>
> **(c)**
>
> | defence | catches | cost |
> |---|---|---|
> | **`const`** | compile error when the target is `const` | only helps if the target *can* be `const` |
> | **`/W4`** | **C4706** *(verified)* | must be enabled; `/W3` is silent |
> | **Yoda `if (7 == z)`** | compile error on the typo | reads backwards; fails when both sides are variables |
>
> **`const` is the strongest where it applies**, because it is a compile error with no configuration and no style cost — and it is [[Database Management Systems/contents/01 - Databases and Data Models|the constraint principle]] again: make the invalid state unrepresentable.
>
> **Warnings are the broadest**, catching the case where neither operand can be `const`.
>
> **Yoda conditions are the most divisive.** They work, but only when one side is a literal, and they impose a permanent readability cost on every condition to guard against an occasional typo. **Most style guides now prefer `const` + warnings**, precisely because the tooling improved.
>
> **(d) Because the default warning level does not catch it.**
>
> [[01 - Fundamentals - Types, Variables and Expressions|Ch. 01]]'s `-1 < 1u` produced **C4018 at `/W3`** — the level most builds use. **Here `/W3` is silent and only `/W4` gives C4706** *(both verified)*.
>
> **So a project on default settings gets a diagnostic for one trap and nothing for the other**, even though this one is more damaging: signed/unsigned gives a wrong comparison, while `=` gives a wrong branch *and* corrupts a variable.
>
> **The conclusion is the same but stronger: `/W4` (or `-Wall -Wextra`), and warnings as errors.** A warning you have not enabled is not a warning.

**2. (Structure and evaluation order.)** (a) Explain the dangling `else`. (b) Why can Python not have this bug? (c) What does short-circuiting guarantee? (d) Why is operand order a correctness issue?

> [!example]- Solution
> **(a) `else` binds to the nearest unmatched `if`, and indentation is irrelevant.**
>
> *(Verified with `a = 1`, `b = 99`: the `else` branch executed — so it bound to `if (b == 2)`, not to `if (a == 1)` as the layout suggested.)*
>
> **The compiler sees a token stream with no whitespace significance.** Faced with `if … if … else`, the grammar is ambiguous, and C++ resolves it by attaching the `else` to the closest available `if`.
>
> **The damage is that the code is a lie.** Someone reading it sees an outer `else` and reasons about a case that does not exist — and the misreading survives review precisely because the indentation is persuasive.
>
> **The fix is unconditional: brace every `if` and `else` body**, even single statements. *(Verified: with braces the behaviour matches the layout.)*
>
> **Bracing also prevents the related bug** where someone adds a second statement to an unbraced branch:
> ```cpp
> if (x) doA();
>        doB();       // ALWAYS runs -- it was never in the branch
> ```
> **which is the same class of failure and arguably more common.**
>
> **(b) Because in Python indentation *is* the structure.**
>
> Python's parser uses `INDENT`/`DEDENT` tokens, so **the layout and the meaning cannot disagree** — there is exactly one way to read a nested `if`/`else`, and it is the one you can see.
>
> **The trade:** Python cannot express this bug but is sensitive to whitespace damage — which is exactly what [[Data Structures and Algorithms/contents/00-Index|DSA]] found when Goodrich's Python listings lost their indentation in extraction and became unrecoverable. **C++ code survived the same extraction** ([[00-Index|index]]) **because its structure is in the braces, not the layout.**
>
> **So the same design decision that creates the dangling `else` makes C++ robust to reformatting.** Neither choice is free.
>
> **(c) That the right operand is not evaluated when the left already determines the result.**
>
> *(Verified: `false && rhs` and `true || rhs` did not evaluate `rhs`; `true && rhs` did.)*
>
> **This is a guarantee in the standard, not a permitted optimisation** — which is what makes it usable for correctness rather than merely for speed. `&&` and `||` are among the few operators in C++ with a *sequenced* evaluation order.
>
> **Three uses:**
> 1. **Guarding** — `if (p != nullptr && *p == 5)` *(verified: `*p` never dereferenced)*.
> 2. **Bounds** — `if (!v.empty() && v[0] > 0)` *(verified)*, or `if (i < n && a[i] == x)`.
> 3. **Cost ordering** — put the cheap, highly-selective test first, so the expensive one usually does not run.
>
> **(d) Because reversing the operands can turn a correct program into undefined behaviour.**
>
> **`!v.empty() && v[0] > 0` is correct. `v[0] > 0 && !v.empty()` is UB on an empty vector** — `v[0]` is evaluated first and reads out of bounds.
>
> **The two read identically to a human.** Both say "the vector is non-empty and its first element is positive". **Only the order distinguishes safe from undefined**, and no diagnostic will tell you — `operator[]` does not check bounds ([[06 - Arrays, C-Strings and std vector|ch. 06]]).
>
> **This is unusual and worth internalising.** In most of C++, reordering a boolean expression is a performance question. **With `&&` and `||` it can be the difference between a working program and one that reads memory it does not own** — and, per [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]], UB means *no constraints on behaviour*, so it may appear to work in testing.
>
> **The rule: the guard always comes first**, and read every `&&` as "check, then use".

**3. (`switch` and `?:`.)** (a) Why is fall-through the default? (b) What are `switch`'s restrictions and what follows? (c) When is `?:` right? (d) What connects all this chapter's traps?

> [!example]- Solution
> **(a) Because a `switch` is a computed jump, not a set of branches.**
>
> **The case label is a *target*, not a boundary.** Execution jumps to the matching label and continues until a `break` or the closing brace — *(verified: without breaks, `grade 1` printed **one two three**)*.
>
> **And the behaviour is genuinely useful**, which is why it was kept:
> ```cpp
> case 'a': case 'e': case 'i': case 'o': case 'u':
>     std::cout << "a vowel"; break;
> ```
> *(Verified.)* **Grouping cases requires fall-through**, and it is the cleanest way to express "these values are equivalent".
>
> **The cost is that the accidental case is silent.** A missing `break` runs the next case's code with no diagnostic — [[02 - Input and Output|ch. 02]]'s pattern once more.
>
> **C++17's `[[fallthrough]];` resolves the tension**: mark the deliberate cases, and the compiler can warn about the rest. **Use it.**
>
> **(b) The condition must be integral or an enum; every label must be a compile-time constant; there are no ranges.**
>
> *(Verified: a `std::string` comparison needs `if`/`else if`.)*
>
> **The reason is the implementation.** A `switch` over a dense set of integers compiles to a **jump table** — index the table, jump, done, in constant time regardless of the number of cases. **That requires integral values known at compile time.** Strings and doubles have no such mapping. *(`case 1 ... 10` is a GNU extension and not portable.)*
>
> **What follows practically:**
> - **`switch` for a small fixed set of integral values or enum members** — and with an `enum`, most compilers warn if you miss one, which `if`/`else if` cannot do.
> - **`if`/`else if` for strings, ranges, floating point, or any runtime-computed condition.**
> - **A lookup table (`std::map`, or an array indexed by the value) when the set is large or data-driven** — often clearer than either, and modifiable without recompiling.
>
> **(c) When you need a *value*, not a statement.**
>
> ```cpp
> const int limit = (a > b) ? a : b;
> ```
> *(Verified.)* **`?:` is an expression, so it can initialise a `const` or a reference.** An `if`/`else` cannot — you would declare the variable first and assign in both branches, **which forfeits `const`** and reintroduces the risk of a path that leaves it uninitialised.
>
> **That is the real case for it**, and it is a good one: it lets you keep [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] §7's `const` discipline in places where you otherwise could not.
>
> **It is not a case for brevity.** Nested conditional operators are notoriously unreadable, and **two levels is the practical limit**. Beyond that, or when the branches have side effects, use `if`/`else`.
>
> *(A modern alternative for complex initialisation is an immediately-invoked lambda: `const int x = [&]{ if (…) return 1; … }();` — verbose, but it keeps `const` with arbitrary logic.)*
>
> **(d) Every one of them is code that compiles, runs, and means something other than it looks like.**
>
> | trap | looks like | actually |
> |---|---|---|
> | `if (z = 7)` | a comparison | an assignment, always true |
> | dangling `else` | binds to the outer `if` | binds to the inner |
> | missing `break` | one case runs | the following cases run too |
> | `v[0] > 0 && !v.empty()` | a safe check | undefined behaviour |
> | `a == b` on doubles | equality | almost never true |
>
> **None produces an error. All produce plausible behaviour.** *(Verified for each.)*
>
> **This is the shape of every serious bug this vault has logged** — [[Data Structures and Algorithms/contents/00-Index|DSA]]'s five misleading measurements, [[Database Management Systems/contents/00-Index|DBMS]]'s fan trap, `NOT IN`, `RANGE` frame and lost update, and [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]'s overflowing factorial. **The system does exactly what it was told; what it was told is not what was meant.**
>
> **What is specific to this chapter is that the defences are cheap and mechanical:**
> 1. **Brace every branch** — kills the dangling `else` and the added-statement bug.
> 2. **`/W4` or `-Wall -Wextra`, as errors** — kills `= `, missing `break`, and more.
> 3. **`const` wherever possible** — turns a class of mistake into a compile error.
> 4. **Guard first in `&&`** — the only defence against that one, since no tool checks it.
> 5. **Never `==` on floating point.**
>
> **Four of the five are habits, not knowledge**, which is why they are worth adopting before they are needed.

## 📝 Summary

- **Any non-zero value is true, including negatives** *(verified)*. One rule, simpler than Python's — and that simplicity is what makes `if (x = 5)` legal.
- **⚠️ An assignment is an expression, so `if (z = 7)` compiles.** *(Verified: the branch is **taken**, and `z` is destroyed to 7; `if (y = 0)` is never taken and zeroes `y`.)* **The condition is true for every non-zero right-hand side — it does not depend on the variable at all.**
- **⚠️ `/W3` does not warn; `/W4` gives C4706** *(both verified)* — so the common default catches nothing. **Stronger than [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]'s case, where `/W3` did warn.**
- **Defences: `const` (compile error), `/W4`, and constant-first `if (7 == z)`.** `const` is strongest where it applies; warnings are broadest.
- **⚠️ `else` binds to the nearest unmatched `if`, whatever the indentation** *(verified: the `else` bound to the inner `if`)*. **Brace every branch, always.**
- **Python cannot express this bug** because indentation *is* structure — the same property that made Goodrich's Python unrecoverable when extraction lost it, while C++ survived.
- **Short-circuit evaluation is a standard guarantee, not an optimisation** *(verified: `false && rhs` and `true || rhs` do not evaluate `rhs`)*.
- **⚠️ So operand order is a correctness issue**: `!v.empty() && v[0] > 0` is safe; **`v[0] > 0 && !v.empty()` is undefined behaviour**, and reads identically. **The guard always comes first.**
- **Floating-point equality in a condition is worse than in an expression** — *(verified: `0.1+0.2 == 0.3` is false, difference 5.55×10⁻¹⁷)* — because **a wrong branch is not proportional to the input.**
- **`switch` fall-through is the default** *(verified: without breaks, `grade 1` printed **one two three**)*. It exists because grouping cases needs it; **C++17's `[[fallthrough]];` marks the deliberate kind.**
- **`switch` requires integral or enum conditions and compile-time-constant labels** — because it compiles to a jump table. **No strings, no doubles, no ranges.**
- **`?:` earns its place by being an *expression***, so it can initialise a `const` or a reference where `if`/`else` cannot *(verified)*.
- **Every trap here is code that compiles, runs, and means something other than it looks like** — and four of the five defences are habits, not knowledge.

## ⚠️ Important Notes

1. **⚠️ Compile with `/W4` (MSVC) or `-Wall -Wextra` (GCC/Clang), as errors.** `/W3` is silent on assignment-in-condition — **a warning you have not enabled is not a warning.**
2. **Declare `const` wherever possible.** It turns `if (LIMIT = z)` into a compile error at no cost.
3. **⚠️ Brace every `if` and `else` body, including one-liners.** It prevents the dangling `else` *and* the bug where a second statement silently escapes the branch.
4. **⚠️ Put the guard first in `&&`.** `p != nullptr && *p == 5`, never the reverse — no tool will catch it, and the reverse is UB.
5. **Read every `&&` as "check, then use".**
6. **Rely on short-circuiting for correctness** — it is guaranteed by the standard.
7. **Never compare floating-point values with `==` in a condition.** A wrong branch is worse than a wrong number.
8. **Always `break` — and mark deliberate fall-through with `[[fallthrough]];`** so the compiler can flag the accidental kind.
9. **Prefer `switch` over an `enum`**, where most compilers warn about unhandled members. `if`/`else if` chains cannot do that.
10. **Use `if`/`else if` for strings, ranges and floating point** — `switch` cannot take them.
11. **Consider a lookup table** when the case set is large or data-driven; it is often clearer than either construct and changeable without recompiling.
12. **Use `?:` to initialise a `const` or reference**, not for brevity. Two levels of nesting is the limit.
13. **Avoid Yoda conditions as a primary defence** — they only work with a literal operand and cost readability everywhere. Use `const` and warnings instead.

> [!warning] Gaps in the source material
> **Malik ch. 4 extracts well** — the relational and logical operator tables, the `if`/`else` forms, `switch` syntax, and the worked selection examples all came through readably, with code listings intact. **Book page $n$ = PDF page $n+50$; ch. 4 is PDF pages 237–314.** *(The standing quirk applies: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost.** Minimal impact — this chapter's figures are flowcharts for `if`/`else` and `switch`, and the executed output conveys the control flow directly.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 4.**
>
> **Additions beyond the source.** **Malik teaches selection as syntax — the forms, the operators, the precedence. Every failure mode here is an addition:**
>
> - **§2's `=` versus `==` demonstration is mine.** Malik warns that the two are different; **executing `if (z = 7)` to show the branch is taken *and* `z` is destroyed makes the double damage concrete.**
> - **⚠️ The warning-level test is my own and produced the sharpest finding in the chapter**: `/W3` is **silent**, `/W4` emits **C4706** *(both verified by compiling the same file twice)*. **This is stronger than [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]'s case, where the signed/unsigned warning did appear at `/W3`** — so the two chapters together show that default warning levels are inconsistent about which traps they catch. **My own build helper uses `/W3`, so it would have missed this**; testing rather than assuming is what surfaced it.
> - **§3's dangling-`else` execution is mine**, as is the comparison with Python — including the observation that **the same property that prevents the bug in Python is what destroyed Goodrich's listings in extraction**, while C++ survived.
> - **§4's short-circuit demonstration with a visible side effect is mine**, and **the point that operand order decides between correct and undefined** — not merely fast and slow — is the chapter's most practically important addition. Malik describes short-circuiting as an efficiency feature.
> - **§5's framing that a wrong *branch* is worse than a wrong *number*** — because the error is not proportional to the input — is my own.
> - **§6's no-`break` execution trace**, and the explanation that `switch` compiles to a **jump table** and that this is *why* the restrictions in §7 exist, are additions. Malik lists the restrictions without the reason.
> - **§8's point that `?:` earns its place by being an expression** that can initialise a `const` — connecting back to [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] §7 — is mine, as is the immediately-invoked-lambda alternative.
> - **The modern-practice notes** — `[[fallthrough]]`, enum-switch exhaustiveness warnings, and the argument against Yoda conditions — are additions per the subject file.
>
> **Deliberately compressed.** **Malik's full relational- and logical-operator precedence tables** are omitted as reference material; the practical rule — parenthesise anything non-obvious — does not require memorising them. **His extended worked examples** (grade calculators, quadratic solvers) are not reproduced; they exercise the syntax without exposing behaviour. **`assert` and defensive programming** are deferred to [[11 - Exception Handling and RAII|ch. 11]]. **Nested `if` chains for menu logic** are covered by §7's lookup-table remark rather than at length.

**Previous:** [[02 - Input and Output]] · **Next:** [[04 - Repetition]]
