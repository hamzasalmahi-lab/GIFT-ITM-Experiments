import unittest

from sympy import Eq, cancel, simplify 

from analyze_warped_ricci import (
    build_symbols,
    compute_full_ricci_scalar,
    compute_matching_data,
    compute_warp_error,
)


class AnalyzeWarpedRicciTest(unittest.TestCase):
    def test_full_ricci_scalar_matches_closed_form(self):
        coords, n, epsilon, _, _ = build_symbols()
        Phi_voi = coords[-1]

        expected = (
            3
            * n
            * (epsilon**2 * n * Phi_voi**n - 2 * epsilon**2 * Phi_voi**n - 2 * n + 2)
            / (2 * Phi_voi**2 * (epsilon**2 * Phi_voi**n - 1) ** 2)
        )

        self.assertEqual(cancel(simplify(compute_full_ricci_scalar() - expected)), 0)

    def test_matching_conditions_and_leading_warp_error(self):
        coords, n, epsilon, lambda_symbol, Phi_0 = build_symbols()
        Phi_voi = coords[-1]
        matching_data = compute_matching_data()
        _, leading_error = compute_warp_error()

        self.assertEqual(
            matching_data["zero_order_condition"],
            Eq(Phi_0**n * epsilon**2 * (n - 2), 2 * (n - 1)),
        )
        self.assertEqual(
            matching_data["lambda_reduced"],
            Eq(
                lambda_symbol,
                3 * (n - 2) ** 2 * (n - 1) / (2 * Phi_0**3),
            ),
        )
        expected_leading_error = (
            -3
            * (n - 2) ** 2
            * (n - 1)
            * (7 * n - 3)
            * (Phi_voi - Phi_0) ** 2
            / (2 * Phi_0**4)
        )
        self.assertEqual(simplify(leading_error - expected_leading_error), 0)


if __name__ == "__main__":
    unittest.main()