import sympy as sp


def run_slow_manifold_derivation():
    # 1. Setup Symbols
    t = sp.symbols('t', real=True)
    kappa, lam, Phi_0 = sp.symbols('kappa lambda Phi_0', positive=True)
    Phi = sp.Function('Phi')(t)

    # 2. Define the Field Equation (from your previous derivation)
    # We use the EL equation: (1 + kappa*Phi)*ddot(Phi) + G(Phi, dot(Phi)) = 0
    # Let's define the 2nd order term G based on your EL result:
    Phi_dot = sp.diff(Phi, t)
    Phi_ddot = sp.diff(Phi, t, 2)

    # From your ddot(Phi) result in Mission 3:
    numerator = (-Phi_0**2*kappa*lam + 4*Phi_0*kappa*lam*Phi - 3*kappa*lam*Phi**2 + 2*Phi_0*lam - 2*lam*Phi - kappa*Phi_dot**2)
    denominator = 2*(kappa*Phi + 1)

    field_eq = sp.Eq(Phi_ddot, numerator / denominator)

    print("--- STEP 1: Full 2nd-Order Field Equation ---")
    sp.pprint(field_eq)

    # 3. Apply Slow-Manifold Assumption (Adiabatic Approximation)
    # We assume the system is "overdamped" by biological impedance.
    # On the slow manifold, acceleration (ddot) is negligible compared to velocity (dot).
    # We set Phi_ddot approx 0 to find the 'Equilibrium Velocity'
    slow_manifold_condition = sp.solve(sp.Eq(0, numerator / denominator), Phi_dot**2)

    print("\n--- STEP 2: Slow-Manifold Velocity Squared (Phi_dot^2) ---")
    v_sq = sp.simplify(slow_manifold_condition[0])
    sp.pprint(v_sq)

    # 4. Extract alpha(Phi)
    # If dot(Phi) = -alpha * (Phi - Phi_0), then alpha^2 = v_sq / (Phi - Phi_0)^2
    alpha_sq = sp.simplify(v_sq / (Phi - Phi_0)**2)

    print("\n--- STEP 3: Derived State-Dependent Restoring Force (alpha^2) ---")
    sp.pprint(alpha_sq)

    # 5. Taylor Expansion near Phi_0
    # To see the 'Linear ODE' constant, we expand alpha near Phi_0
    phi = sp.symbols('phi', real=True)
    alpha_sq_scalar = sp.simplify(alpha_sq.subs(Phi, phi))
    alpha_near_eq = alpha_sq_scalar.series(phi, Phi_0, 1).removeO()

    print("\n--- STEP 4: Effective Alpha at Equilibrium (Phi -> Phi_0) ---")
    sp.pprint(sp.simplify(alpha_near_eq))


if __name__ == "__main__":
    run_slow_manifold_derivation()