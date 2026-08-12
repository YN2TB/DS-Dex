---
subject: Basic Programming (C++)
chapter: 0
tags: [ds, cpp, index, moc, programming, pointers, oop, memory]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, Cengage 2017"
---

# Basic Programming (C++) — Index

Map of Content for the subject. **Every chapter note is listed below with a one-line description and a status.**

## Course framing

**A data science degree teaches Python, and this subject teaches what Python is hiding.**

Everything in [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] was built in Python, where memory is managed for you, every variable is a reference, and an out-of-range index raises a clean exception. **C++ removes all three cushions**, and what shows through is worth seeing:

1. **Memory is yours to manage.** [[Data Structures and Algorithms/contents/06 - Linked Lists|DSA ch. 06]] built linked lists without once asking where the nodes lived. Here you allocate and free them, and **forgetting to free is a leak while freeing twice is a crash.**
2. **Value versus reference is a decision, not a default.** Python decides for you; C++ makes you choose, and the choice changes both correctness and cost.
3. **⚠️ Errors do not announce themselves.** Python raises `IndexError`; **C++ reads whatever byte happens to be there and carries on.** This is *undefined behaviour*, and it is the single most important thing this subject has to teach.

> [!note] Why point 3 matters more than the syntax
> Every subject in this vault so far has converged on one lesson: **the expensive bugs are the ones that produce a plausible wrong answer with no error.** [[Data Structures and Algorithms/contents/00-Index|DSA]] found five. [[Database Management Systems/contents/00-Index|DBMS]] found the fan trap, the `NOT IN` trap, the `RANGE` frame default, the lost update, and the business-key join.
>
> **C++ is where that failure mode is native rather than incidental.** An off-by-one in Python is an exception; in C++ it is a number that looks fine. **Learning to distrust a plausible result is the transferable skill**, and this is the subject that teaches it hardest.

## Chapters

| # | Note | Source | Status | What it covers |
|---|---|---|---|---|
| 01 | [[01 - Fundamentals - Types, Variables and Expressions]] | M 1–2 | ✅ | Compilation vs interpretation; **fixed-width types and overflow**; declarations, `const`, expressions, implicit conversion and `static_cast` |
| 02 | [[02 - Input and Output]] | M 3 | ✅ | `cin`/`cout`, stream state and **why a failed read leaves a variable untouched**; manipulators; file streams |
| 03 | [[03 - Selection]] | M 4 | ✅ | `if`/`else`, `switch`, boolean expressions, short-circuit evaluation; the classic `=` vs `==` and dangling-`else` traps |
| 04 | [[04 - Repetition]] | M 5 | ✅ | `while`, `do-while`, `for`, **range-based `for`**; loop invariants; `break`/`continue` |
| 05 | [[05 - Functions and Scope]] | M 6–7 | ✅ | Parameters **by value, by reference, by const reference**; overloading; default arguments; scope, lifetime and storage duration; `enum` |
| 06 | [[06 - Arrays, C-Strings and std vector]] | M 8 | ✅ | Raw arrays and **why they decay to pointers**; `std::string` vs C-strings; **`std::vector` as the modern default**; bounds are not checked |
| 07 | [[07 - Structs and Classes]] | M 9–10 | ✅ | `struct` vs `class`; encapsulation, constructors, member functions; **the compiler-generated members you get for free** |
| 08 | [[08 - Pointers and Dynamic Memory]] | M 12 | ✅ | Pointers, `new`/`delete`, **leaks, dangling pointers and double-free**; the rule of three; **smart pointers as the modern answer** |
| 09 | [[09 - Inheritance and Polymorphism]] | M 11, 12 | ✅ | Inheritance vs composition; **`virtual` functions and why a non-virtual destructor leaks**; abstract classes; slicing |
| 10 | [[10 - Operator Overloading and Templates]] | M 13 | ✅ | Operator overloading and its limits; function and class templates; **templates as compile-time polymorphism** |
| 11 | [[11 - Exception Handling and RAII]] | M 14 | ✅ | `try`/`catch`/`throw`; exception safety; **RAII — why C++ needs no `finally`** |

## What is not covered, and why

| Malik chapter | Why omitted |
|---|---|
| **15 — Recursion** | **[[Data Structures and Algorithms/contents/03 - Recursion\|DSA ch. 03]] owns recursion**, including the measured $\varphi^n$ blow-up of naive Fibonacci and its memoised fix. The language difference adds nothing; the algorithmic content is already covered. |
| **16 — Searching, Sorting and `vector`** | **[[Data Structures and Algorithms/contents/11 - Sorting and Selection\|DSA ch. 11]] owns searching and sorting**, with comparison counts measured against the $\lg(n!)$ bound. **`std::vector` itself is covered here in ch. 06**, where it belongs as the modern replacement for raw arrays. |
| **17 — Linked Lists** | **[[Data Structures and Algorithms/contents/06 - Linked Lists\|DSA ch. 06]] owns linked lists.** The one thing C++ adds — manual node allocation and ownership — is covered in **ch. 08**, where it is the point rather than a detail. |
| **18 — Stacks and Queues** | **[[Data Structures and Algorithms/contents/05 - Stacks, Queues and Deques\|DSA ch. 05]] owns these**, including the measured $O(1)$-vs-$O(n)$ front-insertion result. |

> [!warning] Scope decision — needs confirming against the real syllabus
> **Malik has 18 chapters. This vault covers 11**, mapping to Malik 1–14.
>
> **The four omissions are deliberate and are recorded in both indexes**, as the subject file required: **[[Data Structures and Algorithms/contents/00-Index|DSA]] is complete and owns recursion, linked lists, searching/sorting, and stacks/queues.** Re-teaching them in C++ would duplicate the algorithmic content while adding only the memory-management angle — **which ch. 08 covers directly and better.**
>
> **This is my editorial judgement, not the lecturer's.** If the course treats this as the data-structures unit rather than a language unit, chapters 15–18 need adding. **Please check against the syllabus.**

## Conventions for this subject

> [!note] Every program in these notes has been compiled and run
> **This subject's analogue of the verify-every-number rule is: compile it.**
>
> **Toolchain, verified available:** **MSVC 14.50.35717** (Visual Studio 18 Build Tools), invoked with `/EHsc /std:c++17 /Zc:__cplusplus /W3`. *(There is no `g++` or `clang++` on this machine — checked, per the subject file's instruction.)*
>
> *(Verified: a `std::vector` + range-`for` program compiles and runs, and reports `__cplusplus = 201703`.)*
>
> **⚠️ MSVC quirk, verified:** without `/Zc:__cplusplus`, the `__cplusplus` macro reports **199711** (C++98) **even when `/std:c++17` is set** — a legacy default. Any code branching on `__cplusplus` will take the wrong path unless the flag is passed.
>
> **Compiler warnings are reported alongside output**, because in C++ a warning is frequently the only notice you get before undefined behaviour.

- **Where the book teaches something now considered bad practice, the modern form is given alongside it** and labelled as an addition — `std::vector` over raw arrays, `std::string` over C-strings, smart pointers over raw `new`/`delete`, `nullptr` over `NULL`, range-based `for`, and `auto`.
- **Undefined behaviour is demonstrated, not just described** — and its results are labelled as *this machine, this compiler, this run*, since that is exactly what UB means.
- **Cross-subject links are used heavily**, chiefly to [[Data Structures and Algorithms/contents/00-Index|DSA]], where the same structures were built with the cushions on.

## The Data Structures and Algorithms boundary

[[Data Structures and Algorithms/contents/00-Index|DSA]] is **complete**. **Cross-link rather than re-derive:**

| Topic | Owned by DSA | This subject adds |
|---|---|---|
| recursion, call stack | [[Data Structures and Algorithms/contents/03 - Recursion\|ch. 03]] | stack overflow as a *crash*, not an exception |
| arrays vs linked lists | [[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis\|ch. 04]], [[Data Structures and Algorithms/contents/06 - Linked Lists\|ch. 06]] | **contiguous memory, and why the locality argument is stronger here than in Python** |
| stacks, queues | [[Data Structures and Algorithms/contents/05 - Stacks, Queues and Deques\|ch. 05]] | — |
| searching, sorting | [[Data Structures and Algorithms/contents/11 - Sorting and Selection\|ch. 11]] | `std::sort` and comparators |
| hash tables | [[Data Structures and Algorithms/contents/09 - Maps, Hash Tables and Skip Lists\|ch. 09]] | `std::unordered_map` |
| **memory management** | **not covered — Python hides it** | **ch. 08: this subject's core contribution** |

## Errata

*(Empty so far — populated as errors are found and verified.)*

| Chapter | Location | Book says | Should be | Verified by |
|---|---|---|---|---|

## Source and its extraction

**D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*** (Cengage 2017), **1 490 PDF pages, 18 chapters.** **No lecture slides.**

**The PDF has a usable bookmark outline**, giving exact chapter start pages — the first source in this vault to do so. **Book page $n$ = PDF page $n+50$.**

> [!warning] Extraction quirks, tested
> **Code listings extract well** — far better than [[Data Structures and Algorithms/contents/00-Index|Goodrich's Python]] did. **`#include` directives, braces, semicolons and operators all survive**, and indentation is partially preserved. *(Verified: `for (i = 10; i <= 9; i++)` and `i = i + 2` came through exactly, and **728 literal `+` characters** survive across pages 81–400.)*
>
> **⚠️ But `C++` in *prose* renders as `C11`** — *"The following C11 program…"* — **238 times in those same pages.** The prose evidently sets `C++` in a different font from the code, and only that glyph is lost.
>
> **The practical consequence: trust operators inside code listings, and read `C11` as `C++` in prose.** *(Since `+` survives in code, arithmetic and increment operators are safe — which is the thing that would have mattered.)*
>
> **All figures and memory diagrams are images and are lost.** For [[08 - Pointers and Dynamic Memory|ch. 08]] and [[09 - Inheritance and Polymorphism|ch. 09]] this is significant — pointer diagrams are the conventional teaching device — so those chapters give **printed addresses and `sizeof` values from running programs** instead.
>
> **Malik targets C++11 at best**, and predates the practices now considered standard. Every such divergence is noted and labelled.

**Previous:** *(start of subject)* · **Next:** [[01 - Fundamentals - Types, Variables and Expressions]]
