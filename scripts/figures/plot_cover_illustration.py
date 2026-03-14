"""
Cover Illustration — GIFT-ITM Physics Journal
==============================================
A4 portrait (8.27 × 11.69 in) at 600 DPI.

Elements
--------
* 50 translucent Ricci Curvature Manifold ribbons using
  y = sin(x)*exp(-x/5) + Gaussian topological warps.
* HST Singularity: multi-layer golden glow cluster with
  neural-network connection edges.
* Fisher Information Metric: ultra-thin golden lines (alpha≈0.3)
  radiating from the singularity, plus perpendicular tick-marks
  on every 5th ribbon.
* Top 30 % of the canvas is kept dark/empty for title placement.
"""

from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection


ARTIFACTS_DIR = Path("artifacts")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _gaussian_warp(x, rng, n_warps):
    """Sum of random Gaussian bumps along the x-axis."""
    warp = np.zeros_like(x)
    for _ in range(n_warps):
        wc = rng.uniform(x[0] + 0.8, x[-1] - 0.8)
        wa = rng.uniform(-0.14, 0.14)
        ww = rng.uniform(0.5, 2.5)
        warp += wa * np.exp(-((x - wc) ** 2) / (2.0 * ww ** 2))
    return warp


def _gold_rgba(alpha):
    return mcolors.to_rgba("#FFD700", float(alpha))


# ---------------------------------------------------------------------------
# Panel builders
# ---------------------------------------------------------------------------

def _draw_background_stars(ax, rng, x_min, x_max, y_min, y_max):
    n = 300
    ax.scatter(
        rng.uniform(x_min, x_max, n),
        rng.uniform(y_min, y_max, n),
        c="white",
        s=rng.uniform(0.04, 0.9, n),
        alpha=0.22,
        linewidths=0,
        rasterized=True,
        zorder=1,
    )


def _draw_ribbons(ax, rng, x, y_min, y_top_content, n_ribbons=50):
    """
    Plot 50 translucent ribbon curves that form the Ricci Curvature Landscape.
    Each ribbon uses:
        y_base = A * sin(x + phase) * exp(-x / 5)   +   Gaussian warp(s)
    stacked vertically within the content zone.
    """
    cmap = plt.colormaps["cool"]
    ribbon_ys = []

    spacing = (y_top_content - y_min - 0.45) / max(n_ribbons - 1, 1)

    for i in range(n_ribbons):
        t = i / (n_ribbons - 1)

        center_y = y_min + 0.25 + i * spacing

        # Base curve: exact formula structure from spec
        amp   = 0.20 + 0.18 * np.sin(t * np.pi)
        phase = t * 0.80
        y_base = amp * np.sin(x + phase) * np.exp(-x / 5.0)

        # Gaussian topological warp (1–3 lobes per ribbon)
        y_base += _gaussian_warp(x, rng, rng.integers(1, 4))

        y_curve = y_base + center_y
        ribbon_ys.append(y_curve)

        color  = cmap(t)
        alpha  = 0.10 + 0.22 * t
        lw     = 0.30 + 0.45 * t

        # Soft glow pass (thick, low-alpha)
        ax.plot(x, y_curve, color=color, alpha=alpha * 0.30,
                linewidth=lw * 4.5, solid_capstyle="round",
                rasterized=True, zorder=2)
        # Sharp ribbon pass
        ax.plot(x, y_curve, color=color, alpha=alpha,
                linewidth=lw, solid_capstyle="round",
                rasterized=True, zorder=2)

    return ribbon_ys


def _draw_hst_singularity(ax, rng, cx, cy):
    """
    Multi-layer golden scatter glow representing the Homeostatic
    Servo-Transducer, with neural-network connectivity edges.
    """
    cmap_glow = plt.colormaps["YlOrBr"]

    # Glow tiers: outer → inner  (n_pts, spread, alpha, max_size)
    tiers = [
        (700, 1.70, 0.05, 14),
        (600, 1.05, 0.09, 20),
        (500, 0.58, 0.17, 28),
        (380, 0.30, 0.28, 38),
        (240, 0.13, 0.50, 50),
        (110, 0.05, 0.78, 60),
    ]
    for n_pts, spread, alpha, smax in tiers:
        px = rng.normal(cx, spread,        n_pts)
        py = rng.normal(cy, spread * 0.82, n_pts)
        dist = np.hypot((px - cx) / (spread + 1e-9),
                        (py - cy) / (spread * 0.82 + 1e-9))
        c_vals = np.clip(1.0 - 0.80 * dist / (dist.max() + 1e-9), 0.0, 1.0)
        s_vals = np.clip(smax * np.exp(-dist * 1.3), 0.2, smax)
        ax.scatter(px, py,
                   c=cmap_glow(c_vals), s=s_vals,
                   alpha=alpha, linewidths=0,
                   rasterized=True, zorder=5)

    # Neural-network node mesh
    n_nodes = 30
    node_r = rng.uniform(0.08, 0.72, n_nodes)
    node_a = rng.uniform(0.0, 2.0 * np.pi, n_nodes)
    nx_arr = cx + node_r * np.cos(node_a)
    ny_arr = cy + node_r * 0.78 * np.sin(node_a)

    edge_segs, edge_colors = [], []
    for j in range(n_nodes):
        for k in range(j + 1, n_nodes):
            d = np.hypot(nx_arr[j] - nx_arr[k], ny_arr[j] - ny_arr[k])
            if d < 0.54:
                edge_segs.append(
                    [[nx_arr[j], ny_arr[j]], [nx_arr[k], ny_arr[k]]])
                edge_colors.append(_gold_rgba(0.16))

    ax.add_collection(LineCollection(
        edge_segs, colors=edge_colors, linewidths=0.28,
        rasterized=True, zorder=5))

    # Bright core point
    ax.scatter([cx], [cy], c="white", s=55, alpha=0.98,
               linewidths=0, zorder=7)

    # Orbital halos (elliptic rings)
    theta = np.linspace(0.0, 2.0 * np.pi, 500)
    for r_ratio, oa, olw, ols in [
        (0.85, 0.09, 0.40, "--"),
        (1.12, 0.05, 0.30, ":"),
    ]:
        ax.plot(cx + r_ratio * np.cos(theta),
                cy + r_ratio * 0.64 * np.sin(theta),
                color="#FFD700", alpha=oa, linewidth=olw,
                linestyle=ols, rasterized=True, zorder=5)

    # Four swept arcs — "light cone" emanating outward
    for sweep_angle in np.linspace(0, np.pi * 2, 5)[:-1]:
        t_arc = np.linspace(0, 1, 200)
        arc_r = 0.9 + t_arc * 2.2
        arc_a = sweep_angle + t_arc * 0.45
        arc_fade = np.exp(-t_arc * 3.0) * 0.22
        ax.plot(cx + arc_r * np.cos(arc_a),
                cy + arc_r * 0.70 * np.sin(arc_a),
                color="#FFD700", alpha=0.18, linewidth=0.30,
                rasterized=True, zorder=4)
        _ = arc_fade  # kept for reference; per-segment fade not applied in line


def _draw_fisher_lines(ax, rng, cx, cy, ribbon_ys, x):
    """
    Fisher Information Metric g_{ab} visualised as:
      (a) A starburst of fading gold rays from the HST singularity.
      (b) Perpendicular tick-marks along every 5th ribbon.
    Both rendered as a single LineCollection each for efficiency.
    """
    # --- (a) Radial starburst ---
    n_fisher = 240
    f_segs, f_colors = [], []
    for _ in range(n_fisher):
        angle  = rng.uniform(0.0, 2.0 * np.pi)
        length = rng.uniform(0.3, 3.8)
        n_seg  = 55
        tt     = np.linspace(0.0, 1.0, n_seg)
        fade   = np.exp(-tt * 3.0)
        lx = cx + tt * length * np.cos(angle)
        ly = cy + tt * length * np.sin(angle) * 0.84
        for j in range(n_seg - 1):
            f_segs.append([[lx[j], ly[j]], [lx[j + 1], ly[j + 1]]])
            f_colors.append(_gold_rgba(float(fade[j]) * 0.28))

    ax.add_collection(LineCollection(
        f_segs, colors=f_colors, linewidths=0.28,
        rasterized=True, zorder=4))

    # --- (b) Perpendicular metric ticks on ribbons ---
    tick_segs, tick_colors = [], []
    stride = 22
    tick_len = 0.09
    for i in range(0, len(ribbon_ys), 5):
        y_c = ribbon_ys[i]
        for j in range(0, len(x) - stride, stride * 5):
            if j + stride >= len(x):
                continue
            dx_t = x[j + stride] - x[j]
            dy_t = y_c[j + stride] - y_c[j]
            mag  = np.hypot(dx_t, dy_t) + 1e-9
            px_t = -dy_t / mag * tick_len
            py_t =  dx_t / mag * tick_len
            tick_segs.append(
                [[x[j] - px_t, y_c[j] - py_t],
                 [x[j] + px_t, y_c[j] + py_t]])
            tick_colors.append(_gold_rgba(0.30))

    ax.add_collection(LineCollection(
        tick_segs, colors=tick_colors, linewidths=0.32,
        rasterized=True, zorder=4))


# ---------------------------------------------------------------------------
# Main figure assembly
# ---------------------------------------------------------------------------

def make_figure():
    fig_w, fig_h = 8.27, 11.69           # A4 portrait, inches
    rng = np.random.default_rng(2026)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor("#0A0A0A")
    ax.set_facecolor("#0A0A0A")

    # Coordinate frame
    x_min, x_max = -np.pi * 0.65, np.pi * 3.05
    y_min, y_max = -3.0, 3.0
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Top 30 % reserved → content ceiling at 70 % of total y-range
    y_top_content = y_min + 0.70 * (y_max - y_min)   # ≈ 1.20

    x = np.linspace(x_min, x_max, 1200)

    # Layer order: stars → ribbons → Fisher lines / ticks → HST glow
    _draw_background_stars(ax, rng, x_min, x_max, y_min, y_max)

    ribbon_ys = _draw_ribbons(ax, rng, x, y_min, y_top_content, n_ribbons=50)

    # HST singularity: centre-right of content zone
    cx = x_min + 0.64 * (x_max - x_min)
    cy = y_min + 0.34 * (y_top_content - y_min)

    _draw_fisher_lines(ax, rng, cx, cy, ribbon_ys, x)
    _draw_hst_singularity(ax, rng, cx, cy)

    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    return fig


def main():
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    output_path = ARTIFACTS_DIR / "cover_illustration.png"

    print("Rendering cover illustration at 600 DPI (this may take a moment)…")
    fig = make_figure()
    fig.savefig(output_path, dpi=600, bbox_inches="tight", pad_inches=0,
                facecolor="#0A0A0A", edgecolor="none")
    plt.close(fig)
    print(f"Saved: {output_path}")

    if "agg" not in plt.get_backend().lower():
        plt.show()


if __name__ == "__main__":
    main()
