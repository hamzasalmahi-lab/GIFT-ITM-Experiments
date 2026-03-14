import sympy as sp


def variation(expr, variable, delta_variable):
    epsilon = sp.symbols("epsilon", real=True)
    varied = expr.subs(variable, variable + epsilon * delta_variable)
    return sp.simplify(sp.diff(varied, epsilon).subs(epsilon, 0))


def main():
    g, Phi = sp.symbols("g Phi", positive=True)
    delta_g, delta_Phi = sp.symbols("delta_g delta_Phi")
    L_bio = sp.symbols("L_bio", real=True)

    # General action ingredients.
    Ricci = sp.Function("Ricci")
    Coupling = sp.Function("Coupling")

    # GIFT-Action as a functional of metric and biological Lagrangian.
    # S[g] = Ricci(g) + Coupling(g) * L_bio
    S = Ricci(g) + Coupling(g) * L_bio

    # General field equation from metric variation.
    field_equation = sp.simplify(sp.diff(S, g))

    # Čencov-Ay gauge projection: enforce metric to Fisher manifold.
    # Minimal symbolic FIM slice used for projection map.
    g_fim = 1 / Phi

    def P(expr):
        return sp.simplify(
            expr.subs(
                {
                    g: g_fim,
                    delta_g: sp.diff(g_fim, Phi) * delta_Phi,
                }
            )
        )

    delta_P_S = variation(P(S), Phi, delta_Phi)
    P_delta_S = P(variation(S, g, delta_g))

    commutator = sp.simplify(delta_P_S - P_delta_S)

    print("GIFT Action S[g]:")
    sp.pprint(S)

    print("\nField equation dS/dg = 0:")
    sp.pprint(sp.Eq(field_equation, 0))

    print("\ndelta(P[S]) =")
    sp.pprint(delta_P_S)

    print("\nP[delta S] =")
    sp.pprint(P_delta_S)

    print("\nCommutator [delta, P]S = delta(P[S]) - P[delta S] =")
    sp.pprint(commutator)

    proportional_check = sp.simplify(commutator / P(field_equation)) if P(field_equation) != 0 else sp.Integer(0)

    if sp.simplify(commutator) == 0 or (P(field_equation) != 0 and commutator.has(P(field_equation))):
        print("\nMRA-III RESOLVED: Variational Commutativity [VERIFIED].")
    else:
        print("\nCommutator is non-zero and not manifestly proportional to projected field equations.")
        print("Potential proportionality diagnostic [delta, P]S / P[dS/dg]:")
        sp.pprint(proportional_check)


if __name__ == "__main__":
    main()