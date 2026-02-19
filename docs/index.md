---
hide:
  - navigation
---

<div class="hero">
<h1>Optimal Hermite Lattices</h1>
<p class="subtitle">
A curated database of optimal on-lattice Gauss–Hermite quadrature rules in 1D, 2D, and 3D — designed for kinetic theory, lattice Boltzmann methods, and anyone who needs to integrate polynomials against Gaussians on a regular grid.
</p>
</div>

<div class="stats-row">
<div class="stat-box">
  <div class="number">35</div>
  <div class="label">Lattice rules</div>
</div>
<div class="stat-box">
  <div class="number">1D–3D</div>
  <div class="label">Dimensions</div>
</div>
<div class="stat-box">
  <div class="number">675</div>
  <div class="label">Max quadrature points</div>
</div>
<div class="stat-box">
  <div class="number">33</div>
  <div class="label">Max polynomial degree</div>
</div>
</div>

---

## What is this?

These lattices solve a deceptively elegant problem: **find the smallest set of equally-spaced points** (on a Cartesian grid) that can exactly integrate multivariate polynomials against the Gaussian weight function

\[
\int_{\mathbb{R}^d} f(\boldsymbol{\xi})\, \frac{e^{-|\boldsymbol{\xi}|^2/2}}{(2\pi)^{d/2}} \, d\boldsymbol{\xi} \;=\; \sum_{a} w_a \, f(c\,\boldsymbol{\xi}_a)
\]

where \(\boldsymbol{\xi}_a\) are integer-coordinate points on a lattice with spacing \(c\), and \(w_a\) are the quadrature weights.

Unlike classical Gauss–Hermite quadrature (which uses irregularly spaced nodes), these rules live on a **regular lattice** — which is essential for lattice Boltzmann methods, discrete velocity models, and other applications where particles must travel between grid points in exact integer steps.

## Why does it matter?

In the **lattice Boltzmann method** (LBM), the discrete velocity set *is* the computational grid. The accuracy of macroscopic conservation laws — mass, momentum, energy, and higher-order stress tensors — depends directly on how well the velocity lattice integrates Hermite polynomial moments of the equilibrium distribution. These optimal lattices tell you the **minimum number of velocities needed** to recover a given order of accuracy.

The connection is precise: a lattice that is exact for Hermite polynomials up to degree \(N\) guarantees that the Chapman–Enskog expansion of the LBM recovers the Navier–Stokes equations (and beyond) to the corresponding order.

## Getting started

<div class="lattice-grid">
<div class="lattice-card">
<a href="background/">
<h3>📐 Background</h3>
<div class="meta">The mathematical framework: Hermite polynomials, Gauss–Hermite quadrature, and the lattice constraint.</div>
</a>
</div>
<div class="lattice-card">
<a href="methods/">
<h3>🔧 Methods</h3>
<div class="meta">How these lattices are computed: characteristic matrices, root-finding, and integer programming.</div>
</a>
</div>
<div class="lattice-card">
<a href="catalog/">
<h3>📊 Lattice Catalog</h3>
<div class="meta">Browse all 35 lattice rules with full weights, abscissas, and spacing values.</div>
</a>
</div>
</div>

## Quick reference

| Dimension | Available lattices | Points range | Max degree |
|:---------:|:------------------:|:------------:|:----------:|
| 1D | D1Q3 – D1Q29 (10 rules) | 3 – 29 | 20 |
| 2D | D2Q9 – D2Q413 (21 rules) | 9 – 413 | 33 |
| 3D | D3Q15 – D3Q675 (4 rules) | 15 – 675 | 15 |

## Citation

If you use these lattices in your research, please cite:

> X. Shan, "The mathematical structure of the lattices of the lattice Boltzmann method," *J. Comput. Sci.*, vol. 17, pp. 475–481, 2016.

```bibtex
@article{shan2016,
  title={The mathematical structure of the lattices of the lattice Boltzmann method},
  author={Shan, Xiaowen},
  journal={Journal of Computational Science},
  volume={17},
  pages={475--481},
  year={2016}
}
```

---

<p style="text-align:center; color: var(--md-default-fg-color--light); font-size:0.85rem;">
Built with ❤️ for the lattice Boltzmann community · Data by Pakorn Wongwaitayakornkul
</p>
