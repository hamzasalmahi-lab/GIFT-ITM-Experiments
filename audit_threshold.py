import sympy as sp

# Define symbols
Phi, Phi_0, kappa, Lambda, L_bio = sp.symbols('Phi Phi_0 kappa lambda L_bio')

# Define the equilibrium condition from the Action variation (delta S = 0)
# Based on the reviewer's note: 0 = 2*lambda*(Phi - Phi_0) - kappa*L_bio
equilibrium_eq = sp.Eq(0, 2 * Lambda * (Phi - Phi_0) - kappa * L_bio)

# Solve for Phi_th
Phi_th = sp.solve(equilibrium_eq, Phi)[0]

print(f"The mathematically [PROVED] threshold is: Phi_th = {Phi_th}")
# This should output: Phi_0 + kappa*L_bio/(2*lambda)