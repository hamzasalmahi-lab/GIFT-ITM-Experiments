from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


ARTIFACTS_DIR = Path("artifacts")


def panel_1_ou_potential(ax, alpha=8.0, phi_0=2.0 / 3.0):
    phi = np.linspace(0.1, 0.95, 500)
    potential = 0.5 * alpha * (phi - phi_0) ** 2

    ax.plot(phi, potential, color="#1f77b4", linewidth=2.2)
    ax.axvline(phi_0, linestyle="--", color="black", linewidth=1.2, alpha=0.8)
    ax.set_title("Panel 1: OU Potential Well")
    ax.set_xlabel(r"$\Phi_{voi}$")
    ax.set_ylabel(r"$V(\Phi_{voi})$")
    ax.grid(alpha=0.25)

    ax.annotate(
        r"Kramers MFPT: $\tau_{esc} \propto \exp(\Delta V / D)$",
        xy=(phi_0 + 0.06, 0.5 * alpha * (0.06**2)),
        xytext=(0.18, 0.88),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "lw": 1.1},
        fontsize=10,
        ha="left",
        va="top",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "alpha": 0.8},
    )


def panel_2_saddle_node(ax, alpha=8.0, phi_target=0.8, beta_tilde=1.0):
    z_sn = alpha * (phi_target**2) / (4.0 * beta_tilde)
    z_values = np.linspace(0.0, z_sn * 0.999, 260)

    discriminant = np.maximum(phi_target**2 - 4.0 * (beta_tilde / alpha) * z_values, 0.0)
    lower_branch = 0.5 * (phi_target - np.sqrt(discriminant))
    upper_branch = 0.5 * (phi_target + np.sqrt(discriminant))

    z_smooth = np.linspace(z_values.min(), z_values.max(), 600)
    lower_interp = interp1d(z_values, lower_branch, kind="cubic")
    upper_interp = interp1d(z_values, upper_branch, kind="cubic")
    lower_smooth = lower_interp(z_smooth)
    upper_smooth = upper_interp(z_smooth)

    phi_sn = phi_target / 2.0

    ax.plot(z_smooth, upper_smooth, color="#2ca02c", linewidth=2.2, label="Upper stable branch")
    ax.plot(
        z_smooth,
        lower_smooth,
        color="#d62728",
        linewidth=2.0,
        linestyle="--",
        label="Lower unstable branch",
    )
    ax.scatter([z_sn], [phi_sn], color="black", s=40, zorder=4)
    ax.annotate(
        rf"Saddle-node\n$\Phi_{{sn}}=\Phi_{{target}}/2={phi_sn:.2f}$",
        xy=(z_sn, phi_sn),
        xytext=(0.48, 0.18),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "lw": 1.1},
        fontsize=9,
        ha="left",
    )

    ax.set_title("Panel 2: Saddle-Node Bifurcation")
    ax.set_xlabel(r"$z$ (control parameter $\mu$)")
    ax.set_ylabel(r"$\Phi_{voi}$")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", fontsize=8)


def panel_3_phase_plane(ax):
    phi_vals = np.linspace(0.1, 0.95, 36)
    rho_vals = np.linspace(0.0, 1.0, 36)
    phi_grid, rho_grid = np.meshgrid(phi_vals, rho_vals)

    phi_dpdr = 0.30
    phi_high = 0.80
    barrier = 0.56
    coupling = 0.45

    double_well_gradient = (
        2.0 * (phi_grid - phi_dpdr) * (phi_grid - phi_high) ** 2
        + 2.0 * (phi_grid - phi_high) * (phi_grid - phi_dpdr) ** 2
    )
    dphi = -double_well_gradient - coupling * (rho_grid - 0.5) - 0.2 * (phi_grid - barrier)

    rho_target = 1.0 / (1.0 + np.exp(-(phi_grid - 0.62) / 0.04))
    drho = 2.0 * (rho_target - rho_grid)

    speed = np.hypot(dphi, drho)
    dphi_norm = dphi / (speed + 1e-9)
    drho_norm = drho / (speed + 1e-9)

    ax.streamplot(
        phi_grid,
        rho_grid,
        dphi_norm,
        drho_norm,
        density=1.0,
        color=speed,
        cmap="viridis",
        linewidth=1.1,
        arrowsize=1.0,
    )

    ax.scatter([phi_high], [0.88], s=65, color="#2ca02c", zorder=5, label="Integrated attractor")
    ax.scatter([phi_dpdr], [0.12], s=65, color="#9467bd", zorder=5, label="DPDR decoupled state")
    ax.set_title("Panel 3: Phase Plane (schematic)")
    ax.set_xlabel(r"$\Phi_{voi}$")
    ax.set_ylabel(r"$\rho_{tA}$")
    ax.set_xlim(0.1, 0.95)
    ax.set_ylim(0.0, 1.0)
    ax.legend(loc="lower right", fontsize=8)


def make_figure():
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

    panel_1_ou_potential(axes[0])
    panel_2_saddle_node(axes[1])
    panel_3_phase_plane(axes[2])

    fig.suptitle("Figure 3: The HST Metastability Landscape", fontsize=14)
    plt.tight_layout()
    return fig


def main():
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    output_path = ARTIFACTS_DIR / "figure3_hst_metastability_landscape.png"

    fig = make_figure()
    fig.savefig(output_path, dpi=220)
    print(f"Saved figure: {output_path}")

    if "agg" not in plt.get_backend().lower():
        plt.show()


if __name__ == "__main__":
    main()