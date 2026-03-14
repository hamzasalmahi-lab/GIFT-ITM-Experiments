from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ARTIFACTS_DIR = Path("artifacts")


def modified_ife_2(phi_voi, phi_0, lambda_val, kappa, l_bio):
    return 2.0 * lambda_val * (phi_voi - phi_0) - kappa * l_bio


def effective_threshold(phi_0, lambda_val, kappa, l_bio):
    return phi_0 + (kappa * l_bio) / (2.0 * lambda_val)


def make_figure(phi_min=0.1, phi_max=0.95, n_points=800):
    phi_voi = np.linspace(phi_min, phi_max, n_points)

    phi_0 = 2.0 / 3.0
    kappa = 1.0
    lambda_val = (3.0**7) / 16.0
    l_bio_values = [0.0, 500.0, 1000.0]

    fig, ax = plt.subplots(figsize=(10, 5.5))

    curve_colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    threshold_markers = ["o", "s", "^"]

    for l_bio, color, marker in zip(l_bio_values, curve_colors, threshold_markers):
        r_values = modified_ife_2(phi_voi, phi_0, lambda_val, kappa, l_bio)
        phi_th = effective_threshold(phi_0, lambda_val, kappa, l_bio)

        ax.plot(
            phi_voi,
            r_values,
            color=color,
            linewidth=2.0,
            label=rf"$L_{{bio}}={int(l_bio)}$",
        )

        if phi_min <= phi_th <= phi_max:
            ax.scatter(
                [phi_th],
                [0.0],
                color=color,
                marker=marker,
                s=70,
                zorder=4,
                edgecolors="black",
                linewidths=0.5,
            )
            ax.annotate(
                rf"$\Phi_{{th}}={phi_th:.3f}$",
                xy=(phi_th, 0.0),
                xytext=(6, 10),
                textcoords="offset points",
                fontsize=9,
                color=color,
                ha="left",
            )

    ax.axhline(0.0, color="black", linestyle="--", linewidth=1.2, alpha=0.85, label="R = 0")

    # Shade one representative DPDR-vulnerable zone (R < 0) for the highest load case.
    l_bio_ref = max(l_bio_values)
    r_ref = modified_ife_2(phi_voi, phi_0, lambda_val, kappa, l_bio_ref)
    ax.fill_between(
        phi_voi,
        r_ref,
        0.0,
        where=(r_ref < 0.0),
        color="gray",
        alpha=0.12,
        label=rf"DPDR-vulnerable zone ($L_{{bio}}={int(l_bio_ref)}$)",
    )

    ax.set_xlim(phi_min, phi_max)
    ax.set_xlabel(r"$\Phi_{voi}$")
    ax.set_ylabel(r"$\mathcal{R}$")
    ax.set_title("Figure 2: The Modified Tuning Curve")
    ax.grid(alpha=0.25)
    ax.legend(loc="best", frameon=True)

    plt.tight_layout()
    return fig


def main():
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    output_path = ARTIFACTS_DIR / "figure2_modified_tuning_curve.png"

    fig = make_figure()
    fig.savefig(output_path, dpi=200)
    print(f"Saved figure: {output_path}")

    if "agg" not in plt.get_backend().lower():
        plt.show()


if __name__ == "__main__":
    main()