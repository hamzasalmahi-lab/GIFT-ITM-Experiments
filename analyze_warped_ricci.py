from sympy import Eq, cancel, diff, factor, simplify, symbols
from einsteinpy.symbolic import MetricTensor, RicciScalar


def build_symbols():
    t, h, s, r, Phi_voi = symbols("t h s r Phi_voi", positive=True)
    n, epsilon, lambda_symbol, Phi_0 = symbols(
        "n epsilon lambda Phi_0", real=True
    )
    return (t, h, s, r, Phi_voi), n, epsilon, lambda_symbol, Phi_0


def build_metric():
    coords, n, epsilon, _, _ = build_symbols()
    Phi_voi = coords[-1]
    warp_factor = Phi_voi**n

    metric_list = [
        [1, 0, 0, 0, 0],
        [0, warp_factor, 0, 0, epsilon * warp_factor],
        [0, 0, warp_factor, 0, 0],
        [0, 0, 0, warp_factor, 0],
        [0, epsilon * warp_factor, 0, 0, 1],
    ]

    return MetricTensor(metric_list, list(coords))


def compute_full_ricci_scalar():
    metric = build_metric()
    ricci = RicciScalar.from_metric(metric)
    return factor(simplify(ricci.expr))


def compute_matching_data():
    coords, n, epsilon, lambda_symbol, Phi_0 = build_symbols()
    Phi_voi = coords[-1]
    ricci_scalar = compute_full_ricci_scalar()

    zero_order_condition = Eq(
        epsilon**2 * Phi_0**n * (n - 2),
        2 * (n - 1),
    )

    lambda_general = Eq(
        lambda_symbol,
        simplify(diff(ricci_scalar, Phi_voi).subs(Phi_voi, Phi_0) / 2),
    )

    matching_substitution = {
        epsilon**2: simplify(2 * (n - 1) / ((n - 2) * Phi_0**n))
    }
    lambda_reduced = Eq(
        lambda_symbol,
        factor(simplify(lambda_general.rhs.subs(matching_substitution))),
    )

    return {
        "ricci_scalar": ricci_scalar,
        "zero_order_condition": zero_order_condition,
        "lambda_general": lambda_general,
        "lambda_reduced": lambda_reduced,
        "matching_substitution": matching_substitution,
    }


def compute_warp_error():
    coords, n, _, _, Phi_0 = build_symbols()
    Phi_voi = coords[-1]
    matching_data = compute_matching_data()

    warp_error = factor(
        cancel(
            simplify(
                (
                    matching_data["ricci_scalar"]
                    - 2 * matching_data["lambda_reduced"].rhs * (Phi_voi - Phi_0)
                ).subs(matching_data["matching_substitution"])
            )
        )
    )

    leading_error = simplify(
        -3
        * (n - 2) ** 2
        * (n - 1)
        * (7 * n - 3)
        * (Phi_voi - Phi_0) ** 2
        / (2 * Phi_0**4)
    )

    return warp_error, leading_error


def main():
    coords, n, epsilon, _, Phi_0 = build_symbols()
    Phi_voi = coords[-1]
    metric = build_metric()
    matching_data = compute_matching_data()
    warp_error, leading_error = compute_warp_error()

    print("Coordinates:", coords)
    print("Metric tensor:")
    print(metric.tensor())
    print()
    print("Full 5D Ricci scalar:")
    print(matching_data["ricci_scalar"])
    print()
    print("First-order reduction conditions for R = 2*lambda*(Phi_voi - Phi_0):")
    print("1.", matching_data["zero_order_condition"])
    print("2.", matching_data["lambda_general"])
    print("3. Under condition 1:", matching_data["lambda_reduced"])
    print()
    print("Regularity requires epsilon**2*Phi_voi**n != 1.")
    print("Positive-definite (Riemannian) background at Phi_0 requires:")
    print("   Phi_0 > 0 and 0 < epsilon**2*Phi_0**n < 1.")
    print(
        "   Combined with condition 1, this restricts the matched Riemannian branch to 0 < n < 1."
    )
    print()
    print("Exact warp error term E_warp = R - 2*lambda*(Phi_voi - Phi_0):")
    print(warp_error)
    print()
    print("Leading warp error near Phi_0:")
    print(leading_error)


if __name__ == "__main__":
    main()