# GIFT-ITM-Experiments
GIFT Math Experimentations 

## Repository Organization

- Conceptual audit and reviewer-response structure: `docs/REVISION_STRATEGY.md`
- Symbolic audits and derivations:
	- `audit_threshold.py`
	- `derive_mrai_variation.py`
	- `derive_slow_manifold.py`
	- `gauge_commutation_test.py`
	- `hierarchical_metric_induction.py`
- Numerical experiments and simulation:
	- `simulate_dpdr.py`
	- `optimize_unified_parameters.py`
	- `simulate_transduction_probability.py`
- Geometric curvature analysis:
	- `calc_ricci.py`
	- `analyze_warped_ricci.py`
- Tests: `tests/`
- Generated figures: `artifacts/`

## Setup

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run all tests:

```bash
python3 -m unittest discover -s tests
```

## Mandatory Mathematical Corrections

### 1) Algebraic Sign Correction (Major Concern 4)

Run the symbolic derivation:

```bash
python3 audit_threshold.py
```

Expected result:

```text
The mathematically [PROVED] threshold is: Phi_th = L_bio*kappa/(2*lambda) + Phi_0
```

### 2) Threshold Disambiguation (Major Concern 3)

Run the global consistency optimization:

```bash
python3 optimize_unified_parameters.py
```

If no coherent unified solution exists, the script writes:

```text
artifacts/incoherence_gap.png
```

## Master Research Agenda (MRA)

### MRA-I: IFE–ODE Integration Bridge

Run the action-level variational bridge derivation:

```bash
python3 derive_mrai_variation.py
```

Run the explicit slow-manifold reduction:

```bash
python3 derive_slow_manifold.py
```

### MRA-III: Commutation Problem

Run the symbolic gauge commutator test for the GIFT action:

```bash
python3 gauge_commutation_test.py
```

### MRA-IV: Transduction Map Derivation

Run the Monte Carlo transducer simulation and sigmoid fit:

```bash
python3 simulate_transduction_probability.py
```

The script writes:

```text
artifacts/transduction_probability_fit.png
```

### MRA-VI: Hierarchical Scaling & Theorem 2

Run hierarchical curvature induction and additivity check:

```bash
python3 hierarchical_metric_induction.py
```

## Supporting Geometry/Numerics

Run the ODE simulation:

```bash
python3 simulate_dpdr.py
```

If you are running in a headless environment:

```bash
MPLBACKEND=Agg python3 simulate_dpdr.py
```

Run the symbolic Ricci scalar calculation:

```bash
python3 calc_ricci.py
```

Run the warped-metric Ricci analysis:

```bash
python3 analyze_warped_ricci.py
```

Generate Figure 1 (the \((\Phi_{voi}, H)\) curvature landscape):

```bash
python3 scripts/figures/plot_curvature_landscape.py
```

The script writes:

```text
artifacts/figure1_curvature_landscape.png
```

Generate Figure 2 (the modified tuning curve):

```bash
python3 scripts/figures/plot_modified_tuning_curve.py
```

The script writes:

```text
artifacts/figure2_modified_tuning_curve.png
```

Generate Figure 3 (the HST metastability landscape):

```bash
python3 scripts/figures/plot_hst_metastability_landscape.py
```

The script writes:

```text
artifacts/figure3_hst_metastability_landscape.png
```

Generate Figure 4 (the HST architecture):

```bash
python3 scripts/figures/plot_hst_architecture.py
```

The script writes:

```text
artifacts/figure4_hst_architecture.png
```

Generate Figure 5 (the \(\alpha(\Phi)\) domain map):

```bash
python3 scripts/figures/plot_alpha_domain_map.py
```

The script writes:

```text
artifacts/figure5_alpha_domain_map.png
```

## Verification

Core regression suite:

```bash
python3 -m unittest discover -s tests
```
