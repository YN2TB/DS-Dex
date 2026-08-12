---
subject: Discrete Mathematics
chapter: 5
tags: [ds, discrete-mathematics, number-theory, primes, gcd, euclidean-algorithm, modular-arithmetic, rsa, cryptography]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 5 (book pp. 214–254)"
---

# Number Theory and Cryptography

Number theory was, for most of its history, the purest branch of mathematics — G. H. Hardy famously boasted that it had no practical use. Then in 1977 Rivest, Shamir and Adleman built a cryptosystem on it, and now **every secure transaction on the internet depends on the material in this chapter.**

The arc is short and it closes cleanly. §1 defines divisibility and primes; §2 shows how integers are actually represented and computed with; §3 gives the Euclidean algorithm, one of the oldest algorithms in existence and still asymptotically optimal; and §4 assembles all of it into RSA. Two earlier chapters supply the foundations: the **Quotient–Remainder Theorem** of [[02 - Proofs and Mathematical Induction|ch. 02]] §8, which is what makes `mod` well defined, and the observation from [[03 - Functions, Sequences and Relations|ch. 03]] §6 that **congruence mod $n$ is an equivalence relation** — which is precisely why arithmetic on remainders is legitimate.

## 📘 Main Knowledge

### 1. Divisors and primes

> [!note] Definition
> Let $n,d$ be integers with $d\ne0$. **$d$ divides $n$**, written $d\mid n$, if there is an integer $q$ with $n=dq$. Then $q$ is the **quotient** and $d$ a **divisor** (or **factor**) of $n$. If $d$ does not divide $n$ we write $d\nmid n$.

So $3\mid21$ since $21=3\cdot7$. Note the definition is existential — "there is an integer $q$" — so it behaves exactly as [[02 - Proofs and Mathematical Induction|ch. 02]] §1 described: *assuming* $d\mid n$ hands you a $q$; *proving* $d\mid n$ requires producing one.

**And $d\mid n$ iff the remainder is zero:** by the Quotient–Remainder Theorem, $n=dq+r$ with $0\le r<d$ uniquely, and $r=0$ exactly when $d$ divides $n$. That is the bridge between the definition and the computation `n % d == 0`.

**Basic properties** (Johnsonbaugh's Theorem 5.1.3). If $d\mid m$ and $d\mid n$ then $d\mid(m+n)$, $d\mid(m-n)$, and $d\mid cm$ for any integer $c$. Each is a one-line proof from the definition — e.g. $m=dq_1$, $n=dq_2$ give $m+n=d(q_1+q_2)$. *(Note the distinct witnesses $q_1,q_2$ — ch. 02's Important Note 1.)*

> [!note] Definition
> An integer $>1$ whose only positive divisors are itself and $1$ is **prime**. An integer $>1$ that is not prime is **composite**.

**Testing primality: the $\sqrt n$ bound.** Naively one tests $2,3,\dots,n-1$. But:

> [!note] Theorem 5.1.7
> $n>1$ is composite **if and only if** $n$ has a divisor $d$ with $2\le d\le\sqrt n$.

*Proof idea.* If $n$ is composite it has a divisor $d'$ with $2\le d'<n$. If $d'\le\sqrt n$ we are done. Otherwise $d'>\sqrt n$, and its cofactor $q=n/d'$ is also a divisor — and $q\le\sqrt n$, since $q>\sqrt n$ together with $d'>\sqrt n$ would give $n=d'q>n$, a contradiction. $\blacksquare$

**The divisors of $n$ come in pairs $(d,n/d)$ straddling $\sqrt n$**, so it suffices to look below. That cuts the work from $n$ trials to $\sqrt n$ — verified: $43$ needs only $d\le6$ and has no divisor there, hence is prime; $451$ needs $d\le21$ and $11\mid451$ ($451=11\cdot41$), hence is composite.

```python
def is_prime(n):                 # returns 0 if prime, else a prime divisor
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return 0
```

> [!warning] $\sqrt n$ trials is still exponential time
> This is Johnsonbaugh's own observation and it is the point on which the whole chapter turns. The *size of the input* is not $n$ but the **number of digits** — a $k$-bit integer $n$ satisfies $n<2^k$, so $\sqrt n<2^{k/2}$. The algorithm therefore runs in $\Theta(2^{k/2})$ time **in the length of its input**: exponential, in the sense of [[04 - Algorithms and Their Analysis|ch. 04]].
>
> **Measuring complexity in $n$ instead of $\log n$ is the classic error in number-theoretic algorithms.** It is why "just test all divisors" does not break RSA, and why a 2048-bit key is safe against a method that would need $2^{1024}$ trials. *(Polynomial-time primality testing does exist — AKS, 2002 — but polynomial-time **factoring** does not, and RSA rests on that gap.)*

**Notice the algorithm returns a *prime* divisor.** If it returned a composite $a$, then $a$ has a divisor $a'<a$ which also divides $n$, so the loop would have returned $a'$ first — a contradiction. Repeating the extraction therefore factors any integer completely: $1274\to2\to7\to7\to13$, giving $1274=2\cdot7^2\cdot13$ *(verified)*.

> [!note] Theorem 5.1.11 — the Fundamental Theorem of Arithmetic
> **Every integer $>1$ can be written as a product of primes, and if the primes are written in nondecreasing order the factorization is unique.**

Uniqueness is the deep half and is easy to take for granted; it is what makes "the prime factorization" a well-defined object, and hence what makes $\gcd$ and $\operatorname{lcm}$ computable from factorizations.

> [!note] Theorem 5.1.12 — there are infinitely many primes
> *Proof (Euclid).* It suffices to show that for any prime $p$ there is a larger one. Let $p_1,\dots,p_n$ be **all** primes $\le p$ and set
> $$m=p_1p_2\cdots p_n+1 .$$
> Each $p_i$ divides $p_1\cdots p_n$, so if $p_i$ also divided $m$ it would divide the difference $m-p_1\cdots p_n=1$ — impossible. So **no $p_i$ divides $m$.** Let $p'$ be any prime factor of $m$. Then $p'$ is none of the $p_i$, and since the $p_i$ were all primes $\le p$, we must have $p'>p$. $\blacksquare$
>
> **A frequent misreading:** the proof does **not** claim $m$ is prime. It claims $m$ has a prime factor outside the list. With $p=11$: $m=2\cdot3\cdot5\cdot7\cdot11+1=2311$, which happens to be prime *(verified)* — but at $p=13$, $m=30031=59\cdot509$, prime factors both larger than 13 and neither equal to $m$. The proof works either way, which is exactly why it is stated in terms of "a prime factor of $m$".

**Greatest common divisor and least common multiple.** For integers $m,n$ not both zero, $\gcd(m,n)$ is the largest integer dividing both, and $\operatorname{lcm}(m,n)$ the smallest positive integer divisible by both. If $\gcd(m,n)=1$ the integers are **relatively prime** (coprime) — equivalently, the fraction $m/n$ is in lowest terms.

Both can be read off prime factorizations — take the minimum exponent of each prime for $\gcd$, the maximum for $\operatorname{lcm}$ — from which

$$\gcd(m,n)\cdot\operatorname{lcm}(m,n)=mn$$

follows, since $\min(a,b)+\max(a,b)=a+b$ for each exponent. **But factoring is expensive**, which is the whole reason §3 exists.

### 2. How integers are represented

A **bit** is a binary digit. In base $b$, the string $d_kd_{k-1}\cdots d_1d_0$ denotes

$$d_kb^k+d_{k-1}b^{k-1}+\cdots+d_1b+d_0 .$$

**Binary** ($b=2$) uses digits $0,1$; **hexadecimal** ($b=16$) uses $0$–$9$ and $A$–$F$ for $10$–$15$. So $101101_2=45$ and $\mathrm{B4F}_{16}=11\cdot256+4\cdot16+15=2895$ *(verified)*.

**Base $b$ to decimal** is Horner's rule and runs in $\Theta(k)$ for a $k$-digit input. **Decimal to base $b$** is repeated division: divide by $b$, record the remainder, repeat; **the remainders are the digits, least significant first.** So $20385=4\mathrm{FA1}_{16}$ *(verified)*.

> [!note] Digit count — the formula to remember
> A positive integer $m$ has exactly $\lfloor1+\log_b m\rfloor$ digits in base $b$; in binary, $\lfloor1+\lg m\rfloor$ bits.
>
> *(Verified: $91$ has $7$ bits, $130$ has $8$, $20385$ has $15$.)* **This is the identity that converts between "the value of $n$" and "the size of the input", and forgetting it produces the exponential-time confusion of §1.** Note also that hexadecimal is popular precisely because $16=2^4$: each hex digit is exactly four bits, so conversion is regrouping rather than arithmetic.

**Arithmetic in any base** uses the school algorithms with the base's addition table; in binary $1+1=10_2$. Adding two $n$-digit numbers is $\Theta(n)$.

**Exponentiation by repeated squaring.** Computing $a^{29}$ by $28$ multiplications is wasteful. Instead use the binary expansion $29=11101_2=16+8+4+1$:

$$a^{29}=a^{16}\cdot a^8\cdot a^4\cdot a^1,$$

and the powers $a,a^2,a^4,a^8,a^{16}$ come from **four squarings**. In general $a^n$ needs $\Theta(\lg n)$ multiplications rather than $n$.

```python
def power_mod(a, n, z):          # a^n mod z by repeated squaring
    result = 1
    a %= z
    while n > 0:
        if n % 2 == 1:           # this bit is set
            result = (result * a) % z
        a = (a * a) % z
        n //= 2
    return result
```

> [!note] Theorem 5.2.17 — and why the `% z` sits inside the loop
> For positive integers $a,b,z$:
> $$ab\bmod z=\big((a\bmod z)(b\bmod z)\big)\bmod z .$$
> **So you may reduce mod $z$ at every step**, and this is what makes modular exponentiation practical: without it, $a^{29}$ for a 600-digit $a$ would be an astronomically long integer. With it, every intermediate value stays below $z^2$.
>
> This theorem is the computational face of [[03 - Functions, Sequences and Relations|ch. 03]] §6: **multiplication is well defined on equivalence classes mod $z$**, so it does not matter which representative you carry. Johnsonbaugh's worked case is $572^{29}\bmod713=113$ *(verified)* — and it is no accident that this is exactly an RSA encryption, as §4 shows.

### 3. The Euclidean algorithm

Computing $\gcd$ by factoring is hopeless for large inputs. The Euclidean algorithm — about 2300 years old — needs no factorization at all.

> [!note] Theorem 5.3.2 — the whole idea
> If $a\ge0$, $b>0$ and $r=a\bmod b$, then
> $$\gcd(a,b)=\gcd(b,r).$$

*Proof idea.* Write $a=bq+r$. Any common divisor of $b$ and $r$ divides $bq+r=a$, so it is a common divisor of $a$ and $b$; conversely any common divisor of $a$ and $b$ divides $a-bq=r$. **The two pairs have exactly the same set of common divisors**, hence the same greatest one. $\blacksquare$

Iterating shrinks the arguments until the second is $0$, and $\gcd(a,0)=a$.

```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
```

*Verified trace of $\gcd(504,396)$:*
$$504\bmod396=108,\quad 396\bmod108=72,\quad 108\bmod72=36,\quad 72\bmod36=0,$$
returning $\mathbf{36}$ after **4** modulus operations.

**Correctness is a loop invariant** ([[02 - Proofs and Mathematical Induction|ch. 02]] §6): $G=\gcd(a,b)$ holds before the loop, is preserved by each iteration (Theorem 5.3.2), and when $b=0$ becomes $G=\gcd(a,0)=a$ — the returned value. **Termination** holds because $b$ strictly decreases and is a nonnegative integer, so by well-ordering it cannot decrease forever.

> [!example]- The worst case is the Fibonacci sequence
> How bad can it get? Tabulating the smallest input pair $(a,b)$ with $a>b$ requiring $n$ modulus operations gives a startling pattern *(verified by exhaustive search over all $a<400$)*:
>
> | $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
> |---|---|---|---|---|---|---|---|---|
> | smallest $a$ | 1 | 2 | 3 | 5 | 8 | 13 | 21 | 34 |
> | smallest $b$ | 0 | 1 | 2 | 3 | 5 | 8 | 13 | 21 |
>
> **These are consecutive Fibonacci numbers:** the smallest pair needing $n$ steps is $(f_{n+2},f_{n+1})$, where $f_1=f_2=1$ and $f_n=f_{n-1}+f_{n-2}$.
>
> **Why:** to make the algorithm work hardest you want each quotient to be as small as possible, i.e. $1$, so that $a\bmod b=a-b$. That is exactly the Fibonacci recurrence run backwards — consecutive Fibonacci numbers are the slowest possible descent.
>
> **The consequence is the complexity bound.** Since $f_n$ grows like $\phi^n$ with $\phi=\frac{1+\sqrt5}2$, requiring $n$ steps forces $a\ge f_{n+2}\approx\phi^{n+2}$, so
> $$n=O(\log_\phi a)=O(\log a).$$
> **The Euclidean algorithm is logarithmic in its input value — that is, *linear in the number of digits*.** Contrast §1's factoring, which is exponential in the digits. **This gap is the entire practical basis of RSA:** computing gcds is cheap, factoring is not. (The result is Lamé's theorem, 1844 — historically the first analysis of an algorithm's running time.)

**The extended Euclidean algorithm.** Running the recursion while tracking coefficients yields Bézout's identity:

$$\gcd(m,n)=sm+tn\qquad\text{for some integers }s,t .$$

*(Verified: $\gcd(504,396)=36=4\cdot504-5\cdot396$.)*

```python
def egcd(a, b):                  # returns (g, s, t) with g = gcd(a,b) = s*a + t*b
    if b == 0:
        return a, 1, 0
    g, s, t = egcd(b, a % b)
    return g, t, s - (a // b) * t
```

**This is how modular inverses are computed**, and it is the step §4 cannot do without. If $\gcd(e,\varphi)=1$ then $se+t\varphi=1$, so $se\equiv1\pmod\varphi$ and $s\bmod\varphi$ is the inverse of $e$. *(Verified: $\gcd(29,660)=1$ with $s=-91$, so $29^{-1}\equiv569\pmod{660}$, and indeed $29\cdot569\equiv1$.)*

**An inverse exists mod $\varphi$ exactly when $\gcd(e,\varphi)=1$** — which is why coprimality is demanded everywhere below.

### 4. The RSA public-key cryptosystem

**The problem with private keys.** In a classical cipher — Johnsonbaugh's example substitutes a permuted alphabet, so `SEND MONEY` becomes `QARUESKRAN` — sender and receiver share one secret key. Two weaknesses: simple substitution falls to frequency analysis (E is the commonest English letter, ER the commonest pair), and, more fundamentally, **the key itself must somehow be delivered securely first.** That is a chicken-and-egg problem.

**RSA's idea** (Rivest, Shamir, Adleman) removes it: **each participant publishes an encryption key and keeps a decryption key secret.** Anyone can encrypt to you; only you can decrypt. No secret ever needs to travel.

> [!note] The construction
> **Key generation.** The recipient:
> 1. chooses two large primes $p,q$ and computes $z=pq$;
> 2. chooses $e$ **relatively prime** to $(p-1)(q-1)$;
> 3. computes $s$ with $se\equiv1\pmod{(p-1)(q-1)}$ — by the extended Euclidean algorithm of §3.
>
> **Public key: $(z,e)$. Private key: $s$** (and $p,q$, which must be destroyed or kept secret).
>
> **Encryption** of a message $a$ with $0\le a<z$: $\ c=a^e\bmod z$.
> **Decryption:** $\ a=c^s\bmod z$.
>
> Both directions are modular exponentiation, so both are fast by §2's repeated squaring.

Messages are numbers: with blank $=1$, A $=2$, B $=3$, …, `SEND MONEY` becomes $20,6,15,5,1,14,16,15,6,26$, optionally concatenated into one integer.

> [!example]- A complete worked round-trip (all values verified)
> Take $p=23$, $q=31$. Then
> $$z=pq=713,\qquad (p-1)(q-1)=22\cdot30=660 .$$
> Choose $e=29$. Check coprimality: $660=2^2\cdot3\cdot5\cdot11$ and $29$ is prime and not among those, so $\gcd(29,660)=1$ ✓
>
> Private key from the extended Euclidean algorithm: $s=\mathbf{569}$, since $29\cdot569=16501=25\cdot660+1$, i.e. $29\cdot569\equiv1\pmod{660}$ ✓
>
> **Encrypt $a=572$:** $\ c=572^{29}\bmod713=\mathbf{113}$ — which is exactly Johnsonbaugh's Example 5.2.18, now revealed as an RSA encryption.
>
> **Decrypt:** $\ 113^{569}\bmod713=\mathbf{572}$ ✓ Round-trip confirmed, and also for $a=100\to288\to100$ and $a=3\to393\to3$.
>
> **One curiosity worth noticing:** $a=712$ encrypts to $712$. That is not a bug — $712\equiv-1\pmod{713}$ and $29$ is odd, so $(-1)^{29}=-1$. **RSA always has some fixed points** (at least $0$, $1$ and $z-1$), which is one of several reasons real implementations never encrypt a raw message but pad it first (OAEP).

**Why it works.** The identity behind decryption is that $a^{es}\equiv a\pmod z$ whenever $es\equiv1\pmod{(p-1)(q-1)}$. This follows from Fermat's little theorem applied mod $p$ and mod $q$ separately, then recombined — Johnsonbaugh gives the argument, and the modern route is Euler's theorem with $\varphi(z)=(p-1)(q-1)$.

> [!warning] Why RSA is believed secure — and exactly what it rests on
> An attacker knows $z$ and $e$. To find $s$ they need $(p-1)(q-1)$, which needs $p$ and $q$ — that is, **they must factor $z$.**
>
> So the security rests on an *asymmetry of difficulty*, and this chapter has quantified both sides:
> - **multiplying $p$ and $q$**: fast, $\Theta(k^2)$ or better by §2;
> - **computing $\gcd$ and modular inverses**: fast, $O(\log)$ by §3;
> - **modular exponentiation**: fast, $\Theta(\lg n)$ multiplications by §2;
> - **factoring $z$**: no known polynomial-time method, and §1's trial division is $\Theta(2^{k/2})$.
>
> **"Believed secure" is the honest phrase.** No proof exists that factoring is hard — it is not known to be NP-complete either. Two caveats worth carrying: **Shor's algorithm factors in polynomial time on a quantum computer**, which is why post-quantum cryptography is an active field; and in practice RSA is broken far more often through implementation faults — poor randomness in choosing $p,q$, reused primes, no padding, timing side channels — than through factoring.

## ✏️ Exercises

**1. (Divisors and primes.)** (a) Determine whether $221$ and $227$ are prime, stating how many trial divisions the $\sqrt n$ bound requires. (b) Give the prime factorization of $2520$. (c) Compute $\gcd(2520,594)$ and $\operatorname{lcm}(2520,594)$ from factorizations, and verify $\gcd\cdot\operatorname{lcm}=mn$. (d) Explain why Euclid's proof does **not** show $p_1p_2\cdots p_n+1$ is prime.

> [!example]- Solution
> **(a)** $\lfloor\sqrt{221}\rfloor=14$, so test $d=2,\dots,14$ — **13 trial divisions**. We find $13\mid221$ ($221=13\cdot17$), so **221 is composite**.
> $\lfloor\sqrt{227}\rfloor=15$, so test $d=2,\dots,15$. None divides $227$ (it is odd, digit sum $11$ so not divisible by 3, does not end in 0/5, and $7,11,13$ fail), so **227 is prime**.
>
> **(b)** Repeatedly extract the smallest prime factor:
> $$2520=2\cdot1260=2^2\cdot630=2^3\cdot315=2^3\cdot3\cdot105=2^3\cdot3^2\cdot35=\mathbf{2^3\cdot3^2\cdot5\cdot7}.$$
> Check: $8\cdot9\cdot5\cdot7=2520$ ✓
>
> **(c)** $594=2\cdot297=2\cdot3^3\cdot11$.
>
> | prime | in 2520 | in 594 | min (gcd) | max (lcm) |
> |---|---|---|---|---|
> | 2 | $2^3$ | $2^1$ | $2^1$ | $2^3$ |
> | 3 | $3^2$ | $3^3$ | $3^2$ | $3^3$ |
> | 5 | $5^1$ | — | $5^0$ | $5^1$ |
> | 7 | $7^1$ | — | $7^0$ | $7^1$ |
> | 11 | — | $11^1$ | $11^0$ | $11^1$ |
>
> $$\gcd=2\cdot3^2=\mathbf{18},\qquad \operatorname{lcm}=2^3\cdot3^3\cdot5\cdot7\cdot11=\mathbf{83160}.$$
> Check: $18\cdot83160=1496880$ and $2520\cdot594=1496880$ ✓
>
> **Why the identity holds:** for each prime, $\min(a,b)+\max(a,b)=a+b$, so multiplying $\gcd$ by $\operatorname{lcm}$ recovers every prime to its total exponent — i.e. $mn$.
>
> **(d)** The proof shows only that **no $p_i$ divides $m=p_1\cdots p_n+1$** — because each $p_i$ divides the product, so dividing $m$ too would force $p_i\mid1$. From that it concludes that **any prime factor of $m$** lies outside the list, hence exceeds $p$. Whether $m$ is itself prime is irrelevant and often false:
> - $p=11$: $m=2311$, which **is** prime *(verified)*;
> - $p=13$: $m=30031=59\cdot509$ — **composite**, but both factors exceed 13, so the conclusion still holds.
>
> **This is why the proof is phrased in terms of "a prime factor of $m$", and misremembering it as "$m$ is prime" turns a correct proof into a false claim.**

**2. (Representations.)** (a) Convert $1011011_2$ and $\mathrm{B4F}_{16}$ to decimal. (b) Convert $130$ to binary and $20385$ to hexadecimal. (c) How many bits does $20385$ need, and how does the formula confirm it? (d) Compute $3^{13}\bmod7$ by repeated squaring, showing the intermediate values, and say how many multiplications you used versus the naive method.

> [!example]- Solution
> **(a)** $1011011_2=1\cdot64+0+1\cdot16+1\cdot8+0+1\cdot2+1=64+16+8+2+1=\mathbf{91}$.
> $\mathrm{B4F}_{16}=11\cdot16^2+4\cdot16+15=2816+64+15=\mathbf{2895}$ *(verified)*.
>
> **(b)** Repeated division by 2, remainders bottom-up:
> $$130\to65\ r0,\quad65\to32\ r1,\quad32\to16\ r0,\quad16\to8\ r0,\quad8\to4\ r0,\quad4\to2\ r0,\quad2\to1\ r0,\quad1\to0\ r1$$
> Reading the remainders in reverse: $130=\mathbf{10000010_2}$ ✓
>
> For hex, divide by 16: $20385=1274\cdot16+1$; $1274=79\cdot16+10\ (\mathrm A)$; $79=4\cdot16+15\ (\mathrm F)$; $4=0\cdot16+4$. Reading upward: $20385=\mathbf{4FA1_{16}}$ ✓ *(both verified)*
>
> **(c)** $20385$ needs **15 bits** ($100111110100001_2$). The formula gives
> $$\lfloor1+\lg20385\rfloor=\lfloor1+14.316\rfloor=\lfloor15.316\rfloor=15\ \checkmark$$
> Cross-check with hex: $4\mathrm{FA1}$ has 4 hex digits $=16$ bits, but the leading digit $4=0100_2$ contributes only 3 significant bits, so $16-1=15$ ✓
>
> **(d)** $13=1101_2=8+4+1$, so $3^{13}=3^8\cdot3^4\cdot3^1$. Working mod 7 throughout (Theorem 5.2.17 permits reducing at every step):
>
> | | value mod 7 | in expansion? |
> |---|---|---|
> | $3^1$ | $3$ | ✔ ($1$) |
> | $3^2$ | $9\equiv2$ | ✘ |
> | $3^4$ | $2^2=4$ | ✔ ($4$) |
> | $3^8$ | $4^2=16\equiv2$ | ✔ ($8$) |
>
> $$3^{13}\equiv3\cdot4\cdot2=24\equiv\mathbf3\pmod7 .$$
> *(Check: $3^{13}=1594323=227760\cdot7+3$ ✓)*
>
> **Cost:** 3 squarings plus 2 multiplications to combine $=$ **5 multiplications**, versus **12** for the naive $3\cdot3\cdots3$. The saving is $\Theta(\lg n)$ against $\Theta(n)$ — modest here, decisive in RSA where $n$ has hundreds of digits and the naive method is simply impossible. **And every intermediate value stayed below 49**, which is the other half of the point: without reducing mod 7 inside the loop, $3^{13}$ would already be a seven-digit number.

**3. (Euclidean algorithm.)** (a) Compute $\gcd(1071,462)$ by the Euclidean algorithm, showing each step and counting modulus operations. (b) Find the smallest pair $(a,b)$ with $a>b$ requiring exactly 6 modulus operations, and identify the pattern. (c) Deduce the algorithm's complexity in the number of digits of the input. (d) Contrast with computing $\gcd$ by factoring.

> [!example]- Solution
> **(a)**
> $$\begin{aligned} 1071\bmod462&=147\\ 462\bmod147&=21\\ 147\bmod21&=0 \end{aligned}$$
> $\gcd(1071,462)=\mathbf{21}$, in **3 modulus operations**. *(Sanity check by factoring: $1071=3^2\cdot7\cdot17$, $462=2\cdot3\cdot7\cdot11$, so $\gcd=3\cdot7=21$ ✓)*
>
> **(b)** Exhaustive search *(verified over all $a<400$)* gives $(a,b)=(\mathbf{21},\mathbf{13})$ — and the full table is
>
> | $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
> |---|---|---|---|---|---|---|---|---|
> | smallest $a$ | 1 | 2 | 3 | 5 | 8 | 13 | **21** | 34 |
> | smallest $b$ | 0 | 1 | 2 | 3 | 5 | 8 | **13** | 21 |
>
> **These are consecutive Fibonacci numbers:** the smallest pair needing $n$ steps is $(f_{n+2},f_{n+1})$.
>
> **Why Fibonacci is the worst case.** Each step replaces $(a,b)$ by $(b,a\bmod b)$; the arguments shrink *slowest* when each quotient is as small as possible, namely $1$, so that $a\bmod b=a-b$. Running that backwards, $a=b+r$ with $r$ the previous $b$ — which is exactly $f_{n+2}=f_{n+1}+f_n$. **Consecutive Fibonacci numbers are the slowest possible descent, by construction.**
>
> **(c)** Since $n$ steps force $a\ge f_{n+2}$, and $f_n\sim\phi^n/\sqrt5$ with $\phi=\frac{1+\sqrt5}2\approx1.618$:
> $$\phi^{n+2}\lesssim\sqrt5\,a\ \Longrightarrow\ n=O(\log_\phi a)=O(\log a).$$
> By §2's digit-count formula, $\log a$ is proportional to the **number of digits $k$** of $a$. **So the Euclidean algorithm is $O(k)$ — linear in the input size**, i.e. genuinely polynomial-time. *(This is Lamé's theorem, 1844 — the first published running-time analysis of an algorithm.)*
>
> **(d)** Computing $\gcd(m,n)$ by factoring requires factoring both, and §1's trial division is $\Theta(\sqrt n)=\Theta(2^{k/2})$ — **exponential in the digits.** For 20-digit numbers the Euclidean algorithm needs a few dozen operations; trial division needs about $10^{10}$.
>
> **This is the asymmetry RSA is built on**, and it is worth stating plainly: **$\gcd$ is easy, factoring is hard, and they are not the same problem.** It is a common intuition that finding a common factor requires finding the factors; the Euclidean algorithm refutes it.

**4. (Bézout and modular inverses.)** (a) Use the extended Euclidean algorithm to write $\gcd(240,46)$ as $240s+46t$. (b) Find $17^{-1}\bmod60$. (c) State exactly when $a^{-1}\bmod m$ exists, and give an $a,m$ for which it does not. (d) Why does RSA key generation need this?

> [!example]- Solution
> **(a)** Forward pass:
> $$240=5\cdot46+10,\qquad 46=4\cdot10+6,\qquad 10=1\cdot6+4,\qquad 6=1\cdot4+2,\qquad 4=2\cdot2+0$$
> so $\gcd(240,46)=\mathbf2$. Back-substituting:
> $$2=6-1\cdot4=6-(10-6)=2\cdot6-10=2(46-4\cdot10)-10=2\cdot46-9\cdot10=2\cdot46-9(240-5\cdot46)$$
> $$\boxed{2=-9\cdot240+47\cdot46}$$
> Check: $-2160+2162=2$ ✓
>
> **(b)** $\gcd(17,60)$: $60=3\cdot17+9$, $17=1\cdot9+8$, $9=1\cdot8+1$, $8=8\cdot1+0$, so $\gcd=1$ and an inverse exists. Back-substituting:
> $$1=9-8=9-(17-9)=2\cdot9-17=2(60-3\cdot17)-17=2\cdot60-7\cdot17 .$$
> So $-7\cdot17\equiv1\pmod{60}$, giving
> $$17^{-1}\equiv-7\equiv\mathbf{53}\pmod{60}.$$
> Check: $17\cdot53=901=15\cdot60+1$ ✓
>
> **(c) $a^{-1}\bmod m$ exists if and only if $\gcd(a,m)=1$.**
>
> (⟸) If $\gcd(a,m)=1$, Bézout gives $sa+tm=1$, so $sa\equiv1\pmod m$ and $s\bmod m$ is the inverse.
> (⟹) If $d=\gcd(a,m)>1$ and $ab\equiv1\pmod m$, then $ab-1=km$, so $d$ divides $ab-km=1$ — impossible.
>
> **Example with no inverse:** $a=6$, $m=9$. Here $\gcd(6,9)=3$, and indeed $6b\bmod9$ takes only the values $0,6,3$ as $b$ ranges over $0,\dots,8$ — never $1$.
>
> **(d)** Step 3 of key generation requires $s$ with $se\equiv1\pmod{(p-1)(q-1)}$ — that is, **$s$ is the modular inverse of $e$**, and the extended Euclidean algorithm is how it is computed. Part (c) explains why step 2 insists that $e$ be **relatively prime** to $(p-1)(q-1)$: without coprimality no inverse exists, no private key exists, and the scheme does not get off the ground.
>
> **Note also what makes this practical:** the extended Euclidean algorithm is $O(\log)$ by Exercise 3, so key generation is fast even for 2048-bit keys. **The same asymmetry as before — the legitimate operations are all cheap.**

**5. (Hard — RSA end to end.)** Let $p=23$, $q=31$, $e=29$. (a) Compute $z$, $(p-1)(q-1)$, and verify $e$ is a valid choice. (b) Find the private key $s$. (c) Encrypt $a=572$ and decrypt the result. (d) Explain why decryption recovers the message. (e) An attacker knows $z=713$ and $e=29$. What must they do, and why is that hard for realistic key sizes? (f) Why does $a=712$ encrypt to itself, and what does that imply for real implementations?

> [!example]- Solution
> **(a)** $z=pq=23\cdot31=\mathbf{713}$ and $(p-1)(q-1)=22\cdot30=\mathbf{660}$.
>
> $e=29$ is valid iff $\gcd(29,660)=1$. Since $660=2^2\cdot3\cdot5\cdot11$ and $29$ is prime, not appearing in that factorization, $\gcd(29,660)=1$ ✓ *(verified)*
>
> **Public key $(713,29)$.**
>
> **(b)** Solve $29s\equiv1\pmod{660}$ by the extended Euclidean algorithm:
> $$660=22\cdot29+22,\qquad 29=1\cdot22+7,\qquad 22=3\cdot7+1,\qquad 7=7\cdot1+0$$
> Back-substituting: $1=22-3\cdot7=22-3(29-22)=4\cdot22-3\cdot29=4(660-22\cdot29)-3\cdot29=4\cdot660-91\cdot29$.
>
> So $-91\cdot29\equiv1\pmod{660}$ and
> $$s\equiv-91\equiv\mathbf{569}\pmod{660}.$$
> Check: $29\cdot569=16501=25\cdot660+1$ ✓ *(verified)* **Private key $s=569$.**
>
> **(c)** Encrypt by repeated squaring mod 713:
> $$c=572^{29}\bmod713=\mathbf{113}$$
> — Johnsonbaugh's Example 5.2.18, now in context. Decrypt:
> $$113^{569}\bmod713=\mathbf{572}\ \checkmark$$
> *(Both verified; the round trip also works for $a=100\to288\to100$ and $a=3\to393\to3$.)*
>
> **(d)** Decryption computes $(a^e)^s=a^{es}\bmod z$, so it suffices that
> $$a^{es}\equiv a\pmod z\quad\text{whenever } es\equiv1\!\!\pmod{(p-1)(q-1)}.$$
> Write $es=1+k(p-1)(q-1)$. Work mod $p$ first. If $p\nmid a$, Fermat's little theorem gives $a^{p-1}\equiv1\pmod p$, so
> $$a^{es}=a\cdot\big(a^{p-1}\big)^{k(q-1)}\equiv a\cdot1=a\pmod p,$$
> and if $p\mid a$ both sides are $\equiv0$. So $a^{es}\equiv a\pmod p$ always, and symmetrically mod $q$. Since $p,q$ are distinct primes, $p$ and $q$ both divide $a^{es}-a$, hence so does $pq=z$ — giving $a^{es}\equiv a\pmod z$. $\blacksquare$
>
> **Note where each hypothesis was used:** $e$ coprime to $(p-1)(q-1)$ made $s$ exist; **$p\ne q$** let the two congruences be combined; and $0\le a<z$ makes the recovered residue equal $a$ rather than merely congruent to it.
>
> **(e)** The attacker needs $s$, which needs $(p-1)(q-1)$, which needs $p$ and $q$ — **they must factor $z$.**
>
> Here $z=713$ is trivial to factor ($\lfloor\sqrt{713}\rfloor=26$, and $23\mid713$ — at most 22 trial divisions). Real keys use $z$ of 2048 bits, so $\sqrt z\approx2^{1024}$: trial division needs about $10^{308}$ operations, exceeding the number of atoms in the observable universe by some 230 orders of magnitude. Even the best known method (the general number field sieve) is sub-exponential but still infeasible at that size.
>
> **What the attacker cannot shortcut:** everything the legitimate parties do is cheap — multiplying $p,q$, running the extended Euclidean algorithm, and modular exponentiation are all polynomial in the digit count (§§2–3). **Only the inverse problem, factoring, is hard.** That one-way asymmetry *is* RSA.
>
> **Two honest caveats.** No one has *proved* factoring is hard; and **Shor's algorithm factors in polynomial time on a quantum computer**, which is why post-quantum schemes are being standardised now.
>
> **(f)** $712=713-1\equiv-1\pmod{713}$, and $e=29$ is **odd**, so
> $$712^{29}\equiv(-1)^{29}=-1\equiv712\pmod{713}.$$
> The message encrypts to itself *(verified)*.
>
> **Implication: textbook RSA leaks information and must never be used directly.** It has fixed points ($0$, $1$, $z-1$ always, and generally more), and worse, it is **deterministic** — the same plaintext always gives the same ciphertext, so an attacker who can guess candidate messages can simply encrypt each with the *public* key and compare. Real implementations therefore apply **randomised padding** (OAEP) before exponentiating, which destroys both properties. **This is the general lesson: the mathematics of §4 is necessary but nowhere near sufficient for security**, and most real RSA failures are implementation failures rather than mathematical ones.

## 📝 Summary

- **$d\mid n$** means $n=dq$ for some integer $q$ — an existential statement, so assuming it gives you a $q$ and proving it requires producing one. And $d\mid n$ iff $n\bmod d=0$, by the Quotient–Remainder Theorem of [[02 - Proofs and Mathematical Induction|ch. 02]].
- **Primality needs only trial divisors up to $\sqrt n$**, because divisors pair up as $(d,n/d)$ across $\sqrt n$. The algorithm returns a **prime** divisor, so repeating it factors completely.
- **$\sqrt n$ trials is exponential in the input *size*.** A $k$-bit $n$ gives $\sqrt n<2^{k/2}$. **Measuring complexity in $n$ rather than $\log n$ is the classic error here**, and it is why trial division does not threaten RSA.
- **Fundamental Theorem of Arithmetic:** every integer $>1$ factors into primes, **uniquely** up to order. **Infinitely many primes** (Euclid): $m=p_1\cdots p_n+1$ has a prime factor outside the list — the proof does **not** claim $m$ is prime.
- $\gcd\cdot\operatorname{lcm}=mn$, from $\min+\max=a+b$ on each exponent. **Coprime** means $\gcd=1$.
- **Base $b$:** digits are remainders under repeated division by $b$, read least-significant-first. A positive $m$ has **$\lfloor1+\log_b m\rfloor$ digits** — the identity that converts input *value* into input *size*. Hex is popular because one hex digit is exactly four bits.
- **Repeated squaring** computes $a^n$ in $\Theta(\lg n)$ multiplications, using $n$'s binary expansion. And $ab\bmod z=\big((a\bmod z)(b\bmod z)\big)\bmod z$ **lets you reduce at every step** — the computational face of [[03 - Functions, Sequences and Relations|ch. 03]] §6's equivalence classes, and what keeps intermediate values small.
- **Euclidean algorithm:** $\gcd(a,b)=\gcd(b,a\bmod b)$, because both pairs have *the same set of common divisors*. Correctness is a **loop invariant**; termination is **well-ordering**.
- **Its worst case is consecutive Fibonacci numbers** — $(f_{n+2},f_{n+1})$ is the smallest pair needing $n$ steps, because quotients of $1$ give the slowest descent. Hence $n=O(\log a)$: **linear in the number of digits** (Lamé, 1844).
- **The extended Euclidean algorithm** gives Bézout's $\gcd(m,n)=sm+tn$, and hence **modular inverses**. **$a^{-1}\bmod m$ exists iff $\gcd(a,m)=1$.**
- **RSA:** publish $(z,e)$ with $z=pq$ and $\gcd(e,(p-1)(q-1))=1$; keep $s$ with $es\equiv1\pmod{(p-1)(q-1)}$. Encrypt $c=a^e\bmod z$, decrypt $a=c^s\bmod z$. **It works because $a^{es}\equiv a\pmod z$**, via Fermat's little theorem mod $p$ and mod $q$ separately.
- **Its security is an asymmetry this chapter has quantified:** multiplying, gcd, inverses and modular exponentiation are all cheap; **factoring $z$ is not.** "Believed secure" — factoring is not proved hard, and Shor's algorithm breaks it on a quantum computer.
- **Textbook RSA is unsafe as written:** it is deterministic and has fixed points ($712\equiv-1$ encrypts to itself since $e$ is odd). Real systems pad randomly first.

## ⚠️ Important Notes

1. **Measure complexity in the number of digits, not the value.** $\Theta(\sqrt n)$ looks polynomial and is exponential in $k=\lfloor1+\lg n\rfloor$. Every complexity claim in this chapter depends on getting this right.
2. **Trial division up to $\sqrt n$, not $n$** — and remember why: divisors come in pairs straddling $\sqrt n$. Testing to $n-1$ is not wrong, just wasteful by a square root.
3. **Euclid's proof does not say $p_1\cdots p_n+1$ is prime.** At $p=13$ it is $30031=59\cdot509$. It says $m$ has a prime factor larger than $p$ — a weaker claim, and the one that is true.
4. **Unique factorization is a theorem, not a definition.** It is what licenses "*the* prime factorization" and hence the $\gcd$/$\operatorname{lcm}$ exponent rules.
5. **Don't compute $\gcd$ by factoring.** The Euclidean algorithm is $O(\log)$; factoring is exponential. Finding a common factor does **not** require finding the factors — this is the counterintuitive fact of the chapter.
6. **In base conversion the remainders come out least-significant-first**, so the digits must be **reversed**. This is the commonest slip in §2's algorithm.
7. **Reduce mod $z$ inside the exponentiation loop, never at the end.** $a^n$ before reduction is astronomically large; Theorem 5.2.17 is what makes reducing early legal.
8. **Repeated squaring is $\Theta(\lg n)$ multiplications, not $\Theta(n)$.** Writing `a ** n % z` in a language without modular exponentiation can build a gigantic integer first — use `pow(a, n, z)` in Python.
9. **A modular inverse exists only when $\gcd(a,m)=1$.** $6$ has no inverse mod $9$. Check coprimality before solving, and note this is exactly why RSA demands $\gcd(e,(p-1)(q-1))=1$.
10. **Keep $\bmod z$ and $\bmod(p-1)(q-1)$ straight in RSA.** Exponents live mod $(p-1)(q-1)$; messages and ciphertexts live mod $z$. Mixing the two moduli is the standard beginner's error.
11. **$p$ and $q$ must be distinct**, and both must be destroyed after key generation. Distinctness is used in the correctness proof (combining the congruences mod $p$ and mod $q$); retaining them hands an attacker the private key.
12. **Messages must satisfy $0\le a<z$.** Otherwise decryption recovers $a\bmod z$, not $a$ — which is why real messages are split into blocks smaller than $z$.
13. **Textbook RSA is deterministic, and that alone breaks it.** With a public key, an attacker can encrypt guesses and compare ciphertexts. Never encrypt a raw message; pad it (OAEP).
14. **"Believed secure" is the correct phrase.** No proof exists that factoring is hard, and Shor's algorithm factors in polynomial time on a quantum computer. Treat any claim of provable RSA security with suspicion.
15. **Most RSA failures are implementation failures** — weak randomness when choosing $p,q$, reused or shared primes, missing padding, timing side channels. The mathematics of §4 is necessary and far from sufficient.
16. **Do not implement production cryptography from a textbook chapter, including this one.** The purpose here is to understand *why* it works. Use a reviewed library.

> [!warning] Gaps in the source material
> **Extraction was good for prose, definitions and theorem statements**, as throughout this book. New artefact in this chapter: **$d\nmid n$ extracts as `d |/n`**, which is legible once expected. `lg` remains $\log_2$ (see `00-Index.md`).
>
> **All numbered Algorithm boxes again extract as empty headings** — Algorithms 5.1.8 (primality), 5.2.3 (base $b$ to decimal), 5.2.7 (decimal to base $b$), 5.2.12 (binary addition), 5.2.16 and 5.2.19 (exponentiation by repeated squaring) and 5.3.3 (Euclidean) survive as titles with input/output lines only. **So all code in this note is my own Python reconstruction** from the surrounding prose and traces, and each was verified by running it — the primality test reproduces the book's results for $43$ (prime) and $451=11\cdot41$; the Euclidean trace of $\gcd(504,396)$ matches step for step ($108,72,36,0$, four modulus operations, answer $36$); and `power_mod` reproduces Example 5.2.18's $572^{29}\bmod713=113$.
>
> **The worked arithmetic inside §5.2's examples is largely lost** — Examples 5.2.2, 5.2.5, 5.2.6, 5.2.9, 5.2.10, 5.2.13, 5.2.15 and 5.2.18 arrive as statements of the problem with the computation dropped, and the binary/hexadecimal addition tables and Figure 5.2.4's repeated-squaring diagram are images. **Every conversion and computation in §2 was therefore recomputed:** $1011011_2=91$, $\mathrm{B4F}_{16}=2895$, $130=10000010_2$, $20385=4\mathrm{FA1}_{16}$, and the digit-count formula checked at seven values.
>
> **Table 5.3.1 (the modulus-operation counts) extracts as an unaligned digit soup** — its rows run together with the axis labels, so individual entries cannot be trusted. **Table 5.3.2 was recovered instead by independent exhaustive search**, confirming that the smallest pair requiring $n$ modulus operations is $(f_{n+2},f_{n+1})$ for $n=0,\dots,7$: $(1,0),(2,1),(3,2),(5,3),(8,5),(13,8),(21,13),(34,21)$. The book's Fibonacci observation is therefore verified rather than transcribed.
>
> **§5.4's RSA worked example is the most damaged part of the chapter.** The construction is described in prose, but the specific $p,q,e,s$ and the encryption/decryption computations are lost with the surrounding displays. **The example in §4 is my own reconstruction**, built on the book's own $z=713$ and $e=29$ (recoverable from Example 5.2.18, which is an RSA encryption in disguise): $713=23\cdot31$, $(p-1)(q-1)=660$, $s=569$ from the extended Euclidean algorithm, and the verified round trip $572\to113\to572$. **Flagged as reconstruction; the numbers are correct but may not be Johnsonbaugh's.**
>
> **All figures are images and are lost**, including Figures 5.2.2 and 5.2.3 (the binary and hexadecimal place-value diagrams — their content is in the prose) and Figure 5.2.4.
>
> **No error was found in Johnsonbaugh ch. 5.** The errata table in `00-Index.md` remains empty after five chapters — unusual for this vault, and worth noting as a fact about the book rather than about the checking.
>
> **Additions beyond the source.** The **exponential-vs-polynomial framing of §1's primality test in terms of input size** is Johnsonbaugh's own point, but the explicit $\Theta(2^{k/2})$ and its link to why RSA survives trial division is mine. The **Lamé's-theorem derivation** — that $n$ steps force $a\ge f_{n+2}\approx\phi^{n+2}$, hence $O(\log a)$, hence linear in digits — is mine; Johnsonbaugh observes the Fibonacci pattern in the table but does not draw the complexity conclusion in this form. The **extended Euclidean algorithm and Bézout's identity** are not in ch. 5 at all (they appear in the exercises), yet RSA key generation needs them, so §3 develops them properly and Exercise 4 is my own. **The correctness proof of RSA in Exercise 5(d)**, via Fermat's little theorem mod $p$ and mod $q$ then recombined, is written out here with attention to where each hypothesis is used. **Everything about the security discussion is an addition**: the four-way cheap/expensive table, the 2048-bit infeasibility estimate, **Shor's algorithm**, the observation that **textbook RSA is deterministic and has fixed points** ($712\equiv-1$ with odd $e$), and the **OAEP padding** requirement — Johnsonbaugh's 1980s-vintage treatment says only that RSA "is believed to be secure". The $\gcd\cdot\operatorname{lcm}=mn$ derivation from $\min+\max$ is also mine.
>
> **Not covered.** Johnsonbaugh's "Problem-Solving Corner: Making Postage" (book p. 249) is the strong-induction stamp problem already handled as [[02 - Proofs and Mathematical Induction|ch. 02]] Exercise 4. The **octal** exercises of §5.2 are omitted as a routine repetition of the hexadecimal method. Johnsonbaugh's classical substitution cipher (Example 5.4.1) is retained only as motivation for public-key cryptography, since frequency analysis is not further developed.

**Previous:** [[04 - Algorithms and Their Analysis]] · **Next:** [[06 - Counting Methods and the Pigeonhole Principle]]
