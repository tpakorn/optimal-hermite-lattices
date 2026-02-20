#!/usr/bin/env python3
"""Generate all MkDocs pages from lattice.dl data — v2 with fixes."""

import sys, os, re, json
import numpy as np
import dill as dl

lattice_path = os.path.join(os.path.dirname(__file__), '..', 'lattice.dl')
lattice = dl.load(open(lattice_path, 'rb'))
print(f"Loaded {len(lattice)} lattices: {list(lattice.keys())}")

DOCS = os.path.join(os.path.dirname(__file__), 'docs')
LATTICE_DIR = os.path.join(DOCS, 'lattices')
os.makedirs(LATTICE_DIR, exist_ok=True)


def parse_name(name):
    m = re.match(r'D(\d+)Q(\d+)([a-z]?)', name)
    if m:
        return int(m.group(1)), int(m.group(2)), m.group(3)
    return None, None, ''


def format_float(x, digits=10):
    if abs(x) < 1e-30:
        return "0"
    return f"{x:.{digits}e}"


def format_spacing(spacing):
    try:
        val = float(spacing)
        return f"{val:.15f}"
    except:
        return str(spacing)[:60]


def dim_label(d):
    return {1: "1D", 2: "2D", 3: "3D"}.get(d, f"{d}D")


def dim_css(d):
    return {1: "dim-1d", 2: "dim-2d", 3: "dim-3d"}.get(d, "dim-1d")


def sort_key(name):
    m = re.match(r'D(\d+)Q(\d+)([a-z]?)', name)
    if m:
        return (int(m.group(1)), int(m.group(2)), m.group(3))
    return (999, 999, name)


sorted_names = sorted(lattice.keys(), key=sort_key)

# ────────────────────────────────────────────────
# Generate individual lattice pages
# ────────────────────────────────────────────────
for name in sorted_names:
    data = lattice[name]
    dim, npts, suffix = parse_name(name)
    spacing_val = format_spacing(data.get('spacing', 'N/A'))
    degree = data.get('degree', 'N/A')
    max_layer = data.get('max_layer', 'N/A')
    num_points = data.get('num_points', 'N/A')

    abscissas = data.get('abscissas', [])
    abscissas_on = data.get('abscissas_on', np.array([]))
    weights = data.get('weights', np.array([]))

    active_points = []
    if len(abscissas_on) > 0 and len(weights) > 0:
        for i, ab in enumerate(abscissas):
            if i < len(abscissas_on):
                is_on = bool(abscissas_on[i]) if hasattr(abscissas_on, '__getitem__') else False
                w = weights[i] if i < len(weights) else 0.0
                if is_on and abs(w) > 1e-30:
                    active_points.append((ab, w))

    md = []
    md.append(f"# {name}")
    md.append("")
    md.append(f'<span class="{dim_css(dim)} dim-badge">{dim_label(dim)}</span>')
    md.append("")
    md.append(f"**{dim_label(dim)} lattice with {num_points} quadrature points**")
    md.append("")
    md.append("## Properties")
    md.append("")
    md.append("| Property | Value |")
    md.append("|:---------|:------|")
    md.append(f"| **Dimension** | {dim} |")
    md.append(f"| **Total points** | {num_points} |")
    md.append(f"| **Max layer** | {max_layer} |")
    md.append(f"| **Polynomial degree** | {degree} |")
    md.append(f"| **Lattice spacing** | `c = {spacing_val}` |")
    md.append("")

    if active_points:
        md.append("## Abscissa Classes & Weights")
        md.append("")
        md.append("Each row is a *generator point* (in units of the spacing *c*).")
        md.append("The full quadrature set is obtained by all permutations and sign reflections.")
        md.append("")

        if dim == 1:
            md.append("| Index | Generator | Weight |")
            md.append("|:-----:|:---------:|:------:|")
            for i, (ab, w) in enumerate(active_points):
                idx = ab[0] if isinstance(ab, (list, tuple)) else ab
                md.append(f"| {i} | {idx} | `{format_float(w)}` |")
        elif dim == 2:
            md.append("| Class | Generator | Weight |")
            md.append("|:-----:|:---------:|:------:|")
            for i, (ab, w) in enumerate(active_points):
                md.append(f"| {i} | ({ab[0]}, {ab[1]}) | `{format_float(w)}` |")
        elif dim == 3:
            md.append("| Class | Generator | Weight |")
            md.append("|:-----:|:---------:|:------:|")
            for i, (ab, w) in enumerate(active_points):
                md.append(f"| {i} | ({ab[0]}, {ab[1]}, {ab[2]}) | `{format_float(w)}` |")
        md.append("")

    md.append("## Quadrature Rule")
    md.append("")
    md.append("This lattice exactly integrates polynomials up to the given degree against the Gaussian weight:")
    md.append("")
    md.append("$$")
    md.append(r"\int_{\mathbb{R}^d} f(\boldsymbol{\xi})\, \frac{e^{-|\boldsymbol{\xi}|^2/2}}{(2\pi)^{d/2}} \, d\boldsymbol{\xi} = \sum_{a} w_a \, f(c\,\boldsymbol{\xi}_a)")
    md.append("$$")
    md.append("")
    md.append("---")
    md.append("")
    md.append("[Back to Catalog](../catalog.md)")

    with open(os.path.join(LATTICE_DIR, f"{name}.md"), 'w') as f:
        f.write("\n".join(md))
    print(f"  Generated {name}.md")


# ────────────────────────────────────────────────
# Generate catalog.md  (fix card links: ../lattices/NAME/)
# ────────────────────────────────────────────────
catalog = []
catalog.append("# Lattice Catalog")
catalog.append("")
catalog.append("Browse all computed optimal Hermite lattice quadrature rules. Click any entry to see full details.")
catalog.append("")

for dim_val, dim_name in [(1, "1D Lattices"), (2, "2D Lattices"), (3, "3D Lattices")]:
    names_in_dim = [n for n in sorted_names if parse_name(n)[0] == dim_val]
    if not names_in_dim:
        continue

    catalog.append(f"## {dim_name}")
    catalog.append("")
    catalog.append("| Name | Points | Degree | Max Layer | Spacing *c* |")
    catalog.append("|:-----|:------:|:------:|:---------:|:------------|")
    for name in names_in_dim:
        d = lattice[name]
        sp = format_spacing(d.get('spacing', 'N/A'))[:12]
        catalog.append(f"| [{name}](lattices/{name}.md) | {d.get('num_points','?')} | {d.get('degree','?')} | {d.get('max_layer','?')} | `{sp}…` |")
    catalog.append("")

    # Cards — use RELATIVE path from catalog page (which lives at catalog/index.html)
    catalog.append(f'<div class="lattice-grid">')
    for name in names_in_dim:
        d = lattice[name]
        dim, npts, suffix = parse_name(name)
        catalog.append(f'<div class="lattice-card">')
        catalog.append(f'<a href="../lattices/{name}/">')
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


# ────────────────────────────────────────────────
# Build JSON data for Plotly charts on index page
# ────────────────────────────────────────────────
chart_data = {}
for dim_val in [1, 2, 3]:
    entries = []
    for name in sorted_names:
        d_dim, _, _ = parse_name(name)
        if d_dim != dim_val:
            continue
        data = lattice[name]
        try:
            sp = float(data.get('spacing', 0))
        except:
            sp = 0
        entries.append({
            'name': name,
            'num_points': int(data.get('num_points', 0)),
            'degree': int(data.get('degree', 0)),
            'max_layer': int(data.get('max_layer', 0)),
            'spacing': round(sp, 8),
        })
    chart_data[f"D{dim_val}"] = entries

with open(os.path.join(DOCS, 'javascripts', 'lattice_data.json'), 'w') as f:
    json.dump(chart_data, f, indent=2)
print("Generated lattice_data.json for Plotly")


# ────────────────────────────────────────────────
# Build the summary table rows for index.md
# ────────────────────────────────────────────────
table_rows = []
for name in sorted_names:
    data = lattice[name]
    dim, _, _ = parse_name(name)
    sp = format_spacing(data.get('spacing', 'N/A'))[:10]
    table_rows.append(
        f"| [{name}](lattices/{name}.md) "
        f"| {dim_label(dim)} "
        f"| {data.get('num_points','?')} "
        f"| {data.get('degree','?')} "
        f"| {data.get('max_layer','?')} "
        f"| `{sp}…` |"
    )

summary_table = "\n".join(table_rows)
print(f"Built summary table with {len(table_rows)} rows")

# Write to a snippet file so we can embed it
with open(os.path.join(DOCS, '_summary_table.txt'), 'w') as f:
    f.write(summary_table)

print("\nDone! All pages regenerated.")
