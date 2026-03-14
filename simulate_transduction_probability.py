import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import sympy as sp
import matplotlib.pyplot as plt


def sigmoid(phi, gain, phi_c):
    return 1.0 / (1.0 + np.exp(-gain * (phi - phi_c)))


def run_simulation(
    n_iterations=10_000,
    n_phi_points=99,
    seed=42,
    viability_center=0.55,
    belief_noise=0.08,
    viability_noise=0.05,
):
    rng = np.random.default_rng(seed)
    phi_values = np.linspace(0.01, 0.99, n_phi_points)
    transduction_prob = np.zeros_like(phi_values)

    for index, phi in enumerate(phi_values):
        belief_state = stats.norm.rvs(
            loc=phi,
            scale=belief_noise,
            size=n_iterations,
            random_state=rng,
        )
        viability_threshold = stats.norm.rvs(
            loc=viability_center,
            scale=viability_noise,
            size=n_iterations,
            random_state=rng,
        )

        # Material Circularity condition:
        # Coupling occurs only when internal belief meets/exceeds metabolic viability.
        coupled = belief_state >= viability_threshold
        transduction_prob[index] = coupled.mean()

    return phi_values, transduction_prob


def fit_sigmoid(phi_values, probabilities):
    fit_params, _ = curve_fit(
        sigmoid,
        phi_values,
        probabilities,
        p0=(12.0, 0.5),
        bounds=([0.0, 0.0], [100.0, 1.0]),
        maxfev=20_000,
    )

    fitted = sigmoid(phi_values, *fit_params)
    residual = probabilities - fitted
    ss_res = np.sum(residual**2)
    ss_tot = np.sum((probabilities - np.mean(probabilities)) ** 2)
    r_squared = 1.0 - ss_res / ss_tot

    return fit_params, fitted, r_squared


def plot_results(phi_values, probabilities, fitted_curve, r_squared):
    plt.figure(figsize=(8, 5))
    plt.scatter(phi_values, probabilities, s=12, alpha=0.6, label="Monte Carlo")
    plt.plot(phi_values, fitted_curve, color="crimson", linewidth=2, label="Sigmoid fit")
    plt.xlabel("Phi")
    plt.ylabel("Transduction Probability")
    plt.title(f"Stochastic Transduction with Material Circularity (R^2={r_squared:.4f})")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("transduction_probability_fit.png", dpi=150)
    print("Saved plot: transduction_probability_fit.png")

    if "agg" not in plt.get_backend().lower():
        plt.show()


def main():
    phi_values, probabilities = run_simulation()
    fit_params, fitted_curve, r_squared = fit_sigmoid(phi_values, probabilities)

    gain_hat, phi_c_hat = fit_params
    print(f"Sigmoid fit parameters: gain={gain_hat:.6f}, phi_c={phi_c_hat:.6f}")
    print(f"Goodness of fit (R^2): {r_squared:.6f}")

    fit_threshold = 0.98
    if r_squared >= fit_threshold:
        Phi, gain, Phi_c = sp.symbols("Phi gain Phi_c", real=True)
        T_AA = 1 / (1 + sp.exp(-gain * (Phi - Phi_c)))

        print("\nSigmoid model accepted. Symbolic transduction map:")
        print(sp.Eq(sp.Symbol("T_AA"), T_AA))
        print("Estimated symbolic parameters:")
        print(f"  gain -> {gain_hat:.6f}")
        print(f"  Phi_c -> {phi_c_hat:.6f}")
    else:
        print("\nSigmoid fit not sufficient; symbolic T_AA parameters not reported.")

    plot_results(phi_values, probabilities, fitted_curve, r_squared)


if __name__ == "__main__":
    main()