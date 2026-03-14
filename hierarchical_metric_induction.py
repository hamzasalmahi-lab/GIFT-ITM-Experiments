import sympy as sp
from einsteinpy.symbolic import MetricTensor, RicciScalar


def build_metric(L):
    if L < 1:
        raise ValueError("L must be >= 1")

    coordinates = []
    phi_symbols = []
    for index in range(1, L + 1):
        h_i, phi_i = sp.symbols(f"h_{index} Phi_{index}", positive=True)
        coordinates.extend([h_i, phi_i])
        phi_symbols.append(phi_i)

    size = 2 * L
    metric_matrix = [[sp.Integer(0) for _ in range(size)] for _ in range(size)]

    for index, phi_i in enumerate(phi_symbols):
        row = 2 * index
        metric_matrix[row][row] = 1 / phi_i
        metric_matrix[row + 1][row + 1] = 1 / phi_i**2

    return MetricTensor(metric_matrix, coordinates), phi_symbols


def get_ricci(L):
    metric, _ = build_metric(L)
    ricci = RicciScalar.from_metric(metric)
    return sp.simplify(ricci.expr)


def get_layer_curvature():
    h, phi = sp.symbols("h Phi", positive=True)
    metric = MetricTensor([[1 / phi, 0], [0, 1 / phi**2]], [h, phi])
    ricci = RicciScalar.from_metric(metric)
    return sp.simplify(ricci.expr)


def main():
    print("Hierarchical Metric Induction for block metrics g_i = diag(1/Phi_i, 1/Phi_i^2)")

    layer_curvature = get_layer_curvature()
    print("\nSingle-layer curvature R_i:")
    sp.pprint(layer_curvature)

    results = {}
    for L in (1, 2, 3):
        total_curvature = get_ricci(L)
        linear_sum = sp.simplify(L * layer_curvature)
        residual = sp.simplify(total_curvature - linear_sum)

        results[L] = total_curvature

        print(f"\nL = {L}")
        print("R_total =")
        sp.pprint(total_curvature)
        print("Sum_i R_i =")
        sp.pprint(linear_sum)
        print("Residual R_total - Sum_i R_i =")
        sp.pprint(residual)

    L_symbol = sp.symbols("L", integer=True, positive=True)
    pattern = sp.simplify(L_symbol * layer_curvature)
    print("\nPattern from L = 1,2,3:")
    print("R_total(L) = L * R_i =")
    sp.pprint(pattern)

    print("\nUniversal Coupling depth-invariance statement:")
    print("For this block-diagonal hierarchical metric, mixed Christoffel symbols vanish,")
    print("the Ricci tensor is blockwise additive, and therefore the Ricci scalar is linear")
    print("in hierarchical depth: R_total = sum_i R_i = L * R_i.")


if __name__ == "__main__":
    main()