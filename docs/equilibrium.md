# Equilibrium Distribution: Laguerre–Hermite Expansion

The Maxwell–Boltzmann equilibrium distribution can be expanded exactly in the Hermite basis using a closed-form **Laguerre expansion** in powers of $(1-\theta)$. This page presents the main result, explicit expansion terms up to 6th order, and a Python implementation.

---

## Main result

The Maxwell–Boltzmann equilibrium

$$
f^{0}(\boldsymbol{\xi}) = \frac{\rho}{(2\pi\theta)^{D/2}}\exp\!\left(-\frac{|\boldsymbol{\xi}-\mathbf{u}|^{2}}{2\theta}\right)
$$

expanded in the Hermite basis with weight $\omega(\boldsymbol{\xi}) = (2\pi)^{-D/2}e^{-|\boldsymbol{\xi}|^{2}/2}$, admits the closed-form Laguerre expansion:

$$
\boxed{\;
\frac{f^{0}(\boldsymbol{\xi})}{\omega(\boldsymbol{\xi})\,\rho}
= e^{\,\boldsymbol{\xi}\cdot\mathbf{u} - |\mathbf{u}|^{2}/2}
\sum_{p=0}^{\infty}(1-\theta)^{p}\,
L_{p}^{(D/2-1)}\!\!\left(\frac{|\boldsymbol{\xi}-\mathbf{u}|^{2}}{2}\right)
\;}
$$

Here $L_{p}^{(\alpha)}$ is the generalized Laguerre polynomial, $D$ is the spatial dimension, $\theta = T/T_{\mathrm{ref}}$, and truncation at order $P$ gives accuracy $O((\theta{-}1)^{P+1})$.

---

## Explicit expansion to 6th order

### Notation

Define the shorthand variables:

| Symbol | Definition |
|:------:|:-----------|
| $\varepsilon$ | $\theta - 1$ |
| $s$ | $\boldsymbol{\xi}\cdot\mathbf{u}$ |
| $v$ | $\lvert\boldsymbol{\xi}\rvert^{2}$ |
| $w$ | $\lvert\mathbf{u}\rvert^{2}$ |
| $\mathrm{He}_{n}(s;w)$ | $\displaystyle\sum_{j=0}^{\lfloor n/2\rfloor}(-1)^{j}\frac{n!}{j!(n{-}2j)!\,2^{j}}\,w^{j}\,s^{n-2j}$ |

### (a) Hermite coefficients $a_{0}^{(n)}/\rho$

From the generating function $e^{tu + \varepsilon t^{2}/2}$:

| $n$ | $a_{0}^{(n)}/\rho$ | $n$ | $a_{0}^{(n)}/\rho$ |
|:---:|:--------------------|:---:|:--------------------|
| 0 | $1$ | 4 | $u^{4} + 6\varepsilon\, u^{2} + 3\varepsilon^{2}$ |
| 1 | $u$ | 5 | $u^{5} + 10\varepsilon\, u^{3} + 15\varepsilon^{2}\, u$ |
| 2 | $u^{2} + \varepsilon$ | 6 | $u^{6} + 15\varepsilon\, u^{4} + 45\varepsilon^{2}\, u^{2} + 15\varepsilon^{3}$ |
| 3 | $u^{3} + 3\varepsilon\, u$ | | |

### (b) Full expansion table

The full expansion $f^{0}\!/(\omega\rho) = \sum_{n}\tfrac{1}{n!}\,\mathbf{a}_{0}^{(n)}:\mathcal{H}^{(n)}(\boldsymbol{\xi})$, organized by Hermite order $n$ and power of $\varepsilon$. All formulas hold for any $D$; $L_{p}^{(\alpha)}(v/2)$ denotes the Laguerre polynomial at $|\boldsymbol{\xi}|^{2}/2$.

| $n$ | $\varepsilon^{0}$ | $\varepsilon^{1}$ | $\varepsilon^{2}$ | $\varepsilon^{3}$ |
|:---:|:---|:---|:---|:---|
| 0 | $1$ | | | |
| 1 | $s$ | | | |
| 2 | $\dfrac{s^{2}-w}{2}$ | $\dfrac{v - D}{2}$ | | |
| 3 | $\dfrac{s^{3}-3ws}{6}$ | $\dfrac{s(v - D - 2)}{2}$ | | |
| 4 | $\dfrac{\mathrm{He}_{4}}{24}$ | $\dfrac{s^{2}(v{-}D{-}4) - w(v{-}D{-}2)}{4}$ | $L_{2}^{(D/2-1)}\!\bigl(\tfrac{v}{2}\bigr)$ | |
| 5 | $\dfrac{\mathrm{He}_{5}}{120}$ | $\dfrac{s^{3}(v{-}D{-}6) - 3sw(v{-}D{-}4)}{12}$ | $s\,L_{2}^{(D/2)}\!\bigl(\tfrac{v}{2}\bigr)$ | |
| 6 | $\dfrac{\mathrm{He}_{6}}{720}$ | $\dfrac{s^{4}(v{-}D{-}8) - 6s^{2}w(v{-}D{-}6) + 3w^{2}(v{-}D{-}4)}{48}$ | $\dfrac{s^{2}\,L_{2}^{(D/2+1)}\!(\frac{v}{2}) - w\,L_{2}^{(D/2)}\!(\frac{v}{2})}{2}$ | $-L_{3}^{(D/2-1)}\!\bigl(\tfrac{v}{2}\bigr)$ |

Entry $(n,\varepsilon^{k})$ gives $F_{n,k}$; the full expansion is $f^{0}\!/(\omega\rho) = \sum_{n,k} \varepsilon^{k}F_{n,k}$; $\mathrm{He}_{n} \equiv \mathrm{He}_{n}(s;w)$; row $n$ has $k = 0,\ldots,\lfloor n/2\rfloor$.

!!! info "Useful general formulas"
    **General $\varepsilon^{1}$ formula** ($n \ge 2$):

    $$
    F_{n,1} = \frac{(v{-}D)\,\mathrm{He}_{n-2} - 2(n{-}2)\,s\,\mathrm{He}_{n-3} + (n{-}2)(n{-}3)\,w\,\mathrm{He}_{n-4}}{2\,(n{-}2)!}
    $$

    **Highest-$\varepsilon$ terms:**

    $$
    F_{2k,k} = L_{k}^{(D/2-1)}\!(v/2), \qquad F_{2k+1,k} = s\,L_{k}^{(D/2)}\!(v/2)
    $$

---

## Derivation sketch

1. **Exact ratio.** Divide $f^{0}$ by $\omega\rho$ and define $q := s - (v{+}w)/2 = -|\boldsymbol{\xi}{-}\mathbf{u}|^{2}/2$:

    $$
    \frac{f^{0}}{\omega\rho}
    = e^{s-w/2}\,\underbrace{(1{+}\varepsilon)^{-D/2}\exp\!\bigl(-\tfrac{q\varepsilon}{1{+}\varepsilon}\bigr)}_{=:\,G(\varepsilon)}
    $$

2. **Expand $G(\varepsilon)$.** Write $\exp(-q\varepsilon/(1{+}\varepsilon)) = \sum_{m}\frac{(-q)^{m}}{m!}\varepsilon^{m}(1{+}\varepsilon)^{-m}$, giving

    $$
    G(\varepsilon) = \sum_{m=0}^{\infty}\frac{(-q)^{m}}{m!}\varepsilon^{m}(1{+}\varepsilon)^{-(D/2+m)}
    $$

3. **Collect $\varepsilon^{p}$.** The coefficient is

    $$
    C_{p} = (-1)^{p}\sum_{m=0}^{p}\binom{D/2{+}p{-}1}{p{-}m}\frac{q^{m}}{m!}
    = (-1)^{p}L_{p}^{(D/2-1)}\!\bigl(\tfrac{|\boldsymbol{\xi}-\mathbf{u}|^{2}}{2}\bigr)
    $$

    which is precisely the generalized Laguerre polynomial.

4. **Conclude.** Since $(-1)^{p}\varepsilon^{p} = (1{-}\theta)^{p}$, multiplying by $e^{s-w/2}$ yields the main result. Convergence: analytic for $\varepsilon > -1$ ($\theta > 0$).

---

## Python implementation

The following code computes the equilibrium distribution $f^{0}$ on any lattice using the Laguerre–Hermite expansion truncated at a chosen order.

### Core functions

```python
import numpy as np
from scipy.special import genlaguerre


def feq_exact(xi, rho, u, theta, D):
    """Exact Maxwell-Boltzmann equilibrium distribution.

    Parameters
    ----------
    xi : ndarray, shape (Q, D)
        Discrete velocity vectors.
    rho : float
        Density.
    u : ndarray, shape (D,)
        Macroscopic velocity.
    theta : float
        Reduced temperature T / T_ref.
    D : int
        Spatial dimension.

    Returns
    -------
    f0 : ndarray, shape (Q,)
        Equilibrium distribution at each velocity.
    """
    diff = xi - u  # (Q, D)
    return rho / (2 * np.pi * theta) ** (D / 2) * np.exp(
        -np.sum(diff**2, axis=1) / (2 * theta)
    )


def feq_laguerre(xi, rho, u, theta, D, P):
    """Equilibrium via Laguerre-Hermite expansion truncated at order P.

    Parameters
    ----------
    xi : ndarray, shape (Q, D)
        Discrete velocity vectors.
    rho : float
        Density.
    u : ndarray, shape (D,)
        Macroscopic velocity.
    theta : float
        Reduced temperature T / T_ref.
    D : int
        Spatial dimension.
    P : int
        Truncation order in (1 - theta).

    Returns
    -------
    f0 : ndarray, shape (Q,)
        Approximate equilibrium distribution at each velocity.
    """
    # Gaussian weight
    omega = (2 * np.pi) ** (-D / 2) * np.exp(-np.sum(xi**2, axis=1) / 2)

    # Velocity-shift exponential
    s = xi @ u                          # xi . u
    w = np.dot(u, u)                    # |u|^2
    exp_shift = np.exp(s - w / 2)

    # Argument of the Laguerre polynomials: |xi - u|^2 / 2
    diff = xi - u
    z = np.sum(diff**2, axis=1) / 2

    # Sum the Laguerre series
    alpha = D / 2 - 1
    eps_minus = 1 - theta
    series = np.zeros(len(xi))
    for p in range(P + 1):
        Lp = genlaguerre(p, alpha)(z)   # L_p^(alpha)(z)
        series += eps_minus**p * Lp

    return rho * omega * exp_shift * series
```

### Example: D2Q9 lattice

```python
import numpy as np

# D2Q9 velocity set (spacing c = sqrt(3))
c = np.sqrt(3)
xi = c * np.array([
    [0, 0],
    [1, 0], [-1, 0], [0, 1], [0, -1],
    [1, 1], [-1, 1], [1, -1], [-1, -1],
])

# Macroscopic quantities
rho = 1.0
u = np.array([0.1, 0.05])
theta = 1.0   # isothermal case
D = 2

# Compare exact vs Laguerre expansion at different truncation orders
f_exact = feq_exact(xi, rho, u, theta, D)

for P in [0, 2, 4, 6]:
    f_lag = feq_laguerre(xi, rho, u, theta, D, P)
    err = np.max(np.abs(f_lag - f_exact))
    print(f"P = {P:2d}:  max |error| = {err:.2e}")
```

??? example "Expected output"
    ```
    P =  0:  max |error| = 0.00e+00
    P =  2:  max |error| = 0.00e+00
    P =  4:  max |error| = 0.00e+00
    P =  6:  max |error| = 0.00e+00
    ```

    At $\theta = 1$ (isothermal), $\varepsilon = 0$ so all correction terms vanish — any truncation order gives the exact result. The expansion becomes nontrivial for $\theta \neq 1$.

### Thermal flow example ($\theta \neq 1$)

```python
# Thermal case: theta != 1
theta = 1.2
D = 2

# Use a higher-order lattice for thermal flows
# D2Q49 velocity set with appropriate spacing
# (replace with actual lattice data from the catalog)

f_exact = feq_exact(xi, rho, u, theta, D)

print("Convergence of Laguerre expansion (theta = 1.2):")
for P in range(7):
    f_lag = feq_laguerre(xi, rho, u, theta, D, P)
    err = np.max(np.abs(f_lag - f_exact))
    print(f"  P = {P}:  max |error| = {err:.2e}")
```

!!! tip "Choosing the truncation order"
    The error scales as $O((\theta - 1)^{P+1})$. For mildly thermal flows ($\theta \approx 1$), even $P = 2$ is often sufficient. For strongly non-isothermal flows, use $P = 4$ or $P = 6$ with a lattice that has enough quadrature points to support the higher-order moments.

---

## Reference

*"Equilibrium Distribution as Hermite Expansion: General Theory and the Laguerre Representation"* (2026).
