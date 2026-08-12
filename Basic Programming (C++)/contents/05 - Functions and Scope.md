---
subject: Basic Programming (C++)
chapter: 5
tags: [ds, cpp, functions, pass-by-reference, const-reference, dangling-reference, overloading, scope]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 6–7"
---

# Functions and Scope

**This chapter contains the one thing Python hides completely: how an argument gets into a function.**

Python has no choice to make — everything is a reference to an object, and whether you can mutate it depends on the object's type. **C++ makes you choose per parameter**, and the choice determines three separate things: whether the caller's variable can change, how much the call costs, and whether the code is even safe.

Two results carry the chapter:

- **§2 — a missing `&` is a one-character bug with no diagnostic.** The function compiles, runs, modifies a copy, and throws it away.
- **§5 — returning a reference to a local.** The values came back as **12289** and **54273** where the locals were **12345** and **54321** — **close enough to look plausible, and completely wrong.**

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17 /W4`).

## 📘 Main Knowledge

### 1. The three ways to pass

| | caller's variable | copy made | can modify |
|---|---|---|---|
| `void f(int x)` — **by value** | unchanged | **yes** | the copy only |
| `void f(int& x)` — **by reference** | **changed** | no | yes |
| `void f(const int& x)` — **by const reference** | unchanged | no | **no — enforced** |

*(Verified: after `byValue(a)` the caller's `a` was still 1; after `byReference(b)` it was 99. A `const&` parameter does not compile if the body assigns to it.)*

> [!note] Python makes this decision for you; C++ does not
> In Python, `def f(lst)` can always mutate the list and never rebind the caller's name. **There is one mechanism and the type decides the behaviour.**
>
> **In C++ the parameter declaration decides**, and it says three things at once: *does the caller see changes?*, *what does this cost?*, and *is the function promising not to modify?* — which is why the choice is worth making deliberately rather than by habit.

### 2. ⚠️ The missing `&` — a silent bug

```cpp
auto addOneByValue = [](std::vector<int> vec) { for (int& x : vec) ++x; };
auto addOneByRef   = [](std::vector<int>& vec){ for (int& x : vec) ++x; };
```
```
after addOneByValue(v):  v = 1 2 3      <- UNCHANGED, and no error
after addOneByRef(v):    v = 2 3 4      <- modified
```
*(Verified.)*

> [!warning] It compiled, ran, did the work, and discarded it
> **The by-value version is not broken code** — it correctly increments every element of a copy that is then destroyed. **There is no diagnostic**, because nothing is wrong from the compiler's point of view.
>
> **The symptom is "my function isn't doing anything"**, which is a confusing thing to debug because the function *is* doing something — just not to the object you meant.
>
> **And it is one character.** This is [[04 - Repetition|ch. 04]]'s stray semicolon in a different place: **a tiny, invisible edit that changes behaviour with no complaint.**

### 3. What passing by value costs — measured

*(Verified — a struct holding a `vector<double>` of 200 000 elements, 200 calls, best of 3:)*

| | time |
|---|---|
| by value | 0.1458 s |
| **by `const&`** | **0.0987 s — 1.5× faster** |

**Same answer.** The by-value version **allocates and copies 200 000 doubles on every call, purely in order to read them.**

**And counting the copies directly** *(verified, with an instrumented copy constructor)*:
```
after takeByValue(t)     : copies = 1
after takeByConstRef(t)  : copies = 1   (0 new)
```

> [!note] 1.5× is the honest figure, and the copy count is the stronger evidence
> **The timing understates the cost** because both versions still do the summing work, which dominates. **The copy count is unambiguous: one copy per call versus none.**
>
> **On a smaller object with more calls the ratio would be far larger** — and on a type whose copy constructor allocates, the cost is a heap allocation per call, which also fragments memory and defeats caching.
>
> **The rule: pass by `const&` for anything larger than a pointer or two.** For `int`, `double` and pointers, by value is at least as fast and clearer.

### 4. ⚠️ Returning a reference to a local

```cpp
int& danglingRef() {
    int local = 12345;
    return local;          // the local dies here
}
```

*(Verified:)*
```
int& r = danglingRef();   r = 12289          (the local was 12345)
int* p = danglingPtr();   *p = 54273         (the local was 54321)

after calling other functions (reusing that stack space):
  r  = 54273
  *p = 54273
```

> [!warning] The values are close but wrong — which is worse than obvious garbage
> **12289 against 12345. 54273 against 54321.** These are not random-looking values; they are the right order of magnitude and could pass a glance or a loose assertion.
>
> **And the values *changed* after unrelated function calls** — both became 54273 once other calls reused that stack space. **The same expression evaluated twice gave different answers, with no assignment in between.**
>
> **This is undefined behaviour in its purest form.** Not "sometimes wrong" — **no guarantees at all.** The local's storage was reclaimed when the function returned; anything may now be there.
>
> **✅ MSVC `/W4` does warn: `C4172: returning address of local variable or temporary`** *(verified — it fired for both functions)*. **This is one the compiler does catch**, unlike [[04 - Repetition|ch. 04]]'s stray semicolon.
>
> **Return by value instead.** Modern C++ makes this cheap — copy elision and move semantics mean returning a large object by value usually costs nothing.

### 5. Overloading — resolved at compile time

*(Verified:)*
```
show(42)              -> show(int)    -> 42
show(3.14)            -> show(double) -> 3.14
show(std::string(…))  -> show(string) -> hello
show('a')             -> show(int)    -> 97        <- char promoted to int
```

> [!note] The static type decides, and promotions can surprise
> **The compiler picks the overload from the *declared* type of the argument.** There is no runtime dispatch — that is [[09 - Inheritance and Polymorphism|ch. 09]]'s `virtual`.
>
> **`show('a')` selected `show(int)` and printed 97**, because `char` promotes to `int` and no `show(char)` exists. **A plausible-looking call silently selected a different function** — the same shape as every other trap in this subject.
>
> **Overloads that differ only in ways the conversion rules can bridge (`int`/`char`/`double`, or `T` and `const T&`) are a hazard.** Prefer distinct names when the behaviours genuinely differ.

### 6. Default arguments

```cpp
int area(int w, int h = 1);
area(5)     // 5
area(5, 3)  // 15
```
*(Verified.)*

**Two constraints worth knowing:** defaults must be **trailing** (`int f(int a = 1, int b)` is illegal), and they are **substituted at the call site** — so **changing a default requires recompiling every caller**, and a default in a header is part of your ABI.

### 7. Scope, lifetime, and `static` locals

*(Verified:)*
```
counterStatic() : 51 52 53 54 55     <- one object, initialised once, persists
counterPlain()  :  1  1  1  1  1     <- new object each call
```

**A `static` local is initialised once, on first use, and lives for the program's duration** — but its *name* is still local. *(The counter shows 51 because earlier code in the same program had already called it 50 times, which is itself the point: the state is global even though the name is not.)*

**Shadowing** *(verified)*:
```cpp
int x = 1;
{ int x = 2; }      // shadows the outer x
```
```
inner block: x = 2
outer block: x = 1
```

> [!note] ✅ MSVC `/W4` warns about shadowing — verified
> `C4456: declaration of 'x' hides previous local declaration`.
>
> **I had expected it not to.** *(GCC and Clang need `-Wshadow`, which is **not** in `-Wall`.)*
>
> **So warning coverage differs by compiler as well as by level** — a third data point after [[03 - Selection|ch. 03]] (`/W3` silent, `/W4` warns) and [[04 - Repetition|ch. 04]] (`/W4` silent on loops). **Test your compiler rather than assuming.**

## ✏️ Exercises

**1. (Parameter passing.)** (a) What do the three forms do? (b) Why is the missing `&` so hard to find? (c) What did the measurements show? (d) What is the rule?

> [!example]- Solution
> **(a)** **By value** copies the argument; the function works on the copy and the caller sees nothing. **By reference** binds to the caller's object; modifications are visible. **By const reference** binds without copying and **the compiler forbids modification**.
>
> *(Verified: `byValue` left the caller's `a` at 1; `byReference` set `b` to 99; a `const&` parameter does not compile if assigned to.)*
>
> **`const&` is the important one**, because it separates two things that by-value passing conflates: **avoiding a copy** and **promising not to modify.** It gives you both, which is why it is the default for non-trivial types.
>
> **(b) Because nothing is wrong.**
>
> *(Verified: `addOneByValue(v)` left `v` as `1 2 3`; `addOneByRef(v)` gave `2 3 4`.)*
>
> **The by-value function is correct code.** It increments every element of its parameter. **The parameter just happens to be a copy that is destroyed on return** — so the compiler has nothing to object to, and there is no warning at any level.
>
> **The symptom misleads.** "My function isn't doing anything" suggests the function is broken, so you debug inside it — where everything works perfectly. **The bug is in the signature, one line up and one character wide.**
>
> **It also scales badly**: the larger the object, the more work is done and discarded, so a function can be both wrong *and* slow for the same reason.
>
> **(c)** *(Verified, 200 calls on a struct holding 200 000 doubles:)*
>
> | | |
> |---|---|
> | by value | 0.1458 s |
> | by `const&` | **0.0987 s — 1.5×** |
> | copies made, by value | **1 per call** |
> | copies made, by `const&` | **0** |
>
> **The copy count is the stronger evidence.** The timing understates the difference because both versions still perform the summation, which dominates — **1.5× is the honest number and it is not the point.** The point is that one version performs a heap allocation and a 1.6 MB memcpy per call for no reason.
>
> **Reporting 1.5× rather than inflating it matters**, and it is the same discipline [[Database Management Systems/contents/04 - Normalization|DBMS ch. 04]] applied to denormalisation (1.6×) and [[Database Management Systems/contents/10 - Data Warehouses and OLAP|ch. 10]] to star schemas (1.14×): **argue the case on the mechanism, not on an exaggerated ratio.**
>
> **(d)**
>
> | parameter type | pass as |
> |---|---|
> | `int`, `double`, pointer, small enum | **by value** — a reference would be indirection for nothing |
> | any container, string, or large struct, read-only | **`const&`** |
> | anything the function must modify | **`&`** |
> | a value the function will take ownership of | by value, then `std::move` |
>
> **The threshold is roughly "larger than two pointers".** Below it, by value is at least as fast and clearer.
>
> **And `const&` should be the reflex for containers even when the object is small today** — the signature outlives the assumption.

**2. (Hard — dangling references.)** (a) What happened and why? (b) Why is "close but wrong" worse than garbage? (c) Why did the values change? (d) What is the fix, and did the compiler help?

> [!example]- Solution
> **(a) The function returned a reference to a variable whose storage was reclaimed on return.**
>
> A local lives in the function's **stack frame**. When the function returns, that frame is popped — **the storage is no longer reserved for anything.** The reference still points at the address.
>
> *(Verified: `danglingRef()` returned a reference to a local holding **12345**; reading it gave **12289**. `danglingPtr()` returned a pointer to a local holding **54321**; reading it gave **54273**.)*
>
> **The values were already wrong at the first read** — the returning process itself (restoring registers, adjusting the stack pointer) had overwritten that memory before `main` could look.
>
> **(b) Because plausible values survive review and testing.**
>
> **12289 against 12345 is a 0.5% difference.** If this were a price, a measurement or a count, it would pass a glance, pass an assertion like `assert(x > 0)`, and pass a test checking the order of magnitude.
>
> **Obvious garbage — a huge number, a negative where none is possible, a crash — is a *gift*.** It fails loudly and immediately, at the site of the bug.
>
> **This is the vault's recurring theme in its sharpest form.** [[01 - Fundamentals - Types, Variables and Expressions|Ch. 01]]'s factorial gave 1 932 053 504 — positive, large, plausible. [[04 - Repetition|Ch. 04]]'s out-of-bounds read gave an ordinary-looking integer. [[Database Management Systems/contents/00-Index|DBMS]]'s fan trap gave small plausible counts. **In every case the failure mode is *believability*, not magnitude.**
>
> **(c) Because intervening calls reused the stack space.**
>
> *(Verified: after calling other functions, **both** `r` and `*p` read **54273** — the same value, from two different dead locals.)*
>
> **The two dead frames occupied overlapping addresses**, and later calls wrote over them. **The same expression, evaluated twice with no assignment in between, gave different answers.**
>
> **That is what makes UB qualitatively different from a wrong value.** A wrong value is at least *stable* — you can observe it, reason about it, and trace it. **Here the object being read does not exist**, so there is nothing to reason about: the result depends on unrelated code, on optimisation settings, and on the build.
>
> **[[01 - Fundamentals - Types, Variables and Expressions|Ch. 01]]'s definition applies: UB is not "an unpredictable value", it is "no constraints on program behaviour".** The compiler may assume it cannot happen and optimise accordingly.
>
> **(d) Return by value — and yes, the compiler warned.**
>
> **✅ `C4172: returning address of local variable or temporary`, fired for both functions at `/W4`** *(verified)*.
>
> **This is a case where the tooling works**, in contrast to [[04 - Repetition|ch. 04]]'s stray semicolon, which `/W4` ignored. **Together the two chapters show that warning coverage is patchy but real — worth having, not sufficient alone.**
>
> **The fix is to return by value**, and in modern C++ that is cheap:
> - **Copy elision / RVO** means the return object is usually constructed directly in the caller's storage — **zero copies**.
> - **Move semantics** cover the rest: returning a large `vector` transfers ownership of its buffer rather than copying it.
>
> **So the historical reason for returning references out of functions — avoiding a copy — has largely gone.** Return references only to something that outlives the call: a member of `*this`, an element of a container the caller owns, or a `static`.
>
> **The same bug appears with pointers, with references to temporaries (`const std::string& s = getName() + "!";`), and with a `std::string_view` outliving its buffer** — the last being a modern, common form.

**3. (Overloading, defaults, scope.)** (a) When is an overload chosen? (b) Why did `show('a')` print 97? (c) What are default arguments' constraints? (d) What did the shadowing test show?

> [!example]- Solution
> **(a) At compile time, from the static types of the arguments.**
>
> *(Verified: `show(42)` → `show(int)`, `show(3.14)` → `show(double)`, `show(std::string(…))` → `show(string)`.)*
>
> **The compiler considers all candidates, ranks the conversions each would need, and picks the best.** An exact match beats a promotion, which beats a standard conversion. **Ambiguity is a compile error**, which is one of the few places C++ fails loudly.
>
> **There is no runtime component.** A variable's *declared* type decides, not what it points to — which is exactly the distinction [[09 - Inheritance and Polymorphism|ch. 09]]'s `virtual` exists to remove.
>
> **(b) Because `char` promotes to `int`, and no `show(char)` existed.**
>
> *(Verified: printed **97**, the ASCII code for `'a'`.)*
>
> **Integral promotion is a high-ranked conversion**, so `show(int)` was chosen unambiguously — no warning, no ambiguity error. **The call looks like it should print `a`.**
>
> **The hazard is general: adding an overload can silently change which function existing calls resolve to.** Adding a `show(char)` later would redirect every `show('a')` in the codebase, with no edit and no diagnostic.
>
> **So overload sets whose members behave differently are dangerous.** Overload when the functions do *the same thing* to different types (`print(int)`, `print(string)`); **use distinct names when the behaviour differs.** *(`explicit` and deleted overloads — `void show(char) = delete;` — can block unwanted conversions deliberately.)*
>
> **(c) They must be trailing, and they are substituted at the call site.**
>
> **Trailing**, because arguments bind positionally — `int f(int a = 1, int b)` gives no way to supply `b` alone, and is illegal.
>
> **Substituted at the call site** is the consequential one. **The default is not stored in the function; it is compiled into every caller.** Three results:
> 1. **Changing a default requires recompiling all callers.** Recompiling only the function leaves old callers passing the old value — a real problem across a library boundary, and an ABI break.
> 2. **A default in a header is part of your public interface**, as much as the parameter types.
> 3. **A virtual function's default arguments are taken from the *static* type**, so an override's default is ignored — a genuinely surprising interaction with [[09 - Inheritance and Polymorphism|ch. 09]].
>
> **Defaults are fine for a stable, obvious value.** For anything else, an overload is clearer and does not bake a value into callers.
>
> **(d) That MSVC `/W4` *does* warn — which I had expected it not to.**
>
> *(Verified: `C4456: declaration of 'x' hides previous local declaration`.)*
>
> **GCC and Clang need `-Wshadow`, which is not in `-Wall`** — so a project on `-Wall -Wextra` gets nothing.
>
> **This is now the third data point on warning coverage in this subject, and they do not agree:**
>
> | trap | MSVC |
> |---|---|
> | signed/unsigned ([[01 - Fundamentals - Types, Variables and Expressions\|ch. 01]]) | warns at **`/W3`** |
> | assignment in condition ([[03 - Selection\|ch. 03]]) | warns only at **`/W4`** |
> | stray `;` as a loop body ([[04 - Repetition\|ch. 04]]) | **never warns** |
> | returning a local's address (§4) | warns at `/W4` |
> | shadowing (§7) | warns at `/W4` |
>
> **The conclusion is not "warnings are unreliable" — it is "test what your compiler catches, and do not infer coverage from one example."** Which is the same discipline this vault applied to [[Database Management Systems/contents/02 - The Relational Model and Relational Algebra|SQLite's constraints]]: **a declaration is not an enforcement; try to violate it and see.**
>
> **On shadowing itself:** it is legal and occasionally intentional, but **an inner name silently taking precedence is exactly the "code that means something other than it looks like" pattern.** Prefer distinct names; keep the warning on.

## 📝 Summary

- **C++ makes you choose how each parameter is passed; Python does not.** The choice decides visibility of changes, cost, and safety at once.
- **By value copies; by reference exposes the caller's object; by `const&` does neither** *(all verified)*. **`const&` separates "no copy" from "no modification" and gives both.**
- **⚠️ A missing `&` is a one-character bug with no diagnostic.** *(Verified: the by-value version left `v` as `1 2 3` — it incremented a copy and discarded it.)* The symptom is "my function isn't doing anything", which sends you debugging the wrong place.
- **Passing by value cost 1.5× here** *(verified, 0.1458 s vs 0.0987 s)* — **but the copy count is the real evidence: 1 per call versus 0.** The timing understates it because the summing work dominates.
- **⚠️ Returning a reference to a local is undefined behaviour, and the values came back *plausible*:** **12289** for a local of **12345**, **54273** for **54321** *(verified)*.
- **The values then changed after unrelated calls** — both became 54273 *(verified)*. **The same expression gave different answers with no assignment between.**
- **"Close but wrong" is worse than obvious garbage**, because it survives review, assertions and tests — the vault's recurring failure mode in its sharpest form.
- **✅ `/W4` warns here (`C4172`)** *(verified)* — unlike [[04 - Repetition|ch. 04]]'s stray semicolon. **Return by value instead; copy elision and moves make it cheap.**
- **Overloads are resolved at compile time from static types** *(verified)*. **`show('a')` printed 97** because `char` promotes to `int` — a plausible call silently selecting a different function.
- **Default arguments must be trailing and are substituted at the call site**, so changing one requires recompiling every caller and is an ABI break.
- **A `static` local is initialised once and persists**, though its name stays local *(verified: 51–55, continuing a count from earlier in the program)*.
- **✅ `/W4` warns about shadowing (`C4456`)** *(verified — I expected otherwise)*; **GCC/Clang need `-Wshadow`, not in `-Wall`.**
- **Five warning data points now, and they disagree** — coverage varies by trap, by level and by compiler. **Test what your compiler catches.**

## ⚠️ Important Notes

1. **Pass `const&` for anything larger than about two pointers.** By value for `int`, `double` and pointers.
2. **⚠️ Check the signature when a function "doesn't do anything".** A missing `&` produces no diagnostic at any warning level.
3. **Use `const&` even when the object is small today** — the signature outlives the assumption.
4. **⚠️ Never return a reference or pointer to a local.** Return by value; copy elision and move semantics make it cheap.
5. **Return a reference only to something that outlives the call** — a member of `*this`, an element of a caller-owned container, or a `static`.
6. **Watch for the modern form of the same bug**: a `std::string_view` or `span` outliving its buffer, or `const T& x = f() + g();`.
7. **Overload only when the functions do the same thing to different types.** Different behaviour deserves different names.
8. **Beware promotions in overload sets** — `show('a')` silently chose `show(int)`. Use `= delete` to block an unwanted conversion.
9. **Adding an overload can silently redirect existing calls.** It is a source-compatible change that is not a behaviour-compatible one.
10. **Prefer an overload to a default argument across a library boundary** — defaults are compiled into callers and changing one is an ABI break.
11. **Never give a `virtual` function default arguments** — they are taken from the static type, so an override's defaults are ignored.
12. **Keep shadowing warnings on** (`/W4`, or `-Wshadow`, which `-Wall` does **not** include).
13. **⚠️ Test which warnings your compiler actually emits.** Five traps in this subject so far have five different coverage answers — do not infer from one example.

> [!warning] Gaps in the source material
> **Malik ch. 6–7 extract well** — function definitions and prototypes, value and reference parameters, scope rules, overloading, default arguments, and the `enum` material of ch. 7 all came through readably, with listings intact. **Book page $n$ = PDF page $n+50$; ch. 6–7 are PDF pages 397–570.** *(Standing quirk: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost** — chiefly the stack-frame and parameter-passing diagrams, which are the conventional teaching device for this material. **§§3–4 substitute measured copy counts and actual dangling values from running programs**, which show the same thing more concretely than a diagram can.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 6–7.**
>
> **Additions beyond the source.** **Malik teaches the syntax of value and reference parameters and states that value parameters are copies. Everything demonstrating the consequences is an addition:**
>
> - **§2's missing-`&` demonstration is mine**, including the observation that **the symptom ("my function isn't doing anything") points at the wrong place** — the function body is correct and the bug is in the signature.
> - **§3's measurement is mine.** Malik does not quantify the copy cost. **Both the timing (1.5×) and the instrumented copy count (1 per call vs 0) are my own**, and I report the modest ratio honestly and argue from the copy count instead — the same discipline used for [[Database Management Systems/contents/04 - Normalization|DBMS ch. 04]]'s 1.6× and [[Database Management Systems/contents/10 - Data Warehouses and OLAP|ch. 10]]'s 1.14×.
> - **§4 is the chapter's centrepiece and is entirely mine.** Malik warns against returning references to locals; **executing it produced values that were *close but wrong* (12289 for 12345, 54273 for 54321), and then showed both change to 54273 after unrelated calls** — demonstrating that the same expression yields different answers with no assignment between. **That is a much stronger statement of what UB means than any prose warning.**
> - **⚠️ Two of my own claims were contradicted by my own output and corrected before writing**: I had written that the dangling read "printed the right number" (it printed 12289, not 12345), and that `/W4` does not warn about shadowing (**it does — C4456**). Both were fixed by reading the program's actual output.
> - **The running warning-coverage table** (five traps, five different answers across `/W3`, `/W4` and never) is my own accumulated finding across [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]], [[03 - Selection|ch. 03]], [[04 - Repetition|ch. 04]] and this chapter, and it generalises [[Database Management Systems/contents/02 - The Relational Model and Relational Algebra|the DBMS lesson]] that a declaration is not an enforcement.
> - **The modern-practice notes** — copy elision and move semantics removing the historical reason to return references, `= delete` to block conversions, `string_view` lifetime hazards, and the `virtual` + default-argument interaction — are additions per the subject file.
>
> **Deliberately compressed.** **Malik's extensive worked examples** (temperature converters, palindrome checkers) exercise syntax without exposing behaviour and are not reproduced. **Function prototypes and the one-definition rule** are mentioned only where they bear on defaults; the header/source split belongs with [[07 - Structs and Classes|ch. 07]]. **`enum` (Malik ch. 7)** is folded in as a type rather than given its own treatment — its main modern relevance is `enum class` and switch-exhaustiveness, both covered in [[03 - Selection|ch. 03]]. **Namespaces** are noted only via `std::`; **`using namespace std;` is avoided throughout these notes on purpose**, which is itself the modern-practice position. **Recursion is excluded** — [[Data Structures and Algorithms/contents/03 - Recursion|DSA ch. 03]] owns it, per the scope decision in `00-Index.md`.

**Previous:** [[04 - Repetition]] · **Next:** [[06 - Arrays, C-Strings and std vector]]
