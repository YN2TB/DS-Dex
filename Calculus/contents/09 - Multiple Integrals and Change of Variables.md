---
subject: Calculus
chapter: 09
tags: [ds, calculus, multiple-integrals, fubini, polar-coordinates, jacobian, change-of-variables, gaussian-integral, curse-of-dimensionality]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., ch. 15 (pp. 1037–1120)"
---

# Multiple Integrals and Change of Variables

> [!abstract] What this chapter is for
> **This is the chapter that makes [[Probability Theory/contents/00-Index|probability]] possible.** A joint density is a function of two or more variables; a probability is its integral over a region; a marginal is an integral over one variable; an expectation is an integral against a density. **Every one of those is a multiple integral**, and none of them can be written down before this chapter.
>
> **Three ideas, and the third is the one worth the effort:**
>
> | § | Idea | Why it matters |
> |---|---|---|
> | **1–3** | **Fubini** — a double integral is two single integrals, *in either order* | Turns a new object into old machinery. The *choice* of order is where the skill is. |
> | **4–5** | **Polar, cylindrical, spherical** | Not new theory — three special cases of §7 that come up constantly |
> | **6** | Triple integrals | Same again with one more variable |
> | **7** | **The Jacobian** | $\boxed{dA=\left\lvert\dfrac{\partial(x,y)}{\partial(u,v)}\right\rvert du\,dv}$ — **the single most reused formula in the rest of the degree** |
> | **8** | **Probability** | Joint densities, independence, expectations — Stewart's own §15.4 |
> | **9** | **High dimensions** | Where geometric intuition stops being reliable |
>
> **If you learn one thing here, learn §7.** The change-of-variables formula for probability densities, the derivation of the $\chi^2$ and $t$ distributions, the normalising constant of the multivariate normal, and every reparameterisation trick in generative modelling are all *the same formula*.

---

## 📘 Main Knowledge

### 1. The double integral: the definition, and why it is unsurprising

Everything from [[04 - Integrals|ch. 04]] repeats with one more variable. Chop the rectangle $R=[a,b]\times[c,d]$ into $mn$ subrectangles of area $\Delta A=\Delta x\,\Delta y$, pick a sample point $(x_{ij}^*,y_{ij}^*)$ in each, and add:

$$\iint_R f(x,y)\,dA=\lim_{m,n\to\infty}\sum_{i=1}^m\sum_{j=1}^n f(x_{ij}^*,y_{ij}^*)\,\Delta A$$

**If $f\ge0$ this is the volume under the surface $z=f(x,y)$ and above $R$.** If $f$ changes sign it is a *difference* of volumes — exactly as the single integral is signed area.

> [!note] The integrability condition is more generous than it looks
> $f$ is integrable if it is **bounded on $R$ and continuous except on finitely many smooth curves.** That "except on finitely many smooth curves" clause is what makes the whole subject work: it lets you extend $f$ by **zero** outside an awkward region $D$ and integrate over a rectangle containing it. The discontinuity along $\partial D$ costs nothing.
>
> **This trick is used silently everywhere below**, and it is why $\iint_D$ makes sense at all.

The **average value** of $f$ over $R$ is
$$f_{\text{avg}}=\frac{1}{A(R)}\iint_R f(x,y)\,dA$$
— the height of the flat-topped box with the same base and the same volume.

---

### 2. Fubini's theorem: the only computational tool

> [!important] Fubini's Theorem
> If $f$ is continuous on $R=[a,b]\times[c,d]$ then
> $$\iint_R f(x,y)\,dA=\int_a^b\!\!\int_c^d f(x,y)\,dy\,dx=\int_c^d\!\!\int_a^b f(x,y)\,dx\,dy$$
> More generally this holds if $f$ is bounded, discontinuous only on finitely many smooth curves, and the iterated integrals exist.

**Read it as a licence, not a formula.** It says: *hold $x$ fixed, integrate out $y$, then integrate the result over $x$ — and you may do it in the other order instead.* The double integral is a genuinely two-dimensional limit; Fubini says it equals two one-dimensional limits, so all of [[05 - Techniques of Integration|ch. 05]] applies.

**The intuition** (for $f\ge0$): by the slicing method, $V=\int_a^b A(x)\,dx$ where $A(x)$ is the cross-sectional area at $x$. But that cross-section is the region under the curve $z=f(x,y)$ for fixed $x$, so $A(x)=\int_c^d f(x,y)\,dy$. Slicing the other way gives the other order.

> [!warning] Fubini needs a hypothesis, and it is not decorative
> **For unbounded $f$ or infinite regions the two orders can genuinely differ.** The standard counterexample is
> $$\int_0^1\!\!\int_0^1\frac{x^2-y^2}{(x^2+y^2)^2}\,dy\,dx=\frac{\pi}{4},\qquad \int_0^1\!\!\int_0^1\frac{x^2-y^2}{(x^2+y^2)^2}\,dx\,dy=-\frac{\pi}{4}$$
> The integrand blows up at the origin and $\iint|f|=\infty$. **Fubini for possibly-signed integrands requires absolute integrability** — the version of this you will meet again is **Tonelli/Fubini** in measure theory. Stewart does not mention it; for continuous $f$ on a bounded region the issue cannot arise.

**Separable integrands factor.** If $f(x,y)=g(x)h(y)$ **and $R$ is a rectangle**, then
$$\iint_R g(x)h(y)\,dA=\left(\int_a^b g(x)\,dx\right)\left(\int_c^d h(y)\,dy\right)$$

> [!warning] The rectangle hypothesis is doing all the work here
> This is exactly the statement that **independent random variables have product densities and factoring expectations** ([[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]]). It fails the instant the region is not a product set — on the triangle $x+y\le1$ the limits of the inner integral depend on the outer variable and nothing factors. **Non-rectangular support is precisely how dependence sneaks into a "product" density.**

---

### 3. General regions, and the order of integration as a *choice*

Two shapes cover almost everything.

| Type | Description | Iterated integral |
|---|---|---|
| **Type I** (vertically simple) | $D=\{(x,y): a\le x\le b,\ g_1(x)\le y\le g_2(x)\}$ | $\displaystyle\int_a^b\!\!\int_{g_1(x)}^{g_2(x)}f\,dy\,dx$ |
| **Type II** (horizontally simple) | $D=\{(x,y): c\le y\le d,\ h_1(y)\le x\le h_2(y)\}$ | $\displaystyle\int_c^d\!\!\int_{h_1(y)}^{h_2(y)}f\,dx\,dy$ |

> [!important] The rule that prevents most errors
> **The outer limits are always constants. The inner limits may depend on the outer variable, never the reverse.**
>
> An answer containing $y$ after you have integrated $y$ out is wrong, and this check catches the error immediately.

**Properties** (all inherited from the single integral): linearity; additivity over regions $D=D_1\cup D_2$ meeting only on a boundary; monotonicity; and
$$m\cdot A(D)\le\iint_D f\,dA\le M\cdot A(D)\quad\text{when } m\le f\le M$$
Also $\iint_D 1\,dA=A(D)$, which is how areas get computed as double integrals.

#### Reversing the order

**Sometimes the swap is a convenience; sometimes it is the only route.** The canonical case:

$$\int_0^1\!\!\int_x^1 e^{-y^2}\,dy\,dx$$

The inner integral **has no elementary antiderivative** — $\int e^{-y^2}dy$ is the error function. But the region is the triangle $0\le x\le y\le 1$, which is *also* Type I in the other order: for each $y\in[0,1]$, $x$ runs from $0$ to $y$. So

$$\int_0^1\!\!\int_0^y e^{-y^2}\,dx\,dy=\int_0^1 y\,e^{-y^2}\,dy=\left[-\tfrac12e^{-y^2}\right]_0^1=\frac{1-e^{-1}}{2}\approx0.3161$$

**The swap manufactured the factor $y$ that makes the substitution work.** This is not a trick you should hope to spot — it is the standard move whenever the inner integrand is one of $e^{-y^2}$, $\sin(y^2)$, $\frac{\sin y}{y}$, $e^{y^2}$, $\sqrt{1+y^3}$.

> [!tip] The procedure, every time
> 1. **Draw the region from the given limits** — do not attempt the algebra first.
> 2. **Re-describe the same region in the other order**, reading the new outer limits off the axis.
> 3. Integrate.
>
> **Step 1 is not optional.** "Reversing the order" is not "swap $dx\,dy$ and swap the limit pairs"; that is wrong except on a rectangle, and it is the single most common error in this chapter.

---

### 4. Polar coordinates: the first change of variables

With $x=r\cos\theta$, $y=r\sin\theta$ (so $x^2+y^2=r^2$):

$$\boxed{\iint_R f(x,y)\,dA=\int_\alpha^\beta\!\!\int_a^b f(r\cos\theta,\,r\sin\theta)\ \color{red}{r}\ dr\,d\theta}$$

and more generally, for $D=\{\alpha\le\theta\le\beta,\ h_1(\theta)\le r\le h_2(\theta)\}$, the inner limits become $h_1(\theta)$ and $h_2(\theta)$.

> [!warning] The extra $r$ is the whole content of the formula
> **Forgetting it is the most-punished single mistake in the chapter.** It is not a convention — it is a *fact about area*. An infinitesimal polar rectangle has sides $dr$ and $r\,d\theta$ (arc length = radius $\times$ angle), so
> $$dA=r\,dr\,d\theta$$
> **The factor grows with $r$ because a polar cell far from the origin is physically bigger** at the same $\Delta r,\Delta\theta$. §7 shows this $r$ is a Jacobian determinant.

**Use polar when** the region is a disk, annulus, sector or is bounded by circles, **or** when the integrand contains $x^2+y^2$. Both together is a guarantee.

Taking $f=1$ recovers the polar area formula $A=\int_\alpha^\beta\frac12[h(\theta)]^2\,d\theta$.

#### The integral that justifies the entire chapter

$$I=\int_{-\infty}^{\infty}e^{-x^2}\,dx$$

**has no elementary antiderivative, and one dimension cannot evaluate it.** Two dimensions can. Square it, and — because $e^{-x^2}e^{-y^2}=e^{-(x^2+y^2)}$ and the domain is all of $\mathbb R^2$, a product set — Fubini runs backwards:

$$I^2=\left(\int_{-\infty}^{\infty}\!\!e^{-x^2}dx\right)\!\left(\int_{-\infty}^{\infty}\!\!e^{-y^2}dy\right)=\iint_{\mathbb R^2}e^{-(x^2+y^2)}\,dA$$

Now go polar, where the integrand is a function of $r$ alone and the $r\,dr$ supplies exactly the missing factor:

$$I^2=\int_0^{2\pi}\!\!\int_0^{\infty}e^{-r^2}\,r\,dr\,d\theta=2\pi\cdot\left[-\tfrac12e^{-r^2}\right]_0^{\infty}=2\pi\cdot\tfrac12=\pi$$

$$\boxed{\int_{-\infty}^{\infty}e^{-x^2}dx=\sqrt{\pi}}\qquad\text{and, with }t=x\sqrt2,\qquad \int_{-\infty}^{\infty}e^{-x^2/2}dx=\sqrt{2\pi}$$

> [!important] This is where the $\frac{1}{\sqrt{2\pi}}$ in the normal density comes from
> $$\varphi(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}$$
> **The constant is not chosen for elegance — it is forced, and this polar-coordinate argument is the only elementary way to find it.** Equivalently $\Gamma(\tfrac12)=\sqrt\pi$, which is why the $\chi^2$ and $t$ densities carry $\sqrt\pi$'s ([[Mathematical Statistics/contents/00-Index|Math Stats]]).
>
> **Stewart puts this in Exercise 15.3.50, not in the text.** For a data-science reader it is the most important single result in the chapter and belongs in the body.

---

### 5. Triple integrals

Same construction, one more variable. Over a box $B=[a,b]\times[c,d]\times[r,s]$, Fubini gives **six** iterated orders, all equal. Over a general solid $E$:

**Type 1** (the common case) — $E$ sits over a plane region $D$, between two surfaces:
$$E=\{(x,y,z):(x,y)\in D,\ u_1(x,y)\le z\le u_2(x,y)\}$$
$$\iiint_E f\,dV=\iint_D\left[\int_{u_1(x,y)}^{u_2(x,y)}f(x,y,z)\,dz\right]dA$$

**Do the $z$-integral first, then fall back to a double integral over the shadow $D$.** Types 2 and 3 are the same with the roles of the axes permuted; choose whichever projection is simplest.

$\iiint_E 1\,dV=V(E)$. **Applications**: mass $\iiint\rho\,dV$, centre of mass, moments of inertia, and — the one that matters here — **probabilities from a joint density of three variables**.

#### Cylindrical and spherical coordinates

| System | Substitution | Volume element | Use when |
|---|---|---|---|
| **Cylindrical** $(r,\theta,z)$ | $x=r\cos\theta,\ y=r\sin\theta,\ z=z$ | $dV=r\,dz\,dr\,d\theta$ | axial symmetry; $x^2+y^2$ appears |
| **Spherical** $(\rho,\theta,\varphi)$ | $x=\rho\sin\varphi\cos\theta$, $y=\rho\sin\varphi\sin\theta$, $z=\rho\cos\varphi$ | $\boxed{dV=\rho^2\sin\varphi\,d\rho\,d\theta\,d\varphi}$ | spheres, cones, balls; $x^2+y^2+z^2$ appears |

with $\rho\ge0$, $0\le\varphi\le\pi$ (measured **down from the positive $z$-axis**), $\rho^2=x^2+y^2+z^2$.

> [!warning] Notation is not standardised, and this bites
> **Most physics texts swap $\theta$ and $\varphi$ and write $r$ for $\rho$.** Stewart flags this himself. Always check which angle is polar and which is azimuthal before using a formula from another source.

**Worked check — the volume of the unit ball:**
$$V=\int_0^{2\pi}\!\!\int_0^{\pi}\!\!\int_0^1\rho^2\sin\varphi\,d\rho\,d\varphi\,d\theta=2\pi\cdot\big[-\cos\varphi\big]_0^{\pi}\cdot\tfrac13=2\pi\cdot2\cdot\tfrac13=\frac{4\pi}{3}\ \checkmark$$

The $\rho^2\sin\varphi$ is again a statement about volume: the spherical wedge has edges $\Delta\rho$, $\rho\,\Delta\varphi$, and $\rho\sin\varphi\,\Delta\theta$ — the last shrinks near the poles, where $\sin\varphi\to0$, because circles of latitude get small there.

---

### 6. Surface area (in one paragraph)

For a surface $z=f(x,y)$ over $D$ with $f_x,f_y$ continuous:
$$A(S)=\iint_D\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,dA$$

**The parallel with arc length $L=\int\sqrt{1+(dy/dx)^2}\,dx$ is exact**, and the derivation is the same: approximate the surface by the tangent planes from [[07 - Partial Derivatives and the Gradient|ch. 07]] and add the areas of the resulting parallelograms, $|\mathbf a\times\mathbf b|$.

*This section is included for completeness; nothing downstream in this vault uses it.*

---

### 7. **The Jacobian and change of variables** — the section that matters

In one variable, substitution reads
$$\int_a^b f(x)\,dx=\int_c^d f(x(u))\,\frac{dx}{du}\,du$$
**The derivative $dx/du$ is a local stretch factor**: it says how much a small interval $du$ is stretched into $dx$. In several variables the same idea holds, with a determinant in place of a derivative.

Let $T(u,v)=(x,y)$ with $x=g(u,v)$, $y=h(u,v)$ be a $C^1$ transformation from the $uv$-plane to the $xy$-plane.

> [!important] Definition — the Jacobian
> $$\frac{\partial(x,y)}{\partial(u,v)}=\begin{vmatrix}\dfrac{\partial x}{\partial u}&\dfrac{\partial x}{\partial v}\\[8pt] \dfrac{\partial y}{\partial u}&\dfrac{\partial y}{\partial v}\end{vmatrix}=\frac{\partial x}{\partial u}\frac{\partial y}{\partial v}-\frac{\partial x}{\partial v}\frac{\partial y}{\partial u}$$
>
> **This is the determinant of the derivative matrix of $T$** — the matrix whose rows are the gradients of the component functions, i.e. the *Jacobian matrix* of [[07 - Partial Derivatives and the Gradient|ch. 07 §5]].

> [!important] Change of Variables in a Double Integral
> Suppose $T$ is $C^1$ with **non-zero Jacobian**, maps $S$ onto $R$, and is **one-to-one except possibly on the boundary of $S$**. Then
> $$\iint_R f(x,y)\,dA=\iint_S f\big(x(u,v),\,y(u,v)\big)\ \left\lvert\frac{\partial(x,y)}{\partial(u,v)}\right\rvert\,du\,dv$$
> In three variables the same statement holds with the $3\times3$ determinant $\dfrac{\partial(x,y,z)}{\partial(u,v,w)}$.

#### Why a determinant

**Because a determinant *is* a volume scale factor** — the fact proved in [[Linear Algebra/contents/03 - Determinants and Diagonalization|Linear Algebra ch. 03]].

$T$ is not linear, but near a point it is: its best linear approximation is multiplication by the Jacobian matrix. A small rectangle of sides $\Delta u,\Delta v$ maps to a region approximated by the **parallelogram spanned by $\Delta u\,\mathbf r_u$ and $\Delta v\,\mathbf r_v$**, where $\mathbf r_u=\frac{\partial x}{\partial u}\mathbf i+\frac{\partial y}{\partial u}\mathbf j$. Its area is the cross product
$$|\Delta u\,\mathbf r_u\times\Delta v\,\mathbf r_v|=\left\lvert\frac{\partial(x,y)}{\partial(u,v)}\right\rvert\Delta u\,\Delta v$$
Sum over cells and pass to the limit. **So the chain is: derivative $\to$ linear approximation $\to$ determinant $\to$ area factor.** All three links come from earlier chapters.

> [!warning] Four things go wrong here, reliably
> 1. **The absolute value.** The formula uses $\left\lvert\,\cdot\,\right\rvert$. A negative Jacobian just means $T$ reverses orientation; areas stay positive. (Single-variable substitution hides this by letting the *limits* swap instead.)
> 2. **The direction.** The formula wants $\dfrac{\partial(x,y)}{\partial(u,v)}$ — **old variables differentiated with respect to new.** If you were handed $u=u(x,y)$, either invert the relations or use $\dfrac{\partial(x,y)}{\partial(u,v)}=\left[\dfrac{\partial(u,v)}{\partial(x,y)}\right]^{-1}$, which follows from $\det(A^{-1})=1/\det A$.
> 3. **The region must be transformed too.** Changing variables without redrawing $S$ is the error that produces confidently wrong answers.
> 4. **One-to-one matters.** Polar coordinates fail injectivity at $r=0$ (every $\theta$ maps there) — harmless, because that is a boundary set of area zero, which is exactly what the hypothesis permits.

#### The three standard cases, all derived, not assumed

| Transformation | Jacobian |
|---|---|
| **Polar** $x=r\cos\theta,\ y=r\sin\theta$ | $\begin{vmatrix}\cos\theta&-r\sin\theta\\ \sin\theta&r\cos\theta\end{vmatrix}=r\cos^2\theta+r\sin^2\theta=r$ |
| **Cylindrical** | $r$ (the polar computation, bordered by a $1$ in the $z$ row) |
| **Spherical** $(\rho,\theta,\varphi)$ | $-\rho^2\sin\varphi$, so $\left\lvert\,\cdot\,\right\rvert=\rho^2\sin\varphi$ since $\sin\varphi\ge0$ on $[0,\pi]$ |

> [!note] Why the spherical Jacobian comes out negative
> **The sign is an artefact of the variable order, not a fact about spheres.** In Stewart's order $(\rho,\theta,\varphi)$ the determinant is $-\rho^2\sin\varphi$; in the order $(\rho,\varphi,\theta)$ it is $+\rho^2\sin\varphi$. **Swapping two columns flips a determinant's sign** ([[Linear Algebra/contents/03 - Determinants and Diagonalization|Linear Algebra ch. 03]]). The absolute value in the formula is exactly what makes the answer independent of a choice that carries no meaning.

#### Choosing a substitution

**Two things can motivate one, and they pull in different directions:**

- **A hard integrand.** If $f$ contains a repeated combination, name it. For $\iint_R e^{(x+y)/(x-y)}dA$, set $u=x+y$, $v=x-y$; then $x=\frac12(u+v)$, $y=\frac12(u-v)$, $\frac{\partial(x,y)}{\partial(u,v)}=-\frac12$, and the integrand collapses to $e^{u/v}$.
- **A hard region.** If $R$ is a parallelogram, ellipse or curvilinear quadrilateral, choose $T$ so that $S$ is a rectangle.

**When both apply, they usually agree** — the combinations appearing in $f$ tend to be the ones describing $\partial R$.

> [!tip] Linear substitutions have constant Jacobians
> If $\mathbf x=A\mathbf u$ for a fixed invertible matrix $A$, the Jacobian is **$\det A$ everywhere**, so it comes straight out of the integral:
> $$\iint_{A(S)}f(\mathbf x)\,d\mathbf x=|\det A|\iint_S f(A\mathbf u)\,d\mathbf u$$
> **This one line is the whole derivation of the multivariate normal's normalising constant** — see §8.

---

### 8. Probability: what this machinery was built for

Stewart devotes §15.4 to it, and it is the section a data-science reader should read twice.

> [!important] Joint density
> $f(x,y)$ is a **joint density function** for $(X,Y)$ if
> $$f(x,y)\ge0\qquad\text{and}\qquad \iint_{\mathbb R^2}f(x,y)\,dA=1$$
> and then $$P\big((X,Y)\in D\big)=\iint_D f(x,y)\,dA$$
>
> **Probability is volume under the density surface.** The integral over $\mathbb R^2$ is improper — defined as the limit over expanding disks or squares.

**The dictionary between §15.4 and §15.4's own mass calculations is exact**, and Stewart says so: probability behaves like continuously distributed mass of total weight 1.

| Mass language | Probability language |
|---|---|
| density $\rho(x,y)$ | joint density $f(x,y)$ |
| total mass $m=\iint_D\rho\,dA$ | total probability $=1$ |
| moment $M_y=\iint x\rho\,dA$ | $\mu_1=\displaystyle\iint_{\mathbb R^2}x f(x,y)\,dA=E[X]$ |
| centre of mass $(\bar x,\bar y)$ | **$(\mu_1,\mu_2)$, the mean vector** |
| moment of inertia $I_0=\iint(x^2+y^2)\rho\,dA$ | second moments — the ingredients of the **covariance matrix** |

**Independence.** $X$ and $Y$ are independent iff the joint density factors:
$$f(x,y)=f_1(x)f_2(y)$$
Combined with §2's product rule, **independent variables on a rectangular region give a product of two single integrals** — this is why independence makes everything computable. Compare [[Probability Theory/contents/06 - Jointly Distributed Random Variables|Probability ch. 06]], which develops the same idea properly.

> [!example]- Stewart's Example 7 — worth following, because the region is the point
> Ticket queue $X\sim\text{Exp}$ with mean 10, popcorn queue $Y\sim\text{Exp}$ with mean 5, independent. So $f(x,y)=\tfrac1{50}e^{-x/10}e^{-y/5}$ on the first quadrant. Then
> $$P(X+Y<20)=\int_0^{20}\!\!\int_0^{20-x}\tfrac1{50}e^{-x/10}e^{-y/5}\,dy\,dx=1+e^{-4}-2e^{-2}\approx0.7476$$
> **Note what happened: the density factored, but the *region* $\{x+y<20\}$ did not**, so the product rule of §2 is unavailable and the inner limit depends on $x$. **This is the general shape of a convolution** — see below.

#### The change-of-variables formula for densities

**This is §7 applied to §8, and it is the reason the chapter exists.**

If $\mathbf Y=T(\mathbf X)$ for a one-to-one $C^1$ map, then
$$\boxed{f_{\mathbf Y}(\mathbf y)=f_{\mathbf X}\big(T^{-1}(\mathbf y)\big)\left\lvert\det \frac{\partial \mathbf x}{\partial \mathbf y}\right\rvert}$$

Two consequences used constantly:

**(a) Sums of independent variables are convolutions.** Put $u=x+y$, $v=y$; then $x=u-v$, $y=v$ and the Jacobian is $1$, so
$$f_{X+Y}(u)=\int_{-\infty}^{\infty}f(u-v,v)\,dv \;\xrightarrow{\ \text{independent}\ }\; \int_{-\infty}^{\infty}f_1(u-v)f_2(v)\,dv$$
**The convolution formula of [[Probability Theory/contents/06 - Jointly Distributed Random Variables|Probability ch. 06]] is a Jacobian computation whose answer happens to be 1.**

**(b) The multivariate normal's normalising constant.** Let $\Sigma$ be symmetric positive definite and write $\Sigma=AA^{\mathsf T}$. Substituting $\mathbf x=A\mathbf u$ (Jacobian $\det A$, with $(\det A)^2=\det\Sigma$) turns the quadratic form into $|\mathbf u|^2$, and the integral separates into $n$ copies of the Gaussian integral of §4:

$$\int_{\mathbb R^n}e^{-\frac12\mathbf x^{\mathsf T}\Sigma^{-1}\mathbf x}\,d\mathbf x=|\det A|\int_{\mathbb R^n}e^{-\frac12|\mathbf u|^2}d\mathbf u=\sqrt{\det\Sigma}\ \big(\sqrt{2\pi}\big)^n$$

$$\boxed{f(\mathbf x)=\frac{1}{(2\pi)^{n/2}\sqrt{\det\Sigma}}\exp\!\left(-\tfrac12(\mathbf x-\boldsymbol\mu)^{\mathsf T}\Sigma^{-1}(\mathbf x-\boldsymbol\mu)\right)}$$

**Every symbol in that constant has now been derived**: the $2\pi$ from the polar-coordinate Gaussian integral, the $\sqrt{\det\Sigma}$ from the Jacobian, and the existence of $A$ from the Cholesky/spectral factorisation of [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]].

> [!tip] This is also the reparameterisation trick
> $\mathbf x=\boldsymbol\mu+A\mathbf u$ with $\mathbf u\sim N(\mathbf 0,I)$ is how a variational autoencoder samples from a learned Gaussian while keeping gradients flowing to $\boldsymbol\mu$ and $A$. **The randomness is pushed into a fixed distribution and the parameters enter through a smooth, differentiable transformation** — whose Jacobian is what makes the density come out right. Normalising flows are the same idea iterated, and the log-determinant of the Jacobian is the quantity their architectures are designed to keep cheap.

---

### 9. High dimensions: where the pictures stop working

Stewart's Discovery Project on hyperspheres computes, by iterated integration, the volume of the unit ball in $\mathbb R^n$:

$$V_n(1)=\frac{\pi^{n/2}}{\Gamma\!\left(\frac n2+1\right)}$$

| $n$ | $V_n(1)$ | $V_n(1)/2^n$ = ball $\div$ enclosing cube |
|---|---|---|
| 1 | 2 | 1 |
| 2 | $\pi\approx3.1416$ | 0.785 |
| 3 | $\tfrac{4\pi}{3}\approx4.1888$ | 0.524 |
| **5** | **$\approx5.2638$ (the maximum)** | 0.165 |
| 10 | 2.5502 | $2.5\times10^{-3}$ |
| 20 | 0.0258 | $2.5\times10^{-8}$ |
| 50 | $1.7\times10^{-13}$ | $1.5\times10^{-28}$ |
| 100 | $2.4\times10^{-40}$ | $1.9\times10^{-70}$ |

> [!warning] Three facts that break intuition, all of them consequences of this table
> 1. **The volume of the unit ball peaks at $n=5$ and then goes to zero.** In $\mathbb R^{100}$ the unit ball is, for all practical purposes, empty.
> 2. **Almost all of a high-dimensional cube is in its corners.** The inscribed ball occupies $10^{-70}$ of $[-1,1]^{100}$. **A "typical" point of a high-dimensional cube is far from the centre and near a face.**
> 3. **Almost all of a ball's volume is in a thin shell at its surface.** The fraction inside radius $0.99$ is $0.99^{n}$: 97% at $n=3$, 37% at $n=100$, 0.7% at $n=500$.
>
> **These are the geometric content of the curse of dimensionality.** They are why nearest-neighbour distances become uninformative in high dimensions, why sampling a high-dimensional space by grid is hopeless, and why volume-based density estimation (histograms, kernel methods with fixed bandwidth) degrades so fast with $n$. See [[Machine Learning/contents/00-Index|Machine Learning]].
>
> **All three are computed with the machinery of this chapter and nothing else.**

---

## ✏️ Exercises

> [!question] Exercise 1 — Fubini both ways *(easy)*
> Evaluate $\displaystyle\iint_R (xy^2+2x)\,dA$ over $R=[1,3]\times[0,2]$ in **both** orders, and confirm they agree.

> [!example]- Solution
> **Order $dy\,dx$:**
> $$\int_0^2(xy^2+2x)\,dy=\left[\frac{xy^3}{3}+2xy\right]_0^2=\frac{8x}{3}+4x=\frac{20x}{3}$$
> $$\int_1^3\frac{20x}{3}\,dx=\frac{20}{3}\cdot\frac{x^2}{2}\bigg|_1^3=\frac{10}{3}(9-1)=\frac{80}{3}$$
>
> **Order $dx\,dy$:**
> $$\int_1^3(xy^2+2x)\,dx=(y^2+2)\cdot\frac{x^2}{2}\bigg|_1^3=(y^2+2)\cdot4=4y^2+8$$
> $$\int_0^2(4y^2+8)\,dy=\frac{4\cdot8}{3}+16=\frac{32}{3}+16=\frac{80}{3}\quad\checkmark$$
>
> $$\boxed{\dfrac{80}{3}}$$
>
> **Shortcut worth noticing:** $xy^2+2x=x(y^2+2)$ is separable **and $R$ is a rectangle**, so §2's product rule applies directly: $\left(\int_1^3 x\,dx\right)\left(\int_0^2(y^2+2)\,dy\right)=4\cdot\frac{20}{3}=\frac{80}{3}$.

---

> [!question] Exercise 2 — a general region, described twice *(easy–medium)*
> Let $D$ be the region bounded by $y=x^2$ and $y=2x$. Evaluate $\displaystyle\iint_D 6x\,dA$ as a Type I integral, then set it up and evaluate it as a Type II integral.

> [!example]- Solution
> **Intersection:** $x^2=2x\Rightarrow x=0,2$, giving the points $(0,0)$ and $(2,4)$. On $(0,2)$ we have $2x>x^2$, so the parabola is the *lower* boundary.
>
> **Type I:** $0\le x\le2$, $x^2\le y\le 2x$.
> $$\int_0^2\!\!\int_{x^2}^{2x}6x\,dy\,dx=\int_0^2 6x(2x-x^2)\,dx=\int_0^2(12x^2-6x^3)\,dx=\left[4x^3-\tfrac32x^4\right]_0^2=32-24=8$$
>
> **Type II:** solve each boundary for $x$. From $y=2x$, $x=y/2$; from $y=x^2$ (right branch), $x=\sqrt y$. For $0\le y\le4$, $x$ runs from $y/2$ to $\sqrt y$.
> $$\int_0^4\!\!\int_{y/2}^{\sqrt y}6x\,dx\,dy=\int_0^4 3x^2\Big|_{y/2}^{\sqrt y}dy=\int_0^4\left(3y-\tfrac34y^2\right)dy=\left[\tfrac32y^2-\tfrac14y^3\right]_0^4=24-16=8\ \checkmark$$
>
> $$\boxed{8}$$
>
> **The point of doing both:** the limits are *not* related by any mechanical swap. $x^2\le y\le2x$ became $y/2\le x\le\sqrt y$, and the outer range changed from $[0,2]$ to $[0,4]$. **This is why §3 insists on redrawing the region.**

---

> [!question] Exercise 3 — the swap is the only route *(medium)*
> Evaluate $\displaystyle\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$.

> [!example]- Solution
> **The inner integral cannot be done** — $e^{y^2}$ has no elementary antiderivative. So the order must change.
>
> **Read the region off the limits:** $0\le x\le1$ and $x\le y\le1$, i.e.
> $$D=\{(x,y):0\le x\le y\le 1\}$$
> the triangle with vertices $(0,0)$, $(0,1)$, $(1,1)$ — the half of the unit square **above** the diagonal.
>
> **Re-describe by horizontal strips:** for each $y\in[0,1]$, $x$ runs from $0$ to $y$.
> $$\int_0^1\!\!\int_0^y e^{y^2}\,dx\,dy=\int_0^1 e^{y^2}\cdot y\,dy$$
>
> Now substitute $t=y^2$, $dt=2y\,dy$:
> $$=\frac12\int_0^1 e^{t}\,dt=\frac{e-1}{2}$$
>
> $$\boxed{\dfrac{e-1}{2}\approx0.8591}$$
>
> **What made it work:** integrating $x$ out over $[0,y]$ produced a factor of $y$ — exactly the derivative needed for the substitution. **That is the mechanism in every problem of this type**, not a coincidence of this integrand.

---

> [!question] Exercise 4 — the Gaussian integral, and what it buys *(medium–hard)*
> **(a)** Evaluate $\displaystyle\iint_{\mathbb R^2}e^{-(x^2+y^2)/2}\,dA$ using polar coordinates.
> **(b)** Deduce the value of $\displaystyle\int_{-\infty}^{\infty}e^{-x^2/2}\,dx$ and hence the normalising constant of the standard normal density.
> **(c)** Use the same result to show $\Gamma\!\left(\tfrac12\right)=\sqrt\pi$, where $\Gamma(s)=\int_0^\infty t^{s-1}e^{-t}dt$.

> [!example]- Solution
> **(a)** The integrand is a function of $r^2=x^2+y^2$, and $\mathbb R^2$ in polar coordinates is $0\le r<\infty$, $0\le\theta\le2\pi$. **Do not forget the $r$:**
> $$\iint_{\mathbb R^2}e^{-(x^2+y^2)/2}dA=\int_0^{2\pi}\!\!\int_0^{\infty}e^{-r^2/2}\,r\,dr\,d\theta$$
> The inner integral is elementary — substitute $s=r^2/2$, $ds=r\,dr$:
> $$\int_0^{\infty}e^{-r^2/2}r\,dr=\int_0^{\infty}e^{-s}\,ds=1$$
> Therefore the double integral is $\int_0^{2\pi}1\,d\theta=\boxed{2\pi}$.
>
> **(b)** The integrand factors *and* the domain $\mathbb R^2$ is a product set, so §2 gives
> $$2\pi=\left(\int_{-\infty}^{\infty}e^{-x^2/2}dx\right)\!\left(\int_{-\infty}^{\infty}e^{-y^2/2}dy\right)=\left(\int_{-\infty}^{\infty}e^{-x^2/2}dx\right)^{\!2}$$
> Both factors are positive, so
> $$\int_{-\infty}^{\infty}e^{-x^2/2}dx=\sqrt{2\pi}\quad\Longrightarrow\quad \boxed{\varphi(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}}$$
> integrates to 1. **The constant is forced, not chosen.**
>
> **(c)** In $\Gamma(\tfrac12)=\int_0^\infty t^{-1/2}e^{-t}\,dt$ substitute $t=x^2/2$, so $dt=x\,dx$ and $t^{-1/2}=\sqrt2/x$ for $x>0$:
> $$\Gamma\!\left(\tfrac12\right)=\int_0^{\infty}\frac{\sqrt2}{x}e^{-x^2/2}\,x\,dx=\sqrt2\int_0^{\infty}e^{-x^2/2}dx=\sqrt2\cdot\frac{\sqrt{2\pi}}{2}=\sqrt\pi$$
>
> $$\boxed{\Gamma\!\left(\tfrac12\right)=\sqrt\pi}$$
>
> **This single number is why $\sqrt\pi$ appears in the $\chi^2$, $t$ and $F$ densities.** It has no elementary one-dimensional derivation — the detour through two dimensions is essential.

---

> [!question] Exercise 5 — a linear change of variables and the bivariate normal *(hard)*
> Let $\displaystyle\Sigma=\begin{pmatrix}4&2\\2&3\end{pmatrix}$ and $Q(x,y)=(x\ \ y)\,\Sigma^{-1}\begin{pmatrix}x\\y\end{pmatrix}$.
> **(a)** Compute $\det\Sigma$, $\Sigma^{-1}$ and $Q$ explicitly.
> **(b)** Evaluate $\displaystyle\iint_{\mathbb R^2}e^{-Q(x,y)/2}\,dA$ by a linear change of variables, without computing the integral directly.
> **(c)** Write down the normalised density and check it against the general formula $\left[(2\pi)^{n/2}\sqrt{\det\Sigma}\right]^{-1}$.
> **(d)** Explain, in one sentence each, where the $2\pi$ and the $\sqrt{\det\Sigma}$ come from.

> [!example]- Solution
> **(a)** $\det\Sigma=4\cdot3-2\cdot2=8$, so
> $$\Sigma^{-1}=\frac{1}{8}\begin{pmatrix}3&-2\\-2&4\end{pmatrix}=\begin{pmatrix}\tfrac38&-\tfrac14\\[2pt]-\tfrac14&\tfrac12\end{pmatrix}$$
> $$Q(x,y)=\tfrac38x^2-\tfrac12xy+\tfrac12y^2$$
> ($\Sigma$ is symmetric with leading minors $4>0$ and $8>0$, so it is positive definite and $Q>0$ off the origin — the integral converges.)
>
> **(b)** Since $\Sigma$ is symmetric positive definite it factors as $\Sigma=AA^{\mathsf T}$ (Cholesky, or $A=\Sigma^{1/2}$ from the spectral theorem). Substitute $\mathbf x=A\mathbf u$. Then
> $$\mathbf x^{\mathsf T}\Sigma^{-1}\mathbf x=\mathbf u^{\mathsf T}A^{\mathsf T}(AA^{\mathsf T})^{-1}A\mathbf u=\mathbf u^{\mathsf T}\mathbf u=|\mathbf u|^2$$
> **The change of variables diagonalises the exponent.** The Jacobian of a linear map is constant:
> $$\left\lvert\frac{\partial(x,y)}{\partial(u_1,u_2)}\right\rvert=|\det A|=\sqrt{\det\Sigma}=\sqrt8=2\sqrt2$$
> Therefore, using Exercise 4(a) for the transformed integral,
> $$\iint_{\mathbb R^2}e^{-Q/2}\,dA=\sqrt{\det\Sigma}\iint_{\mathbb R^2}e^{-|\mathbf u|^2/2}\,d\mathbf u=2\sqrt2\cdot2\pi=\boxed{4\sqrt2\,\pi\approx17.7715}$$
>
> **(c)** Dividing by that total,
> $$f(x,y)=\frac{1}{4\sqrt2\,\pi}\exp\!\left(-\tfrac12\left(\tfrac38x^2-\tfrac12xy+\tfrac12y^2\right)\right)$$
> and the general formula gives $(2\pi)^{2/2}\sqrt{\det\Sigma}=2\pi\cdot2\sqrt2=4\sqrt2\,\pi\ \checkmark$.
>
> **(d)**
> - **The $2\pi$** is the Gaussian integral of §4 — one factor of $\sqrt{2\pi}$ per dimension — and it exists only because the polar-coordinate $r\,dr$ makes $\int e^{-r^2/2}r\,dr$ elementary.
> - **The $\sqrt{\det\Sigma}$** is the Jacobian: $A$ stretches volume by $|\det A|$, and $(\det A)^2=\det(AA^{\mathsf T})=\det\Sigma$. **A covariance matrix with larger determinant spreads the same probability over more volume, so the density's peak must be lower by exactly that factor.**
>
> > [!note]- Why the answer does not depend on which $A$ you pick
> > $\Sigma=AA^{\mathsf T}$ has many solutions — Cholesky, $\Sigma^{1/2}$, or $AQ$ for any orthogonal $Q$. **But $|\det A|=\sqrt{\det\Sigma}$ for every one of them**, since $\det(AQ)=\det A\det Q=\pm\det A$. The change-of-variables formula's absolute value makes the ambiguity vanish — the same reason the sign of the spherical Jacobian did not matter in §7.

---

## 📝 Summary

- **A double integral is a limit of Riemann sums over subrectangles**, and for $f\ge0$ it is the volume under $z=f(x,y)$. Signed, like the single integral. The average value is $\frac{1}{A(R)}\iint_R f\,dA$.
- **Fubini's theorem** turns it into two single integrals **in either order** — this is the only computational tool in the chapter. **The two orders are usually not equally easy, and sometimes only one is possible at all.**
- **General regions** are Type I ($y$ between two functions of $x$) or Type II. **Outer limits are constants; inner limits may depend on the outer variable.** Reversing the order requires **redrawing the region**, never a mechanical swap of symbols.
- **Polar coordinates:** $dA=r\,dr\,d\theta$. Use for disks, annuli, sectors, and for integrands in $x^2+y^2$. **The $r$ is not a convention — it is the local area factor**, and omitting it is the chapter's most common error.
- **The Gaussian integral $\int_{-\infty}^\infty e^{-x^2}dx=\sqrt\pi$** is provable only by squaring it and going polar. **It is where the $\frac{1}{\sqrt{2\pi}}$ in the normal density and the $\Gamma(\frac12)=\sqrt\pi$ in the $\chi^2$ and $t$ densities come from.**
- **Triple integrals** add one variable and two coordinate systems: cylindrical ($dV=r\,dz\,dr\,d\theta$) for axial symmetry, spherical ($dV=\rho^2\sin\varphi\,d\rho\,d\theta\,d\varphi$) for balls and cones.
- **Change of variables:** $\displaystyle\iint_R f\,dA=\iint_S f(x(u,v),y(u,v))\left\lvert\frac{\partial(x,y)}{\partial(u,v)}\right\rvert du\,dv$. **The Jacobian is the determinant of the derivative matrix, and it is there because a determinant is a volume scale factor.** Absolute value; old-over-new; transform the region too.
- **Probability is this chapter applied.** Joint densities integrate to 1; probabilities are volumes; independence is factorisation; expectations are the centre of mass. **The density transformation rule $f_{\mathbf Y}(\mathbf y)=f_{\mathbf X}(T^{-1}(\mathbf y))|\det \partial\mathbf x/\partial\mathbf y|$ is the change-of-variables formula**, and it yields both the convolution formula and the multivariate normal's constant $(2\pi)^{-n/2}(\det\Sigma)^{-1/2}$.
- **In high dimensions the volume of the unit ball peaks at $n=5$ and then collapses to zero**, and almost all of a ball's volume lies in a thin shell at its surface. **That is the curse of dimensionality, computed with nothing but this chapter's tools.**

---

## ⚠️ Important Notes

> [!warning] The eight mistakes that actually cost marks
> 1. **Forgetting the $r$ in polar** (or the $\rho^2\sin\varphi$ in spherical). **Every polar answer that is off by a clean factor is this.**
> 2. **Reversing the order by swapping symbols.** $\int_0^1\!\int_x^1 f\,dy\,dx$ is **not** $\int_0^1\!\int_y^1 f\,dx\,dy$. Redraw. Every time.
> 3. **A variable surviving its own integration.** If $y$ appears after $\int\cdots dy$, the limits were wrong.
> 4. **Dropping the absolute value on the Jacobian.** A negative Jacobian is fine; a negative area is not.
> 5. **Inverting the Jacobian.** The formula needs $\frac{\partial(x,y)}{\partial(u,v)}$ — **old with respect to new.** If you have the other one, take its reciprocal.
> 6. **Changing variables in the integrand but not in the region.** The new region $S$ must be found by transforming the boundary of $R$.
> 7. **Factoring $\iint g(x)h(y)$ over a non-rectangle.** The product rule requires a *product* region.
> 8. **Assuming a triple integral's order is forced.** All six orders are legal on a box; on a general solid, choosing the right projection can turn three integrals into one line.

> [!tip] How to choose the order of integration
> **In priority order:**
> 1. **Can the inner integral be done at all?** $e^{\pm y^2}$, $\sin(y^2)$, $\frac{\sin y}{y}$, $\sqrt{1+y^3}$ as *inner* integrands mean the order is wrong. Swap.
> 2. **Does one order need fewer pieces?** A region that is one Type II strip but two Type I strips should be integrated as Type II.
> 3. **Does the integrand contain $x^2+y^2$, or the region contain circles?** Go polar.
> 4. **Otherwise take the one with simpler algebra**, usually the one whose inner limits are constants.

> [!note] Where each idea reappears
> - **[[Probability Theory/contents/06 - Jointly Distributed Random Variables|Probability ch. 06]]** is §8 of this chapter done properly: joint and marginal densities, independence, convolution, the bivariate normal, and **the Jacobian formula for transformations of random vectors** — which is §7 verbatim.
> - **[[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]]**: expectations of functions of two variables are double integrals; the covariance matrix collects second moments, i.e. moments of inertia.
> - **[[Mathematical Statistics/contents/00-Index|Math Stats]]**: the sampling distributions of $\bar X$ and $S^2$, and the derivations of the $\chi^2$, $t$ and $F$ densities, are Jacobian computations on the multivariate normal.
> - **[[Linear Algebra/contents/03 - Determinants and Diagonalization|Linear Algebra ch. 03]]** supplies the fact that makes §7 true: $|\det A|$ is the volume scale factor of a linear map. **[[Linear Algebra/contents/08 - Orthogonality|Ch. 08]]** supplies the factorisation $\Sigma=AA^{\mathsf T}$.
> - **[[Machine Learning/contents/00-Index|Machine Learning]]**: §9's dimension counting is the curse of dimensionality; §8's reparameterisation is how VAEs and normalising flows are trained.

> [!important] The one-sentence version of the chapter
> **A multiple integral is several single integrals, in an order you get to choose; and when you change variables, the price is the absolute value of a determinant.**

---

> [!warning] Gaps in the source material
> **Extraction.** Chapter 15 suffers the vault-wide Stewart cipher documented in [[00-Index|the index]] (`s`…`d` for parentheses, `−` for $=$, isolated `1`/`2` for $+$/$-$, `y` for the fraction bar). **In this chapter the damage is worse than elsewhere for one specific reason: the integral signs, their limits, and the differentials all detach from one another.** A displayed iterated integral arrives as a column of loose numbers — `y | 3 | 0 | y | 2 | 1 | x2y dy dx` for $\int_0^3\!\int_1^2 x^2y\,dy\,dx$ — with **no reliable way to tell which limit belongs to which sign**. Stacked limits also invert: Example 4 of §15.3 extracts with its lower limit printed above the upper. **Every iterated integral in this note was reconstructed from the region description and then recomputed**, not read off.
>
> **Figures lost, and here the loss is structural rather than decorative.** This chapter's arguments *are* pictures:
> - **Every region of integration** — the parabola-and-line region, the trapezoid of §15.9 Example 3, the triangle $x+y<20$ of the waiting-time example. **§3 is a section about drawing regions, taught entirely through figures that do not survive.**
> - **Figures 3–6 of §15.9**, which show a small $uv$-rectangle mapping to a curvilinear parallelogram spanned by $\Delta u\,\mathbf r_u$ and $\Delta v\,\mathbf r_v$. **This sequence is the derivation of the Jacobian**; §7 above has to argue it in prose.
> - **The polar and spherical volume elements** (Figures 5 of §15.3, 9 of §15.7, 8 of §15.8) — the diagrams from which $dA=r\,dr\,d\theta$ and $dV=\rho^2\sin\varphi\,d\rho\,d\theta\,d\varphi$ are *read off* rather than computed.
> - **Figure 9 of §15.4, the bivariate normal surface**, and Figure 7's picture of probability as volume.
> - The Riemann-sum column diagrams and the Colorado snowfall contour maps of §15.1 (Examples 9, and Exercises 7–8), which **cannot be attempted at all** — the data exists only in the images.
>
> **Verification performed.** Every numeric claim quoted from or checked against Stewart in this note was recomputed symbolically with `sympy`:
> - §15.1: Example 4 both orders ($27/2$), Example 5 both orders ($-12$), Example 7 ($48$), the Midpoint Rule value $-11.875$.
> - §15.3: Examples 1–5 ($15\pi/2$, $\pi/4$, $\pi/2$, $\pi/8$, $3\pi/2$) — **all correct.**
> - §15.4: Example 6 ($C=1/1500$, $P=868/1500=217/375\approx0.5787$), Example 7 ($1+e^{-4}-2e^{-2}\approx0.74765$), Example 8 (the bivariate-normal probability $\approx0.9111$, so $\approx0.09$ — correct).
> - §15.7 Example 3 ($16\pi/3$); §15.8 Examples 1–3 (including $4\pi(e-1)/3$).
> - §15.9: the polar Jacobian $r$; Example 2's Jacobian $4u^2+4v^2$ and answer $2$; Example 3's Jacobian $-\tfrac12$ and answer $\tfrac34(e-e^{-1})=\tfrac32\sinh 1\approx1.7628$; the spherical Jacobian $-\rho^2\sin\varphi$ in Stewart's $(\rho,\theta,\varphi)$ ordering.
> - The hypersphere table of §9, the unit-ball volume $4\pi/3$, the cone $\tfrac13\pi R^2h$, and all five exercises.
>
> **No mathematical error was found in Stewart's chapter 15.** One cosmetic artefact: the spherical-Jacobian expansion on p. 1115 extracts with a duplicated $\theta$ inside the second $2\times2$ determinant; recomputation confirms the printed *result* $-\rho^2\sin\varphi$ is right, so this is an extraction artefact rather than a typo in the book.
>
> **Scope and editorial decisions.**
> - **§15.5 (surface area) is compressed to one paragraph** and **§15.4's mass, centre-of-mass, moment-of-inertia and radius-of-gyration material is given only as the dictionary in §8.** Nothing downstream in this vault uses them as physics; they matter here **only** because they are literally the same integrals as means and second moments.
> - **The Gaussian integral is promoted from Exercise 15.3.50 into the body**, and **the hyperspheres Discovery Project (§15.6) is promoted into §9.** Both are the chapter's most consequential results for a data-science reader and both are, in Stewart, optional. **This is a deliberate departure from the book's emphasis.**
> - **§8's material beyond Stewart** — the general density-transformation rule, the convolution derivation, the multivariate normal's normalising constant, and the reparameterisation trick — **is my own addition**, drawn from [[Probability Theory/contents/06 - Jointly Distributed Random Variables|Probability ch. 06]] and [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]]. **Stewart's §15.4 stops at the bivariate normal with a diagonal covariance and independent margins**; he never writes $\Sigma$ at all.
> - **The Fubini counterexample in §2 is not in Stewart**, who states the continuity hypothesis without showing what its failure costs. It is included because the hypothesis is otherwise invisible and is exactly the one that fails in probability, where domains are infinite.
> - **Applied/Discovery Projects otherwise omitted** per the index's standing convention: *Roller Derby* (§15.7) and *The Intersection of Three Cylinders* (§15.8).

#calculus #multiple-integrals #fubini #polar-coordinates #spherical-coordinates #jacobian #change-of-variables #gaussian-integral #joint-density #curse-of-dimensionality
