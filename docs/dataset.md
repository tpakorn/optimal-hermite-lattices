# Dataset Usage

This page explains how to load and work with the lattice data file (`lattice.dl`).

<a href="../lattice/lattice.dl" download class="md-button md-button--primary" style="font-size:0.9rem;">
⬇ Download lattice.dl
</a>

---

## File format

The lattice database is stored as a Python dictionary serialized with [dill](https://pypi.org/project/dill/), a drop-in replacement for `pickle` that supports a wider range of Python objects (including SymPy expressions used for exact lattice spacings).

## Loading the data

```python
import dill

with open("lattice.dl", "rb") as f:
    lattices = dill.load(f)
```

The resulting object `lattices` is a `dict` keyed by lattice name strings:

```python
print(list(lattices.keys()))
# ['D1Q3', 'D1Q7', 'D1Q11', ..., 'D3Q675']
```

## Dictionary keys

Each entry `lattices[name]` is itself a dictionary with the following keys:

| Key | Type | Description |
|:----|:-----|:------------|
| `name` | `str` | Lattice identifier, e.g. `"D2Q9"` |
| `dimension` | `int` | Spatial dimension *d* (1, 2, or 3) |
| `num_points` | `int` | Total number of quadrature points *Q* |
| `degree` | `int` | Maximum polynomial degree exactly integrated |
| `max_layer` | `int` | Maximum shell index (outermost lattice layer used) |
| `spacing` | SymPy `Float` | Lattice spacing *c* (high-precision) |
| `abscissas` | `list` of tuples | Generator points (integer coordinates on the lattice) |
| `abscissas_on` | `numpy.ndarray[bool]` | Boolean mask — `True` if the corresponding abscissa is active in this rule |
| `weights` | `numpy.ndarray[float64]` | Quadrature weights for each generator point |

## Naming convention

Lattice names follow the pattern **D***d***Q***q*[*suffix*]:

- **D***d* — the spatial dimension (*d* = 1, 2, or 3)
- **Q***q* — the total number of quadrature points
- *suffix* (optional) — a lowercase letter distinguishing different lattices that share the same *d* and *q* (e.g. `D2Q49a` through `D2Q49i`)

## Example: inspecting a lattice

```python
import dill
import numpy as np

with open("lattice.dl", "rb") as f:
    lattices = dill.load(f)

lat = lattices["D2Q9"]

print(f"Name:      {lat['name']}")
print(f"Dimension: {lat['dimension']}")
print(f"Points:    {lat['num_points']}")
print(f"Degree:    {lat['degree']}")
print(f"Spacing c: {float(lat['spacing']):.15f}")
print(f"Max layer: {lat['max_layer']}")
```

## Working with abscissas and weights

The `abscissas` list contains all candidate generator points up to `max_layer`. The boolean mask `abscissas_on` indicates which of these are actually used in the quadrature rule. To extract the active points and their weights:

```python
active = [
    (ab, w)
    for ab, on, w in zip(lat["abscissas"], lat["abscissas_on"], lat["weights"])
    if on and abs(w) > 0
]

for point, weight in active:
    print(f"  {point}  w = {weight:.10e}")
```

Each generator point represents a symmetry class. The full set of quadrature nodes is obtained by applying all permutations and sign reflections to each generator. For example, the generator `(1, 2)` in 2D expands to the orbit: `{(±1, ±2), (±2, ±1)}`.

## Computing a quadrature sum

To evaluate the Gauss–Hermite integral approximation:

$$
\int_{\mathbb{R}^d} f(\boldsymbol{\xi})\, \frac{e^{-|\boldsymbol{\xi}|^2/2}}{(2\pi)^{d/2}} \, d\boldsymbol{\xi} \approx \sum_{a} w_a \, f(c\,\boldsymbol{\xi}_a)
$$

you need to expand each generator into its full orbit, then sum:

```python
from itertools import product

def expand_orbit(gen, dim):
    """Expand a generator point into its full orbit under
    permutations and sign reflections."""
    from itertools import permutations
    orbit = set()
    for perm in permutations(gen):
        for signs in product([-1, 1], repeat=dim):
            orbit.add(tuple(s * p for s, p in zip(signs, perm)))
    return list(orbit)

c = float(lat["spacing"])

# Example: integrate f(xi) = |xi|^2  (should give d = dimension)
total = 0.0
for ab, on, w in zip(lat["abscissas"], lat["abscissas_on"], lat["weights"]):
    if not on or abs(w) < 1e-30:
        continue
    for node in expand_orbit(ab, lat["dimension"]):
        xi = np.array(node) * c
        total += w * np.dot(xi, xi)

print(f"|xi|^2 integral: {total:.10f}  (expected: {lat['dimension']})")
```

## Dependencies

To load and use the lattice data you need:

- **Python 3.8+**
- **dill** — `pip install dill`
- **NumPy** — `pip install numpy`
- **SymPy** (optional, for exact spacing arithmetic) — `pip install sympy`

---

[Back to Home](index.md)
