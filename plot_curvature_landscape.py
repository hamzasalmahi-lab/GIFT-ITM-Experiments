from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm


ARTIFACTS_DIR = Path("artifacts")


def ricci_2d(phi_voi):
    return (3.0 * phi_voi - 2.0) / (2.0 * (phi_voi**2) * ((1.0 - phi_voi) ** 4))


def make_figure(phi_min=0.1, phi_max=0.95, n_phi=800, n_h=120):
    phi_values = np.linspace(phi_min, phi_max, n_phi)
    curvature = ricci_2d(phi_values)

    h_values = np.linspace(0.0, 1.0, n_h)
    _, _ = np.meshgrid(phi_values, h_values)
    curvature_landscape = np.tile(curvature, (n_h, 1))

    # Robust symmetric bounds keep both negative and positive regions visible
    # despite the divergence as Phi_voi -> 1.
    color_limit = np.percentile(np.abs(curvature), 98)
    norm = TwoSlopeNorm(vmin=-color_limit, vcenter=0.0, vmax=color_limit)

    fig, ax = plt.subplots(figsize=(10, 5))
    mesh = ax.pcolormesh(
        phi_values,
        h_values,
        curvature_landscape,
        shading="auto",
        cmap="RdBu_r",
        norm=norm,
    )

    phi_dpdr_boundary = 0.40
    phi_zero = 2.0 / 3.0

    ax.axvline(
        phi_dpdr_boundary,
        color="black",
        linestyle="--",
        linewidth=1.5,
        alpha=0.9,
    )
    ax.axvline(
        phi_zero,
        color="darkgreen",
        linestyle="-",
        linewidth=2.0,
        alpha=0.95,
    )

    ax.text(
        0.18,
        0.93,
        "DPDR regime\n$\\Phi_{voi} < 0.40$",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.75},
    )
    ax.annotate(
        "Allostatic Reference\n(Zero-crossing)\n$\\Phi_0 = 2/3$",
        xy=(phi_zero, 0.55),
        xytext=(0.56, 0.95),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "lw": 1.2, "color": "darkgreen"},
        ha="center",
        va="top",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.8},
    )
    ax.text(
        0.83,
        0.93,
        "Hyperarousal\n$\\Phi_{voi} > 2/3$",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.75},
    )

    ax.set_xlim(phi_min, phi_max)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel(r"$\Phi_{voi}$")
    ax.set_ylabel("H")
    ax.set_title(r"Figure 1: The $(\Phi_{voi}, H)$ Curvature Landscape")

    cbar = fig.colorbar(mesh, ax=ax, pad=0.02)
    cbar.set_label(r"$\mathcal{R}_{2D}(\Phi_{voi})$")

    plt.tight_layout()
    return fig


def main():
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    output_path = ARTIFACTS_DIR / "figure1_curvature_landscape.png"

    fig = make_figure()
    fig.savefig(output_path, dpi=200)
    print(f"Saved figure: {output_path}")

    if "agg" not in plt.get_backend().lower():
        plt.show()


if __name__ == "__main__":
    main()