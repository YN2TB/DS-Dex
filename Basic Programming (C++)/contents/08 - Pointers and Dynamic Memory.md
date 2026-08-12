---
subject: Basic Programming (C++)
chapter: 8
tags: [ds, cpp, pointers, dynamic-memory, memory-leak, rule-of-three, smart-pointers, raii, unique-ptr]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 12"
---

# Pointers and Dynamic Memory

**This is the chapter Python has no equivalent of, and it is this subject's core contribution.**

[[Data Structures and Algorithms/contents/00-Index|DSA]] built linked lists, trees and graphs without once asking where the nodes lived. **Here you allocate them and you free them** — and the three ways that goes wrong are all silent:

- **§2 — the leak.** Five objects allocated, five pointers lost, **nothing destroyed and nothing reported.**
- **§4 — the Rule of Three**, which exists because [[07 - Structs and Classes|ch. 07]] §5 showed the compiler's generated copy aliasing, dangling and double-freeing an owning pointer.
- **§7 — the strongest result in the chapter.** A raw `new` followed by an exception **leaks**; the identical code with `make_unique` **does not**, because a destructor still runs while the stack unwinds.

**And §§5–6 are the modern answer**: hold a `vector` or a `unique_ptr` and every bug above becomes either impossible or a compile error.

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17 /W4`).

## 📘 Main Knowledge

### 1. Stack versus heap

```cpp
int  x = 42;         int* p = &x;      // p holds an ADDRESS
int* q = new int(7);                   // heap: yours to delete
delete q;
```
*(Verified: `sizeof(int*)` = 8 bytes regardless of what it points to.)*

> [!note] The one difference that generates the whole chapter
> **A stack object is destroyed automatically at scope exit** ([[07 - Structs and Classes|ch. 07]] §2). **A heap object is destroyed only when you say so.**
>
> **`new` is for objects that must outlive the scope that created them**, or whose size or number is unknown at compile time. **Everything else should be on the stack**, where the language handles it.

### 2. ⚠️ The leak

```cpp
for (int i = 0; i < 5; ++i) {
    Res* r = new Res("leaked");        // pointer dies at end of iteration
}
```
```
constructed = 5, destructed = 0, STILL LIVE = 5
```
*(Verified.)*

> [!warning] The pointers died; the objects did not
> **The only handle to each object went out of scope.** The objects remain allocated, unreachable, and will never be freed.
>
> **No error. No warning. No crash.** The program simply uses memory it can never reclaim — **and in a loop or a long-running server this is how a process grows until the OS kills it.**
>
> **This is the failure mode a garbage-collected language removes entirely**, and it is the price C++ pays for deterministic destruction. *(Tools exist — Valgrind, AddressSanitizer, MSVC's CRT debug heap — and they are worth running, but they find leaks after the fact.)*

### 3. Matching the `new` and `delete` forms

*(Verified: `new Res[4]` constructed 4; `delete[] arr` destructed **all 4**.)*

> [!warning] `new` ↔ `delete`, `new[]` ↔ `delete[]`, never crossed
> **`delete arr` on an array is undefined behaviour** — typically only one destructor runs and the block is freed with the wrong size, corrupting the heap.
>
> **It is not demonstrated here**, because heap corruption crashes somewhere unrelated and would prove nothing about where the fault was. *(That in itself is the lesson: the symptom appears far from the cause.)*
>
> **`std::vector` removes the question entirely.**

### 4. The Rule of Three

**[[07 - Structs and Classes|Ch. 07]] §5 showed a class with an owning `int*` and no copy constructor**: `b = a` gave the same address, writes through one changed the other, and the second destructor double-freed.

**The fix is all three together** — if you need any one, you need all three:

```cpp
RuleOfThree(const RuleOfThree& o);              // 1. copy constructor
RuleOfThree& operator=(const RuleOfThree& o);   // 2. copy assignment
~RuleOfThree();                                 // 3. destructor
```

*(Verified:)*
```
a.data = …A1C0
b = a;   b.data = …A7E0        <- a DIFFERENT buffer
b.data[0] = 999  ->  a.data[0] = 0      <- 'a' untouched
a = a;   (self-assignment)  a.data[3] = 3    <- survived
```

> [!note] Copy assignment is the hard one, for two reasons
> **1. Self-assignment.** `a = a` looks absurd but arises through references and aliases (`v[i] = v[j]`). **Without the guard, `operator=` would `delete[]` its own buffer and then copy from the freed memory into itself.**
>
> **2. Allocation order.** The implementation allocates the new buffer **before** releasing the old one:
> ```cpp
> int* fresh = new int[o.n];   // if this throws...
> …copy…
> delete[] data;               // ...we never got here, and the object is intact
> data = fresh;
> ```
> **If `new` throws, the object is unchanged rather than left half-destroyed.** That is the **strong exception guarantee** ([[11 - Exception Handling and RAII|ch. 11]]), and reversing the two lines quietly forfeits it.
>
> *(With move operations this becomes the **Rule of Five**. The cleaner idiom is copy-and-swap, which gets self-assignment and exception safety for free.)*

### 5. The Rule of Zero

```cpp
struct RuleOfZero { std::vector<int> data; };    // special members declared: 0
```
*(Verified: `b = a` produced a correct deep copy — `a.data[0]` unchanged at 0.)*

> [!note] No destructor, no copy constructor, no `operator=`, no `new`, no `delete`
> **The `vector` already knows how to copy and free itself**, so the compiler-generated members are correct ([[07 - Structs and Classes|ch. 07]] §2).
>
> **This is the right default.** §4 is worth understanding because you will read code that needs it — **but writing it is a decision to take on work the library has already done.**

### 6. Smart pointers — ownership stated in the type

**`std::unique_ptr` — one owner** *(verified)*:
```
unique_ptr created.  live = 1
std::unique_ptr<Res> v = u;         // WILL NOT COMPILE -- not copyable
auto v = std::move(u);              // ownership transferred
after move:  u is null, v is non-null
scope ended: live = 0, destroyed = 1     <- freed automatically
```

> [!note] The double free became a compile error
> **`unique_ptr` is not copyable.** [[07 - Structs and Classes|Ch. 07]] §5's disaster — two objects believing they own one buffer — **is rejected by the compiler**, not diagnosed at runtime.
>
> **This is the [[01 - Fundamentals - Types, Variables and Expressions|`const` principle]] again, and the [[Database Management Systems/contents/01 - Databases and Data Models|DBMS constraint principle]]: make the invalid state unrepresentable rather than detecting it.**
>
> **And it costs nothing** — `unique_ptr` is the size of a raw pointer with no runtime overhead.

**`std::shared_ptr` — shared ownership, reference counted** *(verified)*:
```
use_count = 1
after a copy:      use_count = 2, live = 1
inner copy gone:   use_count = 1, live = 1      <- NOT freed yet
last owner gone:   live = 0                      <- freed at count 0
```

**Copying is *correct* here, because the type says ownership is shared.** The cost is an atomic increment per copy — **use `unique_ptr` unless sharing is genuinely required.**

### 7. ⚠️ The result that settles the argument

*(Verified — the same function two ways, both throwing before cleanup:)*

| | outcome |
|---|---|
| `Res* r = new Res(…); throw …; delete r;` | **live = 1 — LEAKED** |
| `auto r = std::make_unique<Res>(…); throw …;` | **live = 0 — freed** |

> [!warning] The `delete` was never reached, and the compiler said so
> **The `throw` skipped straight past `delete r`.** *(MSVC emitted `C4702: unreachable code` for that line — another warning-coverage data point, and here a genuinely useful one.)*
>
> **But `unique_ptr`'s destructor still ran**, because [[07 - Structs and Classes|ch. 07]] §2's guarantee holds during stack unwinding: **every automatic object is destroyed on every exit path, including an exception.**
>
> **This is RAII — Resource Acquisition Is Initialisation — and it is the single most important idea in C++.** Tie a resource's lifetime to an object's, and cleanup becomes automatic and exception-proof.
>
> **It is also why C++ has no `finally`.** The destructor already runs, guaranteed. *(Contrast Python, where `__del__` timing is unspecified, so `with` is needed to get the same effect.)*
>
> **And note the scale of the problem it solves.** In a function with five allocations and several early returns, correct manual cleanup means a `delete` on every path — which is exactly the code nobody gets right.

### 8. What to use

| | |
|---|---|
| raw `new`/`delete` | **essentially never** in application code |
| **`std::vector<T>`** | a dynamic array — **first choice** |
| **`std::unique_ptr<T>`** | one owner — **the default smart pointer**, zero overhead |
| `std::shared_ptr<T>` | genuinely shared ownership; costs an atomic count |
| raw `T*` | a **non-owning observer** only — never `delete` it |

## ✏️ Exercises

**1. (Leaks and ownership.)** (a) What happened in §2 and why is nothing reported? (b) Why must `new`/`delete` forms match? (c) What does "ownership" mean? (d) When is `new` justified?

> [!example]- Solution
> **(a) The pointers went out of scope; the objects did not.**
>
> *(Verified: 5 constructed, **0 destructed**, 5 still live.)*
>
> **`Res* r` is an automatic variable holding an address.** At the end of each iteration `r` is destroyed — but destroying a pointer does nothing to what it points at. **The object remains allocated with no handle to it, so it can never be freed.**
>
> **Nothing is reported because nothing is wrong from the language's point of view.** Allocating is legal; not deallocating is legal. **There is no rule being broken** — which is why this is a *design* error rather than a detectable fault.
>
> **The consequence scales with time, not with correctness.** A leak in a script that runs for a second is invisible. **The same leak in a server handling requests grows until the process is killed** — and the crash appears as an out-of-memory condition with no connection to the code responsible.
>
> *(Tools — Valgrind, AddressSanitizer, MSVC's `_CrtDumpMemoryLeaks` — do find these, but after the fact. The structural fix is §§5–6.)*
>
> **(b) Because `new[]` records how many objects it made, and the two forms free differently.**
>
> **`new Res[4]` must run four destructors and free one block; `new Res` runs one and frees a differently-sized block.** *(Verified: `delete[]` on an array of 4 ran **all four** destructors.)*
>
> **`delete` on an array is undefined behaviour**: typically one destructor runs — leaking anything the other three held — and the block is released with the wrong bookkeeping, **corrupting the heap's own metadata.**
>
> **The crash then appears at the *next* allocation**, in unrelated code. **A stack trace pointing at correct code is worse than none**, because it directs attention to the wrong place. *(That is why this is described rather than demonstrated here — running it would prove nothing about where the fault was.)*
>
> **`std::vector` removes the question**: there is no form to mismatch.
>
> **(c) Ownership is the answer to "whose job is it to free this?"**
>
> **C++ does not track it.** A `T*` may be an owner, a borrowed view, an element of someone else's array, or null — **and the type is identical in every case.** So ownership lives in documentation and convention, which is exactly why it is got wrong.
>
> **The failures are the three this chapter and [[07 - Structs and Classes|ch. 07]] cover:** nobody frees it (**leak**), two owners free it (**double free**), or someone frees it while another still points at it (**dangling pointer**).
>
> **Smart pointers put ownership into the type**, which is the whole point: **`unique_ptr` says "exactly one owner" and enforces it by being non-copyable; `shared_ptr` says "shared" and counts; a raw `T*` should then mean "observer, not owner" by convention.**
>
> **(d) When the object must outlive its scope, or its size/count/type is not known at compile time.**
>
> - **Lifetime exceeds scope** — a factory returning an object the caller keeps.
> - **Size unknown at compile time** — but this is `std::vector`'s job, not yours.
> - **Polymorphic objects** — you need a pointer or reference for `virtual` dispatch ([[09 - Inheritance and Polymorphism|ch. 09]]), and the concrete type may vary.
> - **Very large objects** that would overflow the stack.
>
> **And even then, `new` should appear as `make_unique` or `make_shared`, not raw.** In modern application code an explicit `delete` is close to a code smell.

**2. (Hard — the Rule of Three.)** (a) Why all three together? (b) Why is self-assignment a real problem? (c) Why does allocation order matter? (d) Rule of Zero versus Rule of Three?

> [!example]- Solution
> **(a) Because needing any one implies the class manages a resource, and the other two must handle it too.**
>
> **A destructor means the class owns something.** If it owns something, **the compiler-generated copy constructor and copy assignment — which are member-wise ([[07 - Structs and Classes|ch. 07]] §2) — will copy the handle rather than the resource**, giving two owners.
>
> *(Verified in [[07 - Structs and Classes|ch. 07]] §5: aliasing, dangling, double free — three bugs from one missing function.)*
>
> **Conversely, if you wrote a correct copy constructor, the resource is being duplicated, so it must also be released — hence a destructor.** **The three are one decision, not three.**
>
> **⚠️ The dangerous case is declaring one and forgetting the others**, because the compiler silently supplies the rest and they do the wrong thing. **`= delete` the ones you do not want**, so the mistake becomes a compile error.
>
> *(With move constructor and move assignment it is the **Rule of Five**. Declaring any of the five suppresses some of the others in ways that are easy to get wrong — another argument for §5.)*
>
> **(b) Because it happens through aliases, not because anyone writes `a = a`.**
>
> *(Verified: with the guard, `a = a` left `a.data[3]` intact at 3.)*
>
> **Nobody writes literal self-assignment. It arises indirectly:** `v[i] = v[j]` when `i == j`; `*p = *q` when the pointers alias; passing the same object as both arguments to a swap or copy helper. **None of these looks like self-assignment at the call site.**
>
> **Without the guard the sequence is fatal:**
> ```cpp
> delete[] data;                     // frees the buffer
> data = new int[o.n];               // o IS *this -- o.n is now garbage
> for (…) data[i] = o.data[i];       // copies from freed memory into itself
> ```
> **It corrupts the object and reads freed memory**, and it only triggers when the alias occurs — **so it passes every test that does not happen to alias.**
>
> **(c) Because if allocation throws, the object must survive unchanged.**
>
> The implementation allocates first:
> ```cpp
> int* fresh = new int[o.n];   // may throw std::bad_alloc
> …copy into fresh…
> delete[] data;               // only now release the old
> data = fresh;
> ```
> **If `new` throws, control leaves before `delete[]`, and the object still holds its original valid buffer.** That is the **strong exception guarantee**: the operation either succeeds completely or has no effect ([[11 - Exception Handling and RAII|ch. 11]]).
>
> **Reversing the two lines forfeits it silently.** Freeing first and then throwing leaves the object holding a dangling pointer — **and its destructor will later `delete[]` it again.** The class is now a double-free waiting for an out-of-memory condition, which is exactly when you can least afford another failure.
>
> **This is a case where the *order* of two lines is the difference between exception-safe and catastrophically unsafe**, with no visual cue. *(The copy-and-swap idiom — copy the argument by value, then `swap` — gets both self-assignment safety and the strong guarantee automatically, and is the reason it is the recommended form.)*
>
> **(d) The Rule of Zero, always, unless you are implementing a resource wrapper.**
>
> *(Verified: `struct RuleOfZero { std::vector<int> data; };` declares **nothing** and copies correctly.)*
>
> | | Rule of Three | Rule of Zero |
> |---|---|---|
> | code to write | 3–5 functions | **none** |
> | self-assignment | your problem | handled |
> | exception safety | your problem | handled |
> | move operations | must be added | free |
> | opportunities to err | many | **none** |
>
> **The Rule of Three is still worth understanding**, because you will read code that needs it — every container and smart pointer is written that way — and because it explains *why* the library types behave as they do.
>
> **But writing it in application code is choosing to redo work the standard library has already done correctly.** The modern position: **resource management belongs in a small number of well-tested wrapper types; everything else composes them.**

**3. (RAII.)** (a) Explain the leak-on-exception result. (b) Why does `unique_ptr` not leak? (c) `unique_ptr` vs `shared_ptr`? (d) What is the chapter's general lesson?

> [!example]- Solution
> **(a) The `throw` skipped the `delete`.**
>
> *(Verified: raw `new` + throw → **live = 1, leaked**; `make_unique` + throw → **live = 0, freed**.)*
>
> ```cpp
> Res* r = new Res("raw");
> throw std::runtime_error("boom");
> delete r;                  // never reached
> ```
> **Control transfers to the handler immediately**, and every statement between the throw and the end of the function is skipped. **MSVC even said so — `C4702: unreachable code`** — though in real code the throw is usually inside a called function, where no such warning is possible.
>
> **This is why manual cleanup is so hard to get right.** It is not just `throw`: an early `return`, a `break`, or any function that might throw creates another exit path. **A function with five allocations and three early returns needs fifteen `delete`s in the right order** — and one missing path is a leak nobody will find.
>
> **(b) Because its destructor runs during stack unwinding.**
>
> **When an exception propagates, C++ destroys every automatic object in each scope it leaves** — [[07 - Structs and Classes|ch. 07]] §2's guarantee, and it holds on *every* exit path, not just normal returns.
>
> **`unique_ptr` is an automatic object whose destructor calls `delete`.** So the cleanup happens without any statement to skip. **There is no line for the `throw` to jump over.**
>
> **This is RAII: tie a resource's lifetime to an object's lifetime**, and the language's existing guarantee about object lifetime does the work. **It applies far beyond memory** — `std::lock_guard` for mutexes, `std::fstream` for files, and any wrapper you write yourself.
>
> **And it is why C++ has no `finally`.** A `finally` block is a way to say "run this on every exit path"; **a destructor already does that, and it does it once at the type level rather than at every call site.** *(Python's `__del__` runs at an unspecified time under GC, which is why it needs `with`.)*
>
> **(c)**
>
> | | `unique_ptr` | `shared_ptr` |
> |---|---|---|
> | owners | **exactly one** | many |
> | copyable | **no — compile error** | yes |
> | transfer | `std::move` | copy |
> | overhead | **none** (pointer-sized) | control block + **atomic** refcount |
> | frees when | the owner is destroyed | **the last owner is destroyed** |
>
> *(Both verified: `unique_ptr` moved and freed at scope exit; `shared_ptr` showed `use_count` 1 → 2 → 1 → 0, freeing only at 0.)*
>
> **Default to `unique_ptr`.** It is free, and **its non-copyability turns [[07 - Structs and Classes|ch. 07]]'s double free into a compile error** — the invalid state is unrepresentable rather than merely detected.
>
> **Use `shared_ptr` only when ownership is genuinely shared** and no single owner can be identified. **The costs are real**: an allocation for the control block, an atomic increment/decrement per copy (which does not scale well across threads), **and reference cycles leak** — two objects holding `shared_ptr`s to each other never reach count 0, which needs `weak_ptr` to break.
>
> **Reaching for `shared_ptr` because ownership is unclear is a design smell**, not a solution.
>
> **(d) Make the resource's lifetime the object's lifetime, and let the language enforce it.**
>
> **Every failure in this chapter is a *manual* step someone must remember:** free it (§2), match the form (§3), copy it deeply (§4), free it on every exit path (§7). **Every fix removes the step rather than making it easier to remember.**
>
> | manual step | how it is removed |
> |---|---|
> | remember to `delete` | destructor runs automatically |
> | match `delete`/`delete[]` | `vector` — no form to match |
> | write three copy functions | **Rule of Zero** — members already correct |
> | delete on every exit path | RAII — unwinding runs destructors |
> | avoid two owners | `unique_ptr` — **compile error** |
>
> **This is the same principle the vault has now met in four subjects:** [[01 - Fundamentals - Types, Variables and Expressions|`const`]] making an invalid assignment a compile error; [[Database Management Systems/contents/01 - Databases and Data Models|DBMS]]'s constraints converting corruption into errors; [[Database Management Systems/contents/04 - Normalization|normalisation]] restricting the representable states rather than the answerable questions.
>
> **The strongest fix is never "be careful". It is to make the mistake unrepresentable.**

## 📝 Summary

- **A stack object is destroyed automatically; a heap object only when you say so.** That single difference generates the whole chapter.
- **⚠️ The leak: 5 objects allocated, 5 pointers lost, 0 destructed** *(verified)*. **No error, no warning, no crash** — the program simply uses memory it can never reclaim.
- **`new` ↔ `delete`, `new[]` ↔ `delete[]`, never crossed** *(verified: `delete[]` ran all 4 destructors)*. Mismatching corrupts the heap, and the crash lands somewhere unrelated.
- **The Rule of Three: destructor, copy constructor, copy assignment — need one, need all three** *(verified: correct copies gave different buffers and left the source untouched)*.
- **⚠️ Self-assignment arises through aliases** (`v[i] = v[j]`), not because anyone writes `a = a`. **Without a guard, `operator=` frees its own buffer then copies from freed memory** *(verified: with the guard, `a = a` survived)*.
- **⚠️ Allocate before releasing.** If `new` throws, the object is left intact — the **strong exception guarantee**. **Reversing two lines forfeits it silently.**
- **The Rule of Zero: hold a `vector` and declare nothing** *(verified: correct deep copy, zero special members)*. **This is the right default.**
- **`unique_ptr` is not copyable, so [[07 - Structs and Classes|ch. 07]]'s double free becomes a compile error** *(verified: move transfers ownership, `u` becomes null, freed at scope exit)*. **Zero overhead.**
- **`shared_ptr` counts owners** *(verified: 1 → 2 → 1 → 0, freed only at 0)* — correct when ownership is genuinely shared, at the cost of an atomic count, and **cycles leak**.
- **⚠️ The decisive result: raw `new` + exception = LEAKED (live = 1); `make_unique` + exception = freed (live = 0)** *(verified)*. **The `throw` skipped the `delete`; the destructor still ran during unwinding.**
- **That is RAII, and it is why C++ needs no `finally`.**
- **Every fix in this chapter removes a manual step rather than making it easier to remember** — the same principle as [[01 - Fundamentals - Types, Variables and Expressions|`const`]] and [[Database Management Systems/contents/01 - Databases and Data Models|database constraints]]: **make the mistake unrepresentable.**

## ⚠️ Important Notes

1. **Prefer `std::vector` to `new[]`, always.** It removes leaks, form-mismatches and the Rule of Three at once.
2. **Prefer `std::unique_ptr` to raw `new`.** Zero overhead, and double ownership becomes a compile error.
3. **Use `std::make_unique` / `std::make_shared`, not raw `new`.** They are exception-safe and say what they mean.
4. **⚠️ An explicit `delete` in application code is a smell.** If you are writing one, ask what should have owned the object.
5. **A raw `T*` should mean "non-owning observer".** Never `delete` through one.
6. **⚠️ If you declare a destructor, copy constructor or copy assignment, declare all three** — and `= delete` the ones you do not want.
7. **Always guard `operator=` against self-assignment**, or use copy-and-swap, which handles it structurally.
8. **⚠️ Allocate the replacement before releasing the original.** The line order is the difference between exception-safe and double-free-prone.
9. **Prefer copy-and-swap for assignment operators** — it gives self-assignment safety and the strong guarantee free.
10. **Default to `unique_ptr`; use `shared_ptr` only for genuine shared ownership.** Reaching for it because ownership is unclear is a design problem.
11. **`shared_ptr` cycles leak.** Break them with `weak_ptr`.
12. **Remember destructors run during exception unwinding.** That is what makes RAII work and manual cleanup unnecessary.
13. **Never write cleanup code on multiple exit paths.** Wrap the resource instead — the pattern extends to files, locks and handles.
14. **Run a leak detector** (AddressSanitizer, Valgrind, `_CrtDumpMemoryLeaks`) — but treat leaks found as a design signal, not something to patch with an extra `delete`.

> [!warning] Gaps in the source material
> **Malik ch. 12 extracts well** — pointer declaration and dereferencing, `new`/`delete`, dynamic arrays, shallow versus deep copy, the destructor discussion, and pointer arithmetic all came through readably, with listings intact. **Book page $n$ = PDF page $n+50$; ch. 12 is PDF pages 867–942.** *(Standing quirk: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost** — and for this chapter that is the **most significant loss in the subject**, because pointer diagrams (boxes and arrows showing two pointers into one buffer) are the conventional teaching device. **§§4 and 6 substitute printed addresses and live-object counts from running programs**, which show the same relationships as facts rather than pictures: two identical addresses *is* the aliasing diagram.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 12.**
>
> **Additions beyond the source.** **Malik covers pointers, `new`/`delete`, and shallow-versus-deep copy thoroughly for a first course — it is the strongest chapter in the book for this material. What is added is instrumentation and the modern answer:**
>
> - **§2's leak is instrumented rather than described** — a live-object counter showing **5 constructed, 0 destructed** makes "leak" a number instead of a warning.
> - **§4's self-assignment and allocation-order discussion is mine.** Malik presents the copy constructor and `operator=`; **the point that self-assignment arrives through aliases like `v[i] = v[j]` rather than literal `a = a`, and that allocating before releasing is what provides the strong exception guarantee, are additions** — as is the observation that **reversing two lines forfeits exception safety with no visual cue.**
> - **§§5–6 are entirely absent from Malik**, which predates the modern consensus. **`unique_ptr`, `shared_ptr`, `make_unique`, the Rule of Zero and the Rule of Five are all additions** per the subject file's instruction to give the modern form.
> - **⚠️ §7 is the chapter's centrepiece and is my own.** Running the same function with raw `new` and with `make_unique`, both throwing before cleanup, gives **live = 1 versus live = 0** — and MSVC's `C4702: unreachable code` on the skipped `delete` is a bonus confirmation. **This makes the case for RAII as a measurement rather than an assertion**, and connects [[07 - Structs and Classes|ch. 07]] §2's destructor guarantee to its practical payoff.
> - **The framing that every fix *removes a manual step* rather than making it easier to remember**, and its connection to [[01 - Fundamentals - Types, Variables and Expressions|`const`]] and [[Database Management Systems/contents/01 - Databases and Data Models|database constraints]] as the same principle across four subjects, is my own.
>
> **Deliberately compressed.** **Pointer arithmetic** (`p + 1`, `p - q`, pointer comparison) is not developed — it is [[06 - Arrays, C-Strings and std vector|ch. 06]]'s array decay in another form, and modern code uses iterators and ranges. **Pointers to functions** are deferred; the modern equivalent is `std::function` and lambdas. **Malik's linked-list-building examples** are excluded by the scope decision in `00-Index.md` — **[[Data Structures and Algorithms/contents/06 - Linked Lists|DSA ch. 06]] owns linked lists**, and what C++ adds is exactly the ownership question this chapter covers directly. **`virtual` destructors and abstract classes** (also in Malik ch. 12) are deferred to [[09 - Inheritance and Polymorphism|ch. 09]], where inheritance makes them meaningful. **Copy-and-swap is described but not implemented**, since the explicit form shows the failure modes more clearly.

**Previous:** [[07 - Structs and Classes]] · **Next:** [[09 - Inheritance and Polymorphism]]
