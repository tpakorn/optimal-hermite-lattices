#!/usr/bin/env python3
"""Generate MkDocs pages from lattice.dl data."""

import sys
import os
import numpy as np
import dill as dl
import re

# Load the lattice data
lattice_path = os.path.join(os.path.dirname(__file__), '..', 'lattice.dl')
lattice = dl.load(open(lattice_path, 'rb'))

# Also generate 1D lattices inline (they're computed, not stored in lattice.dl)
# We'll check what's in the file first
print(f"Loaded {len(lattice)} lattices: {list(lattice.keys())}")

DOCS = os.path.join(os.path.dirname(__file__), 'docs')
LATTICE_DIR = os.path.join(DOCS, 'lattices')
os.makedirs(LATTICE_DIR, exist_ok=True)


def parse_name(name):
    """Extract dimension and num_points from name like D2Q17a."""
    m = re.match(r'D(\d+)Q(\d+)([a-z]?)', name)
    if m:
        return int(m.group(1)), int(m.group(2)), m.group(3)
    return None, None, ''


def format_float(x, digits=10):
    """Format float to given significant digits."""
    if abs(x) < 1e-30:
        return "0"
    return f"{x:.{digits}e}"


def format_spacing(spacing):
    """Format the spacing value."""
    try:
        val = float(spacing)
        return f"{val:.15f}"
    except:
        return str(spacing)[:60]


def dim_label(d):
    return {1: "1D", 2: "2D", 3: "3D"}.get(d, f"{d}D")


def dim_css(d):
    return {1: "dim-1d", 2: "dim-2d", 3: "dim-3d"}.get(d, "dim-1d")


def generate_lattice_page(name, data):
    """Generate a single lattice detail page."""
    dim, npts, suffix = parse_name(name)

    spacing_val = format_spacing(data.get('spacing', 'N/A'))
    degree = data.get('degree', 'N/A')
    max_layer = data.get('max_layer', 'N/A')
    num_points = data.get('num_points', 'N/A')

    # Get abscissas and weights
    abscissas = data.get('abscissas', [])
    abscissas_on = data.get('abscissas_on', np.array([]))
    weights = data.get('weights', np.array([]))

    # Build the points table
    active_points = []
    if len(abscissas_on) > 0 and len(weights) > 0:
        for i, ab in enumerate(abscissas):
            if i < len(abscissas_on):
                is_on = bool(abscissas_on[i]) if hasattr(abscissas_on, '__getitem__') else False
                w = weights[i] if i < len(weights) else 0.0
                if is_on and abs(w) > 1e-30:
                    active_points.append((ab, w))

    # Count total quadrature points (with symmetry)
    def count_symmetric(point):
        """Count number of symmetric copies of a point."""
        from itertools import permutations, product as iprod
        abs_pt = tuple(abs(x) for x in point)
        perms = set(permutations(abs_pt))
        count = 0
        for perm in perms:
            for signs in iprod([1, -1], repeat=len(perm)):
                sym_pt = tuple(p * s for p, s in zip(perm, signs))
                count += 1  # simplified; set would deduplicate
        # Actually let's just use the set approach
        all_pts = set()
        for perm in perms:
            for signs in iprod([1, -1], repeat=len(perm)):
                all_pts.add(tuple(p * s for p, s in zip(perm, signs)))
        return len(all_pts)

    md = []
    md.append(f"# {name}")
    md.append("")
    md.append(f'<span class="{dim_css(dim)} dim-badge">{dim_label(dim)}</span>')
    md.append("")
    md.append(f"**{dim_label(dim)} lattice with {num_points} quadrature points**")
    md.append("")

    # Properties table
    md.append("## Properties")
    md.append("")
    md.append("| Property | Value |")
    md.append("|:---------|:------|")
    md.append(f"| **Dimension** | {dim} |")
    md.append(f"| **Total points** | {num_points} |")
    md.append(f"| **Max layer** | {max_layer} |")
    md.append(f"| **Polynomial degree** | {degree} |")
    md.append(f"| **Lattice spacing** \\(c\\) | `{spacing_val}` |")
    md.append("")

    # Abscissa classes and weights
    if active_points:
        md.append("## Abscissa Classes & Weights")
        md.append("")
        md.append("Each row below is a *generator point* \\(\\boldsymbol{\\xi}_a\\) (in units of \\(c\\)).")
        md.append("The full set of quadrature nodes is obtained by applying all permutations and sign reflections.")
        md.append("")

        if dim == 1:
            md.append("| Index | \\(\\xi / c\\) | Weight \\(w\\) |")
            md.append("|:-----:|:----------:|:----------:|")
            for i, (ab, w) in enumerate(active_points):
                idx = ab[0] if isinstance(ab, (list, tuple)) else ab
                md.append(f"| {i} | {idx} | `{format_float(w)}` |")
        elif dim == 2:
            md.append("| Class | \\((\\xi_1, \\xi_2)/c\\) | Weight \\(w\\) |")
            md.append("|:-----:|:--------------------:|:----------:|")
            for i, (ab, w) in enumerate(active_points):
                pt_str = f"({ab[0]}, {ab[1]})"
                md.append(f"| {i} | {pt_str} | `{format_float(w)}` |")
        elif dim == 3:
            md.append("| Class | \\((\\xi_1, \\xi_2, \\xi_3)/c\\) | Weight \\(w\\) |")
            md.append("|:-----:|:----------------------------:|:----------:|")
            for i, (ab, w) in enumerate(active_points):
                pt_str = f"({ab[0]}, {ab[1]}, {ab[2]})"
                md.append(f"| {i} | {pt_str} | `{format_float(w)}` |")
        md.append("")

    # Quadrature rule
    md.append("## Quadrature Rule")
    md.append("")
    md.append("This lattice exactly integrates polynomials up to the given degree against the Gaussian weight:")
    md.append("")
    md.append("\\[")
    md.append(r"\int_{\mathbb{R}^d} f(\boldsymbol{\xi})\, \frac{e^{-|\boldsymbol{\xi}|^2/2}}{(2\pi)^{d/2}} \, d\boldsymbol{\xi} \;=\; \sum_{a} w_a \, f(c\,\boldsymbol{\xi}_a)")
    md.append("\\]")
    md.append("")
    md.append(f"where \\(d = {dim}\\) and \\(c = {spacing_val[:20]}\\ldots\\)")
    md.append("")

    # Navigation
    md.append("---")
    md.append("")
    md.append("[← Back to Catalog](../catalog.md)")
    md.append("")

    return "\n".join(md)


# Sort lattices
def sort_key(name):
    m = re.match(r'D(\d+)Q(\d+)([a-z]?)', name)
    if m:
        return (int(m.group(1)), int(m.group(2)), m.group(3))
    return (999, 999, name)

sorted_names = sorted(lattice.keys(), key=sort_key)

# Generate individual pages
for name in sorted_names:
    data = lattice[name]
    page_content = generate_lattice_page(name, data)
    with open(os.path.join(LATTICE_DIR, f"{name}.md"), 'w') as f:
        f.write(page_content)
    print(f"  Generated {name}.md")


# ─── Generate catalog.md ───

catalog = []
catalog.append("# Lattice Catalog")
catalog.append("")
catalog.append("A complete listing of all computed optimal Hermite lattice quadrature rules,")
catalog.append("organized by spatial dimension. Click any card to see full details.")
catalog.append("")

for dim_val, dim_name in [(1, "1D Lattices"), (2, "2D Lattices"), (3, "3D Lattices")]:
    names_in_dim = [n for n in sorted_names if parse_name(n)[0] == dim_val]
    if not names_in_dim:
        continue

    catalog.append(f"## {dim_name}")
    catalog.append("")

    # Summary table
    catalog.append("| Name | Points | Degree | Max Layer | Spacing \\(c\\) |")
    catalog.append("|:-----|:------:|:------:|:---------:|:------------|")
    for name in names_in_dim:
        d = lattice[name]
        sp = format_spacing(d.get('spacing', 'N/A'))[:12]
        catalog.append(f"| [{name}](lattices/{name}.md) | {d.get('num_points','?')} | {d.get('degree','?')} | {d.get('max_layer','?')} | `{sp}…` |")
    catalog.append("")

    # Cards
    catalog.append(f'<div class="lattice-grid">')
    for name in names_in_dim:
        d = lattice[name]
        dim, npts, suffix = parse_name(name)
        catalog.append(f'<div class="lattice-card">')
        catalog.append(f'<a href="lattices/{name}/">')
        catalog.append(f'<span class="{dim_css(dim)} dim-badge">{dim_label(dim)}</span>')
        catalog.append(f'<h3>{name}</h3>')
        catalog.append(f'<div class="meta">')
        catalog.append(f'{d.get("num_points","?")} points · degree {d.get("degree","?")}<br>')
        catalog.append(f'layer {d.get("max_layer","?")} · c ≈ {format_spacing(d.get("spacing","?"))[:8]}')
        catalog.append(f'</div>')
        catalog.append(f'</a>')
        catalog.append(f'</div>')
    catalog.append(f'</div>')
    catalog.append("")

with open(os.path.join(DOCS, 'catalog.md'), 'w') as f:
    f.write("\n".join(catalog))
print("Generated catalog.md")


# ─── Compute stats for home page ───
total = len(sorted_names)
dims = set(parse_name(n)[0] for n in sorted_names)
max_pts = max(lattice[n].get('num_points', 0) for n in sorted_names)
max_deg = max(lattice[n].get('degree', 0) for n in sorted_names)

print(f"\nStats: {total} lattices, dims={dims}, max_points={max_pts}, max_degree={max_deg}")
print("Done!")
