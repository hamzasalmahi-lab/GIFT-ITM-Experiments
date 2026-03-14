import unittest

from sympy import symbols

from calc_ricci import compute_ricci_scalar


class CalcRicciTest(unittest.TestCase):
    def test_compute_ricci_scalar_matches_expected_expression(self):
        phi = symbols('phi')
        expected = -13 / (2 * phi**2)

        self.assertEqual(compute_ricci_scalar(), expected)


if __name__ == "__main__":
    unittest.main()