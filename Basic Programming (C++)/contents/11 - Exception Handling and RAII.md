---
subject: Basic Programming (C++)
chapter: 11
tags: [ds, cpp, exceptions, raii, exception-safety, noexcept, stack-unwinding, error-handling]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 14"
---

# Exception Handling and RAII

The last chapter of the subject, and it completes the arc [[08 - Pointers and Dynamic Memory|ch. 08]] opened.

**Ch. 08 *measured* RAII**: a raw `new` followed by a `throw` leaked (`live = 1`), while the identical code using `make_unique` did not (`live = 0`). **This chapter explains why, and what else follows from it.**

Three results:

- **§1 — unwinding releases every automatic object, in reverse order, on the exception path**, with no cleanup code written anywhere. **That is why C++ has no `finally`.**
- **§3 — `catch` by value slices**, exactly as [[09 - Inheritance and Polymorphism|ch. 09]]'s parameter passing did: a `DerivEx` caught as `BaseEx` reported `BaseEx`.
- **§5 — the exception-safety guarantees, demonstrated.** A failed operation left an object **half-updated (size 6)**; the same operation written copy-then-commit left it **untouched (size 3)**.

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17 /W4`).

## 📘 Main Knowledge

### 1. Stack unwinding

*(Verified:)*
```
+ acquired file-handle
+ acquired lock
both acquired, live = 2
                              <- throw
- released lock               <- REVERSE order
- released file-handle
caught: something failed
after the catch, live = 0
```

**Two resources acquired, an exception thrown between them and the handler, and both released — in reverse order of acquisition, automatically.** No cleanup code exists anywhere in the program.

> [!note] This is the whole of RAII
> **When an exception propagates, C++ destroys every automatic object in each scope it leaves.** That is the same guarantee [[07 - Structs and Classes|ch. 07]] §2 established for normal scope exit — **it simply also holds on the exception path.**
>
> **So tying a resource's lifetime to an object's lifetime makes cleanup automatic and exception-proof.** The pattern covers memory ([[08 - Pointers and Dynamic Memory|ch. 08]]'s `unique_ptr`), files (`fstream`), locks (`lock_guard`), and anything you wrap yourself.

### 2. Why C++ has no `finally`

```
Java / Python                      C++
--------------------------         --------------------------
acquire();                         Tracker t("thing");
try   { work(); }                  work();
finally { release(); }             // the destructor releases it
-> written at EVERY call site      -> written ONCE, in the type
```

> [!note] A `finally` is a promise to remember; a destructor is a guarantee
> **`finally` puts the cleanup at the *call site*, so every caller must remember it.** A destructor puts it in the *type*, once — **and then no caller can forget.**
>
> **This is [[08 - Pointers and Dynamic Memory|ch. 08]]'s principle again: remove the manual step rather than making it easier to remember.**
>
> *(Python needs `with` for the same reason — `__del__` runs at an unspecified time under garbage collection, so it cannot serve as a destructor.)*

### 3. ⚠️ `catch` by value slices

*(Verified:)*
```cpp
catch (BaseEx e)         -> BaseEx      <- SLICED
catch (const BaseEx& e)  -> DerivEx     <- correct
```

**This is [[09 - Inheritance and Polymorphism|ch. 09]] §2's object slicing, now in a `catch` clause.** The derived exception is copied into a base-typed object, the derived part is discarded, **and you handle the wrong error.**

> [!warning] Always throw by value, catch by `const&`
> **Throw by value** so the exception object's lifetime is managed for you — `throw new MyError()` leaks, and is a Java habit that does not transfer.
>
> **Catch by `const&`** to avoid slicing and avoid a copy. *(Catching by non-const reference is legal and occasionally used to annotate and rethrow.)*

### 4. Exception hierarchies

*(Verified — three throws, three different handlers selected:)*
```
DiskError   : disk is full
AppError    : generic app error
std::except : something else
```

**Handlers are tried in order, so the most-derived must come first.** Putting `catch (const std::exception&)` first would swallow all three — **and the compiler warns (`C4286`)**, which is one of the more useful warnings in the language.

**Derive your exception types from `std::runtime_error` or `std::logic_error`** so that generic handlers catching `std::exception` still work.

### 5. ⚠️ The three exception-safety guarantees

*(Verified — the same operation written two ways, both failing:)*

| | size before | size after a **failed** call |
|---|---|---|
| `appendNoGuarantee` | 3 | **6 — HALF-UPDATED** |
| **`appendStrong`** | 3 | **3 — unchanged** |

**The first mutated the object and then threw.** The object is *valid* but *wrong*: it contains elements from an operation that reported failure, **and the caller cannot retry safely because it does not know how far the operation got.**

**The second worked on a copy and committed with a `noexcept` operation:**
```cpp
std::vector<int> tmp = v_;      // work on a copy
…modify tmp…
if (fail) throw …;              // nothing has changed yet
v_.swap(tmp);                   // swap is noexcept: the commit point
```

| guarantee | meaning |
|---|---|
| **nothrow** | marked `noexcept`; cannot fail — swaps, destructors, moves |
| **strong** | succeeds completely, or has **no effect** |
| **basic** | the object stays **valid** but may be changed |
| none | the object may be corrupt; touching it is UB |

> [!note] The copy-then-commit shape is the same one [[08 - Pointers and Dynamic Memory|ch. 08]] used
> **`operator=` there allocated the new buffer *before* releasing the old one** — so if `new` threw, the object was untouched. **Same structure: do all the work that can fail first, then commit with something that cannot.**
>
> **Aim for the basic guarantee everywhere and the strong guarantee where a retry is plausible.** The strong guarantee costs a copy, so it is not always the right trade — but *no* guarantee is never acceptable.

### 6. ⚠️ Destructors must not throw

*(Verified: a throwing destructor was survivable **only because no other exception was active**.)*

> [!warning] If a destructor throws while the stack is already unwinding, `std::terminate` is called
> **The program dies immediately, with no handler run and no further cleanup.** *(This is not demonstrated here for exactly that reason.)*
>
> **The reason is that there would be two exceptions in flight and no coherent way to handle both.** The language chooses to stop.
>
> **Destructors are implicitly `noexcept` since C++11.** If a destructor must do something that can fail — flushing a buffer, closing a socket — **catch it internally and log it**, or expose an explicit `close()` that the caller may call and handle.

### 7. `noexcept`

*(Verified: `noexcept(f())` = **true**, `noexcept(g())` = **false**.)*

**`noexcept` is a promise, not a request.** Break it and `std::terminate` is called — **there is no way to catch a violation.**

> [!note] One keyword can change a container's complexity
> **`std::vector` inspects `noexcept` on your move constructor.** If moving cannot throw, growth **moves** the elements; if it might, growth must **copy** them, because a half-moved reallocation could not be rolled back and the strong guarantee would be lost.
>
> **So marking a move constructor `noexcept` can turn $O(n)$ copies into $O(n)$ moves** on every reallocation — [[06 - Arrays, C-Strings and std vector|ch. 06]]'s geometric growth and [[08 - Pointers and Dynamic Memory|ch. 08]]'s ownership meeting exception safety.
>
> **Mark move constructors and move assignment `noexcept`** whenever they genuinely cannot throw.

### 8. When *not* to use exceptions

- **Expected outcomes.** *"The user typed a letter where a number was wanted"* is not exceptional — [[02 - Input and Output|ch. 02]]'s stream state is the right mechanism.
- **Across a C API or DLL boundary**, where exceptions do not propagate reliably.
- **In a destructor** — never (§6).
- **Where the cost is unacceptable.** Throwing is slow; *not* throwing costs nothing, which is why exceptions suit genuinely exceptional cases.

**For failures that are part of normal operation, use a return value, `std::optional`, or `std::expected` (C++23).**

## ✏️ Exercises

**1. (Unwinding and RAII.)** (a) What did §1 show? (b) Why no `finally`? (c) Why catch by `const&`? (d) How should exception types be organised?

> [!example]- Solution
> **(a) Both resources were released, in reverse order, on the exception path, with no cleanup code.**
>
> *(Verified: two `Tracker`s acquired, an exception thrown, both released — lock first, then file-handle — and `live` returned to 0.)*
>
> **Unwinding destroys every automatic object in each scope the exception leaves.** It is the same guarantee as normal scope exit ([[07 - Structs and Classes|ch. 07]] §2), extended to the failure path — **which is precisely the path that manual cleanup gets wrong.**
>
> **Reverse order matters** because later resources may depend on earlier ones: releasing the lock before closing the file is safe; the reverse may not be.
>
> **This is what [[08 - Pointers and Dynamic Memory|ch. 08]] §7 measured** — raw `new` + throw leaked, `make_unique` + throw did not. **Here is the mechanism behind that result.**
>
> **(b) Because a destructor does the same job once, in the type, instead of at every call site.**
>
> **`finally` is a per-call-site obligation.** Ten places acquire the resource, ten `try`/`finally` blocks must be written, and **one omission is a leak.**
>
> **A destructor is a per-type guarantee.** Write it once and **no caller can forget it** — there is nothing at the call site to omit.
>
> **This is [[08 - Pointers and Dynamic Memory|ch. 08]]'s organising principle:** *every fix removes a manual step rather than making it easier to remember.* **`finally` makes the step easier; RAII removes it.**
>
> **It also composes.** Five RAII objects in a scope are released correctly in reverse order automatically; five nested `try`/`finally` blocks are a pyramid nobody writes correctly.
>
> *(Python's `with` is the same idea reached differently — a context manager is a scope-bound cleanup — but it is still opt-in at the call site, so it can be forgotten.)*
>
> **(c) To avoid slicing and to avoid a copy.**
>
> *(Verified: `catch (BaseEx e)` reported **BaseEx**; `catch (const BaseEx&)` reported **DerivEx**.)*
>
> **Catching by value copies the exception into a base-typed object, discarding the derived part** — [[09 - Inheritance and Polymorphism|ch. 09]] §2's slicing exactly. **You then handle a generic error when a specific one was thrown**, losing both the type and any extra data it carried.
>
> **And throw by value**, not `throw new MyError()`. The exception object's lifetime is managed by the runtime; **throwing a pointer leaks it**, since no one will delete it. *(This is a Java habit that does not transfer.)*
>
> **The pairing is fixed: throw by value, catch by `const&`.**
>
> **(d) Derive from `std::runtime_error` or `std::logic_error`, and catch most-derived first.**
>
> *(Verified: `DiskError` → `AppError` → `std::exception` handlers each selected correctly.)*
>
> **Handlers are tried in source order**, not by best match — unlike [[05 - Functions and Scope|ch. 05]]'s overload resolution. **So a base-class handler placed first swallows everything below it**, and the compiler warns (`C4286`).
>
> **Deriving from `std::exception`** means generic code catching `const std::exception&` still works, and `what()` is available. **`logic_error` for programming mistakes** (a precondition violated), **`runtime_error` for conditions detected at run time** (a disk full).
>
> **And catch what you can handle.** A handler that catches, logs, and continues as if nothing happened is usually worse than letting the exception propagate to someone who can act on it.

**2. (Hard — safety guarantees.)** (a) What did the two versions show? (b) Why is "valid but wrong" bad? (c) How is the strong guarantee achieved? (d) Which guarantee should you aim for?

> [!example]- Solution
> **(a) The same failure left the object in two very different states.**
>
> *(Verified: after a failed call, `appendNoGuarantee` left size **6**; `appendStrong` left size **3** — its original value.)*
>
> **The first mutated first and threw second**, so half the work survives. **The second did all the fallible work on a copy and committed with `swap`**, which cannot throw — so the failure happened before anything was visible.
>
> **(b) Because the caller cannot recover.**
>
> **The object is *valid*** — no invariants broken, safe to destroy, safe to inspect. **It is *wrong*** — it holds three elements from an operation that reported failure.
>
> **The caller's options are all bad:**
> - **Retry?** It does not know how far the operation got, so it may duplicate the first three elements.
> - **Undo?** There is no record of what was applied.
> - **Continue?** The data is silently incorrect.
>
> **So the exception told the caller *that* it failed but not *what state it left behind*** — and there is no way to find out from the outside.
>
> **This is the vault's recurring failure shape once more:** the program is running, the object looks fine, and the data is wrong. Compare [[Database Management Systems/contents/08 - Transactions and Concurrency Control|DBMS ch. 08]]'s atomicity — **a transfer that debits without crediting is exactly this bug**, and the database's answer (all-or-nothing) is the same answer as the strong guarantee.
>
> **(c) Do everything that can fail first, then commit with an operation that cannot.**
> ```cpp
> std::vector<int> tmp = v_;      // 1. copy
> …modify tmp…                    // 2. all the fallible work
> if (fail) throw …;              //    nothing visible has changed
> v_.swap(tmp);                   // 3. commit -- swap is noexcept
> ```
> **The commit must be `noexcept`**, or it could fail halfway and there would be no guarantee at all. **`swap` on standard containers is exactly that** — it exchanges internal pointers, allocating nothing.
>
> **This is the copy-and-swap idiom**, and it is why [[08 - Pointers and Dynamic Memory|ch. 08]] recommended it for `operator=`: **it gives self-assignment safety and the strong guarantee together**, and ch. 08's explicit version used the same shape — allocate the new buffer *before* releasing the old.
>
> **The cost is the copy.** For a large object that may be unacceptable, which is why the strong guarantee is a choice rather than a default.
>
> **(d) Basic everywhere; strong where a retry is plausible; nothrow where the language requires it.**
>
> | | aim for |
> |---|---|
> | **any function** | at least **basic** — the object must remain valid and destructible |
> | operations a caller may **retry** or roll back | **strong** |
> | **destructors, swaps, move operations** | **nothrow** — required |
> | performance-critical bulk operations | basic, documented as such |
>
> **No guarantee is never acceptable**, because a corrupt object cannot even be safely destroyed — and its destructor will run during unwinding whether you like it or not.
>
> **The strong guarantee is not free**, and pursuing it everywhere means copying everywhere. **The judgement is whether a caller could sensibly recover** — for a transaction, a save operation, a configuration update, yes; for appending to a log, no.
>
> **And whichever you provide, document it.** A caller cannot write correct error handling without knowing what state a failure leaves behind — **which is the actual lesson of §5.**

**3. (Discipline and closing.)** (a) Why must destructors not throw? (b) What does `noexcept` buy? (c) When should you not use exceptions? (d) What holds this subject together?

> [!example]- Solution
> **(a) Because a second exception during unwinding calls `std::terminate`.**
>
> *(Verified: a throwing destructor was survivable **only** because no other exception was in flight.)*
>
> **If an exception is already propagating and a destructor throws another, there are two exceptions and no coherent way to handle both.** The language does not try — **it calls `std::terminate`, and the program dies immediately with no handler run and no further cleanup.**
>
> **That makes it uniquely bad**, because §1 established that unwinding is *exactly* when destructors run in bulk. **A destructor that can throw is a landmine that detonates during error handling** — the moment you can least afford it.
>
> **Destructors are implicitly `noexcept` since C++11**, so a throwing one terminates even without a second exception unless explicitly marked `noexcept(false)`.
>
> **If cleanup can fail** — flushing a buffer, closing a socket — **catch and log internally**, and offer an explicit `close()` that callers may use when they want to handle the failure. *(`std::fstream` does exactly this: the destructor closes and swallows errors; `close()` reports them.)*
>
> **(b) A promise that enables optimisations — including a complexity change.**
>
> *(Verified: `noexcept(f())` = true, `noexcept(g())` = false.)*
>
> **It is a promise, not a request.** Violating it calls `std::terminate` with no way to catch the violation — **so mark `noexcept` only where it is genuinely true.**
>
> **The payoff that matters most is in `std::vector`.** During growth ([[06 - Arrays, C-Strings and std vector|ch. 06]] §6's geometric reallocation) the elements must be transferred to the new buffer. **If your move constructor is `noexcept`, `vector` moves them; if not, it must copy** — because a move that threw halfway would leave elements neither in the old buffer nor the new, destroying the strong guarantee.
>
> **So one keyword turns $O(n)$ copies into $O(n)$ moves on every reallocation.** For a `vector<std::string>` that is the difference between copying every character and swapping pointers.
>
> **Mark move constructors and move assignment `noexcept`**, and swaps, and destructors (implicit).
>
> **(c) When failure is *expected*, when it must cross a boundary, or when the cost is unacceptable.**
>
> **Expected outcomes are not exceptional.** A user typing letters where a number was wanted is normal input handling — [[02 - Input and Output|ch. 02]]'s stream state is the right mechanism, and throwing there would be both slow and misleading.
>
> **Across a C API or DLL boundary**, exceptions do not propagate reliably; error codes are required.
>
> **In a destructor**, never (§6).
>
> **Where throwing is too slow.** Exceptions are designed so that *not* throwing costs nothing and throwing costs a great deal — **which is exactly right if throws are rare, and exactly wrong if they are not.**
>
> **For expected failures use a return value, `std::optional`, or `std::expected` (C++23)**, which make the failure part of the type and force the caller to consider it — the [[Database Management Systems/contents/07 - Database Design|make-it-explicit]] principle again.
>
> **(d) Every chapter is a case of "the language will do something silently; state your intent so it does the right thing."**
>
> | chapter | the silent default | stating your intent |
> |---|---|---|
> | [[01 - Fundamentals - Types, Variables and Expressions\|01]] | overflow wraps or is UB | wider types, `const` |
> | [[02 - Input and Output\|02]] | a failed read sets a flag and continues | check the stream |
> | [[03 - Selection\|03]] | `if (x = 5)` compiles | `const`, `/W4` |
> | [[04 - Repetition\|04]] | `v[i]` is unchecked | `.at()`, range-`for` |
> | [[05 - Functions and Scope\|05]] | parameters are copied | `const&` |
> | [[06 - Arrays, C-Strings and std vector\|06]] | arrays decay, losing their length | `vector`, `span` |
> | [[07 - Structs and Classes\|07]] | copies are member-wise | Rule of Zero |
> | [[08 - Pointers and Dynamic Memory\|08]] | nothing frees what you allocate | RAII, `unique_ptr` |
> | [[09 - Inheritance and Polymorphism\|09]] | calls bind to the static type | `virtual`, `override` |
> | [[10 - Operator Overloading and Templates\|10]] | template requirements are implicit | concepts |
> | **11** | **a throw can leave an object half-updated** | **the safety guarantees** |
>
> **In every row the default is defensible, silent, and frequently not what you meant** — and in every row the fix is to say something that lets the compiler or the type system enforce it.
>
> **That is why this subject matters for a data scientist who will mostly write Python.** Python makes most of these choices for you and is right most of the time. **C++ makes you choose, and in doing so shows you that a choice was being made at all** — which is the transferable part.
>
> **And `std::vector<T>` is the worked example.** It uses fixed-width types, RAII, the Rule of Zero, operator overloading, templates, `noexcept` and the strong guarantee — **every mechanism in this subject, in one class that most users never think about.**

## 📝 Summary

- **Stack unwinding destroys every automatic object in each scope it leaves, in reverse order** *(verified: two resources released automatically on the exception path, `live` back to 0)*. **This is RAII, and it is what [[08 - Pointers and Dynamic Memory|ch. 08]] §7 measured.**
- **C++ has no `finally` because a destructor does the job once in the type**, rather than at every call site. **A `finally` is a promise to remember; a destructor is a guarantee.**
- **⚠️ `catch` by value slices** *(verified: `BaseEx` where `DerivEx` was thrown)* — [[09 - Inheritance and Polymorphism|ch. 09]]'s slicing in a `catch` clause. **Throw by value, catch by `const&`.**
- **`throw new MyError()` leaks** — the exception object's lifetime is managed for you.
- **Handlers are tried in source order, so most-derived first** *(verified)*; a base handler placed first swallows everything, and the compiler warns (`C4286`).
- **⚠️ The safety guarantees, demonstrated: a failed `appendNoGuarantee` left the object HALF-UPDATED (size 6); `appendStrong` left it UNCHANGED (size 3)** *(both verified)*.
- **"Valid but wrong" is the dangerous state** — the caller cannot retry, undo, or trust it, and the exception said nothing about what was left behind.
- **The strong guarantee is achieved by copy-then-commit**, with a `noexcept` commit (`swap`). **The same shape as [[08 - Pointers and Dynamic Memory|ch. 08]]'s `operator=`** — do the fallible work first, commit with something that cannot fail.
- **Aim for basic everywhere, strong where retry is plausible, nothrow where required. No guarantee is never acceptable** — and **document which you provide.**
- **⚠️ A destructor that throws during unwinding calls `std::terminate`** — the program dies with no handler run. Destructors are implicitly `noexcept` since C++11.
- **`noexcept` is a promise whose violation terminates** — and **`vector` uses it to decide whether growth moves or copies**, so one keyword can change $O(n)$ copies into $O(n)$ moves.
- **Do not use exceptions for expected outcomes, across C/DLL boundaries, in destructors, or where throwing is too costly.** Use `std::optional` / `std::expected`.
- **The subject's thread: the language does something silently by default; state your intent so it does what you meant.**

## ⚠️ Important Notes

1. **Wrap every resource in an RAII type.** Never write cleanup code on multiple exit paths.
2. **⚠️ Throw by value, catch by `const&`.** Catching by value slices; throwing a pointer leaks.
3. **Order handlers most-derived first**, and heed `C4286`.
4. **Derive exception types from `std::runtime_error` or `std::logic_error`** so generic handlers still work.
5. **Catch only what you can handle.** Catching, logging and continuing is usually worse than propagating.
6. **⚠️ Never let an exception escape a destructor.** During unwinding it calls `std::terminate`.
7. **Offer an explicit `close()`** when cleanup can genuinely fail, and swallow errors in the destructor.
8. **⚠️ Aim for at least the basic guarantee in every function.** No guarantee means the object cannot even be safely destroyed.
9. **Use copy-then-commit for the strong guarantee**, and make the commit `noexcept` (`swap`).
10. **Document which guarantee a function provides.** Callers cannot write correct handling without it.
11. **Mark move constructors, move assignment and swaps `noexcept`** — `vector` growth depends on it.
12. **⚠️ Never mark something `noexcept` that might throw.** Violation terminates and cannot be caught.
13. **Do not use exceptions for expected failures** — use `std::optional`, `std::expected`, or a return value.
14. **Do not throw across a C API or DLL boundary.**
15. **Remember the arc:** in every chapter the silent default is defensible and frequently not what you meant. **Say what you mean, and let the compiler enforce it.**

> [!warning] Gaps in the source material
> **Malik ch. 14 extracts well** — `try`/`catch`/`throw` syntax, the `std::exception` hierarchy, creating your own exception classes, rethrowing, and stack unwinding all came through readably, with listings intact. **Book page $n$ = PDF page $n+50$; ch. 14 is PDF pages 1041–1084.** *(Standing quirk: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost.** Minimal impact — the figures are mostly flow diagrams for `try`/`catch`, and §1's execution trace shows the unwinding order directly.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 14.**
>
> **Additions beyond the source.** **Malik covers exception *syntax* thoroughly — how to throw, catch, and define exception classes. Almost everything about exception *safety* is added:**
>
> - **§§1–2's RAII framing is mine.** Malik describes stack unwinding as a mechanism; **showing two resources released in reverse order on the exception path, and drawing the contrast with `finally` as "a promise to remember versus a guarantee", makes it the chapter's organising idea** rather than a footnote. It also completes [[08 - Pointers and Dynamic Memory|ch. 08]] §7's measurement.
> - **§3's `catch`-by-value slicing is mine**, connecting it to [[09 - Inheritance and Polymorphism|ch. 09]] §2 — the same bug in a new place, which is why the rule "throw by value, catch by `const&`" is worth stating as a pair.
> - **⚠️ §5, the three guarantees, is the chapter's centrepiece and is entirely absent from Malik.** **Demonstrating the same operation leaving an object half-updated (size 6) versus untouched (size 3) turns an abstract taxonomy into a measured difference** — and the observation that "valid but wrong" leaves the caller unable to retry, undo *or* trust the object is the practically important consequence. **The link to [[Database Management Systems/contents/08 - Transactions and Concurrency Control|DBMS ch. 08]]'s atomicity** — a debit without a credit is precisely this bug, and all-or-nothing is precisely the strong guarantee — **is my own cross-subject observation.**
> - **§6's terminate-during-unwinding rule and §7's `noexcept` material are additions** (the book predates C++11's `noexcept`). **The finding that `vector` inspects `noexcept` to decide between moving and copying** — so one keyword changes the cost of every reallocation — connects [[06 - Arrays, C-Strings and std vector|ch. 06]]'s growth to [[08 - Pointers and Dynamic Memory|ch. 08]]'s ownership.
> - **§8's "when not to use exceptions", including `std::optional` and `std::expected`,** is modern practice not in the book.
> - **The closing table in Exercise 3(d)** — every chapter as a case of "the language does something silently; state your intent" — is my own synthesis of the subject.
>
> **Deliberately compressed.** **Malik's coverage of `throw` specifications** (`void f() throw(int)`) is omitted: dynamic exception specifications were deprecated in C++11 and **removed in C++17**, so teaching them would be actively misleading. **His extended examples of custom exception classes** are represented by §4's three-level hierarchy. **`std::exception`'s full derived hierarchy** (`bad_alloc`, `bad_cast`, `out_of_range`, …) is not catalogued — the ones that matter appear where they arise ([[04 - Repetition|ch. 04]]'s `out_of_range` from `.at()`, [[08 - Pointers and Dynamic Memory|ch. 08]]'s `bad_alloc`). **Rethrowing and nested exceptions** are mentioned only in passing; `std::nested_exception` is beyond a first course.

**Previous:** [[10 - Operator Overloading and Templates]] · **Next:** *(end of subject — see [[00-Index]])*
