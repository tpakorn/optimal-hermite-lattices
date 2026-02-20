# Mathematical Background

This page introduces the mathematical framework behind optimal Hermite lattice quadrature. The key idea: choose a set of **equally-spaced points on a Cartesian grid** that can exactly reproduce the moments of a Gaussian-weighted polynomial — the building blocks of kinetic theory.

---

## The Gauss–Hermite integration problem

We want to approximate integrals of the form

$$
\int_{\mathbb{R}^d} f(\boldsymbol{\xi})\, \omega(\boldsymbol{\xi})\, d\boldsymbol{\xi}
$$

where $\omega$ is the standard $d$-dimensional Gaussian weight

$$
\omega(\boldsymbol{\xi}) = \frac{1}{(2\pi)^{d/2}} \exp\!\left(-\frac{|\boldsymbol{\xi}|^2}{2}\right).
$$

The classical *Gauss–Hermite quadrature* picks $n$ nodes and weights $\{(\boldsymbol{\xi}_a, w_a)\}$ so that

$$
\int_{\mathbb{R}^d} f(\boldsymbol{\xi})\, \omega(\boldsymbol{\xi})\, d\boldsymbol{\xi} = \sum_{a=1}^{n} w_a\, f(\boldsymbol{\xi}_a)
$$

holds exactly whenever $f$ is a polynomial up to some degree $N$. In 1D, the optimal $n$-point Gauss–Hermite rule is exact for polynomials of degree up to $2n - 1$, with nodes at the roots of the probabilist's Hermite polynomial $\mathrm{He}_n(\xi)$.

!!! info "Why Hermite polynomials?"
    Hermite polynomials are the orthogonal polynomial family with respect to the Gaussian weight. They form a natural basis for expanding distribution functions in kinetic theory — particularly the Maxwell–Boltzmann equilibrium distribution.

---

## Hermite polynomials — the multivariate version

### 1D probabilist's Hermite polynomials

The 1D probabilist's Hermite polynomial of degree $n$ satisfies

$$
\mathrm{He}_n(\xi) = (-1)^n \, e^{\xi^2/2}\, \frac{d^n}{d\xi^n}\, e^{-\xi^2/2}
$$

and the orthogonality relation

$$
\int_{-\infty}^{\infty} \mathrm{He}_m(\xi)\, \mathrm{He}_n(\xi)\, \omega(\xi)\, d\xi = n!\, \delta_{mn}.
$$

The first few:

| $n$ | $\mathrm{He}_n(\xi)$ |
|:-----:|:--------------------:|
| 0 | 1 |
| 1 | $\xi$ |
| 2 | $\xi^2 - 1$ |
| 3 | $\xi^3 - 3\xi$ |
| 4 | $\xi^4 - 6\xi^2 + 3$ |

### Multivariate (tensorial) Hermite polynomials

In $d$ dimensions, the rank-$n$ Hermite polynomial is a **tensor** $\mathbf{H}^{(n)}(\boldsymbol{\xi})$ with components

$$
H^{(n)}_{i_1 i_2 \cdots i_n}(\boldsymbol{\xi}) = (-1)^n\, \frac{1}{\omega(\boldsymbol{\xi})}\, \frac{\partial^n \omega(\boldsymbol{\xi})}{\partial \xi_{i_1}\, \partial \xi_{i_2} \cdots \partial \xi_{i_n}}.
$$

These tensorial polynomials inherit the key orthogonality property from the 1D case. They show up naturally in the Hermite expansion of the Maxwell–Boltzmann distribution:

$$
f^{(\mathrm{eq})}(\boldsymbol{\xi}) = \omega(\boldsymbol{\xi}) \sum_{n=0}^{\infty} \frac{1}{n!}\, \mathbf{a}^{(n)} : \mathbf{H}^{(n)}(\boldsymbol{\xi})
$$

where $\mathbf{a}^{(n)}$ are the expansion coefficients (related to macroscopic moments: density, velocity, temperature, stress, heat flux, …).

!!! example "Rank-2 example (2D)"
    For $d = 2$ and $n = 2$:

    $$H^{(2)}_{ij}(\boldsymbol{\xi}) = \xi_i \xi_j - \delta_{ij}$$

    The unique components are $H^{(2)}_{11} = \xi_1^2 - 1$, $H^{(2)}_{12} = \xi_1 \xi_2$, $H^{(2)}_{22} = \xi_2^2 - 1$.

---

## The lattice constraint

Here is what makes this problem interesting — and different from classical Gauss–Hermite quadrature.

We require all quadrature nodes to lie on a **regular Cartesian lattice** with spacing $c$:

$$
\boldsymbol{\xi}_a = c\, \mathbf{n}_a, \qquad \mathbf{n}_a \in \mathbb{Z}^d.
$$

This constraint is not merely aesthetic. In the **lattice Boltzmann method**, particle velocities must map grid points to grid points in a single time step. The spacing $c$ relates the thermal velocity scale to the grid spacing — it encodes the *lattice temperature*.

The quadrature condition becomes: find integer vectors $\{\mathbf{n}_a\}$, a spacing $c > 0$, and weights $\{w_a\}$ such that

$$
\sum_{a} w_a\, H^{(n)}_{i_1 \cdots i_n}(c\, \mathbf{n}_a) = \delta_{n0}
$$

for all $n = 0, 1, \ldots, N$. (The right-hand side reflects the fact that $\int \mathbf{H}^{(n)} \omega\, d\boldsymbol{\xi} = 0$ for $n \geq 1$ and equals 1 for $n = 0$.)

---

## Connection to the lattice Boltzmann method

The lattice Boltzmann equation evolves a set of distribution functions $\{f_a\}$ — one per discrete velocity $\boldsymbol{\xi}_a = c\, \mathbf{n}_a$ — through streaming and collision steps. The equilibrium distribution is

$$
f_a^{(\mathrm{eq})} = w_a \left[ \rho + \rho\, \frac{\mathbf{u} \cdot \boldsymbol{\xi}_a}{c_s^2} + \frac{\rho}{2\, c_s^4}\left((\mathbf{u} \cdot \boldsymbol{\xi}_a)^2 - c_s^2\, |\mathbf{u}|^2\right) + \cdots \right]
$$

where $c_s^2 = c^2/d$ is the lattice speed of sound. The quadrature weights $w_a$ and lattice spacing $c$ **must be chosen so that the discrete moments match the continuous Gaussian moments** — which is exactly the Hermite quadrature condition above.

A lattice that satisfies the quadrature condition up to degree $N$ guarantees:

| Degree $N$ | Physical accuracy |
|:---:|:---|
| 2 | Correct density and momentum (isothermal, incompressible limit) |
| 4 | Correct stress tensor — recovers Navier–Stokes equations |
| 6 | Correct heat flux — recovers energy equation (thermal flows) |
| 8+ | Higher-order non-equilibrium effects (Burnett, super-Burnett) |

!!! tip "The naming convention"
    **DdQn** means: $d$-dimensional lattice with $n$ quadrature points. For example, **D2Q9** is the classic 2D lattice Boltzmann velocity set with 9 velocities. **D2Q49a** is a higher-order variant with 49 velocities, sufficient for thermal flows.

---

## Symmetry and lattice shells

The Gaussian weight $\omega(\boldsymbol{\xi})$ is invariant under the full symmetry group of the $d$-dimensional hypercube (permutations and sign changes of coordinates). This means we can organize the lattice into **shells** — orbits of the symmetry group.

Each shell is generated by a single representative point $\mathbf{n}$, and all points obtained by permuting and reflecting its coordinates share the same weight. For example, in 2D, the generator $(1, 2)$ produces the shell

$$
\{(\pm 1, \pm 2),\; (\pm 2, \pm 1)\} \quad \text{(8 points total)}.
$$

This dramatically reduces the number of unknowns. Instead of solving for individual $w_a$, we solve for **one weight per shell** — and the lattice spacing $c$.

The "max layer" parameter in our database indicates the outermost shell index: a lattice with max layer $L$ uses points $\mathbf{n}$ with $\max_i |n_i| \leq L$.

---

## References

1. X. Shan, "The mathematical structure of the lattices of the lattice Boltzmann method," *J. Comput. Sci.*, vol. 17, pp. 475–481, 2016.
2. X. Shan, X.-F. Yuan, and H. Chen, "Kinetic theory representation of hydrodynamics: a way beyond the Navier–Stokes equation," *J. Fluid Mech.*, vol. 550, pp. 413–441, 2006.
3. X. Shan, "General solution of lattices for Cartesian lattice Bhatnagar–Gross–Krook models," *Phys. Rev. E*, vol. 81, 036702, 2010.
