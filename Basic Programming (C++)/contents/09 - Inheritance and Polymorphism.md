---
subject: Basic Programming (C++)
chapter: 9
tags: [ds, cpp, inheritance, polymorphism, virtual, object-slicing, vtable, composition]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 11–12"
---

# Inheritance and Polymorphism

**`virtual` is one keyword, and forgetting it produces three different silent failures.**

- **§1** — a non-virtual function redefined in a derived class **hides** rather than overrides, so a base pointer always calls the base version.
- **§2 — object slicing.** Pass a derived object by value as a base and **the derived part is silently cut off**: `sizeof` 16 becomes 8, `area()` returns 0, and it compiles without a murmur.
- **§3** — a **non-virtual destructor**. Deleting through a base pointer ran the base destructor and **not the derived one**: `BaseNV dtors = 1, DerivedNV dtors = 0`. The derived object's `vector` was never freed.

**And §5 is the strangest result in the subject so far:** with default arguments on a virtual function, **the body is chosen dynamically and the default argument statically** — so a single call assembles its two halves from two different classes.

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17 /W4`).

## 📘 Main Knowledge

### 1. `virtual` dispatches on the dynamic type

*(Verified, through a `unique_ptr<Shape>`:)*
```
virtual  name()   -> Circle,  area 3.14159
virtual  name()   -> Square,  area 4
NON-virt nameNV() -> Shape        <- always the BASE version
NON-virt nameNV() -> Shape
```

> [!warning] Redefining a non-virtual function **hides** it; it does not override it
> **A non-virtual call is resolved from the *static* type of the pointer or reference**, exactly like [[05 - Functions and Scope|ch. 05]]'s overload resolution.
>
> **Writing `std::string nameNV() const` in `Circle` creates a new, unrelated function that shadows the base one.** Through a `Shape*` you always get `Shape::nameNV()`. **No error, no warning.**
>
> **`override` is the defence.** Marking a function `override` makes the compiler check that it really does override something — **so a typo in the signature, or a missing `virtual` in the base, becomes a compile error instead of silent hiding.** *(C++11; use it on every override.)*

### 2. ⚠️ Object slicing

```cpp
void byValue(Shape s);         // takes a Shape BY VALUE
void byRef(const Shape& s);
Circle c(1.0);
```
```
c.name()  = Circle,  c.area() = 3.14159
byValue(c) -> Shape,   area 0            <- SLICED
byRef(c)   -> Circle,  area 3.14159      <- correct

sizeof(Shape) = 8   vs   sizeof(Circle) = 16
```
*(All verified.)*

> [!warning] The derived part was cut off, and it compiled silently
> **A `Shape` parameter is 8 bytes; a `Circle` is 16.** Copying a `Circle` into a `Shape` **copies only the base subobject** — `r` is gone, the vtable pointer is reset to `Shape`'s, and `area()` returns the base's 0.
>
> **`vector<Shape>` does the same on `push_back`** *(verified: it reported `Shape`)*. **This is why polymorphic containers must hold pointers** — `vector<unique_ptr<Shape>>`, never `vector<Shape>`.
>
> **The rule follows directly from [[05 - Functions and Scope|ch. 05]]: pass polymorphic types by reference or `const&`, never by value.** There, by-value passing was merely wasteful; **here it changes the answer.**
>
> *(Making the base abstract — a pure virtual function — turns slicing into a compile error, because `Shape` can no longer be instantiated. That is the strongest defence.)*

### 3. ⚠️ The non-virtual destructor

*(Verified — `BaseNV* p = new DerivedNV(); delete p;`:)*

| | base dtors | derived dtors |
|---|---|---|
| **destructor NOT virtual** | 1 | **0** |
| destructor **virtual** | 1 | **1** |

> [!warning] The derived destructor never ran
> **`DerivedNV` held a `vector<int>` of 1 000 elements. It was never freed.** And any other resource the derived class owned — a file handle, a lock, a `unique_ptr` — is leaked identically.
>
> **This is undefined behaviour**, not merely a leak: deleting through a base pointer whose destructor is not virtual is explicitly UB.
>
> **With `virtual`, both ran, derived first** *(verified)* — the reverse of construction order, as [[07 - Structs and Classes|ch. 07]] §2 established.
>
> **The rule: if a class has any virtual function, its destructor must be virtual.** The presence of virtuals means the class is intended to be used polymorphically, which means someone will delete it through a base pointer.
>
> *(The alternative for a base not meant for polymorphic deletion is a **protected non-virtual destructor** — which makes `delete basePtr` a compile error instead.)*

### 4. Calling a virtual function from a constructor

*(Verified — constructing a `CtorDerived`:)*
```
CtorBase ctor calls which(): CtorBase        <- the BASE version
after construction, d.which() = CtorDerived (tag=initialised)
```

> [!note] During the base constructor, the object is not yet derived
> **Construction runs base-first.** While `CtorBase`'s constructor is executing, the derived part **does not exist yet** — its members are uninitialised — so the language deliberately dispatches to the base version.
>
> **This is the safe choice**: had it called the override, `CtorDerived::which()` would have read `tag` before it was initialised.
>
> **But it means a virtual call in a constructor does not do what it looks like it does.** *(Destructors are the mirror image: the derived part is already gone, so a virtual call there also resolves to the base.)*
>
> **Never call a virtual function from a constructor or destructor.**

### 5. ⚠️ Default arguments on a virtual function

*(Verified:)*
```cpp
struct DefBase    { virtual int f(int x = 1) const { return x * 10;  } };
struct DefDerived : DefBase { int f(int x = 2) const override { return x * 100; } };
```
```
d.f()   (static type DefDerived) = 200      <- default 2, derived body
b.f()   (static type DefBase)    = 100      <- default 1 from BASE, derived body
```

> [!warning] The body is chosen dynamically; the default argument statically
> **`b.f()` used `DefBase`'s default of 1 and `DefDerived`'s body** — the call assembles its two halves from two different classes.
>
> **Neither result is what the code appears to say.** The derived author wrote `x = 2` and it was ignored; the base author wrote `x * 10` and it was ignored.
>
> **Default arguments are substituted at the call site from the static type** ([[05 - Functions and Scope|ch. 05]] §6), while virtual dispatch happens at runtime from the dynamic type. **The two mechanisms simply do not agree**, and nothing warns.
>
> **Never give a virtual function default arguments.** Use an overload, or a non-virtual public function with a default that forwards to a virtual one.

### 6. What `virtual` costs

*(Verified:)*
```
sizeof(Plain, no virtuals)  =  8
sizeof(WithV, has virtuals) = 16      <- +8 bytes for the vtable pointer
```

> [!note] One hidden pointer per object, one indirection per call
> **Every polymorphic object carries a pointer to its class's virtual table**, and a virtual call reads that pointer, indexes the table, and jumps.
>
> **The jump is cheap; blocking inlining usually costs more.** A non-virtual one-line accessor can be inlined to nothing; a virtual one generally cannot, because the target is not known until runtime.
>
> **So: do not add `virtual` speculatively, and do not remove it "for performance" without measuring** — [[Data Structures and Algorithms/contents/02 - Algorithm Analysis in Practice|DSA ch. 02]]'s discipline applies. **The 8 bytes matter most in large arrays of small objects**, where they also cost cache lines ([[06 - Arrays, C-Strings and std vector|ch. 06]] §7).

### 7. Composition versus inheritance

```cpp
struct Car { Engine engine; … };      // Car HAS-A Engine
```
*(Verified.)*

> [!note] Inheritance is the tightest coupling C++ offers
> **A derived class depends on the base's protected members and its virtual contract**, and can be broken by changes to the base it never sees — the *fragile base class* problem.
>
> **Composition couples through a public interface only**, which is far weaker and easier to change. **It also composes freely**: a class can hold many members but has one base hierarchy.
>
> **Use inheritance only for genuine IS-A substitutability** — where a derived object can stand in for a base anywhere the base is expected without surprising anyone. **Otherwise compose.**

## ✏️ Exercises

**1. (Dispatch and slicing.)** (a) Static vs dynamic dispatch? (b) Why is hiding dangerous, and what prevents it? (c) Explain slicing. (d) What follows for containers and parameters?

> [!example]- Solution
> **(a) A non-virtual call is resolved at compile time from the *static* type; a virtual call at runtime from the *dynamic* type.**
>
> *(Verified: through a `Shape*`, `name()` gave `Circle`/`Square` while `nameNV()` gave `Shape` both times.)*
>
> **The mechanism is the vtable.** A polymorphic object carries a pointer to its class's table of virtual functions; the call reads that pointer and jumps to whatever the *actual* class installed. **A non-virtual call is just an address the compiler already knows.**
>
> **This is the distinction [[05 - Functions and Scope|ch. 05]]'s overloading could not provide** — there the compiler chose from declared types, which is why `show('a')` selected `show(int)`.
>
> **(b) Because it looks exactly like an override and behaves nothing like one.**
>
> **Declaring `nameNV()` in `Circle` creates a new function that hides the base's.** Through a `Circle` you get the derived one; through a `Shape*` you get the base one. **The same object gives different answers depending on how you hold it** — with no diagnostic.
>
> **It also arises by accident**, from a signature mismatch: `void f(int)` in the base and `void f(long)` in the derived, or forgetting `const`. **The derived function is then a new overload rather than an override**, and virtual dispatch silently stops working.
>
> **`override` is the fix.** Marking a function `override` asks the compiler to verify it really overrides something — **so a typo, a missing `const`, or a missing `virtual` in the base becomes a compile error.** *(And `final` prevents further overriding.)*
>
> **Use `override` on every override, without exception.** It costs a word and converts a whole class of silent failure into build errors — the [[08 - Pointers and Dynamic Memory|ch. 08]] principle of making the mistake unrepresentable.
>
> **(c) Copying a derived object into a base-typed variable copies only the base subobject.**
>
> *(Verified: `sizeof(Shape)` = 8, `sizeof(Circle)` = 16; passing by value gave `Shape, area 0` while by `const&` gave `Circle, area 3.14159`.)*
>
> **A `Shape` parameter is 8 bytes of storage.** There is nowhere to put a `Circle`'s extra members, so `r` is dropped and the vtable pointer is set to `Shape`'s — **the object genuinely becomes a `Shape`.** It is not a view or a cast; it is a smaller object.
>
> **What makes it dangerous is that it is legal and silent.** `Circle` *is-a* `Shape`, so the conversion is exactly what the type system permits. **The compiler has no way to know you did not mean it.**
>
> **And the result is plausible** — `area()` returned 0, a perfectly ordinary number, which is the vault's recurring failure shape.
>
> **(d)**
> - **⚠️ Never pass a polymorphic type by value.** Use `const&` for read-only access, `&` to modify, or a pointer if it may be absent.
> - **⚠️ Never store polymorphic types in a container by value.** *(Verified: `vector<Shape>` sliced on `push_back`.)* Use `vector<std::unique_ptr<Shape>>`.
> - **Make the base abstract** — one pure virtual function makes `Shape` uninstantiable, so **slicing becomes a compile error.** This is the strongest defence and costs nothing when the base has no sensible standalone meaning.
> - **Consider deleting the base's copy operations** if it must remain concrete.
>
> **Note how this sharpens [[05 - Functions and Scope|ch. 05]]'s rule.** There, passing by value was *wasteful* (measured at 1.5× plus a copy per call). **Here it is *wrong*** — the same guidance, with much higher stakes.

**2. (Hard — destructors and constructors.)** (a) What did the non-virtual destructor do? (b) Why is it UB rather than just a leak? (c) Why does a virtual call in a constructor use the base? (d) When must a destructor be virtual?

> [!example]- Solution
> **(a) It ran the base destructor and not the derived one.**
>
> *(Verified: `BaseNV dtors = 1, DerivedNV dtors = **0**`; with `virtual`, both were 1.)*
>
> **`DerivedNV` held a `vector<int>` of 1 000 elements.** Its destructor — which would have freed that buffer — never ran, **so the memory was leaked.** Any other resource the derived class owned would be leaked identically: a file handle, a mutex, a `unique_ptr`.
>
> **And `delete` freed the block using the base's size**, which is the second half of the problem.
>
> **(b) Because the standard says so, and the consequences exceed a leak.**
>
> **Deleting an object through a base pointer with a non-virtual destructor is explicitly undefined behaviour** — not "leaks the derived part", but *no constraints on behaviour* ([[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]).
>
> **The practical reasons it is worse than a leak:**
> 1. **The allocation size is wrong.** `delete` may return the block using the base's size, corrupting the heap's bookkeeping — [[08 - Pointers and Dynamic Memory|ch. 08]] §3's `delete`/`delete[]` mismatch in another form, and it crashes somewhere unrelated.
> 2. **Derived members are never destroyed**, so their invariants are never unwound — an unreleased lock is worse than leaked memory.
> 3. **It is silent.** *(Verified: the program ran to completion normally.)*
>
> **(c) Because the derived part does not exist yet.**
>
> *(Verified: `CtorBase`'s constructor printed `CtorBase`, while after construction `d.which()` gave `CtorDerived`.)*
>
> **Construction runs base-first**, then derived members, then the derived body. While the base constructor runs, **the derived members are uninitialised memory.**
>
> **So dispatching to the override would be worse than useless** — `CtorDerived::which()` reads `tag`, which has not been constructed. **The language sets the vtable pointer progressively**, so during `CtorBase` the object genuinely *is* a `CtorBase`.
>
> **Destructors are the mirror image**: the derived part is destroyed first, so a virtual call from the base destructor also resolves to the base.
>
> **This is a case where the language chose the safe behaviour and the surprising one at the same time.** The alternative — calling the override — would read uninitialised memory, which is worse. **But it means a virtual call in a constructor silently does not do what it appears to.**
>
> **The practical rule: never call a virtual function from a constructor or destructor.** If you need polymorphic behaviour during construction, use a two-phase `init()` called after construction, or a factory function.
>
> **(d) Whenever a class might be deleted through a base pointer — which, if it has any virtual function, it will be.**
>
> **The presence of a virtual function announces "this class is meant to be used polymorphically".** Polymorphic use means base pointers, and base pointers eventually get deleted.
>
> **Three positions, all defensible:**
>
> | | when |
> |---|---|
> | **`virtual ~Base() = default;`** | the class is a polymorphic base — **the usual answer** |
> | **`protected: ~Base() = default;`** | polymorphic interface, but deletion through a base pointer should be forbidden — **makes it a compile error** |
> | non-virtual public destructor | the class is not a base at all |
>
> **The `protected` option is underused and elegant**: it permits polymorphic *use* while making polymorphic *deletion* impossible. **It is the [[08 - Pointers and Dynamic Memory|ch. 08]] principle again** — the invalid operation does not compile.
>
> **And it costs nothing when the class already has virtuals** — the vtable pointer is already there, so `virtual ~Base()` adds no per-object storage.

**3. (Costs and design.)** (a) What does `virtual` cost? (b) Explain the default-argument result. (c) Composition or inheritance? (d) What connects this chapter's traps?

> [!example]- Solution
> **(a) 8 bytes per object and one indirection per call — but the real cost is lost inlining.**
>
> *(Verified: `sizeof` went from **8** to **16** when virtuals were added.)*
>
> **Every polymorphic object stores a hidden pointer to its class's vtable**, and a virtual call loads it, indexes, and jumps.
>
> **The indirection is cheap on modern hardware** — predictable, and usually cached. **What costs more is that the compiler cannot inline the call**, because the target is unknown until runtime. **A one-line accessor that would have compiled to nothing becomes a real function call**, which also blocks the optimisations inlining enables.
>
> **The 8 bytes matter most in large arrays of small objects.** Doubling an object's size halves how many fit in a cache line — **[[06 - Arrays, C-Strings and std vector|ch. 06]] §7 measured that effect at 2.5×**, so the storage cost can become a speed cost.
>
> **But do not optimise this speculatively.** [[Data Structures and Algorithms/contents/02 - Algorithm Analysis in Practice|DSA ch. 02]]'s discipline applies: **measure before removing `virtual`**, and remember that the alternative is usually a `switch` on a type tag, which is slower and worse.
>
> **(b) The body comes from the dynamic type; the default argument from the static type.**
>
> *(Verified: `d.f()` = **200**, `b.f()` = **100**, where `b` is a `DefBase&` bound to a `DefDerived`.)*
>
> **Two different mechanisms with two different timings:**
> - **Default arguments are substituted at the call site**, from the *declared* type, at compile time ([[05 - Functions and Scope|ch. 05]] §6).
> - **Virtual dispatch happens at runtime**, from the *actual* type.
>
> **So `b.f()` becomes `b.f(1)` — using the base's default — and then dispatches to `DefDerived::f`, giving `1 * 100 = 100`.**
>
> **Neither author gets what they wrote.** The derived author's `x = 2` is ignored; the base author's `x * 10` is ignored. **The call is assembled from two classes, and nothing warns.**
>
> **Why it is allowed at all** is that defaults are a call-site convenience, not part of the function's identity — they are not part of the signature and do not participate in overriding. **The interaction is a consequence of two reasonable rules meeting.**
>
> **The fix: never give a virtual function default arguments.** If a default is wanted, use the **Non-Virtual Interface** idiom — a non-virtual public function carrying the default, forwarding to a protected pure virtual:
> ```cpp
> int f(int x = 1) const { return doF(x); }      // non-virtual, owns the default
> private: virtual int doF(int x) const = 0;     // virtual, no default
> ```
>
> **(c) Composition by default; inheritance only for genuine IS-A substitutability.**
>
> **Inheritance is the tightest coupling C++ offers.** The derived class sees the base's protected members, depends on its virtual contract, and can be broken by base changes it never sees — the **fragile base class** problem.
>
> **Composition couples only through a public interface** *(verified: `Car` holds an `Engine` and uses `describe()`)*, which is far weaker, easier to change, and easier to test with a substitute.
>
> **Composition also composes.** A class can hold many members; it has one base hierarchy. **And it permits changing the relationship at runtime**, which inheritance cannot.
>
> **The test for inheritance is substitutability**: can a derived object be used *anywhere* a base is expected, without surprising the caller? **If not — if the derived class removes a capability, or strengthens a precondition — it is not IS-A**, whatever the domain vocabulary suggests.
>
> **In modern C++ the strongest use of inheritance is a pure-virtual interface** — no data, no implementation, just a contract. **That has none of the fragile-base problems**, because there is no implementation to be fragile.
>
> **(d) Every one is a mismatch between the static type and the dynamic type.**
>
> | trap | static | dynamic |
> |---|---|---|
> | hiding (§1) | picks the base function | ignored |
> | slicing (§2) | the object *becomes* the static type | destroyed |
> | non-virtual destructor (§3) | picks the base destructor | ignored |
> | virtual in a constructor (§4) | the object *is* the base at that moment | not yet derived |
> | default arguments (§5) | supplies the argument | supplies the body |
>
> **In each case the compiler consults the declared type and the object is something else** — and because both are legal, nothing is reported.
>
> **The defences all reduce to making the intent explicit:**
> 1. **`override` on every override** — turns hiding into a compile error.
> 2. **`virtual` destructor** on any class with virtuals.
> 3. **Never pass or store polymorphic types by value.**
> 4. **Make bases abstract** where possible — slicing then cannot compile.
> 5. **No virtual calls in constructors; no defaults on virtuals.**
>
> **Three of the five are compile-time enforcement**, which is the principle this vault keeps arriving at — [[01 - Fundamentals - Types, Variables and Expressions|`const`]], [[08 - Pointers and Dynamic Memory|`unique_ptr`'s non-copyability]], [[Database Management Systems/contents/01 - Databases and Data Models|database constraints]]: **make the mistake unrepresentable rather than detectable.**

## 📝 Summary

- **`virtual` dispatches on the dynamic type; everything else on the static type** *(verified: `name()` gave `Circle`/`Square`, `nameNV()` gave `Shape` both times)*.
- **⚠️ Redefining a non-virtual function *hides* it, it does not override it** — the same object answers differently depending on how you hold it, with no diagnostic. **`override` turns this into a compile error.**
- **⚠️ Object slicing: passing a derived object by value as a base cuts off the derived part** *(verified: `sizeof` 16 → 8; `byValue` gave `Shape, area 0` while `const&` gave `Circle, area 3.14159`)*. **`vector<Shape>` sliced on `push_back`.**
- **So polymorphic containers hold pointers, and polymorphic parameters are references** — [[05 - Functions and Scope|ch. 05]]'s rule, now a correctness issue rather than a performance one.
- **⚠️ A non-virtual destructor never runs the derived destructor** *(verified: base 1, derived **0**)*. The derived object's `vector` was never freed, and this is **undefined behaviour**, not just a leak.
- **If a class has any virtual function, its destructor must be virtual** — or `protected`, which makes deletion through a base pointer a compile error.
- **A virtual call in a constructor resolves to the base** *(verified)*, because the derived part does not exist yet. **Never call virtuals from constructors or destructors.**
- **⚠️ Default arguments on a virtual: the body is chosen dynamically, the default statically** *(verified: `b.f()` = **100** — base's default 1, derived's body ×100)*. **The call is assembled from two classes and neither author gets what they wrote.**
- **`virtual` costs 8 bytes per object and blocks inlining** *(verified: `sizeof` 8 → 16)*. Do not add or remove it speculatively.
- **Composition by default; inheritance only for genuine IS-A substitutability.** Inheritance is the tightest coupling C++ offers.
- **Every trap in this chapter is a static/dynamic type mismatch**, and three of the five defences are compile-time.

## ⚠️ Important Notes

1. **⚠️ Mark every override `override`.** It converts silent hiding — from a typo, a missing `const`, or a missing `virtual` — into a compile error.
2. **⚠️ Give every polymorphic base a `virtual` destructor**, or a `protected` non-virtual one if it must not be deleted polymorphically.
3. **⚠️ Never pass a polymorphic type by value.** Use `const&`, `&`, or a pointer.
4. **⚠️ Never store polymorphic types by value in a container.** Use `vector<std::unique_ptr<Base>>`.
5. **Make polymorphic bases abstract** where you can — slicing then cannot compile.
6. **Never call a virtual function from a constructor or destructor.** Use a post-construction `init()` or a factory.
7. **⚠️ Never give a virtual function default arguments.** Use the Non-Virtual Interface idiom instead.
8. **Do not add `virtual` speculatively** — it costs a pointer per object and blocks inlining.
9. **Do not remove `virtual` for performance without measuring.** The usual alternative is worse.
10. **Prefer composition.** Inheritance couples through protected members and the virtual contract; composition couples only through a public interface.
11. **Test IS-A by substitutability**: can the derived object be used anywhere the base is expected without surprising the caller?
12. **Prefer pure-virtual interfaces** — no data, no implementation, no fragile base.
13. **Remember `sizeof` grows with the first virtual function.** In large arrays of small objects that also costs cache lines ([[06 - Arrays, C-Strings and std vector|ch. 06]]).

> [!warning] Gaps in the source material
> **Malik ch. 11 and the polymorphism sections of ch. 12 extract well** — inheritance syntax and access modes, redefining member functions, constructors in derived classes, composition, `virtual` functions, abstract classes, and the slicing discussion all came through readably. **Book page $n$ = PDF page $n+50$; ch. 11 is PDF pages 793–866, and ch. 12's virtual-function material is PDF ~900–942.** *(Standing quirk: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost** — the class-hierarchy diagrams and, more importantly, **the vtable diagrams** showing an object's hidden pointer into a table of function addresses. **§6 substitutes the measured `sizeof` difference (8 → 16)**, which demonstrates the vtable pointer's existence as a fact rather than a picture.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 11–12.**
>
> **Additions beyond the source.** **Malik covers inheritance, `virtual`, abstract classes and slicing at a first-course level — the material is present. What is added is execution and the consequences:**
>
> - **§1's hiding demonstration is mine**, including **`override` as the defence** — a C++11 feature Malik's edition does not emphasise, and the single most valuable habit in this chapter.
> - **§2 executes the slicing** rather than describing it, and **prints `sizeof(Shape)` = 8 against `sizeof(Circle)` = 16** so the mechanism is visible: there is nowhere to put the extra bytes. **The `vector<Shape>` case and the "make the base abstract" defence are additions.**
> - **§3's instrumented destructor count is mine** — `BaseNV dtors = 1, DerivedNV dtors = **0**` makes "the derived destructor doesn't run" a number. **The `protected` non-virtual destructor alternative is an addition.**
> - **§4's constructor demonstration is mine**, including the point that the language's choice is *safe* (the override would read uninitialised members) *and* surprising.
> - **⚠️ §5 is the chapter's strangest result and is entirely mine.** Malik does not discuss default arguments on virtual functions. **Showing `b.f()` = 100 — base's default, derived's body — demonstrates a call assembled from two classes**, and it completes a thread opened in [[05 - Functions and Scope|ch. 05]] §6, where the static substitution of defaults was established. **The Non-Virtual Interface fix is an addition.**
> - **§6's `sizeof` measurement and the observation that lost inlining usually costs more than the indirection** are additions, as is the link to [[06 - Arrays, C-Strings and std vector|ch. 06]]'s cache-line result.
> - **The closing synthesis — that all five traps are static/dynamic type mismatches** — is my own framing.
>
> **Deliberately compressed.** **Malik's access-mode table for inheritance** (`public`/`protected`/`private` inheritance and how member access is transformed) is omitted: `private` and `protected` inheritance are rare in modern code, and composition is the better answer to what they attempt. **Multiple inheritance and virtual base classes** are not covered — they are genuinely complex, rarely justified outside interface inheritance, and the scope decision keeps this a first course. **Malik's extended `personType`/`studentType` hierarchies** are not reproduced; they exercise syntax without exposing behaviour. **Abstract classes** appear via the "make the base abstract" recommendation rather than as a separate section, since their main practical role here is preventing slicing. **`dynamic_cast` and RTTI** are omitted — needing them usually signals a design problem, and they would be a distraction at this level.

**Previous:** [[08 - Pointers and Dynamic Memory]] · **Next:** [[10 - Operator Overloading and Templates]]
