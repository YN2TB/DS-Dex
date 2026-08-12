---
subject: Basic Programming (C++)
chapter: 7
tags: [ds, cpp, classes, structs, encapsulation, constructors, special-members, shallow-copy, padding]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 9–10"
---

# Structs and Classes

**The compiler writes several member functions for you, and whether they are correct depends entirely on what your members are.**

That is this chapter's real content. §2 shows a struct with *nothing* declared getting a default constructor, copy constructor, copy assignment, move operations and a destructor — **all correct**, because its members (`string`, `vector`) manage themselves.

**§5 changes one member to a raw pointer and the same generated copy becomes catastrophic**: two objects silently share one buffer, modifying one changes the other, and the second destructor frees memory that is already gone.

**That is the bridge to [[08 - Pointers and Dynamic Memory|ch. 08]]** — the Rule of Three exists precisely because the compiler's default is a *member-wise* copy, which is right for values and wrong for ownership.

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17 /W4`).

## 📘 Main Knowledge

### 1. `struct` versus `class` — one difference

*(Verified:)*
```cpp
struct SPoint { int x; int y; };        // members PUBLIC by default
class  CPoint { int x; int y; ... };    // members PRIVATE by default
```
```
s.x        = 1     (direct access)
c.getX()   = 3     (needs an accessor)
```

> [!note] That is the *only* language difference
> **Default member access, and default inheritance access.** Nothing else. A `struct` can have constructors, private members, virtual functions and inheritance; a `class` can be entirely public.
>
> **The distinction is conventional**: `struct` for passive aggregates with no invariant to protect, `class` when the object must maintain something. **Choosing by that convention communicates intent**, which is its whole value.

### 2. The members the compiler writes for you

```cpp
struct Plain { int a; std::string s; std::vector<int> v; };
```
**Declared: nothing. Available: default constructor, copy constructor, copy assignment, move constructor, move assignment, destructor.**

*(Verified: `Plain q = p;` produced a genuine deep copy — `q.s = "hello"`, `q.v.size() = 3`.)*

> [!note] The generated copy is *member-wise*, and here that is correct
> **It copies each member using that member's own copy operation.** `std::string` and `std::vector` copy their contents properly, so the whole object copies properly. **You get correct value semantics for free.**
>
> **This is why modern C++ says "prefer members that manage themselves".** Build a class out of `string`, `vector` and smart pointers and **you need to write none of the special members at all** — the "Rule of Zero".

**Destructors fire automatically, in reverse order of construction** *(verified: 3 objects constructed, 3 destructors run at scope exit)*.

> [!note] This is the mechanism behind RAII
> **Scope exit is deterministic and guaranteed**, including when an exception unwinds the stack. **That is what [[11 - Exception Handling and RAII|ch. 11]] is built on, and why C++ needs no `finally`.**

### 3. Initialiser lists versus assigning in the body

*(Verified — counting constructor and assignment calls on a member:)*

| | constructor calls | assignment calls |
|---|---|---|
| **`UsesInitList() : m("via init list") {}`** | **1** | **0** |
| `UsesBody() { m = Member("via body"); }` | **2** | **1** |

> [!warning] The body version constructs the member twice
> **Members are constructed *before* the constructor body runs.** So assigning in the body **default-constructs the member first, then throws that value away** and assigns over it — strictly more work, and it requires the member to *be* default-constructible.
>
> **The initialiser list builds it once, directly, with the right value.**
>
> **And for `const` members and references it is not an optimisation but the only option** — they cannot be assigned after construction, so a body assignment does not compile.
>
> *(One subtlety: members are initialised in **declaration order**, not the order written in the list. Writing them out of order compiles, may warn, and can read an uninitialised member.)*

### 4. `const` member functions

```cpp
int value() const { ++reads; return n; }    // 'reads' is mutable
```
*(Verified: `value()` callable on a `const Counter&`; `increment()` is not; a `mutable` member changed inside a `const` function.)*

> [!note] `const` is part of the signature, and it is what makes [[05 - Functions and Scope|ch. 05]] work
> **A `const&` parameter can only call `const` member functions.** So if your accessors are not marked `const`, **callers cannot pass your object by `const&` at all** — they are forced into a copy, which is exactly what [[05 - Functions and Scope|ch. 05]] §3 measured as wasteful.
>
> **Mark every member function `const` that does not modify observable state.** `mutable` is the escape hatch for members that are genuinely implementation detail — caches, counters, mutexes.

### 5. ⚠️ Where the generated copy is catastrophic

```cpp
struct ShallowBuf {
    int* data;  std::size_t n;
    ShallowBuf(std::size_t sz) : data(new int[sz]), n(sz) { … }
    ~ShallowBuf() { delete[] data; }
    // no copy constructor declared -> compiler writes a member-wise one
};
```

*(Verified:)*
```
a.data = 0000026D014DA600,  a.data[0] = 0
b = a;   b.data = 0000026D014DA600      <- THE SAME ADDRESS
b.data[0] = 999   ->   a.data[0] = 999  <- 'a' changed too
```

**Then `b`'s destructor runs and calls `delete[]` on the shared buffer.**

> [!warning] Three bugs from one missing function
> 1. **Aliasing.** `a` and `b` share one array, so modifying either changes both — **`b = a` looks like a copy and is not.**
> 2. **Dangling pointer.** After `b` is destroyed, `a.data` points at freed memory.
> 3. **Double free.** `a`'s destructor will `delete[]` the same block again — **heap corruption, usually crashing somewhere unrelated.**
>
> *(The demonstration deliberately nulls `a.data` before exiting, to avoid the crash. **Nothing in the language prevented any of this** — the copy constructor was generated silently and is perfectly legal.)*
>
> **The generated copy is member-wise: it copies the *pointer*, not what it points to.** For `string` and `vector` that is right, because their own copy operations do the work. **For a raw pointer it copies a *reference to ownership* that was never meant to be shared.**
>
> **This is precisely why [[08 - Pointers and Dynamic Memory|ch. 08]]'s Rule of Three exists** — and why the modern answer is to hold a `std::vector` or smart pointer instead, so the question never arises.

### 6. Layout and padding

*(Verified:)*
```
struct Padded { char a; int b; char c; };   sizeof = 12
struct Packed { int b; char a; char c; };   sizeof =  8
raw member sizes (1+4+1)                             6

offsets in Padded:  a = 0,  b = 4,  c = 8
```

> [!note] Reordering members saved 33% for free
> **An `int` must sit on a 4-byte boundary**, so the compiler inserts **3 bytes of padding after `a`** — visible in the offsets (`a` at 0, `b` at 4, not 1).
>
> **Declaring members largest-first packs them tightly** and cost nothing but the edit.
>
> **It matters at scale.** A million-element array of `Padded` wastes 4 MB against `Packed` — and, per [[06 - Arrays, C-Strings and std vector|ch. 06]] §7, a smaller object means **more of them per cache line**, so the saving compounds into speed.

## ✏️ Exercises

**1. (Generated members.)** (a) What does the compiler write, and when is it right? (b) Why do destructors matter here? (c) Explain the init-list result. (d) Why mark member functions `const`?

> [!example]- Solution
> **(a) Default constructor, copy constructor, copy assignment, move constructor, move assignment, and destructor** — and the copy operations are **member-wise**: each member is copied using its own copy operation.
>
> *(Verified: `struct Plain { int a; std::string s; std::vector<int> v; };` with nothing declared produced a genuine deep copy.)*
>
> **It is right whenever every member manages itself.** `std::string` copies its characters; `std::vector` copies its buffer; `int` copies its value. **Member-wise copying of correct members gives a correct whole.**
>
> **It is wrong when a member is a raw pointer that owns something** (§5), because copying the pointer copies a *reference to ownership* rather than the resource.
>
> **The modern conclusion is the "Rule of Zero": build classes out of self-managing members and declare none of the special functions.** Declaring one correctly usually means declaring all of them, which is [[08 - Pointers and Dynamic Memory|ch. 08]]'s subject — and avoiding that is better than doing it well.
>
> **(b) Because scope exit is deterministic, which is the foundation of RAII.**
>
> *(Verified: three objects constructed, three destructors run at scope exit, in reverse order.)*
>
> **Reverse order matters** because later objects may depend on earlier ones — destroying in reverse guarantees a dependency is still alive while its dependent is being torn down.
>
> **And it happens on *every* exit path**, including an exception unwinding the stack. **That is why C++ has no `finally`**: a destructor already runs, guaranteed, and [[11 - Exception Handling and RAII|ch. 11]] builds on exactly this.
>
> **Contrast Python**, where `__del__` runs at an unspecified time under garbage collection — which is why Python needs `with` and context managers to get deterministic cleanup.
>
> **(c)**
>
> | | ctor calls | assign calls |
> |---|---|---|
> | initialiser list | **1** | **0** |
> | assignment in body | **2** | **1** |
>
> *(Verified.)*
>
> **Members are constructed before the constructor body begins.** So the body version:
> 1. default-constructs the member (call 1),
> 2. constructs a temporary with the wanted value (call 2),
> 3. assigns it over the default (the assignment),
> 4. destroys the temporary.
>
> **The initialiser list does step 2 only** — it constructs the member directly with the right value.
>
> **Three consequences beyond the cost:**
> - **`const` members and references *must* use the init list** — they cannot be assigned after construction, so the body form does not compile.
> - **A member with no default constructor forces the init list** for the same reason.
> - **⚠️ Members are initialised in declaration order, not list order.** Writing them out of order compiles and can read an uninitialised member — a real bug that `/W4` flags but which is easy to introduce while reordering.
>
> **(d) Because a `const&` parameter can only call `const` member functions.**
>
> *(Verified: `value() const` was callable on a `const Counter&`; `increment()` was not.)*
>
> **[[05 - Functions and Scope|Ch. 05]] established that `const&` is the default way to pass non-trivial objects** — no copy, no modification. **But that only works if the class offers `const` accessors.** A class whose getters are not `const` forces every caller to take it by value, **reintroducing exactly the copy cost ch. 05 measured.**
>
> **So `const`-correctness is not decoration: it is what makes efficient interfaces possible**, and it propagates — one missing `const` deep in a call chain forces copies all the way up.
>
> **`mutable` is the deliberate exception**, for members that are implementation detail rather than observable state — a memoised result, a hit counter *(verified: a `mutable` counter incremented inside a `const` function)*, a mutex. **The test is whether a caller could tell**: if not, `mutable` is honest.

**2. (Hard — the shallow copy.)** (a) What are the three bugs? (b) Why is the compiler's behaviour reasonable? (c) Why is this worse than a crash? (d) What is the fix?

> [!example]- Solution
> **(a) Aliasing, a dangling pointer, and a double free — all from one missing function.**
>
> *(Verified: `b = a` gave `b.data` **the same address** as `a.data`; setting `b.data[0] = 999` changed `a.data[0]` to 999.)*
>
> 1. **Aliasing.** `b = a` reads as "make a copy" and does not — the two objects share one buffer, so a change through either is visible through both. **Every function taking `ShallowBuf` by value now silently mutates its caller's data.**
> 2. **Dangling pointer.** When `b` is destroyed it calls `delete[]` on the shared buffer. **`a.data` now points at freed memory**, and reading it is [[05 - Functions and Scope|ch. 05]]'s dangling-reference problem again.
> 3. **Double free.** `a`'s destructor calls `delete[]` on the same block. **This corrupts the heap's own bookkeeping**, and the crash usually appears later, in unrelated correct code — the hardest kind of bug to attribute.
>
> **(b) Because member-wise copying is the only thing it could reasonably do, and it is right in the common case.**
>
> **The compiler cannot know what a pointer means.** `int* data` might be an owned array, a borrowed view, a pointer to a shared cache, or an index into someone else's buffer. **Only the copy semantics for the *owned* case involve allocating a new array** — and guessing wrong in the other direction would be equally bad.
>
> **So it does the one thing that is defensible without knowledge: it copies each member.** And for `string`, `vector` and smart pointers **that is exactly right**, because those members encode their own ownership semantics.
>
> **The problem is not the rule; it is a raw pointer's failure to say what it means.** *(This is why `std::unique_ptr` is not copyable and `std::shared_ptr` is — each states its ownership model in the type, so member-wise copying does the right thing automatically.)*
>
> **(c) Because two of the three bugs are silent and the third crashes somewhere else.**
>
> **The aliasing produces no diagnostic at all** — the program runs, and a value changes that "shouldn't have". This is the vault's recurring shape: [[06 - Arrays, C-Strings and std vector|ch. 06]]'s clobbered neighbour, [[05 - Functions and Scope|ch. 05]]'s plausible dangling value, [[Database Management Systems/contents/00-Index|DBMS]]'s silently inflated joins.
>
> **The double free does usually crash — but not at the fault.** It corrupts heap metadata, and the failure surfaces at the *next* allocation, which may be in a completely different module. **A stack trace pointing at correct code is worse than no information**, because it sends you to the wrong place.
>
> **And it is timing- and layout-dependent**, so it may not reproduce under a debugger.
>
> **(d) Three options, in increasing order of preference.**
>
> **1. Declare the copy operations correctly** — [[08 - Pointers and Dynamic Memory|ch. 08]]'s **Rule of Three**: if you need a destructor, a copy constructor, or copy assignment, you almost certainly need all three. *(With move operations it becomes the Rule of Five.)*
>
> **2. Forbid copying** — `ShallowBuf(const ShallowBuf&) = delete;`. **Turns the silent bug into a compile error**, which is the [[01 - Fundamentals - Types, Variables and Expressions|`const` principle]] again: make the invalid operation unrepresentable.
>
> **3. ✅ Don't own a raw pointer.** Replace `int* data; size_t n;` with **`std::vector<int> data;`** — and now the compiler-generated copy is correct, the destructor is unnecessary, there is nothing to double-free, and the size travels with the data ([[06 - Arrays, C-Strings and std vector|ch. 06]]).
>
> **Option 3 is the modern answer**, and it is the Rule of Zero: **the best way to get resource management right is to delegate it to a member that already does.**

**3. (Layout.)** (a) Why is `Padded` 12 bytes? (b) What did reordering save? (c) When does it matter? (d) What is the general lesson of this chapter?

> [!example]- Solution
> **(a) Alignment padding.**
>
> *(Verified: `sizeof(Padded)` = **12**, against 6 bytes of actual members. Offsets: `a` = 0, `b` = **4**, `c` = 8.)*
>
> **An `int` must be stored at an address that is a multiple of 4** — most architectures require it, and all penalise misalignment. So after `char a` at offset 0, **3 bytes of padding** are inserted so `b` lands on offset 4.
>
> **Then `c` sits at offset 8, and the struct is padded to 12** so that an *array* of `Padded` keeps every element aligned — the struct's size must be a multiple of its strictest member's alignment.
>
> **(b) 33%.** *(Verified: `Packed { int b; char a; char c; }` is **8** bytes.)*
>
> **Declaring the `int` first means the two `char`s pack into the gap after it**: 4 + 1 + 1 = 6, padded to 8. **Same members, same types, same semantics — one third less memory, for the cost of reordering a declaration.**
>
> **The general rule: declare members in decreasing size order.** It is close to optimal and requires no analysis.
>
> **(c) At scale, and then it compounds into speed.**
>
> **For one object, 4 bytes is nothing.** For an array of a million, `Padded` wastes **4 MB**.
>
> **And the memory saving becomes a speed saving**, by [[06 - Arrays, C-Strings and std vector|ch. 06]] §7's mechanism: **a 64-byte cache line holds 5 `Padded` objects but 8 `Packed` ones.** A traversal therefore fetches 37% fewer lines — which is the same argument that made row-major traversal 2.5× faster.
>
> **So padding is not just a memory question**; it is a locality question, and locality is the one that showed up as 2.5×.
>
> *(Caveats: never reorder members to save bytes at the cost of a sensible grouping in code people read; and `#pragma pack` — which removes padding entirely — buys size at the cost of misaligned access, which is slower and on some architectures a fault.)*
>
> **(d) The compiler does a great deal on your behalf, and the question is always whether its defaults match your intent.**
>
> **Each section is an instance:**
>
> | the compiler | correct when | wrong when |
> |---|---|---|
> | generates copy operations (§2) | members manage themselves | a member is an owning raw pointer (§5) |
> | constructs members before the body (§3) | you use the initialiser list | you assign in the body — double work |
> | enforces `const` (§4) | you mark accessors `const` | you don't — callers are forced to copy |
> | inserts padding (§6) | always — it is required | you declared members in a wasteful order |
>
> **In every case the default is defensible and silent**, and in every case you can do better by stating your intent explicitly.
>
> **The unifying advice is the Rule of Zero: choose members whose own semantics are already right, and the generated defaults become correct automatically.** That is a stronger position than writing the special members well — it removes the opportunity to write them badly.

## 📝 Summary

- **`struct` and `class` differ only in default access** *(verified)* — everything else is convention: `struct` for passive data, `class` when there is an invariant.
- **The compiler generates six special members**: default constructor, copy constructor, copy assignment, move constructor, move assignment, destructor. **The copies are *member-wise*.**
- **That is correct when members manage themselves** *(verified: a struct of `int`/`string`/`vector` copied deeply with nothing declared)* — the **Rule of Zero**.
- **Destructors run automatically at scope exit, in reverse order of construction** *(verified: 3 objects, 3 destructors)* — the basis of RAII and why C++ needs no `finally`.
- **Initialiser lists construct once; assigning in the body constructs twice.** *(Verified: **1 ctor / 0 assigns** vs **2 ctors / 1 assign**.)* **For `const` members and references the init list is the only option.**
- **⚠️ Members are initialised in declaration order, not list order.**
- **`const` member functions are what make `const&` parameters usable** — without them callers are forced to copy, reintroducing [[05 - Functions and Scope|ch. 05]]'s measured cost. **`mutable` is the escape hatch for non-observable state.**
- **⚠️ With a raw owning pointer, the generated copy causes three bugs at once** *(verified: `b = a` gave the **same address**, and `b.data[0] = 999` changed `a.data[0]`)*: **aliasing, a dangling pointer, and a double free.**
- **The compiler's behaviour is reasonable** — it cannot know what a pointer means, and member-wise copying is right for `string`, `vector` and smart pointers. **The fault is the raw pointer not stating its ownership.**
- **Fixes, best last: write the Rule of Three; `= delete` the copy; or ✅ hold a `std::vector`/smart pointer so the question never arises.**
- **Padding: `{char, int, char}` is 12 bytes; `{int, char, char}` is 8** *(verified — offsets 0, 4, 8)*. **Reordering saved 33% for free**, and at scale it compounds into cache-line efficiency ([[06 - Arrays, C-Strings and std vector|ch. 06]] §7).

## ⚠️ Important Notes

1. **Prefer the Rule of Zero**: build classes from `string`, `vector` and smart pointers, and declare none of the special members.
2. **⚠️ If you declare a destructor, a copy constructor, or copy assignment, you probably need all three** ([[08 - Pointers and Dynamic Memory|ch. 08]]'s Rule of Three; five with moves).
3. **⚠️ Never let a class own a raw pointer.** Member-wise copying will alias it, dangle it, and double-free it — silently.
4. **`= delete` the copy operations** when copying makes no sense. A compile error beats a runtime disaster.
5. **Always use the constructor initialiser list**, never assignment in the body. It is faster and it is the only option for `const` members and references.
6. **⚠️ List initialisers in declaration order** — that is the order they actually run in.
7. **Mark every member function `const` that does not change observable state.** Omitting it forces callers to copy.
8. **Use `mutable` only for state a caller could not observe** — caches, counters, mutexes.
9. **Declare members largest-first.** It costs one edit and can save a third of the memory.
10. **Avoid `#pragma pack` unless a binary format demands it** — misaligned access is slower and on some architectures faults.
11. **Use `struct` for aggregates with no invariant and `class` when there is one.** The compiler does not care; readers do.
12. **Remember destructors run on every exit path, including exceptions** — that guarantee is what [[11 - Exception Handling and RAII|ch. 11]] is built on.

> [!warning] Gaps in the source material
> **Malik ch. 9–10 extract well** — `struct` declaration and member access, arrays of structs, the class construct, access specifiers, constructors and destructors, and the accessor/mutator discussion all came through readably, with listings intact. **Book page $n$ = PDF page $n+50$; ch. 9–10 are PDF pages 661–792.** *(Standing quirk: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost** — the object-layout diagrams and the UML-style class diagrams. **§6 substitutes real `sizeof` values and member offsets printed from a running program**, which shows the layout more precisely than a diagram.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 9–10.**
>
> **Additions beyond the source.** **Malik teaches classes as a first course does: syntax, access specifiers, constructors, and the discipline of accessors. The behavioural material is added:**
>
> - **§2's instrumented count of generated members is mine** — showing that a struct declaring *nothing* still gets six functions, and that the generated copy is genuinely deep when the members are. **The "Rule of Zero" framing is modern practice and not in the book.**
> - **§3's measurement is mine and gives the crisp number**: initialiser list **1 constructor, 0 assignments**; body assignment **2 constructors, 1 assignment**. Malik recommends the initialiser list; **counting the calls shows exactly what it saves**, and the `const`-member argument makes it a requirement rather than a preference.
> - **§5 is the chapter's centrepiece and is entirely mine.** Malik discusses shallow versus deep copy in the pointer chapter; **executing it — showing the identical address, the aliased write, and then the double free — makes all three bugs concrete at once**, and sets up [[08 - Pointers and Dynamic Memory|ch. 08]] directly. **The argument that the compiler's behaviour is *reasonable*** — it cannot know what a pointer means, which is why `unique_ptr`/`shared_ptr` encode ownership in the type — is my own framing.
> - **§6's padding measurement is mine** — `sizeof` 12 versus 8 against 6 bytes of members, with printed offsets proving where the padding sits — as is **the link to [[06 - Arrays, C-Strings and std vector|ch. 06]] §7**: a smaller object means more per cache line, so the memory saving becomes the 2.5× locality effect.
> - **The `const`-correctness argument connecting to [[05 - Functions and Scope|ch. 05]]** — that missing `const` accessors force callers into the copies ch. 05 measured — is mine.
>
> **Deliberately compressed.** **Malik's extended class examples** (`clockType`, `personType`) are not reproduced; they exercise accessor/mutator syntax without exposing behaviour, and later chapters reuse them for inheritance, which [[09 - Inheritance and Polymorphism|ch. 09]] covers with its own examples. **The header/implementation-file split and include guards** are mentioned only in passing — they are build mechanics, and `#pragma once` has largely replaced hand-written guards. **`static` members and friend functions** are deferred: `static` members appear in [[10 - Operator Overloading and Templates|ch. 10]] where they matter, and `friend` is best introduced alongside operator overloading, which is its main legitimate use. **Arrays of structs** are covered implicitly by [[06 - Arrays, C-Strings and std vector|ch. 06]]'s containers.

**Previous:** [[06 - Arrays, C-Strings and std vector]] · **Next:** [[08 - Pointers and Dynamic Memory]]
