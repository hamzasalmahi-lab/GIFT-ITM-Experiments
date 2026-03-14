import sympy as sp


def main():
    t = sp.symbols("t", real=True)
    kappa, Lambda, Phi_0 = sp.symbols("kappa lambda Phi_0", positive=True)

    Phi = sp.Function("Phi")(t)
    Phi_dot = sp.diff(Phi, t)
    Phi_ddot = sp.diff(Phi, t, 2)

    R = sp.symbols("R", real=True)

    # Biological Lagrangian as a harmonic oscillator in belief/transduction space.
    # Identification: belief coordinate ~ Phi.
    L_bio = sp.Rational(1, 2) * Phi_dot**2 - sp.Rational(1, 2) * Lambda * (Phi - Phi_0) ** 2

    # 1D effective Lagrangian density from
    # S = ∫ [R + (1 + kappa*Phi) L_bio] dOmega.
    L_eff = R + (1 + kappa * Phi) * L_bio

    dL_dPhi = sp.diff(L_eff, Phi)
    dL_dPhidot = sp.diff(L_eff, Phi_dot)
    euler_lagrange = sp.simplify(sp.diff(dL_dPhidot, t) - dL_dPhi)

    print("Biological Lagrangian L_bio:")
    print(L_bio)
    print("\nEuler-Lagrange field equation (delta S / delta Phi = 0):")
    print(sp.Eq(euler_lagrange, 0))

    # Rearranged explicit second-order dynamics.
    phi_ddot_form = sp.simplify(sp.solve(sp.Eq(euler_lagrange, 0), Phi_ddot)[0])
    print("\nSecond-order dynamical form: ddot(Phi) = G(Phi, dot(Phi))")
    print(sp.Eq(Phi_ddot, phi_ddot_form))

    # Adiabatic reduction (slow-manifold closure): ddot(Phi) ≈ 0.
    adiabatic_eq = sp.simplify(sp.expand(euler_lagrange.subs(Phi_ddot, 0)))
    dot_phi_squared = sp.simplify(sp.solve(sp.Eq(adiabatic_eq, 0), Phi_dot**2)[0])

    F_plus = sp.simplify(sp.sqrt(dot_phi_squared))
    F_minus = sp.simplify(-sp.sqrt(dot_phi_squared))

    print("\nAdiabatic first-order closure (ddot(Phi) ≈ 0):")
    print(sp.Eq(Phi_dot, F_plus))
    print("or")
    print(sp.Eq(Phi_dot, F_minus))

    # Test whether alpha in dot(Phi) = -alpha*(Phi - Phi_0) can be written purely in
    # terms of (lambda, kappa).
    alpha = sp.symbols("alpha", real=True)
    alpha_required_sq = sp.simplify(dot_phi_squared / (Phi - Phi_0) ** 2)

    print("\nIf one enforces dot(Phi) = -alpha*(Phi - Phi_0), then")
    print(sp.Eq(alpha**2, alpha_required_sq))

    has_phi = (Phi in alpha_required_sq.free_symbols) or (Phi_0 in alpha_required_sq.free_symbols)
    conclusion = (
        "alpha is not identifiable purely from (lambda, kappa); it also depends on Phi and Phi_0 "
        "under this action-level closure."
        if has_phi
        else "alpha can be written purely in terms of (lambda, kappa)."
    )
    print("\nConclusion:")
    print(conclusion)


if __name__ == "__main__":
    main()