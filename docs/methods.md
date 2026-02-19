# Computational Methods

This page walks through the algorithms used to compute the optimal Hermite lattice quadrature rules in our database. The approach combines **symbolic algebra**, **polynomial root-finding**, and **integer linear programming** — a satisfying blend of pure math and optimization.

---

## Overview of the pipeline

The computation proceeds in four main stages:

<div class="method-step">
<h3>Step 1 — Compute multivariate Hermite polynomials</h3>
Build the tensorial Hermite polynomials \(\mathbf{H}^{(n)}(\boldsymbol{\xi})\) up to the desired degree, using a recursive formula.
</div>

<div class="method-step">
<h3>Step 2 — Assemble the characteristic matrix</h3>
Substitute lattice points into the Hermite polynomials and collect the quadrature conditions into a single matrix equation in the weights and spacing.
</div>

<div class="method-step">
<h3>Step 3 — Solve for the lattice spacing</h3>
Reduce the matrix to row-echelon form. The last row yields a polynomial in the spacing \(c\), whose positive real roots give candidate lattice spacings.
</div>

<div class="method-step">
<h3>Step 4 — Minimize the number of points</h3>
For each valid spacing, solve a mixed-integer program to find the fewest lattice shells (and their weights) that satisfy all quadrature conditions.
</div>

Let's dig into each step.

---

## Step 1: Multivariate Hermite polynomials

### The recurrence relation

Instead of computing the tensorial Hermite polynomial from its definition (which involves high-order derivatives of the Gaussian), we use a **three-term recurrence**:

\[
H^{(n)}_{i_1 i_2 \cdots i_n}(\boldsymbol{\xi}) = \xi_{i_1}\, H^{(n-1)}_{i_2 \cdots i_n}(\boldsymbol{\xi}) - \sum_{k=2}^{n} \delta_{i_1 i_k}\, H^{(n-2)}_{i_2 \cdots \hat{i}_k \cdots i_n}(\boldsymbol{\xi})
\]

where \(\hat{i}_k\) means "omit index \(i_k\)." The base cases are

\[
H^{(0)} = 1, \qquad H^{(1)}_i = \xi_i.
\]

This recurrence is implemented in the `HermiteDict` class, which stores the polynomials as a dictionary keyed by sorted index tuples. Memoization avoids recomputing lower-order terms.

!!! note "Symmetry reduction"
    Because the Hermite tensor is symmetric under permutation of its indices, we only need to store entries for **sorted** index tuples \((i_1 \leq i_2 \leq \cdots \leq i_n)\). The number of unique components for a rank-\(n\) tensor in \(d\) dimensions is \(\binom{d + n - 1}{n}\), which is much smaller than \(d^n\).

### Example: 2D, order 4

The rank-4 Hermite polynomial in 2D has \(\binom{2 + 4 - 1}{4} = 5\) unique components:

| Index | \(H^{(4)}_{ijkl}(\xi_1, \xi_2)\) |
|:-----:|:---------------------------------|
| (1,1,1,1) | \(\xi_1^4 - 6\xi_1^2 + 3\) |
| (1,1,1,2) | \(\xi_1^3 \xi_2 - 3\xi_1 \xi_2\) |
| (1,1,2,2) | \(\xi_1^2 \xi_2^2 - \xi_1^2 - \xi_2^2 + 1\) |
| (1,2,2,2) | \(\xi_1 \xi_2^3 - 3\xi_1 \xi_2\) |
| (2,2,2,2) | \(\xi_2^4 - 6\xi_2^2 + 3\) |

---

## Step 2: The characteristic matrix

### Setting up the linear system

Given a dimension \(d\), maximum layer \(L\), and target polynomial degree \(N\), we:

1. **Enumerate generator points.** List all ordered tuples \(\mathbf{n} = (n_1, \ldots, n_d)\) with \(0 \leq n_1 \leq n_2 \leq \cdots \leq n_d \leq L\). Each generator produces a full symmetry orbit of lattice points.

2. **Assign one weight per generator.** Let \(w_1, w_2, \ldots, w_K\) be the unknown weights, one for each generator.

3. **Write the quadrature conditions.** For each even order \(n = 0, 2, 4, \ldots, N-1\), substitute each symmetric orbit into the Hermite polynomial and sum:

\[
\sum_{k=1}^{K} w_k \sum_{\mathbf{n}' \in \text{orbit}(\mathbf{n}_k)} H^{(n)}_{i_1 \cdots i_n}(c\, \mathbf{n}') = \delta_{n0}
\]

!!! info "Why only even orders?"
    The odd-order Hermite polynomials are automatically zero when summed over the full symmetry orbit (which includes both \(\mathbf{n}\) and \(-\mathbf{n}\)). So we only need to enforce the even-order conditions.

4. **Collect into a matrix.** Each unique polynomial condition gives one row. The columns correspond to weights \(w_1, \ldots, w_K\), and the rightmost column is the target vector (1 for order 0, 0 otherwise). The matrix entries are polynomials in \(c\).

This yields the **characteristic matrix** \(\mathbf{M}(c)\):

\[
\mathbf{M}(c)\, \mathbf{w} = \mathbf{b}
\]

---

## Step 3: Solving for the lattice spacing

### Row reduction and the spacing polynomial

We apply **Gaussian elimination** (symbolically) to reduce \(\mathbf{M}(c)\) to row-echelon form. After elimination, the last non-trivial row contains only \(c\) (no weights), producing a **univariate polynomial equation** in \(c\):

\[
P(c) = 0.
\]

The positive real roots of \(P(c)\) are the candidate lattice spacings. We compute these roots to high precision (typically 200+ digits) using SymPy's `real_roots` function.

!!! tip "Physical interpretation of the spacing"
    The lattice spacing \(c\) determines the **lattice temperature** \(T_L = c^2\). In LBM applications, \(c = \sqrt{3}\) gives the familiar D1Q3 / D2Q9 lattices where the speed of sound is \(c_s = 1/\sqrt{3}\).

### Example: 1D with layer 1

For \(d = 1\), \(L = 1\), and degree 5, the generator points are \(\{0, 1\}\). The characteristic matrix after row reduction gives:

\[
P(c) = c^2 - 3 = 0 \quad \Longrightarrow \quad c = \sqrt{3} \approx 1.73205
\]

This is the classic D1Q3 lattice!

---

## Step 4: Minimizing the number of points

### The integer programming formulation

For each valid spacing \(c^*\), we substitute into the characteristic matrix and solve for the weights. But we want the **minimum number of active shells** — this is where optimization enters.

We formulate a **mixed-integer linear program** (MILP):

**Variables:**

- \(w_k \geq 0\): weight for shell \(k\) (continuous)
- \(x_k \in \{0, 1\}\): indicator — is shell \(k\) active? (binary)

**Constraints:**

\[
\mathbf{M}(c^*)\, \mathbf{w} = \mathbf{b}
\]
\[
w_k \leq M\, x_k \qquad \text{(big-M: if } x_k = 0 \text{ then } w_k = 0\text{)}
\]

**Objective:** minimize \(\sum_k s_k\, x_k\), where \(s_k\) is the number of points in shell \(k\).

This is solved using the **Gurobi** optimizer. The result gives us the minimum total number of quadrature points and the corresponding weights.

!!! example "D2Q9: the classic lattice"
    For \(d = 2\), the MILP selects 3 shells from the available candidates:

    | Shell | Generator | Points | Weight |
    |:-----:|:---------:|:------:|:------:|
    | 0 | (0, 0) | 1 | 4/9 |
    | 1 | (0, 1) | 4 | 1/9 |
    | 2 | (1, 1) | 4 | 1/36 |

    Total: **9 points**, exact for degree 5. Spacing: \(c = \sqrt{3}\).

---

## Multiple solutions and naming conventions

For higher-order lattices (e.g., D2Q49), the spacing polynomial \(P(c)\) can have **multiple positive real roots**, each yielding a different valid lattice. These are labeled with letter suffixes: D2Q49**a**, D2Q49**b**, D2Q49**c**, etc.

All solutions in our database are **optimal** in the sense that they use the minimum number of quadrature points for their given polynomial degree and dimension, among all lattice spacings arising from the same characteristic matrix.

---

## Implementation details

The core computation is implemented in Python, using:

| Component | Library |
|:----------|:--------|
| Symbolic algebra (Hermite polynomials, row reduction) | [SymPy](https://www.sympy.org/) |
| Numerical arrays and linear algebra | [NumPy](https://numpy.org/) |
| Mixed-integer optimization | [Gurobi](https://www.gurobi.com/) |
| High-precision arithmetic | SymPy's arbitrary-precision floats |
| Serialization of lattice data | [dill](https://dill.readthedocs.io/) |

The implementation lives in the `HermiteDict` and `Lattice` classes, with key methods:

```python
# Compute Hermite polynomials recursively
hermite = HermiteDict()
H = hermite.recursive_hermite(order=6, dim=2)

# Build the characteristic matrix
lat = Lattice()
M = lat.create_characteristic_matrix(dim=2, layer=3, order=9)

# Find lattice spacings (roots of the last row)
spacings = lat.root_last_element(M, precision=200)

# Minimize points via MILP
result = lat.minimize_points(M_evaluated)
# → [num_points, active_shells, weights]
```

---

## Computational complexity

The hardest part is the **symbolic row reduction** of the characteristic matrix, which grows rapidly with dimension and layer count. Some rough scaling:

| Dimension | Layers | Matrix size | Compute time |
|:---------:|:------:|:-----------:|:------------:|
| 1D | 1–19 | Small (~20×20) | Seconds |
| 2D | 1–7 | Medium (~50×50) | Minutes |
| 3D | 1–5 | Large (~100+×100+) | Hours to days |

The 3D lattices (D3Q15 through D3Q675) represent significant computational effort and are among the largest optimal Hermite lattices computed to date.

---

## References

1. X. Shan, "The mathematical structure of the lattices of the lattice Boltzmann method," *J. Comput. Sci.*, vol. 17, pp. 475–481, 2016.
2. X. Shan, "General solution of lattices for Cartesian lattice Bhatnagar–Gross–Krook models," *Phys. Rev. E*, vol. 81, 036702, 2010.
