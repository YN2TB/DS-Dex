---
subject: Basic Programming (C++)
chapter: 10
tags: [ds, cpp, operator-overloading, templates, generics, compile-time-polymorphism, specialisation]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 13"
---

# Operator Overloading and Templates

**These two features look unrelated and are the same idea: making your own types behave like built-in ones.**

Operator overloading lets `a + b` work on a `Money`. Templates let one `maxOf` work on `int`, `string` and `Money` alike. **Together they are why `std::vector<T>` feels like a language feature rather than a library type.**

**And §7 is the chapter's point.** [[09 - Inheritance and Polymorphism|Chapter 09]] gave polymorphism at *runtime*, costing a vtable pointer per object and blocking inlining. **Templates give polymorphism at *compile time*** — verified here as **8 bytes per object versus 1** — and the two are alternatives with genuinely different trade-offs, not a hierarchy.

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17 /W4`).

## 📘 Main Knowledge

### 1. Operators on your own type

```cpp
class Money {
    long cents_;                                   // integer cents -- ch.01's rule
public:
    Money& operator+=(const Money& o) { cents_ += o.cents_; return *this; }
    bool   operator< (const Money& o) const { return cents_ < o.cents_; }
};
Money operator+(Money a, const Money& b) { a += b; return a; }     // FREE, by value
std::ostream& operator<<(std::ostream& os, const Money& m);        // MUST be free
```
*(Verified: `12.50 + 3.75 = 16.25`, comparisons correct.)*

> [!note] Three conventions worth following exactly
> **1. Implement `+=` as a member, then build `+` on it as a free function.** One implementation of the arithmetic instead of two, and they cannot drift apart.
>
> **2. `operator+` takes its first argument *by value*.** That copy is the result — it is then modified and returned, so no extra copy is made.
>
> **3. `operator<<` must be a free function**, because the left operand is the **stream**, and you cannot add members to `std::ostream`. *(This is the standard reason `friend` exists: a free `operator<<` that needs private access.)*

### 2. What you may not do

- **Invent an operator** — there is no `operator**`.
- **Change precedence or associativity** — `a + b * c` always groups `b * c` first.
- **Change arity** — `operator/` is always binary.
- **Overload for built-in types only** — at least one operand must be your type.
- **Overload `.`, `::`, `?:` or `sizeof`.**

> [!warning] Precedence is fixed by the grammar, not by your definition
> **If `*` makes no sense for your type but `+` does, `a + b * c` still parses as `a + (b * c)`.** You can define what the operators *do*, never how expressions *group*.
>
> **Which is the argument against clever overloading.** `operator+` on a `Matrix` is obvious; `operator+` meaning "append to a log" is not, and readers will assume the built-in meaning — commutativity, precedence, no side effects. **Overload only when the analogy to the built-in operator is exact.**

### 3. `operator[]` needs two versions

```cpp
int&       operator[](std::size_t i)       { return v_[i]; }   // read/write
const int& operator[](std::size_t i) const { return v_[i]; }   // read-only
```
*(Verified: `r[0] = 10` works; reading through a `const Row&` works; writing through it does not compile.)*

> [!note] Without the `const` overload, a `const` object could not be read at all
> **[[05 - Functions and Scope|Ch. 05]] established that `const&` is how you pass objects.** A container whose `operator[]` is not `const`-qualified **cannot be indexed through a `const&`**, so every caller is forced into a copy — exactly the cost ch. 05 measured.
>
> **This is `const`-correctness propagating**: one missing `const` at the bottom forces copies all the way up.

### 4. Function templates

*(Verified — one template, four types:)*
```
maxOf(3, 7)                  = 7
maxOf(2.5, 1.5)              = 2.5
maxOf(string, string)        = pear
maxOf(Money, Money)          = 12.50
```

> [!note] The compiler generated four separate functions
> **Each has the concrete type baked in — no indirection, fully inlinable.** That is why templates cost nothing at runtime, and why `std::sort` on a `vector<int>` is as fast as a hand-written int sort.
>
> **`maxOf` works on `Money` only because `Money` defines `operator<`.** The template's requirement is **implicit**: "must support `<`". Nothing states it, and nothing checks it until you try.

> [!warning] Errors appear at *instantiation*, not at definition
> **The template body is only checked once you use it with a concrete type.** So `maxOf` compiles fine on its own, and `maxOf(NoLess{1}, NoLess{2})` fails — with an error pointing *inside* the template, or worse, inside library code several layers down.
>
> **This is why template error messages are notoriously long**: the compiler reports the failure where it occurred, not where you caused it.
>
> **C++20 concepts fix this** by stating the requirement up front (`template <std::totally_ordered T>`), so the error names the constraint you violated at the call site.

### 5. Class templates

```cpp
template <typename T, std::size_t N> class FixedStack { T data_[N]; … };
```
*(Verified: capacity 4 refused the 5th push; `sizeof(FixedStack<int,4>)` = **24**, `sizeof(FixedStack<double,8>)` = **72**.)*

**`N` is a compile-time *value* parameter**, so `data_` is a genuine fixed array and **the two instantiations are different types** — you cannot assign one to the other, and each gets its own generated code.

### 6. Specialisation

*(Verified: `describe(42)` and `describe(3.14)` gave `generic`; `describe(true)` gave `bool (specialised)`.)*

**A specialisation replaces the generic body for one specific type.**

> [!warning] `std::vector<bool>` is the standard library's cautionary tale
> **It is a specialisation that packs bits**, so it is *not* a normal container: `operator[]` returns a proxy object rather than a `bool&`, `&v[0]` does not give you a pointer to bools, and generic code written for `vector<T>` can silently misbehave.
>
> **It is widely considered a mistake** — and it is a good warning that a specialisation which changes the *interface's semantics*, not just its implementation, breaks the generic code that relies on it.

### 7. Compile-time versus runtime polymorphism

*(Verified:)*
```
runtime  (virtual)  : rb.f() = 1,   sizeof(RuntimeImpl) = 8
compile  (template) : callF(ci) = 1, sizeof(CompileImpl) = 1
```

**8 bytes versus 1, for classes with no data at all** — the difference is entirely [[09 - Inheritance and Polymorphism|ch. 09]]'s vtable pointer.

| **`virtual`** ([[09 - Inheritance and Polymorphism\|ch. 09]]) | **template** (here) |
|---|---|
| resolved at **runtime** | resolved at **compile time** |
| one function, many types | one source, **many functions** |
| needs a common base class | needs only the right **members** |
| **+1 pointer per object** | **no per-object cost** |
| cannot inline the call | **fully inlinable** |
| **types can vary within one container** | types fixed at compile time |
| binary stays small | **code bloat, slower builds** |

> [!note] They solve the same problem at different times
> **Use `virtual` when the type varies at runtime** — a `vector<unique_ptr<Shape>>` holding circles and squares, a plugin loaded from a file, anything decided by input.
>
> **Use a template when the type is known at compile time** — a container *of* a type, an algorithm over any comparable type.
>
> **The distinction is not "old versus modern".** They are different tools, and the standard library uses both: `std::vector<T>` is a template; `std::function` and stream buffers are virtual.
>
> *(The row that decides it in practice is usually the sixth: **can one container hold a mixture?** If yes, you need `virtual`; a template cannot express it.)*

## ✏️ Exercises

**1. (Operators.)** (a) Why implement `+` in terms of `+=`? (b) Why must `operator<<` be free? (c) Why does `operator[]` need two versions? (d) When should you *not* overload?

> [!example]- Solution
> **(a) One implementation of the arithmetic, and correct copies for free.**
>
> ```cpp
> Money& operator+=(const Money& o);              // member: the actual arithmetic
> Money operator+(Money a, const Money& b) { a += b; return a; }   // free, by value
> ```
> **The logic exists once.** Writing both independently means two places to change and two places to get wrong — and they will eventually disagree.
>
> **Taking the first parameter *by value* is the second half of the idiom.** That copy *becomes* the result: it is modified in place and returned, so no additional copy is made. **Taking `const Money&` and constructing a local would be an extra object.**
>
> **And making `+` a free function gives symmetry.** As a member, the left operand must be a `Money`, so `5 + money` could not work even with an implicit conversion available. **As a free function, both operands convert equally.**
>
> **(b) Because the left operand is the stream, and you cannot add members to `std::ostream`.**
>
> `os << m` means `operator<<(os, m)`. **As a member it would have to be `std::ostream::operator<<`**, and that class is not yours to modify.
>
> **This is the standard, legitimate use of `friend`**: a free `operator<<` declared a friend so it can read private members.
>
> **It also returns `std::ostream&`**, which is what makes chaining work — `os << a << b` is `(os << a) << b`, so each call must hand the stream back.
>
> **(c) So that `const` objects can be read.**
>
> *(Verified: reading through a `const Row&` worked; writing through it did not compile.)*
>
> **A non-`const` member function cannot be called on a `const` object** ([[07 - Structs and Classes|ch. 07]] §4). **Without the `const` overload, a `const Row` could not be indexed at all** — not even to read.
>
> **And [[05 - Functions and Scope|ch. 05]] established that `const&` is how non-trivial objects are passed.** So the missing `const` does not merely block reading — **it forces every caller to take the object by value**, reintroducing the copy cost ch. 05 measured at 1.5× plus an allocation per call.
>
> **The two versions differ in return type on purpose**: `int&` permits `r[0] = 10`; `const int&` permits reading only. **This is `const`-correctness propagating upward**, and one omission at the bottom of a call chain forces copies all the way to the top.
>
> **(d) When the analogy to the built-in operator is not exact.**
>
> **Readers bring expectations that you cannot override:** that `+` is commutative and cheap and has no side effects; that `==` is reflexive and consistent with `!=`; that `*` binds tighter than `+` *(verified as unchangeable — §2)*.
>
> **So `operator+` on a `Matrix` or a `Money` is right** — the analogy holds exactly. **`operator+` meaning "append to a log" is wrong**, even though it compiles: it is not commutative, it has side effects, and `a + b * c` will group in a way that makes no sense.
>
> **The practical test: would a reader who has never seen your class predict what the expression does?** If not, a named function is clearer. **`stream << x` survives this test only because the convention is universal** — and it is worth noting that `<<` for output is itself an abuse of a bit-shift operator, grandfathered in by forty years of use.

**2. (Hard — templates.)** (a) What does the compiler actually generate? (b) Why do errors appear late? (c) What are the requirements, and how are they stated? (d) What does specialisation risk?

> [!example]- Solution
> **(a) A separate function for every type it is used with.**
>
> *(Verified: `maxOf` was used with `int`, `double`, `std::string` and `Money` — four instantiations from one source.)*
>
> **Each generated function has the concrete type baked in.** `maxOf<int>` compares `int`s directly, with no indirection and nothing to dispatch on — **so it inlines to a single comparison**, exactly as a hand-written `int` version would.
>
> **That is why templates are zero-cost at runtime**, and why `std::sort` on a `vector<int>` matches a hand-written int sort — a claim [[Data Structures and Algorithms/contents/11 - Sorting and Selection|DSA ch. 11]] verified from the other direction, where C's `sorted()` beat a hand-written Python merge-sort by 14×.
>
> **The cost is moved to build time and binary size.** Four instantiations means four functions compiled and four in the binary — **"code bloat"**, and a large part of why C++ builds are slow.
>
> **(b) Because the body is only checked once a concrete type is supplied.**
>
> **A template is a *pattern*, not code.** Until `T` is known, most of the body cannot be checked — the compiler does not know whether `a < b` is valid because it does not know what `a` is.
>
> *(Verified in principle: `maxOf` compiles fine standing alone; instantiating it with a type lacking `operator<` is what fails.)*
>
> **Three practical consequences:**
> 1. **A template can contain errors nobody has found**, because no one has instantiated it that way.
> 2. **Error messages are enormous and point at the wrong place** — inside the template, or inside library code several layers down, rather than at the call you wrote.
> 3. **Templates usually live in headers**, since the definition must be visible wherever it is instantiated. That is a build-time cost and a real design constraint.
>
> **(c) Implicitly, by what the body does — which is the problem.**
>
> **`maxOf` requires `operator<` and copy-constructibility. Nothing says so.** The requirement is discovered by reading the body, or by instantiating and reading the error.
>
> **This is *duck typing checked at compile time*:** the type does not need to inherit from anything or declare anything — **it just needs the right members.** That is more flexible than [[09 - Inheritance and Polymorphism|ch. 09]]'s inheritance, which requires a common base, and it is why templates work on `int` as readily as on your own class.
>
> **The flexibility is exactly what makes the errors bad.** With `virtual`, the base class *states* the contract and a violation is reported at the class. **With a template the contract is implicit and a violation is reported deep in the instantiation.**
>
> **C++20 concepts close the gap:**
> ```cpp
> template <std::totally_ordered T> T maxOf(const T& a, const T& b);
> ```
> **The requirement is now part of the signature**, so a bad call is rejected *at the call site* with a message naming the unsatisfied constraint. **This is the same principle as [[01 - Fundamentals - Types, Variables and Expressions|`const`]] and [[08 - Pointers and Dynamic Memory|`unique_ptr`]] — state the constraint so the compiler can enforce it early.**
>
> **(d) That a specialisation changes the *semantics* rather than just the implementation.**
>
> *(Verified: `describe(true)` selected the `bool` specialisation while `int` and `double` used the generic body.)*
>
> **A specialisation is legitimate when it changes only *how*** — a faster algorithm for a specific type, a different storage layout with identical behaviour. **Generic code carries on working.**
>
> **It is dangerous when it changes *what*, and `std::vector<bool>` is the standard example.** It packs bits, so:
> - **`operator[]` returns a proxy object, not a `bool&`** — so `auto& b = v[0];` does not do what it does for every other `vector<T>`;
> - **`&v[0]` is not a pointer to contiguous `bool`s**, so code assuming `vector`'s contiguity guarantee breaks;
> - **it is not a `Container`** in the standard's own sense.
>
> **So `template <typename T> void f(std::vector<T>&)` can work for every `T` except `bool`** — and the failure is at instantiation, deep in the error output.
>
> **The lesson: a specialisation must honour the generic contract.** Change the implementation freely; changing observable behaviour breaks every generic caller, and they will not find out until they instantiate.

**3. (The two polymorphisms.)** (a) What did §7 measure? (b) When `virtual`, when template? (c) Can they be combined? (d) What connects this chapter to the subject?

> [!example]- Solution
> **(a) The per-object cost of runtime polymorphism.**
>
> *(Verified: `sizeof(RuntimeImpl)` = **8**, `sizeof(CompileImpl)` = **1** — for classes with no data members at all.)*
>
> **The 8 bytes are entirely [[09 - Inheritance and Polymorphism|ch. 09]]'s vtable pointer.** The 1 byte is because C++ requires distinct objects to have distinct addresses, so an empty class still occupies one byte.
>
> **The template version has *no* per-object cost**, and its call is resolved at compile time — so it can be inlined, which [[09 - Inheritance and Polymorphism|ch. 09]] §6 noted usually matters more than the indirection itself.
>
> **In a large array the 8 bytes also cost cache lines** ([[06 - Arrays, C-Strings and std vector|ch. 06]] §7 measured locality at 2.5×), **so the storage difference can become a speed difference.**
>
> **(b) The deciding question is whether one container must hold a mixture.**
>
> | use `virtual` | use a template |
> |---|---|
> | the type varies **at runtime** | the type is known **at compile time** |
> | a `vector<unique_ptr<Shape>>` of circles *and* squares | a `vector<int>`, a `sort` over any comparable type |
> | plugins, input-driven dispatch | containers, algorithms, policies |
> | you want a stated interface | you want to accept anything with the right members |
> | binary size matters | runtime cost matters |
>
> **If a single collection must hold several concrete types, only `virtual` can express it** — a template's type is fixed at instantiation. **That one requirement decides most real cases.**
>
> **The other frequent decider is build cost.** Templates put definitions in headers and generate code per instantiation, so heavy template use means slow builds and large binaries. **`virtual` compiles once.**
>
> **This is not old versus modern.** The standard library uses both deliberately: `std::vector<T>` and `std::sort` are templates; `std::function`, `std::pmr::memory_resource` and the stream buffers are virtual.
>
> **(c) Yes, and the combination is a standard idiom.**
>
> **Type erasure** — `std::function` is the canonical example — **uses a template constructor to accept any callable, then stores it behind a virtual interface internally.** The user gets template flexibility at the boundary and runtime polymorphism inside.
>
> **The CRTP** (curiously recurring template pattern) does the reverse: `class Derived : Base<Derived>`, letting a base call into its derived class **with no virtual dispatch** — compile-time polymorphism wearing an inheritance shape.
>
> **Both are beyond a first course**, but they are worth knowing exist, because they show the two mechanisms are complementary rather than competing.
>
> **(d) It is the last piece of "make your type behave like a built-in one".**
>
> **The subject's arc:** [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]] showed what built-in types do; [[07 - Structs and Classes|ch. 07]] built your own; [[08 - Pointers and Dynamic Memory|ch. 08]] made them manage resources correctly; [[09 - Inheritance and Polymorphism|ch. 09]] made them substitutable at runtime; **this chapter makes them usable with the same syntax and the same generic algorithms as `int`.**
>
> **That is what `std::vector<T>` is.** It is not a language feature — it is a class template with overloaded `operator[]`, correct special members ([[07 - Structs and Classes|ch. 07]]), RAII ([[08 - Pointers and Dynamic Memory|ch. 08]]) and value semantics. **Every mechanism in this subject is used in it.**
>
> **And the recurring principle appears once more.** Concepts, `override`, `const`, `= delete`, `unique_ptr`'s non-copyability — **each states a constraint so the compiler can enforce it early.** Templates without concepts are the exception that proves it: **the constraint exists but is unstated, and the cost is an error message nobody can read.**

## 📝 Summary

- **Operator overloading and templates both exist to make your types behave like built-in ones** — together they are why `std::vector<T>` feels like a language feature.
- **Implement `+=` as a member and build `+` on it as a free function taking its first argument by value** — one implementation, correct copies, symmetric conversions.
- **`operator<<` must be free**, because the left operand is the stream. This is `friend`'s legitimate use.
- **You cannot invent operators, change precedence, arity, or overload for built-ins only.** `a + b * c` always groups `b * c` first, whatever your types mean.
- **⚠️ `operator[]` needs a `const` and a non-`const` version** *(verified)*. Without the `const` one, a `const` object cannot be read — **forcing every caller into the copies [[05 - Functions and Scope|ch. 05]] measured.**
- **A template generates a separate function per type** *(verified on `int`, `double`, `string`, `Money`)* — concrete types baked in, fully inlinable, **zero runtime cost**. The price is build time and code size.
- **⚠️ Template errors appear at instantiation, not definition** — so a template can contain undiscovered errors, and messages point inside the template or into library code.
- **A template's requirements are implicit** — `maxOf` needs `operator<` and nothing says so. **C++20 concepts state them in the signature** so errors name the violated constraint at the call site.
- **Class templates take type *and* value parameters** *(verified: `sizeof(FixedStack<int,4>)` = 24, `<double,8>` = 72 — genuinely different types)*.
- **A specialisation must honour the generic contract.** `std::vector<bool>` changes observable semantics and breaks generic code — the standard library's cautionary tale.
- **⚠️ Compile-time versus runtime polymorphism, measured: `sizeof` **8** with `virtual` versus **1** without** — the difference is [[09 - Inheritance and Polymorphism|ch. 09]]'s vtable pointer.
- **The deciding question is whether one container must hold a mixture of types.** If yes, only `virtual` can express it.
- **They are complementary, not competing** — the standard library uses both deliberately.

## ⚠️ Important Notes

1. **Overload an operator only when the analogy to the built-in is exact.** Readers assume commutativity, precedence and no side effects.
2. **Implement `op=` as a member, then `op` as a free function built on it** — one implementation, and symmetric conversions on both operands.
3. **Take the first parameter of a binary `operator+` by value** — that copy becomes the result.
4. **`operator<<` and `operator>>` must be free functions**, and must return the stream reference to allow chaining.
5. **⚠️ Always provide both `const` and non-`const` `operator[]`.** Omitting the `const` version blocks reading through a `const&` and forces callers to copy.
6. **Keep `==` and `!=` consistent**, and define `!=` in terms of `==`. *(C++20's `operator<=>` generates the comparison set for you.)*
7. **Expect template errors at the call site to point somewhere else.** Read the *first* error, not the last.
8. **Document a template's requirements**, or state them with concepts (C++20) so the compiler enforces them.
9. **Template definitions usually belong in headers** — the definition must be visible where it is instantiated.
10. **Be aware of code bloat**: every instantiation generates code. Heavy template use means slow builds and large binaries.
11. **⚠️ A specialisation must not change observable semantics.** `std::vector<bool>` did, and generic code written for `vector<T>` breaks on it.
12. **Choose `virtual` when one container must hold several concrete types** — a template cannot express that.
13. **Choose a template when the type is known at compile time** — it costs nothing per object and inlines fully.
14. **Do not treat templates as "modern" and `virtual` as "old".** The standard library uses both on purpose.

> [!warning] Gaps in the source material
> **Malik ch. 13 extracts well** — operator-overloading syntax and the member/free distinction, `friend` functions, overloading the stream operators, and both function and class templates came through readably, with listings intact. **Book page $n$ = PDF page $n+50$; ch. 13 is PDF pages 943–1040.** *(Standing quirk: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost.** Minimal impact here — this chapter's figures are mostly code screenshots, and every result in this note is real program output.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 13.**
>
> **Additions beyond the source.** **Malik teaches the syntax of operator overloading and templates thoroughly — this is one of the better chapters in the book. What is added is the design guidance and the comparison:**
>
> - **The `+=`-then-`+` idiom, with the by-value first parameter, is an addition** — Malik shows both operators implemented independently, which duplicates the arithmetic.
> - **§3's `const`/non-`const` `operator[]` pair is mine**, including the consequence that omitting the `const` version **forces callers into the copies [[05 - Functions and Scope|ch. 05]] measured** — connecting operator design to a cost established two chapters earlier.
> - **§4's instantiation-time error discussion** and **the observation that a template's requirements are implicit** are additions, as is **C++20 concepts as the fix** — which the book predates.
> - **§6's `std::vector<bool>` warning is mine**, and it is the practically important caveat about specialisation: changing implementation is fine, changing semantics breaks every generic caller.
> - **⚠️ §7 is the chapter's centrepiece and is entirely mine.** Malik covers templates and inheritance in separate chapters and does not compare them. **Measuring `sizeof` at 8 versus 1 for otherwise-identical empty classes makes the vtable cost concrete**, and the seven-row comparison table — especially **"can one container hold a mixture?" as the deciding question** — is the guidance a first course most needs and least often gets.
> - **The closing observation that `std::vector<T>` uses every mechanism in this subject** is my own framing of the arc.
>
> **Deliberately compressed.** **Malik's full catalogue of overloadable operators** (`++` prefix/postfix, `->`, `()`, conversion operators, `new`/`delete`) is not reproduced — the pattern generalises from the examples given, and several are rare. **`friend` functions** are covered only where they are genuinely needed (`operator<<`); the broader use of `friend` to grant access between classes is usually a design smell. **Template metaprogramming and variadic templates** are far beyond a first course. **The standard library's template-heavy design (iterators, allocators, traits)** is deferred — [[Data Structures and Algorithms/contents/00-Index|DSA]] owns the containers and algorithms, and the scope decision in `00-Index.md` keeps this a language course. **`std::function` and lambdas** appear only in §7's type-erasure remark.

**Previous:** [[09 - Inheritance and Polymorphism]] · **Next:** [[11 - Exception Handling and RAII]]
