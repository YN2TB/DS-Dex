---
subject: Data Structures and Algorithms
chapter: 1
tags: [ds, dsa, python, oop, classes, special-methods, iterators, inheritance, adt]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 1–2; Lambert, *Fundamentals of Python: Data Structures*, ch. 1, 5–6"
---

# Python and Object-Oriented Foundations

Every chapter after this one implements a data structure as a Python class. This chapter builds the machinery those implementations need — and nothing more. It is deliberately **not** a Python tutorial; it is the subset of the language that matters when you are writing a container.

Three things here do real work later:

- **Python's object model** (§1) — because a data structure is a graph of references, and aliasing bugs are the commonest way an implementation goes wrong;
- **Special methods** (§4) — because they are how a class you write becomes indistinguishable from a built-in, which is the whole aesthetic of this subject;
- **Abstract data types** (§7) — the organising idea of every remaining chapter.

> [!note] The only place in the vault that teaches core Python
> `Programming for Data Science (Python)` is blocked for lack of source material, so this chapter carries that load too. [[Data Preparation and Visualization/contents/01 - Getting Started with Pandas|Data Prep & Visualization]] assumes the fluency built here.

## 📘 Main Knowledge

### 1. Names, objects, and aliasing

**In Python, a variable is not a box holding a value — it is a name bound to an object.** Assignment binds a name; it never copies.

This single fact explains most surprising behaviour, and it matters enormously here because **a data structure is a web of references.**

```python
a = [1, 2, 3]
b = a              # b and a name the SAME list
b.append(4)
print(a)           # [1, 2, 3, 4]   -- a changed too
print(a is b)      # True
```

*(Verified.)* `b = a` created an **alias**, not a copy. To copy:

```python
c = a[:]           # shallow copy (also list(a), or copy.copy(a))
```

**Mutable versus immutable** is the distinction that decides whether aliasing bites:

| Immutable | Mutable |
|---|---|
| `int`, `float`, `bool`, `str`, `tuple`, `frozenset` | `list`, `dict`, `set`, and **every class you write** |

An immutable object cannot be changed in place, so aliasing it is harmless. **A mutable one shared between two names means a change through either is visible through both** — which is exactly what you want when a linked list's nodes reference each other, and exactly what ruins your afternoon when you did not intend it.

> [!warning] Shallow copy is not deep copy
> A shallow copy duplicates the *outer* container and shares the inner objects:
> ```python
> import copy
> grid = [[0, 0], [0, 0]]
> shallow = copy.copy(grid)
> deep    = copy.deepcopy(grid)
> grid[0][0] = 9
> # grid    == [[9, 0], [0, 0]]
> # shallow == [[9, 0], [0, 0]]   <- changed!
> # deep    == [[0, 0], [0, 0]]   <- independent
> ```
> *(Verified.)* **`[[0]*2]*2` is the classic trap** — it creates one inner list referenced twice, so writing to one row writes to both. Use `[[0]*2 for _ in range(2)]`.

> [!warning] The mutable default argument
> A function's default arguments are evaluated **once, when the function is defined** — not on each call. So a mutable default is shared across every call:
> ```python
> def bad(item, box=[]):
>     box.append(item)
>     return box
>
> bad(1)   # [1]
> bad(2)   # [1, 2]      <- not [2]
> bad(3)   # [1, 2, 3]
> ```
> *(Verified — the three calls returned `[1]`, `[1,2]`, `[1,2,3]`.)*
>
> **The fix is idiomatic and should be automatic:**
> ```python
> def good(item, box=None):
>     if box is None:
>         box = []
>     box.append(item)
>     return box
> ```
> This bites constantly when writing container classes with optional initial contents.

### 2. Classes and encapsulation

A **class** is the primary abstraction mechanism. `__init__` is the constructor; `self` is the instance, and it is **explicit** in every method signature — unlike C++ or Java.

```python
class CreditCard:
    def __init__(self, customer, limit, balance=0):
        self._customer = customer
        self._limit = limit
        self._balance = balance

    def get_balance(self):
        return self._balance

    def charge(self, price):
        """Return True if the charge was processed."""
        if price + self._balance > self._limit:
            return False
        self._balance += price
        return True
```

> [!note] Encapsulation by convention, not enforcement
> **Python has no `private`.** The convention is a **single leading underscore**: `_balance` means "this is internal; do not touch it from outside." Nothing stops you — the language trusts you.
>
> **Goodrich adheres to this throughout, and so do these notes.** The reason it matters for data structures: a container's internal representation (an array, a chain of nodes) is precisely what should be free to change without breaking users. **Encapsulation is what makes the ADT/implementation split of §7 real rather than aspirational.**
>
> *(A double leading underscore, `__x`, triggers name mangling — a different and rarely-needed mechanism. Single underscore is the convention you want.)*

### 3. Special methods: making your class behave like a built-in

This is the most useful section in the chapter. **Python's operators and built-in functions are implemented by dunder ("double underscore") methods**, and defining them makes your type work with ordinary syntax.

| You write | Python calls |
|---|---|
| `len(x)` | `x.__len__()` |
| `x[j]` | `x.__getitem__(j)` |
| `x[j] = v` | `x.__setitem__(j, v)` |
| `x + y` | `x.__add__(y)` |
| `x == y` | `x.__eq__(y)` |
| `x < y` | `x.__lt__(y)` |
| `str(x)`, `print(x)` | `x.__str__()` |
| `repr(x)` | `x.__repr__()` |
| `v in x` | `x.__contains__(v)`, or falls back to iteration |
| `for e in x` | `x.__iter__()` |
| `x()` | `x.__call__()` |

> [!example]- A vector class, and what the special methods buy (all output verified)
> ```python
> class Vector:
>     """A mathematical vector of fixed dimension."""
>
>     def __init__(self, d):
>         if isinstance(d, int):
>             self._coords = [0] * d          # d zeros
>         else:
>             self._coords = list(d)          # or copy a given sequence
>
>     def __len__(self):
>         return len(self._coords)
>
>     def __getitem__(self, j):
>         return self._coords[j]
>
>     def __setitem__(self, j, val):
>         self._coords[j] = val
>
>     def __add__(self, other):
>         if len(self) != len(other):
>             raise ValueError('dimensions differ')
>         result = Vector(len(self))
>         for j in range(len(self)):
>             result[j] = self[j] + other[j]
>         return result
>
>     def __eq__(self, other):
>         return self._coords == other._coords
>
>     def __ne__(self, other):
>         return not self == other
>
>     def __str__(self):
>         return '<' + str(self._coords)[1:-1] + '>'
>
>     def __repr__(self):
>         return 'Vector(' + repr(self._coords) + ')'
> ```
>
> ```
> v = Vector(5); v[1] = 23; v[-1] = 45
> v            -> <0, 23, 0, 0, 45>
> len(v)       -> 5
> v + v        -> <0, 46, 0, 0, 90>
> u = Vector([1,2,3])
> repr(u)      -> Vector([1, 2, 3])
> u == Vector([1,2,3])  -> True
> u + v        -> ValueError: dimensions differ
> ```
>
> **The two lines worth noticing are these:**
> ```
> [x for x in u]   ->  [1, 2, 3]
> 3 in u           ->  True
> ```
> **Neither `__iter__` nor `__contains__` was defined.** Python synthesised both from `__len__` and `__getitem__` — it calls `x[0]`, `x[1]`, … until `IndexError`. **Implementing two methods gave iteration, membership testing, unpacking and comprehension support for free.**
>
> Note also `v[-1]` worked: negative indexing came free because `__getitem__` delegates to a `list`, which already handles it. **Delegating to a built-in inherits its behaviour, including its edge cases** — a theme throughout the subject.

> [!note] `__str__` versus `__repr__`
> `__str__` is for humans (`print`); `__repr__` is for developers, and should ideally be valid Python that recreates the object. The Vector above returns `<1, 2, 3>` from `str` and `Vector([1, 2, 3])` from `repr` — **and a container's `repr` is what you see when you inspect a list of them in a debugger**, which is why it is worth writing.

### 4. Iterators and generators

An **iterator** supports one operation: `__next__()`, returning the next element or raising `StopIteration`. An **iterable** is anything that can produce an iterator via `__iter__()`.

```python
class SequenceIterator:
    """An iterator for any Python sequence type."""

    def __init__(self, sequence):
        self._seq = sequence
        self._k = -1

    def __next__(self):
        self._k += 1
        if self._k < len(self._seq):
            return self._seq[self._k]
        raise StopIteration()

    def __iter__(self):
        return self        # by convention, an iterator returns itself
```

*(Verified: three `next()` calls on `[10,20,30]` returned `10,20,30`, and the fourth raised `StopIteration`.)*

**But you will almost never write that.** A **generator** — a function using `yield` — produces an iterator automatically:

```python
def factors(n):
    """Generate the factors of n."""
    k = 1
    while k * k < n:
        if n % k == 0:
            yield k
            yield n // k
        k += 1
    if k * k == n:
        yield k
```

*(Verified: `sorted(factors(100))` gives `[1, 2, 4, 5, 10, 20, 25, 50, 100]`.)*

> [!note] Generators are lazy, and that is the point
> `factors(100)` returns a **generator object**, not a list — nothing is computed until you iterate. Three consequences that matter later:
> 1. **Memory is $O(1)$ rather than $O(n)$** — you never build the list.
> 2. **You can generate infinite sequences** and stop when you like.
> 3. **The traversals of [[07 - Trees and Traversals|ch. 07]] are naturally generators**, because a tree traversal is exactly "produce the elements one at a time in this order".
>
> Note also the $\sqrt n$ loop bound: the same "divisors pair up around $\sqrt n$" argument as [[Discrete Mathematics/contents/05 - Number Theory and Cryptography|DM ch. 05]] §1.

### 5. Inheritance: extending and overriding

Inheritance lets a **subclass** reuse and specialise a **base class**. Two distinct things a subclass can do:

- **Override** — replace an inherited method with a new implementation;
- **Extend** — add new methods (or call the parent's version via `super()` and do more).

```python
class PredatoryCreditCard(CreditCard):

    def __init__(self, customer, limit, apr, balance=0):
        super().__init__(customer, limit, balance)   # EXTEND the constructor
        self._apr = apr

    def charge(self, price):                          # OVERRIDE
        success = super().charge(price)
        if not success:
            self._balance += 5                        # penalty for a declined charge
        return success

    def process_month(self):                          # NEW behaviour
        if self._balance > 0:
            monthly_factor = pow(1 + self._apr, 1/12)
            self._balance *= monthly_factor
```

*(Verified: a standard card declining a \$1500 charge leaves the balance at 0; the predatory card declines it and leaves the balance at **5**. After a further \$500 charge and one month at 8.25% APR, the balance is **508.35**.)*

**`super().charge(price)` is the pattern to internalise** — override by *wrapping* the parent's behaviour rather than copying it. Copying the parent's body into the subclass is the standard way inheritance hierarchies rot.

**Polymorphism** means the right version is chosen at run time by the object's actual class. Because `PredatoryCreditCard` *is* a `CreditCard` (`isinstance` returns `True` ✓), any code written against the base class works with either.

> [!note] Duck typing, and why Python cares less about inheritance than Java does
> Python is dynamically typed: **if an object supports the operations you use, it works** — regardless of its class. *"If it walks like a duck and quacks like a duck, it must be a duck."*
>
> So a function that iterates its argument works with a `list`, a `str`, a generator, or the `Vector` of §3 — none of which share a base class. **Inheritance in Python is therefore used more for sharing implementation than for declaring types**, which is the opposite emphasis from a statically typed language. Compare [[Basic Programming (C++)/contents/00-Index|C++]], where the type hierarchy is checked at compile time.

### 6. Abstract data types — the idea the whole subject is built on

> [!note] Definition
> An **abstract data type (ADT)** is a specification: **what operations exist and what they mean**, with no commitment to how they are implemented.

A *stack* is an ADT: `push`, `pop`, `top`, `is_empty`. Whether it is backed by an array or a linked list is an implementation choice, invisible to the user.

**This separation is the organising principle of every remaining chapter**, and it is what makes the comparison tables meaningful: two implementations of the same ADT are interchangeable in behaviour and different in performance, so the choice between them is purely about which operations you perform often.

**Python supports ADTs in two ways.** Informally by **duck typing** (§5). Formally by an **abstract base class (ABC)** — a class that declares methods that subclasses *must* provide:

```python
from abc import ABCMeta, abstractmethod

class Sequence(metaclass=ABCMeta):
    """An abstract base class for a read-only sequence."""

    @abstractmethod
    def __len__(self): ...

    @abstractmethod
    def __getitem__(self, j): ...

    def __contains__(self, val):        # CONCRETE, built on the two abstract methods
        for j in range(len(self)):
            if self[j] == val:
                return True
        return False

    def index(self, val):
        for j in range(len(self)):
            if self[j] == val:
                return j
        raise ValueError('value not in sequence')
```

> [!example]- The ABC in action: re-implementing `range` (verified)
> ```python
> class Range(Sequence):
>     """A re-implementation of Python's built-in range class."""
>
>     def __init__(self, start, stop=None, step=1):
>         if step == 0:
>             raise ValueError('step cannot be 0')
>         if stop is None:
>             start, stop = 0, start          # range(n) means range(0, n)
>         self._length = max(0, (stop - start + step - 1) // step)
>         self._start, self._step = start, step
>
>     def __len__(self):
>         return self._length
>
>     def __getitem__(self, k):
>         if k < 0:
>             k += len(self)                  # support negative indices
>         if not 0 <= k < self._length:
>             raise IndexError('index out of range')
>         return self._start + k * self._step
> ```
>
> ```
> r = Range(2, 20, 3)
> list(r)      -> [2, 5, 8, 11, 14, 17]
> len(r)       -> 6
> 14 in r      -> True        r.index(14) -> 4
> 15 in r      -> False
> Sequence()   -> TypeError   <- the ABC cannot be instantiated
> ```
>
> **Two lessons.** First, **`__contains__` and `index` were inherited for free** — the ABC implemented them once in terms of `__len__` and `__getitem__`, so every subclass gets them. That is the payoff of an ABC over duck typing: **shared concrete behaviour, not just a promise.**
>
> Second, `Range` computes its length arithmetically and never stores the elements, so **`Range(0, 10**100)` is instantaneous and uses constant memory.** *(This is exactly what Python's own `range` does, and it is why `range` is not a list.)*

## ✏️ Exercises

**1. (Aliasing and mutability.)** Predict the output of each, then explain. (a) `a=[1,2]; b=a; b.append(3); print(a)`. (b) `a=[1,2]; b=a[:]; b.append(3); print(a)`. (c) `def f(x, acc=[]): acc.append(x); return acc` called three times with `1`, `2`, `3`. (d) `grid=[[0]*2]*2; grid[0][0]=9; print(grid)`.

> [!example]- Solution
> **(a) `[1, 2, 3]`.** `b = a` binds a second **name** to the same list object; it does not copy. Mutating through `b` is visible through `a`, and `a is b` is `True` *(verified)*.
>
> **(b) `[1, 2]`.** `a[:]` creates a **new** list with the same elements, so `b` is a separate object and `a` is untouched *(verified)*.
>
> **(c) `[1]`, `[1, 2]`, `[1, 2, 3]`** — **not** `[1]`, `[2]`, `[3]`.
>
> The default `[]` is evaluated **once, at function-definition time**, and the *same* list object is reused by every call that omits the argument. *(Verified.)* Fix with `acc=None` and `if acc is None: acc = []`.
>
> **(d) `[[9, 0], [9, 0]]`** — **both rows changed.**
>
> `[[0]*2]*2` builds one inner list and puts **two references to it** in the outer list. `grid[0]` and `grid[1]` are the same object, so assigning through one is visible through the other. Use `[[0]*2 for _ in range(2)]`, which evaluates the inner expression twice.
>
> **All four are the same fact:** *assignment binds names, it does not copy.* **This is the single most useful thing to internalise before implementing a data structure**, because a linked list is nothing but deliberate aliasing — and an accidental alias is indistinguishable from a deliberate one until it corrupts your structure.

**2. (Special methods.)** Write a `Vector` class supporting `len`, indexing (including negative), `+`, `==`, and a readable `str`. Then show that iteration and `in` work **without** defining `__iter__` or `__contains__`, and explain why.

> [!example]- Solution
> The implementation is §3's, and it runs as shown there. The part to explain is this *(verified)*:
> ```
> u = Vector([1, 2, 3])
> [x for x in u]   ->  [1, 2, 3]
> 3 in u           ->  True
> ```
>
> **Why it works.** When Python needs to iterate an object with no `__iter__`, it falls back to the **legacy iteration protocol**: call `x[0]`, `x[1]`, `x[2]`, … and stop when `IndexError` is raised. Since `Vector.__getitem__` delegates to a `list`, the `IndexError` arrives exactly when the coordinates run out. Membership testing `3 in u` then falls back to iteration in turn.
>
> **So two methods bought four behaviours** — indexing, iteration, membership, and everything built on iteration (comprehensions, `list(u)`, `max(u)`, tuple unpacking).
>
> **Two cautions.**
> - The fallback works only because `__getitem__` raises `IndexError` for an out-of-range index. **If it raised `ValueError` instead, iteration would crash rather than terminate** — the protocol depends on the *specific* exception type.
> - For a structure where indexing is $O(n)$ — a linked list ([[06 - Linked Lists|ch. 06]]) — relying on this fallback makes iteration $O(n^2)$. **There, define `__iter__` explicitly**, usually as a generator.
>
> **Also worth noting:** defining `__eq__` without `__hash__` makes instances unhashable, so they cannot be dict keys or set members. Python does this deliberately — a mutable object with value equality would break the hash tables of [[09 - Maps, Hash Tables and Skip Lists|ch. 09]] if mutated after insertion.

**3. (Iterators and generators.)** (a) Implement an iterator class for any sequence. (b) Write a generator producing the factors of `n`. (c) State two advantages of the generator. (d) Why does `factors` loop only while `k*k < n`?

> [!example]- Solution
> **(a)** §4's `SequenceIterator`. The three requirements: `__next__` returns the next element, raises `StopIteration` when exhausted, and `__iter__` returns `self`. *(Verified: `10, 20, 30`, then `StopIteration`.)*
>
> **The `__iter__` returning `self` convention** is what lets an iterator be used directly in a `for` loop — a `for` loop calls `iter()` on its subject, and for an iterator that must be a no-op.
>
> **(b)** §4's `factors`. *(Verified: `sorted(factors(100))` = `[1, 2, 4, 5, 10, 20, 25, 50, 100]` — the nine divisors of 100.)*
>
> **(c)** 1. **Constant memory.** The generator yields values one at a time; the list is never materialised. For a large `n` — or an infinite sequence — this is the difference between working and not.
> 2. **Much less code, and no state to get wrong.** The generator is 8 lines with no explicit index; the iterator class is 10 lines with a `_k` field that must be initialised to `-1` and incremented in exactly the right place. **The commonest iterator bug is off-by-one in that index**, and generators eliminate the category.
>
> *(A third: laziness composes. `next(factors(n))` costs nothing beyond the first factor.)*
>
> **(d) Because divisors come in pairs.** If $k$ divides $n$ then so does $n/k$, and one member of each pair is $\le\sqrt n$. So looping to $\sqrt n$ and yielding **both** $k$ and $n/k$ finds every divisor in $O(\sqrt n)$ rather than $O(n)$.
>
> The trailing `if k*k == n: yield k` handles the perfect square, where $k$ and $n/k$ coincide and must be yielded **once** — omit it and `factors(36)` loses the divisor 6; make it `yield k; yield n//k` and it reports 6 twice. *(This is the same $\sqrt n$ argument as [[Discrete Mathematics/contents/05 - Number Theory and Cryptography|DM ch. 05]] §1's primality test.)*

**4. (Inheritance.)** Given the `CreditCard` class of §2, write `PredatoryCreditCard` adding an APR, charging a \$5 penalty on a declined charge, and accruing monthly interest. Identify what is overridden and what is extended.

> [!example]- Solution
> The implementation is §5's. Classifying each member:
>
> | Member | Kind | Note |
> |---|---|---|
> | `__init__` | **extended** | calls `super().__init__(...)`, then adds `_apr` |
> | `charge` | **overridden** | calls `super().charge(...)`, then adds the penalty |
> | `process_month` | **new** | no counterpart in the base class |
> | `get_balance`, `make_payment` | **inherited unchanged** | not mentioned in the subclass |
>
> *(Verified: the standard card declines a \$1500 charge and keeps balance 0; the predatory card declines it and ends at balance **5**. After `charge(500)` the balance is **505**, and after `process_month()` at 8.25% APR it is **508.35** — since $505\times(1.0825)^{1/12}=508.35$.)*
>
> **Two design points.**
>
> **Both modified methods call `super()` rather than duplicating the parent's code.** If the base class later changes how a limit is checked, the subclass inherits the fix automatically. **Copying the parent's body into the override is the standard way a class hierarchy rots** — the two copies drift apart and the bug appears in only one.
>
> **`charge` still returns the same thing it always did** (`True`/`False` for success). An override must honour the base class's contract — same signature, same meaning of the return value — or polymorphism breaks: code written against `CreditCard` would misbehave when handed a `PredatoryCreditCard`. *(That obligation is the Liskov substitution principle, and it is the practical reason `isinstance(pred, CreditCard)` being `True` is a promise and not just a fact.)*

**5. (Hard — ADTs and abstract base classes.)** (a) Define "abstract data type" and say why the concept organises this subject. (b) Write an ABC `Sequence` requiring `__len__` and `__getitem__` and providing `__contains__` and `index`. (c) Subclass it to re-implement `range`. (d) What does the ABC give you that duck typing does not? (e) Why is `Range(0, 10**100)` instant?

> [!example]- Solution
> **(a)** An **ADT** specifies **which operations exist and what they mean**, saying nothing about implementation. A *stack* is `push`/`pop`/`top`/`is_empty`; whether it is an array or a chain of nodes is invisible.
>
> **Why it organises the subject:** nearly every remaining chapter is *one ADT and two or three implementations*, and **the content is the comparison.** Because the implementations are interchangeable in behaviour and differ only in performance, the engineering question becomes purely "which operations do I perform, and how often?" — which is what the index's comparison table answers. **Without the ADT/implementation split there would be no basis for comparing anything.**
>
> **(b)–(c)** §7's `Sequence` and `Range`. *(Verified: `Range(2,20,3)` yields `[2, 5, 8, 11, 14, 17]`, `len` is 6, `14 in r` is `True` with `index` 4, `15 in r` is `False`, and instantiating `Sequence()` directly raises `TypeError`.)*
>
> **(d) Three things.**
> 1. **Shared concrete behaviour.** `__contains__` and `index` are written **once** in the ABC in terms of the two abstract methods, and every subclass inherits working versions. Duck typing gives no place to put shared code — each duck reimplements it.
> 2. **The contract is enforced at instantiation.** `Sequence()` raises `TypeError`, and so would a subclass that forgot `__getitem__`. **The error arrives when the object is created, not later when the missing method is finally called** — which in a data structure might be much later, under different data.
> 3. **It is documentation that cannot go stale**, because it is executable.
>
> **What duck typing still gives you** is reach: a function iterating its argument works with `list`, `str`, generators and `Vector` alike, none of which share a base class. **Python's real answer is to use both** — ABCs where shared implementation and an enforced contract pay for themselves, duck typing everywhere else. Note `collections.abc` ships exactly these ABCs (`Sequence`, `Mapping`, `MutableSet`, …) and **the subsequent chapters' ADTs mirror them deliberately.**
>
> **(e) Because `Range` stores three integers and computes on demand.** The constructor evaluates
> $$\texttt{length} = \max\left(0,\ \left\lfloor\frac{\text{stop}-\text{start}+\text{step}-1}{\text{step}}\right\rfloor\right)$$
> arithmetically, and `__getitem__` returns `start + k*step`. **No element is ever stored**, so construction is $O(1)$ in time and memory regardless of the range's size — `Range(0, 10**100)` is as cheap as `Range(0, 10)`.
>
> **This is the first appearance of the subject's central trade-off: store versus compute.** A list of $10^{100}$ integers is impossible; a rule for producing the $k$th on demand is trivial. **Python's own `range` works exactly this way**, which is why `range` is not a list and why `list(range(n))` is the expensive step.
>
> *(The ceiling-division idiom `(a + b - 1) // b` computes $\lceil a/b\rceil$ with integer arithmetic — worth recognising, it recurs in [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s resizing and [[08 - Priority Queues and Heaps|ch. 08]]'s heap indexing.)*

## 📝 Summary

- **A variable is a name bound to an object; assignment never copies.** `b = a` creates an **alias**. This one fact explains aliasing bugs, and **a data structure is deliberate aliasing** — so the distinction must be automatic.
- **Immutable** (`int`, `str`, `tuple`) versus **mutable** (`list`, `dict`, `set`, your classes) decides whether sharing matters. **Shallow copy duplicates the outer container and shares the inner objects**; `copy.deepcopy` recurses. `[[0]*2]*2` makes one row referenced twice.
- **Mutable default arguments are evaluated once at definition time** and shared across calls. Always use `None` as the default and build inside.
- **Encapsulation is by convention:** a single leading underscore means "internal". Python does not enforce it, and **that convention is what makes the ADT/implementation split real.**
- **Special methods make your class behave like a built-in:** `__len__`, `__getitem__`, `__setitem__`, `__add__`, `__eq__`, `__lt__`, `__str__`, `__repr__`, `__iter__`, `__contains__`.
- **Defining `__len__` and `__getitem__` gives iteration and `in` for free**, via the legacy protocol that indexes until `IndexError`. **It depends on that exact exception type**, and it makes iteration $O(n^2)$ for a structure with $O(n)$ indexing — define `__iter__` explicitly there.
- **`__str__` is for users, `__repr__` for developers** and should ideally recreate the object.
- **An iterator** provides `__next__` (raising `StopIteration`) and `__iter__` returning `self`. **A generator** — any function using `yield` — produces one automatically, in less code, with **$O(1)$ memory** and laziness. Tree traversals in [[07 - Trees and Traversals|ch. 07]] are naturally generators.
- **Inheritance: override** (replace, ideally by wrapping `super()`) versus **extend** (add). **Never copy the parent's body into an override** — that is how hierarchies rot. An override must honour the base class's contract or polymorphism breaks.
- **Duck typing** means an object works if it supports the operations used, regardless of class — so Python uses inheritance more for sharing implementation than for declaring types.
- **An ADT specifies operations and meanings, not implementation.** It is the organising idea of the subject: every later chapter is one ADT with several implementations, and **the content is always the comparison.**
- **An ABC** (`abc.ABCMeta`, `@abstractmethod`) enforces the contract at instantiation and, more usefully, **holds shared concrete methods** built on the abstract ones. `collections.abc` ships the standard ones.
- **Store versus compute** is the subject's first trade-off: `Range` holds three integers and computes elements on demand, so `Range(0, 10**100)` is instant.

## ⚠️ Important Notes

1. **`=` binds a name; it never copies.** Before debugging "why did this list change", check whether you have two names for one object. `a is b` answers it.
2. **Never use a mutable default argument.** `def f(x, acc=[])` shares `acc` across calls. Use `None` and construct inside — this is not a style preference, it is a correctness issue.
3. **`[[0]*n]*m` is almost always a bug.** It creates $m$ references to **one** row. Use a comprehension.
4. **Know whether you need a shallow or a deep copy**, and remember that a shallow copy of a structure containing mutable elements shares those elements.
5. **Use a single leading underscore for internals.** Nothing enforces it, but code that reaches into another object's `_fields` will break the moment the representation changes — which is the entire point of studying alternative representations.
6. **Prefer `super()` to naming the parent class explicitly.** It survives refactoring and behaves correctly under multiple inheritance.
7. **An override must keep the parent's signature and the meaning of its return value.** Otherwise code written against the base class silently misbehaves on subclass instances.
8. **`__getitem__` must raise `IndexError`, not another exception, for out-of-range access** — the automatic iteration fallback depends on it, and the wrong exception turns a clean loop termination into a crash.
9. **Do not rely on the `__getitem__` iteration fallback when indexing is not $O(1)$.** For linked structures it silently makes a single pass quadratic. Write `__iter__` as a generator instead.
10. **Defining `__eq__` makes instances unhashable** unless you also define `__hash__`. That is deliberate, and it protects [[09 - Maps, Hash Tables and Skip Lists|ch. 09]]'s hash tables from objects that change after insertion.
11. **Prefer generators to hand-written iterator classes.** Less code, no index to get wrong, $O(1)$ memory. Write the class only when you need several independent iterators over one object with non-trivial state.
12. **A generator returns immediately and computes nothing** until iterated. If you need the values more than once, materialise with `list(...)` — a generator is exhausted after one pass, and that silent exhaustion is a common bug.
13. **`isinstance` checks are usually a smell in Python.** Prefer duck typing or an ABC; reserve `isinstance` for genuinely polymorphic constructors like `Vector(5)` versus `Vector([1,2,3])`.
14. **Design to the ADT, not the implementation.** If your code depends on a stack being a list, swapping in a linked implementation breaks it — and the whole point of the next twelve chapters is that you should be free to swap.
15. **Store versus compute is a real choice, not an optimisation detail.** `range` computes; a list stores. The same question recurs for every structure ahead.

> [!warning] Gaps in the source material
> **This chapter's sources had to be used in an unusual split, and the reason is the most consequential extraction finding in the vault.**
>
> **Goodrich's code cannot be transcribed.** A Code Fragment extracts as
> ```
> 1 class GameEntry:
> 4 def  init  (self,n a m e ,s c o r e ) :
> 5 self.  name = name
> ```
> — **all indentation lost** (fatal in Python and unrecoverable without understanding the code), **double underscores rendered as spaces** (`__init__`→`init`, `_name`→`name`, so the result looks plausible and is wrong), and **identifiers space-separated** with operators broken (`*=`→`=`). Line numbers do survive, which at least marks where lines begin. **Goodrich's prose, by contrast, extracts cleanly**, so it is used here for structure, terminology and the design discussion.
>
> **Lambert's code extracts perfectly** — indentation, dunders and docstrings all intact — so it is the usable source wherever the two books overlap. Full detail in `00-Index.md`.
>
> **Consequently every listing in this chapter is my own**, written from understanding rather than transcribed, **and every one was executed before being written down.** The verified outputs are quoted inline: the aliasing and mutable-default demonstrations; the `Vector` class with all its operations including the `ValueError` on mismatched dimensions and the free iteration/membership; `SequenceIterator` including the `StopIteration`; `factors(100)` giving the nine divisors of 100; the `CreditCard`/`PredatoryCreditCard` sequence (balances 0, 5, 505, 508.35); and `Range(2,20,3)` with its `index`, membership tests and the `TypeError` from instantiating the ABC.
>
> **The class designs follow Goodrich's** (`CreditCard`, `Vector`, `SequenceIterator`, `Range` are his examples, recognisable from the surviving prose and section headings) **but the code is a reconstruction, not a transcription.** Where his exact implementation choices are unrecoverable I have used the idiomatic version and verified it behaves as the prose describes.
>
> **All figures are images and are lost** — including the class-diagram illustrations of §2.4's inheritance hierarchies and the progress-of-execution diagrams. **Table 2.1 (the catalogue of overloaded operations) did not survive**; §3's table is reconstructed from the surrounding prose and from the Python documentation, and each entry was confirmed by use.
>
> **No error was found in either source** — though note that little of Goodrich's *code* could be checked against, since it is unreadable; the verification here is that my reconstructions behave as his prose says they should.
>
> **Additions beyond the sources.** The **mutable default argument** trap, the **`[[0]*n]*m`** trap and the shallow/deep copy demonstration are mine — Goodrich mentions aliasing but does not collect the practical failure modes, and they are the ones that actually bite when implementing containers. The observation that **`__len__` + `__getitem__` buys iteration and membership for free via the legacy protocol**, that it **depends on `IndexError` specifically**, and that it is **$O(n^2)$ for linked structures**, is my own emphasis and is a forward pointer to [[06 - Linked Lists|ch. 06]]. The note that **`__eq__` without `__hash__` makes instances unhashable**, and why that protects [[09 - Maps, Hash Tables and Skip Lists|ch. 09]], is mine. The **Liskov substitution** framing of Exercise 4, the **store-versus-compute** framing of Exercise 5(e), and the remark that `collections.abc` ships the ABCs the later chapters mirror, are additions. The comparison with [[Basic Programming (C++)/contents/00-Index|C++]] on duck typing versus compile-time type checking is mine.
>
> **Deliberately compressed.** **Goodrich ch. 1 (the Python primer — expressions, control flow, files, exceptions, comprehensions, modules) is reduced to §1's object model**, on the assumption that a Data Science major has Python already; only what the *rest of this subject* needs is kept. **Goodrich §§2.1.3 (design patterns) and 2.2 (software development, pseudo-code, testing and debugging)** are omitted as process material rather than data-structure content — though **§2.2.4's point that a container must be tested on empty, single-element and duplicate inputs is adopted as this subject's standing verification rule** (see `00-Index.md`). **Lambert ch. 5–6 (interfaces, implementations, inheritance, abstract classes)** are folded into §§5–7 rather than treated separately.

**Previous:** [[00-Index]] · **Next:** [[02 - Algorithm Analysis in Practice]]
