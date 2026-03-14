from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ARTIFACTS_DIR = Path("artifacts")


def alpha_sq(phi, phi_0, kappa, lambda_val):
    numerator = lambda_val * (phi_0 * kappa - 3.0 * kappa * phi - 2.0)
    denominator = kappa * (phi - phi_0)

    with np.errstate(divide="ignore", invalid="ignore"):
        values = numerator / denominator

    values[np.isclose(phi, phi_0, atol=1e-12)] = np.nan
    return values


def make_figure(phi_min=-0.6, phi_max=1.0, n_points=2000):
    phi_0 = 2.0 / 3.0
    kappa = 1.0
    lambda_val = (3.0**7) / 16.0

    phi = np.linspace(phi_min, phi_max, n_points)
    alpha_sq_values = alpha_sq(phi, phi_0, kappa, lambda_val)

    fig, ax = plt.subplots(figsize=(10, 5.8))

    valid_left = -0.44
    valid_right = phi_0
    ax.axvspan(
        valid_left,
        valid_right,
        color="#d4edda",
        alpha=0.45,
        label="Valid Domain (DPDR onset dynamics)",
    )
    ax.axvspan(
        phi_0,
        phi_max,
        color="#f8d7da",
        alpha=0.35,
        label="Complex-valued region (Recovery dynamics)",
    )

    ax.plot(phi, alpha_sq_values, color="#1f77b4", linewidth=2.0, label=r"$\alpha^2(\Phi)$")

    ax.axvline(phi_0, color="black", linestyle="--", linewidth=1.4, alpha=0.9)
    ax.annotate(
        r"Vertical asymptote at $\Phi=\Phi_0=2/3$",
        xy=(phi_0, 3200),
        xytext=(0.46, 0.93),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "lw": 1.1},
        fontsize=10,
        ha="left",
        va="top",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "alpha": 0.85},
    )

    ax.text(
        0.16,
        0.15,
        r"Approx. valid interval: $\Phi\in(-0.44,0.667)$",
        transform=ax.transAxes,
        fontsize=9.5,
        color="#155724",
        bbox={"boxstyle": "round,pad=0.22", "facecolor": "white", "alpha": 0.85},
    )

    ax.set_xlim(phi_min, phi_max)
    ax.set_ylim(-5000, 5000)
    ax.set_xlabel("Coupling Precision (Phi)")
    ax.set_ylabel("Restoring Force Squared (alpha^2)")
    ax.set_title(r"Figure 5: The $\alpha(\Phi)$ Domain Map")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper left", fontsize=9)

    plt.tight_layout()
    return fig


def main():
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    output_path = ARTIFACTS_DIR / "figure5_alpha_domain_map.png"

    fig = make_figure()
    fig.savefig(output_path, dpi=220)
    print(f"Saved figure: {output_path}")

    if "agg" not in plt.get_backend().lower():
        plt.show()


if __name__ == "__main__":
    main()