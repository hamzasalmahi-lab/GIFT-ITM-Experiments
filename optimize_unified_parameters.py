import numpy as np
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt
from pathlib import Path


PHI_0 = 2.0 / 3.0
ARTIFACTS_DIR = Path("artifacts")


def Phi_th_IFE(L_bio, kappa, Lambda, Phi_0=PHI_0):
    return Phi_0 + (kappa * L_bio) / (2.0 * Lambda)


def Phi_th_ODE(Phi_target):
    return Phi_target / 2.0


def Phi_th_A2(phi_th_a2):
    return phi_th_a2


def mismatch_objective(params):
    L_bio, kappa, Lambda, Phi_target, phi_th_a2 = params

    phi_ife = Phi_th_IFE(L_bio, kappa, Lambda)
    phi_ode = Phi_th_ODE(Phi_target)
    phi_a2 = Phi_th_A2(phi_th_a2)

    return (
        (phi_ife - phi_ode) ** 2
        + (phi_ife - phi_a2) ** 2
        + (phi_ode - phi_a2) ** 2
    )


def optimize_unified_parameters():
    bounds = [
        (0.0, 2.0),
        (0.0, 5.0),
        (1e-3, 5.0),
        (1e-6, 1.0 - 1e-6),
        (0.0, 1.0),
    ]

    return differential_evolution(
        mismatch_objective,
        bounds=bounds,
        seed=42,
        polish=True,
        tol=1e-8,
        maxiter=300,
    )


def plot_incoherence_gap(kappa, Lambda, Phi_target):
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    output_path = ARTIFACTS_DIR / "incoherence_gap.png"

    L_values = np.linspace(0.0, 2.0, 120)
    phi_ode = Phi_th_ODE(Phi_target)
    phi_ife_values = Phi_th_IFE(L_values, kappa, Lambda)
    gap_values = np.abs(phi_ife_values - phi_ode)

    plt.figure(figsize=(8, 5))
    plt.plot(L_values, gap_values, linewidth=2)
    plt.title("Incoherence Gap vs Biological Stress")
    plt.xlabel("L_bio")
    plt.ylabel("Incoherence Gap")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Saved plot: {output_path}")

    if "agg" not in plt.get_backend().lower():
        plt.show()


def main():
    result = optimize_unified_parameters()
    tolerance = 1e-6

    L_bio, kappa, Lambda, Phi_target, phi_th_a2 = result.x
    phi_ife = Phi_th_IFE(L_bio, kappa, Lambda)
    phi_ode = Phi_th_ODE(Phi_target)
    phi_a2 = Phi_th_A2(phi_th_a2)

    print("Optimization status:", result.message)
    print(f"Phi_0 fixed at: {PHI_0}")
    print(f"Best mismatch: {result.fun:.6e}")
    print("Best parameters:")
    print(f"  L_bio     = {L_bio:.6f}")
    print(f"  kappa     = {kappa:.6f}")
    print(f"  Lambda    = {Lambda:.6f}")
    print(f"  Phi_target= {Phi_target:.6f}")
    print(f"  Phi_th_A2 = {phi_th_a2:.6f}")
    print("Threshold values:")
    print(f"  Phi_th_IFE = {phi_ife:.6f}")
    print(f"  Phi_th_ODE = {phi_ode:.6f}")
    print(f"  Phi_th_A2  = {phi_a2:.6f}")

    if result.fun <= tolerance:
        print("\nCoherent unified solution found within tolerance.")
    else:
        print("\nNo coherent unified solution found within tolerance.")
        print("Generating Incoherence Gap plot as a function of L_bio...")
        plot_incoherence_gap(kappa, Lambda, Phi_target)


if __name__ == "__main__":
    main()