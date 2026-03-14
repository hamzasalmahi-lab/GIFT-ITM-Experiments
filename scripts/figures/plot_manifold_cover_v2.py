import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

ARTIFACTS_DIR = Path("artifacts")

# --- Configure for Publication-Quality, A4 Cover ---
fig_width_inch = 8.27
fig_height_inch = 11.69
DPI = 600


def generate_manifold_data(u_res=1500, v_res=200):
    u = np.linspace(-3 * np.pi, 3 * np.pi, u_res)
    v = np.linspace(-1, 1, v_res)
    U, V = np.meshgrid(u, v)

    # 1. Main Ribbon: World-Inference coordinates (H, S, R)
    amplitude_1 = 3 * np.sin(U / 1.5)
    f_mod_1     = np.exp(-V**2 / 0.5)
    gauss_env_1 = np.exp(-(U - np.pi)**2 / 8)
    sig_env_1   = 1 / (1 + np.exp(-(U + np.pi) * 2))

    # 2. Secondary Ribbon: Body-Inference / Temporal Sector (Phi_voi, T)
    amplitude_2 = 1.5 * np.cos(U * 2.5)
    f_mod_2     = np.exp(-(V - 0.2)**2 / 0.1)
    gauss_env_2 = np.exp(-(U + np.pi / 2)**2 / 12)
    sig_env_2   = 1 / (1 + np.exp((U - 2 * np.pi) * 1.5))

    phi = (1 + np.sqrt(5)) / 2  # Golden Ratio weighting

    y = (phi**2 * amplitude_1 * f_mod_1 * gauss_env_1 * sig_env_1) + \
        (amplitude_2 * f_mod_2 * gauss_env_2 * sig_env_2)

    return U, y, V


def generate_singularities(num_points=1200, seed=2026):
    rng = np.random.default_rng(seed)
    u_cluster = rng.normal(np.pi, 1.2, num_points)
    y_cluster = rng.normal(0.6, 0.4, num_points)
    alphas    = rng.uniform(0.01, 0.3, num_points)
    return u_cluster, y_cluster, alphas


def main():
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    output_path = ARTIFACTS_DIR / "GIFT-ITM_ManifoldCover_V2.png"

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(fig_width_inch, fig_height_inch),
                     dpi=DPI, facecolor="#000000")
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)

    # --- Manifold ribbons ---
    U, Y, V = generate_manifold_data()

    colors_cmap = [(0.8, 0.3, 0.0), (1.0, 0.7, 0.0), (1.0, 0.9, 0.2)]
    cmap_gold   = LinearSegmentedColormap.from_list("MetricGold", colors_cmap, N=200)

    ax.contourf(U, Y, V, cmap=cmap_gold, levels=120, alpha=0.9)
    ax.contour(U, Y, V, colors=["#D4AF37"], levels=120,
               linewidths=0.08, alpha=0.3)

    # --- HST Singularity glow ---
    u_sing, y_sing, alpha_sing = generate_singularities()

    cmap_sing  = plt.colormaps["YlOrBr"]           # no deprecation warning
    colors_sing = cmap_sing(np.linspace(0.4, 0.9, len(u_sing)))
    colors_sing[:, 3] = alpha_sing * 0.4

    ax.scatter(u_sing, y_sing, s=0.01, color=colors_sing,
               marker=".", zorder=10)

    # --- Viewport: top ~35 % left dark for title ---
    ax.set_xlim(-10, 10)
    ax.set_ylim(-1, 5)

    print(f"Rendering at {DPI} DPI — this may take a moment…")
    fig.savefig(output_path, facecolor=fig.get_facecolor(),
                edgecolor="none", bbox_inches="tight",
                pad_inches=0, transparent=False)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
